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
- steps: Array of objects with fields: step_number, action, expected
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
                logger.info("llm_raw_response", response_preview=response[:500])
                # Extract JSON from response
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    test_cases = json.loads(json_str)
                else:
                    # Fallback: try parsing entire response
                    parsed = json.loads(response)
                    if isinstance(parsed, dict):
                        test_cases = [parsed]
                    elif isinstance(parsed, list):
                        test_cases = parsed
                    else:
                        logger.warning("unexpected_json_type", type=str(type(parsed)))
                        test_cases = self._generate_fallback_test_cases(feature, requirements)
                
                # Validate test_cases is a list of dicts
                if not isinstance(test_cases, list):
                     test_cases = [test_cases] if isinstance(test_cases, dict) else []
                
                valid_cases = []
                for tc in test_cases:
                    if isinstance(tc, dict):
                        valid_cases.append(tc)
                    else:
                        logger.warning("invalid_test_case_format", test_case=str(tc))
                
                if not valid_cases:
                    logger.warning("no_valid_test_cases_found", original_count=len(test_cases))
                    test_cases = self._generate_fallback_test_cases(feature, requirements)
                else:
                    test_cases = valid_cases

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
            # Safely get test case fields
            if not isinstance(tc, dict):
                tc = {"title": str(tc), "id": f"TC-{idx:03d}"}
            
            title = tc.get('title', 'Untitled Test')
            tc_id = tc.get('id', 'N/A')
            priority = tc.get('priority', 'medium')
            tc_type = tc.get('type', 'functional')
            duration = tc.get('estimated_duration', 'N/A')
            
            md_content += f"""### {idx}. {title}

**Test ID**: `{tc_id}`  
**Priority**: {priority}  
**Type**: {tc_type}  
**Estimated Duration**: {duration}

#### Preconditions
"""
            preconditions = tc.get('preconditions', [])
            if not isinstance(preconditions, list):
                preconditions = [preconditions] if preconditions else []
            for precond in preconditions:
                md_content += f"- {precond}\n"
            
            md_content += "\n#### Test Steps\n\n"
            steps = tc.get('steps', [])
            if not isinstance(steps, list):
                steps = [steps] if steps else []
            for step in steps:
                if isinstance(step, dict):
                    step_num = step.get('step_number', '')
                    action = step.get('action', '')
                    expected = step.get('expected', '')
                else:
                    step_num = ''
                    action = str(step)
                    expected = ''
                md_content += f"{step_num}. **{action}**\n"
                if expected:
                    md_content += f"   - Expected: {expected}\n"
            
            md_content += "\n#### Expected Results\n\n"
            expected_results = tc.get('expected_results', [])
            if not isinstance(expected_results, list):
                expected_results = [expected_results] if expected_results else []
            for result in expected_results:
                md_content += f"- {result}\n"
            
            md_content += f"\n#### Grounding Documents\n\n"
            grounding_docs = tc.get('grounding_docs', [])
            if not isinstance(grounding_docs, list):
                grounding_docs = [grounding_docs] if grounding_docs else []
            for doc in grounding_docs:
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
        # Safely get test_id with fallback
        test_id = str(test_case.get('id', 'TC-000') if isinstance(test_case, dict) else 'TC-000')
        title = str(test_case.get('title', 'Untitled Test') if isinstance(test_case, dict) else 'Untitled Test')
        priority = str(test_case.get('priority', 'medium') if isinstance(test_case, dict) else 'medium')
        test_type = str(test_case.get('type', 'functional') if isinstance(test_case, dict) else 'functional')
        
        # Clean test_id for class name (remove special characters)
        clean_test_id = ''.join(c if c.isalnum() else '' for c in test_id)
        
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


class Test{clean_test_id}:
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
        
        Priority: {priority}
        Type: {test_type}
        """
        try:
'''
        
        # Get steps safely
        steps = []
        if isinstance(test_case, dict):
            steps = test_case.get('steps', [])
            if not isinstance(steps, list):
                steps = [steps] if steps else []
        
        # Generate step implementations
        for i, step in enumerate(steps, 1):
            if isinstance(step, dict):
                action = str(step.get('action', '')).lower()
                step_num = step.get('step_number', i)
                expected = str(step.get('expected', ''))
            else:
                action = str(step).lower()
                step_num = i
                expected = "N/A"
            
            script += f'''            # Step {step_num}: {action}
            # Expected: {expected}
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
