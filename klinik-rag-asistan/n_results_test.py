import time
from rag_sorgula import ilgili_chunklari_bul

# Test sorulari - farkli senaryolari kapsayan kucuk bir set
TEST_SORULARI = [
    "Warfarin kullanan bir hastaya ibuprofen verilirse ne olur?",
    "Metformin ve glimepirid birlikte kullanilabilir mi?",
    "Ibuprofen icin yetiskinlerde onerilen gunluk maksimum doz nedir?",
    "Warfarin hangi durumlarda kesinlikle kullanilmamali?",
    "Parasetamol ile amoksisilin birlikte kullanilabilir mi?",  # kapsam disi - halusinasyon testi
]

N_RESULTS_DEGERLERI = [3, 5, 7]


def analiz_et(soru, n):
    baslangic = time.time()
    chunklar = ilgili_chunklari_bul(soru, n_results=n)
    sure = time.time() - baslangic

    ilaclar = [c["ilac"] for c in chunklar]
    benzersiz_ilac_sayisi = len(set(ilaclar))

    return {
        "sure": round(sure, 2),
        "chunk_sayisi": len(chunklar),
        "benzersiz_ilac": benzersiz_ilac_sayisi,
        "ilaclar": ilaclar,
    }


def main():
    print(f"{'='*80}")
    print("N_RESULTS KARSILASTIRMA TESTI")
    print(f"{'='*80}\n")

    for soru in TEST_SORULARI:
        print(f"\nSORU: {soru}")
        print("-" * 80)
        for n in N_RESULTS_DEGERLERI:
            sonuc = analiz_et(soru, n)
            print(f"  n_results={n}: "
                  f"sure={sonuc['sure']}s, "
                  f"chunk={sonuc['chunk_sayisi']}, "
                  f"benzersiz_ilac={sonuc['benzersiz_ilac']}, "
                  f"ilaclar={sonuc['ilaclar']}")
        print()

    print(f"\n{'='*80}")
    print("Test tamamlandi. Yukaridaki sonuclari inceleyerek:")
    print("- Hangi n_results degerinde alakali ilaclarin hepsi yakalaniyor?")
    print("- n_results arttikca sure ne kadar artiyor?")
    print("- Coklu ilac sorularinda (ornek: metformin+glimepirid) kac tanesi")
    print("  n=3'te bulunuyor, n=5 veya 7 gerekiyor mu?")
    print(f"{'='*80}")



def router_testi():
    print(f"\n{'='*80}")
    print("ROUTER TESTI (coklu ilac tespiti)")
    print(f"{'='*80}\n")

    sorular = [
        "Metformin ve glimepirid birlikte kullanilabilir mi?",
        "Warfarin kullanan bir hastaya ibuprofen verilirse ne olur?",
        "Ibuprofen icin gunluk maksimum doz nedir?",  # tek ilac
    ]

    for soru in sorular:
        chunklar = ilgili_chunklari_bul(soru)
        ilaclar = [c["ilac"] for c in chunklar]
        benzersiz = set(ilaclar)
        print(f"SORU: {soru}")
        print(f"  Toplam chunk: {len(chunklar)}, Benzersiz ilac: {len(benzersiz)}")
        print(f"  Ilaclar: {ilaclar}\n")


if __name__ == "__main__":
    main()
    router_testi()