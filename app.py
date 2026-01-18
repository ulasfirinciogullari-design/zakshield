import streamlit as st
import boto3
import json

# --- KONFİGÜRASYON ---
MODEL_ID = "anthropic.claude-4-5-v1:0" # Sizin o devasa gücünüz: Claude 4.5
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

st.set_page_config(page_title="ZAKShield AI | Powered by Claude 4.5", page_icon="🛡️", layout="wide")

# PROFESYONEL FERAH TASARIM
st.markdown("""
    <style>
    .main { background: #fdfdfd; }
    h1, h2, h3, p, span { color: #111827 !important; font-family: 'Inter', sans-serif; }
    .stButton>button { 
        background: #000000; color: #ffffff !important; border-radius: 4px; 
        font-weight: 700; height: 3.5em; border: none; letter-spacing: 1px;
    }
    .stButton>button:hover { background: #333333; }
    .stTextArea textarea { background-color: #ffffff; color: #111827; border: 1px solid #d1d5db; font-size: 16px; }
    [data-testid="stSidebar"] { background-color: #f9fafb; border-right: 1px solid #e5e7eb; }
    .status-bar { padding: 10px; border-radius: 4px; background: #f0fdf4; color: #166534; font-weight: 600; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR - NAVİGASYON
with st.sidebar:
    st.markdown("### 🛡️ ZAKShield AI")
    st.markdown("<p style='font-size: 11px; color: #6b7280;'>MEDICAL LEGAL-TECH</p>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("SİSTEM MENÜSÜ", ["🛡️ Risk Analiz Paneli", "💳 Abonelik ve Kayıt", "📂 Vaka Arşivi"])
    st.divider()
    st.markdown("<div class='status-bar'>MODEL: CLAUDE 4.5 ACTIVE</div>", unsafe_allow_html=True)

# ANA PANEL
if menu == "🛡️ Risk Analiz Paneli":
    st.markdown("# 🛡️ Risk Analiz Paneli")
    st.markdown("##### Claude 4.5 motoru ile saniyeler içinde yüksek hassasiyetli tıbbi-hukuki analiz.")
    
    col_input, col_info = st.columns([2, 1])
    
    with col_input:
        uploaded_file = st.file_uploader("Belge Yükleyin (PDF/JPG)", type=['pdf', 'png', 'jpg'])
        vaka_input = st.text_area("Vaka Detayı veya Hukuki Soru:", height=350, placeholder="Hekim notlarını veya analiz edilecek onam formunu buraya girin...")
        
        if st.button("STRATEJİK ANALİZİ BAŞLAT"):
            if vaka_input:
                placeholder = st.empty()
                full_response = ""
                
                try:
                    client = boto3.client(service_name='bedrock-runtime', region_name=REGION,
                                        aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                    
                    # CLAUDE 4.5 STREAMING CALL
                    body = json.dumps({
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 4096,
                        "messages": [{"role": "user", "content": f"Sen tıbbi hukuk uzmanı ZAKShield AI'sın. Claude 4.5 yeteneklerini kullanarak şu vakayı analiz et, eksikleri bul ve hukuki koruma stratejisi öner: {vaka_input}"}],
                        "temperature": 0.4,
                    })
                    
                    response = client.invoke_model_with_response_stream(modelId=MODEL_ID, body=body)
                    
                    for event in response.get("body"):
                        chunk = event.get("chunk")
                        if chunk:
                            decoded = json.loads(chunk.get("bytes").decode())
                            if decoded.get("type") == "content_block_delta":
                                text = decoded.get("delta").get("text")
                                full_response += text
                                placeholder.markdown(full_response + "▌")
                    
                    placeholder.markdown(full_response)
                    st.success("Claude 4.5 Analizi Başarıyla Tamamlandı.")
                    st.download_button("Raporu İndir", full_response, "ZAKShield_Rapor.txt")
                except Exception as e:
                    st.error(f"Sistem Hatası: {e}")
            else:
                st.warning("Analiz için bir metin girilmelidir.")

    with col_info:
        st.markdown("### 💎 Neden Claude 4.5?")
        st.write("Sistemimiz, dünyanın en gelişmiş yapay zeka modeli Claude 4.5'i kullanır. Bu sayede karmaşık tıbbi davalarda hata payını minimize eder.")
        st.divider()
        st.markdown("#### ⚡ Hız ve Keskinlik")
        st.write("Saniyeler içinde milyonlarca sayfalık mevzuatı süzerek size en güvenli savunma hattını sunar.")

# FOOTER
st.markdown("---")
st.caption("© 2026 ZAKShield AI | Premium Medical Defense Platform")
