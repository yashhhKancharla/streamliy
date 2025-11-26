"""
ChromeDriver Setup and Diagnostic Script
Grounded_In: Assignment - 1.pdf

Automatically diagnoses and fixes ChromeDriver issues.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print(f"   ✅ Success!")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()[:200]}")
            return True
        else:
            print(f"   ❌ Failed!")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False


def check_chrome_installed():
    """Check if Chrome browser is installed."""
    print_header("Step 1: Check Chrome Browser")
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome found at: {path}")
            return True
    
    print("❌ Chrome browser not found!")
    print("\n📥 Please install Chrome:")
    print("   https://www.google.com/chrome/")
    return False


def clear_chromedriver_cache():
    """Clear ChromeDriver cache."""
    print_header("Step 2: Clear ChromeDriver Cache")
    
    cache_dir = Path.home() / ".wdm"
    
    if cache_dir.exists():
        try:
            shutil.rmtree(cache_dir)
            print(f"✅ Cleared cache directory: {cache_dir}")
            return True
        except Exception as e:
            print(f"❌ Failed to clear cache: {e}")
            print(f"   Please manually delete: {cache_dir}")
            return False
    else:
        print(f"ℹ️  Cache directory doesn't exist: {cache_dir}")
        return True


def reinstall_webdriver_manager():
    """Reinstall webdriver-manager."""
    print_header("Step 3: Reinstall webdriver-manager")
    
    # Uninstall
    success1 = run_command(
        "pip uninstall webdriver-manager -y",
        "Uninstalling webdriver-manager"
    )
    
    # Reinstall
    success2 = run_command(
        "pip install webdriver-manager --upgrade",
        "Installing latest webdriver-manager"
    )
    
    return success1 and success2


def test_chromedriver():
    """Test ChromeDriver installation."""
    print_header("Step 4: Test ChromeDriver")
    
    test_code = """
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

try:
    print("Installing ChromeDriver...")
    driver_path = ChromeDriverManager().install()
    print("ChromeDriver installed at: " + str(driver_path))
    
    print("Creating Chrome WebDriver...")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    print("Testing WebDriver...")
    driver.get("https://www.google.com")
    print("Page title: " + driver.title)
    
    driver.quit()
    print("SUCCESS: ChromeDriver is working correctly!")
    
except Exception as e:
    print("ERROR: ChromeDriver test failed: " + str(e))
    import traceback
    traceback.print_exc()
"""
    
    # Write test script with UTF-8 encoding
    test_file = "test_chromedriver_temp.py"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_code)
    
    # Run test
    success = run_command(
        f"python {test_file}",
        "Testing ChromeDriver installation"
    )
    
    # Clean up
    try:
        os.remove(test_file)
    except:
        pass
    
    return success


def main():
    """Main diagnostic and fix function."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║           ChromeDriver Setup & Diagnostic Tool                   ║
║                                                                  ║
║  This script will:                                              ║
║  1. Check if Chrome browser is installed                        ║
║  2. Clear ChromeDriver cache                                    ║
║  3. Reinstall webdriver-manager                                 ║
║  4. Test ChromeDriver installation                              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    input("Press Enter to start diagnostic...")
    
    # Step 1: Check Chrome
    if not check_chrome_installed():
        print("\n❌ Cannot proceed without Chrome browser.")
        print("   Install Chrome and run this script again.")
        return False
    
    # Step 2: Clear cache
    clear_chromedriver_cache()
    
    # Step 3: Reinstall webdriver-manager
    if not reinstall_webdriver_manager():
        print("\n⚠️  webdriver-manager installation had issues.")
        print("   Try running manually: pip install webdriver-manager --upgrade")
    
    # Step 4: Test ChromeDriver
    if test_chromedriver():
        print_header("✅ SUCCESS!")
        print("""
All checks passed! ChromeDriver is now properly configured.

You can now run Selenium tests:
- Via Streamlit UI: http://localhost:8501
- Via pytest: pytest tests/selenium/test_tc_auth_001.py -v

""")
        return True
    else:
        print_header("❌ Setup Incomplete")
        print("""
ChromeDriver test failed. Please try:

1. Manual ChromeDriver Installation:
   - Visit: https://chromedriver.chromium.org/downloads
   - Download version matching your Chrome
   - Add to PATH

2. Check Antivirus:
   - Add exception for .wdm folder
   - Add exception for chromedriver.exe

3. Use Firefox Instead:
   - Install Firefox browser
   - Use geckodriver (automatically handled)

For detailed help, see: SELENIUM_SETUP_GUIDE.md
""")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
