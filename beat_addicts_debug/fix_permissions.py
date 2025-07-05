#!/usr/bin/env python3
"""
BEAT ADDICTS - Permission Fixer
Fix Windows permission issues and setup alternative environment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def fix_permissions():
    """Fix permission issues for BEAT ADDICTS"""
    print("BEAT ADDICTS - Permission Fixer")
    print("=" * 40)
    
    project_dir = Path(__file__).parent
    
    # Method 1: Clean up and try different location
    print("1. Cleaning up existing .venv...")
    venv_dir = project_dir / ".venv"
    if venv_dir.exists():
        try:
            shutil.rmtree(venv_dir)
            print("   Removed existing .venv")
        except PermissionError:
            print("   Using alternative cleanup...")
            subprocess.run(["rmdir", "/s", "/q", str(venv_dir)], shell=True, check=False)
    
    # Method 2: Try creating in user directory
    print("2. Creating virtual environment in user directory...")
    user_env_dir = Path.home() / "beat_addicts_env"
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "venv", str(user_env_dir), "--clear"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   Virtual environment created: {user_env_dir}")
            create_activation_script(user_env_dir, project_dir)
            return True
        else:
            print(f"   Failed: {result.stderr}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Method 3: Use --user pip instead
    print("3. Setting up --user pip installation...")
    return setup_user_pip()

def create_activation_script(venv_dir, project_dir):
    """Create activation script for the virtual environment"""
    activate_script = project_dir / "activate_beat_addicts.bat"
    
    script_content = f'''@echo off
echo BEAT ADDICTS - Activating Environment
call "{venv_dir}\\Scripts\\activate.bat"
echo Installing BEAT ADDICTS dependencies...
pip install flask colorama werkzeug
echo Starting BEAT ADDICTS...
cd /d "{project_dir}\\beat_addicts_core"
python run.py
pause
'''
    
    with open(activate_script, 'w') as f:
        f.write(script_content)
    
    print(f"   Created activation script: {activate_script}")
    print(f"   Run: {activate_script}")

def setup_user_pip():
    """Setup using --user pip installation"""
    print("   Installing to user directory...")
    
    deps = ["flask==3.0.0", "colorama==0.4.6", "werkzeug==3.0.1"]
    
    for dep in deps:
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "--user", dep
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   Installed: {dep}")
            else:
                print(f"   Warning: {dep} - {result.stderr}")
        except Exception as e:
            print(f"   Error with {dep}: {e}")
    
    # Create simple run script
    run_script = Path(__file__).parent / "run_beat_addicts.py"
    
    script_content = '''#!/usr/bin/env python3
"""BEAT ADDICTS Runner"""

import os
import sys

def main():
    os.chdir("beat_addicts_core")
    
    try:
        from web_interface import app
        print("BEAT ADDICTS starting at http://localhost:5000")
        app.run(debug=False, host='0.0.0.0', port=5000)
    except ImportError:
        print("Flask not available. Install: pip install --user flask")

if __name__ == "__main__":
    main()
'''
    
    with open(run_script, 'w') as f:
        f.write(script_content)
    
    print(f"   Created runner: {run_script}")
    print("   Run: python run_beat_addicts.py")
    return True

def fix_directory_permissions():
    """Fix directory permissions"""
    print("4. Fixing directory permissions...")
    
    try:
        # Make sure all directories are writable
        for root, dirs, files in os.walk("."):
            for d in dirs:
                dir_path = os.path.join(root, d)
                try:
                    os.chmod(dir_path, 0o755)
                except Exception:
                    pass
        
        print("   Directory permissions updated")
        return True
    except Exception as e:
        print(f"   Permission fix failed: {e}")
        return False

def main():
    """Main permission fixing function"""
    print("BEAT ADDICTS Permission Fixer")
    print("Fixing Windows permission issues...")
    print()
    
    # Try all methods
    methods = [
        ("Virtual Environment Fix", fix_permissions),
        ("Directory Permissions", fix_directory_permissions)
    ]
    
    for method_name, method_func in methods:
        print(f"Trying: {method_name}")
        try:
            if method_func():
                print(f"Success: {method_name}")
            else:
                print(f"Partial: {method_name}")
        except Exception as e:
            print(f"Failed: {method_name} - {e}")
        print()
    
    print("SOLUTIONS:")
    print("1. Run: activate_beat_addicts.bat (if created)")
    print("2. Run: python run_beat_addicts.py")
    print("3. Manual: cd beat_addicts_core && python run.py")

if __name__ == "__main__":
    main()
