import os
import streamlit as st
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

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


@st.cache_resource
def init_llm(temperature, max_tokens):
    return ChatOllama(
        model=model_name,
        temperature=temperature,
        num_predict=max_tokens,
        base_url=model_url,
    )


def sidebar():
    customize_llm = st.sidebar.toggle("Customize LLM")
    if customize_llm:
        temperature = st.sidebar.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1
        )
        max_tokens = st.sidebar.slider(
            "Max Tokens", min_value=128, max_value=4096, value=512, step=128
        )
    else:  # Default values
        temperature = 0.7
        max_tokens = None
    st.session_state.llm = init_llm(temperature, max_tokens)

    display_metrics(st.session_state.usage_metadata, st.session_state.generation_time)


def display_metrics(usage_metadata, generation_time):
    input_tokens, output_tokens, gen_time = st.sidebar.columns(3)
    input_tokens.metric("Input Tokens:", value=usage_metadata["input_tokens"])
    output_tokens.metric("Output Tokens:", value=usage_metadata["output_tokens"])
    gen_time.metric("Generation Time (s):", value=generation_time)


def stream_output(stream):
    # Initializes an empty dictionary to store the response metadata and usage metadata
    response_metadata = {}
    usage_metadata = None
    for chunk in stream:
        # Updates usage metadata if present
        if chunk.usage_metadata:
            usage_metadata = chunk.usage_metadata
        # Stores the response metadata when available
        if chunk.response_metadata:
            response_metadata = chunk.response_metadata
        yield chunk

    # After the streaming is complete, processes saves the metadata
    if response_metadata:
        total_duration = response_metadata.get("total_duration")
        if total_duration is not None:
            st.session_state.generation_time = round(float(total_duration) / 10e9, 3)
    if usage_metadata:
        st.session_state.usage_metadata = usage_metadata


def main():
    init_states()
    st.title("AssistAI - Personal AI Assistant")

    sidebar()

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Digite seu prompt"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):

            messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            stream = st.session_state.llm.stream(messages)

            response = st.write_stream(stream_output(stream))

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


if __name__ == "__main__":
    main()
