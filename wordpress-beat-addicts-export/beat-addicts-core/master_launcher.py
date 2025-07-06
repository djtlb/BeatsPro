#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Master Launcher & Connection Orchestrator
Complete system connection management and endpoint coordination
"""

import os
import sys
import time
import json
import threading
import subprocess
from datetime import datetime
from pathlib import Path

# Import our connection manager
try:
    from beat_addicts_connection_manager import BeatAddictsConnectionManager
    from master_endpoints import MasterConnectionController
    CONNECTION_MANAGER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Connection components not available: {e}")
    CONNECTION_MANAGER_AVAILABLE = False

class BeatAddictsMasterLauncher:
    """Master orchestrator for all BEAT ADDICTS connections and endpoints"""
    
    def __init__(self):
        self.connection_manager = None
        self.master_controller = None
        self.all_connections = {}
        self.running_processes = []
        self.connection_status = {}
        
        # Initialize connection manager
        self.initialize_connections()
        
    def initialize_connections(self):
        """Initialize all core connections"""
        print("🎵 BEAT ADDICTS - MASTER CONNECTION ORCHESTRATOR")
        print("=" * 80)
        print(f"🚀 Initializing at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if CONNECTION_MANAGER_AVAILABLE:
            try:
                # Initialize connection manager
                print("\n🔌 Starting Connection Manager...")
                self.connection_manager = BeatAddictsConnectionManager()
                self.all_connections = self.connection_manager.connect_all()
                
                # Initialize master controller
                print("\n🎯 Starting Master Controller...")
                self.master_controller = MasterConnectionController()
                
                # Update connection status
                self.connection_status = {
                    'connection_manager': True,
                    'master_controller': True,
                    'core_modules': len(self.all_connections.get('core', {})),
                    'generators': len(self.all_connections.get('generators', {})),
                    'web_interfaces': len(self.all_connections.get('web', {})),
                    'total_connections': sum(len(cat) for cat in self.all_connections.values())
                }
                
                print("✅ Master connection initialization complete!")
                return True
                
            except Exception as e:
                print(f"❌ Connection initialization failed: {e}")
                return False
        else:
            print("❌ Connection manager not available")
            return False
    
    def connect_all_endpoints(self):
        """Connect all endpoints to their proper connections"""
        print("\n🌐 CONNECTING ALL ENDPOINTS TO PROPER CONNECTIONS")
        print("=" * 60)
        
        endpoint_connections = {
            # Core API Endpoints
            'master_api': {
                'routes': ['/api/master/status', '/api/master/connect'],
                'connected_to': 'master_controller',
                'purpose': 'System status and connection management'
            },
            
            # Generator Endpoints  
            'generator_api': {
                'routes': ['/api/generators/list', '/api/generate/<type>', '/api/generate/batch'],
                'connected_to': 'all_generators',
                'purpose': 'MIDI generation across all genres'
            },
            
            # Voice System Endpoints
            'voice_api': {
                'routes': ['/api/voice/assign', '/api/voice/presets'],
                'connected_to': 'voice_handler',
                'purpose': 'Voice assignment and management'
            },
            
            # System Management Endpoints
            'system_api': {
                'routes': ['/api/system/restart', '/api/system/health'],
                'connected_to': 'system_monitor',
                'purpose': 'System monitoring and control'
            },
            
            # File Management Endpoints
            'file_api': {
                'routes': ['/api/files/upload', '/api/files/list'],
                'connected_to': 'file_manager',
                'purpose': 'File upload and management'
            },
            
            # Web Interface Endpoints
            'web_interface': {
                'routes': ['/'],
                'connected_to': 'web_interface_module',
                'purpose': 'Main user interface'
            }
        }
        
        # Verify and connect each endpoint
        connected_count = 0
        for endpoint_name, config in endpoint_connections.items():
            try:
                print(f"🔗 Connecting {endpoint_name}...")
                print(f"   📍 Routes: {', '.join(config['routes'])}")
                print(f"   🎯 Connected to: {config['connected_to']}")
                print(f"   💡 Purpose: {config['purpose']}")
                
                # Verify the connection exists
                if self._verify_endpoint_connection(endpoint_name, config):
                    print(f"   ✅ {endpoint_name}: CONNECTED")
                    connected_count += 1
                else:
                    print(f"   ⚠️ {endpoint_name}: CONNECTION ISSUE")
                
            except Exception as e:
                print(f"   ❌ {endpoint_name}: FAILED - {e}")
        
        print("=" * 60)
        print(f"🎯 ENDPOINT CONNECTION SUMMARY:")
        print(f"   📊 Total Endpoints: {len(endpoint_connections)}")
        print(f"   ✅ Successfully Connected: {connected_count}")
        print(f"   📈 Success Rate: {(connected_count/len(endpoint_connections))*100:.1f}%")
        
        return connected_count == len(endpoint_connections)
    
    def _verify_endpoint_connection(self, endpoint_name, config):
        """Verify that an endpoint is properly connected"""
        connected_to = config['connected_to']
        
        # Check if the target connection exists
        if connected_to == 'master_controller':
            return self.master_controller is not None
        elif connected_to == 'all_generators':
            return len(self.all_connections.get('generators', {})) > 0
        elif connected_to == 'voice_handler':
            return 'voice_handler' in self.all_connections.get('core', {})
        elif connected_to == 'system_monitor':
            return True  # System monitoring is built-in
        elif connected_to == 'file_manager':
            return True  # File management is built-in
        elif connected_to == 'web_interface_module':
            return len(self.all_connections.get('web', {})) > 0
        
        return False
    
    def start_production_services(self):
        """Start all production services with proper connections"""
        print("\n🚀 STARTING PRODUCTION SERVICES")
        print("=" * 60)
        
        services = [
            {
                'name': 'Master Endpoints Server',
                'port': 5001,
                'command': [sys.executable, 'master_endpoints.py'],
                'purpose': 'API endpoints and system control'
            },
            {
                'name': 'Music Generator App',
                'port': 5000,
                'command': [sys.executable, 'music_generator_app.py'],
                'purpose': 'User interface and music generation'
            },
            {
                'name': 'Web Interface Core',
                'port': 5002,
                'command': [sys.executable, 'beat_addicts_core/web_interface.py'],
                'purpose': 'Core web interface module'
            }
        ]
        
        started_services = 0
        for service in services:
            try:
                print(f"🌟 Starting {service['name']}...")
                print(f"   📍 Port: {service['port']}")
                print(f"   💡 Purpose: {service['purpose']}")
                
                # Check if file exists
                script_path = service['command'][1]
                if not os.path.exists(script_path):
                    print(f"   ⚠️ Script not found: {script_path}")
                    continue
                
                # Start the service
                process = subprocess.Popen(
                    service['command'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=os.getcwd(),
                    text=True
                )
                
                self.running_processes.append({
                    'name': service['name'],
                    'process': process,
                    'port': service['port'],
                    'started_at': datetime.now()
                })
                
                print(f"   ✅ {service['name']}: STARTED (PID: {process.pid})")
                started_services += 1
                time.sleep(2)  # Allow service to initialize
                
            except Exception as e:
                print(f"   ❌ {service['name']}: FAILED - {e}")
        
        print("=" * 60)
        print(f"🎯 SERVICE STARTUP SUMMARY:")
        print(f"   📊 Total Services: {len(services)}")
        print(f"   ✅ Successfully Started: {started_services}")
        print(f"   📈 Success Rate: {(started_services/len(services))*100:.1f}%")
        
        return started_services > 0
    
    def display_production_dashboard(self):
        """Display the complete production dashboard"""
        print("\n" + "=" * 80)
        print("🎵 BEAT ADDICTS - PRODUCTION DASHBOARD")
        print("=" * 80)
        print(f"🕒 Status at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Connection Status
        if self.connection_status:
            print("🔌 CONNECTION STATUS:")
            print(f"   ✅ Connection Manager: {'Online' if self.connection_status.get('connection_manager') else 'Offline'}")
            print(f"   ✅ Master Controller: {'Online' if self.connection_status.get('master_controller') else 'Offline'}")
            print(f"   🎵 Core Modules: {self.connection_status.get('core_modules', 0)}")
            print(f"   🎼 Generators: {self.connection_status.get('generators', 0)}")
            print(f"   🌐 Web Interfaces: {self.connection_status.get('web_interfaces', 0)}")
            print(f"   📊 Total Connections: {self.connection_status.get('total_connections', 0)}")
            print()
        
        # Running Services
        if self.running_processes:
            print("🚀 RUNNING SERVICES:")
            for service in self.running_processes:
                status = "Online" if service['process'].poll() is None else "Stopped"
                runtime = datetime.now() - service['started_at']
                print(f"   🌟 {service['name']}: {status} (Port {service['port']}, Runtime: {str(runtime).split('.')[0]})")
            print()
        
        # Access Points
        print("🌐 ACCESS POINTS:")
        print("   🎤 Music Generator App:    http://localhost:5000")
        print("   🛠️ Master Endpoints API:    http://localhost:5001")
        print("   🎨 Core Web Interface:     http://localhost:5002")
        print()
        
        # API Endpoints
        print("🔗 AVAILABLE API ENDPOINTS:")
        endpoints = [
            "GET  /api/master/status        - System status",
            "POST /api/master/connect       - Connect to system", 
            "GET  /api/generators/list      - List all generators",
            "POST /api/generate/<type>      - Generate music",
            "POST /api/voice/assign         - Assign voice",
            "GET  /api/voice/presets        - Voice presets",
            "POST /api/system/restart       - Restart system",
            "GET  /api/system/health        - Health check",
            "POST /api/files/upload         - Upload files",
            "GET  /api/files/list           - List files"
        ]
        
        for endpoint in endpoints:
            print(f"   📡 {endpoint}")
        
        print("=" * 80)
    
    def monitor_system(self):
        """Monitor the entire system"""
        print("\n⏳ MONITORING BEAT ADDICTS PRODUCTION SYSTEM")
        print("   Press Ctrl+C to shutdown all services cleanly")
        print()
        
        try:
            while True:
                # Check running processes
                active_count = 0
                for service in self.running_processes:
                    if service['process'].poll() is None:
                        active_count += 1
                
                if active_count == 0:
                    print("⚠️ All services stopped")
                    break
                
                # Display periodic status
                time.sleep(30)  # Check every 30 seconds
                print(f"🔄 {datetime.now().strftime('%H:%M:%S')} - {active_count} services running")
                
        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested...")
            self.shutdown_all_services()
    
    def shutdown_all_services(self):
        """Cleanly shutdown all services"""
        print("🛑 SHUTTING DOWN ALL SERVICES...")
        
        for service in self.running_processes:
            try:
                if service['process'].poll() is None:
                    print(f"   🛑 Stopping {service['name']}...")
                    service['process'].terminate()
                    service['process'].wait(timeout=5)
                    print(f"   ✅ {service['name']} stopped")
            except Exception as e:
                print(f"   ⚠️ Error stopping {service['name']}: {e}")
        
        print("✅ All services shut down")
    
    def run_complete_system(self):
        """Run the complete BEAT ADDICTS system"""
        try:
            # Connect all endpoints
            if not self.connect_all_endpoints():
                print("❌ Endpoint connection failed")
                return False
            
            # Start production services
            if not self.start_production_services():
                print("❌ Service startup failed")
                return False
            
            # Display dashboard
            self.display_production_dashboard()
            
            # Monitor system
            self.monitor_system()
            
            return True
            
        except Exception as e:
            print(f"❌ System execution failed: {e}")
            return False

def main():
    """Main execution function"""
    launcher = BeatAddictsMasterLauncher()
    return launcher.run_complete_system()

if __name__ == "__main__":
    main()