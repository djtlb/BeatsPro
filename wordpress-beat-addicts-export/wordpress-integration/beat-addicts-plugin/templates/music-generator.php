<div class="beat-addicts-generator" style="width: <?php echo esc_attr($atts['width']); ?>; height: <?php echo esc_attr($atts['height']); ?>;">
    <div class="beat-addicts-header">
        <h3>🎵 BEAT ADDICTS Music Generator</h3>
    </div>
    
    <div class="beat-addicts-controls">
        <div class="control-group">
            <label for="ba-generator">Generator Type:</label>
            <select id="ba-generator" name="generator">
                <option value="universal" <?php selected($atts['generator'], 'universal'); ?>>Universal</option>
                <option value="dnb" <?php selected($atts['generator'], 'dnb'); ?>>Drum & Bass</option>
                <option value="hiphop" <?php selected($atts['generator'], 'hiphop'); ?>>Hip-Hop</option>
                <option value="electronic" <?php selected($atts['generator'], 'electronic'); ?>>Electronic</option>
                <option value="rock" <?php selected($atts['generator'], 'rock'); ?>>Rock</option>
                <option value="country" <?php selected($atts['generator'], 'country'); ?>>Country</option>
                <option value="futuristic" <?php selected($atts['generator'], 'futuristic'); ?>>Futuristic</option>
            </select>
        </div>
        
        <div class="control-group">
            <label for="ba-tempo">Tempo (BPM):</label>
            <input type="range" id="ba-tempo" name="tempo" min="60" max="200" value="120">
            <span id="tempo-value">120</span>
        </div>
        
        <div class="control-group">
            <label for="ba-duration">Duration (bars):</label>
            <input type="range" id="ba-duration" name="duration" min="8" max="64" value="32">
            <span id="duration-value">32</span>
        </div>
        
        <div class="control-group">
            <button type="button" id="generate-btn" class="beat-addicts-btn">🎵 Generate Music</button>
        </div>
    </div>
    
    <div class="beat-addicts-output">
        <div id="generation-status">Ready to generate music...</div>
        <div id="audio-player" style="display: none;">
            <audio controls style="width: 100%;">
                <source id="audio-source" src="" type="audio/wav">
                Your browser does not support the audio element.
            </audio>
        </div>
        <div id="download-link" style="display: none;">
            <a href="#" id="download-midi" class="beat-addicts-btn">📥 Download MIDI</a>
        </div>
    </div>
</div>

<style>
.beat-addicts-generator {
    border: 2px solid #0073aa;
    border-radius: 8px;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-family: Arial, sans-serif;
}

.beat-addicts-header h3 {
    margin: 0 0 20px 0;
    text-align: center;
    font-size: 24px;
}

.beat-addicts-controls {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    padding: 15px;
    margin-bottom: 20px;
}

.control-group {
    margin-bottom: 15px;
}

.control-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.control-group select,
.control-group input[type="range"] {
    width: 100%;
    padding: 8px;
    border: none;
    border-radius: 4px;
}

.beat-addicts-btn {
    background: #ff4081;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 25px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    text-decoration: none;
    display: inline-block;
    transition: background 0.3s;
}

.beat-addicts-btn:hover {
    background: #e91e63;
}

.beat-addicts-output {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    padding: 15px;
    text-align: center;
}

#generation-status {
    font-size: 16px;
    margin-bottom: 15px;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const tempoSlider = document.getElementById('ba-tempo');
    const tempoValue = document.getElementById('tempo-value');
    const durationSlider = document.getElementById('ba-duration');
    const durationValue = document.getElementById('duration-value');
    const generateBtn = document.getElementById('generate-btn');
    
    // Update display values
    tempoSlider.addEventListener('input', function() {
        tempoValue.textContent = this.value;
    });
    
    durationSlider.addEventListener('input', function() {
        durationValue.textContent = this.value;
    });
    
    // Generate music
    generateBtn.addEventListener('click', function() {
        const generator = document.getElementById('ba-generator').value;
        const tempo = document.getElementById('ba-tempo').value;
        const duration = document.getElementById('ba-duration').value;
        
        document.getElementById('generation-status').textContent = 'Generating music...';
        generateBtn.disabled = true;
        
        fetch(beatAddicts.ajax_url, {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `action=beat_addicts_generate&generator=${generator}&tempo=${tempo}&duration=${duration}&nonce=${beatAddicts.nonce}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('generation-status').textContent = 'Music generated successfully!';
                // Handle successful generation
                if (data.data.output_file) {
                    document.getElementById('download-link').style.display = 'block';
                    document.getElementById('download-midi').href = '/path/to/generated/' + data.data.output_file;
                }
            } else {
                document.getElementById('generation-status').textContent = 'Generation failed: ' + (data.data || 'Unknown error');
            }
        })
        .catch(error => {
            document.getElementById('generation-status').textContent = 'Error: ' + error.message;
        })
        .finally(() => {
            generateBtn.disabled = false;
        });
    });
});
</script>