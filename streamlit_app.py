import openai
import streamlit as st

st.title("TigerChat")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    
with st.chat_message(name="assistant", avatar="🐯"):
    st.write("Hello!")

# Initialize chat history
if "messages" not in st.session_state:
    st,session_state.messages = []

# Display chat messages from history on app rerun
for message in st.sessions_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Hello! How may I help you today?")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

st.session_state.messages.append({"role": "user", "content": prompt})

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    for response in openai.ChatCompletion.create(
    model=st.session_state["openai_model"],
    messages=[
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ],
    stream=True,
):
    if "choices" in response and len(response.choices) > 0:
        delta = response.choices[0].delta.get("content", "")
        full_response += delta
        message_placeholder.markdown(full_response + "▌")

    ],
    stream=True,
):
    full_response += response.choices[0]
