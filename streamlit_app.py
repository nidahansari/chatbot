import streamlit as st
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import time

st.set_page_config(page_title="TigerChat 🐯 - Hugging Face")
st.title("TigerChat 🐯 - Hugging Face (Free Model)")

# -------------------------------
# Load model and tokenizer
# -------------------------------
@st.cache_resource  # load once
def load_model():
    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

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
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()

        # Prepare input for model
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids

        # Generate response
        output_ids = model.generate(input_ids, max_length=100)
        response_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Simulate typing effect
        full_response = ""
        for char in response_text:
            full_response += char
            placeholder.markdown(full_response + "▌")
            time.sleep(0.03)  # faster typing for small model

        placeholder.markdown(full_response)

        # Add assistant message to history
        st.session_state["messages"].append({"role": "assistant", "content": full_response})
