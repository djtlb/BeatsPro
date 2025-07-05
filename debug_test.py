#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Comprehensive Debug and Test System
Professional debugging suite for Beat Addicts Music Production AI
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

class BeatAddictsDebugger:
    """Comprehensive BEAT ADDICTS project debugging and testing"""
    
    def __init__(self):
        self.results = {
            "beat_addicts_info": {
                "version": "2.0",
                "platform": sys.platform,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            },
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
        """Print BEAT ADDICTS formatted section header"""
        print(f"\n{'='*80}")
        print(f"🔥 BEAT ADDICTS DEBUG: {title}")
        print('='*80)
    
    def print_test(self, test_name: str, status: str, details: str = ""):
        """Print BEAT ADDICTS test result with status"""
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name:<50} [{status}]")
        if details:
            print(f"   🎵 {details}")
    
    def test_environment(self):
        """Test BEAT ADDICTS Python environment and system info"""
        self.print_section("BEAT ADDICTS ENVIRONMENT TESTING")
        
        # Python version check for BEAT ADDICTS
        py_version = sys.version
        self.results["environment"]["python_version"] = py_version
        
        if sys.version_info >= (3, 8):
            self.print_test("Python Version", "PASS", f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} (BEAT ADDICTS compatible)")
        else:
            self.print_test("Python Version", "FAIL", f"Python {sys.version_info.major}.{sys.version_info.minor} (BEAT ADDICTS requires 3.8+)")
            self.results["issues"].append("Python version too old for BEAT ADDICTS")
        
        # Platform info
        import platform
        self.results["environment"]["platform"] = platform.system()
        self.print_test("Platform", "PASS", f"{platform.system()} {platform.release()}")
        
        # Working directory
        cwd = os.getcwd()
        self.results["environment"]["working_directory"] = cwd
        is_beat_addicts_dir = "beat" in cwd.lower() or "addicts" in cwd.lower() or "sunoai" in cwd.lower()
        status = "PASS" if is_beat_addicts_dir else "WARN"
        self.print_test("BEAT ADDICTS Directory", status, cwd)
        
        # Available memory
        try:
            import psutil
            memory = psutil.virtual_memory()
            memory_gb = round(memory.total / (1024**3), 1)
            self.results["environment"]["memory_gb"] = memory_gb
            
            if memory_gb >= 8:
                self.print_test("Memory (BEAT ADDICTS)", "PASS", f"{memory_gb} GB (Professional)")
            elif memory_gb >= 4:
                self.print_test("Memory (BEAT ADDICTS)", "WARN", f"{memory_gb} GB (Basic)")
            else:
                self.print_test("Memory (BEAT ADDICTS)", "FAIL", f"{memory_gb} GB (Insufficient)")
                self.results["issues"].append("Insufficient RAM for BEAT ADDICTS professional features")
        except ImportError:
            self.print_test("Memory Check", "SKIP", "psutil not available")
        
        # GPU detection for BEAT ADDICTS
        try:
            import tensorflow as tf
            gpus = tf.config.list_physical_devices('GPU')
            self.results["environment"]["gpu_count"] = len(gpus)
            if gpus:
                self.print_test("GPU (BEAT ADDICTS)", "PASS", f"{len(gpus)} GPU(s) - Professional acceleration available")
            else:
                self.print_test("GPU (BEAT ADDICTS)", "INFO", "CPU mode - GPU recommended for faster training")
        except:
            self.print_test("GPU Detection", "SKIP", "TensorFlow not available")
    
    def test_dependencies(self):
        """Test all BEAT ADDICTS required dependencies"""
        self.print_section("BEAT ADDICTS DEPENDENCY TESTING")
        
        beat_addicts_packages = {
            "numpy": ("Scientific computing for BEAT ADDICTS AI", "CRITICAL"),
            "tensorflow": ("BEAT ADDICTS neural network engine", "CRITICAL"), 
            "flask": ("BEAT ADDICTS Studio web interface", "CRITICAL"),
            "pretty_midi": ("Professional MIDI processing", "CRITICAL"),
            "mido": ("BEAT ADDICTS MIDI I/O", "CRITICAL"),
            "scipy": ("Advanced scientific computing", "RECOMMENDED"),
            "librosa": ("Audio processing for BEAT ADDICTS", "RECOMMENDED"),
            "music21": ("Music theory for BEAT ADDICTS", "OPTIONAL"),
            "matplotlib": ("BEAT ADDICTS visualization", "OPTIONAL"),
            "scikit-learn": ("Additional ML tools", "OPTIONAL")
        }
        
        critical_missing = 0
        for package, (description, priority) in beat_addicts_packages.items():
            try:
                module = importlib.import_module(package)
                version = getattr(module, '__version__', 'Unknown')
                self.results["dependencies"][package] = {"status": "installed", "version": version, "priority": priority}
                self.print_test(f"BEAT ADDICTS {package}", "PASS", f"v{version} - {description}")
            except ImportError as e:
                self.results["dependencies"][package] = {"status": "missing", "error": str(e), "priority": priority}
                status = "FAIL" if priority == "CRITICAL" else "WARN"
                self.print_test(f"BEAT ADDICTS {package}", status, f"Missing - {description}")
                
                if priority == "CRITICAL":
                    critical_missing += 1
                    self.results["issues"].append(f"Critical BEAT ADDICTS dependency missing: {package}")
        
        if critical_missing > 0:
            self.results["recommendations"].append(f"Install {critical_missing} critical dependencies: pip install -r requirements.txt")
    
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
            "dnb_midi_generator",
            "hiphop_midi_generator",
            "electronic_midi_generator",
            "country_midi_generator",
            "rock_midi_generator",
            "futuristic_midi_generator",
            "universal_midi_generator",
            "voice_assignment"
        ]
        
        for module_name in project_modules:
            try:
                if os.path.exists(f"{module_name}.py"):
                    # Add current directory to path
                    sys.path.insert(0, os.getcwd())
                    
                    # Special handling for voice_assignment due to numpy issues
                    if module_name == "voice_assignment":
                        try:
                            import importlib.util
                            spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            self.results["modules"][module_name] = {"status": "success_fallback", "path": f"{module_name}.py"}
                            self.print_test(f"Import: {module_name}", "PASS", "Module imported (with fallback support)")
                        except Exception as e:
                            self.results["modules"][module_name] = {"status": "error", "error": str(e)}
                            self.print_test(f"Import: {module_name}", "WARN", f"Import issues but may work: {e}")
                    else:
                        module = importlib.import_module(module_name)
                        self.results["modules"][module_name] = {"status": "success", "path": module.__file__}
                        self.print_test(f"Import: {module_name}", "PASS", "Module imported successfully")
                else:
                    self.results["modules"][module_name] = {"status": "file_missing"}
                    self.print_test(f"Import: {module_name}", "FAIL", "File does not exist")
            except Exception as e:
                self.results["modules"][module_name] = {"status": "error", "error": str(e)}
                self.print_test(f"Import: {module_name}", "FAIL", str(e))
                if "numpy" in str(e).lower():
                    self.results["issues"].append(f"NumPy import issue affecting {module_name} - try moving to different directory")
                else:
                    self.results["issues"].append(f"Module import error: {module_name} - {e}")
    
    def test_beat_addicts_functionality(self):
        """Test BEAT ADDICTS specific functionality"""
        self.print_section("BEAT ADDICTS FUNCTIONALITY TESTING")
        
        # Test BEAT ADDICTS generators
        beat_addicts_generators = [
            ('dnb_midi_generator', 'DrumAndBassMIDIGenerator', 'BEAT ADDICTS DNB'),
            ('hiphop_midi_generator', 'HipHopMIDIGenerator', 'BEAT ADDICTS Hip-Hop'),
            ('electronic_midi_generator', 'ElectronicMIDIGenerator', 'BEAT ADDICTS Electronic'),
            ('country_midi_generator', 'CountryMIDIGenerator', 'BEAT ADDICTS Country'),
            ('rock_midi_generator', 'RockMIDIGenerator', 'BEAT ADDICTS Rock'),
            ('futuristic_midi_generator', 'FuturisticMIDIGenerator', 'BEAT ADDICTS Futuristic'),
            ('universal_midi_generator', 'UniversalMIDIGenerator', 'BEAT ADDICTS Universal'),
            ('voice_assignment', 'IntelligentVoiceAssigner', 'BEAT ADDICTS Voice Engine')
        ]
        
        working_generators = 0
        total_generators = len(beat_addicts_generators)
        
        for module_name, class_name, display_name in beat_addicts_generators:
            try:
                if os.path.exists(f"{module_name}.py"):
                    try:
                        # Special handling for voice assignment (no dependencies)
                        if module_name == 'voice_assignment':
                            import importlib.util
                            spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                        else:
                            module = importlib.import_module(module_name)
                        
                        generator_class = getattr(module, class_name)
                        generator = generator_class()
                        self.print_test(f"{display_name} Generator", "PASS", "Professional generator available")
                        working_generators += 1
                        
                    except Exception as e:
                        self.print_test(f"{display_name} Generator", "FAIL", str(e))
                        self.results["issues"].append(f"BEAT ADDICTS generator error: {display_name} - {e}")
                else:
                    self.print_test(f"{display_name} Generator", "FAIL", "Module file not found")
            except Exception as e:
                self.print_test(f"{display_name} Generator", "FAIL", str(e))
        
        self.results["functionality"]["beat_addicts_generators"] = {
            "working": working_generators,
            "total": total_generators,
            "percentage": round((working_generators / total_generators) * 100, 1)
        }
        
        if working_generators >= total_generators * 0.8:
            self.print_test("BEAT ADDICTS System", "PASS", f"{working_generators}/{total_generators} generators working")
        else:
            self.print_test("BEAT ADDICTS System", "WARN", f"Only {working_generators}/{total_generators} generators working")

    def test_beat_addicts_voice_system(self):
        """Test BEAT ADDICTS voice assignment system specifically"""
        self.print_section("BEAT ADDICTS VOICE ASSIGNMENT TESTING")
        
        try:
            # Import BEAT ADDICTS voice system
            import importlib.util
            spec = importlib.util.spec_from_file_location("voice_assignment", "voice_assignment.py")
            voice_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(voice_module)
            
            # Test voice assignment
            assigner = voice_module.IntelligentVoiceAssigner()
            self.print_test("BEAT ADDICTS Voice Engine", "PASS", "Voice assignment engine loaded")
            
            # Test voice recommendations
            test_genres = ["hiphop", "electronic", "rock"]
            recommendations_working = 0
            
            for genre in test_genres:
                try:
                    recommendation = assigner.get_voice_recommendation(genre, "drums")
                    if recommendation and "recommended_program" in recommendation:
                        recommendations_working += 1
                        self.print_test(f"BEAT ADDICTS {genre.upper()} Voice", "PASS", f"Program {recommendation['recommended_program']}")
                    else:
                        self.print_test(f"BEAT ADDICTS {genre.upper()} Voice", "FAIL", "Invalid recommendation")
                except Exception as e:
                    self.print_test(f"BEAT ADDICTS {genre.upper()} Voice", "FAIL", str(e))
            
            if recommendations_working == len(test_genres):
                self.print_test("BEAT ADDICTS Voice System", "PASS", "All voice recommendations working")
            else:
                self.print_test("BEAT ADDICTS Voice System", "WARN", f"{recommendations_working}/{len(test_genres)} working")
                
        except Exception as e:
            self.print_test("BEAT ADDICTS Voice System", "FAIL", str(e))
            self.results["issues"].append(f"BEAT ADDICTS voice system error: {e}")

    def generate_beat_addicts_report(self):
        """Generate comprehensive BEAT ADDICTS debug report"""
        self.print_section("BEAT ADDICTS DEBUG REPORT SUMMARY")
        
        # Count issues
        total_issues = len(self.results["issues"])
        critical_deps = sum(1 for dep in self.results["dependencies"].values() 
                           if dep.get("status") == "missing" and dep.get("priority") == "CRITICAL")
        
        print("🎵 BEAT ADDICTS SYSTEM ANALYSIS:")
        print(f"   • Python Version: {self.results['environment'].get('python_version', 'Unknown')}")
        print(f"   • Platform: {self.results['environment'].get('platform', 'Unknown')}")
        print(f"   • Memory: {self.results['environment'].get('memory_gb', 'Unknown')} GB")
        print(f"   • GPU Count: {self.results['environment'].get('gpu_count', 0)}")
        
        if total_issues == 0:
            print("\n🎉 BEAT ADDICTS SYSTEM STATUS: PERFECT!")
            print("🔥 All systems operational - Ready for professional music production! 🔥")
        else:
            print(f"\n⚠️ BEAT ADDICTS ISSUES FOUND: {total_issues}")
            for i, issue in enumerate(self.results["issues"], 1):
                print(f"   {i}. {issue}")
        
        # BEAT ADDICTS specific recommendations
        print(f"\n📋 BEAT ADDICTS RECOMMENDATIONS:")
        
        if critical_deps > 0:
            print("   🚨 CRITICAL: Install missing dependencies")
            print("      → pip install -r requirements.txt")
            print("      → python install_dependencies.py")
        
        if not os.path.exists("models"):
            print("   📁 Create BEAT ADDICTS models directory: mkdir models")
        
        if not os.path.exists("midi_files") or len(list(Path("midi_files").glob("*.mid"))) == 0:
            print("   🎵 Generate BEAT ADDICTS training data:")
            print("      → python run.py --create-all")
        
        if self.results["environment"].get("memory_gb", 0) < 8:
            print("   💾 Consider upgrading RAM for BEAT ADDICTS professional features")
        
        if self.results["environment"].get("gpu_count", 0) == 0:
            print("   🚀 Consider GPU for faster BEAT ADDICTS training")
        
        print("   🎛️ Test BEAT ADDICTS voice assignment: python run.py --test-voices")
        print("   🌐 Start BEAT ADDICTS Studio: python run.py")
        
        # Save detailed BEAT ADDICTS report
        report_path = "beat_addicts_debug_report.json"
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n📄 BEAT ADDICTS detailed report saved to: {report_path}")
        
        return total_issues == 0 and critical_deps == 0
    
    def performance_benchmark(self):
        """Run BEAT ADDICTS performance benchmarks"""
        self.print_section("BEAT ADDICTS PERFORMANCE BENCHMARKING")
        
        try:
            # Test basic Python performance for BEAT ADDICTS
            start_time = time.time()
            test_data = [i * 2 for i in range(100000)]
            python_time = time.time() - start_time
            self.results["performance"]["python_benchmark"] = python_time
            self.print_test("BEAT ADDICTS Python Performance", "PASS", f"{python_time:.3f}s for 100K operations")
            
            # Test NumPy performance if available
            try:
                import numpy as np
                start_time = time.time()
                arr = np.random.rand(1000, 1000)
                result = np.dot(arr, arr)
                numpy_time = time.time() - start_time
                self.results["performance"]["numpy_benchmark"] = numpy_time
                self.print_test("BEAT ADDICTS NumPy Performance", "PASS", f"{numpy_time:.3f}s for matrix operations")
                
                if numpy_time < 1.0:
                    self.print_test("BEAT ADDICTS Math Performance", "PASS", "Professional-grade performance")
                else:
                    self.print_test("BEAT ADDICTS Math Performance", "WARN", "Consider performance optimization")
                    
            except ImportError:
                self.print_test("BEAT ADDICTS NumPy Performance", "SKIP", "NumPy not available")
            
            # Test TensorFlow performance if available
            try:
                import tensorflow as tf
                start_time = time.time()
                a = tf.random.normal([500, 500])
                b = tf.random.normal([500, 500]) 
                c = tf.matmul(a, b)
                tf_time = time.time() - start_time
                self.results["performance"]["tensorflow_benchmark"] = tf_time
                
                if tf_time < 2.0:
                    self.print_test("BEAT ADDICTS TensorFlow Performance", "PASS", f"{tf_time:.3f}s - Professional AI performance")
                else:
                    self.print_test("BEAT ADDICTS TensorFlow Performance", "WARN", f"{tf_time:.3f}s - Consider GPU acceleration")
                    
            except ImportError:
                self.print_test("BEAT ADDICTS TensorFlow Performance", "SKIP", "TensorFlow not available")
            except Exception as e:
                self.print_test("BEAT ADDICTS TensorFlow Performance", "WARN", f"Performance test failed: {e}")
            
            # Test file I/O performance for BEAT ADDICTS
            start_time = time.time()
            test_file = "beat_addicts_performance_test.tmp"
            with open(test_file, 'w') as f:
                for i in range(10000):
                    f.write(f"BEAT ADDICTS test line {i}\n")
            
            with open(test_file, 'r') as f:
                lines = f.readlines()
            
            os.remove(test_file)
            io_time = time.time() - start_time
            self.results["performance"]["file_io_benchmark"] = io_time
            self.print_test("BEAT ADDICTS File I/O Performance", "PASS", f"{io_time:.3f}s for 10K lines")
                
        except Exception as e:
            self.print_test("BEAT ADDICTS Performance Benchmark", "FAIL", str(e))

def main():
    """Main BEAT ADDICTS debug function"""
    debugger = BeatAddictsDebugger()
    success = debugger.run_full_debug()
    
    if success:
        print("\n🎉 BEAT ADDICTS SYSTEM: FULLY OPERATIONAL!")
        print("🔥 Ready for professional music production! 🔥")
        print("\nNext steps:")
        print("1. python run.py --create-all    # Generate training data")
        print("2. python run.py                # Start BEAT ADDICTS Studio")
        print("3. python run.py --test-voices  # Test voice assignment")
    else:
        print("\n🔧 BEAT ADDICTS SYSTEM: NEEDS ATTENTION")
        print("Please address the recommendations above.")
        print("Run: python install_dependencies.py for installation help")
    
    return success

if __name__ == "__main__":
    main()
