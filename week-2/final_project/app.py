import os
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

from rag_engine import DocumentRAGEngine
from ai_agent import EnterpriseAIAgent

# Robust Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="LexiRAG Enterprise Production API", version="1.0.0")

# CORS for external integrations if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("temp_uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Singleton Initialization
rag_engine = DocumentRAGEngine()
ai_agent = EnterpriseAIAgent()

class ChatResponse(BaseModel):
    response: str
    status: str

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Handles secure PDF upload and RAG indexing."""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")
        
    file_path = f"temp_uploads/{file.filename}"
    
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
            
        logger.info(f"Initiating processing for: {file.filename}")
        success, message = rag_engine.process_and_store_pdf(file_path)
        
        if not success:
            raise HTTPException(status_code=500, detail=message)
            
        return {"status": "success", "message": message, "filename": file.filename}
        
    finally:
        if os.path.exists(file_path):
            os.remove(file_path) # Clean up storage

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_document(query: str = Form(...)):
    """Handles AI querying over the vector database."""
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    logger.info(f"Incoming Query: {query}")
    
    context = rag_engine.retrieve_context(query)
    
    if not context:
        return ChatResponse(response="No document is loaded or the document contains no relevant text. Please upload a valid PDF.", status="warning")
        
    answer = ai_agent.generate_answer(query, context)
    return ChatResponse(response=answer, status="success")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    logger.info(f"🚀 Launching Production Server on port {port}")
    # BUG FIX: Set reload=False so that ChromaDB writing files doesn't restart the server mid-upload!
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)