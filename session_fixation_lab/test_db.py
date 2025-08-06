#!/usr/bin/env python3
"""
Test database connection
"""

from database import get_db_connection, init_database

def test_connection():
    print("🔍 Testing Database Connection")
    print("=" * 40)
    
    # Test connection
    conn = get_db_connection()
    if conn:
        print("✅ Database connection successful!")
        conn.close()
    else:
        print("❌ Database connection failed!")
        print("Make sure PostgreSQL container is running:")
        print("docker ps")
        return False
    
    # Test initialization
    if init_database():
        print("✅ Database initialization successful!")
        return True
    else:
        print("❌ Database initialization failed!")
        return False

if __name__ == '__main__':
    if test_connection():
        print("\n🎉 Database is ready for the session fixation lab!")
    else:
        print("\n❌ Database setup failed. Check your multipass k3s instance.") 