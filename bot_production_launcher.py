import os
import sys
import time
import threading
from datetime import datetime
import json

class BotProductionStarter:
    def __init__(self):
        self.session_active = False
        self.auto_mode = True
        self.production_queue = []
        self.current_project = None
        
        # Import AI components
        try:
            from ai_production_bot import AIProductionBot
            from modern_rap_generator import ModernRapGenerator
            self.ai_bot = AIProductionBot()
            self.lyric_gen = ModernRapGenerator()
            self.components_loaded = True
            print("✅ AI components loaded successfully")
        except ImportError as e:
            print(f"⚠️  Some components missing: {e}")
            self.components_loaded = False
    
    def start_production_session(self):
        """Start automated production session"""
        print("\n🤖 STARTING BOT PRODUCTION SESSION 🤖")
        print("=" * 50)
        
        self.session_active = True
        session_start = datetime.now()
        
        # Auto-generate multiple tracks
        session_tracks = []
        
        presets = ["hyperpop_2025", "drill_uk", "phonk_wave", "jersey_club"]
        
        for i, preset in enumerate(presets, 1):
            print(f"\n🎵 Track {i}/{len(presets)}: {preset}")
            print("-" * 30)
            
            try:
                # Load preset
                self.ai_bot.load_preset(preset)
                
                # Generate lyrics
                song_title = f"Bot Track {i} - {preset.replace('_', ' ').title()}"
                lyrics = self.lyric_gen.create_full_song(song_title)
                
                # Produce audio
                audio = self.ai_bot._produce_full_track(duration=12.0)
                
                # Export
                timestamp = datetime.now().strftime("%H%M%S")
                base_name = f"bot_session_{timestamp}_{preset}"
                
                audio_file, metadata_file = self.ai_bot.export_production(audio, base_name)
                
                # Save lyrics
                lyrics_file = f"{base_name}_lyrics.txt"
                with open(lyrics_file, 'w') as f:
                    f.write(self.lyric_gen.export_lyrics(lyrics))
                
                track_info = {
                    "title": song_title,
                    "preset": preset,
                    "files": {
                        "audio": audio_file,
                        "lyrics": lyrics_file,
                        "metadata": metadata_file
                    },
                    "timestamp": datetime.now().isoformat()
                }
                
                session_tracks.append(track_info)
                print(f"✅ Track {i} complete: {song_title}")
                
                # Brief pause between tracks
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error on track {i}: {e}")
                continue
        
        # Save session summary
        session_duration = (datetime.now() - session_start).total_seconds()
        session_summary = {
            "session_start": session_start.isoformat(),
            "session_duration_seconds": session_duration,
            "tracks_generated": len(session_tracks),
            "tracks": session_tracks,
            "ai_settings": {
                "creativity_factor": self.ai_bot.ai_brain.creativity_factor,
                "learning_sessions": len(self.ai_bot.session_data)
            }
        }
        
        summary_file = f"bot_session_{session_start.strftime('%Y%m%d_%H%M%S')}_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(session_summary, f, indent=2)
        
        print(f"\n🎉 SESSION COMPLETE!")
        print(f"⏱️  Duration: {session_duration:.1f} seconds")
        print(f"🎵 Tracks generated: {len(session_tracks)}")
        print(f"📋 Session summary: {summary_file}")
        
        self.session_active = False
        return session_summary
    
    def quick_fire_mode(self, count=3):
        """Rapid-fire track generation"""
        print(f"\n🔥 QUICK FIRE MODE - {count} TRACKS 🔥")
        print("=" * 40)
        
        for i in range(count):
            print(f"\n⚡ Quick track {i+1}/{count}")
            
            # Random preset
            import random
            preset = random.choice(["hyperpop_2025", "drill_uk", "phonk_wave"])
            self.ai_bot.load_preset(preset)
            
            # Quick generation (shorter duration)
            audio = self.ai_bot._produce_full_track(duration=8.0)
            
            # Quick export
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"quickfire_{timestamp}_{i+1}"
            self.ai_bot.export_production(audio, filename)
            
            print(f"✅ Quick track {i+1} done!")
    
    def interactive_mode(self):
        """Interactive production mode"""
        print("\n🎛️ INTERACTIVE BOT MODE 🎛️")
        print("Commands: 'generate', 'preset [name]', 'quit'")
        
        while True:
            command = input("\n🤖 Bot> ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'generate':
                self._interactive_generate()
            elif command.startswith('preset '):
                preset_name = command.split(' ', 1)[1]
                if self.ai_bot.load_preset(preset_name):
                    print(f"✅ Loaded: {preset_name}")
                else:
                    print(f"❌ Unknown preset: {preset_name}")
            elif command == 'help':
                self._show_help()
            else:
                print("❓ Unknown command. Type 'help' for options.")
    
    def _interactive_generate(self):
        """Generate track in interactive mode"""
        print("🎹 Generating track...")
        try:
            audio = self.ai_bot._produce_full_track(duration=10.0)
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"interactive_{timestamp}"
            self.ai_bot.export_production(audio, filename)
            print("✅ Track generated!")
        except Exception as e:
            print(f"❌ Generation failed: {e}")
    
    def _show_help(self):
        """Show help information"""
        print("\n📖 BOT COMMANDS:")
        print("  generate     - Create new track")
        print("  preset [name] - Load production preset")
        print("  quit         - Exit interactive mode")
        print("\n🎛️ AVAILABLE PRESETS:")
        for preset in self.ai_bot.presets.keys():
            print(f"  - {preset}")
    
    def monitor_mode(self):
        """Background monitoring and auto-production"""
        print("\n👁️ MONITOR MODE ACTIVE")
        print("Bot will auto-generate tracks every 5 minutes...")
        
        track_counter = 1
        
        while self.session_active:
            try:
                print(f"\n🤖 Auto-generating track #{track_counter}...")
                
                # Random preset selection
                import random
                preset = random.choice(list(self.ai_bot.presets.keys()))
                self.ai_bot.load_preset(preset)
                
                # Generate
                audio = self.ai_bot._produce_full_track(duration=8.0)
                
                # Export with auto-naming
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"auto_{timestamp}_{track_counter:03d}"
                self.ai_bot.export_production(audio, filename)
                
                print(f"✅ Auto-track #{track_counter} complete")
                track_counter += 1
                
                # Wait 5 minutes
                time.sleep(300)
                
            except KeyboardInterrupt:
                print("\n⏹️ Monitor mode stopped")
                break
            except Exception as e:
                print(f"❌ Auto-generation error: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    def launch_bot(self):
        """Main bot launcher"""
        if not self.components_loaded:
            print("❌ Cannot start - missing components")
            return
        
        print("🚀 BOT PRODUCTION LAUNCHER 🚀")
        print("Choose mode:")
        print("1. Auto Session (4 tracks)")
        print("2. Quick Fire (3 tracks)")
        print("3. Interactive Mode")
        print("4. Monitor Mode")
        print("5. Exit")
        
        while True:
            choice = input("\nSelect mode (1-5): ").strip()
            
            if choice == '1':
                self.start_production_session()
                break
            elif choice == '2':
                self.quick_fire_mode()
                break
            elif choice == '3':
                self.interactive_mode()
                break
            elif choice == '4':
                self.session_active = True
                self.monitor_mode()
                break
            elif choice == '5':
                print("👋 Bot shutdown")
                break
            else:
                print("❓ Invalid choice")

if __name__ == "__main__":
    launcher = BotProductionStarter()
    launcher.launch_bot()
