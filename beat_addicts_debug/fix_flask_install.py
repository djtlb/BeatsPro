#!/usr/bin/env python3
"""
BEAT ADDICTS - Flask Installation Fixer
Fix pip installation issues
"""

import os
import sys
import subprocess

def fix_flask_install():
    """Fix Flask installation issues"""
    print("BEAT ADDICTS - Flask Installation Fixer")
    print("=" * 40)
    
    # Try multiple installation methods
    methods = [
        ("Virtual Environment Install", install_in_venv),
        ("User Install", install_user),
        ("System Install", install_system),
        ("Direct Install", install_direct)
    ]
    
    for method_name, method_func in methods:
        print(f"Trying: {method_name}")
        if method_func():
            print(f"✅ Success: {method_name}")
            return True
        print(f"❌ Failed: {method_name}")
    
    return False

def install_in_venv():
    """Install in virtual environment"""
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "flask==3.0.0", "colorama==0.4.6", "werkzeug==3.0.1"
        ], capture_output=True, text=True, timeout=60)
        
        return result.returncode == 0
    except Exception:
        return False

def install_user():
    """Install with --user flag"""
    try:
        # Deactivate virtual environment first
        if 'VIRTUAL_ENV' in os.environ:
            del os.environ['VIRTUAL_ENV']
        
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "--user",
            "flask==3.0.0", "colorama==0.4.6", "werkzeug==3.0.1"
        ], capture_output=True, text=True, timeout=60)
        
        return result.returncode == 0
    except Exception:
        return False

def install_system():
    """Install to system Python"""
    try:
        result = subprocess.run([
            "python", "-m", "pip", "install",
            "flask==3.0.0", "colorama==0.4.6", "werkzeug==3.0.1"
        ], capture_output=True, text=True, timeout=60)
        
        return result.returncode == 0
    except Exception:
        return False

def install_direct():
    """Direct pip install"""
    try:
        result = subprocess.run([
            "pip", "install", 
            "flask", "colorama", "werkzeug"
        ], capture_output=True, text=True, timeout=60)
        
        return result.returncode == 0
    except Exception:
        return False

def test_flask():
    """Test if Flask is available"""
    try:
        import flask
        print(f"✅ Flask {flask.__version__} available")
        return True
    except ImportError:
        print("❌ Flask not available")
        return False

if __name__ == "__main__":
    if fix_flask_install():
        test_flask()
        print("🚀 Ready to run BEAT ADDICTS!")
    else:
        print("❌ Flask installation failed")
