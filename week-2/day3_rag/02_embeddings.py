# 02_embeddings.py
import os
from ollama import Client
from dotenv import load_dotenv

load_dotenv()
client = Client(host='https://ollama.com', headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'})
# We use a specialized embedding model, not a chat model
embed_model = "nomic-embed-text" 

def generate_embeddings():
    print("--- 2. Generating Text Embeddings ---")
    
    sample_text = "Retrieval-Augmented Generation (RAG) is highly effective for enterprise AI."
    print(f"Input Text: '{sample_text}'\n")
    
    try:
        print("Converting text to vectors (Embeddings)...")
        # Calling the embed API
        response = client.embeddings(
            model=embed_model,
            prompt=sample_text
        )
        
        vector = response['embedding']
        print(f"✅ Embedding Generation Successful!")
        print(f"Vector Dimensions (Length of array): {len(vector)}")
        print(f"Preview of Vector: {vector[:5]} ... (truncated)")
        
    except Exception as e:
        print(f"Error: {e}\n(Make sure 'nomic-embed-text' is available on your Ollama host)")

if __name__ == "__main__":
    generate_embeddings()