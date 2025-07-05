#!/usr/bin/env python3
"""
Smart Music Generator AI - Main Entry Point
"""

import sys
import argparse
import argparse
# Fix encoding for Windows
if sys.platform == "win32":
    import locale
    try:
        # Try to set UTF-8 encoding
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        pass

def main():
    parser = argparse.ArgumentParser(description='Smart Music Generator AI')
    parser.add_argument('--mode', choices=['web', 'cli'], default='web', 
                       help='Run mode: web interface or command line')
    parser.add_argument('--train', type=str, help='Path to MIDI files directory for training')
    parser.add_argument('--generate', action='store_true', help='Generate music (CLI mode)')
    parser.add_argument('--length', type=int, default=500, help='Length of generated music')
    parser.add_argument('--temperature', type=float, default=0.8, help='Generation temperature')
    parser.add_argument('--create-dnb', action='store_true', help='Generate DNB training dataset')
    parser.add_argument('--create-hiphop', action='store_true', help='Generate Hip-Hop training dataset')
    parser.add_argument('--create-electronic', action='store_true', help='Generate Electronic training dataset')
    parser.add_argument('--create-country', action='store_true', help='Generate Country training dataset')
    parser.add_argument('--create-rock', action='store_true', help='Generate Rock training dataset')
    parser.add_argument('--create-futuristic', action='store_true', help='Generate Futuristic training dataset')
    parser.add_argument('--create-all', action='store_true', help='Generate ALL music training datasets')
    parser.add_argument('--debug', action='store_true', help='Run comprehensive debug test')
    parser.add_argument('--test', action='store_true', help='Run system tests')
    
    args = parser.parse_args()
    
    # Handle universal dataset generation
    if args.create_all:
        print("🌍 Generating UNIVERSAL training dataset (all genres)...")
        try:
            from universal_midi_generator import main as generate_all
            success = generate_all()
            if success:
                print("\n✅ Universal dataset generated successfully!")
                print("🎯 You now have the most comprehensive music training dataset!")
                print("Run 'python run.py' to start training")
            else:
                print("\n❌ Universal dataset generation had issues. Check output above.")
            return
        except ImportError as e:
            print(f"❌ Error: Could not import Universal generator: {e}")
            return
    
    # Handle individual genre generation
    genre_handlers = {
        'create_electronic': ('electronic_midi_generator', 'Electronic'),
        'create_country': ('country_midi_generator', 'Country'),
        'create_rock': ('rock_midi_generator', 'Rock'),
        'create_futuristic': ('futuristic_midi_generator', 'Futuristic')
    }
    
    for arg, (module, genre_name) in genre_handlers.items():
        if getattr(args, arg.replace('-', '_')):
            print(f"🎵 Generating {genre_name} training dataset...")
            try:
                generator_module = __import__(module)
                success = generator_module.main()
                if success:
                    print(f"\n✅ {genre_name} dataset generated successfully!")
                else:
                    print(f"\n❌ {genre_name} dataset generation failed.")
                return
            except ImportError as e:
                print(f"❌ Error: Could not import {genre_name} generator: {e}")
                return
    
    if args.mode == 'web':
        print("Smart Music Generator AI - Web Interface")
        print("=" * 45)
        print("Server starting at: http://localhost:5000")
        print("Tip: Generate DNB training data with: python run.py --create-dnb")
        print()
        
        try:
            from web_interface import app
            app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
        except ImportError as e:
            print(f"Error: Missing dependencies. Please run: pip install -r requirements.txt")
            print(f"Details: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error starting web interface: {e}")
            sys.exit(1)
    
    elif args.mode == 'cli':
        try:
            from music_generator import SmartMusicGenerator
            generator = SmartMusicGenerator()
            
            if args.train:
                print(f"Looking for MIDI files in: {args.train}")
                midi_files = generator.get_sample_midi_files(args.train)
                
                if not midi_files:
                    print("No valid MIDI files found in the specified directory.")
                    print("Generate DNB training data with: python run.py --create-dnb")
                    return
                
                print(f"Found {len(midi_files)} MIDI files")
                print("Starting training...")
                
                generator.train(midi_files, epochs=20)
                print("Training completed and model saved.")
            
            if args.generate:
                print("Loading model and generating music...")
                
                if not generator.load_model():
                    print("No trained model found. Please train first using --train")
                    return
                
                try:
                    output_path = generator.generate(
                        length=args.length, 
                        temperature=args.temperature
                    )
                    print(f"Music generated successfully: {output_path}")
                    
                except Exception as e:
                    print(f"Error generating music: {e}")
                    
        except ImportError as e:
            print(f"Error: Missing dependencies. Please run: pip install -r requirements.txt")
            print(f"Details: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
