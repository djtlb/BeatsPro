#!/usr/bin/env python3
"""
BEAT ADDICTS v2.0 - ORGANIZED MASTER LAUNCHER
Launches from organized directory structure
"""

import os
import sys
from pathlib import Path

def main():
    """Main launcher with organized structure"""
    print("BEAT ADDICTS v2.0 - Organized Launch")
    
    # Get project root directory
    launcher_dir = Path(__file__).parent
    project_dir = launcher_dir.parent
    
    print(f"Project directory: {project_dir}")
    
    # Add paths for organized structure
    sys.path.insert(0, str(project_dir / "beat_addicts_core"))
    sys.path.insert(0, str(project_dir / "beat_addicts_generators"))
    
    # Change to core directory for execution
    core_dir = project_dir / "beat_addicts_core"
    if core_dir.exists():
        os.chdir(str(core_dir))
        
        try:
            from web_interface import app
# Import for music_generator_app
# sys.path.append('.')
# Import for fix_web_interface
# sys.path.append('beat_addicts_core')
            print("Starting BEAT ADDICTS Studio at: http://localhost:5000")
            app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
        except ImportError as e:
            print(f"Import error: {e}")
            print("Try running setup first")
    else:
        print("Core directory not found")

if __name__ == "__main__":
    main()
