import os
import logging
from ollama import Client
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class EnterpriseAIAgent:
    """Production-ready AI Wrapper for Ollama Cloud Interactions."""
    
    def __init__(self):
        self.api_key = os.getenv("OLLAMA_API_KEY", "dummy_key")
        self.model = os.getenv("OLLAMA_MODEL", "gemma3:27b")
        
        try:
            self.client = Client(host='https://ollama.com', headers={'Authorization': f'Bearer {self.api_key}'})
            logger.info(f"✅ AI Agent Initialized (Model: {self.model})")
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")

    def generate_answer(self, user_query: str, context: str) -> str:
        """Generates contextual answers preventing hallucinations."""
        
        system_prompt = """
        You are 'Lexi', an elite Enterprise AI Analyst.
        Rules:
        1. Base your answer strictly on the provided 'Context'.
        2. If the answer is not in the context, say: "Based on the provided document, I cannot determine this." Do NOT hallucinate.
        3. Format your response professionally using Markdown (bolding key terms, using bullet points).
        4. Be concise but comprehensive.
        """

        full_prompt = f"### CONTEXT ###\n{context}\n\n### USER QUESTION ###\n{user_query}"

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt}
                ],
                options={"temperature": 0.1, "top_p": 0.9} # Tuned for factual accuracy
            )
            return response['message']['content']
        except Exception as e:
            logger.error(f"LLM Generation Error: {e}")
            return "⚠️ System Error: Unable to reach the AI Engine. Please check API configurations."