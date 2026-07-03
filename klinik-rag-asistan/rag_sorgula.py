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

SISTEM_PROMPTU = """Sen profesyonel bir klinik asistansın. Yalnizca sana asagida verilen
KUB (Kisa Urun Bilgisi) dokumanlarindaki bilgilere sadik kalarak cevap ver.

KURALLAR:
- Eger dokumanlarda soruyu cevaplayacak bilgi yoksa kesinlikle tahmin yurutme,
  "Yeterli klinik veri bulunamadi" de.
- Cevabinin sonunda mutlaka hangi ilactan ve hangi sayfadan bilgi aldigini belirt.
- Ilac etkilesimi sorularinda, riski acikca belirt (dusuk/orta/yuksek gibi bir
  degerlendirme dokumanda varsa onu kullan; yoksa sadece dokumandaki ifadeyi aktar).
- Tibbi tavsiye degil, dokuman ozeti sundugunu unutma; nihai karar hekime aittir.
- Cevabinin en sonuna, ayri bir satirda, sadece su ifadeyi ekle: "Bu bilgi
  dokuman ozetidir, tibbi tavsiye degildir; nihai karar hekime aittir."
- Turkce ve acik, anlasilir bir dille cevap ver.
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