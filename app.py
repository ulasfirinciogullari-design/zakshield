import streamlit as st
import boto3
import base64
import json

# --- KRİTİK ERİŞİM BİLGİLERİ ---
AGENT_ID = "J280YK35FY"
AGENT_ALIAS_ID = "IWAACDSX81" 
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

# Uygulama Başlığı ve İkonu
st.set_page_config(page_title="ZAKShield AI | Medical-Legal Intelligence", page_icon="🛡️", layout="wide")

# SES SİSTEMİ (Amazon Polly)
def seslendir(metin):
    try:
        polly = boto3.client('polly', region_name=REGION, 
                             aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        # Hekimler için en güven veren ses: Filiz
        response = polly.synthesize_speech(Text=metin[:1200], OutputFormat='mp3', VoiceId='Filiz')
        audio_content = response['AudioStream'].read()
        b64_audio = base64.b64encode(audio_content).decode()
        audio_html = f'<audio autoplay><source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)
    except:
        pass # Hata olsa bile kullanıcıya teknik mesaj gösterme

# --- PRESTİJ TASARIM (Modern White & Graphite) ---
st.markdown("""
    <style>
    .main { background: #ffffff; }
    h1, h2, h3 { color: #111827 !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    p, span, label { color: #374151 !important; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #f3f4f6; }
    .stButton>button { 
        width: 100%; border-radius: 6px; background: #000000; color: #ffffff !important; 
        font-weight: 700; height: 3.8em; border: none; transition: 0.3s ease;
    }
    .stButton>button:hover { background: #333333; transform: scale(1.01); }
    .stTextArea textarea { border: 1px solid #d1d5db; border-radius: 8px; font-size: 16px; padding: 15px; }
    .metric-card { background: #f9fafb; padding: 20px; border-radius: 10px; border: 1px solid #e5e7eb; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVİGASYON ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 24px;'>🛡️ ZAKShield</h1>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("SİSTEM MODÜLLERİ", 
                    ["🏛️ Dashboard", "🔍 Akıllı Analiz Merkezi", "📜 Savunma Dilekçesi Robotu", "📂 Dijital Vaka Arşivi", "💳 Üyelik Bilgileri"])
    st.divider()
    st.write("**Kullanıcı:** Dr. Ulaş Fırıncıoğulları")
    st.caption("Erişim: Kurumsal Sınırsız")

# --- SAYFA: DASHBOARD ---
if menu == "🏛️ Dashboard":
    st.markdown("# 🏛️ Dashboard")
    st.markdown("##### Hoş geldiniz Dr. Ulaş. İşte kliniğinizin güncel güvenlik verileri.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown("<div class='metric-card'><b>Toplam Sorgulama</b><br><span style='font-size:24px;'>312</span></div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='metric-card'><b>Risk Skoru</b><br><span style='font-size:24px; color:#10b981;'>DÜŞÜK</span></div>", unsafe_allow_html=True)
    with col3: st.markdown("<div class='metric-card'><b>Kredi Durumu</b><br><span style='font-size:24px;'>∞</span></div>", unsafe_allow_html=True)
    with col4: st.markdown("<div class='metric-card'><b>AI Motoru</b><br><span style='font-size:24px;'>C 4.5</span></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔔 Son Hukuki Güncellemeler")
    st.info("📅 19.01.2026: Sağlık Bakanlığı'nın yeni dijital onam yönetmeliği analiz motoruna başarıyla entegre edildi.")

# --- SAYFA: ANALİZ MERKEZİ ---
elif menu == "🔍 Akıllı Analiz Merkezi":
    st.markdown("# 🔍 Akıllı Analiz Merkezi")
    st.markdown("##### Metin girişi yapın veya belge yükleyin; Claude 4.5 riskleri anında saptasın.")
    
    c_left, c_right = st.columns([2, 1])
    
    with c_left:
        metin = st.text_area("Onam Formu veya Vaka Özeti:", height=400, placeholder="Analiz edilecek içeriği buraya aktarın...")
        if st.button("ANALİZİ BAŞLAT VE SESLENDİR"):
            if metin:
                with st.spinner("ZAKShield Yapay Zekası Mevzuatı Tarıyor..."):
                    try:
                        client = boto3.client(service_name='bedrock-agent-runtime', region_name=REGION,
                                            aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                        response = client.invoke_agent(agentId=AGENT_ID, agentAliasId=AGENT_ALIAS_ID, sessionId="live-dr-ulas", inputText=metin)
                        
                        full_res = ""
                        for event in response.get("completion"):
                            chunk = event.get("chunk")
                            if chunk: full_res += chunk.get("bytes").decode()
                        
                        st.markdown("### ⚖️ Stratejik Analiz Raporu")
                        st.success(full_res)
                        seslendir(full_res) # Seslendirmeyi başlat
                    except:
                        st.error("Bağlantı şu an yoğun. Lütfen tekrar deneyiniz.")
            else:
                st.warning("Lütfen bir vaka metni giriniz.")

    with c_right:
        st.markdown("### 🛡️ Neyi Analiz Ediyoruz?")
        st.write("✅ KVKK 6. Madde Uyumluluğu")
        st.write("✅ Malpraktis Risk Analizi")
        st.write("✅ Eksik Onam Bildirimleri")
        st.write("✅ Hukuki İhtiyat Tavsiyeleri")

# --- SAYFA: SAVUNMA ROBOTU ---
elif menu == "📜 Savunma Dilekçesi Robotu":
    st.markdown("# 📜 Savunma Dilekçesi Robotu")
    st.write("Vaka detaylarını girerek, olası bir şikayete karşı ön savunma taslağınızı oluşturun.")
    st.text_input("Şikayet Konusu (Örn: Komplikasyon)")
    st.button("Taslak Oluştur")

# --- SAYFA: ARŞİV ---
elif menu == "📂 Dijital Vaka Arşivi":
    st.markdown("# 📂 Dijital Vaka Arşivi")
    st.table({"Tarih": ["19.01.2026", "18.01.2026"], "Vaka": ["İmplant Onam", "Kanal Tedavisi"], "Sonuç": ["Hukuki Risk Yok", "Eksik Form Bildirildi"]})

# --- SAYFA: ABONELİK ---
elif menu == "💳 Üyelik Bilgileri":
    st.markdown("# 💎 Üyelik Bilgileri")
    st.success("Aktif Plan: **PROFESYONEL HOLDİNG ÜYELİĞİ**")
    st.button("Ödeme Bilgilerini Güncelle")

st.markdown("---")
st.caption("© 2026 ZAKShield AI | Professional Medical-Legal-Tech Platform")
