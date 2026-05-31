# 01_streaming.py
import os
import sys
from ollama import Client
from dotenv import load_dotenv

load_dotenv()
# Initialize Official Ollama Client
client = Client(host='https://ollama.com', headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'})
model_name = os.getenv("OLLAMA_MODEL", "gemma3:27b")

def test_streaming():
    print("--- 1. Testing LLM Streaming Output ---")
    prompt = "Explain Quantum Computing in 3 simple bullet points."
    print(f"User: {prompt}\n")
    print("AI is typing... \n")
    
    try:
        # stream=True is the magic parameter here
        response = client.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=True 
        )
        
        # Iterating over the chunks as they arrive from the server
        for chunk in response:
            text = chunk['message']['content']
            # sys.stdout.write prints without moving to the next line immediately
            sys.stdout.write(text)
            sys.stdout.flush() 
        print("\n\n[Streaming Completed ✅]")
        
    except Exception as e:
        print(f"\nError occurred: {e}")

if __name__ == "__main__":
    test_streaming()