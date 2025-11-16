import streamlit as st
import requests
import time

# -----------------------------------------
# Load Hugging Face Token from Streamlit Secrets
HF_TOKEN = st.secrets["HF_TOKEN"]

# More stable and faster multilingual model
API_URL = "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt"

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
# -----------------------------------------


# Retry logic for stable translation
def translate(text, src, tgt, retries=3):
    payload = {
        "inputs": text,
        "parameters": {"src_lang": src, "tgt_lang": tgt}
    }

    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
            json_resp = response.json()

            # Successful translation
            if isinstance(json_resp, list) and "translation_text" in json_resp[0]:
                return json_resp[0]["translation_text"]

            # Model loading or error
            if "error" in json_resp:
                if "loading" in json_resp["error"].lower():
                    time.sleep(4)  # wait for model to warm
                    continue  # retry
                else:
                    return f"Model error: {json_resp['error']}"

        except Exception as e:
            time.sleep(3)

    return "⚠️ Model is warming up or busy. Please try again."


# -----------------------------------------
# STREAMLIT UI
# -----------------------------------------
st.set_page_config(page_title="AfricanaAI", page_icon="🌍", layout="centered")

st.title("🌍 AfricanaAI – African Language AI Prototype")
st.markdown("""
This is a stable prototype of **AfricanaAI**, designed for multilingual African language translation  
with automatic retries, intelligent error handling, and improved reliability.
""")

languages = {
    "Hausa": "hau_XX",
    "Yoruba": "yor_XX",
    "Igbo": "ibo_XX",
    "Swahili": "swh_KE",
    "Amharic": "amh_XX",
    "Somali": "som_XX",
    "Arabic": "ar_AR",
    "English": "en_XX"
}

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("From language:", list(languages.keys()))
with col2:
    tgt_lang = st.selectbox("To language:", list(languages.keys()))

text_input = st.text_area("Enter text to translate:", height=150)

if st.button("Translate"):
    if text_input.strip() == "":
        st.warning("Please type something to translate.")
    else:
        with st.spinner("Processing (warming model if needed)..."):
            result = translate(text_input, languages[src_lang], languages[tgt_lang])

        st.success("Translation:")
        st.write(result)

st.markdown("---")
st.caption("Prototype by AfricanaAI | Powered by Hugging Face")
