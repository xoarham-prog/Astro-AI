import streamlit as st
from groq import Groq
import requests

# 1. SETUP
GROQ_API_KEY = "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"
HF_TOKEN = "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"

# 2. ULTRA PREMIUM INTERFACE
st.set_page_config(page_title="Astro AI", page_icon="🚀", layout="wide")

# Custom CSS for Modern Neon Theme
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border-right: 1px solid #00f2fe;
    }
    /* Input Box */
    .stTextInput input, .stChatInput textarea {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #00f2fe !important;
        border-radius: 10px !important;
    }
    /* Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        color: black;
        font-weight: bold;
        border-radius: 20px;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px #00f2fe;
    }
    /* Chat bubbles */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Navigation
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #00f2fe;'>🚀 ASTRO AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    mode = st.radio("MAIN MENU", ["💬 SMART CHAT", "🎨 IMAGINATION STUDIO"])
    st.markdown("---")
    st.success("System: Active 🟢")
    st.info("Tip: You can chat in Roman Urdu!")

# --- CHAT ENGINE ---
if mode == "💬 SMART CHAT":
    st.markdown("<h2 style='color: #00f2fe;'>💬 Astro Assistant</h2>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Baat karein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Astro AI. Reply in the user's language (Roman Urdu/English). Be cool and professional."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile", 
            )
            res = response.choices.message.content
            with st.chat_message("assistant"):
                st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except:
            st.error("Server update ho raha hai. Please try again.")

# --- IMAGE ENGINE ---
else:
    st.markdown("<h2 style='color: #4facfe;'>🎨 Image Studio</h2>", unsafe_allow_html=True)
    prompt_img = st.text_input("Kya tasveer banani hai?")
    
    if st.button("Generate Art"):
        if prompt_img:
            with st.spinner("Astro is thinking..."):
                API_URL = "https://huggingface.co"
                headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                response = requests.post(API_URL, headers=headers, json={"inputs": prompt_img})
                if response.status_code == 200:
                    st.image(response.content, use_container_width=True)
                else:
                    st.info("AI Model garam ho raha hai. 10 second baad try karein!")
