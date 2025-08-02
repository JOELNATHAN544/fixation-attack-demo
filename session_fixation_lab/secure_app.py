#!/usr/bin/env python3
"""
SECURE Flask App - Prevents Session Fixation Attack
"""

from flask import Flask, request, session, redirect, url_for
from flask_session import Session
import bcrypt
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Strong secret key
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
            # SECURE: Regenerate session ID to prevent session fixation
            # Clear the session and create a new one
            session.clear()
            
            # Create new session data
            session['user_id'] = username
            session['login_time'] = '2025-01-15T10:30:00Z'
            session['authenticated'] = True
            
            print(f"[SECURE] User {username} logged in with NEW session ID")
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    
    return '''
    <h2>Secure Login System</h2>
    <p style="color: green;">✅ This app prevents session fixation attacks!</p>
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
    <p><em>Note: Session ID will change after successful login</em></p>
    '''

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session or not session.get('authenticated'):
        return redirect(url_for('login'))
    
    return f'''
    <h2>Welcome {session['user_id']}!</h2>
    <p>Login time: {session['login_time']}</p>
    <p><strong>Session Data:</strong> {dict(session)}</p>
    <p style="color: green;">✅ Session fixation attack prevented!</p>
    <a href="/logout">Logout</a>
    '''

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