import streamlit as st
from rag_sorgula import ilgili_chunklari_bul, cevap_uret

st.set_page_config(page_title="Klinik Rehber & İlaç Etkileşim Asistanı", page_icon="💊", layout="wide")

st.title("💊 Klinik Rehber & İlaç Etkileşim Güvenliği Asistanı")
st.caption("Yalnızca yüklenen KÜB dokümanlarındaki bilgilere dayanarak yanıt verir. Tıbbi tavsiye yerine geçmez.")

# --- Sol panel ---
with st.sidebar:
    st.header("📄 Veri Kaynakları")
    st.markdown("""
    - **Warfmadin** 5mg (Varfarin)
    - **Artril** 600mg (İbuprofen)
    - **Amaryl** 2mg (Glimepirid)
    - **Atamet** 1000mg (Metformin)
    """)
    st.info("Sistem yalnızca bu 4 KÜB dokümanına dayanarak cevap verir. Dokümanlarda olmayan bilgi için 'yeterli veri yok' der.")

    st.divider()

    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.mesajlar = []
        st.rerun()

    st.divider()
    st.caption("⚠️ Bu bir prototiptir. Klinik karar desteği amaçlı geliştirilmektedir, nihai karar her zaman hekime aittir.")

# --- State başlatma ---
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

# --- Örnek sorular (sohbet boşsa göster) ---
if not st.session_state.mesajlar:
    st.markdown("##### 💡 Örnek sorular ile başlayabilirsiniz:")
    ornek_sorular = [
        "Warfarin kullanan bir hastaya ibuprofen verilirse ne olur?",
        "Metformin ve glimepirid birlikte kullanılabilir mi?",
        "Warfarin hangi durumlarda kesinlikle kullanılmamalı?",
        "Ibuprofen için günlük maksimum doz nedir?",
    ]
    cols = st.columns(2)
    secilen_soru = None
    for i, ornek in enumerate(ornek_sorular):
        if cols[i % 2].button(ornek, use_container_width=True, key=f"ornek_{i}"):
            secilen_soru = ornek
else:
    secilen_soru = None

# --- Geçmiş mesajları göster ---
for mesaj in st.session_state.mesajlar:
    with st.chat_message(mesaj["rol"], avatar="👨‍⚕️" if mesaj["rol"] == "user" else "💊"):
        st.markdown(mesaj["icerik"])
        if mesaj["rol"] == "assistant" and mesaj.get("kaynaklar"):
            with st.expander("📚 Kullanılan Kaynaklar"):
                for k in mesaj["kaynaklar"]:
                    st.markdown(f"- **{k['ilac']}** (Sayfa {k['ilk_sayfa']}-{k['son_sayfa']})")


def soruyu_isle(soru):
    st.session_state.mesajlar.append({"rol": "user", "icerik": soru})
    with st.chat_message("user", avatar="👨‍⚕️"):
        st.markdown(soru)

    with st.chat_message("assistant", avatar="💊"):
        try:
            with st.spinner("İlgili dokümanlar taranıyor ve cevap hazırlanıyor..."):
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

        except Exception as e:
            hata_mesaji = (
                "⚠️ Şu anda dokümanlara erişirken veya cevap üretirken bir sorun oluştu. "
                "Bu genellikle geçici bir bağlantı veya sistem yoğunluğu sorunudur. "
                "Lütfen birkaç saniye sonra tekrar deneyin."
            )
            st.error(hata_mesaji)
            st.session_state.mesajlar.append({
                "rol": "assistant",
                "icerik": hata_mesaji,
                "kaynaklar": None,
            })


# --- Örnek soru tıklanırsa işle ---
if secilen_soru:
    soruyu_isle(secilen_soru)
    st.rerun()

# --- Chat input ---
soru = st.chat_input("Vaka veya ilaç etkileşimi sorunuzu yazın...")
if soru:
    soruyu_isle(soru)