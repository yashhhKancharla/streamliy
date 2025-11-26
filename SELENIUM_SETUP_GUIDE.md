# 🔧 Selenium ChromeDriver Setup Guide

## ❌ Error: OSError: [WinError 193] %1 is not a valid Win32 application

This error means ChromeDriver is not properly configured. Here's how to fix it:

---

## 🚀 Quick Fix (Recommended)

### Step 1: Check Chrome Browser Version

1. Open Google Chrome
2. Click menu (three dots) → **Help** → **About Google Chrome**
3. Note your version (e.g., Chrome 119.0.6045.105)

### Step 2: Reinstall webdriver-manager

```bash
cd "c:/temporary projects/ocean Ai/task 1"
source .venv/Scripts/activate  # Activate virtual environment
pip uninstall webdriver-manager -y
pip install webdriver-manager --upgrade
```

### Step 3: Clear ChromeDriver Cache

```bash
# Windows
del /f /s /q %USERPROFILE%\.wdm\*
# Or manually delete: C:\Users\<YourUsername>\.wdm\
```

### Step 4: Test ChromeDriver Installation

```bash
python -c "from webdriver_manager.chrome import ChromeDriverManager; print(ChromeDriverManager().install())"
```

If this prints a path without errors, you're good to go!

---

## 🔄 Alternative Fix: Manual ChromeDriver Installation

### Step 1: Download ChromeDriver

1. Visit: https://chromedriver.chromium.org/downloads
2. Download version matching your Chrome browser
3. Extract `chromedriver.exe`

### Step 2: Place ChromeDriver

**Option A: Add to PATH**

```bash
# Add the folder containing chromedriver.exe to your system PATH
# Example: C:\WebDrivers\
```

**Option B: Place in Project**

```bash
# Copy chromedriver.exe to project root
cp chromedriver.exe "c:/temporary projects/ocean Ai/task 1/"
```

### Step 3: Update conftest.py (if using manual installation)

```python
# In tests/conftest.py, change:
service = Service(ChromeDriverManager().install())

# To:
service = Service("./chromedriver.exe")  # or full path
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Chrome Version Mismatch

**Symptom**: "This version of ChromeDriver only supports Chrome version XX"

**Solution**:

```bash
# Update Chrome browser to latest version
# Then reinstall webdriver-manager
pip install webdriver-manager --upgrade --force-reinstall
```

### Issue 2: 32-bit vs 64-bit Mismatch

**Symptom**: WinError 193

**Solution**:

- Ensure Chrome browser is 64-bit (check in About Chrome)
- Download 64-bit ChromeDriver from official site

### Issue 3: Antivirus Blocking ChromeDriver

**Symptom**: Executable is deleted or blocked

**Solution**:

- Add exception in antivirus for `.wdm` folder
- Add exception for `chromedriver.exe`

### Issue 4: Permission Denied

**Symptom**: PermissionError when starting ChromeDriver

**Solution**:

```bash
# Run terminal as Administrator
# Or manually set permissions on chromedriver.exe
```

---

## ✅ Verify Setup is Working

Run this test command:

```bash
cd "c:/temporary projects/ocean Ai/task 1"
source .venv/Scripts/activate
pytest tests/selenium/test_tc_auth_001_login.py -v --headless
```

If you see tests running (even if they fail due to app not running), ChromeDriver is working!

---

## 🎯 Alternative: Use Firefox Instead

If Chrome issues persist, switch to Firefox:

### Step 1: Install Firefox

Download from: https://www.mozilla.org/firefox/

### Step 2: Install geckodriver

```bash
pip install webdriver-manager --upgrade
```

### Step 3: Update conftest.py

```python
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# In driver fixture:
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)
```

---

## 📋 Complete Setup Checklist

- [ ] Chrome browser installed and up-to-date
- [ ] Python virtual environment activated
- [ ] `webdriver-manager` installed: `pip install webdriver-manager`
- [ ] ChromeDriver cache cleared
- [ ] No antivirus blocking ChromeDriver
- [ ] Test command runs without WinError 193

---

## 🆘 Still Having Issues?

### Check System Requirements:

- ✅ Windows 10/11 64-bit
- ✅ Python 3.8+
- ✅ Chrome 100+ (latest recommended)
- ✅ 4GB+ RAM

### Get Detailed Error Info:

```bash
python -c "
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import traceback

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    print('✅ ChromeDriver working!')
    driver.quit()
except Exception as e:
    print('❌ Error:', e)
    traceback.print_exc()
"
```

---

## 🔗 Useful Resources

- Chrome Releases: https://chromedriver.chromium.org/downloads
- WebDriver Manager: https://github.com/SergeyPirogov/webdriver_manager
- Selenium Docs: https://www.selenium.dev/documentation/
- Chrome for Testing: https://googlechromelabs.github.io/chrome-for-testing/

---

## 💡 Pro Tips

1. **Keep Chrome Updated**: Enable automatic updates
2. **Use Headless Mode**: Faster and more stable for CI/CD
3. **Clear Cache Regularly**: Delete `.wdm` folder periodically
4. **Use Docker**: Consider Docker containers for consistent environment
5. **Version Pinning**: Pin ChromeDriver version in production

---

**After fixing, try running tests again from the Streamlit UI!**
