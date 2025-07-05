#!/usr/bin/env python3
"""
🤖 INSTANT BOT PRODUCTION STARTER 🤖
Run this to immediately start producing music!
"""

import os
import sys
from datetime import datetime
import traceback
import time

def create_minimal_fallback():
    """Create minimal fallback system if full AI not available"""
    fallback_code = '''
import numpy as np
from scipy.io.wavfile import write
import random

class FallbackProducer:
    def __init__(self):
        self.sr = 44100
        self.bpm = 140
        
    def generate_beat(self, duration=8.0):
        samples = int(self.sr * duration)
        beat = np.zeros(samples)
        
        # Simple kick pattern
        kick_freq = 60
        for i in range(0, int(duration), 1):
            start = int(i * self.sr)
            t = np.linspace(0, 0.5, int(0.5 * self.sr))
            kick = np.sin(2 * np.pi * kick_freq * t) * np.exp(-t * 5)
            end = min(start + len(kick), samples)
            beat[start:end] += kick[:end-start] * 0.8
        
        return beat
    
    def export_beat(self, audio, filename):
        audio_16bit = (np.clip(audio, -1, 1) * 32767).astype(np.int16)
        write(f"{filename}.wav", self.sr, audio_16bit)
        return f"{filename}.wav"
'''
    
    with open("fallback_producer.py", 'w') as f:
        f.write(fallback_code)
    print("✅ Fallback system created")

def start_bot_immediately():
    """Start bot production immediately with multiple fallback options"""
    print("🤖" * 30)
    print("🚀 STARTING MUSIC PRODUCTION BOT NOW! 🚀")
    print("🤖" * 30)
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Initializing...")
    
    # Try full system first
    try:
        print("🧠 Loading full AI system...")
        from bot_production_launcher import BotProductionStarter
        
        bot = BotProductionStarter()
        if bot.components_loaded:
            print("✅ Full AI system ready!")
            print("\n🎵 LAUNCHING FULL PRODUCTION SESSION 🎵")
            
            # Start immediate production
            session_result = bot.start_production_session()
            
            print(f"\n🎉 PRODUCTION COMPLETE!")
            print(f"Generated {session_result['tracks_generated']} professional tracks")
            print("Check your folder for the new music files!")
            return True
        else:
            raise ImportError("Components not fully loaded")
            
    except Exception as e:
        print(f"⚠️ Full system error: {e}")
        print("🔄 Trying alternative launch methods...")
        
        # Try direct launch
        try:
            print("🎹 Attempting direct AI launch...")
            from ai_production_bot import AIProductionBot
            from modern_rap_generator import ModernRapGenerator
            
            bot = AIProductionBot()
            lyric_gen = ModernRapGenerator()
            
            print("✅ Direct AI system loaded!")
            
            # Quick 3-track production
            presets = ["hyperpop_2025", "drill_uk", "phonk_wave"]
            
            for i, preset in enumerate(presets, 1):
                print(f"\n🎵 Generating track {i}/3: {preset}")
                
                bot.load_preset(preset)
                song = lyric_gen.create_full_song(f"AI Track {i}")
                audio = bot._produce_full_track(duration=8.0)
                
                timestamp = datetime.now().strftime("%H%M%S")
                filename = f"ai_track_{timestamp}_{i}_{preset}"
                
                bot.export_production(audio, filename)
                
                with open(f"{filename}_lyrics.txt", 'w') as f:
                    f.write(lyric_gen.export_lyrics(song))
                
                print(f"✅ Track {i} complete!")
            
            print(f"\n🎊 3 AI TRACKS GENERATED!")
            return True
            
        except Exception as e2:
            print(f"⚠️ Direct launch failed: {e2}")
            print("🔧 Creating fallback system...")
            
            # Create and use fallback
            try:
                create_minimal_fallback()
                from fallback_producer import FallbackProducer
                
                producer = FallbackProducer()
                print("✅ Fallback system active!")
                
                # Generate simple beats
                for i in range(3):
                    print(f"\n🥁 Generating simple beat {i+1}/3")
                    beat = producer.generate_beat(duration=6.0)
                    filename = f"fallback_beat_{datetime.now().strftime('%H%M%S')}_{i+1}"
                    producer.export_beat(beat, filename)
                    print(f"✅ Beat {i+1} exported: {filename}.wav")
                
                print(f"\n🎵 3 FALLBACK BEATS GENERATED!")
                return True
                
            except Exception as e3:
                print(f"❌ All systems failed: {e3}")
                print("🛠️ Please check dependencies and try again")
                return False

def main():
    print("🎵" * 20)
    print("🤖 MUSIC PRODUCTION BOT STARTING 🤖")
    print("🎵" * 20)
    print(f"⏰ Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Auto-start immediately
    print("\n🚀 AUTO-STARTING PRODUCTION...")
    
    try:
        success = start_bot_immediately()
        
        if success:
            print(f"\n✨ BOT PRODUCTION COMPLETE! ✨")
            print("🎧 Your music files are ready in this folder!")
            print("🔥 Bot successfully generated fresh tracks!")
        else:
            print(f"\n⚠️ Bot encountered issues but tried multiple fallbacks")
            print("Check error messages above for troubleshooting")
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        traceback.print_exc()
        print("\n🔧 Quick fixes to try:")
        print("  1. Run: pip install numpy scipy")
        print("  2. Ensure all .py files are in same folder")
        print("  3. Run: python debug_production_system.py")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
