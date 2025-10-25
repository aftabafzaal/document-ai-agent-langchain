# 🚀 Quick Code Reference

## File-by-File Breakdown

### 1. `config/settings.py` (50 lines)
**Purpose:** Central configuration

**Key Code:**
```python
class Settings(BaseSettings):
    EMBEDDING_PROVIDER: str = "huggingface"  # Which embedding model
    LLM_PROVIDER: str = "openai"             # Which LLM
    OPENAI_API_KEY: Optional[str] = None     # API key
    CHUNK_SIZE: int = 1000                   # Text chunk size
```

**What to modify:**
- Change `CHUNK_SIZE` for different chunk sizes
- Add new settings as needed

---

### 2. `src/core/langchain_loader.py` (94 lines)
**Purpose:** Load documents from files

**Key Code:**
```python
class LangChainDocumentProcessor:
    def __init__(self):
        self.loader_mapping = {
            '.pdf': PyPDFLoader,        # PDF files
            '.docx': Docx2txtLoader,    # Word docs
            '.txt': TextLoader,         # Text files
        }
    
    def load_documents_from_folder(self, folder_path: str):
        """Loads all supported files from folder"""
        for file in folder:
            loader = self.loader_mapping[file.extension]
            documents += loader.load()
        return documents
```

**What to modify:**
- Add new file types to `loader_mapping`

---

### 3. `src/core/text_splitter.py` (65 lines)
**Purpose:** Split documents into chunks

**Key Code:**
```python
class AdvancedTextSplitter:
    def split_documents(self, documents):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". "]  # Split priority
        )
        return splitter.split_documents(documents)
```

**What to modify:**
- Change separators for different splitting logic
- Add preprocessing before splitting

---

### 4. `src/embeddings/embedding_manager.py` (43 lines)
**Purpose:** Convert text to vectors

**Key Code:**
```python
class EmbeddingManager:
    def _initialize_embeddings(self):
        if provider == "huggingface":
            self.embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-mpnet-base-v2"
            )
        elif provider == "openai":
            self.embedding_model = OpenAIEmbeddings()
```

**What to modify:**
- Change model_name for different embedding models
- Add new providers

---

### 5. `src/vector_store/vector_store_manager.py` (87 lines)
**Purpose:** Store and search vectors

**Key Code:**
```python
class VectorStoreManager:
    def add_documents(self, documents):
        """Add to vector store"""
        self.vector_store.add_documents(documents)
    
    def similarity_search(self, query: str, k: int = 4):
        """Find similar documents"""
        return self.vector_store.similarity_search(query, k=k)
```

**What to modify:**
- Change `k` for more/fewer results
- Add filtering by metadata

---

### 6. `src/agents/simple_qa_agent.py` (94 lines)
**Purpose:** AI agent that answers questions

**Key Code:**
```python
class SimpleQAAgent:
    def query(self, question: str):
        # 1. Get relevant docs
        docs = self.retriever.invoke(question)
        
        # 2. Generate answer
        answer = self.chain.invoke(question)
        
        return {"answer": answer, "source_documents": docs}
```

**What to modify:**
- Change prompt template for different answer styles
- Add conversation memory

---

### 7. `src/api/main.py` (130 lines)
**Purpose:** REST API server

**Key Code:**
```python
@app.post("/upload/")
async def upload_files(files: List[UploadFile]):
    """Upload documents"""
    save_files(files)
    background_tasks.add_task(process_documents, files)

@app.post("/query/")
async def query_documents(request: QueryRequest):
    """Ask questions"""
    result = ai_agent.query(request.question)
    return result
```

**What to modify:**
- Add new endpoints
- Change response format

---

## Common Modifications

### Add New File Type
```python
# In langchain_loader.py
from langchain_community.document_loaders import UnstructuredExcelLoader

self.loader_mapping['.xlsx'] = UnstructuredExcelLoader
```

### Change Prompt
```python
# In simple_qa_agent.py
prompt = PromptTemplate.from_template("""
You are a helpful assistant. Answer based on this context:

Context: {context}
Question: {question}

Provide a detailed answer:
""")
```

### Add Debug Endpoint
```python
# In main.py
@app.get("/debug/stats")
async def get_stats():
    return {
        "total_chunks": vector_store_manager.count(),
        "model": settings.LLM_MODEL
    }
```

### Change Number of Results
```python
# In main.py, when initializing
retriever = vector_store_manager.as_retriever(
    search_kwargs={"k": 10}  # Return 10 chunks instead of 4
)
```

---

## Quick Testing

### Test Upload
```bash
curl -X POST http://localhost:8000/upload/ \
  -F "files=@test.pdf"
```

### Test Query
```bash
curl -X POST http://localhost:8000/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this about?"}'
```

### Check Logs
```bash
docker-compose logs -f document-ai-agent
```

---

## Code Flow Cheat Sheet

```
UPLOAD:
File → Save → Load → Split → Embed → Store
       ↓      ↓      ↓       ↓       ↓
     main   loader  split  embed  vector_db

QUERY:
Question → Embed → Search → Format → LLM → Answer
           ↓        ↓        ↓       ↓      ↓
         embed   vector_db  agent  openai  main
```

---

## Dependencies Reference

```txt
Core:
- fastapi         → Web server
- langchain       → AI framework
- chromadb        → Vector database

Embeddings:
- sentence-transformers → HuggingFace models
- langchain-openai      → OpenAI embeddings

LLMs:
- langchain-openai     → GPT models
- langchain-anthropic  → Claude models

Document Loaders:
- pypdf          → PDF files
- docx2txt       → Word files
- unstructured   → Various formats
```

---

## Environment Variables Quick Reference

```bash
# Model Selection
EMBEDDING_PROVIDER=huggingface  # or openai
LLM_PROVIDER=openai             # or anthropic or local

# API Keys
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
HUGGINGFACEHUB_API_TOKEN=hf_...

# Model Names
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
LLM_MODEL=gpt-3.5-turbo

# Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_FILE_SIZE=104857600

# Storage
UPLOAD_DIRECTORY=./data/uploads
PERSIST_DIRECTORY=./data/vector_store
VECTOR_STORE=chroma
```

