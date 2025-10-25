import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
    CSVLoader,
    JSONLoader
)
from langchain_core.documents import Document
from loguru import logger
from config.settings import settings

class LangChainDocumentProcessor:
    def __init__(self):
        self.loader_mapping = {
            '.pdf': PyPDFLoader,
            '.txt': TextLoader,
            '.docx': Docx2txtLoader,
            '.doc': Docx2txtLoader,
            '.md': UnstructuredMarkdownLoader,
            '.csv': CSVLoader,
            '.json': JSONLoader,
        }
        
        self.processed_files = set()
    
    def load_documents_from_folder(self, folder_path: str) -> List[Document]:
        """Load all documents from folder using LangChain loaders"""
        documents = []
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            raise ValueError(f"Folder {folder_path} does not exist")
        
        for file_path in folder_path.rglob('*'):
            if self._should_process_file(file_path):
                try:
                    file_docs = self._load_single_file(file_path)
                    documents.extend(file_docs)
                    self.processed_files.add(str(file_path))
                    logger.info(f"Loaded {len(file_docs)} documents from {file_path}")
                except Exception as e:
                    logger.error(f"Error loading {file_path}: {e}")
        
        return documents
    
    def _load_single_file(self, file_path: Path) -> List[Document]:
        """Load a single file using appropriate LangChain loader"""
        file_extension = file_path.suffix.lower()
        
        if file_extension not in self.loader_mapping:
            logger.warning(f"Unsupported file type: {file_extension}")
            return []
        
        loader_class = self.loader_mapping[file_extension]
        
        # Configure specific loaders
        if file_extension == '.json':
            loader = loader_class(
                str(file_path),
                jq_schema='.',
                text_content=False
            )
        elif file_extension == '.csv':
            loader = loader_class(str(file_path))
        else:
            loader = loader_class(str(file_path))
        
        return loader.load()
    
    def _should_process_file(self, file_path: Path) -> bool:
        """Check if file should be processed"""
        return (file_path.is_file() and 
                file_path.suffix.lower() in self.loader_mapping and
                str(file_path) not in self.processed_files)
