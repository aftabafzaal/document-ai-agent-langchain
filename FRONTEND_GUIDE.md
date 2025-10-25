# 🎨 Frontend Guide - ChatGPT-Style Interface

## 📁 What Was Created

A beautiful, modern chat interface styled like ChatGPT that connects to your Document AI backend.

**File:** `frontend/index.html`

---

## ✨ Features

### **1. ChatGPT-Style Design**
- ✅ Dark theme matching ChatGPT
- ✅ Smooth animations
- ✅ User & AI message bubbles
- ✅ Typing indicators
- ✅ Responsive design (mobile-friendly)

### **2. Functionality**
- ✅ Send questions to `/query` endpoint
- ✅ Display AI responses
- ✅ Show source documents
- ✅ Processing time display
- ✅ Example prompts
- ✅ Chat history (localStorage)
- ✅ Clear chat button
- ✅ Error handling
- ✅ Connection status

### **3. User Experience**
- ✅ Auto-scrolling
- ✅ Enter to send, Shift+Enter for new line
- ✅ Auto-resizing text area
- ✅ Loading animations
- ✅ Keyboard shortcuts

---

## 🚀 How to Use

### **Option 1: Open Directly in Browser (Simplest)**

```bash
# Just open the file
open frontend/index.html

# Or on Linux
xdg-open frontend/index.html

# Or Windows
start frontend/index.html
```

**Full path:**
```
file:///Users/maftab/Desktop/Projects/Cloudways/ai/document-ai-agent-langchain/frontend/index.html
```

---

### **Option 2: Serve with Python (Recommended)**

```bash
# Navigate to frontend folder
cd frontend

# Start HTTP server
python3 -m http.server 3000

# Open in browser
open http://localhost:3000
```

Then navigate to: **http://localhost:3000**

---

### **Option 3: Serve with Node.js**

```bash
# Install http-server globally (once)
npm install -g http-server

# Navigate to frontend
cd frontend

# Start server
http-server -p 3000

# Open in browser
open http://localhost:3000
```

---

## 🔧 Configuration

### **Change API URL**

Edit `index.html` line ~297:

```javascript
// Current
const API_BASE_URL = 'http://localhost:8000';

// Change to your server
const API_BASE_URL = 'https://your-domain.com';
```

---

## 🎯 How It Works

### **Architecture:**

```
┌─────────────────┐
│   User Browser  │
│  (index.html)   │
└────────┬────────┘
         │
         │ HTTP POST /query/
         ▼
┌─────────────────┐
│  FastAPI Server │
│  (port 8000)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   AI Backend    │
│ (OpenAI, etc)   │
└─────────────────┘
```

### **Flow:**

1. **User types question** → Input box
2. **Frontend sends POST** → `/query/` endpoint
3. **Backend processes** → Retrieves docs + AI response
4. **Frontend displays** → Answer + sources

---

## 📸 Screenshots & Features

### **1. Empty State**
- Welcome message
- Example prompts
- Clean, inviting design

### **2. Chat Interface**
- User messages on left (dark background)
- AI messages on right (lighter background)
- Clear visual separation

### **3. Sources Display**
- Shows document sources
- File names and page numbers
- Expandable source content

### **4. Loading State**
- Animated dots while waiting
- Clear feedback

---

## 🎨 Customization

### **Change Colors**

Edit CSS variables in `index.html` (lines 12-24):

```css
:root {
    --bg-primary: #343541;      /* Main background */
    --bg-secondary: #444654;    /* Header/footer */
    --bg-chat: #40414f;         /* Chat bubbles */
    --text-primary: #ececf1;    /* Main text */
    --accent: #10a37f;          /* Brand color */
}
```

### **Light Theme Example:**

```css
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f7f7f8;
    --bg-chat: #f0f0f0;
    --text-primary: #1a1a1a;
    --accent: #0066cc;
}
```

### **Add Company Branding:**

Change header (line 278):

```html
<h1>
    <span>🤖</span>
    Your Company AI
</h1>
```

---

## 🔌 API Integration Details

### **Request Format:**

```javascript
POST http://localhost:8000/query/
Content-Type: application/json

{
    "question": "What is machine learning?",
    "use_conversation": false
}
```

### **Expected Response:**

```json
{
    "answer": "Machine learning is...",
    "sources": [
        {
            "content": "Snippet of relevant text...",
            "source": "file.pdf",
            "page": 5
        }
    ],
    "processing_time": 1.23
}
```

### **Error Handling:**

The frontend handles:
- ✅ Network errors
- ✅ API not running
- ✅ Empty responses
- ✅ Invalid JSON
- ✅ 404/500 errors

---

## 🚀 Production Deployment

### **1. Update CORS Settings**

In `src/api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Specific domain
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### **2. Serve Frontend**

#### **Option A: Nginx**

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/frontend;
        index index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000/;
    }
}
```

#### **Option B: Apache**

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /path/to/frontend
    
    ProxyPass /api http://localhost:8000
    ProxyPassReverse /api http://localhost:8000
</VirtualHost>
```

#### **Option C: Add to Docker**

Create `Dockerfile.frontend`:

```dockerfile
FROM nginx:alpine
COPY frontend/index.html /usr/share/nginx/html/
EXPOSE 80
```

Update `docker-compose.yml`:

```yaml
services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:80"
    depends_on:
      - document-ai-agent
```

---

## 🧪 Testing

### **1. Test with curl:**

```bash
# Make sure API is working
curl -X POST http://localhost:8000/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'
```

### **2. Test CORS:**

```bash
# Check CORS headers
curl -X OPTIONS http://localhost:8000/query/ \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

### **3. Browser Console:**

Open DevTools (F12) and check:
- Network tab for API calls
- Console for JavaScript errors

---

## 📱 Mobile Responsive

The interface automatically adapts to mobile:
- ✅ Smaller padding
- ✅ Single column layout
- ✅ Touch-friendly buttons
- ✅ Readable font sizes

Test with Chrome DevTools Device Toolbar (Ctrl+Shift+M)

---

## 🎁 Bonus Features

### **Add File Upload UI**

Add this after the header:

```html
<div class="upload-section">
    <input type="file" id="fileInput" accept=".pdf,.docx,.txt" multiple>
    <button onclick="uploadFiles()">Upload Documents</button>
</div>
```

```javascript
async function uploadFiles() {
    const input = document.getElementById('fileInput');
    const formData = new FormData();
    
    for (const file of input.files) {
        formData.append('files', file);
    }
    
    const response = await fetch(`${API_BASE_URL}/upload/`, {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    alert('Files uploaded successfully!');
}
```

### **Add Conversation History Sidebar**

```html
<div class="sidebar">
    <h3>History</h3>
    <div id="historyList"></div>
</div>
```

### **Add Voice Input**

```javascript
function startVoiceInput() {
    const recognition = new webkitSpeechRecognition();
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('messageInput').value = transcript;
    };
    recognition.start();
}
```

---

## 🐛 Troubleshooting

### **Issue: "Cannot connect to API"**

**Solution:**
1. Check Docker container is running:
   ```bash
   docker-compose ps
   ```
2. Test API directly:
   ```bash
   curl http://localhost:8000/health
   ```
3. Check CORS is enabled in `main.py`

### **Issue: "No response from AI"**

**Solution:**
1. Check API logs:
   ```bash
   docker-compose logs document-ai-agent --tail=50
   ```
2. Verify OpenAI API key is set
3. Check documents are uploaded

### **Issue: "Sources not showing"**

**Solution:**
- Check backend response includes `sources` array
- Verify vector store has documents
- Check browser console for JS errors

### **Issue: "Chat history not saving"**

**Solution:**
- Enable localStorage in browser
- Check browser privacy settings
- Clear cache and reload

---

## 📚 Related Files

- `src/api/main.py` - Backend API endpoints
- `docker-compose.yml` - Container configuration
- `.env` - API keys and settings

---

## 🎯 Quick Start Checklist

- [ ] Backend is running (`docker-compose ps`)
- [ ] API accessible (`curl http://localhost:8000/health`)
- [ ] Documents uploaded
- [ ] Frontend opened (`open frontend/index.html`)
- [ ] Test a query
- [ ] Check sources display

---

## 🌟 Future Enhancements

Ideas for improvement:
- [ ] Markdown rendering in responses
- [ ] Code syntax highlighting
- [ ] Export chat history
- [ ] Dark/Light theme toggle
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] File upload from chat
- [ ] Search chat history
- [ ] Share conversations
- [ ] Mobile app (PWA)

---

**Enjoy your ChatGPT-style Document AI interface! 🚀**

For questions or issues, check:
- `LEARNING_GUIDE.md` - How the system works
- `SETUP_COMPLETE.md` - Running the application
- API Docs: http://localhost:8000/docs




