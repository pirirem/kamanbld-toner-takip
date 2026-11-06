import base64
from datetime import datetime
import pandas as pd
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Kaman Belediyesi - UTAX Toner Takip",
    page_icon="🖨️",
    layout="wide",
)

# Yönetici parolası
ADMIN_SIFRE = "1924.Blds"

# Oturum durumu kontrolü
if "giris_yapildi" not in st.session_state:
    st.session_state["giris_yapildi"] = False

# Veri Yapısı Başlangıcı (Stoklar sıfırlandı)
if "stoklar" not in st.session_state:
    st.session_state["stoklar"] = {
        "UTAX 2507": {
            "Siyah": 0,
            "Mavi (Cyan)": 0,
            "Kırmızı (Magenta)": 0,
            "Sarı (Yellow)": 0,
        },
        "UTAX 2508": {
            "Siyah": 0,
            "Mavi (Cyan)": 0,
            "Kırmızı (Magenta)": 0,
            "Sarı (Yellow)": 0,
        },
        "UTAX 3062": {
            "Siyah": 0,
            "Mavi (Cyan)": 0,
            "Kırmızı (Magenta)": 0,
            "Sarı (Yellow)": 0,
        },
        "UTAX 4035": {"Siyah": 0},
        "UTAX 4531": {"Siyah": 0},
        "UTAX 4532": {"Siyah": 0},
    }

if "gecmis" not in st.session_state:
    st.session_state["gecmis"] = []

# --- GİRİŞ EKRANI ---
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
st.markdown(
    """
    <style>
    thead tr th {
        text-align: center !important;
        justify-content: center !important;
    }
    tbody tr td {
        text-align: center !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🖨️ Kaman Belediyesi - UTAX Toner & Envanter Takip Sistemi")
st.markdown("---")

# KRİTİK STOK ALARMI (3 ve altı)
kritik_urunler = []
for m_ad, r_dict in st.session_state["stoklar"].items():
    for r_ad, st_adet in r_dict.items():
        if st_adet <= 3:
            kritik_urunler.append(f"⚠️ **{m_ad} ({r_ad})**: {st_adet} adet kaldı!")

if kritik_urunler:
    st.error(
        "🚨 **Kritik Stok Alarmı:** Aşağıdaki tonerlerin stoku 3 adedin"
        " altındadır!\n\n"
        + "\n".join(kritik_urunler)
    )

# Üst Özet Paneli
toplam_stok = sum(
    sum(stoklar_dict.values())
    for stoklar_dict in st.session_state["stoklar"].values()
)
toplam_yazici_modeli = len(st.session_state["stoklar"])

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("📦 Toplam Dolu Toner Stoğu", toplam_stok)
col_m2.metric("🖨️ Takip Edilen Model", f"{toplam_yazici_modeli} Çeşit")
col_m3.metric("🏢 Kayıtlı Birim Dağıtımı", len(st.session_state["gecmis"]))
if col_m4.button("🔒 Oturumu Kapat"):
    st.session_state["giris_yapildi"] = False
    st.rerun()

st.markdown("---")

# YATAY SEKMELER
sekme1, sekme2, sekme3, sekme4, sekme5 = st.tabs(
    [
        "📦 Mevcut Stok Durumu",
        "🔄 Manuel Stok Ekle & Birime Ver",
        "📊 Yıl İçinde Sarfiyat Grafikleri",
        "📋 İşlem Geçmişi & Arama",
        "📥 Excel Rapor & Tutanak",
    ]
)

with sekme1:
    st.subheader("📊 Yazıcı Bazlı Mevcut Toner Stokları")
    st.markdown(
        "Yazıcı adlarının üzerine tıklayarak detaylı stok durumlarını"
        " görebilirsiniz."
    )

    for model, renkler in st.session_state["stoklar"].items():
        with st.expander(f"🖨️ {model} - Stok Detayları", expanded=False):
            tablo_verisi = []
            for renk, stok_miktari in renkler.items():
                tablo_verisi.append({
                    "Model": model,
                    "Renk": renk,
                    "Stok Adedi": stok_miktari,
                })

            df_model = pd.DataFrame(tablo_verisi)
            st.dataframe(df_model, use_container_width=True, hide_index=True)

with sekme2:
    st.subheader("🔄 Manuel Stok Ekleme / Çıkarma ve Birime Teslim Paneli")
    st.markdown(
        "Bu alandan stoğa yeni toner ekleyebilir veya birimlere çıkış"
        " yapabilirsiniz."
    )

    with st.form("stok_islem_formu"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            secilen_model = st.selectbox(
                "Yazıcı Modeli", list(st.session_state["stoklar"].keys())
            )
        with c2:
            secilen_renk = st.selectbox(
                "Renk", list(st.session_state["stoklar"][secilen_model].keys())
            )
        with c3:
            islem_tipi = st.selectbox(
                "İşlem Tipi", ["Stok Ekle (+)", "Birime Ver / Düş (-)"]
            )
        with c4:
            miktar = st.number_input("Miktar", min_value=1, value=1, step=1)

        birim_adi = st.text_input(
            "Teslim Edilen Birim",
            placeholder="Örn: Yazı İşleri Müdürlüğü vb.",
        )
        islem_notu = st.text_input("Açıklama / Not", placeholder="İsteğe bağlı")

        submit_islem = st.form_submit_button("İşlemi Gerçekleştir")

        if submit_islem:
            mevcut = st.session_state["stoklar"][secilen_model][secilen_renk]
            if "Ekle" in islem_tipi:
                st.session_state["stoklar"][secilen_model][secilen_renk] += (
                    miktar
                )
                st.success(
                    f"✅ {secilen_model} ({secilen_renk}) stoğa {miktar} adet"
                    " eklendi."
                )
                st.rerun()
            else:
                if mevcut >= miktar:
                    st.session_state["stoklar"][secilen_model][secilen_renk] -= (
                        miktar
                    )
                    kayit = {
                        "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Model": secilen_model,
                        "Renk": secilen_renk,
                        "Miktar": miktar,
                        "İşlem": islem_tipi,
                        "Birim": birim_adi if birim_adi else "Belirtilmedi",
                        "Not": islem_notu,
                    }
