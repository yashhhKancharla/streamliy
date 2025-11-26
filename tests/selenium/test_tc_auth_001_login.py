"""
Selenium Test: Successful user login with valid credentials
Test ID: TC-AUTH-001
Feature: User Authentication
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


class TestTCAUTH001:
    """Test class for TC-AUTH-001."""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup test fixture."""
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(self.driver, 10)
    
    def test_tc_auth_001(self):
        """
        Successful user login with valid credentials
        
        Priority: high
        Type: functional
        """
        try:
            # Step 1: Navigate to login page
            # Expected: Login page loads successfully
            self.driver.get(f"{self.base_url}/login")
            time.sleep(1)

            # Step 2: Enter email address
            # Expected: Email field accepts input
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.send_keys("testuser@example.com")

            # Step 3: Enter password
            # Expected: Password field masks input
            password_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_field.send_keys("SecurePass123!")

            # Step 4: Click login button
            # Expected: Form submits and loading indicator appears
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "login-btn"))
            )
            login_button.click()

            # Verify redirection to dashboard
            self.wait.until(
                EC.url_contains("/dashboard")
            )
            
            # Verify success message
            success_msg = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
            )
            assert "Welcome back" in success_msg.text.lower()
            
            # Test passed
            print("✓ Test TC-AUTH-001 passed")
            
        except TimeoutException as e:
            pytest.fail(f"Timeout waiting for element: {e}")
        except AssertionError as e:
            pytest.fail(f"Assertion failed: {e}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {e}")
