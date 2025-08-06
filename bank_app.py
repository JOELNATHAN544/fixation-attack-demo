#!/usr/bin/env python3
"""
BANK APP - The real bank application where users normally log in
This represents the legitimate bank website that the attacker wants to access.
"""

from flask import Flask, request, session, redirect, url_for, render_template, flash, make_response
import secrets
import json
import base64
import hmac
import hashlib
from database import init_database, register_user, verify_user, get_user_info

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Strong secret key

# SECURE: Proper cookie security configurations
app.config['SESSION_COOKIE_HTTPONLY'] = True   # Prevents JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Prevents CSRF
app.config['SESSION_COOKIE_SECURE'] = False    # Allow HTTP for demo

def create_session_cookie(data):
    """Create a signed session cookie"""
    # Convert data to JSON and encode
    json_data = json.dumps(data, separators=(',', ':'))
    encoded_data = base64.urlsafe_b64encode(json_data.encode()).decode()
    
    # Create signature
    signature = hmac.new(
        app.secret_key.encode(),
        encoded_data.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return f"{encoded_data}.{signature}"

def verify_session_cookie(cookie_value):
    """Verify and decode session cookie"""
    try:
        encoded_data, signature = cookie_value.split('.', 1)
        
        # Verify signature
        expected_signature = hmac.new(
            app.secret_key.encode(),
            encoded_data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            return None
        
        # Decode data
        json_data = base64.urlsafe_b64decode(encoded_data).decode()
        return json.loads(json_data)
    except:
        return None

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('bank_dashboard'))
    return redirect(url_for('bank_login'))

@app.route('/bank/register', methods=['GET', 'POST'])
def bank_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('bank_register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters!', 'error')
            return render_template('bank_register.html')
        
        success, message = register_user(username, password)
        if success:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('bank_login'))
        else:
            flash(message, 'error')
            return render_template('bank_register.html')
    
    return render_template('bank_register.html')

@app.route('/bank/login', methods=['GET', 'POST'])
def bank_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        success, message = verify_user(username, password)
        if success:
            # SECURE: Regenerate session ID to prevent session fixation
            # Get old session data for comparison
            old_cookie = request.cookies.get('session', '')
            old_session_data = verify_session_cookie(old_cookie) if old_cookie else None
            old_session_id = old_session_data.get('_id', 'Unknown') if old_session_data is not None else 'Unknown'
            
            # Generate completely new session data
            import secrets
            new_session_id = secrets.token_urlsafe(32)
            
            # Create new session data
            new_session_data = {
                'user_id': username,
                'login_time': '2025-01-15T10:30:00Z',
                'authenticated': True,
                '_id': new_session_id
            }
            
            # Create new session cookie
            new_cookie_value = create_session_cookie(new_session_data)
            
            # Create response with redirect
            response = make_response(redirect(url_for('bank_dashboard')))
            
            # Delete old session cookie
            response.delete_cookie('session', domain='localhost', path='/')
            
            # Set new session cookie
            response.set_cookie(
                'session',
                new_cookie_value,
                httponly=True,
                samesite='Strict',
                secure=False,
                max_age=3600,
                domain='localhost'
            )
            
            print(f"[BANK] User {username} logged in successfully")
            print(f"[BANK] Old session ID: {old_session_id}")
            print(f"[BANK] New session ID: {new_session_id}")
            print(f"[BANK] Session ID changed: {old_session_id != new_session_id}")
            print(f"[BANK] Old cookie: {old_cookie[:50]}...")
            print(f"[BANK] New cookie: {new_cookie_value[:50]}...")
            
            return response
        else:
            flash(message, 'error')
            return render_template('bank_login.html')
    
    # Create a session when someone visits the login page
    # This allows the hacker to capture the session ID
    session['visitor'] = 'true'
    session.modified = True
    
    return render_template('bank_login.html')

@app.route('/bank/dashboard')
def bank_dashboard():
    # Get session data from cookie
    cookie_value = request.cookies.get('session', '')
    session_data = verify_session_cookie(cookie_value) if cookie_value else {}
    
    if 'user_id' not in session_data:
        return redirect(url_for('bank_login'))
    
    username = session_data['user_id']
    user_info = get_user_info(username)
    
    if not user_info:
        flash('User information not found!', 'error')
        return redirect(url_for('bank_logout'))
    
    return render_template('bank_dashboard.html', 
                         user_info=user_info,
                         session_data=session_data)

@app.route('/bank/logout')
def bank_logout():
    response = make_response(redirect(url_for('bank_login')))
    response.delete_cookie('session', domain='localhost', path='/')
    flash('You have been logged out successfully.', 'success')
    return response

if __name__ == '__main__':
    print("🏦 BANK APP STARTING 🏦")
    print("This is the legitimate bank website")
    print("Access the bank at: http://localhost:5001/bank/login")
    print("Database will be initialized automatically")
    
    # Initialize database
    if init_database():
        print("✅ Database ready")
    else:
        print("❌ Database initialization failed")
        print("Make sure PostgreSQL is running with Docker:")
        print("docker-compose up -d")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 