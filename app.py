import streamlit as st
from groq import Groq
import requests

# 1. API KEYS
GROQ_API_KEY = "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"
HF_TOKEN = "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"

# 2. CLEAN PROFESSIONAL UI (ENGLISH ONLY)
st.set_page_config(page_title="Astro AI", page_icon="🚀")

# Modern Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: #e9eaeb; }
    [data-testid="stSidebar"] { background-color: #15191d !important; border-right: 1px solid #30363d; }
    .stTextInput input { background-color: #0b0e11 !important; color: white !important; border: 1px solid #30363d !important; }
    div.stButton > button { background-color: #238636; color: white; border-radius: 6px; border: none; font-weight: 600; }
    div.stButton > button:hover { border: 1px solid #2ea043; background-color: #2ea043; }
    .stChatInput textarea { background-color: #0b0e11 !important; border: 1px solid #30363d !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar (English)
with st.sidebar:
    st.title("Astro AI 🚀")
    st.markdown("---")
    mode = st.radio("Navigation", ["Smart Chat", "Image Studio"])
    st.markdown("---")
    st.success("Status: Online")
    st.caption("Multilingual Support Enabled")

# --- CHAT SECTION ---
if mode == "Smart Chat":
    st.subheader("Astro Smart Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat Input (English)
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            client = Groq(api_key=GROQ_API_KEY)
            # Smart language detection via system prompt
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Astro AI. Always reply in the same language the user is using (English, Roman Urdu, or Urdu). Be professional and concise."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.1-8b-instant", # Faster & more stable model
            )
            res = response.choices.message.content
            with st.chat_message("assistant"):
                st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except Exception:
            st.error("Engine timeout. Please refresh the page.")

# --- IMAGE SECTION ---
else:
    st.subheader("Image Generation Studio")
    prompt_img = st.text_input("Enter your image prompt:")
    
    if st.button("Generate Art"):
        if prompt_img:
            with st.spinner("Generating..."):
                API_URL = "https://huggingface.co"
                headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                response = requests.post(API_URL, headers=headers, json={"inputs": prompt_img})
                if response.status_code == 200:
                    st.image(response.content, use_container_width=True)
                else:
                    st.info("AI model is loading. Try again in 5 seconds.")
