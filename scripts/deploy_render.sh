#!/bin/bash

# Deploy to Render
# Grounded_In: Assignment - 1.pdf

echo "🚀 Deploying to Render..."

# Check if render CLI is installed
if ! command -v render &> /dev/null; then
    echo "⚠️  Render CLI not found. Install from: https://render.com/docs/cli"
    echo "    Or deploy via Render Dashboard: https://dashboard.render.com/"
    exit 1
fi

# Check for required environment variables
if [ -z "$RENDER_API_KEY" ]; then
    echo "❌ RENDER_API_KEY not set"
    exit 1
fi

# Deploy
echo "📦 Deploying application..."
render deploy

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful"
else
    echo "❌ Deployment failed"
    exit 1
fi

echo "
🎉 Deployment complete!

Next steps:
1. Configure environment variables in Render Dashboard
2. Set up persistent disk for /data/chroma
3. Verify health endpoint: https://your-app.onrender.com/health
"
