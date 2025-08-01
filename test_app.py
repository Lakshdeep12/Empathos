#!/usr/bin/env python3
"""
Simple test script for Empathos application
"""

import requests
import time

def test_app():
    """Test basic application functionality"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Empathos Application...")
    print("=" * 50)
    
    # Test 1: Home page
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Home page accessible")
        else:
            print(f"❌ Home page error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to application: {e}")
        return False
    
    # Test 2: Login page
    try:
        response = requests.get(f"{base_url}/login", timeout=5)
        if response.status_code == 200:
            print("✅ Login page accessible")
        else:
            print(f"❌ Login page error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Login page error: {e}")
    
    # Test 3: Register page
    try:
        response = requests.get(f"{base_url}/register", timeout=5)
        if response.status_code == 200:
            print("✅ Register page accessible")
        else:
            print(f"❌ Register page error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Register page error: {e}")
    
    # Test 4: Awareness page
    try:
        response = requests.get(f"{base_url}/awareness", timeout=5)
        if response.status_code == 200:
            print("✅ Awareness page accessible")
        else:
            print(f"❌ Awareness page error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Awareness page error: {e}")
    
    print("=" * 50)
    print("🎉 Basic functionality tests completed!")
    print("\n📋 Next Steps:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. Register as an individual user")
    print("3. Register as an authority member")
    print("4. Test the chatbot functionality")
    print("5. Submit help requests")
    print("6. Test the admin dashboard")
    
    return True

if __name__ == "__main__":
    # Wait a moment for the app to start
    print("⏳ Waiting for application to start...")
    time.sleep(3)
    
    test_app() 