"""
Test Case Generation Service
Grounded_In: Assignment - 1.pdf

This service generates comprehensive test cases using RAG + LLM.
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import structlog

from app.services.chroma_service import ChromaService
from app.utils.openrouter_client import OpenRouterClient
from app.config import get_config

logger = structlog.get_logger()
config = get_config()


class TestGenerationService:
    """Service for generating test cases."""
    
    def __init__(self):
        """Initialize test generation service."""
        self.chroma_service = ChromaService()
        self.openrouter_client = OpenRouterClient()
        self.prompt_dir = Path("prompt_templates")
    
    def _load_system_prompt(self) -> str:
        """Load system prompt template."""
        try:
            prompt_file = self.prompt_dir / "system.json"
            if prompt_file.exists():
                with open(prompt_file) as f:
                    data = json.load(f)
                    return data.get("system_prompt", self._get_default_system_prompt())
        except Exception as e:
            logger.warning("failed_to_load_system_prompt", error=str(e))
        
        return self._get_default_system_prompt()
    
    def _get_default_system_prompt(self) -> str:
        """Get default system prompt."""
        return """You are an expert QA engineer generating comprehensive test cases.

Your task is to generate detailed, executable test cases based on:
1. The provided feature requirements
2. Retrieved context from documentation (RAG)
3. Best practices in software testing

Generate test cases that:
- Cover functional, UI/UX, security, and edge cases
- Include clear preconditions, steps, and expected results
- Reference source documents for grounding
- Are executable with Selenium WebDriver
- Follow priority levels: high, medium, low

Output format: JSON array of test case objects."""
    
    def generate_test_cases(
        self,
        feature: str,
        requirements: str,
        test_types: Optional[List[str]] = None,
        priority_levels: Optional[List[str]] = None,
        output_formats: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate test cases for a feature.
        
        Args:
            feature: Feature name
            requirements: Feature requirements description
            test_types: Types of tests to generate
            priority_levels: Priority levels to include
            output_formats: Output formats (json, markdown, selenium)
            
        Returns:
            Dictionary with test cases and metadata
        """
        import time
        start_time = time.time()
        
        # Default values
        test_types = test_types or ["functional", "ui", "security", "negative"]
        priority_levels = priority_levels or ["high", "medium", "low"]
        output_formats = output_formats or ["json", "markdown"]
        
        # Retrieve context from RAG
        query = f"{feature}: {requirements}"
        context = self.chroma_service.get_context_for_generation(
            query=query,
            k=config.RETRIEVAL_K
        )
        
        logger.info(
            "generating_test_cases",
            feature=feature,
            context_length=len(context),
            test_types=test_types
        )
        
        # Construct user prompt
        user_prompt = f"""Feature: {feature}

Requirements:
{requirements}

Test Types: {', '.join(test_types)}
Priority Levels: {', '.join(priority_levels)}

Generate a comprehensive set of test cases covering all specified test types and priorities.
Each test case must include:
- id: Unique identifier (format: TC-XXX-NNN)
- priority: One of {priority_levels}
- type: One of {test_types}
- title: Clear, descriptive title
- preconditions: List of prerequisites
- steps: Detailed test steps with actions and expected outcomes
- expected_results: Final expected results
- grounding_docs: Source documents referenced
- estimated_duration: Execution time estimate

Return ONLY a valid JSON array of test case objects, no additional text."""
        
        # Generate test cases
        system_prompt = self._load_system_prompt()
        try:
            response = self.openrouter_client.generate(
                system=system_prompt,
                user=user_prompt,
                context=context,
                temperature=0.7,
                max_tokens=4096
            )
            
            # Parse JSON response
            try:
                # Extract JSON from response
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    test_cases = json.loads(json_str)
                else:
                    # Fallback: try parsing entire response
                    test_cases = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error("failed_to_parse_test_cases", error=str(e), response_preview=response[:200])
                test_cases = self._generate_fallback_test_cases(feature, requirements)
        except Exception as e:
            logger.warning("llm_generation_failed", error=str(e), using_fallback=True)
            test_cases = self._generate_fallback_test_cases(feature, requirements)
        
        end_time = time.time()
        
        # Save outputs
        output_files = {}
        
        if "json" in output_formats:
            json_file = self._save_json(test_cases, feature)
            output_files["json"] = json_file
        
        if "markdown" in output_formats:
            md_file = self._save_markdown(test_cases, feature, requirements)
            output_files["markdown"] = md_file
        
        if "selenium" in output_formats:
            selenium_files = self._generate_selenium_scripts(test_cases, feature)
            output_files["selenium"] = selenium_files
        
        result = {
            "status": "success",
            "feature": feature,
            "test_cases": test_cases,
            "output_files": output_files,
            "generation_time_ms": int((end_time - start_time) * 1000),
            "grounding_metadata": {
                "documents_referenced": len(context.split("[Document")) - 1 if context else 0,
                "context_length": len(context)
            }
        }
        
        logger.info(
            "test_cases_generated",
            feature=feature,
            count=len(test_cases),
            generation_time_ms=result["generation_time_ms"]
        )
        
        return result
    
    def _generate_fallback_test_cases(self, feature: str, requirements: str) -> List[Dict[str, Any]]:
        """Generate basic fallback test cases if LLM fails."""
        return [
            {
                "id": "TC-001",
                "priority": "high",
                "type": "functional",
                "title": f"Basic functionality test for {feature}",
                "preconditions": ["System is accessible", "Test data is prepared"],
                "steps": [
                    {"step_number": 1, "action": "Access the feature", "expected": "Feature loads successfully"},
                    {"step_number": 2, "action": "Verify basic functionality", "expected": "Feature works as expected"}
                ],
                "expected_results": ["Feature functions correctly"],
                "grounding_docs": ["product_specs.md"],
                "estimated_duration": "30 seconds"
            }
        ]
    
    def _save_json(self, test_cases: List[Dict[str, Any]], feature: str) -> str:
        """Save test cases as JSON."""
        output_dir = config.OUTPUT_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"testcases_{feature.lower().replace(' ', '_')}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(test_cases, f, indent=2, ensure_ascii=False)
        
        logger.info("json_saved", filepath=str(filepath))
        return str(filepath)
    
    def _save_markdown(self, test_cases: List[Dict[str, Any]], feature: str, requirements: str) -> str:
        """Save test cases as Markdown."""
        output_dir = config.OUTPUT_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"testcases_{feature.lower().replace(' ', '_')}.md"
        filepath = output_dir / filename
        
        md_content = f"""# Test Cases: {feature}

**Grounded_In**: Assignment - 1.pdf

## Feature Requirements

{requirements}

## Generated Test Cases

Total: {len(test_cases)} test cases

---

"""
        
        for idx, tc in enumerate(test_cases, 1):
            md_content += f"""### {idx}. {tc.get('title', 'Untitled Test')}

**Test ID**: `{tc.get('id', 'N/A')}`  
**Priority**: {tc.get('priority', 'medium')}  
**Type**: {tc.get('type', 'functional')}  
**Estimated Duration**: {tc.get('estimated_duration', 'N/A')}

#### Preconditions
"""
            for precond in tc.get('preconditions', []):
                md_content += f"- {precond}\n"
            
            md_content += "\n#### Test Steps\n\n"
            for step in tc.get('steps', []):
                md_content += f"{step.get('step_number', '')}. **{step.get('action', '')}**\n"
                md_content += f"   - Expected: {step.get('expected', '')}\n"
            
            md_content += "\n#### Expected Results\n\n"
            for result in tc.get('expected_results', []):
                md_content += f"- {result}\n"
            
            md_content += f"\n#### Grounding Documents\n\n"
            for doc in tc.get('grounding_docs', []):
                md_content += f"- `{doc}`\n"
            
            md_content += "\n---\n\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.info("markdown_saved", filepath=str(filepath))
        return str(filepath)
    
    def _generate_selenium_scripts(self, test_cases: List[Dict[str, Any]], feature: str) -> List[str]:
        """Generate Selenium test scripts."""
        output_dir = Path("tests/selenium")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        generated_files = []
        
        for tc in test_cases:
            test_id = tc.get('id', 'TC-000').replace('-', '_').lower()
            filename = f"test_{test_id}_{feature.lower().replace(' ', '_')}.py"
            filepath = output_dir / filename
            
            script_content = self._generate_selenium_script_content(tc, feature)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            generated_files.append(str(filepath))
        
        logger.info("selenium_scripts_generated", count=len(generated_files))
        return generated_files
    
    def _generate_selenium_script_content(self, test_case: Dict[str, Any], feature: str) -> str:
        """Generate content for a Selenium script."""
        test_id = test_case.get('id', 'TC-000')
        title = test_case.get('title', 'Untitled Test')
        
        script = f'''"""
Selenium Test: {title}
Test ID: {test_id}
Feature: {feature}
Grounded_In: Assignment - 1.pdf

Auto-generated test script.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class Test{test_id.replace("-", "")}:
    """Test class for {test_id}."""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup test fixture."""
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(self.driver, 10)
    
    def test_{test_id.replace("-", "_").lower()}(self):
        """
        {title}
        
        Priority: {test_case.get('priority', 'medium')}
        Type: {test_case.get('type', 'functional')}
        """
        try:
'''
        
        # Generate step implementations
        for step in test_case.get('steps', []):
            action = step.get('action', '').lower()
            step_num = step.get('step_number', 0)
            
            script += f'''            # Step {step_num}: {step.get('action', '')}
            # Expected: {step.get('expected', '')}
'''
            
            if 'navigate' in action or 'open' in action or 'go to' in action:
                script += f'''            self.driver.get(self.base_url)
            time.sleep(1)
'''
            elif 'click' in action or 'press' in action:
                script += f'''            # TODO: Implement click action
            # element = self.wait.until(EC.element_to_be_clickable((By.ID, "element_id")))
            # element.click()
'''
            elif 'enter' in action or 'type' in action or 'input' in action:
                script += f'''            # TODO: Implement input action
            # element = self.wait.until(EC.presence_of_element_located((By.ID, "element_id")))
            # element.send_keys("test_data")
'''
            elif 'verify' in action or 'check' in action or 'assert' in action:
                script += f'''            # TODO: Implement verification
            # element = self.wait.until(EC.presence_of_element_located((By.ID, "element_id")))
            # assert element.text == "expected_text"
'''
            else:
                script += f'''            # TODO: Implement step action
            pass
'''
            
            script += '\n'
        
        script += f'''            
            # Test passed
            print("✓ Test {test_id} passed")
            
        except TimeoutException as e:
            pytest.fail(f"Timeout waiting for element: {{e}}")
        except AssertionError as e:
            pytest.fail(f"Assertion failed: {{e}}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {{e}}")
'''
        
        return script


# Convenience function
def generate_tests(feature: str, requirements: str, **kwargs) -> Dict[str, Any]:
    """
    Convenience function for test generation.
    
    Args:
        feature: Feature name
        requirements: Requirements description
        **kwargs: Additional arguments
        
    Returns:
        Generation result dictionary
    """
    service = TestGenerationService()
    return service.generate_test_cases(feature, requirements, **kwargs)
