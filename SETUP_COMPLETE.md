# ✅ Docker Setup Complete!

Your Document AI Agent is successfully running in Docker!

## 🎯 What's Working

- ✅ Docker container running on port 8000
- ✅ HuggingFace embeddings (local, no API key needed)
- ✅ Vector store (ChromaDB) initialized
- ✅ Document upload endpoint ready
- ✅ Health check endpoint working

## 🔧 What You Need To Do

### 1. Add Your OpenAI API Key

Edit `.env` and replace the placeholder:
```bash
# Open the file
nano .env

# Change this line:
OPENAI_API_KEY=your-openai-api-key-here

# To your actual key:
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

Get your API key from: https://platform.openai.com/api-keys

### 2. Restart the Container

After adding your API key:
```bash
docker-compose restart document-ai-agent

# Wait 30-45 seconds for model initialization
sleep 45

# Test
curl http://localhost:8000/health
```

## 📊 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Root Info
```bash
curl http://localhost:8000/
```

### Upload Documents
```bash
curl -X POST http://localhost:8000/upload/ \
  -F "files=@your-document.pdf"
```

### Query (After uploading documents)
```bash
curl -X POST http://localhost:8000/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

### Clear Memory
```bash
curl -X POST http://localhost:8000/clear_memory/
```

## 🌐 Web Interface

- **API Documentation:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## 📁 Persistent Data

Your data is stored in:
- `./data/vector_store` - Vector embeddings
- `./data/uploads` - Uploaded documents  
- `./data/cache` - Model cache

## 🚀 Common Commands

```bash
# View logs
docker-compose logs -f document-ai-agent

# Restart
docker-compose restart document-ai-agent

# Stop
docker-compose down

# Rebuild after code changes
docker-compose build document-ai-agent
docker-compose up -d document-ai-agent

# Check status
docker-compose ps
```

## ⚠️ Important Notes

1. **First startup takes 1-2 minutes** - HuggingFace model needs to load (~500MB)
2. **OpenAI API Key Required** - For the query endpoint to work
3. **Upload documents first** - The vector store is empty until you upload files
4. **Port 8000** - Make sure nothing else is using this port

## 🐛 Troubleshooting

### "Internal Server Error" on /query/
- **Cause:** OpenAI API key not set
- **Fix:** Edit `.env` with your actual API key and restart

### Container keeps restarting
```bash
# Check logs
docker-compose logs document-ai-agent --tail=50
```

### Empty response from health check
- Wait 45 seconds after start
- Model is still loading

### Port already in use
```bash
# Stop conflicting container
docker stop python-latest

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

## 💡 Next Steps

1. **Add your OpenAI API key** to `.env`
2. **Restart** the container
3. **Upload** some documents
4. **Query** your documents!

## 📖 Example Workflow

```bash
# 1. Add API key (edit .env first)
docker-compose restart document-ai-agent
sleep 45

# 2. Check health
curl http://localhost:8000/health

# 3. Upload a document
curl -X POST http://localhost:8000/upload/ \
  -F "files=@mydocument.pdf"

# 4. Query it
curl -X POST http://localhost:8000/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic of this document?",
    "use_conversation": false
  }' | python3 -m json.tool
```

## ✨ Success!

Your Document AI Agent is ready to use! Just add your OpenAI API key and start uploading documents.

For interactive API testing, visit: http://localhost:8000/docs

