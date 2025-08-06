#!/usr/bin/env python3
"""
BANK APP - The real bank application where users normally log in
This represents the legitimate bank website that the attacker wants to access.
"""

from flask import Flask, request, session, redirect, url_for, render_template, flash
from flask_session import Session
import secrets
from database import init_database, register_user, verify_user, get_user_info

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Strong secret key
app.config['SESSION_TYPE'] = 'filesystem'

# SECURE: Proper cookie security configurations
app.config['SESSION_COOKIE_HTTPONLY'] = True   # Prevents JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Prevents CSRF
app.config['SESSION_COOKIE_SECURE'] = False    # Allow HTTP for demo

Session(app)

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
            session.clear()
            session['user_id'] = username
            session['login_time'] = '2025-01-15T10:30:00Z'
            session['authenticated'] = True
            
            print(f"[BANK] User {username} logged in successfully")
            print(f"[BANK] New session ID generated for security")
            
            return redirect(url_for('bank_dashboard'))
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
    if 'user_id' not in session:
        return redirect(url_for('bank_login'))
    
    username = session['user_id']
    user_info = get_user_info(username)
    
    if not user_info:
        flash('User information not found!', 'error')
        return redirect(url_for('bank_logout'))
    
    session_data = dict(session)
    
    return render_template('bank_dashboard.html', 
                         user_info=user_info,
                         session_data=session_data)

@app.route('/bank/logout')
def bank_logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('bank_login'))

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

@app.route('/bank/logout')
def bank_logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('bank_login'))

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