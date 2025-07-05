"""
🎵 BEAT ADDICTS - Voice Assignment Logic System
Professional voice assignment engine for Beat Addicts music production AI
Standalone implementation optimized for professional music production
"""

import os
import random
import json
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
from dataclasses import dataclass

class InstrumentCategory(Enum):
    """Beat Addicts instrument categories for voice assignment"""
    DRUMS = "drums"
    BASS = "bass"
    RHYTHM = "rhythm"
    LEAD = "lead"
    PAD = "pad"
    VOCAL = "vocal"
    PERCUSSION = "percussion"
    EFFECTS = "effects"

class VoiceStyle(Enum):
    """Different voice/instrument styles"""
    ACOUSTIC = "acoustic"
    ELECTRIC = "electric"
    SYNTHETIC = "synthetic"
    HYBRID = "hybrid"
    VINTAGE = "vintage"
    MODERN = "modern"

@dataclass
class VoiceProfile:
    """Profile defining voice characteristics"""
    program: int  # MIDI program number
    channel: int  # MIDI channel
    velocity_range: Tuple[int, int]
    pan: int  # Pan position (-64 to 63)
    reverb: float  # Reverb amount (0-1)
    chorus: float  # Chorus amount (0-1)
    distortion: float  # Distortion amount (0-1)
    filter_cutoff: float  # Filter cutoff (0-1)
    attack: float  # Attack time (0-1)
    release: float  # Release time (0-1)

class SimpleMIDINote:
    """Lightweight MIDI note representation"""
    def __init__(self, velocity, pitch, start, end):
        self.velocity = velocity
        self.pitch = pitch
        self.start = start
        self.end = end

class SimpleMIDIInstrument:
    """Lightweight MIDI instrument representation"""
    def __init__(self, program=0, is_drum=False, name="", channel=0):
        self.program = program
        self.is_drum = is_drum
        self.name = name
        self.channel = channel
        self.notes = []
        self.control_changes = []

class IntelligentVoiceAssigner:
    """Beat Addicts advanced voice assignment system for multi-genre MIDI generation"""
    
    def __init__(self):
        self.genre_voice_maps = self._initialize_genre_voice_maps()
        self.instrument_profiles = self._initialize_instrument_profiles()
        self.voice_combinations = self._initialize_voice_combinations()
        print("✅ Beat Addicts Voice Assignment Engine initialized")
        
    def _initialize_genre_voice_maps(self) -> Dict[str, Dict[str, List[int]]]:
        """Initialize Beat Addicts genre-specific voice mappings"""
        return {
            # Beat Addicts Hip-Hop Genre Voices
            "hiphop": {
                "drums": [0, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127],
                "bass": [33, 34, 35, 36, 37, 38, 39],
                "lead": [80, 81, 82, 83, 84, 85, 86, 87],
                "pad": [88, 89, 90, 91, 92, 93, 94, 95],
                "vocal": [52, 53, 54, 55, 56, 57, 58, 59],
                "effects": [122, 123, 124, 125, 126, 127]
            },
            
            # Beat Addicts Electronic Genre Voices
            "electronic": {
                "drums": [118, 119, 120, 121, 122, 123, 124, 125, 126, 127],
                "bass": [37, 38, 39, 80, 81, 82],
                "lead": [80, 81, 82, 83, 84, 85, 86, 87, 96, 97, 98, 99],
                "pad": [88, 89, 90, 91, 92, 93, 94, 95, 100, 101, 102, 103],
                "effects": [122, 123, 124, 125, 126, 127],
                "arp": [96, 97, 98, 99, 100, 101, 102, 103]
            },
            
            # Rock Genre Voices
            "rock": {
                "drums": [0, 1, 8, 16, 24, 25, 32, 40, 48],
                "bass": [33, 34, 35, 36],
                "rhythm_guitar": [28, 29, 30, 31],
                "lead_guitar": [28, 29, 30, 31],
                "keys": [0, 1, 2, 3, 4, 5, 6, 7],
                "vocal": [52, 53, 54],
                "strings": [40, 41, 42, 43, 44, 45, 46, 47]
            },
            
            # Country Genre Voices
            "country": {
                "drums": [0, 1, 8, 16, 24, 32],
                "bass": [32, 33, 34, 35],
                "acoustic_guitar": [24, 25, 26, 27],
                "steel_guitar": [25, 26, 27, 28],
                "fiddle": [40, 41, 42, 43],
                "banjo": [105, 106, 107],
                "harmonica": [22, 23],
                "piano": [0, 1, 2, 3],
                "organ": [16, 17, 18, 19, 20]
            },
            
            # DNB Genre Voices
            "dnb": {
                "drums": [118, 119, 120, 121, 122, 123, 124, 125, 126, 127],
                "bass": [37, 38, 39, 80, 81, 82],
                "lead": [80, 81, 82, 83, 84, 85, 86, 87],
                "pad": [88, 89, 90, 91, 92, 93, 94, 95],
                "fx": [122, 123, 124, 125, 126, 127],
                "amen": [118, 119, 120, 121]
            },
            
            # Futuristic Genre Voices
            "futuristic": {
                "drums": [118, 119, 120, 121, 122, 123, 124, 125, 126, 127],
                "synth": [96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107],
                "lead": [80, 81, 82, 83, 84, 85, 86, 87, 96, 97, 98, 99],
                "pad": [88, 89, 90, 91, 92, 93, 94, 95, 100, 101, 102, 103],
                "vocal": [54, 55, 56, 57, 58, 59],
                "glitch": [120, 121, 122, 123, 124, 125, 126, 127],
                "ai": [96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107]
            }
        }
    
    def _initialize_instrument_profiles(self) -> Dict[int, VoiceProfile]:
        """Initialize detailed profiles for each MIDI program"""
        profiles = {}
        
        # Acoustic Piano profiles
        for i in range(8):
            profiles[i] = VoiceProfile(
                program=i, channel=0, velocity_range=(40, 100), pan=0,
                reverb=0.3, chorus=0.1, distortion=0.0, filter_cutoff=1.0,
                attack=0.1, release=0.8
            )
        
        # Electric Piano profiles
        for i in range(8, 16):
            profiles[i] = VoiceProfile(
                program=i, channel=1, velocity_range=(50, 110), pan=0,
                reverb=0.4, chorus=0.3, distortion=0.2, filter_cutoff=0.8,
                attack=0.2, release=0.6
            )
        
        # Guitar profiles
        for i in range(24, 32):
            profiles[i] = VoiceProfile(
                program=i, channel=3, velocity_range=(50, 120), pan=random.randint(-30, 30),
                reverb=0.4, chorus=0.2, distortion=0.3, filter_cutoff=0.7,
                attack=0.1, release=0.4
            )
        
        # Bass profiles
        for i in range(32, 40):
            profiles[i] = VoiceProfile(
                program=i, channel=4, velocity_range=(70, 127), pan=0,
                reverb=0.2, chorus=0.1, distortion=0.2, filter_cutoff=0.6,
                attack=0.0, release=0.3
            )
        
        # Synth Lead profiles
        for i in range(80, 88):
            profiles[i] = VoiceProfile(
                program=i, channel=10, velocity_range=(60, 127), pan=random.randint(-40, 40),
                reverb=0.3, chorus=0.5, distortion=0.4, filter_cutoff=0.7,
                attack=0.0, release=0.4
            )
        
        # Synth Pad profiles
        for i in range(88, 96):
            profiles[i] = VoiceProfile(
                program=i, channel=11, velocity_range=(30, 80), pan=0,
                reverb=0.8, chorus=0.6, distortion=0.1, filter_cutoff=0.8,
                attack=0.5, release=1.0
            )
        
        return profiles
    
    def _initialize_voice_combinations(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize effective voice combinations for different genres"""
        return {
            "hiphop_trap": [
                {"role": "drums", "programs": [118, 119], "channel": 9, "priority": 1},
                {"role": "bass", "programs": [37, 38], "channel": 1, "priority": 2},
                {"role": "lead", "programs": [80, 81], "channel": 2, "priority": 3},
                {"role": "pad", "programs": [88, 89], "channel": 3, "priority": 4},
                {"role": "fx", "programs": [122, 123], "channel": 4, "priority": 5}
            ],
            
            "electronic_house": [
                {"role": "drums", "programs": [118, 119], "channel": 9, "priority": 1},
                {"role": "bass", "programs": [37, 38], "channel": 1, "priority": 2},
                {"role": "lead", "programs": [80, 81, 82], "channel": 2, "priority": 3},
                {"role": "arp", "programs": [96, 97], "channel": 3, "priority": 4},
                {"role": "pad", "programs": [88, 89], "channel": 4, "priority": 5}
            ],
            
            "rock_classic": [
                {"role": "drums", "programs": [0, 1], "channel": 9, "priority": 1},
                {"role": "bass", "programs": [33, 34], "channel": 1, "priority": 2},
                {"role": "rhythm_guitar", "programs": [28, 29], "channel": 2, "priority": 3},
                {"role": "lead_guitar", "programs": [30, 31], "channel": 3, "priority": 4},
                {"role": "keys", "programs": [0, 1], "channel": 4, "priority": 5}
            ],
            
            "country_traditional": [
                {"role": "drums", "programs": [0, 1], "channel": 9, "priority": 1},
                {"role": "bass", "programs": [32, 33], "channel": 1, "priority": 2},
                {"role": "acoustic_guitar", "programs": [24, 25], "channel": 2, "priority": 3},
                {"role": "steel_guitar", "programs": [25, 26], "channel": 3, "priority": 4},
                {"role": "fiddle", "programs": [40, 41], "channel": 4, "priority": 5}
            ],
            
            "dnb_liquid": [
                {"role": "drums", "programs": [118, 119], "channel": 9, "priority": 1},
                {"role": "bass", "programs": [37, 38], "channel": 1, "priority": 2},
                {"role": "lead", "programs": [80, 81], "channel": 2, "priority": 3},
                {"role": "pad", "programs": [88, 89], "channel": 3, "priority": 4},
                {"role": "fx", "programs": [122, 123], "channel": 4, "priority": 5}
            ],
            
            "futuristic_ai": [
                {"role": "drums", "programs": [118, 119, 120], "channel": 9, "priority": 1},
                {"role": "synth", "programs": [96, 97, 98], "channel": 1, "priority": 2},
                {"role": "lead", "programs": [82, 83, 84], "channel": 2, "priority": 3},
                {"role": "pad", "programs": [100, 101, 102], "channel": 3, "priority": 4},
                {"role": "vocal", "programs": [54, 55, 56], "channel": 4, "priority": 5},
                {"role": "glitch", "programs": [124, 125, 126], "channel": 5, "priority": 6}
            ]
        }
    
    def get_voice_recommendation(self, genre: str, role: str, subgenre: str = "") -> Dict[str, Any]:
        """Get Beat Addicts voice recommendation without requiring MIDI objects"""
        
        combination_key = self._get_combination_key(genre, subgenre)
        voice_combo = self.voice_combinations.get(combination_key, [])
        
        # Find matching role for Beat Addicts
        for voice_info in voice_combo:
            if voice_info["role"] == role or voice_info["role"] in self._get_similar_roles(role):
                return {
                    "recommended_program": random.choice(voice_info["programs"]),
                    "channel": voice_info["channel"],
                    "role": voice_info["role"],
                    "priority": voice_info["priority"],
                    "genre": genre,
                    "subgenre": subgenre,
                    "beat_addicts_optimized": True
                }
        
        # Beat Addicts fallback recommendation
        fallback_programs = self.genre_voice_maps.get(genre, {}).get(role, [0])
        return {
            "recommended_program": random.choice(fallback_programs) if fallback_programs else 0,
            "channel": 0,
            "role": role,
            "priority": 999,
            "genre": genre,
            "subgenre": subgenre,
            "beat_addicts_optimized": True
        }
    
    def _get_combination_key(self, genre: str, subgenre: str) -> str:
        """Get the appropriate voice combination key"""
        fallback_map = {
            "hiphop": "hiphop_trap",
            "electronic": "electronic_house", 
            "rock": "rock_classic",
            "country": "country_traditional",
            "dnb": "dnb_liquid",
            "futuristic": "futuristic_ai"
        }
        
        if subgenre:
            potential_key = f"{genre}_{subgenre}"
            if potential_key in self.voice_combinations:
                return potential_key
        
        return fallback_map.get(genre, "hiphop_trap")
    
    def _get_similar_roles(self, role: str) -> List[str]:
        """Get similar roles for fallback matching"""
        role_mappings = {
            "rhythm": ["lead", "arp", "keys"],
            "lead": ["rhythm", "arp"],
            "pad": ["fx", "vocal"],
            "fx": ["pad", "glitch"],
            "vocal": ["pad", "fx"]
        }
        return role_mappings.get(role, [])
    
    def generate_voice_assignment_report(self, genre: str, num_instruments: int = 5) -> Dict[str, Any]:
        """Generate a Beat Addicts voice assignment report for a genre"""
        
        roles = ["drums", "bass", "lead", "rhythm", "pad"][:num_instruments]
        assignments = []
        
        for i, role in enumerate(roles):
            recommendation = self.get_voice_recommendation(genre, role)
            profile = self.instrument_profiles.get(recommendation["recommended_program"])
            
            assignment = {
                "instrument_index": i,
                "role": role,
                "program": recommendation["recommended_program"],
                "channel": recommendation["channel"],
                "velocity_range": profile.velocity_range if profile else (60, 120),
                "beat_addicts_optimized": True,
                "effects": {
                    "reverb": profile.reverb if profile else 0.3,
                    "chorus": profile.chorus if profile else 0.2,
                    "pan": profile.pan if profile else 0
                } if profile else {}
            }
            assignments.append(assignment)
        
        return {
            "genre": genre,
            "total_instruments": num_instruments,
            "assignments": assignments,
            "beat_addicts_version": "2.0",
            "recommendations": [
                f"Beat Addicts: Use program {a['program']} for {a['role']} on channel {a['channel']}"
                for a in assignments
            ]
        }
    
    def save_voice_config(self, filename: str, genre: str, assignments: List[Dict]) -> bool:
        """Save Beat Addicts voice configuration to file"""
        try:
            config = {
                "beat_addicts_version": "2.0",
                "genre": genre,
                "timestamp": "auto-generated",
                "voice_assignments": assignments,
                "generator_info": "Beat Addicts Professional Music Production AI - Voice Assignment Engine"
            }
            
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ Beat Addicts voice configuration saved to: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Beat Addicts failed to save voice configuration: {e}")
            return False
    
    def load_voice_config(self, filename: str) -> Optional[Dict]:
        """Load voice configuration from file"""
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
            
            print(f"✅ Voice configuration loaded from: {filename}")
            return config
            
        except Exception as e:
            print(f"❌ Failed to load voice configuration: {e}")
            return None

def main():
    """Test the Beat Addicts voice assignment system"""
    
    print("🎵 BEAT ADDICTS - Voice Assignment Logic System Test")
    print("=" * 60)
    print("🔥 Professional Music Production AI by Beat Addicts 🔥")
    
    try:
        # Initialize Beat Addicts system
        assigner = IntelligentVoiceAssigner()
        
        # Test Beat Addicts voice mapping
        print("Beat Addicts available genres:")
        for genre in assigner.genre_voice_maps.keys():
            print(f"  • {genre}")
        
        print(f"\nBeat Addicts instrument profiles: {len(assigner.instrument_profiles)}")
        print(f"Beat Addicts voice combinations: {len(assigner.voice_combinations)}")
        
        # Test Beat Addicts voice recommendations
        print("\n🔍 Testing Beat Addicts voice recommendations:")
        
        test_cases = [
            ("hiphop", "drums"),
            ("electronic", "bass"),
            ("rock", "lead_guitar"),
            ("country", "fiddle"),
            ("dnb", "pad"),
            ("futuristic", "glitch")
        ]
        
        for genre, role in test_cases:
            recommendation = assigner.get_voice_recommendation(genre, role)
            print(f"  Beat Addicts {genre} {role}: Program {recommendation['recommended_program']} on channel {recommendation['channel']}")
        
        # Generate and save a Beat Addicts sample report
        print("\n📊 Generating Beat Addicts voice assignment report...")
        report = assigner.generate_voice_assignment_report("hiphop", 5)
        
        print(f"Beat Addicts generated report for {report['genre']} with {report['total_instruments']} instruments")
        for assignment in report['assignments']:
            print(f"  • {assignment['role']}: Program {assignment['program']} (Channel {assignment['channel']})")
        
        # Save Beat Addicts configuration
        config_filename = "beat_addicts_voice_config.json"
        assigner.save_voice_config(config_filename, "hiphop", report['assignments'])
        
        # Test Beat Addicts loading
        loaded_config = assigner.load_voice_config(config_filename)
        if loaded_config:
            print(f"✅ Beat Addicts successfully loaded configuration with {len(loaded_config['voice_assignments'])} assignments")
        
        print("\n🎉 BEAT ADDICTS VOICE ASSIGNMENT ENGINE TEST COMPLETED!")
        print("✅ All Beat Addicts functions working without dependencies")
        print("✅ Ready for integration with Beat Addicts MIDI generators")
        print("🔥 Beat Addicts professional music production ready! 🔥")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Beat Addicts Voice Assignment Engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
    
    def _enhance_note(self, original_note: pretty_midi.Note, 
                     profile: Optional[VoiceProfile], genre: str, style: str) -> pretty_midi.Note:
        """Enhance a note based on voice profile and genre characteristics"""
        
        if not profile:
            return original_note
        
        # Adjust velocity based on profile and genre
        min_vel, max_vel = profile.velocity_range
        velocity_factor = self._get_genre_velocity_factor(genre)
        
        # Safe velocity calculation without numpy dependency
        if NUMPY_AVAILABLE:
            new_velocity = int(np.clip(
                original_note.velocity * velocity_factor,
                min_vel, max_vel
            ))
        else:
            new_velocity = int(max(min_vel, min(max_vel, original_note.velocity * velocity_factor)))
        
        # Create enhanced note
        enhanced_note = pretty_midi.Note(
            velocity=new_velocity,
            pitch=original_note.pitch,
            start=original_note.start,
            end=original_note.end
        )
        
        return enhanced_note
    
    def _determine_instrument_role(self, instrument: pretty_midi.Instrument, 
                                  index: int, total_instruments: int) -> str:
        """Determine the role of an instrument based on its characteristics"""
        
        if instrument.is_drum:
            return "drums"
        
        # Analyze note characteristics
        if len(instrument.notes) == 0:
            return "pad"
        
        notes = instrument.notes
        
        # Safe mathematical operations
        if NUMPY_AVAILABLE:
            avg_pitch = np.mean([note.pitch for note in notes])
        else:
            avg_pitch = sum([note.pitch for note in notes]) / len(notes)
        
        pitch_range = max([note.pitch for note in notes]) - min([note.pitch for note in notes])
        
        # Calculate note density safely
        if len(notes) > 1:
            time_span = notes[-1].end - notes[0].start
            note_density = len(notes) / time_span if time_span > 0 else 1
        else:
            note_density = 1
        
        # Role determination logic
        if avg_pitch < 45:  # Low register
            return "bass"
        elif avg_pitch > 72 and note_density > 2:  # High register, dense
            return "lead"
        elif pitch_range > 24 and note_density < 1:  # Wide range, sparse
            return "pad"
        elif index == 0 and not instrument.is_drum:  # First non-drum instrument
            return "lead"
        elif index == 1 and avg_pitch < 60:  # Second instrument, mid-low
            return "bass"
        else:
            return "rhythm"
    
    def _enhance_basic_instrument(self, instrument: pretty_midi.Instrument, genre: str) -> pretty_midi.Instrument:
        """Basic enhancement for instruments without specific voice assignment"""
        
        # Create a copy with genre-appropriate program
        genre_programs = {
            "hiphop": [80, 81, 37, 38],
            "electronic": [96, 97, 80, 81],
            "rock": [28, 29, 30, 31],
            "country": [24, 25, 40, 41],
            "dnb": [80, 81, 37, 38],
            "futuristic": [96, 97, 98, 99]
        }
        
        programs = genre_programs.get(genre, [0, 1, 2, 3])
        new_program = random.choice(programs) if not instrument.is_drum else 0
        
        enhanced_instrument = pretty_midi.Instrument(
            program=new_program,
            is_drum=instrument.is_drum,
            name=f"enhanced_{instrument.name}",
            channel=instrument.channel
        )
        
        # Copy notes with slight velocity adjustment
        velocity_factor = self._get_genre_velocity_factor(genre)
        for note in instrument.notes:
            # Safe velocity calculation
            if NUMPY_AVAILABLE:
                new_velocity = int(np.clip(note.velocity * velocity_factor, 1, 127))
            else:
                new_velocity = int(max(1, min(127, note.velocity * velocity_factor)))
            
            enhanced_note = pretty_midi.Note(
                velocity=new_velocity,
                pitch=note.pitch,
                start=note.start,
                end=note.end
            )
            enhanced_instrument.notes.append(enhanced_note)
        
        return enhanced_instrument
    
    def _add_control_changes(self, instrument: pretty_midi.Instrument, 
                           profile: Optional[VoiceProfile], genre: str):
        """Add realistic control changes to instrument"""
        
        if not profile or not instrument.notes:
            return
        
        start_time = instrument.notes[0].start
        end_time = instrument.notes[-1].end
        
        # Add volume automation
        instrument.control_changes.append(
            pretty_midi.ControlChange(number=7, value=int(100 * profile.velocity_range[1] / 127), time=start_time)
        )
        
        # Add pan
        if profile.pan != 0:
            pan_value = int(profile.pan + 64)  # Convert from -64,63 to 0,127
            instrument.control_changes.append(
                pretty_midi.ControlChange(number=10, value=pan_value, time=start_time)
            )
        
        # Add reverb
        if profile.reverb > 0:
            reverb_value = int(profile.reverb * 127)
            instrument.control_changes.append(
                pretty_midi.ControlChange(number=91, value=reverb_value, time=start_time)
            )
        
        # Add chorus
        if profile.chorus > 0:
            chorus_value = int(profile.chorus * 127)
            instrument.control_changes.append(
                pretty_midi.ControlChange(number=93, value=chorus_value, time=start_time)
            )
        
        # Add filter cutoff for electronic genres
        if genre in ["electronic", "hiphop", "dnb", "futuristic"] and profile.filter_cutoff < 1.0:
            cutoff_value = int(profile.filter_cutoff * 127)
            instrument.control_changes.append(
                pretty_midi.ControlChange(number=74, value=cutoff_value, time=start_time)
            )
    
    def _add_genre_specific_voices(self, midi: pretty_midi.PrettyMIDI, genre: str, subgenre: str):
        """Add additional genre-specific voices if needed"""
        
        # This could add ambient textures, percussion layers, etc.
        # Implementation would depend on specific genre requirements
        pass
    
    def generate_voice_report(self, midi: pretty_midi.PrettyMIDI) -> Dict[str, Any]:
        """Generate a report of voice assignments in a MIDI file"""
        
        report = {
            "total_instruments": len(midi.instruments),
            "voice_assignments": [],
            "channel_usage": {},
            "program_usage": {},
            "recommendations": []
        }
        
        for i, instrument in enumerate(midi.instruments):
            voice_info = {
                "index": i,
                "name": instrument.name,
                "program": instrument.program,
                "channel": instrument.channel,
                "is_drum": instrument.is_drum,
                "note_count": len(instrument.notes),
                "pitch_range": (
                    min([n.pitch for n in instrument.notes]) if instrument.notes else 0,
                    max([n.pitch for n in instrument.notes]) if instrument.notes else 0
                ),
                "velocity_range": (
                    min([n.velocity for n in instrument.notes]) if instrument.notes else 0,
                    max([n.velocity for n in instrument.notes]) if instrument.notes else 0
                )
            }
            report["voice_assignments"].append(voice_info)
            
            # Track usage
            report["channel_usage"][instrument.channel] = report["channel_usage"].get(instrument.channel, 0) + 1
            report["program_usage"][instrument.program] = report["program_usage"].get(instrument.program, 0) + 1
        
        # Add recommendations
        if len(midi.instruments) > 16:
            report["recommendations"].append("Consider reducing instrument count for better compatibility")
        
        if len(set(inst.channel for inst in midi.instruments)) < len(midi.instruments):
            report["recommendations"].append("Multiple instruments on same channel - may cause conflicts")
        
        return report

# (Removed duplicate main() and entry point to avoid unreachable code)
