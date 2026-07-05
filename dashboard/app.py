import streamlit as st
import os
import base64
import textwrap

# Page configuration
st.set_page_config(
    page_title="Klinik Karar Destek Sistemi",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to load and convert image to base64
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception:
        return None

# Load logo
logo_path = os.path.join("assets", "medical_logo.png")
logo_base64 = get_image_base64(logo_path)

# Custom Styling (CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

    /* Global Typography & Background */
    html, body, [class*="css"], .stApp, .main, .block-container, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #F4F6F9 !important;
        color: #1E293B;
    }
    
    /* Hide Streamlit components for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header styling */
    .header-container {
        display: flex;
        align-items: center;
        padding: 1.5rem 2rem;
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 2rem;
        border-left: 6px solid #004080;
    }
    .logo-img {
        height: 60px;
        margin-right: 1.5rem;
        border-radius: 6px;
    }
    .logo-fallback {
        font-size: 2.5rem;
        margin-right: 1.5rem;
        background: #E0F2FE;
        padding: 0.5rem;
        border-radius: 8px;
        color: #004080;
    }
    .header-title-container {
        display: flex;
        flex-direction: column;
    }
    .header-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #004080;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748B;
        margin: 0;
        margin-top: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .institution {
        font-size: 0.75rem;
        color: #94A3B8;
        font-weight: 500;
    }

    /* Target Streamlit native container borders for panel division */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 1.75rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.01) !important;
        margin-bottom: 1.5rem !important;
    }

    /* Style the Search Form container */
    form[data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 1.25rem !important;
        margin-top: 1rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02) !important;
    }

    /* Subtitle details */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 1.25rem;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Custom Message Balloons */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
        min-height: 100px;
    }
    
    .message-user {
        align-self: flex-end;
        background-color: #F1F5F9;
        border: 1px solid #E2E8F0;
        color: #0F172A;
        padding: 1rem 1.25rem;
        border-radius: 16px 16px 4px 16px;
        max-width: 85%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    .message-user-header {
        font-size: 0.7rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
        text-align: right;
    }
    .message-user-text {
        font-size: 0.95rem;
        line-height: 1.5;
        font-weight: 500;
    }

    /* Medical Report / AI Response */
    .medical-report {
        align-self: flex-start;
        background-color: #ffffff;
        border: 1px solid #E2E8F0;
        border-top: 5px solid #004080;
        border-radius: 12px;
        padding: 1.5rem;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .medical-report-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 0.75rem;
        margin-bottom: 1rem;
    }
    .medical-report-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #004080;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Risk Badges (Pill shape and medical palette colors) */
    .risk-badge {
        padding: 0.25rem 0.75rem !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        border-radius: 9999px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        display: inline-block !important;
    }
    .risk-high {
        background-color: #F8D7DA !important;
        color: #721C24 !important;
        border: 1px solid #F5C6CB !important;
    }
    .risk-moderate {
        background-color: #FFF3CD !important;
        color: #856404 !important;
        border: 1px solid #FFEBAA !important;
    }
    .risk-low {
        background-color: #D4EDDA !important;
        color: #155724 !important;
        border: 1px solid #C3E6CB !important;
    }

    .report-section {
        margin-bottom: 1.25rem;
    }
    .report-section:last-child {
        margin-bottom: 0;
    }
    .report-section-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.35rem;
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }
    .report-section-content {
        font-size: 0.92rem;
        line-height: 1.6;
        color: #334155;
    }
    .report-section-content ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    .report-section-content li {
        margin-bottom: 0.25rem;
    }

    /* Right Sidebar Sources Panel Title */
    .sources-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #004080;
        margin: 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #E2E8F0;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .source-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    .source-card:hover {
        border-color: #004080;
        background-color: #F1F5F9;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .source-meta {
        display: flex;
        justify-content: space-between;
        font-size: 0.72rem;
        color: #64748B;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .source-title-text {
        font-size: 0.88rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }
    .source-snippet {
        font-size: 0.8rem;
        color: #475569;
        line-height: 1.5;
        font-style: italic;
        background: #ffffff;
        padding: 0.6rem 0.75rem;
        border-radius: 6px;
        border-left: 3px solid #94A3B8;
        margin-bottom: 0.75rem;
    }
    
    /* PDF Viewer Simulation Modal */
    .pdf-simulation {
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        background-color: #F1F5F9;
        padding: 1.5rem;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Dashboard Empty/State Components */
    .dashboard-welcome {
        background: linear-gradient(135deg, #004080 0%, #0B5394 100%);
        color: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 51, 102, 0.15);
    }
    .dashboard-welcome h2 {
        color: #ffffff !important;
        margin: 0 0 0.5rem 0;
        font-weight: 700;
    }
    .dashboard-welcome p {
        color: #E2E8F0;
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .quick-queries-container {
        margin-top: 1.5rem;
    }
    
    /* Buttons Custom Overrides */
    
    /* Secondary buttons (Quick queries & Clear history) */
    div.stButton > button, button[kind="secondary"] {
        background-color: #E6F0FA !important;
        color: #004080 !important;
        border: 1px solid #BEE3F8 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover, button[kind="secondary"]:hover {
        background-color: #004080 !important;
        color: #ffffff !important;
        border-color: #004080 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 6px -1px rgba(0, 64, 128, 0.1) !important;
    }

    /* Primary buttons (Sorgula) */
    button[kind="primary"], button[type="submit"], button[data-testid="stFormSubmitButton"], .stFormSubmitButton > button {
        background-color: #0056B3 !important;
        color: #ffffff !important;
        border: 1px solid #0056B3 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }
    button[kind="primary"]:hover, button[type="submit"]:hover, button[data-testid="stFormSubmitButton"]:hover, .stFormSubmitButton > button:hover {
        background-color: #004080 !important;
        border-color: #004080 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0, 86, 179, 0.25) !important;
    }

    /* Right column minimalist gray border buttons (Dökümanı Aç) - overriding default button style */
    div[data-testid="stColumn"]:nth-child(2) div.stButton > button {
        background-color: #ffffff !important;
        color: #475569 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        padding: 0.35rem 0.75rem !important;
    }
    div[data-testid="stColumn"]:nth-child(2) div.stButton > button:hover {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border-color: #94A3B8 !important;
    }
/* 1. Üstteki Siyah Menü Çubuğunu Tamamen Gizleme (Yüksekliği Sıfırlar) */
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0rem;
    }
    
    /* Sayfa içeriğinin yukarıdaki boşluğunu azaltarak yukarı yanaşmasını sağlar */
    .block-container {
        padding-top: 1.5rem !important;
    }

    /* 2. Input Focus Olduğunda Çıkan Kırmızı Çerçeveyi Maviye Çevirme */
    /* Streamlit'in kendi iç elementlerindeki kırmızı focus rengini eziyoruz */
    div[data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
        border-color: #0056B3 !important;
        box-shadow: 0 0 0 1px #0056B3 !important;
    }
    
    /* Input elementinin kendisine de ekstra garanti olarak mavi border veriyoruz */
    div[data-testid="stTextInput"] input {
        background-color: #ffffff !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        border-color: #0056B3 !important;
        box-shadow: none !important;
    }

    .empty-sources {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 1rem;
        text-align: center;
        color: #94A3B8;
        background: #F8FAFC;
        border: 2px dashed #E2E8F0;
        border-radius: 8px;
    }
    .empty-sources-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #CBD5E1;
    }
    .empty-sources-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #64748B;
        margin-bottom: 0.25rem;
    }
    .empty-sources-desc {
        font-size: 0.8rem;
        color: #94A3B8;
        max-width: 200px;
    }
</style>
""", unsafe_allow_html=True)

# Mock Clinical Database
MOCK_DATA = {
    "Aspirin ve İbuprofen birlikte kullanılabilir mi?": {
        "risk": "moderate",
        "risk_label": "Orta Risk / Farmakodinamik Etkileşim",
        "title": "Aspirin & İbuprofen Etkileşim Raporu",
        "summary": [
            "İbuprofen, düşük doz Aspirin'in (kardiyoprotektif amaçlı) trombosit agregasyonunu önleyici (antiplatelet) etkisini antagonize eder.",
            "Her iki ilaç da NSAİİ (Non-Steroid Antiinflamatuar İlaç) sınıfında yer aldığından, gastrointestinal kanama, peptik ülser ve renal toksisite riski sinerjik şekilde artar.",
            "Kardiyovasküler koruma altında olan hastalarda aspirin etkinliğinin azalması trombotik olay riskini yükseltebilir."
        ],
        "mechanism": "İbuprofen, trombositlerdeki Siklooksijenaz-1 (COX-1) enziminin aktif bölgesindeki hidrofobik kanala geçici olarak bağlanarak, Aspirin'in (asetilsalisilik asit) COX-1 serin kalıntısını (Ser529) geri dönüşümsüz olarak asetillemesini sterik olarak engeller.",
        "recommendation": "Kardiyoprotektif aspirin kullanan hastalarda analjezik veya antiinflamatuar olarak İbuprofen yerine <b>Parasetamol</b> tercih edilmelidir. İbuprofen kullanımı zorunlu ise, <b>Aspirin İbuprofen'den en az 30-60 dakika önce</b> veya <b>İbuprofen alımından en az 8 saat sonra</b> uygulanmalıdır. Uzun süreli ortak kullanımda gastrointestinal profilaksi amacıyla Proton Pompası İnhibitörü (PPİ) eklenmesi önerilir.",
        "references": [
            {
                "doc_name": "TUKMOS Romatoloji ve Klinik Farmakoloji Kılavuzu 2024",
                "chapter_page": "Bölüm 8, Sayfa 142",
                "snippet": "Non-selektif NSAİİ'lerin kardiyoprotektif aspirin dozuyla eşzamanlı kullanımı platelet agregasyon önleyici etkiyi azaltmaktadır. Bu durum kardiyovasküler korumayı sekteye uğratabilir.",
                "doc_id": "TUKMOS_ROM_2024"
            },
            {
                "doc_name": "Türkiye İlaç ve Tıbbi Cihaz Kurumu (TİTCK) Prospektüs Uyarı Bülteni",
                "chapter_page": "Ek-1: Kardiyovasküler Risk ve NSAİİ Kombinasyonları, Sayfa 18",
                "snippet": "İbuprofen'in aspirin antiplatelet etkisini antagonize etmesini önlemek amacıyla dozlama zamanlaması hassasiyetle ayarlanmalıdır. Aspirin'in en az 30 dk önce veya İbuprofen'den 8 saat sonra alınması tavsiye edilir.",
                "doc_id": "TITCK_NSAIID_2023"
            }
        ]
    },
    "Metformin ve Kontrast Madde etkileşimi nasıldır?": {
        "risk": "high",
        "risk_label": "Ciddi Risk / İşlem Öncesi Tedbir Gerekli",
        "title": "Metformin & İyotlu Kontrast Madde Etkileşim Raporu",
        "summary": [
            "İntravasküler iyotlu kontrast madde uygulaması akut renal perfüzyon bozukluğuna ve kontrast nefropatisine (CIN) yol açabilir.",
            "Böbrek fonksiyonları bozulan hastalarda vücuttan atılamayan Metformin birikerek <b>Laktik Asidoz</b> gelişimine neden olur.",
            "Laktik asidoz, yüksek mortalite oranına sahip (%30-50) acil bir metabolik tablodur."
        ],
        "mechanism": "İyotlu kontrast maddeler renal tübüler hücreler üzerinde direkt sitotoksisite ve renal vazokonstriksiyon oluşturarak akut böbrek hasarı yapabilir. Metformin böbrek tübüllerinden aktif sekresyonla atılır; böbrek yetmezliği geliştiğinde biriken metformin, mitokondriyal solunum zincirini inhibe ederek anaerobik glikolizi arttırır ve laktik asit üretimini patolojik seviyelere taşır.",
        "recommendation": "eGFR değeri < 60 mL/dak/1.73m² olan veya intra-arteriyel kontrast enjeksiyonu yapılacak hastalarda <b>Metformin işlem saatinde veya öncesinde kesilmelidir</b>. İşlemden sonra en az 48 saat boyunca metformin askıda tutulmalı ve ancak 48. saat sonrasında yapılan renal fonksiyon testinde (kreatinin/eGFR) bozulma olmadığı teyit edildikten sonra ilaca tekrar başlanmalıdır. eGFR > 60 ve IV kontrast alacak elektif hastalarda hidrasyon desteği verilerek metformin kesilmeden işlem yapılabilir.",
        "references": [
            {
                "doc_name": "Türkiye Radyoloji Derneği (TRD) Kontrast Madde Kullanım Rehberi v4.1",
                "chapter_page": "Bölüm 3.2: Diyabetik Hastalarda Yaklaşım, Sayfa 74",
                "snippet": "Renal fonksiyon bozukluğu olan (eGFR < 45-60) veya arteriyel kateterizasyon yapılan hastalarda metformin enjeksiyon anında kesilmeli ve 48 saat sonra kreatinin takibi ile normal sınırlarda ise başlanmalıdır.",
                "doc_id": "TRD_KONTRAST_V4"
            },
            {
                "doc_name": "TUKMOS Endokrinoloji ve Metabolizma Hastalıkları Klinik Rehberi",
                "chapter_page": "Bölüm 12: Metformin Güvenlik Profili ve Renal Kısıtlar, Sayfa 218",
                "snippet": "Metformin ilişkili laktik asidoz (MALA) nadir olmakla birlikte, kontrast nefropatisi varlığında dramatik olarak tetiklenebilir. Profilaktik askıya alma kararı hayati önem taşır.",
                "doc_id": "TUKMOS_ENDO_MET"
            }
        ]
    },
    "Gebelikte Parasetamol kullanımı güvenli midir?": {
        "risk": "low",
        "risk_label": "Düşük Risk / Birinci Basamak Tercih",
        "title": "Gebelikte Parasetamol (Asetaminofen) Güvenlik Raporu",
        "summary": [
            "Parasetamol, gebeliğin tüm trimesterlerinde analjezik (ağrı kesici) ve antipiretik (ateş düşürücü) olarak en güvenli kabul edilen ve birinci basamak önerilen ajandır.",
            "Terapötik dozlarda majör konjenital malformasyonlar veya olumsuz obstetrik sonuçlar ile ilişkili bulunmamıştır.",
            "Diğer analjezikler (özellikle NSAİİ'ler; gebeliğin 30. haftasından sonra duktus arteriozusun erken kapanmasına yol açabilir) ile kıyaslandığında belirgin şekilde güvenlidir."
        ],
        "mechanism": "Parasetamol santral sinir sisteminde prostaglandin sentezini inhibe ederek (COX-3 veya COX-1/2 varyantları üzerinden) etki gösterir. Periferik dokularda antiinflamatuar etkisi zayıftır. Plasentadan serbestçe geçmesine rağmen, terapötik dozlarda fetotoksik metabolitler oluşturmaz.",
        "recommendation": "Gebelik boyunca ihtiyaç halinde <b>en düşük etkin dozda</b> ve <b>mümkün olan en kısa süreyle</b> kullanılmalıdır. Günlük maksimum doz olan 4 gram (8 adet 500 mg tablet) aşılmamalıdır. Son yıllarda yapılan bazı epidemiyolojik çalışmalarda uzun süreli maruziyet (29 günden uzun) ile DEHB/otizm ilişkisi öne sürülmüş olsa da nedensellik kanıtlanmamıştır; yine de kısa süreli ve endikasyona yönelik kullanım prensibine sadık kalınmalıdır.",
        "references": [
            {
                "doc_name": "T.C. Sağlık Bakanlığı Kadın Sağlığı ve Doğum Klinik Protokolleri",
                "chapter_page": "Bölüm 5: Gebelikte Farmakoterapi Yaklaşımları, Sayfa 89",
                "snippet": "Parasetamol gebelikte analjezik ve antipiretik amaçla güvenle kullanılebilecek birinci basamak ajandır. Teratojenik riski saptanmamıştır.",
                "doc_id": "SB_GEBELIK_PROTOKOL"
            },
            {
                "doc_name": "FDA Gebelik Kategorileri ve Güvenli Analjezik Kullanım Rehberi",
                "chapter_page": "Bölüm 2: Obstetrik Analjezi Tercihleri, Sayfa 32",
                "snippet": "Gebelik süresince kısa süreli parasetamol maruziyeti ile majör fetal anomali veya gelişimsel kusurlar arasında kanıta dayalı klinik bir ilişki gösterilmemiştir. Diğer NSAİİ'lere kıyasla önceliklidir.",
                "doc_id": "FDA_PREG_ANALGESIC"
            }
        ]
    }
}

# Dynamic General RAG response generator
def generate_dynamic_response(query):
    query_lower = query.lower()
    
    # Simple semantic router to make custom queries feel intelligent
    if "warfarin" in query_lower or "kumadin" in query_lower or "alkol" in query_lower:
        return {
            "risk": "high",
            "risk_label": "Ciddi Risk / Koagülasyon Kararsızlığı",
            "title": "Warfarin & Etkileşim Raporu",
            "summary": [
                f"Sorguladığınız durum ('{query}'), oral antikoagülan olan Warfarin'in terapötik indeksinin darlığı nedeniyle kritik öneme sahiptir.",
                "Eşzamanlı kullanılan ajanlar veya besinler Warfarin'in metabolizmasını (CYP2C9) etkileyerek kanama riskini veya tromboz eğilimini artırabilir.",
                "INR düzeylerinde ani oynamalar hayatı tehdit edici iç kanamalara (özellikle GİS ve intrakraniyal) yol açabilir."
            ],
            "mechanism": "Warfarin, karaciğerde K vitamini epoksit redüktaz (VKORC1) enzimini inhibe ederek pıhtılaşma faktörlerinin (Faktör II, VII, IX, X) sentezini engeller. CYP2C9 indükleyicileri veya inhibitörleri ile etkileşime girerek klirensini doğrudan değiştirir.",
            "recommendation": "Hastanın yakın dönem <b>INR takibi</b> yapılmalı, hedef aralık (genelde 2.0 - 3.0) dışına çıkıldığında doz ayarlamasına gidilmelidir. K vitamini içeren yeşil yapraklı sebzelerin tüketimi sabit tutulmalıdır. Analjezi ihtiyacında parasetamol tercih edilmeli, NSAİİ grubu ilaçlardan kanama riskini katladıkları için uzak durulmalıdır.",
            "references": [
                {
                    "doc_name": "TUKMOS Hematoloji Klinik Kılavuzu 2025",
                    "chapter_page": "Bölüm 3: Antikoagülan Tedavi Yönetimi, Sayfa 102",
                    "snippet": "Oral antikoagülan alan hastalarda ek ilaç veya besin eklenmesi durumunda INR değeri 3-5 gün içinde mutlaka kontrol edilmeli ve gerekirse doz revize edilmelidir.",
                    "doc_id": "TUKMOS_HEM_2025"
                },
                {
                    "doc_name": "Ulusal Akılcı İlaç Kullanımı Kılavuzu",
                    "chapter_page": "Bölüm 9: Yüksek Riskli İlaçların Yönetimi, Sayfa 215",
                    "snippet": "Warfarin ile klinik olarak anlamlı etkileşime giren yüzlerce molekül bulunmaktadır. Her yeni ilaç başlanmasında etkileşim kontrolü zorunludur.",
                    "doc_id": "ULUSAL_AKILCI_ILAC"
                }
            ]
        }
    
    elif "greyfurt" in query_lower or "cyp3a4" in query_lower or "statik" in query_lower or "atorvastatin" in query_lower:
        return {
            "risk": "moderate",
            "risk_label": "Orta Risk / CYP3A4 Metabolizma Etkileşimi",
            "title": "CYP3A4 Enzim Etkileşim Raporu",
            "summary": [
                f"Sorgunuz ('{query}'), bağırsak ve karaciğerdeki CYP3A4 sitokrom p450 enzim yolağını ilgilendiren bir etkileşime işaret etmektedir.",
                "CYP3A4 inhibitörleri (örn. greyfurt suyu, klaritromisin), bu yolakla metabolize olan ilaçların (örn. Atorvastatin, Amlodipin) plazma konsantrasyonunu artırır.",
                "Bu durum ilacın sistemik yan etkilerinin ve toksisitesinin (örn. statin kullananlarda rabdomiyoliz ve kas ağrıları) ortaya çıkma ihtimalini güçlendirir."
            ],
            "mechanism": "Greyfurt suyundaki furanokumarinler, intestinal duvardaki CYP3A4 enzimini geri dönüşümsüz olarak inhibe eder. Bu durum, ilk geçiş metabolizmasını bloke ederek ilacın biyoyararlanımını ve dolayısıyla serum seviyelerini katlayarak artırır.",
            "recommendation": "CYP3A4 üzerinden yoğun metabolize olan statinler (Atorvastatin, Simvastatin) kullanan hastaların greyfurt ve greyfurt suyu tüketiminden kaçınması önerilir. Kas ağrısı, koyu renkli idrar veya halsizlik gelişen hastalarda kreatin kinaz (CK) düzeyleri izlenmelidir. Gerekirse CYP3A4 dışı yolaklarla elime edilen Pravastatin veya Rosuvastatin tercih edilebilir.",
            "references": [
                {
                    "doc_name": "TUKMOS Kardiyoloji Klinik Kılavuzu - Lipid Yönetimi",
                    "chapter_page": "Bölüm 6, Sayfa 59",
                    "snippet": "CYP3A4 enzimini inhibe eden besin ve ilaçların Atorvastatin gibi statinlerle eşzamanlı kullanımı miyopati ve rabdomiyoliz riskini artırır.",
                    "doc_id": "TUKMOS_KARD_LIPID"
                }
            ]
        }
        
    else:
        # Fallback RAG Response
        return {
            "risk": "moderate",
            "risk_label": "Klinik İnceleme Gerekli / RAG Analizi",
            "title": f"'{query}' Klinik Analiz Raporu",
            "summary": [
                f"Sorguladığınız klinik durum veya kombinasyon ('{query}') RAG motorumuz tarafından ulusal kılavuzlar taranarak değerlendirilmiştir.",
                "Hastanın genel klinik tablosu, böbrek/karaciğer fonksiyonları ve eşlik eden hastalıkları (komorbiditeler) bu etkileşimin seyrini belirleyebilir.",
                "Polifarmasi vakalarında ilaçlar arası çapraz reaksiyonlar ve aditif yan etkiler göz önünde bulundurulmalıdır."
            ],
            "mechanism": "Raporlanan ajanların farmakokinetik (absorbsiyon, dağılım, metabolizma, eliminasyon) veya farmakodinamik (reseptör düzeyinde antagonizma veya sinerjizm) yollarla etkileşme potansiyeli klinik gözlem gerektirmektedir.",
            "recommendation": "Reçete edilmeden önce hastanın güncel ilaç listesi (Reçetem sistemi) kontrol edilmeli ve ilaçların yarı ömürleri göz önüne alınarak alım saatleri ayrılmalıdır. Olası advers reaksiyonlar (bulantı, döküntü, baş dönmesi, laboratuvar parametrelerinde sapmalar) açısından hasta bilgilendirilmelidir.",
            "references": [
                {
                    "doc_name": "Türkiye İlaç Rehberi v24.2 (Sağlık Bakanlığı Akılcı İlaç Yönetimi)",
                    "chapter_page": "Genel İlaç Etkileşimleri Bölümü, Sayfa 304",
                    "snippet": "Kombine ilaç kullanımlarında hastanın renal klirensi (kreatinin klirensi) ve hepatik fonksiyonları her zaman ilk belirleyici parametre olarak ele alınmalıdır.",
                    "doc_id": "TR_ILAC_REHBERI_24"
                }
            ]
        }

# Initializing Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_references" not in st.session_state:
    st.session_state.current_references = []
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# Function to execute a query
def handle_query(query_text):
    if not query_text or query_text.strip() == "":
        return
        
    query_text = query_text.strip()
    
    # Process
    if query_text in MOCK_DATA:
        result = MOCK_DATA[query_text]
    else:
        result = generate_dynamic_response(query_text)
        
    # Append user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": query_text
    })
    
    # Append assistant medical report response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": result
    })
    
    # Update current active references on right panel
    st.session_state.current_references = result.get("references", [])
    st.session_state.last_query = query_text

# Custom Streamlit Modal Dialog for PDF Simulator
@st.dialog("Kılavuz Belgesi Görüntüleyici", width="large")
def show_pdf_viewer(doc_name, chapter_page, snippet):
    st.markdown(textwrap.dedent(f"""
    <div style="background-color: #0F172A; padding: 1rem; border-radius: 8px 8px 0 0; color: white; display: flex; justify-content: space-between; align-items: center;">
        <div style="font-weight: 700; font-size: 0.95rem; display: flex; align-items: center; gap: 0.5rem;">
            <i class="fa-solid fa-book-medical"></i> {doc_name}
        </div>
        <div style="background-color: #334155; padding: 0.25rem 0.6rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">
            {chapter_page}
        </div>
    </div>
    <div style="background-color: white; border: 1px solid #E2E8F0; border-top: none; padding: 2rem; border-radius: 0 0 8px 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <div style="text-align: center; border-bottom: 2px double #E2E8F0; padding-bottom: 1rem; margin-bottom: 1.5rem;">
            <h4 style="color: #004080; margin: 0; font-weight: 700; font-size: 1.1rem; text-transform: uppercase;">T.C. SAĞLIK BAKANLIĞI</h4>
            <small style="color: #64748B; font-weight: 600; font-size: 0.75rem; letter-spacing: 1px;">KLİNİK REHBER & TEDAVİ PROTOKOLLERİ ARŞİVİ</small>
        </div>
        
        <p style="font-size: 0.85rem; color: #64748B; margin-bottom: 1.5rem; line-height: 1.4;">
            <b>Belge Sınıfı:</b> Ulusal Klinik Karar Destek Standardı Belgesi<br/>
            <b>Arşiv Kodu:</b> SB-GUIDE-2025-v9.42 &nbsp;|&nbsp; <b>Erişim:</b> Yetkili Sağlık Personeli (Güvenli Bağlantı)
        </p>
        
        <div style="background-color: #FFFBEB; border-left: 4px solid #F59E0B; padding: 1.25rem; margin-bottom: 1.5rem; border-radius: 4px;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #B45309; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.5px;">
                <i class="fa-solid fa-triangle-exclamation"></i> ALINTILANAN RESMİ KLİNİK PARAGRAF:
            </div>
            <p style="font-size: 0.95rem; color: #78350F; line-height: 1.6; font-style: italic; margin: 0;">
                "... {snippet} ..."
            </p>
        </div>
        
        <div style="font-size: 0.85rem; color: #334155; line-height: 1.6;">
            <p><b>Klinik Uygulama Notu:</b> Yukarıda alıntılanan kılavuz metni, T.C. Sağlık Bakanlığı TUKMOS (Tıpta Uzmanlık Kurulu Müfredat Oluşturma ve Standart Belirleme Sistemi) komisyonları ve ilgili dernekler tarafından onaylanan en güncel konsensüs kararlarını yansıtmaktadır. Karar aşamasında hastanın bireysel böbrek/karaciğer parametreleri ve komorbidite geçmişi önceliklidir.</p>
        </div>
        
        <div style="margin-top: 2rem; border-top: 1px solid #E2E8F0; padding-top: 1rem; display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: #94A3B8;">
            <span>Dijital İmzalı Doküman: TUKMOS-SECURE-ID-884A9</span>
            <span>Sayfa Arşivi Resmi Çıktısı</span>
        </div>
    </div>
    """), unsafe_allow_html=True)
    if st.button("Kapat", use_container_width=True):
        st.rerun()

# ----------------- UI RENDERING -----------------

# Page Header
if logo_base64:
    header_html = f"""
    <div class="header-container">
        <img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="Logo">
        <div class="header-title-container">
            <span class="header-title">KLİNİK KARAR DESTEK SİSTEMİ</span>
            <span class="header-subtitle">Klinik Rehber & İlaç Etkileşim Güvenliği RAG Asistanı</span>
            <span class="institution">T.C. SAĞLIK BAKANLIĞI • AKILCI İLAÇ KULLANIMI PORTALI</span>
        </div>
    </div>
    """
else:
    header_html = """
    <div class="header-container">
        <span class="logo-fallback"><i class="fa-solid fa-stethoscope"></i></span>
        <div class="header-title-container">
            <span class="header-title">KLİNİK KARAR DESTEK SİSTEMİ</span>
            <span class="header-subtitle">Klinik Rehber & İlaç Etkileşim Güvenliği RAG Asistanı</span>
            <span class="institution">T.C. SAĞLIK BAKANLIĞI • AKILCI İLAÇ KULLANIMI PORTALI</span>
        </div>
    </div>
    """
st.markdown(header_html, unsafe_allow_html=True)

# Main Grid Layout: Left 2/3 (Query & History), Right 1/3 (References)
col1, col2 = st.columns([2, 1], gap="medium")

# LEFT 2/3: QUERY AREA & CHAT HISTORY
with col1:
    # Welcome banner & Quick Queries if chat history is empty
    if len(st.session_state.chat_history) == 0:
        with st.container(border=True):
            st.markdown("""
            <div class="dashboard-welcome">
                <h2>Klinik Güvenlik Sorgulama Modülü</h2>
                <p>Hastalarınıza reçete edeceğiniz ilaçların birbiriyle veya klinik durumlarıyla (gebelik, böbrek yetmezliği vb.) etkileşimini, ulusal klinik rehberler ve prospektüs veri tabanları üzerinden RAG (Retrieval-Augmented Generation) teknolojisiyle sorgulayın.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="quick-queries-title"><i class="fa-solid fa-circle-info"></i> Hızlı Örnek Sorgular (Prototip Deneyin)</div>', unsafe_allow_html=True)
            
            # Grid layout for quick query cards
            q_cols = st.columns(3)
            quick_queries = list(MOCK_DATA.keys())
            for idx, q_text in enumerate(quick_queries):
                with q_cols[idx]:
                    # We use a unique key for each button and custom styled streamlit buttons to trigger the action
                    if st.button(
                        q_text, 
                        key=f"btn_q_{idx}", 
                        use_container_width=True, 
                        type="secondary"
                    ):
                        handle_query(q_text)
                        st.rerun()

    # Chat / Query History Container
    if len(st.session_state.chat_history) > 0:
        with st.container(border=True):
            st.markdown('<div class="section-title"><i class="fa-solid fa-magnifying-glass"></i> Klinik Sorgu Geçmişi ve Sonuçlar</div>', unsafe_allow_html=True)
            
            # Render messages in historical order
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-container">
                        <div class="message-user">
                            <div class="message-user-header">HEKİM SORGUSU</div>
                            <div class="message-user-text">{msg["content"]}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Assistant Medical Report response
                    rep = msg["content"]
                    
                    # Dynamic risk class based on value
                    risk_class = f"risk-{rep['risk']}"
                    
                    # Generate bulleted points list HTML
                    bullets_html = "".join([f"<li>{item}</li>" for item in rep["summary"]])
                    
                    st.markdown(f"""
                    <div class="chat-container">
                        <div class="medical-report">
                            <div class="medical-report-header">
                                <span class="medical-report-title"><i class="fa-solid fa-notes-medical"></i> {rep['title']}</span>
                                <span class="risk-badge {risk_class}">{rep['risk_label']}</span>
                            </div>
                            <div class="report-section">
                                <div class="report-section-title"><i class="fa-solid fa-clipboard-list"></i> Klinik Bulgular ve Özet</div>
                                <div class="report-section-content">
                                    <ul>
                                        {bullets_html}
                                    </ul>
                                </div>
                            </div>
                            <div class="report-section">
                                <div class="report-section-title"><i class="fa-solid fa-dna"></i> Etkileşim Mekanizması</div>
                                <div class="report-section-content">{rep['mechanism']}</div>
                            </div>
                            <div class="report-section" style="background-color: #F8FAFC; padding: 0.85rem; border-radius: 6px; border-left: 3px solid #004080;">
                                <div class="report-section-title" style="color: #004080;"><i class="fa-solid fa-triangle-exclamation"></i> Hekim Klinik Karar Önerisi</div>
                                <div class="report-section-content" style="font-weight: 500;">{rep['recommendation']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # Search bar form at the bottom
    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
    with st.container():
        # Text input using streamlit form to handle enter and click cleanly
        with st.form(key="query_form", clear_on_submit=True):
            input_cols = st.columns([5, 1])
            with input_cols[0]:
                user_input = st.text_input(
                    label="Klinik Sorgu Girişi",
                    placeholder="İlaç adları, etkileşimler veya klinik durum sorgulayın (örn: Metformin ve Kontrast Madde)...",
                    label_visibility="collapsed",
                    key="query_input"
                )
            with input_cols[1]:
                submit_button = st.form_submit_button(
                    label="Sorgula", 
                    use_container_width=True,
                    type="primary"
                )
                
            if submit_button and user_input:
                handle_query(user_input)
                st.rerun()
                
    # Reset/Clear history button (for convenience)
    if len(st.session_state.chat_history) > 0:
        st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)
        if st.button("Sorgu Geçmişini Temizle", type="secondary", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.current_references = []
            st.session_state.last_query = ""
            st.rerun()


# RIGHT 1/3: SOURCES & REFERENCES PANEL
with col2:
    with st.container(border=True):
        st.markdown('<div class="sources-title"><i class="fa-solid fa-book-medical"></i> Kaynaklar ve Referanslar</div>', unsafe_allow_html=True)
        
        if len(st.session_state.current_references) > 0:
            st.markdown(f"""
            <div style="font-size: 0.8rem; color: #64748B; font-weight: 600; margin-bottom: 0.75rem; text-transform: uppercase;">
                "{st.session_state.last_query}" sorgusu için bulunan referanslar:
            </div>
            """, unsafe_allow_html=True)
            
            # Render each source card
            for idx, src in enumerate(st.session_state.current_references):
                st.markdown(f"""
                <div class="source-card">
                    <div class="source-meta">
                        <span>DOKÜMAN ID: {src['doc_id']}</span>
                        <span>{src['chapter_page']}</span>
                    </div>
                    <div class="source-title-text">
                        <i class="fa-solid fa-file-invoice"></i> {src['doc_name']}
                    </div>
                    <div class="source-snippet">
                        "{src['snippet']}"
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Use Streamlit dialog/modal simulation for "Dökümanı Aç"
                # Note: We must place the button within the streamlit flow for interaction
                # To lay it out neatly, we put it directly after each markdown block using st.button
                if st.button(
                    f"Dökümanı Aç ({src['doc_id']})", 
                    key=f"open_doc_{idx}", 
                    use_container_width=True
                ):
                    show_pdf_viewer(
                        doc_name=src['doc_name'], 
                        chapter_page=src['chapter_page'], 
                        snippet=src['snippet']
                    )
        else:
            # Empty state
            st.markdown("""
            <div class="empty-sources">
                <span class="empty-sources-icon"><i class="fa-solid fa-magnifying-glass"></i></span>
                <div class="empty-sources-title">Referans Bulunamadı</div>
                <div class="empty-sources-desc">Sol panelden bir klinik sorgu yaptığınızda, ilgili tıbbi rehber bölümleri burada listelenecektir.</div>
            </div>
            """, unsafe_allow_html=True)
