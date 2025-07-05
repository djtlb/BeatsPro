import numpy as np
import scipy.signal as signal
from scipy.io.wavfile import write
import math

class PremiumAudioEngine:
    def __init__(self, sample_rate=44100):
        self.sr = sample_rate
        self.bpm = 140
        self.beat_duration = 60.0 / self.bpm
        
    def generate_808_kick(self, frequency=50, duration=0.8):
        """Professional 808 kick with sub-bass frequencies"""
        t = np.linspace(0, duration, int(self.sr * duration))
        
        # Fundamental frequency with pitch bend
        pitch_envelope = np.exp(-t * 3)
        freq_mod = frequency * (1 + 0.5 * pitch_envelope)
        
        # Generate sine wave with frequency modulation
        kick = np.sin(2 * np.pi * freq_mod * t)
        
        # Add harmonics for body
        kick += 0.3 * np.sin(2 * np.pi * freq_mod * 1.5 * t)
        kick += 0.1 * np.sin(2 * np.pi * freq_mod * 2 * t)
        
        # Amplitude envelope
        amplitude_env = np.exp(-t * 2.5)
        kick *= amplitude_env
        
        # Add click for punch
        click_duration = 0.005
        click_samples = int(self.sr * click_duration)
        click = np.random.uniform(-1, 1, click_samples)
        click *= np.exp(-np.linspace(0, 10, click_samples))
        
        # Combine click with kick
        kick[:click_samples] += click * 0.3
        
        # Soft saturation
        kick = np.tanh(kick * 2) * 0.8
        
        return self.apply_eq(kick, low_gain=3, mid_gain=0, high_gain=-2)
    
    def generate_trap_snare(self, duration=0.15):
        """Modern trap snare with crisp attack"""
        t = np.linspace(0, duration, int(self.sr * duration))
        
        # Tone component (fundamental around 200Hz)
        tone = np.sin(2 * np.pi * 200 * t)
        tone += 0.5 * np.sin(2 * np.pi * 400 * t)
        
        # Noise component
        noise = np.random.uniform(-1, 1, len(t))
        
        # High-pass filter for crisp noise
        b, a = signal.butter(6, 2000, 'highpass', fs=self.sr)
        noise = signal.filtfilt(b, a, noise)
        
        # Mix components
        snare = 0.2 * tone + 0.8 * noise
        
        # Sharp attack envelope
        envelope = np.exp(-t * 25)
        envelope[0] = 1.0  # Ensure sharp attack
        snare *= envelope
        
        # Add compression effect
        snare = self.compress_audio(snare, threshold=0.3, ratio=4)
        
        return self.apply_eq(snare, low_gain=-1, mid_gain=2, high_gain=3)
    
    def generate_modern_hihat(self, duration=0.08, is_open=False):
        """High-quality hi-hat with metallic sheen"""
        t = np.linspace(0, duration, int(self.sr * duration))
        
        # High-frequency noise
        hihat = np.random.uniform(-1, 1, len(t))
        
        # Band-pass filter for metallic sound
        freq_low = 8000 if not is_open else 6000
        freq_high = 16000 if not is_open else 18000
        b, a = signal.butter(4, [freq_low, freq_high], 'bandpass', fs=self.sr)
        hihat = signal.filtfilt(b, a, hihat)
        
        # Envelope
        if is_open:
            envelope = np.exp(-t * 8)  # Longer decay for open hat
        else:
            envelope = np.exp(-t * 40)  # Quick decay for closed hat
        
        hihat *= envelope
        
        # Add subtle reverb
        return self.add_reverb(hihat, size=0.1, decay=0.2)
    
    def generate_bass_808(self, note='E', duration=2.0):
        """Deep 808 bass line"""
        note_freqs = {
            'C': 65.41, 'D': 73.42, 'E': 82.41, 'F': 87.31,
            'G': 98.00, 'A': 110.00, 'B': 123.47
        }
        
        fundamental = note_freqs.get(note, 82.41)
        t = np.linspace(0, duration, int(self.sr * duration))
        
        # Sub-bass sine wave
        bass = np.sin(2 * np.pi * fundamental * t)
        
        # Add subtle harmonics
        bass += 0.3 * np.sin(2 * np.pi * fundamental * 2 * t)
        bass += 0.1 * np.sin(2 * np.pi * fundamental * 3 * t)
        
        # Modulation for movement
        lfo = np.sin(2 * np.pi * 0.25 * t)  # Slow LFO
        bass *= (1 + 0.15 * lfo)
        
        # Saturation
        bass = np.tanh(bass * 1.8) * 0.7
        
        # Low-pass filter to remove harsh frequencies
        b, a = signal.butter(6, 200, 'lowpass', fs=self.sr)
        bass = signal.filtfilt(b, a, bass)
        
        return bass
    
    def create_trap_pattern(self, duration=8.0):
        """Create a professional trap beat pattern"""
        samples = int(self.sr * duration)
        pattern = np.zeros(samples)
        
        # Generate drum samples
        kick = self.generate_808_kick()
        snare = self.generate_trap_snare()
        hihat_closed = self.generate_modern_hihat(is_open=False)
        hihat_open = self.generate_modern_hihat(duration=0.2, is_open=True)
        
        # Pattern timing
        beats_per_measure = 4
        subdivisions = 4  # 16th notes
        step_duration = self.beat_duration / subdivisions
        
        # 16-step pattern for 4 beats
        kick_pattern = [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        snare_pattern = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        hihat_pattern = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1]
        open_hat_pattern = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        
        # Apply pattern for entire duration
        measures = int(duration / (self.beat_duration * beats_per_measure))
        
        for measure in range(measures):
            for step in range(16):
                step_time = (measure * 16 + step) * step_duration
                step_sample = int(step_time * self.sr)
                
                if step_sample >= samples:
                    break
                
                # Add kick
                if kick_pattern[step]:
                    end_sample = min(step_sample + len(kick), samples)
                    pattern[step_sample:end_sample] += kick[:end_sample-step_sample] * 0.8
                
                # Add snare
                if snare_pattern[step]:
                    end_sample = min(step_sample + len(snare), samples)
                    pattern[step_sample:end_sample] += snare[:end_sample-step_sample] * 0.7
                
                # Add closed hi-hat
                if hihat_pattern[step]:
                    end_sample = min(step_sample + len(hihat_closed), samples)
                    pattern[step_sample:end_sample] += hihat_closed[:end_sample-step_sample] * 0.4
                
                # Add open hi-hat
                if open_hat_pattern[step]:
                    end_sample = min(step_sample + len(hihat_open), samples)
                    pattern[step_sample:end_sample] += hihat_open[:end_sample-step_sample] * 0.3
        
        return pattern
    
    def apply_eq(self, audio, low_gain=0, mid_gain=0, high_gain=0):
        """Simple 3-band EQ"""
        if len(audio) == 0:
            return audio
            
        # Low shelf (below 300Hz)
        if low_gain != 0:
            b, a = signal.butter(2, 300, 'lowpass', fs=self.sr)
            low = signal.filtfilt(b, a, audio)
            audio = audio + low * (10**(low_gain/20) - 1)
        
        # Mid band (300Hz - 3kHz)
        if mid_gain != 0:
            b1, a1 = signal.butter(2, 300, 'highpass', fs=self.sr)
            b2, a2 = signal.butter(2, 3000, 'lowpass', fs=self.sr)
            mid = signal.filtfilt(b1, a1, audio)
            mid = signal.filtfilt(b2, a2, mid)
            audio = audio + mid * (10**(mid_gain/20) - 1)
        
        # High shelf (above 3kHz)
        if high_gain != 0:
            b, a = signal.butter(2, 3000, 'highpass', fs=self.sr)
            high = signal.filtfilt(b, a, audio)
            audio = audio + high * (10**(high_gain/20) - 1)
        
        return audio
    
    def compress_audio(self, audio, threshold=0.5, ratio=4, attack=0.003, release=0.1):
        """Simple audio compressor"""
        # Convert to dB
        audio_db = 20 * np.log10(np.abs(audio) + 1e-10)
        
        # Apply compression
        compressed_db = np.where(
            audio_db > threshold,
            threshold + (audio_db - threshold) / ratio,
            audio_db
        )
        
        # Convert back to linear
        gain_reduction = 10**((compressed_db - audio_db) / 20)
        
        return audio * gain_reduction
    
    def add_reverb(self, audio, size=0.3, decay=0.5):
        """Add reverb effect"""
        if len(audio) == 0:
            return audio
            
        # Create impulse response
        impulse_length = int(self.sr * size)
        impulse = np.random.exponential(0.1, impulse_length)
        impulse *= np.exp(-np.linspace(0, 5 * decay, impulse_length))
        
        # Convolve with input
        reverb = np.convolve(audio, impulse, mode='same')
        
        return audio + 0.2 * reverb
    
    def master_track(self, audio):
        """Final mastering with limiting"""
        # Normalize
        peak = np.max(np.abs(audio))
        if peak > 0:
            audio = audio / peak * 0.8
        
        # Soft limiting
        audio = np.tanh(audio * 1.2) * 0.9
        
        return audio
    
    def export_wav(self, audio, filename, normalize=True):
        """Export audio to WAV file"""
        if normalize:
            audio = self.master_track(audio)
        
        # Convert to 16-bit
        audio_16bit = (audio * 32767).astype(np.int16)
        
        write(filename, self.sr, audio_16bit)
        print(f"Audio exported to: {filename}")

# Example usage
if __name__ == "__main__":
    engine = PremiumAudioEngine()
    
    # Create full beat
    drums = engine.create_trap_pattern(8.0)
    bass = engine.generate_bass_808('E', 8.0)
    
    # Mix
    full_beat = drums + bass * 0.6
    
    # Export
    engine.export_wav(full_beat, "premium_trap_beat.wav")
