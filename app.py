import streamlit as st
from bot.openai_helper import OpenAIHelper
from chat.ui import ChatUI
import sys

# Set page configuration
st.set_page_config(
    page_title="OpenAI Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
<style>
.stApp {
    max-width: 1200px;
    margin: 0 auto;
}
.stChatMessage {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state for messages if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize the UI and OpenAI helper
    chat_ui = ChatUI()
    openai_helper = OpenAIHelper()
    
    # Set up the sidebar and get user settings
    api_key, model, temperature = chat_ui.setup_sidebar()
    
    # Update the API key in the OpenAI helper
    if api_key:
        # Check if this is a new key or different from the stored one
        if "current_api_key" not in st.session_state or st.session_state.current_api_key != api_key:
            st.session_state.current_api_key = api_key
            st.sidebar.info(f"Validating API key...")
            is_valid = openai_helper.set_api_key(api_key)
            
            if not is_valid:
                st.sidebar.error("Invalid API key. Please check and try again.")
                # Add troubleshooting info
                with st.sidebar.expander("Troubleshooting"):
                    st.markdown("""
                    - Make sure your API key starts with 'sk-'
                    - Check that your OpenAI account has sufficient credits
                    - Verify that your API key hasn't expired
                    - Try generating a new API key from the OpenAI dashboard
                    """)
            else:
                st.sidebar.success("API key validated successfully!")
                # Store the validated key in session state
                st.session_state.validated_api_key = api_key
    
    # Main chat interface
    st.title("OpenAI Chatbot")
    st.markdown("Welcome to the OpenAI Chatbot! Enter your message below to start chatting.")
    
    # Display existing messages
    chat_ui.display_messages()
    
    # Get user input
    user_message = chat_ui.get_user_input()
    
    # Process user input and generate response
    if user_message:
        # Add user message to chat history
        chat_ui.add_message("user", user_message)
        
        # Display user message (since the history won't update until rerun)
        with st.chat_message("user"):
            st.markdown(user_message)
        
        # Use the validated key from session state if available
        if "validated_api_key" in st.session_state:
            openai_helper.set_api_key(st.session_state.validated_api_key)
        
        # Check if API key is valid before generating response
        if not openai_helper.is_api_key_valid():
            with st.chat_message("assistant"):
                st.error("Please provide a valid OpenAI API key in the sidebar.")
                st.info("Note: Make sure your API key starts with 'sk-' and has sufficient credits.")
        else:
            # Prepare messages for OpenAI API
            messages = [
                {"role": msg["role"], "content": msg["content"]} 
                for msg in st.session_state.messages
            ]
            
            # Generate and display streaming response
            response_generator = openai_helper.generate_response(
                messages=messages,
                model=model,
                temperature=temperature
            )
            
            chat_ui.display_streaming_response(response_generator)

if __name__ == "__main__":
    main()
