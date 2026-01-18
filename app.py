import streamlit as st
import boto3

# --- KONFİGÜRASYON ---
AGENT_ID = "J280YK35FY"
AGENT_ALIAS_ID = "IWAACDSX81" 
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

# Sayfa Ayarları (Artık MeDentShield!)
st.set_page_config(page_title="MeDentShield AI", page_icon="🛡️", layout="wide")

# Kurumsal Tasarım (Lacivert & Gümüş)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1c3d5a; color: white; font-weight: bold; }
    .stTextArea>div>div>textarea { border: 2px solid #1c3d5a; border-radius: 10px; }
    .sidebar .sidebar-content { background-image: linear-gradient(#1c3d5a, #2d5a88); color: white; }
    </style>
    """, unsafe_allow_html=True)

# Yan Panel
with st.sidebar:
    st.image("https://img.icons8.com/external-flatart-icons-flat-flatarticons/128/external-shield-protection-and-security-flatart-icons-flat-flatarticons-1.png", width=80)
    st.title("MeDentShield")
    st.info("Tüm Sağlık Branşları İçin Hukuki Koruma")
    menu = st.radio("İşlem Menüsü", ["Hukuki Analiz", "Onam Formu Üretici", "PDF/Belge Tara (Yakında)"])
    st.divider()
    st.caption("Geliştirici: Dr. Ulaş FIRINCIOĞULLARI")

# Ana Ekran
st.title("🛡️ MeDentShield AI")
st.markdown("### Sağlık Hukuku & Malpraktis Savunma Sistemi")

if menu == "Hukuki Analiz":
    user_input = st.text_area("Analiz edilecek metni veya rıza formunu buraya yapıştırın:", height=300, placeholder="Örn: Hastaya tüm riskler anlatıldı...")
    
    if st.button("ANALİZİ BAŞLAT"):
        if user_input:
            with st.spinner("MeDentShield Zekası Analiz Ediyor..."):
                try:
                    client = boto3.client(service_name='bedrock-agent-runtime', region_name=REGION,
                                        aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                    response = client.invoke_agent(agentId=AGENT_ID, agentAliasId=AGENT_ALIAS_ID,
                                                sessionId="medentshield-2026", inputText=user_input)
                    completion = "".join([event.get("chunk").get("bytes").decode() for event in response.get("completion") if event.get("chunk")])
                    st.markdown("---")
                    st.subheader("📋 Analiz Sonucu")
                    st.markdown(completion)
                except Exception as e:
                    st.error(f"Bağlantı Hatası: {e}")
        else:
            st.warning("Lütfen bir metin girin.")

elif menu == "Onam Formu Üretici":
    st.subheader("📝 Yeni Onam Formu Oluştur")
    branş = st.selectbox("Branş Seçin", ["Diş Hekimliği", "Genel Cerrahi", "Plastik Cerrahi", "Dermatoloji", "Diğer"])
    islem = st.text_input("Yapılacak İşlem/Ameliyat Adı")
    if st.button("Hukuka Uygun Form Oluştur"):
        st.info(f"🤖 {branş} - {islem} için örnek form taslağı hazırlanıyor... (Yakında aktif)")

st.divider()
st.caption("© 2026 MeDentShield - Profesyonel Hekim Koruma Teknolojileri")
