from flask import Flask, jsonify, render_template, request, send_file
from generate_song import generate_song, generate_lyrics_with_ai
import os
import glob
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main UI"""
    return render_template('index.html')

@app.route('/generate_song', methods=['POST'])
def generate():
    """Generate a complete song with AI lyrics and audio"""
    try:
        data = request.get_json() or {}
        theme = data.get('theme', 'love')
        genre = data.get('genre', 'pop')
        mood = data.get('mood', 'happy')
        duration = data.get('duration', 30)
        
        result = generate_song(theme=theme, genre=genre, mood=mood, duration=duration)
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/generate_lyrics', methods=['POST'])
def generate_lyrics():
    """Generate AI-powered lyrics only"""
    try:
        data = request.get_json() or {}
        theme = data.get('theme', 'love')
        style = data.get('style', 'modern')
        
        lyrics = generate_lyrics_with_ai(theme=theme, style=style)
        return jsonify({
            'success': True,
            'lyrics': lyrics,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/downloads')
def list_downloads():
    """List all generated songs"""
    try:
        songs_dir = 'generated_songs'
        if not os.path.exists(songs_dir):
            return jsonify({'songs': []})
        
        songs = []
        for file in glob.glob(os.path.join(songs_dir, '*.json')):
            with open(file, 'r') as f:
                song_data = json.load(f)
                song_data['filename'] = os.path.basename(file).replace('.json', '')
                songs.append(song_data)
        
        # Sort by creation time, newest first
        songs.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return jsonify({'songs': songs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download a generated audio file"""
    try:
        audio_file = os.path.join('generated_songs', f'{filename}.wav')
        if os.path.exists(audio_file):
            return send_file(audio_file, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_downloads', methods=['POST'])
def clear_downloads():
    """Clear all generated songs"""
    try:
        songs_dir = 'generated_songs'
        if os.path.exists(songs_dir):
            for file in glob.glob(os.path.join(songs_dir, '*')):
                os.remove(file)
        return jsonify({'success': True, 'message': 'All downloads cleared'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
