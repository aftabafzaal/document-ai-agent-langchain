from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from enum import Enum

class EmbeddingProvider(str, Enum):
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    LOCAL = "local"

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Document AI Agent with LangChain"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # LangChain Settings
    EMBEDDING_PROVIDER: EmbeddingProvider = EmbeddingProvider.HUGGINGFACE
    LLM_PROVIDER: LLMProvider = LLMProvider.OPENAI
    
    # API Keys (use environment variables)
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    HUGGINGFACEHUB_API_TOKEN: Optional[str] = None
    
    # Model Settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"
    LLM_MODEL: str = "gpt-3.5-turbo"
    
    # Vector Store
    VECTOR_STORE: str = "chroma"
    PERSIST_DIRECTORY: str = "./data/vector_store"
    
    # Text Splitting
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # File Processing
    UPLOAD_DIRECTORY: str = "./data/uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # Ignore extra environment variables
    )

settings = Settings()