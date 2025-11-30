#!/bin/bash
# Render startup script - runs both Flask backend and Streamlit frontend

set -e

echo "Starting Autonomous QA Agent on Render..."

# Create necessary directories
mkdir -p logs data/chroma output

# Set PORT default if not set (for local development)
export PORT=${PORT:-8501}

# Start Flask backend in background (on port 8000)
echo "Starting Flask backend server on port 8000..."
python start_server.py &
FLASK_PID=$!

# Wait for Flask to start
echo "Waiting for Flask to initialize..."
sleep 5

# Start Streamlit frontend on the assigned PORT
echo "Starting Streamlit frontend on port $PORT..."
streamlit run ui_app.py \
  --server.port=$PORT \
  --server.address=0.0.0.0 \
  --logger.level=info \
  --client.showErrorDetails=true

# Cleanup on exit
trap "kill $FLASK_PID 2>/dev/null || true" EXIT
