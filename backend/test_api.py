
#!/usr/bin/env python3
"""
Test script for the AI Health & Wellbeing Agent API
Run this to test the backend functionality
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health endpoint"""
    print("🔍 Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_chat():
    """Test the chat endpoint with sample queries"""
    print("\n🔍 Testing chat endpoint...")
    
    test_messages = [
        "Hello! Can you help me with health and fitness?",
        "I'm 25 years old, weigh 70kg, and am 175cm tall. Can you calculate my BMI?",
        "I'm feeling stressed and overwhelmed. Can you help?",
        "What are some good exercises for beginners?"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📨 Test Message {i}: {message}")
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": message},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response received:")
                print(f"🤖 Agent: {data['response'][:200]}...")
            else:
                print(f"❌ Chat request failed: {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Chat error: {e}")

def test_reset():
    """Test the reset endpoint"""
    print("\n🔍 Testing reset endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/reset")
        if response.status_code == 200:
            print("✅ Reset successful")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Reset failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Reset error: {e}")

if __name__ == "__main__":
    print("🚀 AI Health & Wellbeing Agent API Test Suite")
    print("=" * 50)
    
    # Run all tests
    test_health_check()
    test_chat()
    test_reset()
    
    print("\n" + "=" * 50)
    print("🏁 Test suite completed!")
    print("\n💡 To run the backend server:")
    print("   cd backend && python app.py")
    print("\n💡 To run the frontend:")
    print("   npm run dev")
