import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:5000"

def test_home():
    """Test the home endpoint"""
    print("Testing home endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)

def test_generate_song():
    """Test the song generation endpoint"""
    print("Testing song generation endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/generate_song")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)

def test_downloads():
    """Test the downloads endpoint to see where files are saved"""
    print("Testing downloads endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/downloads")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Download Directory: {data['download_info']['absolute_path']}")
            print(f"Directory Exists: {data['download_info']['exists']}")
            print(f"Total Songs: {data['total_songs']}")
            if data['generated_songs']:
                print("Generated Songs:")
                for song in data['generated_songs']:
                    print(f"  - {song['filename']} ({song['size_mb']} MB)")
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)

if __name__ == "__main__":
    print("SunoAI API Test Script")
    print("=" * 50)
    
    test_home()
    test_generate_song()
    test_downloads()
    
    print("Test completed!")
