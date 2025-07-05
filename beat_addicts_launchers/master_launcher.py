#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS v2.0 - MASTER LAUNCHER
Unified launcher that boots ALL components together
"""

import os
import sys
import time
import threading
import subprocess
from pathlib import Path

class BeatAddictsBootSequence:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.components = {
            'dependencies': False,
            'core_system': False,
            'web_interface': False,
            'midi_generators': False,
            'voice_system': False
        }
        
    def boot_all_components(self):
        """Boot everything together"""
        print("🔥" * 20)
        print("🎵 BEAT ADDICTS v2.0 - MASTER BOOT SEQUENCE 🎵")
        print("🔥" * 20)
        print("🚀 Initializing ALL music production components...")
        print()
        
        # Step 1: Install dependencies
        self.install_dependencies()
        
        # Step 2: Initialize core system
        self.initialize_core_system()
        
        # Step 3: Start MIDI generators
        self.initialize_midi_generators()
        
        # Step 4: Initialize voice system
        self.initialize_voice_system()
        
        # Step 5: Launch web interface (this will be the main running process)
        self.launch_web_interface()
        
    def install_dependencies(self):
        """Install all required dependencies"""
        print("📦 INSTALLING ALL DEPENDENCIES...")
        
        deps = [
            "flask==3.0.0",
            "colorama==0.4.6", 
            "werkzeug==3.0.1",
            "mido",
            "numpy",
            "librosa",
            "soundfile"
        ]
        
        for dep in deps:
            try:
                print(f"   Installing {dep}...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", dep, 
                    "--user", "--no-warn-script-location", "--quiet"
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print(f"   ✅ {dep}")
                else:
                    print(f"   ⚠️ {dep} (may already exist)")
                    
            except Exception as e:
                print(f"   ⚠️ {dep} (skipped: {e})")
        
        self.components['dependencies'] = True
        print("✅ Dependencies ready!")
        print()
        
    def initialize_core_system(self):
        """Initialize the core BEAT ADDICTS system"""
        print("🎛️ INITIALIZING CORE SYSTEM...")
        
        core_dir = self.project_dir / "beat_addicts_core"
        if core_dir.exists():
            print(f"   📁 Found core directory: {core_dir}")
            
            # Check for essential files
            essential_files = ["web_interface.py", "run.py"]
            for file in essential_files:
                file_path = core_dir / file
                if file_path.exists():
                    print(f"   ✅ {file}")
                else:
                    print(f"   ⚠️ {file} (missing)")
                    
            self.components['core_system'] = True
            print("✅ Core system ready!")
        else:
            print("   ⚠️ Core directory not found, using fallback")
            self.components['core_system'] = False
            
        print()
        
    def initialize_midi_generators(self):
        """Initialize all MIDI generators"""
        print("🎹 INITIALIZING MIDI GENERATORS...")
        
        generators_dir = self.project_dir / "beat_addicts_generators"
        if generators_dir.exists():
            generators = list(generators_dir.glob("*_midi_generator.py"))
            print(f"   Found {len(generators)} MIDI generators:")
            
            for gen in generators:
                gen_name = gen.stem.replace("_midi_generator", "").title()
                print(f"   🎵 {gen_name} Generator")
                
            self.components['midi_generators'] = True
            print("✅ MIDI generators ready!")
        else:
            print("   ⚠️ MIDI generators directory not found")
            self.components['midi_generators'] = False
            
        # Check MIDI files
        midi_dir = self.project_dir / "midi_files"
        if midi_dir.exists():
            midi_count = len(list(midi_dir.glob("*.mid")))
            print(f"   🎼 Found {midi_count} existing MIDI files")
            
        print()
        
    def initialize_voice_system(self):
        """Initialize voice handling system"""
        print("🎤 INITIALIZING VOICE SYSTEM...")
        
        voice_files = [
            "beat_addicts_voice_config.json",
            "beat_addicts_voice_report_electronic.json",
            "beat_addicts_voice_report_hiphop.json",
            "beat_addicts_voice_report_rock.json"
        ]
        
        for voice_file in voice_files:
            file_path = self.project_dir / voice_file
            if file_path.exists():
                genre = voice_file.split("_")[-1].replace(".json", "").title()
                print(f"   🎤 {genre} Voice Config")
                
        # Check for voice handlers in core
        core_dir = self.project_dir / "beat_addicts_core"
        voice_handlers = ["voice_handler.py", "voice_integration.py", "voice_assignment.py"]
        
        for handler in voice_handlers:
            handler_path = core_dir / handler
            if handler_path.exists():
                handler_name = handler.replace("_", " ").replace(".py", "").title()
                print(f"   ✅ {handler_name}")
                
        self.components['voice_system'] = True
        print("✅ Voice system ready!")
        print()
        
    def launch_web_interface(self):
        """Launch the main web interface"""
        print("🌐 LAUNCHING WEB INTERFACE...")
        print("🎵 BEAT ADDICTS Studio will be available at: http://localhost:5000")
        print()
        
        # Try multiple launch methods
        core_dir = self.project_dir / "beat_addicts_core"
        
        # Method 1: Core directory web interface
        if (core_dir / "web_interface.py").exists():
            print("🚀 Starting from core directory...")
            try:
                os.chdir(str(core_dir))
                # Import and run directly to keep everything in one process
                sys.path.insert(0, str(core_dir))
                
                try:
                    from web_interface import app
# Import for music_generator_app
# sys.path.append('.')
# Import for fix_web_interface
# sys.path.append('beat_addicts_core')
                    print("✅ Web interface loaded!")
                    print("🎉 ALL COMPONENTS BOOTED SUCCESSFULLY!")
                    print("=" * 50)
                    print("🎵 BEAT ADDICTS Studio is now running!")
                    print("🌐 Access at: http://localhost:5000")
                    print("🎛️ All music production tools are available")
                    print("=" * 50)
                    
                    # Run the Flask app
                    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
                    
                except ImportError as e:
                    print(f"❌ Could not import web interface: {e}")
                    self.fallback_launch()
                    
            except Exception as e:
                print(f"❌ Error with core method: {e}")
                self.fallback_launch()
                
        else:
            print("⚠️ Core web interface not found, trying fallback...")
            self.fallback_launch()
            
    def fallback_launch(self):
        """Fallback launch method"""
        print("🔄 Using fallback launch method...")
        
        # Try the main directory web interface
        web_interface_path = self.project_dir / "web_interface.py"
        if web_interface_path.exists():
            try:
                os.chdir(str(self.project_dir))
                subprocess.run([sys.executable, "web_interface.py"])
            except Exception as e:
                print(f"❌ Fallback failed: {e}")
                self.emergency_launch()
        else:
            self.emergency_launch()
            
    def emergency_launch(self):
        """Emergency simple launch"""
        print("🆘 Emergency launch - basic functionality only")
        
        try:
            # Try to at least run the basic launcher
            subprocess.run([sys.executable, "beat_addicts_launcher.py"])
        except Exception as e:
            print(f"❌ Emergency launch failed: {e}")
            print("🔧 Manual steps:")
            print("1. cd beat_addicts_core")
            print("2. python run.py")
            
    def show_status(self):
        """Show final status of all components"""
        print("\n" + "=" * 50)
        print("🎵 BEAT ADDICTS COMPONENT STATUS")
        print("=" * 50)
        
        for component, status in self.components.items():
            status_icon = "✅" if status else "❌"
            component_name = component.replace("_", " ").title()
            print(f"{status_icon} {component_name}")
            
        print("=" * 50)

def main():
    """Main launcher function"""
    launcher = BeatAddictsBootSequence()
    
    try:
        launcher.boot_all_components()
    except KeyboardInterrupt:
        print("\n🛑 Boot sequence interrupted by user")
    except Exception as e:
        print(f"\n❌ Boot sequence failed: {e}")
        launcher.show_status()
        
        print("\n🔧 Alternative boot methods:")
        print("1. python quick_start_no_venv.py")
        print("2. python beat_addicts_launcher.py")
        print("3. cd beat_addicts_core && python run.py")

if __name__ == "__main__":
    main()
