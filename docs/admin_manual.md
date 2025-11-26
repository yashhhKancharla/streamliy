# Administrator Manual - Autonomous QA Agent System

**Grounded_In**: Assignment - 1.pdf

## Table of Contents

1. [System Overview](#system-overview)
2. [Installation & Setup](#installation--setup)
3. [Configuration Management](#configuration-management)
4. [User Management](#user-management)
5. [Database Administration](#database-administration)
6. [Monitoring & Logging](#monitoring--logging)
7. [Backup & Recovery](#backup--recovery)
8. [Troubleshooting](#troubleshooting)
9. [Security Best Practices](#security-best-practices)
10. [Maintenance Procedures](#maintenance-procedures)

---

## System Overview

The Autonomous QA Agent is a Flask-based system that provides:

- Automated test case generation using RAG
- Vector database for document storage and retrieval
- Selenium-based test execution
- RESTful API for integration

### Architecture Components

```
┌─────────────────────────────────────────┐
│          Load Balancer (Render)         │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│        Flask Application (Gunicorn)     │
│  ┌──────────────────────────────────┐   │
│  │  API Layer (Routes & Controllers)│   │
│  └──────────┬───────────────────────┘   │
│             │                            │
│  ┌──────────▼───────────┐  ┌─────────┐  │
│  │  RAG Service         │  │ TestGen │  │
│  │  - OpenRouter LLM    │  │ Service │  │
│  │  - Embeddings        │  └────┬────┘  │
│  └──────────┬───────────┘       │       │
└─────────────┼───────────────────┼───────┘
              │                   │
     ┌────────▼──────┐   ┌────────▼──────┐
     │  ChromaDB     │   │   Selenium    │
     │  Vector Store │   │   WebDriver   │
     └───────────────┘   └───────────────┘
```

---

## Installation & Setup

### Prerequisites

- **Operating System**: Linux (Ubuntu 20.04+) or Docker
- **Python**: 3.10 or higher
- **RAM**: Minimum 2GB, Recommended 4GB
- **Disk Space**: 10GB available
- **Network**: Outbound HTTPS access for OpenRouter API

### Initial Setup (Local)

1. **Clone Repository**

```bash
git clone https://github.com/your-org/qa-agent.git
cd qa-agent
```

2. **Create Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure Environment**

```bash
cp .env.example .env
nano .env  # Edit with your configuration
```

Required environment variables:

- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `OPENROUTER_MODEL`: Model to use (e.g., anthropic/claude-3.5-sonnet)
- `SECRET_KEY`: Flask secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)

5. **Initialize Database**

```bash
python scripts/init_db.py
```

6. **Ingest Documentation**

```bash
bash scripts/ingest_docs.sh
```

7. **Start Application**

```bash
bash scripts/run_local.sh
```

Access at: `http://localhost:8000`

### Docker Setup

1. **Build Image**

```bash
docker build -t qa-agent:latest .
```

2. **Run Container**

```bash
docker-compose up -d
```

3. **Verify Health**

```bash
curl http://localhost:8000/health
```

### Render Deployment

1. **Connect Repository**

   - Go to Render Dashboard → New Web Service
   - Connect your GitHub repository

2. **Configure Build**

   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:8000 app.main:app`

3. **Set Environment Variables**

   - Add all variables from `.env.example`
   - Set `FLASK_ENV=production`

4. **Configure Persistent Storage**

   - Add disk: `/data` → 10GB
   - Mount path: `/data/chroma`

5. **Deploy**

```bash
bash scripts/deploy_render.sh
```

---

## Configuration Management

### Environment Variables

**Core Settings**

```bash
FLASK_APP=app.main:app
FLASK_ENV=production
SECRET_KEY=<generated-secret>
HOST=0.0.0.0
PORT=8000
```

**OpenRouter Configuration**

```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxx
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

**ChromaDB Settings**

```bash
CHROMA_PERSIST_DIR=/data/chroma
CHROMA_COLLECTION=assignment_index
```

**RAG Parameters**

```bash
CHUNK_SIZE=800
CHUNK_OVERLAP=150
RETRIEVAL_K=6
```

**Selenium Configuration**

```bash
SELENIUM_HEADLESS=true
CHROME_DRIVER_PATH=/usr/bin/chromedriver
CHROME_BINARY_PATH=/usr/bin/google-chrome
```

**Logging**

```bash
LOG_LEVEL=INFO
LOG_DIR=logs
LOG_FORMAT=json
```

### Configuration Files

**Flask Config**: `app/config.py`

```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    CHROMA_PERSIST_DIR = os.getenv('CHROMA_PERSIST_DIR', '/data/chroma')
    # ... other settings
```

**Gunicorn Config**: `gunicorn.conf.py`

```python
workers = 4
worker_class = 'sync'
timeout = 120
bind = '0.0.0.0:8000'
```

---

## User Management

### Creating Admin User

```bash
python scripts/create_user.py --email admin@example.com --role admin
```

### User Roles

1. **Admin**: Full system access, user management
2. **Developer**: Test generation, execution, API access
3. **Viewer**: Read-only access to tests and results

### API Key Management

Generate new API key:

```bash
python scripts/generate_api_key.py --user admin@example.com
```

Revoke API key:

```bash
python scripts/revoke_api_key.py --key sk_xxx
```

List active keys:

```bash
python scripts/list_api_keys.py
```

---

## Database Administration

### ChromaDB Management

**View Collections**

```bash
python scripts/chroma_admin.py list-collections
```

**Collection Statistics**

```bash
python scripts/chroma_admin.py stats --collection assignment_index
```

**Clear Collection**

```bash
python scripts/chroma_admin.py clear --collection assignment_index
```

**Backup Database**

```bash
python scripts/chroma_admin.py backup --output /backups/chroma_$(date +%Y%m%d).tar.gz
```

**Restore Database**

```bash
python scripts/chroma_admin.py restore --input /backups/chroma_20251125.tar.gz
```

### Optimizing Vector Database

**Rebuild Index**

```bash
python scripts/chroma_admin.py rebuild-index
```

**Remove Duplicates**

```bash
python scripts/chroma_admin.py deduplicate
```

---

## Monitoring & Logging

### Log Locations

- **Application Logs**: `logs/app.log`
- **Error Logs**: `logs/error.log`
- **Action Audit**: `logs/actions.jsonl`
- **Test Execution**: `logs/test_execution.log`

### Log Rotation

Configured in `logging.conf`:

```ini
[handler_rotatingFileHandler]
maxBytes=10485760  # 10MB
backupCount=5
```

### Health Monitoring

**Check Service Health**

```bash
curl http://localhost:8000/health
```

Expected response:

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

**System Metrics Endpoint**

```bash
curl http://localhost:8000/metrics
```

Returns:

- Request count
- Average response time
- Error rate
- Database size
- Active connections

### Setting Up Alerts

**Email Alerts** (configure in `.env`):

```bash
ALERT_EMAIL=admin@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=alerts@example.com
SMTP_PASSWORD=<app-password>
```

**Alert Conditions**:

- Error rate > 5% for 5 minutes
- Response time > 5 seconds
- Database connection failures
- Disk space < 10%

---

## Backup & Recovery

### Automated Backups

**Configure Cron Job**:

```bash
crontab -e
```

Add:

```cron
# Daily backup at 2 AM
0 2 * * * /app/scripts/backup.sh >> /var/log/backup.log 2>&1

# Weekly full backup on Sunday
0 3 * * 0 /app/scripts/backup_full.sh >> /var/log/backup.log 2>&1
```

### Manual Backup

**Full System Backup**:

```bash
bash scripts/backup.sh --type full --output /backups
```

**Database Only**:

```bash
bash scripts/backup.sh --type db --output /backups
```

### Restore Procedures

**Restore from Backup**:

```bash
bash scripts/restore.sh --input /backups/backup_20251125.tar.gz
```

**Verify Restore**:

```bash
python scripts/verify_restore.py
```

---

## Troubleshooting

### Common Issues

#### Application Won't Start

**Symptom**: Flask fails to start
**Solution**:

```bash
# Check logs
tail -f logs/error.log

# Verify Python version
python --version  # Should be 3.10+

# Check dependencies
pip check

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### ChromaDB Connection Error

**Symptom**: "Cannot connect to ChromaDB"
**Solution**:

```bash
# Check permissions
ls -la /data/chroma

# Fix permissions
sudo chown -R $(whoami):$(whoami) /data/chroma

# Verify directory exists
mkdir -p /data/chroma
```

#### OpenRouter API Errors

**Symptom**: "Authentication failed" or "Rate limit exceeded"
**Solution**:

```bash
# Verify API key
echo $OPENROUTER_API_KEY

# Test API connectivity
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  https://openrouter.ai/api/v1/models

# Check rate limits
python scripts/check_api_limits.py
```

#### Selenium Tests Failing

**Symptom**: "Chrome driver not found"
**Solution**:

```bash
# Install ChromeDriver
bash scripts/install_chrome.sh

# Verify installation
which chromedriver
google-chrome --version

# Update driver
pip install --upgrade webdriver-manager
```

### Debug Mode

Enable detailed logging:

```bash
export LOG_LEVEL=DEBUG
export FLASK_DEBUG=1
python app/main.py
```

---

## Security Best Practices

### API Key Security

1. **Never commit keys to repository**

   - Use `.env` files (gitignored)
   - Use environment variables in production

2. **Rotate keys regularly**

   ```bash
   python scripts/rotate_api_keys.py --all
   ```

3. **Use different keys per environment**
   - Development: Low rate limit key
   - Production: High rate limit key

### Access Control

1. **Implement authentication** for all endpoints
2. **Use HTTPS** in production
3. **Enable CORS** selectively:
   ```python
   CORS(app, origins=['https://yourdomain.com'])
   ```

### Data Protection

1. **Encrypt sensitive data** at rest
2. **Sanitize user inputs** to prevent injection
3. **Implement rate limiting**:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["100 per hour"])
   ```

### Audit Logging

All sensitive operations logged to `logs/actions.jsonl`:

```json
{
  "timestamp": "2025-11-25T10:00:00Z",
  "user": "admin@example.com",
  "action": "test_generated",
  "resource": "TC-001",
  "ip_address": "192.168.1.100"
}
```

---

## Maintenance Procedures

### Weekly Maintenance

```bash
# Update dependencies
pip list --outdated
pip install -U <package>

# Clean old logs
find logs/ -name "*.log" -mtime +30 -delete

# Optimize database
python scripts/chroma_admin.py optimize

# Test backups
bash scripts/test_restore.sh
```

### Monthly Maintenance

```bash
# Security updates
pip install -r requirements.txt --upgrade

# Database vacuum
python scripts/chroma_admin.py vacuum

# Review access logs
python scripts/analyze_logs.py --month $(date +%Y-%m)

# Update SSL certificates (if applicable)
```

### Performance Tuning

**Adjust Worker Count**:

```bash
# In gunicorn.conf.py
workers = (2 * cpu_count) + 1
```

**Optimize ChromaDB**:

```python
# In chroma_service.py
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="/data/chroma",
    anonymized_telemetry=False
))
```

---

## Support & Resources

- **Documentation**: https://docs.yourapp.com
- **Issue Tracker**: https://github.com/your-org/qa-agent/issues
- **Email Support**: support@yourapp.com
- **Slack Channel**: #qa-agent-support

### Emergency Contacts

- **On-Call Engineer**: +1-555-0100
- **DevOps Lead**: devops@yourapp.com
- **Security Team**: security@yourapp.com
