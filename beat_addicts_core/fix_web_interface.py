#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Web Interface Syntax Fixer
Check and fix indentation errors in web_interface.py
"""

import ast
import os

def check_syntax():
    """Check web_interface.py for syntax errors"""
    print("🔍 BEAT ADDICTS - Checking web_interface.py syntax...")
    
    if not os.path.exists("web_interface.py"):
        print("❌ web_interface.py not found")
        return False
    
    try:
        with open("web_interface.py", "r") as f:
            content = f.read()
        
        # Try to parse the file
        ast.parse(content)
        print("✅ web_interface.py syntax is correct")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error found:")
        print(f"   Line {e.lineno}: {e.msg}")
        print(f"   Text: {e.text.strip() if e.text else 'Unknown'}")
        return False
    except Exception as e:
        print(f"❌ Error checking syntax: {e}")
        return False

def create_minimal_web_interface():
    """Create a minimal working web interface"""
    print("📝 Creating minimal BEAT ADDICTS web interface...")
    
    minimal_content = '''"""
🎵 BEAT ADDICTS - Minimal Web Interface
Professional Music Production AI v2.0
"""

import os
import sys
import time
import math
import random
import struct

try:
    from flask import Flask, render_template_string, jsonify, request, send_file, abort
except ImportError:
    print("❌ Flask not installed. Run: pip install flask")
    exit(1)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'beat_addicts_2024'

# Create directories
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static', 'generated')
DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), 'downloads')

for directory in [STATIC_DIR, DOWNLOADS_DIR]:
    os.makedirs(directory, exist_ok=True)

class SimpleAudioGenerator:
    def __init__(self):
        self.sample_rate = 44100
    
    def generate_simple_beat(self, bpm=140, bars=4):
        beat_duration = 60.0 / bpm
        total_duration = bars * 4 * beat_duration
        total_samples = int(self.sample_rate * total_duration)
        audio_buffer = [0] * (total_samples * 2)
        
        for bar in range(bars):
            for beat in range(4):
                beat_time = (bar * 4 + beat) * beat_duration
                beat_sample = int(beat_time * self.sample_rate) * 2
                
                if beat in [0, 2]:  # Kick
                    for i in range(4410):  # 0.1 second
                        if beat_sample + i < len(audio_buffer):
                            t = i / self.sample_rate
                            sample = int(math.sin(2 * math.pi * 60 * t) * math.exp(-t * 10) * 16000)
                            audio_buffer[beat_sample + i] = sample
                            if beat_sample + i + 1 < len(audio_buffer):
                                audio_buffer[beat_sample + i + 1] = sample
        
        return audio_buffer
    
    def export_wav(self, audio_data, filename):
        wav_header = struct.pack('<4sI4s4sIHHIIHH4sI',
            b'RIFF', 36 + len(audio_data) * 2, b'WAVE', b'fmt ', 16, 1, 2,
            self.sample_rate, self.sample_rate * 2 * 2, 4, 16, b'data', len(audio_data) * 2)
        
        with open(filename, 'wb') as f:
            f.write(wav_header)
            for sample in audio_data:
                f.write(struct.pack('<h', sample))

audio_gen = SimpleAudioGenerator()

@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>🔥 BEAT ADDICTS Studio 🔥</title>
    <style>
        body { font-family: Arial; background: #121212; color: white; text-align: center; padding: 50px; }
        h1 { color: #ff4081; font-size: 3em; }
        .btn { background: #ff4081; color: #121212; border: none; padding: 15px 30px; 
               border-radius: 25px; cursor: pointer; font-size: 1em; margin: 10px; }
        .controls { margin: 20px 0; }
        .controls input { margin: 0 10px; }
        audio { width: 100%; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>🔥 BEAT ADDICTS Studio 🔥</h1>
    <p>Professional Music Production AI v2.0</p>
    
    <div class="controls">
        <label>BPM: <input type="range" id="bpm" min="80" max="180" value="140"></label>
        <span id="bpm-value">140</span><br><br>
        <label>Bars: <input type="range" id="bars" min="2" max="8" value="4"></label>
        <span id="bars-value">4</span>
    </div>
    
    <button class="btn" onclick="generateBeat()" id="generate-btn">🎵 Generate Beat</button>
    
    <div id="result" style="display: none;">
        <audio id="audio-player" controls>
            <source id="audio-source" src="" type="audio/wav">
        </audio>
        <br>
        <button class="btn" onclick="downloadBeat()">⬇️ Download</button>
    </div>

    <script>
        let currentFile = null;
        
        document.getElementById('bpm').oninput = function() {
            document.getElementById('bpm-value').textContent = this.value;
        };
        
        document.getElementById('bars').oninput = function() {
            document.getElementById('bars-value').textContent = this.value;
        };
        
        function generateBeat() {
            const btn = document.getElementById('generate-btn');
            btn.disabled = true;
            btn.textContent = '🎵 Generating...';
            
            fetch('/api/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    bpm: parseInt(document.getElementById('bpm').value),
                    bars: parseInt(document.getElementById('bars').value)
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    currentFile = data.filename;
                    document.getElementById('audio-source').src = '/static/generated/' + data.filename;
                    document.getElementById('audio-player').load();
                    document.getElementById('result').style.display = 'block';
                }
                btn.disabled = false;
                btn.textContent = '🎵 Generate Beat';
            })
            .catch(error => {
                btn.disabled = false;
                btn.textContent = '🎵 Generate Beat';
                alert('Generation failed: ' + error);
            });
        }
        
        function downloadBeat() {
            if (currentFile) {
                window.location.href = '/download/' + currentFile;
            }
        }
    </script>
</body>
</html>
    """)

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        bpm = data.get('bpm', 140)
        bars = data.get('bars', 4)
        
        timestamp = int(time.time())
        filename = f"beat_{timestamp}.wav"
        filepath = os.path.join(STATIC_DIR, filename)
        
        audio_data = audio_gen.generate_simple_beat(bpm=bpm, bars=bars)
        audio_gen.export_wav(audio_data, filepath)
        
        download_path = os.path.join(DOWNLOADS_DIR, filename)
        audio_gen.export_wav(audio_data, download_path)
        
        return jsonify({'success': True, 'filename': filename})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    try:
        download_path = os.path.join(DOWNLOADS_DIR, filename)
        if os.path.exists(download_path):
            return send_file(download_path, as_attachment=True, download_name=filename)
        abort(404)
    except Exception:
        abort(500)

@app.route('/static/generated/<filename>')
def serve_audio(filename):
    try:
        filepath = os.path.join(STATIC_DIR, filename)
        if os.path.exists(filepath):
            return send_file(filepath)
        abort(404)
    except Exception:
        abort(500)

if __name__ == '__main__':
    print("🎵 BEAT ADDICTS Studio starting...")
    print("🔥 Minimal Professional Music Production AI 🔥")
    print("🌐 Access at: http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
'''
    
    with open("web_interface.py", "w") as f:
        f.write(minimal_content)
    
    print("✅ Created minimal web_interface.py")
    return True

def main():
    """Main syntax checker and fixer"""
    print("🔧 BEAT ADDICTS - Web Interface Syntax Fixer")
    print("=" * 50)
    
    if check_syntax():
        print("✅ No fixes needed - web interface is ready!")
        return True
    else:
        print("🔧 Creating clean web interface...")
        return create_minimal_web_interface()

if __name__ == "__main__":
    main()
