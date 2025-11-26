# Test Cases Overview

**Grounded_In**: Assignment - 1.pdf

## Feature-Based Test Case Organization

This directory contains test cases organized by application features. Each feature folder includes:

- ✅ **testcases.json** - Structured test cases for easy copy-paste or API integration
- ✅ **README.md** - Quick reference guide for that feature

## Available Feature Test Suites

### 1. Authentication (`/authentication`)

- **8 test cases** covering login, logout, session management, security
- Priority: High (critical security feature)
- Coverage: Functional, Security, Negative, UI

### 2. Shopping Cart (`/shopping_cart`)

- **8 test cases** for cart operations, quantity management, discounts
- Priority: High (core e-commerce feature)
- Coverage: Functional, Negative, UI

### 3. Payment Processing (`/payment_processing`)

- **8 test cases** for payment methods, security, validation
- Priority: High (revenue-critical feature)
- Coverage: Functional, Security, Negative, UI
- Compliance: PCI-DSS

### 4. User Management (`/user_management`)

- **8 test cases** for registration, profile management, account operations
- Priority: High (user lifecycle)
- Coverage: Functional, Security, Negative, UI

### 5. Search Functionality (`/search_functionality`)

- **8 test cases** for search, filters, sorting, autocomplete
- Priority: High (user experience)
- Coverage: Functional, Negative, UI

## Total Test Coverage

- **40 comprehensive test cases** across 5 major features
- **All test types**: Functional, Security, Negative, UI/UX
- **Ready to use**: Copy-paste or automated execution

## How to Use These Test Cases

### Option 1: Manual Testing (Copy-Paste)

1. Navigate to the feature folder you need (e.g., `/authentication`)
2. Open `testcases.json`
3. Copy the test cases
4. Paste into your test management system (JIRA, TestRail, etc.)

### Option 2: API Integration

Use the test generation API to create automated Selenium tests:

```bash
# Generate automated tests from JSON
curl -X POST http://localhost:8000/api/v1/generate-tests \
  -H "Content-Type: application/json" \
  -d @app/testcases/authentication/testcases.json
```

### Option 3: Run Automated Tests

Execute Selenium tests directly:

```bash
# Run all tests
pytest tests/selenium/ -v

# Run specific feature tests
pytest tests/selenium/test_tc_auth_*.py -v
pytest tests/selenium/test_tc_cart_*.py -v
pytest tests/selenium/test_tc_pay_*.py -v
pytest tests/selenium/test_tc_user_*.py -v
pytest tests/selenium/test_tc_search_*.py -v
```

## Test Case Structure

Each test case includes:

- **ID**: Unique identifier (e.g., TC-AUTH-001)
- **Priority**: High/Medium/Low
- **Type**: Functional/Security/Negative/UI
- **Title**: Clear description
- **Preconditions**: Setup requirements
- **Steps**: Detailed execution steps with expected results
- **Expected Results**: Final validation criteria
- **Grounding Docs**: Source documentation references
- **Estimated Duration**: Time to execute

## Quick Reference by Priority

### High Priority Test Cases (24 tests)

These are critical path tests that must pass:

- All authentication flows
- Payment processing
- Cart operations
- User registration
- Core search functionality

### Medium Priority Test Cases (16 tests)

Important for user experience:

- Edge cases
- UI validations
- Optional features

## Grounding Documents

All test cases are grounded in:

- `product_specs.md` - Product requirements
- `legal_constraints.md` - Security & compliance
- `ui_ux_guide.md` - User experience standards
- `admin_manual.md` - System configuration

## Need More Test Cases?

Use the UI or API to generate additional test cases:

1. Open the Streamlit UI: http://localhost:8501
2. Go to "Generate Test Cases"
3. Enter feature name and requirements
4. System will generate comprehensive test cases using RAG + LLM
