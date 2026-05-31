# 01_chromadb_basics.py
import chromadb

def test_vector_db():
    print("--- 1. Testing ChromaDB Vector Database ---")
    
    # 1. Initialize ChromaDB Client (In-Memory for testing)
    client = chromadb.Client()
    
    # 2. Create a Collection (Like a Table in SQL)
    collection = client.create_collection(name="ai_knowledge_base")
    print("✅ Collection 'ai_knowledge_base' created.")
    
    # 3. Add Documents (Chroma automatically converts these to embeddings behind the scenes)
    documents = [
        "Retrieval-Augmented Generation (RAG) combines search and LLM generation.",
        "Python is the most popular programming language for AI.",
        "Vector databases store data as high-dimensional vectors for fast similarity search."
    ]
    ids = ["doc1", "doc2", "doc3"]
    
    collection.add(
        documents=documents,
        ids=ids
    )
    print("✅ Stored 3 documents into the Vector DB.\n")
    
    # 4. Perform a Similarity Search
    query = "What is used to store high-dimensional vectors?"
    print(f"🔍 Searching DB for: '{query}'")
    
    results = collection.query(
        query_texts=[query],
        n_results=1 # We only want the top 1 best match
    )
    
    print("\n[Search Result]:")
    print(f"Matched Document ID: {results['ids'][0][0]}")
    print(f"Extracted Context: {results['documents'][0][0]}")
    # Distance indicates how close the match is (Lower is better)
    print(f"Distance Score: {results['distances'][0][0]:.4f}")

if __name__ == "__main__":
    test_vector_db()