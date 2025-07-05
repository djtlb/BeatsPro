import pretty_midi
import numpy as np
import os
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

class RockSubgenre(Enum):
    """Rock music subgenres"""
    CLASSIC_ROCK = "classic_rock"
    HARD_ROCK = "hard_rock"
    PUNK_ROCK = "punk_rock"
    ALTERNATIVE_ROCK = "alternative_rock"
    INDIE_ROCK = "indie_rock"
    PROGRESSIVE_ROCK = "progressive_rock"
    METAL = "metal"
    GRUNGE = "grunge"
    BLUES_ROCK = "blues_rock"
    PSYCHEDELIC_ROCK = "psychedelic_rock"
    GARAGE_ROCK = "garage_rock"
    POST_ROCK = "post_rock"
    MATH_ROCK = "math_rock"
    STONER_ROCK = "stoner_rock"
    FOLK_ROCK = "folk_rock"

@dataclass
class RockCharacteristics:
    """Characteristics for each Rock subgenre"""
    bpm_range: Tuple[int, int]
    distortion_level: float
    rhythm_complexity: float
    solo_style: str
    power_chords: bool
    atmosphere: str
    dynamics: str

class RockMIDIGenerator:
    """Rock music MIDI generator covering all subgenres"""
    
    def __init__(self):
        self.subgenre_specs = {
            RockSubgenre.CLASSIC_ROCK: RockCharacteristics(
                bpm_range=(100, 140), distortion_level=0.6, rhythm_complexity=0.6,
                solo_style="blues_based", power_chords=True, atmosphere="anthemic", dynamics="medium"
            ),
            RockSubgenre.HARD_ROCK: RockCharacteristics(
                bpm_range=(110, 150), distortion_level=0.8, rhythm_complexity=0.7,
                solo_style="fast", power_chords=True, atmosphere="aggressive", dynamics="loud"
            ),
            RockSubgenre.PUNK_ROCK: RockCharacteristics(
                bpm_range=(150, 200), distortion_level=0.9, rhythm_complexity=0.4,
                solo_style="simple", power_chords=True, atmosphere="rebellious", dynamics="raw"
            ),
            RockSubgenre.PROGRESSIVE_ROCK: RockCharacteristics(
                bpm_range=(80, 160), distortion_level=0.5, rhythm_complexity=0.9,
                solo_style="complex", power_chords=False, atmosphere="sophisticated", dynamics="dynamic"
            ),
            RockSubgenre.GRUNGE: RockCharacteristics(
                bpm_range=(90, 130), distortion_level=0.8, rhythm_complexity=0.5,
                solo_style="feedback", power_chords=True, atmosphere="angsty", dynamics="loud_quiet"
            )
        }

    def generate_rock_track(self, subgenre: RockSubgenre, duration_bars: int = 32) -> pretty_midi.PrettyMIDI:
        """Generate a complete Rock track"""
        specs = self.subgenre_specs[subgenre]
        bpm = random.randint(*specs.bpm_range)
        
        midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
        
        # Add instruments
        drums = pretty_midi.Instrument(program=0, is_drum=True, name="Drums")
        bass = pretty_midi.Instrument(program=34, name="Electric Bass")
        guitar_rhythm = pretty_midi.Instrument(program=29, name="Electric Guitar")
        guitar_lead = pretty_midi.Instrument(program=30, name="Lead Guitar")
        
        bar_duration = 60 / bpm * 4
        
        self._generate_rock_drums(drums, subgenre, duration_bars, bar_duration)
        self._generate_rock_bass(bass, subgenre, duration_bars, bar_duration)
        self._generate_rock_rhythm_guitar(guitar_rhythm, subgenre, duration_bars, bar_duration)
        self._generate_rock_lead_guitar(guitar_lead, subgenre, duration_bars, bar_duration)
        
        midi.instruments.extend([drums, bass, guitar_rhythm, guitar_lead])
        return midi

    def _generate_rock_drums(self, drums: pretty_midi.Instrument, subgenre: RockSubgenre,
                            duration_bars: int, bar_duration: float):
        """Generate rock drum patterns"""
        kick_note = 36
        snare_note = 38
        hihat_note = 42
        crash_note = 49
        
        # Rock pattern variations
        if subgenre == RockSubgenre.PUNK_ROCK:
            pattern = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # Fast pattern
        else:
            pattern = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # Standard rock
        
        step_duration = bar_duration / 16
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            
            for step, hit in enumerate(pattern):
                if hit:
                    step_time = bar_start + step * step_duration
                    
                    if step % 4 == 0:  # Kick
                        velocity = random.randint(100, 127)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=kick_note,
                            start=step_time, end=step_time + step_duration * 0.8
                        ))
                    
                    elif step in [4, 12]:  # Snare
                        velocity = random.randint(90, 127)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=snare_note,
                            start=step_time, end=step_time + step_duration * 0.6
                        ))
                    
                    # Hi-hat
                    if random.random() < 0.8:
                        velocity = random.randint(50, 80)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=hihat_note,
                            start=step_time, end=step_time + step_duration * 0.3
                        ))

    def _generate_rock_bass(self, bass: pretty_midi.Instrument, subgenre: RockSubgenre,
                           duration_bars: int, bar_duration: float):
        """Generate rock basslines"""
        bass_notes = [28, 31, 33, 35, 36, 38, 40, 43]
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            subdivisions = 8
            step_duration = bar_duration / subdivisions
            
            for step in range(subdivisions):
                if step % 2 == 0 or random.random() < 0.3:
                    step_time = bar_start + step * step_duration
                    note = random.choice(bass_notes)
                    velocity = random.randint(80, 120)
                    duration = step_duration * 0.8
                    
                    bass.notes.append(pretty_midi.Note(
                        velocity=velocity, pitch=note,
                        start=step_time, end=step_time + duration
                    ))

    def _generate_rock_rhythm_guitar(self, guitar: pretty_midi.Instrument, subgenre: RockSubgenre,
                                    duration_bars: int, bar_duration: float):
        """Generate rhythm guitar (power chords)"""
        power_chord_roots = [40, 43, 45, 47, 50, 52, 55]
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            
            # Power chord (root + fifth)
            root = random.choice(power_chord_roots)
            chord_notes = [root, root + 7]  # Power chord
            
            for note in chord_notes:
                velocity = random.randint(90, 120)
                guitar.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note,
                    start=bar_start, end=bar_start + bar_duration
                ))

    def _generate_rock_lead_guitar(self, lead: pretty_midi.Instrument, subgenre: RockSubgenre,
                                  duration_bars: int, bar_duration: float):
        """Generate lead guitar solos/riffs"""
        scale = [60, 62, 63, 65, 67, 68, 70, 72]  # Minor pentatonic
        
        for bar in range(0, duration_bars, 4):
            bar_start = bar * bar_duration
            phrase_length = bar_duration * 4
            
            num_notes = random.randint(8, 16)
            
            for i in range(num_notes):
                note_time = bar_start + random.uniform(0, phrase_length)
                note_duration = random.uniform(0.1, 0.5)
                note_pitch = random.choice(scale) + random.choice([0, 12])
                velocity = random.randint(80, 120)
                
                lead.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_pitch,
                    start=note_time, end=note_time + note_duration
                ))

    def generate_training_dataset(self, output_dir: str = "midi_files", tracks_per_subgenre: int = 4):
        """Generate Rock training dataset"""
        os.makedirs(output_dir, exist_ok=True)
        generated_files = []
        
        print("🎸 Generating Rock training dataset...")
        
        for subgenre in RockSubgenre:
            print(f"🎵 Generating {tracks_per_subgenre} tracks for {subgenre.value}...")
            
            for track_num in range(tracks_per_subgenre):
                duration_bars = random.randint(16, 48)
                midi_track = self.generate_rock_track(subgenre, duration_bars)
                
                filename = f"rock_{subgenre.value}_{track_num + 1:02d}.mid"
                filepath = os.path.join(output_dir, filename)
                midi_track.write(filepath)
                
                generated_files.append(filepath)
                print(f"   ✅ Generated: {filename}")
        
        print(f"\n🎉 Rock dataset complete! Generated {len(generated_files)} tracks")
        return generated_files

def main():
    """Generate Rock training dataset"""
    generator = RockMIDIGenerator()
    files = generator.generate_training_dataset(tracks_per_subgenre=4)
    print(f"\n🚀 Ready to train with {len(files)} Rock tracks!")
    return len(files) > 0

if __name__ == "__main__":
    main()