#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Quick Start (No Virtual Environment)
Direct system installation for immediate use
"""

import os
import sys
import subprocess

def quick_start():
    """Quick start BEAT ADDICTS without virtual environment"""
    print("🔥 BEAT ADDICTS v2.0 - Quick Start 🔥")
    print("🎵 Professional Music Production AI 🎵")
    print("=" * 50)
    
    # Install minimal dependencies
    print("📦 Installing essential dependencies...")
    deps = ["flask==3.0.0", "colorama==0.4.6", "werkzeug==3.0.1"]
    
    for dep in deps:
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", dep, "--user", "--no-warn-script-location"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"   ✅ {dep}")
            else:
                print(f"   ⚠️ {dep} (may already be installed)")
        except Exception as e:
            print(f"   ⚠️ {dep} (installation skipped: {e})")
    
    # Navigate to core and start
    print("\n🚀 Starting BEAT ADDICTS Studio...")
    try:
        os.chdir("beat_addicts_core")
        
        # Check if run.py exists, create if missing
        if not os.path.exists("run.py"):
            print("📝 Creating BEAT ADDICTS run.py...")
            create_basic_run_py()
        
        print("🌐 BEAT ADDICTS Studio starting at: http://localhost:5000")
        subprocess.run([sys.executable, "run.py"])
        
    except Exception as e:
        print(f"❌ Could not start BEAT ADDICTS: {e}")
        print("🔧 Try: python fix_venv_permissions.py")

def create_basic_run_py():
    """Create basic run.py if missing"""
    basic_run_content = '''#!/usr/bin/env python3
"""Basic BEAT ADDICTS runner"""

import os
import sys

def main():
    print("🎵 BEAT ADDICTS Basic Runner")
    try:
        from web_interface import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except ImportError:
        print("❌ Web interface not available")
        return False
    return True

if __name__ == "__main__":
    main()
'''
    
    with open("run.py", "w") as f:
        f.write(basic_run_content)
    print("✅ Created basic run.py")

if __name__ == "__main__":
    quick_start()
    with open("run.py", "w") as f:
        f.write(basic_run_content)
    print("✅ Created basic run.py")

if __name__ == "__main__":
    quick_start()
