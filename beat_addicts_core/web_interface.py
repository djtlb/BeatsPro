# filepath: c:\Users\sally\Downloads\sunoai-1.0.7-rebuild\beat_addicts_core\web_interface.py
"""🎵 BEAT ADDICTS - Working Web Interface"""

try:
    from flask import Flask, render_template_string
except ImportError:
    print("❌ Run: pip install flask")
    exit(1)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BEAT ADDICTS Studio v{{ version }}</title>
    <style>
        body { background: #121212; color: white; text-align: center; padding: 50px; font-family: Arial; }
        h1 { color: #ff4081; font-size: 3em; }
        .btn { background: #ff4081; color: #121212; padding: 15px 30px; border: none; border-radius: 25px; cursor: pointer; margin: 10px; }
        
        .container { max-width: 1200px; margin: 0 auto; }
        .header { margin-bottom: 30px; }
        .subtitle { font-size: 1.2em; color: #ccc; }
        .version-badge { background: #333; padding: 5px 10px; border-radius: 15px; display: inline-block; margin-top: 10px; }
        
        .dashboard { display: flex; flex-wrap: wrap; justify-content: space-between; }
        .card { background: #1e1e1e; border-radius: 8px; padding: 20px; margin: 10px; flex: 1 1 300px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); }
        .card h3 { color: #ff4081; }
        .controls { margin: 15px 0; }
        .controls label { margin-right: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>BEAT ADDICTS STUDIO</h1>
            <div class="subtitle">Professional Music Production AI</div>
            <div class="version-badge">v{{ version }}</div>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h3>Voice Assignment Engine</h3>
                <p>Professional voice mapping and control system</p>
                <div class="controls">
                    <label>Channel: <input type="number" id="voice-channel" min="0" max="15" value="0"></label>
                    <label>Voice Type: 
                        <select id="voice-type">
                            <option value="lead_synth">Lead Synth</option>
                            <option value="bass_synth">Bass Synth</option>
                            <option value="pad_synth">Pad Synth</option>
                            <option value="vocal_lead">Vocal Lead</option>
                            <option value="vocal_harmony">Vocal Harmony</option>
                        </select>
                    </label>
                    <label>Genre: 
                        <select id="voice-genre">
                            <option value="hiphop">Hip-Hop</option>
                            <option value="electronic">Electronic</option>
                            <option value="vocal">Vocal</option>
                            <option value="general">General</option>
                        </select>
                    </label>
                </div>
                <button class="btn" onclick="assignVoice()">Assign Voice</button>
                <button class="btn" onclick="loadVoiceProfiles()">Load Profiles</button>
                <div id="voice-status"></div>
            </div>
            
            <div class="card">
                <h3>Lyric Integration</h3>
                <p>AI-powered lyric to voice mapping</p>
                <textarea id="lyrics-input" placeholder="Enter lyrics here..." style="width: 100%; height: 100px; margin: 10px 0;"></textarea>
                <button class="btn" onclick="processWithLyrics()">Process with Lyrics</button>
                <div id="lyric-status"></div>
            </div>
            
            <div class="card">
                <h3>MIDI File Processing</h3>
                <p>Advanced MIDI file analysis and processing</p>
                <input type="file" id="midi-file-input" accept=".mid, .midi" style="margin: 10px 0;">
                <button class="btn" onclick="processMidiFile()">Process MIDI File</button>
                <div id="midi-status"></div>
            </div>
        </div>
    </div>

    <script>
        function assignVoice() {
            const channel = document.getElementById('voice-channel').value;
            const voiceType = document.getElementById('voice-type').value;
            const genre = document.getElementById('voice-genre').value;
            
            fetch('/api/voice/assign', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    channel: parseInt(channel),
                    voice_id: voiceType,
                    genre: genre
                })
            })
            .then(response => response.json())
            .then(data => {
                const status = document.getElementById('voice-status');
                if (data.success) {
                    status.innerHTML = `<p style="color: green;">Voice ${data.voice_id} assigned to channel ${data.channel} (${data.genre})</p>`;
                } else {
                    status.innerHTML = `<p style="color: red;">Assignment failed: ${data.error}</p>`;
                }
            })
            .catch(error => {
                document.getElementById('voice-status').innerHTML = `<p style="color: red;">Error: ${error}</p>`;
            });
        }
        
        function loadVoiceProfiles() {
            fetch('/api/voice/profiles')
            .then(response => response.json())
            .then(data => {
                const status = document.getElementById('voice-status');
                let html = '<h4>Voice Profiles:</h4>';
                
                for (const [voiceId, profile] of Object.entries(data.profiles)) {
                    html += `
                        <div style="border: 1px solid #444; margin: 5px; padding: 10px; border-radius: 5px;">
                            <strong>${voiceId}</strong> (${profile.instrument_type})<br>
                            Range: ${profile.pitch_range[0]}-${profile.pitch_range[1]} | 
                            Polyphony: ${profile.polyphony_limit}<br>
                            Modes: ${profile.articulation_modes.join(', ')}
                        </div>
                    `;
                }
                
                status.innerHTML = html;
            })
            .catch(error => {
                document.getElementById('voice-status').innerHTML = `<p style="color: red;">Error: ${error}</p>`;
            });
        }
        
        function processWithLyrics() {
            const lyrics = document.getElementById('lyrics-input').value;
            if (!lyrics.trim()) {
                alert('Please enter lyrics');
                return;
            }
            
            // Sample MIDI data for testing
            const sampleMidiData = [
                {type: 'note_on', pitch: 60, velocity: 100, time: 0.0, duration: 1.0, channel: 2},
                {type: 'note_on', pitch: 64, velocity: 90, time: 1.0, duration: 1.0, channel: 2},
                {type: 'note_on', pitch: 67, velocity: 80, time: 2.0, duration: 1.0, channel: 2}
            ];
            
            fetch('/api/voice/process', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    midi_data: sampleMidiData,
                    lyrics: lyrics,
                    bpm: 120
                })
            })
            .then(response => response.json())
            .then(data => {
                const status = document.getElementById('lyric-status');
                if (data.success) {
                    status.innerHTML = `<p style="color: green;">Processed ${data.note_count} notes with lyrics</p>`;
                    
                    // Display processed notes
                    let html = '<h4>Processed Notes:</h4>';
                    data.processed_notes.slice(0, 5).forEach(note => {
                        html += `
                            <div style="font-size: 12px; margin: 2px; padding: 5px; background: #333;">
                                Pitch: ${note.pitch} | Vel: ${note.velocity} | Time: ${note.start_time.toFixed(2)}s
                                ${note.lyric ? ` | Lyric: "${note.lyric}"` : ''}
                                ${note.phoneme ? ` | Phoneme: ${note.phoneme}` : ''}
                            </div>
                        `;
                    });
                    status.innerHTML += html;
                } else {
                    status.innerHTML = `<p style="color: red;">Processing failed: ${data.error}</p>`;
                }
            })
            .catch(error => {
                document.getElementById('lyric-status').innerHTML = `<p style="color: red;">Error: ${error}</p>`;
            });
        }
        
        function processMidiFile() {
            const fileInput = document.getElementById('midi-file-input');
            if (fileInput.files.length === 0) {
                alert('Please select a MIDI file');
                return;
            }
            
            const formData = new FormData();
            formData.append('midi_file', fileInput.files[0]);
            
            fetch('/api/midi/process', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const status = document.getElementById('midi-status');
                if (data.success) {
                    status.innerHTML = `<p style="color: green;">MIDI file processed: ${data.file_name}</p>`;
                } else {
                    status.innerHTML = `<p style="color: red;">Processing failed: ${data.error}</p>`;
                }
            })
            .catch(error => {
                document.getElementById('midi-status').innerHTML = `<p style="color: red;">Error: ${error}</p>`;
            });
        }
    </script>
</body>
</html>
    """, version=app.config['BEAT_ADDICTS_VERSION'])

if __name__ == '__main__':
    # Initialize voice integration
    try:
        from voice_integration import integrate_voice_handler_with_web
        integrate_voice_handler_with_web()
    except ImportError:
        print("Voice integration not available")
    
    print("BEAT ADDICTS Studio starting at http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
