import streamlit as st
from groq import Groq
import requests

# 1. SETUP & KEYS
GROQ_API_KEY = "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"
HF_TOKEN = "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"

# 2. ULTRA PREMIUM INTERFACE CONFIG
st.set_page_config(page_title="Astro AI", page_icon="🚀", layout="wide")

# Custom CSS for Neon Dark Look
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border-right: 2px solid #00f2fe;
    }
    .stTextInput input, .stChatInput textarea {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #00f2fe !important;
    }
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        color: black; font-weight: bold; border-radius: 20px;
    }
    /* Text Visibility Fix */
    p, span, label { color: white !important; font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h1 style='color: #00f2fe;'>🚀 ASTRO AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    mode = st.radio("CHOOSE MODULE", ["💬 AI CHATBOT", "🎨 IMAGE STUDIO"])
    st.markdown("---")
    st.success("Status: Online 🟢")

# --- CHATBOT SECTION ---
if mode == "💬 AI CHATBOT":
    st.markdown("<h2 style='color: #00f2fe;'>Astro Smart Assistant</h2>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask anything (English/Roman Urdu)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Astro AI. Reply in the same language the user uses (Roman Urdu/English)."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile", 
            )
            res = response.choices.message.content
            with st.chat_message("assistant"):
                st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except:
            st.error("AI is thinking hard. Please refresh or try again!")

# --- IMAGE SECTION ---
else:
    st.markdown("<h2 style='color: #4facfe;'>Astro Image Creator</h2>", unsafe_allow_html=True)
    prompt_img = st.text_input("Describe your imagination:")
    
    if st.button("Generate Now"):
        if prompt_img:
            with st.spinner("Creating..."):
                API_URL = "https://huggingface.co"
                headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                response = requests.post(API_URL, headers=headers, json={"inputs": prompt_img})
                if response.status_code == 200:
                    st.image(response.content)
                else:
                    st.info("Image server busy. Try again in 10 seconds.")
