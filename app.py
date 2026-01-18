import streamlit as st
import boto3

# --- STRATEJİK KONFİGÜRASYON ---
AGENT_ID = "J280YK35FY"
AGENT_ALIAS_ID = "IWAACDSX81" 
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

# Sayfa Yapılandırması
st.set_page_config(page_title="VENUShield AI | Elite Medical Defense", page_icon="🛡️", layout="wide")

# HOLDING PRESTİJ TASARIMI (Custom CSS)
st.markdown("""
    <style>
    /* Ana Arka Plan: Derin Antrasit */
    .main { background-color: #0a0a0b; }
    
    /* Buton: Rose Gold Gradient */
    .stButton>button { 
        width: 100%; border-radius: 4px; 
        background: linear-gradient(135deg, #b79471 0%, #8c6e51 100%); 
        color: #ffffff; font-weight: 700; border: none; height: 3.8em;
        text-transform: uppercase; letter-spacing: 2px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover { 
        box-shadow: 0 0 25px rgba(183, 148, 113, 0.4); 
        transform: translateY(-2px);
    }
    
    /* Metin Alanı: Cam Efekti */
    .stTextArea>div>div>textarea { 
        background-color: rgba(255, 255, 255, 0.03); 
        color: #e0e0e0; border: 1px solid #3d3d3d; border-radius: 8px;
        font-family: 'Inter', sans-serif; font-size: 16px;
    }
    
    /* Başlıklar ve Sidebar */
    h1, h2, h3 { color: #b79471 !important; font-family: 'Georgia', serif; letter-spacing: 1px; }
    .css-1d391kg { background-color: #000000; border-right: 1px solid #1a1a1a; }
    
    /* Bilgi Kutuları */
    .stAlert { background-color: rgba(183, 148, 113, 0.1); border: 1px solid #b79471; color: #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR (HOLDING MÜHRÜ)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>🛡️</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>VENUShield <span style='font-size: 14px; vertical-align: middle;'>AI</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8c6e51; font-size: 12px; letter-spacing: 2px;'>HEKİM HUKUKU MUHAFIZI</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### 🏛️ Komuta Merkezi")
    choice = st.radio("", ["Hukuki Analiz Paneli", "Onam Formu Taslağı", "Dava Risk Ölçer", "Holding Destek"])
    
    st.divider()
    st.caption("Fırıncıoğulları Holding iştirakidir.")
    st.caption("v1.0.2 - Premium Edition")

# ANA PANEL
if choice == "Hukuki Analiz Paneli":
    st.markdown("### 🔍 Stratejik Hukuki Analiz")
    st.markdown("<p style='color: #888;'>Analiz edilecek vaka detayını, rıza metnini veya hukuki sorunuzu giriniz.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_area("", height=400, placeholder="Vaka detaylarını buraya profesyonel bir dille aktarın...")
    
    with col2:
        st.markdown("#### 💎 VENUShield Güvencesi")
        st.write("Yapay zekamız saniyeler içinde binlerce Yargıtay emsal kararını ve güncel mevzuatı tarayarak size en güvenli rotayı çizer.")
        
        st.markdown("---")
        if st.button("ANALİZİ BAŞLAT"):
            if user_input:
                with st.spinner("AI Algoritmaları Taranıyor..."):
                    try:
                        client = boto3.client(service_name='bedrock-agent-runtime', region_name=REGION,
                                            aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                        response = client.invoke_agent(agentId=AGENT_ID, agentAliasId=AGENT_ALIAS_ID,
                                                    sessionId="venus-shield-session", inputText=user_input)
                        
                        completion = ""
                        for event in response.get("completion"):
                            chunk = event.get("chunk")
                            if chunk:
                                completion += chunk.get("bytes").decode()
                        
                        st.session_state.last_analysis = completion
                    except Exception as e:
                        st.error(f"Erişim Hatası: Lütfen sistem yöneticisiyle iletişime geçin. ({e})")
            else:
                st.warning("Lütfen bir veri girişi yapın.")

    if 'last_analysis' in st.session_state:
        st.markdown("---")
        st.markdown("### 📋 AI Analiz Sonucu ve Savunma Stratejisi")
        st.success(st.session_state.last_analysis)
        st.download_button("Raporu PDF Olarak İndir", data=st.session_state.last_analysis, file_name="VENUShield_Analiz.txt")

# ALT BİLGİ
st.markdown("<br><br><hr><p style='text-align: center; color: #555; font-size: 11px;'>© 2026 VENUShield AI. Bu platform bir yapay zeka danışmanlık sistemidir. Nihai kararlar için lütfen hukuk müşavirinize danışın.</p>", unsafe_allow_html=True)
