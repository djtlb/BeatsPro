#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Quick Diagnostic
Fast system check for BEAT ADDICTS readiness
"""

import os
import sys

def quick_check():
    """Quick BEAT ADDICTS system check"""
    
    print("🔥 BEAT ADDICTS - Quick Diagnostic 🔥")
    print("=" * 40)
    
    issues = []
    warnings = []
    
    # Check Python version
    if sys.version_info >= (3, 8):
        print("✅ Python version: Compatible")
    else:
        print("❌ Python version: Too old")
        issues.append("Upgrade Python to 3.8+")
    
    # Check critical files
    critical_files = [
        "run.py", "voice_assignment.py", "requirements.txt"
    ]
    
    for file in critical_files:
        if os.path.exists(file):
            print(f"✅ {file}: Found")
        else:
            print(f"❌ {file}: Missing")
            issues.append(f"Missing {file}")
    
    # Check dependencies
    deps = ["numpy", "flask", "pretty_midi", "mido"]
    for dep in deps:
        try:
            __import__(dep)
            print(f"✅ {dep}: Installed")
        except ImportError:
            print(f"❌ {dep}: Missing")
            issues.append(f"Install {dep}")
    
    # Check directories
    dirs = ["models", "midi_files", "templates"]
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/: Found")
        else:
            print(f"⚠️ {dir_name}/: Missing")
            warnings.append(f"Create {dir_name} directory")
    
    # Summary
    print("\n" + "=" * 40)
    if not issues and not warnings:
        print("🎉 BEAT ADDICTS: READY TO ROCK!")
        print("Run: python run.py")
    elif not issues:
        print("✅ BEAT ADDICTS: Good to go!")
        print("Minor issues can be fixed later")
    else:
        print(f"🔧 BEAT ADDICTS: {len(issues)} issues need fixing")
        for issue in issues:
            print(f"  • {issue}")
    
    return len(issues) == 0

if __name__ == "__main__":
    quick_check()
