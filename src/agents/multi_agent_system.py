from langchain.agents import initialize_agent, Tool, AgentType
from langchain.tools import BaseTool
from typing import List, Dict, Any

class DocumentAIAgentSystem:
    def __init__(self, langchain_agent: LangChainAIAgent, vector_store_manager: VectorStoreManager):
        self.langchain_agent = langchain_agent
        self.vector_store_manager = vector_store_manager
        self.tools = self._create_tools()
        self.agent = self._create_agent()
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the agent"""
        tools = [
            Tool(
                name="DocumentSearch",
                func=self.vector_store_manager.similarity_search,
                description="Search for relevant documents based on a query"
            ),
            Tool(
                name="QA",
                func=self.langchain_agent.query,
                description="Answer questions based on document content"
            ),
            Tool(
                name="DocumentSummary",
                func=self._summarize_documents,
                description="Summarize document content"
            )
        ]
        return tools
    
    def _create_agent(self):
        """Create the agent with tools"""
        return initialize_agent(
            tools=self.tools,
            llm=self.langchain_agent.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def _summarize_documents(self, query: str) -> str:
        """Summarize relevant documents"""
        docs = self.vector_store_manager.similarity_search(query, k=3)
        content = "\n\n".join([doc.page_content for doc in docs])
        
        summary_prompt = f"""
        Summarize the following document content related to: {query}
        
        Documents:
        {content}
        
        Summary:
        """
        
        return self.langchain_agent.llm.predict(summary_prompt)
    
    def run(self, input_text: str) -> Dict[str, Any]:
        """Run the agent with given input"""
        try:
            result = self.agent.run(input_text)
            return {
                "success": True,
                "result": result,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e)
            }