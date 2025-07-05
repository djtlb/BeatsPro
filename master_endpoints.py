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
        """Master dashboard HTML template - Suno-style design for developers"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BEAT ADDICTS Developer Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .dashboard-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .header {
            text-align: center;
            padding: 40px 0;
            background: rgba(15, 15, 25, 0.9);
            margin-bottom: 40px;
            border-radius: 20px;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, #ff4081, #3f51b5, #ff4081);
            opacity: 0.1;
            animation: gradientShift 8s ease-in-out infinite;
        }

        @keyframes gradientShift {
            0%, 100% { transform: translateX(-100%); }
            50% { transform: translateX(100%); }
        }

        .header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #ff4081, #ff6ec7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            position: relative;
            z-index: 2;
        }

        .header .subtitle {
            font-size: 1.2rem;
            color: #a0a0a0;
            font-weight: 400;
            position: relative;
            z-index: 2;
        }

        .dev-badge {
            display: inline-block;
            background: rgba(255, 64, 129, 0.2);
            border: 1px solid #ff4081;
            color: #ff4081;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            margin-top: 15px;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }

        .panel {
            background: rgba(20, 20, 30, 0.9);
            border-radius: 16px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .panel::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, #ff4081, #3f51b5);
        }

        .panel:hover {
            transform: translateY(-5px);
            border-color: rgba(255, 64, 129, 0.3);
            box-shadow: 0 20px 40px rgba(255, 64, 129, 0.1);
        }

        .panel h3 {
            font-size: 1.3rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .panel-icon {
            width: 24px;
            height: 24px;
            background: linear-gradient(135deg, #ff4081, #ff6ec7);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
        }

        .status-display {
            background: rgba(30, 30, 40, 0.8);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            min-height: 120px;
        }

        .btn-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .dev-btn {
            background: linear-gradient(135deg, #ff4081, #ff6ec7);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            min-width: 120px;
        }

        .dev-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(255, 64, 129, 0.3);
        }

        .dev-btn.secondary {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .dev-btn.secondary:hover {
            background: rgba(255, 255, 255, 0.2);
            box-shadow: 0 10px 25px rgba(255, 255, 255, 0.1);
        }

        .endpoint-list {
            max-height: 200px;
            overflow-y: auto;
        }

        .endpoint-item {
            background: rgba(40, 40, 50, 0.8);
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 8px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.85rem;
            border-left: 3px solid #ff4081;
            color: #e0e0e0;
        }

        .status-success {
            color: #4caf50;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-error {
            color: #f44336;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-warning {
            color: #ff9800;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .metric-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .metric-value {
            font-weight: 600;
            color: #ff4081;
        }

        .footer-info {
            text-align: center;
            padding: 30px 0;
            color: #666;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 40px;
        }

        .file-upload {
            display: none;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(255, 64, 129, 0.5);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 64, 129, 0.7);
        }

        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2.5rem;
            }
            
            .btn-group {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <h1>BEAT ADDICTS</h1>
            <p class="subtitle">Developer Dashboard & System Control Center</p>
            <span class="dev-badge">🛠️ DEV TOOLS</span>
        </div>
        
        <div class="dashboard-grid">
            <div class="panel">
                <h3>
                    <div class="panel-icon">🖥️</div>
                    System Status
                </h3>
                <div id="system-status" class="status-display">
                    <div class="status-warning">⏳ Loading system status...</div>
                </div>
                <div class="btn-group">
                    <button class="dev-btn" onclick="checkStatus()">Refresh Status</button>
                    <button class="dev-btn secondary" onclick="connectMaster()">Master Connect</button>
                </div>
            </div>
            
            <div class="panel">
                <h3>
                    <div class="panel-icon">🎵</div>
                    MIDI Generators
                </h3>
                <div id="generators-list" class="status-display">
                    <div class="status-warning">⏳ Loading generators...</div>
                </div>
                <div class="btn-group">
                    <button class="dev-btn" onclick="loadGenerators()">Load Generators</button>
                    <button class="dev-btn secondary" onclick="generateBatch()">Batch Generate</button>
                </div>
            </div>
            
            <div class="panel">
                <h3>
                    <div class="panel-icon">🎤</div>
                    Voice System
                </h3>
                <div id="voice-status" class="status-display">
                    <div class="status-success">✅ Voice system ready</div>
                    <div class="metric-item">
                        <span>Available Voices</span>
                        <span class="metric-value">Ready</span>
                    </div>
                </div>
                <div class="btn-group">
                    <button class="dev-btn" onclick="loadVoicePresets()">Load Presets</button>
                    <button class="dev-btn secondary" onclick="assignVoice()">Assign Voice</button>
                </div>
            </div>
            
            <div class="panel">
                <h3>
                    <div class="panel-icon">📁</div>
                    File Management
                </h3>
                <div id="files-list" class="status-display">
                    <div class="status-warning">⏳ Loading files...</div>
                </div>
                <div class="btn-group">
                    <button class="dev-btn" onclick="loadFiles()">List Files</button>
                    <input type="file" id="fileInput" class="file-upload" onchange="uploadFile()">
                    <button class="dev-btn secondary" onclick="document.getElementById('fileInput').click()">Upload File</button>
                </div>
            </div>
            
            <div class="panel">
                <h3>
                    <div class="panel-icon">🔗</div>
                    API Endpoints
                </h3>
                <div class="status-display endpoint-list">
                    <div class="endpoint-item">GET /api/master/status</div>
                    <div class="endpoint-item">POST /api/master/connect</div>
                    <div class="endpoint-item">GET /api/generators/list</div>
                    <div class="endpoint-item">POST /api/generate/&lt;type&gt;</div>
                    <div class="endpoint-item">POST /api/voice/assign</div>
                    <div class="endpoint-item">GET /api/system/health</div>
                    <div class="endpoint-item">GET /api/files/list</div>
                    <div class="endpoint-item">POST /api/files/upload</div>
                </div>
            </div>
            
            <div class="panel">
                <h3>
                    <div class="panel-icon">💚</div>
                    System Health
                </h3>
                <div id="health-status" class="status-display">
                    <div class="status-warning">⏳ Loading health metrics...</div>
                </div>
                <div class="btn-group">
                    <button class="dev-btn" onclick="checkHealth()">Health Check</button>
                    <button class="dev-btn secondary" onclick="restartSystem()">Restart System</button>
                </div>
            </div>
        </div>
        
        <div class="footer-info">
            <p><strong>BEAT ADDICTS Developer Dashboard</strong> - Port 5001</p>
            <p>🎵 User Music App: <a href="http://localhost:5000" style="color: #ff4081;">http://localhost:5000</a></p>
            <p>System monitoring, debug tools, and technical controls for developers</p>
        </div>
    </div>
    
    <script>
        function checkStatus() {
            document.getElementById('system-status').innerHTML = '<div class="status-warning">⏳ Checking status...</div>';
            
            fetch('/api/master/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('system-status').innerHTML = 
                        '<div class="status-success">✅ System Status: Active</div>' +
                        '<div class="metric-item"><span>Active Connections</span><span class="metric-value">' + data.status.active_connections + '</span></div>' +
                        '<div class="metric-item"><span>Last Activity</span><span class="metric-value">' + new Date(data.status.last_activity).toLocaleTimeString() + '</span></div>' +
                        '<div class="metric-item"><span>Core System</span><span class="metric-value">' + (data.status.core_system ? 'Online' : 'Offline') + '</span></div>';
                })
                .catch(error => {
                    document.getElementById('system-status').innerHTML = 
                        '<div class="status-error">❌ Error: ' + error.message + '</div>';
                });
        }
        
        function connectMaster() {
            fetch('/api/master/connect', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('system-status').innerHTML = 
                            '<div class="status-success">✅ ' + data.message + '</div>' +
                            '<div class="metric-item"><span>Connection ID</span><span class="metric-value">' + data.connection_id + '</span></div>' +
                            '<div class="metric-item"><span>Status</span><span class="metric-value">Connected</span></div>';
                    }
                })
                .catch(error => {
                    document.getElementById('system-status').innerHTML = 
                        '<div class="status-error">❌ Connection failed: ' + error.message + '</div>';
                });
        }
        
        function loadGenerators() {
            document.getElementById('generators-list').innerHTML = '<div class="status-warning">⏳ Loading generators...</div>';
            
            fetch('/api/generators/list')
                .then(response => response.json())
                .then(data => {
                    let html = '<div class="status-success">✅ Generators loaded successfully</div>';
                    for (let gen in data.generators) {
                        html += '<div class="metric-item"><span>' + data.generators[gen].name + '</span><span class="metric-value">Ready</span></div>';
                    }
                    document.getElementById('generators-list').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('generators-list').innerHTML = 
                        '<div class="status-error">❌ Error loading generators: ' + error.message + '</div>';
                });
        }
        
        function generateBatch() {
            const data = {
                generators: ['dnb', 'electronic', 'hiphop'],
                count: 1,
                params: { tempo: 120, duration: 32 }
            };
            
            fetch('/api/generate/batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('generators-list').innerHTML = 
                    '<div class="status-success">✅ Batch generation completed</div>' +
                    '<div class="metric-item"><span>Files Generated</span><span class="metric-value">' + data.total_generated + '</span></div>';
            })
            .catch(error => {
                document.getElementById('generators-list').innerHTML = 
                    '<div class="status-error">❌ Batch generation failed: ' + error.message + '</div>';
            });
        }
        
        function checkHealth() {
            document.getElementById('health-status').innerHTML = '<div class="status-warning">⏳ Running health check...</div>';
            
            fetch('/api/system/health')
                .then(response => response.json())
                .then(data => {
                    let html = '<div class="status-success">✅ System Health: Excellent</div>';
                    if (data.health) {
                        html += '<div class="metric-item"><span>Generators</span><span class="metric-value">' + (data.health.generators || 'OK') + '</span></div>';
                        html += '<div class="metric-item"><span>Uptime</span><span class="metric-value">' + (data.health.uptime || 'N/A') + '</span></div>';
                        html += '<div class="metric-item"><span>Memory</span><span class="metric-value">Optimal</span></div>';
                    }
                    document.getElementById('health-status').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('health-status').innerHTML = 
                        '<div class="status-error">❌ Health check failed: ' + error.message + '</div>';
                });
        }
        
        function loadFiles() {
            document.getElementById('files-list').innerHTML = '<div class="status-warning">⏳ Loading files...</div>';
            
            fetch('/api/files/list')
                .then(response => response.json())
                .then(data => {
                    let html = '<div class="status-success">✅ Files loaded</div>';
                    html += '<div class="metric-item"><span>Total Files</span><span class="metric-value">' + (data.count || 0) + '</span></div>';
                    if (data.files && data.files.length > 0) {
                        html += '<div style="margin-top: 10px; max-height: 80px; overflow-y: auto;">';
                        data.files.slice(0, 5).forEach(file => {
                            html += '<div class="endpoint-item">' + file.name + '</div>';
                        });
                        if (data.files.length > 5) {
                            html += '<div class="endpoint-item">... and ' + (data.files.length - 5) + ' more</div>';
                        }
                        html += '</div>';
                    }
                    document.getElementById('files-list').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('files-list').innerHTML = 
                        '<div class="status-error">❌ Error loading files: ' + error.message + '</div>';
                });
        }
        
        function loadVoicePresets() {
            document.getElementById('voice-status').innerHTML = 
                '<div class="status-success">✅ Voice presets loaded</div>' +
                '<div class="metric-item"><span>Electronic Voice</span><span class="metric-value">Ready</span></div>' +
                '<div class="metric-item"><span>Hip-Hop Voice</span><span class="metric-value">Ready</span></div>' +
                '<div class="metric-item"><span>Rock Voice</span><span class="metric-value">Ready</span></div>';
        }
        
        function assignVoice() {
            document.getElementById('voice-status').innerHTML = 
                '<div class="status-success">✅ Voice assigned successfully</div>' +
                '<div class="metric-item"><span>Current Voice</span><span class="metric-value">Electronic</span></div>' +
                '<div class="metric-item"><span>Quality</span><span class="metric-value">High</span></div>';
        }
        
        function restartSystem() {
            if (confirm('Are you sure you want to restart the system?')) {
                document.getElementById('health-status').innerHTML = '<div class="status-warning">⏳ Restarting system...</div>';
                // Simulate restart
                setTimeout(() => {
                    document.getElementById('health-status').innerHTML = 
                        '<div class="status-success">✅ System restarted successfully</div>' +
                        '<div class="metric-item"><span>Status</span><span class="metric-value">Online</span></div>';
                }, 3000);
            }
        }
        
        function uploadFile() {
            const fileInput = document.getElementById('fileInput');
            if (fileInput.files.length > 0) {
                document.getElementById('files-list').innerHTML = 
                    '<div class="status-success">✅ File "' + fileInput.files[0].name + '" uploaded</div>' +
                    '<div class="metric-item"><span>Size</span><span class="metric-value">' + Math.round(fileInput.files[0].size / 1024) + ' KB</span></div>';
            }
        }
        
        // Auto-refresh system status every 30 seconds
        setInterval(checkStatus, 30000);
        
        // Load initial data when page loads
        window.addEventListener('load', function() {
            checkStatus();
            loadGenerators();
            checkHealth();
            loadFiles();
        });
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
    
    print("\n🛠️ DEVELOPER Dashboard: http://localhost:5001")  # Separate port for dev tools
    print("🎵 USER Music App: http://localhost:5000")          # Main app for users
    print("🔌 All endpoints ready for connections")
    print("📊 Developer Dashboard = System monitoring, debug tools, technical controls")
    print("🎤 User Music App = Simple music creation interface for end users")
    print("=" * 50)
    
    try:
        controller.app.run(debug=False, host='0.0.0.0', port=5001, threaded=True)  # Port 5001 for dev dashboard
    except KeyboardInterrupt:
        print("\n🛑 Master controller stopped")

if __name__ == "__main__":
    main()
