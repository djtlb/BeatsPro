import pretty_midi
import numpy as np
import os
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

class CountrySubgenre(Enum):
    """Country music subgenres"""
    TRADITIONAL = "traditional"
    BLUEGRASS = "bluegrass"
    COUNTRY_ROCK = "country_rock"
    COUNTRY_POP = "country_pop"
    OUTLAW_COUNTRY = "outlaw_country"
    HONKY_TONK = "honky_tonk"
    WESTERN_SWING = "western_swing"
    AMERICANA = "americana"
    ALT_COUNTRY = "alt_country"
    COUNTRY_FOLK = "country_folk"
    SOUTHERN_ROCK = "southern_rock"
    TEXAS_COUNTRY = "texas_country"
    NASHVILLE_SOUND = "nashville_sound"
    BAKERSFIELD_SOUND = "bakersfield_sound"
    COUNTRY_BLUES = "country_blues"

@dataclass
class CountryCharacteristics:
    """Characteristics for each Country subgenre"""
    bpm_range: Tuple[int, int]
    rhythm_style: str
    instrumentation: List[str]
    vocal_style: str
    chord_complexity: float
    atmosphere: str
    storytelling: bool

class CountryMIDIGenerator:
    """Country music MIDI generator covering all subgenres"""
    
    def __init__(self):
        self.subgenre_specs = {
            CountrySubgenre.TRADITIONAL: CountryCharacteristics(
                bpm_range=(90, 120), rhythm_style="steady", 
                instrumentation=["acoustic_guitar", "steel_guitar", "fiddle", "bass"],
                vocal_style="storytelling", chord_complexity=0.5, 
                atmosphere="nostalgic", storytelling=True
            ),
            CountrySubgenre.BLUEGRASS: CountryCharacteristics(
                bpm_range=(120, 160), rhythm_style="driving",
                instrumentation=["banjo", "mandolin", "fiddle", "acoustic_guitar", "upright_bass"],
                vocal_style="harmonious", chord_complexity=0.7,
                atmosphere="energetic", storytelling=True
            ),
            CountrySubgenre.COUNTRY_ROCK: CountryCharacteristics(
                bpm_range=(110, 140), rhythm_style="rock_steady",
                instrumentation=["electric_guitar", "drums", "bass", "steel_guitar"],
                vocal_style="powerful", chord_complexity=0.6,
                atmosphere="driving", storytelling=True
            ),
            CountrySubgenre.COUNTRY_POP: CountryCharacteristics(
                bpm_range=(80, 120), rhythm_style="laid_back",
                instrumentation=["synths", "electric_guitar", "bass", "drums"],
                vocal_style="smooth", chord_complexity=0.4,
                atmosphere="uplifting", storytelling=False
            ),
            CountrySubgenre.OUTLAW_COUNTRY: CountryCharacteristics(
                bpm_range=(90, 130), rhythm_style="steady",
                instrumentation=["acoustic_guitar", "harmonica", "bass", "drums"],
                vocal_style="gritty", chord_complexity=0.5,
                atmosphere="rebellious", storytelling=True
            ),
            CountrySubgenre.HONKY_TONK: CountryCharacteristics(
                bpm_range=(100, 130), rhythm_style="shuffle",
                instrumentation=["piano", "steel_guitar", "fiddle", "drums"],
                vocal_style="twangy", chord_complexity=0.5,
                atmosphere="barroom", storytelling=True
            ),
            CountrySubgenre.WESTERN_SWING: CountryCharacteristics(
                bpm_range=(120, 160), rhythm_style="swing",
                instrumentation=["fiddle", "steel_guitar", "piano", "horns"],
                vocal_style="smooth", chord_complexity=0.8,
                atmosphere="danceable", storytelling=False
            )
        }

    def generate_country_track(self, subgenre: CountrySubgenre, duration_bars: int = 32) -> pretty_midi.PrettyMIDI:
        """Generate a complete Country track"""
        specs = self.subgenre_specs[subgenre]
        bpm = random.randint(*specs.bpm_range)
        
        midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
        
        # Add instruments
        drums = pretty_midi.Instrument(program=0, is_drum=True, name="Drums")
        bass = pretty_midi.Instrument(program=32, name="Acoustic Bass")
        guitar = pretty_midi.Instrument(program=25, name="Steel Guitar")
        fiddle = pretty_midi.Instrument(program=40, name="Violin")
        
        bar_duration = 60 / bpm * 4
        
        self._generate_country_drums(drums, subgenre, duration_bars, bar_duration)
        self._generate_country_bass(bass, subgenre, duration_bars, bar_duration)
        self._generate_country_guitar(guitar, subgenre, duration_bars, bar_duration)
        self._generate_country_fiddle(fiddle, subgenre, duration_bars, bar_duration)
        
        midi.instruments.extend([drums, bass, guitar, fiddle])
        return midi

    def _generate_country_drums(self, drums: pretty_midi.Instrument, subgenre: CountrySubgenre,
                               duration_bars: int, bar_duration: float):
        """Generate country drum patterns"""
        kick_note = 36
        snare_note = 38
        hihat_note = 42
        
        # Basic country pattern
        pattern = [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        step_duration = bar_duration / 16
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            
            for step, hit in enumerate(pattern):
                if hit:
                    step_time = bar_start + step * step_duration
                    
                    if step % 4 == 0:  # Kick
                        velocity = random.randint(90, 120)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=kick_note,
                            start=step_time, end=step_time + step_duration * 0.8
                        ))
                    
                    elif step in [4, 12]:  # Snare
                        velocity = random.randint(70, 100)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=snare_note,
                            start=step_time, end=step_time + step_duration * 0.6
                        ))

    def _generate_country_bass(self, bass: pretty_midi.Instrument, subgenre: CountrySubgenre,
                              duration_bars: int, bar_duration: float):
        """Generate country basslines"""
        bass_notes = [28, 31, 33, 35, 36, 38, 40]
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            subdivisions = 4
            step_duration = bar_duration / subdivisions
            
            for step in range(subdivisions):
                if step == 0 or random.random() < 0.4:
                    step_time = bar_start + step * step_duration
                    note = random.choice(bass_notes)
                    velocity = random.randint(70, 100)
                    duration = step_duration * 0.8
                    
                    bass.notes.append(pretty_midi.Note(
                        velocity=velocity, pitch=note,
                        start=step_time, end=step_time + duration
                    ))

    def _generate_country_guitar(self, guitar: pretty_midi.Instrument, subgenre: CountrySubgenre,
                                duration_bars: int, bar_duration: float):
        """Generate country guitar parts"""
        chord_notes = [48, 52, 55, 60]  # C major chord spread
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            
            for note in chord_notes:
                velocity = random.randint(50, 80)
                guitar.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note,
                    start=bar_start, end=bar_start + bar_duration
                ))

    def _generate_country_fiddle(self, fiddle: pretty_midi.Instrument, subgenre: CountrySubgenre,
                                duration_bars: int, bar_duration: float):
        """Generate country fiddle melodies"""
        scale = [60, 62, 64, 65, 67, 69, 71, 72]
        
        for bar in range(0, duration_bars, 2):
            bar_start = bar * bar_duration
            phrase_length = bar_duration * 2
            
            num_notes = random.randint(4, 8)
            
            for i in range(num_notes):
                note_time = bar_start + random.uniform(0, phrase_length)
                note_duration = random.uniform(0.25, 0.5)
                note_pitch = random.choice(scale) + random.choice([0, 12])
                velocity = random.randint(60, 90)
                
                fiddle.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_pitch,
                    start=note_time, end=note_time + note_duration
                ))

    def generate_training_dataset(self, output_dir: str = "midi_files", tracks_per_subgenre: int = 4):
        """Generate Country training dataset"""
        os.makedirs(output_dir, exist_ok=True)
        generated_files = []
        
        print("🤠 Generating Country training dataset...")
        
        for subgenre in CountrySubgenre:
            print(f"🎵 Generating {tracks_per_subgenre} tracks for {subgenre.value}...")
            
            for track_num in range(tracks_per_subgenre):
                duration_bars = random.randint(16, 48)
                midi_track = self.generate_country_track(subgenre, duration_bars)
                
                filename = f"country_{subgenre.value}_{track_num + 1:02d}.mid"
                filepath = os.path.join(output_dir, filename)
                midi_track.write(filepath)
                
                generated_files.append(filepath)
                print(f"   ✅ Generated: {filename}")
        
        print(f"\n🎉 Country dataset complete! Generated {len(generated_files)} tracks")
        return generated_files

def main():
    """Generate Country training dataset"""
    generator = CountryMIDIGenerator()
    files = generator.generate_training_dataset(tracks_per_subgenre=4)
    print(f"\n🚀 Ready to train with {len(files)} Country tracks!")
    return len(files) > 0

if __name__ == "__main__":
    main()