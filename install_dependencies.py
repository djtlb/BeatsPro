#!/usr/bin/env python3
"""
Comprehensive Dependency Installer for Smart Music Generator AI
Handles all Windows installation issues with multiple fallback strategies
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

class DependencyInstaller:
    """Advanced dependency installer with multiple strategies"""
    
    def __init__(self):
        self.installed_packages = []
        self.failed_packages = []
        self.python_exe = sys.executable
        
    def log(self, message, level="INFO"):
        """Log messages with timestamps"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def run_command(self, command, timeout=300):
        """Run command with timeout and detailed output"""
        self.log(f"Running: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                self.log("✅ Success!")
                return True, result.stdout
            else:
                self.log(f"❌ Failed (code {result.returncode})")
                if result.stderr:
                    self.log(f"Error: {result.stderr}")
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            self.log(f"⏰ Command timed out after {timeout} seconds")
            return False, "Timeout"
        except Exception as e:
            self.log(f"❌ Exception: {e}")
            return False, str(e)
    
    def check_package(self, package_name):
        """Check if a package is already installed"""
        try:
            __import__(package_name.replace('-', '_'))
            return True
        except ImportError:
            return False
    
    def upgrade_pip(self):
        """Upgrade pip and essential tools"""
        self.log("🔧 Upgrading pip and tools...", "STEP")
        
        commands = [
            f'"{self.python_exe}" -m pip install --upgrade pip',
            f'"{self.python_exe}" -m pip install --upgrade setuptools wheel'
        ]
        
        for cmd in commands:
            success, output = self.run_command(cmd)
            if not success:
                self.log(f"⚠️ Failed to upgrade tools, continuing anyway...")
    
    def install_package_strategies(self, package, description=""):
        """Try multiple installation strategies for a package"""
        if self.check_package(package.split('=')[0]):
            self.log(f"✅ {package} already installed")
            self.installed_packages.append(package)
            return True
        
        self.log(f"📦 Installing {package} - {description}", "PACKAGE")
        
        # Multiple installation strategies
        strategies = [
            # Strategy 1: User install with no cache
            f'"{self.python_exe}" -m pip install --user --no-cache-dir "{package}"',
            
            # Strategy 2: Force reinstall
            f'"{self.python_exe}" -m pip install --user --force-reinstall --no-deps "{package}"',
            
            # Strategy 3: Ignore installed
            f'"{self.python_exe}" -m pip install --ignore-installed "{package}"',
            
            # Strategy 4: System install (might need admin)
            f'"{self.python_exe}" -m pip install "{package}"',
            
            # Strategy 5: Pre-release versions
            f'"{self.python_exe}" -m pip install --user --pre "{package}"'
        ]
        
        for i, strategy in enumerate(strategies, 1):
            self.log(f"🔄 Strategy {i}/{len(strategies)}")
            success, output = self.run_command(strategy)
            
            if success and self.check_package(package.split('=')[0]):
                self.log(f"✅ {package} installed successfully!")
                self.installed_packages.append(package)
                return True
            
            time.sleep(1)  # Brief pause between attempts
        
        self.log(f"❌ All strategies failed for {package}")
        self.failed_packages.append(package)
        return False
    
    def install_core_dependencies(self):
        """Install core dependencies required for basic functionality"""
        self.log("🎯 Installing Core Dependencies", "PHASE")
        
        core_deps = [
            ("flask>=2.0.0", "Web framework - Essential"),
            ("werkzeug>=2.0.0", "Web utilities - Essential"),
            ("numpy>=1.20.0", "Scientific computing - Essential")
        ]
        
        success_count = 0
        for package, description in core_deps:
            if self.install_package_strategies(package, description):
                success_count += 1
        
        self.log(f"📊 Core Dependencies: {success_count}/{len(core_deps)} installed")
        return success_count >= 2  # Need at least 2 core packages
    
    def install_midi_dependencies(self):
        """Install MIDI processing dependencies"""
        self.log("🎵 Installing MIDI Dependencies", "PHASE")
        
        midi_deps = [
            ("pretty_midi>=0.2.9", "MIDI processing - Required"),
            ("mido>=1.2.0", "MIDI I/O - Required")
        ]
        
        success_count = 0
        for package, description in midi_deps:
            if self.install_package_strategies(package, description):
                success_count += 1
        
        self.log(f"📊 MIDI Dependencies: {success_count}/{len(midi_deps)} installed")
        return success_count >= 1  # Need at least one MIDI library
    
    def install_ai_dependencies(self):
        """Install AI/ML dependencies (optional)"""
        self.log("🧠 Installing AI Dependencies (Optional)", "PHASE")
        
        ai_deps = [
            ("tensorflow>=2.8.0", "AI framework - Optional"),
            ("scipy>=1.7.0", "Scientific computing - Optional"),
            ("librosa>=0.9.0", "Audio processing - Optional")
        ]
        
        success_count = 0
        for package, description in ai_deps:
            if self.install_package_strategies(package, description):
                success_count += 1
        
        self.log(f"📊 AI Dependencies: {success_count}/{len(ai_deps)} installed")
        return success_count  # Return count, not boolean
    
    def install_from_wheels(self):
        """Try installing pre-compiled wheels for problematic packages"""
        self.log("🎡 Trying Pre-compiled Wheels", "PHASE")
        
        # For numpy issues, try specific wheel versions
        if not self.check_package('numpy'):
            wheel_commands = [
                f'"{self.python_exe}" -m pip install --user numpy==1.24.3',
                f'"{self.python_exe}" -m pip install --user numpy==1.23.5',
                f'"{self.python_exe}" -m pip install --user numpy==1.21.6'
            ]
            
            for cmd in wheel_commands:
                success, output = self.run_command(cmd)
                if success and self.check_package('numpy'):
                    self.log("✅ NumPy installed from wheel")
                    break
    
    def create_fallback_environment(self):
        """Create a minimal working environment"""
        self.log("🔄 Creating Fallback Environment", "PHASE")
        
        # Create a simple requirements file with only essentials
        fallback_requirements = """flask>=2.0.0
werkzeug>=2.0.0
"""
        
        with open("requirements_emergency.txt", "w") as f:
            f.write(fallback_requirements)
        
        self.log("📝 Created emergency requirements file")
        
        # Try installing just the basics
        success, output = self.run_command(
            f'"{self.python_exe}" -m pip install --user -r requirements_emergency.txt'
        )
        
        return success
    
    def test_installation(self):
        """Test what actually works after installation"""
        self.log("🧪 Testing Installation", "PHASE")
        
        test_modules = {
            'flask': 'Web framework',
            'numpy': 'Scientific computing',
            'pretty_midi': 'MIDI processing',
            'mido': 'MIDI I/O',
            'tensorflow': 'AI framework',
            'scipy': 'Scientific computing',
            'librosa': 'Audio processing'
        }
        
        working = []
        broken = []
        
        for module, description in test_modules.items():
            try:
                __import__(module)
                working.append({'module': module, 'description': description, 'status': 'working'})
                self.log(f"✅ {module} - {description}")
            except ImportError as e:
                broken.append({'module': module, 'description': description, 'status': 'broken', 'error': str(e)})
                self.log(f"❌ {module} - {description} ({e})")
        
        # Check minimum requirements
        essential_modules = ['flask']
        has_minimum = any(item['module'] in essential_modules for item in working)
        
        return {
            'working': working,
            'broken': broken,
            'has_minimum': has_minimum,
            'working_count': len(working),
            'broken_count': len(broken)
        }
    
    def generate_report(self, test_results):
        """Generate installation report"""
        report = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'python_version': sys.version,
            'platform': sys.platform,
            'installed_packages': self.installed_packages,
            'failed_packages': self.failed_packages,
            'test_results': test_results,
            'recommendations': []
        }
        
        # Add recommendations
        if not test_results['has_minimum']:
            report['recommendations'].append("Install Flask manually: pip install --user flask")
        
        if 'numpy' not in [item['module'] for item in test_results['working']]:
            report['recommendations'].append("Install NumPy manually: pip install --user numpy")
        
        if len(test_results['working']) < 3:
            report['recommendations'].append("Try running as administrator")
            report['recommendations'].append("Consider using conda instead of pip")
        
        # Save report
        with open("installation_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def run_installation(self):
        """Run the complete installation process"""
        self.log("🎵 Smart Music Generator AI - Dependency Installer", "START")
        self.log("=" * 60)
        
        try:
            # Step 1: Upgrade pip
            self.upgrade_pip()
            
            # Step 2: Install core dependencies
            core_success = self.install_core_dependencies()
            
            # Step 3: Install MIDI dependencies
            midi_success = self.install_midi_dependencies()
            
            # Step 4: Try wheels for problematic packages
            self.install_from_wheels()
            
            # Step 5: Install AI dependencies (optional)
            ai_count = self.install_ai_dependencies()
            
            # Step 6: Fallback if needed
            if not core_success:
                self.log("⚠️ Core installation failed, trying fallback...")
                self.create_fallback_environment()
            
            # Step 7: Test everything
            test_results = self.test_installation()
            
            # Step 8: Generate report
            report = self.generate_report(test_results)
            
            # Final summary
            self.log("=" * 60, "SUMMARY")
            if test_results['has_minimum']:
                self.log("✅ SUCCESS! Minimum requirements met", "SUCCESS")
                self.log(f"📊 Working: {test_results['working_count']}, Broken: {test_results['broken_count']}")
                self.log("🚀 You can now run: python run.py")
            else:
                self.log("⚠️ PARTIAL SUCCESS - Manual intervention needed", "WARNING")
                self.log("🔧 Check installation_report.json for details")
            
            return test_results['has_minimum']
            
        except Exception as e:
            self.log(f"❌ Installation failed with error: {e}", "ERROR")
            return False

def main():
    """Main installation function"""
    installer = DependencyInstaller()
    return installer.run_installation()

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Installation completed successfully!")
            print("Next steps:")
            print("1. python run.py --create-dnb  # Generate training data")
            print("2. python run.py              # Start web interface")
        else:
            print("\n🔧 Installation needs manual intervention")
            print("Check installation_report.json for detailed recommendations")
    except KeyboardInterrupt:
        print("\n\n👋 Installation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
