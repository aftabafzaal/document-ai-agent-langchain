#!/bin/bash

echo "🔍 Third-Party Services Status Check"
echo "===================================="
echo ""

echo "📊 Current Configuration:"
echo "------------------------"
cat .env | grep -E "EMBEDDING_PROVIDER|LLM_PROVIDER|VECTOR_STORE" | grep -v "^#"
echo ""

echo "✅ Active Services:"
echo "-------------------"
docker exec document-ai-agent-langchain-document-ai-agent-1 python3 -c "
from config.settings import settings

print(f'1. Embeddings: {settings.EMBEDDING_PROVIDER.value} (Model: {settings.EMBEDDING_MODEL})')
print(f'   → Cost: FREE (local)')
print(f'   → Network: No')
print()
print(f'2. LLM: {settings.LLM_PROVIDER.value} (Model: {settings.LLM_MODEL})')
if settings.LLM_PROVIDER.value == 'openai':
    print(f'   → Cost: ~\$0.0005/1K tokens')
    print(f'   → Network: Yes')
elif settings.LLM_PROVIDER.value == 'anthropic':
    print(f'   → Cost: ~\$0.003/1K tokens')
    print(f'   → Network: Yes')
else:
    print(f'   → Cost: FREE (local)')
    print(f'   → Network: No')
print()
print(f'3. Vector Store: {settings.VECTOR_STORE}')
print(f'   → Cost: FREE (local)')
print(f'   → Network: No')
" 2>/dev/null

echo ""
echo "💾 Storage Usage:"
echo "----------------"
echo "Uploads: $(du -sh data/uploads/ 2>/dev/null | cut -f1)"
echo "Vectors: $(du -sh data/vector_store/ 2>/dev/null | cut -f1)"
echo "Total:   $(du -sh data/ 2>/dev/null | cut -f1)"
echo ""

echo "🔑 API Keys Configured:"
echo "----------------------"
[ ! -z "$OPENAI_API_KEY" ] && echo "✅ OpenAI" || echo "❌ OpenAI"
[ ! -z "$ANTHROPIC_API_KEY" ] && echo "✅ Anthropic" || echo "❌ Anthropic"
[ ! -z "$HUGGINGFACEHUB_API_TOKEN" ] && echo "✅ HuggingFace" || echo "❌ HuggingFace"
echo ""

echo "📡 External Network Calls:"
echo "-------------------------"
docker exec document-ai-agent-langchain-document-ai-agent-1 python3 -c "
from config.settings import settings

if settings.LLM_PROVIDER.value in ['openai', 'anthropic']:
    print(f'⚠️  YES - {settings.LLM_PROVIDER.value.upper()} is making external API calls')
else:
    print('✅ NO - Fully running locally')
" 2>/dev/null

echo ""
echo "💰 Estimated Cost (per 1000 queries):"
echo "-------------------------------------"
docker exec document-ai-agent-langchain-document-ai-agent-1 python3 -c "
from config.settings import settings

if settings.LLM_PROVIDER.value == 'openai':
    print('~\$0.50 USD')
elif settings.LLM_PROVIDER.value == 'anthropic':
    print('~\$3.00 USD')
else:
    print('\$0.00 (FREE)')
" 2>/dev/null



