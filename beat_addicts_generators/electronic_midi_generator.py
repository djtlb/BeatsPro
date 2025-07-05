import pretty_midi
import numpy as np
import os
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

class ElectronicSubgenre(Enum):
    """Electronic music subgenres"""
    HOUSE = "house"
    TECHNO = "techno"
    TRANCE = "trance"
    BREAKBEAT = "breakbeat"
    BIG_ROOM = "big_room"
    PROGRESSIVE_HOUSE = "progressive_house"
    DEEP_HOUSE = "deep_house"
    TECH_HOUSE = "tech_house"
    MINIMAL_TECHNO = "minimal_techno"
    HARDSTYLE = "hardstyle"
    HARDCORE = "hardcore"
    BASS_MUSIC = "bass_music"
    DUBSTEP = "dubstep"
    ELECTRO = "electro"
    AMBIENT = "ambient"
    IDM = "idm"
    GARAGE = "garage"
    FUTURE_BASS = "future_bass"
    TROPICAL_HOUSE = "tropical_house"
    PSYTRANCE = "psytrance"

@dataclass
class ElectronicCharacteristics:
    """Characteristics for each Electronic subgenre"""
    bpm_range: Tuple[int, int]
    kick_pattern: str
    bass_complexity: float
    synth_style: str
    build_ups: bool
    atmosphere: str
    energy_level: float

class ElectronicMIDIGenerator:
    """Advanced Electronic music MIDI generator"""
    
    def __init__(self):
        self.subgenre_specs = {
            ElectronicSubgenre.HOUSE: ElectronicCharacteristics(
                bpm_range=(120, 130), kick_pattern="four_on_floor", bass_complexity=0.6,
                synth_style="warm", build_ups=True, atmosphere="uplifting", energy_level=0.7
            ),
            ElectronicSubgenre.TECHNO: ElectronicCharacteristics(
                bpm_range=(120, 150), kick_pattern="driving", bass_complexity=0.8,
                synth_style="industrial", build_ups=False, atmosphere="hypnotic", energy_level=0.9
            ),
            ElectronicSubgenre.TRANCE: ElectronicCharacteristics(
                bpm_range=(128, 140), kick_pattern="four_on_floor", bass_complexity=0.7,
                synth_style="ethereal", build_ups=True, atmosphere="euphoric", energy_level=0.8
            ),
            ElectronicSubgenre.BREAKBEAT: ElectronicCharacteristics(
                bpm_range=(120, 140), kick_pattern="broken", bass_complexity=0.9,
                synth_style="gritty", build_ups=True, atmosphere="energetic", energy_level=0.8
            ),
            ElectronicSubgenre.BIG_ROOM: ElectronicCharacteristics(
                bpm_range=(126, 132), kick_pattern="festival", bass_complexity=0.5,
                synth_style="massive", build_ups=True, atmosphere="anthemic", energy_level=1.0
            ),
            ElectronicSubgenre.DUBSTEP: ElectronicCharacteristics(
                bpm_range=(140, 150), kick_pattern="dubstep", bass_complexity=0.9,
                synth_style="wobbly", build_ups=True, atmosphere="aggressive", energy_level=0.9
            ),
            ElectronicSubgenre.BASS_MUSIC: ElectronicCharacteristics(
                bpm_range=(140, 160), kick_pattern="complex", bass_complexity=1.0,
                synth_style="heavy", build_ups=True, atmosphere="intense", energy_level=0.9
            ),
            ElectronicSubgenre.DEEP_HOUSE: ElectronicCharacteristics(
                bpm_range=(120, 125), kick_pattern="four_on_floor", bass_complexity=0.5,
                synth_style="deep", build_ups=False, atmosphere="groovy", energy_level=0.6
            ),
            ElectronicSubgenre.PROGRESSIVE_HOUSE: ElectronicCharacteristics(
                bpm_range=(128, 132), kick_pattern="four_on_floor", bass_complexity=0.7,
                synth_style="evolving", build_ups=True, atmosphere="building", energy_level=0.8
            ),
            ElectronicSubgenre.AMBIENT: ElectronicCharacteristics(
                bpm_range=(60, 90), kick_pattern="minimal", bass_complexity=0.3,
                synth_style="atmospheric", build_ups=False, atmosphere="peaceful", energy_level=0.2
            )
        }
        
        self.kick_patterns = {
            "four_on_floor": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            "driving": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            "broken": [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
            "festival": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            "dubstep": [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            "complex": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],
            "minimal": [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        }

    def generate_electronic_track(self, subgenre: ElectronicSubgenre, duration_bars: int = 32) -> pretty_midi.PrettyMIDI:
        """Generate a complete Electronic track for the specified subgenre"""
        
        specs = self.subgenre_specs[subgenre]
        bpm = random.randint(*specs.bpm_range)
        
        # Create MIDI object
        midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
        
        # Add instruments
        drums = pretty_midi.Instrument(program=0, is_drum=True, name="Drums")
        bass = pretty_midi.Instrument(program=38, name="Synth Bass")
        lead = pretty_midi.Instrument(program=81, name="Synth Lead")
        pads = pretty_midi.Instrument(program=88, name="Synth Pad")
        
        # Generate sections
        bar_duration = 60 / bpm * 4
        
        # Generate tracks
        self._generate_electronic_drums(drums, subgenre, duration_bars, bar_duration)
        self._generate_electronic_bass(bass, subgenre, duration_bars, bar_duration)
        self._generate_electronic_lead(lead, subgenre, duration_bars, bar_duration)
        self._generate_electronic_pads(pads, subgenre, duration_bars, bar_duration)
        
        midi.instruments.extend([drums, bass, lead, pads])
        return midi

    def _generate_electronic_drums(self, drums: pretty_midi.Instrument, subgenre: ElectronicSubgenre,
                                  duration_bars: int, bar_duration: float):
        """Generate electronic drum patterns"""
        specs = self.subgenre_specs[subgenre]
        pattern = self.kick_patterns.get(specs.kick_pattern, self.kick_patterns["four_on_floor"])
        
        kick_note = 36
        snare_note = 38
        hihat_note = 42
        
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
                        velocity = random.randint(80, 110)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=snare_note,
                            start=step_time, end=step_time + step_duration * 0.6
                        ))
                    
                    # Hi-hats
                    if random.random() < 0.8:
                        velocity = random.randint(40, 70)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=hihat_note,
                            start=step_time, end=step_time + step_duration * 0.3
                        ))

    def _generate_electronic_bass(self, bass: pretty_midi.Instrument, subgenre: ElectronicSubgenre,
                                 duration_bars: int, bar_duration: float):
        """Generate electronic basslines"""
        bass_notes = [24, 26, 28, 31, 33, 36]
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            subdivisions = 8
            step_duration = bar_duration / subdivisions
            
            for step in range(subdivisions):
                if step % 2 == 0 or random.random() < 0.3:
                    step_time = bar_start + step * step_duration
                    note = random.choice(bass_notes)
                    velocity = random.randint(80, 120)
                    duration = step_duration * random.uniform(0.6, 1.2)
                    
                    bass.notes.append(pretty_midi.Note(
                        velocity=velocity, pitch=note,
                        start=step_time, end=step_time + duration
                    ))

    def _generate_electronic_lead(self, lead: pretty_midi.Instrument, subgenre: ElectronicSubgenre,
                                 duration_bars: int, bar_duration: float):
        """Generate electronic lead synth"""
        scale = [60, 62, 64, 65, 67, 69, 71, 72]
        
        for bar in range(0, duration_bars, 4):
            bar_start = bar * bar_duration
            phrase_length = bar_duration * 4
            
            num_notes = random.randint(4, 12)
            
            for i in range(num_notes):
                note_time = bar_start + random.uniform(0, phrase_length)
                note_duration = random.uniform(0.25, 1.0)
                note_pitch = random.choice(scale) + random.choice([0, 12, 24])
                velocity = random.randint(70, 100)
                
                lead.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_pitch,
                    start=note_time, end=note_time + note_duration
                ))

    def _generate_electronic_pads(self, pads: pretty_midi.Instrument, subgenre: ElectronicSubgenre,
                                 duration_bars: int, bar_duration: float):
        """Generate atmospheric pads"""
        pad_chords = [[48, 52, 55], [46, 50, 53], [44, 48, 51], [49, 53, 56]]
        chord_duration = bar_duration * 4
        
        for bar in range(0, duration_bars, 4):
            bar_start = bar * bar_duration
            chord = random.choice(pad_chords)
            
            for note_pitch in chord:
                velocity = random.randint(40, 60)
                pads.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_pitch,
                    start=bar_start, end=bar_start + chord_duration
                ))

    def generate_training_dataset(self, output_dir: str = "midi_files", tracks_per_subgenre: int = 4):
        """Generate Electronic training dataset"""
        os.makedirs(output_dir, exist_ok=True)
        generated_files = []
        
        print("🎛️ Generating Electronic training dataset...")
        
        for subgenre in ElectronicSubgenre:
            print(f"🎵 Generating {tracks_per_subgenre} tracks for {subgenre.value}...")
            
            for track_num in range(tracks_per_subgenre):
                duration_bars = random.randint(16, 48)
                midi_track = self.generate_electronic_track(subgenre, duration_bars)
                
                filename = f"electronic_{subgenre.value}_{track_num + 1:02d}.mid"
                filepath = os.path.join(output_dir, filename)
                midi_track.write(filepath)
                
                generated_files.append(filepath)
                print(f"   ✅ Generated: {filename}")
        
        print(f"\n🎉 Electronic dataset complete! Generated {len(generated_files)} tracks")
        return generated_files

def main():
    """Generate Electronic training dataset"""
    generator = ElectronicMIDIGenerator()
    files = generator.generate_training_dataset(tracks_per_subgenre=4)
    print(f"\n🚀 Ready to train with {len(files)} Electronic tracks!")
    return len(files) > 0

if __name__ == "__main__":
    main()