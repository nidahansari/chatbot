import streamlit as st
import random
import time

st.set_page_config(page_title="TigerChat 🐯")
st.title("TigerChat 🐯")

# -------------------------------
# Initialize chat history
# -------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# -------------------------------
# Display chat history
# -------------------------------
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# User input
# -------------------------------
prompt = st.chat_input("Type your message here...")

if prompt:
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()

        # Mock GPT logic: simple canned responses or random selection
        canned_responses = [
            "Hello! How can I help you today?",
            "Interesting! Tell me more.",
            "I'm here to chat with you.",
            "Can you clarify that for me?",
            "That sounds great! What else?"
        ]
        
        # Simulate typing effect
        response_text = random.choice(canned_responses)
        full_response = ""
        for char in response_text:
            full_response += char
            placeholder.markdown(full_response + "▌")
            st.sleep(0.05)  # simulate typing

        placeholder.markdown(full_response)

        # Add assistant message to history
        st.session_state["messages"].append({"role": "assistant", "content": full_response})
        # Simulate typing effect
response_text = random.choice(canned_responses)
full_response = ""
for char in response_text:
    full_response += char
    placeholder.markdown(full_response + "▌")
    time.sleep(0.05)  # <-- use time.sleep instead of st.sleep

placeholder.markdown(full_response)
