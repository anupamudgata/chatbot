import openai
import time
import sys
import requests

class OpenAIHelper:
    def __init__(self, api_key=None):
        """
        Initialize the OpenAI helper with an optional API key.
        
        Args:
            api_key (str, optional): OpenAI API key. Defaults to None.
        """
        self.api_key = api_key
        if api_key:
            try:
                print(f"Attempting to initialize OpenAI client...", file=sys.stderr)
                openai.api_key = api_key
                print("OpenAI client initialized successfully", file=sys.stderr)
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}", file=sys.stderr)
    
    def set_api_key(self, api_key):
        """
        Set or update the OpenAI API key.
        
        Args:
            api_key (str): OpenAI API key
            
        Returns:
            bool: True if the API key is valid, False otherwise
        """
        try:
            # Remove any whitespace that might have been accidentally copied
            api_key = api_key.strip()
            
            # Try a direct API call using requests to validate the key
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            print("Attempting to validate API key with direct request...", file=sys.stderr)
            response = requests.get("https://api.openai.com/v1/models", headers=headers)
            
            if response.status_code == 200:
                print("API key validated successfully with direct request", file=sys.stderr)
                self.api_key = api_key
                openai.api_key = api_key
                return True
            else:
                print(f"API key validation failed: {response.status_code} - {response.text}", file=sys.stderr)
                return False
                
        except Exception as e:
            print(f"Error validating API key: {str(e)}", file=sys.stderr)
            return False
    
    def is_api_key_valid(self):
        """
        Check if the current API key is valid.
        
        Returns:
            bool: True if the API key is valid, False otherwise
        """
        if not self.api_key:
            return False
        
        try:
            models = openai.Model.list()
            # Add debug print to verify models are being retrieved
            print(f"Models retrieved successfully")
            return True
        except Exception as e:
            print(f"API key validation failed: {e}", file=sys.stderr)
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
            yield "Please provide a valid OpenAI API key in the sidebar. If you've already provided a key, it may be invalid or expired."
            return
        
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=True
            )
            
            # For streaming response
            for chunk in response:
                if 'choices' in chunk and chunk['choices'][0].get('delta', {}).get('content'):
                    yield chunk['choices'][0]['delta']['content']
                    time.sleep(0.02)  # Small delay for smoother streaming
                
        except Exception as e:
            yield f"Error: {str(e)}"
