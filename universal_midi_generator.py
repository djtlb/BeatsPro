#!/usr/bin/env python3
"""
Universal MIDI Generator for Smart Music Generator AI
Manages all genre generators and creates comprehensive training datasets
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any

class UniversalMIDIGenerator:
    """Manages all genre-specific MIDI generators"""
    
    def __init__(self):
        self.generators = {}
        self.available_genres = []
        self.setup_generators()
    
    def setup_generators(self):
        """Initialize all available genre generators"""
        generator_configs = [
            ('dnb_midi_generator', 'DrumAndBassMIDIGenerator', 'dnb', 'DNB'),
            ('hiphop_midi_generator', 'HipHopMIDIGenerator', 'hiphop', 'Hip-Hop'),
            ('electronic_midi_generator', 'ElectronicMIDIGenerator', 'electronic', 'Electronic'),
            ('country_midi_generator', 'CountryMIDIGenerator', 'country', 'Country'),
            ('rock_midi_generator', 'RockMIDIGenerator', 'rock', 'Rock'),
            ('futuristic_midi_generator', 'FuturisticMIDIGenerator', 'futuristic', 'Futuristic')
        ]
        
        for module_name, class_name, key, display_name in generator_configs:
            try:
                if os.path.exists(f"{module_name}.py"):
                    module = __import__(module_name)
                    generator_class = getattr(module, class_name)
                    self.generators[key] = generator_class()
                    self.available_genres.append(key)
                    print(f"✅ {display_name} Generator loaded")
                else:
                    print(f"⚠️ {display_name} Generator file not found: {module_name}.py")
            except Exception as e:
                print(f"⚠️ {display_name} Generator not available: {e}")
    
    def generate_all_datasets(self, output_dir: str = "midi_files", tracks_per_subgenre: int = 4):
        """Generate comprehensive training datasets for all available genres"""
        
        print("🎵 Universal MIDI Generator - Creating Comprehensive Training Dataset")
        print("=" * 80)
        
        os.makedirs(output_dir, exist_ok=True)
        
        total_files = []
        generation_stats = {}
        
        # Initialize voice assignment system
        try:
            from voice_assignment import IntelligentVoiceAssigner
            voice_assigner = IntelligentVoiceAssigner()
            print("✅ Voice Assignment System loaded")
            use_voice_assignment = True
        except ImportError:
            print("⚠️ Voice Assignment System not available")
            use_voice_assignment = False
        
        for genre in self.available_genres:
            try:
                print(f"\n🎼 Generating {genre.upper()} dataset...")
                generator = self.generators[genre]
                
                files = generator.generate_training_dataset(
                    output_dir=output_dir,
                    tracks_per_subgenre=tracks_per_subgenre
                )
                
                # Apply voice assignment to generated files if available
                if use_voice_assignment and files:
                    print(f"🎛️ Applying voice assignment to {genre} tracks...")
                    enhanced_files = []
                    
                    for file_path in files[:5]:  # Enhance first 5 files as examples
                        try:
                            midi = pretty_midi.PrettyMIDI(file_path)
                            enhanced_midi = voice_assigner.assign_voices_to_track(midi, genre)
                            
                            # Save enhanced version
                            enhanced_path = file_path.replace('.mid', '_enhanced.mid')
                            enhanced_midi.write(enhanced_path)
                            enhanced_files.append(enhanced_path)
                            
                        except Exception as e:
                            print(f"⚠️ Voice assignment failed for {file_path}: {e}")
                    
                    if enhanced_files:
                        print(f"✅ Enhanced {len(enhanced_files)} {genre} tracks with voice assignment")
                
                total_files.extend(files)
                generation_stats[genre] = {
                    'files_generated': len(files),
                    'status': 'success',
                    'voice_enhanced': len(enhanced_files) if use_voice_assignment else 0
                }
                
                print(f"✅ {genre.upper()}: {len(files)} files generated")
                
            except Exception as e:
                print(f"❌ {genre.upper()} generation failed: {e}")
                generation_stats[genre] = {
                    'files_generated': 0,
                    'status': 'failed',
                    'error': str(e)
                }
        
        # Generate comprehensive summary with voice assignment info
        self._generate_universal_summary(output_dir, total_files, generation_stats, use_voice_assignment)
        
        return total_files, generation_stats
    
    def _generate_universal_summary(self, output_dir: str, total_files: List[str], stats: Dict[str, Any], use_voice_assignment: bool):
        """Generate comprehensive summary of all generated datasets"""
        
        summary_path = os.path.join(output_dir, "universal_dataset_summary.txt")
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("Universal Music Training Dataset Summary\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Total files generated: {len(total_files)}\n")
            f.write(f"Total genres covered: {len(self.available_genres)}\n")
            f.write(f"Generation timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("Genre Breakdown:\n")
            f.write("-" * 40 + "\n")
            
            for genre, data in stats.items():
                status_icon = "✅" if data['status'] == 'success' else "❌"
                f.write(f"{status_icon} {genre.upper():<15} {data['files_generated']:>3} files\n")
                if data['status'] == 'failed':
                    f.write(f"    Error: {data.get('error', 'Unknown error')}\n")
            
            f.write(f"\nTraining Recommendations:\n")
            f.write("- Use all genres for maximum diversity\n")
            f.write("- Train for 40-60 epochs for multi-genre model\n")
            f.write("- Experiment with temperature 0.7-0.9\n")
            f.write("- Consider genre-specific fine-tuning\n\n")
            
            f.write("File Distribution by Genre:\n")
            f.write("-" * 40 + "\n")
            
            genre_counts = {}
            for file_path in total_files:
                filename = os.path.basename(file_path)
                genre = filename.split('_')[0] if '_' in filename else 'unknown'
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
            
            for genre, count in sorted(genre_counts.items()):
                f.write(f"{genre:<15} {count:>3} files\n")
        
        print(f"\n📋 Universal summary saved to: {summary_path}")

def main():
    """Generate all available music datasets"""
    
    generator = UniversalMIDIGenerator()
    
    if not generator.available_genres:
        print("❌ No genre generators available!")
        print("Please ensure genre generator files are present and dependencies are installed.")
        return False
    
    print(f"\n🎵 Available genres: {', '.join(generator.available_genres)}")
    
    # Generate comprehensive dataset
    files, stats = generator.generate_all_datasets(
        output_dir="midi_files",
        tracks_per_subgenre=4  # Adjust based on your needs
    )
    
    successful_genres = len([g for g, s in stats.items() if s['status'] == 'success'])
    total_genres = len(stats)
    
    print(f"\n🎉 UNIVERSAL DATASET GENERATION COMPLETE!")
    print(f"📊 Generated {len(files)} total files")
    print(f"🎼 Success rate: {successful_genres}/{total_genres} genres")
    print(f"📁 Files saved to: {os.path.abspath('midi_files')}")
    print(f"\n🚀 Ready for AI training with comprehensive multi-genre dataset!")
    
    return len(files) > 0

if __name__ == "__main__":
    main()
