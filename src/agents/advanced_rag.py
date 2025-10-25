from langchain.retrievers import (
    ContextualCompressionRetriever,
    EnsembleRetriever,
    BM25Retriever
)
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.ensemble import FusionAlgorithm

class AdvancedRAGSystem:
    def __init__(self, vector_store_manager: VectorStoreManager, llm):
        self.vector_store_manager = vector_store_manager
        self.llm = llm
        self.compression_retriever = self._create_compression_retriever()
        self.ensemble_retriever = self._create_ensemble_retriever()
    
    def _create_compression_retriever(self):
        """Create retriever with content compression"""
        compressor = LLMChainExtractor.from_llm(self.llm)
        base_retriever = self.vector_store_manager.as_retriever()
        return ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )
    
    def _create_ensemble_retriever(self):
        """Create ensemble retriever combining multiple methods"""
        vector_retriever = self.vector_store_manager.as_retriever()
        
        return EnsembleRetriever(
            retrievers=[vector_retriever],
            weights=[1.0]
        )