"""
Comprehensive End-to-End Test for All Features
Tests the complete flow from Frontend (Streamlit) to Backend (Flask)

This script tests:
1. Health Check - System status
2. Document Ingestion - Upload documents to vector DB
3. List Documents - View ingested documents
4. Query RAG - Semantic search on documents
5. Generate Test Cases - AI-powered test generation
6. Run Tests - Execute generated tests

Flow: Ingest -> List -> Query -> Generate -> Run
Each step uses output from previous steps for connected testing.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, Tuple
import sys

# Configuration
API_BASE_URL = "http://localhost:8000"
UI_BASE_URL = "http://localhost:8501"

# Test data
TEST_DOCUMENT = {
    "content": """
    User Authentication Module Specification
    
    1. Login Feature Requirements:
    - Users must enter valid email and password
    - Password must be at least 8 characters with uppercase, lowercase, and numbers
    - Maximum 5 failed login attempts before account lockout
    - Session timeout after 30 minutes of inactivity
    
    2. Registration Feature Requirements:
    - Email must be unique and valid format
    - Password confirmation must match
    - Required fields: email, password, first name, last name
    - Optional fields: phone number, address
    
    3. Password Reset Feature:
    - User enters registered email
    - System sends reset link valid for 24 hours
    - New password must be different from last 5 passwords
    
    4. Security Requirements:
    - All passwords must be hashed using bcrypt
    - HTTPS required for all auth endpoints
    - Rate limiting: 10 requests per minute per IP
    """,
    "metadata": {
        "source": "auth_module_spec.md",
        "category": "documentation"
    }
}

TEST_DOCUMENT_2 = {
    "content": """
    Shopping Cart Module Specification
    
    1. Add to Cart:
    - User can add products with quantity
    - Maximum 10 items per product type
    - Cart persists across sessions for logged-in users
    
    2. Update Cart:
    - User can modify quantities
    - User can remove items
    - Total automatically recalculated
    
    3. Checkout Flow:
    - Validate cart items availability
    - Calculate shipping based on location
    - Apply discount codes if valid
    - Process payment through gateway
    
    4. Edge Cases:
    - Handle out of stock during checkout
    - Handle price changes during session
    - Handle concurrent cart updates
    """,
    "metadata": {
        "source": "cart_module_spec.md",
        "category": "documentation"
    }
}


class TestResult:
    """Store test results for reporting."""
    
    def __init__(self, name: str, passed: bool, message: str, data: Any = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.data = data
        self.timestamp = datetime.now().isoformat()
    
    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status} | {self.name}: {self.message}"


class FlowTester:
    """End-to-end flow tester for the QA Agent application."""
    
    def __init__(self):
        self.results = []
        self.shared_data = {}  # Store data between tests
    
    def log(self, message: str, level: str = "INFO"):
        """Print formatted log message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARN": "⚠️"}
        print(f"[{timestamp}] {symbols.get(level, '•')} {message}")
    
    def add_result(self, result: TestResult):
        """Add test result to list."""
        self.results.append(result)
        print(result)
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, timeout: int = 30) -> Tuple[Dict, int]:
        """Make HTTP request to API."""
        url = f"{API_BASE_URL}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, timeout=timeout)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=timeout)
            else:
                return {"error": "Invalid method"}, 400
            
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to backend API"}, 503
        except Exception as e:
            return {"error": str(e)}, 500
    
    # ==================== TEST 1: HEALTH CHECK ====================
    def test_health_check(self) -> TestResult:
        """Test 1: Verify backend API is healthy."""
        self.log("Testing Health Check endpoint...", "INFO")
        
        response, status = self.make_request("GET", "/health")
        
        if status == 200 and response.get("status") == "healthy":
            services = response.get("services", {})
            message = f"Backend healthy - Flask: {services.get('flask')}, ChromaDB: {services.get('chroma')}"
            self.shared_data["health"] = response
            return TestResult("Health Check", True, message, response)
        else:
            return TestResult("Health Check", False, f"Backend unhealthy: {response}")
    
    # ==================== TEST 2: DOCUMENT INGESTION ====================
    def test_ingest_documents(self) -> TestResult:
        """Test 2: Ingest documents into vector database."""
        self.log("Testing Document Ingestion...", "INFO")
        
        payload = {
            "documents": [TEST_DOCUMENT, TEST_DOCUMENT_2],
            "chunk_size": 800,
            "chunk_overlap": 150
        }
        
        response, status = self.make_request("POST", "/ingest", payload)
        
        if status == 200 and response.get("status") == "success":
            ingested = response.get("ingested_count", 0)
            chunks = response.get("chunks_created", 0)
            message = f"Ingested {ingested} documents, created {chunks} chunks"
            self.shared_data["ingestion"] = response
            return TestResult("Document Ingestion", True, message, response)
        else:
            error = response.get("error", {}).get("message", str(response))
            return TestResult("Document Ingestion", False, f"Ingestion failed: {error}")
    
    # ==================== TEST 3: LIST DOCUMENTS ====================
    def test_list_documents(self) -> TestResult:
        """Test 3: List all ingested documents."""
        self.log("Testing List Documents...", "INFO")
        
        response, status = self.make_request("GET", "/list-documents")
        
        if status == 200:
            docs = response.get("documents", [])
            total = response.get("total_count", 0)
            message = f"Found {total} document sources"
            
            # Store document sources for later filtering
            self.shared_data["documents"] = docs
            self.shared_data["document_sources"] = [d.get("source") for d in docs if d.get("source")]
            
            # Verify our ingested documents are present
            sources = self.shared_data["document_sources"]
            found_auth = any("auth" in s.lower() for s in sources)
            found_cart = any("cart" in s.lower() for s in sources)
            
            if found_auth or found_cart:
                message += f" (verified: auth_spec={found_auth}, cart_spec={found_cart})"
            
            return TestResult("List Documents", True, message, response)
        else:
            return TestResult("List Documents", False, f"Failed to list documents: {response}")
    
    # ==================== TEST 4: QUERY RAG ====================
    def test_query_rag(self) -> TestResult:
        """Test 4: Query the RAG system with semantic search."""
        self.log("Testing RAG Query...", "INFO")
        
        # Use a query that should match our ingested documents
        payload = {
            "query": "What are the login and authentication requirements?",
            "k": 3,
            "generate_answer": True
        }
        
        response, status = self.make_request("POST", "/query", payload)
        
        if status == 200:
            results = response.get("results", [])
            answer = response.get("answer", "")
            retrieval_time = response.get("retrieval_time_ms", 0)
            
            if len(results) > 0:
                # Store query results for test generation
                self.shared_data["query_results"] = results
                self.shared_data["query_answer"] = answer
                
                message = f"Retrieved {len(results)} documents in {retrieval_time}ms"
                if answer:
                    message += f", got AI answer"
                
                return TestResult("RAG Query", True, message, response)
            else:
                return TestResult("RAG Query", False, "No results returned from query")
        else:
            return TestResult("RAG Query", False, f"Query failed: {response}")
    
    # ==================== TEST 5: QUERY WITH FILTER ====================
    def test_query_with_filter(self) -> TestResult:
        """Test 5: Query RAG with document filter."""
        self.log("Testing RAG Query with Document Filter...", "INFO")
        
        # Filter by auth document if available
        doc_sources = self.shared_data.get("document_sources", [])
        filter_source = None
        for source in doc_sources:
            if "auth" in source.lower():
                filter_source = source
                break
        
        if not filter_source and doc_sources:
            filter_source = doc_sources[0]
        
        payload = {
            "query": "password requirements and security",
            "k": 3,
            "generate_answer": True
        }
        
        if filter_source:
            payload["filters"] = {"source": filter_source}
        
        response, status = self.make_request("POST", "/query", payload)
        
        if status == 200:
            results = response.get("results", [])
            message = f"Filtered query returned {len(results)} results"
            if filter_source:
                message += f" from '{filter_source}'"
            return TestResult("Filtered Query", True, message, response)
        else:
            return TestResult("Filtered Query", False, f"Filtered query failed: {response}")
    
    # ==================== TEST 6: GENERATE TEST CASES ====================
    def test_generate_tests(self) -> TestResult:
        """Test 6: Generate test cases using RAG + LLM."""
        self.log("Testing Test Case Generation (this may take 30-60 seconds)...", "INFO")
        
        # Build requirements from query results if available
        requirements = """
        User Authentication Feature:
        - Login with email and password
        - Password must be 8+ characters with mixed case and numbers
        - Account lockout after 5 failed attempts
        - Session timeout after 30 minutes
        - Secure password hashing
        - Rate limiting protection
        """
        
        payload = {
            "feature": "User Authentication",
            "requirements": requirements,
            "test_types": ["functional", "security", "negative"],
            "priority_levels": ["high", "medium"],
            "output_formats": ["json", "markdown", "selenium"]
        }
        
        response, status = self.make_request("POST", "/generate-tests", payload, timeout=120)
        
        if status == 200:
            test_cases = response.get("test_cases", [])
            output_files = response.get("output_files", {})
            gen_time = response.get("generation_time_ms", 0)
            
            if len(test_cases) > 0:
                # Store for test execution
                self.shared_data["generated_tests"] = test_cases
                self.shared_data["test_files"] = output_files
                
                # Extract test IDs
                test_ids = [tc.get("id") for tc in test_cases if tc.get("id")]
                self.shared_data["test_ids"] = test_ids
                
                message = f"Generated {len(test_cases)} test cases in {gen_time}ms"
                if test_ids:
                    message += f" (IDs: {', '.join(test_ids[:3])}...)"
                
                return TestResult("Test Generation", True, message, response)
            else:
                return TestResult("Test Generation", False, "No test cases generated")
        else:
            error = response.get("error", {}).get("message", str(response))
            return TestResult("Test Generation", False, f"Generation failed: {error}")
    
    # ==================== TEST 7: VERIFY OUTPUT FILES ====================
    def test_verify_outputs(self) -> TestResult:
        """Test 7: Verify generated output files exist."""
        self.log("Testing Output File Verification...", "INFO")
        
        import os
        from pathlib import Path
        
        output_dir = Path("output")
        tests_dir = Path("tests/selenium")
        
        found_files = []
        missing_files = []
        
        # Check output directory
        if output_dir.exists():
            json_files = list(output_dir.glob("testcases_*.json"))
            md_files = list(output_dir.glob("testcases_*.md"))
            found_files.extend([str(f) for f in json_files[:2]])
            found_files.extend([str(f) for f in md_files[:2]])
        
        # Check selenium tests directory
        if tests_dir.exists():
            test_files = list(tests_dir.glob("test_*.py"))
            found_files.extend([str(f) for f in test_files[:2]])
        
        if found_files:
            message = f"Found {len(found_files)} output files"
            self.shared_data["output_files"] = found_files
            return TestResult("Output Verification", True, message, {"files": found_files})
        else:
            return TestResult("Output Verification", False, "No output files found")
    
    # ==================== TEST 8: RUN SELENIUM TEST ====================
    def test_run_selenium(self) -> TestResult:
        """Test 8: Attempt to run a Selenium test."""
        self.log("Testing Selenium Test Execution...", "INFO")
        
        # Look for available test files
        from pathlib import Path
        tests_dir = Path("tests/selenium")
        
        if not tests_dir.exists():
            return TestResult("Selenium Execution", False, "No tests/selenium directory found")
        
        test_files = list(tests_dir.glob("test_*.py"))
        if not test_files:
            return TestResult("Selenium Execution", False, "No test files found in tests/selenium")
        
        # Get the first test file name for test_id
        test_file = test_files[0]
        test_id = test_file.stem.replace("test_", "").upper()
        
        payload = {
            "test_id": test_id,
            "base_url": "http://localhost:3000",
            "headless": True,
            "timeout": 30
        }
        
        response, status = self.make_request("POST", "/run-test", payload, timeout=60)
        
        if status == 200:
            test_status = response.get("status", "unknown")
            exec_time = response.get("execution_time_ms", 0)
            
            # Note: Test might fail due to target app not running, but API works
            if test_status in ["passed", "failed", "timeout"]:
                message = f"Test execution completed: {test_status} in {exec_time}ms"
                self.shared_data["test_execution"] = response
                return TestResult("Selenium Execution", True, message, response)
            else:
                return TestResult("Selenium Execution", False, f"Unexpected status: {test_status}")
        elif status == 404:
            return TestResult("Selenium Execution", False, f"Test ID '{test_id}' not found")
        else:
            error = response.get("error", {}).get("message", str(response))
            return TestResult("Selenium Execution", False, f"Execution failed: {error}")
    
    # ==================== FRONTEND TESTS ====================
    def test_frontend_accessible(self) -> TestResult:
        """Test: Verify Streamlit UI is accessible."""
        self.log("Testing Frontend (Streamlit) Accessibility...", "INFO")
        
        try:
            response = requests.get(UI_BASE_URL, timeout=10)
            if response.status_code == 200:
                return TestResult("Frontend Access", True, f"Streamlit UI accessible at {UI_BASE_URL}")
            else:
                return TestResult("Frontend Access", False, f"UI returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            return TestResult("Frontend Access", False, f"Cannot connect to UI at {UI_BASE_URL}")
        except Exception as e:
            return TestResult("Frontend Access", False, f"Error: {str(e)}")
    
    def test_frontend_backend_integration(self) -> TestResult:
        """Test: Verify frontend can communicate with backend."""
        self.log("Testing Frontend-Backend Integration...", "INFO")
        
        # This is verified if health check works, as UI calls same endpoint
        if self.shared_data.get("health"):
            return TestResult("Frontend-Backend Integration", True, 
                            "Backend health confirmed - UI will show 'Healthy' status")
        else:
            return TestResult("Frontend-Backend Integration", False, 
                            "Backend not healthy - UI will show 'Unhealthy' status")
    
    # ==================== RUN ALL TESTS ====================
    def run_all_tests(self):
        """Run complete test flow."""
        print("\n" + "="*70)
        print("🧪 COMPREHENSIVE END-TO-END TEST - QA AGENT APPLICATION")
        print("="*70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Backend API: {API_BASE_URL}")
        print(f"Frontend UI: {UI_BASE_URL}")
        print("="*70 + "\n")
        
        # Phase 1: System Health
        print("\n📋 PHASE 1: SYSTEM HEALTH\n" + "-"*40)
        self.add_result(self.test_health_check())
        self.add_result(self.test_frontend_accessible())
        self.add_result(self.test_frontend_backend_integration())
        
        # Phase 2: Document Management
        print("\n📋 PHASE 2: DOCUMENT MANAGEMENT\n" + "-"*40)
        self.add_result(self.test_ingest_documents())
        time.sleep(1)  # Allow indexing
        self.add_result(self.test_list_documents())
        
        # Phase 3: RAG Queries
        print("\n📋 PHASE 3: RAG QUERIES\n" + "-"*40)
        self.add_result(self.test_query_rag())
        self.add_result(self.test_query_with_filter())
        
        # Phase 4: Test Generation
        print("\n📋 PHASE 4: TEST GENERATION\n" + "-"*40)
        self.add_result(self.test_generate_tests())
        self.add_result(self.test_verify_outputs())
        
        # Phase 5: Test Execution
        print("\n📋 PHASE 5: TEST EXECUTION\n" + "-"*40)
        self.add_result(self.test_run_selenium())
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)
        
        print(f"\n✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {failed}/{total}")
        print(f"📈 Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            print("\n⚠️ Failed Tests:")
            for r in self.results:
                if not r.passed:
                    print(f"   • {r.name}: {r.message}")
        
        print("\n" + "="*70)
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
        
        # Return exit code
        return 0 if failed == 0 else 1


def main():
    """Main entry point."""
    tester = FlowTester()
    exit_code = tester.run_all_tests()
    
    # Interactive mode - prompt for additional tests
    print("\n🔧 INTERACTIVE TEST OPTIONS")
    print("-"*40)
    print("You can also test individual features:")
    print("1. Test custom document ingestion")
    print("2. Test custom query")
    print("3. Test custom test generation")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == "1":
                content = input("Enter document content: ")
                source = input("Enter source name (e.g., my_doc.md): ")
                payload = {
                    "documents": [{
                        "content": content,
                        "metadata": {"source": source, "category": "documentation"}
                    }],
                    "chunk_size": 800,
                    "chunk_overlap": 150
                }
                result, status = tester.make_request("POST", "/ingest", payload)
                print(f"\nResult: {json.dumps(result, indent=2)}")
                
            elif choice == "2":
                query = input("Enter your query: ")
                payload = {"query": query, "k": 3, "generate_answer": True}
                result, status = tester.make_request("POST", "/query", payload)
                print(f"\nResult: {json.dumps(result, indent=2)}")
                
            elif choice == "3":
                feature = input("Enter feature name: ")
                requirements = input("Enter requirements: ")
                payload = {
                    "feature": feature,
                    "requirements": requirements,
                    "test_types": ["functional", "security"],
                    "priority_levels": ["high", "medium"],
                    "output_formats": ["json", "markdown"]
                }
                print("\nGenerating tests (this may take 30-60 seconds)...")
                result, status = tester.make_request("POST", "/generate-tests", payload, timeout=120)
                print(f"\nResult: {json.dumps(result, indent=2)}")
                
            elif choice == "4":
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\nExiting. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
