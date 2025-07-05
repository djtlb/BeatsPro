#!/usr/bin/env python3
"""
Comprehensive Debug and Test Script for Smart Music Generator AI
Tests all components, identifies issues, and provides solutions
"""

import os
import sys
import subprocess
import importlib
import traceback
import json
import time
from pathlib import Path
from typing import List, Dict, Tuple

class ProjectDebugger:
    """Comprehensive project debugging and testing"""
    
    def __init__(self):
        self.results = {
            "environment": {},
            "dependencies": {},
            "files": {},
            "modules": {},
            "functionality": {},
            "performance": {},
            "issues": [],
            "recommendations": []
        }
        
    def print_section(self, title: str):
        """Print formatted section header"""
        print(f"\n{'='*80}")
        print(f"🔍 {title}")
        print('='*80)
    
    def print_test(self, test_name: str, status: str, details: str = ""):
        """Print test result with status"""
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name:<40} [{status}]")
        if details:
            print(f"   {details}")
    
    def test_environment(self):
        """Test Python environment and system info"""
        self.print_section("ENVIRONMENT TESTING")
        
        # Python version
        py_version = sys.version
        self.results["environment"]["python_version"] = py_version
        self.print_test("Python Version", "PASS", f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        
        # Platform info
        import platform
        self.results["environment"]["platform"] = platform.system()
        self.print_test("Platform", "PASS", platform.system())
        
        # Working directory
        cwd = os.getcwd()
        self.results["environment"]["working_directory"] = cwd
        self.print_test("Working Directory", "PASS", cwd)
        
        # Available memory
        try:
            import psutil
            memory = psutil.virtual_memory()
            self.results["environment"]["memory_gb"] = round(memory.total / (1024**3), 1)
            self.print_test("Available Memory", "PASS", f"{round(memory.total / (1024**3), 1)} GB")
        except ImportError:
            self.print_test("Memory Check", "SKIP", "psutil not available")
        
        # GPU detection
        try:
            import tensorflow as tf
            gpus = tf.config.list_physical_devices('GPU')
            self.results["environment"]["gpu_count"] = len(gpus)
            if gpus:
                self.print_test("GPU Detection", "PASS", f"{len(gpus)} GPU(s) found")
            else:
                self.print_test("GPU Detection", "INFO", "No GPU found (CPU training)")
        except:
            self.print_test("GPU Detection", "SKIP", "TensorFlow not available")
    
    def test_dependencies(self):
        """Test all required dependencies"""
        self.print_section("DEPENDENCY TESTING")
        
        required_packages = {
            "numpy": "Scientific computing",
            "tensorflow": "Machine learning framework",
            "flask": "Web framework",
            "pretty_midi": "MIDI processing",
            "mido": "MIDI I/O",
            "scipy": "Scientific computing",
            "librosa": "Audio processing (optional)"
        }
        
        for package, description in required_packages.items():
            try:
                module = importlib.import_module(package)
                version = getattr(module, '__version__', 'Unknown')
                self.results["dependencies"][package] = {"status": "installed", "version": version}
                self.print_test(f"{package}", "PASS", f"v{version}")
            except ImportError as e:
                self.results["dependencies"][package] = {"status": "missing", "error": str(e)}
                self.print_test(f"{package}", "FAIL", f"Not installed - {description}")
                self.results["issues"].append(f"Missing dependency: {package}")
    
    def test_file_structure(self):
        """Test project file structure and integrity"""
        self.print_section("FILE STRUCTURE TESTING")
        
        required_files = {
            "run.py": "Main entry point",
            "music_generator.py": "Core AI model",
            "midi_processor.py": "MIDI processing",
            "web_interface.py": "Web interface",
            "dnb_midi_generator.py": "DNB dataset generator",
            "requirements.txt": "Dependencies list",
            "README.md": "Documentation"
        }
        
        required_dirs = {
            "templates": "Web templates",
            "models": "AI models storage",
            "midi_files": "Training data"
        }
        
        # Test files
        for file_path, description in required_files.items():
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                self.results["files"][file_path] = {"exists": True, "size": size}
                self.print_test(f"File: {file_path}", "PASS", f"{size:,} bytes - {description}")
            else:
                self.results["files"][file_path] = {"exists": False}
                self.print_test(f"File: {file_path}", "FAIL", f"Missing - {description}")
                self.results["issues"].append(f"Missing file: {file_path}")
        
        # Test directories
        for dir_path, description in required_dirs.items():
            if os.path.exists(dir_path):
                file_count = len(list(Path(dir_path).rglob('*')))
                self.results["files"][dir_path] = {"exists": True, "file_count": file_count}
                self.print_test(f"Directory: {dir_path}", "PASS", f"{file_count} items - {description}")
            else:
                self.results["files"][dir_path] = {"exists": False}
                self.print_test(f"Directory: {dir_path}", "FAIL", f"Missing - {description}")
                self.results["issues"].append(f"Missing directory: {dir_path}")
    
    def test_module_imports(self):
        """Test importing project modules"""
        self.print_section("MODULE IMPORT TESTING")
        
        project_modules = [
            "music_generator",
            "midi_processor", 
            "web_interface",
            "dnb_midi_generator"
        ]
        
        for module_name in project_modules:
            try:
                if os.path.exists(f"{module_name}.py"):
                    # Add current directory to path
                    sys.path.insert(0, os.getcwd())
                    module = importlib.import_module(module_name)
                    self.results["modules"][module_name] = {"status": "success", "path": module.__file__}
                    self.print_test(f"Import: {module_name}", "PASS", "Module imported successfully")
                else:
                    self.results["modules"][module_name] = {"status": "file_missing"}
                    self.print_test(f"Import: {module_name}", "FAIL", "File does not exist")
            except Exception as e:
                self.results["modules"][module_name] = {"status": "error", "error": str(e)}
                self.print_test(f"Import: {module_name}", "FAIL", str(e))
                self.results["issues"].append(f"Module import error: {module_name} - {e}")
    
    def test_midi_functionality(self):
        """Test MIDI generation and processing"""
        self.print_section("MIDI FUNCTIONALITY TESTING")
        
        # Test all generators
        generators_to_test = [
            ('dnb_midi_generator', 'DrumAndBassMIDIGenerator', 'DNB'),
            ('hiphop_midi_generator', 'HipHopMIDIGenerator', 'Hip-Hop'),
            ('electronic_midi_generator', 'ElectronicMIDIGenerator', 'Electronic'),
            ('country_midi_generator', 'CountryMIDIGenerator', 'Country'),
            ('rock_midi_generator', 'RockMIDIGenerator', 'Rock'),
            ('futuristic_midi_generator', 'FuturisticMIDIGenerator', 'Futuristic')
        ]
        
        working_generators = 0
        total_generators = len(generators_to_test)
        
        for module_name, class_name, genre_name in generators_to_test:
            try:
                if os.path.exists(f"{module_name}.py"):
                    try:
                        module = __import__(module_name)
                        generator_class = getattr(module, class_name)
                        generator = generator_class()
                        self.print_test(f"{genre_name} Generator", "PASS", "Generator class available")
                        working_generators += 1
                    except Exception as e:
                        self.print_test(f"{genre_name} Generator", "FAIL", str(e))
                        self.results["issues"].append(f"{genre_name} generator error: {e}")
                else:
                    self.print_test(f"{genre_name} Generator", "SKIP", "Module file not found")
            except Exception as e:
                self.print_test(f"{genre_name} Generator", "FAIL", str(e))
        
        # Test universal generator
        try:
            if os.path.exists("universal_midi_generator.py"):
                from universal_midi_generator import UniversalMIDIGenerator
                universal = UniversalMIDIGenerator()
                self.print_test("Universal Generator", "PASS", f"{len(universal.available_genres)} genres loaded")
            else:
                self.print_test("Universal Generator", "SKIP", "Module not found")
        except Exception as e:
            self.print_test("Universal Generator", "FAIL", str(e))
        
        # Test MIDI files
        midi_dir = Path("midi_files")
        if midi_dir.exists():
            midi_files = list(midi_dir.glob("*.mid"))
            self.print_test("MIDI Files Found", "PASS", f"{len(midi_files)} files")
            
            # Test file loading
            if midi_files:
                try:
                    import pretty_midi
                    test_file = midi_files[0]
                    midi_data = pretty_midi.PrettyMIDI(str(test_file))
                    self.print_test("MIDI File Loading", "PASS", f"Loaded {test_file.name}")
                except Exception as e:
                    self.print_test("MIDI File Loading", "FAIL", str(e))
        else:
            self.print_test("MIDI Files Found", "FAIL", "No midi_files directory")
        
        self.results["functionality"]["midi_generators"] = {
            "working": working_generators,
            "total": total_generators
        }

    def test_ai_functionality(self):
        """Test AI model functionality"""
        self.print_section("AI MODEL TESTING")
        
        try:
            if os.path.exists("music_generator.py"):
                try:
                    from music_generator import SmartMusicGenerator
                    generator = SmartMusicGenerator()
                    self.print_test("AI Generator Import", "PASS", "SmartMusicGenerator available")
                    
                    # Test model info
                    info = generator.get_model_info()
                    if info:
                        self.print_test("Model Info", "PASS", f"Vocab size: {info.get('vocab_size', 'Unknown')}")
                    
                except Exception as e:
                    self.print_test("AI Generator Import", "FAIL", str(e))
                    self.results["issues"].append(f"AI generator error: {e}")
        except Exception as e:
            self.print_test("AI Testing", "FAIL", str(e))
    
    def test_web_interface(self):
        """Test web interface functionality"""
        self.print_section("WEB INTERFACE TESTING")
        
        try:
            if os.path.exists("web_interface.py"):
                try:
                    from web_interface import app
                    self.print_test("Flask App Import", "PASS", "Web app available")
                    
                    # Test template exists
                    template_path = Path("templates/index.html")
                    if template_path.exists():
                        self.print_test("HTML Template", "PASS", "index.html found")
                    else:
                        self.print_test("HTML Template", "FAIL", "index.html missing")
                        self.results["issues"].append("Missing HTML template")
                    
                except Exception as e:
                    self.print_test("Flask App Import", "FAIL", str(e))
                    self.results["issues"].append(f"Web interface error: {e}")
        except Exception as e:
            self.print_test("Web Interface Testing", "FAIL", str(e))
    
    def performance_benchmark(self):
        """Run basic performance benchmarks"""
        self.print_section("PERFORMANCE BENCHMARKING")
        
        try:
            import numpy as np
            
            # NumPy benchmark
            start_time = time.time()
            arr = np.random.rand(1000, 1000)
            result = np.dot(arr, arr)
            numpy_time = time.time() - start_time
            self.results["performance"]["numpy_benchmark"] = numpy_time
            self.print_test("NumPy Performance", "PASS", f"{numpy_time:.3f}s for 1M x 1M matrix multiplication")
            
            # TensorFlow benchmark (if available)
            try:
                import tensorflow as tf
                start_time = time.time()
                a = tf.random.normal([1000, 1000])
                b = tf.random.normal([1000, 1000])
                c = tf.matmul(a, b)
                tf_time = time.time() - start_time
                self.results["performance"]["tensorflow_benchmark"] = tf_time
                self.print_test("TensorFlow Performance", "PASS", f"{tf_time:.3f}s for GPU/CPU computation")
            except:
                self.print_test("TensorFlow Performance", "SKIP", "TensorFlow not available")
                
        except Exception as e:
            self.print_test("Performance Benchmark", "FAIL", str(e))
    
    def generate_report(self):
        """Generate comprehensive debug report"""
        self.print_section("DEBUG REPORT SUMMARY")
        
        # Count issues
        total_issues = len(self.results["issues"])
        
        if total_issues == 0:
            print("🎉 NO ISSUES FOUND - Project is ready to use!")
        else:
            print(f"⚠️ {total_issues} ISSUES FOUND:")
            for i, issue in enumerate(self.results["issues"], 1):
                print(f"   {i}. {issue}")
        
        # Recommendations
        print(f"\n📋 RECOMMENDATIONS:")
        
        if not os.path.exists("models"):
            print("   • Create models directory: mkdir models")
        
        if "tensorflow" not in self.results["dependencies"] or self.results["dependencies"]["tensorflow"]["status"] != "installed":
            print("   • Install TensorFlow: pip install tensorflow")
        
        if not os.path.exists("midi_files") or len(list(Path("midi_files").glob("*.mid"))) == 0:
            print("   • Generate training data: python run.py --create-dnb")
        
        if total_issues > 0:
            print("   • Run installation fix: python install_fix.py")
        
        print("   • Start web interface: python run.py")
        
        # Save detailed report
        report_path = "debug_report.json"
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        return total_issues == 0
    
    def run_full_test(self):
        """Run all tests and generate report"""
        print("🎵 Smart Music Generator AI - Comprehensive Debug & Test")
        print("This will test all components and identify any issues...")
        
        try:
            self.test_environment()
            self.test_dependencies()
            self.test_file_structure()
            self.test_module_imports()
            self.test_midi_functionality()
            self.test_ai_functionality()
            self.test_web_interface()
            self.performance_benchmark()
            
            return self.generate_report()
            
        except Exception as e:
            print(f"\n❌ Debug testing failed: {e}")
            traceback.print_exc()
            return False

def main():
    """Main debug function"""
    debugger = ProjectDebugger()
    success = debugger.run_full_test()
    
    if success:
        print("\n🚀 All tests passed! Your project is ready to use.")
        print("Next steps:")
        print("1. python run.py --create-dnb  # Generate training data")
        print("2. python run.py              # Start web interface")
    else:
        print("\n🔧 Issues found. Please address the recommendations above.")
        print("Run: python install_fix.py for installation help")
    
    return success

if __name__ == "__main__":
    main()
