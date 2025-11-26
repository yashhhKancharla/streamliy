# Complete User Guide - Test Case Management System

**Last Updated**: November 26, 2025

---

## 🎯 Quick Start Guide

### Both servers are already running:

- **Backend API**: http://localhost:8000
- **Streamlit UI**: http://localhost:8501

**You don't need to run any commands** - just open the UI in your browser!

---

## 📁 Pre-Built Test Cases - Ready to Use!

We've created **40 comprehensive test cases** organized by feature. These are **ready to copy and use immediately**!

### Location: `app/testcases/`

### Available Test Suites:

#### 1. **Authentication** (`/authentication`)

- 8 test cases covering login, logout, security
- Test IDs: `TC-AUTH-001` to `TC-AUTH-008`
- Priority: HIGH (critical security)

#### 2. **Shopping Cart** (`/shopping_cart`)

- 8 test cases for cart operations
- Test IDs: `TC-CART-001` to `TC-CART-008`
- Priority: HIGH (core e-commerce)

#### 3. **Payment Processing** (`/payment_processing`)

- 8 test cases for payments, security
- Test IDs: `TC-PAY-001` to `TC-PAY-008`
- Priority: HIGH (revenue-critical)

#### 4. **User Management** (`/user_management`)

- 8 test cases for user lifecycle
- Test IDs: `TC-USER-001` to `TC-USER-008`
- Priority: HIGH

#### 5. **Search Functionality** (`/search_functionality`)

- 8 test cases for search and filters
- Test IDs: `TC-SEARCH-001` to `TC-SEARCH-008`
- Priority: HIGH

---

## 🔧 How to Use the System

### Method 1: Copy Pre-Built Test Cases (Easiest!)

1. **Navigate to feature folder:**

   ```
   c:\temporary projects\ocean Ai\task 1\app\testcases\authentication\
   ```

2. **Open `testcases.json`** - Contains all test cases in structured format

3. **Open `README.md`** - Quick reference guide for that feature

4. **Copy what you need:**

   - Copy entire JSON for batch import
   - Copy individual test cases
   - View in Markdown format for easy reading

5. **Paste into your tool:**
   - Test management system (JIRA, TestRail, etc.)
   - Documentation
   - Your own test scripts

### Method 2: Use the Streamlit UI

#### Open UI: http://localhost:8501

#### A. **Ingest Documents** Tab

If you need to add more documentation:

1. Click "📥 Ingest Documents"
2. Choose "Single Document" or "Multiple Documents"
3. Paste content or upload files
4. Click "📤 Ingest Document"
5. Wait for confirmation

#### B. **Query RAG** Tab

To search through documentation:

1. Click "🔍 Query RAG"
2. Enter your question (e.g., "How does authentication work?")
3. Adjust number of results (default: 3)
4. Enable "Generate AI Answer" for synthesized response
5. Click "🔍 Search"
6. View results and AI answer

**Example Queries:**

- "What are the payment processing requirements?"
- "How should user authentication work?"
- "What security constraints apply?"

#### C. **Generate Tests** Tab

To create NEW test cases:

1. Click "🧪 Generate Tests"
2. Enter **Feature Name** (e.g., "Order Management")
3. Enter **Requirements** (detailed description)
4. Select **Test Types**:
   - ✅ Functional
   - ✅ UI/UX
   - ✅ Security
   - ✅ Negative
5. Select **Output Formats**:
   - ✅ JSON (for test management tools)
   - ✅ Markdown (for documentation)
   - ✅ Selenium (for automation)
6. Click "🚀 Generate Test Cases"
7. Wait for AI to generate comprehensive tests
8. View results and download files

**Output locations:**

- `output/testcases_<feature>.json`
- `output/testcases_<feature>.md`
- `tests/selenium/test_<feature>.py`

#### D. **Run Tests** Tab

To execute Selenium tests:

1. Click "▶️ Run Tests"
2. Read the instructions on available test IDs
3. Enter **Test ID** (e.g., `TC-AUTH-001`)
4. Enter **Base URL** of your app (e.g., `http://localhost:3000`)
5. Configure options:
   - Headless mode (run without browser UI)
   - Timeout (default: 30 seconds)
6. Click "▶️ Run Test"
7. View execution results

**Available Test IDs:**

- `TC-AUTH-001` to `TC-AUTH-008` - Authentication
- `TC-CART-001` to `TC-CART-008` - Shopping Cart
- `TC-PAY-001` to `TC-PAY-008` - Payment
- `TC-USER-001` to `TC-USER-008` - User Management
- `TC-SEARCH-001` to `TC-SEARCH-008` - Search

### Method 3: Use REST API

If you prefer API calls:

#### Query RAG

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does authentication work?",
    "k": 3,
    "generate_answer": true
  }'
```

#### Generate Test Cases

```bash
curl -X POST http://localhost:8000/api/v1/generate-tests \
  -H "Content-Type: application/json" \
  -d '{
    "feature": "Order Processing",
    "requirements": "User should be able to place orders...",
    "test_types": ["functional", "ui", "security"],
    "priority_levels": ["high", "medium"],
    "output_formats": ["json", "markdown", "selenium"]
  }'
```

#### Run Test

```bash
curl -X POST http://localhost:8000/api/v1/run-test \
  -H "Content-Type: application/json" \
  -d '{
    "test_id": "TC-AUTH-001",
    "base_url": "http://localhost:3000",
    "headless": false,
    "timeout": 30
  }'
```

---

## 🐛 Troubleshooting

### Issue 1: "AttributeError: 'str' object has no attribute 'get'"

**Status**: ✅ FIXED

- This was in the UI when displaying output files
- Updated code to handle both dict and list formats
- Should work correctly now

### Issue 2: Duplicate results in Query RAG

**Cause**: Multiple ingestions of the same document
**Solution**: This is expected behavior - shows historical ingestions

- Each result has a unique `chunk_id` with timestamp
- All are valid, just from different ingestion times

### Issue 3: "How to run tests?"

**Answer**:

1. Use Streamlit UI "Run Tests" tab (easiest)
2. Or run from terminal:
   ```bash
   cd "c:/temporary projects/ocean Ai/task 1"
   pytest tests/selenium/test_tc_auth_001.py -v
   ```

### Issue 4: "Where are my test cases?"

**Answer**: Multiple locations:

- **Pre-built**: `app/testcases/<feature>/testcases.json`
- **Generated**: `output/testcases_<feature>.json`
- **Selenium scripts**: `tests/selenium/test_*.py`

---

## 📊 System Architecture

```
User Interface (Streamlit) → REST API (Flask) → Services
                                                    ↓
                                            ┌──────────────┐
                                            │  ChromaDB    │
                                            │  (Vector DB) │
                                            └──────────────┘
                                                    ↓
                                            ┌──────────────┐
                                            │  OpenRouter  │
                                            │  (LLM/AI)    │
                                            └──────────────┘
```

---

## 📂 Directory Structure

```
app/
  testcases/              # ← Pre-built test suites (NEW!)
    authentication/
      testcases.json      # ← 8 ready-to-use test cases
      README.md           # ← Quick reference
    shopping_cart/
      testcases.json
      README.md
    payment_processing/
      testcases.json
      README.md
    user_management/
      testcases.json
      README.md
    search_functionality/
      testcases.json
      README.md
    README.md             # ← Main test cases guide

output/                   # Generated test cases
  testcases_*.json
  testcases_*.md

tests/
  selenium/               # Automated test scripts
    test_tc_auth_*.py
    test_tc_cart_*.py
    test_tc_pay_*.py
    test_tc_user_*.py
    test_tc_search_*.py

docs/                     # Source documentation
  product_specs.md
  legal_constraints.md
  ui_ux_guide.md
  admin_manual.md
```

---

## 💡 Best Practices

### For Test Case Generation:

1. **Be specific** in requirements description
2. **Include edge cases** and constraints
3. **Reference documentation** for grounding
4. **Select appropriate test types** for your needs
5. **Review generated tests** before execution

### For Test Execution:

1. **Verify your app is running** at the base URL
2. **Start with functional tests** before edge cases
3. **Run in headless mode** for faster execution
4. **Check logs** if tests fail
5. **Update test data** as needed

### For Documentation:

1. **Ingest all relevant docs** before generating tests
2. **Use consistent naming** for categories
3. **Update docs** when requirements change
4. **Verify ingestion** with Query RAG

---

## 🎓 Example Workflows

### Workflow 1: Quick Test Execution (5 minutes)

1. Open Streamlit UI: http://localhost:8501
2. Go to "Run Tests" tab
3. Enter test ID: `TC-AUTH-001`
4. Enter base URL: `http://localhost:3000`
5. Click "Run Test"
6. Review results

### Workflow 2: Copy Pre-Built Tests (2 minutes)

1. Navigate to: `app/testcases/authentication/`
2. Open `testcases.json`
3. Copy the JSON content
4. Paste into your test management system
5. Done!

### Workflow 3: Generate New Tests (10 minutes)

1. Open Streamlit UI
2. Ingest your documentation (if not done)
3. Go to "Generate Tests" tab
4. Enter feature: "Order Cancellation"
5. Enter requirements: "Users should be able to cancel orders within 24 hours..."
6. Select test types and formats
7. Click "Generate"
8. Download generated files from `output/` folder

### Workflow 4: Full Cycle (30 minutes)

1. **Ingest** new product documentation
2. **Query** to verify documentation is searchable
3. **Generate** test cases for new feature
4. **Review** generated tests in JSON/Markdown
5. **Run** automated Selenium tests
6. **Analyze** results and logs

---

## 🔑 Key Features

### ✅ Completed

- [x] 40 pre-built test cases across 5 features
- [x] Feature-based organization
- [x] JSON and Markdown formats
- [x] Selenium test generation
- [x] RAG-powered AI generation
- [x] REST API endpoints
- [x] Streamlit UI with guides
- [x] Copy-paste ready test cases
- [x] Fixed UI bugs

### 📋 Usage Options

1. **Copy-Paste**: Grab pre-built tests from folders
2. **UI Generation**: Use Streamlit to create new tests
3. **API Integration**: Call REST endpoints programmatically
4. **Automated Execution**: Run Selenium tests

---

## 📞 Need Help?

### Common Questions:

**Q: Where do I start?**
A: Open `app/testcases/README.md` and browse the pre-built test cases!

**Q: How do I copy a test case?**
A: Open `app/testcases/<feature>/testcases.json`, copy the JSON for the test you need.

**Q: Can I modify test cases?**
A: Yes! Copy them and edit as needed. They're templates.

**Q: How do I generate new tests?**
A: Use Streamlit UI → "Generate Tests" tab, or call the API.

**Q: Do tests run automatically?**
A: Not automatically. You trigger them via UI or API.

**Q: Where are test results?**
A: In the UI after execution, or in terminal output if using pytest.

---

## 🚀 Summary

You now have:

- ✅ 40 ready-to-use test cases
- ✅ 5 feature-based test suites
- ✅ Easy copy-paste access
- ✅ AI-powered test generation
- ✅ Automated test execution
- ✅ Complete documentation
- ✅ Both UI and API access

**Start using**: Navigate to `app/testcases/` and copy what you need!
