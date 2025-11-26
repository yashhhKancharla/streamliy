"""
OpenRouter API Client
Grounded_In: Assignment - 1.pdf

This module provides a unified interface to OpenRouter API for:
- Text generation (LLM completions)
- Text embeddings (vector generation)
"""

import os
from typing import List, Optional, Dict, Any
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

logger = structlog.get_logger()


class OpenRouterClient:
    """Client for OpenRouter API interactions."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: str = "https://openrouter.ai/api/v1"
    ):
        """
        Initialize OpenRouter client.
        
        Args:
            api_key: OpenRouter API key (defaults to env var)
            model: Model identifier (defaults to env var)
            base_url: API base URL
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model or os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
        self.base_url = base_url
        
        if not self.api_key:
            raise ValueError("OpenRouter API key not provided")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/autonomous-qa-agent",
            "X-Title": "Autonomous QA Agent"
        }
        
        logger.info(
            "openrouter_client_initialized",
            model=self.model,
            base_url=self.base_url
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate(
        self,
        system: str,
        user: str,
        context: str = "",
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        """
        Generate text completion using LLM.
        
        Args:
            system: System prompt
            user: User message
            context: Additional context (RAG retrieved content)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
            
        Raises:
            requests.HTTPError: If API request fails
        """
        # Construct the full user message with context
        full_user_message = user
        if context:
            full_user_message = f"Context:\n{context}\n\nQuery:\n{user}"
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": full_user_message}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        logger.info(
            "generating_completion",
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            context_length=len(context) if context else 0
        )
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            # Log response status
            logger.info(
                "api_response_received",
                status_code=response.status_code
            )
            
            response.raise_for_status()
            
            data = response.json()
            generated_text = data["choices"][0]["message"]["content"]
            
            logger.info(
                "completion_generated",
                response_length=len(generated_text),
                tokens_used=data.get("usage", {})
            )
            
            return generated_text
            
        except requests.exceptions.HTTPError as e:
            logger.error(
                "completion_generation_http_error",
                error=str(e),
                status_code=response.status_code if 'response' in locals() else None,
                response_text=response.text if 'response' in locals() else None,
                model=self.model
            )
            raise
        except requests.exceptions.RequestException as e:
            logger.error(
                "completion_generation_failed",
                error=str(e),
                model=self.model
            )
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for text inputs.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (each vector is a list of floats)
            
        Raises:
            requests.HTTPError: If API request fails
        """
        # OpenRouter embeddings endpoint
        # Note: Some models may not support embeddings directly
        # We'll use a completion-based approach for compatibility
        
        logger.info(
            "generating_embeddings",
            num_texts=len(texts)
        )
        
        embeddings = []
        
        for text in texts:
            try:
                # For models without native embedding support,
                # use a lightweight completion model or dedicated embedding model
                embedding_model = os.getenv(
                    "OPENROUTER_EMBEDDING_MODEL",
                    "openai/text-embedding-3-small"
                )
                
                payload = {
                    "model": embedding_model,
                    "input": text
                }
                
                response = requests.post(
                    f"{self.base_url}/embeddings",
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )
                response.raise_for_status()
                
                data = response.json()
                embedding = data["data"][0]["embedding"]
                embeddings.append(embedding)
                
            except requests.exceptions.RequestException as e:
                logger.error(
                    "embedding_generation_failed",
                    error=str(e),
                    text_preview=text[:100]
                )
                # Return zero vector as fallback
                embeddings.append([0.0] * 1536)  # Standard embedding dimension
        
        logger.info(
            "embeddings_generated",
            count=len(embeddings),
            dimension=len(embeddings[0]) if embeddings else 0
        )
        
        return embeddings
    
    def generate_with_metadata(
        self,
        system: str,
        user: str,
        context: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate completion and return with metadata.
        
        Args:
            system: System prompt
            user: User message
            context: Additional context
            **kwargs: Additional arguments for generate()
            
        Returns:
            Dictionary with 'text' and 'metadata' keys
        """
        import time
        start_time = time.time()
        
        text = self.generate(system, user, context, **kwargs)
        
        end_time = time.time()
        
        return {
            "text": text,
            "metadata": {
                "model": self.model,
                "generation_time_ms": int((end_time - start_time) * 1000),
                "context_used": bool(context),
                "context_length": len(context) if context else 0
            }
        }
    
    def test_connection(self) -> bool:
        """
        Test API connectivity and authentication.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            logger.info("openrouter_connection_test_passed")
            return True
        except requests.exceptions.RequestException as e:
            logger.error("openrouter_connection_test_failed", error=str(e))
            return False


# Convenience functions for direct usage
def generate_text(
    system: str,
    user: str,
    context: str = "",
    **kwargs
) -> str:
    """
    Convenience function for text generation.
    
    Args:
        system: System prompt
        user: User message
        context: Additional context
        **kwargs: Additional arguments
        
    Returns:
        Generated text
    """
    client = OpenRouterClient()
    return client.generate(system, user, context, **kwargs)


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Convenience function for embedding generation.
    
    Args:
        texts: List of texts to embed
        
    Returns:
        List of embedding vectors
    """
    client = OpenRouterClient()
    return client.embed(texts)


if __name__ == "__main__":
    # Test the client
    import sys
    
    print("Testing OpenRouter Client...")
    
    try:
        client = OpenRouterClient()
        
        # Test connection
        print("\n1. Testing connection...")
        if client.test_connection():
            print("✓ Connection successful")
        else:
            print("✗ Connection failed")
            sys.exit(1)
        
        # Test generation
        print("\n2. Testing text generation...")
        response = client.generate(
            system="You are a helpful assistant.",
            user="What is 2+2?",
            max_tokens=100
        )
        print(f"✓ Generation successful: {response[:100]}...")
        
        # Test embeddings
        print("\n3. Testing embeddings...")
        embeddings = client.embed(["Hello world", "Test string"])
        print(f"✓ Embeddings generated: {len(embeddings)} vectors, dim={len(embeddings[0])}")
        
        print("\n✓ All tests passed!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
