from ai_music_producer import NeuralMusicAI, ProductionSettings
import numpy as np
import json
import time
from datetime import datetime
from scipy.io.wavfile import write
from scipy import signal
import threading
import random

class AIProductionBot:
    def __init__(self):
        self.ai_brain = NeuralMusicAI(sample_rate=48000)
        self.is_learning = True
        self.session_data = []
        self.real_time_mode = False
        
        # 2025 Production Presets
        self.presets = {
            "hyperpop_2025": {
                "bpm": 160, "genre": "hyperpop", "energy_level": 0.95,
                "complexity": 0.8, "modern_factor": 1.0
            },
            "drill_uk": {
                "bpm": 140, "genre": "drill", "energy_level": 0.85,
                "complexity": 0.6, "modern_factor": 0.9
            },
            "phonk_wave": {
                "bpm": 135, "genre": "phonk", "energy_level": 0.75,
                "complexity": 0.7, "modern_factor": 0.8
            },
            "jersey_club": {
                "bpm": 145, "genre": "jersey", "energy_level": 0.9,
                "complexity": 0.75, "modern_factor": 0.95
            },
            "future_ambient": {
                "bpm": 120, "genre": "ambient_trap", "energy_level": 0.4,
                "complexity": 0.5, "modern_factor": 1.0
            }
        }
    
    def load_preset(self, preset_name):
        """Load production preset"""
        if preset_name in self.presets:
            preset = self.presets[preset_name]
            self.ai_brain.settings = ProductionSettings(
                bpm=preset["bpm"],
                genre=preset["genre"],
                energy_level=preset["energy_level"],
                complexity=preset["complexity"],
                modern_factor=preset["modern_factor"]
            )
            print(f"🎛️ Loaded preset: {preset_name}")
            return True
        return False
    
    def ai_analyze_and_produce(self, reference_audio=None, duration=16.0):
        """AI analyzes reference and produces matching track"""
        print("🧠 AI Brain analyzing...")
        
        # AI analysis
        analysis = self.ai_brain.analyze_vibe(reference_audio)
        print(f"📊 Detected: Energy={analysis['detected_energy']:.2f}, "
              f"Complexity={analysis['complexity']:.2f}")
        
        # Auto-select genre
        suggested_genre = analysis['recommended_genre']
        print(f"🎵 AI suggests: {suggested_genre}")
        
        # Find matching preset
        matching_preset = None
        for preset_name, preset in self.presets.items():
            if preset["genre"] == suggested_genre:
                matching_preset = preset_name
                break
        
        if matching_preset:
            self.load_preset(matching_preset)
        
        # Generate production
        return self._produce_full_track(duration)
    
    def _produce_full_track(self, duration):
        """Produce complete track with AI"""
        print("🎹 AI generating drums...")
        drums = self.ai_brain.generate_intelligent_drums(duration)
        
        print("🎸 AI generating bass...")
        bass = self._generate_ai_bass(duration)
        
        print("🎺 AI generating melody...")
        melody = self._generate_ai_melody(duration)
        
        print("🎛️ AI mixing...")
        # Mix with AI intelligence
        mix = drums + bass * 0.6 + melody * 0.4
        
        print("🎚️ AI mastering...")
        mastered = self.ai_brain.ai_master_track(mix)
        
        # Learn from this production
        self._learn_from_session(drums, bass, melody, mastered)
        
        return mastered
    
    def _generate_ai_bass(self, duration):
        """AI-generated bass line"""
        samples = int(self.ai_brain.sr * duration)
        bass_line = np.zeros(samples)
        
        # AI determines note progression
        root_freq = 82.41  # E2
        progression = self._ai_chord_progression()
        
        note_duration = 60.0 / self.ai_brain.settings.bpm * 2  # Half notes
        
        for i, note_offset in enumerate(progression):
            start_time = i * note_duration
            if start_time >= duration:
                break
            
            note_freq = root_freq * (2 ** (note_offset / 12))
            bass_note = self.ai_brain.generate_neural_808(note_freq, note_duration, "modern")
            
            start_sample = int(start_time * self.ai_brain.sr)
            end_sample = min(start_sample + len(bass_note), samples)
            
            bass_line[start_sample:end_sample] += bass_note[:end_sample-start_sample]
        
        return bass_line
    
    def _generate_ai_melody(self, duration):
        """AI-generated melody"""
        samples = int(self.ai_brain.sr * duration)
        melody = np.zeros(samples)
        
        # AI melody generation
        scale = [0, 2, 4, 5, 7, 9, 11]  # Major scale
        base_freq = 329.63  # E4
        
        note_duration = 60.0 / self.ai_brain.settings.bpm / 2  # Eighth notes
        num_notes = int(duration / note_duration)
        
        for i in range(num_notes):
            if random.random() < 0.7:  # 70% chance of note
                scale_degree = random.choice(scale)
                octave_shift = random.choice([0, 12, -12]) * 0.1 * self.ai_brain.creativity_factor
                
                note_freq = base_freq * (2 ** ((scale_degree + octave_shift) / 12))
                note = self._generate_synth_note(note_freq, note_duration * 0.8)
                
                start_sample = int(i * note_duration * self.ai_brain.sr)
                end_sample = min(start_sample + len(note), samples)
                
                melody[start_sample:end_sample] += note[:end_sample-start_sample] * 0.3
        
        return melody
    
    def _generate_synth_note(self, frequency, duration):
        """Generate synthesized note"""
        t = np.linspace(0, duration, int(self.ai_brain.sr * duration))
        
        # Saw wave with filter
        note = signal.sawtooth(2 * np.pi * frequency * t)
        
        # Low-pass filter
        cutoff = frequency * 4 * (1 + 0.5 * self.ai_brain.settings.modern_factor)
        b, a = signal.butter(4, cutoff, 'lowpass', fs=self.ai_brain.sr)
        note = signal.filtfilt(b, a, note)
        
        # ADSR envelope
        attack_time = 0.05
        decay_time = 0.1
        sustain_level = 0.7
        release_time = duration * 0.3
        
        envelope = self._adsr_envelope(len(t), attack_time, decay_time, 
                                     sustain_level, release_time, self.ai_brain.sr)
        
        return note * envelope
    
    def _adsr_envelope(self, length, attack, decay, sustain, release, sr):
        """Generate ADSR envelope"""
        envelope = np.zeros(length)
        
        attack_samples = int(attack * sr)
        decay_samples = int(decay * sr)
        release_samples = int(release * sr)
        sustain_samples = length - attack_samples - decay_samples - release_samples
        
        # Attack
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay
        start_idx = attack_samples
        end_idx = start_idx + decay_samples
        envelope[start_idx:end_idx] = np.linspace(1, sustain, decay_samples)
        
        # Sustain
        start_idx = end_idx
        end_idx = start_idx + sustain_samples
        envelope[start_idx:end_idx] = sustain
        
        # Release
        start_idx = end_idx
        envelope[start_idx:] = np.linspace(sustain, 0, len(envelope[start_idx:]))
        
        return envelope
    
    def _ai_chord_progression(self):
        """AI generates chord progression"""
        progressions = [
            [0, 5, 3, 4],    # vi-IV-I-V
            [0, 3, 5, 4],    # vi-I-IV-V
            [0, 4, 5, 3],    # vi-V-IV-I
            [0, 7, 5, 3]     # vi-bVII-IV-I
        ]
        
        return random.choice(progressions) * 4  # Repeat 4 times
    
    def _learn_from_session(self, drums, bass, melody, final):
        """AI learns from production session"""
        session_info = {
            "timestamp": datetime.now().isoformat(),
            "settings": {
                "bpm": self.ai_brain.settings.bpm,
                "genre": self.ai_brain.settings.genre,
                "energy": self.ai_brain.settings.energy_level,
                "complexity": self.ai_brain.settings.complexity
            },
            "audio_features": {
                "drums_rms": float(np.sqrt(np.mean(drums**2))),
                "bass_rms": float(np.sqrt(np.mean(bass**2))),
                "melody_rms": float(np.sqrt(np.mean(melody**2))),
                "final_rms": float(np.sqrt(np.mean(final**2)))
            }
        }
        
        self.session_data.append(session_info)
        
        # Adapt AI parameters based on learning
        if len(self.session_data) > 5:
            self._adapt_ai_parameters()
    
    def _adapt_ai_parameters(self):
        """Adapt AI parameters based on learning"""
        recent_sessions = self.session_data[-5:]
        
        # Calculate average parameters
        avg_energy = np.mean([s["settings"]["energy"] for s in recent_sessions])
        avg_complexity = np.mean([s["settings"]["complexity"] for s in recent_sessions])
        
        # Slight adaptation towards successful patterns
        adaptation_rate = 0.05
        self.ai_brain.creativity_factor += adaptation_rate * (avg_energy - 0.5)
        self.ai_brain.creativity_factor = np.clip(self.ai_brain.creativity_factor, 0.1, 1.0)
        
        print(f"🤖 AI adapted: creativity_factor = {self.ai_brain.creativity_factor:.3f}")
    
    def export_production(self, audio, filename_base):
        """Export production with metadata"""
        # Ensure stereo
        if audio.ndim == 1:
            audio_stereo = np.column_stack([audio, audio])
        else:
            audio_stereo = audio
        
        # Normalize
        peak = np.max(np.abs(audio_stereo))
        if peak > 0:
            audio_stereo = audio_stereo / peak * 0.9
        
        # Convert to 16-bit
        audio_16bit = (audio_stereo * 32767).astype(np.int16)
        
        # Export audio
        audio_file = f"{filename_base}.wav"
        write(audio_file, self.ai_brain.sr, audio_16bit)
        
        # Export metadata
        metadata = {
            "ai_producer_version": "2025.1.0",
            "timestamp": datetime.now().isoformat(),
            "settings": {
                "bpm": self.ai_brain.settings.bpm,
                "genre": self.ai_brain.settings.genre,
                "energy_level": self.ai_brain.settings.energy_level,
                "complexity": self.ai_brain.settings.complexity,
                "modern_factor": self.ai_brain.settings.modern_factor
            },
            "ai_parameters": {
                "creativity_factor": self.ai_brain.creativity_factor,
                "learning_rate": self.ai_brain.learning_rate,
                "sessions_learned": len(self.session_data)
            },
            "audio_info": {
                "sample_rate": self.ai_brain.sr,
                "channels": audio_stereo.shape[1] if audio_stereo.ndim > 1 else 1,
                "duration": len(audio_stereo) / self.ai_brain.sr,
                "peak_level": float(peak)
            }
        }
        
        metadata_file = f"{filename_base}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"🎵 Exported: {audio_file}")
        print(f"📋 Metadata: {metadata_file}")
        
        return audio_file, metadata_file

# Example usage
if __name__ == "__main__":
    bot = AIProductionBot()
    
    print("🤖 AI MUSIC PRODUCTION BOT 2025 🤖")
    print("=" * 40)
    
    # Load a 2025 preset
    bot.load_preset("hyperpop_2025")
    
    # Produce track
    print("🎹 AI producing track...")
    track = bot._produce_full_track(16.0)
    
    # Export
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bot.export_production(track, f"ai_production_{timestamp}")
    
    print("✅ AI production complete!")
