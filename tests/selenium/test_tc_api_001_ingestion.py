"""
Selenium Test: Test document ingestion via API
Test ID: TC-API-001
Feature: API Testing
Grounded_In: Assignment - 1.pdf

Auto-generated API test using requests library.
"""

import pytest
import requests
import json


class TestTCAPI001:
    """Test class for TC-API-001 - API ingestion test."""
    
    @pytest.fixture(autouse=True)
    def setup(self, base_url):
        """Setup test fixture."""
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/ingest"
    
    def test_tc_api_001_document_ingestion(self):
        """
        Test document ingestion via API
        
        Priority: high
        Type: functional
        """
        # Step 1: Prepare test document
        test_document = {
            "documents": [
                {
                    "content": "This is a test document for ingestion. It contains sample authentication requirements.",
                    "metadata": {
                        "source": "test_doc.md",
                        "doc_type": "test",
                        "test_id": "TC-API-001"
                    }
                }
            ],
            "chunk_size": 800,
            "chunk_overlap": 150
        }
        
        # Step 2: Send POST request to /ingest endpoint
        response = requests.post(
            self.api_endpoint,
            json=test_document,
            headers={"Content-Type": "application/json"}
        )
        
        # Step 3: Verify response status is 200
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Step 4: Verify response contains ingestion statistics
        data = response.json()
        
        assert "status" in data, "Response missing 'status' field"
        assert data["status"] == "success", "Ingestion status not success"
        
        assert "ingested_count" in data, "Response missing 'ingested_count'"
        assert data["ingested_count"] > 0, "No documents ingested"
        
        assert "chunks_created" in data, "Response missing 'chunks_created'"
        assert data["chunks_created"] > 0, "No chunks created"
        
        # Step 5: Query for ingested content
        query_endpoint = f"{self.base_url}/query"
        query_data = {
            "query": "authentication requirements",
            "k": 3
        }
        
        query_response = requests.post(
            query_endpoint,
            json=query_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert query_response.status_code == 200, "Query failed"
        query_result = query_response.json()
        
        assert "results" in query_result, "Query response missing results"
        assert len(query_result["results"]) > 0, "No results returned from query"
        
        # Test passed
        print("✓ Test TC-API-001 passed")
        print(f"  - Ingested: {data['ingested_count']} documents")
        print(f"  - Created: {data['chunks_created']} chunks")
        print(f"  - Query returned: {len(query_result['results'])} results")
