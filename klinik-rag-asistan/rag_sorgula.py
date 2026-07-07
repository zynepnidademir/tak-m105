import os
import time
import httpx
import chromadb
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY ortam degiskeni bulunamadi!")

client_genai = genai.Client(api_key=API_KEY)

client = chromadb.PersistentClient(path="chroma_db")
koleksiyon = client.get_collection("ilac_kub_koleksiyonu")

EMBEDDING_MODEL = "models/gemini-embedding-001"
LLM_MODEL = "gemini-2.5-flash"

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


def _yeniden_denemeli_cagri(fonksiyon, max_deneme=6):
    """Rate limit veya baglanti hatasinda bekleyip tekrar dener."""
    bekleme = 3
    for deneme in range(max_deneme):
        try:
            return fonksiyon()
        except (ClientError, ServerError) as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e) or "UNAVAILABLE" in str(e) or "503" in str(e):
                time.sleep(bekleme)
                bekleme = min(bekleme * 2, 30)
            else:
                raise
        except (httpx.ConnectError, httpx.ReadTimeout, httpx.ConnectTimeout):
            time.sleep(bekleme)
            bekleme = min(bekleme * 2, 30)
    raise RuntimeError("Baglanti veya kota sorunu devam ediyor, lutfen internetinizi kontrol edin.")


def embed_sorgu(metin):
    def cagri():
        sonuc = client_genai.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=metin,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
        )
        return sonuc.embeddings[0].values
    return _yeniden_denemeli_cagri(cagri)


def ilgili_chunklari_bul(soru, n_results=5):
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


if __name__ == "__main__":
    sorgula("Warfarin kullanan bir hastaya ibuprofen verilirse ne olur?")