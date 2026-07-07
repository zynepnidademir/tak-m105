"""
Klinik Karar Destek Sistemi - Test Betigi
==========================================
Bu dosya iki seviyeli test icerir:

  SEVIYE 1 - RAG Soru Testleri:
      Sadece Retrieval Agent + LLM cevaplama katmanini test eder.
      Hasta baglami yoktur, dogrudan genel bilgi sorusu sorulur.
      Kullanilan fonksiyon: sorgula(soru)

  SEVIYE 2 - Epikriz Tabanli Uctan Uca Sistem Testleri:
      Document Ingestion -> Orchestrator -> Drug Interaction Checker /
      Risk Assessment -> Citation Validator -> Report Generation zincirinin tamamini test eder. 
      Hasta epikrizi + soru birlikte verilir.
      Kullanilan fonksiyon: analiz_et(epikriz, soru)
"""

from rag_sorgula import sorgula

try:
    from orchestrator import analiz_et  # beklenen imza: analiz_et(epikriz: str, soru: str) -> None/dict
    ANALIZ_ET_MOCK = False
except ImportError:
    ANALIZ_ET_MOCK = True

    def analiz_et(epikriz: str, soru: str):
        """
        GECICI ISKELET (MOCK) - orchestrator.analiz_et henuz yazilmadi.
        Gercek agent pipeline hazir oldugunda bu fonksiyon yerine
        orchestrator.py icindeki gercek analiz_et() kullanilacaktir.
        Simdilik epikriz + soruyu birlestirip mevcut sorgula() ile
        RAG uzerinden gecici bir cevap uretir; boylece test akisi
        bozulmadan calisir.
        """
        print("[UYARI] analiz_et() henuz gercek pipeline'a bagli degil - MOCK modda calisiyor.")
        birlesik_sorgu = (
            f"Hasta epikrizi:\n{epikriz}\n\n"
            f"Soru: {soru}\n\n"
            f"Lutfen yukaridaki hasta bilgilerine gore etkilesim, "
            f"kontrendikasyon ve risk acisindan degerlendir."
        )
        return sorgula(birlesik_sorgu)


# ---------------------------------------------------------------------------
# SEVIYE 1 - RAG Soru Testleri (baglamsiz, genel bilgi sorulari)
# ---------------------------------------------------------------------------
TEST_SORULARI = [
    # 1. Basit ilac etkilesimi (bilinen senaryo)
    "Warfarin kullanan bir hastaya ibuprofen verilirse ne olur?",
    # 2. Coklu ilac kombinasyonu (iki farkli dokumandan bilgi birlestirme)
    "Metformin ve glimepirid birlikte kullanilabilir mi, dikkat edilmesi gereken bir sey var mi?",
    # 3. Dozaj sorusu (sayisal bilginin dogru aktarilmasi)
    "Ibuprofen (Artril) icin yetiskinlerde onerilen gunluk maksimum doz nedir?",
    # 4. Kontrendikasyon sorusu (net uyarilarin yakalanmasi)
    "Warfarin hangi durumlarda kesinlikle kullanilmamali?",
    # 5. Bilinen "risksiz" kombinasyon (false-positive / uydurma etkilesim testi)
    #    NOT: Bu kombinasyonun onemli bir etkilesimi yoktur; test amaci,
    #    sistemin OLMAYAN bir etkilesimi UYDURMADIGINI dogrulamaktir.
    "Parasetamol ile amoksisilin birlikte kullanilabilir mi?",
    # 6. Belirsiz/genel soru (sistemin hasta baglami olmadan ne yaptigini gormek)
    "Bu hastaya hangi ilaci verebilirim?",
]


# ---------------------------------------------------------------------------
# SEVIYE 2 - Epikriz Tabanli Vaka Testleri (uctan uca agent pipeline)
# ---------------------------------------------------------------------------
VAKA_TESTLERI = [
    {
        "ad": "Vaka 1 - Kontrol Vakasi (risk beklenmiyor)",
        "epikriz": (
            "34 yasinda kadin hasta, mevsimsel alerjik rinit tanisiyla "
            "loratadin 10 mg/gun baslandi. Ek hastaligi ve ilac kullanimi yok. "
            "Alerji oykusu yok."
        ),
        "soru": "Bu hastanin tedavisinde herhangi bir risk veya etkilesim var mi?",
        "beklenen": "Anlamli bir etkilesim/kontrendikasyon bulunmamali (dusuk risk).",
    },
    {
        "ad": "Vaka 2 - Ilac-Ilac Etkilesimi (kanama riski)",
        "epikriz": (
            "68 yasinda erkek hasta, atriyal fibrilasyon nedeniyle varfarin "
            "kullanmakta (INR 2.4). Diz agrisi sikayeti uzerine ibuprofen "
            "400 mg gunde 2 kez eklendi."
        ),
        "soru": "Yeni eklenen ilac mevcut tedaviyle cakisiyor mu?",
        "beklenen": "Varfarin + NSAID kombinasyonu -> yuksek onem dereceli kanama riski uyarisi.",
    },
    {
        "ad": "Vaka 3 - Ilac-Hastalik Kontrendikasyonu",
        "epikriz": (
            "72 yasinda kadin hasta, evre 4 kronik bobrek yetmezligi "
            "(eGFR 28) mevcut. Tip 2 diyabet tanisiyla metformin 1000 mg/gun "
            "baslanmasi planlaniyor."
        ),
        "soru": "Planlanan tedavi hastanin mevcut durumuna uygun mu?",
        "beklenen": "Dusuk eGFR + metformin -> laktik asidoz riski nedeniyle yuksek risk uyarisi.",
    },
    {
        "ad": "Vaka 4 - Alerji Cakismasi",
        "epikriz": (
            "45 yasinda erkek hasta, akut bakteriyel sinuzit tanisiyla "
            "amoksisilin 500 mg gunde 3 kez recete edilmek isteniyor. "
            "Ozgecmisinde penisilin alerjisi (dokuntu, anjiyoodem) kayitli."
        ),
        "soru": "Recete edilmek istenen ilac hastanin alerji gecmisiyle uyumlu mu?",
        "beklenen": "Amoksisilin - penisilin alerjisi cakismasi -> kritik/yuksek oncelikli uyari.",
    },
    {
        "ad": "Vaka 5 - Coklu Risk Faktoru / Polifarmasi",
        "epikriz": (
            "79 yasinda kadin hasta; hipertansiyon, tip 2 diyabet ve kronik "
            "kalp yetmezligi tanilariyla ramipril, metformin ve furosemid "
            "kullanmakta. Kalp yetmezligi tedavisine spironolakton eklenmesi "
            "planlaniyor. Son tahlilde potasyum 5.3 mEq/L, eGFR 45."
        ),
        "soru": "Spironolakton eklenmesi bu hasta icin guvenli mi? Genel risk durumu nedir?",
        "beklenen": "Ramipril + Spironolakton + yuksek K+ -> hiperkalemi riski, genel risk 'yuksek'.",
    },
    {
        "ad": "Vaka 6 - Kaynakta Olmayan / Belirsiz Bilgi (gercek halusinasyon testi)",
        "epikriz": (
            "51 yasinda erkek hasta, nadir bir otoimmun hastalik tanisiyla "
            "takip edilmekte. Iki farkli biyolojik ajanin birlikte kullanimi "
            "planlaniyor (bu kombinasyona dair kaynak veri setinde dogrudan "
            "bilgi bulunmamaktadir)."
        ),
        "soru": "Bu iki biyolojik ajanin birlikte kullanimi guvenli mi?",
        "beklenen": (
            "Sistem kaynak yetersizligini acikca belirtmeli, kesin bir yargi "
            "uydurmamali ('kaynak yetersiz, hekim degerlendirmesi onerilir')."
        ),
    },
]


def seviye_1_calistir():
    print("\n" + "=" * 70)
    print("SEVIYE 1 - RAG SORU TESTLERI (baglamsiz)")
    print("=" * 70)
    for i, soru in enumerate(TEST_SORULARI, start=1):
        print(f"\n\n{'#' * 70}")
        print(f"# TEST {i}/{len(TEST_SORULARI)}")
        print(f"# Soru: {soru}")
        print("#" * 70)
        sorgula(soru)
        input("\n[Devam etmek icin Enter'a basin...]")


def seviye_2_calistir():
    print("\n" + "=" * 70)
    print("SEVIYE 2 - EPIKRIZ TABANLI VAKA TESTLERI (uctan uca)")
    if ANALIZ_ET_MOCK:
        print("(MOCK MOD: orchestrator.analiz_et henuz baglanmadi)")
    print("=" * 70)
    for i, vaka in enumerate(VAKA_TESTLERI, start=1):
        print(f"\n\n{'#' * 70}")
        print(f"# VAKA {i}/{len(VAKA_TESTLERI)}: {vaka['ad']}")
        print(f"# Beklenen: {vaka['beklenen']}")
        print("#" * 70)
        print(f"\n[Epikriz]\n{vaka['epikriz']}")
        print(f"\n[Soru]\n{vaka['soru']}\n")
        analiz_et(vaka["epikriz"], vaka["soru"])
        input("\n[Devam etmek icin Enter'a basin...]")


def tum_testleri_calistir():
    seviye_1_calistir()
    seviye_2_calistir()


if __name__ == "__main__":
    tum_testleri_calistir()