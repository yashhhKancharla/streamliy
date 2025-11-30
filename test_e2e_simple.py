"""
Simple End-to-End Test for QA Agent Application
Tests all features with proper error handling
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

API = "http://localhost:8000"
UI = "http://localhost:8501"

def log(msg, status="INFO"):
    symbols = {"PASS": "[+]", "FAIL": "[-]", "INFO": "[*]", "WARN": "[!]"}
    print(f"{symbols.get(status, '[*]')} {msg}")

def test_health():
    """Test 1: Health Check"""
    try:
        r = requests.get(f"{API}/health", timeout=5)
        if r.status_code == 200 and r.json().get("status") == "healthy":
            services = r.json().get("services", {})
            log(f"Health Check: Backend healthy - Flask: {services.get('flask')}, ChromaDB: {services.get('chroma')}", "PASS")
            return True
        else:
            log(f"Health Check: Unhealthy - {r.json()}", "FAIL")
            return False
    except Exception as e:
        log(f"Health Check: Failed - {e}", "FAIL")
        return False

def test_frontend():
    """Test 2: Frontend Accessibility"""
    try:
        r = requests.get(UI, timeout=10)
        if r.status_code == 200:
            log("Frontend: Streamlit UI accessible", "PASS")
            return True
        else:
            log(f"Frontend: Status {r.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"Frontend: {e}", "FAIL")
        return False

def test_ingest():
    """Test 3: Document Ingestion"""
    try:
        payload = {
            "documents": [
                {
                    "content": """User Authentication System
                    - Login with email/password
                    - Password: 8+ chars, mixed case, numbers
                    - Account lockout after 5 failures
                    - Session timeout: 30 minutes
                    """,
                    "metadata": {"source": "e2e_auth_test.md", "category": "documentation"}
                },
                {
                    "content": """Shopping Cart Module
                    - Add/remove items
                    - Update quantities
                    - Persist cart for logged-in users
                    - Checkout with payment processing
                    """,
                    "metadata": {"source": "e2e_cart_test.md", "category": "documentation"}
                }
            ],
            "chunk_size": 800,
            "chunk_overlap": 150
        }
        r = requests.post(f"{API}/ingest", json=payload, timeout=30)
        if r.status_code == 200:
            resp = r.json()
            log(f"Ingest: Ingested {resp.get('ingested_count', 0)} docs, {resp.get('chunks_created', 0)} chunks", "PASS")
            return True
        else:
            log(f"Ingest: {r.json()}", "FAIL")
            return False
    except Exception as e:
        log(f"Ingest: {e}", "FAIL")
        return False

def test_list_documents():
    """Test 4: List Documents"""
    try:
        r = requests.get(f"{API}/list-documents", timeout=10)
        if r.status_code == 200:
            resp = r.json()
            count = resp.get("total_count", 0)
            log(f"List Documents: Found {count} document sources", "PASS")
            return True, resp.get("documents", [])
        else:
            log(f"List Documents: {r.json()}", "FAIL")
            return False, []
    except Exception as e:
        log(f"List Documents: {e}", "FAIL")
        return False, []

def test_query():
    """Test 5: RAG Query"""
    try:
        payload = {
            "query": "What are the login and authentication requirements?",
            "k": 3,
            "generate_answer": True
        }
        r = requests.post(f"{API}/query", json=payload, timeout=30)
        if r.status_code == 200:
            resp = r.json()
            log(f"Query: Retrieved {resp.get('total_results', 0)} results in {resp.get('retrieval_time_ms', 0)}ms", "PASS")
            return True, resp
        else:
            log(f"Query: {r.json()}", "FAIL")
            return False, None
    except Exception as e:
        log(f"Query: {e}", "FAIL")
        return False, None

def test_filtered_query(source=None):
    """Test 6: Filtered RAG Query"""
    try:
        payload = {
            "query": "shopping cart checkout",
            "k": 2,
            "generate_answer": True
        }
        if source:
            payload["filters"] = {"source": source}
        
        r = requests.post(f"{API}/query", json=payload, timeout=30)
        if r.status_code == 200:
            resp = r.json()
            log(f"Filtered Query: {resp.get('total_results', 0)} results (filtered by: {source or 'none'})", "PASS")
            return True
        else:
            log(f"Filtered Query: {r.json()}", "FAIL")
            return False
    except Exception as e:
        log(f"Filtered Query: {e}", "FAIL")
        return False

def test_generate():
    """Test 7: Test Case Generation"""
    try:
        log("Generating test cases (this may take 30-60 seconds)...", "INFO")
        payload = {
            "feature": "E2E User Authentication",
            "requirements": "User login with email/password. Password 8+ chars. Account lockout after 5 failures.",
            "test_types": ["functional", "security"],
            "priority_levels": ["high", "medium"],
            "output_formats": ["json", "markdown"]
        }
        r = requests.post(f"{API}/generate-tests", json=payload, timeout=120)
        if r.status_code == 200:
            resp = r.json()
            tc_count = len(resp.get("test_cases", []))
            gen_time = resp.get("generation_time_ms", 0)
            log(f"Generate Tests: Created {tc_count} test cases in {gen_time}ms", "PASS")
            return True, resp.get("test_cases", [])
        else:
            log(f"Generate Tests: {r.json()}", "FAIL")
            return False, []
    except Exception as e:
        log(f"Generate Tests: {e}", "FAIL")
        return False, []

def test_run_selenium():
    """Test 8: Run Selenium Test"""
    try:
        # Check if test files exist
        test_dir = Path("tests/selenium")
        if not test_dir.exists():
            log("Run Test: No tests/selenium directory (skipping)", "WARN")
            return True
        
        test_files = list(test_dir.glob("test_*.py"))
        if not test_files:
            log("Run Test: No test files found (skipping)", "WARN")
            return True
        
        payload = {
            "test_id": "TC-001",
            "base_url": "http://localhost:3000",
            "headless": True,
            "timeout": 30
        }
        r = requests.post(f"{API}/run-test", json=payload, timeout=60)
        if r.status_code == 200:
            resp = r.json()
            status = resp.get("status", "unknown")
            exec_time = resp.get("execution_time_ms", 0)
            log(f"Run Test: {status.upper()} in {exec_time}ms", "PASS")
            return True
        elif r.status_code == 404:
            log("Run Test: Test not found (API works, but no matching test)", "WARN")
            return True
        else:
            log(f"Run Test: {r.json()}", "FAIL")
            return False
    except Exception as e:
        log(f"Run Test: {e}", "FAIL")
        return False

def main():
    print("=" * 60)
    print("COMPREHENSIVE END-TO-END TEST - QA AGENT APPLICATION")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Backend API: {API}")
    print(f"Frontend UI: {UI}")
    print("=" * 60)
    print()
    
    results = []
    
    # Phase 1: System Health
    print("PHASE 1: SYSTEM HEALTH")
    print("-" * 40)
    results.append(("Health Check", test_health()))
    results.append(("Frontend Access", test_frontend()))
    
    # Phase 2: Document Management
    print()
    print("PHASE 2: DOCUMENT MANAGEMENT")
    print("-" * 40)
    results.append(("Document Ingestion", test_ingest()))
    time.sleep(1)
    passed, docs = test_list_documents()
    results.append(("List Documents", passed))
    
    # Get a source for filtering
    filter_source = None
    for doc in docs:
        if "e2e" in doc.get("source", "").lower():
            filter_source = doc.get("source")
            break
    
    # Phase 3: RAG Queries
    print()
    print("PHASE 3: RAG QUERIES")
    print("-" * 40)
    passed, query_result = test_query()
    results.append(("RAG Query", passed))
    results.append(("Filtered Query", test_filtered_query(filter_source)))
    
    # Phase 4: Test Generation
    print()
    print("PHASE 4: TEST GENERATION")
    print("-" * 40)
    passed, test_cases = test_generate()
    results.append(("Test Generation", passed))
    
    # Phase 5: Test Execution
    print()
    print("PHASE 5: TEST EXECUTION")
    print("-" * 40)
    results.append(("Selenium Test", test_run_selenium()))
    
    # Summary
    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed_count = sum(1 for _, p in results if p)
    failed_count = sum(1 for _, p in results if not p)
    total = len(results)
    
    print(f"Passed: {passed_count}/{total}")
    print(f"Failed: {failed_count}/{total}")
    print(f"Success Rate: {(passed_count/total)*100:.1f}%")
    
    if failed_count > 0:
        print()
        print("Failed Tests:")
        for name, p in results:
            if not p:
                print(f"  - {name}")
    
    print()
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    exit(main())
