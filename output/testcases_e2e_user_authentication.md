# Test Cases: E2E User Authentication

**Grounded_In**: Assignment - 1.pdf

## Feature Requirements

User login with email/password. Password 8+ chars. Account lockout after 5 failures.

## Generated Test Cases

Total: 6 test cases

---

### 1. Successful login with valid credentials

**Test ID**: `TC-AUTH-001`  
**Priority**: high  
**Type**: functional  
**Estimated Duration**: 2

#### Preconditions
- User has registered account
- User is on login page

#### Test Steps

1. **Enter valid email address: user@example.com**
   - Expected: Email field accepts input
2. **Enter valid password: Pass1234**
   - Expected: Password field accepts input
3. **Click login button**
   - Expected: User is redirected to dashboard

#### Expected Results

- Successful login and dashboard access

#### Grounding Documents

- `Document 1`
- `Document 2`

---

### 2. Login attempt with invalid email format

**Test ID**: `TC-AUTH-002`  
**Priority**: high  
**Type**: functional  
**Estimated Duration**: 1

#### Preconditions
- User is on login page

#### Test Steps

1. **Enter invalid email: invalid-email**
   - Expected: Email field accepts input
2. **Enter valid password: Pass1234**
   - Expected: Password field accepts input
3. **Click login button**
   - Expected: Error message displayed about invalid email format

#### Expected Results

- System rejects invalid email format with error message

#### Grounding Documents

- `Document 2`

---

### 3. Login attempt with incorrect password

**Test ID**: `TC-AUTH-003`  
**Priority**: high  
**Type**: security  
**Estimated Duration**: 1

#### Preconditions
- User has registered account
- User is on login page

#### Test Steps

1. **Enter valid email address: user@example.com**
   - Expected: Email field accepts input
2. **Enter invalid password: Wrong123**
   - Expected: Password field accepts input
3. **Click login button**
   - Expected: Error message displayed about invalid credentials

#### Expected Results

- System rejects invalid credentials with error message

#### Grounding Documents

- `Document 1`
- `Document 2`

---

### 4. Password length validation - 7 characters

**Test ID**: `TC-AUTH-004`  
**Priority**: medium  
**Type**: functional  
**Estimated Duration**: 1

#### Preconditions
- User is on login page

#### Test Steps

1. **Enter valid email address: user@example.com**
   - Expected: Email field accepts input
2. **Enter short password: Short12**
   - Expected: Password field accepts input
3. **Click login button**
   - Expected: Error message displayed about password requirements

#### Expected Results

- System rejects password shorter than 8 characters

#### Grounding Documents

- `Document 1`
- `Document 2`

---

### 5. Account lockout after 5 consecutive failed attempts

**Test ID**: `TC-AUTH-005`  
**Priority**: medium  
**Type**: security  
**Estimated Duration**: 3

#### Preconditions
- User has registered account
- User is on login page

#### Test Steps

1. **Repeat 5 times: Enter valid email with invalid password and submit**
   - Expected: Error message after each attempt
2. **Attempt login with correct credentials**
   - Expected: Account locked error message displayed

#### Expected Results

- Account is locked after 5 failed attempts and prevents further login

#### Grounding Documents

- `Document 1`

---

### 6. Session timeout after 30 minutes of inactivity

**Test ID**: `TC-AUTH-006`  
**Priority**: medium  
**Type**: security  
**Estimated Duration**: 3

#### Preconditions
- User is successfully logged in
- User is on dashboard page

#### Test Steps

1. **Wait 30 minutes without activity**
   - Expected: Session remains active during waiting period
2. **Attempt to refresh dashboard page**
   - Expected: User is redirected to login page

#### Expected Results

- Session automatically expires after 30 minutes of inactivity

#### Grounding Documents

- `Document 1`

---

