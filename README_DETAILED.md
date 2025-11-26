# Autonomous QA Agent - Detailed Documentation

**Grounded_In**: Assignment - 1.pdf

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [API Reference](#api-reference)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Development](#development)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Autonomous QA Agent is a production-grade Flask application that combines Retrieval-Augmented Generation (RAG) with Large Language Models to automatically generate and execute comprehensive test cases for web applications.

### Key Components

- **Flask API**: RESTful endpoints for all operations
- **ChromaDB**: Vector database for document storage and semantic search
- **OpenRouter**: LLM API for generation and embeddings
- **Selenium**: Browser automation for test execution
- **Docker**: Containerization for deployment

### Core Capabilities

1. **Document Ingestion**: Process and vectorize product documentation
2. **RAG Query**: Semantic search over documentation
3. **Test Generation**: Create test cases from requirements using RAG context
4. **Test Execution**: Run Selenium tests automatically
5. **Multi-Format Output**: JSON, Markdown, and Python scripts

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────┐
│          Client Applications             │
│     (CLI, Web UI, API Consumers)        │
└────────────┬────────────────────────────┘
             │ HTTP/REST
┌────────────▼────────────────────────────┐
│        Flask Application                 │
│  ┌──────────────────────────────────┐   │
│  │  API Layer                       │   │
│  │  - /health                       │   │
│  │  - /ingest                       │   │
│  │  - /query                        │   │
│  │  - /generate-tests               │   │
│  │  - /run-test                     │   │
│  └──────────┬───────────────────────┘   │
│             │                            │
│  ┌──────────▼───────────┐  ┌─────────┐  │
│  │  Services Layer      │  │ TestGen │  │
│  │  - ChromaService     │  │ Service │  │
│  │  - OpenRouterClient  │  └────┬────┘  │
│  └──────────┬───────────┘       │       │
└─────────────┼───────────────────┼───────┘
              │                   │
     ┌────────▼──────┐   ┌────────▼──────┐
     │  ChromaDB     │   │   Selenium    │
     │  Vector Store │   │   WebDriver   │
     └───────────────┘   └───────────────┘
              │                   │
     ┌────────▼──────┐   ┌────────▼──────┐
     │  OpenRouter   │   │    Chrome     │
     │     API       │   │   Browser     │
     └───────────────┘   └───────────────┘
```

### Data Flow

1. **Ingestion Flow**:

   - Documents → Chunking → Embedding → ChromaDB

2. **Query Flow**:

   - Query → Embedding → Vector Search → Ranked Results

3. **Generation Flow**:

   - Requirements → RAG Query → Context + Prompt → LLM → Test Cases

4. **Execution Flow**:
   - Test ID → Find Script → Selenium → Browser → Results

---

## Installation

### Local Development

#### Prerequisites

```bash
# Check Python version (3.10+ required)
python3 --version

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    google-chrome-stable \
    chromium-chromedriver
```

#### Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd "ocean Ai/task 1"

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
nano .env  # Add your OpenRouter API key

# 5. Create directories
mkdir -p logs output /data/chroma tests/selenium

# 6. Ingest documentation
bash scripts/ingest_docs.sh

# 7. Run application
bash scripts/run_local.sh
```

### Docker Setup

```bash
# 1. Build image
docker build -t qa-agent:latest .

# 2. Run with Docker Compose
docker-compose up -d

# 3. Check logs
docker-compose logs -f

# 4. Health check
curl http://localhost:8000/health
```

---

## Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```bash
# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-v1-xxxxx
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
OPENROUTER_EMBEDDING_MODEL=openai/text-embedding-3-small

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=<generate-with-python-secrets>
HOST=0.0.0.0
PORT=8000

# ChromaDB Configuration
CHROMA_PERSIST_DIR=/data/chroma
CHROMA_COLLECTION=assignment_index

# RAG Parameters
CHUNK_SIZE=800
CHUNK_OVERLAP=150
RETRIEVAL_K=6

# Selenium Configuration
SELENIUM_HEADLESS=false
CHROME_DRIVER_PATH=/usr/bin/chromedriver
CHROME_BINARY_PATH=/usr/bin/google-chrome

# Logging
LOG_LEVEL=INFO
LOG_DIR=logs
```

### Generate Secret Key

```python
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Usage

### 1. Ingest Documentation

```bash
# Ingest all docs in docs/ directory
bash scripts/ingest_docs.sh

# Or via API
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "content": "Your documentation content...",
        "metadata": {"source": "my_doc.md"}
      }
    ]
  }'
```

### 2. Query RAG System

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does authentication work?",
    "k": 6
  }'
```

### 3. Generate Test Cases

```bash
curl -X POST http://localhost:8000/generate-tests \
  -H "Content-Type: application/json" \
  -d '{
    "feature": "User Authentication",
    "requirements": "Users should be able to login with email and password",
    "output_formats": ["json", "markdown", "selenium"]
  }'
```

### 4. Run Tests

```bash
# Run specific test
curl -X POST http://localhost:8000/run-test \
  -H "Content-Type: application/json" \
  -d '{
    "test_id": "TC-AUTH-001",
    "base_url": "https://example.com",
    "headless": false
  }'

# Or run all tests with pytest
bash scripts/run_tests.sh
```

---

## API Reference

### Health Check

**GET** `/health`

Response:

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "flask": "running",
    "chroma": "connected",
    "openrouter": "available"
  }
}
```

### Document Ingestion

**POST** `/ingest`

Request:

```json
{
  "documents": [
    {
      "content": "string",
      "metadata": { "source": "string" }
    }
  ],
  "chunk_size": 800,
  "chunk_overlap": 150
}
```

### RAG Query

**POST** `/query`

Request:

```json
{
  "query": "string",
  "k": 6,
  "filters": { "source": "string" }
}
```

### Test Generation

**POST** `/generate-tests`

Request:

```json
{
  "feature": "string",
  "requirements": "string",
  "test_types": ["functional", "ui", "security"],
  "output_formats": ["json", "markdown", "selenium"]
}
```

### Test Execution

**POST** `/run-test`

Request:

```json
{
  "test_id": "string",
  "base_url": "string",
  "headless": false
}
```

---

## Testing

### Run All Tests

```bash
# Run with pytest
pytest tests/ -v

# Or use script
bash scripts/run_tests.sh
```

### Run Specific Test

```bash
pytest tests/selenium/test_tc_auth_001.py -v
```

### Headless Mode

```bash
# Set environment variable
export SELENIUM_HEADLESS=true
pytest tests/

# Or use flag
pytest tests/ --headless
```

### CI/CD Testing

```bash
# Run in CI environment
export SELENIUM_HEADLESS=true
export CI=true
pytest tests/ --tb=short --maxfail=3
```

---

## Deployment

### Deploy to Render

1. **Connect Repository**

   - Go to https://dashboard.render.com
   - New → Web Service
   - Connect your GitHub repository

2. **Configure Build**

   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 app.main:app`

3. **Environment Variables**

   - Add all variables from `.env.example`
   - Set `FLASK_ENV=production`
   - Set `SELENIUM_HEADLESS=true`

4. **Persistent Storage**

   - Add disk: `/data` → 10GB
   - Mount path: `/data/chroma`

5. **Deploy**

```bash
bash scripts/deploy_render.sh
```

### Docker Deployment

```bash
# Build
docker build -t qa-agent:latest .

# Run
docker run -d \
  -p 8000:8000 \
  -e OPENROUTER_API_KEY=your_key \
  -v /data/chroma:/data/chroma \
  qa-agent:latest
```

---

## Development

### Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # Flask app entry
│   ├── config.py            # Configuration
│   ├── api/                 # API endpoints
│   │   ├── health.py
│   │   ├── ingest.py
│   │   ├── query.py
│   │   ├── generate_tests.py
│   │   └── run_test.py
│   ├── services/            # Business logic
│   │   ├── chroma_service.py
│   │   └── test_generation_service.py
│   └── utils/               # Utilities
│       ├── openrouter_client.py
│       └── logger.py
├── docs/                    # Documentation
│   ├── product_specs.md
│   ├── api_endpoints.md
│   ├── ui_ux_guide.md
│   ├── admin_manual.md
│   ├── legal_constraints.md
│   └── sample_payloads.json
├── tests/                   # Tests
│   ├── conftest.py          # Pytest fixtures
│   └── selenium/            # Selenium tests
├── scripts/                 # Utility scripts
│   ├── build.sh
│   ├── run_local.sh
│   ├── ingest_docs.sh
│   ├── run_tests.sh
│   └── deploy_render.sh
├── prompt_templates/        # LLM prompts
│   ├── system.json
│   ├── user_short.txt
│   └── run_prompt.py
├── output/                  # Generated files
│   ├── testcases.json
│   └── testcases.md
├── logs/                    # Log files
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

### Adding New Endpoints

1. Create blueprint in `app/api/`
2. Register in `app/main.py`
3. Add tests in `tests/`

### Adding New Services

1. Create service in `app/services/`
2. Add type hints and docstrings
3. Import in endpoints

---

## Troubleshooting

### Common Issues

#### ChromaDB Not Connecting

```bash
# Check directory exists
ls -la /data/chroma

# Fix permissions
sudo chown -R $(whoami):$(whoami) /data/chroma
```

#### OpenRouter API Errors

```bash
# Test API key
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  https://openrouter.ai/api/v1/models
```

#### Selenium/Chrome Issues

```bash
# Install Chrome (Ubuntu)
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Install ChromeDriver
pip install webdriver-manager
```

#### Port Already in Use

```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Logs

```bash
# Application logs
tail -f logs/app.log

# Error logs
tail -f logs/error.log

# Docker logs
docker-compose logs -f
```

---

## Contributing

1. Fork repository
2. Create feature branch
3. Add tests
4. Submit pull request

---

## License

Proprietary - All Rights Reserved

---

## Support

- **Email**: support@example.com
- **Documentation**: See `docs/` directory
- **Issues**: GitHub Issues
- **Demo**: See `demo_script.md`

---

**Version**: 1.0.0  
**Last Updated**: November 25, 2025  
**Grounded_In**: Assignment - 1.pdf
