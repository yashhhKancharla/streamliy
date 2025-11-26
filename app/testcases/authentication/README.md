# Authentication Test Cases

**Feature**: User Authentication  
**Grounded_In**: Assignment - 1.pdf

## Overview

This folder contains comprehensive test cases for authentication functionality including login, logout, session management, and security validations.

## Test Cases Summary

| Test ID     | Title                                     | Priority | Type       | Duration |
| ----------- | ----------------------------------------- | -------- | ---------- | -------- |
| TC-AUTH-001 | Valid User Login with Correct Credentials | High     | Functional | 45s      |
| TC-AUTH-002 | Login Attempt with Invalid Credentials    | High     | Negative   | 30s      |
| TC-AUTH-003 | Session Expiration After Timeout Period   | High     | Security   | 2m       |
| TC-AUTH-004 | Logout Functionality                      | Medium   | Functional | 40s      |
| TC-AUTH-005 | Password Field Masking and Security       | High     | Security   | 50s      |
| TC-AUTH-006 | Login Form Validation and Error Messages  | Medium   | UI         | 1m       |
| TC-AUTH-007 | SQL Injection Attack Prevention in Login  | High     | Security   | 1m       |
| TC-AUTH-008 | Remember Me Functionality                 | Medium   | Functional | 1.5m     |

## How to Use

### Option 1: Copy and Paste Test Cases

1. Open `testcases.json` in this folder
2. Copy the test case(s) you need
3. Paste into your test management system

### Option 2: Use with API

```bash
# Generate automated Selenium tests from these test cases
curl -X POST http://localhost:8000/api/v1/generate-tests \
  -H "Content-Type: application/json" \
  -d @testcases.json
```

### Option 3: Run Automated Tests

```bash
# Navigate to project root
cd "c:/temporary projects/ocean Ai/task 1"

# Run authentication tests
pytest tests/selenium/test_tc_auth_*.py -v
```

## Test Coverage

- ✅ Functional Testing (Login, Logout)
- ✅ Security Testing (SQL Injection, Session Management, Password Masking)
- ✅ Negative Testing (Invalid Credentials)
- ✅ UI/UX Testing (Form Validation, Error Messages)

## Grounding Documents

- `product_specs.md` - Product specifications
- `legal_constraints.md` - Security and compliance requirements
- `admin_manual.md` - Administrator documentation
- `ui_ux_guide.md` - UI/UX guidelines
