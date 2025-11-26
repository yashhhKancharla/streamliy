"""
Pytest Configuration and Fixtures
Grounded_In: Assignment - 1.pdf

Provides shared fixtures for Selenium tests.
"""

import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:3000",
        help="Base URL for tests"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome in headless mode"
    )
    parser.addoption(
        "--window-size",
        action="store",
        default="1920,1080",
        help="Browser window size (width,height)"
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Create and configure Chrome WebDriver.
    
    Supports both headed and headless modes.
    Default: headed (for debugging)
    Headless: Set SELENIUM_HEADLESS=true or use --headless flag
    """
    # Check if headless mode is requested
    headless = (
        request.config.getoption("--headless") or
        os.getenv("SELENIUM_HEADLESS", "false").lower() == "true"
    )
    
    # Configure Chrome options
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
    
    # Window size
    window_size = request.config.getoption("--window-size")
    chrome_options.add_argument(f"--window-size={window_size}")
    
    # Additional options for stability
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Logging
    chrome_options.add_argument("--log-level=3")  # Suppress logs
    
    # Create driver with better error handling
    try:
        # Try to install/get ChromeDriver automatically
        driver_path = ChromeDriverManager().install()
        
        # Fix path if it points to wrong file
        import os
        if not driver_path.endswith('.exe'):
            # Path might be pointing to THIRD_PARTY_NOTICES, fix it
            driver_dir = os.path.dirname(driver_path)
            driver_path = os.path.join(driver_dir, 'chromedriver.exe')
            if not os.path.exists(driver_path):
                # Try parent directory
                driver_path = os.path.join(os.path.dirname(driver_dir), 'chromedriver.exe')
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        # If automatic installation fails, try system ChromeDriver
        print(f"\n⚠️ ChromeDriver auto-installation failed: {e}")
        print("Attempting to use system ChromeDriver...")
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e2:
            error_msg = f"""
❌ Chrome WebDriver Setup Failed!

Error: {str(e2)}

🔧 To fix this issue:

1. Install/Update Chrome Browser:
   - Download from: https://www.google.com/chrome/

2. Install ChromeDriver automatically:
   pip install webdriver-manager --upgrade
   
3. OR download ChromeDriver manually:
   - Visit: https://chromedriver.chromium.org/downloads
   - Download version matching your Chrome browser
   - Add to PATH or place in project root

4. Verify Chrome version:
   - Open Chrome → Help → About Google Chrome
   - Note the version number
   - Download matching ChromeDriver

Current Error: {str(e2)}
"""
            pytest.exit(error_msg, returncode=1)
    
    # Set implicit wait
    driver.implicitly_wait(10)
    
    # Maximize window (if not headless)
    if not headless:
        driver.maximize_window()
    
    yield driver
    
    # Teardown
    driver.quit()


@pytest.fixture(scope="function")
def base_url(request):
    """Get base URL from command line or environment."""
    return request.config.getoption("--base-url") or os.getenv("BASE_URL", "http://localhost:3000")


@pytest.fixture(scope="function")
def screenshot_on_failure(request, driver):
    """Take screenshot on test failure."""
    yield
    
    if request.node.rep_call.failed:
        # Create screenshots directory
        screenshots_dir = "test-results/screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Generate screenshot filename
        test_name = request.node.name
        screenshot_path = f"{screenshots_dir}/{test_name}.png"
        
        # Take screenshot
        driver.save_screenshot(screenshot_path)
        print(f"\n📸 Screenshot saved: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results for screenshot fixture.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
