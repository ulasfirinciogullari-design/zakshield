import streamlit as st
import boto3

# --- AWS OPERASYON MERKEZİ ---
AGENT_ID = "J280YK35FY"
# ÖNEMLİ: AWS Konsolunda 'Aliases' sekmesinden oluşturduğunuz ID'yi buraya yazın. 
# Eğer oluşturmadıysanız, Konsol'dan bir Alias oluşturup adını 'PRO' yapabilirsiniz.
AGENT_ALIAS_ID = "IWAACDSX81" 
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

st.set_page_config(page_title="ZAKShield AI | Medical Legal Defense", page_icon="🛡️", layout="wide")

# FERAH MEDİKAL TASARIM (High Contrast)
st.markdown("""
    <style>
    .main { background: #ffffff; }
    h1, h2, h3, p, span { color: #0f172a !important; font-family: 'Inter', sans-serif; }
    .stButton>button { 
        background: #2563eb; color: #ffffff !important; border-radius: 4px; 
        font-weight: 700; height: 3.5em; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background: #1e4ed8; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); }
    .stTextArea textarea { background-color: #f8fafc; color: #0f172a; border: 1px solid #e2e8f0; font-size: 16px; }
    [data-testid="stSidebar"] { background-color: #f1f5f9; border-right: 1px solid #e2e8f0; }
    .agent-status { padding: 10px; border-radius: 6px; background: #f0f9ff; border: 1px solid #bae6fd; color: #0369a1; font-weight: 600; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("## 🛡️ ZAKShield AI")
    st.caption("Medical Legal-Tech Solutions")
    st.divider()
    menu = st.radio("OPERASYON MERKEZİ", ["📊 Analiz Paneli", "💳 Abonelik / Kayıt", "📂 Vaka Arşivi"])
    st.divider()
    st.markdown(f"<div class='agent-status'>US-EAST-1 AGENT ACTIVE<br><small>{AGENT_ID}</small></div>", unsafe_allow_html=True)

# ANA PANEL
if menu == "📊 Analiz Paneli":
    st.markdown("# 🛡️ Analiz Paneli")
    st.markdown("##### Claude 4.5 tabanlı yapay zeka ajanı ile medikal risklerinizi minimize edin.")
    
    col_in, col_side = st.columns([2, 1])
    
    with col_in:
        st.markdown("### 📄 Metin veya Belge Analizi")
        vaka_input = st.text_area("", height=450, placeholder="Analiz edilecek vaka içeriğini, onam formunu veya hukuki metni buraya yapıştırın...")
        
        if st.button("ANALİZİ BAŞLAT"):
            if vaka_input:
                with st.spinner("ZAKShield Ajanı Verileri İşliyor..."):
                    try:
                        client = boto3.client(service_name='bedrock-agent-runtime', region_name=REGION,
                                            aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                        
                        response = client.invoke_agent(
                            agentId=AGENT_ID,
                            agentAliasId=AGENT_ALIAS_ID,
                            sessionId="zakshield-live-session",
                            inputText=vaka_input
                        )
                        
                        full_response = ""
                        for event in response.get("completion"):
                            chunk = event.get("chunk")
                            if chunk:
                                full_response += chunk.get("bytes").decode()
                        
                        st.markdown("---")
                        st.markdown("### 📋 Stratejik Analiz Sonucu")
                        st.info(full_response)
                        st.success("Claude 4.5 Analizi Başarıyla Tamamlandı.")
                    except Exception as e:
                        st.error(f"Bağlantı Hatası: {e}")
                        st.info("İpucu: AWS Konsolunda 'Alias ID' bilgisinin güncelliğini kontrol edin.")
            else:
                st.warning("Analiz için bir veri girişi yapılması gerekmektedir.")

    with col_side:
        st.markdown("### ⚖️ Analiz Kapsamı")
        st.write("Sistemimiz aşağıdaki alanlarda derinlemesine tarama yapar:")
        st.markdown("""
        * **KVKK Uyumluluğu**
        * **Malpraktis Riskleri**
        * **Onam Formu Eksiklikleri**
        * **Savunma Stratejisi**
        """)
        st.divider()
        st.markdown("#### 💎 Üyelik Avantajı")
        st.caption("Premium üyelerimiz daha derinlemesine vaka arşivi taraması yapabilir.")

# FOOTER
st.markdown("---")
st.caption("© 2026 ZAKShield AI | Powered by Fırıncıoğulları Technology")
