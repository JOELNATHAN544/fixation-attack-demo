#!/usr/bin/env python3
"""
Hacker Dashboard - Web app that looks like a normal login app
This represents a malicious application where both users and hackers can log in.
"""

from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_session import Session
import os
import bcrypt

app = Flask(__name__)
app.secret_key = 'hacker_secret_key_123'

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session'
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

Session(app)

# Simulated user database (normal users)
USERS = {
    'user123': {
        'password': bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()),
        'email': 'user123@example.com',
        'role': 'user',
        'name': 'User Account'
    },
    'admin': {
        'password': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()),
        'email': 'admin@company.com',
        'role': 'admin',
        'name': 'Administrator'
    }
}

# Simulated stolen session IDs and their associated user data
STOLEN_SESSIONS = {
    'GZlKSxUWk7vYrRma8lkbrIp-id7-LWwM8qdHemnkoFE': {
        'username': 'user123',
        'email': 'user123@example.com',
        'role': 'admin',
        'name': 'Stolen User Account',
        'stolen_from': 'vulnerable_app',
        'stolen_time': '2024-01-15 14:30:00',
        'is_stolen': True
    },
    'mt7ObtEQxmFTlhkU7cRDHyF49ligOZP2yHHlTIppZhM': {
        'username': 'admin',
        'email': 'admin@company.com',
        'role': 'super_admin',
        'name': 'Stolen Admin Account',
        'stolen_from': 'vulnerable_app',
        'stolen_time': '2024-01-15 15:45:00',
        'is_stolen': True
    },
    'abc123def456ghi789': {
        'username': 'john_doe',
        'email': 'john.doe@corp.com',
        'role': 'user',
        'name': 'Stolen John Doe Account',
        'stolen_from': 'vulnerable_app',
        'stolen_time': '2024-01-15 16:20:00',
        'is_stolen': True
    }
}

@app.route('/')
def index():
    """Main page - looks like a normal company login."""
    return render_template('normal_login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page that accepts both normal credentials and stolen session IDs."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        session_id = request.form.get('session_id')
        
        # Check if it's a stolen session ID login
        if session_id and session_id in STOLEN_SESSIONS:
            user_data = STOLEN_SESSIONS[session_id]
            session['logged_in'] = True
            session['user_data'] = user_data
            session['login_method'] = 'stolen_session'
            session['stolen_session_id'] = session_id
            
            print(f"🎭 HACKER LOGIN SUCCESS!")
            print(f"Stolen Session ID: {session_id}")
            print(f"Stolen from user: {user_data['username']}")
            print(f"User role: {user_data['role']}")
            
            return redirect(url_for('dashboard'))
        
        # Check if it's a normal user login
        elif username and password and username in USERS:
            stored_password = USERS[username]['password']
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                user_data = USERS[username].copy()
                user_data['username'] = username
                user_data['is_stolen'] = False
                
                session['logged_in'] = True
                session['user_data'] = user_data
                session['login_method'] = 'normal'
                
                print(f"👤 NORMAL USER LOGIN SUCCESS!")
                print(f"Username: {username}")
                print(f"Role: {user_data['role']}")
                
                return redirect(url_for('dashboard'))
        
        # Invalid login
        return render_template('normal_login.html', error="Invalid credentials or session ID")
    
    return render_template('normal_login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard showing user information."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    user_data = session.get('user_data')
    login_method = session.get('login_method')
    stolen_session_id = session.get('stolen_session_id')
    
    return render_template('normal_dashboard.html', 
                         user_data=user_data, 
                         login_method=login_method,
                         session_id=stolen_session_id)

@app.route('/logout')
def logout():
    """Logout."""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create flask_session directory if it doesn't exist
    os.makedirs('./flask_session', exist_ok=True)
    
    print("🏢 COMPANY LOGIN SYSTEM STARTING...")
    print("=" * 40)
    print("This looks like a normal company login system.")
    print("But hackers can also log in using stolen session IDs!")
    print()
    print("👤 Normal users can log in with:")
    print("  user123/password123")
    print("  admin/admin123")
    print()
    print("🎭 Hackers can log in with stolen session IDs:")
    for session_id, data in STOLEN_SESSIONS.items():
        print(f"  {session_id} -> {data['username']} ({data['role']})")
    print()
    print("🌐 Access at: http://localhost:5002")
    print("💡 This looks like a normal app but has a backdoor!")
    
    app.run(host='0.0.0.0', port=5002, debug=True) 