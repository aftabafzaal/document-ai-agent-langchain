from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.chains.llm import LLMChain
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.retrievers import BaseRetriever
from typing import Dict, Any, List, Optional
from config.settings import settings, LLMProvider

class LangChainAIAgent:
    def __init__(self, retriever: BaseRetriever):
        self.retriever = retriever
        self.llm = self._initialize_llm()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.qa_chain = self._create_qa_chain()
        self.conversational_chain = self._create_conversational_chain()
    
    def _initialize_llm(self):
        """Initialize LLM based on configuration"""
        provider = settings.LLM_PROVIDER
        
        if provider == LLMProvider.OPENAI:
            if not settings.OPENAI_API_KEY:
                raise ValueError("OpenAI API key required")
            return ChatOpenAI(
                model=settings.LLM_MODEL,
                temperature=0.1,
                openai_api_key=settings.OPENAI_API_KEY
            )
        
        elif provider == LLMProvider.ANTHROPIC:
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("Anthropic API key required")
            return ChatAnthropic(
                model=settings.LLM_MODEL,
                temperature=0.1,
                anthropic_api_key=settings.ANTHROPIC_API_KEY
            )
        
        elif provider == LLMProvider.LOCAL:
            return HuggingFaceHub(
                repo_id=settings.LLM_MODEL,
                model_kwargs={"temperature": 0.1, "max_length": 512}
            )
    
    def _create_qa_chain(self):
        """Create retrieval QA chain"""
        prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context: {context}

        Question: {question}
        
        Answer: """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
    
    def _create_conversational_chain(self):
        """Create conversational retrieval chain"""
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
            verbose=True
        )
    
    def query(self, question: str, use_conversation: bool = False) -> Dict[str, Any]:
        """Query the document knowledge base"""
        if use_conversation:
            result = self.conversational_chain({"question": question})
        else:
            result = self.qa_chain({"query": question})
        
        return {
            "answer": result.get("result", ""),
            "source_documents": result.get("source_documents", []),
            "chat_history": self.memory.chat_memory.messages if use_conversation else []
        }
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()