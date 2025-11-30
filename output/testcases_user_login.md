# Test Cases: User Login

**Grounded_In**: Assignment - 1.pdf

## Feature Requirements

Users can login with email and password. Password must be 8+ characters. Account lockout after 5 failed attempts.

## Generated Test Cases

Total: 9 test cases

---

### 1. Successful login with valid credentials

**Test ID**: `TC-FUNC-001`  
**Priority**: high  
**Type**: functional  
**Estimated Duration**: 3

#### Preconditions
- User account exists
- User is on login page

#### Test Steps

1. **Enter valid email address**
   - Expected: Email field accepts input
2. **Enter valid password (8+ characters)**
   - Expected: Password field accepts input
3. **Click login button**
   - Expected: System processes credentials

#### Expected Results

- User is redirected to dashboard

#### Grounding Documents

- `test_specs.md`

---

### 2. Login attempt with invalid email format

**Test ID**: `TC-FUNC-002`  
**Priority**: high  
**Type**: functional  
**Estimated Duration**: 2

#### Preconditions
- User is on login page

#### Test Steps

1. **Enter invalid email (e.g., 'user@')**
   - Expected: Email field accepts input
2. **Enter valid password**
   - Expected: Password field accepts input
3. **Click login button**
   - Expected: System validates inputs

#### Expected Results

- Error message displayed about invalid email format

#### Grounding Documents

- `test_specs.md`

---

### 3. Login attempt with invalid password

**Test ID**: `TC-FUNC-003`  
**Priority**: high  
**Type**: functional  
**Estimated Duration**: 2

#### Preconditions
- Valid user account exists
- User is on login page

#### Test Steps

1. **Enter valid email**
   - Expected: Email field accepts input
2. **Enter incorrect password (8+ characters)**
   - Expected: Password field accepts input
3. **Click login button**
   - Expected: System verifies credentials

#### Expected Results

- Error message displayed about invalid credentials

#### Grounding Documents

- `test_specs.md`

---

### 4. Login attempt with password <8 characters

**Test ID**: `TC-FUNC-004`  
**Priority**: medium  
**Type**: functional  
**Estimated Duration**: 2

#### Preconditions
- User is on login page

#### Test Steps

1. **Enter valid email**
   - Expected: Email field accepts input
2. **Enter 7-character password**
   - Expected: Password field accepts input
3. **Click login button**
   - Expected: System validates password length

#### Expected Results

- Error message displayed about password requirements

#### Grounding Documents

- `test_specs.md`

---

### 5. Account lockout after 5 failed attempts

**Test ID**: `TC-FUNC-005`  
**Priority**: high  
**Type**: functional  
**Estimated Duration**: 5

#### Preconditions
- Valid user account exists
- User is on login page

#### Test Steps

1. **Repeat invalid login attempts 5 times**
   - Expected: System tracks failed attempts
2. **Attempt valid login on 6th try**
   - Expected: System checks account status

#### Expected Results

- Account is locked and appropriate error message is displayed

#### Grounding Documents

- `test_specs.md`

---

### 6. SQL injection attempt in login fields

**Test ID**: `TC-SEC-001`  
**Priority**: high  
**Type**: security  
**Estimated Duration**: 3

#### Preconditions
- User is on login page

#### Test Steps

1. **Enter SQL injection payload in email field**
   - Expected: Input sanitization occurs
2. **Enter random password**
   - Expected: Password field accepts input
3. **Click login button**
   - Expected: System handles malicious input

#### Expected Results

- Login attempt rejected with generic error message

#### Grounding Documents

- `test_specs.md`

---

### 7. Password field masking verification

**Test ID**: `TC-SEC-002`  
**Priority**: medium  
**Type**: security  
**Estimated Duration**: 1

#### Preconditions
- User is on login page

#### Test Steps

1. **Enter text in password field**
   - Expected: Input is masked (e.g., asterisks/dots)

#### Expected Results

- Password characters are not visible in plain text

#### Grounding Documents

- `test_specs.md`

---

### 8. Session management after successful login

**Test ID**: `TC-SEC-003`  
**Priority**: high  
**Type**: security  
**Estimated Duration**: 4

#### Preconditions
- User successfully logged in

#### Test Steps

1. **Check session cookies**
   - Expected: Secure/HttpOnly flags set
2. **Check authentication tokens**
   - Expected: Proper encryption in place

#### Expected Results

- Secure session establishment with proper cookie settings

#### Grounding Documents

- `test_specs.md`

---

### 9. Brute force attack mitigation

**Test ID**: `TC-SEC-004`  
**Priority**: medium  
**Type**: security  
**Estimated Duration**: 5

#### Preconditions
- User account exists
- Login page accessible

#### Test Steps

1. **Perform 5 rapid failed login attempts**
   - Expected: Account lockout mechanism activates
2. **Attempt login with different passwords after lockout**
   - Expected: System maintains lockout state

#### Expected Results

- Account remains locked despite varied password attempts

#### Grounding Documents

- `test_specs.md`

---

