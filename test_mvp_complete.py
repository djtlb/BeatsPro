#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Comprehensive Frontend Testing
Test all genres and features to ensure MVP is complete
"""

import requests
import json
import time

def test_all_genres():
    """Test all available genres"""
    print("🎵 Testing All BEAT ADDICTS Genres...")
    
    genres = [
        "electronic",
        "hip-hop", 
        "dnb",
        "rock",
        "country",
        "futuristic"
    ]
    
    results = []
    
    for genre in genres:
        print(f"\n🎼 Testing {genre.upper()} generation...")
        
        test_data = {
            "prompt": f"fresh {genre} beat",
            "genre": genre,
            "mood": "energetic",
            "duration": 15  # Quick test
        }
        
        try:
            response = requests.post(
                'http://localhost:5000/drop_beat',
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ {genre}: {result['result']['filename']} ({result['result']['file_size']})")
                results.append((genre, True, result['result']['filename']))
            else:
                print(f"   ❌ {genre}: Failed - {response.status_code}")
                results.append((genre, False, f"Error {response.status_code}"))
                
        except Exception as e:
            print(f"   ❌ {genre}: Exception - {e}")
            results.append((genre, False, str(e)))
    
    return results

def test_different_durations():
    """Test different song durations"""
    print("\n⏱️ Testing Different Durations...")
    
    durations = [10, 30, 60]  # Short tests
    
    for duration in durations:
        print(f"\n🕒 Testing {duration}s duration...")
        
        test_data = {
            "prompt": "test beat",
            "genre": "electronic",
            "mood": "energetic", 
            "duration": duration
        }
        
        try:
            response = requests.post(
                'http://localhost:5000/drop_beat',
                json=test_data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                actual_duration = result['result']['duration']
                print(f"   ✅ {duration}s: Generated {actual_duration}s ({result['result']['file_size']})")
            else:
                print(f"   ❌ {duration}s: Failed")
                
        except Exception as e:
            print(f"   ❌ {duration}s: Error - {e}")

def test_download_endpoint():
    """Test download functionality"""
    print("\n⬇️ Testing Download Endpoint...")
    
    # First generate a beat
    test_data = {
        "prompt": "download test",
        "genre": "electronic",
        "duration": 10
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/drop_beat',
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            filename = result['result']['filename']
            
            # Test download
            download_response = requests.get(f'http://localhost:5000/download/{filename}')
            
            if download_response.status_code == 200:
                print(f"   ✅ Download working: {filename}")
                return True
            else:
                print(f"   ❌ Download failed: {download_response.status_code}")
                return False
        else:
            print("   ❌ Could not generate test file for download")
            return False
            
    except Exception as e:
        print(f"   ❌ Download test error: {e}")
        return False

def main():
    """Run comprehensive tests"""
    print("🎵 BEAT ADDICTS MVP - Comprehensive Frontend Testing")
    print("=" * 60)
    
    # Test all genres
    genre_results = test_all_genres()
    
    # Test durations
    test_different_durations()
    
    # Test downloads
    download_ok = test_download_endpoint()
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    successful_genres = sum(1 for _, success, _ in genre_results if success)
    total_genres = len(genre_results)
    
    print(f"📊 Genre Tests: {successful_genres}/{total_genres} passed")
    for genre, success, info in genre_results:
        status = "✅" if success else "❌"
        print(f"   {status} {genre}: {info}")
    
    print(f"⬇️ Download Test: {'✅ Passed' if download_ok else '❌ Failed'}")
    
    # Overall status
    all_genres_ok = successful_genres == total_genres
    mvp_ready = all_genres_ok and download_ok
    
    print("\n" + "=" * 60)
    if mvp_ready:
        print("🎉 BEAT ADDICTS MVP IS FULLY OPERATIONAL!")
        print("🎵 Ready for production use!")
    else:
        print("⚠️ Some features need attention")
    print("=" * 60)

if __name__ == "__main__":
    main()
