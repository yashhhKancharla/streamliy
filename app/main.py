"""
Flask Application Main Entry Point
Grounded_In: Assignment - 1.pdf
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import structlog
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.config import get_config
from app.api import health, ingest, query, generate_tests, run_test, list_documents
from app.utils.logger import setup_logging


def create_app():
    """Application factory pattern."""
    
    # Load configuration
    config = get_config()
    
    # Setup logging
    setup_logging(config.LOG_LEVEL, config.LOG_DIR)
    logger = structlog.get_logger()
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app)
    
    # Create necessary directories
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    Path(config.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(health.bp)
    app.register_blueprint(ingest.bp)
    app.register_blueprint(query.bp)
    app.register_blueprint(generate_tests.bp)
    app.register_blueprint(run_test.bp)
    app.register_blueprint(list_documents.bp)
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "error": {
                "code": "INVALID_REQUEST",
                "message": str(e)
            },
            "status": "error"
        }), 400
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "error": {
                "code": "RESOURCE_NOT_FOUND",
                "message": "The requested resource was not found"
            },
            "status": "error"
        }), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        logger.error("internal_server_error", error=str(e))
        return jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred"
            },
            "status": "error"
        }), 500
    
    logger.info(
        "flask_app_created",
        environment=config.FLASK_ENV,
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    config = get_config()
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
