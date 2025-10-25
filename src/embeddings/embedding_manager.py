from langchain_community.embeddings import (
    OpenAIEmbeddings,
    HuggingFaceEmbeddings,
    HuggingFaceInstructEmbeddings
)
from typing import Optional
from config.settings import settings, EmbeddingProvider
import os

class EmbeddingManager:
    def __init__(self):
        self.embedding_model = None
        self.cache = None
        self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """Initialize embedding model based on configuration"""
        provider = settings.EMBEDDING_PROVIDER
        
        if provider == EmbeddingProvider.OPENAI:
            if not settings.OPENAI_API_KEY:
                raise ValueError("OpenAI API key required for OpenAI embeddings")
            self.embedding_model = OpenAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
                openai_api_key=settings.OPENAI_API_KEY
            )
        
        elif provider == EmbeddingProvider.HUGGINGFACE:
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        
        elif provider == EmbeddingProvider.LOCAL:
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                cache_folder="./models"
            )
    
    def get_embeddings(self):
        """Get the embedding model"""
        return self.embedding_model