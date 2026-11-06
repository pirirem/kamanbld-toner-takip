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

# Veri Yapısı Başlangıcı (Tablo Yapısına Uygun)
if "stoklar" not in st.session_state:
    # Her model için renklerin dolu ve boş adetleri
    st.session_state["stoklar"] = {
        "UTAX 2507": {
            "Siyah": {"Dolu": 10, "Boş": 2},
            "Mavi (Cyan)": {"Dolu": 10, "Boş": 2},
            "Kırmızı (Magenta)": {"Dolu": 10, "Boş": 2},
            "Sarı (Yellow)": {"Dolu": 10, "Boş": 2},
        },
        "UTAX 2508": {
            "Siyah": {"Dolu": 8, "Boş": 3},
            "Mavi (Cyan)": {"Dolu": 8, "Boş": 3},
            "Kırmızı (Magenta)": {"Dolu": 8, "Boş": 3},
            "Sarı (Yellow)": {"Dolu": 8, "Boş": 3},
        },
        "UTAX 3062": {
            "Siyah": {"Dolu": 6, "Boş": 1},
            "Mavi (Cyan)": {"Dolu": 6, "Boş": 1},
            "Kırmızı (Magenta)": {"Dolu": 6, "Boş": 1},
            "Sarı (Yellow)": {"Dolu": 6, "Boş": 1},
        },
        "UTAX 4035": {
            "Siyah": {"Dolu": 12, "Boş": 4},
        },
        "UTAX 4531": {
            "Siyah": {"Dolu": 9, "Boş": 2},
        },
        "UTAX 4532": {
            "Siyah": {"Dolu": 7, "Boş": 3},
        },
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
st.markdown("---")

# Üst Özet Hesaplamaları
toplam_dolu = sum(
    sum(durumlar["Dolu"] for durumlar in renkler.values())
    for renkler in st.session_state["stoklar"].values()
)
toplam_bos = sum(
    sum(durumlar.get("Boş", 0) for durumlar in renkler.values())
    for renkler in st.session_state["stoklar"].values()
)
toplam_yazici_modeli = len(st.session_state["stoklar"])

# Üst Özet Paneli (Metrics)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("📦 Toplam Dolu Toner", toplam_dolu)
col_m2.metric("♻️ Toplam Boş Toner", toplam_bos)
col_m3.metric("🖨️ Takip Edilen Model", f"{toplam_yazici_modeli} Çeşit")
col_m4.metric("🏢 Kayıtlı Birim İşlemi", len(st.session_state["gecmis"]))

st.markdown("---")

# Yan Menü / Sekmeler
menu = st.sidebar.selectbox(
    "Menü", ["Stok Durumu & Dağıtım", "İşlem Geçmişi & Raporlar"]
)

if menu == "Stok Durumu & Dağıtım":
    st.subheader("📦 Mevcut Stok Durumu (Yazıcı Bazlı Detaylar)")
    st.markdown(
        "Yazıcı adlarının üzerine tıklayarak detaylı stok durumlarını"
        " görebilirsiniz."
    )

    # Ekrandaki gibi her yazıcı için tablo oluşturuyoruz
    for model, renkler in st.session_state["stoklar"].items():
        with st.expander(f"🖨️ {model} - Stok Detayları", expanded=True):
            tablo_verisi = []
            for renk, durumlar in renkler.items():
                tablo_verisi.append({
                    "Model": model,
                    "Renk": renk,
                    "Durum": "Dolu",
                    "Stok": durumlar["Dolu"],
                })
                if "Boş" in durumlar:
                    tablo_verisi.append({
                        "Model": model,
                        "Renk": renk,
                        "Durum": "Boş",
                        "Stok": durumlar["Boş"],
                    })

            df_model = pd.DataFrame(tablo_verisi)
            st.dataframe(df_model, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("🔄 Stok Ekleme / Çıkarma ve Birime Teslim")

    with st.form("stok_islem_formu"):
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            secilen_model = st.selectbox(
                "Yazıcı Modeli", list(st.session_state["stoklar"].keys())
            )
        with c2:
            secilen_renk = st.selectbox(
                "Renk", list(st.session_state["stoklar"][secilen_model].keys())
            )
        with c3:
            secilen_durum = st.selectbox("Durum", ["Dolu", "Boş"])
        with c4:
            islem_tipi = st.selectbox(
                "İşlem Tipi", ["Stok Ekle (+)", "Birime Ver / Düş (-)"]
            )
        with c5:
            miktar = st.number_input("Miktar", min_value=1, value=1, step=1)

        birim_adi = st.text_input(
            "Teslim Edilen Birim", placeholder="Örn: Yazı İşleri Müdürlüğü"
        )
        islem_notu = st.text_input("Açıklama / Not", placeholder="İsteğe bağlı")

        submit_islem = st.form_submit_button("İşlemi Gerçekleştir")

        if submit_islem:
            # Kontrol et: Eğer modelde Boş toner yoksa ama Boş seçildiyse uyarı ver
            if (
                secilen_durum == "Boş"
                and secilen_durum
                not in st.session_state["stoklar"][secilen_model][secilen_renk]
            ):
                st.error(
                    f"❌ {secilen_model} modelinde boş toner takibi"
                    " bulunmamaktadır."
                )
            else:
                mevcut = st.session_state["stoklar"][secilen_model][
                    secilen_renk
                ][secilen_durum]
                if "Ekle" in islem_tipi:
                    st.session_state["stoklar"][secilen_model][secilen_renk][
                        secilen_durum
                    ] += miktar
                    st.success(
                        f"✅ {secilen_model} ({secilen_renk} - {secilen_durum})"
                        f" stoğa {miktar} adet eklendi."
                    )
                    st.rerun()
                else:
                    if mevcut >= miktar:
                        st.session_state["stoklar"][secilen_model][secilen_renk][
                            secilen_durum
                        ] -= miktar
                        kayit = {
                            "Tarih": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "Model": secilen_model,
                            "Renk": secilen_renk,
                            "Durum": secilen_durum,
                            "Miktar": miktar,
                            "İşlem": islem_tipi,
                            "Birim": birim_adi if birim_adi else "Belirtilmedi",
                            "Not": islem_notu,
                        }
                        st.session_state["gecmis"].insert(0, kayit)
                        st.success(
                            "✅ İşlem başarılı! Güncel stok:"
                            f" {st.session_state['stoklar'][secilen_model][secilen_renk][secilen_durum]}"
                        )
                        st.rerun()
                    else:
                        st.error(
                            f"❌ Yetersiz stok! Mevcut {secilen_durum} stok:"
                            f" {mevcut}"
                        )

elif menu == "İşlem Geçmişi & Raporlar":
    st.subheader("📋 Birim Dağıtım ve İşlem Geçmişi")

    if len(st.session_state["gecmis"]) > 0:
        df_gecmis = pd.DataFrame(st.session_state["gecmis"])
        st.dataframe(df_gecmis, use_container_width=True, hide_index=True)

        csv_veri = df_gecmis.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Raporu Excel/CSV Olarak İndir",
            data=csv_veri,
            file_name=(
                "kaman_toner_raporu_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            ),
            mime="text/csv",
        )
    else:
        st.info("Henüz bir birime toner çıkışı yapılmamış.")

st.markdown("---")
if st.button("🔒 Güvenli Oturumu Kapat"):
    st.session_state["giris_yapildi"] = False
    st.rerun()
