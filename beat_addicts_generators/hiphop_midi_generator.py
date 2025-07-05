import pretty_midi
import numpy as np
import os
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

class HipHopSubgenre(Enum):
    """Hip-Hop subgenres with their characteristics"""
    OLD_SCHOOL = "old_school"
    BOOM_BAP = "boom_bap"
    GANGSTA_RAP = "gangsta_rap"
    TRAP = "trap"
    DRILL = "drill"
    MUMBLE_RAP = "mumble_rap"
    CONSCIOUS_RAP = "conscious_rap"
    JAZZ_RAP = "jazz_rap"
    EXPERIMENTAL = "experimental"
    PHONK = "phonk"
    CRUNK = "crunk"
    DIRTY_SOUTH = "dirty_south"
    WEST_COAST = "west_coast"
    EAST_COAST = "east_coast"
    MIDWEST = "midwest"
    UK_DRILL = "uk_drill"
    AFRO_TRAP = "afro_trap"
    CLOUD_RAP = "cloud_rap"
    HORRORCORE = "horrorcore"
    HYPHY = "hyphy"

@dataclass
class HipHopCharacteristics:
    """Characteristics for each Hip-Hop subgenre"""
    bpm_range: Tuple[int, int]
    drum_complexity: float  # 0-1
    bass_style: str
    typical_sounds: List[str]
    rhythm_patterns: List[str]
    melodic_elements: bool
    atmosphere: str
    swing_factor: float  # 0-1, how much swing/shuffle

class HipHopMIDIGenerator:
    """Advanced Hip-Hop MIDI generator covering all subgenres"""
    
    def __init__(self):
        self.subgenre_specs = {
            HipHopSubgenre.OLD_SCHOOL: HipHopCharacteristics(
                bpm_range=(100, 120),
                drum_complexity=0.5,
                bass_style="funky",
                typical_sounds=["vinyl_crackle", "breaks", "scratches"],
                rhythm_patterns=["four_four", "break_beat"],
                melodic_elements=True,
                atmosphere="nostalgic",
                swing_factor=0.3
            ),
            HipHopSubgenre.BOOM_BAP: HipHopCharacteristics(
                bpm_range=(85, 100),
                drum_complexity=0.6,
                bass_style="punchy",
                typical_sounds=["vinyl_kicks", "snare_snaps", "jazz_samples"],
                rhythm_patterns=["boom_bap", "head_nod"],
                melodic_elements=True,
                atmosphere="gritty",
                swing_factor=0.4
            ),
            HipHopSubgenre.GANGSTA_RAP: HipHopCharacteristics(
                bpm_range=(85, 105),
                drum_complexity=0.5,
                bass_style="heavy",
                typical_sounds=["808_drums", "synth_leads", "vocal_chops"],
                rhythm_patterns=["g_funk", "west_coast"],
                melodic_elements=True,
                atmosphere="aggressive",
                swing_factor=0.2
            ),
            HipHopSubgenre.TRAP: HipHopCharacteristics(
                bpm_range=(130, 150),
                drum_complexity=0.8,
                bass_style="808_heavy",
                typical_sounds=["trap_snares", "hi_hat_rolls", "synth_plucks"],
                rhythm_patterns=["trap_pattern", "triplet_hats"],
                melodic_elements=True,
                atmosphere="modern",
                swing_factor=0.1
            ),
            HipHopSubgenre.DRILL: HipHopCharacteristics(
                bpm_range=(130, 160),
                drum_complexity=0.9,
                bass_style="sliding_808",
                typical_sounds=["drill_snares", "sliding_bass", "dark_pads"],
                rhythm_patterns=["drill_pattern", "syncopated"],
                melodic_elements=False,
                atmosphere="menacing",
                swing_factor=0.1
            ),
            HipHopSubgenre.MUMBLE_RAP: HipHopCharacteristics(
                bpm_range=(120, 140),
                drum_complexity=0.6,
                bass_style="melodic_808",
                typical_sounds=["autotune_vocals", "lush_pads", "bell_sounds"],
                rhythm_patterns=["melodic_trap", "flowing"],
                melodic_elements=True,
                atmosphere="dreamy",
                swing_factor=0.2
            ),
            HipHopSubgenre.CONSCIOUS_RAP: HipHopCharacteristics(
                bpm_range=(85, 110),
                drum_complexity=0.6,
                bass_style="organic",
                typical_sounds=["live_drums", "soul_samples", "jazz_chords"],
                rhythm_patterns=["soul_groove", "live_feel"],
                melodic_elements=True,
                atmosphere="uplifting",
                swing_factor=0.5
            ),
            HipHopSubgenre.JAZZ_RAP: HipHopCharacteristics(
                bpm_range=(90, 120),
                drum_complexity=0.7,
                bass_style="walking",
                typical_sounds=["jazz_samples", "upright_bass", "horn_sections"],
                rhythm_patterns=["jazz_swing", "complex"],
                melodic_elements=True,
                atmosphere="sophisticated",
                swing_factor=0.6
            ),
            HipHopSubgenre.EXPERIMENTAL: HipHopCharacteristics(
                bpm_range=(70, 140),
                drum_complexity=0.8,
                bass_style="abstract",
                typical_sounds=["glitch", "ambient_textures", "field_recordings"],
                rhythm_patterns=["irregular", "polyrhythmic"],
                melodic_elements=True,
                atmosphere="avant_garde",
                swing_factor=0.3
            ),
            HipHopSubgenre.PHONK: HipHopCharacteristics(
                bpm_range=(120, 140),
                drum_complexity=0.7,
                bass_style="distorted_808",
                typical_sounds=["cowbell", "vocal_chops", "lo_fi_drums"],
                rhythm_patterns=["phonk_groove", "memphis_style"],
                melodic_elements=True,
                atmosphere="dark",
                swing_factor=0.3
            ),
            HipHopSubgenre.CRUNK: HipHopCharacteristics(
                bpm_range=(70, 90),
                drum_complexity=0.5,
                bass_style="booming_808",
                typical_sounds=["heavy_drums", "chant_vocals", "synth_stabs"],
                rhythm_patterns=["crunk_bounce", "slow_heavy"],
                melodic_elements=False,
                atmosphere="aggressive",
                swing_factor=0.2
            ),
            HipHopSubgenre.DIRTY_SOUTH: HipHopCharacteristics(
                bpm_range=(65, 85),
                drum_complexity=0.6,
                bass_style="trunk_rattling",
                typical_sounds=["car_audio", "vocal_chops", "orchestral_hits"],
                rhythm_patterns=["bounce", "southern_swing"],
                melodic_elements=True,
                atmosphere="swaggering",
                swing_factor=0.4
            ),
            HipHopSubgenre.WEST_COAST: HipHopCharacteristics(
                bpm_range=(85, 105),
                drum_complexity=0.6,
                bass_style="g_funk",
                typical_sounds=["talk_box", "funk_samples", "whiny_synths"],
                rhythm_patterns=["g_funk_groove", "laid_back"],
                melodic_elements=True,
                atmosphere="smooth",
                swing_factor=0.3
            ),
            HipHopSubgenre.EAST_COAST: HipHopCharacteristics(
                bpm_range=(85, 100),
                drum_complexity=0.7,
                bass_style="punchy",
                typical_sounds=["jazz_samples", "vinyl_crackle", "string_sections"],
                rhythm_patterns=["boom_bap", "complex"],
                melodic_elements=True,
                atmosphere="lyrical",
                swing_factor=0.4
            ),
            HipHopSubgenre.UK_DRILL: HipHopCharacteristics(
                bpm_range=(135, 155),
                drum_complexity=0.9,
                bass_style="sliding_808",
                typical_sounds=["uk_drill_snares", "dark_pads", "ethnic_samples"],
                rhythm_patterns=["uk_drill_pattern", "offbeat"],
                melodic_elements=False,
                atmosphere="gritty",
                swing_factor=0.1
            ),
            HipHopSubgenre.AFRO_TRAP: HipHopCharacteristics(
                bpm_range=(110, 130),
                drum_complexity=0.7,
                bass_style="afro_808",
                typical_sounds=["african_drums", "ethnic_vocals", "trap_elements"],
                rhythm_patterns=["afrobeat", "trap_fusion"],
                melodic_elements=True,
                atmosphere="cultural",
                swing_factor=0.3
            ),
            HipHopSubgenre.CLOUD_RAP: HipHopCharacteristics(
                bpm_range=(60, 90),
                drum_complexity=0.4,
                bass_style="ethereal",
                typical_sounds=["ambient_pads", "reverb_vocals", "dreamy_synths"],
                rhythm_patterns=["floating", "minimal"],
                melodic_elements=True,
                atmosphere="ethereal",
                swing_factor=0.2
            ),
            HipHopSubgenre.HORRORCORE: HipHopCharacteristics(
                bpm_range=(80, 110),
                drum_complexity=0.6,
                bass_style="menacing",
                typical_sounds=["horror_samples", "distorted_vocals", "eerie_pads"],
                rhythm_patterns=["horror_groove", "unsettling"],
                melodic_elements=True,
                atmosphere="dark",
                swing_factor=0.3
            ),
            HipHopSubgenre.HYPHY: HipHopCharacteristics(
                bpm_range=(120, 140),
                drum_complexity=0.7,
                bass_style="bouncy",
                typical_sounds=["synth_leads", "vocal_chops", "party_sounds"],
                rhythm_patterns=["hyphy_bounce", "energetic"],
                melodic_elements=True,
                atmosphere="party",
                swing_factor=0.2
            )
        }
        
        # Common hip-hop drum patterns
        self.drum_patterns = {
            "boom_bap": [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
            "trap_pattern": [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1],
            "drill_pattern": [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],
            "old_school": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            "crunk_bounce": [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
            "g_funk": [1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0]
        }
        
        # Bass patterns for different subgenres
        self.bass_patterns = {
            "808_heavy": [(36, 0, 480), (36, 720, 240), (38, 960, 480), (36, 1440, 240)],
            "boom_bap": [(36, 0, 240), (40, 480, 240), (36, 720, 240), (38, 960, 240)],
            "g_funk": [(36, 0, 360), (38, 480, 120), (36, 720, 240), (40, 960, 360)],
            "sliding_808": [(36, 0, 120), (37, 120, 120), (38, 240, 120), (36, 480, 360)],
            "walking": [(36, 0, 240), (38, 240, 240), (40, 480, 240), (38, 720, 240)]
        }
    
    def generate_hiphop_track(self, subgenre: HipHopSubgenre, duration_bars: int = 32) -> pretty_midi.PrettyMIDI:
        """Generate a complete Hip-Hop track for the specified subgenre"""
        
        specs = self.subgenre_specs[subgenre]
        bpm = random.randint(*specs.bpm_range)
        
        # Create MIDI object
        midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
        
        # Add instruments with intelligent voice assignment
        drums = pretty_midi.Instrument(program=0, is_drum=True, name="Drums")
        
        # Select bass program based on subgenre
        bass_programs = {
            HipHopSubgenre.TRAP: 37,  # Synth Bass 1
            HipHopSubgenre.DRILL: 38,  # Synth Bass 2  
            HipHopSubgenre.BOOM_BAP: 33,  # Electric Bass (finger)
            HipHopSubgenre.JAZZ_RAP: 32,  # Acoustic Bass
        }
        bass_program = bass_programs.get(subgenre, 33)
        bass = pretty_midi.Instrument(program=bass_program, name="Bass")
        
        # Add melodic elements if characteristic of the subgenre
        if specs.melodic_elements:
            # Select lead program based on subgenre atmosphere
            lead_programs = {
                "modern": 81,  # Sawtooth
                "dreamy": 89,  # Warm Pad
                "sophisticated": 96,  # FX 1 (rain)
                "dark": 80,  # Square
            }
            lead_program = lead_programs.get(specs.atmosphere, 81)
            lead = pretty_midi.Instrument(program=lead_program, name="Lead")
            
            # Piano program based on subgenre
            piano_programs = {
                HipHopSubgenre.JAZZ_RAP: 0,  # Acoustic Grand Piano
                HipHopSubgenre.CONSCIOUS_RAP: 1,  # Bright Acoustic Piano
            }
            piano_program = piano_programs.get(subgenre, 4)  # Electric Piano 1
            piano = pretty_midi.Instrument(program=piano_program, name="Piano")
        
        # Generate sections
        bar_duration = 60 / bpm * 4  # Duration of one bar in seconds
        
        # Generate tracks with intelligent voice assignment
        self._generate_hiphop_drums(drums, subgenre, duration_bars, bar_duration)
        self._generate_hiphop_bass(bass, subgenre, duration_bars, bar_duration)
        
        # Add melodic elements
        if specs.melodic_elements:
            self._generate_hiphop_melody(lead, subgenre, duration_bars, bar_duration)
            self._generate_hiphop_chords(piano, subgenre, duration_bars, bar_duration)
            
            # Add pads for atmospheric subgenres
            if specs.atmosphere in ["dreamy", "ethereal", "sophisticated"]:
                pad_program = 88 if specs.atmosphere == "dreamy" else 94  # String Ensemble or Halo Pad
                pads = pretty_midi.Instrument(program=pad_program, name="Pads")
                self._generate_hiphop_pads(pads, subgenre, duration_bars, bar_duration)
                midi.instruments.append(pads)
            
            midi.instruments.extend([lead, piano])
        
        midi.instruments.extend([drums, bass])
        
        # Apply intelligent voice assignment
        try:
            from voice_assignment import IntelligentVoiceAssigner
            assigner = IntelligentVoiceAssigner()
            enhanced_midi = assigner.assign_voices_to_track(midi, "hiphop", subgenre.value)
            return enhanced_midi
        except ImportError:
            print("⚠️ Voice assignment not available, using basic voices")
            return midi
    
    def _generate_hiphop_drums(self, drums: pretty_midi.Instrument, subgenre: HipHopSubgenre, 
                              duration_bars: int, bar_duration: float):
        """Generate drum patterns specific to Hip-Hop subgenre"""
        
        specs = self.subgenre_specs[subgenre]
        
        # Select appropriate pattern
        if subgenre in [HipHopSubgenre.BOOM_BAP, HipHopSubgenre.EAST_COAST]:
            pattern = self.drum_patterns["boom_bap"]
        elif subgenre in [HipHopSubgenre.TRAP, HipHopSubgenre.MUMBLE_RAP]:
            pattern = self.drum_patterns["trap_pattern"]
        elif subgenre in [HipHopSubgenre.DRILL, HipHopSubgenre.UK_DRILL]:
            pattern = self.drum_patterns["drill_pattern"]
        elif subgenre == HipHopSubgenre.OLD_SCHOOL:
            pattern = self.drum_patterns["old_school"]
        elif subgenre == HipHopSubgenre.CRUNK:
            pattern = self.drum_patterns["crunk_bounce"]
        elif subgenre in [HipHopSubgenre.WEST_COAST, HipHopSubgenre.GANGSTA_RAP]:
            pattern = self.drum_patterns["g_funk"]
        else:
            pattern = self.drum_patterns["boom_bap"]  # Default
        
        # Drum sounds
        kick_note = 36
        snare_note = 38
        hihat_closed = 42
        hihat_open = 46
        
        step_duration = bar_duration / 16  # 16th note steps
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            
            # Add swing if characteristic of subgenre
            swing_amount = specs.swing_factor * 0.05  # Convert to time offset
            
            for step, hit in enumerate(pattern):
                if hit:
                    step_time = bar_start + step * step_duration
                    
                    # Apply swing to off-beats
                    if step % 2 == 1 and swing_amount > 0:
                        step_time += swing_amount
                    
                    # Kick pattern
                    if step % 4 == 0:
                        velocity = random.randint(100, 127)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=kick_note,
                            start=step_time, end=step_time + step_duration * 0.8
                        ))
                    
                    # Snare pattern (genre-specific)
                    elif step in [4, 12] or (random.random() < specs.drum_complexity * 0.2):
                        velocity = random.randint(90, 120) if step in [4, 12] else random.randint(50, 80)
                        drums.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=snare_note,
                            start=step_time, end=step_time + step_duration * 0.6
                        ))
                    
                    # Hi-hat patterns (genre-specific complexity)
                    if subgenre in [HipHopSubgenre.TRAP, HipHopSubgenre.DRILL]:
                        # Complex hi-hat rolls for trap/drill
                        if random.random() < specs.drum_complexity:
                            for i in range(3):  # Triplet rolls
                                roll_time = step_time + i * (step_duration / 3)
                                velocity = random.randint(40, 80)
                                drums.notes.append(pretty_midi.Note(
                                    velocity=velocity, pitch=hihat_closed,
                                    start=roll_time, end=roll_time + step_duration * 0.2
                                ))
                    else:
                        # Standard hi-hat pattern
                        if random.random() < 0.7:
                            hat_note = hihat_open if step % 8 == 6 else hihat_closed
                            velocity = random.randint(30, 70)
                            drums.notes.append(pretty_midi.Note(
                                velocity=velocity, pitch=hat_note,
                                start=step_time, end=step_time + step_duration * 0.3
                            ))
    
    def _generate_hiphop_bass(self, bass: pretty_midi.Instrument, subgenre: HipHopSubgenre,
                             duration_bars: int, bar_duration: float):
        """Generate bass lines characteristic of each Hip-Hop subgenre"""
        
        specs = self.subgenre_specs[subgenre]
        
        # Bass note ranges for different subgenres
        if subgenre in [HipHopSubgenre.TRAP, HipHopSubgenre.DRILL]:
            bass_notes = [24, 26, 28]  # Lower 808s
        elif subgenre == HipHopSubgenre.JAZZ_RAP:
            bass_notes = [28, 31, 33, 35, 36]  # Walking bass range
        elif subgenre in [HipHopSubgenre.BOOM_BAP, HipHopSubgenre.EAST_COAST]:
            bass_notes = [26, 28, 31, 33]  # Classic range
        else:
            bass_notes = [24, 26, 28, 31]  # Standard range
        
        for bar in range(duration_bars):
            bar_start = bar * bar_duration
            
            if specs.bass_style == "808_heavy":
                # Modern trap/drill style with long 808s
                subdivisions = 4
                step_duration = bar_duration / subdivisions
                
                for step in range(subdivisions):
                    if step in [0, 2] or random.random() < 0.3:
                        step_time = bar_start + step * step_duration
                        note = random.choice(bass_notes)
                        velocity = random.randint(100, 127)
                        duration = step_duration * random.uniform(0.8, 1.5)
                        
                        bass.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=note,
                            start=step_time, end=step_time + duration
                        ))
            
            elif specs.bass_style == "sliding_808":
                # Drill style with sliding bass
                subdivisions = 8
                step_duration = bar_duration / subdivisions
                
                for step in range(subdivisions):
                    if random.random() < 0.4:
                        step_time = bar_start + step * step_duration
                        start_note = random.choice(bass_notes)
                        end_note = start_note + random.choice([-2, -1, 1, 2])
                        velocity = random.randint(90, 120)
                        
                        # Create sliding effect with pitch bend (simplified)
                        bass.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=start_note,
                            start=step_time, end=step_time + step_duration * 1.5
                        ))
            
            elif specs.bass_style == "walking":
                # Jazz rap walking bass
                subdivisions = 8
                step_duration = bar_duration / subdivisions
                current_note = bass_notes[0]
                
                for step in range(subdivisions):
                    step_time = bar_start + step * step_duration
                    
                    # Walking bass movement
                    if step > 0:
                        movement = random.choice([-2, -1, 1, 2])
                        current_note = max(min(current_note + movement, max(bass_notes)), min(bass_notes))
                    
                    velocity = random.randint(70, 100)
                    bass.notes.append(pretty_midi.Note(
                        velocity=velocity, pitch=current_note,
                        start=step_time, end=step_time + step_duration * 0.9
                    ))
            
            else:
                # Standard boom-bap style
                subdivisions = 4
                step_duration = bar_duration / subdivisions
                
                for step in range(subdivisions):
                    if step == 0 or random.random() < 0.6:
                        step_time = bar_start + step * step_duration
                        note = random.choice(bass_notes)
                        velocity = random.randint(80, 110)
                        duration = step_duration * random.uniform(0.6, 1.0)
                        
                        bass.notes.append(pretty_midi.Note(
                            velocity=velocity, pitch=note,
                            start=step_time, end=step_time + duration
                        ))

    def _generate_hiphop_melody(self, lead: pretty_midi.Instrument, subgenre: HipHopSubgenre,
                               duration_bars: int, bar_duration: float):
        """Generate melodic elements for melodic Hip-Hop subgenres"""
        
        specs = self.subgenre_specs[subgenre]
        
        # Scale selection based on subgenre
        if subgenre == HipHopSubgenre.JAZZ_RAP:
            scale = [60, 62, 64, 65, 67, 69, 71, 72]  # Major scale
        elif subgenre in [HipHopSubgenre.HORRORCORE, HipHopSubgenre.DRILL]:
            scale = [60, 62, 63, 65, 67, 68, 70, 72]  # Minor scale
        elif subgenre == HipHopSubgenre.TRAP:
            scale = [60, 63, 65, 67, 70, 72, 75]  # Minor pentatonic + blue notes
        else:
            scale = [60, 62, 63, 65, 67, 68, 70, 72]  # Natural minor
        
        melody_density = 0.3 if specs.atmosphere == "minimal" else 0.5
        
        for bar in range(0, duration_bars, 4):  # 4-bar phrases
            bar_start = bar * bar_duration
            phrase_length = bar_duration * 4
            
            num_notes = int(phrase_length / (bar_duration / 8) * melody_density)
            
            for i in range(num_notes):
                note_time = bar_start + random.uniform(0, phrase_length)
                note_duration = random.uniform(0.2, 1.0)
                note_pitch = random.choice(scale) + random.choice([0, 12])
                velocity = random.randint(60, 90)
                
                lead.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_pitch,
                    start=note_time, end=note_time + note_duration
                ))

    def _generate_hiphop_chords(self, piano: pretty_midi.Instrument, subgenre: HipHopSubgenre,
                               duration_bars: int, bar_duration: float):
        """Generate chord progressions for Hip-Hop"""
        
        # Common hip-hop chord progressions
        if subgenre == HipHopSubgenre.JAZZ_RAP:
            progressions = [
                [[48, 52, 55, 59], [53, 57, 60, 64], [50, 54, 57, 61], [45, 49, 52, 56]],  # Jazz progression
                [[48, 52, 55], [46, 50, 53], [44, 48, 51], [43, 47, 50]]  # Simpler jazz
            ]
        elif subgenre in [HipHopSubgenre.BOOM_BAP, HipHopSubgenre.CONSCIOUS_RAP]:
            progressions = [
                [[48, 51, 55], [46, 49, 53], [44, 47, 51], [42, 45, 49]],  # Minor progression
                [[48, 52, 55], [45, 48, 52], [43, 47, 50], [41, 44, 48]]   # Soul progression
            ]
        else:
            progressions = [
                [[48, 51, 55], [46, 49, 53], [44, 47, 51], [49, 52, 56]],  # Standard minor
                [[48, 52, 55], [50, 53, 57], [47, 51, 54], [45, 48, 52]]   # Mixed
            ]
        
        progression = random.choice(progressions)
        chord_duration = bar_duration * 2  # 2-bar chords
        
        for bar in range(0, duration_bars, 2):
            bar_start = bar * bar_duration
            chord_index = (bar // 2) % len(progression)
            chord = progression[chord_index]
            
            for note_pitch in chord:
                velocity = random.randint(40, 70)
                piano.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_pitch,
                    start=bar_start, end=bar_start + chord_duration
                ))

    def _generate_hiphop_pads(self, pads: pretty_midi.Instrument, subgenre: HipHopSubgenre,
                             duration_bars: int, bar_duration: float):
        """Generate atmospheric pad sounds"""
        
        # Simple sustained pads for atmosphere
        pad_notes = [48, 51, 55, 58]  # Basic minor chord
        pad_duration = bar_duration * 8  # Long sustained notes
        
        for bar in range(0, duration_bars, 8):
            bar_start = bar * bar_duration
            
            for note_pitch in pad_notes:
                velocity = random.randint(30, 50)
                pads.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_pitch,
                    start=bar_start, end=bar_start + pad_duration
                ))

    def generate_training_dataset(self, output_dir: str = "midi_files", 
                                 tracks_per_subgenre: int = 5):
        """Generate a complete training dataset with all Hip-Hop subgenres"""
        
        os.makedirs(output_dir, exist_ok=True)
        generated_files = []
        
        print("🎤 Generating Hip-Hop training dataset...")
        
        for subgenre in HipHopSubgenre:
            print(f"🎵 Generating {tracks_per_subgenre} tracks for {subgenre.value}...")
            
            for track_num in range(tracks_per_subgenre):
                # Vary track length
                duration_bars = random.randint(16, 64)
                
                # Generate track
                midi_track = self.generate_hiphop_track(subgenre, duration_bars)
                
                # Save file
                filename = f"hiphop_{subgenre.value}_{track_num + 1:02d}.mid"
                filepath = os.path.join(output_dir, filename)
                midi_track.write(filepath)
                
                generated_files.append(filepath)
                print(f"   ✅ Generated: {filename}")
        
        print(f"\n🎉 Hip-Hop dataset generation complete!")
        print(f"📊 Generated {len(generated_files)} tracks across {len(HipHopSubgenre)} subgenres")
        print(f"📁 Files saved to: {output_dir}")
        
        # Generate summary
        self._generate_dataset_summary(output_dir, generated_files)
        
        return generated_files

    def _generate_dataset_summary(self, output_dir: str, generated_files: List[str]):
        """Generate a summary of the Hip-Hop dataset"""
        
        summary_path = os.path.join(output_dir, "hiphop_dataset_info.txt")
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("Hip-Hop Training Dataset Summary\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total tracks generated: {len(generated_files)}\n")
            f.write(f"Number of subgenres: {len(HipHopSubgenre)}\n\n")
            
            f.write("Subgenres included:\n")
            for subgenre in HipHopSubgenre:
                specs = self.subgenre_specs[subgenre]
                f.write(f"  - {subgenre.value.upper().replace('_', ' ')}\n")
                f.write(f"    BPM Range: {specs.bpm_range[0]}-{specs.bpm_range[1]}\n")
                f.write(f"    Atmosphere: {specs.atmosphere}\n")
                f.write(f"    Bass Style: {specs.bass_style}\n\n")
            
            f.write("Training Tips:\n")
            f.write("- Use all files for diverse Hip-Hop generation\n")
            f.write("- Train for 30-50 epochs for best results\n")
            f.write("- Experiment with temperature 0.6-0.9 for Hip-Hop generation\n")
            f.write("- Different subgenres have distinct rhythmic patterns\n\n")
            
            f.write("File List:\n")
            for i, file_path in enumerate(generated_files, 1):
                filename = os.path.basename(file_path)
                f.write(f"{i:3d}. {filename}\n")
        
        print(f"📋 Dataset summary saved to: {summary_path}")

def main():
    """Generate the complete Hip-Hop training dataset"""
    generator = HipHopMIDIGenerator()
    
    # Generate comprehensive dataset
    files = generator.generate_training_dataset(
        output_dir="midi_files",
        tracks_per_subgenre=6  # 6 tracks per subgenre = 120 total tracks
    )
    
    print(f"\n🚀 Ready to train your AI with {len(files)} Hip-Hop tracks!")
    print("Run: python run.py to start training")

if __name__ == "__main__":
    main()
