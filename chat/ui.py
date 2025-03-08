import streamlit as st

class ChatUI:
    def __init__(self):
        """
        Initialize the chat UI components.
        """
        # Initialize session state variables if they don't exist
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'api_key' not in st.session_state:
            st.session_state.api_key = ""
    
    def setup_sidebar(self):
        """
        Set up the sidebar with API key input and other controls.
        
        Returns:
            str: The OpenAI API key entered by the user
        """
        with st.sidebar:
            st.title("OpenAI Chatbot Settings")
            
            # API key input
            api_key = st.text_input(
                "Enter your OpenAI API Key", 
                value=st.session_state.api_key,
                type="password",
                help="Get your API key from https://platform.openai.com/"
            )
            
            # Save API key to session state
            if api_key:
                st.session_state.api_key = api_key
            
            # Model selection
            model = st.selectbox(
                "Select Model",
                ["gpt-3.5-turbo", "gpt-4"],
                index=0,
                help="Select the OpenAI model to use for chat"
            )
            
            # Temperature slider
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values make output more random, lower values make it more deterministic"
            )
            
            # Clear chat button
            if st.button("Clear Chat History"):
                st.session_state.messages = []
                st.rerun()
                
            st.divider()
            st.markdown("### About")
            st.markdown(
                "This is a simple OpenAI chatbot built with Streamlit. "
                "Enter your OpenAI API key to start chatting with the AI."
            )
        
        return api_key, model, temperature
    
    def display_messages(self):
        """
        Display all messages in the chat history.
        """
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def get_user_input(self):
        """
        Get user input from the chat input box.
        
        Returns:
            str: The user's message or None if no message was entered
        """
        return st.chat_input("Type your message here...")
    
    def add_message(self, role, content):
        """
        Add a message to the chat history.
        
        Args:
            role (str): The role of the message sender ("user" or "assistant")
            content (str): The content of the message
        """
        st.session_state.messages.append({"role": role, "content": content})
    
    def display_streaming_response(self, response_generator):
        """
        Display a streaming response from the AI.
        
        Args:
            response_generator: Generator yielding response chunks
        """
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Display the response as it's being generated
            for response_chunk in response_generator:
                full_response += response_chunk
                message_placeholder.markdown(full_response + "▌")
            
            # Display the final response without the cursor
            message_placeholder.markdown(full_response)
        
        # Add the full response to the message history
        self.add_message("assistant", full_response)

