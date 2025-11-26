#!/bin/bash

# Run all tests
# Grounded_In: Assignment - 1.pdf

echo "🧪 Running tests..."

# Load environment
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate || . venv/Scripts/activate
fi

# Set headless mode for CI
export SELENIUM_HEADLESS=true

# Run pytest
echo "🧪 Running Selenium tests..."
pytest tests/selenium/ -v --tb=short --maxfail=3

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "✅ All tests passed"
else
    echo "❌ Some tests failed"
fi

exit $exit_code
