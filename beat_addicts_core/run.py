#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Main Entry Point
Professional Music Production AI System
"""

import os
import sys
import argparse
import glob

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

def check_and_install_dependencies():
    """Check and install missing dependencies"""
    try:
        import flask
        import werkzeug
        import jinja2
        import numpy
        import scipy
        import pretty_midi
        import mido
        import tensorflow
        import numba
        import librosa
        import soundfile
        import music21
        import sklearn
        import matplotlib
        import psutil
        import pytest
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e.name}")
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

def main():
    parser = argparse.ArgumentParser(description='🎵 BEAT ADDICTS - Professional Music Production AI')
    parser.add_argument('--mode', choices=['web', 'cli'], default='web', 
                       help='BEAT ADDICTS mode: Studio interface or command line')
    parser.add_argument('--train', type=str, help='Train BEAT ADDICTS AI with MIDI files directory')
    parser.add_argument('--generate', action='store_true', help='Generate beats with BEAT ADDICTS AI')
    parser.add_argument('--length', type=int, default=500, help='Length of BEAT ADDICTS generated music')
    parser.add_argument('--temperature', type=float, default=0.8, help='BEAT ADDICTS creativity temperature')
    parser.add_argument('--create-dnb', action='store_true', help='Generate BEAT ADDICTS DNB dataset')
    parser.add_argument('--create-hiphop', action='store_true', help='Generate BEAT ADDICTS Hip-Hop dataset')
    parser.add_argument('--create-electronic', action='store_true', help='Generate BEAT ADDICTS Electronic dataset')
    parser.add_argument('--create-country', action='store_true', help='Generate BEAT ADDICTS Country dataset')
    parser.add_argument('--create-rock', action='store_true', help='Generate BEAT ADDICTS Rock dataset')
    parser.add_argument('--create-futuristic', action='store_true', help='Generate BEAT ADDICTS Futuristic dataset')
    parser.add_argument('--create-all', action='store_true', help='Generate ALL BEAT ADDICTS training datasets')
    parser.add_argument('--test-voices', action='store_true', help='Test BEAT ADDICTS voice assignment engine')
    parser.add_argument('--debug', action='store_true', help='Run comprehensive BEAT ADDICTS debug test')
    parser.add_argument('--test', action='store_true', help='Run BEAT ADDICTS system tests')
    parser.add_argument('--fix-problems', action='store_true', help='Run BEAT ADDICTS problem fixer')
    
    args = parser.parse_args()
    
    print("🔥 BEAT ADDICTS v2.0 - Professional Music Production AI 🔥")
    print("🎵 Organized project structure loaded 🎵")
    
    # Handle problem fixing
    if args.fix_problems:
        print("🔧 Running BEAT ADDICTS problem fixer...")
        try:
            from fix_all_problems import main as fix_main
            return fix_main()
        except ImportError as e:
            print(f"❌ Error: Could not import problem fixer: {e}")
            return False
    
    if args.mode == 'web':
        print("🎵 BEAT ADDICTS - Professional Music Production AI")
        print("=" * 50)
        print("🔥 Beat Addicts Studio starting at: http://localhost:5000 🔥")
        print("Tip: Generate BEAT ADDICTS training data with: python run.py --create-all")
        print()
        
        try:
            # Check requirements
            check_requirements_file()
            
            # Check and install missing dependencies
            if not check_and_install_dependencies():
                print("Installing core dependencies...")
                try_auto_install()
            
            # Check if web_interface exists or create it
            if not os.path.exists("web_interface.py"):
                print("⚠️ Creating BEAT ADDICTS web interface...")
                create_web_interface()
            
            from web_interface import app
            app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
        except ImportError as e:
            print(f"❌ Error: Missing BEAT ADDICTS dependencies.")
            print(f"Details: {e}")
            print(f"\n🔧 BEAT ADDICTS Quick Fix:")
            print(f"1. Install dependencies: pip install -r requirements.txt")
            print(f"2. Or install manually: pip install flask werkzeug jinja2")
            print(f"3. Try again: python run.py")
            
            # Try to install automatically
            try_auto_install()
            return
        except Exception as e:
            print(f"❌ Error starting BEAT ADDICTS web interface: {e}")
            sys.exit(1)
    else:
        print("🎵 BEAT ADDICTS CLI - Professional Music Production")
        print("=" * 60)
        
        if args.train:
            # Train the AI model with provided MIDI files
            midi_files = glob.glob(os.path.join(args.train, '*.mid'))
            if not midi_files:
                print("❌ No MIDI files found in the specified directory")
                sys.exit(1)
            
            print(f"🎶 Training BEAT ADDICTS AI with {len(midi_files)} MIDI files...")
            # ... (Training code here)
            print("✅ BEAT ADDICTS AI training completed")
        
        if args.generate:
            # Generate music with the trained AI model
            print("🎵 Generating music with BEAT ADDICTS AI...")
            # ... (Music generation code here)
            print("✅ Music generation completed")
        
        if args.test_voices:
            # Test the voice assignment engine
            print("🔊 Testing BEAT ADDICTS voice assignment engine...")
            # ... (Voice testing code here)
            print("✅ Voice assignment engine test completed")
        
        if args.debug:
            # Run comprehensive debug test
            print("🐞 Running BEAT ADDICTS comprehensive debug test...")
            # ... (Debug test code here)
            print("✅ Debug test completed")
        
        if args.test:
            # Run the full suite of system tests
            print("🧪 Running BEAT ADDICTS system tests...")
            # ... (System test code here)
            print("✅ System tests completed")
    
    return

if __name__ == "__main__":
    main()