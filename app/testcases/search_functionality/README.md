# Search Functionality Test Cases

**Feature**: Search & Filter  
**Grounded_In**: Assignment - 1.pdf

## Overview

Complete test suite for search functionality including keyword search, filters, sorting, autocomplete, and pagination.

## Test Cases Summary

| Test ID       | Title                                         | Priority | Type       | Duration |
| ------------- | --------------------------------------------- | -------- | ---------- | -------- |
| TC-SEARCH-001 | Basic Keyword Search Returns Relevant Results | High     | Functional | 1m       |
| TC-SEARCH-002 | Search with No Results Found                  | Medium   | Negative   | 45s      |
| TC-SEARCH-003 | Filter Search Results by Category             | High     | Functional | 1.5m     |
| TC-SEARCH-004 | Sort Search Results by Price                  | High     | Functional | 1m       |
| TC-SEARCH-005 | Search Autocomplete Suggestions               | Medium   | UI         | 1m       |
| TC-SEARCH-006 | Search with Special Characters                | Medium   | Functional | 1m       |
| TC-SEARCH-007 | Pagination of Search Results                  | High     | Functional | 1.5m     |
| TC-SEARCH-008 | Search History Preservation                   | Medium   | Functional | 1.5m     |

## How to Use

Copy from `testcases.json` or run:

```bash
pytest tests/selenium/test_tc_search_*.py -v
```
