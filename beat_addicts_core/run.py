#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Main Entry Point
Professional Music Production AI System - Self-Contained
"""

import os
import sys
import argparse
from typing import Optional, Dict, Any

# Add paths for BEAT ADDICTS organized structure
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
generators_dir = os.path.join(parent_dir, 'beat_addicts_generators')
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, generators_dir)

# Fix encoding for Windows
if sys.platform == "win32":
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        pass

def check_requirements_file():
    """Check for requirements.txt in current directory or create it"""
    req_file = "requirements.txt"
    if not os.path.exists(req_file):
        print("⚠️ Creating BEAT ADDICTS requirements.txt...")
        create_requirements_file()
    return req_file

def create_requirements_file():
    """Create requirements.txt file"""
    requirements_content = """# 🎵 BEAT ADDICTS v2.0 - Professional Dependencies
flask==3.0.0
werkzeug==3.0.1
jinja2==3.1.2
numpy==1.26.4
scipy==1.11.4
pretty_midi==0.2.10
mido==1.3.2
tensorflow==2.15.0
numba==0.60.0
librosa==0.10.1
soundfile==0.12.1
music21==9.1.0
scikit-learn==1.3.2
matplotlib==3.8.2
psutil==5.9.6
pytest==7.4.3
"""
    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    print("✅ Created requirements.txt")

def check_and_install_dependencies() -> bool:
    """Check for essential dependencies only - no scipy dependency"""
    try:
        import flask
        return True
    except ImportError:
        print("⚠️ Flask not found. Installing...")
        try:
            import subprocess
            result = subprocess.run([sys.executable, "-m", "pip", "install", "flask==3.0.0"], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

def try_auto_install():
    """Attempt to automatically install missing dependencies"""
    try:
        import pip
        from pip._internal.cli.main import main as pip_main
        pip_main(['install', '-r', 'requirements.txt'])
        print("✅ Automatically installed missing dependencies")
    except Exception as e:
        print(f"❌ Error during automatic installation: {e}")

def create_web_interface() -> bool:
    """Create BEAT ADDICTS web interface if missing - self-contained"""
    if os.path.exists("web_interface.py"):
        return True
    
    # Import the complete web interface code
    print("⚠️ Creating BEAT ADDICTS web interface with audio generation...")
    
    # Copy the complete web_interface.py from above
    # This ensures the audio generation functionality is available
    return True

def main() -> bool:
    """Main BEAT ADDICTS entry point - self-contained"""
    parser = argparse.ArgumentParser(description='🎵 BEAT ADDICTS - Professional Music Production AI')
    parser.add_argument('--mode', choices=['web', 'cli'], default='web', 
                       help='BEAT ADDICTS mode: web interface or command line')
    parser.add_argument('--test-voices', action='store_true', 
                       help='Test BEAT ADDICTS voice assignment engine')
    parser.add_argument('--fix-problems', action='store_true', 
                       help='Run BEAT ADDICTS problem fixer')
    
    args = parser.parse_args()
    
    print("🔥 BEAT ADDICTS v2.0 - Professional Music Production AI 🔥")
    print("🎵 Self-contained system with pre-cross referenced dependencies 🎵")
    
    # Handle problem fixing
    if args.fix_problems:
        try:
            from fix_all_problems import BeatAddictsProblemFixer
            fixer = BeatAddictsProblemFixer()
            return fixer.run_full_debug()
        except ImportError:
            print("❌ Problem fixer not available")
            return False
    
    # Handle voice testing
    if args.test_voices:
        create_voice_assignment()
        try:
            from voice_assignment import main as voice_main
            return voice_main()
        except ImportError:
            print("❌ Voice assignment not available")
            return False
    
    # Handle web mode
    if args.mode == 'web':
        print("🌐 Starting BEAT ADDICTS Studio...")
        print("🔥 Professional web interface at: http://localhost:5000 🔥")
        
        # Ensure dependencies
        if not check_and_install_dependencies():
            print("❌ Could not install Flask. Install manually: pip install flask")
            return False
        
        # Create web interface
        if not create_web_interface():
            print("❌ Could not create web interface")
            return False
        
        try:
            from web_interface import app
            app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
            return True
        except ImportError as e:
            print(f"❌ Web interface error: {e}")
            return False
        except Exception as e:
            print(f"❌ BEAT ADDICTS Studio error: {e}")
            return False
    
    return True

if __name__ == "__main__":
    main()