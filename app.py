from datetime import datetime
import io
import os
import pandas as pd
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Kaman Belediyesi - Envanter Yönetim Paneli",
    page_icon="📦",
    layout="wide",
)

# --- DOSYA YOLLARI VE BAŞLANGIÇ AYARLARI ---
DOSYA_YOLU = "stok.csv"
LOG_YOLU = "islem_gecmisi.csv"


def standart_stok_olustur():
  data = []
  renkler = ["Siyah", "Mavi (Cyan)", "Kırmızı (Magenta)", "Sarı (Yellow)"]
  for model in ["UTAX 2507", "UTAX 2508"]:
    for renk in renkler:
      data.append([model, renk, "Dolu Toner", 10])
      data.append([model, renk, "Boş Toner", 2])
  for renk in renkler:
    data.append(["UTAX 3062", renk, "Dolu Toner", 5])
  for model in ["UTAX 4035", "UTAX 4532", "UTAX 4531"]:
    data.append([model, "Siyah", "Dolu Toner", 5])
  return pd.DataFrame(data, columns=["Model", "Renk", "Durum", "Stok"])


if not os.path.exists(DOSYA_YOLU):
  ornek_df = standart_stok_olustur()
  ornek_df.to_csv(DOSYA_YOLU, index=False)

df = pd.read_csv(DOSYA_YOLU)

if not os.path.exists(LOG_YOLU):
  bos_log = pd.DataFrame(
      columns=[
          "Tarih",
          "İşlem",
          "Model",
          "Renk",
          "Durum",
          "Miktar",
          "Birim",
          "Açıklama",
      ]
  )
  bos_log.to_csv(LOG_YOLU, index=False)

log_df = pd.read_csv(LOG_YOLU)
if "Birim" not in log_df.columns:
  log_df["Birim"] = "Genel"
  log_df.to_csv(LOG_YOLU, index=False)

# --- KURUMSAL GİRİŞ EKRANI (BELEDİYE AMBLEMİ İLE) ---
ADMIN_SIFRE = "1924.Blds"

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

  col1, col2, col3 = st.columns([1, 1.3, 1])
  with col2:
    # GitHub'a yüklediğimiz logo.png dosyasını doğrudan ekrana basıyoruz
    try:
        st.image("logo.png", width=90)
    except:
        st.markdown('<div class="emblem-badge">1924</div>', unsafe_allow_html=True)
        
    st.markdown(
        """
        <div class="login-container">
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

# =========================================================================
# ŞİFRE DOĞRU GİRİLDİKTEN SONRA AÇILAN ANA UYGULAMA
# =========================================================================

st.sidebar.title("🔐 Oturum Yönetimi")
if st.sidebar.button("Oturumu Kapat (Çıkış Yap)"):
  st.session_state["giris_yapildi"] = False
  st.rerun()

# --- ÜST PANEL & ÖZET METRİKLER ---
st.title("📦 Kurumsal Depo ve Envanter Yönetim Paneli")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)

toplam_dolu = df[df["Durum"] == "Dolu Toner"]["Stok"].sum()
toplam_bos = df[df["Durum"] == "Boş Toner"]["Stok"].sum()
kritik_df = df[(df["Durum"] == "Dolu Toner") & (df["Stok"] <= 2)]
toplam_kritik = len(kritik_df)
toplam_islem = len(log_df)

col_m1.metric("🟢 Toplam Dolu Toner", f"{toplam_dolu} Adet")
col_m2.metric("🟠 Toplam Boş Toner", f"{toplam_bos} Adet")
col_m3.metric(
    "🔴 Kritik Seviyedeki Dolu Tonerler",
    f"{toplam_kritik} Çeşit",
    delta_color="inverse",
)
col_m4.metric("📋 Toplam İşlem", f"{toplam_islem} Kayıt")

# --- KRİTİK STOK UYARI PANELİ (KIRMIZI ALAN) ---
if toplam_kritik > 0:
  st.error(
      "🚨 **KRİTİK STOK UYARISI!** Aşağıdaki tonerlerin stoğu tükenmek üzere"
      " (Kritik Seviye ≤ 2):"
  )
  for _, row in kritik_df.iterrows():
    st.markdown(
        f"- 🔴 **{row['Model']} ({row['Renk']})**: Kalan Dolu Toner Stoğu:"
        f" **{row['Stok']} adet**"
    )

st.markdown("---")

# --- ARAYÜZ SEKME YAPISI ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Stok Durumu",
    "📤 Manuel Çıkış / Ekle",
    "📊 Tüketim Analizi",
    "📋 Geçmiş & Raporlar",
])

# ------------------- TAB 1: STOK DURUMU & TOPLU YÜKLEME -------------------
with tab1:
  st.subheader("📦 Mevcut Stok Durumu ve Toplu Veri Yönetimi")

  arama_kelimesi = st.text_input(
      "🔎 Model veya Renk Ara:", placeholder="Örn: 2507, Siyah, Mavi..."
  )

  st.markdown("---")
  st.markdown("##### 📥 Excel/CSV ile Toplu Stok Yükle")
  yuklenen_dosya = st.file_uploader(
      "Dosya Seç", type=["csv", "xlsx"], key="toplu_yukle"
  )
  if yuklenen_dosya is not None:
    try:
      if yuklenen_dosya.name.endswith(".csv"):
        yeni_veri = pd.read_csv(yuklenen_dosya)
      else:
        yeni_veri = pd.read_excel(yuklenen_dosya)

      if all(k in yeni_veri.columns for k in ["Model", "Renk", "Durum", "Stok"]):
        yeni_veri.to_csv(DOSYA_YOLU, index=False)
        st.success("🎉 Stok listesi başarıyla güncellendi!")
        st.rerun()
      else:
        st.error(
            "❌ Dosya sütunları geçersiz! 'Model, Renk, Durum, Stok' olmalı."
        )
    except Exception as e:
      st.error(f"Hata oluştu: {e}")

  st.markdown("---")
  filtered_df = df.copy()
  if arama_kelimesi:
    filtered_df = filtered_df[
        filtered_df["Model"].str.contains(arama_kelimesi, case=False, na=False)
        | filtered_df["Renk"].str.contains(
            arama_kelimesi, case=False, na=False
        )
    ]

  modeller = filtered_df["Model"].unique()
  if len(modeller) == 0:
    st.warning("Aramanıza uygun stok kaydı bulunamadı.")
  else:
    for model in modeller:
      with st.expander(f"🖨️ {model} - Stok Detayları", expanded=True):
        model_tum_df = filtered_df[filtered_df["Model"] == model].reset_index(
            drop=True
        )
        st.dataframe(model_tum_df, use_container_width=True)

# ------------------- TAB 2: MANUEL ÇIKIŞ / EKLEME -------------------
with tab2:
  st.subheader("📤 Manuel Stok Hareketi ve Departman Notu")

  islem_tipi = st.radio(
      "İşlem Türü Seçin", ["Stok Çıkışı (Harca)", "Stok Ekle (Giriş Yap)"]
  )

  m_model = st.selectbox("Model Seç", df["Model"].unique(), key="mc_m")
  m_renk = st.selectbox(
      "Renk Seç", df[df["Model"] == m_model]["Renk"].unique(), key="mc_r"
  )
  mevcut_durumlar = df[(df["Model"] == m_model) & (df["Renk"] == m_renk)][
      "Durum"
  ].unique()
  m_durum = st.selectbox("Toner Durumu", mevcut_durumlar, key="mc_durum")
  m_adet = st.number_input("Adet", min_value=1, value=1, key="mc_adet")
  m_birim = st.text_input(
      "İlgili Birim / Departman",
      placeholder="Örn: Fen İşleri, Tapu...",
      key="mc_birim",
  )

  if st.button("İşlemi Kaydet"):
    idx = df[
        (df["Model"] == m_model)
        & (df["Renk"] == m_renk)
        & (df["Durum"] == m_durum)
    ].index
    if not idx.empty:
      if "Çıkışı" in islem_tipi:
        if df.loc[idx[0], "Stok"] >= m_adet:
          df.loc[idx[0], "Stok"] -= m_adet
          islem_adi = "Manuel Stok Çıkışı"
        else:
          st.error("❌ Yetersiz stok!")
          st.stop()
      else:
        df.loc[idx[0], "Stok"] += m_adet
        islem_adi = "Manuel Stok Girişi"

      df.to_csv(DOSYA_YOLU, index=False)
      yeni_log = pd.DataFrame(
          [[
              datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              islem_adi,
              m_model,
              m_renk,
              m_durum,
              m_adet,
              m_birim if m_birim else "Genel",
              "Manuel işlem",
          ]],
          columns=[
              "Tarih",
              "İşlem",
              "Model",
              "Renk",
              "Durum",
              "Miktar",
              "Birim",
              "Açıklama",
          ],
      )
      log_df = pd.concat([log_df, yeni_log], ignore_index=True)
      log_df.to_csv(LOG_YOLU, index=False)

      st.success(
          f"✅ İşlem başarılı: {m_model} ({m_renk} - {m_durum}) -> {m_adet} adet"
      )
      st.rerun()

# ------------------- TAB 3: TÜKETİM ANALİZİ VE GRAFİKLER -------------------
with tab3:
  st.subheader("📊 Tüketim ve Model Bazlı İstatistik Grafikleri")

  if log_df.empty:
    st.info("ℹ️ Grafik oluşturmak için henüz yeterli işlem geçmişi yok.")
  else:
    col_g1, col_g2 = st.columns(2)
    with col_g1:
      st.markdown("##### 🖨️ Model Bazlı Toplam Stok Dağılımı")
      model_stok = df.groupby("Model")["Stok"].sum()
      st.bar_chart(model_stok)

    with col_g2:
      st.markdown("##### 📦 Dolu vs Boş Toner Oranları")
      durum_stok = df.groupby("Durum")["Stok"].sum()
      st.bar_chart(durum_stok)

# ------------------- TAB 4: GEÇMİŞ & RAPORLAR -------------------
with tab4:
  st.subheader("📋 Geçmiş İşlem Kayıtları ve Raporlama")

  if not log_df.empty:
    st.markdown("##### 📅 Tarih Aralığı Filtresi")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
      baslangic_tarihi = st.date_input(
          "Başlangıç Tarihi", value=datetime.strptime("2026-01-01", "%Y-%m-%d")
      )
    with col_t2:
      bitis_tarihi = st.date_input("Bitiş Tarihi", value=datetime.today())

    filtrelenmis_log = log_df.copy()
    filtrelenmis_log["Tarih_Obj"] = pd.to_datetime(
        filtrelenmis_log["Tarih"], errors="coerce"
    )
    mask = (filtrelenmis_log["Tarih_Obj"].dt.date >= baslangic_tarihi) & (
        filtrelenmis_log["Tarih_Obj"].dt.date <= bitis_tarihi
    )
    filtrelenmis_log = filtrelenmis_log.loc[mask].drop(
        columns=["Tarih_Obj"], errors="ignore"
    )
  else:
    filtrelenmis_log = log_df.copy()

  log_arama = st.text_input(
      "🔍 Model, Birim veya İşlem Ara:",
      placeholder="Örn: Bilgi İşlem, 2507...",
  )
  if log_arama:
    filtrelenmis_log = filtrelenmis_log[
        filtrelenmis_log["Model"].str.contains(log_arama, case=False, na=False)
        | filtrelenmis_log["Birim"].str.contains(
            log_arama, case=False, na=False
        )
        | filtrelenmis_log["İşlem"].str.contains(
            log_arama, case=False, na=False
        )
    ]

  if filtrelenmis_log.empty:
    st.info("ℹ️ Seçilen tarih aralığında veya aramada kayıt bulunamadı.")
  else:
    st.dataframe(filtrelenmis_log, use_container_width=True)

    st.markdown("---")
    st.subheader("🗑️ Arşiv / Kayıt Yönetimi")
    secenekler = []
    for i, row in filtrelenmis_log.iterrows():
      secenekler.append(
          f"Kayıt {i}: [{row['Tarih']}] {row['Model']} - {row['Renk']} | Birim:"
          f" {row['Birim']} - {row['Miktar']} Adet"
      )

    secilen_satir_str = st.selectbox(
        "İşlem Yapılacak Kaydı Seçin", secenekler, key="arsiv_sec"
    )

    if st.button("Seçilen Kaydı Sil", type="primary"):
      secilen_idx = int(
          secilen_satir_str.split(":")[0].replace("Kayıt", "").strip()
      )
      log_df = log_df.drop(secilen_idx).reset_index(drop=True)
      log_df.to_csv(LOG_YOLU, index=False)
      st.success("✅ Kayıt silindi!")
      st.rerun()

  st.markdown("---")
  st.subheader("📥 Rapor İndirme Seçenekleri")
  col_r1, col_r2 = st.columns(2)

  with col_r1:
    log_csv = filtrelenmis_log.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📄 Filtrelenmiş CSV Raporu İndir",
        data=log_csv,
        file_name="filtrelenmis_islem_gecmisi.csv",
        mime="text/csv",
    )

  with col_r2:
    try:
      output = io.BytesIO()
      with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Mevcut Stok", index=False)
        filtrelenmis_log.to_excel(
            writer, sheet_name="Filtrelenmis Islem Gecmisi", index=False
        )
      excel_data = output.getvalue()

      st.download_button(
          label="📊 Detaylı Excel (.xlsx) Raporu İndir",
          data=excel_data,
          file_name="Stok_ve_Islem_Raporu.xlsx",
          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      )
    except Exception as e:
      st.error(f"Excel raporu oluşturulamadı: {e}")