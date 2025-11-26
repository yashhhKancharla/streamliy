"""
ChromaDB Vector Store Service
Grounded_In: Assignment - 1.pdf

This module provides RAG capabilities using ChromaDB for:
- Document ingestion and chunking
- Vector storage and persistence
- Semantic similarity search
- Context retrieval for test generation
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
import structlog

from app.utils.openrouter_client import OpenRouterClient

logger = structlog.get_logger()


class ChromaService:
    """Service for ChromaDB vector operations."""
    
    def __init__(
        self,
        persist_directory: Optional[str] = None,
        collection_name: Optional[str] = None
    ):
        """
        Initialize ChromaDB service.
        
        Args:
            persist_directory: Directory for persistent storage
            collection_name: Name of the collection to use
        """
        self.persist_directory = persist_directory or os.getenv(
            "CHROMA_PERSIST_DIR",
            "/data/chroma"
        )
        self.collection_name = collection_name or os.getenv(
            "CHROMA_COLLECTION",
            "assignment_index"
        )
        
        # Create directory if it doesn't exist
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client with new API
        self.client = chromadb.PersistentClient(
            path=self.persist_directory
        )
        
        # Initialize OpenRouter client for embeddings
        self.openrouter_client = OpenRouterClient()
        
        # Get or create collection
        self.collection = self._get_or_create_collection()
        
        logger.info(
            "chroma_service_initialized",
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
    
    def _get_or_create_collection(self):
        """Get existing collection or create new one."""
        try:
            collection = self.client.get_collection(
                name=self.collection_name
            )
            logger.info(
                "collection_retrieved",
                name=self.collection_name,
                count=collection.count()
            )
        except Exception:
            collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "RAG index for test generation"}
            )
            logger.info("collection_created", name=self.collection_name)
        
        return collection
    
    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 800,
        chunk_overlap: int = 150
    ) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Input text to chunk
            chunk_size: Maximum tokens per chunk
            chunk_overlap: Overlap between chunks (tokens)
            
        Returns:
            List of text chunks
        """
        # Simple word-based chunking (approximates tokens)
        words = text.split()
        chunks = []
        
        i = 0
        while i < len(words):
            chunk_words = words[i:i + chunk_size]
            chunk = " ".join(chunk_words)
            chunks.append(chunk)
            i += chunk_size - chunk_overlap
        
        logger.debug(
            "text_chunked",
            original_words=len(words),
            chunks_created=len(chunks),
            chunk_size=chunk_size
        )
        
        return chunks
    
    def ingest_documents(
        self,
        documents: List[Dict[str, Any]],
        chunk_size: int = 800,
        chunk_overlap: int = 150
    ) -> Dict[str, Any]:
        """
        Ingest documents into vector store.
        
        Args:
            documents: List of dicts with 'content' and 'metadata' keys
            chunk_size: Tokens per chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            Ingestion statistics
            
        Example:
            documents = [
                {
                    "content": "API documentation...",
                    "metadata": {"source": "api_docs.md", "version": "1.0"}
                }
            ]
        """
        import time
        start_time = time.time()
        
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        chunk_counter = 0
        
        for doc_idx, doc in enumerate(documents):
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            
            # Chunk the document
            chunks = self._chunk_text(content, chunk_size, chunk_overlap)
            
            for chunk_idx, chunk in enumerate(chunks):
                chunk_id = f"doc_{doc_idx}_chunk_{chunk_idx}_{int(time.time() * 1000)}"
                
                chunk_metadata = {
                    **metadata,
                    "chunk_id": chunk_id,
                    "doc_index": doc_idx,
                    "chunk_index": chunk_idx,
                    "chunk_count": len(chunks)
                }
                
                all_chunks.append(chunk)
                all_metadatas.append(chunk_metadata)
                all_ids.append(chunk_id)
                chunk_counter += 1
        
        # Generate embeddings
        logger.info("generating_embeddings", count=len(all_chunks))
        embeddings = self.openrouter_client.embed(all_chunks)
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )
        
        end_time = time.time()
        
        result = {
            "status": "success",
            "ingested_count": len(documents),
            "chunks_created": chunk_counter,
            "collection": self.collection_name,
            "processing_time_ms": int((end_time - start_time) * 1000)
        }
        
        logger.info(
            "documents_ingested",
            **result
        )
        
        return result
    
    def query(
        self,
        query_text: str,
        k: int = 6,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query vector store for similar documents.
        
        Args:
            query_text: Query string
            k: Number of results to return
            filters: Metadata filters (e.g., {"source": "api_docs.md"})
            
        Returns:
            Query results with documents, metadata, and similarity scores
        """
        import time
        start_time = time.time()
        
        # Generate query embedding
        query_embedding = self.openrouter_client.embed([query_text])[0]
        
        # Query collection
        where_clause = filters if filters else None
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where_clause
        )
        
        end_time = time.time()
        
        # Format results
        formatted_results = []
        
        if results and results.get("documents"):
            documents = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0]
            
            for doc, metadata, distance in zip(documents, metadatas, distances):
                # Convert distance to similarity score (1 - normalized distance)
                similarity_score = 1 - (distance / 2)  # Cosine distance range [0, 2]
                
                formatted_results.append({
                    "content": doc,
                    "metadata": metadata,
                    "similarity_score": round(similarity_score, 4)
                })
        
        response = {
            "query": query_text,
            "results": formatted_results,
            "retrieval_time_ms": int((end_time - start_time) * 1000),
            "total_results": len(formatted_results)
        }
        
        logger.info(
            "query_executed",
            query_preview=query_text[:50],
            results_count=len(formatted_results),
            retrieval_time_ms=response["retrieval_time_ms"]
        )
        
        return response
    
    def get_context_for_generation(
        self,
        query: str,
        k: int = 6,
        filters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Retrieve context string for LLM generation.
        
        Args:
            query: Query text
            k: Number of chunks to retrieve
            filters: Metadata filters
            
        Returns:
            Formatted context string
        """
        results = self.query(query, k, filters)
        
        if not results["results"]:
            return ""
        
        # Format context
        context_parts = []
        for idx, result in enumerate(results["results"], 1):
            source = result["metadata"].get("source", "unknown")
            content = result["content"]
            score = result["similarity_score"]
            
            context_parts.append(
                f"[Document {idx} - {source} (relevance: {score:.2f})]\n{content}\n"
            )
        
        context = "\n".join(context_parts)
        
        logger.debug(
            "context_retrieved",
            chunks=len(context_parts),
            total_length=len(context)
        )
        
        return context
    
    def delete_collection(self) -> bool:
        """
        Delete the current collection.
        
        Returns:
            True if successful
        """
        try:
            self.client.delete_collection(name=self.collection_name)
            logger.info("collection_deleted", name=self.collection_name)
            return True
        except Exception as e:
            logger.error("collection_delete_failed", error=str(e))
            return False
    
    def list_document_sources(self) -> List[Dict[str, Any]]:
        """
        List all unique document sources in the collection.
        
        Returns:
            List of unique document sources with metadata
        """
        try:
            count = self.collection.count()
            
            if count == 0:
                return []
            
            # Get all documents
            all_docs = self.collection.get(
                limit=count,
                include=["metadatas"]
            )
            
            # Extract unique sources
            sources_map = {}
            
            if all_docs and all_docs.get("metadatas"):
                for metadata in all_docs["metadatas"]:
                    source = metadata.get("source", "unknown")
                    
                    if source not in sources_map:
                        sources_map[source] = {
                            "source": source,
                            "category": metadata.get("category", "unknown"),
                            "uploaded_at": metadata.get("uploaded_at", "unknown"),
                            "chunk_count": 0
                        }
                    
                    sources_map[source]["chunk_count"] += 1
            
            sources_list = list(sources_map.values())
            
            logger.info(
                "document_sources_listed",
                unique_sources=len(sources_list)
            )
            
            return sources_list
            
        except Exception as e:
            logger.error("list_sources_failed", error=str(e))
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get collection statistics.
        
        Returns:
            Statistics dictionary
        """
        try:
            count = self.collection.count()
            
            # Get sample metadata
            sample = self.collection.peek(limit=1)
            
            stats = {
                "collection_name": self.collection_name,
                "document_count": count,
                "persist_directory": self.persist_directory,
                "has_documents": count > 0
            }
            
            if sample and sample.get("metadatas"):
                stats["sample_metadata"] = sample["metadatas"][0] if sample["metadatas"] else None
            
            logger.info("collection_stats_retrieved", **stats)
            
            return stats
            
        except Exception as e:
            logger.error("stats_retrieval_failed", error=str(e))
            return {
                "error": str(e),
                "collection_name": self.collection_name
            }
    
    def clear_collection(self) -> bool:
        """
        Clear all documents from collection (but keep collection).
        
        Returns:
            True if successful
        """
        try:
            # Delete and recreate collection
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "RAG index for test generation"}
            )
            
            logger.info("collection_cleared", name=self.collection_name)
            return True
            
        except Exception as e:
            logger.error("collection_clear_failed", error=str(e))
            return False


# Convenience functions
def ingest_from_files(file_paths: List[str]) -> Dict[str, Any]:
    """
    Ingest documents from file paths.
    
    Args:
        file_paths: List of file paths to ingest
        
    Returns:
        Ingestion statistics
    """
    service = ChromaService()
    documents = []
    
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            logger.warning("file_not_found", path=file_path)
            continue
        
        content = path.read_text(encoding="utf-8")
        documents.append({
            "content": content,
            "metadata": {
                "source": path.name,
                "file_path": str(path),
                "file_type": path.suffix
            }
        })
    
    return service.ingest_documents(documents)


if __name__ == "__main__":
    # Test the service
    print("Testing ChromaDB Service...")
    
    try:
        service = ChromaService()
        
        # Test ingestion
        print("\n1. Testing document ingestion...")
        test_docs = [
            {
                "content": "User authentication requires valid email and password. JWT tokens expire after 24 hours.",
                "metadata": {"source": "test_doc_1.md", "type": "spec"}
            },
            {
                "content": "The login endpoint is POST /api/auth/login. Returns 200 on success with token.",
                "metadata": {"source": "test_doc_2.md", "type": "api"}
            }
        ]
        
        result = service.ingest_documents(test_docs)
        print(f"✓ Ingestion successful: {result}")
        
        # Test query
        print("\n2. Testing query...")
        query_result = service.query("How does authentication work?", k=2)
        print(f"✓ Query successful: Found {len(query_result['results'])} results")
        
        # Test stats
        print("\n3. Testing stats...")
        stats = service.get_stats()
        print(f"✓ Stats retrieved: {stats}")
        
        print("\n✓ All tests passed!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
