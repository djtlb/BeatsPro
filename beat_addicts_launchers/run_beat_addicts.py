#!/usr/bin/env python3
"""
BEAT ADDICTS - Direct Runner
No virtual environment required
"""

import os
import sys
import subprocess

def ensure_dependencies():
    """Ensure BEAT ADDICTS dependencies are installed"""
    deps = ["flask", "colorama", "werkzeug"]
    
    for dep in deps:
        try:
            __import__(dep)
        except ImportError:
            print(f"Installing {dep}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--user", dep
            ], check=False, capture_output=True)

def main():
    """Main BEAT ADDICTS runner"""
    print("BEAT ADDICTS v2.0 - Direct Runner")
    print("=" * 35)
    
    # Ensure dependencies
    ensure_dependencies()
    
    # Navigate to core directory
    core_dir = os.path.join(os.path.dirname(__file__), "beat_addicts_core")
    
    if os.path.exists(core_dir):
        os.chdir(core_dir)
        print("Starting BEAT ADDICTS Studio...")
        print("Access at: http://localhost:5000")
        
        try:
            subprocess.run([sys.executable, "run.py"])
        except KeyboardInterrupt:
            print("\nBEAT ADDICTS stopped by user")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Error: beat_addicts_core directory not found")

if __name__ == "__main__":
    main()
