#!/usr/bin/env python3
"""
BANK APP - The real bank application where users normally log in
This represents the legitimate bank website that the attacker wants to access.
"""

from flask import Flask, request, session, redirect, url_for, render_template
from flask_session import Session
import bcrypt
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Strong secret key
app.config['SESSION_TYPE'] = 'filesystem'

# SECURE: Proper cookie security configurations
app.config['SESSION_COOKIE_HTTPONLY'] = True   # Prevents JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Prevents CSRF
app.config['SESSION_COOKIE_SECURE'] = False    # Allow HTTP for demo

Session(app)

# Bank user database
BANK_USERS = {
    'john': bcrypt.hashpw('john123'.encode('utf-8'), bcrypt.gensalt(rounds=12)),
    'alice': bcrypt.hashpw('alice123'.encode('utf-8'), bcrypt.gensalt(rounds=12)),
    'bob': bcrypt.hashpw('bob123'.encode('utf-8'), bcrypt.gensalt(rounds=12))
}

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('bank_dashboard'))
    return redirect(url_for('bank_login'))

@app.route('/bank/login', methods=['GET', 'POST'])
def bank_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in BANK_USERS and verify_password(password, BANK_USERS[username]):
            # SECURE: Regenerate session ID to prevent session fixation
            session.clear()
            session['user_id'] = username
            session['login_time'] = '2025-01-15T10:30:00Z'
            session['account_type'] = 'premium'
            session['authenticated'] = True
            
            print(f"[BANK] User {username} logged in successfully")
            print(f"[BANK] New session ID generated for security")
            
            return redirect(url_for('bank_dashboard'))
        else:
            return "Invalid credentials"
    
    # Create a session when someone visits the login page
    # This allows the hacker to capture the session ID
    session['visitor'] = 'true'
    session.modified = True
    
    return render_template('bank_login.html')

@app.route('/bank/dashboard')
def bank_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('bank_login'))
    
    user = session['user_id']
    session_data = dict(session)
    
    # Bank account information
    account_info = {
        'john': {'balance': '$50,000', 'account_number': '1234-5678-9012'},
        'alice': {'balance': '$75,000', 'account_number': '2345-6789-0123'},
        'bob': {'balance': '$25,000', 'account_number': '3456-7890-1234'}
    }
    
    user_account = account_info.get(user, {'balance': '$0', 'account_number': 'N/A'})
    
    return render_template('bank_dashboard.html', 
                         user=user, 
                         session_data=session_data,
                         account_info=user_account)

@app.route('/bank/logout')
def bank_logout():
    session.clear()
    return redirect(url_for('bank_login'))

if __name__ == '__main__':
    print("🏦 BANK APP STARTING 🏦")
    print("This is the legitimate bank website")
    print("Access the bank at: http://localhost:5001/bank/login")
    print("Test accounts: john/john123, alice/alice123, bob/bob123")
    app.run(debug=True, host='0.0.0.0', port=5001) 