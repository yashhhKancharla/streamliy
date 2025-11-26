# Autonomous QA Agent

**Grounded_In**: Assignment - 1.pdf

An intelligent Flask-based testing system that leverages RAG (Retrieval-Augmented Generation) to automatically generate and execute comprehensive test cases for web applications.

## Features

- 🤖 **RAG-Powered Test Generation**: Uses OpenRouter LLM + ChromaDB for context-aware test case creation
- 🧪 **Selenium Automation**: Automated test execution with Chrome WebDriver
- 📊 **Multi-Format Output**: JSON, Markdown, and executable Python test scripts
- 🐳 **Docker Ready**: Containerized for easy deployment on Render or any container platform
- 🔍 **Vector Search**: Semantic search over documentation for grounded test generation
- 📡 **RESTful API**: Complete API for ingestion, querying, generation, and execution

## Quick Start

### Prerequisites

- Python 3.10+
- Docker (optional)
- OpenRouter API key

### Installation

```bash
# Clone repository
git clone <repository-url>
cd task\ 1

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and add your OpenRouter API key
nano .env
```

### Running the Application

#### Option 1: Backend + UI (Recommended)

```bash
# Terminal 1: Start Backend API
python start_server.py

# Terminal 2: Start Streamlit UI
python start_ui.py
```

Then open your browser to:
- **UI**: http://localhost:8501
- **API**: http://localhost:8000

#### Option 2: Backend Only

```bash
# Run backend API
python start_server.py

# Or use script
bash scripts/run_local.sh
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check health
curl http://localhost:8000/health
```

## API Endpoints

- `GET /health` - Health check
- `POST /ingest` - Ingest documents
- `POST /query` - Query RAG system
- `POST /generate-tests` - Generate test cases
- `POST /run-test` - Execute test

See [API Documentation](docs/api_endpoints.md) for details.

## Documentation

- [Product Specifications](docs/product_specs.md)
- [API Endpoints](docs/api_endpoints.md)
- [UI/UX Guide](docs/ui_ux_guide.md)
- [Admin Manual](docs/admin_manual.md)
- [Legal Constraints](docs/legal_constraints.md)
- [Demo Script](demo_script.md)

## Project Structure

```
.
├── app/
│   ├── api/              # Flask API endpoints
│   ├── services/         # Business logic
│   └── utils/            # Utilities
├── docs/                 # Documentation
├── tests/                # Test files
├── scripts/              # Utility scripts
├── output/               # Generated test cases
└── prompt_templates/     # LLM prompts
```

## License

Proprietary - All Rights Reserved

## Support

For issues or questions, please contact: support@example.com
