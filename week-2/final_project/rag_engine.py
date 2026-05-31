import os
import chromadb
from chromadb.config import Settings
import PyPDF2
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class DocumentRAGEngine:
    """Enterprise Grade RAG Engine with Persistent Vector Storage and Advanced Chunking."""
    
    def __init__(self):
        # Using Persistent DB so data survives server restarts
        os.makedirs("chroma_storage", exist_ok=True)
        
        # BUG FIX: Disable telemetry to stop PostHog errors filling up your terminal
        self.chroma_client = chromadb.PersistentClient(
            path="./chroma_storage",
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.collection_name = "enterprise_docs"
        try:
            self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name)
            logger.info("✅ Persistent ChromaDB Initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")

    def clear_database(self):
        """Wipes previous knowledge base for a fresh document context."""
        try:
            self.chroma_client.delete_collection(name=self.collection_name)
            self.collection = self.chroma_client.create_collection(name=self.collection_name)
        except Exception:
            pass

    def process_and_store_pdf(self, file_path: str) -> Tuple[bool, str]:
        """Extracts, chunks, and creates vector embeddings securely."""
        try:
            self.clear_database() # Ensure only current document is queried
            
            text = ""
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + " "
            
            text = " ".join(text.split()) # Clean multiple spaces
            
            if not text.strip():
                return False, "PDF is empty or unreadable (might be a scanned image)."

            # Advanced Semantic Overlap Chunking
            chunk_size = 1200
            overlap = 200
            chunks = []
            
            for i in range(0, len(text), chunk_size - overlap):
                chunk = text[i : i + chunk_size]
                if len(chunk) > 100: 
                    chunks.append(chunk)

            if not chunks:
                return False, "Document does not contain enough text."

            # Batch insert for performance
            ids = [f"chunk_{i}" for i in range(len(chunks))]
            self.collection.add(documents=chunks, ids=ids)
            
            logger.info(f"✅ Stored {len(chunks)} chunks into Vector DB.")
            return True, f"Successfully processed {len(chunks)} knowledge chunks."
            
        except Exception as e:
            logger.error(f"PDF Processing Error: {e}")
            return False, f"Internal Processing Error: {str(e)}"

    def retrieve_context(self, query: str, top_k: int = 4) -> str:
        """Retrieves top K semantically relevant chunks."""
        if self.collection.count() == 0:
            return ""

        results = self.collection.query(query_texts=[query], n_results=top_k)
        
        if not results['documents'] or not results['documents'][0]:
            return ""
            
        return "\n\n---\n\n".join(results['documents'][0])