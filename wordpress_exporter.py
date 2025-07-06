#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - WordPress Exporter
Complete WordPress site package generator
"""

import os
import shutil
import zipfile
import json
from datetime import datetime
from pathlib import Path

class BeatAddictsWordPressExporter:
    """Export BEAT ADDICTS to WordPress-ready package"""
    
    def __init__(self):
        self.export_dir = "wordpress-beat-addicts-export"
        self.source_dir = os.getcwd()
        self.export_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.export_package = f"beat-addicts-wordpress-{self.export_timestamp}.zip"
        
    def create_export_structure(self):
        """Create WordPress-compatible directory structure"""
        print("📁 Creating WordPress directory structure...")
        
        # Remove existing export directory
        if os.path.exists(self.export_dir):
            shutil.rmtree(self.export_dir)
        
        # Create main directories
        directories = [
            self.export_dir,
            f"{self.export_dir}/beat-addicts-core",
            f"{self.export_dir}/beat-addicts-generators", 
            f"{self.export_dir}/beat-addicts-api",
            f"{self.export_dir}/beat-addicts-web",
            f"{self.export_dir}/beat-addicts-config",
            f"{self.export_dir}/beat-addicts-docs",
            f"{self.export_dir}/beat-addicts-assets",
            f"{self.export_dir}/wordpress-integration"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"   ✅ Created: {directory}")
    
    def copy_core_files(self):
        """Copy core BEAT ADDICTS files"""
        print("\n🔧 Copying core system files...")
        
        core_files = [
            'beat_addicts_connection_manager.py',
            'master_endpoints.py',
            'music_generator_app.py',
            'master_launcher.py',
            'safe_wordpress_test.py'
        ]
        
        for file in core_files:
            if os.path.exists(file):
                dest = f"{self.export_dir}/beat-addicts-core/{file}"
                shutil.copy2(file, dest)
                print(f"   ✅ Copied: {file}")
            else:
                print(f"   ⚠️ Missing: {file}")
    
    def copy_module_directories(self):
        """Copy module directories"""
        print("\n📦 Copying module directories...")
        
        modules = [
            ('beat_addicts_core', 'beat-addicts-core/modules'),
            ('beat_addicts_generators', 'beat-addicts-generators'),
            ('beat_addicts_config', 'beat-addicts-config'),
            ('beat_addicts_docs', 'beat-addicts-docs'),
            ('static', 'beat-addicts-assets/static'),
            ('templates', 'beat-addicts-assets/templates'),
            ('exports', 'beat-addicts-assets/exports'),
            ('midi_files', 'beat-addicts-assets/midi')
        ]
        
        for source_dir, dest_subdir in modules:
            if os.path.exists(source_dir):
                dest_path = f"{self.export_dir}/{dest_subdir}"
                shutil.copytree(source_dir, dest_path, dirs_exist_ok=True)
                print(f"   ✅ Copied directory: {source_dir} -> {dest_subdir}")
            else:
                print(f"   ⚠️ Directory not found: {source_dir}")
    
    def create_wordpress_integration(self):
        """Create WordPress integration files"""
        print("\n🌐 Creating WordPress integration files...")
        
        # Create WordPress plugin structure
        plugin_dir = f"{self.export_dir}/wordpress-integration/beat-addicts-plugin"
        os.makedirs(plugin_dir, exist_ok=True)
        
        # Main plugin file
        plugin_content = '''<?php
/**
 * Plugin Name: BEAT ADDICTS Music Production AI
 * Description: Professional AI-powered music generation system with multiple genres and voice assignment
 * Version: 2.0.0
 * Author: BEAT ADDICTS Team
 * License: GPL v2 or later
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('BEAT_ADDICTS_VERSION', '2.0.0');
define('BEAT_ADDICTS_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('BEAT_ADDICTS_PLUGIN_URL', plugin_dir_url(__FILE__));

class BeatAddictsWordPress {
    
    public function __construct() {
        add_action('init', array($this, 'init'));
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_action('wp_ajax_beat_addicts_generate', array($this, 'ajax_generate_music'));
        add_action('wp_ajax_nopriv_beat_addicts_generate', array($this, 'ajax_generate_music'));
        
        // Add admin menu
        add_action('admin_menu', array($this, 'add_admin_menu'));
        
        // Add shortcode
        add_shortcode('beat_addicts', array($this, 'shortcode_handler'));
    }
    
    public function init() {
        // Initialize BEAT ADDICTS system
        $this->start_beat_addicts_services();
    }
    
    public function enqueue_scripts() {
        wp_enqueue_script('beat-addicts-js', BEAT_ADDICTS_PLUGIN_URL . 'assets/beat-addicts.js', array('jquery'), BEAT_ADDICTS_VERSION, true);
        wp_enqueue_style('beat-addicts-css', BEAT_ADDICTS_PLUGIN_URL . 'assets/beat-addicts.css', array(), BEAT_ADDICTS_VERSION);
        
        // Localize script for AJAX
        wp_localize_script('beat-addicts-js', 'beatAddicts', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('beat_addicts_nonce')
        ));
    }
    
    public function add_admin_menu() {
        add_menu_page(
            'BEAT ADDICTS',
            'BEAT ADDICTS',
            'manage_options',
            'beat-addicts',
            array($this, 'admin_page'),
            'dashicons-format-audio',
            30
        );
    }
    
    public function admin_page() {
        include BEAT_ADDICTS_PLUGIN_DIR . 'admin/admin-page.php';
    }
    
    public function shortcode_handler($atts) {
        $atts = shortcode_atts(array(
            'generator' => 'universal',
            'style' => 'modern',
            'width' => '100%',
            'height' => '600px'
        ), $atts);
        
        ob_start();
        include BEAT_ADDICTS_PLUGIN_DIR . 'templates/music-generator.php';
        return ob_get_clean();
    }
    
    public function ajax_generate_music() {
        check_ajax_referer('beat_addicts_nonce', 'nonce');
        
        $generator = sanitize_text_field($_POST['generator']);
        $tempo = intval($_POST['tempo']);
        $duration = intval($_POST['duration']);
        
        // Call Python backend
        $result = $this->call_python_generator($generator, $tempo, $duration);
        
        wp_send_json_success($result);
    }
    
    private function start_beat_addicts_services() {
        // Start Python services if not already running
        $python_path = $this->get_python_path();
        $script_path = BEAT_ADDICTS_PLUGIN_DIR . '../beat-addicts-core/master_launcher.py';
        
        if (file_exists($script_path)) {
            // Check if services are running, start if needed
            $this->ensure_services_running($python_path, $script_path);
        }
    }
    
    private function call_python_generator($generator, $tempo, $duration) {
        $api_url = 'http://localhost:5001/api/generate/' . $generator;
        
        $data = array(
            'tempo' => $tempo,
            'duration' => $duration,
            'complexity' => 'medium'
        );
        
        $response = wp_remote_post($api_url, array(
            'body' => json_encode($data),
            'headers' => array('Content-Type' => 'application/json'),
            'timeout' => 30
        ));
        
        if (is_wp_error($response)) {
            return array('error' => 'Failed to connect to BEAT ADDICTS API');
        }
        
        return json_decode(wp_remote_retrieve_body($response), true);
    }
    
    private function get_python_path() {
        // Try to find Python
        $python_commands = array('python3', 'python', 'py');
        
        foreach ($python_commands as $cmd) {
            $output = shell_exec("which $cmd 2>/dev/null");
            if (!empty($output)) {
                return trim($output);
            }
        }
        
        return 'python'; // Fallback
    }
    
    private function ensure_services_running($python_path, $script_path) {
        // Check if services are running by testing API endpoint
        $response = wp_remote_get('http://localhost:5001/api/master/status', array('timeout' => 5));
        
        if (is_wp_error($response)) {
            // Services not running, start them
            $command = "$python_path $script_path > /dev/null 2>&1 &";
            shell_exec($command);
        }
    }
}

// Initialize the plugin
new BeatAddictsWordPress();

// Activation hook
register_activation_hook(__FILE__, 'beat_addicts_activate');
function beat_addicts_activate() {
    // Create necessary database tables or options
    add_option('beat_addicts_version', BEAT_ADDICTS_VERSION);
}

// Deactivation hook
register_deactivation_hook(__FILE__, 'beat_addicts_deactivate');
function beat_addicts_deactivate() {
    // Stop Python services
    shell_exec('pkill -f "master_launcher.py"');
}
?>'''
        
        with open(f"{plugin_dir}/beat-addicts.php", 'w', encoding='utf-8') as f:
            f.write(plugin_content)
        
        print("   ✅ Created WordPress plugin file")
        
        # Create admin page
        admin_dir = f"{plugin_dir}/admin"
        os.makedirs(admin_dir, exist_ok=True)
        
        admin_page_content = '''<div class="wrap">
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
</style>'''
        
        with open(f"{admin_dir}/admin-page.php", 'w', encoding='utf-8') as f:
            f.write(admin_page_content)
        
        print("   ✅ Created admin page")
        
        # Create templates directory
        templates_dir = f"{plugin_dir}/templates"
        os.makedirs(templates_dir, exist_ok=True)
        
        # Create music generator template
        generator_template = '''<div class="beat-addicts-generator" style="width: <?php echo esc_attr($atts['width']); ?>; height: <?php echo esc_attr($atts['height']); ?>;">
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
</script>'''
        
        with open(f"{templates_dir}/music-generator.php", 'w', encoding='utf-8') as f:
            f.write(generator_template)
        
        print("   ✅ Created music generator template")
    
    def create_installation_guide(self):
        """Create installation and setup guide"""
        print("\n📚 Creating installation guide...")
        
        guide_content = '''# 🎵 BEAT ADDICTS WordPress Installation Guide

## 🚀 Quick Installation

### Step 1: Upload Files
1. Upload the entire `beat-addicts-wordpress-export` folder to your WordPress server
2. Place Python files in a directory accessible by WordPress (e.g., `/var/www/html/beat-addicts/`)

### Step 2: Install WordPress Plugin
1. Copy the `wordpress-integration/beat-addicts-plugin` folder to `/wp-content/plugins/`
2. Go to WordPress Admin → Plugins → Activate "BEAT ADDICTS Music Production AI"

### Step 3: Install Python Dependencies
```bash
pip install flask numpy scipy librosa
```

### Step 4: Start BEAT ADDICTS Services
```bash
cd /path/to/beat-addicts-core/
python master_launcher.py
```

### Step 5: Test Installation
1. Go to WordPress Admin → BEAT ADDICTS
2. Check system status
3. Add `[beat_addicts]` shortcode to any page

## 🔧 Configuration

### Python Path Configuration
Edit the plugin file and update the Python path if needed:
```php
private function get_python_path() {
    return '/usr/bin/python3'; // Update this path
}
```

### Port Configuration
Default ports:
- API Server: 5001
- Music App: 5000
- Core Interface: 5002

Update these in the plugin if your server uses different ports.

### File Permissions
Ensure WordPress can execute Python scripts:
```bash
chmod +x /path/to/beat-addicts-core/*.py
chown -R www-data:www-data /path/to/beat-addicts/
```

## 🎵 Usage

### Shortcode Options
```
[beat_addicts]
[beat_addicts generator="dnb"]
[beat_addicts generator="hiphop" style="modern"]
[beat_addicts generator="electronic" width="80%" height="500px"]
```

### Available Generators
- `universal` - All-purpose music generation
- `dnb` - Drum & Bass
- `hiphop` - Hip-Hop beats
- `electronic` - Electronic music
- `rock` - Rock music
- `country` - Country music
- `futuristic` - Futuristic sounds

### Admin Panel
Access via WordPress Admin → BEAT ADDICTS:
- Monitor system status
- Start/stop services
- View generator information
- System configuration

## 🛠️ Troubleshooting

### Services Won't Start
1. Check Python path: `which python3`
2. Verify permissions: `ls -la /path/to/beat-addicts/`
3. Check port availability: `netstat -ln | grep 5001`
4. View error logs: `tail -f /var/log/apache2/error.log`

### API Connection Issues
1. Test API directly: `curl http://localhost:5001/api/master/status`
2. Check firewall settings
3. Verify WordPress can make HTTP requests

### Generator Not Working
1. Run connection test: `python safe_wordpress_test.py`
2. Check Python dependencies: `pip list`
3. Verify file permissions

## 📁 File Structure
```
wordpress-beat-addicts-export/
├── beat-addicts-core/          # Core Python files
├── beat-addicts-generators/    # Music generators
├── beat-addicts-api/          # API endpoints
├── beat-addicts-web/          # Web interfaces
├── beat-addicts-config/       # Configuration files
├── beat-addicts-assets/       # Static assets
├── wordpress-integration/     # WordPress plugin
└── installation-guide.md     # This file
```

## 🔒 Security Considerations

### Production Setup
1. Use HTTPS for all connections
2. Restrict API access to WordPress server only
3. Run Python services with limited user permissions
4. Regular security updates

### Firewall Configuration
```bash
# Allow only WordPress server to access API
iptables -A INPUT -s [wordpress-server-ip] -p tcp --dport 5001 -j ACCEPT
iptables -A INPUT -p tcp --dport 5001 -j DROP
```

## 📞 Support

### System Requirements
- WordPress 5.0+
- Python 3.8+
- PHP 7.4+
- 512MB RAM minimum
- 1GB disk space

### Testing Commands
```bash
# Test connection manager
python beat_addicts_connection_manager.py

# Test WordPress readiness
python safe_wordpress_test.py

# Test API endpoints
curl http://localhost:5001/api/master/status
```

### Performance Optimization
1. Use Python virtual environment
2. Enable caching for static assets
3. Consider using gunicorn for production
4. Monitor system resources

---

🎵 **BEAT ADDICTS is now ready for WordPress!** 🎵

For additional support, refer to the documentation in the beat-addicts-docs folder.
'''
        
        with open(f"{self.export_dir}/installation-guide.md", 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print("   ✅ Created installation guide")
    
    def create_config_files(self):
        """Create configuration files"""
        print("\n⚙️ Creating configuration files...")
        
        config_dir = f"{self.export_dir}/beat-addicts-config"
        
        # WordPress configuration
        wp_config = {
            "wordpress_integration": {
                "plugin_name": "BEAT ADDICTS Music Production AI",
                "version": "2.0.0",
                "api_endpoints": {
                    "master": "http://localhost:5001",
                    "generators": "http://localhost:5001/api/generators",
                    "voice": "http://localhost:5001/api/voice"
                },
                "default_ports": {
                    "api_server": 5001,
                    "music_app": 5000,
                    "core_interface": 5002
                }
            },
            "system_settings": {
                "auto_start_services": True,
                "debug_mode": False,
                "max_generation_time": 30,
                "supported_formats": ["midi", "wav", "mp3"]
            },
            "security": {
                "enable_cors": True,
                "allowed_origins": ["localhost", "127.0.0.1"],
                "api_key_required": False
            }
        }
        
        with open(f"{config_dir}/wordpress-config.json", 'w') as f:
            json.dump(wp_config, f, indent=2)
        
        print("   ✅ Created WordPress configuration")
        
        # Requirements file
        requirements = '''# BEAT ADDICTS WordPress Requirements
flask>=2.0.0
numpy>=1.21.0
scipy>=1.7.0
librosa>=0.8.0
requests>=2.25.0

# Optional dependencies
matplotlib>=3.3.0
soundfile>=0.10.0
'''
        
        with open(f"{config_dir}/requirements.txt", 'w', encoding='utf-8') as f:
            f.write(requirements)
        
        print("   ✅ Created requirements.txt")
        
        # Environment setup script
        setup_script = '''#!/bin/bash
# BEAT ADDICTS WordPress Setup Script

echo "🎵 BEAT ADDICTS WordPress Setup"
echo "================================"

# Check Python version
python_version=$(python3 --version 2>&1)
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv beat-addicts-env
source beat-addicts-env/bin/activate

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

# Set permissions
echo "Setting file permissions..."
chmod +x ../beat-addicts-core/*.py
chmod +x setup.sh

# Test installation
echo "Testing installation..."
cd ../beat-addicts-core/
python safe_wordpress_test.py

echo "✅ Setup complete!"
echo "📚 See installation-guide.md for next steps"
'''
        
        with open(f"{config_dir}/setup.sh", 'w', encoding='utf-8') as f:
            f.write(setup_script)
        
        os.chmod(f"{config_dir}/setup.sh", 0o755)
        
        print("   ✅ Created setup script")
    
    def create_package_info(self):
        """Create package information and manifest"""
        print("\n📋 Creating package information...")
        
        # Package manifest
        manifest = {
            "package_name": "BEAT ADDICTS WordPress Export",
            "version": "2.0.0",
            "export_date": datetime.now().isoformat(),
            "description": "Complete WordPress-ready package for BEAT ADDICTS Music Production AI",
            "components": {
                "core_system": "beat-addicts-core/",
                "generators": "beat-addicts-generators/",
                "wordpress_plugin": "wordpress-integration/",
                "documentation": "beat-addicts-docs/",
                "assets": "beat-addicts-assets/",
                "configuration": "beat-addicts-config/"
            },
            "requirements": {
                "python": "3.8+",
                "wordpress": "5.0+",
                "php": "7.4+",
                "memory": "512MB",
                "disk": "1GB"
            },
            "features": [
                "7 Music Generators (Universal, DNB, Hip-Hop, Electronic, Rock, Country, Futuristic)",
                "Voice Assignment System",
                "RESTful API",
                "WordPress Plugin Integration",
                "Admin Dashboard",
                "Shortcode Support",
                "AJAX-powered Frontend",
                "Comprehensive Documentation"
            ]
        }
        
        with open(f"{self.export_dir}/package-manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print("   ✅ Created package manifest")
        
        # README for the package
        readme_content = '''# 🎵 BEAT ADDICTS WordPress Export Package

## What's Included

This package contains everything needed to deploy BEAT ADDICTS Music Production AI to WordPress.

### 📁 Directory Structure
- `beat-addicts-core/` - Core Python system files
- `beat-addicts-generators/` - Music generation modules
- `wordpress-integration/` - WordPress plugin
- `beat-addicts-config/` - Configuration files
- `beat-addicts-assets/` - Static assets and templates
- `beat-addicts-docs/` - Documentation

### 🚀 Quick Start
1. Read `installation-guide.md` for detailed instructions
2. Run setup script: `cd beat-addicts-config && ./setup.sh`
3. Install WordPress plugin from `wordpress-integration/`
4. Add `[beat_addicts]` shortcode to any page

### ✅ Pre-Deployment Checklist
- [ ] Python 3.8+ installed
- [ ] WordPress 5.0+ ready
- [ ] Required packages installed
- [ ] File permissions set
- [ ] Port 5001 available
- [ ] Plugin activated

### 🎵 Features
- Professional music generation
- Multiple genre support
- WordPress integration
- Admin dashboard
- User-friendly interface

### 📞 Need Help?
Check the installation guide and documentation in the package.

---

**Package exported on:** ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''
**Version:** 2.0.0
**Ready for WordPress deployment!** 🚀
'''
        
        with open(f"{self.export_dir}/README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("   ✅ Created package README")
    
    def create_zip_package(self):
        """Create ZIP package for easy distribution"""
        print(f"\n📦 Creating ZIP package: {self.export_package}")
        
        with zipfile.ZipFile(self.export_package, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.export_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, os.path.dirname(self.export_dir))
                    zipf.write(file_path, arc_path)
                    
        file_size = os.path.getsize(self.export_package) / (1024 * 1024)  # MB
        print(f"   ✅ Package created: {self.export_package} ({file_size:.1f} MB)")
    
    def export_to_wordpress(self):
        """Main export function"""
        print("🎵 BEAT ADDICTS WORDPRESS EXPORTER")
        print("=" * 80)
        print(f"🕒 Export started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 Creating complete WordPress deployment package")
        print("=" * 80)
        
        try:
            # Execute all export steps
            self.create_export_structure()
            self.copy_core_files()
            self.copy_module_directories()
            self.create_wordpress_integration()
            self.create_installation_guide()
            self.create_config_files()
            self.create_package_info()
            self.create_zip_package()
            
            # Final summary
            print("\n" + "=" * 80)
            print("🎉 WORDPRESS EXPORT COMPLETE!")
            print("=" * 80)
            print(f"📦 Export Package: {self.export_package}")
            print(f"📁 Export Directory: {self.export_dir}")
            print(f"🕒 Export Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            print("🚀 NEXT STEPS:")
            print("   1. Download the ZIP package")
            print("   2. Extract on your WordPress server")
            print("   3. Follow the installation guide")
            print("   4. Activate the WordPress plugin")
            print("   5. Add [beat_addicts] shortcode to pages")
            print()
            print("📚 Documentation included:")
            print("   - installation-guide.md (detailed setup)")
            print("   - package-manifest.json (package info)")
            print("   - WordPress plugin (ready to install)")
            print("   - Configuration files (pre-configured)")
            print("=" * 80)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Export failed: {e}")
            return False

def main():
    """Main execution"""
    exporter = BeatAddictsWordPressExporter()
    success = exporter.export_to_wordpress()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
