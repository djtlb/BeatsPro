#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Debug Runner
Quick access to BEAT ADDICTS comprehensive debugging
"""

import sys
import os

def main():
    """Run BEAT ADDICTS comprehensive debug"""
    
    print("🔥 BEAT ADDICTS v2.0 - COMPREHENSIVE DEBUG RUNNER 🔥")
    print("🎵 Professional Music Production AI Diagnostics 🎵")
    print("=" * 70)
    
    # Add current directory to path
    sys.path.insert(0, os.getcwd())
    
    try:
        # Import and run BEAT ADDICTS debug system
        from debug_test import BeatAddictsDebugger
        
        debugger = BeatAddictsDebugger()
        success = debugger.run_full_debug()
        
        if success:
            print("\n🎉 BEAT ADDICTS SYSTEM: FULLY OPERATIONAL!")
            print("🔥 Ready for professional music production! 🔥")
            
            print("\n🎵 BEAT ADDICTS NEXT STEPS:")
            print("1. python run.py --create-all    # Generate ALL BEAT ADDICTS training data")
            print("2. python run.py --test-voices   # Test BEAT ADDICTS voice assignment")
            print("3. python run.py                 # Start BEAT ADDICTS Studio")
            print("4. Create professional beats! 🎧")
            
        else:
            print("\n🔧 BEAT ADDICTS SYSTEM: NEEDS ATTENTION")
            print("Check the recommendations above to fix issues.")
            print("\n🛠️ Quick fixes:")
            print("• pip install -r requirements.txt")
            print("• python install_dependencies.py")
            print("• mkdir models")
            
        return success
        
    except Exception as e:
        print(f"\n❌ BEAT ADDICTS debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
