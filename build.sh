#!/bin/bash
# Build script for Render - Forces binary wheels only

set -e

echo "=== Render Build Script ==="
echo "Python version:"
python --version

echo ""
echo "=== Upgrading pip ==="
pip install --upgrade pip setuptools wheel

echo ""
echo "=== Installing requirements (prefer binary wheels) ==="
pip install --prefer-binary -r requirements.txt

echo ""
echo "=== Creating directories ==="
mkdir -p logs data/chroma output

echo ""
echo "=== Build complete ==="
