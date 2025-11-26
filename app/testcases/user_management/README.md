# User Management Test Cases

**Feature**: User Management  
**Grounded_In**: Assignment - 1.pdf

## Overview

Comprehensive test suite for user registration, profile management, password changes, and account deletion.

## Test Cases Summary

| Test ID     | Title                                           | Priority | Type       | Duration |
| ----------- | ----------------------------------------------- | -------- | ---------- | -------- |
| TC-USER-001 | User Registration with Valid Details            | High     | Functional | 2m       |
| TC-USER-002 | Registration with Already Existing Email        | Medium   | Negative   | 1m       |
| TC-USER-003 | View and Edit User Profile                      | High     | Functional | 1.5m     |
| TC-USER-004 | Change User Password                            | High     | Security   | 2m       |
| TC-USER-005 | Upload and Update Profile Picture               | Medium   | Functional | 1.5m     |
| TC-USER-006 | Upload Invalid File Type as Profile Picture     | Medium   | Negative   | 1m       |
| TC-USER-007 | Delete User Account                             | High     | Functional | 2m       |
| TC-USER-008 | Password Strength Indicator During Registration | Medium   | UI         | 1m       |

## How to Use

Copy test cases from `testcases.json` or execute:

```bash
pytest tests/selenium/test_tc_user_*.py -v
```
