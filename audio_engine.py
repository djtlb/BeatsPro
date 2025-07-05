import numpy as np
import soundfile as sf
from scipy import signal
import librosa
class ModernAudioEngine:
    def __init__(self, sample_rate=44100):
        self.sr = sample_rate
        self.bpm = 140  # Modern trap/rap tempo
        
    def generate_808_kick(self, duration=0.5, fundamental=60):
        """Generate a punchy 808-style kick drum"""
        t = np.linspace(0, duration, int(self.sr * duration))
        
        # Sine wave with exponential decay
        kick = np.sin(2 * np.pi * fundamental * t)
        
        # Add harmonics for punch
        kick += 0.3 * np.sin(2 * np.pi * fundamental * 2 * t)
        kick += 0.1 * np.sin(2 * np.pi * fundamental * 3 * t)
        
        # Exponential decay envelope
        envelope = np.exp(-t * 8)
        kick *= envelope
        
        # Add click for attack
        click = np.random.normal(0, 0.1, len(t))
        click_envelope = np.exp(-t * 50)
        kick += click * click_envelope * 0.2
        
        # Saturation/distortion
        kick = np.tanh(kick * 2)
        
        return self.normalize_audio(kick)
    
    def generate_hi_hat(self, duration=0.1):
        """Generate crisp hi-hat"""
        t = np.linspace(0, duration, int(self.sr * duration))
        
        # High frequency noise
        hihat = np.random.normal(0, 1, len(t))
        
        # High-pass filter
        sos = signal.butter(4, 8000, 'highpass', fs=self.sr, output='sos')
        hihat_filtered = signal.sosfilt(sos, hihat)
        
        # Ensure hihat_filtered is an array, not a tuple
        if isinstance(hihat_filtered, tuple):
            hihat_filtered = hihat_filtered[0]
        
        # Sharp attack, quick decay
        envelope = np.exp(-t * 30)
        hihat = hihat_filtered * envelope
        
        return self.normalize_audio(hihat)
    
    def generate_snare(self, duration=0.2):
        """Generate punchy snare"""
        t = np.linspace(0, duration, int(self.sr * duration))
        
        # Tone component (200Hz fundamental)
        tone = np.sin(2 * np.pi * 200 * t)
        # Band-pass filter for noise
        sos = signal.butter(4, [1000, 8000], 'bandpass', fs=self.sr, output='sos')
        noise_filtered = signal.sosfilt(sos, noise)
        
        # Ensure noise_filtered is an array, not a tuple
        if isinstance(noise_filtered, tuple):
            noise_filtered = noise_filtered[0]
        
        # Mix tone and noise
        snare = 0.3 * tone + 0.7 * noise_filtered
            noise = noise[0]
        
        # Mix tone and noise
        snare = 0.3 * tone + 0.7 * noise
        
        # Envelope
        envelope = np.exp(-t * 15)
        snare *= envelope
        
        return self.normalize_audio(snare)
    
    def generate_bass_line(self, duration=2.0, key='E'):
        """Generate modern trap-style bass line"""
        note_frequencies = {
            'E': 82.41, 'F': 87.31, 'G': 98.00, 'A': 110.00, 'B': 123.47
        }
        
        fundamental = note_frequencies.get(key, 82.41)
        t = np.linspace(0, duration, int(self.sr * duration))
        
        # Sub bass with harmonics
        bass = np.sin(2 * np.pi * fundamental * t)
        bass += 0.5 * np.sin(2 * np.pi * fundamental * 2 * t)
        bass += 0.2 * np.sin(2 * np.pi * fundamental * 4 * t)
        
        # Add movement with LFO
        lfo = np.sin(2 * np.pi * 0.5 * t)  # 0.5 Hz LFO
        bass *= (1 + 0.2 * lfo)
        
        # Saturation
        bass = np.tanh(bass * 1.5)
        
        return self.normalize_audio(bass)
    
    def create_trap_beat(self, duration=8.0):
        """Create a modern trap beat pattern"""
        samples = int(self.sr * duration)
        beat = np.zeros(samples)
        
        # Calculate timing
        beat_duration = 60.0 / self.bpm  # Duration of one beat
        samples_per_beat = int(self.sr * beat_duration)
        
        # Generate samples
        kick = self.generate_808_kick()
        snare = self.generate_snare()
        hihat = self.generate_hi_hat()
        
        # Pattern: Kick on 1 and 3, snare on 2 and 4
        for beat_num in range(int(duration / beat_duration)):
            start_sample = beat_num * samples_per_beat
            
            # Kick pattern (1, 1.5, 3, 3.5)
            if beat_num % 4 in [0, 2]:  # Beats 1 and 3
                end_sample = min(start_sample + len(kick), samples)
                beat[start_sample:end_sample] += kick[:end_sample-start_sample]
                
                # Add off-beat kick
                off_beat_start = start_sample + samples_per_beat // 2
                if off_beat_start < samples:
                    off_beat_end = min(off_beat_start + len(kick), samples)
                    beat[off_beat_start:off_beat_end] += kick[:off_beat_end-off_beat_start] * 0.7
            
            # Snare on beats 2 and 4
            if beat_num % 4 in [1, 3]:
                end_sample = min(start_sample + len(snare), samples)
                beat[start_sample:end_sample] += snare[:end_sample-start_sample]
            
            # Hi-hats on every 1/8th note
            for eighth in range(2):
                hihat_start = start_sample + eighth * (samples_per_beat // 2)
                if hihat_start < samples:
                    hihat_end = min(hihat_start + len(hihat), samples)
                    beat[hihat_start:hihat_end] += hihat[:hihat_end-hihat_start] * 0.6
        
        return self.normalize_audio(beat)
    
    def add_reverb(self, audio, room_size=0.5, damping=0.5):
        """Add reverb effect"""
        # Simple convolution reverb
        impulse_length = int(self.sr * 2 * room_size)
        impulse = np.random.exponential(0.1, impulse_length)
        impulse *= np.exp(-np.linspace(0, 10 * damping, impulse_length))
        
        reverb = np.convolve(audio, impulse, mode='same')
        return audio + 0.3 * reverb
    
    def normalize_audio(self, audio, target_db=-6):
        """Normalize audio to target dB"""
        if np.max(np.abs(audio)) == 0:
            return audio
        
        target_amplitude = 10 ** (target_db / 20)
        current_peak = np.max(np.abs(audio))
        gain = target_amplitude / current_peak
        
        return audio * gain
    
    def save_audio(self, audio, filename):
        """Save audio to file"""
        sf.write(filename, audio, self.sr)

# Usage example
if __name__ == "__main__":
    engine = ModernAudioEngine()
    
    # Create a beat
    beat = engine.create_trap_beat(duration=8.0)
    
    # Add bass line
    bass = engine.generate_bass_line(duration=8.0)
    
    # Mix together
    full_track = beat + 0.7 * bass
    full_track = engine.add_reverb(full_track)
    full_track = engine.normalize_audio(full_track)
    
    # Save
    engine.save_audio(full_track, "modern_rap_beat.wav")
    print("Modern rap beat generated and saved!")
