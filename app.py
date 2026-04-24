import streamlit as st
from groq import Groq
import requests

# 1. SETUP & KEYS
GROQ_API_KEY = "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"
HF_TOKEN = "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"

# 2. PROFESSIONAL PAGE CONFIG
st.set_page_config(page_title="Astro AI - Pro", page_icon="🚀", layout="centered")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #2e7bcf; color: white; }
    .stTextInput>div>div>input { border-radius: 15px; }
    </style>
    """, unsafe_allow_now_safe=True)

# Sidebar
with st.sidebar:
    st.title("🚀 Astro AI Pro")
    st.markdown("---")
    mode = st.radio("Navigation", ["💬 Smart Chat", "🎨 Image Studio"])
    st.markdown("---")
    st.write("Status: 🟢 Online")

# --- SMART CHAT MODE ---
if mode == "💬 Smart Chat":
    st.title("💬 Astro Chat")
    st.info("I can speak English, Urdu, and Roman Urdu. Just type!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            client = Groq(api_key=GROQ_API_KEY)
            # System instruction added for language flexibility
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Astro AI. Reply in the same language the user uses (English, Urdu, or Roman Urdu). Be helpful and smart."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-70b-8192", # Higher model for better logic
            )
            full_response = response.choices.message.content
            with st.chat_message("assistant"):
                st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error("Connection error. Please try again.")

# --- IMAGE MODE ---
else:
    st.title("🎨 Astro Image Studio")
    st.write("Generate high-quality visuals instantly.")
    
    img_prompt = st.text_input("Describe the image you want to create:")
    
    if st.button("Generate Masterpiece"):
        if img_prompt:
            with st.spinner("Astro is creating your image..."):
                try:
                    # Switched to a more reliable model endpoint
                    API_URL = "https://huggingface.co"
                    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                    response = requests.post(API_URL, headers=headers, json={"inputs": img_prompt})
                    if response.status_code == 200:
                        st.image(response.content, use_column_width=True)
                    else:
                        st.error("AI is busy. Please try in 10 seconds.")
                except:
                    st.error("Something went wrong with the image server.")
        else:
            st.warning("Please enter a description first!")
