"""Flask API Blueprint - Health Check"""

from flask import Blueprint, jsonify
import structlog
from datetime import datetime

from app.services.chroma_service import ChromaService
from app.utils.openrouter_client import OpenRouterClient

bp = Blueprint('health', __name__)
logger = structlog.get_logger()


@bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Grounded_In: Assignment - 1.pdf
    
    Returns service status and availability of dependencies.
    """
    try:
        # Check ChromaDB
        chroma_status = "connected"
        try:
            chroma_service = ChromaService()
            chroma_service.get_stats()
        except Exception as e:
            chroma_status = f"error: {str(e)}"
            logger.error("chroma_health_check_failed", error=str(e))
        
        # Check OpenRouter
        openrouter_status = "available"
        try:
            client = OpenRouterClient()
            if not client.test_connection():
                openrouter_status = "unavailable"
        except Exception as e:
            openrouter_status = f"error: {str(e)}"
            logger.error("openrouter_health_check_failed", error=str(e))
        
        response = {
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "services": {
                "flask": "running",
                "chroma": chroma_status,
                "openrouter": openrouter_status
            }
        }
        
        logger.info("health_check_performed", services=response["services"])
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error("health_check_failed", error=str(e))
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500
