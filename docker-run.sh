#!/bin/bash

# Docker run script for Document AI Agent

echo "🚀 Starting Document AI Agent with Docker..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your configuration."
    echo "You can use .env.example as a template."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data/vector_store data/uploads data/cache models logs

# Build and run with docker-compose
echo "🔨 Building Docker containers..."
docker-compose build

echo "▶️  Starting containers..."
docker-compose up -d

echo ""
echo "✅ Document AI Agent is starting up!"
echo ""
echo "📊 API Documentation: http://localhost:8000/docs"
echo "🏥 Health Check: http://localhost:8000/health"
echo "🎨 Frontend (if available): http://localhost:8501"
echo ""
echo "📝 View logs with: docker-compose logs -f"
echo "🛑 Stop with: docker-compose down"
echo ""

