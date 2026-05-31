# 02_prompt_chaining.py
import os
from ollama import Client
from dotenv import load_dotenv

load_dotenv()
client = Client(host='https://ollama.com', headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'})
model_name = os.getenv("OLLAMA_MODEL", "gemma3:27b")

def prompt_chaining():
    print("--- 2. Testing Prompt Chaining ---\n")
    
    # STEP 1: Generate a Title
    topic = "Artificial Intelligence in Healthcare"
    print(f"Step 1: Generating a catchy title for topic: '{topic}'...")
    
    resp_1 = client.chat(
        model=model_name,
        messages=[{"role": "user", "content": f"Write a catchy, 5-word title for an article about {topic}. Return ONLY the title."}]
    )
    title = resp_1['message']['content'].strip()
    print(f"✅ Generated Title: {title}\n")
    
    # STEP 2: Use the Title to generate a short intro
    print("Step 2: Passing the title to generate an introduction...")
    resp_2 = client.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a professional blog writer."},
            {"role": "user", "content": f"Write a 2-sentence introduction for an article titled: '{title}'"}
        ]
    )
    intro = resp_2['message']['content'].strip()
    print(f"✅ Generated Intro: {intro}\n")
    
    print("🎉 Prompt Chaining Successful!")

if __name__ == "__main__":
    prompt_chaining()