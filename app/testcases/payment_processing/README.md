# Payment Processing Test Cases

**Feature**: Payment Processing  
**Grounded_In**: Assignment - 1.pdf

## Overview

Complete test suite for payment processing including credit card, PayPal, security validation, and error handling.

## Test Cases Summary

| Test ID    | Title                                           | Priority | Type       | Duration |
| ---------- | ----------------------------------------------- | -------- | ---------- | -------- |
| TC-PAY-001 | Complete Payment with Valid Credit Card         | High     | Functional | 2m       |
| TC-PAY-002 | Payment Failure with Invalid Card Details       | High     | Negative   | 1.5m     |
| TC-PAY-003 | Credit Card Information Encryption and Security | High     | Security   | 2m       |
| TC-PAY-004 | Process Payment with PayPal                     | High     | Functional | 2.5m     |
| TC-PAY-005 | Payment Form Validation                         | Medium   | UI         | 1.5m     |
| TC-PAY-006 | Order Summary Verification Before Payment       | High     | Functional | 1m       |
| TC-PAY-007 | Save Payment Method for Future Use              | Medium   | Functional | 2m       |
| TC-PAY-008 | Handle Payment Gateway Timeout                  | High     | Negative   | 2m       |

## How to Use

Copy test cases from `testcases.json` or run automated tests:

```bash
pytest tests/selenium/test_tc_pay_*.py -v
```

## Security Compliance

- ✅ PCI-DSS Compliant
- ✅ HTTPS Encryption
- ✅ No Plain-Text Storage
- ✅ Secure Token Handling
