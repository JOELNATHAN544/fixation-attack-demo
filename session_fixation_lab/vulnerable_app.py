#!/usr/bin/env python3
"""
VULNERABLE Flask App - Demonstrates Session Fixation Attack
DO NOT USE IN PRODUCTION!
"""

from flask import Flask, request, session, redirect, url_for, render_template, make_response
from flask_session import Session
import bcrypt

app = Flask(__name__)
app.secret_key = 'vulnerable_secret_key'  # Weak secret key
app.config['SESSION_TYPE'] = 'filesystem'

# VULNERABLE: Missing or weak cookie security configurations
app.config['SESSION_COOKIE_HTTPONLY'] = False  # Allows JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = None   # Allows cross-site requests
app.config['SESSION_COOKIE_SECURE'] = False    # Allows HTTP transmission

Session(app)

# Override Flask-Session defaults for vulnerable app
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SAMESITE'] = None

# Simple user database
USERS = {
    'admin': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt(rounds=12)),
    'user1': bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt(rounds=12))
}

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and verify_password(password, USERS[username]):
            # VULNERABLE: Session ID remains the same - SESSION FIXATION!
            session['user_id'] = username
            session['login_time'] = '2025-01-15T10:30:00Z'
            
            print(f"[VULNERABLE] User {username} logged in")
            response = redirect(url_for('dashboard'))
            
            # Force vulnerable cookie settings by overriding Flask-Session
            response.delete_cookie('session')  # Remove Flask-Session cookie
            response.set_cookie('session', session.sid, 
                              httponly=False, 
                              samesite='Lax',  # Use Lax instead of None for HTTP
                              secure=False,
                              max_age=3600,
                              domain='localhost')
            return response
        else:
            return "Invalid credentials"
    
    # Create a session ID before login to demonstrate the vulnerability
    session['pre_login'] = 'true'
    session.modified = True
    
    # Pass session ID to template for display
    session_id = session.sid if hasattr(session, 'sid') else 'No session ID'
    return render_template('vulnerable_login.html', session_id=session_id)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    session_data = dict(session)
    return render_template('vulnerable_dashboard.html', session_data=session_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("🚨 VULNERABLE APP STARTING 🚨")
    print("This app demonstrates session fixation vulnerability")
    print("Access the app at: http://localhost:5000")
    print("Session ID will remain the same after login!")
    app.run(debug=True, host='0.0.0.0', port=5000) 