#!/bin/bash
# Build script for Render - Forces Python 3.11

set -e

echo "=== Render Build Script ==="
echo "Python version check:"
python3.11 --version || python3 --version

echo ""
echo "=== Installing dependencies with Python 3.11 ==="
python3.11 -m pip install --upgrade pip setuptools wheel || python3 -m pip install --upgrade pip setuptools wheel

echo ""
echo "=== Installing requirements ==="
python3.11 -m pip install -r requirements.txt || python3 -m pip install -r requirements.txt

echo ""
echo "=== Build complete ==="
