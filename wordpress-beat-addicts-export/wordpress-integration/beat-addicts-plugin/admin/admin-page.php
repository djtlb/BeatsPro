<div class="wrap">
    <h1>BEAT ADDICTS Music Production AI</h1>
    
    <div class="beat-addicts-admin">
        <div class="status-section">
            <h2>System Status</h2>
            <div id="beat-addicts-status">
                <p>Checking system status...</p>
            </div>
        </div>
        
        <div class="controls-section">
            <h2>System Controls</h2>
            <button type="button" class="button button-primary" onclick="startServices()">Start Services</button>
            <button type="button" class="button" onclick="stopServices()">Stop Services</button>
            <button type="button" class="button" onclick="restartServices()">Restart Services</button>
        </div>
        
        <div class="generators-section">
            <h2>Available Generators</h2>
            <div class="generator-grid">
                <div class="generator-card">
                    <h3>Universal</h3>
                    <p>All-purpose music generation</p>
                </div>
                <div class="generator-card">
                    <h3>DNB</h3>
                    <p>Drum & Bass generation</p>
                </div>
                <div class="generator-card">
                    <h3>Hip-Hop</h3>
                    <p>Hip-Hop beat generation</p>
                </div>
                <div class="generator-card">
                    <h3>Electronic</h3>
                    <p>Electronic music generation</p>
                </div>
                <div class="generator-card">
                    <h3>Rock</h3>
                    <p>Rock music generation</p>
                </div>
                <div class="generator-card">
                    <h3>Country</h3>
                    <p>Country music generation</p>
                </div>
                <div class="generator-card">
                    <h3>Futuristic</h3>
                    <p>Futuristic sound generation</p>
                </div>
            </div>
        </div>
        
        <div class="usage-section">
            <h2>Usage</h2>
            <p>Use the shortcode <code>[beat_addicts]</code> to embed the music generator in any post or page.</p>
            <p>Available attributes:</p>
            <ul>
                <li><code>generator</code> - Specify generator type (universal, dnb, hiphop, etc.)</li>
                <li><code>style</code> - Interface style (modern, classic)</li>
                <li><code>width</code> - Widget width (default: 100%)</li>
                <li><code>height</code> - Widget height (default: 600px)</li>
            </ul>
            <p>Example: <code>[beat_addicts generator="dnb" style="modern"]</code></p>
        </div>
    </div>
</div>

<script>
function checkStatus() {
    fetch('/wp-admin/admin-ajax.php', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'action=beat_addicts_status&nonce=' + beatAddicts.nonce
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('beat-addicts-status').innerHTML = 
            data.success ? '<span style="color: green;">✅ Online</span>' : '<span style="color: red;">❌ Offline</span>';
    });
}

function startServices() {
    // Implementation for starting services
    alert('Starting BEAT ADDICTS services...');
}

function stopServices() {
    // Implementation for stopping services
    alert('Stopping BEAT ADDICTS services...');
}

function restartServices() {
    // Implementation for restarting services
    alert('Restarting BEAT ADDICTS services...');
}

// Check status on page load
document.addEventListener('DOMContentLoaded', checkStatus);
setInterval(checkStatus, 30000); // Check every 30 seconds
</script>

<style>
.beat-addicts-admin {
    max-width: 1200px;
}

.status-section, .controls-section, .generators-section, .usage-section {
    background: #fff;
    border: 1px solid #ccd0d4;
    border-radius: 4px;
    padding: 20px;
    margin: 20px 0;
}

.generator-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-top: 15px;
}

.generator-card {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 15px;
    text-align: center;
    background: #f9f9f9;
}

.generator-card h3 {
    margin: 0 0 10px 0;
    color: #0073aa;
}

.generator-card p {
    margin: 0;
    color: #666;
    font-size: 14px;
}

.button {
    margin-right: 10px;
}
</style>