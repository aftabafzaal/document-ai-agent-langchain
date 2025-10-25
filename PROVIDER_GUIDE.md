# 🤖 AI Provider Configuration Guide

## Current Setup

Your Document AI Agent uses a **hybrid approach** for cost optimization:

- **Embeddings:** HuggingFace (FREE, local)
- **LLM:** OpenAI GPT-3.5-turbo (Cheap, high-quality)

## Available Providers

### 1. HuggingFace 🤗

**Best For:** Embeddings (document vectorization)

**Advantages:**
- ✅ Completely FREE
- ✅ Runs locally (privacy)
- ✅ No API rate limits
- ✅ Works offline

**Current Model:** `sentence-transformers/all-mpnet-base-v2`

**Configuration:**
```bash
EMBEDDING_PROVIDER=huggingface
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

**Can Also Use For LLM (Lower Quality):**
```bash
LLM_PROVIDER=local
LLM_MODEL=google/flan-t5-large
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

---

### 2. OpenAI 🌐

**Best For:** LLM (answering questions)

**Advantages:**
- ✅ Highest quality responses
- ✅ Fast and reliable
- ✅ Best for production
- ✅ Cheap ($0.0005/1K tokens)

**Current Model:** `gpt-3.5-turbo`

**Configuration:**
```bash
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
OPENAI_API_KEY=sk-proj-...
```

**Available Models:**
- `gpt-3.5-turbo` - Fast, cheap, good quality
- `gpt-4` - Best quality, more expensive
- `gpt-4-turbo` - Fast GPT-4, good balance

**For Embeddings (More Expensive):**
```bash
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
```

---

### 3. Anthropic (Claude) 🔮

**Best For:** Complex reasoning, long documents

**Advantages:**
- ✅ Very accurate and safe
- ✅ 200K+ token context window
- ✅ Excellent reasoning
- ✅ Good alternative to OpenAI

**Configuration:**
```bash
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-sonnet-20240229
ANTHROPIC_API_KEY=sk-ant-...
```

**Available Models:**
- `claude-3-haiku-20240307` - Fastest, cheapest
- `claude-3-sonnet-20240229` - Balanced
- `claude-3-opus-20240229` - Most capable

---

## 💡 Recommended Configurations

### Configuration 1: Cost-Optimized (Current)
**Use Case:** Production, cost-sensitive

```bash
EMBEDDING_PROVIDER=huggingface  # FREE
LLM_PROVIDER=openai             # Cheap
LLM_MODEL=gpt-3.5-turbo
```

**Cost:** ~$0.02 per 1000 queries

---

### Configuration 2: Best Quality
**Use Case:** High-quality responses needed

```bash
EMBEDDING_PROVIDER=openai       # Better embeddings
EMBEDDING_MODEL=text-embedding-3-large
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo
```

**Cost:** ~$0.50 per 1000 queries

---

### Configuration 3: Claude Alternative
**Use Case:** OpenAI issues or prefer Claude

```bash
EMBEDDING_PROVIDER=huggingface  # FREE
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-sonnet-20240229
```

**Cost:** ~$0.03 per 1000 queries

---

### Configuration 4: Completely Free
**Use Case:** Testing, no budget

```bash
EMBEDDING_PROVIDER=huggingface
LLM_PROVIDER=local
LLM_MODEL=google/flan-t5-large
HUGGINGFACEHUB_API_TOKEN=your_token
```

**Cost:** $0.00 (quality is lower)

---

## 🔄 How to Switch Providers

### 1. Edit `.env` file
```bash
nano .env
```

### 2. Change the provider settings
```bash
# Example: Switch to Claude
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-sonnet-20240229
```

### 3. Restart the container
```bash
docker-compose down
docker-compose up -d document-ai-agent

# Wait for initialization (45 seconds)
sleep 45
```

### 4. Test the change
```bash
curl -X POST http://localhost:8000/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello, what model are you?"}'
```

---

## 📊 Provider Comparison

| Feature | HuggingFace | OpenAI | Anthropic |
|---------|-------------|--------|-----------|
| **Embeddings** | ✅ FREE | 💰 Paid | ❌ N/A |
| **LLM Quality** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Speed** | Fast | Very Fast | Fast |
| **Cost** | $0 | $0.0005/1K | $0.003/1K |
| **Context Length** | 8K | 128K | 200K |
| **Privacy** | ✅ Local | ❌ Cloud | ❌ Cloud |
| **Internet Required** | ❌ No | ✅ Yes | ✅ Yes |

---

## 🎯 Best Practices

### For Development
```bash
EMBEDDING_PROVIDER=huggingface
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
```

### For Production
```bash
EMBEDDING_PROVIDER=huggingface
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo
```

### For Long Documents
```bash
EMBEDDING_PROVIDER=huggingface
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-sonnet-20240229
```

### For Privacy-Sensitive Data
```bash
EMBEDDING_PROVIDER=huggingface
LLM_PROVIDER=local
LLM_MODEL=meta-llama/Llama-2-7b-chat-hf
```

---

## 🔑 Getting API Keys

### OpenAI
1. Go to: https://platform.openai.com/api-keys
2. Create new secret key
3. Add to `.env`: `OPENAI_API_KEY=sk-proj-...`

### Anthropic
1. Go to: https://console.anthropic.com/settings/keys
2. Create new API key
3. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

### HuggingFace
1. Go to: https://huggingface.co/settings/tokens
2. Create new token
3. Add to `.env`: `HUGGINGFACEHUB_API_TOKEN=hf_...`

---

## 💰 Cost Calculator

Assuming 1000 queries per month:

| Configuration | Monthly Cost |
|--------------|--------------|
| HuggingFace + Local | **$0** |
| HuggingFace + GPT-3.5 | **~$2** |
| HuggingFace + GPT-4 | **~$50** |
| HuggingFace + Claude | **~$3** |
| OpenAI Embeddings + GPT-4 | **~$60** |

**Current Setup:** ~$2/month for 1000 queries

---

## ❓ FAQ

**Q: Why not use OpenAI for embeddings too?**
A: HuggingFace embeddings are free and work great. OpenAI embeddings cost money with minimal quality improvement.

**Q: Can I use multiple LLM providers simultaneously?**
A: Not currently, but you can switch by changing `.env` and restarting.

**Q: Which is better: OpenAI or Anthropic?**
A: OpenAI is faster and cheaper. Anthropic is better for complex reasoning and long documents.

**Q: What if I don't have an API key?**
A: Use the "Completely Free" configuration with HuggingFace for both.

**Q: How do I know which provider is currently active?**
A: Check: `cat .env | grep -E "EMBEDDING_PROVIDER|LLM_PROVIDER"`

---

## 🔧 Troubleshooting

### Error: "AuthenticationError: Invalid API key"
**Fix:** Check your API key in `.env` and restart the container.

### Error: "Rate limit exceeded"
**Fix:** Switch to a different provider or wait.

### Slow responses
**Fix:** Use GPT-3.5-turbo instead of GPT-4, or switch to local models.

### Out of money
**Fix:** Switch to the "Completely Free" configuration.

---

**Current Active Configuration:**
- Embeddings: HuggingFace (FREE)
- LLM: OpenAI GPT-3.5-turbo (~$0.02/1000 queries)

