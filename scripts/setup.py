#!/usr/bin/env python3
"""
Setup script for Document AI Agent
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🔧 Setting up Document AI Agent with LangChain...")
    
    # Create necessary directories
    directories = [
        "data/uploads",
        "data/vector_store",
        "data/cache",
        "models",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        sys.exit(1)
    
    # Check if .env exists, if not create from example
    if not Path(".env").exists():
        if Path(".env.example").exists():
            run_command("cp .env.example .env", "Creating .env file from example")
            print("📝 Please edit .env file with your API keys")
        else:
            print("⚠️  No .env.example file found")
    
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python run.py (for backend)")
    print("3. Run: streamlit run frontend/app.py (for frontend)")

if __name__ == "__main__":
    main()