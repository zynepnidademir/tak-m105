import os
import json
import time
import chromadb
from google import genai
from google.genai import types
from google.genai.errors import ClientError

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY ortam degiskeni bulunamadi!")

client_genai = genai.Client(api_key=API_KEY)

CHUNKS_DOSYA = "data/chunks.json"
DB_KLASORU = "chroma_db"
KOLEKSIYON_ADI = "ilac_kub_koleksiyonu"

EMBEDDING_MODEL = "models/gemini-embedding-001"


def embed_metin(metin, gorev_tipi="RETRIEVAL_DOCUMENT", max_deneme=6):
    """Tek bir metni Gemini ile embed eder, rate limit'e takilirsa bekleyip tekrar dener."""
    bekleme = 5
    for deneme in range(max_deneme):
        try:
            sonuc = client_genai.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=metin,
                config=types.EmbedContentConfig(task_type=gorev_tipi),
            )
            return sonuc.embeddings[0].values
        except ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                print(f"  Rate limit'e takildi, {bekleme} saniye bekleniyor... (deneme {deneme + 1}/{max_deneme})")
                time.sleep(bekleme)
                bekleme = min(bekleme * 2, 60)  # ustel artis, max 60 sn
            else:
                raise
    raise RuntimeError("Cok fazla rate limit hatasi, script durduruldu.")


def main():
    with open(CHUNKS_DOSYA, "r", encoding="utf-8") as f:
        chunklar = json.load(f)

    print(f"{len(chunklar)} chunk toplamda var.")

    client = chromadb.PersistentClient(path=DB_KLASORU)
    koleksiyon = client.get_or_create_collection(name=KOLEKSIYON_ADI)

    # Zaten eklenmis olan ID'leri bul, onlari atla
    mevcut_idler = set(koleksiyon.get()["ids"])
    print(f"Koleksiyonda zaten {len(mevcut_idler)} chunk var, bunlar atlanacak.")

    kalan_chunklar = [c for c in chunklar if c["id"] not in mevcut_idler]
    print(f"{len(kalan_chunklar)} chunk kaldi.\n")

    for idx, chunk in enumerate(kalan_chunklar, start=1):
        print(f"[{idx}/{len(kalan_chunklar)}] Embedding: {chunk['id']} ({chunk['ilac']}, sayfa {chunk['ilk_sayfa']}-{chunk['son_sayfa']})")
        embedding = embed_metin(chunk["metin"])

        koleksiyon.add(
            ids=[chunk["id"]],
            documents=[chunk["metin"]],
            embeddings=[embedding],
            metadatas=[{
                "ilac": chunk["ilac"],
                "dosya": chunk["dosya"],
                "ilk_sayfa": chunk["ilk_sayfa"],
                "son_sayfa": chunk["son_sayfa"],
            }],
        )

        time.sleep(3)  # istekler arasi bekleme, rate limit'i tetiklememek icin

    print(f"\nTamamlandi! Toplam {koleksiyon.count()} chunk '{DB_KLASORU}' klasorune kaydedildi.")


if __name__ == "__main__":
    main()