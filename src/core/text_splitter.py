from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
    MarkdownTextSplitter
)
from langchain_core.documents import Document
from typing import List, Callable
from pathlib import Path
from config.settings import settings

class AdvancedTextSplitter:
    def __init__(self):
        self.splitter_mapping = {
            'recursive': RecursiveCharacterTextSplitter,
            'character': CharacterTextSplitter,
            'token': TokenTextSplitter,
            'markdown': MarkdownTextSplitter,
        }
        
        self.default_splitter = self._create_default_splitter()
    
    def _create_default_splitter(self) -> RecursiveCharacterTextSplitter:
        """Create the default text splitter"""
        return RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
    
    def split_documents(self, documents: List[Document], 
                       splitter_type: str = 'recursive',
                       **kwargs) -> List[Document]:
        """Split documents into chunks"""
        if splitter_type == 'recursive':
            splitter = self.default_splitter
        else:
            splitter_class = self.splitter_mapping.get(splitter_type)
            if not splitter_class:
                raise ValueError(f"Unknown splitter type: {splitter_type}")
            splitter = splitter_class(**kwargs)
        
        return splitter.split_documents(documents)
    
    def split_documents_by_type(self, documents: List[Document]) -> List[Document]:
        """Intelligently split documents based on their type"""
        split_docs = []
        
        for doc in documents:
            source = doc.metadata.get('source', '')
            file_extension = Path(source).suffix.lower()
            
            if file_extension == '.md':
                # Use markdown-specific splitting
                markdown_splitter = MarkdownTextSplitter(
                    chunk_size=settings.CHUNK_SIZE,
                    chunk_overlap=settings.CHUNK_OVERLAP
                )
                split_docs.extend(markdown_splitter.split_documents([doc]))
            else:
                # Use default recursive splitting
                split_docs.extend(self.default_splitter.split_documents([doc]))
        
        return split_docs