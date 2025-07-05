#!/usr/bin/env python3
"""
BEAT ADDICTS - No Virtual Environment Runner
Direct system Python execution
"""

import os
import sys
import subprocess

def install_deps():
    """Install dependencies to user directory"""
    deps = ["flask", "colorama", "werkzeug"]
    
    for dep in deps:
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--user", dep
            ], check=False)
        except Exception:
            pass

def main():
    """Run BEAT ADDICTS without virtual environment"""
    print("BEAT ADDICTS - No VEnv Runner")
    print("Installing dependencies...")
    install_deps()
    
    print("Starting BEAT ADDICTS...")
    os.chdir("beat_addicts_core")
    
    try:
        subprocess.run([sys.executable, "run.py"])
    except Exception as e:
        print(f"Error: {e}")
        print("Try: cd beat_addicts_core && python run.py")

if __name__ == "__main__":
    main()
