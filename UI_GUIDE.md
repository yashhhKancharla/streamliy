# 🌐 Streamlit UI Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Backend Server (Required)

```bash
python start_server.py
```

The backend API must be running on `http://localhost:8000`

### 3. Start Streamlit UI

```bash
python start_ui.py
```

Or directly:

```bash
streamlit run ui_app.py
```

The UI will open automatically at: **http://localhost:8501**

---

## UI Features

### 🏠 Home
- System status overview
- Quick start guide
- Feature highlights

### 📥 Ingest Documents
- **Single Document Upload**: Add one document at a time
- **Batch Upload**: Add multiple documents simultaneously
- Configure chunk size and overlap
- Support for multiple categories (documentation, api, ui, legal, specs)

### 🔍 Query RAG
- Semantic search across ingested documents
- Adjustable number of results (k)
- AI-generated answers from retrieved context
- View similarity scores and metadata

### 🧪 Generate Tests
- Create test cases for any feature
- Select test types: Functional, UI, Security, Negative, Performance
- Choose priority levels: High, Medium, Low
- Multiple output formats: JSON, Markdown, Selenium Python scripts
- View generated test cases with detailed steps
- Download generated test files

### ▶️ Run Tests
- Execute generated Selenium tests
- Configure base URL and timeout
- Headless or visible browser mode
- View real-time execution results
- Access detailed logs and outputs

---

## Navigation

Use the **sidebar** to:
- Check system health status
- Navigate between pages
- Monitor service availability (Flask, ChromaDB, OpenRouter)

---

## System Status Indicators

- ✅ **Green (Healthy)**: All services running normally
- ❌ **Red (Unhealthy)**: Backend API not responding

If you see unhealthy status:
1. Ensure backend is running: `python start_server.py`
2. Check that port 8000 is available
3. Verify `.env` configuration

---

## Configuration

### Backend API URL

Default: `http://localhost:8000`

To change, edit `ui_app.py`:

```python
API_BASE_URL = "http://your-backend-url:port"
```

### UI Port

Default: `8501`

To change, edit `.streamlit/config.toml`:

```toml
[server]
port = 8501
```

Or run with custom port:

```bash
streamlit run ui_app.py --server.port=8502
```

---

## Typical Workflow

1. **Start Backend**: `python start_server.py` (Terminal 1)
2. **Start UI**: `python start_ui.py` (Terminal 2)
3. **Ingest Documents**: Upload your project documentation
4. **Query to Verify**: Test semantic search on ingested docs
5. **Generate Tests**: Create test cases for your features
6. **Run Tests**: Execute tests against your application

---

## Example: Complete Flow

### Step 1: Ingest Documentation

```
Navigate to: 📥 Ingest Documents
Content: "User authentication requires email and password. Users must verify email before login."
Source: "auth_specs.md"
Category: "documentation"
Click: 🚀 Ingest Document
```

### Step 2: Query the System

```
Navigate to: 🔍 Query RAG
Query: "How does user authentication work?"
Results: 3
Click: 🔍 Search
```

### Step 3: Generate Test Cases

```
Navigate to: 🧪 Generate Tests
Feature: "User Login"
Requirements: "Users must login with email and password. Email verification required."
Test Types: ✅ Functional, ✅ UI, ✅ Security
Priority: ✅ High, ✅ Medium
Formats: ✅ JSON, ✅ Markdown, ✅ Selenium
Click: 🚀 Generate Test Cases
```

### Step 4: Review Generated Tests

View generated test cases with:
- Test ID and title
- Priority level (🔴 High, 🟡 Medium, 🟢 Low)
- Test type (functional, ui, security)
- Preconditions
- Detailed test steps
- Expected results

### Step 5: Run Tests (Optional)

```
Navigate to: ▶️ Run Tests
Test ID: "tc_user_login"
Base URL: "http://localhost:3000"
Click: ▶️ Run Test
```

---

## Troubleshooting

### UI Won't Start

**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
pip install streamlit
```

### Backend Not Responding

**Symptom**: Red status indicator in sidebar

**Solution**:
1. Check if backend is running:
   ```bash
   curl http://localhost:8000/health
   ```
2. Start backend if not running:
   ```bash
   python start_server.py
   ```

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Kill existing Streamlit process
pkill -f streamlit

# Or use different port
streamlit run ui_app.py --server.port=8502
```

### Connection Refused

**Symptom**: "Connection refused" when querying API

**Solution**:
- Verify backend URL in `ui_app.py`
- Check firewall settings
- Ensure backend and UI are on same network

---

## Advanced Usage

### Running on Different Machines

1. **Backend on Server A**:
   ```bash
   python start_server.py --host 0.0.0.0 --port 8000
   ```

2. **UI on Machine B**:
   Edit `ui_app.py`:
   ```python
   API_BASE_URL = "http://server-a-ip:8000"
   ```

### Custom Styling

Edit CSS in `ui_app.py` under the `st.markdown()` section to customize:
- Colors
- Fonts
- Card styles
- Layout

### Adding New Pages

1. Add new page in sidebar radio:
   ```python
   page = st.radio("Select Page", [..., "🆕 New Page"])
   ```

2. Add page content:
   ```python
   elif "🆕 New Page" in page:
       st.markdown("New page content")
   ```

---

## Screenshots

### Home Page
- System overview
- Quick start guide
- Feature cards

### Ingest Page
- Document upload form
- Batch processing
- Chunking configuration

### Query Page
- Search interface
- AI-generated answers
- Retrieved documents with scores

### Generate Tests Page
- Feature and requirements input
- Test type selection
- Generated test cases display

### Run Tests Page
- Test execution interface
- Real-time logs
- Pass/fail status

---

## Performance Tips

1. **Batch Ingestion**: Upload multiple documents at once
2. **Adjust k Value**: Lower k for faster queries
3. **Headless Mode**: Run tests headless for better performance
4. **Cache Results**: Streamlit auto-caches function results

---

## Keyboard Shortcuts

- `Ctrl + R` / `Cmd + R`: Rerun the app
- `Ctrl + Shift + R` / `Cmd + Shift + R`: Clear cache and rerun
- `Ctrl + K` / `Cmd + K`: Focus search (in Streamlit)

---

## API Endpoints Used

The UI interacts with these backend endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check system status |
| `/ingest` | POST | Upload documents |
| `/query` | POST | Search documents |
| `/generate-tests` | POST | Create test cases |
| `/run-test` | POST | Execute tests |

---

## Security Notes

- UI runs on localhost by default (not exposed externally)
- No authentication implemented (add if deploying publicly)
- Backend API should be secured if exposed to internet
- Consider adding rate limiting for production

---

## Deployment

### Local Development
```bash
python start_ui.py
```

### Production (with Authentication)

Add authentication using `streamlit-authenticator`:

```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(...)
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show app
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

---

## Support

For issues or questions:
- Check logs in `logs/` directory
- Verify backend health: `http://localhost:8000/health`
- Test API directly with `python test_all_apis.py`

---

**Version**: 1.0.0  
**Last Updated**: November 26, 2025  
**Tech Stack**: Streamlit, Flask, ChromaDB, OpenRouter
