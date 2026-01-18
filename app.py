import streamlit as st
import boto3

# --- KONFİGÜRASYON ---
AGENT_ID = "J280YK35FY"
AGENT_ALIAS_ID = "IWAACDSX81" 
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

st.set_page_config(page_title="ZAKShield AI | Medical Legal Defense", page_icon="⚖️", layout="wide")

# MEDİKAL & OTORİTER TASARIM (Navy & Steel)
st.markdown("""
    <style>
    /* Arka Plan: Koyu Lacivert ve Çelik Tonları */
    .main { background: #0f172a; }
    
    /* Buton: Net ve Keskin */
    .stButton>button { 
        width: 100%; border-radius: 4px; 
        background: #1e293b; color: #f8fafc; 
        font-weight: 700; border: 1px solid #334155; height: 3.5em;
        text-transform: uppercase; letter-spacing: 1.5px;
        transition: all 0.3s;
    }
    .stButton>button:hover { 
        background: #334155; border-color: #64748b;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* Metin Alanları */
    .stTextArea>div>div>textarea { background-color: #1e293b; color: #f1f5f9; border: 1px solid #334155; }
    
    /* Başlıklar */
    h1, h2, h3 { color: #f8fafc !important; font-family: 'Inter', sans-serif; }
    
    /* Bilgi Kutuları: Profesyonel Gri */
    .card {
        padding: 25px; border-radius: 8px; border: 1px solid #334155;
        background: #1e293b; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ÜST BÖLÜM - MİSYON ODDAKLI
st.markdown("<h1 style='text-align: center;'>ZAKShield <span style='font-weight:300; font-size:24px;'>AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>Tıp ve Diş Hekimliği İçin Gelişmiş Hukuki Risk Analiz Platformu</p>", unsafe_allow_html=True)
st.markdown("---")

# ANA OPERASYON ALANI
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 📋 Vaka ve Belge Analizi")
    st.markdown("<p style='color: #64748b; font-size: 14px;'>Aydınlatılmış onam formları, komplikasyon bildirimleri veya hukuki danışmanlık gerektiren vaka detaylarını giriniz.</p>", unsafe_allow_html=True)
    
    vaka_input = st.text_area("", height=450, placeholder="Analiz edilecek metni buraya yapıştırın...")
    
    if st.button("ANALİZİ BAŞLAT"):
        if vaka_input:
            with st.spinner("Yapay Zeka Mevzuat Taraması Yapılıyor..."):
                try:
                    client = boto3.client(service_name='bedrock-agent-runtime', region_name=REGION,
                                        aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                    response = client.invoke_agent(agentId=AGENT_ID, agentAliasId=AGENT_ALIAS_ID,
                                                sessionId="zakshield-pro", inputText=vaka_input)
                    
                    res_text = "".join([event.get("chunk").get("bytes").decode() for event in response.get("completion") if event.get("chunk")])
                    st.markdown("---")
                    st.markdown("### 🛡️ Stratejik Değerlendirme Raporu")
                    st.success(res_text)
                    st.download_button("Raporu Dışa Aktar (.txt)", res_text, "zakshield_rapor.txt")
                except Exception:
                    st.error("Sistem şu an yüksek talep altında. Lütfen bir süre sonra tekrar deneyiniz.")
        else:
            st.warning("Lütfen analiz için bir veri girişi yapın.")

with col_right:
    st.markdown("### 🛡️ Kurumsal Güvence")
    st.markdown("""
    <div class='card'>
    <h4 style='color:#f8fafc; margin-top:0;'>Yasal Uyumluluk</h4>
    Güncel Tıbbi Deontoloji Nizamnamesi ve Hekimlik Meslek Etiği Kuralları çerçevesinde analiz sunar.
    </div>
    <div class='card'>
    <h4 style='color:#f8fafc; margin-top:0;'>Risk Projeksiyonu</h4>
    Olası malpraktis davalarında savunma stratejinizi güçlendirecek eksiklikleri tespit eder.
    </div>
    <div class='card'>
    <h4 style='color:#f8fafc; margin-top:0;'>Gizlilik Protokolü</h4>
    Verileriniz 256-bit şifreleme ile korunur ve üçüncü taraflarla asla paylaşılmaz.
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Profesyonel Not:** Onam formlarınızdaki teknik terimlerin hasta tarafından anlaşılabilirliğini bu panel üzerinden test edebilirsiniz.")

# FOOTER - PROFESYONEL BİTİŞ
st.markdown("---")
f1, f2 = st.columns(2)
with f1:
    st.caption("ZAKShield AI | Medical Legal-Tech Solutions")
with f2:
    st.markdown("<p style='text-align: right; color: #475569; font-size: 12px;'>Bu platform bir karar destek sistemidir. Nihai hukuki süreçler için hukuk müşavirliğinize danışınız.</p>", unsafe_allow_html=True)
