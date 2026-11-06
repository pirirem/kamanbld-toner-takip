import base64
import pandas as pd
import streamlit as st

# Yönetici parolası
ADMIN_SIFRE = "1924.Blds"

# Oturum durumu kontrolü
if "giris_yapildi" not in st.session_state:
    st.session_state["giris_yapildi"] = False

if not st.session_state["giris_yapildi"]:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        }
        .login-container {
            background: rgba(30, 41, 59, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            max-width: 420px;
            margin: 0 auto;
            text-align: center;
        }
        .emblem-badge {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
            color: white;
            font-size: 20px;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            margin: 0 auto 12px auto;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
            border: 3px solid rgba(255, 255, 255, 0.3);
            letter-spacing: 1px;
        }
        .login-title {
            color: #f8fafc;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .login-subtitle {
            color: #94a3b8;
            font-size: 13px;
            margin-bottom: 20px;
        }
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 12px;
            border: none;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            box-shadow: 0 6px 15px rgba(59, 130, 246, 0.6);
            color: white;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Logoyu güvenli bir şekilde okuyup HTML içine ortalıyoruz
    try:
        with open("logo.png", "rb") as f:
            logo_bytes = f.read()
        logo_base64 = base64.b64encode(logo_bytes).decode()
        logo_element = f'<img src="data:image/png;base64,{logo_base64}" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 3px solid rgba(255, 255, 255, 0.3); box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);">'
    except:
        logo_element = '<div class="emblem-badge">1924</div>'

    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown(
            f"""
            <div class="login-container">
                <div style="display: flex; justify-content: center; margin-bottom: 15px;">
                    {logo_element}
                </div>
                <div class="login-title">Kaman Belediyesi</div>
                <div class="login-subtitle">Bilgi İşlem & Envanter Yönetimi</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("giris_formu"):
            girilen_sifre = st.text_input(
                "Yönetici Parolası",
                type="password",
                placeholder="Parolanızı girin...",
            )
            kabul_et = st.checkbox(
                "Güvenlik şartlarını ve kullanım koşullarını okudum."
            )
            submit_btn = st.form_submit_button("Güvenli Oturum Aç")

            if submit_btn:
                if not kabul_et:
                    st.warning(
                        "⚠️ Devam etmek için lütfen onay kutusunu işaretleyin."
                    )
                elif girilen_sifre == ADMIN_SIFRE:
                    st.session_state["giris_yapildi"] = True
                    st.success("✅ Yetki onaylandı, yönlendiriliyorsunuz...")
                    st.rerun()
                else:
                    st.error("❌ Hatalı parola! Lütfen tekrar deneyin.")

    st.stop()

# --- GİRİŞ YAPILDIKTAN SONRAKİ ANA UYGULAMA ALANI ---
st.title("🖨️ Kaman Belediyesi - UTAX Toner & Envanter Takip Sistemi")
st.success("Oturum başarıyla açıldı. Yönetim paneline hoş geldiniz.")

if st.button("Oturumu Kapat"):
    st.session_state["giris_yapildi"] = False
    st.rerun()
