#!/bin/bash
# Start both Flask API server and Streamlit UI
# Flask runs on port 8000, Streamlit on port 8501

echo "========================================"
echo "Starting Autonomous QA Agent"
echo "========================================"
echo ""
echo "Flask API Server: http://localhost:8000"
echo "Streamlit UI:     http://localhost:8501"
echo ""
echo "Press Ctrl+C in each terminal to stop servers"
echo "========================================"
echo ""

# Activate virtual environment if it exists
if [ -f .venv/Scripts/activate ]; then
    source .venv/Scripts/activate
    echo "Virtual environment activated"
elif [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
    echo "Virtual environment activated"
else
    echo "Warning: Virtual environment not found"
fi

echo ""
echo "Starting Flask server on port 8000..."
python start_server.py &
FLASK_PID=$!

# Wait a moment for Flask to start
sleep 3

echo "Starting Streamlit UI on port 8501..."
streamlit run ui_app.py &
STREAMLIT_PID=$!

echo ""
echo "Both servers are running!"
echo "Flask PID: $FLASK_PID"
echo "Streamlit PID: $STREAMLIT_PID"
echo ""
echo "To stop servers, run:"
echo "  kill $FLASK_PID $STREAMLIT_PID"
echo ""

# Wait for user interrupt
wait
