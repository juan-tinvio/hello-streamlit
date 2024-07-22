import streamlit as st
import os
import base64

os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

############################################################
from chat import start_llm_chat, system_message, Attachment

if "api_key" not in st.session_state:
    st.session_state.api_key = None
############################################################
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage

# Initialize the LangChain messages
def get_chat_history() -> list[BaseMessage]:
    msg = [SystemMessage(content="You are a helpful assistant accountant.")]
    for m in st.session_state.messages[2:]:
        msg.append(m)
    return msg

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        AIMessage("Hello, please enter your API key on the left."),
        AIMessage("How can I help you today?"),
    ]

for msg in st.session_state.messages:
    content = []
    if isinstance(msg.content, str):
        content.append(msg.content)
    else:
        for c in msg.content:
            if c["type"] == "text":
                content.append(c["text"])
                break
    st.chat_message(msg.type).write(','.join(content))

# Initialize uploaded files
if "already_uploaded_files" not in st.session_state:
    st.session_state["already_uploaded_files"] = []

def add_uploaded_file(files):
    for f in files:
        st.session_state["already_uploaded_files"].append(f.name)

uploaded_files = None

with st.sidebar:
    st.title("Jaz AI")
    st.subheader("AI Interface for Jaz")
    st.text_input('API_KEY', key="api_key", type="password")
    uploaded_files = st.file_uploader("Attach a file to request",
        accept_multiple_files=True,
        label_visibility="collapsed")

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

        st.chat_message("user").write(prompt)

        uploaded_attachments = []

        if uploaded_files is None:
            st.session_state.messages.append(HumanMessage(content=prompt))
        # Handle Uploads
        else:
            content = [{"type": "text", "text": prompt}]
            uploaded_files = [f for f in uploaded_files if f.name not in st.session_state["already_uploaded_files"]]
            #print(f"Uploaded Files: {uploaded_files}")
            for uploaded_file in uploaded_files:
                match uploaded_file.type:
                    case "image/png", "image/jpeg", "image/jpg":
                        bytes_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
                        content.append({"type": "image_url", "image_url": {"url": f"data:{uploaded_file.type};base64,{bytes_data}"}})
                    case _:
                        uploaded_attachments.append(Attachment(name=uploaded_file.name, type=uploaded_file.type, data=uploaded_file))
                        content.append({"type": "text", "text": f"Attached file: {uploaded_file.name}, type: {uploaded_file.type}"})
            st.session_state.messages.append(HumanMessage(content=content))

        assistant = []

        try:
            for event in graph.stream(
                {"messages": get_chat_history(), "files": uploaded_attachments},
                {"recursion_limit": 25, "max_concurrency": 25}):
                if "chatbot" in event:
                    for msg in event["chatbot"]["messages"]:
                        if msg.content != "":
                            assistant.append(msg.content)
                            st.chat_message("assistant").markdown(msg.content)
            uploaded_file = None
        except Exception as e:
            assistant.append(f"Error: {e}")
            st.chat_message("assistant").write(f"Error: {e}")
            raise e 
        finally:
            st.session_state.messages.append(AIMessage(content=', '.join(assistant)))
            if uploaded_files is not None:
                add_uploaded_file(uploaded_files)
            uploaded_files = None
            #st.session_state['waiting_for_assistant'] = False