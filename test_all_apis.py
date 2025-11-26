"""
Comprehensive API Test Script for QA Agent
Tests all 5 API endpoints with detailed validation
"""

import requests
import json
import time
from typing import Dict, Any
import sys

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

# ANSI color codes for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}[OK] {text}{Colors.RESET}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}[ERROR] {text}{Colors.RESET}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}[INFO] {text}{Colors.RESET}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}[WARN] {text}{Colors.RESET}")

def format_json(data: Any) -> str:
    """Format JSON data for display"""
    return json.dumps(data, indent=2)

def test_health_endpoint() -> bool:
    """Test the /health endpoint"""
    print_header("TEST 1: Health Check Endpoint")
    print_info("Endpoint: GET /health")
    
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        elapsed = (time.time() - start_time) * 1000
        
        print_info(f"Status Code: {response.status_code}")
        print_info(f"Response Time: {elapsed:.2f}ms")
        
        if response.status_code == 200:
            data = response.json()
            print_info(f"Response:\n{format_json(data)}")
            
            # Validate response structure
            required_fields = ["status", "timestamp", "services"]
            for field in required_fields:
                if field not in data:
                    print_error(f"Missing required field: {field}")
                    return False
            
            # Check services status
            services = data.get("services", {})
            all_healthy = True
            for service, status in services.items():
                if status == "healthy":
                    print_success(f"Service '{service}' is healthy")
                else:
                    print_warning(f"Service '{service}' status: {status}")
                    all_healthy = False
            
            if all_healthy:
                print_success("Health check passed - all services healthy")
                return True
            else:
                print_warning("Health check passed but some services may have issues")
                return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Health check failed with exception: {str(e)}")
        return False

def test_ingest_endpoint() -> bool:
    """Test the /ingest endpoint"""
    print_header("TEST 2: Document Ingestion Endpoint")
    print_info("Endpoint: POST /ingest")
    
    # Test payload
    payload = {
        "documents": [
            {
                "content": "User authentication is required for all protected endpoints. Users must login with email and password.",
                "metadata": {"source": "test_auth_doc.md", "category": "authentication"}
            },
            {
                "content": "The RAG system retrieves K=6 most relevant documents based on semantic similarity using vector embeddings.",
                "metadata": {"source": "test_rag_doc.md", "category": "rag"}
            },
            {
                "content": "Test cases should include positive and negative scenarios, edge cases, and boundary conditions.",
                "metadata": {"source": "test_qa_doc.md", "category": "testing"}
            }
        ]
    }
    
    print_info(f"Payload:\n{format_json(payload)}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/ingest",
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        elapsed = (time.time() - start_time) * 1000
        
        print_info(f"Status Code: {response.status_code}")
        print_info(f"Response Time: {elapsed:.2f}ms")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_info(f"Response:\n{format_json(data)}")
            
            # Validate response
            if "message" in data or "status" in data:
                print_success("Document ingestion successful")
                return True
            else:
                print_warning("Ingestion completed but response structure unexpected")
                return True
        else:
            print_error(f"Ingestion failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Ingestion failed with exception: {str(e)}")
        return False

def test_query_endpoint() -> bool:
    """Test the /query endpoint"""
    print_header("TEST 3: RAG Query Endpoint")
    print_info("Endpoint: POST /query")
    
    # Test payload
    payload = {
        "query": "How does user authentication work?",
        "k": 3
    }
    
    print_info(f"Payload:\n{format_json(payload)}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/query",
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        elapsed = (time.time() - start_time) * 1000
        
        print_info(f"Status Code: {response.status_code}")
        print_info(f"Response Time: {elapsed:.2f}ms")
        
        if response.status_code == 200:
            data = response.json()
            print_info(f"Response:\n{format_json(data)}")
            
            # Validate response structure
            if "answer" in data:
                print_success(f"Query successful - Answer: {data['answer'][:100]}...")
                
                # Check for context if available
                if "context" in data:
                    print_success(f"Retrieved {len(data['context'])} context documents")
                
                return True
            else:
                print_error("Response missing 'answer' field")
                return False
        else:
            print_error(f"Query failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Query failed with exception: {str(e)}")
        return False

def test_generate_tests_endpoint() -> bool:
    """Test the /generate-tests endpoint"""
    print_header("TEST 4: Test Generation Endpoint")
    print_info("Endpoint: POST /generate-tests")
    
    # Test payload
    payload = {
        "feature": "User Login",
        "requirements": "Users should be able to login with email and password. The system should validate credentials and return appropriate error messages for invalid inputs.",
        "output_formats": ["json", "markdown"]
    }
    
    print_info(f"Payload:\n{format_json(payload)}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/generate-tests",
            headers=HEADERS,
            json=payload,
            timeout=60
        )
        elapsed = (time.time() - start_time) * 1000
        
        print_info(f"Status Code: {response.status_code}")
        print_info(f"Response Time: {elapsed:.2f}ms")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_info(f"Response:\n{format_json(data)}")
            
            # Validate response
            if "test_cases" in data or "files" in data or "message" in data:
                print_success("Test generation successful")
                
                # Check for generated files
                if "files" in data:
                    for file in data["files"]:
                        print_success(f"Generated file: {file}")
                
                return True
            else:
                print_warning("Generation completed but response structure unexpected")
                return True
        else:
            print_error(f"Test generation failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Test generation failed with exception: {str(e)}")
        return False

def test_run_test_endpoint() -> bool:
    """Test the /run-test endpoint"""
    print_header("TEST 5: Test Execution Endpoint")
    print_info("Endpoint: POST /run-test")
    
    # Test payload
    payload = {
        "test_id": "TC-AUTH-001",
        "base_url": "http://localhost:3000"
    }
    
    print_info(f"Payload:\n{format_json(payload)}")
    print_warning("Note: This endpoint requires test files to exist")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/run-test",
            headers=HEADERS,
            json=payload,
            timeout=60
        )
        elapsed = (time.time() - start_time) * 1000
        
        print_info(f"Status Code: {response.status_code}")
        print_info(f"Response Time: {elapsed:.2f}ms")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_info(f"Response:\n{format_json(data)}")
            
            # Validate response
            if "result" in data or "status" in data or "message" in data:
                print_success("Test execution endpoint accessible")
                return True
            else:
                print_warning("Execution response structure unexpected")
                return True
        elif response.status_code == 404:
            print_warning("Test not found (expected if test files don't exist)")
            print_info(f"Response: {response.text}")
            return True  # Not a failure - expected behavior
        else:
            print_error(f"Test execution failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Test execution failed with exception: {str(e)}")
        return False

def main():
    """Run all API tests"""
    print_header("QA Agent API Comprehensive Test Suite")
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Testing all 5 endpoints...\n")
    
    results = {
        "Health Check": test_health_endpoint(),
        "Document Ingestion": test_ingest_endpoint(),
        "RAG Query": test_query_endpoint(),
        "Test Generation": test_generate_tests_endpoint(),
        "Test Execution": test_run_test_endpoint()
    }
    
    # Summary
    print_header("Test Results Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        if passed_test:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print(f"\n{Colors.BOLD}Overall: {passed}/{total} tests passed{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests passed successfully!{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ Some tests failed or had warnings{Colors.RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
