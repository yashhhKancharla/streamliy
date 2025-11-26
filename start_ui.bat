@echo off
REM Streamlit UI Launcher for Windows
REM Grounded_In: Assignment - 1.pdf

echo ========================================
echo Starting Streamlit UI
echo ========================================
echo.
echo UI will be available at: http://localhost:8501
echo.
echo IMPORTANT: Make sure backend is running on http://localhost:8000
echo To start backend: python start_server.py
echo.
echo ========================================

python start_ui.py
