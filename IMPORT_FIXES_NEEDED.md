# LangChain Import Fixes Needed

## Issue
The codebase uses **LangChain v0.1.x** import paths, but the requirements.txt installed **LangChain v1.0+**, which has breaking changes.

## Files with Deprecated Imports

### ✅ FIXED:
- `src/core/langchain_loader.py` ✓
- `src/core/text_splitter.py` ✓  
- `src/vector_store/vector_store_manager.py` ✓
- `src/embeddings/embedding_manager.py` ✓

### ❌ NEEDS FIXING:
- `src/agents/langchain_agent.py` - Uses `langchain.chains`, `langchain.chat_models`, etc.
- `src/agents/advanced_rag.py` - May have similar issues
- `src/agents/multi_agent_system.py` - May have similar issues

## Quick Fix Options

### Option 1: Downgrade LangChain (Easiest)
Edit `requirements.txt`:
```txt
# Change from:
langchain>=0.1.0

# To:
langchain==0.0.354
langchain-community==0.0.38
langchain-core==0.1.52
```

Then rebuild:
```bash
docker build -t document-ai-agent:latest .
```

### Option 2: Update All Imports (Recommended Long-term)

#### Changes needed in `src/agents/langchain_agent.py`:
```python
# OLD (v0.1.x):
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseRetriever

# NEW (v1.0+):
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.retrievers import BaseRetriever
```

### Option 3: Simplified Working Version (Fastest)

I can create a minimal working API that:
- ✅ Uploads documents
- ✅ Stores in vector database
- ✅ Basic similarity search
- ❌ Skip complex agent/chain features for now

## Recommendation

**For immediate testing**, I suggest **Option 1** (downgrade) because:
1. Quickest solution (5 minutes)
2. No code changes needed
3. All existing code will work

**For production**, plan **Option 2** (update all imports) to use latest LangChain features.

## Commands to Fix Now

```bash
# 1. Edit requirements.txt
nano requirements.txt

# 2. Change these lines:
#    langchain>=0.1.0 → langchain==0.0.354
#    langchain-community>=0.0.1 → langchain-community==0.0.38  
#    langchain-core>=0.1.0 → langchain-core==0.1.52

# 3. Rebuild
docker build --no-cache -t document-ai-agent:latest .

# 4. Run
docker run -d -p 8001:8000 -v $(pwd)/data:/app/data --env-file .env --name doc-ai-agent document-ai-agent:latest

# 5. Test
curl http://localhost:8001/health
```

## Status
- Docker image: ✅ Built successfully  
- Container: ❌ Crashes on start due to import errors
- Solution: Choose one of the 3 options above

The fastest path forward is **Option 1** - downgrade LangChain to match your existing code.

