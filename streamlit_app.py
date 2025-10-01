import streamlit as st
import random
import time  # <- needed for sleep

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

        # Mock GPT logic: canned responses
        canned_responses = [
            "Hello! How can I help you today?",
            "Interesting! Tell me more.",
            "I'm here to chat with you.",
            "Can you clarify that for me?",
            "That sounds great! What else?"
        ]
        
        # Pick a random response
        response_text = random.choice(canned_responses)
        full_response = ""

        # Simulate typing effect
        for char in response_text:
            full_response += char
            placeholder.markdown(full_response + "▌")
            time.sleep(0.05)  # <-- correct sleep

        # Finalize message
        placeholder.markdown(full_response)

        # Add assistant message to history
        st.session_state["messages"].append({"role": "assistant", "content": full_response})
