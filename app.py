import streamlit as st
import requests
import os

# -------------------------------
# Get Hugging Face API key from Streamlit secrets
HF_TOKEN = st.secrets["HF_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
# -------------------------------

def translate(text, src, tgt):
    payload = {
        "inputs": text,
        "parameters": {"src_lang": src, "tgt_lang": tgt}
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    try:
        return response.json()[0]['translation_text']
    except:
        return "Error: model is sleeping or overloaded. Try again."

# ---------- Streamlit UI ----------
st.set_page_config(page_title="AfricanaAI", page_icon="🌍", layout="centered")
st.title("🌍 AfricanaAI – African Language AI Prototype")
st.markdown(
    """
    **AfricanaAI** is a prototype AI tool for translating between African languages.
    Select source and target languages, type your text, and get instant translations.
    """
)

languages = {
    "Hausa": "hau_Latn",
    "Yoruba": "yor_Latn",
    "Igbo": "ibo_Latn",
    "Swahili": "swh_Latn",
    "Somali": "som_Latn",
    "Amharic": "amh_Ethi",
    "Fulfulde": "fuv_Latn"
}

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("From language:", list(languages.keys()))
with col2:
    tgt_lang = st.selectbox("To language:", list(languages.keys()))

text_input = st.text_area("Enter text to translate:", height=150)

if st.button("Translate"):
    if text_input.strip() == "":
        st.warning("Please enter text to translate.")
    elif src_lang == tgt_lang:
        st.info("Source and target languages are the same. Nothing to translate.")
    else:
        with st.spinner("Translating..."):
            result = translate(text_input, languages[src_lang], languages[tgt_lang])
        st.success("✅ Translation:")
        st.write(result)

st.markdown("---")
st.markdown("Prototype by **AfricanaAI** | Powered by Hugging Face NLLB-200 model")
