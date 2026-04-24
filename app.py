import streamlit as st
from groq import Groq
import requests

# 1. SETUP
GROQ_API_KEY = "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"
HF_TOKEN = "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"

# 2. PREMIUM INTERFACE (Grok Style)
st.set_page_config(page_title="Astro AI", page_icon="🚀")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #333; }
    .stTextInput input { background-color: #222 !important; color: white !important; border: 1px solid #444 !important; }
    div.stButton > button:first-child { background-color: #2e7bcf; color: white; border-radius: 10px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# Navigation
with st.sidebar:
    st.image("https://flaticon.com", width=100)
    st.title("Astro AI")
    mode = st.radio("Go to:", ["💬 Chat", "🎨 Imagine"])
    st.markdown("---")
    st.write("💡 **Tip:** Type in Roman Urdu or English!")

# --- CHAT ENGINE ---
if mode == "💬 Chat":
    st.subheader("Astro Smart Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            client = Groq(api_key=GROQ_API_KEY)
            # Higher model use kar rahe hain takay error na aye
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Astro AI. Be cool, smart, and reply in the user's language (Roman Urdu or English)."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile", 
            )
            res = response.choices[0].message.content
            with st.chat_message("assistant"):
                st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except:
            st.error("Server busy! Please refresh the page.")

# --- IMAGE ENGINE ---
else:
    st.subheader("Astro Image Studio")
    prompt_img = st.text_input("What should I imagine?")
    
    if st.button("Generate"):
        if prompt_img:
            with st.spinner("Creating..."):
                API_URL = "https://huggingface.co"
                headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                response = requests.post(API_URL, headers=headers, json={"inputs": prompt_img})
                if response.status_code == 200:
                    st.image(response.content)
                else:
                    st.info("Image model loading... try again in 5 seconds.")
