#!/usr/bin/env python3
"""
Smart Installer for Smart Music Generator AI
Handles Windows dependency conflicts and permission issues
"""

import os
import sys
import subprocess
import time

def print_header(title):
    print(f"\n{'='*70}")
    print(f"🔧 {title}")
    print('='*70)

def run_pip_command(command, description=""):
    """Run pip command with detailed output"""
    print(f"\n▶️ {description}")
    print(f"Command: {command}")
    
    try:
        # Use subprocess with real-time output
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Print output in real-time
        for line in process.stdout:
            print(line.rstrip())
        
        process.wait()
        
        if process.returncode == 0:
            print("✅ Success!")
            return True
        else:
            print(f"❌ Failed with return code: {process.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def upgrade_pip():
    """Upgrade pip to latest version"""
    print_header("UPGRADING PIP")
    commands = [
        f'"{sys.executable}" -m pip install --upgrade pip',
        f'"{sys.executable}" -m pip install --upgrade setuptools wheel'
    ]
    
    for cmd in commands:
        run_pip_command(cmd, "Upgrading pip and tools")

def install_method_1():
    """Method 1: Install minimal requirements"""
    print_header("METHOD 1: MINIMAL INSTALLATION")
    
    packages = [
        "flask==2.3.3",
        "numpy==1.24.3", 
        "pretty_midi==0.2.10",
        "mido==1.3.0"
    ]
    
    success_count = 0
    for package in packages:
        if run_pip_command(
            f'"{sys.executable}" -m pip install --user --no-cache-dir "{package}"',
            f"Installing {package}"
        ):
            success_count += 1
        else:
            print(f"⚠️ Failed to install {package}")
    
    print(f"\n📊 Method 1 Results: {success_count}/{len(packages)} packages installed")
    return success_count >= 3  # Need at least flask, numpy, and one MIDI lib

def install_method_2():
    """Method 2: Install from requirements_minimal.txt"""
    print_header("METHOD 2: REQUIREMENTS FILE INSTALLATION")
    
    if not os.path.exists("requirements_minimal.txt"):
        print("❌ requirements_minimal.txt not found")
        return False
    
    commands = [
        f'"{sys.executable}" -m pip install --user -r requirements_minimal.txt',
        f'"{sys.executable}" -m pip install --no-cache-dir -r requirements_minimal.txt',
        f'"{sys.executable}" -m pip install --force-reinstall -r requirements_minimal.txt'
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"\n🔄 Attempt {i}/3:")
        if run_pip_command(cmd, f"Installing from requirements_minimal.txt (attempt {i})"):
            return True
        time.sleep(2)  # Brief pause between attempts
    
    return False

def install_method_3():
    """Method 3: TensorFlow installation (optional)"""
    print_header("METHOD 3: TENSORFLOW INSTALLATION (OPTIONAL)")
    
    tf_versions = [
        "tensorflow==2.13.0",
        "tensorflow-cpu==2.13.0", 
        "tensorflow==2.12.0",
        "tensorflow-cpu==2.12.0"
    ]
    
    for tf_version in tf_versions:
        print(f"\n🧠 Trying {tf_version}...")
        if run_pip_command(
            f'"{sys.executable}" -m pip install --user "{tf_version}"',
            f"Installing {tf_version}"
        ):
            print(f"✅ TensorFlow installed: {tf_version}")
            return True
        
        print(f"⚠️ {tf_version} failed, trying next...")
    
    print("⚠️ TensorFlow installation failed - you can still use basic features")
    return False

def test_imports():
    """Test if critical modules can be imported"""
    print_header("TESTING INSTALLATION")
    
    modules = {
        'flask': 'Web framework',
        'numpy': 'Scientific computing',
        'pretty_midi': 'MIDI processing',
        'mido': 'MIDI I/O',
        'tensorflow': 'AI framework (optional)'
    }
    
    working = []
    broken = []
    
    for module, description in modules.items():
        try:
            __import__(module)
            working.append(f"✅ {module} - {description}")
        except ImportError as e:
            broken.append(f"❌ {module} - {description} ({e})")
    
    print("\n📦 WORKING MODULES:")
    for item in working:
        print(f"  {item}")
    
    if broken:
        print("\n⚠️ BROKEN MODULES:")
        for item in broken:
            print(f"  {item}")
    
    # Check if we have minimum for basic functionality
    essential = ['flask', 'numpy']
    has_essential = all(module in str(working) for module in essential)
    
    return has_essential, len(working), len(broken)

def main():
    """Main installation process"""
    print("🎵 Smart Music Generator AI - Smart Installer")
    print("This installer uses multiple strategies to handle Windows dependency issues.")
    
    # Step 1: Upgrade pip
    upgrade_pip()
    
    # Step 2: Try installation methods
    method1_success = install_method_1()
    
    if not method1_success:
        print("\n🔄 Method 1 failed, trying Method 2...")
        method2_success = install_method_2()
        
        if not method2_success:
            print("\n⚠️ Both methods had issues, but continuing...")
    
    # Step 3: Optional TensorFlow
    install_method_3()
    
    # Step 4: Test everything
    has_essential, working_count, broken_count = test_imports()
    
    print(f"\n{'='*70}")
    print("🎯 INSTALLATION SUMMARY")
    print(f"{'='*70}")
    
    if has_essential:
        print(f"✅ SUCCESS! Essential components working ({working_count} modules)")
        print("🚀 You can now run: python run.py")
        
        if broken_count > 0:
            print(f"ℹ️ {broken_count} optional modules failed - advanced features may be limited")
    else:
        print(f"⚠️ PARTIAL SUCCESS ({working_count} modules working, {broken_count} failed)")
        print("\n🔧 TROUBLESHOOTING OPTIONS:")
        print("1. Run as administrator: Right-click Command Prompt → 'Run as administrator'")
        print("2. Try: python -m pip install --user flask numpy pretty_midi mido")
        print("3. Use virtual environment: python -m venv venv && venv\\Scripts\\activate")
        print("4. Install Python from microsoft store (often fixes permission issues)")
    
    return has_essential

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Installation completed! Run 'python run.py' to start.")
        else:
            print("\n🔧 Installation needs manual intervention. See troubleshooting above.")
    except KeyboardInterrupt:
        print("\n\n👋 Installation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
