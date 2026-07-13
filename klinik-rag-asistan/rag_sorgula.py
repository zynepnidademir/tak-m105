import os
import time
import httpx
import chromadb
import hashlib
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY ortam degiskeni bulunamadi!")

client_genai = genai.Client(api_key=API_KEY)

_BU_DOSYANIN_KLASORU = os.path.dirname(os.path.abspath(__file__))
client = chromadb.PersistentClient(path=os.path.join(_BU_DOSYANIN_KLASORU, "chroma_db"))
koleksiyon = client.get_collection("ilac_kub_koleksiyonu")

EMBEDDING_MODEL = "models/gemini-embedding-001"
LLM_MODEL = "gemini-3.5-flash"

SISTEM_PROMPTU = """Sen, hekimlere yönelik bir Klinik Karar Destek Sistemi'nde çalışan bir klinik asistansın.
Yalnizca sana asagida DOKUMANLAR bolumunde verilen KUB (Kisa Urun Bilgisi) belgelerindeki
bilgilere sadik kalarak cevap ver. Bu belgelerde yer almayan hicbir tibbi bilgiyi kendi
bilgine dayanarak EKLEME, TAHMIN ETME veya GENELLEME YAPMA.

CEVABINI HER ZAMAN ASAGIDAKI BASLIKLARLA, TAM OLARAK BU SIRAYLA VER:

**OZET:**
[Soruya 1-2 cumlelik dogrudan yanit]

**BULGULAR:**
- [Dokumanlardan cikarilan her ilgili bulguyu ayri bir madde olarak yaz. Sayisal
  degerleri (doz, INR, eGFR, potasyum vb.) SADECE dokumanda veya soruda acikca
  belirtilmisse kullan; hicbir sayiyi tahmin etme veya yuvarlama.]
- [Birden fazla ilac/dokuman ilgiliyse her birinin bulgusunu ayri maddede ver;
  dokumanlar arasinda celiski varsa bunu acikca belirt.]

**RISK SEVIYESI:** [Dusuk / Orta / Yuksek / Belirsiz]
[Bu seviyeyi neye dayanarak verdigini tek cumlede gerekcelendir. Dokumanda acik bir
onem derecesi belirtilmemisse ve dokuman icerigiyle net bir cikarim yapilamiyorsa
"Belirsiz" yaz. Risk seviyesini kaynaksiz/dokumansiz asla uydurma.]

**KAYNAKLAR:**
- [Ilac adi] (Sayfa [ilk]-[son])
[SADECE DOKUMANLAR bolumunde sana fiilen verilen kaynaklari listele; kullanmadigin
veya sana verilmeyen bir kaynak ismi ya da sayfa numarasi asla uydurma.]

KURALLAR:
- Dokumanlarda soruyu cevaplayacak yeterli bilgi yoksa BULGULAR bolumune "Yeterli
  klinik veri bulunamadi" yaz ve RISK SEVIYESI'ni "Belirsiz" olarak isaretle.
- Soru belirsiz veya hastaya ozgu yeterli bilgi icermiyorsa (ornek: "Bu hastaya
  hangi ilaci verebilirim?"), OZET bolumunde bunu belirt ve hangi ek bilgilerin
  (tani, kullanilan diger ilaclar, laboratuvar degerleri vb.) gerekli oldugunu sor;
  bu durumda BULGULAR ve KAYNAKLAR bolumlerini bos birakabilirsin.
- Bu bir tibbi tavsiye degil, dokuman ozeti ve karar destek bilgisidir; nihai karar
  her zaman hekime aittir. Cevabin en altina, ayri bir satirda sadece su ifadeyi ekle:
  "Bu bilgi dokuman ozetidir, tibbi tavsiye degildir; nihai karar hekime aittir."
- Turkce ve acik, anlasilir bir dille cevap ver. Yukaridaki basliklari degistirme,
  cevirme veya kaldirma.
"""


def _yeniden_denemeli_cagri(fonksiyon, max_deneme=8):
    """Rate limit veya baglanti hatasinda bekleyip tekrar dener."""
    bekleme = 3
    son_hata = None
    for deneme in range(max_deneme):
        try:
            return fonksiyon()
        except (ClientError, ServerError) as e:
            son_hata = e
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e) or "UNAVAILABLE" in str(e) or "503" in str(e):
                print(f"[RETRY {deneme+1}/{max_deneme}] {type(e).__name__}: {e}")
                time.sleep(bekleme)
                bekleme = min(bekleme * 2, 60)
            else:
                raise
        except (httpx.ConnectError, httpx.ReadTimeout, httpx.ConnectTimeout) as e:
            son_hata = e
            print(f"[RETRY {deneme+1}/{max_deneme}] {type(e).__name__}: {e}")
            time.sleep(bekleme)
            bekleme = min(bekleme * 2, 60)
    raise RuntimeError(
        f"Baglanti veya kota sorunu devam ediyor. Son hata: {type(son_hata).__name__}: {son_hata}"
    )


def embed_sorgu(metin):
    def cagri():
        sonuc = client_genai.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=metin,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
        )
        return sonuc.embeddings[0].values
    return _yeniden_denemeli_cagri(cagri)


# Veri setimizdeki ilaclarin anahtar kelimeleri -> ChromaDB'deki "ilac" metadata degeri
_ILAC_ANAHTAR_KELIMELERI = {
    "Varfarin (Warfmadin 5mg)": ["warfarin", "warfmadin", "kumadin"],
    "Ibuprofen (Artril 600mg)": ["ibuprofen", "artril"],
    "Glimepirid (Amaryl 2mg)": ["glimepirid", "amaryl"],
    "Metformin (Atamet 1000mg)": ["metformin", "atamet"],
}


def _soruda_gecen_ilaclar(soru):
    """Soru metninde veri setimizdeki hangi ilaclarin gectigini tespit eder."""
    soru_lower = soru.lower()
    bulunanlar = []
    for ilac_adi, anahtarlar in _ILAC_ANAHTAR_KELIMELERI.items():
        if any(anahtar in soru_lower for anahtar in anahtarlar):
            bulunanlar.append(ilac_adi)
    return bulunanlar


def _ilac_bazli_chunk_bul(soru, ilac_listesi, ilac_basina_sonuc=4):
    """Birden fazla ilac tespit edildiginde, her ilac icin ayri ayri
    retrieval yapip sonuclari birlestirir. Boylece hicbir ilac
    diger(ler)inin golgesinde kalip kaybolmaz."""
    soru_embedding = embed_sorgu(soru)

    tum_chunklar = []
    for ilac_adi in ilac_listesi:
        sonuclar = koleksiyon.query(
            query_embeddings=[soru_embedding],
            n_results=ilac_basina_sonuc,
            where={"ilac": ilac_adi},
        )
        for i in range(len(sonuclar["ids"][0])):
            tum_chunklar.append({
                "metin": sonuclar["documents"][0][i],
                "ilac": sonuclar["metadatas"][0][i]["ilac"],
                "dosya": sonuclar["metadatas"][0][i]["dosya"],
                "ilk_sayfa": sonuclar["metadatas"][0][i]["ilk_sayfa"],
                "son_sayfa": sonuclar["metadatas"][0][i]["son_sayfa"],
            })
    return tum_chunklar















def ilgili_chunklari_bul(soru, n_results=5):

    # Router: soruda birden fazla ilac geciyorsa, her ilac icin ayri
    # retrieval yaparak hicbirinin gozden kacmamasini garanti altina al
    ilaclar = _soruda_gecen_ilaclar(soru)
    if len(ilaclar) >= 2:
        return _ilac_bazli_chunk_bul(soru, ilaclar)
    
    soru_embedding = embed_sorgu(soru)
    sonuclar = koleksiyon.query(
        query_embeddings=[soru_embedding],
        n_results=n_results,
    )

    chunklar = []
    for i in range(len(sonuclar["ids"][0])):
        chunklar.append({
            "metin": sonuclar["documents"][0][i],
            "ilac": sonuclar["metadatas"][0][i]["ilac"],
	    "dosya": sonuclar["metadatas"][0][i]["dosya"],
            "ilk_sayfa": sonuclar["metadatas"][0][i]["ilk_sayfa"],
            "son_sayfa": sonuclar["metadatas"][0][i]["son_sayfa"],
        })
    return chunklar


def baglam_olustur(chunklar):
    parcalar = []
    for i, c in enumerate(chunklar, start=1):
        parcalar.append(
            f"[Kaynak {i} - {c['ilac']}, Sayfa {c['ilk_sayfa']}-{c['son_sayfa']}]\n{c['metin']}"
        )
    return "\n\n---\n\n".join(parcalar)


def cevap_uret(soru, chunklar):
    baglam = baglam_olustur(chunklar)

    prompt = f"""{SISTEM_PROMPTU}

DOKUMANLAR:
{baglam}

SORU: {soru}

CEVAP:"""

    def cagri():
        sonuc = client_genai.models.generate_content(
            model=LLM_MODEL,
            contents=prompt,
        )
        return sonuc.text

    return _yeniden_denemeli_cagri(cagri)


def sorgula(soru):
    print(f"\n{'='*60}")
    print(f"SORU: {soru}")
    print('='*60)

    chunklar = ilgili_chunklari_bul(soru)

    print(f"\n[Bulunan {len(chunklar)} ilgili kaynak:]")
    for c in chunklar:
        print(f"  - {c['ilac']} (sayfa {c['ilk_sayfa']}-{c['son_sayfa']})")

    cevap = cevap_uret(soru, chunklar)

    print(f"\n[CEVAP]\n{cevap}")
    return cevap

import json
import re


def _ilac_dosya_haritasi():
    return {
        "Varfarin (Warfmadin 5mg)": "Warfmadin 5mg KÜB",
        "Ibuprofen (Artril 600mg)": "Artril 600mg KÜB",
        "Glimepirid (Amaryl 2mg)": "Amaryl 2mg KÜB",
        "Metformin (Atamet 1000mg)": "Atamet 1000mg KÜB",
    }

def _cache_anahtari(soru):
    return hashlib.md5(soru.strip().lower().encode("utf-8")).hexdigest()


def _cache_klasoru():
    bu_klasor = os.path.dirname(os.path.abspath(__file__))
    klasor = os.path.join(bu_klasor, "cache")
    os.makedirs(klasor, exist_ok=True)
    return klasor


def _cacheden_oku(soru):
    yol = os.path.join(_cache_klasoru(), _cache_anahtari(soru) + ".json")
    if os.path.exists(yol):
        with open(yol, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _cachee_yaz(soru, rapor):
    yol = os.path.join(_cache_klasoru(), _cache_anahtari(soru) + ".json")
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(rapor, f, ensure_ascii=False, indent=2)








def analiz_uret(soru):
    """
    Gercek retrieval + LLM kullanarak, dashboard arayuzunun bekledigi
    yapilandirilmis (JSON) klinik rapor formatinda cevap uretir.
    Referanslar LLM'e degil, dogrudan retrieval sonucuna dayanir.
    """

    onbellek = _cacheden_oku(soru)
    if onbellek is not None:
        return onbellek
    
    chunklar = ilgili_chunklari_bul(soru, n_results=5)
    baglam = baglam_olustur(chunklar)

    analiz_promptu = f"""{SISTEM_PROMPTU}

DOKUMANLAR:
{baglam}

SORU: {soru}

Yukaridaki dokumanlara dayanarak, asagidaki JSON formatinda BIR CEVAP ver.
Baska hicbir metin ekleme, sadece gecerli JSON dondur:

{{
  "risk": "high" veya "moderate" veya "low" veya "unknown",
  "risk_label": "kisa risk etiketi (orn. 'Ciddi Risk / Kanama Artisi')",
  "title": "raporun kisa basligi",
  "summary": ["madde 1", "madde 2", "madde 3"],
  "mechanism": "etkilesim mekanizmasinin kisa aciklamasi",
  "recommendation": "hekime yonelik oneri metni"
}}

Eger dokumanlarda yeterli bilgi yoksa risk alanini "unknown" yap ve
diger alanlarda "Yeterli klinik veri bulunamadi" ifadesini kullan.
"""

    def cagri():
        sonuc = client_genai.models.generate_content(
            model=LLM_MODEL,
            contents=analiz_promptu,
        )
        return sonuc.text

    ham_cevap = _yeniden_denemeli_cagri(cagri)

    # Ilk { ile son } arasindaki her seyi al - kod bloklarindan bagimsiz calisir
    ilk_parantez = ham_cevap.find("{")
    son_parantez = ham_cevap.rfind("}")

    if ilk_parantez != -1 and son_parantez != -1:
        temiz = ham_cevap[ilk_parantez:son_parantez + 1]
    else:
        temiz = ham_cevap.strip()

    try:
        rapor = json.loads(temiz)

    except json.JSONDecodeError:
        rapor = {
            "risk": "unknown",
            "risk_label": "Analiz Hatasi",
            "title": f"'{soru}' Sorgusu",
            "summary": ["Cevap yapilandirilamadi, ham cevap:", ham_cevap[:500]],
            "mechanism": "",
            "recommendation": "",
        }

    dosya_haritasi = _ilac_dosya_haritasi()
    referanslar = []
    for c in chunklar:
        referanslar.append({
            "doc_name": dosya_haritasi.get(c["ilac"], c["ilac"]),
            "chapter_page": f"Sayfa {c['ilk_sayfa']}-{c['son_sayfa']}",
            "snippet": c["metin"][:220].strip() + "...",
            "doc_id": c["dosya"].replace(".txt", "").upper(),
        })
    
     # LLM bazen summary'yi liste yerine tek string dondurebilir, garanti altina alalim
    if isinstance(rapor.get("summary"), str):
        rapor["summary"] = [rapor["summary"]]
    elif not isinstance(rapor.get("summary"), list):
        rapor["summary"] = [str(rapor.get("summary", ""))]

    rapor["references"] = referanslar

    _cachee_yaz(soru, rapor)
    return rapor


if __name__ == "__main__":
    sorgula("Warfarin kullanan bir hastaya ibuprofen verilirse ne olur?")