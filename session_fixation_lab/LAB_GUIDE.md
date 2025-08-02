# Session Fixation Attack Lab Guide

## Overview
This lab demonstrates the session fixation vulnerability and how to prevent it. You'll run both a vulnerable and secure version of a Flask application to see the difference.

## What is Session Fixation?

Session fixation is an attack where an attacker sets a known session ID for the victim, then waits for the victim to authenticate using that session ID. After authentication, the attacker can use the same session ID to access the victim's authenticated session.

### Attack Flow:
1. **Attacker** visits login page and gets a session ID
2. **Attacker** sends login link with session ID to victim
3. **Victim** logs in using attacker's session ID
4. **Attacker** can now access victim's authenticated session

## Lab Setup

### Prerequisites
- Python 3.8+
- Virtual environment (already set up)
- Required packages: Flask, Flask-Session, bcrypt

### Files Created:
- `vulnerable_app.py` - Demonstrates the vulnerability
- `secure_app.py` - Shows how to prevent the attack
- `cookie_analyzer.py` - Tool to analyze cookies and demonstrate attack

## Running the Lab

### Step 1: Start the Vulnerable App
```bash
# In your virtual environment
python vulnerable_app.py
```

The vulnerable app will start on `http://localhost:5000`

**Key Vulnerability:**
- Session ID remains the same after login
- No session regeneration
- Weak secret key

### Step 2: Start the Secure App
```bash
# In a new terminal (keep vulnerable app running)
python secure_app.py
```

The secure app will start on `http://localhost:5001`

**Key Security Features:**
- Session ID regenerated after login
- Strong secret key
- Session validation

### Step 3: Run the Cookie Analyzer
```bash
# In a third terminal
python cookie_analyzer.py
```

This tool will:
- Analyze cookies from both apps
- Demonstrate the session fixation attack
- Show the difference between vulnerable and secure implementations

## Lab Exercises

### Exercise 1: Manual Testing

#### Test the Vulnerable App:
1. Visit `http://localhost:5000/login`
2. Note the session ID displayed on the page
3. Login with `admin/admin123`
4. Check that the session ID remains the same
5. This demonstrates the vulnerability!

#### Test the Secure App:
1. Visit `http://localhost:5001/login`
2. Note the session ID displayed on the page
3. Login with `admin/admin123`
4. Check that the session ID changes
5. This demonstrates the fix!

### Exercise 2: Cookie Analysis

#### Using Browser Developer Tools:
1. Open browser developer tools (F12)
2. Go to Network tab
3. Visit the login page
4. Submit login form
5. Observe the session cookie changes

#### Using the Cookie Analyzer:
```bash
python cookie_analyzer.py
```

This will automatically test both apps and show the differences.

### Exercise 3: Session Fixation Attack Simulation

#### Manual Attack Steps:
1. **Attacker Phase:**
   - Visit `http://localhost:5000/login`
   - Note the session ID (e.g., `abc123`)
   - Send this link to victim: `http://localhost:5000/login`

2. **Victim Phase:**
   - Victim visits the link
   - Victim logs in with credentials
   - Session ID remains `abc123`

3. **Attacker Exploitation:**
   - Attacker can now access `http://localhost:5000/dashboard` with session `abc123`
   - Attacker has access to victim's session

## Code Analysis

### Vulnerable Code (vulnerable_app.py):
```python
# VULNERABLE: Session ID remains the same
session['user_id'] = username
session['login_time'] = '2025-01-15T10:30:00Z'
```

### Secure Code (secure_app.py):
```python
# SECURE: Regenerate session ID
old_session_data = dict(session)
session.clear()
session.regenerate()  # New session ID
session['user_id'] = username
session['login_time'] = '2025-01-15T10:30:00Z'
session['authenticated'] = True
```

## Security Measures Implemented

### 1. Session Regeneration
```python
session.regenerate()  # Creates new session ID
```

### 2. Strong Secret Key
```python
app.secret_key = secrets.token_hex(32)  # 256-bit random key
```

### 3. Session Validation
```python
if 'user_id' not in session or not session.get('authenticated'):
    return redirect(url_for('login'))
```

### 4. Proper Session Cleanup
```python
session.clear()  # Remove all session data
```

## Testing Checklist

### Vulnerable App (Should FAIL):
- [ ] Session ID remains same after login
- [ ] Attacker can access victim's session
- [ ] No session regeneration
- [ ] Weak secret key

### Secure App (Should PASS):
- [ ] Session ID changes after login
- [ ] Attacker cannot access victim's session
- [ ] Session regeneration implemented
- [ ] Strong secret key
- [ ] Session validation

## Next Steps
After completing this lab, you should understand:
- How session fixation attacks work
- How to prevent session fixation
- The importance of session security
- How to implement secure session management

This knowledge is crucial for building secure authentication systems and will be valuable when working with Keycloak and other identity management systems. 