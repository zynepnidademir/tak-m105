import os
import re
import json

KAYNAK_KLASOR = "data/ilaclar_metin"
HEDEF_DOSYA = "data/chunks.json"

CHUNK_SIZE = 1200
OVERLAP = 250
ILAC_ADLARI = {
    "atamet": "Metformin (Atamet 1000mg)",
    "glimepirid": "Glimepirid (Amaryl 2mg)",
    "ibuprofen2": "Ibuprofen (Artril 600mg)",
    "warfmadin5mgtabletpdf": "Varfarin (Warfmadin 5mg)",
    "delix": "DELIX PLUS (5mg/25mg)",
    "plavix": "PLAVIX (75mg)",
    "lipitor": "LIPITOR (20mg)",
    "norvasc": "NORVASC (5mg)",
    "Beloc": "BELOC ZOK (50mg)"
}

def ilac_adi_bul(dosya_adi):
    # Dosya adını küçük harfe çeviriyoruz
    anahtar = dosya_adi.lower().replace(".txt", "")
    
    for parca, ad in ILAC_ADLARI.items():
        # Sözlükteki anahtarı (parca) da küçük harfe çevirerek arıyoruz
        if parca.lower() in anahtar: 
            return ad
            
    return dosya_adi.replace(".txt", "")

def sayfalara_ayir(icerik):
    parcalar = re.split(r"\[SAYFA (\d+)\]", icerik)
    sayfalar = []
    for i in range(1, len(parcalar), 2):
        sayfa_no = int(parcalar[i])
        metin = parcalar[i + 1]
        sayfalar.append((sayfa_no, metin))
    return sayfalar


def chunkla(sayfalar, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    tam_metin = ""
    pozisyon_sayfa_haritasi = []

    for sayfa_no, metin in sayfalar:
        tam_metin += metin
        pozisyon_sayfa_haritasi.extend([sayfa_no] * len(metin))

    chunklar = []
    baslangic = 0
    while baslangic < len(tam_metin):
        bitis = min(baslangic + chunk_size, len(tam_metin))
        parca_metin = tam_metin[baslangic:bitis].strip()

        if parca_metin:
            ilgili_sayfalar = pozisyon_sayfa_haritasi[baslangic:bitis]
            if ilgili_sayfalar:
                ilk_sayfa = min(ilgili_sayfalar)
                son_sayfa = max(ilgili_sayfalar)
            else:
                ilk_sayfa = son_sayfa = None

            chunklar.append({
                "metin": parca_metin,
                "ilk_sayfa": ilk_sayfa,
                "son_sayfa": son_sayfa,
            })

        if bitis == len(tam_metin):
            break
        baslangic += chunk_size - overlap

    return chunklar


def main():
    tum_chunklar = []
    chunk_id_sayaci = 0

    for dosya_adi in sorted(os.listdir(KAYNAK_KLASOR)):
        if not dosya_adi.endswith(".txt"):
            continue

        yol = os.path.join(KAYNAK_KLASOR, dosya_adi)
        with open(yol, "r", encoding="utf-8") as f:
            icerik = f.read()

        ilac_adi = ilac_adi_bul(dosya_adi)
        sayfalar = sayfalara_ayir(icerik)
        chunklar = chunkla(sayfalar)

        print(f"{dosya_adi} -> {ilac_adi}: {len(chunklar)} chunk uretildi")

        for chunk in chunklar:
            chunk_id_sayaci += 1
            tum_chunklar.append({
                "id": f"chunk_{chunk_id_sayaci}",
                "dosya": dosya_adi,
                "ilac": ilac_adi,
                "ilk_sayfa": chunk["ilk_sayfa"],
                "son_sayfa": chunk["son_sayfa"],
                "metin": chunk["metin"],
            })

    os.makedirs(os.path.dirname(HEDEF_DOSYA), exist_ok=True)
    with open(HEDEF_DOSYA, "w", encoding="utf-8") as f:
        json.dump(tum_chunklar, f, ensure_ascii=False, indent=2)

    print(f"\nToplam {len(tum_chunklar)} chunk '{HEDEF_DOSYA}' dosyasina kaydedildi.")


if __name__ == "__main__":
    main()