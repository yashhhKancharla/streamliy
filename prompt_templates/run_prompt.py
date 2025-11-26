"""
Prompt Template Runner
Grounded_In: Assignment - 1.pdf

Utility to run prompts with templates.
"""

import json
from pathlib import Path
from app.utils.openrouter_client import OpenRouterClient
from app.services.chroma_service import ChromaService


def load_system_prompt() -> str:
    """Load system prompt from template."""
    with open("prompt_templates/system.json") as f:
        data = json.load(f)
        return data["system_prompt"]


def load_user_template() -> str:
    """Load user prompt template."""
    with open("prompt_templates/user_short.txt") as f:
        return f.read()


def run_prompt(
    feature_name: str,
    requirements: str,
    test_types: str = "functional, ui, security",
    priority_levels: str = "high, medium, low"
):
    """
    Run prompt with templates.
    
    Args:
        feature_name: Feature to test
        requirements: Requirements description
        test_types: Comma-separated test types
        priority_levels: Comma-separated priorities
    """
    # Load templates
    system_prompt = load_system_prompt()
    user_template = load_user_template()
    
    # Fill user template
    user_prompt = user_template.format(
        feature_name=feature_name,
        requirements_description=requirements,
        test_types=test_types,
        priority_levels=priority_levels
    )
    
    # Get RAG context
    chroma = ChromaService()
    context = chroma.get_context_for_generation(
        query=f"{feature_name}: {requirements}",
        k=6
    )
    
    # Generate
    client = OpenRouterClient()
    response = client.generate(
        system=system_prompt,
        user=user_prompt,
        context=context
    )
    
    print("Generated Response:")
    print("=" * 80)
    print(response)
    print("=" * 80)
    
    return response


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python run_prompt.py <feature> <requirements>")
        sys.exit(1)
    
    feature = sys.argv[1]
    requirements = sys.argv[2]
    
    run_prompt(feature, requirements)
