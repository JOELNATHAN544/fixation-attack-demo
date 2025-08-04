#!/usr/bin/env python3
"""
Test Session Change - Simple test to verify session regeneration
"""

import requests
import time

def test_session_regeneration():
    """Test if session ID actually changes in the browser."""
    
    print("🧪 Testing Session Regeneration")
    print("=" * 40)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Step 1: Visit login page and get initial session
    print("1. Visiting login page...")
    response = session.get('http://localhost:5001/login')
    print(f"   Status: {response.status_code}")
    
    # Get initial session cookie
    initial_cookies = dict(session.cookies)
    print(f"   Initial cookies: {initial_cookies}")
    
    # Step 2: Login to trigger session regeneration
    print("\n2. Logging in...")
    login_data = {'username': 'admin', 'password': 'admin123'}
    response = session.post('http://localhost:5001/login', data=login_data)
    print(f"   Status: {response.status_code}")
    
    # Get cookies after login
    final_cookies = dict(session.cookies)
    print(f"   Final cookies: {final_cookies}")
    
    # Step 3: Check if session ID changed
    print("\n3. Analyzing session change...")
    
    if 'session' in initial_cookies and 'session' in final_cookies:
        old_session = initial_cookies['session']
        new_session = final_cookies['session']
        
        print(f"   Old session ID: {old_session}")
        print(f"   New session ID: {new_session}")
        
        if old_session != new_session:
            print("   ✅ Session ID changed successfully!")
            return True
        else:
            print("   ❌ Session ID did not change!")
            return False
    else:
        print("   ❌ Session cookies not found!")
        return False

if __name__ == '__main__':
    test_session_regeneration() 