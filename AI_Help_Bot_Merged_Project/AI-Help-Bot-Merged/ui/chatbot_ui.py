# ui/chatbot_ui.py

import streamlit as st
import requests

st.set_page_config(
    page_title="MOSDAC AI Bot",
    page_icon="🛰️",
    layout="centered",
)

# --- Sidebar ---
with st.sidebar:
    st.title("🛰️ MOSDAC AI Bot")
    st.markdown("**Powered by AI for Intelligent Query Support**")
    st.markdown("---")
    st.markdown("🔹 Ask questions about satellite data, products, downloads, formats, and more.")
    st.markdown("🔹 Uses NLP, Knowledge Graph & GPT fallback.")
    st.markdown("---")
    st.markdown("Made with ❤️ by [YourName]")

# --- Main UI ---
st.markdown(
    """
    <style>
    .stTextInput>div>div>input {
        font-size: 16px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💬 Ask your question:")
query = st.text_input("", placeholder="e.g., How do I download satellite data?", key="input")

if st.button("Submit"):
    if query.strip():
        with st.spinner("🔍 Searching for the best answer..."):
            try:
                response = requests.get("http://localhost:8000/ask", params={"q": query})
                data = response.json()

                if "answer" in data:
                    st.success("✅ **Answer:**\n\n" + data["answer"])
                else:
                    st.warning("🤔 No answer found. Try a different question.")
            except requests.exceptions.RequestException as e:
                st.error("❌ Unable to connect to backend.")
                st.code(str(e))
            except Exception as e:
                st.error("⚠️ An unexpected error occurred.")
                st.code(str(e))
    else:
        st.warning("⚠️ Please enter a valid question.")
