import openai
import streamlit as st

st.title("TigerChat 🐯")

# Set model in session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Hello! How may I help you today?")

if prompt:
    # Add user input to history
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant reply (streamed)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state["messages"]
            ],
            stream=True,
        ):
            if "choices" in response and len(response.choices) > 0:
                delta = response.choices[0].delta.get("content", "")
                full_response += delta
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Save assistant reply
    st.session_state["messages"].append({"role": "assistant", "content": full_response})
