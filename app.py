import streamlit as st
from groq import Groq
import requests

# 1. NEW ACTIVATED KEYS
GROQ_API_KEY = "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"
HF_TOKEN = "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"

# 2. CLEAN & MODERN UI (White Theme)
st.set_page_config(page_title="Astro AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    /* White Background & Black Text */
    .stApp { background-color: #FFFFFF; color: #1a1a1a; }
    [data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 1px solid #dee2e6; }
    
    /* Input Field Styling */
    .stChatInput textarea { 
        background-color: #ffffff !important; 
        color: #1a1a1a !important; 
        border: 1px solid #ced4da !important;
        border-radius: 10px !important;
    }
    
    /* Chat Bubbles */
    .stChatMessage { border-radius: 15px; padding: 15px; margin-bottom: 10px; border: 1px solid #f0f0f0; }
    
    /* Buttons */
    div.stButton > button { 
        background-color: #10a37f; 
        color: white; 
        border-radius: 8px; 
        border: none;
        padding: 10px 20px;
    }
    div.stButton > button:hover { background-color: #1a7f64; }
    
    /* Fix Visibility */
    p, span, h1, h2, h3, label { color: #1a1a1a !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Astro AI 🚀</h2>", unsafe_allow_html=True)
    st.markdown("---")
    mode = st.radio("Select Tool:", ["💬 Smart Chatbot", "🎨 Image Studio"])
    st.markdown("---")
    st.success("Astro System: Live 🟢")

# --- CHATBOT SECTION ---
if mode == "💬 Smart Chatbot":
    st.title("Astro Smart Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            client = Groq(api_key=GROQ_API_KEY)
            # Using llama-3.1-8b for super fast response
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Astro AI. Reply in the same language user uses (English/Roman Urdu/Urdu). Be smart and professional."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.1-8b-instant", 
            )
            res = response.choices.message.content
            with st.chat_message("assistant"):
                st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except Exception as e:
            st.error("Engine busy. Please refresh the page and try again.")

# --- IMAGE SECTION ---
else:
    st.title("Astro Image Studio")
    st.write("Generate high-quality images from text.")
    img_prompt = st.text_input("Describe the image you want:")
    
    if st.button("Generate Art"):
        if img_prompt:
            with st.spinner("Astro is painting..."):
                try:
                    API_URL = "https://huggingface.co"
                    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                    response = requests.post(API_URL, headers=headers, json={"inputs": img_prompt})
                    if response.status_code == 200:
                        st.image(response.content, use_container_width=True)
                    else:
                        st.warning("Model is loading. Please wait 10 seconds and try again.")
                except:
                    st.error("Image server error. Try a different prompt.")
