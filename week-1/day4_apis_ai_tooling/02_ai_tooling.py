# 02_ai_tooling.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# .env లో దాచిన API కీ ని లోడ్ చేస్తుంది
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

def summarize_text_with_ai(text_to_summarize: str):
    """Uses AI to perform a task (e.g., summarization or sentiment analysis)"""
    if not API_KEY or API_KEY == "your_openai_api_key_here":
        print("⚠️ Warning: Valid OpenAI API key not found in .env file.")
        print("💡 Assuming Ollama Local AI fallback (Mock response):")
        print(f"AI Summary: The provided text is about '{text_to_summarize[:10]}...'")
        return

    try:
        client = OpenAI(api_key=API_KEY)
        print("Connecting to OpenAI... 🤖")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # లేదా నీకు నచ్చిన మోడల్
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": f"Explain this text in one sentence: {text_to_summarize}"}
            ]
        )
        print("\n✅ AI Response:")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"❌ AI Error: {e}")

# టెస్ట్ చేద్దాం
sample_data = "REST (Representational State Transfer) is an architectural style for APIs."
summarize_text_with_ai(sample_data)