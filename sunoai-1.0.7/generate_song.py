import numpy as np
import librosa
import os
import json
import uuid
from datetime import datetime
from ai_lyrics_generator import AILyricsGenerator

# Initialize the AI lyrics generator
lyrics_generator = AILyricsGenerator()

def generate_audio_file(duration=30, genre='pop', mood='happy'):
    """Generate a realistic audio file with varying characteristics"""
    sample_rate = 22050
    total_samples = int(duration * sample_rate)
    
    # Generate base frequency based on genre
    base_freq = {
        'pop': 440,      # A4
        'rock': 330,     # E4
        'jazz': 523,     # C5
        'classical': 262, # C4
        'electronic': 880, # A5
        'blues': 247,    # B3
        'country': 349,  # F4
    }.get(genre.lower(), 440)
    
    # Create time array
    t = np.linspace(0, duration, total_samples)
    
    # Generate complex waveform
    audio = np.zeros(total_samples)
    
    # Main melody line
    melody_freq = base_freq * (1 + 0.2 * np.sin(2 * np.pi * 0.5 * t))  # Vibrato
    audio += 0.4 * np.sin(2 * np.pi * melody_freq * t)
    
    # Harmony (fifth)
    harmony_freq = base_freq * 1.5
    audio += 0.2 * np.sin(2 * np.pi * harmony_freq * t)
    
    # Bass line
    bass_freq = base_freq * 0.5
    audio += 0.3 * np.sin(2 * np.pi * bass_freq * t)
    
    # Add rhythmic elements
    beat_freq = 2.0  # 120 BPM
    rhythm = np.sin(2 * np.pi * beat_freq * t)
    audio += 0.1 * rhythm * np.sin(2 * np.pi * base_freq * 2 * t)
    
    # Apply mood modifications
    if mood.lower() == 'sad':
        # Lower pitch, slower rhythm
        audio = np.interp(np.linspace(0, len(audio), int(len(audio) * 0.8)), 
                         np.arange(len(audio)), audio)
        audio = np.pad(audio, (0, total_samples - len(audio)), 'constant')
    elif mood.lower() == 'energetic':
        # Add more harmonics and faster rhythm
        audio += 0.15 * np.sin(2 * np.pi * base_freq * 3 * t)
        audio += 0.1 * np.sin(2 * np.pi * base_freq * 4 * t)
    
    # Add some realistic noise and dynamics
    noise = np.random.normal(0, 0.02, total_samples)
    audio += noise
    
    # Apply envelope (fade in/out)
    fade_samples = int(0.1 * sample_rate)  # 0.1 second fade
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    
    audio[:fade_samples] *= fade_in
    audio[-fade_samples:] *= fade_out
    
    # Normalize
    audio = audio / np.max(np.abs(audio)) * 0.8
    
    return audio, sample_rate

def generate_lyrics_with_ai(theme='love', style='modern'):
    """Generate AI-powered lyrics"""
    try:
        result = lyrics_generator.generate_lyrics(theme=theme, mood=style)
        return result.get('lyrics', generate_fallback_lyrics(theme, style))
    except Exception as e:
        print(f"AI lyrics generation failed: {e}")
        # Fallback to template-based lyrics
        return generate_fallback_lyrics(theme, style)

def generate_fallback_lyrics(theme='love', style='modern'):
    """Fallback lyrics generator"""
    templates = {
        'love': [
            "In the moonlight, I see your face",
            "Dancing through the starlit space",
            "Every heartbeat calls your name",
            "In this love, we're both the same"
        ],
        'adventure': [
            "Beyond the mountains, past the sea",
            "There's a world that's calling me",
            "With courage strong and spirit free",
            "I'll chase my dreams eternally"
        ],
        'friendship': [
            "Through the laughter and the tears",
            "You've been with me through the years",
            "In good times and when skies are gray",
            "True friendship lights the way"
        ],
        'hope': [
            "When the darkness seems too deep",
            "And the mountain's way too steep",
            "There's a light that shines so bright",
            "Hope will guide us through the night"
        ]
    }
    
    base_lyrics = templates.get(theme.lower(), templates['love'])
    
    # Add chorus
    chorus = [
        "This is our moment, this is our time",
        "Every reason, every rhyme",
        "In this song, our hearts align",
        "Forever yours, forever mine"
    ]
    
    # Combine verse and chorus
    full_lyrics = base_lyrics + [""] + chorus + [""] + base_lyrics + [""] + chorus
    
    return "\n".join(full_lyrics)

def generate_song(theme='love', genre='pop', mood='happy', duration=30):
    """Generate a complete song with AI lyrics and audio"""
    try:
        # Generate unique filename
        song_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"song_{timestamp}_{song_id}"
        
        # Generate AI lyrics
        lyrics = generate_lyrics_with_ai(theme=theme, style=genre)
        
        # Generate audio
        audio_data, sample_rate = generate_audio_file(duration=duration, genre=genre, mood=mood)
        
        # Save audio file
        audio_path = os.path.join('generated_songs', f'{filename}.wav')
        os.makedirs('generated_songs', exist_ok=True)
        
        # Convert to int16 for WAV format
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        # Save using soundfile (librosa's preferred method)
        import soundfile as sf
        sf.write(audio_path, audio_data, sample_rate)
        
        # Create metadata
        metadata = {
            'id': song_id,
            'filename': filename,
            'title': f"{theme.title()} Song",
            'theme': theme,
            'genre': genre,
            'mood': mood,
            'duration': duration,
            'lyrics': lyrics,
            'created_at': datetime.now().isoformat(),
            'audio_file': f'{filename}.wav',
            'sample_rate': sample_rate
        }
        
        # Save metadata
        metadata_path = os.path.join('generated_songs', f'{filename}.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            'success': True,
            'song_id': song_id,
            'filename': filename,
            'metadata': metadata,
            'message': f'Song generated successfully: {metadata["title"]}'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Failed to generate song'
        }