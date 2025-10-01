from openai import OpenAI
import streamlit as st

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("TigerChat 🐯")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Hello! How may I help you today?")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        response_stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state["messages"]
            ],
            stream=True,
        )

        for chunk in response_stream:
            # `chunk` is a Pydantic model, not a dict
            delta = chunk.choices[0].delta.content or ""
            full_response += delta
            placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    st.session_state["messages"].append(
        {"role": "assistant", "content": full_response}
    )
