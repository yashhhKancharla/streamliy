# Quick Start Guide

## ⚡ 30-Second Setup

1. **Start Server** (in project directory):

   ```bash
   python start_server.py
   ```

2. **Test All APIs**:

   ```bash
   python test_all_apis.py
   ```

3. **Expected Result**: 5/5 tests passing ✅

---

## 🔗 API Endpoints

### GET /health

Returns health status of all services.

**Example:**

```bash
curl http://localhost:8000/health
```

**Response:**

```json
{
  "status": "healthy",
  "services": {
    "flask": "running",
    "chroma": "connected",
    "openrouter": "available"
  }
}
```

---

### POST /ingest

Ingest documents into the RAG system.

**Request:**

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "content": "Your document text here",
        "metadata": {
          "source": "doc1.md",
          "category": "documentation"
        }
      }
    ]
  }'
```

**Response:**

```json
{
  "status": "success",
  "ingested_count": 1,
  "chunks_created": 2,
  "processing_time_ms": 5234
}
```

---

### POST /query

Query the RAG system with semantic search and LLM answer generation.

**Request:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does authentication work?",
    "k": 3
  }'
```

**Response:**

```json
{
  "query": "How does authentication work?",
  "answer": "Based on the search results: User authentication requires...",
  "results": [
    {
      "content": "User authentication is required for endpoints...",
      "metadata": { "source": "doc1.md", "category": "auth" },
      "similarity_score": 0.89
    }
  ],
  "total_results": 3,
  "retrieval_time_ms": 2456
}
```

---

### POST /generate-tests

Generate test cases for a feature.

**Request:**

```bash
curl -X POST http://localhost:8000/generate-tests \
  -H "Content-Type: application/json" \
  -d '{
    "feature": "User Login",
    "requirements": "Users must be able to login with email and password",
    "output_formats": ["json", "markdown", "selenium"]
  }'
```

**Response:**

```json
{
  "status": "success",
  "feature": "User Login",
  "test_cases": [
    {
      "id": "TC-001",
      "priority": "high",
      "type": "functional",
      "title": "Valid login with correct credentials",
      "preconditions": ["User registered", "App is accessible"],
      "steps": [
        {
          "step_number": 1,
          "action": "Open login page",
          "expected": "Login form displayed"
        },
        {
          "step_number": 2,
          "action": "Enter credentials",
          "expected": "Fields populated"
        }
      ]
    }
  ],
  "generation_time_ms": 8500
}
```

---

### POST /run-test

Execute a test case.

**Request:**

```bash
curl -X POST http://localhost:8000/run-test \
  -H "Content-Type: application/json" \
  -d '{
    "test_id": "TC-AUTH-001",
    "base_url": "http://localhost:3000"
  }'
```

**Response:**

```json
{
  "status": "failed",
  "test_id": "TC-AUTH-001",
  "exit_code": 1,
  "execution_time_ms": 5234,
  "logs": [{ "message": "test session starts", "timestamp": "..." }]
}
```

---

## 🐛 Troubleshooting

### Port 8000 already in use

```bash
# Kill existing process and restart
pkill -f "python start_server.py"
python start_server.py
```

### ChromaDB connection error

```bash
# Clear and reinit ChromaDB
rm -rf ./data/chroma
python start_server.py
```

### OpenRouter API key invalid

1. Check `.env` file
2. Verify API key starts with `sk-or-v1-`
3. Ensure you have OpenRouter credits

### Test failures

1. Verify server is running: `curl http://localhost:8000/health`
2. Check logs in `logs/` directory
3. Run: `python test_all_apis.py` for detailed output

---

## 📊 Test All Endpoints

```bash
python test_all_apis.py
```

This runs comprehensive tests on all 5 endpoints and reports pass/fail status.

---

## 🎯 What's Included

✅ Flask REST API with 5 endpoints  
✅ ChromaDB vector database integration  
✅ OpenRouter LLM integration  
✅ Semantic search (RAG)  
✅ Automatic test case generation  
✅ Selenium test execution framework  
✅ Comprehensive error handling  
✅ Structured logging

---

## 📞 Configuration

All settings in `.env` file:

```
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=mistralai/mistral-nemo:free
CHROMA_PERSIST_DIR=./data/chroma
FLASK_ENV=development
DEBUG=true
```

---

**Status**: ✅ All 5 endpoints working  
**Success Rate**: 100%  
**Last Updated**: November 26, 2025
