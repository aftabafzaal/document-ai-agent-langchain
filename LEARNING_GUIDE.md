# 📚 Document AI Agent - Complete Learning Guide

## 🎯 What You'll Learn

1. **Project Structure** - How files are organized
2. **Core Concepts** - RAG, embeddings, vector stores, LLMs
3. **Code Flow** - Step-by-step execution
4. **Key Components** - What each file does
5. **How to Modify** - Extend and customize

---

## 📁 Project Structure

```
document-ai-agent-langchain/
├── config/
│   └── settings.py              # Configuration (API keys, models, settings)
├── src/
│   ├── core/
│   │   ├── langchain_loader.py  # Loads documents (PDF, DOCX, etc.)
│   │   └── text_splitter.py     # Splits documents into chunks
│   ├── embeddings/
│   │   └── embedding_manager.py # Converts text to vectors
│   ├── vector_store/
│   │   └── vector_store_manager.py # Stores & searches vectors
│   ├── agents/
│   │   └── simple_qa_agent.py   # AI agent that answers questions
│   └── api/
│       └── main.py              # FastAPI server (REST API)
├── data/
│   ├── uploads/                 # User uploaded files
│   ├── vector_store/            # ChromaDB database
│   └── cache/                   # Model cache
├── docker-compose.yml           # Docker setup
├── Dockerfile                   # Docker image definition
├── requirements.txt             # Python dependencies
└── .env                         # Environment variables (API keys)
```

---

## 🧠 Core Concepts

### 1. RAG (Retrieval-Augmented Generation)

**What is RAG?**
Instead of the AI making up answers, it first **retrieves relevant information** from your documents, then **generates an answer** based on that information.

```
Your Question
    ↓
Find Similar Documents (Retrieval)
    ↓
Send Context + Question to AI
    ↓
AI Generates Answer (Generation)
```

### 2. Embeddings (Vector Representations)

**What are embeddings?**
Converting text into numbers (vectors) that capture meaning.

```
Text: "The cat sat on the mat"
      ↓
Embedding: [0.2, -0.5, 0.8, 0.1, ...]  (768 numbers)
```

Similar texts have similar vectors, allowing semantic search!

### 3. Vector Store (Database)

**What is a vector store?**
A database optimized for storing and searching vectors.

```
Document 1: [0.2, 0.5, ...]  ← "Machine learning basics"
Document 2: [0.3, 0.4, ...]  ← "Introduction to AI"
Document 3: [-0.5, 0.1, ...] ← "Cooking recipes"

Query: "What is AI?"
Vector: [0.25, 0.45, ...]

Vector Store finds: Document 2 (most similar!)
```

### 4. LLM (Large Language Model)

**What is an LLM?**
The AI (like ChatGPT) that reads context and generates intelligent answers.

```
Input: Context + Question
Output: Natural language answer
```

---

## 🔄 Complete Flow Diagram

### **When You Upload a Document:**

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENT UPLOAD FLOW                      │
└─────────────────────────────────────────────────────────────┘

1. User uploads PDF file
   ↓
2. FastAPI receives file (main.py → /upload/ endpoint)
   ↓
3. File saved to ./data/uploads/
   ↓
4. Background processing starts (process_documents function)
   ↓
5. LangChainDocumentProcessor loads file
   │  → Uses PyPDFLoader for PDFs
   │  → Extracts text + metadata
   ↓
6. AdvancedTextSplitter splits into chunks
   │  → Each chunk = ~1000 characters
   │  → 200 character overlap for context
   ↓
7. EmbeddingManager converts chunks to vectors
   │  → Uses HuggingFace model locally
   │  → Each chunk → 768-dimensional vector
   ↓
8. VectorStoreManager stores vectors in ChromaDB
   │  → Persists to ./data/vector_store/
   │  → Ready for searching!
   ↓
9. Done! Document is searchable
```

### **When You Ask a Question:**

```
┌─────────────────────────────────────────────────────────────┐
│                      QUERY FLOW                              │
└─────────────────────────────────────────────────────────────┘

1. User sends question: "What is machine learning?"
   ↓
2. FastAPI receives query (main.py → /query/ endpoint)
   ↓
3. Question converted to vector (same embedding model)
   ↓
4. VectorStoreManager searches for similar chunks
   │  → Compares question vector with all document vectors
   │  → Returns top 4 most similar chunks
   ↓
5. SimpleQAAgent prepares prompt:
   │  Context: [Retrieved chunks]
   │  Question: "What is machine learning?"
   ↓
6. OpenAI GPT-3.5 generates answer
   │  → Reads context
   │  → Formulates answer based on documents
   ↓
7. Response returned with:
   │  → Answer
   │  → Source documents
   │  → Processing time
   ↓
8. User receives answer!
```

---

## 🔍 Deep Dive: Key Files

### 1. `config/settings.py` - Configuration Hub

**What it does:** Stores all configuration in one place.

**Key concepts:**
```python
class Settings(BaseSettings):
    EMBEDDING_PROVIDER: str = "huggingface"  # Which embedding model
    LLM_PROVIDER: str = "openai"             # Which AI for answers
    OPENAI_API_KEY: Optional[str] = None     # API credentials
    CHUNK_SIZE: int = 1000                   # Text chunk size
    
    class Config:
        env_file = ".env"  # Load from .env file
```

**How to modify:**
- Change `CHUNK_SIZE` for larger/smaller chunks
- Add new settings by adding new variables
- Environment variables override defaults

---

### 2. `src/core/langchain_loader.py` - Document Loading

**What it does:** Loads different file types (PDF, DOCX, TXT, etc.)

**Key concepts:**
```python
class LangChainDocumentProcessor:
    def __init__(self):
        # Map file extensions to loaders
        self.loader_mapping = {
            '.pdf': PyPDFLoader,      # For PDFs
            '.docx': Docx2txtLoader,  # For Word docs
            '.txt': TextLoader,       # For text files
        }
    
    def load_documents_from_folder(self, folder_path: str):
        """Load all documents from a folder"""
        for file in folder:
            loader = self.loader_mapping[file.extension]
            documents += loader.load()
        return documents
```

**How it works:**
1. Scans folder for files
2. Picks appropriate loader based on extension
3. Extracts text and metadata
4. Returns list of Document objects

**How to add new file types:**
```python
from langchain_community.document_loaders import UnstructuredExcelLoader

self.loader_mapping['.xlsx'] = UnstructuredExcelLoader
```

---

### 3. `src/core/text_splitter.py` - Chunking

**What it does:** Splits long documents into smaller, manageable chunks.

**Why needed?** 
- LLMs have token limits
- Embeddings work better on focused chunks
- Enables precise source attribution

**Key concepts:**
```python
class AdvancedTextSplitter:
    def split_documents(self, documents):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,      # Max chunk size
            chunk_overlap=200,    # Overlap for context
            separators=["\n\n", "\n", ". ", " "]  # Split priority
        )
        return splitter.split_documents(documents)
```

**How it works:**
```
Original Document (5000 chars):
"Machine learning is... [3000 more chars] ...and that's AI."

↓ Split into chunks ↓

Chunk 1 (1000 chars): "Machine learning is... [overlap] ..."
Chunk 2 (1000 chars): "... [overlap from 1] ... neural networks... [overlap] ..."
Chunk 3 (1000 chars): "... [overlap from 2] ... and that's AI."
```

**Overlap is important!** Ensures context isn't lost at boundaries.

---

### 4. `src/embeddings/embedding_manager.py` - Vector Conversion

**What it does:** Converts text to numerical vectors (embeddings).

**Key concepts:**
```python
class EmbeddingManager:
    def _initialize_embeddings(self):
        if provider == "huggingface":
            # Load local model
            self.embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-mpnet-base-v2"
            )
        elif provider == "openai":
            # Use OpenAI API
            self.embedding_model = OpenAIEmbeddings(
                api_key=settings.OPENAI_API_KEY
            )
```

**How it works:**
```
Input: "Machine learning is a subset of AI"
       ↓
Model: sentence-transformers/all-mpnet-base-v2
       ↓
Output: [0.234, -0.567, 0.891, ..., 0.123]  (768 numbers)
```

**Why HuggingFace by default?**
- FREE (runs locally)
- Good quality
- No API calls needed

---

### 5. `src/vector_store/vector_store_manager.py` - Database

**What it does:** Stores vectors and performs similarity search.

**Key concepts:**
```python
class VectorStoreManager:
    def add_documents(self, documents):
        """Add documents to vector store"""
        self.vector_store.add_documents(documents)
    
    def similarity_search(self, query: str, k: int = 4):
        """Find most similar documents"""
        return self.vector_store.similarity_search(query, k=k)
```

**How similarity search works:**
```
Query Vector:      [0.5, 0.3, 0.8]
                      ↓ Calculate distance
Doc 1 Vector:      [0.4, 0.3, 0.7]  → Distance: 0.15 ✅ Close!
Doc 2 Vector:      [0.1, 0.9, 0.2]  → Distance: 0.89 ❌ Far
Doc 3 Vector:      [0.6, 0.2, 0.9]  → Distance: 0.18 ✅ Close!

Returns: Doc 1, Doc 3 (most similar)
```

**Persistence:**
- Saves to `./data/vector_store/`
- Survives container restarts
- SQLite-based (ChromaDB)

---

### 6. `src/agents/simple_qa_agent.py` - AI Brain

**What it does:** Orchestrates retrieval and answer generation.

**Key concepts:**
```python
class SimpleQAAgent:
    def _create_chain(self):
        """Create RAG chain"""
        prompt = PromptTemplate.from_template("""
            Context: {context}
            Question: {question}
            Answer:
        """)
        
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return chain
```

**LCEL (LangChain Expression Language):**
```
Question → Retriever → Format Context → Prompt → LLM → Parse → Answer
```

**How query works:**
```python
def query(self, question: str):
    # 1. Get relevant documents
    docs = self.retriever.invoke(question)
    
    # 2. Generate answer with context
    answer = self.chain.invoke(question)
    
    # 3. Return answer + sources
    return {"answer": answer, "source_documents": docs}
```

---

### 7. `src/api/main.py` - REST API Server

**What it does:** Provides HTTP endpoints for the application.

**Key endpoints:**

#### **POST /upload/**
```python
@app.post("/upload/")
async def upload_files(files: List[UploadFile]):
    # 1. Save files
    for file in files:
        save_file(file)
    
    # 2. Process in background
    background_tasks.add_task(process_documents, files)
    
    return {"message": "Processing started"}
```

#### **POST /query/**
```python
@app.post("/query/")
async def query_documents(request: QueryRequest):
    # 1. Call AI agent
    result = ai_agent.query(request.question)
    
    # 2. Format response
    return {
        "answer": result["answer"],
        "sources": result["source_documents"]
    }
```

#### **GET /health**
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**Background processing:**
```python
def process_documents(file_paths):
    # Load → Split → Embed → Store
    documents = processor.load_documents(folder)
    chunks = splitter.split_documents(documents)
    vector_store.add_documents(chunks)
```

---

## 🔬 Step-by-Step: What Happens Internally

### **Example: Uploading `research.pdf` and asking "What is ML?"**

```
┌──────────────────────────────────────────────────────────────┐
│ STEP 1: Upload PDF                                           │
└──────────────────────────────────────────────────────────────┘

User uploads "research.pdf" (50 pages about machine learning)

main.py:
  ├─ Receives file via FastAPI
  ├─ Saves to ./data/uploads/research.pdf
  └─ Starts background task: process_documents()

process_documents():
  ├─ Calls LangChainDocumentProcessor
  │   └─ Uses PyPDFLoader to extract text
  │       → Result: 1 Document object per page (50 total)
  │       → Each has .page_content and .metadata
  │
  ├─ Calls AdvancedTextSplitter
  │   └─ Splits 50 pages into chunks
  │       → Input: 50 Document objects
  │       → Output: 250 chunks (5 per page average)
  │       → Each chunk: ~1000 chars with 200 overlap
  │
  ├─ Calls EmbeddingManager
  │   └─ Converts each chunk to vector
  │       → Downloads HuggingFace model (first time only)
  │       → Input: "Machine learning is..."
  │       → Output: [0.234, -0.567, ..., 0.123] (768 dims)
  │       → Processes all 250 chunks
  │
  └─ Calls VectorStoreManager
      └─ Stores vectors in ChromaDB
          → Creates ./data/vector_store/chroma.sqlite3
          → Indexes vectors for fast search
          → Links vectors to original text + metadata

Done! 250 chunks ready for search.

┌──────────────────────────────────────────────────────────────┐
│ STEP 2: Ask Question                                         │
└──────────────────────────────────────────────────────────────┘

User asks: "What is machine learning?"

main.py (/query/ endpoint):
  └─ Receives: {"question": "What is machine learning?"}

ai_agent.query():
  ├─ RETRIEVAL PHASE
  │   ├─ Convert question to vector
  │   │   → "What is machine learning?" 
  │   │   → [0.245, -0.523, ..., 0.134]
  │   │
  │   └─ Search vector store
  │       → Compare with all 250 chunks
  │       → Calculate cosine similarity
  │       → Return top 4 most similar:
  │           1. "Machine learning (ML) is a subset..." (score: 0.95)
  │           2. "ML algorithms learn from data..." (score: 0.89)
  │           3. "Types of ML include supervised..." (score: 0.85)
  │           4. "Applications of ML are vast..." (score: 0.82)
  │
  ├─ GENERATION PHASE
  │   ├─ Build prompt:
  │   │   Context: [4 retrieved chunks]
  │   │   Question: "What is machine learning?"
  │   │
  │   ├─ Send to OpenAI GPT-3.5
  │   │   → API call to OpenAI
  │   │   → Model reads context
  │   │   → Generates answer based on context
  │   │
  │   └─ Receive answer:
  │       "Machine learning is a subset of artificial 
  │        intelligence that enables systems to learn
  │        and improve from experience without being
  │        explicitly programmed..."
  │
  └─ Return response:
      {
        "answer": "Machine learning is...",
        "sources": [
          {"content": "...", "source": "research.pdf", "page": 1},
          {"content": "...", "source": "research.pdf", "page": 3}
        ],
        "processing_time": 1.79
      }

User receives answer!
```

---

## 🛠️ How to Modify & Extend

### **1. Add a New File Type**

**Goal:** Support `.xlsx` (Excel) files

```python
# In src/core/langchain_loader.py

from langchain_community.document_loaders import UnstructuredExcelLoader

class LangChainDocumentProcessor:
    def __init__(self):
        self.loader_mapping = {
            '.pdf': PyPDFLoader,
            '.docx': Docx2txtLoader,
            '.xlsx': UnstructuredExcelLoader,  # ← Add this!
        }
```

**Then rebuild:**
```bash
docker-compose build document-ai-agent
docker-compose up -d document-ai-agent
```

---

### **2. Change Chunk Size**

**Goal:** Use larger chunks (2000 instead of 1000)

```bash
# Edit .env
CHUNK_SIZE=2000
CHUNK_OVERLAP=400

# Restart
docker-compose down
docker-compose up -d document-ai-agent
```

**Effect:** Fewer chunks, more context per chunk, might be better for long-form content.

---

### **3. Add Custom Endpoint**

**Goal:** Add `/summarize/` endpoint

```python
# In src/api/main.py

@app.post("/summarize/")
async def summarize_document(file_id: str):
    # Get document from vector store
    docs = vector_store_manager.get_document_by_id(file_id)
    
    # Create summary prompt
    prompt = f"Summarize this document: {docs[0].page_content}"
    
    # Call LLM
    summary = ai_agent.llm.invoke(prompt)
    
    return {"summary": summary}
```

---

### **4. Switch to GPT-4**

**Goal:** Use more powerful model

```bash
# Edit .env
LLM_MODEL=gpt-4-turbo

# Restart
docker-compose down
docker-compose up -d document-ai-agent
```

**Effect:** Better answers, but more expensive ($0.01 vs $0.0005 per 1K tokens).

---

### **5. Add Conversation Memory**

**Goal:** Remember previous questions

```python
# In src/agents/simple_qa_agent.py

from langchain.memory import ConversationBufferMemory

class SimpleQAAgent:
    def __init__(self, retriever):
        self.retriever = retriever
        self.llm = self._initialize_llm()
        self.memory = ConversationBufferMemory()  # ← Add this!
        self.chain = self._create_chain()
    
    def query(self, question: str):
        # Get conversation history
        history = self.memory.load_memory_variables({})
        
        # Include history in prompt
        full_question = f"{history}\n\nCurrent question: {question}"
        
        # Get answer
        answer = self.chain.invoke(full_question)
        
        # Save to memory
        self.memory.save_context(
            {"input": question},
            {"output": answer}
        )
        
        return {"answer": answer}
```

---

### **6. Add Custom Preprocessing**

**Goal:** Clean text before embedding

```python
# In src/core/text_splitter.py

import re

class AdvancedTextSplitter:
    def preprocess_text(self, text: str) -> str:
        """Clean text before splitting"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Lowercase
        text = text.lower()
        
        return text
    
    def split_documents(self, documents):
        # Preprocess before splitting
        for doc in documents:
            doc.page_content = self.preprocess_text(doc.page_content)
        
        # Then split as normal
        return self.splitter.split_documents(documents)
```

---

## 🎓 Learning Path

### **Beginner (Week 1-2)**
1. ✅ Understand the flow diagram above
2. ✅ Read through each key file
3. ✅ Try uploading documents and querying
4. ✅ Modify `.env` settings and see effects
5. ✅ Read LangChain documentation: https://python.langchain.com/

### **Intermediate (Week 3-4)**
1. Add a new file type support
2. Modify the prompt template in `simple_qa_agent.py`
3. Change chunking strategy
4. Add logging to see what's happening
5. Experiment with different embedding models

### **Advanced (Week 5+)**
1. Implement conversation memory
2. Add document summarization
3. Create custom vector store adapter
4. Implement multi-query retrieval
5. Add re-ranking for better results
6. Build a web frontend

---

## 📖 Key Resources

### **LangChain**
- Official Docs: https://python.langchain.com/
- RAG Tutorial: https://python.langchain.com/docs/use_cases/question_answering/
- LCEL Guide: https://python.langchain.com/docs/expression_language/

### **Vector Databases**
- ChromaDB: https://docs.trychroma.com/
- FAISS: https://github.com/facebookresearch/faiss/wiki

### **Embeddings**
- HuggingFace Models: https://huggingface.co/models?pipeline_tag=sentence-similarity
- Sentence Transformers: https://www.sbert.net/

### **FastAPI**
- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

---

## 🐛 Debugging Tips

### **Enable Debug Mode**
```bash
# In .env
DEBUG=True

# Restart
docker-compose down
docker-compose up -d document-ai-agent

# View detailed logs
docker-compose logs -f document-ai-agent
```

### **Check What's in Vector Store**
```python
# Add this endpoint to main.py
@app.get("/debug/vector_count")
def get_vector_count():
    count = vector_store_manager.vector_store._collection.count()
    return {"total_chunks": count}
```

### **Test Individual Components**
```bash
# Enter container
docker exec -it document-ai-agent-langchain-document-ai-agent-1 bash

# Test embedding
python3 -c "
from src.embeddings.embedding_manager import EmbeddingManager
em = EmbeddingManager()
vec = em.get_embeddings().embed_query('test')
print(f'Vector length: {len(vec)}')
"
```

---

## 💡 Next Steps

1. **Read through this guide** completely
2. **Follow the flow diagrams** with a real example
3. **Modify one small thing** (like chunk size) and observe
4. **Read the code files** in this order:
   - `config/settings.py` (easiest)
   - `src/core/langchain_loader.py`
   - `src/core/text_splitter.py`
   - `src/embeddings/embedding_manager.py`
   - `src/vector_store/vector_store_manager.py`
   - `src/agents/simple_qa_agent.py`
   - `src/api/main.py` (most complex)
5. **Experiment!** Break things, fix them, learn

---

## ❓ Common Questions

**Q: Why do we split documents into chunks?**
A: LLMs have token limits, and smaller chunks give better search results and source attribution.

**Q: Why HuggingFace for embeddings but OpenAI for LLM?**
A: HuggingFace embeddings are free and good quality. OpenAI LLM is paid but much better at generating answers.

**Q: Can I run everything locally without API keys?**
A: Yes! Set `LLM_PROVIDER=local` and use HuggingFace models for both embeddings and LLM.

**Q: How do I see what's in my vector store?**
A: Check `./data/vector_store/chroma.sqlite3` with a SQLite browser, or add a debug endpoint.

**Q: Why is first startup so slow?**
A: HuggingFace model (500MB) is downloading. Subsequent starts are fast.

**Q: How accurate are the answers?**
A: Depends on document quality and relevance. RAG is very accurate if the answer is in your documents.

---

## 🎯 Summary

You now understand:
- ✅ How documents flow from upload to searchable vectors
- ✅ How questions are answered using RAG
- ✅ What each file and component does
- ✅ How to modify and extend the system
- ✅ Key concepts: embeddings, vector stores, LLMs, RAG

**Next:** Start experimenting! The best way to learn is by modifying the code and seeing what happens.

Happy learning! 🚀

