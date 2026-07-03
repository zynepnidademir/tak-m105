import streamlit as st
from rag_sorgula import sorgula, ilgili_chunklari_bul, cevap_uret

st.set_page_config(page_title="Klinik Rehber & İlaç Etkileşim Asistanı", layout="wide")

st.title("💊 Klinik Rehber & İlaç Etkileşim Güvenliği Asistanı")
st.caption("Yalnızca yüklenen KÜB dokümanlarındaki bilgilere dayanarak yanıt verir.")

# Sol panel: veri durumu
with st.sidebar:
    st.header("📄 Veri Kaynakları")
    st.markdown("""
    - Warfmadin 5mg (Varfarin)
    - Artril 600mg (İbuprofen)
    - Amaryl 2mg (Glimepirid)
    - Atamet 1000mg (Metformin)
    """)
    st.info("Sistem yalnızca bu 4 KÜB dokümanına dayanarak cevap verir.")

# Sohbet geçmişi state'te tutulur
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

# Geçmiş mesajları göster
for mesaj in st.session_state.mesajlar:
    with st.chat_message(mesaj["rol"]):
        st.markdown(mesaj["icerik"])
        if mesaj["rol"] == "assistant" and "kaynaklar" in mesaj:
            with st.expander("📚 Kullanılan Kaynaklar"):
                for k in mesaj["kaynaklar"]:
                    st.markdown(f"- **{k['ilac']}** (Sayfa {k['ilk_sayfa']}-{k['son_sayfa']})")

# Yeni soru girişi
soru = st.chat_input("Vaka veya ilaç etkileşimi sorunuzu yazın...")

if soru:
    st.session_state.mesajlar.append({"rol": "user", "icerik": soru})
    with st.chat_message("user"):
        st.markdown(soru)

    with st.chat_message("assistant"):
        with st.spinner("Dokümanlar taranıyor..."):
            chunklar = ilgili_chunklari_bul(soru)
            cevap = cevap_uret(soru, chunklar)

        st.markdown(cevap)
        with st.expander("📚 Kullanılan Kaynaklar"):
            for c in chunklar:
                st.markdown(f"- **{c['ilac']}** (Sayfa {c['ilk_sayfa']}-{c['son_sayfa']})")

    st.session_state.mesajlar.append({
        "rol": "assistant",
        "icerik": cevap,
        "kaynaklar": chunklar,
    })