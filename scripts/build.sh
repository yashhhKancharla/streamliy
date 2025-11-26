#!/bin/bash

# Build Docker image
# Grounded_In: Assignment - 1.pdf

echo "🔨 Building Docker image..."

docker build -t autonomous-qa-agent:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
    echo "📦 Image: autonomous-qa-agent:latest"
else
    echo "❌ Build failed"
    exit 1
fi
