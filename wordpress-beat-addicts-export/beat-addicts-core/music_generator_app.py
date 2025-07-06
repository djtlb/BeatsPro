from flask import Flask, jsonify, render_template, request, send_file, url_for
import os
import sys
import numpy as np
import wave
from datetime import datetime
import io
import base64
import random
import math

# Try to import scipy components with fallbacks
try:
    import scipy.signal
    from scipy import signal
    SCIPY_AVAILABLE = True
except ImportError:
    print("⚠️ SciPy not available - using basic audio processing")
    SCIPY_AVAILABLE = False

try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    print("⚠️ Librosa not available - using basic audio processing")
    LIBROSA_AVAILABLE = False

# Add beat_addicts modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'beat_addicts_core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'beat_addicts_generators'))

# Import BEAT ADDICTS modules using connection manager
try:
    from beat_addicts_connection_manager import BeatAddictsConnectionManager
    
    # Initialize connection manager
    print("🔌 Initializing BEAT ADDICTS Connection Manager...")
    connection_manager = BeatAddictsConnectionManager()
    all_connections = connection_manager.connect_all()
    
    # Extract connected modules
    connected_core = all_connections.get('core', {})
    connected_generators = all_connections.get('generators', {})
    
    # Get the instances we need
    voice_handler = connected_core.get('voice_handler')
    voice_integration = connected_core.get('voice_integration')
    song_exporter = connected_core.get('song_exporter')
    simple_audio_generator = connected_core.get('simple_audio_generator')
    universal_generator = connected_generators.get('universal')
    
    BEAT_ADDICTS_AVAILABLE = True
    print("🎵 BEAT ADDICTS modules successfully connected via Connection Manager!")
    
except ImportError as e:
    print(f"⚠️ BEAT ADDICTS Connection Manager not available: {e}")
    BEAT_ADDICTS_AVAILABLE = False
    voice_handler = None
    simple_audio_generator = None

app = Flask(__name__)

# Create directories for generated content
os.makedirs('static/generated', exist_ok=True)
os.makedirs('static/previews', exist_ok=True)

# Advanced music production classes and functions
class MusicEngine:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.note_frequencies = self._generate_note_frequencies()
        
        # Initialize BEAT ADDICTS modules if available
        if BEAT_ADDICTS_AVAILABLE and simple_audio_generator:
            try:
                self.voice_handler = voice_handler
                self.simple_audio_generator = simple_audio_generator
                self.universal_generator = universal_generator
                self.song_exporter = song_exporter
                
                self.beat_addicts_enabled = True
                print("🔥 BEAT ADDICTS Professional Music Engine Activated!")
                print(f"   ✅ Voice Handler: {'Available' if voice_handler else 'Not Available'}")
                print(f"   ✅ Audio Generator: {'Available' if simple_audio_generator else 'Not Available'}")
                print(f"   ✅ Universal Generator: {'Available' if universal_generator else 'Not Available'}")
                
            except Exception as e:
                print(f"⚠️ BEAT ADDICTS integration failed: {e}")
                self.beat_addicts_enabled = False
        else:
            self.beat_addicts_enabled = False
            print("⚠️ BEAT ADDICTS modules not available for MusicEngine")
        
    def _generate_note_frequencies(self):
        """Generate a full frequency map for musical notes"""
        # A4 = 440 Hz as reference
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        frequencies = {}
        
        for octave in range(0, 9):
            for i, note in enumerate(notes):
                # Calculate frequency using equal temperament
                semitones_from_a4 = (octave - 4) * 12 + (i - 9)  # A is the 9th note
                freq = 440 * (2 ** (semitones_from_a4 / 12))
                frequencies[f"{note}{octave}"] = freq
                
        return frequencies

class Synthesizer:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        
    def generate_waveform(self, frequency, duration, waveform='sine', amplitude=0.5):
        """Generate various waveforms with proper envelopes"""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples, False)
        
        if waveform == 'sine':
            wave_data = np.sin(2 * np.pi * frequency * t)
        elif waveform == 'square':
            wave_data = np.sign(np.sin(2 * np.pi * frequency * t))
        elif waveform == 'sawtooth':
            wave_data = 2 * (t * frequency - np.floor(t * frequency + 0.5))
        elif waveform == 'triangle':
            wave_data = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
        else:
            wave_data = np.sin(2 * np.pi * frequency * t)  # Default to sine
            
        # Apply envelope (ADSR-style)
        envelope = self._generate_envelope(samples)
        wave_data *= envelope * amplitude
        
        return wave_data
    
    def _generate_envelope(self, samples):
        """Generate a simple envelope"""
        envelope = np.ones(samples)
        fade_length = min(1000, samples // 10)  # Fade in/out
        
        # Fade in
        envelope[:fade_length] = np.linspace(0, 1, fade_length)
        # Fade out
        envelope[-fade_length:] = np.linspace(1, 0, fade_length)
        
        return envelope

def generate_audio_wave(duration, genre, mood, prompt):
    """Generate audio based on genre and mood"""
    sample_rate = 44100
    synth = Synthesizer(sample_rate)
    music_engine = MusicEngine(sample_rate)
    
    # Try BEAT ADDICTS Professional Generation first
    if music_engine.beat_addicts_enabled:
        try:
            print(f"🔥 BEAT ADDICTS Professional Generation: {genre}")
            
            # Use BEAT ADDICTS SimpleAudioGenerator for direct audio
            audio_data = music_engine.simple_audio_generator.generate_genre_beat(
                genre=genre,
                duration=duration,
                bpm=120 if 'electronic' in genre.lower() else 140
            )
            
            if audio_data and len(audio_data) > 0:
                print(f"✅ BEAT ADDICTS generation successful! Generated {len(audio_data)} samples")
                # Convert to numpy array and normalize
                audio_array = np.array(audio_data, dtype=np.float32) / 32768.0
                return audio_array, sample_rate
            else:
                print("⚠️ BEAT ADDICTS returned no audio, falling back to basic generation")
        except Exception as e:
            print(f"⚠️ BEAT ADDICTS generation failed: {e}, using fallback")
    
    # Fallback to basic generation
    print(f"🎵 Basic generation for genre: {genre}")
    
    # Generate beat pattern based on genre
    if 'electronic' in genre.lower() or 'edm' in genre.lower():
        beat_pattern = generate_electronic_beat(duration, sample_rate, synth)
    elif 'hip' in genre.lower() or 'rap' in genre.lower() or 'trap' in genre.lower():
        beat_pattern = generate_hiphop_beat(duration, sample_rate, synth)
    elif 'rock' in genre.lower() or 'metal' in genre.lower():
        beat_pattern = generate_rock_beat(duration, sample_rate, synth)
    elif 'folk' in genre.lower() or 'acoustic' in genre.lower():
        beat_pattern = generate_acoustic_beat(duration, sample_rate, synth)
    else:
        beat_pattern = generate_pop_beat(duration, sample_rate, synth)
    
    # Apply mood effects
    if mood == 'energetic':
        beat_pattern *= 1.2  # Increase amplitude
    elif mood == 'calm':
        beat_pattern *= 0.7  # Decrease amplitude
    elif mood == 'sad':
        # Add minor key feeling (this is simplified)
        beat_pattern = apply_lowpass_filter(beat_pattern, sample_rate, 3000)
    
    # Normalize to prevent clipping
    beat_pattern = np.clip(beat_pattern, -1, 1)
    
    return beat_pattern, sample_rate

def generate_electronic_beat(duration, sample_rate, synth):
    """Generate electronic/EDM style beat"""
    samples = int(duration * sample_rate)
    beat = np.zeros(samples)
    
    # Bass line
    bass_freq = 80  # Deep bass
    bass_duration = 0.5
    bass_samples = int(bass_duration * sample_rate)
    
    # Create repeating bass pattern
    for i in range(0, samples, bass_samples):
        if i + bass_samples < samples:
            bass_wave = synth.generate_waveform(bass_freq, bass_duration, 'sine', 0.8)
            beat[i:i+bass_samples] += bass_wave
    
    # Add kick drum pattern (4/4 beat)
    kick_duration = 0.1
    kick_samples = int(kick_duration * sample_rate)
    kick_freq = 60
    
    beats_per_second = 2  # 120 BPM
    kick_interval = int(sample_rate / beats_per_second)
    
    for i in range(0, samples, kick_interval):
        if i + kick_samples < samples:
            kick_wave = synth.generate_waveform(kick_freq, kick_duration, 'sine', 1.0)
            beat[i:i+kick_samples] += kick_wave
    
    # Add hi-hat pattern
    hihat_freq = 8000
    hihat_duration = 0.05
    hihat_samples = int(hihat_duration * sample_rate)
    hihat_interval = kick_interval // 2
    
    for i in range(hihat_interval, samples, hihat_interval):
        if i + hihat_samples < samples:
            hihat_wave = synth.generate_waveform(hihat_freq, hihat_duration, 'square', 0.3)
            beat[i:i+hihat_samples] += hihat_wave
    
    return beat

def generate_hiphop_beat(duration, sample_rate, synth):
    """Generate hip-hop/trap style beat"""
    samples = int(duration * sample_rate)
    beat = np.zeros(samples)
    
    # Heavy 808 bass
    bass_freq = 50
    bass_duration = 0.8
    bass_samples = int(bass_duration * sample_rate)
    
    beats_per_second = 1.5  # Slower tempo
    bass_interval = int(sample_rate / beats_per_second)
    
    for i in range(0, samples, bass_interval):
        if i + bass_samples < samples:
            bass_wave = synth.generate_waveform(bass_freq, bass_duration, 'sine', 0.9)
            beat[i:i+bass_samples] += bass_wave
    
    # Snare on beats 2 and 4
    snare_freq = 200
    snare_duration = 0.1
    snare_samples = int(snare_duration * sample_rate)
    snare_interval = bass_interval * 2
    
    for i in range(bass_interval, samples, snare_interval):
        if i + snare_samples < samples:
            snare_wave = synth.generate_waveform(snare_freq, snare_duration, 'square', 0.7)
            beat[i:i+snare_samples] += snare_wave
    
    return beat

def generate_rock_beat(duration, sample_rate, synth):
    """Generate rock style beat"""
    samples = int(duration * sample_rate)
    beat = np.zeros(samples)
    
    # Guitar-like chords
    chord_freqs = [220, 277, 330]  # A major chord
    chord_duration = 1.0
    chord_samples = int(chord_duration * sample_rate)
    
    for freq in chord_freqs:
        for i in range(0, samples, chord_samples):
            if i + chord_samples < samples:
                chord_wave = synth.generate_waveform(freq, chord_duration, 'sawtooth', 0.3)
                beat[i:i+chord_samples] += chord_wave
    
    # Rock drum pattern
    kick_freq = 80
    kick_duration = 0.1
    kick_samples = int(kick_duration * sample_rate)
    kick_interval = int(sample_rate / 2)  # 120 BPM
    
    for i in range(0, samples, kick_interval):
        if i + kick_samples < samples:
            kick_wave = synth.generate_waveform(kick_freq, kick_duration, 'sine', 0.8)
            beat[i:i+kick_samples] += kick_wave
    
    return beat

def generate_acoustic_beat(duration, sample_rate, synth):
    """Generate acoustic/folk style beat"""
    samples = int(duration * sample_rate)
    beat = np.zeros(samples)
    
    # Gentle acoustic guitar pattern
    chord_freqs = [196, 247, 294]  # G major chord
    chord_duration = 2.0
    chord_samples = int(chord_duration * sample_rate)
    
    for freq in chord_freqs:
        for i in range(0, samples, chord_samples):
            if i + chord_samples < samples:
                chord_wave = synth.generate_waveform(freq, chord_duration, 'triangle', 0.4)
                beat[i:i+chord_samples] += chord_wave
    
    return beat

def generate_pop_beat(duration, sample_rate, synth):
    """Generate pop style beat"""
    samples = int(duration * sample_rate)
    beat = np.zeros(samples)
    
    # Pop chord progression
    chord_progression = [
        [262, 330, 392],  # C major
        [294, 370, 440],  # D minor
        [247, 311, 370],  # G major
        [262, 330, 392]   # C major
    ]
    
    chord_duration = 2.0
    chord_samples = int(chord_duration * sample_rate)
    
    for i, chord_freqs in enumerate(chord_progression):
        start_pos = i * chord_samples
        if start_pos + chord_samples < samples:
            for freq in chord_freqs:
                chord_wave = synth.generate_waveform(freq, chord_duration, 'sine', 0.3)
                beat[start_pos:start_pos+chord_samples] += chord_wave
    
    # Repeat the progression
    progression_length = len(chord_progression) * chord_samples
    remaining_samples = samples - progression_length
    if remaining_samples > 0:
        repetitions = remaining_samples // progression_length + 1
        for rep in range(repetitions):
            for i, chord_freqs in enumerate(chord_progression):
                start_pos = progression_length + rep * progression_length + i * chord_samples
                if start_pos + chord_samples < samples:
                    for freq in chord_freqs:
                        chord_wave = synth.generate_waveform(freq, chord_duration, 'sine', 0.3)
                        end_pos = min(start_pos + chord_samples, samples)
                        wave_length = end_pos - start_pos
                        beat[start_pos:end_pos] += chord_wave[:wave_length]
    
    return beat

def apply_lowpass_filter(audio, sample_rate, cutoff_freq):
    """Apply a low-pass filter with fallback if scipy not available"""
    if not SCIPY_AVAILABLE:
        # Simple fallback filter - basic smoothing
        return simple_lowpass_filter(audio, cutoff_freq, sample_rate)
    
    try:
        nyquist = sample_rate / 2
        normalized_cutoff = cutoff_freq / nyquist
        
        # Ensure cutoff is valid
        if normalized_cutoff >= 1.0:
            normalized_cutoff = 0.99
        if normalized_cutoff <= 0.0:
            normalized_cutoff = 0.01
            
        b, a = signal.butter(4, normalized_cutoff, btype='low')
        return signal.filtfilt(b, a, audio)
    except Exception as e:
        print(f"⚠️ Filter error: {e}, using simple filter")
        return simple_lowpass_filter(audio, cutoff_freq, sample_rate)

def simple_lowpass_filter(audio, cutoff_freq, sample_rate):
    """Simple lowpass filter fallback"""
    # Simple moving average filter as fallback
    window_size = max(1, int(sample_rate / cutoff_freq / 10))
    if window_size >= len(audio):
        return audio
    
    filtered = np.convolve(audio, np.ones(window_size)/window_size, mode='same')
    return filtered

def save_wav_file(audio_data, sample_rate, filename):
    """Save audio data as WAV file"""
    # Normalize to 16-bit range
    audio_16bit = np.int16(audio_data * 32767)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_16bit.tobytes())

def generate_lyrics(prompt, genre):
    """Generate simple lyrics based on prompt and genre"""
    # This is a simplified lyrics generator
    lyrics_templates = {
        'electronic': [
            "Feel the beat drop, lights are flashing\nBass is pumping, hearts are crashing\nLost in sound, we're never stopping\nElectric dreams, our souls are rocking"
        ],
        'hip-hop': [
            "Started from the bottom, now we here\nDreams so big, the vision crystal clear\nHustle every day, make the paper stack\nNever looking down, ain't no turning back"
        ],
        'rock': [
            "Thunder in the distance, lightning in my veins\nRising from the ashes, breaking all the chains\nLoud and proud we stand, never gonna fall\nRock and roll forever, answering the call"
        ],
        'acoustic': [
            "Simple melodies on a quiet night\nGentle whispers in the fading light\nStrings that sing of love and loss\nMelodies that heal what time has crossed"
        ],
        'pop': [
            "Dancing through the night under neon lights\nChasing all our dreams, reaching for new heights\nMusic in our hearts, rhythm in our souls\nTogether we can shine, together we are whole"
        ]
    }
    
    # Match genre keywords
    for genre_key in lyrics_templates:
        if genre_key in genre.lower():
            return lyrics_templates[genre_key][0]
    
    # Default lyrics
    return "Music flows through every beat\nRhythms make our hearts complete\nMelodies that lift us high\nSongs that make our spirits fly"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/drop_beat', methods=['POST'])
def drop_beat():
    try:
        data = request.get_json() or {}
        prompt = data.get('prompt', 'A fresh vibe')
        genre = data.get('genre', 'pop')
        mood = data.get('mood', 'happy')
        duration = min(int(data.get('duration', 180)), 300)  # Max 5 minutes
        
        # Generate unique filename
        timestamp = int(datetime.now().timestamp())
        filename = f"beataddicts_beat_{timestamp}.wav"
        
        # Generate audio
        print(f"Generating {duration}s beat for {genre} {mood} vibe...")
        audio_data, sample_rate = generate_audio_wave(duration, genre, mood, prompt)
        
        # Save full song
        full_path = f"static/generated/{filename}"
        save_wav_file(audio_data, sample_rate, full_path)
        
        # Generate lyrics
        lyrics = generate_lyrics(prompt, genre)
        
        # Get file size
        file_size = f"{os.path.getsize(full_path) / (1024*1024):.1f} MB"
        
        return jsonify({
            'success': True,
            'result': {
                'title': f"Beat Addicts - {prompt.title()}",
                'genre': genre,
                'mood': mood,
                'duration': duration,
                'lyrics': lyrics,
                'filename': filename,
                'file_size': file_size,
                'download_url': f'/download/{filename}'
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated beat file"""
    try:
        file_path = f"static/generated/{filename}"
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list_beats')
def list_beats():
    """List all generated beats"""
    try:
        beats = []
        generated_dir = "static/generated"
        if os.path.exists(generated_dir):
            for filename in os.listdir(generated_dir):
                if filename.endswith('.wav'):
                    file_path = os.path.join(generated_dir, filename)
                    file_size = os.path.getsize(file_path)
                    creation_time = os.path.getctime(file_path)
                    beats.append({
                        'filename': filename,
                        'size': f"{file_size / (1024*1024):.1f} MB",
                        'created': datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S'),
                        'download_url': f'/download/{filename}'
                    })
        
        return jsonify({'success': True, 'beats': beats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🎵 Beat Addicts Music Generator Starting...")
    print("🚀 Navigate to http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
