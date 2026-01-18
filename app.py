import streamlit as st
import boto3

# --- KONFİGÜRASYON ---
AGENT_ID = "J280YK35FY"
AGENT_ALIAS_ID = "IWAACDSX81" 
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

st.set_page_config(page_title="MediShield AI", page_icon="🛡️")

# Tasarım
st.title("🛡️ MediShield AI")
st.subheader("Sağlık Hukuku ve Malpraktis Analiz Portalı")

st.info("Merhaba Ulaş Bey, analiz edilecek rıza formu metnini aşağıya yapıştırın.")

# Kullanıcı Girişi
user_input = st.text_area("Hukuki metin girişi:", height=250, placeholder="Rıza formu veya hukuki sorunuzu buraya ekleyin...")

if st.button("Hukuki Analizi Başlat"):
    if user_input:
        with st.spinner("Claude 4.5 Sonnet mevzuatı tarıyor..."):
            try:
                # Amazon Bedrock Bağlantısı
                client = boto3.client(
                    service_name='bedrock-agent-runtime',
                    region_name=REGION,
                    aws_access_key_id=AWS_ACCESS_KEY,
                    aws_secret_access_key=AWS_SECRET_KEY
                )
                
                # Ajanı Tetikleme
                response = client.invoke_agent(
                    agentId=AGENT_ID,
                    agentAliasId=AGENT_ALIAS_ID,
                    sessionId="ulas-session-2026",
                    inputText=user_input
                )
                
                # Yanıtı Birleştirme
                event_stream = response.get("completion")
                completion = ""
                for event in event_stream:
                    chunk = event.get("chunk")
                    if chunk:
                        completion += chunk.get("bytes").decode()
                
                st.success("Analiz Raporu Hazır!")
                st.divider()
                st.markdown(completion)
                
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}")
    else:
        st.warning("Lütfen bir metin girin.")

st.divider()
st.caption("MediShield.ai - Hekim Haklarını Koruma Teknolojisi © 2026")
