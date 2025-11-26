# 🎨 Streamlit UI - Quick Access

## 🚀 Start the UI

### Windows
```bash
start_ui.bat
```

Or:
```bash
python start_ui.py
```

### Linux/Mac
```bash
python start_ui.py
```

## 🌐 Access URLs

- **Streamlit UI**: http://localhost:8501
- **Backend API**: http://localhost:8000

## ⚡ Quick Start (Both Backend + UI)

### Terminal 1 - Start Backend:
```bash
python start_server.py
```

### Terminal 2 - Start UI:
```bash
python start_ui.py
```

## 📖 Features Overview

### 🏠 Home Page
- System health monitoring
- Quick start guide
- Feature overview

### 📥 Ingest Documents
- Upload single or multiple documents
- Configure chunking parameters
- Categorize documents

### 🔍 Query RAG
- Semantic search across documents
- AI-generated answers
- View similarity scores

### 🧪 Generate Tests
- Create comprehensive test cases
- Multiple test types (Functional, UI, Security, etc.)
- Multiple output formats (JSON, Markdown, Selenium)

### ▶️ Run Tests
- Execute Selenium tests
- Real-time execution logs
- Pass/fail status

## 🎨 UI Screenshots

The UI provides:
- Clean, modern interface
- Real-time status indicators
- Interactive forms and results
- Expandable sections for details
- JSON export options

## 🔧 Configuration

Default settings in `.streamlit/config.toml`:
- Port: 8501
- Theme: Blue primary color
- Auto-reload enabled

## 📚 Full Documentation

See `UI_GUIDE.md` for complete documentation.

## ❓ Troubleshooting

**UI won't start?**
```bash
pip install streamlit
```

**Backend not responding?**
Check sidebar status indicator. If red:
```bash
python start_server.py
```

**Port already in use?**
```bash
streamlit run ui_app.py --server.port=8502
```

---

**Happy Testing! 🧪✨**
