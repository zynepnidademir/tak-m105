import os
import streamlit as st
import streamlit.components.v1 as components
import sys
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag_sorgula import analiz_uret
import base64
import textwrap

# Page configuration
st.set_page_config(
    page_title="Klinik Karar Destek Sistemi",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
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

    /* ==============================================================
       SIDEBAR - Koyu Medikal Lacivert Tema + Sabit Genişlik
       ============================================================== */

    /* 1. Sidebar ana kutu: koyu lacivert, sabit genişlik, her zaman açık */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"][aria-expanded="false"],
    section[data-testid="stSidebar"][aria-expanded="true"] {
        display:          flex !important;
        visibility:       visible !important;
        min-width:        300px !important;
        max-width:        300px !important;
        width:            300px !important;
        transform:        none !important;
        transition:       none !important;
        opacity:          1 !important;
        pointer-events:   auto !important;
        background-color: #0A2540 !important;
    }

    /* 2. Tüm iç sarmalayıcı katmanları da aynı renge boyandı */
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] > div > div,
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLinks"],
    section[data-testid="stSidebar"] nav,
    section[data-testid="stSidebar"] nav ul,
    section[data-testid="stSidebar"] nav li {
        background-color: #0A2540 !important;
        background:       #0A2540 !important;
        overflow:         visible !important;
    }

    /* 3. Collapse / açma-kapama butonunu tamamen gizle */
    button[data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    button[aria-label="Close sidebar"] {
        display:    none !important;
        visibility: hidden !important;
    }

    /* 4. Nav linkleri: tek satır, taşma yok, daire için göreceli konum */
    section[data-testid="stSidebar"] nav a,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {
        position:         relative !important;
        display:          flex !important;
        align-items:      center !important;
        padding:          0.45rem 0.75rem 0.45rem 2rem !important;
        border-radius:    6px !important;
        text-decoration:  none !important;
        overflow:         visible !important;
        transition:       background-color 0.18s ease !important;
    }

    /* 5. Linklerin içindeki TÜM text taşıyıcıları: kelime kırma yok, üç nokta yok */
    section[data-testid="stSidebar"] nav a *,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] *,
    section[data-testid="stSidebar"] nav span,
    section[data-testid="stSidebar"] nav p,
    section[data-testid="stSidebar"] nav div {
        white-space:  nowrap !important;
        overflow:     visible !important;
        text-overflow: unset !important;
        max-width:    none !important;
        width:        auto !important;
    }

    /* 6. Pasif daire (gümüş gri) */
    section[data-testid="stSidebar"] nav a::before,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]::before {
        content:          '' !important;
        position:         absolute !important;
        left:             0.65rem !important;
        top:              50% !important;
        transform:        translateY(-50%) !important;
        width:            8px !important;
        height:           8px !important;
        border-radius:    50% !important;
        background-color: #CBD5E1 !important;
        flex-shrink:      0 !important;
        transition:       background-color 0.2s, box-shadow 0.2s !important;
    }

    /* 7. Aktif daire (parlak beyaz + hale) */
    section[data-testid="stSidebar"] nav a[aria-current="page"]::before,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"]::before {
        background-color: #FFFFFF !important;
        box-shadow:       0 0 0 3px rgba(255,255,255,0.22) !important;
    }

    /* 8. Hover satır vurgusu */
    section[data-testid="stSidebar"] nav a:hover,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {
        background-color: rgba(255,255,255,0.08) !important;
    }
    section[data-testid="stSidebar"] nav a:hover::before,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover::before {
        background-color: #93C5FD !important;
    }

    /* 9. Pasif link metni: gümüş gri */
    section[data-testid="stSidebar"] nav a,
    section[data-testid="stSidebar"] nav a span,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] p {
        font-family: 'Inter', sans-serif !important;
        font-size:   0.875rem !important;
        font-weight: 500 !important;
        color:       #CBD5E1 !important;
    }

    /* 10. Aktif link: saf beyaz + kalın + açık bant */
    section[data-testid="stSidebar"] nav a[aria-current="page"],
    section[data-testid="stSidebar"] nav a[aria-current="page"] span,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] p {
        color:            #FFFFFF !important;
        font-weight:      700 !important;
        background-color: rgba(255,255,255,0.10) !important;
    }

    /* 11. Bölüm başlıkları (Ana Menü / Bilgi & Destek) */
    section[data-testid="stSidebar"] [data-testid="stSidebarNavSeparator"],
    section[data-testid="stSidebar"] .sidebar-nav-section-header,
    section[data-testid="stSidebar"] span[class*="navSection"],
    section[data-testid="stSidebar"] p[class*="navSection"] {
        font-size:     0.68rem !important;
        font-weight:   700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        color:         #93C5FD !important;
        white-space:   nowrap !important;
        overflow:      visible !important;
        text-overflow: unset !important;
    }

    /* 12. Genel fallback: sidebar içindeki her öğe açık renk */
    section[data-testid="stSidebar"] * {
        color: #CBD5E1;
    }

    
    /* Print Styles for clean report printing */
    @media print {
        header[data-testid="stHeader"], 
        section[data-testid="stSidebar"], 
        div[data-testid="stForm"], 
        .stButton, 
        .dashboard-welcome,
        .quick-queries-title {
            display: none !important;
        }
        .block-container {
            max-width: 100% !important;
            padding: 0 !important;
        }
        body { background: white !important; }
        .medical-report { box-shadow: none !important; border: 1px solid #CBD5E1 !important; }
    }
    
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
    
    /* Risk Badges (Modern styling) */
    .risk-badge {
        padding: 0.35rem 0.85rem !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        display: inline-block !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    .risk-high {
        background: linear-gradient(135deg, #FFE4E6 0%, #FECDD3 100%) !important;
        color: #E11D48 !important;
        border: 1px solid #FDA4AF !important;
        box-shadow: 0 4px 10px rgba(225, 29, 72, 0.15) !important;
    }
    .risk-moderate {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%) !important;
        color: #D97706 !important;
        border: 1px solid #FCD34D !important;
        box-shadow: 0 4px 10px rgba(217, 119, 6, 0.15) !important;
    }
    .risk-low {
        background: linear-gradient(135deg, #DCFCE7 0%, #BBF7D0 100%) !important;
        color: #16A34A !important;
        border: 1px solid #86EFAC !important;
        box-shadow: 0 4px 10px rgba(22, 163, 74, 0.15) !important;
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

# Gercek RAG sistemi kullaniliyor

# Initializing Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_references" not in st.session_state:
    st.session_state.current_references = []
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

def handle_query(query_text):
    if not query_text or query_text.strip() == "":
        return
        
    query_text = query_text.strip()
    
    start_time = time.time()
    
    loading_placeholder = st.empty()
    loading_html = """
    <style>
    @keyframes spin-medical {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    @keyframes fade-seq-1 {
        0%, 25% { opacity: 1; }
        33%, 91% { opacity: 0; }
        100% { opacity: 1; }
    }
    @keyframes fade-seq-2 {
        0%, 25% { opacity: 0; }
        33%, 58% { opacity: 1; }
        66%, 100% { opacity: 0; }
    }
    @keyframes fade-seq-3 {
        0%, 58% { opacity: 0; }
        66%, 91% { opacity: 1; }
        100% { opacity: 0; }
    }

    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        background: #ffffff;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin: 1.5rem 0;
    }
    .medical-spinner {
        width: 45px;
        height: 45px;
        border: 4px solid #F1F5F9;
        border-top: 4px solid #0056B3;
        border-radius: 50%;
        animation: spin-medical 1s linear infinite;
        margin-bottom: 1.5rem;
    }
    .loading-text-wrapper {
        position: relative;
        height: 24px;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .loading-text-wrapper span {
        position: absolute;
        font-weight: 600;
        color: #334155;
        font-size: 1rem;
        text-align: center;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .seq-1 { animation: fade-seq-1 6s infinite; }
    .seq-2 { animation: fade-seq-2 6s infinite; }
    .seq-3 { animation: fade-seq-3 6s infinite; }
    </style>
    <div class="loading-container">
        <div class="medical-spinner"></div>
        <div class="loading-text-wrapper">
            <span class="seq-1">Klinik belgeler taranıyor...</span>
            <span class="seq-2">İlaç etkileşimleri kontrol ediliyor...</span>
            <span class="seq-3">Yapay zeka raporu oluşturuluyor...</span>
        </div>
    </div>
    """
    loading_placeholder.markdown(loading_html, unsafe_allow_html=True)
    
    result = analiz_uret(query_text)
    
    loading_placeholder.empty()
        
    end_time = time.time()
    elapsed_time = end_time - start_time
        
    # Append user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": query_text
    })
    
    # Append assistant medical report response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": result,
        "elapsed_time": elapsed_time
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

# ----------------- MULTIPAGE FUNCTIONS -----------------

def page_giris():
    if logo_base64:
        st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{logo_base64}" width="150" style="border-radius: 12px; margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #004080;'>Klinik Karar Destek Sistemine Hoş Geldiniz</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B; font-size: 1.1rem; max-width: 700px; margin: 0 auto 2rem auto;'>Bu asistan, sağlık profesyonellerinin güncel tıbbi kılavuzlar ve ilaç etkileşim veritabanları ışığında kanıta dayalı ve hızlı klinik kararlar almasına yardımcı olmak için RAG (Retrieval-Augmented Generation) teknolojisi ile geliştirilmiştir.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.info("**Sistemin Yetenekleri**\n\n- Anlık ilaç-ilaç etkileşim analizi\n\n- Güncel TUKMOS yönergelerine göre uyarılar\n\n- Hızlı kanıt (kaynak) gösterimi")
    with col2:
        st.info("**Nasıl Başlarım?**\n\nLütfen sol taraftaki menüden **Klinik Sorgulama Modülü**'nü seçerek hasta sorgunuzu gerçekleştirin.")

def page_sss():
    st.markdown("<h2 style='color: #004080;'><i class='fa-solid fa-circle-question'></i> Sıkça Sorulan Sorular (SSS)</h2>", unsafe_allow_html=True)
    with st.expander("RAG Sistemi Nasıl Çalışır?"):
        st.write("RAG (Retrieval-Augmented Generation), sorduğunuz soruyu önce T.C. Sağlık Bakanlığı'nın güncel ve onaylı klinik rehberlerinde arar. Bulduğu spesifik tıbbi paragrafları referans alarak yapay zeka aracılığıyla size kanıta dayalı, hekim dostu bir özet sunar. Bu sayede halüsinasyon (yanlış bilgi üretimi) riski en aza indirilir.")
    with st.expander("Sistemde Hangi İlaç ve Rehber Verileri Bulunuyor?"):
        st.write("Şu anki prototip sürümünde özellikle Warfarin, Metformin, Glimepirid, İbuprofen (Artril) ve Kontrast Madde (İyotlu) gibi sık etkileşime giren ilaçların 2025 güncel prospektüs ve klinik rehber verileri indekslenmiştir.")
    with st.expander("Sistem İnternet Bağlantısı Gerektirir mi?"):
        st.write("Evet, dil modeline erişim ve güncel veri tabanı sorguları için internet bağlantısı gerekmektedir. Ancak kurum içi sunucularda tamamen yerel (on-premise) çalışacak kapalı devre versiyonu da mevcuttur.")

def page_yardim():
    st.markdown("<h2 style='color: #004080;'><i class='fa-solid fa-headset'></i> Yardım ve İletişim</h2>", unsafe_allow_html=True)
    st.write("Sistemle ilgili teknik bir sorun yaşıyorsanız veya veri tabanına yeni bir klinik kılavuz eklenmesini talep ediyorsanız lütfen bizimle iletişime geçin.")
    st.markdown("""
    <div style="background-color: #F8FAFC; padding: 1.5rem; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 2rem;">
        <h4 style="margin-top: 0; color: #0F172A;"><i class="fa-solid fa-envelope"></i> Teknik Destek Masası</h4>
        <p style="color: #475569; margin-bottom: 0;">E-posta: <b>destek@saglik.gov.tr</b><br>Dahili No: <b>444 0 000 (Dahili: 1122)</b></p>
    </div>
    """, unsafe_allow_html=True)
    with st.form("contact_form"):
        st.markdown("**Destek Talebi Oluştur**")
        st.text_input("Kurum Sicil Numaranız / Ad Soyad")
        st.selectbox("Konu", ["Teknik Hata Bildirimi", "Klinik Veri Güncelleme Talebi", "Diğer"])
        st.text_area("Mesajınız")
        if st.form_submit_button("Talebi Gönder", type="primary"):
            st.success("Talebiniz başarıyla alınmıştır. Sistem yöneticileri en kısa sürede sizinle iletişime geçecektir.")

def page_sorgulama():

    # Page Header
    if logo_base64:
        header_html = f"""
        <div class="header-container">
            <img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="Logo">
            <div class="header-title-container">
                <span class="header-title">KLİNİK KARAR DESTEK SİSTEMİ</span>
                <span class="header-subtitle">Klinik Rehber & İlaç Etkileşim Güvenliği RAG Asistanı</span>
                <span class="institution">T.C. SAĞLIK BAKANLIĞI  •  AKILCI İLAÇ KULLANIMI PORTALI</span>
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
                quick_queries = [
            "Warfarin kullanan bir hastaya ibuprofen verilirse ne olur?",
            "Metformin ve glimepirid birlikte kullanılabilir mi?",
            "Warfarin hangi durumlarda kesinlikle kullanılmamalı?",
        ]
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
                    
                        # Dynamic risk class based on text content
                        summary_text = " ".join(rep.get("summary", [])) if isinstance(rep.get("summary"), list) else str(rep.get("summary", ""))
                        rep_str = f"{summary_text} {rep.get('mechanism', '')} {rep.get('recommendation', '')}".lower()
                    
                        if any(kw in rep_str for kw in ["kontrendike", "kontrendikasyon", "ölüm", "yüksek risk", "tehlikeli"]):
                            risk_class = "risk-high"
                            risk_label = '<i class="fa-solid fa-triangle-exclamation"></i> YÜKSEK RİSK / KONTRENDİKASYON'
                            plain_risk_label = "YÜKSEK RİSK / KONTRENDİKASYON"
                        elif any(kw in rep_str for kw in ["dikkat", "izlenmeli", "takip", "doz ayarı", "orta risk"]):
                            risk_class = "risk-moderate"
                            risk_label = '<i class="fa-solid fa-circle-exclamation"></i> DİKKAT / İZLENMELİ'
                            plain_risk_label = "DİKKAT / İZLENMELİ"
                        else:
                            risk_class = "risk-low"
                            risk_label = '<i class="fa-solid fa-check-circle"></i> GÜVENLİ'
                            plain_risk_label = "GÜVENLİ"
                    
                        # Generate bulleted points list HTML
                        bullets_html = "".join([f"<li>{item}</li>" for item in rep["summary"]])
                    
                        # Render the report card (without bottom padding to seamlessly attach toolbar)
                        st.markdown(f"""
                        <div class="chat-container" style="margin-bottom: 0;">
                            <div class="medical-report" style="border-bottom-left-radius: 0; border-bottom-right-radius: 0; border-bottom: none; box-shadow: none;">
                                <div class="medical-report-header">
                                    <span class="medical-report-title"><i class="fa-solid fa-notes-medical"></i> {rep['title']}</span>
                                    <span class="risk-badge {risk_class}">{risk_label}</span>
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
                                <div class="report-section" style="background-color: #EAEFF5; padding: 1rem; border-radius: 8px; border-left: 5px solid #0056B3; margin-bottom: 0; box-shadow: 0 2px 4px rgba(0, 86, 179, 0.05);">
                                    <div class="report-section-title" style="color: #0056B3; font-size: 0.9rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-user-md" style="font-size: 1.2em; margin-right: 0.2rem;"></i> Hekim Klinik Karar Önerisi</div>
                                    <div class="report-section-content" style="font-weight: 600; color: #1E293B; font-size: 0.95rem;">{rep['recommendation']}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                        # Prepare plain text for clipboard
                        copy_text = f"KLİNİK ANALİZ RAPORU\\n"
                        copy_text += f"──────────────────────────────\\n"
                        copy_text += f"Durum: {plain_risk_label}\\n\\n"
                        copy_text += f"Klinik Bulgular ve Özet:\\n"
                        for item in rep.get("summary", []):
                            copy_text += f"• {item}\\n"
                        copy_text += f"\\nEtkileşim Mekanizması:\\n{rep.get('mechanism', '')}\\n\\n"
                        copy_text += f"Hekim Klinik Karar Önerisi:\\n{rep.get('recommendation', '')}\\n"
                        copy_text += f"──────────────────────────────"
                    
                        safe_copy_text = json.dumps(copy_text)
                        time_text = f"Yanıt süresi: {msg['elapsed_time']:.2f} saniye" if "elapsed_time" in msg else ""
                    
                        # HTML/JS Toolbar with Copy Button
                        html_code = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
                            <style>
                                body {{ 
                                    margin: 0; 
                                    padding: 0.75rem 1.5rem; 
                                    display: flex; 
                                    align-items: center; 
                                    justify-content: space-between; 
                                    background: #ffffff; 
                                    font-family: 'Inter', sans-serif;
                                    border: 1px solid #E2E8F0;
                                    border-top: 1px dashed #E2E8F0;
                                    border-bottom-left-radius: 12px;
                                    border-bottom-right-radius: 12px;
                                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                                }}
                                .btn-group {{
                                    display: flex;
                                    gap: 0.75rem;
                                }}
                                button {{
                                    background-color: #F8FAFC;
                                    color: #475569;
                                    border: 1px solid #CBD5E1;
                                    border-radius: 6px;
                                    padding: 0.4rem 0.8rem;
                                    font-size: 0.78rem;
                                    font-weight: 600;
                                    cursor: pointer;
                                    transition: all 0.2s;
                                    display: flex;
                                    align-items: center;
                                    gap: 0.4rem;
                                }}
                                button:hover {{
                                    background-color: #004080;
                                    color: #ffffff;
                                    border-color: #004080;
                                }}
                                .time-info {{
                                    font-size: 0.75rem;
                                    color: #94A3B8;
                                    display: flex;
                                    align-items: center;
                                    gap: 0.4rem;
                                    font-weight: 500;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="btn-group">
                                <button id="copyBtn" onclick="copyToClipboard()">
                                    <i class="fa-regular fa-copy"></i> Panoya Kopyala
                                </button>
                                <button id="printBtn" onclick="printReport()">
                                    <i class="fa-solid fa-print"></i> Raporu Yazdır
                                </button>
                            </div>
                            <div class="time-info">
                                <i class="fa-solid fa-stopwatch"></i> {time_text}
                            </div>
                            <script>
                                function copyToClipboard() {{
                                    navigator.clipboard.writeText({safe_copy_text}).then(function() {{
                                        const btn = document.getElementById('copyBtn');
                                        btn.innerHTML = '<i class="fa-solid fa-check"></i> Başarıyla Kopyalandı!';
                                        btn.style.backgroundColor = '#ECFDF5';
                                        btn.style.color = '#10B981';
                                        btn.style.borderColor = '#10B981';
                                        setTimeout(() => {{
                                            btn.innerHTML = '<i class="fa-regular fa-copy"></i> Panoya Kopyala';
                                            btn.style.backgroundColor = '';
                                            btn.style.color = '';
                                            btn.style.borderColor = '';
                                        }}, 2500);
                                    }}).catch(function(err) {{
                                        console.error('Kopyalama hatası: ', err);
                                    }});
                                }}
                                function printReport() {{
                                    try {{
                                        window.parent.print();
                                    }} catch (err) {{
                                        window.print();
                                    }}
                                }}
                            </script>
                        </body>
                        </html>
                        """
                        components.html(html_code, height=52)
                        st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

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

# ----------------- ROUTING -----------------
pg = st.navigation({
    "Ana Menü": [
        st.Page(page_giris, title="Ana Sayfa"),
        st.Page(page_sorgulama, title="Klinik Sorgulama Modülü"),
    ],
    "Bilgi & Destek": [
        st.Page(page_sss, title="Sıkça Sorulan Sorular"),
        st.Page(page_yardim, title="Yardım & İletişim"),
    ]
})
pg.run()
