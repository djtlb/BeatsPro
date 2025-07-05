import pretty_midi
import numpy as np
import os
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

class FuturisticSubgenre(Enum):
    """Cutting-edge and futuristic music genres"""
    AI_GENERATED = "ai_generated"
    HYPERPOP = "hyperpop"
    BREAKCORE = "breakcore"
    PHONK_TRAP = "phonk_trap"
    WAVE = "wave"
    SYNTHWAVE = "synthwave"
    VAPORWAVE = "vaporwave"
    FUTURE_GARAGE = "future_garage"
    NEURO_BASS = "neuro_bass"
    GLITCHCORE = "glitchcore"
    MICROGENRE = "microgenre"
    AMBIENT_TRAP = "ambient_trap"
    POST_INTERNET = "post_internet"
    DATACORE = "datacore"
    CYBER_PUNK = "cyber_punk"

@dataclass
class FuturisticCharacteristics:
    """Characteristics for futuristic genres"""
    bpm_range: Tuple[int, int]
    digital_distortion: float
    temporal_complexity: float
    ai_elements: bool
    glitch_factor: float
    atmosphere: str
    innovation_level: float

class FuturisticMIDIGenerator:
    """Futuristic and cutting-edge genre MIDI generator"""
    
    def __init__(self):
        self.subgenre_specs = {
            FuturisticSubgenre.HYPERPOP: FuturisticCharacteristics(
                bpm_range=(150, 200), digital_distortion=0.9, temporal_complexity=0.8,
                ai_elements=True, glitch_factor=0.7, atmosphere="chaotic", innovation_level=0.9
            ),
            FuturisticSubgenre.AI_GENERATED: FuturisticCharacteristics(
                bmp_range=(80, 180), digital_distortion=0.6, temporal_complexity=1.0,
                ai_elements=True, glitch_factor=0.5, atmosphere="algorithmic", innovation_level=1.0
            ),
            FuturisticSubgenre.BREAKCORE: FuturisticCharacteristics(
                bpm_range=(160, 220), digital_distortion=0.8, temporal_complexity=0.9,
                ai_elements=False, glitch_factor=0.9, atmosphere="frantic", innovation_level=0.8
            ),
            FuturisticSubgenre.SYNTHWAVE: FuturisticCharacteristics(
                bpm_range=(110, 130), digital_distortion=0.4, temporal_complexity=0.3,
                ai_elements=False, glitch_factor=0.2, atmosphere="retro_future", innovation_level=0.6
            ),
            FuturisticSubgenre.VAPORWAVE: FuturisticCharacteristics(
                bpm_range=(60, 90), digital_distortion=0.5, temporal_complexity=0.2,
                ai_elements=False, glitch_factor=0.3, atmosphere="nostalgic", innovation_level=0.5
            )
        }

    def generate_futuristic_track(self, subgenre: FuturisticSubgenre, duration_bars: int = 32) -> pretty_midi.PrettyMIDI:
        """Generate a futuristic track"""
        specs = self.subgenre_specs[subgenre]
        bpm = random.randint(*specs.bpm_range)
        
        midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
        
        # Add futuristic instruments
        drums = pretty_midi.Instrument(program=0, is_drum=True, name="Digital_Drums")
        synth = pretty_midi.Instrument(program=102, name="Synth_FX")
        lead = pretty_midi.Instrument(program=103, name="Digital_Lead")
        ambient = pretty_midi.Instrument(program=95, name="Ambient_Pad")
        
        bar_duration = 60 / bpm * 4
        
        self._generate_futuristic_drums(drums, subgenre, duration_bars, bar_duration)
        self._generate_futuristic_synth(synth, subgenre, duration_bars, bar_duration)
        self._generate_futuristic_lead(lead, subgenre, duration_bars, bar_duration)
        self._generate_ambient_texture(ambient, subgenre, duration_bars, bar_duration)
        
        midi.instruments.extend([drums, synth, lead, ambient])
        return midi

    def _generate_futuristic_drums(self, drums: pretty_midi.Instrument, subgenre: FuturisticSubgenre,
                                  duration_bars: int, bar_duration: float):
        """Generate futuristic drum patterns with glitch elements"""
        specs = self.subgenre_specs[subgenre]
        
        kick_note = 36
        snare_note = 38
        hihat_note = 42
        
        # Complex patterns for futuristic genres
        if subgenre == FuturisticSubgenre.BREAKCORE:
            pattern = [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]  # Complex breakbeat
        elif subgenre == FuturisticSubgenre.HYPERPOP:
            pattern = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1]  # Chaotic
        else:
            pattern = [1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0]  # Default complex
        
        step_duration = bar_duration / 16
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            
            for step, hit in enumerate(pattern):
                if hit or random.random() < specs.glitch_factor * 0.3:
                    step_time = bar_start + step * step_duration
                    
                    # Add glitch timing variations
                    if random.random() < specs.glitch_factor * 0.2:
                        step_time += random.uniform(-step_duration * 0.1, step_duration * 0.1)
                    
                    if step % 4 == 0:  # Kick
                        velocity = random.randint(90, 127)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=kick_note,
                            start=step_time, end=step_time + step_duration * 0.8
                        ))
                    
                    elif step in [4, 12] or random.random() < specs.temporal_complexity * 0.3:
                        velocity = random.randint(80, 120)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=snare_note,
                            start=step_time, end=step_time + step_duration * 0.6
                        ))

    def _generate_futuristic_synth(self, synth: pretty_midi.Instrument, subgenre: FuturisticSubgenre,
                                  duration_bars: int, bar_duration: float):
        """Generate futuristic synth patterns"""
        specs = self.subgenre_specs[subgenre]
        
        # Use chromatic and atonal scales for futuristic sound
        scale = [60, 61, 63, 64, 66, 67, 69, 70, 72, 73, 75, 76]
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            
            # Generate complex rhythmic patterns
            num_notes = int(8 * specs.temporal_complexity)
            
            for i in range(num_notes):
                note_time = bar_start + random.uniform(0, bar_duration)
                note_duration = random.uniform(0.1, 0.8)
                note_pitch = random.choice(scale) + random.choice([-12, 0, 12, 24])
                velocity = random.randint(60, 100)
                
                synth.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_pitch,
                    start=note_time, end=note_time + note_duration
                ))

    def _generate_futuristic_lead(self, lead: pretty_midi.Instrument, subgenre: FuturisticSubgenre,
                                 duration_bars: int, bar_duration: float):
        """Generate futuristic lead melodies"""
        specs = self.subgenre_specs[subgenre]
        
        # High-tech scale patterns
        scale = [72, 74, 75, 77, 79, 80, 82, 84, 86, 87, 89, 91]  # High register
        
        for bar in range(0, duration_bars, 2):
            bar_start = bar * bar_duration
            phrase_length = bar_duration * 2
            
            num_notes = random.randint(6, 20)
            
            for i in range(num_notes):
                note_time = bar_start + random.uniform(0, phrase_length)
                note_duration = random.uniform(0.05, 0.5)
                note_pitch = random.choice(scale)
                velocity = random.randint(70, 110)
                
                # Add digital artifacts
                if random.random() < specs.digital_distortion * 0.1:
                    note_pitch += random.choice([-1, 1])  # Micro-pitch variations
                
                lead.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_pitch,
                    start=note_time, end=note_time + note_duration
                ))

    def _generate_ambient_texture(self, ambient: pretty_midi.Instrument, subgenre: FuturisticSubgenre,
                                 duration_bars: int, bar_duration: float):
        """Generate ambient textures"""
        # Long sustained notes for atmosphere
        ambient_notes = [36, 43, 50, 57, 64, 71]
        note_duration = bar_duration * 8
        
        for bar in range(0, duration_bars, 8):
            bar_start = bar * bar_duration
            
            for note_pitch in random.sample(ambient_notes, 3):
                velocity = random.randint(20, 50)
                ambient.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_pitch,
                    start=bar_start, end=bar_start + note_duration
                ))

    def generate_training_dataset(self, output_dir: str = "midi_files", tracks_per_subgenre: int = 4):
        """Generate Futuristic training dataset"""
        os.makedirs(output_dir, exist_ok=True)
        generated_files = []
        
        print("🚀 Generating Futuristic training dataset...")
        
        for subgenre in FuturisticSubgenre:
            print(f"🎵 Generating {tracks_per_subgenre} tracks for {subgenre.value}...")
            
            for track_num in range(tracks_per_subgenre):
                duration_bars = random.randint(16, 48)
                midi_track = self.generate_futuristic_track(subgenre, duration_bars)
                
                filename = f"futuristic_{subgenre.value}_{track_num + 1:02d}.mid"
                filepath = os.path.join(output_dir, filename)
                midi_track.write(filepath)
                
                generated_files.append(filepath)
                print(f"   ✅ Generated: {filename}")
        
        print(f"\n🎉 Futuristic dataset complete! Generated {len(generated_files)} tracks")
        return generated_files

def main():
    """Generate Futuristic training dataset"""
    generator = FuturisticMIDIGenerator()
    files = generator.generate_training_dataset(tracks_per_subgenre=4)
    print(f"\n🚀 Ready to train with {len(files)} Futuristic tracks!")
    return len(files) > 0

if __name__ == "__main__":
    main()