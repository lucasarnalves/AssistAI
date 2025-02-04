import os
import streamlit as st
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from stream_handler import OtherModelStreamHandler,DeepseekStreamHandler

load_dotenv()

model_name = os.getenv("MODEL_NAME")
model_url = os.getenv("MODEL_URL")


def init_states():
    if "llm" not in st.session_state:
        st.session_state.llm = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "usage_metadata" not in st.session_state:
        st.session_state.usage_metadata = {"input_tokens": None, "output_tokens": None}
    if "generation_time" not in st.session_state:
        st.session_state.generation_time = None
    if "last_thinking" not in st.session_state:
        st.session_state.last_thinking = None


@st.cache_resource
def init_llm(temperature, max_tokens):
    return ChatOllama(
        model=model_name,
        temperature=temperature,
        num_predict=max_tokens,
        base_url=model_url,
    )

def display_metrics(usage_metadata, generation_time):
    input_tokens, output_tokens, gen_time = st.sidebar.columns(3)
    input_tokens.metric("Input Tokens:", value=usage_metadata["input_tokens"])
    output_tokens.metric("Output Tokens:", value=usage_metadata["output_tokens"])
    gen_time.metric("Generation Time (s):", value=generation_time)


def sidebar():
    customize_llm = st.sidebar.toggle("Customize LLM")
    if customize_llm:
        temperature = st.sidebar.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1
        )
        max_tokens = st.sidebar.slider(
            "Max Tokens", min_value=256, max_value=16384, value=1024, step=256
        )
    else:  # Default values
        temperature = 0.7
        max_tokens = None
    st.session_state.llm = init_llm(temperature, max_tokens)
    display_metrics(st.session_state.usage_metadata, st.session_state.generation_time)
    display_thinking()


def generate_assistant_response():
    messages = [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]
    stream = st.session_state.llm.stream(messages)
    return stream

def display_chat_messages(messages):
    # Display chat messages from history
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def display_thinking():
    if "deepseek-r1" in model_name and st.session_state.last_thinking:
        with st.sidebar.expander('Deepseek Thinking:'):
            st.markdown(st.session_state.last_thinking)


def add_message_to_history(role, content):
    # Add message to chat history
    st.session_state.messages.append({"role": role, "content": content})

def process_user_input():
    prompt = st.chat_input("Enter your prompt")

    if prompt:
        # Add user message to chat history
        add_message_to_history("user", prompt)

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        stream = generate_assistant_response()
        
        if "deepseek-r1" in model_name:
            stream_handler = DeepseekStreamHandler()
        else:
            stream_handler = OtherModelStreamHandler()

        # Display assistant response in chat message container
        response = stream_handler.display_assistant_response(stream)

        # Add assistant response to chat history
        add_message_to_history("assistant", response)

        st.rerun()


def main():
    st.set_page_config(page_title="AssistAI", layout="wide")
    init_states()
    st.title("AssistAI - Personal AI Assistant")

    sidebar()

    display_chat_messages(st.session_state.messages)
    
    process_user_input()

if __name__ == "__main__":
    main()
