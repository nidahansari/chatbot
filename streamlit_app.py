import streamlit as st
from openai import OpenAI

# -------------------------------
# Initialize OpenAI client
# -------------------------------
# Make sure you added your key in Streamlit Secrets:
# OPENAI_API_KEY = "sk-your-key"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="TigerChat 🐯")

st.title("TigerChat 🐯 - Free Trial Friendly")

# -------------------------------
# Initialize session state
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

    # Assistant response placeholder
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        # Only keep the last 5 messages to save tokens
        history = st.session_state["messages"][-5:]

        try:
            # Stream the response from OpenAI
            for chunk in client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=history,
                stream=True
            ):
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                placeholder.markdown(full_response + "▌")

            # Finalize assistant message
            placeholder.markdown(full_response)
            st.session_state["messages"].append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as e:
            st.error(f"Error: {e}")
