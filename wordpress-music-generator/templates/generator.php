<div id="beat-addicts-container" class="beat-addicts-wrapper">
    <div class="beat-container">
        <h1 class="beat-title">🎵 Beat Addicts</h1>
        <p class="beat-subtitle">Your addiction to perfect beats starts here</p>
        
        <form id="beatForm" class="beat-form">
            <div class="form-group">
                <input type="text" id="prompt" placeholder="What's your vibe? (e.g., 'late night city drive', 'workout energy')" required>
            </div>
            
            <div class="form-group">
                <textarea id="genre" placeholder="Describe your genre/style... (e.g., 'dark electronic with heavy bass', 'acoustic folk with violin')" maxlength="250" required></textarea>
                <div class="character-count">
                    <span id="genreCount">0</span>/250 characters
                </div>
            </div>
            
            <div class="form-group">
                <select id="mood">
                    <option value="happy">Happy</option>
                    <option value="sad">Sad</option>
                    <option value="energetic">Energetic</option>
                    <option value="calm">Calm</option>
                    <option value="romantic">Romantic</option>
                </select>
            </div>
            
            <div class="form-group">
                <select id="duration">
                    <option value="60">1 Minute</option>
                    <option value="120">2 Minutes</option>
                    <option value="180" selected>3 Minutes</option>
                    <option value="240">4 Minutes</option>
                    <option value="300">5 Minutes</option>
                </select>
            </div>
            
            <button type="submit" class="generate-btn">🎵 Drop the Beat</button>
        </form>
        
        <div id="loading" class="loading-section" style="display: none;">
            <h3>🎵 Cooking up your beat...</h3>
            <p>The beat addiction is real - this may take a moment</p>
        </div>
        
        <div id="result" class="result-section" style="display: none;">
            <h3>Your Fresh Beat:</h3>
            <div id="songDetails"></div>
        </div>
        
        <div id="tracksGrid" class="tracks-grid"></div>
    </div>
</div>
