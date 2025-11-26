"""Flask API Blueprint - RAG Query"""

from flask import Blueprint, jsonify, request
import structlog
from datetime import datetime

from app.services.chroma_service import ChromaService
from app.config import get_config

bp = Blueprint('query', __name__)
logger = structlog.get_logger()
config = get_config()


@bp.route('/query', methods=['POST'])
def query_rag():
    """
    Query the RAG system.
    Grounded_In: Assignment - 1.pdf
    
    Expected JSON payload:
    {
        "query": "string",
        "k": 6,
        "filters": {"source": "string", ...}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "Missing required field: query",
                    "details": {
                        "field": "query",
                        "expected_type": "string"
                    }
                },
                "status": "error"
            }), 400
        
        query_text = data['query']
        k = data.get('k', config.RETRIEVAL_K)
        filters = data.get('filters', None)
        generate_answer = data.get('generate_answer', True)
        
        # Query ChromaDB
        chroma_service = ChromaService()
        result = chroma_service.query(
            query_text=query_text,
            k=k,
            filters=filters
        )
        
        # Generate answer from results if requested
        if generate_answer and result['results']:
            try:
                # Simply format the top result as answer
                top_result = result['results'][0]
                answer = f"Based on the search results: {top_result['content'][:200]}..."
                result['answer'] = answer
                
            except Exception as e:
                logger.warning("answer_generation_failed", error=str(e))
                result['answer'] = "Could not generate answer from retrieved documents"
        else:
            result['answer'] = "No relevant documents found to answer the query"
        
        logger.info(
            "query_executed_via_api",
            query_preview=query_text[:50],
            results_count=result['total_results'],
            has_answer=True
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error("query_failed", error=str(e))
        return jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"Query failed: {str(e)}"
            },
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500
