# Docker Fixes Applied

## Issues Fixed

### 1. ✅ Missing `.env` File
**Problem:** Docker Compose requires a `.env` file for environment variables.  
**Solution:** Created `.env` file with default configuration.

### 2. ✅ Missing Python Import
**Problem:** `text_splitter.py` was missing `Path` import causing runtime errors.  
**Solution:** Added `from pathlib import Path` to imports.

### 3. ✅ Health Check Endpoint
**Problem:** Health check was pointing to `/docs` which might fail if docs aren't available.  
**Solution:** Changed health check to use `/health` endpoint in both Dockerfile and docker-compose.yml.

### 4. ✅ Missing Dependencies
**Problem:** Missing LangChain provider packages in requirements.txt.  
**Solution:** Added:
- `langchain-huggingface>=0.0.1`
- `langchain-openai>=0.0.1`
- `langchain-anthropic>=0.0.1`

### 5. ✅ Missing `__init__.py` Files
**Problem:** Python packages missing `__init__.py` files causing import errors.  
**Solution:** Created:
- `config/__init__.py`
- `src/api/__init__.py`

## How to Run

### Option 1: Using the Shell Script (Recommended)
```bash
./docker-run.sh
```

### Option 2: Manual Docker Compose
```bash
# Build the containers
docker-compose build

# Start the containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### Option 3: Docker Only (No Compose)
```bash
# Build the image
docker build -t document-ai-agent .

# Run the container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  --name doc-ai-agent \
  document-ai-agent

# View logs
docker logs -f doc-ai-agent

# Stop container
docker stop doc-ai-agent
docker rm doc-ai-agent
```

## Configuration

### Required Environment Variables

Edit `.env` file and set your API keys:

```bash
# Required for OpenAI LLM
OPENAI_API_KEY=your-actual-openai-api-key

# Optional: Only if using Anthropic
ANTHROPIC_API_KEY=your-anthropic-key

# Optional: Only if using HuggingFace Hub models
HUGGINGFACEHUB_API_TOKEN=your-huggingface-token
```

### Default Settings

- **Embedding Provider:** HuggingFace (runs locally, no API key needed)
- **LLM Provider:** OpenAI (requires API key)
- **Vector Store:** ChromaDB
- **Port:** 8000

## Accessing the Application

Once running:

- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **API Root:** http://localhost:8000/

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs document-ai-agent

# Or for standalone docker
docker logs doc-ai-agent
```

### Health check failing
```bash
# Test health endpoint directly
curl http://localhost:8000/health
```

### Permission issues with volumes
```bash
# Fix data directory permissions
chmod -R 755 data
```

### Out of memory
```bash
# Add memory limits to docker-compose.yml
services:
  document-ai-agent:
    deploy:
      resources:
        limits:
          memory: 4G
```

## Next Steps

1. **Upload Documents:**
   ```bash
   curl -X POST "http://localhost:8000/upload/" \
     -F "files=@your-document.pdf"
   ```

2. **Query Documents:**
   ```bash
   curl -X POST "http://localhost:8000/query/" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is this document about?"}'
   ```

3. **Check Health:**
   ```bash
   curl http://localhost:8000/health
   ```

## Architecture

```
┌─────────────────────────────────────┐
│  Docker Container (Port 8000)       │
│                                     │
│  ┌──────────────────────────────┐  │
│  │     FastAPI Application       │  │
│  │  - Document Upload            │  │
│  │  - Query Processing           │  │
│  │  - Vector Search              │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │     LangChain Components      │  │
│  │  - Document Loaders           │  │
│  │  - Text Splitters             │  │
│  │  - Embeddings                 │  │
│  │  - Vector Store (ChromaDB)    │  │
│  │  - AI Agent                   │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │     Persistent Volumes        │  │
│  │  - ./data → /app/data         │  │
│  │  - ./models → /app/models     │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

## Support

If you encounter any issues:
1. Check the logs: `docker-compose logs -f`
2. Verify `.env` configuration
3. Ensure you have enough memory (4GB+ recommended)
4. Check that ports 8000 is not already in use

