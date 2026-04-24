import streamlit as st
from groq import Groq
import requests

# 1. API KEYS
GROQ_API_KEY = "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"
HF_TOKEN = "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"

# 2. CLEAN PROFESSIONAL UI
st.set_page_config(page_title="Astro AI", page_icon="🚀")

# Simple Dark Theme (No more messy colors)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #1e1e1e !important; }
    .stTextInput input { background-color: #2d2d2d !important; color: white !important; border: 1px solid #444 !important; }
    div.stButton > button { background-color: #007bff; color: white; border-radius: 5px; border: none; width: 100%; }
    .stChatMessage { background-color: #2d2d2d !important; border-radius: 10px; padding: 10px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🚀 Astro AI")
    mode = st.radio("Menu", ["💬 Chat", "🎨 Image"])
    st.markdown("---")
    st.write("Status: 🟢 Active")

# --- CHAT SECTION ---
if mode == "💬 Chat":
    st.subheader("Astro Smart Chat")
    
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
            # Using a more stable model
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Astro AI. Reply in the same language user uses (Roman Urdu/English)."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192", 
            )
            res = response.choices.message.content
            with st.chat_message("assistant"):
                st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except Exception as e:
            st.error("Wait! AI is taking a break. Please refresh the page.")

# --- IMAGE SECTION ---
else:
    st.subheader("Astro Image Creator")
    prompt_img = st.text_input("Enter prompt (e.g. A futuristic car in Lahore):")
    
    if st.button("Generate Image"):
        if prompt_img:
            with st.spinner("Creating..."):
                API_URL = "https://huggingface.co"
                headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                response = requests.post(API_URL, headers=headers, json={"inputs": prompt_img})
                if response.status_code == 200:
                    st.image(response.content)
                else:
                    st.warning("Server is busy. Try again in a few seconds.")
