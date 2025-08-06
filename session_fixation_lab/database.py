#!/usr/bin/env python3
"""
Database management for the bank application
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt

# Database configuration for existing PostgreSQL container
DB_CONFIG = {
    'host': '10.72.220.223',  # k3s instance IP
    'port': 5432,
    'database': 'bank_db',
    'user': 'bank_user',  # Use the user we created
    'password': 'bank_password'  # Use the password we set
}

def get_db_connection():
    """Get database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

def init_database():
    """Initialize database tables."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database initialized successfully")
        return True
        
    except psycopg2.Error as e:
        print(f"Database initialization error: {e}")
        return False

def register_user(username, password):
    """Register a new user."""
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed"
    
    try:
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Username already exists"
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
        
        # Insert new user
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash.decode('utf-8'))
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ User '{username}' registered successfully")
        return True, "User registered successfully"
        
    except psycopg2.Error as e:
        print(f"Registration error: {e}")
        return False, f"Registration failed: {e}"

def verify_user(username, password):
    """Verify user credentials."""
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed"
    
    try:
        cursor = conn.cursor()
        
        # Get user by username
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not result:
            return False, "User not found"
        
        password_hash = result[0]
        
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return True, "Login successful"
        else:
            return False, "Invalid password"
            
    except psycopg2.Error as e:
        print(f"Verification error: {e}")
        return False, f"Verification failed: {e}"

def user_exists(username):
    """Check if user exists in database."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        exists = cursor.fetchone() is not None
        
        cursor.close()
        conn.close()
        
        return exists
        
    except psycopg2.Error as e:
        print(f"User check error: {e}")
        return False

def get_user_info(username):
    """Get user information."""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id, username, created_at FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return user
        
    except psycopg2.Error as e:
        print(f"Get user info error: {e}")
        return None 
"""
Database management for the bank application
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt

# Database configuration for existing PostgreSQL container
DB_CONFIG = {
    'host': '10.72.220.223',  # k3s instance IP
    'port': 5432,
    'database': 'bank_db',
    'user': 'bank_user',  # Use the user we created
    'password': 'bank_password'  # Use the password we set
}

def get_db_connection():
    """Get database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

def init_database():
    """Initialize database tables."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database initialized successfully")
        return True
        
    except psycopg2.Error as e:
        print(f"Database initialization error: {e}")
        return False

def register_user(username, password):
    """Register a new user."""
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed"
    
    try:
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Username already exists"
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
        
        # Insert new user
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash.decode('utf-8'))
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ User '{username}' registered successfully")
        return True, "User registered successfully"
        
    except psycopg2.Error as e:
        print(f"Registration error: {e}")
        return False, f"Registration failed: {e}"

def verify_user(username, password):
    """Verify user credentials."""
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed"
    
    try:
        cursor = conn.cursor()
        
        # Get user by username
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not result:
            return False, "User not found"
        
        password_hash = result[0]
        
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return True, "Login successful"
        else:
            return False, "Invalid password"
            
    except psycopg2.Error as e:
        print(f"Verification error: {e}")
        return False, f"Verification failed: {e}"

def user_exists(username):
    """Check if user exists in database."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        exists = cursor.fetchone() is not None
        
        cursor.close()
        conn.close()
        
        return exists
        
    except psycopg2.Error as e:
        print(f"User check error: {e}")
        return False

def get_user_info(username):
    """Get user information."""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id, username, created_at FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return user
        
    except psycopg2.Error as e:
        print(f"Get user info error: {e}")
        return None 