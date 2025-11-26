# Shopping Cart Test Cases

**Feature**: Shopping Cart Management  
**Grounded_In**: Assignment - 1.pdf

## Overview

Comprehensive test cases for shopping cart functionality including adding/removing items, quantity management, discount codes, and cart persistence.

## Test Cases Summary

| Test ID     | Title                              | Priority | Type       | Duration |
| ----------- | ---------------------------------- | -------- | ---------- | -------- |
| TC-CART-001 | Add Product to Empty Shopping Cart | High     | Functional | 1m       |
| TC-CART-002 | Update Product Quantity in Cart    | High     | Functional | 50s      |
| TC-CART-003 | Remove Product from Shopping Cart  | High     | Functional | 45s      |
| TC-CART-004 | Cart Persistence Across Sessions   | Medium   | Functional | 2m       |
| TC-CART-005 | Add Out-of-Stock Product to Cart   | High     | Negative   | 1m       |
| TC-CART-006 | Empty Cart User Experience         | Medium   | UI         | 40s      |
| TC-CART-007 | Apply Discount Code to Cart        | High     | Functional | 1m       |
| TC-CART-008 | Apply Invalid Discount Code        | Medium   | Negative   | 45s      |

## How to Use These Test Cases

### Quick Copy-Paste

Simply open `testcases.json` and copy the test cases you need into your test management tool or documentation.

### Run as Automated Tests

```bash
# Generate Selenium tests
pytest tests/selenium/test_tc_cart_*.py -v
```

## Test Coverage

- ✅ Add/Remove Items
- ✅ Quantity Management
- ✅ Discount Code Application
- ✅ Cart Persistence
- ✅ Out-of-Stock Handling
- ✅ Empty Cart State
