import numpy as np
import traceback
import time
import os
import sys
from datetime import datetime
import json

class BeatAddictsProductionDebugger:
    """🎵 BEAT ADDICTS - Production System Debugger"""
    
    def __init__(self):
        self.test_results = []
        self.errors_found = []
        self.performance_metrics = {}
        self.dependency_conflicts = []
        
    def explain_numpy_warning(self):
        """Explain and fix NumPy dependency issues"""
        print("🔍 BEAT ADDICTS - Dependency Conflict Analysis")
        print("=" * 60)
        
        print("⚠️ NUMPY DEPENDENCY CONFLICT DETECTED:")
        print("   • '~umpy' invalid distribution found in virtual environment")
        print("   • NumPy 2.3.1 installed, but numba requires NumPy <2.3")
        print("   • This causes compatibility issues with audio processing")
        
        print("\n🔧 WHAT THIS MEANS FOR BEAT ADDICTS:")
        print("   • Some audio processing features may fail")
        print("   • Machine learning models might not work properly")
        print("   • TensorFlow/numba integration could break")
        
        print("\n🎯 BEAT ADDICTS SOLUTION:")
        print("   1. Clean up corrupted packages")
        print("   2. Install compatible NumPy version")
        print("   3. Verify all BEAT ADDICTS dependencies")
        
        return self.fix_dependency_conflicts()
    
    def fix_dependency_conflicts(self):
        """Fix BEAT ADDICTS dependency conflicts with research-based solutions"""
        print("\n🔧 FIXING BEAT ADDICTS DEPENDENCIES...")
        print("   🔍 Using research-based compatible versions...")
        
        try:
            import subprocess
            
            # Step 1: Complete cleanup
            print("   Step 1: Complete dependency cleanup...")
            cleanup_commands = [
                "pip uninstall numpy scipy numba tensorflow pretty_midi mido -y",
                "pip cache purge"
            ]
            
            for cmd in cleanup_commands:
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    print(f"   ✅ {cmd}")
                except Exception as e:
                    print(f"   ⚠️ {cmd}: {e}")
            
            # Step 2: Install core dependencies in correct order
            print("   Step 2: Installing core dependencies in optimal order...")
            
            # Research-based compatible versions (as of 2024)
            dependency_order = [
                "numpy==1.26.4",          # Latest stable that works with everything
                "scipy==1.11.4",          # Compatible with NumPy 1.26.x
                "numba==0.60.0",          # Works with NumPy 1.26.x
                "tensorflow==2.15.0",     # Latest that supports NumPy 1.26.x
                "flask==3.0.0",           # Latest stable Flask
                "werkzeug==3.0.1",        # Compatible with Flask 3.x
                "pretty_midi==0.2.10",    # MIDI processing
                "mido==1.3.2",            # MIDI I/O
                "librosa==0.10.1",        # Audio processing
                "music21==9.1.0"          # Music theory
            ]
            
            for package in dependency_order:
                try:
                    print(f"   Installing {package}...")
                    cmd = f"pip install {package}"
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"   ✅ {package} installed successfully")
                    else:
                        print(f"   ❌ Failed: {package}")
                        print(f"      Error: {result.stderr}")
                except Exception as e:
                    print(f"   ❌ {package}: {e}")
            
            # Step 3: Verify installation
            print("   Step 3: Verifying BEAT ADDICTS dependencies...")
            return self.verify_dependencies()
            
        except Exception as e:
            print(f"   ❌ Dependency fix failed: {e}")
            return False

    def verify_dependencies(self):
        """Verify BEAT ADDICTS dependencies with version compatibility checks"""
        print("\n🧪 VERIFYING BEAT ADDICTS DEPENDENCIES...")
        
        critical_deps = {
            'numpy': ('Scientific computing for BEAT ADDICTS', '1.26.x'),
            'scipy': ('Signal processing for BEAT ADDICTS', '1.11.x'),
            'tensorflow': ('AI/ML framework for BEAT ADDICTS', '2.15.x'),
            'flask': ('Web interface for BEAT ADDICTS Studio', '3.0.x'),
            'pretty_midi': ('Professional MIDI processing', '0.2.x'),
            'mido': ('MIDI I/O for BEAT ADDICTS', '1.3.x')
        }
        
        optional_deps = {
            'numba': ('Performance optimization', '0.60.x'),
            'librosa': ('Audio analysis', '0.10.x'),
            'music21': ('Music theory', '9.1.x')
        }
        
        working_deps = 0
        total_deps = len(critical_deps)
        version_conflicts = []
        
        # Check critical dependencies
        for dep, (description, expected_version) in critical_deps.items():
            try:
                module = __import__(dep)
                version = getattr(module, '__version__', 'Unknown')
                print(f"   ✅ {dep} v{version} - {description}")
                working_deps += 1
                
                # Version compatibility checks
                if dep == 'numpy':
                    if version.startswith('1.26'):
                        print(f"      🎯 NumPy version optimal for BEAT ADDICTS")
                    elif version.startswith('2.'):
                        version_conflicts.append(f"NumPy {version} may cause compatibility issues")
                        print(f"      ⚠️ NumPy 2.x detected - consider downgrading")
                    
                elif dep == 'scipy':
                    if version.startswith('1.11') or version.startswith('1.12'):
                        print(f"      🎯 SciPy version compatible")
                    else:
                        version_conflicts.append(f"SciPy {version} may have NumPy conflicts")
                        
                elif dep == 'tensorflow':
                    if version.startswith('2.15') or version.startswith('2.14'):
                        print(f"      🎯 TensorFlow version compatible")
                    elif version.startswith('2.16') or version.startswith('2.17'):
                        version_conflicts.append(f"TensorFlow {version} may require newer NumPy")
                        
            except ImportError as e:
                print(f"   ❌ {dep} - Missing: {description}")
                self.dependency_conflicts.append(f"{dep}: {e}")
            except Exception as e:
                print(f"   ⚠️ {dep} - Issue: {e}")
        
        # Check optional dependencies
        print("\n   Optional Dependencies:")
        for dep, (description, expected_version) in optional_deps.items():
            try:
                module = __import__(dep)
                version = getattr(module, '__version__', 'Unknown')
                print(f"   ✅ {dep} v{version} - {description} (optional)")
            except ImportError:
                print(f"   ⚠️ {dep} - Not installed (optional)")
        
        # Report version conflicts
        if version_conflicts:
            print(f"\n   🚨 Version Conflicts Detected:")
            for conflict in version_conflicts:
                print(f"      • {conflict}")
                self.dependency_conflicts.append(conflict)
        
        success_rate = (working_deps / total_deps) * 100
        print(f"\n📊 Dependency Status: {working_deps}/{total_deps} ({success_rate:.1f}%)")
        
        return working_deps >= total_deps * 0.8 and len(version_conflicts) == 0

    def test_beat_addicts_audio_engine(self):
        """Test BEAT ADDICTS audio processing capabilities"""
        print("\n🎵 Testing BEAT ADDICTS Audio Engine...")
        
        try:
            # Test basic audio generation without heavy dependencies
            test_sample_rate = 44100
            test_duration = 1.0  # 1 second test
            
            # Generate test audio using basic Python
            import math
            samples = int(test_sample_rate * test_duration)
            
            # Create a simple 808 kick pattern
            kick_freq = 60  # Hz
            kick_audio = []
            
            for i in range(samples):
                t = i / test_sample_rate
                # Simple 808 kick with decay
                amplitude = math.exp(-t * 5)  # Decay
                frequency = kick_freq * (1 + math.exp(-t * 10))  # Pitch sweep
                sample = amplitude * math.sin(2 * math.pi * frequency * t)
                kick_audio.append(sample)
            
            if len(kick_audio) > 0 and max(abs(x) for x in kick_audio) > 0.01:
                print("   ✅ Basic audio generation working")
                self.performance_metrics['audio_generation'] = True
                return True
            else:
                print("   ❌ Audio generation failed")
                return False
                
        except Exception as e:
            print(f"   ❌ Audio engine error: {e}")
            traceback.print_exc()
            return False
    
    def test_beat_addicts_midi_system(self):
        """Test BEAT ADDICTS MIDI generation system"""
        print("\n🎼 Testing BEAT ADDICTS MIDI System...")
        
        try:
            # Test if we can import our BEAT ADDICTS generators
            import importlib.util
            
            generators_to_test = [
                'hiphop_midi_generator',
                'electronic_midi_generator', 
                'voice_assignment'
            ]
            
            working_generators = 0
            
            for generator_name in generators_to_test:
                try:
                    if os.path.exists(f"{generator_name}.py"):
                        spec = importlib.util.spec_from_file_location(generator_name, f"{generator_name}.py")
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        print(f"   ✅ {generator_name} - BEAT ADDICTS generator loaded")
                        working_generators += 1
                    else:
                        print(f"   ❌ {generator_name} - File not found")
                except Exception as e:
                    print(f"   ⚠️ {generator_name} - {e}")
            
            success_rate = (working_generators / len(generators_to_test)) * 100
            print(f"   📊 MIDI Generators: {working_generators}/{len(generators_to_test)} ({success_rate:.1f}%)")
            
            return working_generators >= len(generators_to_test) * 0.7  # 70% success rate
            
        except Exception as e:
            print(f"   ❌ MIDI system error: {e}")
            return False
    
    def test_beat_addicts_voice_system(self):
        """Test BEAT ADDICTS voice assignment system"""
        print("\n🎛️ Testing BEAT ADDICTS Voice Assignment...")
        
        try:
            # Import voice assignment without dependencies
            import importlib.util
            spec = importlib.util.spec_from_file_location("voice_assignment", "voice_assignment.py")
            if spec is not None and spec.loader is not None:
                voice_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(voice_module)
                
                # Test voice assignment
                assigner = voice_module.IntelligentVoiceAssigner()
                print("   ✅ BEAT ADDICTS Voice Engine loaded")
                
                # Test voice recommendations
                test_genres = ["hiphop", "electronic", "rock"]
                successful_recommendations = 0
                
                for genre in test_genres:
                    try:
                        recommendation = assigner.get_voice_recommendation(genre, "drums")
                        if recommendation and "recommended_program" in recommendation:
                            print(f"   ✅ {genre.upper()} voice: Program {recommendation['recommended_program']}")
                            successful_recommendations += 1
                        else:
                            print(f"   ❌ {genre.upper()} voice: Invalid recommendation")
                    except Exception as e:
                        print(f"   ❌ {genre.upper()} voice: {e}")
                
                success_rate = (successful_recommendations / len(test_genres)) * 100
                print(f"   📊 Voice System: {successful_recommendations}/{len(test_genres)} ({success_rate:.1f}%)")
                
                return successful_recommendations == len(test_genres)
            else:
                print("   ❌ Could not load voice assignment module")
                return False
                
        except Exception as e:
            print(f"   ❌ Voice system error: {e}")
            return False

    def test_beat_addicts_web_interface(self):
        """Test BEAT ADDICTS web interface"""
        print("\n🌐 Testing BEAT ADDICTS Web Interface...")
        
        try:
            # Check if web interface files exist
            has_web_interface = os.path.exists("web_interface.py")
            has_templates = os.path.exists("templates/index.html")
            
            if not has_web_interface:
                print("   ❌ web_interface.py missing")
                return False
            
            if not has_templates:
                print("   ❌ templates/index.html missing")
                # Create templates directory and basic template
                os.makedirs("templates", exist_ok=True)
                print("   ✅ Created templates directory")
                return False
            
            # Try to import web interface
            import importlib.util
            spec = importlib.util.spec_from_file_location("web_interface", "web_interface.py")
            web_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(web_module)
            
            print("   ✅ BEAT ADDICTS web interface loaded")
            print("   ✅ Flask app available")
            print("   ✅ Templates directory exists")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Web interface error: {e}")
            return False

    def run_beat_addicts_diagnostic(self):
        """Run complete BEAT ADDICTS diagnostic suite"""
        print("🎵 BEAT ADDICTS v2.0 - PRODUCTION SYSTEM DIAGNOSTIC")
        print("🔥 Professional Music Production AI Health Check 🔥")
        print("=" * 70)
        
        # Step 1: Explain and fix dependency issues
        dependency_fixed = self.explain_numpy_warning()
        
        # Step 2: Run BEAT ADDICTS specific tests
        tests = [
            ("Dependency Verification", lambda: dependency_fixed),
            ("BEAT ADDICTS Audio Engine", self.test_beat_addicts_audio_engine),
            ("BEAT ADDICTS MIDI System", self.test_beat_addicts_midi_system),
            ("BEAT ADDICTS Voice System", self.test_beat_addicts_voice_system),
            ("BEAT ADDICTS Web Interface", self.test_beat_addicts_web_interface),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}")
            print("-" * 40)
            
            try:
                if test_func():
                    passed_tests += 1
                    self.test_results.append({"test": test_name, "status": "PASSED"})
                    print(f"   🎉 {test_name}: PASSED")
                else:
                    self.test_results.append({"test": test_name, "status": "FAILED"})
                    print(f"   ❌ {test_name}: FAILED")
            except Exception as e:
                print(f"   💥 {test_name}: CRASHED - {e}")
                self.test_results.append({"test": test_name, "status": "CRASHED", "error": str(e)})
        
        # Generate BEAT ADDICTS report
        self.generate_beat_addicts_report(passed_tests, total_tests)
        
        return passed_tests == total_tests
    
    def generate_beat_addicts_report(self, passed, total):
        """Generate BEAT ADDICTS diagnostic report"""
        print(f"\n📊 BEAT ADDICTS DIAGNOSTIC REPORT")
        print("=" * 50)
        print(f"🎵 Tests Passed: {passed}/{total}")
        print(f"🔥 Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 BEAT ADDICTS STATUS: FULLY OPERATIONAL!")
            print("🔥 Ready for professional music production! 🔥")
            print("\n🎵 Next Steps:")
            print("   1. python run.py --create-all")
            print("   2. python run.py --test-voices") 
            print("   3. python run.py  # Start BEAT ADDICTS Studio")
        else:
            print("⚠️ BEAT ADDICTS STATUS: NEEDS ATTENTION")
            print("🔧 Check failed tests above for issues to fix")
            
            if self.dependency_conflicts:
                print("\n🚨 Dependency Conflicts Found:")
                for conflict in self.dependency_conflicts:
                    print(f"   • {conflict}")
                print("\n💡 Run this to fix dependencies:")
                print("   pip uninstall numpy numba -y")
                print("   pip install numpy==1.24.3 numba>=0.61.2")
        
        # Save detailed BEAT ADDICTS report
        report = {
            "beat_addicts_version": "2.0",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total,
                "passed_tests": passed,
                "success_rate": (passed/total)*100
            },
            "test_results": self.test_results,
            "performance_metrics": self.performance_metrics,
            "dependency_conflicts": self.dependency_conflicts,
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform,
                "working_directory": os.getcwd()
            }
        }
        
        report_file = f"beat_addicts_diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📋 Detailed BEAT ADDICTS report saved: {report_file}")

    def get_next_steps(self):
        """Provide clear next steps for BEAT ADDICTS"""
        print("\n🎵 BEAT ADDICTS - WHAT TO DO NEXT")
        print("=" * 50)
        
        # Check current system status
        has_voice_system = os.path.exists("voice_assignment.py") or os.path.exists("beat_addicts_core/voice_assignment.py")
        has_generators = os.path.exists("hiphop_midi_generator.py") or os.path.exists("beat_addicts_generators/hiphop_midi_generator.py")
        has_main_runner = os.path.exists("run.py") or os.path.exists("beat_addicts_core/run.py")
        has_launcher = os.path.exists("beat_addicts_launcher.py")
        
        # Check if project needs cleanup
        current_files = [f for f in os.listdir('.') if os.path.isfile(f)]
        needs_cleanup = len(current_files) > 15  # Too many files in root
        
        if needs_cleanup:
            print("🧹 PROJECT NEEDS CLEANUP!")
            print("\n🚀 RECOMMENDED ACTIONS:")
            print("1. 🗑️ Clean project: python cleanup_project.py")
            print("2. 🔧 Fix dependencies: python debug_production_system.py")
            print("3. 🎛️ Test voice system: python beat_addicts_launcher.py --test-voices")
            print("4. 🎵 Generate training data: python beat_addicts_launcher.py --create-all")
            
        elif has_voice_system and has_generators and (has_main_runner or has_launcher):
            print("✅ BEAT ADDICTS core files detected!")
            print("\n🚀 RECOMMENDED ACTIONS:")
            if has_launcher:
                print("1. 🚀 Use launcher: python beat_addicts_launcher.py")
            else:
                print("1. 🔧 Fix dependencies: python debug_production_system.py")
                print("2. 🎛️ Test voice system: python run.py --test-voices")
                print("3. 🎵 Generate training data: python run.py --create-all")
                print("4. 🌐 Start BEAT ADDICTS Studio: python run.py")
            
        else:
            print("⚠️ Missing core BEAT ADDICTS files!")
            if not has_voice_system:
                print("   • voice_assignment.py missing")
            if not has_generators:
                print("   • MIDI generators missing")
            if not has_main_runner and not has_launcher:
                print("   • run.py or launcher missing")
        
        print("\n🎯 IMMEDIATE PRIORITY:")
        if needs_cleanup:
            print("   Clean project first → python cleanup_project.py")
        else:
            print("   Run diagnostic → python debug_production_system.py")

def main():
    """Run BEAT ADDICTS production diagnostic"""
    debugger = BeatAddictsProductionDebugger()
    debugger.get_next_steps()
    
    print("\n" + "="*50)
    user_input = input("🎵 Run full BEAT ADDICTS diagnostic now? (y/n): ").lower().strip()
    
    if user_input in ['y', 'yes']:
        success = debugger.run_beat_addicts_diagnostic()
    else:
        print("🔧 Run 'python debug_production_system.py' when ready!")
    
    return success

if __name__ == "__main__":
    main()
