from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import shutil
import os
from pathlib import Path
import time
import json
from datetime import datetime

from config.settings import settings
from src.core.langchain_loader import LangChainDocumentProcessor
from src.core.text_splitter import AdvancedTextSplitter
from src.embeddings.embedding_manager import EmbeddingManager
from src.vector_store.vector_store_manager import VectorStoreManager
from src.agents.simple_qa_agent import SimpleQAAgent
from src.utils.file_cleanup import FileCleanupManager

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
embedding_manager = EmbeddingManager()
vector_store_manager = VectorStoreManager(embedding_manager.get_embeddings())
retriever = vector_store_manager.as_retriever(search_kwargs={"k": 4})
ai_agent = SimpleQAAgent(retriever)
cleanup_manager = FileCleanupManager(retention_days=30)  # Keep files for 30 days

class QueryRequest(BaseModel):
    question: str
    use_conversation: bool = False

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    processing_time: float

class SyncResponse(BaseModel):
    status: str
    total_files_in_folder: int
    new_files_processed: int
    already_processed: int
    failed: int
    processed_files: List[str]
    failed_files: List[Dict[str, str]]
    processing_time: float

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...), background_tasks: BackgroundTasks = None):
    """Upload and process files"""
    upload_dir = Path(settings.UPLOAD_DIRECTORY)
    upload_dir.mkdir(exist_ok=True)
    
    saved_files = []
    
    for file in files:
        file_path = upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        saved_files.append(str(file_path))
    
    if background_tasks:
        background_tasks.add_task(process_documents, saved_files)
    
    return {"message": "Files uploaded and processing started", "files": saved_files}

@app.post("/query/", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the document knowledge base"""
    if ai_agent is None:
        raise HTTPException(status_code=503, detail="AI Agent not initialized. Agent imports need to be fixed.")
    
    start_time = time.time()
    
    result = ai_agent.query(request.question, request.use_conversation)
    
    sources = []
    for doc in result.get("source_documents", []):
        sources.append({
            "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
            "source": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page", None)
        })
    
    processing_time = time.time() - start_time
    
    return QueryResponse(
        answer=result["answer"],
        sources=sources,
        processing_time=processing_time
    )

@app.post("/clear_memory/")
async def clear_memory():
    """Clear conversation memory"""
    if ai_agent is None:
        raise HTTPException(status_code=503, detail="AI Agent not initialized")
    ai_agent.clear_memory()
    return {"message": "Conversation memory cleared"}

@app.post("/sync/", response_model=SyncResponse)
async def sync_upload_folder(background_tasks: BackgroundTasks = None):
    """
    Sync upload folder with vector store.
    Processes any new files added via FTP, copy-paste, or other methods.
    """
    start_time = time.time()
    
    upload_dir = Path(settings.UPLOAD_DIRECTORY)
    tracking_file = Path(settings.UPLOAD_DIRECTORY) / ".processed_files.json"
    
    # Create upload directory if it doesn't exist
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Load tracking data
    processed_tracking = load_processed_files_tracking(tracking_file)
    
    # Scan upload directory for all supported files
    supported_extensions = ['.pdf', '.txt', '.docx', '.doc', '.md', '.csv', '.json']
    all_files = []
    for ext in supported_extensions:
        all_files.extend(upload_dir.glob(f"*{ext}"))
    
    # Filter out the tracking file
    all_files = [f for f in all_files if f.name != ".processed_files.json"]
    
    new_files = []
    already_processed_files = []
    failed_files = []
    
    # Identify new files
    for file_path in all_files:
        file_info = get_file_info(file_path)
        if not is_file_processed(file_path, file_info, processed_tracking):
            new_files.append(file_path)
        else:
            already_processed_files.append(file_path)
    
    processed_files = []
    
    # Process new files
    if new_files:
        try:
            # Process documents
            processor = LangChainDocumentProcessor()
            splitter = AdvancedTextSplitter()
            
            for file_path in new_files:
                try:
                    # Load single file
                    documents = processor._load_single_file(file_path)
                    
                    if documents:
                        # Split documents
                        split_documents = splitter.split_documents_by_type(documents)
                        
                        # Add to vector store
                        vector_store_manager.add_documents(split_documents)
                        
                        # Track processed file
                        file_info = get_file_info(file_path)
                        processed_tracking[str(file_path)] = file_info
                        processed_files.append(str(file_path.name))
                    else:
                        failed_files.append({
                            "file": str(file_path.name),
                            "error": "No documents extracted"
                        })
                except Exception as e:
                    failed_files.append({
                        "file": str(file_path.name),
                        "error": str(e)
                    })
            
            # Save tracking data
            save_processed_files_tracking(tracking_file, processed_tracking)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")
    
    processing_time = time.time() - start_time
    
    return SyncResponse(
        status="success",
        total_files_in_folder=len(all_files),
        new_files_processed=len(processed_files),
        already_processed=len(already_processed_files),
        failed=len(failed_files),
        processed_files=processed_files,
        failed_files=failed_files,
        processing_time=processing_time
    )

@app.get("/sync/status")
async def get_sync_status():
    """
    Get current sync status - shows which files are processed and which are pending
    """
    upload_dir = Path(settings.UPLOAD_DIRECTORY)
    tracking_file = Path(settings.UPLOAD_DIRECTORY) / ".processed_files.json"
    
    # Load tracking data
    processed_tracking = load_processed_files_tracking(tracking_file)
    
    # Scan upload directory
    supported_extensions = ['.pdf', '.txt', '.docx', '.doc', '.md', '.csv', '.json']
    all_files = []
    for ext in supported_extensions:
        all_files.extend(upload_dir.glob(f"*{ext}"))
    
    all_files = [f for f in all_files if f.name != ".processed_files.json"]
    
    processed = []
    pending = []
    
    for file_path in all_files:
        file_info = get_file_info(file_path)
        if is_file_processed(file_path, file_info, processed_tracking):
            processed.append({
                "filename": file_path.name,
                "size": file_info["size"],
                "modified": file_info["modified"],
                "processed_at": processed_tracking.get(str(file_path), {}).get("processed_at", "Unknown")
            })
        else:
            pending.append({
                "filename": file_path.name,
                "size": file_info["size"],
                "modified": file_info["modified"]
            })
    
    return {
        "total_files": len(all_files),
        "processed_count": len(processed),
        "pending_count": len(pending),
        "processed_files": processed,
        "pending_files": pending
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "docs": "/docs"
    }

def process_documents(file_paths: List[str]):
    """Process documents and add to vector store"""
    processor = LangChainDocumentProcessor()
    splitter = AdvancedTextSplitter()
    tracking_file = Path(settings.UPLOAD_DIRECTORY) / ".processed_files.json"
    
    temp_dir = Path("./data/temp_processing")
    temp_dir.mkdir(exist_ok=True)
    
    for file_path in file_paths:
        temp_path = temp_dir / Path(file_path).name
        shutil.copy2(file_path, temp_path)
    
    documents = processor.load_documents_from_folder(str(temp_dir))
    split_documents = splitter.split_documents_by_type(documents)
    
    vector_store_manager.add_documents(split_documents)
    
    # Track processed files
    processed_tracking = load_processed_files_tracking(tracking_file)
    for file_path in file_paths:
        file_info = get_file_info(Path(file_path))
        processed_tracking[file_path] = file_info
    save_processed_files_tracking(tracking_file, processed_tracking)
    
    for temp_file in temp_dir.glob("*"):
        temp_file.unlink()
    temp_dir.rmdir()

# Helper functions for file tracking
def load_processed_files_tracking(tracking_file: Path) -> Dict:
    """Load the tracking data of processed files"""
    if tracking_file.exists():
        try:
            with open(tracking_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_processed_files_tracking(tracking_file: Path, tracking_data: Dict):
    """Save the tracking data of processed files"""
    try:
        with open(tracking_file, 'w') as f:
            json.dump(tracking_data, f, indent=2)
    except Exception as e:
        print(f"Error saving tracking data: {e}")

def get_file_info(file_path: Path) -> Dict:
    """Get file metadata"""
    stat = file_path.stat()
    return {
        "size": stat.st_size,
        "modified": stat.st_mtime,
        "processed_at": datetime.now().isoformat()
    }

def is_file_processed(file_path: Path, current_info: Dict, tracking_data: Dict) -> bool:
    """Check if a file has been processed based on size and modification time"""
    file_key = str(file_path)
    if file_key not in tracking_data:
        return False
    
    tracked_info = tracking_data[file_key]
    
    # Check if file has been modified since last processing
    return (tracked_info.get("size") == current_info["size"] and 
            tracked_info.get("modified") == current_info["modified"])