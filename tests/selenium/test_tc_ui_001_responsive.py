"""
Selenium Test: Verify responsive layout on mobile viewport
Test ID: TC-UI-001
Feature: UI/UX Testing
Grounded_In: Assignment - 1.pdf

Auto-generated test script - UI test case.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class TestTCUI001:
    """Test class for TC-UI-001."""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup test fixture."""
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(self.driver, 10)
    
    def test_tc_ui_001_responsive_mobile(self):
        """
        Verify responsive layout on mobile viewport
        
        Priority: medium
        Type: ui
        """
        try:
            # Step 1: Set browser viewport to mobile size (375x667)
            # Expected: Viewport resized successfully
            self.driver.set_window_size(375, 667)
            time.sleep(0.5)

            # Step 2: Navigate to home page
            # Expected: Page loads with mobile layout
            self.driver.get(self.base_url)
            time.sleep(1)

            # Step 3: Verify hamburger menu is visible
            # Expected: Hamburger icon displayed instead of full navigation
            hamburger_menu = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "hamburger-menu"))
            )
            assert hamburger_menu.is_displayed()

            # Step 4: Click hamburger menu
            # Expected: Navigation menu expands
            hamburger_menu.click()
            time.sleep(0.5)
            
            # Verify navigation menu is visible
            nav_menu = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "mobile-nav"))
            )
            assert nav_menu.is_displayed()
            
            # Verify no horizontal scrolling
            body_width = self.driver.execute_script("return document.body.scrollWidth")
            viewport_width = self.driver.execute_script("return window.innerWidth")
            assert body_width <= viewport_width, "Horizontal scrolling detected"
            
            # Test passed
            print("✓ Test TC-UI-001 passed")
            
        except TimeoutException as e:
            pytest.fail(f"Timeout waiting for element: {e}")
        except AssertionError as e:
            pytest.fail(f"Assertion failed: {e}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {e}")
