import os
from ollama import Client
from dotenv import load_dotenv

load_dotenv()
client = Client(host='https://ollama.com', headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'})
model_name = os.getenv("OLLAMA_MODEL", "gemma3:27b")

def test_temperature():
    print("--- 2. Testing Temperature (Creativity) ---")
    prompt = "Write a one-sentence story about a robot."

    # Test 1: Low Temperature (0.0) - Focused & Deterministic
    print("\n[Testing with Temperature = 0.0 (Strict)]")
    response_low = client.chat(
        model=model_name, 
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.0} # Ollama options parameter
    )
    print(f"Result: {response_low['message']['content']}")

    # Test 2: High Temperature (0.9) - Highly Creative/Random
    print("\n[Testing with Temperature = 0.9 (Creative)]")
    response_high = client.chat(
        model=model_name, 
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.9}
    )
    print(f"Result: {response_high['message']['content']}")

if __name__ == "__main__":
    test_temperature()