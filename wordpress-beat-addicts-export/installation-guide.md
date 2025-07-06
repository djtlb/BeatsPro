# 🎵 BEAT ADDICTS WordPress Installation Guide

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
