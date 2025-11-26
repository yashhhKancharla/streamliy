"""
Simple Flask Server Starter
Starts the Flask application without debug mode reloader
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
env_file = project_root / '.env'
if env_file.exists():
    load_dotenv(env_file)
    print(f"Loaded environment from {env_file}")
else:
    print(f"Warning: .env file not found at {env_file}")

# Set environment
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '0'

from app.main import app
from app.config import get_config

if __name__ == "__main__":
    config = get_config()
    print(f"Starting Flask server on {config.HOST}:{config.PORT}")
    print(f"Using Chroma directory: {config.CHROMA_PERSIST_DIR}")
    print(f"Using OpenRouter model: {os.getenv('OPENROUTER_MODEL')}")
    print("\nServer is ready for API requests...")
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=False,  # Disable debug mode to prevent reloader
        use_reloader=False
    )
