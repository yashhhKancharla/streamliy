#!/bin/bash
# Start Flask backend for Render deployment

exec gunicorn \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 4 \
  --worker-class sync \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  "app.main:app"
