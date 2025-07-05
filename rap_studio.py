from modern_rap_generator import ModernRapGenerator
from premium_audio_engine import PremiumAudioEngine
import json
import os
from datetime import datetime

class RapStudio:
    def __init__(self):
        self.lyric_gen = ModernRapGenerator()
        self.audio_engine = PremiumAudioEngine()
        
    def create_complete_track(self, title=None, style="aggressive", duration=16.0):
        """Generate complete rap track with lyrics and beat"""
        if not title:
            title = f"Generated Track {datetime.now().strftime('%H%M%S')}"
        
        print(f"🎵 Creating '{title}'...")
        
        # Generate lyrics
        song = self.lyric_gen.create_full_song(title)
        lyrics = self.lyric_gen.export_lyrics(song)
        
        # Generate beat
        print("🥁 Generating drums...")
        drums = self.audio_engine.create_trap_pattern(duration)
        
        print("🎸 Adding bass...")
        bass = self.audio_engine.generate_bass_808('E', duration)
        
        # Mix track
        print("🎛️ Mixing...")
        full_track = drums + bass * 0.6
        
        # Save files
        base_name = title.lower().replace(' ', '_')
        
        # Save lyrics
        lyrics_file = f"{base_name}_lyrics.txt"
        with open(lyrics_file, 'w') as f:
            f.write(lyrics)
        
        # Save audio
        audio_file = f"{base_name}_beat.wav"
        self.audio_engine.export_wav(full_track, audio_file)
        
        # Save project info
        project_info = {
            "title": title,
            "style": style,
            "duration": duration,
            "bpm": self.audio_engine.bpm,
            "created": datetime.now().isoformat(),
            "files": {
                "lyrics": lyrics_file,
                "audio": audio_file
            }
        }
        
        project_file = f"{base_name}_project.json"
        with open(project_file, 'w') as f:
            json.dump(project_info, f, indent=2)
        
        print(f"✅ Track complete!")
        print(f"📝 Lyrics: {lyrics_file}")
        print(f"🎵 Audio: {audio_file}")
        print(f"📋 Project: {project_file}")
        
        return project_info
    
    def quick_demo(self):
        """Generate a quick demo track"""
        print("🚀 Generating quick demo...")
        return self.create_complete_track("2025 Flex Demo", duration=8.0)

if __name__ == "__main__":
    studio = RapStudio()
    
    print("🎤 RAP STUDIO 2025 🎤")
    print("=" * 30)
    
    # Generate demo
    project = studio.quick_demo()
    
    print(f"\n🎉 Demo created: '{project['title']}'")
    print("Check the generated files in your folder!")
