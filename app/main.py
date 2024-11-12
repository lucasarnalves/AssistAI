import os
import streamlit as st

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from dotenv import load_dotenv
load_dotenv()

model_name = os.getenv("MODEL_NAME")
model_url =os.getenv("MODEL_URL")

st.title("AssistAI - Assistente Pessoal de IA")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

llm = ChatOllama(model=model_name,temperature=0.7,max_tokens=1024,base_url=model_url)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt:= st.chat_input("Digite seu prompt"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):

        messages=[{"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
        stream = llm.stream(messages)
        response = st.write_stream(stream)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    