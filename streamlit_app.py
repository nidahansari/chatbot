import streamlit as st
from openai import OpenAI

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Chatbot", page_icon="💬")
st.title("💬 AI Chatbot with Streamlit + OpenAI")

st.write(
    "This chatbot uses OpenAI's GPT model to answer your questions. "
    "To use this app, provide your OpenAI API key below. "
    "You can obtain one from [OpenAI](https://platform.openai.com/account/api-keys)."
)

# --- GET OPENAI API KEY ---
openai_api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please enter your API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # --- CHAT HISTORY ---
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant that provides accurate, concise answers."}
        ]

    # --- DISPLAY PREVIOUS MESSAGES ---
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # --- USER INPUT ---
    if prompt := st.chat_input("Ask me anything..."):
        # Add user input
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # --- GENERATE RESPONSE ---
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)

        # Save the assistant’s reply
        st.session_state.messages.append({"role": "assistant", "content": response})
