#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Virtual Environment Permission Fixer
Fix Windows permission issues and setup alternative environment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def fix_venv_permissions():
    """Fix virtual environment permission issues"""
    print("🔧 BEAT ADDICTS - Virtual Environment Permission Fixer")
    print("=" * 60)
    
    project_dir = Path(__file__).parent
    venv_dir = project_dir / ".venv"
    
    # Step 1: Clean up existing corrupted .venv
    if venv_dir.exists():
        print("🗑️ Removing corrupted .venv directory...")
        try:
            shutil.rmtree(venv_dir)
            print("   ✅ Corrupted .venv removed")
        except PermissionError as e:
            print(f"   ❌ Permission error: {e}")
            print("   🔧 Trying alternative cleanup...")
            
            # Alternative cleanup method
            try:
                if sys.platform == "win32":
                    subprocess.run(["rmdir", "/s", "/q", str(venv_dir)], shell=True, check=False)
                else:
                    subprocess.run(["rm", "-rf", str(venv_dir)], check=False)
                print("   ✅ Alternative cleanup successful")
            except Exception as e:
                print(f"   ⚠️ Could not remove .venv: {e}")
    
    # Step 2: Create new virtual environment with different name
    alt_venv_dir = project_dir / "beat_addicts_env"
    
    print(f"\n📦 Creating BEAT ADDICTS environment: {alt_venv_dir}")
    
    try:
        # Try creating with different name to avoid permission conflicts
        result = subprocess.run([
            sys.executable, "-m", "venv", 
            str(alt_venv_dir),
            "--clear"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ BEAT ADDICTS environment created successfully")
            
            # Create activation scripts
            create_activation_scripts(alt_venv_dir)
            
            return True
        else:
            print(f"   ❌ Environment creation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Environment creation error: {e}")
        return False

def create_activation_scripts(venv_dir):
    """Create easy activation scripts"""
    print("\n📝 Creating BEAT ADDICTS activation scripts...")
    
    project_dir = Path(__file__).parent
    
    # Windows batch script
    if sys.platform == "win32":
        activate_script = project_dir / "activate_beat_addicts.bat"
        script_content = f'''@echo off
echo 🎵 BEAT ADDICTS - Activating Professional Environment
call "{venv_dir}\\Scripts\\activate.bat"
echo ✅ BEAT ADDICTS environment activated
echo 🚀 Install dependencies: pip install -r beat_addicts_core\\requirements.txt
echo 🌐 Start studio: cd beat_addicts_core && python run.py
cmd /k
'''
        with open(activate_script, 'w') as f:
            f.write(script_content)
        print(f"   ✅ Created: {activate_script}")
    
    # Cross-platform Python script
    py_activate_script = project_dir / "activate_beat_addicts.py"
    py_script_content = f'''#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Environment Activator
Cross-platform activation for BEAT ADDICTS
"""

import os
import sys
import subprocess
from pathlib import Path

def activate_beat_addicts():
    """Activate BEAT ADDICTS environment and run setup"""
    print("🎵 BEAT ADDICTS - Professional Environment Activator")
    print("=" * 50)
    
    venv_dir = Path(__file__).parent / "beat_addicts_env"
    
    if not venv_dir.exists():
        print("❌ BEAT ADDICTS environment not found")
        print("Run: python fix_venv_permissions.py")
        return False
    
    # Determine activation script
    if sys.platform == "win32":
        activate_script = venv_dir / "Scripts" / "activate.bat"
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:
        activate_script = venv_dir / "bin" / "activate"
        python_exe = venv_dir / "bin" / "python"
    
    if not python_exe.exists():
        print("❌ Python executable not found in environment")
        return False
    
    print("✅ BEAT ADDICTS environment found")
    print(f"🐍 Using: {{python_exe}}")
    
    # Install dependencies
    print("📦 Installing BEAT ADDICTS dependencies...")
    try:
        result = subprocess.run([
            str(python_exe), "-m", "pip", "install", 
            "-r", "beat_addicts_core/requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed")
        else:
            print(f"⚠️ Dependency installation issues: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Could not install dependencies: {{e}}")
    
    # Run BEAT ADDICTS
    print("🚀 Starting BEAT ADDICTS Studio...")
    try:
        os.chdir("beat_addicts_core")
        subprocess.run([str(python_exe), "run.py"])
    except Exception as e:
        print(f"❌ Could not start BEAT ADDICTS: {{e}}")
        return False
    
    return True

if __name__ == "__main__":
    activate_beat_addicts()
'''
    
    with open(py_activate_script, 'w') as f:
        f.write(py_script_content)
    print(f"   ✅ Created: {py_activate_script}")

def run_without_venv():
    """Run BEAT ADDICTS directly without virtual environment"""
    print("\n🚀 BEAT ADDICTS - Direct System Installation")
    print("=" * 50)
    
    print("Installing BEAT ADDICTS dependencies to system Python...")
    
    try:
        # Install minimal dependencies
        deps = ["flask==3.0.0", "colorama==0.4.6"]
        
        for dep in deps:
            print(f"   Installing {dep}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", dep, "--user"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ {dep} installed")
            else:
                print(f"   ❌ {dep} failed: {result.stderr}")
        
        print("\n🌐 Starting BEAT ADDICTS Studio...")
        os.chdir("beat_addicts_core")
        subprocess.run([sys.executable, "run.py"])
        
    except Exception as e:
        print(f"❌ Direct installation failed: {e}")
        return False
    
    return True

def main():
    """Main permission fixer"""
    print("🎵 BEAT ADDICTS v2.0 - Permission & Environment Fixer")
    print("🔥 Professional Music Production AI Setup 🔥")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not os.path.exists("beat_addicts_core"):
        print("❌ Please run from the BEAT ADDICTS project root directory")
        return False
    
    print("Choose BEAT ADDICTS setup method:")
    print("1. 🔧 Fix virtual environment permissions")
    print("2. 🚀 Run directly with system Python (recommended)")
    print("3. 🔍 Diagnose permission issues")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
    except (EOFError, KeyboardInterrupt):
        choice = "2"  # Default to direct system installation
    
    if choice == "1":
        success = fix_venv_permissions()
        if success:
            print("\n🎉 BEAT ADDICTS environment ready!")
            print("Run: python activate_beat_addicts.py")
        return success
        
    elif choice == "2":
        return run_without_venv()
        
    elif choice == "3":
        print("\n🔍 BEAT ADDICTS Permission Diagnosis:")
        print(f"   • Current user: {os.getenv('USERNAME', 'Unknown')}")
        print(f"   • Python path: {sys.executable}")
        print(f"   • Working directory: {os.getcwd()}")
        print(f"   • Write permissions: {os.access('.', os.W_OK)}")
        
        # Test directory creation
        test_dir = Path("test_permissions")
        try:
            test_dir.mkdir(exist_ok=True)
            test_dir.rmdir()
            print("   ✅ Directory creation/deletion: OK")
        except Exception as e:
            print(f"   ❌ Directory creation/deletion: {e}")
        
        print("\n💡 Recommendation: Use option 2 (direct system installation)")
        return True
    
    else:
        print("Invalid choice. Running direct installation...")
        return run_without_venv()

if __name__ == "__main__":
    main()
