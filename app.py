import streamlit as st
import boto3

# --- STRATEJİK YAPILANDIRMA ---
AGENT_ID = "J280YK35FY"
AGENT_ALIAS_ID = "IWAACDSX81" 
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

# Sayfa Ayarları
st.set_page_config(page_title="ZAKShield AI | Hekim Hakları Koruma", page_icon="🛡️", layout="wide")

# HOLDİNG VİZYON TASARIMI (Titanium & Obsidian Dark)
st.markdown("""
    <style>
    .main { background-color: #0d0d0d; }
    
    /* Buton: Metalik Keskinlik */
    .stButton>button { 
        width: 100%; border-radius: 2px; 
        background: linear-gradient(135deg, #2c3e50 0%, #000000 100%); 
        color: #d1d1d1; font-weight: 800; border: 1px solid #444; height: 3.5em;
        text-transform: uppercase; letter-spacing: 3px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        border: 1px solid #d1d1d1; color: #fff;
        box-shadow: 0 0 15px rgba(255,255,255,0.1);
    }
    
    /* Input Alanları */
    .stTextArea>div>div>textarea { 
        background-color: #151515; color: #fff; 
        border: 1px solid #333; border-radius: 4px;
    }
    
    /* Başlıklar */
    h1, h2, h3 { color: #ffffff !important; font-family: 'Inter', sans-serif; font-weight: 700; }
    .sidebar .sidebar-content { background-color: #050505; }
    
    /* Başarı Mesajı */
    .stAlert { background-color: #1a1a1a; border: 1px solid #2ecc71; color: #2ecc71; }
    </style>
    """, unsafe_allow_html=True)

# YAN PANEL (MARKA KİMLİĞİ)
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🛡️</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; letter-spacing: 2px;'>ZAKShield AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 11px;'>ZEKÂLI ANALİZ VE KORUMA</p>", unsafe_allow_html=True)
    st.divider()
    
    menu = st.selectbox("OPERASYON MERKEZİ", ["Hukuki Risk Analizi", "Vaka Arşivi", "Sistem Ayarları"])
    
    st.divider()
    st.markdown("#### 🏛️ Fırıncıoğulları Holding")
    st.caption("Geleceğin Hukuk Teknolojileri")

# ANA EKRAN
st.markdown(f"# 🛡️ {menu}")
st.markdown("---")

if menu == "Hukuki Risk Analizi":
    st.markdown("### 🔍 AI Destekli Mevzuat Taraması")
    vaka_input = st.text_area("Analiz edilecek metni veya hukuki soruyu buraya girin:", height=300, 
                             placeholder="ZAKShield AI algoritması için veri girişi bekliyor...")
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("ZIRHI DEVREYE SOK"):
            if vaka_input:
                with st.spinner("ZAKShield Veri Tabanı Taranıyor..."):
                    try:
                        client = boto3.client(service_name='bedrock-agent-runtime', region_name=REGION,
                                            aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                        response = client.invoke_agent(agentId=AGENT_ID, agentAliasId=AGENT_ALIAS_ID,
                                                    sessionId="zakshield-final", inputText=vaka_input)
                        
                        full_response = ""
                        for event in response.get("completion"):
                            chunk = event.get("chunk")
                            if chunk:
                                full_response += chunk.get("bytes").decode()
                        
                        st.session_state.res = full_response
                    except Exception as e:
                        st.error(f"Sistem Hatası: {e}")
            else:
                st.warning("Analiz için metin girişi gereklidir.")

    if 'res' in st.session_state:
        st.markdown("---")
        st.markdown("### 📋 Stratejik Analiz Raporu")
        st.success(st.session_state.res)

st.divider()
st.caption("© 2026 ZAKShield AI | Tüm Hakları Saklıdır.")
