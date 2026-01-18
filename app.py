import streamlit as st
import boto3

# --- KONFİGÜRASYON ---
AGENT_ID = "J280YK35FY"
AGENT_ALIAS_ID = "IWAACDSX81" 
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

# Sayfa Ayarları (Açık ve Ferah Tema)
st.set_page_config(page_title="ZAKShield AI | Profesyonel Medikal Hukuk Paneli", page_icon="⚖️", layout="wide")

# MODERN & OKUNABİLİR TASARIM (Clean Light Theme)
st.markdown("""
    <style>
    /* Arka Plan: Açık Gri / Beyaz */
    .main { background: #fdfdfd; }
    
    /* Yazı Renkleri: Net Siyah ve Lacivert */
    h1, h2, h3, p, span { color: #1e293b !important; }
    
    /* Yan Menü (Sidebar) */
    [data-testid="stSidebar"] { background-color: #f1f5f9; border-right: 1px solid #e2e8f0; }
    
    /* Butonlar: Dikkat Çekici Lacivert */
    .stButton>button { 
        width: 100%; border-radius: 8px; 
        background: #2563eb; color: #ffffff !important; 
        font-weight: 700; border: none; height: 3.5em;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .stButton>button:hover { background: #1d4ed8; transform: translateY(-1px); }
    
    /* Kart Yapıları */
    .card {
        background: #ffffff; padding: 20px; border-radius: 12px;
        border: 1px solid #e2e8f0; box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR - NAVİGASYON VE KAYIT
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1063/1063376.png", width=80) # Geçici Logo
    st.title("ZAKShield AI")
    st.markdown("---")
    
    menu = st.radio("MENÜ", ["📊 Analiz Merkezi", "💳 Abonelik & Kayıt", "📂 Vaka Arşivi"])
    
    st.markdown("---")
    if menu == "💳 Abonelik & Kayıt":
        st.subheader("Üye Girişi")
        email = st.text_input("E-posta")
        password = st.text_input("Şifre", type="password")
        if st.button("Giriş Yap"):
            st.info("Kayıtlı kullanıcı bulunamadı. Lütfen abonelik paketlerini inceleyin.")
    else:
        st.info("Oturum: Misafir Kullanıcı")

# ANA İÇERİK
if menu == "📊 Analiz Merkezi":
    st.markdown("# 📊 Analiz Merkezi")
    st.markdown("##### Belge yükleyin veya vaka detaylarını girerek AI analizini başlatın.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # DOSYA YÜKLEME ALANI
        st.markdown("### 📄 Belge Yükleme")
        uploaded_file = st.file_uploader("Onam formu, resim veya PDF yükleyin", type=['pdf', 'png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            st.success(f"Dosya başarıyla yüklendi: {uploaded_file.name}")
            st.info("Dosya içeriği okunuyor ve AI motoruna aktarılıyor...")

        st.markdown("### ✍️ Metin Girişi")
        vaka_text = st.text_area("Vaka veya hukuki metni buraya yazın:", height=300)
        
        if st.button("STRATEJİK ANALİZİ BAŞLAT"):
            if vaka_text or uploaded_file:
                with st.spinner("AI Hukuk Algoritmaları Çalışıyor..."):
                    # Simüle edilmiş veya AWS Bedrock üzerinden gelen yanıt
                    try:
                        client = boto3.client(service_name='bedrock-agent-runtime', region_name=REGION,
                                            aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                        response = client.invoke_agent(agentId=AGENT_ID, agentAliasId=AGENT_ALIAS_ID,
                                                    sessionId="zak-pro-v2", inputText=vaka_text if vaka_text else "Dosya yüklendi.")
                        
                        res = "".join([event.get("chunk").get("bytes").decode() for event in response.get("completion") if event.get("chunk")])
                        st.markdown("---")
                        st.markdown("### ⚖️ Analiz Sonucu")
                        st.write(res)
                    except:
                        st.error("Bağlantı hatası. Lütfen metin girerek deneyiniz.")
            else:
                st.warning("Lütfen bir metin girin veya dosya yükleyin.")

    with col2:
        st.markdown("### 💳 Paketler")
        st.markdown("""
        <div class='card'>
            <h4>Standart Paket</h4>
            <p>Aylık 5 Analiz<br>Temel Mevzuat Taraması</p>
            <hr>
            <b>499 TL / Ay</b>
        </div>
        <div class='card'>
            <h4>Premium Paket</h4>
            <p>Sınırsız Analiz<br>PDF Rapor Çıktısı<br>Emsal Karar Desteği</p>
            <hr>
            <b style='color: #2563eb;'>1.299 TL / Ay</b>
        </div>
        """, unsafe_allow_html=True)
        st.button("ŞİMDİ ABONE OL")

elif menu == "💳 Abonelik & Kayıt":
    st.markdown("# 💎 Üyelik Yönetimi")
    st.write("Abonelik planınızı seçin ve profesyonel koruma kalkanını aktif edin.")
    # Burada Stripe veya Iyzico ödeme linkleri eklenebilir.

elif menu == "📂 Vaka Arşivi":
    st.markdown("# 📂 Geçmiş Analizler")
    st.write("Daha önce yaptığınız analizlere buradan ulaşabilirsiniz.")
    st.warning("Bu özelliği kullanmak için giriş yapmalısınız.")

# FOOTER
st.markdown("---")
st.caption("© 2026 ZAKShield AI | Medical Legal-Tech Solutions | Gizlilik Politikası | Kullanım Şartları")
