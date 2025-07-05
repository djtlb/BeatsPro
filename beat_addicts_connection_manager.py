#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Connection Manager
Centralized system for connecting all modules and their dependencies
"""

import os
import sys
import importlib
import importlib.util
import traceback
from typing import Dict, Any, Optional, List

class BeatAddictsConnectionManager:
    """Manages all connections between BEAT ADDICTS modules"""
    
    def __init__(self):
        self.connected_modules = {}
        self.failed_modules = {}
        self.connection_status = {}
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Add all necessary paths
        self._setup_paths()
        
    def _setup_paths(self):
        """Setup all necessary Python paths for imports"""
        paths_to_add = [
            self.base_path,
            os.path.join(self.base_path, 'beat_addicts_core'),
            os.path.join(self.base_path, 'beat_addicts_generators'),
            os.path.join(self.base_path, 'beat_addicts_tests'),
            os.path.join(self.base_path, 'sunoai-1.0.7')
        ]
        
        for path in paths_to_add:
            if os.path.exists(path) and path not in sys.path:
                sys.path.insert(0, path)
                print(f"✅ Added path: {path}")
    
    def connect_core_modules(self) -> Dict[str, Any]:
        """Connect all core BEAT ADDICTS modules"""
        print("🔌 Connecting BEAT ADDICTS Core Modules...")
        
        core_modules = {
            'voice_handler': 'voice_handler.BeatAddictsVoiceHandler',
            'voice_integration': 'voice_integration',  # Module, not class
            'song_exporter': 'song_exporter.BeatAddictsSongExporter',
            'simple_audio_generator': 'simple_audio_generator.BeatAddictsSimpleAudioGenerator'
        }
        
        connected = {}
        
        for module_name, module_path in core_modules.items():
            try:
                if '.' in module_path:
                    # Class-based module
                    module_parts = module_path.split('.')
                    module = importlib.import_module(module_parts[0])
                    class_name = module_parts[1]
                    module_class = getattr(module, class_name)
                    
                    # Instantiate the module
                    instance = module_class()
                    connected[module_name] = instance
                else:
                    # Function-based module
                    module = importlib.import_module(module_path)
                    connected[module_name] = module
                
                self.connected_modules[module_name] = connected[module_name]
                self.connection_status[module_name] = 'connected'
                print(f"✅ Connected: {module_name}")
                
            except Exception as e:
                print(f"❌ Failed to connect {module_name}: {e}")
                self.failed_modules[module_name] = str(e)
                self.connection_status[module_name] = 'failed'
        
        return connected
    
    def connect_generators(self) -> Dict[str, Any]:
        """Connect all BEAT ADDICTS genre generators"""
        print("🎵 Connecting BEAT ADDICTS Generators...")
        
        generators = {
            'universal': 'universal_midi_generator.BeatAddictsUniversalGenerator',
            'dnb': 'dnb_midi_generator.DrumAndBassMIDIGenerator',
            'hiphop': 'hiphop_midi_generator.HipHopMIDIGenerator',
            'electronic': 'electronic_midi_generator.ElectronicMIDIGenerator',
            'rock': 'rock_midi_generator.RockMIDIGenerator',
            'country': 'country_midi_generator.CountryMIDIGenerator',
            'futuristic': 'futuristic_midi_generator.FuturisticMIDIGenerator'
        }
        
        connected = {}
        
        for gen_name, gen_path in generators.items():
            try:
                module_parts = gen_path.split('.')
                module = importlib.import_module(module_parts[0])
                class_name = module_parts[1]
                gen_class = getattr(module, class_name)
                
                # Instantiate the generator
                instance = gen_class()
                connected[gen_name] = instance
                self.connected_modules[f'generator_{gen_name}'] = instance
                self.connection_status[f'generator_{gen_name}'] = 'connected'
                print(f"✅ Connected generator: {gen_name}")
                
            except Exception as e:
                print(f"❌ Failed to connect {gen_name} generator: {e}")
                self.failed_modules[f'generator_{gen_name}'] = str(e)
                self.connection_status[f'generator_{gen_name}'] = 'failed'
        
        return connected
    
    def connect_web_interfaces(self) -> Dict[str, Any]:
        """Connect web interface modules"""
        print("🌐 Connecting BEAT ADDICTS Web Interfaces...")
        
        web_modules = [
            'beat_addicts_core/web_interface.py',
            'master_endpoints.py'
        ]
        
        connected = {}
        
        for web_module in web_modules:
            try:
                if os.path.exists(os.path.join(self.base_path, web_module)):
                    module_name = os.path.basename(web_module).replace('.py', '')
                    spec = importlib.util.spec_from_file_location(
                        module_name, 
                        os.path.join(self.base_path, web_module)
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        connected[module_name] = module
                        self.connected_modules[f'web_{module_name}'] = module
                        self.connection_status[f'web_{module_name}'] = 'connected'
                        print(f"✅ Connected web module: {module_name}")
                        
            except Exception as e:
                print(f"❌ Failed to connect web module {web_module}: {e}")
                self.failed_modules[f'web_{web_module}'] = str(e)
                self.connection_status[f'web_{web_module}'] = 'failed'
        
        return connected
    
    def connect_all(self) -> Dict[str, Dict[str, Any]]:
        """Connect all BEAT ADDICTS modules"""
        print("🎵 BEAT ADDICTS - UNIVERSAL CONNECTION MANAGER")
        print("=" * 60)
        
        all_connections = {
            'core': self.connect_core_modules(),
            'generators': self.connect_generators(),
            'web': self.connect_web_interfaces()
        }
        
        # Connection summary
        total_attempted = sum(len(cat) for cat in all_connections.values())
        total_connected = sum(len([m for m in cat.values() if m is not None]) for cat in all_connections.values())
        total_failed = len(self.failed_modules)
        
        print("=" * 60)
        print(f"🎯 CONNECTION SUMMARY:")
        print(f"   📊 Total Attempted: {total_attempted}")
        print(f"   ✅ Successfully Connected: {total_connected}")
        print(f"   ❌ Failed Connections: {total_failed}")
        print(f"   📈 Success Rate: {(total_connected/total_attempted)*100:.1f}%")
        
        if self.failed_modules:
            print(f"\n⚠️ FAILED CONNECTIONS:")
            for module, error in self.failed_modules.items():
                print(f"   ❌ {module}: {error[:100]}")
        
        print("=" * 60)
        
        return all_connections
    
    def get_connection_report(self) -> Dict[str, Any]:
        """Get detailed connection report"""
        return {
            'connected_modules': list(self.connected_modules.keys()),
            'failed_modules': self.failed_modules,
            'connection_status': self.connection_status,
            'total_connected': len(self.connected_modules),
            'total_failed': len(self.failed_modules),
            'success_rate': len(self.connected_modules) / (len(self.connected_modules) + len(self.failed_modules)) * 100 if (len(self.connected_modules) + len(self.failed_modules)) > 0 else 0
        }
    
    def test_connections(self) -> Dict[str, bool]:
        """Test all connected modules"""
        print("🧪 Testing BEAT ADDICTS module connections...")
        
        test_results = {}
        
        for module_name, module_instance in self.connected_modules.items():
            try:
                # Basic test - try to call a common method or check attributes
                if hasattr(module_instance, '__dict__'):
                    test_results[module_name] = True
                    print(f"✅ {module_name}: OK")
                else:
                    test_results[module_name] = False
                    print(f"⚠️ {module_name}: No attributes")
                    
            except Exception as e:
                test_results[module_name] = False
                print(f"❌ {module_name}: Test failed - {e}")
        
        return test_results

def main():
    """Main connection manager execution"""
    manager = BeatAddictsConnectionManager()
    connections = manager.connect_all()
    
    # Test connections
    test_results = manager.test_connections()
    
    # Generate report
    report = manager.get_connection_report()
    
    print("🎵 BEAT ADDICTS Connection Manager Complete!")
    return manager, connections, test_results, report

if __name__ == "__main__":
    main()
