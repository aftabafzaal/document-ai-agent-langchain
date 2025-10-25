from langchain_community.vectorstores import Chroma, FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from typing import List, Optional
from config.settings import settings
import os

class VectorStoreManager:
    def __init__(self, embedding_model: Embeddings):
        self.embedding_model = embedding_model
        self.vector_store = None
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize or load existing vector store"""
        persist_directory = settings.PERSIST_DIRECTORY
        
        if settings.VECTOR_STORE == "chroma":
            if os.path.exists(persist_directory) and os.listdir(persist_directory):
                self.vector_store = Chroma(
                    persist_directory=persist_directory,
                    embedding_function=self.embedding_model
                )
                print("Loaded existing Chroma vector store")
            else:
                self.vector_store = Chroma(
                    persist_directory=persist_directory,
                    embedding_function=self.embedding_model
                )
                print("Created new Chroma vector store")
        
        elif settings.VECTOR_STORE == "faiss":
            faiss_path = os.path.join(persist_directory, "faiss_index")
            if os.path.exists(faiss_path):
                self.vector_store = FAISS.load_local(
                    faiss_path,
                    self.embedding_model,
                    allow_dangerous_deserialization=True
                )
                print("Loaded existing FAISS vector store")
            else:
                self.vector_store = None
                print("FAISS vector store will be created when documents are added")
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to vector store"""
        if not documents:
            print("No documents to add")
            return
        
        if settings.VECTOR_STORE == "chroma":
            self.vector_store.add_documents(documents)
            print(f"Added {len(documents)} documents to Chroma vector store")
        
        elif settings.VECTOR_STORE == "faiss":
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(
                    documents, 
                    self.embedding_model
                )
            else:
                self.vector_store.add_documents(documents)
            
            faiss_path = os.path.join(settings.PERSIST_DIRECTORY, "faiss_index")
            self.vector_store.save_local(faiss_path)
            print(f"Added {len(documents)} documents to FAISS vector store")
    
    def similarity_search(self, query: str, k: int = 4, **kwargs) -> List[Document]:
        """Perform similarity search"""
        if self.vector_store is None:
            return []
        
        return self.vector_store.similarity_search(query, k=k, **kwargs)
    
    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        """Perform similarity search with scores"""
        if self.vector_store is None:
            return []
        
        return self.vector_store.similarity_search_with_score(query, k=k)
    
    def as_retriever(self, **kwargs):
        """Get vector store as retriever"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        
        return self.vector_store.as_retriever(**kwargs)