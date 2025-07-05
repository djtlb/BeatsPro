#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Universal MIDI Generator
Professional Music Production AI - Multi-Genre Dataset Generator
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any

class BeatAddictsUniversalGenerator:
    """🔥 BEAT ADDICTS Universal MIDI Generator - Professional Multi-Genre System"""
    
    def __init__(self):
        self.generators = {}
        self.available_genres = []
        self.beat_addicts_version = "2.0"
        self.setup_generators()
    
    def setup_generators(self):
        """Initialize all available BEAT ADDICTS genre generators"""
        print("🎵 BEAT ADDICTS - Initializing Universal Generator")
        print("🔥 Professional Music Production AI v2.0 🔥")
        
        generator_configs = [
            ('dnb_midi_generator', 'DrumAndBassMIDIGenerator', 'dnb', 'BEAT ADDICTS DNB'),
            ('hiphop_midi_generator', 'HipHopMIDIGenerator', 'hiphop', 'BEAT ADDICTS Hip-Hop'),
            ('electronic_midi_generator', 'ElectronicMIDIGenerator', 'electronic', 'BEAT ADDICTS Electronic'),
            ('country_midi_generator', 'CountryMIDIGenerator', 'country', 'BEAT ADDICTS Country'),
            ('rock_midi_generator', 'RockMIDIGenerator', 'rock', 'BEAT ADDICTS Rock'),
            ('futuristic_midi_generator', 'FuturisticMIDIGenerator', 'futuristic', 'BEAT ADDICTS Futuristic')
        ]
        
        for module_name, class_name, key, display_name in generator_configs:
            try:
                # Check multiple possible locations
                module_paths = [
                    f"{module_name}.py",
                    f"../{module_name}.py",
                    f"../beat_addicts_generators/{module_name}.py"
                ]
                
                module_found = False
                for module_path in module_paths:
                    if os.path.exists(module_path):
                        # Add directory to path for import
                        module_dir = os.path.dirname(os.path.abspath(module_path))
                        if module_dir not in sys.path:
                            sys.path.insert(0, module_dir)
                        
                        try:
                            module = __import__(module_name)
                            generator_class = getattr(module, class_name)
                            self.generators[key] = generator_class()
                            self.available_genres.append(key)
                            print(f"✅ {display_name} Generator loaded")
                            module_found = True
                            break
                        except Exception as e:
                            print(f"⚠️ {display_name} import error: {e}")
                
                if not module_found:
                    print(f"⚠️ {display_name} Generator file not found")
                    
            except Exception as e:
                print(f"⚠️ {display_name} Generator not available: {e}")
    
    def generate_all_datasets(self, output_dir: str = "midi_files", tracks_per_subgenre: int = 4):
        """Generate comprehensive BEAT ADDICTS training datasets for all available genres"""
        
        print("🎵 BEAT ADDICTS UNIVERSAL GENERATOR - Professional Dataset Creation")
        print("=" * 80)
        
        os.makedirs(output_dir, exist_ok=True)
        
        total_files = []
        generation_stats = {}
        
        # Initialize BEAT ADDICTS voice assignment system
        try:
            # Check multiple possible locations for voice assignment
            voice_paths = [
                "voice_assignment.py",
                "../voice_assignment.py", 
                "../beat_addicts_core/voice_assignment.py",
                os.path.join(os.path.dirname(__file__), "..", "voice_assignment.py"),
                os.path.join(os.path.dirname(__file__), "..", "beat_addicts_core", "voice_assignment.py")
            ]

            voice_assigner = None
            for voice_path in voice_paths:
                if os.path.exists(voice_path):
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("voice_assignment", voice_path)
                    if spec and spec.loader:
                        voice_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(voice_module)
                        voice_assigner = voice_module.IntelligentVoiceAssigner()
                        print("✅ BEAT ADDICTS Voice Assignment System loaded")
                        break
            
            use_voice_assignment = voice_assigner is not None
            if not use_voice_assignment:
                print("⚠️ BEAT ADDICTS Voice Assignment System not available")
                
        except Exception as e:
            print(f"⚠️ BEAT ADDICTS Voice Assignment error: {e}")
            use_voice_assignment = False
            voice_assigner = None
        
        for genre in self.available_genres:
            try:
                print(f"\n🎼 Generating BEAT ADDICTS {genre.upper()} dataset...")
                generator = self.generators[genre]
                
                files = generator.generate_training_dataset(
                    output_dir=output_dir,
                    tracks_per_subgenre=tracks_per_subgenre
                )
                
                enhanced_files = []
                
                # Apply BEAT ADDICTS voice assignment to generated files if available
                if use_voice_assignment and files and voice_assigner:
                    print(f"🎛️ Applying BEAT ADDICTS voice assignment to {genre} tracks...")
                    
                    for file_path in files[:5]:  # Enhance first 5 files as examples
                        try:
                            # Import pretty_midi safely
                            try:
                                import pretty_midi
                                midi = pretty_midi.PrettyMIDI(file_path)
                                enhanced_midi = voice_assigner.assign_voices_to_track(midi, genre)
                                
                                # Save enhanced version
                                enhanced_path = file_path.replace('.mid', '_beat_addicts_enhanced.mid')
                                enhanced_midi.write(enhanced_path)
                                enhanced_files.append(enhanced_path)
                                
                            except ImportError:
                                print(f"⚠️ pretty_midi not available for voice enhancement")
                                break
                            except Exception as e:
                                print(f"⚠️ Voice assignment failed for {file_path}: {e}")
                                continue
                                
                        except Exception as e:
                            print(f"⚠️ Voice assignment failed for {file_path}: {e}")
                    
                    if enhanced_files:
                        print(f"✅ Enhanced {len(enhanced_files)} {genre} tracks with BEAT ADDICTS voice assignment")
                
                total_files.extend(files)
                generation_stats[genre] = {
                    'files_generated': len(files),
                    'status': 'success',
                    'voice_enhanced': len(enhanced_files),
                    'beat_addicts_version': self.beat_addicts_version
                }
                
                print(f"✅ BEAT ADDICTS {genre.upper()}: {len(files)} files generated")
                
            except Exception as e:
                print(f"❌ BEAT ADDICTS {genre.upper()} generation failed: {e}")
                generation_stats[genre] = {
                    'files_generated': 0,
                    'status': 'failed',
                    'error': str(e),
                    'beat_addicts_version': self.beat_addicts_version
                }
        
        # Generate comprehensive BEAT ADDICTS summary
        self._generate_beat_addicts_summary(output_dir, total_files, generation_stats, use_voice_assignment)
        
        return total_files, generation_stats

    def _generate_beat_addicts_summary(self, output_dir: str, total_files: List[str], stats: Dict[str, Any], use_voice_assignment: bool):
        """Generate comprehensive BEAT ADDICTS dataset summary"""
        
        summary_path = os.path.join(output_dir, "beat_addicts_universal_dataset_summary.txt")
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("🎵 BEAT ADDICTS - Universal Music Training Dataset Summary\n")
            f.write("🔥 Professional Music Production AI v2.0 🔥\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"BEAT ADDICTS Dataset Statistics:\n")
            f.write(f"   • Total files generated: {len(total_files)}\n")
            f.write(f"   • Total genres covered: {len(self.available_genres)}\n")
            f.write(f"   • Voice assignment: {'✅ ENABLED' if use_voice_assignment else '⚠️ DISABLED'}\n")
            f.write(f"   • Generation timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("BEAT ADDICTS Genre Breakdown:\n")
            f.write("-" * 60 + "\n")
            
            total_enhanced = 0
            for genre, data in stats.items():
                status_icon = "✅" if data['status'] == 'success' else "❌"
                enhanced_count = data.get('voice_enhanced', 0)
                total_enhanced += enhanced_count
                
                f.write(f"{status_icon} BEAT ADDICTS {genre.upper():<15} {data['files_generated']:>3} files")
                if enhanced_count > 0:
                    f.write(f" ({enhanced_count} voice-enhanced)")
                f.write("\n")
                
                if data['status'] == 'failed':
                    f.write(f"    ❌ Error: {data.get('error', 'Unknown error')}\n")
            
            f.write(f"\n🎯 BEAT ADDICTS Training Recommendations:\n")
            f.write("   • Use all genres for maximum BEAT ADDICTS diversity\n")
            f.write("   • Train for 40-80 epochs for professional BEAT ADDICTS model\n")
            f.write("   • Experiment with temperature 0.7-0.9 for BEAT ADDICTS creativity\n")
            f.write("   • Consider genre-specific fine-tuning for BEAT ADDICTS specialization\n")
            f.write("   • Use voice-enhanced files for superior instrument assignment\n\n")
            
            f.write("BEAT ADDICTS File Distribution by Genre:\n")
            f.write("-" * 60 + "\n")
            
            genre_counts = {}
            for file_path in total_files:
                filename = os.path.basename(file_path)
                genre = filename.split('_')[0] if '_' in filename else 'unknown'
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
            
            for genre, count in sorted(genre_counts.items()):
                f.write(f"   {genre:<20} {count:>3} files\n")
            
            f.write(f"\n🚀 BEAT ADDICTS v{self.beat_addicts_version} - Ready for Professional AI Training!\n")
            f.write(f"💡 Total voice-enhanced files: {total_enhanced}\n")
        
        print(f"\n📋 BEAT ADDICTS Universal summary saved to: {summary_path}")

def main():
    """Generate all available BEAT ADDICTS music datasets"""
    
    generator = BeatAddictsUniversalGenerator()
    
    if not generator.available_genres:
        print("❌ No BEAT ADDICTS genre generators available!")
        print("Please ensure BEAT ADDICTS generator files are present and dependencies are installed.")
        print("Check these locations:")
        print("   • Current directory")
        print("   • beat_addicts_generators/ directory")
        print("   • Parent directory")
        return False
    
    print(f"\n🎵 BEAT ADDICTS Available genres: {', '.join(generator.available_genres)}")
    
    # Generate comprehensive BEAT ADDICTS dataset
    files, stats = generator.generate_all_datasets(
        output_dir="midi_files",
        tracks_per_subgenre=4  # Professional quality, adjust as needed
    )
    
    successful_genres = len([g for g, s in stats.items() if s['status'] == 'success'])
    total_genres = len(stats)
    
    print(f"\n🎉 BEAT ADDICTS UNIVERSAL DATASET GENERATION COMPLETE!")
    print(f"📊 Generated {len(files)} total professional files")
    print(f"🎼 Success rate: {successful_genres}/{total_genres} genres")
    print(f"📁 Files saved to: {os.path.abspath('midi_files')}")
    print(f"🔥 Ready for BEAT ADDICTS AI training with comprehensive multi-genre dataset! 🔥")
    
    return len(files) > 0

# Maintain compatibility with old import name
UniversalMIDIGenerator = BeatAddictsUniversalGenerator

if __name__ == "__main__":
    main()
