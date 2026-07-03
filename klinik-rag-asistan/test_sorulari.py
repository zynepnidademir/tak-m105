from rag_sorgula import sorgula

TEST_SORULARI = [
    # 1. Basit ilaç etkileşimi (bilinen senaryo)
    "Warfarin kullanan bir hastaya ibuprofen verilirse ne olur?",

    # 2. Coklu ilac kombinasyonu (iki farkli dokumandan bilgi birlestirme)
    "Metformin ve glimepirid birlikte kullanilabilir mi, dikkat edilmesi gereken bir sey var mi?",

    # 3. Dozaj sorusu (sayisal bilginin dogru aktarilmasi)
    "Ibuprofen (Artril) icin yetiskinlerde onerilen gunluk maksimum doz nedir?",

    # 4. Kontrendikasyon sorusu (net uyarilarin yakalanmasi)
    "Warfarin hangi durumlarda kesinlikle kullanilmamali?",

    # 5. Kapsam disi soru (veride olmayan bir ilac - halusinasyon testi)
    "Parasetamol ile amoksisilin birlikte kullanilabilir mi?",

    # 6. Belirsiz/genel soru (sistemin genel bir soruda ne yaptigini gormek)
    "Bu hastaya hangi ilaci verebilirim?",
]


def tum_testleri_calistir():
    for i, soru in enumerate(TEST_SORULARI, start=1):
        print(f"\n\n{'#'*70}")
        print(f"# TEST {i}/{len(TEST_SORULARI)}")
        print('#'*70)
        sorgula(soru)
        input("\n[Devam etmek icin Enter'a basin...]")


if __name__ == "__main__":
    tum_testleri_calistir()