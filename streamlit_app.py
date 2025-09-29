import openai
import streamlit as st

st.title("TigerChat")
openai.api_key = st.secrets["OPENAI_API_KEY"]

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

