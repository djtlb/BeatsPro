import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_ai_lyrics_generation():
    """Test the new AI lyrics generation endpoint"""
    print("🤖 Testing AI Lyrics Generation...")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "Pop Love Song",
            "data": {
                "prompt": "A song about falling in love under the stars",
                "genre": "Pop",
                "style": "romantic"
            }
        },
        {
            "name": "Rock Anthem",
            "data": {
                "prompt": "Fighting against injustice and standing up for what's right",
                "genre": "Rock",
                "style": "epic"
            }
        },
        {
            "name": "Country Heartbreak",
            "data": {
                "prompt": "Lost love on a dusty highway",
                "genre": "Country",
                "style": "sad"
            }
        },
        {
            "name": "Electronic Dance",
            "data": {
                "prompt": "Dancing all night in neon lights",
                "genre": "electronic",
                "style": "energetic"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🎵 {test_case['name']}:")
        print("-" * 40)
        
        try:
            response = requests.post(f"{BASE_URL}/generate_lyrics", json=test_case['data'])
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"✅ SUCCESS!")
                    print(f"Prompt: {test_case['data']['prompt']}")
                    print(f"Genre: {test_case['data']['genre']} | Style: {test_case['data']['style']}")
                    
                    lyrics = result.get('lyrics', '')
                    if isinstance(lyrics, str):
                        print(f"\n🎼 Generated Lyrics:")
                        print(lyrics[:300] + "..." if len(lyrics) > 300 else lyrics)
                    
                    if result.get('model_info'):
                        model_info = result['model_info']
                        print(f"\n🔧 Model: {model_info.get('model', 'Unknown')}")
                        print(f"Device: {model_info.get('device', 'Unknown')}")
                else:
                    print(f"⚠️  Failed: {result.get('error', 'Unknown error')}")
                    if result.get('lyrics'):
                        print(f"Fallback lyrics: {result['lyrics'][:100]}...")
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)

def test_full_song_generation():
    """Test the enhanced song generation with AI lyrics"""
    print("🎵 Testing Full Song Generation with AI Lyrics...")
    print("=" * 60)
    
    test_data = {
        "prompt": "An epic adventure song about exploring space",
        "genre": "rock",
        "mood": "epic"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate_song", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Full Song Generated Successfully!")
            
            song_data = result.get('song_data', {})
            print(f"\n🎵 Song: {song_data.get('title', 'Unknown')}")
            print(f"Genre: {song_data.get('genre')} | Mood: {song_data.get('mood')}")
            print(f"Duration: {song_data.get('duration_formatted')} | BPM: {song_data.get('bpm')}")
            print(f"Key: {song_data.get('key')} | Instruments: {', '.join(song_data.get('instruments', []))}")
            
            lyrics_preview = result.get('lyrics_preview', {})
            print(f"\n🎼 Lyrics Preview:")
            print(f"AI Generated: {lyrics_preview.get('ai_generated', False)}")
            if lyrics_preview.get('full_lyrics'):
                full_lyrics = lyrics_preview['full_lyrics']
                print(full_lyrics[:400] + "..." if len(full_lyrics) > 400 else full_lyrics)
            else:
                print(f"Verse: {lyrics_preview.get('verse_1', 'N/A')}")
                print(f"Chorus: {lyrics_preview.get('chorus', 'N/A')}")
            
            print(f"\n💾 File: {song_data.get('audio_file')} ({song_data.get('file_size_mb')} MB)")
            print(f"Location: {song_data.get('download_location', 'Unknown')}")
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)

def test_lyrics_variants():
    """Test generating multiple lyrics variants"""
    print("🎨 Testing Multiple Lyrics Variants...")
    print("=" * 60)
    
    test_data = {
        "prompt": "A song about friendship and loyalty",
        "genre": "Pop",
        "style": "happy",
        "num_variants": 3
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate_lyrics", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                lyrics = result.get('lyrics', [])
                
                if isinstance(lyrics, list):
                    print(f"✅ Generated {len(lyrics)} variants!")
                    for i, variant in enumerate(lyrics, 1):
                        print(f"\n🎵 Variant {i}:")
                        print("-" * 30)
                        print(variant[:200] + "..." if len(variant) > 200 else variant)
                else:
                    print("✅ Single variant generated:")
                    print(lyrics[:200] + "..." if len(lyrics) > 200 else lyrics)
            else:
                print(f"⚠️  Failed: {result.get('error')}")
        else:
            print(f"❌ Error {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)

def interactive_lyrics_demo():
    """Interactive demo for AI lyrics generation"""
    print("🎤 Interactive AI Lyrics Demo")
    print("=" * 60)
    print("Enter your prompts to generate AI lyrics in real-time!")
    print("Type 'quit' to exit\n")
    
    while True:
        prompt = input("🎵 Enter your song idea: ").strip()
        if prompt.lower() == 'quit':
            break
        
        genre = input("🎸 Genre (pop/rock/country/electronic/jazz): ").strip() or "pop"
        style = input("💫 Style (happy/sad/epic/romantic/energetic): ").strip() or "happy"
        
        print(f"\n🤖 Generating AI lyrics for: '{prompt}'...")
        
        try:
            data = {
                "prompt": prompt,
                "genre": genre,
                "style": style
            }
            
            response = requests.post(f"{BASE_URL}/generate_lyrics", json=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    lyrics = result.get('lyrics', '')
                    print(f"\n🎼 Your AI-Generated Lyrics:")
                    print("=" * 40)
                    print(lyrics)
                    print("=" * 40)
                    
                    model_info = result.get('model_info', {})
                    print(f"Generated by: {model_info.get('model', 'AI')}")
                else:
                    print(f"⚠️  AI generation failed: {result.get('error')}")
                    if result.get('lyrics'):
                        print(f"Fallback lyrics: {result['lyrics']}")
            else:
                print(f"❌ Server error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Can't connect to server. Make sure Flask is running!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "-" * 60 + "\n")

if __name__ == "__main__":
    print("🎵 SunoAI + GPT-2 Lyrics Generator Test Suite")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✅ Server is running!")
        print("=" * 60)
    except:
        print("❌ Server not running! Start the Flask app first.")
        exit(1)
    
    # Run tests
    test_ai_lyrics_generation()
    test_full_song_generation()
    test_lyrics_variants()
    
    # Interactive demo
    print("\n🎤 Ready for interactive demo!")
    interactive_lyrics_demo()
    
    print("\n👋 Thanks for testing SunoAI with AI Lyrics!")
