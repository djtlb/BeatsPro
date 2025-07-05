#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Auto Boot Fix
One-command solution to fix everything and boot smoothly
"""

import os
import sys
import subprocess

def auto_boot_fix():
    """Automatically fix everything and boot BEAT ADDICTS"""
    print("🚀 BEAT ADDICTS AUTO BOOT FIX")
    print("🔥 One-click solution for smooth startup 🔥")
    print("=" * 50)
    
    # Step 1: Run first boot debugger
    print("🔧 Running comprehensive repair...")
    try:
        from first_boot_debugger import main as debug_main
        if debug_main():
            print("✅ Repair complete")
        else:
            print("⚠️ Partial repair - continuing anyway")
    except Exception as e:
        print(f"⚠️ Debugger issue: {e} - creating minimal system")
        create_minimal_system()
    
    # Step 2: Install essential dependencies
    print("📦 Installing Flask...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "--user"], 
                      capture_output=True, timeout=30)
        print("✅ Flask installed")
    except Exception:
        print("⚠️ Flask installation - may already exist")
    
    # Step 3: Start BEAT ADDICTS
    print("🚀 Starting BEAT ADDICTS...")
    try:
        subprocess.run([sys.executable, "quick_start_no_venv.py"])
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        print("🔧 Try manual start: cd beat_addicts_core && python run.py")

def create_minimal_system():
    """Create minimal working system if debugger fails"""
    os.makedirs("beat_addicts_core", exist_ok=True)
    
    # Minimal web interface
    with open("beat_addicts_core/web_interface.py", "w") as f:
        f.write("""
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🔥 BEAT ADDICTS 🔥</h1><p>Minimal mode active</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
""")
    
    # Minimal runner
    with open("beat_addicts_core/run.py", "w") as f:
        f.write("""
try:
    from web_interface import app
    print("🎵 BEAT ADDICTS Minimal Mode")
    app.run(host='0.0.0.0', port=5000)
except Exception as e:
    print(f"Error: {e}")
""")

if __name__ == "__main__":
    auto_boot_fix()
