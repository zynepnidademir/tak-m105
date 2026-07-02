import os
import chromadb
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY")
client_genai = genai.Client(api_key=API_KEY)

client = chromadb.PersistentClient(path="chroma_db")
koleksiyon = client.get_collection("ilac_kub_koleksiyonu")

soru = "Warfarin kullanan bir hastaya ibuprofen verilirse ne olur?"

sonuc = client_genai.models.embed_content(
    model="models/gemini-embedding-001",
    contents=soru,
    config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
)
soru_embedding = sonuc.embeddings[0].values

sonuclar = koleksiyon.query(
    query_embeddings=[soru_embedding],
    n_results=3,
)

print(f"SORU: {soru}\n")
for i in range(len(sonuclar["ids"][0])):
    meta = sonuclar["metadatas"][0][i]
    print(f"--- Sonuc {i+1} ---")
    print(f"Ilac: {meta['ilac']} | Sayfa: {meta['ilk_sayfa']}-{meta['son_sayfa']}")
    print(sonuclar["documents"][0][i][:300])
    print()