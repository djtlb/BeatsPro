try:
    import pretty_midi
    PRETTY_MIDI_AVAILABLE = True
except ImportError:
    print("⚠️ pretty_midi not available, using simple MIDI fallback")
    PRETTY_MIDI_AVAILABLE = False
    # Import our simple MIDI generator as fallback
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'beat_addicts_core'))
    try:
        from simple_midi_generator import BeatAddictsSimpleMIDIGenerator
    except ImportError:
        print("❌ Simple MIDI generator fallback not available")

import numpy as np
import os
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class DNBSubgenre(Enum):
    """Drum and Bass subgenres with their characteristics"""
    LIQUID = "liquid"
    NEUROFUNK = "neurofunk"
    JUMP_UP = "jump_up"
    HARDSTEP = "hardstep"
    TECHSTEP = "techstep"
    JUNGLE = "jungle"
    RAGGA_JUNGLE = "ragga_jungle"
    DRUMFUNK = "drumfunk"
    MINIMAL = "minimal"
    DEEP = "deep"
    ROLLERS = "rollers"
    DARKSTEP = "darkstep"
    AMBIENT_DNB = "ambient_dnb"
    HALFTIME = "halftime"

@dataclass
class DNBCharacteristics:
    """Characteristics for each DNB subgenre"""
    bpm_range: Tuple[int, int]
    bass_complexity: float  # 0-1
    drum_complexity: float  # 0-1
    typical_sounds: List[str]
    rhythm_patterns: List[str]
    melodic_elements: bool
    atmosphere: str

class DrumAndBassMIDIGenerator:
    """Advanced Drum and Bass MIDI generator covering all subgenres"""
    
    def __init__(self):
        self.use_pretty_midi = PRETTY_MIDI_AVAILABLE
        if not self.use_pretty_midi:
            self.simple_generator = BeatAddictsSimpleMIDIGenerator()
        else:
            self.simple_generator = None
            
        self.subgenre_specs = {
            DNBSubgenre.LIQUID: DNBCharacteristics(
                bpm_range=(170, 180),
                bass_complexity=0.6,
                drum_complexity=0.5,
                typical_sounds=["smooth_bass", "jazz_samples", "vocal_chops"],
                rhythm_patterns=["liquid_break", "smooth_groove"],
                melodic_elements=True,
                atmosphere="smooth"
            ),
            DNBSubgenre.NEUROFUNK: DNBCharacteristics(
                bpm_range=(170, 180),
                bass_complexity=0.9,
                drum_complexity=0.8,
                typical_sounds=["reese_bass", "metallic_hits", "dystopian_fx"],
                rhythm_patterns=["complex_break", "syncopated"],
                melodic_elements=False,
                atmosphere="dark"
            ),
            DNBSubgenre.JUMP_UP: DNBCharacteristics(
                bpm_range=(172, 180),
                bass_complexity=0.7,
                drum_complexity=0.6,
                typical_sounds=["bouncy_bass", "vocal_stabs", "party_fx"],
                rhythm_patterns=["jump_break", "bouncy_groove"],
                melodic_elements=True,
                atmosphere="energetic"
            ),
            DNBSubgenre.JUNGLE: DNBCharacteristics(
                bpm_range=(160, 180),
                bass_complexity=0.8,
                drum_complexity=0.9,
                typical_sounds=["amen_break", "ragga_vocals", "sub_bass"],
                rhythm_patterns=["amen_chops", "jungle_groove"],
                melodic_elements=True,
                atmosphere="raw"
            ),
            DNBSubgenre.TECHSTEP: DNBCharacteristics(
                bpm_range=(170, 175),
                bass_complexity=0.8,
                drum_complexity=0.7,
                typical_sounds=["tech_bass", "industrial_fx", "metallic_drums"],
                rhythm_patterns=["tech_break", "industrial_groove"],
                melodic_elements=False,
                atmosphere="mechanical"
            ),
            DNBSubgenre.HARDSTEP: DNBCharacteristics(
                bpm_range=(174, 185),
                bass_complexity=0.9,
                drum_complexity=0.8,
                typical_sounds=["aggressive_bass", "distorted_breaks", "hard_fx"],
                rhythm_patterns=["hard_break", "aggressive_groove"],
                melodic_elements=False,
                atmosphere="aggressive"
            ),
            DNBSubgenre.DRUMFUNK: DNBCharacteristics(
                bpm_range=(165, 175),
                bass_complexity=0.5,
                drum_complexity=0.95,
                typical_sounds=["minimal_bass", "complex_breaks", "funk_samples"],
                rhythm_patterns=["complex_chops", "funk_groove"],
                melodic_elements=False,
                atmosphere="minimal"
            ),
            DNBSubgenre.MINIMAL: DNBCharacteristics(
                bpm_range=(170, 176),
                bass_complexity=0.4,
                drum_complexity=0.4,
                typical_sounds=["clean_bass", "minimal_fx", "space"],
                rhythm_patterns=["minimal_break", "clean_groove"],
                melodic_elements=True,
                atmosphere="spacious"
            ),
            DNBSubgenre.DEEP: DNBCharacteristics(
                bpm_range=(168, 174),
                bass_complexity=0.6,
                drum_complexity=0.5,
                typical_sounds=["deep_bass", "atmospheric_pads", "subtle_fx"],
                rhythm_patterns=["deep_groove", "rolling_break"],
                melodic_elements=True,
                atmosphere="deep"
            ),
            DNBSubgenre.ROLLERS: DNBCharacteristics(
                bpm_range=(172, 178),
                bass_complexity=0.7,
                drum_complexity=0.6,
                typical_sounds=["rolling_bass", "smooth_breaks", "groove_fx"],
                rhythm_patterns=["rolling_pattern", "smooth_groove"],
                melodic_elements=True,
                atmosphere="rolling"
            ),
            DNBSubgenre.DARKSTEP: DNBCharacteristics(
                bpm_range=(170, 180),
                bass_complexity=0.8,
                drum_complexity=0.7,
                typical_sounds=["dark_bass", "horror_fx", "industrial_drums"],
                rhythm_patterns=["dark_break", "sinister_groove"],
                melodic_elements=False,
                atmosphere="dark"
            ),
            DNBSubgenre.AMBIENT_DNB: DNBCharacteristics(
                bpm_range=(160, 170),
                bass_complexity=0.4,
                drum_complexity=0.3,
                typical_sounds=["ambient_bass", "ethereal_pads", "nature_fx"],
                rhythm_patterns=["ambient_break", "floating_groove"],
                melodic_elements=True,
                atmosphere="ethereal"
            ),
            DNBSubgenre.HALFTIME: DNBCharacteristics(
                bpm_range=(85, 95),  # Half tempo
                bass_complexity=0.8,
                drum_complexity=0.6,
                typical_sounds=["wobble_bass", "trap_snares", "modern_fx"],
                rhythm_patterns=["halftime_break", "trap_groove"],
                melodic_elements=True,
                atmosphere="modern"
            ),
            DNBSubgenre.RAGGA_JUNGLE: DNBCharacteristics(
                bpm_range=(160, 180),
                bass_complexity=0.8,
                drum_complexity=0.9,
                typical_sounds=["ragga_bass", "jamaican_vocals", "reggae_fx"],
                rhythm_patterns=["ragga_chops", "caribbean_groove"],
                melodic_elements=True,
                atmosphere="tropical"
            )
        }
        
        # Common DNB drum patterns
        self.drum_patterns = {
            "basic_dnb": [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
            "amen_break": [1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],
            "think_break": [1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1],
            "complex_chop": [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            "minimal_break": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            "jungle_rapid": [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1]
        }
        
        # Bass patterns for different subgenres
        self.bass_patterns = {
            "liquid_bass": [(36, 0, 480), (38, 480, 240), (36, 720, 240), (40, 960, 480)],
            "neurofunk_bass": [(30, 0, 120), (32, 120, 120), (28, 240, 360), (35, 600, 240)],
            "jump_up_bass": [(36, 0, 240), (43, 240, 120), (36, 360, 120), (40, 480, 240)],
            "minimal_bass": [(36, 0, 960), (38, 960, 960)],
            "rolling_bass": [(36, 0, 120), (36, 240, 120), (38, 360, 120), (36, 480, 120)]
        }
    
    def generate_dnb_track(self, subgenre: DNBSubgenre, duration_bars: int = 32) -> pretty_midi.PrettyMIDI:
        """Generate a complete DNB track for the specified subgenre"""
        
        specs = self.subgenre_specs[subgenre]
        bpm = random.randint(*specs.bpm_range)
        
        # Create MIDI object
        midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
        
        # Add instruments
        drums = pretty_midi.Instrument(program=0, is_drum=True, name="Drums")
        bass = pretty_midi.Instrument(program=38, name="Bass")  # Synth Bass 1
        
        # Add melodic elements if characteristic of the subgenre
        if specs.melodic_elements:
            lead = pretty_midi.Instrument(program=81, name="Lead")  # Sawtooth Lead
            pads = pretty_midi.Instrument(program=88, name="Pads")  # Warm Pad
        
        # Generate sections
        bar_duration = 60 / bpm * 4  # Duration of one bar in seconds
        total_duration = duration_bars * bar_duration
        
        # Generate drum track
        self._generate_drums(drums, subgenre, duration_bars, bar_duration)
        
        # Generate bass track
        self._generate_bass(bass, subgenre, duration_bars, bar_duration)
        
        # Add melodic elements
        if specs.melodic_elements:
            self._generate_melody(lead, subgenre, duration_bars, bar_duration)
            self._generate_pads(pads, subgenre, duration_bars, bar_duration)
            midi.instruments.extend([lead, pads])
        
        # Add FX and atmosphere
        fx = pretty_midi.Instrument(program=122, name="FX")  # Seashore/Noise
        self._generate_fx(fx, subgenre, duration_bars, bar_duration)
        
        midi.instruments.extend([drums, bass, fx])
        
        return midi
    
    def _generate_drums(self, drums: pretty_midi.Instrument, subgenre: DNBSubgenre, 
                       duration_bars: int, bar_duration: float):
        """Generate drum patterns specific to DNB subgenre"""
        
        specs = self.subgenre_specs[subgenre]
        
        # Kick drum (36), Snare (38), Hi-hat (42), Crash (49), Ride (51)
        kick_note = 36
        snare_note = 38
        hihat_note = 42
        
        # Select appropriate pattern based on subgenre
        if subgenre in [DNBSubgenre.JUNGLE, DNBSubgenre.RAGGA_JUNGLE]:
            pattern = self.drum_patterns["amen_break"]
        elif subgenre == DNBSubgenre.DRUMFUNK:
            pattern = self.drum_patterns["complex_chop"]
        elif subgenre == DNBSubgenre.MINIMAL:
            pattern = self.drum_patterns["minimal_break"]
        elif subgenre in [DNBSubgenre.NEUROFUNK, DNBSubgenre.DARKSTEP]:
            pattern = self.drum_patterns["think_break"]
        else:
            pattern = self.drum_patterns["basic_dnb"]
        
        # Generate drum hits
        step_duration = bar_duration / 16  # 16th note steps
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            
            # Add variation every 4 bars
            current_pattern = pattern.copy()
            if bar % 4 == 3:  # Fill bar
                current_pattern = self._add_drum_fills(current_pattern, specs.drum_complexity)
            
            for step, hit in enumerate(current_pattern):
                if hit:
                    step_time = bar_start + step * step_duration
                    
                    # Kick on steps 0, 4, 8, 12 (with variations)
                    if step % 4 == 0:
                        velocity = random.randint(100, 127)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=kick_note,
                            start=step_time, end=step_time + step_duration * 0.8
                        ))
                    
                    # Snare on steps 4, 12 (with ghost notes)
                    elif step in [4, 12] or (random.random() < specs.drum_complexity * 0.3):
                        velocity = random.randint(80, 120) if step in [4, 12] else random.randint(40, 70)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=snare_note,
                            start=step_time, end=step_time + step_duration * 0.6
                        ))
                    
                    # Hi-hats with complexity based on subgenre
                    if random.random() < specs.drum_complexity:
                        velocity = random.randint(30, 80)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=hihat_note,
                            start=step_time, end=step_time + step_duration * 0.3
                        ))
    
    def _add_drum_fills(self, pattern: List[int], complexity: float) -> List[int]:
        """Add drum fills based on complexity"""
        fill_pattern = pattern.copy()
        
        # Add extra hits based on complexity
        for i in range(len(fill_pattern)):
            if random.random() < complexity * 0.5:
                fill_pattern[i] = 1
        
        return fill_pattern
    
    def _generate_bass(self, bass: pretty_midi.Instrument, subgenre: DNBSubgenre,
                      duration_bars: int, bar_duration: float):
        """Generate bass lines characteristic of each DNB subgenre"""
        
        specs = self.subgenre_specs[subgenre]
        
        # Bass note ranges for different subgenres
        if subgenre in [DNBSubgenre.NEUROFUNK, DNBSubgenre.DARKSTEP]:
            bass_notes = [24, 26, 28, 30, 31]  # Lower, darker
        elif subgenre in [DNBSubgenre.LIQUID, DNBSubgenre.DEEP]:
            bass_notes = [28, 31, 33, 35, 36]  # Warmer mid-range
        elif subgenre == DNBSubgenre.JUMP_UP:
            bass_notes = [31, 33, 36, 38, 40]  # Higher, bouncier
        else:
            bass_notes = [26, 28, 31, 33, 35]  # Standard range
        
        # Generate bass pattern
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            
            if subgenre == DNBSubgenre.MINIMAL:
                # Minimal: long sustained notes
                note_duration = bar_duration * 2  # 2 bar notes
                if bar % 2 == 0:
                    note = random.choice(bass_notes)
                    velocity = random.randint(80, 110)
                    bass.notes.append(pretty_midi.Note(
                        velocity=velocity, pitch=note,
                        start=bar_start, end=bar_start + note_duration
                    ))
            
            elif subgenre in [DNBSubgenre.NEUROFUNK, DNBSubgenre.TECHSTEP]:
                # Complex, syncopated bass
                subdivisions = 8
                step_duration = bar_duration / subdivisions
                
                for step in range(subdivisions):
                    if random.random() < specs.bass_complexity:
                        step_time = bar_start + step * step_duration
                        note = random.choice(bass_notes)
                        velocity = random.randint(90, 127)
                        duration = step_duration * random.uniform(0.5, 1.5)
                        
                        bass.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=note,
                            start=step_time, end=step_time + duration
                        ))
            
            elif subgenre == DNBSubgenre.ROLLERS:
                # Rolling bass pattern
                subdivisions = 16
                step_duration = bar_duration / subdivisions
                
                for step in range(subdivisions):
                    if step % 2 == 0:  # On beat
                        step_time = bar_start + step * step_duration
                        note = bass_notes[step % len(bass_notes)]
                        velocity = random.randint(85, 115)
                        
                        bass.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=note,
                            start=step_time, end=step_time + step_duration * 0.8
                        ))
            
            else:
                # Standard DNB bass pattern
                subdivisions = 4
                step_duration = bar_duration / subdivisions
                
                for step in range(subdivisions):
                    if random.random() < 0.8:  # 80% chance of note
                        step_time = bar_start + step * step_duration
                        note = random.choice(bass_notes)
                        velocity = random.randint(85, 120)
                        duration = step_duration * random.uniform(0.6, 1.2)
                        
                        bass.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=note,
                            start=step_time, end=step_time + duration
                        ))
    
    def _generate_melody(self, lead: pretty_midi.Instrument, subgenre: DNBSubgenre,
                        duration_bars: int, bar_duration: float):
        """Generate melodic elements for melodic subgenres"""
        
        # Melodic patterns based on subgenre
        if subgenre == DNBSubgenre.LIQUID:
            # Smooth, flowing melodies
            scale = [60, 62, 64, 65, 67, 69, 71, 72]  # C major
            melody_density = 0.3
        elif subgenre == DNBSubgenre.JUMP_UP:
            # Catchy, bouncy melodies
            scale = [60, 62, 64, 67, 69, 72, 74, 76]  # Pentatonic-ish
            melody_density = 0.4
        elif subgenre in [DNBSubgenre.DEEP, DNBSubgenre.AMBIENT_DNB]:
            # Atmospheric, sparse melodies
            scale = [60, 63, 65, 67, 70, 72, 75, 77]  # Minor-ish
            melody_density = 0.2
        else:
            scale = [60, 62, 64, 66, 67, 69, 71, 72]
            melody_density = 0.3
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            
            # Generate melodic phrases every 4 bars
            if bar % 4 == 0:
                phrase_length = bar_duration * 4
                num_notes = int(phrase_length / (bar_duration / 4) * melody_density)
                
                for i in range(num_notes):
                    note_time = bar_start + random.uniform(0, phrase_length)
                    note_duration = random.uniform(0.2, 1.0)
                    note_pitch = random.choice(scale) + random.choice([0, 12, 24])
                    velocity = random.randint(60, 90)
                    
                    lead.notes.append(pretty_midi.Note(
                        velocity=velocity, pitch=note_pitch,
                        start=note_time, end=note_time + note_duration
                    ))
    
    def _generate_pads(self, pads: pretty_midi.Instrument, subgenre: DNBSubgenre,
                      duration_bars: int, bar_duration: float):
        """Generate atmospheric pad sounds"""
        
        # Chord progressions for different subgenres
        if subgenre == DNBSubgenre.LIQUID:
            chords = [[48, 52, 55, 59], [46, 50, 53, 57], [45, 48, 52, 55], [43, 47, 50, 54]]
        elif subgenre in [DNBSubgenre.DEEP, DNBSubgenre.AMBIENT_DNB]:
            chords = [[48, 51, 55, 58], [46, 49, 53, 56], [44, 47, 51, 54], [42, 45, 49, 52]]
        else:
            chords = [[48, 52, 55], [45, 48, 52], [43, 47, 50], [40, 44, 47]]
        
        chord_duration = bar_duration * 4  # 4 bar chords
        
        for bar in range(0, duration_bars, 4):
            bar_start = bar * bar_duration
            chord = random.choice(chords)
            
            for note_pitch in chord:
                velocity = random.randint(40, 70)
                pads.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_pitch,
                    start=bar_start, end=bar_start + chord_duration
                ))
    
    def _generate_fx(self, fx: pretty_midi.Instrument, subgenre: DNBSubgenre,
                    duration_bars: int, bar_duration: float):
        """Generate atmospheric FX and sweeps"""
        
        specs = self.subgenre_specs[subgenre]
        
        # FX density based on atmosphere
        fx_density = 0.1 if specs.atmosphere in ["minimal", "clean"] else 0.3
        
        for bar in range(duration_bars):
            if random.random() < fx_density:
                bar_start = bar * bar_duration
                fx_time = bar_start + random.uniform(0, bar_duration)
                fx_duration = random.uniform(0.5, 2.0)
                fx_pitch = random.randint(80, 100)
                velocity = random.randint(30, 60)
                
                fx.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=fx_pitch,
                    start=fx_time, end=fx_time + fx_duration
                ))
    
    def generate_simple_dnb_track(self, subgenre_name: str = "liquid", duration_bars: int = 32, output_file: Optional[str] = None) -> Optional[str]:
        """Generate DNB track using simple MIDI generator when pretty_midi is not available"""
        if self.use_pretty_midi:
            # Use the original complex method if pretty_midi is available
            try:
                subgenre = DNBSubgenre(subgenre_name.lower())
                midi_result = self.generate_dnb_track(subgenre, duration_bars)
                if output_file:
                    midi_result.write(output_file)
                    return output_file
                else:
                    temp_file = f"dnb_{subgenre_name}_{duration_bars}bars.mid"
                    midi_result.write(temp_file)
                    return temp_file
            except Exception as e:
                print(f"⚠️ Pretty MIDI generation failed: {e}, using simple fallback")
                self.use_pretty_midi = False
        
        # Use simple generator fallback
        if not self.use_pretty_midi and self.simple_generator:
            print(f"🎵 Using simple MIDI generator for DNB {subgenre_name}")
            return self.simple_generator.generate_beat('dnb', duration_bars, output_file)
        else:
            print("❌ No MIDI generation method available")
            return None

    def generate_training_dataset(self, output_dir: str = "midi_files", tracks_per_subgenre: int = 4) -> List[str]:
        """Generate comprehensive DNB training dataset"""
        os.makedirs(output_dir, exist_ok=True)
        generated_files = []
        
        print("🎵 BEAT ADDICTS DNB - Generating Training Dataset")
        
        dnb_subgenres = ["liquid", "neurofunk", "jump_up", "darkstep", "deep"]
        
        for subgenre in dnb_subgenres:
            print(f"   🎼 Generating {subgenre.upper()} tracks...")
            
            for i in range(tracks_per_subgenre):
                bars = 16 + (i * 8)  # Vary track length
                filename = os.path.join(output_dir, f"dnb_{subgenre}_{i+1:02d}.mid")
                
                result = self.generate_simple_dnb_track(subgenre, bars, filename)
                if result:
                    generated_files.append(result)
                    print(f"      ✅ Generated: {os.path.basename(result)}")
        
        print(f"🎯 DNB Dataset complete: {len(generated_files)} files generated")
        return generated_files

    # ...existing code...
    
def main():
    """Generate the complete DNB training dataset"""
    try:
        print("Drum and Bass MIDI Generator v2.0")
        print("=" * 40)
        
        generator = DrumAndBassMIDIGenerator()
        
        # Check if output directory exists
        output_dir = "midi_files"
        if not os.path.exists(output_dir):
            print(f"Creating output directory: {output_dir}")
            os.makedirs(output_dir)
        
        # Generate comprehensive dataset
        print("Starting DNB dataset generation...")
        files = generator.generate_training_dataset(
            output_dir=output_dir,
            tracks_per_subgenre=8  # 8 tracks per subgenre = 112 total tracks
        )
        
        print(f"\nSUCCESS: Generated {len(files)} DNB tracks!")
        print(f"Files saved to: {os.path.abspath(output_dir)}")
        print("\nNext steps:")
        print("1. Run: python run.py")
        print("2. Upload the generated MIDI files")
        print("3. Start training your AI!")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: Failed to generate dataset")
        print(f"Details: {str(e)}")
        print("\nTroubleshooting:")
        print("- Check disk space (need ~50MB)")
        print("- Ensure write permissions in current directory")
        print("- Try running as administrator if needed")
        return False

if __name__ == "__main__":
    main()
