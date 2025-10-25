import streamlit as st
import requests
import os
from typing import List, Dict

st.set_page_config(
    page_title="Document AI Agent with LangChain",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processing" not in st.session_state:
    st.session_state.processing = False

def main():
    st.title("🧠 Document AI Agent with LangChain")
    st.markdown("Upload documents and have intelligent conversations with your data!")
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Document Management")
        
        uploaded_files = st.file_uploader(
            "Choose documents",
            type=['pdf', 'txt', 'docx', 'md', 'csv', 'json'],
            accept_multiple_files=True,
            help="Upload multiple documents to build your knowledge base"
        )
        
        if uploaded_files and st.button("Process Documents", type="primary"):
            process_uploaded_files(uploaded_files)
        
        st.divider()
        
        # Document statistics
        st.header("📊 Statistics")
        if st.button("Refresh Stats"):
            display_statistics()
        
        st.divider()
        
        # Memory management
        st.header("💬 Conversation")
        if st.button("Clear Conversation History"):
            clear_conversation_history()
            st.success("Conversation history cleared!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat with Your Documents")
        
        # Chat interface
        user_question = st.text_area(
            "Ask a question about your documents:",
            placeholder="What would you like to know about your documents?",
            height=100
        )
        
        col1_1, col1_2 = st.columns([1, 1])
        
        with col1_1:
            use_conversation = st.checkbox("Use conversation context", value=True)
        
        with col1_2:
            if st.button("Get Answer", type="primary", use_container_width=True):
                if user_question:
                    get_answer(user_question, use_conversation)
                else:
                    st.warning("Please enter a question")
        
        # Display chat history
        display_chat_history()
    
    with col2:
        st.header("🔍 Source Documents")
        display_source_documents()

def process_uploaded_files(uploaded_files):
    """Process uploaded files"""
    st.session_state.processing = True
    
    with st.spinner("Processing documents..."):
        files = []
        for uploaded_file in uploaded_files:
            files.append(("files", (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)))
        
        try:
            response = requests.post(
                "http://localhost:8000/upload/",
                files=files
            )
            
            if response.status_code == 200:
                st.success(f"Successfully processed {len(uploaded_files)} documents!")
            else:
                st.error("Error processing documents")
        except Exception as e:
            st.error(f"Error connecting to server: {e}")
    
    st.session_state.processing = False

def get_answer(question: str, use_conversation: bool):
    """Get answer from AI agent"""
    with st.spinner("Searching documents..."):
        try:
            response = requests.post(
                "http://localhost:8000/query/",
                json={
                    "question": question,
                    "use_conversation": use_conversation
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": result["answer"],
                    "sources": result["sources"],
                    "processing_time": result["processing_time"]
                })
                
                # Display sources in session state for the sidebar
                st.session_state.last_sources = result["sources"]
                
            else:
                st.error("Error getting answer from server")
        
        except Exception as e:
            st.error(f"Error connecting to server: {e}")

def display_chat_history():
    """Display chat history"""
    for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
        with st.expander(f"Q: {chat['question'][:50]}...", expanded=i==0):
            st.write(f"**Answer:** {chat['answer']}")
            st.caption(f"Processing time: {chat['processing_time']:.2f}s")

def display_source_documents():
    """Display source documents in sidebar"""
    if hasattr(st.session_state, 'last_sources'):
        sources = st.session_state.last_sources
        for i, source in enumerate(sources):
            with st.expander(f"Source {i+1}: {source['source']}", expanded=True):
                st.write(source['content'])
                if source.get('page'):
                    st.caption(f"Page: {source['page']}")

def display_statistics():
    """Display document statistics"""
    st.info("Statistics feature coming soon!")

def clear_conversation_history():
    """Clear conversation history"""
    st.session_state.chat_history = []
    try:
        response = requests.post("http://localhost:8000/clear_memory/")
        if response.status_code == 200:
            st.success("Conversation memory cleared!")
    except:
        st.warning("Could not clear server memory")

if __name__ == "__main__":
    main()