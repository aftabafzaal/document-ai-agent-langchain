# 📁 File Management Guide

## Current Setup

Your Document AI Agent stores files in multiple locations:

```
data/
├── uploads/          # ✅ Original uploaded files (KEPT)
├── temp_processing/  # ❌ Temporary (DELETED after processing)
└── vector_store/     # ✅ Vector embeddings (KEPT)
```

---

## Should You Delete Files After Vector Store Creation?

### ⚖️ **Tradeoffs**

| Factor | Keep Files | Delete Files |
|--------|-----------|--------------|
| **Disk Space** | ❌ More space used | ✅ Less space used |
| **Reprocessing** | ✅ Can re-embed with different models | ❌ Must re-upload |
| **Backup** | ✅ Original preserved | ❌ Lost if vectors corrupt |
| **Audit Trail** | ✅ Can verify sources | ❌ No source verification |
| **Download** | ✅ Can provide to users | ❌ Can't retrieve |

---

## 📋 **Recommended Approach: Retention Policy**

Keep files for **30 days**, then auto-delete. This gives you:
- ✅ Time to verify vector quality
- ✅ Ability to re-embed if needed
- ✅ Automatic cleanup to save space

### **Implementation**

I've created `src/utils/file_cleanup.py` with three options:

#### **Option 1: Keep Files (Current - Recommended for Production)**

No changes needed! Files stay in `data/uploads/`.

**Pros:**
- Safe and flexible
- Can reprocess anytime
- Good for production

**Disk Usage:** ~10 MB per 1000 pages

---

#### **Option 2: Delete Immediately After Processing**

Add this to `src/api/main.py`:

```python
def process_documents(file_paths: List[str]):
    # ... existing processing code ...
    
    # Add at the end:
    for file_path in file_paths:
        cleanup_manager.delete_file_immediately(file_path)
```

**Pros:**
- Minimal disk usage
- Simple and clean

**Cons:**
- Can't reprocess without re-upload
- No backup

---

#### **Option 3: Auto-Delete After 30 Days (Best Balance)** ⭐

Add a cleanup endpoint:

```python
# In src/api/main.py

@app.post("/admin/cleanup-old-files/")
async def cleanup_old_files():
    """Delete files older than retention period"""
    deleted = cleanup_manager.cleanup_old_files()
    return {
        "deleted_count": len(deleted),
        "deleted_files": deleted
    }

@app.get("/admin/file-stats/")
async def get_file_stats():
    """Get file storage statistics"""
    return cleanup_manager.get_file_info()
```

**Schedule cleanup with cron:**

```bash
# Run cleanup daily at 2 AM
echo "0 2 * * * curl -X POST http://localhost:8000/admin/cleanup-old-files/" | crontab -
```

**Or add to docker-compose.yml:**

```yaml
services:
  document-ai-agent:
    # ... existing config ...
    command: >
      bash -c "
      uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
      while true; do
        sleep 86400;
        curl -X POST http://localhost:8000/admin/cleanup-old-files/
      done
      "
```

---

## 🔧 **Configuration Options**

Add to `.env`:

```bash
# File retention settings
FILE_RETENTION_DAYS=30        # Keep files for 30 days
DELETE_AFTER_PROCESSING=false # Set to true for immediate deletion
```

Update `config/settings.py`:

```python
class Settings(BaseSettings):
    # ... existing settings ...
    
    # File Management
    FILE_RETENTION_DAYS: int = 30
    DELETE_AFTER_PROCESSING: bool = False
```

---

## 📊 **Storage Estimates**

### **Current Usage**

```bash
# Check your current storage
du -sh data/uploads/      # Original files
du -sh data/vector_store/ # Vectors
```

### **Typical Storage Requirements**

| Document Type | Original Size | Vector Store Size | Ratio |
|---------------|---------------|-------------------|-------|
| PDF (100 pages) | 5 MB | 2 MB | 2.5x |
| Text (1000 docs) | 50 MB | 20 MB | 2.5x |
| DOCX (500 pages) | 10 MB | 4 MB | 2.5x |

**Rule of thumb:** Vectors = ~40% of original file size

---

## 🚀 **Quick Implementation**

### **For Production (Keep Files):**

No changes needed! Current setup is good.

```bash
# Just monitor disk space
docker exec document-ai-agent-langchain-document-ai-agent-1 df -h
```

---

### **For Development (Delete After Processing):**

```python
# Add to process_documents() in main.py

def process_documents(file_paths: List[str]):
    processor = LangChainDocumentProcessor()
    splitter = AdvancedTextSplitter()
    
    # ... existing processing ...
    
    vector_store_manager.add_documents(split_documents)
    
    # NEW: Delete files immediately
    if settings.DELETE_AFTER_PROCESSING:
        for file_path in file_paths:
            try:
                Path(file_path).unlink()
                logger.info(f"Deleted processed file: {file_path}")
            except Exception as e:
                logger.error(f"Error deleting {file_path}: {e}")
    
    # Clean temp files
    for temp_file in temp_dir.glob("*"):
        temp_file.unlink()
    temp_dir.rmdir()
```

Then set in `.env`:
```bash
DELETE_AFTER_PROCESSING=true
```

---

### **For Auto-Cleanup (Best of Both Worlds):**

1. **Add the cleanup utility** (already done - `src/utils/file_cleanup.py`)

2. **Add endpoints to main.py:**

```python
@app.post("/admin/cleanup-old-files/")
async def cleanup_old_files():
    deleted = cleanup_manager.cleanup_old_files()
    return {"deleted_count": len(deleted), "files": deleted}

@app.get("/admin/file-stats/")
async def get_file_stats():
    return cleanup_manager.get_file_info()
```

3. **Set up daily cleanup:**

```bash
# Add to crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * curl -X POST http://localhost:8000/admin/cleanup-old-files/
```

---

## 🧪 **Testing Different Approaches**

### **Check Current Storage:**

```bash
# Total storage used
du -sh data/

# Breakdown
du -sh data/uploads/        # Original files: ~9 MB
du -sh data/vector_store/   # Vectors: ~3.4 MB
```

### **Test Immediate Deletion:**

```bash
# Set in .env
echo "DELETE_AFTER_PROCESSING=true" >> .env

# Restart
docker-compose restart document-ai-agent

# Upload a test file
curl -X POST http://localhost:8000/upload/ -F "files=@test.pdf"

# Check if file was deleted
ls -lh data/uploads/
```

### **Test Auto-Cleanup:**

```bash
# Manually trigger cleanup
curl -X POST http://localhost:8000/admin/cleanup-old-files/

# Check statistics
curl http://localhost:8000/admin/file-stats/
```

---

## 📈 **Monitoring Disk Usage**

### **Add Monitoring Endpoint:**

```python
@app.get("/admin/storage-stats/")
async def get_storage_stats():
    import shutil
    
    uploads_size = sum(f.stat().st_size for f in Path("data/uploads").glob("*"))
    vectors_size = Path("data/vector_store").stat().st_size if Path("data/vector_store").exists() else 0
    
    disk_usage = shutil.disk_usage(".")
    
    return {
        "uploads_mb": round(uploads_size / 1024 / 1024, 2),
        "vectors_mb": round(vectors_size / 1024 / 1024, 2),
        "total_mb": round((uploads_size + vectors_size) / 1024 / 1024, 2),
        "disk_free_gb": round(disk_usage.free / 1024 / 1024 / 1024, 2),
        "disk_total_gb": round(disk_usage.total / 1024 / 1024 / 1024, 2)
    }
```

---

## 🎯 **My Recommendation for Your Use Case**

Based on your setup, I recommend:

### **Start: Keep Everything (Current)**
- Simple and safe
- Good for initial testing
- Easy to reprocess

### **After Testing: 30-Day Retention**
- Automatic cleanup
- Balances flexibility and disk usage
- Best for production

### **If Disk Space Critical: Delete Immediately**
- Only if absolutely needed
- Make sure you have backups elsewhere

---

## ⚙️ **Configuration Summary**

### **Current (Keep Files Forever):**
```bash
# .env
# No special configuration needed
```

### **Delete Immediately:**
```bash
# .env
DELETE_AFTER_PROCESSING=true
```

### **Auto-Cleanup (30 days):**
```bash
# .env
FILE_RETENTION_DAYS=30
DELETE_AFTER_PROCESSING=false

# Cron job
0 2 * * * curl -X POST http://localhost:8000/admin/cleanup-old-files/
```

---

## 🔍 **Decision Matrix**

**Keep files if:**
- ✅ You might change embedding models
- ✅ You need to verify vector quality
- ✅ Disk space is not a concern
- ✅ Users might need to download originals

**Delete files if:**
- ✅ Disk space is limited
- ✅ Files are backed up elsewhere
- ✅ You won't change embedding settings
- ✅ It's a demo/testing environment

**Use retention policy if:**
- ✅ You want the best of both worlds
- ✅ You're running in production
- ✅ You need time to verify quality
- ✅ You want automatic cleanup

---

## 📚 **Related Documentation**

- `LEARNING_GUIDE.md` - Understanding how the system works
- `PROVIDER_GUIDE.md` - Switching embedding models
- `SETUP_COMPLETE.md` - Running the application

---

**Current Status:** Your system keeps files forever (safest option).

**Recommended:** Implement 30-day retention for production.

