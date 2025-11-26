"""
Flask Application Configuration
Grounded_In: Assignment - 1.pdf
"""

import os
from pathlib import Path


class Config:
    """Base configuration."""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_APP = os.getenv('FLASK_APP', 'app.main:app')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    
    # OpenRouter
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3.5-sonnet')
    OPENROUTER_EMBEDDING_MODEL = os.getenv('OPENROUTER_EMBEDDING_MODEL', 'openai/text-embedding-3-small')
    
    # ChromaDB
    CHROMA_PERSIST_DIR = os.getenv('CHROMA_PERSIST_DIR', '/data/chroma')
    CHROMA_COLLECTION = os.getenv('CHROMA_COLLECTION', 'assignment_index')
    
    # RAG Configuration
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 800))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 150))
    RETRIEVAL_K = int(os.getenv('RETRIEVAL_K', 6))
    
    # Selenium
    SELENIUM_HEADLESS = os.getenv('SELENIUM_HEADLESS', 'false').lower() == 'true'
    CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH', '/usr/bin/chromedriver')
    CHROME_BINARY_PATH = os.getenv('CHROME_BINARY_PATH', '/usr/bin/google-chrome')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DIR = Path(os.getenv('LOG_DIR', 'logs'))
    LOG_FORMAT = os.getenv('LOG_FORMAT', 'json')
    
    # Paths
    DOCS_DIR = Path('docs')
    TESTS_DIR = Path('tests')
    OUTPUT_DIR = Path('output')
    
    # Assignment document
    ASSIGNMENT_DOC = os.getenv('ASSIGNMENT_DOC', '/mnt/data/Assignment - 1.pdf')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV = 'production'


# Select configuration based on environment
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config() -> Config:
    """Get configuration based on environment."""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)
