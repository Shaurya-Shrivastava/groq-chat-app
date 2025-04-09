import streamlit as st
import requests

st.set_page_config(page_title="Groq LLM Chat", page_icon="🤖")

st.title("💬 Chat with Groq LLM")

api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("🚫 GROQ_API_KEY not found in Streamlit secrets!")
    st.stop()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": st.session_state.chat_history
    }

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking... 🤔"):
                res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
                res.raise_for_status()
                reply = res.json()["choices"][0]["message"]["content"]
                st.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
        except requests.exceptions.RequestException as e:
            st.error(f"❌ API error: {e}")
        except Exception as e:
            st.error(f"⚠️ Unexpected error: {e}")
