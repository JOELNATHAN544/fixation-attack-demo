#!/usr/bin/env python3
"""
HACKER'S MALICIOUS LOGIN PAGE - Session Fixation Attack
This looks like the bank login but is actually the attacker's fake page.
DO NOT USE IN PRODUCTION!
"""

from flask import Flask, request, session, redirect, url_for, render_template, make_response
from flask_session import Session
import bcrypt

app = Flask(__name__)
app.secret_key = 'hacker_secret_key'  # Weak secret key
app.config['SESSION_TYPE'] = 'filesystem'

# VULNERABLE: Missing or weak cookie security configurations
app.config['SESSION_COOKIE_HTTPONLY'] = False  # Allows JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = None   # Allows cross-site requests
app.config['SESSION_COOKIE_SECURE'] = False    # Allows HTTP transmission

Session(app)

# Override Flask-Session defaults for vulnerable app
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SAMESITE'] = None

# Fake user database (hacker's fake credentials)
FAKE_USERS = {
    'john': bcrypt.hashpw('john123'.encode('utf-8'), bcrypt.gensalt(rounds=12)),
    'alice': bcrypt.hashpw('alice123'.encode('utf-8'), bcrypt.gensalt(rounds=12)),
    'bob': bcrypt.hashpw('bob123'.encode('utf-8'), bcrypt.gensalt(rounds=12))
}

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('fake_dashboard'))
    return redirect(url_for('fake_login'))

@app.route('/login', methods=['GET', 'POST'])
def fake_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in FAKE_USERS and verify_password(password, FAKE_USERS[username]):
            # VULNERABLE: Session ID remains the same - SESSION FIXATION!
            # The session ID was set before login and remains unchanged
            session['user_id'] = username
            session['login_time'] = '2025-01-15T10:30:00Z'
            session['fake_login'] = True
            
            print(f"[HACKER] Victim {username} logged in with existing session ID")
            print(f"[HACKER] Session ID unchanged: {session.sid if hasattr(session, 'sid') else 'Unknown'}")
            print(f"[HACKER] Now hacker can use this session ID to access victim's bank account!")
            
            return redirect(url_for('fake_dashboard'))
        else:
            return "Invalid credentials"
    
    # VULNERABLE: Allow session ID to be set via URL parameter
    # This simulates an attacker setting a session ID
    session_id_param = request.args.get('session_id')
    if session_id_param:
        print(f"[HACKER] Session ID set via URL parameter: {session_id_param}")
        print(f"[HACKER] Victim will use this session ID when they log in")
        # In a real attack, the hacker would set this session ID
        # and the victim would unknowingly use it
    
    # Create a session ID before login to demonstrate the vulnerability
    session['pre_login'] = 'true'
    session.modified = True
    
    # Pass session ID to template for display
    session_id = session.sid if hasattr(session, 'sid') else 'No session ID'
    return render_template('vulnerable_login.html', session_id=session_id)

@app.route('/dashboard')
def fake_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('fake_login'))
    
    session_data = dict(session)
    return render_template('vulnerable_dashboard.html', session_data=session_data)

@app.route('/logout')
def fake_logout():
    session.clear()
    return redirect(url_for('fake_login'))

if __name__ == '__main__':
    print("🚨 HACKER'S MALICIOUS LOGIN PAGE STARTING 🚨")
    print("This looks like the bank but is actually the attacker's fake page!")
    print("Access the fake login at: http://localhost:5000/login")
    print("Session ID will remain the same after login!")
    app.run(debug=True, host='0.0.0.0', port=5000) 