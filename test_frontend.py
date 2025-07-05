#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Frontend Test & Repair
Test the generation system and fix any errors
"""

import requests
import json
import time

def test_beat_generation():
    """Test beat generation endpoint"""
    print("🎵 Testing BEAT ADDICTS Frontend...")
    
    # Test data
    test_data = {
        "prompt": "upbeat summer vibes",
        "genre": "electronic",
        "mood": "energetic",
        "duration": 30  # Short test
    }
    
    try:
        print("🚀 Sending generation request...")
        response = requests.post(
            'http://localhost:5000/drop_beat',
            json=test_data,
            timeout=60
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Generation successful!")
            print(f"   Title: {result['result']['title']}")
            print(f"   Genre: {result['result']['genre']}")
            print(f"   Duration: {result['result']['duration']}s")
            print(f"   File: {result['result']['filename']}")
            print(f"   Size: {result['result']['file_size']}")
            return True
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the server running?")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_frontend_interface():
    """Test if frontend loads"""
    try:
        print("🌐 Testing frontend interface...")
        response = requests.get('http://localhost:5000', timeout=10)
        
        if response.status_code == 200:
            print("✅ Frontend loads successfully")
            return True
        else:
            print(f"❌ Frontend error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎵 BEAT ADDICTS MVP - Frontend Testing & Repair")
    print("=" * 50)
    
    # Test frontend
    frontend_ok = test_frontend_interface()
    
    if frontend_ok:
        # Test generation
        generation_ok = test_beat_generation()
        
        if generation_ok:
            print("\n✅ BEAT ADDICTS MVP is working!")
            print("🎵 Ready for music production!")
        else:
            print("\n⚠️ Generation needs repair")
    else:
        print("\n❌ Frontend needs repair")

if __name__ == "__main__":
    main()
