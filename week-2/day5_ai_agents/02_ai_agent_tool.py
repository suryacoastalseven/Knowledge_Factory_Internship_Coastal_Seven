# 02_ai_agent_tool.py
import os
import json
from ollama import Client
from dotenv import load_dotenv

load_dotenv()
client = Client(host='https://ollama.com', headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'})
model_name = os.getenv("OLLAMA_MODEL", "gemma3:27b")

# 1. Define the Tool (A simple python function)
def calculate_multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    print(f"\n[🔧 TOOL TRIGGERED]: Calculating {a} * {b} ...")
    return a * b

def test_ai_agent():
    print("--- 2. AI Agent with Tool Usage ---\n")
    
    user_query = "If I have 145 apples and each costs $3.5, what is the total cost?"
    print(f"👤 User: {user_query}")
    print("🤖 Agent is thinking...\n")
    
    # Prompting the LLM to act as an Agent that outputs JSON to trigger tools
    agent_prompt = f"""
    You are an AI Agent with access to a calculator tool. 
    User question: {user_query}
    
    Instead of guessing the math, extract the numbers and return a JSON object with keys "a" and "b" to multiply them. 
    Return ONLY valid JSON. Example: {{"a": 10, "b": 5}}
    """
    
    try:
        # Step 1: LLM Reasoning
        response = client.chat(
            model=model_name,
            messages=[{"role": "user", "content": agent_prompt}],
            options={"temperature": 0.0} # Needs to be strict for JSON
        )
        
        json_output = response['message']['content'].strip()
        
        # Cleaning up markdown formatting if the LLM adds it
        if json_output.startswith("```json"):
            json_output = json_output[7:-3].strip()
            
        print(f"🧠 Agent decided to use tool with parameters: {json_output}")
        
        # Step 2: Tool Execution (Python runs it)
        params = json.loads(json_output)
        tool_result = calculate_multiply(params["a"], params["b"])
        
        # Step 3: Final Answer Generation
        print(f"\n✅ [Final Agent Response]: The total cost is ${tool_result}")
        
    except Exception as e:
        print(f"Agent failed to execute: {e}")

if __name__ == "__main__":
    test_ai_agent()