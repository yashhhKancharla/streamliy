#!/bin/bash

# Run application locally
# Grounded_In: Assignment - 1.pdf

echo "🚀 Starting Autonomous QA Agent..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded from .env"
else
    echo "⚠️  No .env file found, using defaults"
fi

# Create necessary directories
mkdir -p logs output /data/chroma tests/selenium

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "🐍 Python version: $python_version"

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

# Run Flask app
echo "🌐 Starting Flask server on ${HOST:-0.0.0.0}:${PORT:-8000}..."
python app/main.py
