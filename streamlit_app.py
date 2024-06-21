import streamlit as st
import os

os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

############################################################
from chat import start_llm_chat, system_message

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

#if 'waiting_for_assistant' not in st.session_state:
#    st.session_state['waiting_for_assistant'] = False

if prompt := st.chat_input():
    if not st.session_state.api_key:
        st.info("Please add your Jaz API key to continue.")
        st.stop()
    
    # Clean up prompt
    if prompt != "": #and not st.session_state['waiting_for_assistant']:
        #st.session_state['waiting_for_assistant'] = True

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        messages = convert_to_langchain()
        assistant = []

        try:
            for event in graph.stream({"messages": messages}, {"recursion_limit": 25, "max_concurrency": 25}):
                if "chatbot" in event:
                    for msg in event["chatbot"]["messages"]:
                        if msg.content != "":
                            assistant.append(msg.content)
                            st.chat_message("assistant").markdown(msg.content)
        except Exception as e:
            assistant.append(f"Error: {e}")
            st.chat_message("assistant").write(f"Error: {e}")
            raise e 
        finally:
            st.session_state.messages.append({"role": "assistant", "content": ', '.join(assistant)})
            #st.session_state['waiting_for_assistant'] = False