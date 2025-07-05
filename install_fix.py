#!/usr/bin/env python3
"""
Installation Fix Script for Smart Music Generator AI
Handles Windows permission errors and dependency conflicts
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print('='*60)

def run_command_safe(command, description=""):
    """Run command with error handling"""
    print(f"\n▶️ {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ Success!")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False, e.stderr

def check_admin_rights():
    """Check if running with admin privileges"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def fix_venv_permissions():
    """Fix virtual environment permission issues"""
    print_header("FIXING VIRTUAL ENVIRONMENT PERMISSIONS")
    
    venv_path = Path(".venv")
    if venv_path.exists():
        print("Found existing .venv directory")
        
        if check_admin_rights():
            print("✅ Running with admin rights")
        else:
            print("⚠️ Not running as admin - some fixes may be limited")
        
        # Try to remove problematic files
        problematic_paths = [
            venv_path / "Lib" / "site-packages" / "numpy",
            venv_path / "Lib" / "site-packages" / "tensorflow",
        ]
        
        for path in problematic_paths:
            if path.exists():
                try:
                    shutil.rmtree(path, ignore_errors=True)
                    print(f"✅ Removed: {path.name}")
                except Exception as e:
                    print(f"⚠️ Could not remove {path.name}: {e}")
        
        # Remove entire venv if needed
        response = input("\nRemove entire virtual environment? (y/n): ").lower()
        if response == 'y':
            try:
                shutil.rmtree(venv_path, ignore_errors=True)
                print("✅ Virtual environment removed")
                return True
            except Exception as e:
                print(f"❌ Could not remove venv: {e}")
                return False
    
    return True

def install_dependencies_alternative():
    """Try alternative installation methods"""
    print_header("ALTERNATIVE INSTALLATION METHODS")
    
    # Method 1: User installation (no admin required)
    print("\n🔄 Method 1: User-level installation")
    success, output = run_command_safe(
        "pip install --user -r requirements.txt",
        "Installing to user directory (no admin needed)"
    )
    
    if success:
        print("✅ User installation successful!")
        return True
    
    # Method 2: No cache installation
    print("\n🔄 Method 2: No cache installation")
    success, output = run_command_safe(
        "pip install --no-cache-dir -r requirements.txt",
        "Installing without cache"
    )
    
    if success:
        print("✅ No-cache installation successful!")
        return True
    
    # Method 3: Force reinstall
    print("\n🔄 Method 3: Force reinstall")
    success, output = run_command_safe(
        "pip install --force-reinstall -r requirements.txt",
        "Force reinstalling all packages"
    )
    
    if success:
        print("✅ Force reinstall successful!")
        return True
    
    # Method 4: Individual package installation
    print("\n🔄 Method 4: Installing key packages individually")
    key_packages = [
        "numpy",
        "tensorflow",
        "flask",
        "pretty_midi",
        "mido"
    ]
    
    for package in key_packages:
        print(f"\nInstalling {package}...")
        success, output = run_command_safe(
            f"pip install --user {package}",
            f"Installing {package}"
        )
        if not success:
            print(f"⚠️ Failed to install {package}")
    
    return False

def create_simple_requirements():
    """Create a minimal requirements file for problematic systems"""
    print_header("CREATING SIMPLIFIED REQUIREMENTS")
    
    simple_reqs = """# Minimal requirements for Smart Music Generator AI
flask>=2.0.0
numpy>=1.21.0
pretty_midi>=0.2.9
mido>=1.2.0

# Optional but recommended
tensorflow>=2.8.0
librosa>=0.9.0
scipy>=1.7.0
"""
    
    with open("requirements_simple.txt", "w") as f:
        f.write(simple_reqs)
    
    print("✅ Created requirements_simple.txt")
    print("Try: pip install -r requirements_simple.txt")

def provide_manual_solutions():
    """Provide manual installation instructions"""
    print_header("MANUAL INSTALLATION GUIDE")
    
    print("""
🔧 MANUAL INSTALLATION STEPS:

1. RUN AS ADMINISTRATOR:
   - Right-click Command Prompt
   - Select "Run as administrator"
   - Navigate to project folder
   - Try: pip install -r requirements.txt

2. USE CONDA (if available):
   conda create -n music_ai python=3.9
   conda activate music_ai
   pip install -r requirements.txt

3. MINIMAL INSTALLATION:
   pip install flask numpy pretty_midi mido
   
4. CLOUD ALTERNATIVE:
   - Use Google Colab
   - Upload project files
   - Install in cloud environment

5. TROUBLESHOOTING:
   - Close all Python applications
   - Restart computer
   - Disable antivirus temporarily
   - Run installer as admin
""")

def main():
    """Main installation fix process"""
    print("🎵 Smart Music Generator AI - Installation Fix Tool")
    print("This tool will help resolve Windows permission and installation issues.")
    
    # Check current directory
    if not os.path.exists("run.py"):
        print("\n❌ Error: Please run this from the project directory")
        print("Navigate to: C:\\Users\\sally\\Downloads\\sunoai-1.0.7-rebuild")
        return False
    
    print(f"\n📍 Current directory: {os.getcwd()}")
    print(f"🔍 Admin rights: {'Yes' if check_admin_rights() else 'No'}")
    
    # Show options
    print("\n" + "="*60)
    print("SELECT SOLUTION:")
    print("1. Fix virtual environment permissions")
    print("2. Try alternative installation methods")
    print("3. Create simplified requirements file")
    print("4. Show manual installation guide")
    print("5. Exit")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        fix_venv_permissions()
        print("\nTry running: pip install -r requirements.txt")
        
    elif choice == "2":
        install_dependencies_alternative()
        
    elif choice == "3":
        create_simple_requirements()
        print("\nTry running: pip install -r requirements_simple.txt")
        
    elif choice == "4":
        provide_manual_solutions()
        
    elif choice == "5":
        print("👋 Exiting...")
        return True
        
    else:
        print("❌ Invalid choice")
        return False
    
    # Final check
    print("\n" + "="*60)
    print("🧪 TESTING INSTALLATION")
    
    try:
        import numpy
        print("✅ NumPy imported successfully")
    except ImportError:
        print("❌ NumPy not available")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError:
        print("❌ Flask not available")
    
    try:
        import pretty_midi
        print("✅ pretty_midi imported successfully")
    except ImportError:
        print("❌ pretty_midi not available")
    
    print("\n🚀 If imports work, you can run: python run.py")
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Installation fix cancelled")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
