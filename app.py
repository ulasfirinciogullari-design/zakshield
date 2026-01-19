import streamlit as st
import boto3
import json

# AWS Bağlantısı
client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1',
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
)

st.set_page_config(page_title="ZAKShield AI", page_icon="🛡️")
st.title("🛡️ ZAKShield AI")
st.subheader("Hukuki Koruma ve Mevzuat Asistanı")

with st.sidebar:
    st.header("Veri Merkezi")
    uploaded_file = st.file_uploader("Dosya Yükle", type=['pdf', 'txt'])

prompt = st.text_input("Analiz edilmesini istediğiniz konuyu yazın:")

if prompt:
    # Kimlik bilgisi içermeyen profesyonel direktif
    system_instructions = (
        "Sen ZAKShield AI'sın. Uzmanlık alanın sağlık hukuku ve mevzuat analizidir. "
        "Kullanıcıya 'erişimim yok' demek yerine, elindeki verilerle en güvenli "
        "ve profesyonel hukuki mantığı sunarsın."
    )
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "system": system_instructions,
        "messages": [{"role": "user", "content": prompt}]
    })
    
    try:
        response = client.invoke_model(body=body, modelId="anthropic.claude-3-5-sonnet-20240620-v1:0")
        response_body = json.loads(response.get('body').read())
        
        st.write("### 🛡️ ZAKShield Analizi:")
        st.write(response_body['content'][0]['text'])
    except Exception as e:
        st.error(f"Sistem hatası: {e}")
