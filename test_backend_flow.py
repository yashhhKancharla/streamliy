import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def print_step(step):
    print(f"\n{'='*50}")
    print(f"STEP: {step}")
    print(f"{'='*50}")

def check_health():
    print_step("Checking Health")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code != 200:
            print("Health check failed!")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def ingest_document():
    print_step("Ingesting Document")
    doc_content = """
    # User Authentication System
    
    ## Login Feature
    The login feature allows users to access their accounts.
    
    ### Requirements
    1. User must provide a valid email address.
    2. User must provide a password.
    3. Password must be at least 8 characters long.
    4. If credentials are valid, user is redirected to dashboard.
    5. If credentials are invalid, an error message is shown.
    6. Account is locked after 3 failed attempts.
    """
    
    payload = {
        "documents": [{
            "content": doc_content,
            "metadata": {
                "source": "test_specs.md",
                "category": "specs"
            }
        }],
        "chunk_size": 500,
        "chunk_overlap": 50
    }
    
    response = requests.post(f"{BASE_URL}/ingest", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def query_rag():
    print_step("Querying RAG")
    payload = {
        "query": "What are the login requirements?",
        "k": 2,
        "generate_answer": True
    }
    
    response = requests.post(f"{BASE_URL}/query", json=payload)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Answer: {result.get('answer')}")
    return response.status_code == 200

def generate_tests():
    print_step("Generating Tests")
    payload = {
        "feature": "User Login",
        "requirements": "User must provide email and password. Password must be 8 chars. Lockout after 3 failed attempts.",
        "test_types": ["functional", "security"],
        "priority_levels": ["high"],
        "output_formats": ["json", "selenium"]
    }
    
    response = requests.post(f"{BASE_URL}/generate-tests", json=payload)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    
    test_cases = result.get("test_cases", [])
    print(f"Generated {len(test_cases)} test cases.")
    
    if test_cases:
        print(f"First Test Case ID: {test_cases[0].get('id')}")
        return test_cases[0].get('id')
    return None

def run_test(test_id):
    print_step(f"Running Test: {test_id}")
    # Note: This might fail if the generated selenium test requires a real browser/app running on localhost:3000
    # But we want to see if the backend handles the request.
    
    payload = {
        "test_id": test_id,
        "base_url": "http://example.com", # Dummy URL
        "headless": True,
        "timeout": 10
    }
    
    response = requests.post(f"{BASE_URL}/run-test", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def main():
    check_health()
    
    if ingest_document():
        if query_rag():
            test_id = generate_tests()
            if test_id:
                # We won't necessarily expect run_test to pass functionally (since we don't have the target app),
                # but the API call should succeed.
                run_test(test_id)
            else:
                print("No tests generated.")
        else:
            print("Query failed.")
    else:
        print("Ingest failed.")

if __name__ == "__main__":
    main()
