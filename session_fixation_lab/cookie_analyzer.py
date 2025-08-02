#!/usr/bin/env python3
"""
Cookie Analyzer - Demonstrates Session Fixation Attack
This tool helps analyze cookies and demonstrate the attack.
"""

import requests
from urllib.parse import urljoin

class CookieAnalyzer:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_session_info(self):
        """Get current session information."""
        try:
            response = self.session.get(urljoin(self.base_url, '/login'))
            
            print("🔍 Session Analysis")
            print("=" * 50)
            print(f"URL: {response.url}")
            print(f"Status Code: {response.status_code}")
            print(f"All Cookies: {dict(self.session.cookies)}")
            
            # Flask-Session only creates cookies when session data is stored
            # So we need to trigger session creation by visiting a page that uses session
            print("Note: Flask-Session creates cookies only when session data is stored")
            print("No initial session cookie is expected - this is normal behavior")
            return None
                
        except Exception as e:
            print(f"Error getting session info: {e}")
            return None
    
    def login(self, username, password):
        """Attempt to login and capture session."""
        try:
            login_data = {
                'username': username,
                'password': password
            }
            
            response = self.session.post(
                urljoin(self.base_url, '/login'),
                data=login_data,
                allow_redirects=True
            )
            
            print(f"\n🔐 Login Attempt")
            print("=" * 50)
            print(f"Username: {username}")
            print(f"Status Code: {response.status_code}")
            print(f"Final URL: {response.url}")
            print(f"Cookies after login: {dict(self.session.cookies)}")
            
            # Check for any session-related cookies
            session_cookies = [name for name in self.session.cookies.keys() if 'session' in name.lower()]
            if session_cookies:
                session_id = self.session.cookies[session_cookies[0]]
                print(f"Session ID after login: {session_id}")
                return session_id
            else:
                print("No session cookie after login")
                return None
                
        except Exception as e:
            print(f"Error during login: {e}")
            return None
    
    def access_dashboard(self):
        """Try to access dashboard with current session."""
        try:
            response = self.session.get(urljoin(self.base_url, '/dashboard'))
            
            print(f"\n🏠 Dashboard Access")
            print("=" * 50)
            print(f"Status Code: {response.status_code}")
            print(f"URL: {response.url}")
            
            if response.status_code == 200:
                print("✅ Successfully accessed dashboard")
                # Extract user info from response
                if 'Welcome' in response.text:
                    print("✅ User is authenticated")
                else:
                    print("❌ User not authenticated")
            else:
                print("❌ Failed to access dashboard")
                
        except Exception as e:
            print(f"Error accessing dashboard: {e}")
    
    def demonstrate_session_fixation(self):
        """Demonstrate session fixation attack."""
        print("\n🎯 Session Fixation Attack Demonstration")
        print("=" * 60)
        
        # Step 1: Get session after login (simulating attacker capturing session)
        print("Step 1: Simulating attacker capturing session after victim login")
        
        # First login to get a session
        login_session = self.login('admin', 'admin123')
        
        if not login_session:
            print("❌ Could not get session after login")
            return
        
        print(f"Session ID captured: {login_session}")
        
        # Step 2: Demonstrate the vulnerability
        print(f"\nStep 2: Testing if session persists")
        print(f"Session ID: {login_session}")
        
        # Step 3: Try to access dashboard with captured session
        print(f"\nStep 3: Testing access with captured session")
        self.access_dashboard()
        
        # Show the vulnerability
        print(f"\n🚨 VULNERABILITY ANALYSIS 🚨")
        print(f"Session ID: {login_session}")
        print(f"If this session ID doesn't change after logout/login,")
        print(f"it indicates session fixation vulnerability.")

def main():
    print("🍪 Cookie Analyzer - Session Fixation Demo")
    print("=" * 60)
    
    # Test vulnerable app
    print("\n1. Testing VULNERABLE app (port 5000)")
    vulnerable_analyzer = CookieAnalyzer("http://localhost:5000")
    
    try:
        vulnerable_analyzer.demonstrate_session_fixation()
    except Exception as e:
        print(f"Error testing vulnerable app: {e}")
        print("Make sure vulnerable_app.py is running on port 5000")
    
    print("\n" + "=" * 60)
    
    # Test secure app
    print("\n2. Testing SECURE app (port 5001)")
    secure_analyzer = CookieAnalyzer("http://localhost:5001")
    
    try:
        # Test secure app by logging in twice and comparing session IDs
        print("Testing secure app session regeneration...")
        
        # First login
        session1 = secure_analyzer.login('admin', 'admin123')
        if not session1:
            print("❌ First login failed")
            return
            
        print(f"First session ID: {session1}")
        
        # Logout
        secure_analyzer.session.get(f"{secure_analyzer.base_url}/logout")
        
        # Second login
        session2 = secure_analyzer.login('admin', 'admin123')
        if not session2:
            print("❌ Second login failed")
            return
            
        print(f"Second session ID: {session2}")
        
        # Compare session IDs
        if session1 != session2:
            print(f"✅ Session ID changed: {session1} -> {session2}")
            print("✅ Session fixation attack prevented!")
        else:
            print(f"❌ Session ID unchanged: {session1}")
            print("❌ Still vulnerable to session fixation!")
                
    except Exception as e:
        print(f"Error testing secure app: {e}")
        print("Make sure secure_app.py is running on port 5001")

if __name__ == "__main__":
    main() 