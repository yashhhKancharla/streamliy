"""
Selenium Test: Login attempt with invalid credentials
Test ID: TC-AUTH-002
Feature: User Authentication
Grounded_In: Assignment - 1.pdf

Auto-generated test script - Negative test case.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class TestTCAUTH002:
    """Test class for TC-AUTH-002."""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup test fixture."""
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(self.driver, 10)
    
    def test_tc_auth_002_invalid_login(self):
        """
        Login attempt with invalid credentials
        
        Priority: high
        Type: negative
        """
        try:
            # Step 1: Navigate to login page
            # Expected: Login page loads
            self.driver.get(f"{self.base_url}/login")
            time.sleep(1)

            # Step 2: Enter invalid email
            # Expected: Email field accepts input
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.send_keys("nonexistent@example.com")

            # Step 3: Enter incorrect password
            # Expected: Password field accepts input
            password_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_field.send_keys("WrongPassword")

            # Step 4: Click login button
            # Expected: Form submits
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "login-btn"))
            )
            login_button.click()

            # Verify error message appears
            error_msg = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
            )
            assert "invalid" in error_msg.text.lower() or "incorrect" in error_msg.text.lower()
            
            # Verify still on login page
            assert "/login" in self.driver.current_url
            
            # Test passed
            print("✓ Test TC-AUTH-002 passed")
            
        except TimeoutException as e:
            pytest.fail(f"Timeout waiting for element: {e}")
        except AssertionError as e:
            pytest.fail(f"Assertion failed: {e}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {e}")
