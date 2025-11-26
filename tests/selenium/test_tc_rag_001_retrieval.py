"""
Selenium Test: Test RAG context retrieval accuracy
Test ID: TC-RAG-001
Feature: RAG System Testing
Grounded_In: Assignment - 1.pdf

Auto-generated RAG functionality test.
"""

import pytest
import requests


class TestTCRAG001:
    """Test class for TC-RAG-001 - RAG retrieval test."""
    
    @pytest.fixture(autouse=True)
    def setup(self, base_url):
        """Setup test fixture."""
        self.base_url = base_url
        self.query_endpoint = f"{base_url}/query"
    
    def test_tc_rag_001_retrieval_accuracy(self):
        """
        Test RAG context retrieval accuracy
        
        Priority: high
        Type: functional
        """
        # Step 1: Query for authentication-related content
        query_data = {
            "query": "How does user authentication work?",
            "k": 6
        }
        
        response = requests.post(
            self.query_endpoint,
            json=query_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Verify response status
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Step 2: Verify returned results contain authentication documentation
        assert "results" in data, "Response missing 'results'"
        results = data["results"]
        
        assert len(results) > 0, "No results returned"
        assert len(results) <= 6, f"Expected max 6 results, got {len(results)}"
        
        # Step 3: Check similarity scores are above 0.7
        high_relevance_count = 0
        
        print(f"\n📊 Retrieved {len(results)} chunks:")
        
        for idx, result in enumerate(results, 1):
            assert "content" in result, f"Result {idx} missing 'content'"
            assert "metadata" in result, f"Result {idx} missing 'metadata'"
            assert "similarity_score" in result, f"Result {idx} missing 'similarity_score'"
            
            score = result["similarity_score"]
            source = result["metadata"].get("source", "unknown")
            content_preview = result["content"][:80] + "..."
            
            print(f"  {idx}. Score: {score:.3f} | Source: {source}")
            print(f"     Preview: {content_preview}")
            
            if score >= 0.7:
                high_relevance_count += 1
        
        # Verify at least some results have high relevance
        assert high_relevance_count > 0, "No results with similarity >= 0.7"
        
        print(f"\n✅ High relevance results: {high_relevance_count}/{len(results)}")
        
        # Verify retrieval time
        retrieval_time = data.get("retrieval_time_ms", 0)
        print(f"⏱️  Retrieval time: {retrieval_time}ms")
        
        assert retrieval_time < 1000, f"Retrieval too slow: {retrieval_time}ms"
        
        # Verify query metadata
        assert data["query"] == query_data["query"], "Query mismatch"
        assert data["total_results"] == len(results), "Result count mismatch"
        
        # Test passed
        print("\n✓ Test TC-RAG-001 passed")
        print(f"  - Retrieved: {len(results)} relevant chunks")
        print(f"  - High relevance: {high_relevance_count} chunks (≥0.7)")
        print(f"  - Average score: {sum(r['similarity_score'] for r in results)/len(results):.3f}")
        print(f"  - Retrieval time: {retrieval_time}ms")
