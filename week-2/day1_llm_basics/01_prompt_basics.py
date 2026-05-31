import os
from ollama import Client
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OLLAMA_API_KEY", "dummy_key")
model_name = os.getenv("OLLAMA_MODEL", "gemma3:27b") # Replace with whatever model you use

# Initialize Client
client = Client(host='https://ollama.com', headers={'Authorization': f'Bearer {api_key}'})

def test_system_prompt():
    print("--- 1. Testing System Prompts ---")
    
    # System prompt tells the AI "How" to behave
    # User prompt is the actual question
    messages = [
        {"role": "system", "content": "You are a sarcastic but helpful coding assistant. Keep answers under 2 lines."},
        {"role": "user", "content": "What is Python?"}
    ]
    
    print("Sending prompt to AI...")
    response = client.chat(model=model_name, messages=messages)
    
    print(f"\n[AI Response]:\n{response['message']['content']}")

if __name__ == "__main__":
    test_system_prompt()