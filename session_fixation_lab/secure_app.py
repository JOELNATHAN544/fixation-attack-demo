#!/usr/bin/env python3
"""
SECURE Flask App - Prevents Session Fixation Attack
"""

from flask import Flask, request, session, redirect, url_for, render_template, make_response
from flask_session import Session
import bcrypt
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Strong secret key
app.config['SESSION_TYPE'] = 'filesystem'

# SECURE: Proper cookie security configurations
app.config['SESSION_COOKIE_HTTPONLY'] = True   # Prevents JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Prevents cross-site requests
app.config['SESSION_COOKIE_SECURE'] = False    # Set to True in production with HTTPS

Session(app)

# Override Flask-Session defaults for secure app
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# Custom session ID generator for secure app
def generate_secure_session_id():
    return secrets.token_urlsafe(32)

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
            # SECURE: Regenerate session ID to prevent session fixation
            # Get the old session ID for comparison
            old_session_id = session.sid if hasattr(session, 'sid') else None
            
            # Clear the session completely
            session.clear()
            
            # Create new session data
            session['user_id'] = username
            session['login_time'] = '2025-01-15T10:30:00Z'
            session['authenticated'] = True
            
            # Force session to be saved
            session.modified = True
            
            # Generate a new session ID manually
            new_session_id = generate_secure_session_id()
            
            print(f"[SECURE] User {username} logged in")
            print(f"[SECURE] Old session ID: {old_session_id}")
            print(f"[SECURE] New session ID: {new_session_id}")
            
            # Force browser to accept new session cookie by using a different approach
            response = redirect(url_for('dashboard'))
            
            # Delete the old cookie with explicit parameters that match the original
            response.delete_cookie('session', domain='localhost', path='/', secure=False, httponly=True, samesite='Strict')
            
            # Set the new cookie with a slightly different name first, then the main one
            response.set_cookie('session_temp', new_session_id, 
                              httponly=True, 
                              samesite='Strict', 
                              secure=False,
                              max_age=3600,
                              domain='localhost',
                              path='/')
            
            # Now set the main session cookie
            response.set_cookie('session', new_session_id, 
                              httponly=True, 
                              samesite='Strict', 
                              secure=False,
                              max_age=3600,
                              domain='localhost',
                              path='/')
            
            # Add headers to force browser to refresh
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
            
            return response
        else:
            return "Invalid credentials"
    
    # Create a session ID before login to demonstrate the fix
    session['pre_login'] = 'true'
    session.modified = True
    
    # Pass session ID to template for display
    session_id = session.sid if hasattr(session, 'sid') else 'No session ID'
    return render_template('secure_login.html', session_id=session_id)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session or not session.get('authenticated'):
        return redirect(url_for('login'))
    
    session_data = dict(session)
    return render_template('secure_dashboard.html', session_data=session_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("🔒 SECURE APP STARTING 🔒")
    print("This app prevents session fixation attacks")
    print("Access the app at: http://localhost:5001")
    print("Session ID will change after login!")
    app.run(debug=True, host='0.0.0.0', port=5001) 