#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime
import traceback

def start_bot():
    """Launch the music production bot immediately"""
    
    print("🤖" * 20)
    print("🚀 LAUNCHING MUSIC PRODUCTION BOT 🚀")
    print("🤖" * 20)
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Bot starting...")
    
    # Try to import and start components
    try:
        # First try the full system
        print("🧠 Loading AI brain...")
        from ai_production_bot import AIProductionBot
        from modern_rap_generator import ModernRapGenerator
        
        # Initialize bot
        bot = AIProductionBot()
        lyric_gen = ModernRapGenerator()
        
        print("✅ Full AI system loaded!")
        
        # Auto-start production
        print("\n🎵 STARTING AUTO-PRODUCTION 🎵")
        print("Generating 3 tracks with different styles...")
        
        presets = ["hyperpop_2025", "drill_uk", "phonk_wave"]
        generated_files = []
        
        for i, preset in enumerate(presets, 1):
            print(f"\n🎹 Track {i}/3: {preset}")
            
            try:
                # Load preset
                bot.load_preset(preset)
                
                # Generate lyrics
                song = lyric_gen.create_full_song(f"Bot Track {i}")
                
                # Generate audio (optimized duration)
                audio = bot._produce_full_track(duration=8.0)
                
                # Export
                timestamp = datetime.now().strftime("%H%M%S")
                filename = f"bot_track_{timestamp}_{i}_{preset}"
                
                audio_file, metadata_file = bot.export_production(audio, filename)
                
                # Save lyrics
                lyrics_file = f"{filename}_lyrics.txt"
                with open(lyrics_file, 'w') as f:
                    f.write(lyric_gen.export_lyrics(song))
                
                generated_files.extend([audio_file, lyrics_file, metadata_file])
                print(f"✅ Track {i} complete!")
                
            except Exception as track_error:
                print(f"⚠️ Error on track {i}: {track_error}")
                continue
        
        print("\n🎉 BOT PRODUCTION COMPLETE!")
        print(f"Generated {len([f for f in generated_files if f.endswith('.wav')])} tracks")
        print("Check your folder for the new tracks!")
        return True
        
    except ImportError as e:
        print(f"⚠️ Full system not available: {e}")
        print("🔄 Trying minimal version...")
        
        try:
            # Create simple fallback on the fly
            import numpy as np
            
            print("✅ Creating simple beats with numpy...")
            
            # Generate simple beats
            for i in range(3):
                print(f"\n🥁 Simple beat {i+1}/3")
                
                # Create basic beat
                duration = 4.0
                sr = 44100
                t = np.linspace(0, duration, int(sr * duration))
                
                # Simple kick + noise pattern
                beat = np.zeros(len(t))
                
                # Add kicks every beat
                for beat_pos in range(4):
                    start_idx = int(beat_pos * sr)
                    kick_samples = int(0.3 * sr)
                    if start_idx + kick_samples < len(beat):
                        kick = np.sin(2 * np.pi * 60 * t[:kick_samples]) * np.exp(-t[:kick_samples] * 8)
                        beat[start_idx:start_idx + kick_samples] += kick * 0.8
                
                # Add hi-hats
                for eighth in range(8):
                    start_idx = int(eighth * sr * 0.5)
                    hat_samples = int(0.1 * sr)
                    if start_idx + hat_samples < len(beat):
                        hat = np.random.uniform(-0.3, 0.3, hat_samples) * np.exp(-t[:hat_samples] * 20)
                        beat[start_idx:start_idx + hat_samples] += hat
                
                # Export using scipy
                try:
                    from scipy.io.wavfile import write
                    filename = f"simple_beat_{datetime.now().strftime('%H%M%S')}_{i+1}"
                    audio_16bit = (np.clip(beat, -1, 1) * 32767).astype(np.int16)
                    write(f"{filename}.wav", sr, audio_16bit)
                    print(f"✅ Beat {i+1} exported: {filename}.wav")
                except ImportError:
                    print(f"⚠️ Cannot export beat {i+1} - scipy not available")
            
            print("\n🎵 Simple beats complete!")
            return True
            
        except Exception as simple_error:
            print(f"❌ Simple fallback failed: {simple_error}")
            
            # Last resort - just create placeholder files
            print("📝 Creating placeholder files...")
            for i in range(3):
                filename = f"placeholder_track_{i+1}_{datetime.now().strftime('%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write(f"AI Music Bot Track {i+1}\n")
                    f.write(f"Generated: {datetime.now()}\n")
                    f.write("This is a placeholder - install dependencies for audio generation\n")
                print(f"📄 Created: {filename}")
            
            print("🔧 To get audio generation working:")
            print("  pip install numpy scipy soundfile")
            return False
    
    except Exception as e:
        print(f"❌ Bot error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Bot launching in 3 seconds...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("🎵 GO!")
    
    if start_bot():
        print("\n🎤 Bot session complete!")
        print("🔥 Fresh music generated!")
    else:
        print("\n🛠️ Bot needs setup - check error messages above")
        print("💡 Try installing: pip install numpy scipy soundfile")
    
    input("\nPress Enter to exit...")
