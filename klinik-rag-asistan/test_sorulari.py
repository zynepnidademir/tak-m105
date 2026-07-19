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
    # 7. Kardiyoloji ve Diyabet etkilesimi
    "Beloc ZOK kullanan bir diyabet hastasinda Atamet (Metformin) kullanimi hipoglisemi belirtilerini etkiler mi?",
    # 8. Kardiyoloji - Coklu ilac (Kanama riski)
    "Plavix (Klopidogrel) ve Warfmadin (Varfarin) birlikte kullanildiginda kanama riski artar mi?",
    # 9. Kardiyoloji - Diuretik ve NSAII etkilesimi
    "Delix Plus kullanan bir hastaya agri kesici olarak Ibuprofen verilirse bobreklerde ne gibi sorunlar olusabilir?",
    # 10. Kontrendikasyon (Gebelik)
    "Hamile bir hastaya Delix Plus veya Warfmadin recete edilebilir mi?"
    # 7. Ilac-gida etkilesimi (dokuman disi ama klinik olarak onemli bir konu)
    "Warfarin kullanirken K vitamini icerigi yuksek sebzeler (orn. ispanak) tuketmenin bir sakincasi var mi?",
    # 8. Ozel populasyon / kontrendikasyon (gebelik)
    "Glimepirid gebelikte kullanilabilir mi?",
    # 9. Doz ayarlamasi + bobrek fonksiyonu kombinasyonu
    "Bobrek yetmezligi olan bir hastada ibuprofen (Artril) dozunun ayarlanmasi gerekir mi?",
    ''' 10. [ROUTER TETIKLEME] 3+ ilacli soru - farkli 3 KUB dokumanina bolunmus bilginin tek cevapta birlestirilmesi gerekiyor. 
    NOT: n_results=5 sabit oldugu icin bu test, 3 ilacin da dengeli sekilde retrieval'a 
    girip girmedigini (yoksa bir ilacin gozden kacip kacmadigini) ortaya
    cikarir - basarisiz olursa n_results/router mimarisini gozden gecirin.
    '''
    "Warfarin, ibuprofen ve metformin ayni hastada birlikte kullaniliyor. "
    "Bu uc ilac arasinda dikkat edilmesi gereken etkilesimler nelerdir?",
 
    # 11. [ROUTER TETIKLEME] Farkli 3+ ilac kombinasyonu (Vaka 9'a benzer ama baglamsiz/genel soru formatinda - Seviye 1'de ayrica test edilmeli)
    "Glimepirid, metformin ve varfarin ayni anda kullanildiginda "
    "olusabilecek riskler nelerdir?",
 
    # 12. [YANLIS YAZIM] "varfarn" typo'su - embedding'in kelime hatasina ragmen dogru ilaca (warfarin) yonlenip yonlenmedigini test eder.
    "Varfarn kullanan bir hastaya ibuprofen verilirse ne olur?",
 
    # 13. [YANLIS YAZIM] Iki ayri typo ayni soruda ("metformn", "gilmepirid")
    "Metformn ile gilmepirid birlikte kullanilabilir mi?",
 
    # 14. [YANLIS YAZIM] Marka adinda typo ("Artil" -> Artril, "Amaril" -> Amaryl)
    "Artil (ibuprofen) ile Amaril birlikte alinirsa bir sorun olur mu?",
 
    # 15. [KISA/BELIRSIZ] Hicbir ilac veya hasta bilgisi icermiyor - sistem SISTEM_PROMPTU kuralina gore netlestirme istemeli, tahmin yurutmemeli.
    "Etkilesir mi?",
 
    # 16. [KISA/BELIRSIZ] "Bu ilaclar" - onceki konusma baglami olmadan hangi ilaclarin kastedildigi belirsiz.
    "Bu ilaclar birlikte kullanilir mi?",
 
    # 17. [DOZAJ + ETKILESIM BIRLESIK] Tek soruda iki farkli bilgi turu
    #     isteniyor - cevabin hem dozu hem de etkilesim riskini net ayirmasi
    #     gerekir (BULGULAR bolumunde karistirmadan).
    "Ibuprofenin (Artril) gunluk maksimum dozu nedir ve varfarin ile "
    "birlikte kullanilirsa kanama riski artar mi?",
 
    # 18. [DOZAJ + ETKILESIM BIRLESIK] Farkli ilac cifti ile ayni format
    "Metforminin (Atamet) onerilen baslangic dozu nedir ve glimepirid ile "
    "ayni anda kullanilirsa hipoglisemi riski nasil degisir?",
]


def router_regresyon_testi():
    """Coklu ilac router mantiginin dogru calistigini dogrular."""
    from rag_sorgula import ilgili_chunklari_bul

    print(f"\n{'#'*70}")
    print("# ROUTER REGRESYON TESTI")
    print(f"{'#'*70}\n")

    coklu_ilac_sorulari = [
        ("Metformin ve glimepirid birlikte kullanilabilir mi?", 2),
        ("Warfarin kullanan bir hastaya ibuprofen verilirse ne olur?", 2),
        ("Ibuprofen icin gunluk maksimum doz nedir?", 1),
	
	("Metformin ve glimepirid birlikte kullanilabilir mi?", 2),
        ("Warfarin kullanan bir hastaya ibuprofen verilirse ne olur?", 2),
        ("Ibuprofen icin gunluk maksimum doz nedir?", 1),
        ("Warfarin, ibuprofen ve metformin ayni anda kullanilirsa ne olur?", 3),




    ]

    for soru, beklenen_ilac_sayisi in coklu_ilac_sorulari:
        chunklar = ilgili_chunklari_bul(soru)
        benzersiz_ilac = len(set(c["ilac"] for c in chunklar))
        durum = "BASARILI" if benzersiz_ilac >= beklenen_ilac_sayisi else "BASARISIZ"
        print(f"[{durum}] '{soru}' -> {benzersiz_ilac} ilac bulundu (beklenen: {beklenen_ilac_sayisi})")



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
    {
        "ad": "Vaka 7 - Kardiyoloji ve Diyabet Capraz Etkilesimi",
        "epikriz": (
            "55 yasinda erkek hasta, hipertansiyon ve tip 2 diyabet tanisiyla "
            "Beloc ZOK 50 mg ve Atamet 1000 mg kullanmakta. Kan sekeri regulasyonu "
            "zaman zaman bozuluyor."
        ),
        "soru": "Beloc ZOK (metoprolol) kullanimi hastanin hipoglisemi durumunu ve belirtilerini nasil etkiler?",
        "beklenen": "Beta blokerlerin hipoglisemi semptomlarini (tasikardi vb.) maskeleyebilecegi uyarisi.",
    },
    {
        "ad": "Vaka 8 - Kardiyoloji ve Agri Kesici (NSAII) Cakismasi",
        "epikriz": (
            "62 yasinda kadin hasta, esansiyel hipertansiyon nedeniyle Delix Plus "
            "(5mg/25mg) kullanmaktadir. Siddetli osteoartrit agrilari nedeniyle "
            "gunde 2 kez Ibuprofen 600 mg (Artril) recete edilmesi planlaniyor."
        ),
        "soru": "Bu iki ilacin (Delix Plus ve Ibuprofen) birlikte kullanimi bobrekler ve potasyum seviyesi acisindan guvenli mi?",
        "beklenen": "NSAII + ADE Inhibitoru/Diuretik cakismasi -> Akut bobrek yetmezligi ve potasyum artisi riski uyarisi.",
    },
    {
        "ad": "Vaka 9 - Ilac-Durum Kontrendikasyonu (Gebelik)",
        "epikriz": (
            "28 yasinda kadin hasta, 10 haftalik gebe. Gecmiste gecirilmis "
            "derin ven trombozu oykusu nedeniyle Warfmadin 5mg baslanmasi dusunuluyor."
        ),
        "soru": "Gebe hastaya Warfarin (Warfmadin) verilmesi uygun mudur?",
        "beklenen": "Gebelik durumu + Warfarin -> Teratojenik etki/fetus zarari nedeniyle kesin kontrendikasyon uyarisi.",
    },
    {
        "ad": "Vaka 10 - Coklu Kardiyoloji Ilaci Kullanimi",
        "epikriz": (
            "65 yasinda erkek hasta, kronik stabil anjina ve hipertansiyon "
            "tanilariyla Norvasc (Amlodipin) 5 mg kullanmaktadir. Hastanin "
            "tedavisine Beloc ZOK (Metoprolol) eklenmesi planlanmaktadir."
        ),
        "soru": "Norvasc ve Beloc ZOK birlikte kullanildiginda hemodinamik acikdan neye dikkat edilmelidir?",
        "beklenen": "Kalsiyum kanal blokoru + Beta bloker cakismasi -> Kalp hizi ve tansiyon uzerinde aditif etki, bradikardi/hipotansiyon riski.",
    }
    {
        "ad": "Vaka 11- Gebelikte Kontrendike Ilac",
        "epikriz": (
            "28 yasinda gebe hasta (24. gebelik haftasi), tip 2 diyabet "
            "tanisiyla glimepirid 2 mg/gun baslanmasi planlaniyor. Baska "
            "ek hastalik veya ilac kullanimi yok."
        ),
        "soru": "Planlanan tedavi gebelik acisindan uygun mu?",
        "beklenen": (
            "Sulfonilure grubu (glimepirid) gebelikte onerilmez, insulin "
            "tercih edilmeli -> yuksek onem dereceli kontrendikasyon uyarisi."
        ),
    },
    {
        "ad": "Vaka 12 - Yasli Hasta + Bobrek Fonksiyonu + NSAID",
        "epikriz": (
            "81 yasinda erkek hasta, kronik bobrek hastaligi evre 3 "
            "(eGFR 38) mevcut. Osteoartrit agrisi nedeniyle ibuprofen "
            "(Artril) 600 mg gunde 3 kez baslanmasi planlaniyor."
        ),
        "soru": "Bu doz ve ilac secimi hastanin bobrek fonksiyonuna uygun mu?",
        "beklenen": (
            "NSAID nefrotoksisite riski + dusuk eGFR -> doz azaltma veya "
            "alternatif analjezik onerisi ile orta-yuksek risk uyarisi."
        ),
    },
    {
        "ad": "Vaka 13 - Uclu Ilac Kombinasyonu (halusinasyon testi)",
        "epikriz": (
            "60 yasinda kadin hasta; tip 2 diyabet nedeniyle glimepirid ve "
            "metformin (Atamet) kullanmakta. Yeni gelisen atriyal "
            "fibrilasyon nedeniyle tedaviye varfarin eklenmesi planlaniyor."
        ),
        "soru": "Bu uc ilacin birlikte kullanimi guvenli mi, ozel bir etkilesim var mi?",
        "beklenen": (
            "Sistem yalnizca kaynaklarda yer alan ikili etkilesimleri "
            "(varsa) belirtmeli; uclu kombinasyona dair dogrudan veri "
            "yoksa bunu acikca ifade etmeli, uydurma bir etkilesim "
            "iddia etmemeli."
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
        print("#" * 70)h
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
    router_regresyon_testi()