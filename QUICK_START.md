# Quick Start Guide - Document AI Agent

## ✅ All Docker Fixes Applied!

The Docker configuration has been fixed and the image built successfully. Here's how to run it:

## 📋 Prerequisites

### 1. Start Docker/OrbStack

Your Docker daemon (OrbStack) needs to be running:

**Option A: Using Application**
- Open **OrbStack** from your Applications folder
- Wait for it to fully start (check menu bar icon)

**Option B: Using Terminal**
```bash
# Start OrbStack
open -a OrbStack

# Wait a few seconds, then verify it's running
docker ps
```

### 2. Configure API Key

Edit `.env` file and add your OpenAI API key:
```bash
nano .env
# Or use any text editor
```

Change this line:
```
OPENAI_API_KEY=your-openai-api-key-here
```

To your actual key:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

## 🚀 Running the Application

### Method 1: Simple Docker Run (Recommended for Testing)

```bash
# Remove any existing container
docker rm -f doc-ai-agent 2>/dev/null || true

# Run the container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  --name doc-ai-agent \
  document-ai-agent:latest

# Check if it's running
docker ps

# View logs
docker logs -f doc-ai-agent
```

### Method 2: Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Method 3: Using the Shell Script

```bash
chmod +x docker-run.sh
./docker-run.sh
```

## 📊 Access the Application

Once running, access:

- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **API Root:** http://localhost:8000/

## 🧪 Test the API

### 1. Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","timestamp":1234567890.0}
```

### 2. Upload a Document
```bash
curl -X POST "http://localhost:8000/upload/" \
  -F "files=@/path/to/your/document.pdf"
```

### 3. Query Documents
```bash
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this document about?",
    "use_conversation": false
  }'
```

## 🐛 Troubleshooting

### Docker Daemon Not Running
```bash
# Check if OrbStack is running
docker ps

# If not, start OrbStack
open -a OrbStack

# Wait 10-20 seconds and try again
```

### Port Already in Use
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process (if needed)
kill -9 <PID>

# Or use a different port
docker run -d -p 8080:8000 ... document-ai-agent:latest
# Then access at http://localhost:8080
```

### Container Crashes Immediately
```bash
# Check logs
docker logs doc-ai-agent

# Common issues:
# 1. Missing OPENAI_API_KEY in .env
# 2. Invalid API key
# 3. Missing dependencies (rebuild image)
```

### Rebuild Image (If Needed)
```bash
# If you made code changes
docker build -t document-ai-agent:latest .

# Or force rebuild without cache
docker build --no-cache -t document-ai-agent:latest .
```

## 📁 Project Structure

```
.
├── data/                      # Persistent data (mounted as volume)
│   ├── uploads/              # Uploaded documents
│   ├── vector_store/         # ChromaDB data
│   └── cache/                # Embeddings cache
├── src/
│   ├── api/
│   │   └── main.py           # FastAPI application
│   ├── core/
│   │   ├── langchain_loader.py
│   │   └── text_splitter.py
│   ├── embeddings/
│   ├── vector_store/
│   └── agents/
├── config/
│   └── settings.py           # Configuration
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env                      # Environment variables (add your API keys here)
```

## 🔧 Useful Commands

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# Stop container
docker stop doc-ai-agent

# Remove container
docker rm doc-ai-agent

# View logs (follow mode)
docker logs -f doc-ai-agent

# Execute command inside container
docker exec -it doc-ai-agent bash

# View container resource usage
docker stats doc-ai-agent

# Restart container
docker restart doc-ai-agent
```

## 🎯 Next Steps

1. **Start OrbStack** (if not running)
2. **Configure `.env`** with your OpenAI API key
3. **Run the container** using one of the methods above
4. **Test the API** with the examples
5. **Upload documents** and start querying!

## 💡 Tips

- The first run will download the HuggingFace embedding model (~500MB)
- Document processing happens in the background after upload
- Use the `/docs` endpoint to explore all available API endpoints
- Check logs if something doesn't work: `docker logs doc-ai-agent`

## 🆘 Still Having Issues?

1. Check that OrbStack is running: `docker ps`
2. Verify the image exists: `docker images | grep document-ai-agent`
3. Check the logs: `docker logs doc-ai-agent`
4. Ensure `.env` file is properly formatted (no trailing spaces)
5. Verify port 8000 is not in use: `lsof -i :8000`

## ✅ Success Indicators

When everything is working, you should see:

```bash
$ docker ps
CONTAINER ID   IMAGE                          STATUS         PORTS
abc123def456   document-ai-agent:latest      Up 2 minutes   0.0.0.0:8000->8000/tcp

$ curl http://localhost:8000/health
{"status":"healthy","timestamp":1234567890.0}
```

Now you're ready to use your Document AI Agent! 🎉

