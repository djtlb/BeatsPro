#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Simple MIDI Generator
Lightweight MIDI generation without external dependencies
"""

import struct
import os
from typing import List, Tuple, Dict, Any, Optional

class SimpleMIDINote:
    """Simple MIDI note representation"""
    def __init__(self, pitch: int, velocity: int, start_time: float, duration: float, channel: int = 0):
        self.pitch = pitch
        self.velocity = velocity
        self.start_time = start_time
        self.duration = duration
        self.channel = channel

class SimpleMIDIWriter:
    """Simple MIDI file writer without external dependencies"""
    
    def __init__(self, ticks_per_beat: int = 480):
        self.ticks_per_beat = ticks_per_beat
        self.tracks = []
        
    def create_track(self) -> List:
        """Create a new MIDI track"""
        track = []
        self.tracks.append(track)
        return track
    
    def add_note(self, track: List, note: SimpleMIDINote):
        """Add a note to a track"""
        start_tick = int(note.start_time * self.ticks_per_beat)
        end_tick = int((note.start_time + note.duration) * self.ticks_per_beat)
        
        # Note on event
        track.append({
            'type': 'note_on',
            'tick': start_tick,
            'channel': note.channel,
            'note': note.pitch,
            'velocity': note.velocity
        })
        
        # Note off event
        track.append({
            'type': 'note_off', 
            'tick': end_tick,
            'channel': note.channel,
            'note': note.pitch,
            'velocity': 0
        })
    
    def write_file(self, filename: str, tempo: int = 120):
        """Write MIDI file"""
        try:
            with open(filename, 'wb') as f:
                # Write MIDI header
                f.write(b'MThd')  # Header chunk type
                f.write(struct.pack('>I', 6))  # Header length
                f.write(struct.pack('>H', 1))  # Format type 1
                f.write(struct.pack('>H', len(self.tracks)))  # Number of tracks
                f.write(struct.pack('>H', self.ticks_per_beat))  # Ticks per beat
                
                # Write each track
                for track_data in self.tracks:
                    self._write_track(f, track_data, tempo)
            
            return True
        except Exception as e:
            print(f"❌ Error writing MIDI file: {e}")
            return False
    
    def _write_track(self, f, track_data: List, tempo: int):
        """Write a single track"""
        track_bytes = bytearray()
        
        # Add tempo event at beginning
        tempo_microseconds = int(60000000 / tempo)
        track_bytes.extend(self._write_event(0, 0xFF, 0x51, struct.pack('>I', tempo_microseconds)[1:]))
        
        # Sort events by tick
        track_data.sort(key=lambda x: x['tick'])
        
        current_tick = 0
        for event in track_data:
            delta_time = event['tick'] - current_tick
            current_tick = event['tick']
            
            if event['type'] == 'note_on':
                status = 0x90 | event['channel']
                data = bytes([event['note'], event['velocity']])
                track_bytes.extend(self._write_event(delta_time, status, data=data))
            elif event['type'] == 'note_off':
                status = 0x80 | event['channel']
                data = bytes([event['note'], event['velocity']])
                track_bytes.extend(self._write_event(delta_time, status, data=data))
        
        # End of track
        track_bytes.extend(self._write_event(0, 0xFF, 0x2F, b''))
        
        # Write track header
        f.write(b'MTrk')
        f.write(struct.pack('>I', len(track_bytes)))
        f.write(track_bytes)
    
    def _write_event(self, delta_time: int, status: int, data_type: Optional[int] = None, data: bytes = b''):
        """Write a MIDI event"""
        event_bytes = bytearray()
        
        # Write variable-length delta time
        event_bytes.extend(self._write_varlen(delta_time))
        
        # Write status byte
        event_bytes.append(status)
        
        # Write data
        if data_type is not None:
            event_bytes.append(data_type)
            event_bytes.extend(self._write_varlen(len(data)))
        
        event_bytes.extend(data)
        
        return event_bytes
    
    def _write_varlen(self, value: int) -> bytes:
        """Write variable-length quantity"""
        if value == 0:
            return bytes([0])
        
        result = []
        while value > 0:
            result.insert(0, value & 0x7F)
            value >>= 7
        
        # Set continuation bit on all but last byte
        for i in range(len(result) - 1):
            result[i] |= 0x80
        
        return bytes(result)

class BeatAddictsSimpleMIDIGenerator:
    """Simple MIDI generator for BEAT ADDICTS without external dependencies"""
    
    def __init__(self):
        self.genre_patterns = {
            'dnb': {
                'bpm': 174,
                'kick_pattern': [0, 2],
                'snare_pattern': [1, 3],
                'bass_notes': [36, 38, 41, 43]
            },
            'hiphop': {
                'bpm': 90,
                'kick_pattern': [0, 2.5],
                'snare_pattern': [1, 3],
                'bass_notes': [36, 40, 43, 48]
            },
            'electronic': {
                'bpm': 128,
                'kick_pattern': [0, 1, 2, 3],
                'snare_pattern': [1, 3],
                'bass_notes': [36, 40, 43, 48, 52]
            },
            'rock': {
                'bpm': 120,
                'kick_pattern': [0, 2],
                'snare_pattern': [1, 3],
                'bass_notes': [28, 31, 36, 40]
            }
        }
    
    def generate_beat(self, genre: str, bars: int = 4, output_file: Optional[str] = None) -> Optional[str]:
        """Generate a simple beat for the specified genre"""
        if genre.lower() not in self.genre_patterns:
            genre = 'electronic'  # Default fallback
        
        pattern = self.genre_patterns[genre.lower()]
        
        midi_writer = SimpleMIDIWriter()
        drum_track = midi_writer.create_track()
        bass_track = midi_writer.create_track()
        
        beat_duration = 4.0  # 4 beats per bar
        
        # Generate drum pattern
        for bar in range(bars):
            bar_start = bar * beat_duration
            
            # Kick drum
            for kick_beat in pattern['kick_pattern']:
                if kick_beat < 4:  # Ensure we don't go beyond bar
                    note = SimpleMIDINote(
                        pitch=36,  # Kick drum
                        velocity=100,
                        start_time=bar_start + kick_beat,
                        duration=0.1,
                        channel=9  # Drum channel
                    )
                    midi_writer.add_note(drum_track, note)
            
            # Snare drum
            for snare_beat in pattern['snare_pattern']:
                if snare_beat < 4:
                    note = SimpleMIDINote(
                        pitch=38,  # Snare drum
                        velocity=90,
                        start_time=bar_start + snare_beat,
                        duration=0.1,
                        channel=9  # Drum channel
                    )
                    midi_writer.add_note(drum_track, note)
            
            # Hi-hats (every half beat for electronic)
            if genre.lower() == 'electronic':
                for beat in range(8):  # 8 eighth notes per bar
                    note = SimpleMIDINote(
                        pitch=42,  # Closed hi-hat
                        velocity=60,
                        start_time=bar_start + (beat * 0.5),
                        duration=0.1,
                        channel=9
                    )
                    midi_writer.add_note(drum_track, note)
        
        # Generate bass line
        bass_notes = pattern['bass_notes']
        for bar in range(bars):
            for beat in range(4):
                bass_note = bass_notes[beat % len(bass_notes)]
                note = SimpleMIDINote(
                    pitch=bass_note,
                    velocity=80,
                    start_time=bar * beat_duration + beat,
                    duration=0.8,
                    channel=0  # Bass channel
                )
                midi_writer.add_note(bass_track, note)
        
        # Write MIDI file
        if not output_file:
            output_file = f"beat_addicts_{genre}_{bars}bars.mid"
        
        success = midi_writer.write_file(output_file, pattern['bpm'])
        
        if success:
            print(f"✅ Generated MIDI file: {output_file}")
            return output_file
        else:
            print(f"❌ Failed to generate MIDI file")
            return None
    
    def generate_training_dataset(self, output_dir: str = "midi_files", tracks_per_genre: int = 4) -> List[str]:
        """Generate training dataset for all genres"""
        os.makedirs(output_dir, exist_ok=True)
        generated_files = []
        
        for genre in self.genre_patterns.keys():
            print(f"🎵 Generating {genre.upper()} training data...")
            
            for i in range(tracks_per_genre):
                bars = 4 + (i * 2)  # Vary the length
                filename = os.path.join(output_dir, f"{genre}_track_{i+1:02d}.mid")
                
                result = self.generate_beat(genre, bars, filename)
                if result:
                    generated_files.append(result)
        
        return generated_files

def test_simple_midi():
    """Test the simple MIDI generator"""
    print("🎵 Testing BEAT ADDICTS Simple MIDI Generator...")
    
    generator = BeatAddictsSimpleMIDIGenerator()
    
    # Test each genre
    for genre in ['dnb', 'hiphop', 'electronic', 'rock']:
        output_file = f"test_{genre}_beat.mid"
        result = generator.generate_beat(genre, bars=2, output_file=output_file)
        
        if result and os.path.exists(result):
            file_size = os.path.getsize(result)
            print(f"✅ {genre.upper()}: {result} ({file_size} bytes)")
        else:
            print(f"❌ {genre.upper()}: Failed to generate")

if __name__ == "__main__":
    test_simple_midi()
