"""Flask API Blueprint - List Ingested Documents"""

from flask import Blueprint, jsonify
import structlog
from datetime import datetime

from app.services.chroma_service import ChromaService

bp = Blueprint('list_documents', __name__)
logger = structlog.get_logger()


@bp.route('/list-documents', methods=['GET'])
def list_documents():
    """
    List all ingested document sources.
    
    Returns:
        JSON with list of document sources and their metadata
    """
    try:
        chroma_service = ChromaService()
        sources = chroma_service.list_document_sources()
        
        logger.info(
            "documents_listed_via_api",
            count=len(sources)
        )
        
        return jsonify({
            "status": "success",
            "documents": sources,
            "total_count": len(sources),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
        
    except Exception as e:
        logger.error("list_documents_failed", error=str(e))
        return jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"Failed to list documents: {str(e)}"
            },
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500
