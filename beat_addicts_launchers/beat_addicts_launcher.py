#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS v2.0 - Main Launcher
Professional Music Production AI System Launcher - Fixed Version
"""

import os
import sys
import subprocess
# Import for music_generator_app
# sys.path.append('.')
# Import for app
# sys.path.append('sunoai-1.0.7')
# Import for fix_web_interface
# sys.path.append('beat_addicts_core')
# Import for web_interface
# sys.path.append('beat_addicts_core')

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
            
            # Run directly as subprocess to avoid import issues
            result = subprocess.run([sys.executable, 'run.py'], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Subprocess failed with error:")
                print(result.stderr)
            else:
                print(result.stdout)
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Error running BEAT ADDICTS: {e}")
            return False
        finally:
            os.chdir(original_cwd)
    else:
        print("⚠️ Organized structure not found, trying direct run")
        
        # Try current directory
        if os.path.exists("run.py"):
            try:
                subprocess.run([sys.executable, "run.py"])
                return True
            except Exception as e:
                print(f"❌ Could not run BEAT ADDICTS: {e}")
                return False
        else:
            print("❌ Could not find BEAT ADDICTS run.py")
            print("Please run from the beat_addicts_core directory:")
            print("   cd beat_addicts_core")
            print("   python run.py")
            return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n🔧 Troubleshooting:")
        print("1. cd beat_addicts_core")
        print("2. python fix_all_problems.py")
        print("3. python run.py")
