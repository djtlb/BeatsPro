from flask import Flask, request, jsonify, render_template, send_file
import os
import json
import time
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/generated'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# AI Music Generation API Keys (you'll need to get these)
SUNO_API_KEY = os.environ.get('SUNO_API_KEY', '')  # Get from suno.ai
UDIO_API_KEY = os.environ.get('UDIO_API_KEY', '')  # Alternative: udio.com
MUSICGEN_API_KEY = os.environ.get('MUSICGEN_API_KEY', '')  # Alternative: Hugging Face

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/drop_beat', methods=['POST'])
def drop_beat():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        genre = data.get('genre', '')
        mood = data.get('mood', 'energetic')
        duration = data.get('duration', 180)
        
        # Try different AI services in order of preference
        result = None
        
        # 1. Try Suno AI (most popular)
        if SUNO_API_KEY and not result:
            result = generate_with_suno(prompt, genre, mood, duration)
        
        # 2. Try Udio as backup
        if UDIO_API_KEY and not result:
            result = generate_with_udio(prompt, genre, mood, duration)
            
        # 3. Try MusicGen as backup
        if MUSICGEN_API_KEY and not result:
            result = generate_with_musicgen(prompt, genre, mood, duration)
        
        # 4. Fall back to demo if no APIs available
        if not result:
            result = generate_demo_music(prompt, genre, mood, duration)
            result['demo_mode'] = True
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def generate_with_suno(prompt, genre, mood, duration):
    """Generate music using Suno AI API"""
    try:
        # Suno AI API call
        headers = {
            'Authorization': f'Bearer {SUNO_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'prompt': f"{genre} {mood} music: {prompt}",
            'duration': duration,
            'format': 'mp3'
        }
        
        response = requests.post(
            'https://api.suno.ai/v1/generate',  # Example endpoint
            headers=headers,
            json=payload,
            timeout=300  # 5 minute timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'id': data.get('id'),
                'title': data.get('title', f'AI Generated - {prompt[:30]}'),
                'filename': data.get('filename'),
                'duration': duration,
                'genre': genre,
                'mood': mood,
                'prompt': prompt,
                'audio_url': data.get('audio_url'),
                'lyrics': data.get('lyrics', ''),
                'file_size': data.get('file_size', 'Unknown'),
                'ai_service': 'Suno AI'
            }
    except Exception as e:
        print(f"Suno AI failed: {e}")
        return None

def generate_with_udio(prompt, genre, mood, duration):
    """Generate music using Udio API"""
    try:
        # Udio API call (similar structure)
        headers = {
            'Authorization': f'Bearer {UDIO_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'description': f"{genre} {mood}: {prompt}",
            'duration_seconds': duration
        }
        
        # This is a placeholder - replace with actual Udio endpoint
        response = requests.post(
        sub_envelope = np.exp(-t * 8)
        sub_component = sub_wave * sub_envelope * 0.8
        
        # Punch component  
        punch_wave = np.sin(2 * np.pi * punch_freq * t * (1 + np.exp(-t * 15)))
        punch_envelope = np.exp(-t * 12)
        punch_component = punch_wave * punch_envelope * 0.6
        
        # Noise click for attack
        click_samples = min(samples // 20, 100)
        click = np.random.normal(0, 0.1, click_samples) * np.exp(-np.linspace(0, 10, click_samples))
        
        kick = sub_component + punch_component
        kick[:len(click)] += click
        
        return np.clip(kick, -1, 1)
    
    def generate_snare(self, duration=0.3):
        """Generate realistic snare drum"""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples, False)
        
        # Tone component (200Hz fundamental)
        tone_freq = 200
        tone_wave = np.sin(2 * np.pi * tone_freq * t) * 0.4
        
        # Noise component for snare buzz
        noise = np.random.normal(0, 0.3, samples)
        
        # High-pass filter the noise
        b, a = signal.butter(4, 1000 / (self.sample_rate / 2), 'high')
        filtered_noise = signal.filtfilt(b, a, noise)
        
        # Envelope
        envelope = np.exp(-t * 15) * (1 + 0.5 * np.exp(-t * 50))
        
        snare = (tone_wave + filtered_noise * 0.7) * envelope
        return np.clip(snare, -1, 1)
    
    def generate_hihat(self, duration=0.1, closed=True):
        """Generate hi-hat (closed or open)"""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples, False)
        
        # High-frequency noise
        noise = np.random.normal(0, 0.2, samples)
        
        # High-pass filter for metallic sound
        cutoff = 8000 if closed else 6000
        b, a = signal.butter(6, cutoff / (self.sample_rate / 2), 'high')
        filtered_noise = signal.filtfilt(b, a, noise)
        
        # Envelope (shorter for closed hat)
        decay_rate = 25 if closed else 8
        envelope = np.exp(-t * decay_rate)
        
        hihat = filtered_noise * envelope
        return np.clip(hihat, -1, 1)
        
    def generate_808(self, frequency=55, duration=0.8):
        """Generate 808-style sub bass"""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples, False)
        
        # Sine wave with frequency modulation
        freq_mod = frequency * (1 + 0.3 * np.exp(-t * 5))
        phase = 2 * np.pi * np.cumsum(freq_mod) / self.sample_rate
        wave = np.sin(phase)
        
        # Envelope with punch
        envelope = np.exp(-t * 3) * (1 + 0.5 * np.exp(-t * 20))
        
        # Add harmonics for more character
        harmonics = 0.3 * np.sin(phase * 2) * np.exp(-t * 5)
        
        bass_808 = (wave + harmonics) * envelope
        return np.clip(bass_808, -1, 1)

class AudioEffects:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        
    def reverb(self, audio, room_size=0.5, damping=0.5, wet=0.3):
        """Apply reverb effect"""
        # Simple reverb using multiple delayed echoes
        delay_times = [0.03, 0.06, 0.09, 0.12, 0.15]  # seconds
        decays = [0.7, 0.6, 0.5, 0.4, 0.3]
        
        reverb_audio = np.copy(audio)
        
        for delay_time, decay in zip(delay_times, decays):
            delay_samples = int(delay_time * self.sample_rate)
            if delay_samples < len(audio):
                delayed = np.zeros_like(audio)
                delayed[delay_samples:] = audio[:-delay_samples] * decay * room_size
                reverb_audio += delayed
                
        # Apply damping (low-pass filter)
        if damping > 0:
            b, a = signal.butter(2, (1 - damping) * 8000 / (self.sample_rate / 2), 'low')
            reverb_audio = signal.filtfilt(b, a, reverb_audio)
        
        # Mix wet and dry signals
        return audio * (1 - wet) + reverb_audio * wet
    
    def delay(self, audio, delay_time=0.25, feedback=0.4, mix=0.3):
        """Apply delay effect"""
        delay_samples = int(delay_time * self.sample_rate)
        delayed_audio = np.zeros_like(audio)
        
        if delay_samples < len(audio):
            delayed_audio[delay_samples:] = audio[:-delay_samples]
            
            # Add feedback
            for i in range(3):  # Multiple echoes
                delay_offset = delay_samples * (i + 2)
                if delay_offset < len(audio):
                    delayed_audio[delay_offset:] += audio[:-delay_offset] * (feedback ** (i + 1))
        
        return audio * (1 - mix) + delayed_audio * mix
    
    def distortion(self, audio, drive=2.0, mix=1.0):
        """Apply distortion/overdrive"""
        # Soft clipping distortion
        distorted = np.tanh(audio * drive) / drive
        return audio * (1 - mix) + distorted * mix
    
    def chorus(self, audio, depth=0.002, rate=1.5, mix=0.5):
        """Apply chorus effect"""
        # Simple chorus using delayed and modulated signal
        lfo_samples = int(len(audio))
        t = np.linspace(0, len(audio) / self.sample_rate, lfo_samples)
        lfo = np.sin(2 * np.pi * rate * t)
        
        # Variable delay
        base_delay = 0.02  # 20ms base delay
        modulated_delay = base_delay + depth * lfo
        
        chorus_audio = np.zeros_like(audio)
        for i in range(len(audio)):
            delay_samples = int(modulated_delay[i] * self.sample_rate)
            if i >= delay_samples:
                chorus_audio[i] = audio[i - delay_samples]
        
        return audio * (1 - mix) + chorus_audio * mix

def generate_audio_wave(duration=120, genre='pop', mood='happy', prompt=''):
    """Generate professional-quality music with advanced synthesis and production"""
    
    # Initialize music engine
    engine = MusicEngine()
    synth = Synthesizer()
    drums = DrumMachine()
    effects = AudioEffects()
    
    # Analyze genre for detailed musical characteristics
    genre_analysis = analyze_genre_text(genre.lower())
    
    # Set up musical parameters
    key_root = genre_analysis['key']
    scale_type = genre_analysis['scale']
    bpm = calculate_bpm(genre_analysis['type'], mood)
    
    # Generate note frequencies for the key
    scale_notes = generate_scale_frequencies(key_root, scale_type, engine.note_frequencies)
    
    # Create song structure
    structure = create_song_structure(duration, bpm, genre_analysis['type'])
    
    # Initialize audio tracks
    sample_rate = 44100
    total_samples = int(duration * sample_rate)
    
    # Multi-track mixing
    kick_track = np.zeros(total_samples)
    snare_track = np.zeros(total_samples)
    hihat_track = np.zeros(total_samples)
    bass_track = np.zeros(total_samples)
    chord_track = np.zeros(total_samples)
    lead_track = np.zeros(total_samples)
    pad_track = np.zeros(total_samples)
    
    current_sample = 0
    
    for section in structure:
        if current_sample >= total_samples:
            break
            
        section_samples = min(int(section['duration'] * sample_rate), total_samples - current_sample)
        
        # Generate rhythm section
        kick_pattern, snare_pattern, hihat_pattern = get_drum_patterns(genre_analysis['type'], section['name'])
        
        # Generate musical elements for this section
        generate_section_audio(
            section, genre_analysis, scale_notes, bpm, current_sample, section_samples,
            kick_track, snare_track, hihat_track, bass_track, chord_track, lead_track, pad_track,
            synth, drums, kick_pattern, snare_pattern, hihat_pattern, mood
        )
        
        current_sample += section_samples
    
    # Mix all tracks with proper levels and effects
    final_mix = mix_tracks(
        kick_track, snare_track, hihat_track, bass_track, 
        chord_track, lead_track, pad_track, genre_analysis, mood, effects
    )
    
    # Master processing
    final_mix = master_audio(final_mix, genre_analysis, mood, effects)
    
    # Convert to 16-bit integer
    final_mix = np.clip(final_mix, -0.95, 0.95)
    audio_16bit = (final_mix * 32767).astype(np.int16)
    
    return audio_16bit, sample_rate

def save_wav_file(audio_data, sample_rate, filename):
    """Save audio data as WAV file"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def generate_lyrics(prompt, genre, mood):
    """Generate Beat Addicts style lyrics based on vibe"""
    
    # Genre-specific styles
    genre_styles = {
        'pop': ["verse", "hook", "verse", "hook", "bridge", "hook"],
        'rock': ["verse", "hook", "verse", "hook", "breakdown", "hook"],
        'jazz': ["verse", "verse", "bridge", "verse"],
        'electronic': ["intro", "build", "drop", "break", "drop"],
        'country': ["verse", "hook", "verse", "hook", "bridge", "hook"]
    }
    
    # Mood-based Beat Addicts vocabulary
    mood_words = {
        'happy': ['vibes', 'energy', 'rhythm', 'flow', 'beat', 'pulse'],
        'sad': ['feels', 'deep', 'soul', 'heart', 'echo', 'fade'],
        'energetic': ['fire', 'power', 'rush', 'drive', 'electric', 'wild'],
        'calm': ['smooth', 'chill', 'mellow', 'soft', 'float', 'drift'],
        'romantic': ['warmth', 'touch', 'close', 'sync', 'harmony', 'groove']
    }
    
    structure = genre_styles.get(genre, genre_styles['pop'])
    words = mood_words.get(mood, mood_words['happy'])
    
    # Create Beat Addicts themed lyrics
    lyrics_parts = []
    for section in structure:
        if section == "verse":
            lyrics_parts.append(f"[Verse]\n{prompt} got that {words[0]} in the air\n{words[1]} and {words[2]} everywhere\nEvery beat drops so {words[3]}\nThis {genre} {mood} addiction's real")
        elif section == "hook" or section == "chorus":
            lyrics_parts.append(f"[Hook]\n{words[4]} {words[5]} through the night\n{prompt} makes the speakers ignite\nDropping this {genre} frequency\nBeat Addicts, this is our destiny")
        elif section == "bridge":
            lyrics_parts.append(f"[Bridge]\nWhen the {words[0]} start to fade\n{words[1]} and {words[2]} never trade\nThis {prompt} in our DNA\nA {mood} {genre} beat that's here to stay")
        elif section in ["breakdown", "drop", "break", "intro", "build"]:
            lyrics_parts.append(f"[{section.title()}]\n(Beat drops hard)")
    
    return "\n\n".join(lyrics_parts)

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
        filename = f"beataddicts_beat_{timestamp}"
        
        # Generate audio
        print(f"Generating {duration}s beat for {genre} {mood} vibe...")
        audio_data, sample_rate = generate_audio_wave(duration, genre, mood, prompt)
        
        # Save full song (2 minutes max for export)
        export_duration = min(duration, 300)  # 5 minutes max
        export_samples = int(export_duration * sample_rate)
        export_audio = audio_data[:export_samples]
        
        full_path = f"static/generated/{filename}.wav"
        save_wav_file(export_audio, sample_rate, full_path)
        
        # Generate 30-second preview
        preview_samples = min(30 * sample_rate, len(audio_data))
        preview_audio = audio_data[:preview_samples]
        preview_path = f"static/previews/{filename}_preview.wav"
        save_wav_file(preview_audio, sample_rate, preview_path)
        
        # Generate lyrics
        lyrics = generate_lyrics(prompt, genre, mood)
        
        # Calculate file size
        file_size_mb = round(os.path.getsize(full_path) / (1024 * 1024), 1)
        
        result = {
            'title': f"{prompt.title()} - {genre.title()} {mood.title()}",
            'artist': 'Beat Addicts',
            'genre': genre,
            'mood': mood,
            'duration': export_duration,
            'lyrics': lyrics,
            'filename': f"{filename}.wav",
            'file_size': f"{file_size_mb} MB",
            'preview_url': url_for('static', filename=f'previews/{filename}_preview.wav'),
            'download_url': url_for('download_beat', filename=f"{filename}.wav"),
            'created_at': datetime.now().isoformat()
        }
        
        print(f"Beat dropped successfully: {filename}.wav ({file_size_mb}MB)")
        
        return jsonify({
            'success': True,
            'result': result,
            'message': 'Beat dropped successfully! Your addiction begins...'
        })
        
    except Exception as e:
        print(f"Error dropping beat: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download/<filename>')
def download_beat(filename):
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
    """List all dropped beats"""
    try:
        beats = []
        generated_dir = "static/generated"
        if os.path.exists(generated_dir):
            for filename in os.listdir(generated_dir):
                if filename.endswith('.wav'):
                    file_path = os.path.join(generated_dir, filename)
                    file_size = round(os.path.getsize(file_path) / (1024 * 1024), 1)
                    beats.append({
                        'filename': filename,
                        'size': f"{file_size} MB",
                        'download_url': url_for('download_beat', filename=filename)
                    })
        
        return jsonify({
            'success': True,
            'beats': beats,
            'total': len(beats)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def analyze_genre_text(genre_text):
    """Advanced genre analysis with detailed musical characteristics"""
    
    # Electronic/EDM analysis
    if any(word in genre_text for word in ['electronic', 'edm', 'techno', 'house', 'trance', 'dubstep', 'synth']):
        subgenre_details = {
            'house': {'key': 'A3', 'scale': 'minor', 'instruments': ['saw_bass', 'square_lead', 'house_kick']},
            'techno': {'key': 'Bb3', 'scale': 'minor', 'instruments': ['acid_bass', 'tech_lead', 'industrial_kick']},
            'trance': {'key': 'G3', 'scale': 'minor', 'instruments': ['super_saw', 'pluck', 'trance_kick']},
            'dubstep': {'key': 'F#3', 'scale': 'minor', 'instruments': ['wobble_bass', 'scream_lead', 'trap_kick']},
        }
        
        for subgenre, details in subgenre_details.items():
            if subgenre in genre_text:
                return {'type': 'electronic', 'subtype': subgenre, **details}
        
        return {'type': 'electronic', 'subtype': 'general', 'key': 'A3', 'scale': 'minor', 'instruments': ['synth_bass', 'lead', 'electronic_kick']}
    
    # Hip-hop analysis
    elif any(word in genre_text for word in ['hip', 'hop', 'rap', 'trap', 'drill', '808', 'boom', 'bap']):
        if any(word in genre_text for word in ['trap', 'drill']):
            return {'type': 'hiphop', 'subtype': 'trap', 'key': 'F3', 'scale': 'minor', 'instruments': ['808_bass', 'trap_lead', 'trap_kick']}
        elif 'boom' in genre_text or 'bap' in genre_text:
            return {'type': 'hiphop', 'subtype': 'boom_bap', 'key': 'E3', 'scale': 'minor', 'instruments': ['sub_bass', 'jazz_sample', 'vintage_kick']}
        else:
            return {'type': 'hiphop', 'subtype': 'general', 'key': 'D3', 'scale': 'minor', 'instruments': ['hip_bass', 'vocal_chop', 'hip_kick']}
    
    # Rock analysis
    elif any(word in genre_text for word in ['rock', 'metal', 'punk', 'grunge', 'alternative', 'guitar']):
        if any(word in genre_text for word in ['metal', 'heavy']):
            return {'type': 'rock', 'subtype': 'metal', 'key': 'E2', 'scale': 'minor', 'instruments': ['distorted_guitar', 'metal_bass', 'metal_kick']}
        elif 'punk' in genre_text:
            return {'type': 'rock', 'subtype': 'punk', 'key': 'A2', 'scale': 'minor', 'instruments': ['punk_guitar', 'punk_bass', 'punk_kick']}
        else:
            return {'type': 'rock', 'subtype': 'general', 'key': 'G2', 'scale': 'minor', 'instruments': ['electric_guitar', 'rock_bass', 'rock_kick']}
    
    # Jazz analysis
    elif any(word in genre_text for word in ['jazz', 'blues', 'swing', 'bebop', 'fusion', 'smooth']):
        return {'type': 'jazz', 'subtype': 'general', 'key': 'F3', 'scale': 'dorian', 'instruments': ['jazz_bass', 'jazz_piano', 'jazz_kick']}
    
    # Default to pop
    else:
        return {'type': 'pop', 'subtype': 'general', 'key': 'C4', 'scale': 'major', 'instruments': ['pop_bass', 'pop_synth', 'pop_kick']}

def calculate_bpm(genre_type, mood):
    """Calculate appropriate BPM based on genre and mood"""
    base_bpm = {
        'electronic': 128,
        'hiphop': 85,
        'rock': 120,
        'jazz': 110,
        'pop': 120
    }
    
    mood_modifiers = {
        'happy': 1.1,
        'energetic': 1.3,
        'sad': 0.7,
        'calm': 0.8,
        'romantic': 0.9
    }
    
    bpm = base_bpm.get(genre_type, 120) * mood_modifiers.get(mood, 1.0)
    return int(np.clip(bpm, 60, 180))

def generate_scale_frequencies(key_root, scale_type, note_frequencies):
    """Generate frequencies for musical scale"""
    
    # Scale patterns (semitone intervals)
    scales = {
        'major': [0, 2, 4, 5, 7, 9, 11],
        'minor': [0, 2, 3, 5, 7, 8, 10],
        'dorian': [0, 2, 3, 5, 7, 9, 10],
        'mixolydian': [0, 2, 4, 5, 7, 9, 10],
        'blues': [0, 3, 5, 6, 7, 10],
        'pentatonic': [0, 2, 4, 7, 9]
    }
    
    pattern = scales.get(scale_type, scales['major'])
    base_freq = note_frequencies.get(key_root, 261.63)  # Default to C4
    
    scale_freqs = []
    for interval in pattern:
        freq = base_freq * (2 ** (interval / 12.0))
        scale_freqs.append(freq)
    
    return scale_freqs

def create_song_structure(duration, bpm, genre_type):
    """Create dynamic song structure based on duration and genre"""
    beat_duration = 60.0 / bpm
    bar_duration = beat_duration * 4
    
    if genre_type == 'electronic':
        # Electronic structure: Intro -> Build -> Drop -> Break -> Build -> Drop -> Outro
        structure = [
            {'name': 'intro', 'duration': bar_duration * 4, 'intensity': 0.3},
            {'name': 'build', 'duration': bar_duration * 4, 'intensity': 0.6},
            {'name': 'drop', 'duration': bar_duration * 8, 'intensity': 1.0},
            {'name': 'break', 'duration': bar_duration * 4, 'intensity': 0.4},
            {'name': 'build', 'duration': bar_duration * 4, 'intensity': 0.7},
            {'name': 'drop', 'duration': bar_duration * 8, 'intensity': 1.0},
            {'name': 'outro', 'duration': bar_duration * 4, 'intensity': 0.2}
        ]
    elif genre_type == 'hiphop':
        # Hip-hop structure: Intro -> Verse -> Hook -> Verse -> Hook -> Bridge -> Hook -> Outro
        structure = [
            {'name': 'intro', 'duration': bar_duration * 2, 'intensity': 0.4},
            {'name': 'verse', 'duration': bar_duration * 8, 'intensity': 0.7},
            {'name': 'hook', 'duration': bar_duration * 4, 'intensity': 1.0},
            {'name': 'verse', 'duration': bar_duration * 8, 'intensity': 0.7},
            {'name': 'hook', 'duration': bar_duration * 4, 'intensity': 1.0},
            {'name': 'bridge', 'duration': bar_duration * 4, 'intensity': 0.6},
            {'name': 'hook', 'duration': bar_duration * 4, 'intensity': 1.0},
            {'name': 'outro', 'duration': bar_duration * 2, 'intensity': 0.3}
        ]
    else:
        # Standard pop/rock structure
        structure = [
            {'name': 'intro', 'duration': bar_duration * 2, 'intensity': 0.4},
            {'name': 'verse', 'duration': bar_duration * 4, 'intensity': 0.6},
            {'name': 'chorus', 'duration': bar_duration * 4, 'intensity': 1.0},
            {'name': 'verse', 'duration': bar_duration * 4, 'intensity': 0.6},
            {'name': 'chorus', 'duration': bar_duration * 4, 'intensity': 1.0},
            {'name': 'bridge', 'duration': bar_duration * 4, 'intensity': 0.7},
            {'name': 'chorus', 'duration': bar_duration * 4, 'intensity': 1.0},
            {'name': 'outro', 'duration': bar_duration * 2, 'intensity': 0.3}
        ]
    
    # Adjust structure to fit duration
    total_duration = sum(s['duration'] for s in structure)
    if total_duration > duration:
        # Scale down proportionally
        scale_factor = duration / total_duration
        for section in structure:
            section['duration'] *= scale_factor
    
    return structure

def get_drum_patterns(genre_type, section_name):
    """Get drum patterns based on genre and section"""
    
    if genre_type == 'electronic':
        if section_name in ['drop', 'hook']:
            kick_pattern = [1, 0, 1, 0, 1, 0, 1, 0]  # Four on the floor
            snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0]  # Snare on 2 and 4
            hihat_pattern = [1, 1, 1, 1, 1, 1, 1, 1]  # Constant hi-hats
        else:
            kick_pattern = [1, 0, 0, 0, 1, 0, 0, 0]
            snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0]
            hihat_pattern = [0, 1, 0, 1, 0, 1, 0, 1]
    
    elif genre_type == 'hiphop':
        kick_pattern = [1, 0, 0, 0, 0, 0, 1, 0]  # Hip-hop kick pattern
        snare_pattern = [0, 0, 0, 0, 1, 0, 0, 0]  # Snare on 3
        hihat_pattern = [1, 0, 1, 1, 0, 1, 1, 0]  # Syncopated hi-hats
    
    elif genre_type == 'rock':
        kick_pattern = [1, 0, 0, 0, 1, 0, 0, 0]  # Basic rock kick
        snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0]  # Backbeat
        hihat_pattern = [1, 1, 1, 1, 1, 1, 1, 1]  # Eighth note hi-hats
    
    else:  # Pop default
        kick_pattern = [1, 0, 0, 0, 1, 0, 0, 0]
        snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0]
        hihat_pattern = [1, 0, 1, 0, 1, 0, 1, 0]
    
    return kick_pattern, snare_pattern, hihat_pattern

def generate_section_audio(section, genre_analysis, scale_notes, bpm, current_sample, section_samples,
                         kick_track, snare_track, hihat_track, bass_track, chord_track, lead_track, pad_track,
                         synth, drums, kick_pattern, snare_pattern, hihat_pattern, mood):
    """Generate audio for a specific song section"""
    
    sample_rate = 44100
    beat_duration = 60.0 / bpm
    beats_per_section = int(section['duration'] / beat_duration)
    
    # Generate chord progression
    progressions = get_chord_progressions(genre_analysis['type'])
    chord_progression = progressions.get(section['name'], progressions['default'])
    
    # Generate drums
    for beat in range(beats_per_section):
        beat_sample = current_sample + int(beat * beat_duration * sample_rate)
        
        if beat_sample >= len(kick_track):
            break
        
        pattern_index = beat % len(kick_pattern)
        
        # Kick drum
        if kick_pattern[pattern_index]:
            kick_audio = drums.generate_kick(0.5)
            end_sample = min(beat_sample + len(kick_audio), len(kick_track))
            kick_track[beat_sample:end_sample] += kick_audio[:end_sample - beat_sample] * section['intensity']
        
        # Snare drum
        if snare_pattern[pattern_index]:
            snare_audio = drums.generate_snare(0.3)
            end_sample = min(beat_sample + len(snare_audio), len(snare_track))
            snare_track[beat_sample:end_sample] += snare_audio[:end_sample - beat_sample] * section['intensity']
        
        # Hi-hat
        if hihat_pattern[pattern_index]:
            hihat_audio = drums.generate_hihat(0.1, closed=True)
            end_sample = min(beat_sample + len(hihat_audio), len(hihat_track))
            hihat_track[beat_sample:end_sample] += hihat_audio[:end_sample - beat_sample] * section['intensity'] * 0.7
    
    # Generate bass line
    generate_bass_line(bass_track, current_sample, section_samples, scale_notes, chord_progression, 
                      section['duration'], bpm, genre_analysis, synth, section['intensity'])
    
    # Generate chord progression
    if section['name'] not in ['intro', 'outro']:
        generate_chord_track(chord_track, current_sample, section_samples, scale_notes, chord_progression,
                           section['duration'], bpm, genre_analysis, synth, section['intensity'])
    
    # Generate lead melody
    if section['name'] in ['chorus', 'hook', 'drop']:
        generate_lead_melody(lead_track, current_sample, section_samples, scale_notes, chord_progression,
                           section['duration'], bpm, genre_analysis, synth, section['intensity'], mood)
    
    # Generate pad (ambient layer)
    if section['name'] in ['verse', 'bridge', 'build']:
        generate_pad_layer(pad_track, current_sample, section_samples, scale_notes, chord_progression,
                          section['duration'], bpm, genre_analysis, synth, section['intensity'] * 0.6)

def get_chord_progressions(genre_type):
    """Get chord progressions for different genres"""
    
    progressions = {
        'electronic': {
            'intro': [0, 6],
            'build': [0, 4, 5, 6],
            'drop': [0, 6, 4, 5],
            'break': [3, 6],
            'outro': [6, 0],
            'default': [0, 6, 4, 5]
        },
        'hiphop': {
            'intro': [0],
            'verse': [0, 6, 3, 4],
            'hook': [0, 4, 5, 3],
            'bridge': [3, 4, 0, 5],
            'outro': [0],
            'default': [0, 6, 3, 4]
        },
        'rock': {
            'intro': [0, 5],
            'verse': [0, 5, 3, 4],
            'chorus': [0, 4, 5, 3],
            'bridge': [3, 4, 5, 0],
            'outro': [5, 0],
            'default': [0, 5, 3, 4]
        },
        'pop': {
            'intro': [0, 5],
            'verse': [0, 5, 3, 4],
            'chorus': [0, 4, 5, 3],
            'bridge': [3, 4, 5, 0],
            'outro': [5, 0],
            'default': [0, 5, 3, 4]
        }
    }
    
    return progressions.get(genre_type, progressions['pop'])

def generate_bass_line(bass_track, start_sample, section_samples, scale_notes, chord_progression, 
                      section_duration, bpm, genre_analysis, synth, intensity):
    """Generate bass line for the section"""
    
    sample_rate = 44100
    beat_duration = 60.0 / bpm
    chord_duration = section_duration / len(chord_progression)
    
    for i, chord_degree in enumerate(chord_progression):
        chord_start_time = i * chord_duration
        chord_start_sample = start_sample + int(chord_start_time * sample_rate)
        chord_samples = int(chord_duration * sample_rate)
        
        if chord_start_sample >= len(bass_track):
            break
        
        # Bass note (root of chord, one octave down)
        bass_freq = scale_notes[chord_degree % len(scale_notes)] / 2
        
        if genre_analysis['type'] == 'hiphop' and '808' in genre_analysis.get('instruments', []):
            # Use 808-style bass
            drums_instance = DrumMachine()
            bass_audio = drums_instance.generate_808(bass_freq, chord_duration)
        else:
            # Use synthesized bass
            waveform = 'sawtooth' if genre_analysis['type'] == 'electronic' else 'sine'
            bass_audio = synth.generate_waveform(bass_freq, chord_duration, waveform, amplitude=0.8)
        
        end_sample = min(chord_start_sample + len(bass_audio), len(bass_track))
        bass_track[chord_start_sample:end_sample] += bass_audio[:end_sample - chord_start_sample] * intensity

def generate_chord_track(chord_track, start_sample, section_samples, scale_notes, chord_progression,
                        section_duration, bpm, genre_analysis, synth, intensity):
    """Generate chord progression"""
    
    sample_rate = 44100
    chord_duration = section_duration / len(chord_progression)
    
    for i, chord_degree in enumerate(chord_progression):
        chord_start_time = i * chord_duration
        chord_start_sample = start_sample + int(chord_start_time * sample_rate)
        
        if chord_start_sample >= len(chord_track):
            break
        
        # Build triad (root, third, fifth)
        root_freq = scale_notes[chord_degree % len(scale_notes)]
        third_freq = scale_notes[(chord_degree + 2) % len(scale_notes)]
        fifth_freq = scale_notes[(chord_degree + 4) % len(scale_notes)]
        
        # Choose waveform based on genre
        if genre_analysis['type'] == 'electronic':
            waveform = 'square'
            amplitude = 0.4
        elif genre_analysis['type'] == 'rock':
            waveform = 'sawtooth'
            amplitude = 0.5
        else:
            waveform = 'sine'
            amplitude = 0.4
        
        # Generate each chord tone
        chord_audio = np.zeros(int(chord_duration * sample_rate))
        
        for freq, amp_mult in [(root_freq, 1.0), (third_freq, 0.8), (fifth_freq, 0.6)]:
            tone = synth.generate_waveform(freq, chord_duration, waveform, amplitude * amp_mult)
            chord_audio += tone[:len(chord_audio)]
        
        end_sample = min(chord_start_sample + len(chord_audio), len(chord_track))
        chord_track[chord_start_sample:end_sample] += chord_audio[:end_sample - chord_start_sample] * intensity

def generate_lead_melody(lead_track, start_sample, section_samples, scale_notes, chord_progression,
                        section_duration, bpm, genre_analysis, synth, intensity, mood):
    """Generate lead melody"""
    
    sample_rate = 44100
    beat_duration = 60.0 / bpm
    note_duration = beat_duration / 2  # Eighth notes
    
    num_notes = int(section_duration / note_duration)
    
    # Create melody based on mood and genre
    melody_style = get_melody_style(genre_analysis['type'], mood)
    
    for i in range(num_notes):
        note_start_time = i * note_duration
        note_start_sample = start_sample + int(note_start_time * sample_rate)
        
        if note_start_sample >= len(lead_track):
            break
        
        # Choose note from scale with some musical logic
        chord_index = int(i / (len(chord_progression) * 2)) % len(chord_progression)
        chord_degree = chord_progression[chord_index]
        
        # Create melodic movement
        if melody_style == 'arpeggiated':
            note_choices = [chord_degree, (chord_degree + 2) % len(scale_notes), (chord_degree + 4) % len(scale_notes)]
            note_index = note_choices[i % 3]
        elif melody_style == 'scalar':
            direction = 1 if i % 8 < 4 else -1
            note_index = (chord_degree + direction * (i % 4)) % len(scale_notes)
        else:  # 'rhythmic'
            note_index = chord_degree if i % 2 == 0 else (chord_degree + 2) % len(scale_notes)
        
        melody_freq = scale_notes[note_index] * 2  # One octave up
        
        # Choose lead sound based on genre
        if genre_analysis['type'] == 'electronic':
            waveform = 'sawtooth'
            amplitude = 0.6
        elif genre_analysis['type'] == 'rock':
            waveform = 'square'
            amplitude = 0.7
        else:
            waveform = 'triangle'
            amplitude = 0.5
        
        lead_audio = synth.generate_waveform(melody_freq, note_duration, waveform, amplitude)
        
        end_sample = min(note_start_sample + len(lead_audio), len(lead_track))
        lead_track[note_start_sample:end_sample] += lead_audio[:end_sample - note_start_sample] * intensity

def generate_pad_layer(pad_track, start_sample, section_samples, scale_notes, chord_progression,
                      section_duration, bpm, genre_analysis, synth, intensity):
    """Generate ambient pad layer"""
    
    sample_rate = 44100
    chord_duration = section_duration / len(chord_progression)
    
    for i, chord_degree in enumerate(chord_progression):
        chord_start_time = i * chord_duration
        chord_start_sample = start_sample + int(chord_start_time * sample_rate)
        
        if chord_start_sample >= len(pad_track):
            break
        
        # Create lush pad chords with extensions
        frequencies = [
            scale_notes[chord_degree % len(scale_notes)],
            scale_notes[(chord_degree + 2) % len(scale_notes)],
            scale_notes[(chord_degree + 4) % len(scale_notes)],
            scale_notes[(chord_degree + 6) % len(scale_notes)],  # 7th
        ]
        
        pad_audio = np.zeros(int(chord_duration * sample_rate))
        
        for j, freq in enumerate(frequencies):
            amplitude = 0.3 / (j + 1)  # Decreasing amplitude for higher voices
            tone = synth.generate_waveform(freq, chord_duration, 'sine', amplitude)
            pad_audio += tone[:len(pad_audio)]
        
        end_sample = min(chord_start_sample + len(pad_audio), len(pad_track))
        pad_track[chord_start_sample:end_sample] += pad_audio[:end_sample - chord_start_sample] * intensity

def get_melody_style(genre_type, mood):
    """Determine melody style based on genre and mood"""
    
    if genre_type == 'electronic':
        return 'arpeggiated' if mood in ['energetic', 'happy'] else 'rhythmic'
    elif genre_type == 'hiphop':
        return 'rhythmic'
    elif genre_type == 'rock':
        return 'scalar' if mood == 'energetic' else 'rhythmic'
    else:
        return 'scalar' if mood in ['happy', 'romantic'] else 'arpeggiated'

def mix_tracks(kick_track, snare_track, hihat_track, bass_track, chord_track, lead_track, pad_track, 
              genre_analysis, mood, effects):
    """Mix all tracks with proper levels and effects"""
    
    # Set mix levels based on genre
    if genre_analysis['type'] == 'electronic':
        levels = {'kick': 0.8, 'snare': 0.6, 'hihat': 0.4, 'bass': 0.7, 'chord': 0.5, 'lead': 0.6, 'pad': 0.3}
    elif genre_analysis['type'] == 'hiphop':
        levels = {'kick': 0.9, 'snare': 0.7, 'hihat': 0.5, 'bass': 0.8, 'chord': 0.4, 'lead': 0.6, 'pad': 0.2}
    elif genre_analysis['type'] == 'rock':
        levels = {'kick': 0.7, 'snare': 0.8, 'hihat': 0.5, 'bass': 0.6, 'chord': 0.7, 'lead': 0.8, 'pad': 0.3}
    else:  # pop
        levels = {'kick': 0.6, 'snare': 0.7, 'hihat': 0.4, 'bass': 0.6, 'chord': 0.6, 'lead': 0.7, 'pad': 0.4}
    
    # Apply effects to individual tracks
    if mood in ['sad', 'romantic']:
        chord_track = effects.reverb(chord_track, room_size=0.7, wet=0.4)
        lead_track = effects.reverb(lead_track, room_size=0.5, wet=0.3)
        pad_track = effects.reverb(pad_track, room_size=0.8, wet=0.5)
    
    if mood == 'energetic' and genre_analysis['type'] in ['rock', 'electronic']:
        lead_track = effects.distortion(lead_track, drive=1.5, mix=0.3)
        chord_track = effects.distortion(chord_track, drive=1.2, mix=0.2)
    
    if genre_analysis['type'] == 'electronic':
        lead_track = effects.delay(lead_track, delay_time=0.25, feedback=0.3, mix=0.2)
    
    # Mix all tracks
    final_mix = (kick_track * levels['kick'] + 
                snare_track * levels['snare'] + 
                hihat_track * levels['hihat'] + 
                bass_track * levels['bass'] + 
                chord_track * levels['chord'] + 
                lead_track * levels['lead'] + 
                pad_track * levels['pad'])
    
    return final_mix

def master_audio(audio, genre_analysis, mood, effects):
    """Apply mastering effects to final mix"""
    
    # Compression (simple)
    threshold = 0.7
    ratio = 3.0
    compressed = np.where(np.abs(audio) > threshold, 
                         threshold + (np.abs(audio) - threshold) / ratio * np.sign(audio),
                         audio)
    
    # EQ simulation (simple high and low shelf)
    # High shelf for brightness
    if genre_analysis['type'] in ['electronic', 'pop']:
        b, a = signal.butter(2, 8000 / (44100 / 2), 'high')
        high_freq = signal.filtfilt(b, a, compressed)
        compressed = compressed + high_freq * 0.1
    
    # Low shelf for warmth
    if mood in ['romantic', 'calm']:
        b, a = signal.butter(2, 200 / (44100 / 2), 'low')
        low_freq = signal.filtfilt(b, a, compressed)
        compressed = compressed + low_freq * 0.05
    
    # Final limiter
    limited = np.clip(compressed, -0.95, 0.95)
    
    # Normalize to desired level
    peak = np.max(np.abs(limited))
    if peak > 0:
        limited = limited * (0.9 / peak)
    
    return limited

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
