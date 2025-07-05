#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Dependency Installer
Professional Music Production AI - Automated Setup
"""

import subprocess
import sys
import os

def install_beat_addicts_dependencies():
    """Install all BEAT ADDICTS dependencies"""
    print("🎵 BEAT ADDICTS - Dependency Installer")
    print("🔥 Professional Music Production AI Setup 🔥")
    print("=" * 60)
    
    # Core dependencies for BEAT ADDICTS web interface
    core_deps = [
        'flask==3.0.0',
        'werkzeug==3.0.1', 
        'jinja2==3.1.2'
    ]
    
    # Optional dependencies for full BEAT ADDICTS functionality
    optional_deps = [
        'numpy==1.26.4',
        'pretty_midi==0.2.10',
        'mido==1.3.2'
    ]
    
    print("📦 Installing BEAT ADDICTS core dependencies...")
    
    for dep in core_deps:
        try:
            print(f"   Installing {dep}...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ {dep} installed successfully")
            else:
                print(f"   ❌ {dep} failed: {result.stderr}")
        except Exception as e:
            print(f"   ❌ {dep} error: {e}")
    
    print(f"\n📦 Installing BEAT ADDICTS optional dependencies...")
    
    for dep in optional_deps:
        try:
            print(f"   Installing {dep}...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ {dep} installed successfully")
            else:
                print(f"   ⚠️ {dep} failed (optional): {result.stderr}")
        except Exception as e:
            print(f"   ⚠️ {dep} error (optional): {e}")
    
    print(f"\n🎉 BEAT ADDICTS dependency installation complete!")
    print(f"🚀 Try running: python run.py")

if __name__ == "__main__":
    install_beat_addicts_dependencies()
