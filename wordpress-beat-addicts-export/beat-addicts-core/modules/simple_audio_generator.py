#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Simple Audio Generator
Standalone audio generation without Flask dependencies
"""

import os
import math
import struct
from typing import List

class BeatAddictsSimpleAudioGenerator:
    """Simple audio generator for BEAT ADDICTS"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
    
    def generate_simple_beat(self, bpm=140, bars=4, genre='electronic') -> List[int]:
        """Generate a simple beat pattern"""
        beat_duration = 60.0 / bpm
        total_duration = bars * 4 * beat_duration
        total_samples = int(self.sample_rate * total_duration)
        audio_buffer = [0] * total_samples
        
        for bar in range(bars):
            for beat in range(4):
                beat_time = (bar * 4 + beat) * beat_duration
                beat_sample = int(beat_time * self.sample_rate)
                
                # Add kick drum on beats 1 and 3
                if beat in [0, 2]:
                    kick_samples = self._generate_kick()
                    for i, sample in enumerate(kick_samples):
                        if beat_sample + i < len(audio_buffer):
                            audio_buffer[beat_sample + i] = sample
                
                # Add snare on beats 2 and 4
                if beat in [1, 3]:
                    snare_samples = self._generate_snare()
                    for i, sample in enumerate(snare_samples):
                        if beat_sample + i < len(audio_buffer):
                            audio_buffer[beat_sample + i] += sample
                
                # Add hi-hat every half beat
                if genre.lower() in ['electronic', 'dance', 'edm']:
                    for sub_beat in range(2):
                        hihat_time = beat_time + (sub_beat * beat_duration / 2)
                        hihat_sample = int(hihat_time * self.sample_rate)
                        hihat_samples = self._generate_hihat()
                        for i, sample in enumerate(hihat_samples):
                            if hihat_sample + i < len(audio_buffer):
                                audio_buffer[hihat_sample + i] += int(sample * 0.3)
        
        # Add some bass line
        if genre.lower() in ['electronic', 'dance', 'edm', 'dnb']:
            self._add_bass_line(audio_buffer, bars, bpm)
        
        # Normalize to prevent clipping
        max_val = max(abs(s) for s in audio_buffer)
        if max_val > 32767:
            scale = 32767 / max_val
            audio_buffer = [int(s * scale) for s in audio_buffer]
        
        return audio_buffer
    
    def _generate_kick(self) -> List[int]:
        """Generate kick drum sample"""
        duration = 0.15  # 150ms
        samples = int(duration * self.sample_rate)
        kick = []
        
        for i in range(samples):
            t = i / self.sample_rate
            # Exponentially decaying sine wave at low frequency
            amplitude = math.exp(-t * 15) * 0.8
            frequency = 60 * (1 - t * 2)  # Pitch bend down
            sample = int(amplitude * math.sin(2 * math.pi * frequency * t) * 32767)
            kick.append(sample)
        
        return kick
    
    def _generate_snare(self) -> List[int]:
        """Generate snare drum sample"""
        duration = 0.1  # 100ms
        samples = int(duration * self.sample_rate)
        snare = []
        
        for i in range(samples):
            t = i / self.sample_rate
            # Mix of noise and tone
            amplitude = math.exp(-t * 20) * 0.6
            noise = (hash(i) % 1000 - 500) / 500.0  # Simple noise
            tone = math.sin(2 * math.pi * 200 * t)
            sample = int(amplitude * (noise * 0.7 + tone * 0.3) * 32767)
            snare.append(sample)
        
        return snare
    
    def _generate_hihat(self) -> List[int]:
        """Generate hi-hat sample"""
        duration = 0.05  # 50ms
        samples = int(duration * self.sample_rate)
        hihat = []
        
        for i in range(samples):
            t = i / self.sample_rate
            # High frequency noise
            amplitude = math.exp(-t * 40) * 0.3
            noise = (hash(i * 7) % 1000 - 500) / 500.0
            sample = int(amplitude * noise * 32767)
            hihat.append(sample)
        
        return hihat
    
    def _add_bass_line(self, audio_buffer: List[int], bars: int, bpm: int):
        """Add a simple bass line"""
        beat_duration = 60.0 / bpm
        
        # Simple bass pattern
        bass_notes = [40, 40, 45, 45] * bars  # MIDI note numbers
        
        for i, note in enumerate(bass_notes):
            if i >= bars * 4:
                break
                
            note_time = i * beat_duration
            note_sample = int(note_time * self.sample_rate)
            frequency = 440 * (2 ** ((note - 69) / 12))  # Convert MIDI to frequency
            
            # Generate bass note
            note_duration = beat_duration * 0.8  # 80% of beat duration
            note_samples = int(note_duration * self.sample_rate)
            
            for j in range(note_samples):
                if note_sample + j < len(audio_buffer):
                    t = j / self.sample_rate
                    amplitude = 0.4 * (1 - t / note_duration)  # Fade out
                    sample = int(amplitude * math.sin(2 * math.pi * frequency * t) * 32767)
                    audio_buffer[note_sample + j] += sample
    
    def export_wav(self, audio_data: List[int], filename: str):
        """Export audio data to WAV file"""
        wav_header = struct.pack('<4sI4s4sIHHIIHH4sI',
            b'RIFF', 36 + len(audio_data) * 2, b'WAVE', b'fmt ', 16, 1, 1,
            self.sample_rate, self.sample_rate * 2, 2, 16, b'data', len(audio_data) * 2)
        
        with open(filename, 'wb') as f:
            f.write(wav_header)
            for sample in audio_data:
                f.write(struct.pack('<h', max(-32768, min(32767, sample))))
    
    def generate_genre_beat(self, genre: str, duration: int = 30, bpm: int = 120) -> List[int]:
        """Generate beat based on genre"""
        bars = max(1, int(duration * bpm / 240))  # Approximate bars
        
        # Adjust BPM based on genre
        if genre.lower() in ['dnb', 'drum and bass']:
            bpm = 174
        elif genre.lower() in ['dubstep', 'bass']:
            bpm = 140
        elif genre.lower() in ['house', 'techno']:
            bpm = 128
        elif genre.lower() in ['trance']:
            bpm = 138
        elif genre.lower() in ['trap', 'hip hop', 'rap']:
            bpm = 80
        
        return self.generate_simple_beat(bpm=bpm, bars=bars, genre=genre)

# Quick test function
def test_generator():
    """Test the audio generator"""
    generator = BeatAddictsSimpleAudioGenerator()
    
    print("🎵 Testing BEAT ADDICTS Simple Audio Generator...")
    
    # Test electronic beat
    audio_data = generator.generate_genre_beat('electronic', duration=10, bpm=128)
    
    print(f"✅ Generated {len(audio_data)} samples")
    print(f"   Duration: {len(audio_data) / generator.sample_rate:.2f} seconds")
    
    # Export test file
    test_file = "test_beat.wav"
    generator.export_wav(audio_data, test_file)
    
    if os.path.exists(test_file):
        print(f"✅ Exported test file: {test_file}")
        file_size = os.path.getsize(test_file) / 1024
        print(f"   File size: {file_size:.1f} KB")
    else:
        print("❌ Failed to export test file")

if __name__ == "__main__":
    test_generator()
