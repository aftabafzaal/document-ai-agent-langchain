"""
Simplified QA Agent that works with LangChain 1.0+
"""

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any, List, Optional
from config.settings import settings, LLMProvider


class SimpleQAAgent:
    """Simplified QA Agent using LangChain 1.0+ LCEL syntax"""
    
    def __init__(self, retriever: BaseRetriever):
        self.retriever = retriever
        self.llm = self._initialize_llm()
        self.chain = self._create_chain()
    
    def _initialize_llm(self):
        """Initialize LLM based on configuration"""
        provider = settings.LLM_PROVIDER
        
        if provider == LLMProvider.OPENAI:
            if not settings.OPENAI_API_KEY:
                raise ValueError("OpenAI API key required")
            return ChatOpenAI(
                model=settings.LLM_MODEL,
                temperature=0.7,
                api_key=settings.OPENAI_API_KEY
            )
        
        elif provider == LLMProvider.ANTHROPIC:
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("Anthropic API key required")
            return ChatAnthropic(
                model=settings.LLM_MODEL,
                temperature=0.7,
                api_key=settings.ANTHROPIC_API_KEY
            )
        
        elif provider == LLMProvider.LOCAL:
            return HuggingFaceHub(
                repo_id=settings.LLM_MODEL,
                model_kwargs={"temperature": 0.7, "max_length": 512}
            )
    
    def _create_chain(self):
        """Create LCEL chain for QA"""
        prompt = PromptTemplate.from_template(
            """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Question: {question}

Answer:"""
        )
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain
    
    def query(self, question: str, use_conversation: bool = False) -> Dict[str, Any]:
        """Query the document knowledge base"""
        # Get relevant documents
        docs = self.retriever.invoke(question)
        
        # Get answer from LLM
        answer = self.chain.invoke(question)
        
        return {
            "answer": answer,
            "source_documents": docs,
        }
    
    def clear_memory(self):
        """Clear conversation memory (placeholder for compatibility)"""
        pass  # Stateless for now

