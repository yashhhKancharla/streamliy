"""Flask API Blueprint - Test Execution"""

from flask import Blueprint, jsonify, request
import structlog
from datetime import datetime
import subprocess
import json
from pathlib import Path

bp = Blueprint('run_test', __name__)
logger = structlog.get_logger()


@bp.route('/run-test', methods=['POST'])
def run_test_endpoint():
    """
    Execute a Selenium test.
    Grounded_In: Assignment - 1.pdf
    
    Expected JSON payload:
    {
        "test_id": "string",
        "base_url": "string",
        "headless": false,
        "timeout": 30,
        "screenshot_on_failure": true
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'test_id' not in data:
            return jsonify({
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "Missing required field: test_id"
                },
                "status": "error"
            }), 400
        
        test_id = data['test_id']
        base_url = data.get('base_url', 'http://localhost:3000')
        headless = data.get('headless', False)
        timeout = data.get('timeout', 30)
        
        # Find test file
        test_file = _find_test_file(test_id)
        
        if not test_file:
            return jsonify({
                "error": {
                    "code": "RESOURCE_NOT_FOUND",
                    "message": f"Test case with ID '{test_id}' not found"
                },
                "status": "error"
            }), 404
        
        # Run test with pytest
        result = _execute_test(test_file, base_url, headless, timeout)
        
        logger.info(
            "test_execution_completed",
            test_id=test_id,
            status=result['status']
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error("test_execution_failed", error=str(e))
        return jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"Test execution failed: {str(e)}"
            },
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500


def _find_test_file(test_id: str) -> str:
    """Find test file by test ID."""
    test_dir = Path("tests/selenium")
    
    if not test_dir.exists():
        return None
    
    # Search for file containing test_id
    test_id_normalized = test_id.replace('-', '_').lower()
    
    for test_file in test_dir.glob("test_*.py"):
        if test_id_normalized in test_file.name:
            return str(test_file)
    
    return None


def _execute_test(test_file: str, base_url: str, headless: bool, timeout: int) -> dict:
    """Execute test using pytest."""
    import time
    start_time = time.time()
    
    # Prepare pytest command
    cmd = [
        "pytest",
        test_file,
        "-v",
        "--tb=short",
        f"--base-url={base_url}",
        f"--timeout={timeout}"
    ]
    
    if headless:
        cmd.append("--headless")
    
    # Set environment variable for headless mode
    import os
    env = os.environ.copy()
    env['SELENIUM_HEADLESS'] = 'true' if headless else 'false'
    
    try:
        # Execute test
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 10,
            env=env
        )
        
        end_time = time.time()
        
        # Parse result
        passed = result.returncode == 0
        
        return {
            "test_id": Path(test_file).stem.replace('test_', '').upper(),
            "status": "passed" if passed else "failed",
            "execution_time_ms": int((end_time - start_time) * 1000),
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "logs": _parse_logs(result.stdout),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except subprocess.TimeoutExpired:
        return {
            "test_id": Path(test_file).stem.replace('test_', '').upper(),
            "status": "timeout",
            "error_message": f"Test execution exceeded timeout of {timeout} seconds",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        return {
            "test_id": Path(test_file).stem.replace('test_', '').upper(),
            "status": "error",
            "error_message": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


def _parse_logs(output: str) -> list:
    """Parse pytest output into structured logs."""
    logs = []
    
    for line in output.split('\n'):
        if line.strip():
            logs.append({
                "message": line,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
    
    return logs
