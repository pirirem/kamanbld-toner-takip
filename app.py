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

# Veri Yapısı Başlangıcı (Boş tonersiz, sadece renk ve stoklar)
if "stoklar" not in st.session_state:
    st.session_state["stoklar"] = {
        "UTAX 2507": {
            "Siyah": 10,
            "Mavi (Cyan)": 10,
            "Kırmızı (Magenta)": 10,
            "Sarı (Yellow)": 10,
        },
        "UTAX 2508": {
            "Siyah": 8,
            "Mavi (Cyan)": 8,
            "Kırmızı (Magenta)": 8,
            "Sarı (Yellow)": 8,
        },
        "UTAX 3062": {
            "Siyah": 6,
            "Mavi (Cyan)": 6,
            "Kırmızı (Magenta)": 6,
            "Sarı (Yellow)": 6,
        },
        "UTAX 4035": {"Siyah": 12},
        "UTAX 4531": {"Siyah": 9},
        "UTAX 4532": {"Siyah": 7},
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

# Kritik Stok Alarm Kontrolü (Stoku 3 ve altı olanlar)
kritik_urunler = []
for m_ad, r_dict in st.session_state["stoklar"].items():
    for r_ad, st_adet in r_dict.items():
        if st_adet <= 3:
            kritik_urunler.append(f"⚠️ **{m_ad} ({r_ad})**: {st_adet} adet kaldı!")

if kritik_urunler:
    st.error(
        "🚨 **Kritik Stok Alarmı:** Aşağıdaki tonerlerin stoku azalmıştır!\n\n"
        + "\n".join(kritik_urunler)
    )

# Üst Özet Hesaplamaları
toplam_stok = sum(
    sum(stoklar_dict.values())
    for stoklar_dict in st.session_state["stoklar"].values()
)
toplam_yazici_modeli = len(st.session_state["stoklar"])

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("📦 Toplam Dolu Toner Stoğu", toplam_stok)
col_m2.metric("🖨️ Takip Edilen Model", f"{toplam_yazici_modeli} Çeşit")
col_m3.metric("🏢 Kayıtlı Birim Dağıtımı", len(st.session_state["gecmis"]))

st.markdown("---")

menu = st.sidebar.selectbox(
    "Menü", ["Stok Durumu & Dağıtım", "İşlem Geçmişi & Raporlar"]
)

if menu == "Stok Durumu & Dağıtım":
    st.subheader("📦 Mevcut Stok Durumu (Yazıcı Bazlı Detaylar)")
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

    st.markdown("---")
    st.subheader("🔄 Stok Ekleme / Çıkarma ve Birime Teslim")

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
            "Teslim Edilen Birim", placeholder="Örn: Yazı İşleri Müdürlüğü"
        )
        cihaz_serino = st.text_input(
            "Cihaz Lokasyonu / Seri No (İsteğe bağlı)",
            placeholder="Örn: Oda 203 / Cihaz #4",
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
                        "Cihaz/Lokasyon": (
                            cihaz_serino if cihaz_serino else "-"
                        ),
                        "Not": islem_notu,
                    }
                    st.session_state["gecmis"].insert(0, kayit)
                    st.success(
                        "✅ İşlem başarılı! Güncel stok:"
                        f" {st.session_state['stoklar'][secilen_model][secilen_renk]}"
                    )
                    st.rerun()
                else:
                    st.error(f"❌ Yetersiz stok! Mevcut stok: {mevcut}")

elif menu == "İşlem Geçmişi & Raporlar":
    st.subheader("📋 Birim Dağıtım ve İşlem Geçmişi")

    if len(st.session_state["gecmis"]) > 0:
        df_gecmis = pd.DataFrame(st.session_state["gecmis"])
        st.dataframe(df_gecmis, use_container_width=True, hide_index=True)

        # Excel / CSV Rapor İndirme
        csv_veri = df_gecmis.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Raporu Excel/CSV Olarak İndir (Yedekle)",
            data=csv_veri,
            file_name=(
                "kaman_toner_raporu_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            ),
            mime="text/csv",
        )

        st.markdown("---")
        st.subheader("📄 Resmi Toner Teslim Tutanağı Öngörünümü")
        secilen_islem_index = st.selectbox(
            "Tutanak oluşturulacak işlemi seçin:",
            range(len(st.session_state["gecmis"])),
            format_func=lambda x: (
                f"{st.session_state['gecmis'][x]['Tarih']} -"
                f" {st.session_state['gecmis'][x]['Birim']} -"
                f" {st.session_state['gecmis'][x]['Model']}"
                f" ({st.session_state['gecmis'][x]['Renk']})"
            ),
        )

        secilen_kayit = st.session_state["gecmis"][secilen_islem_index]

        # Tutanak Kutusu
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.9); padding: 25px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2); color: white;">
                <h3 style="text-align: center; margin-bottom: 5px;">KAMAN BELEDİYESİ</h3>
                <h4 style="text-align: center; color: #94a3b8; margin-top: 0;">BİLGİ İŞLEM BİRİMİ - TONER TESLIM TUTANAĞI</h4>
                <hr style="border-color: rgba(255,255,255,0.2);">
                <p><b>Tarih / Saat:</b> {secilen_kayit['Tarih']}</p>
                <p><b>Teslim Alan Birim:</b> {secilen_kayit['Birim']}</p>
                <p><b>Cihaz / Lokasyon:</b> {secilen_kayit['Cihaz/Lokasyon']}</p>
                <p><b>Malzeme Detayı:</b> {secilen_kayit['Model']} - {secilen_kayit['Renk']} ({secilen_kayit['Miktar']} Adet)</p>
                <p><b>Açıklama:</b> {secilen_kayit['Not'] if secilen_kayit['Not'] else '-'}</p>
                <br><br>
                <div style="display: flex; justify-content: space-between; margin-top: 40px;">
                    <div><b>Teslim Eden (Bilgi İşlem):</b><br><br>İmza: ........................</div>
                    <div><b>Teslim Alan (Birim Yetkilisi):</b><br><br>İmza: ........................</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Henüz bir birime toner çıkışı yapılmamış.")

st.markdown("---")
if st.button("🔒 Güvenli Oturumu Kapat"):
    st.session_state["giris_yapildi"] = False
    st.rerun()
