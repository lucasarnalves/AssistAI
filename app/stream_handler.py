import re
import streamlit as st


class BaseStreamHandler:
    def stream_output(self, stream):
        raise NotImplementedError("This method should be overridden.")

    def display_assistant_response(self, stream):
        raise NotImplementedError("This method should be overridden.")

class OtherModelStreamHandler(BaseStreamHandler):
    def stream_output(self,stream):
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

    def display_assistant_response(self,stream):
        with st.chat_message("assistant"):
            response = st.write_stream(self.stream_output(stream))
        return response

class DeepseekStreamHandler(BaseStreamHandler):
    def __init__(self):
        self.accumulated_text = ""
        self.response = ""
        self.think_content = ""


    def stream_output(self, stream):
        response_metadata = {}
        usage_metadata = None
        for chunk in stream:
            # Updates usage metadata if present
            if chunk.usage_metadata:
                usage_metadata = chunk.usage_metadata
            # Stores response metadata when available
            if chunk.response_metadata:
                response_metadata = chunk.response_metadata
            yield chunk

        # After streaming, processes and saves the metadata
        if response_metadata:
            total_duration = response_metadata.get("total_duration")
            if total_duration is not None:
                st.session_state.generation_time = round(float(total_duration) / 10e9, 3)
        if usage_metadata:
            st.session_state.usage_metadata = usage_metadata

    def extract_think_section(self, output_text):
        think_section = re.search(r"<think>(.*?)</think>", output_text, re.DOTALL)
        return think_section.group(1).strip() if think_section else None

    def extract_remaining_section(self, output_text):
        return re.sub(r"<think>.*?</think>", "", output_text, flags=re.DOTALL).strip()

    def handler_thinking(self, chunk, placeholder):
        chunk_text = chunk.content  # Accesses the text from the chunk
        self.accumulated_text += chunk_text  # Accumulates the received text
        
        # Extracts the content from the <think> section
        self.think_content = self.extract_think_section(self.accumulated_text)

        # Extracts the remaining text and updates the placeholder
        remaining_content = self.extract_remaining_section(self.accumulated_text)
        placeholder.write(remaining_content)  # Updates the displayed text

        # Saves the remaining_content in the response variable at the end of the stream
        self.response = remaining_content

    def display_assistant_response(self, stream):
        with st.chat_message("assistant"):
            # Create an empty space to update the text
            placeholder = st.empty()
            
            for chunk in self.stream_output(stream):
                self.handler_thinking(chunk, placeholder)  # Processes the chunk and updates the placeholder

            st.session_state.last_thinking = self.get_thinking()
        return self.response
    
    def get_response(self):
        """Retorna o conteúdo restante como resposta final."""
        return self.response

    def get_thinking(self):
        """Retorna o texto pensamento."""
        return self.think_content if self.think_content else "No thinking content available."