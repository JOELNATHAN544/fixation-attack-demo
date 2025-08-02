#!/usr/bin/env python3
"""
VULNERABLE Flask App - Demonstrates Session Fixation Attack
DO NOT USE IN PRODUCTION!
"""

from flask import Flask, request, session, redirect, url_for
from flask_session import Session
import bcrypt

app = Flask(__name__)
app.secret_key = 'vulnerable_secret_key'  # Weak secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    
    return '''
    <h2>Vulnerable Login System</h2>
    <p style="color: red;">⚠️ This app is intentionally vulnerable to session fixation!</p>
    <form method="post">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <input type="submit" value="Login">
    </form>
    <p><strong>Test accounts:</strong></p>
    <ul>
        <li>admin / admin123</li>
        <li>user1 / password123</li>
    </ul>
    <p><em>Note: Session ID will remain the same after login</em></p>
    '''

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return f'''
    <h2>Welcome {session['user_id']}!</h2>
    <p>Login time: {session['login_time']}</p>
    <p style="color: red;">⚠️ Session fixation vulnerability active!</p>
    <p><strong>Session Data:</strong> {dict(session)}</p>
    <a href="/logout">Logout</a>
    '''

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