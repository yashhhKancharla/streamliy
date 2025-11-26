@echo off
REM Start both Flask API server and Streamlit UI
REM Flask runs on port 8000, Streamlit on port 8501

echo ========================================
echo Starting Autonomous QA Agent
echo ========================================
echo.
echo Flask API Server: http://localhost:8000
echo Streamlit UI:     http://localhost:8501
echo.
echo Press Ctrl+C to stop both servers
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo Warning: Virtual environment not found
)

echo.
echo Starting Flask server on port 8000...
start "Flask API Server" cmd /k "python start_server.py"

REM Wait a moment for Flask to start
timeout /t 3 /nobreak >nul

echo Starting Streamlit UI on port 8501...
start "Streamlit UI" cmd /k "streamlit run ui_app.py"

echo.
echo Both servers are starting...
echo Check the new terminal windows for server logs
echo.
pause
