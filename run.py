#!/usr/bin/env python3
"""
Main entry point for the Document AI Agent with LangChain
"""

import uvicorn
import os
from dotenv import load_dotenv

def main():
    """Main application entry point"""
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            print(f"Warning: {var} is not set in environment variables")
    
    # Start the FastAPI server
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("DEBUG") == "True" else False,
        log_level="info"
    )

if __name__ == "__main__":
    main()