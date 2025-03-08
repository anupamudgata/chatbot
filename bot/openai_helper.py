from openai import OpenAI
import time

class OpenAIHelper:
    def __init__(self, api_key=None):
        """
        Initialize the OpenAI helper with an optional API key.
        
        Args:
            api_key (str, optional): OpenAI API key. Defaults to None.
        """
        self.api_key = api_key
        self.client = None
        if api_key:
            self.client = OpenAI(api_key=api_key)
    
    def set_api_key(self, api_key):
        """
        Set or update the OpenAI API key.
        
        Args:
            api_key (str): OpenAI API key
            
        Returns:
            bool: True if the API key is valid, False otherwise
        """
        try:
            self.api_key = api_key
            self.client = OpenAI(api_key=api_key)
            # Make a simple API call to validate the key
            self.client.models.list()
            return True
        except Exception as e:
            print(f"Error validating API key: {e}")
            return False
    
    def is_api_key_valid(self):
        """
        Check if the current API key is valid.
        
        Returns:
            bool: True if the API key is valid, False otherwise
        """
        if not self.api_key or not self.client:
            return False
        
        try:
            self.client.models.list()
            return True
        except:
            return False
    
    def generate_response(self, messages, model="gpt-3.5-turbo", temperature=0.7):
        """
        Generate a response from OpenAI's chat models.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content'
            model (str, optional): The model to use. Defaults to "gpt-3.5-turbo".
            temperature (float, optional): Controls randomness. Defaults to 0.7.
            
        Returns:
            str: The generated response text
        """
        if not self.is_api_key_valid():
            return "Please provide a valid OpenAI API key in the sidebar."
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=True
            )
            
            # For streaming response
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    time.sleep(0.02)  # Small delay for smoother streaming
                
        except Exception as e:
            yield f"Error: {str(e)}"