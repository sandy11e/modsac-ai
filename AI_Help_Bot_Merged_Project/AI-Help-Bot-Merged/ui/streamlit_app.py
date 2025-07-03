import streamlit as st, requests, json

st.set_page_config(page_title="🛰️ MOSDAC Chat‑Bot")
st.title("🛰️ MOSDAC AI Help‑Bot")

if "chat" not in st.session_state: st.session_state.chat = []

def chat(role, text):
    st.chat_message(role).write(text)

# replay
for role,text in st.session_state.chat:
    chat(role,text)

query = st.chat_input("Ask me anything about MOSDAC…")
if query:
    chat("user", query)
    with st.spinner("Thinking…"):
        res = requests.post("http://localhost:8000/generate",
                            json={"query": query}, timeout=120)
        answer = res.json()["answer"]
    chat("assistant", answer)
    st.session_state.chat.append(("user", query))
    st.session_state.chat.append(("assistant", answer))

