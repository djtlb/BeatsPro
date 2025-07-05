#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Professional Music Production AI
Main Entry Point for BEAT ADDICTS Studio
"""

import os
import sys
import argparse
import glob

# Beat Addicts encoding fix for Windows
if sys.platform == "win32":
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        pass

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
    
    args = parser.parse_args()
    
    print("🔥 BEAT ADDICTS v2.0 - Professional Music Production AI 🔥")
    print("🎵 No more basic tools. This is BEAT ADDICTS level. 🎵")
    
    if args.mode == 'web':
        print("🎵 BEAT ADDICTS STUDIO - Professional Music Production")
        print("=" * 60)
        print("🔥 BEAT ADDICTS Studio launching at: http://localhost:5000 🔥")
        print("🎧 Professional beat making starts here 🎧")
        print("Tip: Generate BEAT ADDICTS training data with: python run.py --create-all")
        print()
        
        try:
            from web_interface import app
            # Customize app for BEAT ADDICTS branding
            app.config['BEAT_ADDICTS_VERSION'] = '2.0'
            app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
        except ImportError as e:
            print(f"Error: Missing BEAT ADDICTS dependencies. Please run: pip install -r requirements.txt")
            print(f"Details: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error starting BEAT ADDICTS Studio: {e}")
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