#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Optimal Dependency Installer
Research-based dependency resolution for professional music production
"""

import subprocess
import sys
import os
from datetime import datetime

class OptimalDependencyInstaller:
    """Smart dependency installer with conflict resolution"""
    
    def __init__(self):
        self.install_log = []
        self.conflicts_resolved = []
        
    def print_step(self, step, description):
        print(f"\n🔧 Step {step}: {description}")
        print("-" * 50)
    
    def run_command(self, command, description=""):
        """Run command with logging"""
        print(f"   ▶️ {command}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ Success")
                self.install_log.append(f"SUCCESS: {command}")
                return True
            else:
                print(f"   ❌ Failed: {result.stderr}")
                self.install_log.append(f"FAILED: {command} - {result.stderr}")
                return False
        except Exception as e:
            print(f"   💥 Exception: {e}")
            self.install_log.append(f"EXCEPTION: {command} - {e}")
            return False
    
    def complete_cleanup(self):
        """Complete cleanup of problematic packages"""
        self.print_step(1, "Complete Dependency Cleanup")
        
        # Remove all potentially conflicting packages
        problematic_packages = [
            "numpy", "scipy", "numba", "tensorflow", 
            "sklearn", "scikit-learn", "matplotlib",
            "pretty_midi", "mido", "librosa", "music21"
        ]
        
        for package in problematic_packages:
            self.run_command(f"pip uninstall {package} -y")
        
        # Clear pip cache
        self.run_command("pip cache purge")
        
        # Clean up corrupted installations
        print("   🧹 Cleaning corrupted installations...")
        try:
            import site
            site_packages = site.getsitepackages()[0]
            print(f"   📁 Site-packages: {site_packages}")
            
            # Look for corrupted packages
            corrupted_patterns = ["~umpy", "~cipy", "~ensorflow"]
            for pattern in corrupted_patterns:
                corrupted_path = os.path.join(site_packages, pattern)
                if os.path.exists(corrupted_path):
                    print(f"   🗑️ Found corrupted package: {pattern}")
                    try:
                        import shutil
                        shutil.rmtree(corrupted_path)
                        print(f"   ✅ Removed {pattern}")
                        self.conflicts_resolved.append(f"Removed corrupted {pattern}")
                    except Exception as e:
                        print(f"   ⚠️ Could not remove {pattern}: {e}")
                        
        except Exception as e:
            print(f"   ⚠️ Cleanup check failed: {e}")
    
    def install_core_stack(self):
        """Install core scientific computing stack in optimal order"""
        self.print_step(2, "Installing Core Scientific Stack")
        
        # Install in dependency order
        core_packages = [
            "numpy==1.26.4",           # Base for everything
            "scipy==1.11.4",           # Depends on NumPy
            "numba==0.60.0",           # JIT compiler
        ]
        
        for package in core_packages:
            success = self.run_command(f"pip install {package}")
            if not success:
                print(f"   🚨 Critical failure: {package}")
                return False
        
        return True
    
    def install_ml_frameworks(self):
        """Install ML frameworks"""
        self.print_step(3, "Installing ML Frameworks")
        
        ml_packages = [
            "tensorflow==2.15.0",      # AI framework
            "scikit-learn==1.3.2",     # ML utilities
        ]
        
        success_count = 0
        for package in ml_packages:
            if self.run_command(f"pip install {package}"):
                success_count += 1
        
        return success_count >= len(ml_packages) * 0.5  # 50% success minimum
    
    def install_audio_stack(self):
        """Install audio processing stack"""
        self.print_step(4, "Installing Audio Processing Stack")
        
        audio_packages = [
            "pretty_midi==0.2.10",     # MIDI processing
            "mido==1.3.2",             # MIDI I/O
            "librosa==0.10.1",         # Audio analysis
            "soundfile==0.12.1",       # Audio file I/O
            "music21==9.1.0",          # Music theory
        ]
        
        success_count = 0
        for package in audio_packages:
            if self.run_command(f"pip install {package}"):
                success_count += 1
        
        return success_count >= len(audio_packages) * 0.8  # 80% success minimum
    
    def install_web_stack(self):
        """Install web framework stack"""
        self.print_step(5, "Installing Web Framework Stack")
        
        web_packages = [
            "flask==3.0.0",            # Web framework
            "werkzeug==3.0.1",         # WSGI utilities
            "jinja2==3.1.2",           # Template engine
        ]
        
        success_count = 0
        for package in web_packages:
            if self.run_command(f"pip install {package}"):
                success_count += 1
        
        return success_count == len(web_packages)  # All required for web interface
    
    def install_utilities(self):
        """Install utility packages"""
        self.print_step(6, "Installing Utility Packages")
        
        utility_packages = [
            "matplotlib==3.8.2",       # Plotting
            "psutil==5.9.6",           # System monitoring
            "pytest==7.4.3",           # Testing
        ]
        
        for package in utility_packages:
            self.run_command(f"pip install {package}")  # Non-critical
        
        return True
    
    def verify_installation(self):
        """Verify all installations work together"""
        self.print_step(7, "Verifying Installation")
        
        test_imports = [
            ("numpy", "NumPy"),
            ("scipy", "SciPy"),
            ("tensorflow", "TensorFlow"),
            ("flask", "Flask"),
            ("pretty_midi", "Pretty MIDI"),
            ("mido", "Mido"),
        ]
        
        working_imports = 0
        version_info = {}
        
        for module, name in test_imports:
            try:
                imported_module = __import__(module)
                version = getattr(imported_module, '__version__', 'Unknown')
                version_info[module] = version
                print(f"   ✅ {name} v{version}")
                working_imports += 1
            except ImportError as e:
                print(f"   ❌ {name}: {e}")
            except Exception as e:
                print(f"   ⚠️ {name}: {e}")
        
        # Check for version conflicts
        if 'numpy' in version_info and 'scipy' in version_info:
            numpy_version = version_info['numpy']
            scipy_version = version_info['scipy']
            
            if numpy_version.startswith('1.26') and scipy_version.startswith('1.11'):
                print("   🎯 NumPy/SciPy versions compatible")
            else:
                print(f"   ⚠️ Version mismatch: NumPy {numpy_version}, SciPy {scipy_version}")
        
        success_rate = (working_imports / len(test_imports)) * 100
        print(f"\n   📊 Import Success Rate: {working_imports}/{len(test_imports)} ({success_rate:.1f}%)")
        
        return working_imports >= len(test_imports) * 0.8
    
    def generate_install_report(self):
        """Generate installation report"""
        print(f"\n📋 BEAT ADDICTS INSTALLATION REPORT")
        print("=" * 50)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "conflicts_resolved": self.conflicts_resolved,
            "install_log": self.install_log,
            "python_version": sys.version,
            "platform": sys.platform
        }
        
        report_file = f"beat_addicts_install_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            import json
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"📄 Installation report saved: {report_file}")
        except Exception as e:
            print(f"⚠️ Could not save report: {e}")
    
    def run_optimal_installation(self):
        """Run the complete optimal installation process"""
        print("🎵 BEAT ADDICTS - Optimal Dependency Installation")
        print("🔥 Research-based conflict resolution 🔥")
        print("=" * 60)
        
        steps = [
            ("Cleanup", self.complete_cleanup),
            ("Core Stack", self.install_core_stack),
            ("ML Frameworks", self.install_ml_frameworks),
            ("Audio Stack", self.install_audio_stack),
            ("Web Stack", self.install_web_stack),
            ("Utilities", self.install_utilities),
            ("Verification", self.verify_installation)
        ]
        
        success_count = 0
        total_steps = len(steps)
        
        for step_name, step_func in steps:
            try:
                if step_func():
                    success_count += 1
                    print(f"   🎉 {step_name}: SUCCESS")
                else:
                    print(f"   ⚠️ {step_name}: PARTIAL SUCCESS")
            except Exception as e:
                print(f"   💥 {step_name}: FAILED - {e}")
        
        # Generate report
        self.generate_install_report()
        
        # Final status
        success_rate = (success_count / total_steps) * 100
        print(f"\n🎯 INSTALLATION RESULTS:")
        print(f"   Success Rate: {success_count}/{total_steps} ({success_rate:.1f}%)")
        
        if success_rate >= 85:
            print("🎉 BEAT ADDICTS: INSTALLATION SUCCESSFUL!")
            print("🔥 Ready for professional music production! 🔥")
            print("\nNext steps:")
            print("   python run.py --test-voices")
            print("   python run.py --create-all")
            print("   python run.py")
        else:
            print("⚠️ BEAT ADDICTS: INSTALLATION NEEDS ATTENTION")
            print("Check the install log above for issues")
        
        return success_rate >= 80

def main():
    """Run optimal dependency installation"""
    installer = OptimalDependencyInstaller()
    return installer.run_optimal_installation()

if __name__ == "__main__":
    main()
