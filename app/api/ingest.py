"""Flask API Blueprint - Document Ingestion"""

from flask import Blueprint, jsonify, request
import structlog
from datetime import datetime

from app.services.chroma_service import ChromaService
from app.config import get_config

bp = Blueprint('ingest', __name__)
logger = structlog.get_logger()
config = get_config()


@bp.route('/ingest', methods=['POST'])
def ingest_documents():
    """
    Ingest documents into ChromaDB.
    Grounded_In: Assignment - 1.pdf
    
    Expected JSON payload:
    {
        "documents": [
            {
                "content": "string",
                "metadata": {"source": "string", ...}
            }
        ],
        "chunk_size": 800,
        "chunk_overlap": 150
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'documents' not in data:
            return jsonify({
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "Missing required field: documents"
                },
                "status": "error"
            }), 400
        
        documents = data['documents']
        chunk_size = data.get('chunk_size', config.CHUNK_SIZE)
        chunk_overlap = data.get('chunk_overlap', config.CHUNK_OVERLAP)
        
        # Validate documents
        if not isinstance(documents, list):
            return jsonify({
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "documents must be an array"
                },
                "status": "error"
            }), 400
        
        # Ingest documents
        chroma_service = ChromaService()
        result = chroma_service.ingest_documents(
            documents=documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        logger.info(
            "documents_ingested_via_api",
            count=result['ingested_count'],
            chunks=result['chunks_created']
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error("ingest_failed", error=str(e))
        return jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"Ingestion failed: {str(e)}"
            },
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500
