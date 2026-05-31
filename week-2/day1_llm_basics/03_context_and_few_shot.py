import os
from ollama import Client
from dotenv import load_dotenv

load_dotenv()
client = Client(host='https://ollama.com', headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'})
model_name = os.getenv("OLLAMA_MODEL", "gemma3:27b")

def test_few_shot_prompting():
    print("--- 3. Testing Few-Shot Prompting & Context Window ---")
    
    # We are providing context/examples in the messages list
    messages = [
        {"role": "system", "content": "You are a sentiment analysis bot. Reply ONLY with POSITIVE, NEGATIVE, or NEUTRAL."},
        
        # Example 1
        {"role": "user", "content": "I love this new phone! It's super fast."},
        {"role": "assistant", "content": "POSITIVE"},
        
        # Example 2
        {"role": "user", "content": "The delivery was late and the screen is broken."},
        {"role": "assistant", "content": "NEGATIVE"},
        
        # Actual Question (The AI will look at the previous context to answer this)
        {"role": "user", "content": "The battery life is okay, nothing special but it works."}
    ]
    
    print("\nSending contextual prompt to AI...")
    response = client.chat(model=model_name, messages=messages)
    
    print(f"[Input]: The battery life is okay, nothing special but it works.")
    print(f"[AI Output]: {response['message']['content']}")

if __name__ == "__main__":
    test_few_shot_prompting()