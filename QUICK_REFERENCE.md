# Quick Reference Card

**Grounded_In**: Assignment - 1.pdf

---

## 🚀 Common Commands

### Setup

```bash
# Initial setup
cp .env.example .env
# Add your OPENROUTER_API_KEY to .env

# Install dependencies
pip install -r requirements.txt

# OR use Docker
docker-compose up -d
```

### Start Application

```bash
# Local
bash scripts/run_local.sh

# Docker
docker-compose up -d
```

### Ingest Documentation

```bash
bash scripts/ingest_docs.sh
```

### Run Tests

```bash
# All tests
bash scripts/run_tests.sh

# Specific test
pytest tests/selenium/test_tc_auth_001_login.py -v

# Headless
export SELENIUM_HEADLESS=true
pytest tests/selenium/ -v
```

---

## 📡 API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

### Ingest Documents

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {"content": "...", "metadata": {"source": "doc.md"}}
    ]
  }'
```

### Query RAG

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How does auth work?", "k": 6}'
```

### Generate Tests

```bash
curl -X POST http://localhost:8000/generate-tests \
  -H "Content-Type: application/json" \
  -d '{
    "feature": "User Login",
    "requirements": "Users login with email/password",
    "output_formats": ["json", "markdown", "selenium"]
  }'
```

### Run Test

```bash
curl -X POST http://localhost:8000/run-test \
  -H "Content-Type: application/json" \
  -d '{"test_id": "TC-AUTH-001", "base_url": "http://localhost:3000"}'
```

---

## 🐳 Docker Commands

```bash
# Build
docker build -t qa-agent .

# Run
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build
```

---

## 📁 Important Files

| File                    | Purpose                   |
| ----------------------- | ------------------------- |
| `.env`                  | Environment configuration |
| `requirements.txt`      | Python dependencies       |
| `app/main.py`           | Flask app entry point     |
| `app/config.py`         | Configuration settings    |
| `docs/api_endpoints.md` | API documentation         |
| `output/testcases.json` | Generated test cases      |
| `tests/conftest.py`     | Pytest fixtures           |

---

## 🔧 Environment Variables

```bash
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
CHROMA_PERSIST_DIR=/data/chroma
SELENIUM_HEADLESS=false  # true for CI
HOST=0.0.0.0
PORT=8000
```

---

## 🧪 Test Execution Modes

### Headed (Default)

```bash
export SELENIUM_HEADLESS=false
pytest tests/selenium/test_tc_auth_001_login.py
```

### Headless (CI)

```bash
export SELENIUM_HEADLESS=true
pytest tests/selenium/ -v
```

### With Base URL

```bash
pytest tests/selenium/ --base-url=https://example.com
```

---

## 📊 Check Status

### Service Health

```bash
curl http://localhost:8000/health | jq
```

### ChromaDB Stats

```bash
python3 << 'EOF'
from app.services.chroma_service import ChromaService
service = ChromaService()
print(service.get_stats())
EOF
```

### Test Connection

```bash
python3 app/utils/openrouter_client.py
```

---

## 🐛 Troubleshooting

### Logs

```bash
tail -f logs/app.log
tail -f logs/error.log
```

### Docker Logs

```bash
docker-compose logs -f qa-agent
```

### Reset ChromaDB

```bash
rm -rf /data/chroma/*
bash scripts/ingest_docs.sh
```

### Port Already in Use

```bash
lsof -i :8000
kill -9 <PID>
```

---

## 📚 Documentation

- **Quick Start**: `README.md`
- **Detailed Guide**: `README_DETAILED.md`
- **API Reference**: `docs/api_endpoints.md`
- **Demo Script**: `demo_script.md`
- **Admin Manual**: `docs/admin_manual.md`
- **Project Summary**: `PROJECT_SUMMARY.md`

---

## 🎯 Typical Workflow

1. **Setup** → Install dependencies, configure `.env`
2. **Start** → Run Flask app
3. **Ingest** → Load documentation into ChromaDB
4. **Query** → Test RAG retrieval
5. **Generate** → Create test cases for a feature
6. **Execute** → Run generated Selenium tests
7. **Deploy** → Docker → Render

---

**Grounded_In**: Assignment - 1.pdf  
**Version**: 1.0.0
