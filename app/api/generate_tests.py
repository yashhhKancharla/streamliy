"""Flask API Blueprint - Test Generation"""

from flask import Blueprint, jsonify, request
import structlog
from datetime import datetime

from app.services.test_generation_service import TestGenerationService

bp = Blueprint('generate_tests', __name__)
logger = structlog.get_logger()


@bp.route('/generate-tests', methods=['POST'])
def generate_tests_endpoint():
    """
    Generate test cases using RAG + LLM.
    Grounded_In: Assignment - 1.pdf
    
    Expected JSON payload:
    {
        "feature": "string",
        "requirements": "string",
        "test_types": ["functional", "security", "ui"],
        "priority_levels": ["high", "medium", "low"],
        "output_formats": ["json", "markdown", "selenium"]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "Request body is required"
                },
                "status": "error"
            }), 400
        
        feature = data.get('feature')
        requirements = data.get('requirements')
        
        if not feature or not requirements:
            return jsonify({
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "Missing required fields: feature, requirements"
                },
                "status": "error"
            }), 400
        
        test_types = data.get('test_types', ["functional", "ui", "security", "negative"])
        priority_levels = data.get('priority_levels', ["high", "medium", "low"])
        output_formats = data.get('output_formats', ["json", "markdown", "selenium"])
        
        # Generate test cases
        service = TestGenerationService()
        result = service.generate_test_cases(
            feature=feature,
            requirements=requirements,
            test_types=test_types,
            priority_levels=priority_levels,
            output_formats=output_formats
        )
        
        logger.info(
            "test_generation_completed_via_api",
            feature=feature,
            test_count=len(result['test_cases'])
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error("test_generation_failed", error=str(e))
        return jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"Test generation failed: {str(e)}"
            },
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500
