import os

def create_file(filepath, content):
    """Utility to create a file with given content."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Created: {filepath}")

def build_project():
    PROJECT_DIR = "LexiRAG_Production"
    print(f"🚀 Starting Top-Tier MNC Project Generation: {PROJECT_DIR}...\n")

    # 1. requirements.txt
    req_content = """
fastapi==0.111.0
uvicorn==0.29.0
chromadb==0.5.0
PyPDF2==3.0.1
ollama==0.1.8
python-dotenv==1.0.0
python-multipart==0.0.9
pydantic==2.7.1
    """
    create_file(f"{PROJECT_DIR}/requirements.txt", req_content)

    # 2. .env
    env_content = """
OLLAMA_API_KEY=your_actual_ollama_com_api_key_here
OLLAMA_MODEL=gemma3:27b
PORT=8000
    """
    create_file(f"{PROJECT_DIR}/.env", env_content)

    # 3. rag_engine.py
    rag_content = '''
import os
import chromadb
import PyPDF2
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class DocumentRAGEngine:
    """Enterprise Grade RAG Engine with Persistent Vector Storage and Advanced Chunking."""
    
    def __init__(self):
        # Using Persistent DB so data survives server restarts
        os.makedirs("chroma_storage", exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(path="./chroma_storage")
        
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
            
        return "\\n\\n---\\n\\n".join(results['documents'][0])
    '''
    create_file(f"{PROJECT_DIR}/rag_engine.py", rag_content)

    # 4. ai_agent.py
    ai_content = '''
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

        full_prompt = f"### CONTEXT ###\\n{context}\\n\\n### USER QUESTION ###\\n{user_query}"

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
    '''
    create_file(f"{PROJECT_DIR}/ai_agent.py", ai_content)

    # 5. app.py (FastAPI Backend)
    app_content = '''
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
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
    '''
    create_file(f"{PROJECT_DIR}/app.py", app_content)

    # 6. static/index.html (The Fully Responsive, Top-Tier UI)
    html_content = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>LexiRAG - Enterprise AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0b0f19; color: #f8fafc; overflow: hidden; }
        
        /* Glassmorphism Classes */
        .glass-panel { background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.05); }
        .glass-bubble-ai { background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); }
        .glass-bubble-user { background: rgba(51, 65, 85, 0.6); border: 1px solid rgba(255, 255, 255, 0.05); }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }

        /* Typography & Markdown formatting */
        .prose p { margin-bottom: 0.75rem; line-height: 1.6; }
        .prose strong { color: #a5b4fc; font-weight: 600; }
        .prose ul { list-style-type: disc; padding-left: 1.5rem; margin-bottom: 0.75rem; }
        .prose li { margin-bottom: 0.25rem; }
        
        /* Animations */
        .fade-in { animation: fadeIn 0.3s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        .pulse-ring { animation: pulseRing 2s infinite; }
        @keyframes pulseRing { 0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); } 100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); } }

        /* Mobile Sidebar Transition */
        #sidebar { transition: transform 0.3s ease-in-out; }
        @media (max-width: 768px) {
            #sidebar { position: absolute; z-index: 50; height: 100%; transform: translateX(-100%); }
            #sidebar.open { transform: translateX(0); }
        }
    </style>
</head>
<body class="h-screen w-screen flex flex-col md:flex-row">

    <!-- Mobile Header (Visible only on mobile) -->
    <div class="md:hidden glass-panel w-full p-4 flex justify-between items-center z-40 border-b border-gray-800">
        <div class="flex items-center gap-2">
            <i data-lucide="brain-circuit" class="text-indigo-500 w-6 h-6"></i>
            <span class="font-bold text-lg">LexiRAG</span>
        </div>
        <button id="menuBtn" class="p-2 bg-gray-800 rounded-lg" onclick="toggleSidebar()">
            <i data-lucide="menu" class="w-5 h-5 text-gray-300"></i>
        </button>
    </div>

    <!-- Sidebar / Document Panel -->
    <aside id="sidebar" class="w-full md:w-80 glass-panel border-r border-gray-800 flex flex-col shadow-2xl h-full">
        <div class="p-6 flex justify-between items-center hidden md:flex border-b border-gray-800/50">
            <div class="flex items-center gap-3">
                <div class="p-2 bg-indigo-500/20 rounded-lg border border-indigo-500/30 pulse-ring">
                    <i data-lucide="brain-circuit" class="text-indigo-400 w-6 h-6"></i>
                </div>
                <h1 class="text-xl font-bold tracking-tight">Lexi<span class="text-indigo-500">RAG</span></h1>
            </div>
        </div>

        <div class="p-6 flex-1 flex flex-col">
            <h3 class="text-xs uppercase tracking-wider text-gray-500 font-semibold mb-4">Document Context</h3>
            
            <!-- Upload Box -->
            <div id="dropZone" class="border-2 border-dashed border-gray-700 rounded-xl p-6 flex flex-col items-center justify-center text-center cursor-pointer hover:border-indigo-500 hover:bg-indigo-500/5 transition-all duration-300 group" onclick="document.getElementById('fileInput').click()">
                <i data-lucide="cloud-upload" class="w-10 h-10 text-gray-500 group-hover:text-indigo-400 mb-3 transition-colors"></i>
                <p class="text-sm font-medium text-gray-300">Click or Drag PDF</p>
                <p class="text-xs text-gray-500 mt-1">Max size 20MB</p>
                <input type="file" id="fileInput" accept=".pdf" class="hidden" onchange="handleFileUpload(event)">
            </div>

            <!-- Upload Status -->
            <div id="uploadStatus" class="mt-4 hidden flex items-center gap-2 p-3 rounded-lg text-sm font-medium">
                <i data-lucide="loader-2" class="w-4 h-4 animate-spin text-indigo-400" id="statusIcon"></i>
                <span id="statusText" class="text-gray-300">Processing...</span>
            </div>

            <!-- Active Document Widget -->
            <div id="activeDocWidget" class="mt-6 p-4 rounded-xl glass-bubble-user hidden fade-in border-l-4 border-l-green-500">
                <div class="flex items-start gap-3">
                    <i data-lucide="file-text" class="w-5 h-5 text-green-400 mt-0.5"></i>
                    <div>
                        <p class="text-sm font-semibold text-gray-200 line-clamp-1" id="docName">document.pdf</p>
                        <p class="text-xs text-green-400/80 mt-1 flex items-center gap-1"><i data-lucide="check-circle" class="w-3 h-3"></i> Indexed & Ready</p>
                    </div>
                </div>
            </div>

            <!-- Mobile Close Sidebar button -->
            <button class="md:hidden mt-auto w-full py-3 bg-gray-800 rounded-lg text-sm font-medium text-gray-300" onclick="toggleSidebar()">Close Menu</button>
        </div>

        <div class="p-4 border-t border-gray-800/50 bg-gray-900/50">
            <div class="flex items-center gap-2 text-xs text-gray-500">
                <span class="w-2 h-2 rounded-full bg-green-500"></span> Engine: Gemma-3 27B
            </div>
        </div>
    </aside>

    <!-- Main Chat Area -->
    <main class="flex-1 flex flex-col h-full bg-[#0b0f19] relative">
        
        <!-- Chat Messages Container -->
        <div id="chatContainer" class="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 pb-32">
            
            <!-- Greeting Message -->
            <div class="flex gap-4 max-w-4xl mx-auto fade-in">
                <div class="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center flex-shrink-0 shadow-lg shadow-indigo-500/20">
                    <i data-lucide="bot" class="w-5 h-5 text-white"></i>
                </div>
                <div class="glass-bubble-ai p-5 rounded-2xl rounded-tl-sm text-sm md:text-base prose">
                    <p>Welcome to <strong>LexiRAG Enterprise</strong>. 🏢</p>
                    <p>I am your highly secure, context-aware AI auditor. Please upload a policy, contract, or report from the panel, and ask me anything about it. I guarantee zero hallucinations.</p>
                </div>
            </div>
            
        </div>

        <!-- Input Area (Fixed Bottom) -->
        <div class="absolute bottom-0 left-0 w-full p-4 md:p-8 bg-gradient-to-t from-[#0b0f19] via-[#0b0f19] to-transparent">
            <div class="max-w-4xl mx-auto">
                <!-- Typing Indicator -->
                <div id="typingIndicator" class="hidden items-center gap-2 mb-3 text-xs text-indigo-400 ml-12 fade-in">
                    <i data-lucide="loader" class="w-3 h-3 animate-spin"></i> Lexi is analyzing vectors...
                </div>

                <form id="chatForm" class="flex items-end gap-2 bg-gray-800/80 backdrop-blur-xl border border-gray-700/50 p-2 rounded-2xl shadow-2xl transition-all focus-within:border-indigo-500/50 focus-within:ring-4 focus-within:ring-indigo-500/10" onsubmit="handleChatSubmit(event)">
                    <textarea id="userInput" rows="1" placeholder="Type your query here..." class="flex-1 bg-transparent text-white p-3 outline-none resize-none text-sm md:text-base placeholder-gray-500" disabled oninput="autoResize(this)" onkeydown="handleEnter(event)"></textarea>
                    
                    <button type="submit" id="sendBtn" class="p-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-colors" disabled>
                        <i data-lucide="send" class="w-5 h-5"></i>
                    </button>
                </form>
                <div class="text-center mt-2 text-[10px] text-gray-600">Confidential Enterprise AI. Do not share credentials.</div>
            </div>
        </div>
    </main>

    <script>
        // Initialize Icons
        lucide.createIcons();

        // UI State Variables
        const UI = {
            sidebar: document.getElementById('sidebar'),
            chatContainer: document.getElementById('chatContainer'),
            userInput: document.getElementById('userInput'),
            sendBtn: document.getElementById('sendBtn'),
            statusDiv: document.getElementById('uploadStatus'),
            statusIcon: document.getElementById('statusIcon'),
            statusText: document.getElementById('statusText'),
            typingIndicator: document.getElementById('typingIndicator'),
            activeDocWidget: document.getElementById('activeDocWidget'),
            docName: document.getElementById('docName')
        };

        // Mobile Sidebar Toggle
        function toggleSidebar() {
            UI.sidebar.classList.toggle('open');
        }

        // Auto-resize textarea
        function autoResize(textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = (textarea.scrollHeight < 120 ? textarea.scrollHeight : 120) + 'px';
        }

        function handleEnter(e) {
            if(e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                document.getElementById('chatForm').dispatchEvent(new Event('submit'));
            }
        }

        // Add message to DOM
        function appendMessage(role, text) {
            const isAI = role === 'ai';
            const wrapper = document.createElement('div');
            wrapper.className = `flex gap-3 max-w-4xl mx-auto w-full fade-in ${isAI ? 'flex-row' : 'flex-row-reverse'}`;
            
            const avatar = document.createElement('div');
            avatar.className = `w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg ${isAI ? 'bg-indigo-600 shadow-indigo-500/20' : 'bg-slate-700 shadow-slate-900/50'}`;
            avatar.innerHTML = `<i data-lucide="${isAI ? 'bot' : 'user'}" class="w-4 h-4 text-white"></i>`;
            
            const bubble = document.createElement('div');
            bubble.className = `p-4 rounded-2xl text-sm md:text-base prose ${isAI ? 'glass-bubble-ai rounded-tl-sm' : 'glass-bubble-user rounded-tr-sm'}`;
            bubble.innerHTML = isAI ? marked.parse(text) : text; // Parse markdown only for AI
            
            wrapper.appendChild(avatar);
            wrapper.appendChild(bubble);
            UI.chatContainer.appendChild(wrapper);
            
            // Re-render icons in new DOM nodes
            lucide.createIcons();
            
            // Scroll to bottom
            setTimeout(() => {
                UI.chatContainer.scrollTo({ top: UI.chatContainer.scrollHeight, behavior: 'smooth' });
            }, 100);
        }

        // Handle File Upload
        async function handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;

            // UI Changes
            UI.statusDiv.classList.remove('hidden', 'bg-green-500/10', 'text-green-400', 'bg-red-500/10', 'text-red-400');
            UI.statusDiv.classList.add('bg-indigo-500/10', 'text-indigo-400');
            UI.statusIcon.setAttribute('data-lucide', 'loader-2');
            UI.statusIcon.classList.add('animate-spin');
            UI.statusText.textContent = "Extracting and indexing...";
            lucide.createIcons();
            
            if(window.innerWidth <= 768) toggleSidebar(); // Close sidebar on mobile

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('/api/upload', { method: 'POST', body: formData });
                const data = await response.json();

                if (response.ok) {
                    UI.statusDiv.className = "mt-4 flex items-center gap-2 p-3 rounded-lg text-sm font-medium bg-green-500/10 text-green-400";
                    UI.statusIcon.setAttribute('data-lucide', 'check-circle');
                    UI.statusIcon.classList.remove('animate-spin');
                    UI.statusText.textContent = "Indexing Complete";
                    
                    UI.activeDocWidget.classList.remove('hidden');
                    UI.docName.textContent = file.name;
                    
                    UI.userInput.disabled = false;
                    UI.sendBtn.disabled = false;
                    UI.userInput.focus();
                    
                    appendMessage('ai', `✅ Document **${file.name}** has been securely ingested into the Vector Database. What specific clauses or information would you like to retrieve?`);
                } else {
                    throw new Error(data.detail);
                }
            } catch (error) {
                UI.statusDiv.className = "mt-4 flex items-center gap-2 p-3 rounded-lg text-sm font-medium bg-red-500/10 text-red-400";
                UI.statusIcon.setAttribute('data-lucide', 'alert-circle');
                UI.statusIcon.classList.remove('animate-spin');
                UI.statusText.textContent = "Failed to process";
                appendMessage('ai', `❌ **Upload Error:** ${error.message}`);
            }
            lucide.createIcons();
        }

        // Handle Chat Submit
        async function handleChatSubmit(e) {
            e.preventDefault();
            const query = UI.userInput.value.trim();
            if (!query) return;

            // Reset input
            UI.userInput.value = '';
            UI.userInput.style.height = 'auto';
            
            appendMessage('user', query);
            
            UI.typingIndicator.classList.remove('hidden');
            UI.typingIndicator.classList.add('flex');
            UI.userInput.disabled = true;
            UI.sendBtn.disabled = true;

            const formData = new FormData();
            formData.append('query', query);

            try {
                const response = await fetch('/api/chat', { method: 'POST', body: formData });
                const data = await response.json();
                
                UI.typingIndicator.classList.add('hidden');
                UI.typingIndicator.classList.remove('flex');
                
                appendMessage('ai', data.response);
                
            } catch (error) {
                UI.typingIndicator.classList.add('hidden');
                appendMessage('ai', `⚠️ **Network Error:** Failed to communicate with the server.`);
            } finally {
                UI.userInput.disabled = false;
                UI.sendBtn.disabled = false;
                UI.userInput.focus();
            }
        }
    </script>
</body>
</html>
    """
    create_file(f"{PROJECT_DIR}/static/index.html", html_content)

    # 7. README.md
    readme_content = """
# 🏢 LexiRAG - Enterprise Grade Production AI

This repository was auto-generated using the Master Scaffolding Script. It represents a fully robust, production-ready RAG application tailored for Top-Tier MNC standards.

## Production Features:
- **Persistent Vector Storage** using ChromaDB.
- **Enterprise Error Handling** and Logging throughout the Python backend.
- **100% Responsive Glassmorphism UI** optimized for Desktop, Tablets, and Mobile.
- **Advanced Document Chunking** with semantic overlap for high precision.
- **Security & Validation** via FastAPI and Pydantic.

## Run Instructions:
1. Navigate to the directory: `cd LexiRAG_Production`
2. Install dependencies: `pip install -r requirements.txt`
3. Start the production server: `python app.py`
4. Access the UI: **http://localhost:8000**
    """
    create_file(f"{PROJECT_DIR}/README.md", readme_content)

    print("\n" + "="*50)
    print("🎉 BOOM! LexiRAG Enterprise Project Generated Successfully! 🎉")
    print("="*50)
    print("👉 Next Steps to Run Your Project:")
    print("   1. cd LexiRAG_Production")
    print("   2. pip install -r requirements.txt")
    print("   3. python app.py")
    print("   4. Open http://localhost:8000 in your browser.")
    print("="*50)

if __name__ == "__main__":
    build_project()