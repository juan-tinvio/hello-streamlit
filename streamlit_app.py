import streamlit as st
from chat import start_llm_chat, system_message
import os

FREKI_URL="https://freki-staging.tinvio.dev"

if "api_key" not in st.session_state:
    st.session_state.api_key = None

############################################################

# Initialize the LangChain messages
def convert_to_langchain() -> list[tuple[str, str]]:
    msg = [("system", system_message)]
    for m in st.session_state.messages[2:]:
        msg.append((m["role"], m["content"]))
    return msg

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, please enter your API key on the left."},
        {"role": "assistant", "content": "How can I help you today?"},
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

with st.sidebar:
    st.title("Jaz AI")
    st.subheader("AI Interface for Jaz")
    st.text_input('API_KEY', key="api_key")

graph = start_llm_chat(st.session_state.api_key)

if prompt := st.chat_input():
    if not st.session_state.api_key:
        st.info("Please add your Jaz API key to continue.")
        st.stop()

    # Clean up prompt
    if prompt != "":
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        messages = convert_to_langchain()
        print(messages)

        try:
            for event in graph.stream({"messages": messages}, {"recursion_limit": 25, "max_concurrency": 10}):
                print(event)
                if "chatbot" in event:
                    for msg in event["chatbot"]["messages"]:
                        if msg.content != "":
                            st.session_state.messages.append({"role": "assistant", "content": msg.content})
                            st.chat_message("assistant").write(msg.content)
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})
            st.chat_message("assistant").write(f"Error: {e}")
            raise e 