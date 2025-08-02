# 🍪 Session Fixation Attack Lab

A comprehensive educational lab demonstrating session fixation vulnerabilities and their prevention using Flask applications with professional UI.

## 📋 Overview

This lab provides hands-on experience with session fixation attacks, a critical web security vulnerability. You'll learn how attackers can hijack user sessions and how to prevent these attacks through proper session management.

## 🎯 Learning Objectives

- **Understand** session fixation attack mechanisms
- **Identify** vulnerable session management practices
- **Implement** secure session regeneration techniques
- **Test** both vulnerable and secure implementations
- **Analyze** session behavior using automated tools

## 🏗️ Project Structure

```
session_fixation_lab/
├── static/
│   ├── css/style.css              # Professional UI styling
│   └── js/app.js                  # Interactive features
├── templates/
│   ├── vulnerable_login.html      # Vulnerable app login
│   ├── vulnerable_dashboard.html  # Vulnerable app dashboard
│   ├── secure_login.html          # Secure app login
│   └── secure_dashboard.html      # Secure app dashboard
├── vulnerable_app.py              # Vulnerable Flask application
├── secure_app.py                  # Secure Flask application
├── cookie_analyzer.py             # Automated testing tool
├── LAB_GUIDE.md                  # Detailed lab instructions
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or download** this project
2. **Navigate** to the project directory:
   ```bash
   cd session_fixation_lab
   ```

3. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install flask flask-session bcrypt requests
   ```

### Running the Lab

1. **Start the vulnerable app** (Terminal 1):
   ```bash
   source venv/bin/activate
   python vulnerable_app.py
   ```
   - Access at: http://localhost:5000

2. **Start the secure app** (Terminal 2):
   ```bash
   source venv/bin/activate
   python secure_app.py
   ```
   - Access at: http://localhost:5001

3. **Run automated tests** (Terminal 3):
   ```bash
   source venv/bin/activate
   python cookie_analyzer.py
   ```

## 🔍 Lab Components

### 🚨 Vulnerable Application (`vulnerable_app.py`)

**Purpose**: Demonstrates session fixation vulnerability

**Key Features**:
- Session ID remains constant after login
- Demonstrates exploitable session management
- Professional UI with security warnings

**Test Accounts**:
- `admin` / `admin123`
- `user1` / `password123`

### 🔒 Secure Application (`secure_app.py`)

**Purpose**: Shows how to prevent session fixation attacks

**Key Features**:
- Session regeneration after login
- Secure session management practices
- Professional UI with security indicators

**Security Measures**:
- `session.clear()` before login
- New session ID generation
- Proper session data handling

### 🍪 Cookie Analyzer (`cookie_analyzer.py`)

**Purpose**: Automated testing and demonstration tool

**Features**:
- Tests both vulnerable and secure apps
- Compares session ID behavior
- Demonstrates attack scenarios
- Provides detailed analysis reports

## 🎓 Learning Scenarios

### Scenario 1: Understanding the Vulnerability

1. **Start both applications**
2. **Visit vulnerable app**: http://localhost:5000/login
3. **Note the session behavior**:
   - Session ID remains the same after login
   - Attacker can capture session before login
   - Victim logs in using attacker's session

### Scenario 2: Testing Prevention

1. **Visit secure app**: http://localhost:5001/login
2. **Observe secure behavior**:
   - Session ID changes after login
   - Old session data is cleared
   - New session ID is generated

### Scenario 3: Automated Analysis

1. **Run the cookie analyzer**:
   ```bash
   python cookie_analyzer.py
   ```
2. **Review the results**:
   - Vulnerable app: Session ID unchanged
   - Secure app: Session ID regenerated

## 🛡️ Security Concepts

### Session Fixation Attack

**What it is**: An attack where an attacker sets a user's session ID before the user logs in.

**How it works**:
1. Attacker visits login page and captures session ID
2. Attacker sends link with session ID to victim
3. Victim logs in using the provided session ID
4. Attacker can now access victim's authenticated session

**Why it's dangerous**:
- Bypasses authentication
- Allows session hijacking
- Difficult to detect
- Common in poorly designed applications

### Prevention Techniques

**Session Regeneration**:
- Clear old session data before login
- Generate new session ID after authentication
- Ensure session ID changes on login

**Best Practices**:
- Always regenerate session after login
- Use strong session secrets
- Implement proper session timeouts
- Use secure session storage

## 🎨 UI Features

### Professional Design
- **Modern gradient backgrounds**
- **Responsive layout** (mobile-friendly)
- **Smooth animations** and transitions
- **Professional color scheme**

### Security Indicators
- **Status badges** (vulnerable/secure)
- **Color-coded alerts** (warning/success/danger)
- **Educational content** explaining concepts
- **Interactive elements** for better UX

### Enhanced Functionality
- **Form validation** and loading states
- **Session data formatting**
- **Copy functionality** for session IDs
- **Smooth page transitions**

## 🧪 Testing

### Manual Testing

1. **Browser Testing**:
   - Open two browser tabs
   - Visit both applications
   - Compare session behavior
   - Test login/logout cycles

2. **Session Analysis**:
   - Use browser developer tools
   - Monitor cookie changes
   - Analyze session data

### Automated Testing

1. **Cookie Analyzer**:
   ```bash
   python cookie_analyzer.py
   ```

2. **Expected Results**:
   - Vulnerable app: Session ID unchanged
   - Secure app: Session ID regenerated

## 📚 Educational Resources

### Key Concepts Covered
- **Session Management**
- **Cookie Security**
- **Authentication Flows**
- **Attack Vectors**
- **Defense Mechanisms**

### Related Topics
- **Cross-Site Request Forgery (CSRF)**
- **Session Hijacking**
- **Authentication Bypass**
- **Web Security Best Practices**

## 🔧 Technical Details

### Dependencies
- **Flask**: Web framework
- **Flask-Session**: Session management
- **bcrypt**: Password hashing
- **requests**: HTTP client for testing

### Architecture
- **MVC Pattern**: Templates separate from logic
- **Static Files**: CSS/JS for professional UI
- **Session Storage**: File-based session storage
- **Security Headers**: Proper security configurations

## 🚨 Security Notice

⚠️ **Important**: This lab is for educational purposes only. The vulnerable application demonstrates security flaws and should never be used in production environments.

### Safe Usage
- Use only in controlled, educational environments
- Never deploy vulnerable code to production
- Always implement security best practices in real applications
- Use strong authentication and session management

## 🤝 Contributing

This lab is designed for educational use. If you find issues or have suggestions:

1. **Test thoroughly** before reporting issues
2. **Provide clear descriptions** of problems
3. **Include steps to reproduce** issues
4. **Suggest improvements** for educational value

## 📄 License

This project is for educational purposes. Use responsibly and always follow security best practices in production environments.

## 🎓 Learning Outcomes

After completing this lab, you should be able to:

- ✅ **Identify** session fixation vulnerabilities
- ✅ **Understand** session management security
- ✅ **Implement** secure session practices
- ✅ **Test** session security measures
- ✅ **Explain** attack and defense mechanisms

---

**Happy Learning! 🍪🔒** 