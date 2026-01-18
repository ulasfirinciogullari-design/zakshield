import streamlit as st
import boto3
import base64
import json

# --- AWS HOLDİNG ERİŞİMİ ---
AGENT_ID = "J280YK35FY"
AGENT_ALIAS_ID = "IWAACDSX81" 
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

# Sayfa Yapılandırması
st.set_page_config(page_title="ZAKShield | Medikal Hukuk Koruma", page_icon="🛡️", layout="wide")

# SES MOTORU (Hata Toleranslı)
def seslendir(metin):
    try:
        polly = boto3.client('polly', region_name=REGION, 
                             aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        response = polly.synthesize_speech(Text=metin[:600], OutputFormat='mp3', VoiceId='Filiz')
        audio_content = response['AudioStream'].read()
        b64_audio = base64.b64encode(audio_content).decode()
        audio_html = f'<audio autoplay><source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)
    except:
        pass

# KURUMSAL TASARIM
st.markdown("""
    <style>
    .main { background: #ffffff; }
    h1, h2, h3 { color: #0f172a !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    .stButton>button { 
        background: #1e293b; color: #fff !important; border-radius: 8px; font-weight: 700; height: 3.5em; border: none;
    }
    [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #f1f5f9; }
    .stat-card { padding: 20px; border-radius: 12px; border: 1px solid #f1f5f9; background: #ffffff; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# YAN PANEL
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>ZAKShield</h2>", unsafe_allow_html=True)
    st.divider()
    sayfa = st.radio("MENÜ", ["🏛️ Dashboard", "📊 Risk Analizi", "📂 Vaka Arşivi", "👤 Profil Ayarları"])
    st.divider()
    st.info("**Oturum Açan:**\nDr. Ulaş Fırıncıoğulları")

# SAYFALAR
if sayfa == "🏛️ Dashboard":
    st.markdown("# 🏛️ Dashboard")
    st.markdown("##### Hoş geldiniz Dr. Ulaş. İşte kliniğinizin dijital güvenlik özeti.")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown("<div class='stat-card'><b>Toplam Analiz</b><br>312</div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-card'><b>Risk Seviyesi</b><br><span style='color:green'>Güvenli</span></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-card'><b>Sistem Hızı</b><br>0.3s</div>", unsafe_allow_html=True)
    st.markdown("### 🔔 Son Güncellemeler")
    st.success("✅ Yargıtay'ın güncel malpraktis kararları motorumuza işlendi.")

elif sayfa == "📊 Risk Analizi":
    st.markdown("# 📊 Medikal Risk Analizi")
    vaka = st.text_area("Vaka Notları / Onam Formu:", height=400, placeholder="Analiz edilecek içeriği buraya aktarın...")
    if st.button("STRATEJİK ANALİZİ BAŞLAT"):
        if vaka:
            with st.spinner("ZAKShield Verileri İşliyor..."):
                try:
                    client = boto3.client(service_name='bedrock-agent-runtime', region_name=REGION,
                                        aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                    response = client.invoke_agent(agentId=AGENT_ID, agentAliasId=AGENT_ALIAS_ID, sessionId="live-session", inputText=vaka)
                    res = "".join([e.get("chunk").get("bytes").decode() for e in response.get("completion") if e.get("chunk")])
                    st.markdown("### 📋 Analiz Raporu")
                    st.info(res)
                    seslendir(res)
                except:
                    st.error("Bağlantı şu an yoğun. Lütfen tekrar deneyiniz.")

elif sayfa == "📂 Vaka Arşivi":
    st.markdown("# 📂 Vaka Arşivi")
    st.table({"Tarih": ["19.01.2026", "18.01.2026"], "Vaka": ["İmplant", "Kanal"], "Risk": ["Yok", "Düşük"]})

elif sayfa == "👤 Profil Ayarları":
    st.markdown("# 👤 Profil Ayarları")
    st.text_input("Ad Soyad", "Dr. Ulaş Fırıncıoğulları")
    st.text_input("Klinik Adı", "ZAK Medical Center")
    st.button("Güncelle")

st.markdown("---")
st.caption("© 2026 ZAKShield AI | Professional Medical-Legal-Tech Platform")
