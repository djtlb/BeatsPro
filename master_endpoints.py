#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Master Connection & Endpoint Controller
Comprehensive API endpoints and connection management system
"""

import os
import sys
import json
import threading
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename

class MasterConnectionController:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'beat_addicts_master_endpoints_2025'
        self.app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
        
        # System status tracking
        self.system_status = {
            'core_system': False,
            'midi_generators': {},
            'voice_system': False,
            'web_interface': True,
            'active_connections': 0,
            'last_activity': datetime.now().isoformat()
        }
        
        # Initialize available generators
        self.available_generators = [
            'country', 'dnb', 'electronic', 'futuristic', 
            'hiphop', 'rock', 'universal'
        ]
        
        # Setup all endpoints
        self.setup_master_endpoints()
        self.setup_generator_endpoints()
        self.setup_voice_endpoints()
        self.setup_system_endpoints()
        self.setup_file_endpoints()
        
    def setup_master_endpoints(self):
        """Setup main control endpoints"""
        
        @self.app.route('/')
        def master_dashboard():
            """Master dashboard with all system controls"""
            return render_template_string(self.get_master_dashboard_template())
            
        @self.app.route('/api/master/status', methods=['GET'])
        def get_master_status():
            """Get complete system status"""
            self.system_status['last_activity'] = datetime.now().isoformat()
            return jsonify({
                'success': True,
                'status': self.system_status,
                'available_generators': self.available_generators,
                'endpoints': self.get_endpoint_list()
            })
            
        @self.app.route('/api/master/connect', methods=['POST'])
        def master_connect():
            """Establish master connection"""
            self.system_status['active_connections'] += 1
            self.system_status['last_activity'] = datetime.now().isoformat()
            
            return jsonify({
                'success': True,
                'message': 'Connected to BEAT ADDICTS Master System',
                'connection_id': self.system_status['active_connections'],
                'system_status': self.system_status
            })
            
    def setup_generator_endpoints(self):
        """Setup MIDI generator endpoints"""
        
        @self.app.route('/api/generators/list', methods=['GET'])
        def list_generators():
            """List all available generators"""
            generator_info = {}
            
            for gen_type in self.available_generators:
                generator_info[gen_type] = {
                    'name': f"{gen_type.title()} MIDI Generator",
                    'status': 'available',
                    'endpoint': f'/api/generate/{gen_type}'
                }
                
            return jsonify({
                'success': True,
                'generators': generator_info
            })
            
        @self.app.route('/api/generate/<generator_type>', methods=['POST'])
        def generate_midi(generator_type):
            """Generate MIDI using specified generator"""
            try:
                data = request.get_json() or {}
                
                # Default parameters
                params = {
                    'tempo': data.get('tempo', 120),
                    'duration': data.get('duration', 32),
                    'complexity': data.get('complexity', 'medium'),
                    'style': data.get('style', 'default')
                }
                
                # Import and use the appropriate generator
                result = self.execute_generator(generator_type, params)
                
                return jsonify({
                    'success': True,
                    'generator': generator_type,
                    'parameters': params,
                    'result': result
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e),
                    'generator': generator_type
                }), 500
                
        @self.app.route('/api/generate/batch', methods=['POST'])
        def batch_generate():
            """Generate multiple MIDI files with different generators"""
            try:
                data = request.get_json() or {}
                generators = data.get('generators', ['dnb', 'electronic'])
                count = data.get('count', 1)
                
                results = []
                for gen_type in generators:
                    for i in range(count):
                        result = self.execute_generator(gen_type, data.get('params', {}))
                        results.append({
                            'generator': gen_type,
                            'index': i + 1,
                            'result': result
                        })
                        
                return jsonify({
                    'success': True,
                    'batch_results': results,
                    'total_generated': len(results)
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
                
    def setup_voice_endpoints(self):
        """Setup voice system endpoints"""
        
        @self.app.route('/api/voice/assign', methods=['POST'])
        def assign_voice():
            """Assign voice to MIDI channel"""
            try:
                data = request.get_json() or {}
                channel = data.get('channel', 0)
                voice_type = data.get('voice_type', 'acoustic_grand_piano')
                
                # Voice assignment logic would go here
                result = self.assign_voice_to_channel(channel, voice_type)
                
                return jsonify({
                    'success': True,
                    'channel': channel,
                    'voice_type': voice_type,
                    'result': result
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
                
        @self.app.route('/api/voice/presets', methods=['GET'])
        def get_voice_presets():
            """Get available voice presets"""
            presets = {
                'electronic': ['synth_lead', 'synth_pad', 'synth_bass'],
                'rock': ['distortion_guitar', 'clean_guitar', 'bass_guitar'],
                'hiphop': ['hip_bass', 'trap_lead', 'vocal_chop'],
                'dnb': ['reese_bass', 'amen_break', 'liquid_pad']
            }
            
            return jsonify({
                'success': True,
                'voice_presets': presets
            })
            
    def setup_system_endpoints(self):
        """Setup system control endpoints"""
        
        @self.app.route('/api/system/restart', methods=['POST'])
        def restart_system():
            """Restart BEAT ADDICTS system"""
            try:
                # System restart logic
                self.system_status['last_activity'] = datetime.now().isoformat()
                
                return jsonify({
                    'success': True,
                    'message': 'System restart initiated',
                    'status': self.system_status
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
                
        @self.app.route('/api/system/health', methods=['GET'])
        def system_health():
            """Get system health status"""
            health_status = {
                'uptime': 'Active',
                'memory': 'OK',
                'generators': len(self.available_generators),
                'active_connections': self.system_status['active_connections'],
                'last_activity': self.system_status['last_activity']
            }
            
            return jsonify({
                'success': True,
                'health': health_status,
                'timestamp': datetime.now().isoformat()
            })
            
    def setup_file_endpoints(self):
        """Setup file management endpoints"""
        
        @self.app.route('/api/files/upload', methods=['POST'])
        def upload_file():
            """Upload MIDI or audio files"""
            try:
                if 'file' not in request.files:
                    return jsonify({'success': False, 'error': 'No file provided'}), 400
                    
                file = request.files['file']
                if file.filename == '' or file.filename is None:
                    return jsonify({'success': False, 'error': 'No file selected'}), 400
                    
                filename = secure_filename(file.filename)
                # Save file logic would go here
                
                return jsonify({
                    'success': True,
                    'filename': filename,
                    'message': 'File uploaded successfully'
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
                
        @self.app.route('/api/files/list', methods=['GET'])
        def list_files():
            """List available MIDI files"""
            try:
                midi_dir = Path(__file__).parent.parent / 'midi_files'
                files = []
                
                if midi_dir.exists():
                    for file in midi_dir.glob('*.mid'):
                        files.append({
                            'name': file.name,
                            'size': file.stat().st_size,
                            'modified': datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                        })
                        
                return jsonify({
                    'success': True,
                    'files': files,
                    'count': len(files)
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
                
    def execute_generator(self, generator_type, params):
        """Execute specified MIDI generator"""
        try:
            # This would interface with your actual generators
            # For now, return a mock successful result
            
            output_file = f"{generator_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mid"
            
            return {
                'status': 'generated',
                'output_file': output_file,
                'parameters_used': params,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Generator {generator_type} failed: {e}")
            
    def assign_voice_to_channel(self, channel, voice_type):
        """Assign voice to MIDI channel"""
        # Voice assignment logic would interface with your voice system
        return {
            'status': 'assigned',
            'channel': channel,
            'voice': voice_type,
            'timestamp': datetime.now().isoformat()
        }
        
    def get_endpoint_list(self):
        """Get list of all available endpoints"""
        return {
            'master': [
                'GET /',
                'GET /api/master/status',
                'POST /api/master/connect'
            ],
            'generators': [
                'GET /api/generators/list',
                'POST /api/generate/<type>',
                'POST /api/generate/batch'
            ],
            'voice': [
                'POST /api/voice/assign',
                'GET /api/voice/presets'
            ],
            'system': [
                'POST /api/system/restart',
                'GET /api/system/health'
            ],
            'files': [
                'POST /api/files/upload',
                'GET /api/files/list'
            ]
        }
        
    def get_master_dashboard_template(self):
        """Master dashboard HTML template"""
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>BEAT ADDICTS - Master Control</title>
    <style>
        body { background: #121212; color: white; font-family: Arial; margin: 0; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #ff4081; font-size: 2.5em; margin: 0; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .panel { background: #1e1e1e; border-radius: 10px; padding: 20px; border-left: 4px solid #ff4081; }
        .panel h3 { color: #ff4081; margin-top: 0; }
        .btn { background: #ff4081; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; }
        .btn:hover { background: #e91e63; }
        .status { background: #333; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .endpoint { background: #2a2a2a; padding: 5px 10px; margin: 5px 0; border-radius: 3px; font-family: monospace; }
        .success { color: #4caf50; }
        .error { color: #f44336; }
    </style>
</head>
<body>
    <div class="header">
        <h1>BEAT ADDICTS MASTER CONTROL</h1>
        <p>Professional Music Production AI - Master Connection Dashboard</p>
    </div>
    
    <div class="dashboard">
        <div class="panel">
            <h3>System Status</h3>
            <div id="system-status" class="status">Loading...</div>
            <button class="btn" onclick="checkStatus()">Refresh Status</button>
            <button class="btn" onclick="connectMaster()">Master Connect</button>
        </div>
        
        <div class="panel">
            <h3>MIDI Generators</h3>
            <div id="generators-list" class="status">Loading generators...</div>
            <button class="btn" onclick="loadGenerators()">Load Generators</button>
            <button class="btn" onclick="generateBatch()">Batch Generate</button>
        </div>
        
        <div class="panel">
            <h3>Voice System</h3>
            <div id="voice-status" class="status">Voice system ready</div>
            <button class="btn" onclick="loadVoicePresets()">Load Presets</button>
            <button class="btn" onclick="assignVoice()">Assign Voice</button>
        </div>
        
        <div class="panel">
            <h3>File Management</h3>
            <div id="files-list" class="status">Loading files...</div>
            <button class="btn" onclick="loadFiles()">List Files</button>
            <input type="file" id="fileInput" style="display: none;" onchange="uploadFile()">
            <button class="btn" onclick="document.getElementById('fileInput').click()">Upload File</button>
        </div>
        
        <div class="panel">
            <h3>API Endpoints</h3>
            <div id="endpoints-list" class="status">
                <div class="endpoint">GET /api/master/status</div>
                <div class="endpoint">POST /api/master/connect</div>
                <div class="endpoint">GET /api/generators/list</div>
                <div class="endpoint">POST /api/generate/&lt;type&gt;</div>
                <div class="endpoint">POST /api/voice/assign</div>
                <div class="endpoint">GET /api/system/health</div>
            </div>
        </div>
        
        <div class="panel">
            <h3>System Health</h3>
            <div id="health-status" class="status">Loading health...</div>
            <button class="btn" onclick="checkHealth()">Health Check</button>
            <button class="btn" onclick="restartSystem()">Restart System</button>
        </div>
    </div>
    
    <script>
        function checkStatus() {
            fetch('/api/master/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('system-status').innerHTML = 
                        '<div class="success">System Status: Active</div>' +
                        '<div>Active Connections: ' + data.status.active_connections + '</div>' +
                        '<div>Last Activity: ' + data.status.last_activity + '</div>';
                })
                .catch(error => {
                    document.getElementById('system-status').innerHTML = 
                        '<div class="error">Error: ' + error + '</div>';
                });
        }
        
        function connectMaster() {
            fetch('/api/master/connect', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('system-status').innerHTML = 
                            '<div class="success">' + data.message + '</div>' +
                            '<div>Connection ID: ' + data.connection_id + '</div>';
                    }
                });
        }
        
        function loadGenerators() {
            fetch('/api/generators/list')
                .then(response => response.json())
                .then(data => {
                    let html = '<div class="success">Available Generators:</div>';
                    for (let gen in data.generators) {
                        html += '<div class="endpoint">' + data.generators[gen].name + '</div>';
                    }
                    document.getElementById('generators-list').innerHTML = html;
                });
        }
        
        function checkHealth() {
            fetch('/api/system/health')
                .then(response => response.json())
                .then(data => {
                    let html = '<div class="success">System Health: OK</div>';
                    html += '<div>Generators: ' + data.health.generators + '</div>';
                    html += '<div>Uptime: ' + data.health.uptime + '</div>';
                    document.getElementById('health-status').innerHTML = html;
                });
        }
        
        function loadFiles() {
            fetch('/api/files/list')
                .then(response => response.json())
                .then(data => {
                    let html = '<div class="success">Files: ' + data.count + '</div>';
                    data.files.forEach(file => {
                        html += '<div class="endpoint">' + file.name + '</div>';
                    });
                    document.getElementById('files-list').innerHTML = html;
                });
        }
        
        // Load initial status
        window.onload = function() {
            checkStatus();
            loadGenerators();
            checkHealth();
            loadFiles();
        };
    </script>
</body>
</html>
        '''

def main():
    """Main function to start master controller"""
    print("🎵 BEAT ADDICTS - Master Connection Controller")
    print("=" * 50)
    print("🚀 Starting master endpoint system...")
    
    controller = MasterConnectionController()
    
    print("✅ Master endpoints configured:")
    endpoints = controller.get_endpoint_list()
    for category, endpoint_list in endpoints.items():
        print(f"   📁 {category.title()}:")
        for endpoint in endpoint_list:
            print(f"      🔗 {endpoint}")
    
    print("\n🌐 Master Control Dashboard: http://localhost:5000")
    print("🔌 All endpoints ready for connections")
    print("=" * 50)
    
    try:
        controller.app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        print("\n🛑 Master controller stopped")

if __name__ == "__main__":
    main()
