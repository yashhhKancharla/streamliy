#!/bin/bash
# Start Flask backend for Render deployment

gunicorn app.main:app \
  --bind 0.0.0.0:$PORT \
  --workers 4 \
  --worker-class sync \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
