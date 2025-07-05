import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_basic_generation():
    """Test basic song generation without parameters"""
    print("🎵 Testing basic song generation...")
    response = requests.post(f"{BASE_URL}/generate_song")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Generated: {result['song_data']['title']}")
        print(f"   Genre: {result['song_data']['genre']} | Mood: {result['song_data']['mood']}")
        print(f"   Duration: {result['song_data']['duration_formatted']} | BPM: {result['song_data']['bpm']}")
        print(f"   Processing time: {result['generation_info']['processing_time_seconds']}s")
    else:
        print(f"❌ Error: {response.status_code}")
    print("-" * 60)

def test_custom_generation(prompt, genre=None, mood=None):
    """Test song generation with custom parameters"""
    print(f"🎵 Testing custom generation: '{prompt}'")
    data = {"prompt": prompt}
    if genre:
        data["genre"] = genre
    if mood:
        data["mood"] = mood
    
    response = requests.post(f"{BASE_URL}/generate_song", json=data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Generated: {result['song_data']['title']}")
        print(f"   Genre: {result['song_data']['genre']} | Mood: {result['song_data']['mood']}")
        print(f"   Instruments: {', '.join(result['song_data']['instruments'])}")
        print(f"   Lyrics preview: {result['lyrics_preview']['chorus']}")
        print(f"   File: {result['song_data']['audio_file']} ({result['song_data']['file_size_mb']} MB)")
    else:
        print(f"❌ Error: {response.status_code}")
    print("-" * 60)

def interactive_mode():
    """Interactive mode for live testing"""
    print("🎤 Interactive Song Generation Mode")
    print("Type 'quit' to exit\n")
    
    while True:
        prompt = input("Enter a song prompt (or 'quit'): ").strip()
        if prompt.lower() == 'quit':
            break
            
        genre = input("Enter genre (optional, press Enter to skip): ").strip() or None
        mood = input("Enter mood (optional, press Enter to skip): ").strip() or None
        
        print("\n🎵 Generating your song...")
        try:
            data = {"prompt": prompt}
            if genre:
                data["genre"] = genre
            if mood:
                data["mood"] = mood
                
            response = requests.post(f"{BASE_URL}/generate_song", json=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n🎉 SUCCESS! Generated: {result['song_data']['title']}")
                print(f"📊 Details:")
                print(f"   • Genre: {result['song_data']['genre']}")
                print(f"   • Mood: {result['song_data']['mood']}")
                print(f"   • Duration: {result['song_data']['duration_formatted']}")
                print(f"   • Key: {result['song_data']['key']} | BPM: {result['song_data']['bpm']}")
                print(f"   • Instruments: {', '.join(result['song_data']['instruments'])}")
                print(f"🎼 Lyrics Preview:")
                lyrics = result['lyrics_preview']
                print(f"   Verse: {lyrics['verse_1']}")
                print(f"   Chorus: {lyrics['chorus']}")
                print(f"   Verse: {lyrics['verse_2']}")
                print(f"💿 Audio: {result['song_data']['audio_file']} ({result['song_data']['file_size_mb']} MB)")
                print(f"⏱️  Generated in {result['generation_info']['processing_time_seconds']}s")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Can't connect to the server. Make sure Flask is running!")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    print("🎵 SunoAI Live Action Test Suite")
    print("=" * 60)
    
    # Test if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✅ Server is running!")
        print("=" * 60)
    except:
        print("❌ Server not running! Start the Flask app first.")
        exit(1)
    
    # Run some automated tests
    test_basic_generation()
    test_custom_generation("A happy summer song", "pop", "happy")
    test_custom_generation("Dark mysterious night", "rock", "mysterious")
    test_custom_generation("Smooth jazz for a rainy day", "jazz", "calm")
    
    # Enter interactive mode
    interactive_mode()
    
    print("👋 Thanks for testing SunoAI!")
