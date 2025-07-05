#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS v2.0 - Main Launcher
Professional Music Production AI System Launcher
"""

import os
import sys
import argparse

def main():
    """Main BEAT ADDICTS launcher that works from any directory"""
    print("🔥 BEAT ADDICTS v2.0 - Professional Music Production AI 🔥")
    print("🎵 Launching from organized project structure 🎵")
    
    # Find the correct directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    core_dir = os.path.join(script_dir, 'beat_addicts_core')
    
    # Check if we have the organized structure
    if os.path.exists(core_dir):
        print(f"✅ Found organized BEAT ADDICTS structure")
        
        # Change to core directory and run
        original_cwd = os.getcwd()
        try:
            os.chdir(core_dir)
            print(f"📁 Switched to: {core_dir}")
            
            # Add current directory to path
            sys.path.insert(0, core_dir)
            
            # Import and run from organized structure
            from run import main as core_main
            return core_main()
            
        except ImportError as e:
            print(f"❌ Error importing BEAT ADDICTS core: {e}")
            print("Trying alternative method...")
            
            # Alternative: run as subprocess
            import subprocess
            result = subprocess.run([sys.executable, 'run.py'] + sys.argv[1:])
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Error running BEAT ADDICTS: {e}")
            return False
        finally:
            os.chdir(original_cwd)
    else:
        print("⚠️ Organized structure not found, running from current directory")
        
        # Try to run from current directory
        try:
            from run import main as run_main
            return run_main()
        except ImportError:
            print("❌ Could not find BEAT ADDICTS run.py")
            print("Please run from the beat_addicts_core directory:")
            print("   cd beat_addicts_core")
            print("   python run.py")
            return False

if __name__ == "__main__":
    main()
