# 02_rag_pipeline.py
import os
import chromadb
from ollama import Client
from dotenv import load_dotenv

load_dotenv()
ollama_client = Client(host='https://ollama.com', headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'})
model_name = os.getenv("OLLAMA_MODEL", "gemma3:27b")

def rag_pipeline():
    print("--- 2. End-to-End RAG Pipeline ---\n")
    
    # Setup Vector DB
    db = chromadb.Client()
    collection = db.create_collection(name="company_policies")
    
    # Insert Company Data
    collection.add(
        documents=[
            "Employees can take up to 20 days of paid leave per year.",
            "Work from home is allowed only on Tuesdays and Thursdays.",
            "The office cafeteria is open from 12 PM to 2 PM."
        ],
        ids=["policy1", "policy2", "policy3"]
    )
    
    # User Query
    user_query = "How many days can I work from home?"
    print(f"👤 User Question: '{user_query}'\n")
    
    # 1. Retrieve (లాగడం)
    print("🔍 1. Retrieving context from Vector DB...")
    results = collection.query(query_texts=[user_query], n_results=1)
    retrieved_context = results['documents'][0][0]
    print(f"   -> Found Context: '{retrieved_context}'\n")
    
    # 2. Augment & Generate (కలపడం మరియు ఆన్సర్ రాయడం)
    print("🧠 2. Sending Context + Question to LLM...")
    
    # This is the RAG Prompt Template
    final_prompt = f"""
    Answer the user's question using ONLY the provided context. If the answer is not in the context, say "I don't know."
    
    Context: {retrieved_context}
    Question: {user_query}
    """
    
    response = ollama_client.chat(
        model=model_name,
        messages=[{"role": "user", "content": final_prompt}]
    )
    
    print(f"\n✅ [AI Final Answer]:\n{response['message']['content']}")

if __name__ == "__main__":
    rag_pipeline()