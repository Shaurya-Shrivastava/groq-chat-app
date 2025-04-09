import streamlit as st
import requests
import os

# Title
st.title("💬 Chat with Groq LLM")

# Sidebar to enter Groq API Key
groq_api_key = st.sidebar.text_input("Enter your grok api key here!", type="password")

# Chat input
user_input = st.chat_input("Type your message...")

# Store chat history in session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# When user sends message
if user_input and groq_api_key:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare Groq API call
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": st.session_state.chat_history
    }

    # Call Groq API
    with st.chat_message("assistant"):
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            ai_msg = response.json()["choices"][0]["message"]["content"]
            st.markdown(ai_msg)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_msg})
        else:
            st.error("❌ Error: " + response.json().get("error", {}).get("message", "Unknown error"))
