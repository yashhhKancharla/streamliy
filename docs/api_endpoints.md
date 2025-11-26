# API Endpoints Documentation

**Grounded_In**: Assignment - 1.pdf

## Base URL

```
Development: http://localhost:8000
Production: https://your-app.onrender.com
```

## Authentication

All endpoints require API key in header:

```
X-API-Key: your_openrouter_api_key
```

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check service availability and version.

**Request:**

```bash
curl -X GET http://localhost:8000/health
```

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-25T10:30:00Z",
  "services": {
    "flask": "running",
    "chroma": "connected",
    "openrouter": "available"
  }
}
```

---

### 2. Ingest Documents

**POST** `/ingest`

Ingest and vectorize documentation into ChromaDB.

**Request:**

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "content": "API endpoint documentation...",
        "metadata": {"source": "api_docs", "version": "1.0"}
      }
    ]
  }'
```

**Request Body:**

```json
{
  "documents": [
    {
      "content": "string",
      "metadata": {
        "source": "string",
        "doc_type": "string",
        "version": "string"
      }
    }
  ],
  "chunk_size": 800,
  "chunk_overlap": 150
}
```

**Response:**

```json
{
  "status": "success",
  "ingested_count": 5,
  "chunks_created": 42,
  "collection": "assignment_index",
  "processing_time_ms": 1234
}
```

---

### 3. Query RAG System

**POST** `/query`

Retrieve relevant context from vector database.

**Request:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How to test user authentication?",
    "k": 6
  }'
```

**Request Body:**

```json
{
  "query": "string",
  "k": 6,
  "filters": {
    "source": "api_endpoints",
    "doc_type": "specification"
  }
}
```

**Response:**

```json
{
  "query": "How to test user authentication?",
  "results": [
    {
      "content": "Authentication requires...",
      "metadata": { "source": "api_endpoints.md", "chunk_id": "chunk_12" },
      "similarity_score": 0.92
    }
  ],
  "retrieval_time_ms": 156
}
```

---

### 4. Generate Test Cases

**POST** `/generate-tests`

Generate comprehensive test cases using RAG.

**Request:**

```bash
curl -X POST http://localhost:8000/generate-tests \
  -H "Content-Type: application/json" \
  -d '{
    "feature": "User Authentication",
    "requirements": "Users should be able to login with email and password",
    "output_formats": ["json", "markdown", "selenium"]
  }'
```

**Request Body:**

```json
{
  "feature": "string",
  "requirements": "string",
  "output_formats": ["json", "markdown", "selenium"],
  "priority_levels": ["high", "medium", "low"],
  "test_types": ["functional", "security", "ui"]
}
```

**Response:**

```json
{
  "status": "success",
  "test_cases": [
    {
      "id": "TC-001",
      "priority": "high",
      "title": "Valid user login",
      "preconditions": ["User exists in database"],
      "steps": [
        {
          "step_number": 1,
          "action": "Navigate to login page",
          "data": "https://app.com/login"
        }
      ],
      "expected_results": ["User redirected to dashboard"],
      "grounding_docs": ["api_endpoints.md", "ui_ux_guide.md"]
    }
  ],
  "output_files": {
    "json": "testcases.json",
    "markdown": "testcases.md",
    "selenium": ["test_login.py"]
  },
  "generation_time_ms": 3456
}
```

---

### 5. Run Test

**POST** `/run-test`

Execute a specific Selenium test case.

**Request:**

```bash
curl -X POST http://localhost:8000/run-test \
  -H "Content-Type: application/json" \
  -d '{
    "test_id": "TC-001",
    "base_url": "https://example.com",
    "headless": false
  }'
```

**Request Body:**

```json
{
  "test_id": "string",
  "base_url": "string",
  "headless": false,
  "timeout": 30,
  "screenshot_on_failure": true
}
```

**Response:**

```json
{
  "test_id": "TC-001",
  "status": "passed",
  "execution_time_ms": 5678,
  "steps_executed": 5,
  "screenshots": ["screenshot_001.png"],
  "error_message": null,
  "logs": [
    {
      "timestamp": "2025-11-25T10:35:00Z",
      "level": "INFO",
      "message": "Test started"
    }
  ]
}
```

---

## Error Responses

All endpoints return consistent error format:

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Missing required field: query",
    "details": {
      "field": "query",
      "expected_type": "string"
    }
  },
  "status": "error",
  "timestamp": "2025-11-25T10:40:00Z"
}
```

### Error Codes

- `INVALID_REQUEST`: Malformed request body
- `AUTHENTICATION_FAILED`: Invalid or missing API key
- `RESOURCE_NOT_FOUND`: Test case or document not found
- `INTERNAL_ERROR`: Server error
- `RATE_LIMIT_EXCEEDED`: Too many requests

---

## Rate Limiting

- **Development**: 100 requests/minute
- **Production**: 1000 requests/minute

---

## Webhooks

**POST** `/webhooks/test-complete`

Receive notifications when async tests complete:

```json
{
  "test_id": "TC-001",
  "status": "passed",
  "timestamp": "2025-11-25T10:45:00Z",
  "results_url": "https://api.com/results/TC-001"
}
```
