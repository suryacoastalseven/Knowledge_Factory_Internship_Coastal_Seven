# 03_api_plus_ai_workflow.py
import requests

def complete_workflow():
    print("--- 🚀 AI-Assisted API Workflow ---")
    # Step 1: Fetching an IP address info via public API
    url = "https://ipapi.co/json/"
    print("\n1. Fetching Data from REST API...")
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        data = response.json()
        
        city = data.get("city", "Unknown City")
        country = data.get("country_name", "Unknown Country")
        print(f"✅ Data Fetched: You are located in {city}, {country}.")
        
        # Step 2: Passing it to AI Tooling logic (simulated here for safety)
        print("\n2. Passing Data to AI for analysis...")
        prompt = f"Write a 2-line welcome message for a user from {city}, {country}."
        print(f"Prompt sent to AI: '{prompt}'")
        
        # Here you would call your OpenAI/Ollama function. 
        # For demo, printing the expected behavior:
        print("\n✅ AI Assisted Response:")
        print(f"Welcome friend from {city}! Hope the weather in {country} is great today!")
        
    except Exception as e:
        print(f"Workflow failed: {e}")

complete_workflow()