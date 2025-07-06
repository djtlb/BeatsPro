#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Generator Wrapper
Universal wrapper for all generators with fallback support
"""

import os
import sys
from typing import List, Optional, Dict, Any

# Try to import our simple MIDI generator
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'beat_addicts_core'))
    from simple_midi_generator import BeatAddictsSimpleMIDIGenerator
    SIMPLE_MIDI_AVAILABLE = True
except ImportError:
    print("⚠️ Simple MIDI generator not available")
    SIMPLE_MIDI_AVAILABLE = False

class BeatAddictsGeneratorWrapper:
    """Universal wrapper for all BEAT ADDICTS generators"""
    
    def __init__(self, generator_type: str = "electronic"):
        self.generator_type = generator_type
        self.simple_generator = BeatAddictsSimpleMIDIGenerator() if SIMPLE_MIDI_AVAILABLE else None
        
        # Genre-specific settings
        self.genre_configs = {
            'dnb': {
                'bpm_range': (170, 180),
                'typical_patterns': ['amen_break', 'thinking_break'],
                'bass_style': 'reese',
                'atmosphere': 'dark'
            },
            'hiphop': {
                'bpm_range': (85, 95),
                'typical_patterns': ['boom_bap', 'trap'],
                'bass_style': '808',
                'atmosphere': 'urban'
            },
            'electronic': {
                'bpm_range': (120, 130),
                'typical_patterns': ['four_on_floor', 'breakbeat'],
                'bass_style': 'sub',
                'atmosphere': 'energetic'
            },
            'rock': {
                'bpm_range': (110, 130),
                'typical_patterns': ['rock_beat', 'shuffle'],
                'bass_style': 'electric',
                'atmosphere': 'powerful'
            },
            'country': {
                'bpm_range': (120, 140),
                'typical_patterns': ['country_shuffle', 'ballad'],
                'bass_style': 'acoustic',
                'atmosphere': 'warm'
            },
            'futuristic': {
                'bpm_range': (140, 160),
                'typical_patterns': ['complex_poly', 'glitch'],
                'bass_style': 'modular',
                'atmosphere': 'otherworldly'
            }
        }
    
    def generate_track(self, subgenre: str = None, duration_bars: int = 32, output_file: Optional[str] = None) -> Optional[str]:
        """Generate a track for the specified genre"""
        if not self.simple_generator:
            print("❌ No generator available")
            return None
        
        # Use the appropriate genre
        genre = subgenre if subgenre else self.generator_type
        
        print(f"🎵 Generating {genre.upper()} track ({duration_bars} bars)...")
        
        # Generate using simple MIDI generator
        result = self.simple_generator.generate_beat(
            genre=genre,
            bars=duration_bars,
            output_file=output_file
        )
        
        if result:
            print(f"✅ Generated: {result}")
        else:
            print(f"❌ Failed to generate {genre} track")
        
        return result
    
    def generate_training_dataset(self, output_dir: str = "midi_files", tracks_per_subgenre: int = 4) -> List[str]:
        """Generate training dataset for this generator type"""
        if not self.simple_generator:
            print("❌ No generator available for training dataset")
            return []
        
        os.makedirs(output_dir, exist_ok=True)
        generated_files = []
        
        print(f"🎼 BEAT ADDICTS {self.generator_type.upper()} - Generating Training Dataset")
        
        # Get genre configuration
        config = self.genre_configs.get(self.generator_type, self.genre_configs['electronic'])
        
        # Generate variations
        subgenres = [
            f"{self.generator_type}_style1",
            f"{self.generator_type}_style2", 
            f"{self.generator_type}_ambient",
            f"{self.generator_type}_intense"
        ]
        
        for i, subgenre in enumerate(subgenres):
            if i >= tracks_per_subgenre:
                break
                
            bars = 16 + (i * 8)  # Vary track length
            filename = os.path.join(output_dir, f"{self.generator_type}_{subgenre}_{i+1:02d}.mid")
            
            result = self.generate_track(self.generator_type, bars, filename)
            if result:
                generated_files.append(result)
        
        print(f"🎯 {self.generator_type.upper()} Dataset complete: {len(generated_files)} files")
        return generated_files

# Specific generator classes
class DrumAndBassMIDIGenerator(BeatAddictsGeneratorWrapper):
    def __init__(self):
        super().__init__("dnb")

class HipHopMIDIGenerator(BeatAddictsGeneratorWrapper):
    def __init__(self):
        super().__init__("hiphop")

class ElectronicMIDIGenerator(BeatAddictsGeneratorWrapper):
    def __init__(self):
        super().__init__("electronic")

class RockMIDIGenerator(BeatAddictsGeneratorWrapper):
    def __init__(self):
        super().__init__("rock")

class CountryMIDIGenerator(BeatAddictsGeneratorWrapper):
    def __init__(self):
        super().__init__("country")

class FuturisticMIDIGenerator(BeatAddictsGeneratorWrapper):
    def __init__(self):
        super().__init__("futuristic")

def test_all_generators():
    """Test all generator types"""
    print("🎵 Testing all BEAT ADDICTS Generator Wrappers...")
    
    generators = {
        'DNB': DrumAndBassMIDIGenerator(),
        'Hip-Hop': HipHopMIDIGenerator(),
        'Electronic': ElectronicMIDIGenerator(),
        'Rock': RockMIDIGenerator(),
        'Country': CountryMIDIGenerator(),
        'Futuristic': FuturisticMIDIGenerator()
    }
    
    for name, generator in generators.items():
        print(f"\n🎼 Testing {name} Generator...")
        result = generator.generate_track(duration_bars=4, output_file=f"test_{name.lower()}_wrapper.mid")
        if result:
            file_size = os.path.getsize(result) if os.path.exists(result) else 0
            print(f"   ✅ {name}: {result} ({file_size} bytes)")
        else:
            print(f"   ❌ {name}: Failed")

if __name__ == "__main__":
    test_all_generators()
