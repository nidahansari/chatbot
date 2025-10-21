import streamlit as st
from openai import OpenAI
import PyPDF2  # using PyPDF2 this time

# 🐯 Use API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# TigerChat UI
st.set_page_config(page_title="TigerChat 🐯")
st.title("TigerChat 🐯")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to read PDF text using PyPDF2
def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Load PDF content once at start
if "pdf_text" not in st.session_state:
    st.session_state["pdf_text"] = read_pdf("academic_calendar.pdf")

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Hello! How can I help you?")

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

        # Include PDF text as system context
        pdf_context = st.session_state["pdf_text"][:3000]  # limit to first 3000 chars
        system_message = {
            "role": "system",
            "content": f"You have access to the academic calendar PDF content:\n{pdf_context}"
        }
        messages_with_context = [system_message] + history

        try:
            # Stream the response from OpenAI
            for chunk in client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages_with_context,
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
