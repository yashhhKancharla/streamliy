# Test Cases: Sample Feature Suite

**Grounded_In**: Assignment - 1.pdf

## Feature Requirements

Comprehensive test coverage for authentication, UI, API, security, and RAG functionality of the Autonomous QA Agent system.

## Generated Test Cases

Total: 6 test cases

---

### 1. Successful user login with valid credentials

**Test ID**: `TC-AUTH-001`  
**Priority**: high  
**Type**: functional  
**Estimated Duration**: 30 seconds

#### Preconditions

- User account exists in database
- User is not already logged in
- Browser is open on login page

#### Test Steps

1. **Navigate to login page**
   - Expected: Login page loads successfully
2. **Enter email address**
   - Expected: Email field accepts input
3. **Enter password**
   - Expected: Password field masks input
4. **Click login button**
   - Expected: Form submits and loading indicator appears

#### Expected Results

- User is redirected to dashboard page
- Success message displays: 'Welcome back!'
- Navigation shows user name
- JWT token stored in session

#### Grounding Documents

- `authentication_spec.md`
- `api_endpoints.md`
- `ui_ux_guide.md`

---

### 2. Login attempt with invalid credentials

**Test ID**: `TC-AUTH-002`  
**Priority**: high  
**Type**: negative  
**Estimated Duration**: 20 seconds

#### Preconditions

- Browser is open on login page

#### Test Steps

1. **Navigate to login page**
   - Expected: Login page loads
2. **Enter invalid email**
   - Expected: Email field accepts input
3. **Enter incorrect password**
   - Expected: Password field accepts input
4. **Click login button**
   - Expected: Form submits

#### Expected Results

- User remains on login page
- Error message displays: 'Invalid email or password'
- Email and password fields are cleared
- Failed attempt logged in security logs

#### Grounding Documents

- `authentication_spec.md`
- `security_spec.md`

---

### 3. Verify responsive layout on mobile viewport

**Test ID**: `TC-UI-001`  
**Priority**: medium  
**Type**: ui  
**Estimated Duration**: 45 seconds

#### Preconditions

- Application is accessible

#### Test Steps

1. **Set browser viewport to mobile size (375x667)**
   - Expected: Viewport resized successfully
2. **Navigate to home page**
   - Expected: Page loads with mobile layout
3. **Verify hamburger menu is visible**
   - Expected: Hamburger icon displayed instead of full navigation
4. **Click hamburger menu**
   - Expected: Navigation menu expands

#### Expected Results

- Layout adapts to mobile viewport
- Navigation is accessible via hamburger menu
- Content is readable without horizontal scrolling
- Touch targets are appropriately sized

#### Grounding Documents

- `ui_ux_guide.md`
- `product_specs.md`

---

### 4. Test document ingestion via API

**Test ID**: `TC-API-001`  
**Priority**: high  
**Type**: functional  
**Estimated Duration**: 25 seconds

#### Preconditions

- API is accessible
- Valid API key is available

#### Test Steps

1. **Send POST request to /ingest endpoint**
   - Expected: Request accepted with 200 status
2. **Verify response contains ingested_count**
   - Expected: Response includes ingestion statistics
3. **Query for ingested content**
   - Expected: Document is retrievable via query endpoint

#### Expected Results

- Documents successfully ingested
- ChromaDB collection updated
- Ingested content is searchable

#### Grounding Documents

- `api_endpoints.md`
- `product_specs.md`

---

### 5. Verify API authentication is required

**Test ID**: `TC-SEC-001`  
**Priority**: high  
**Type**: security  
**Estimated Duration**: 30 seconds

#### Preconditions

- API is accessible

#### Test Steps

1. **Send request to /generate-tests without API key**
   - Expected: Request sent
2. **Verify response status is 401 Unauthorized**
   - Expected: Authentication error returned
3. **Send request with invalid API key**
   - Expected: Request sent with invalid key
4. **Verify response status is 401 Unauthorized**
   - Expected: Authentication error returned

#### Expected Results

- All endpoints require valid authentication
- Appropriate error messages returned
- Failed attempts are logged

#### Grounding Documents

- `api_endpoints.md`
- `legal_constraints.md`

---

### 6. Test RAG context retrieval accuracy

**Test ID**: `TC-RAG-001`  
**Priority**: high  
**Type**: functional  
**Estimated Duration**: 20 seconds

#### Preconditions

- Documents are ingested into ChromaDB
- Vector embeddings are generated

#### Test Steps

1. **Query for authentication-related content**
   - Expected: Query processed
2. **Verify returned results contain authentication documentation**
   - Expected: Relevant chunks retrieved
3. **Check similarity scores are above 0.7**
   - Expected: High relevance scores

#### Expected Results

- Relevant documents retrieved
- Similarity scores indicate good matches
- Retrieved content is semantically related to query

#### Grounding Documents

- `product_specs.md`
- `api_endpoints.md`

---
