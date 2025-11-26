#!/usr/bin/env python3
"""
Streamlit UI Launcher for Autonomous QA Agent
Grounded_In: Assignment - 1.pdf

This script starts the Streamlit UI interface.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Start the Streamlit UI."""
    
    # Get the project root directory
    project_root = Path(__file__).parent
    ui_file = project_root / "ui_app.py"
    
    # Check if ui_app.py exists
    if not ui_file.exists():
        print(f"❌ Error: {ui_file} not found!")
        sys.exit(1)
    
    print("🚀 Starting Streamlit UI...")
    print("📍 URL: http://localhost:8501")
    print("⚠️  Make sure the backend server is running on http://localhost:8000")
    print("\nTo start backend: python start_server.py")
    print("\n" + "="*60)
    
    # Start Streamlit
    try:
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(ui_file),
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Streamlit UI stopped")
    except Exception as e:
        print(f"\n❌ Error starting Streamlit: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
