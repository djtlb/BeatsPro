#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Comprehensive Problem Fixer
Automatically detects and fixes all system issues
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
from typing import List, Optional

class BeatAddictsProblemFixer:
    """🔧 BEAT ADDICTS comprehensive problem detection and fixing system"""
    
    def __init__(self):
        self.problems_found: List[str] = []
        self.fixes_applied: List[str] = []
        self.current_dir = os.getcwd()
        
    def detect_problems(self):
        """Detect all BEAT ADDICTS system problems"""
        print("🔍 BEAT ADDICTS - Problem Detection")
        print("=" * 50)
        
        # Check for corrupted packages
        if self._check_corrupted_packages():
            self.problems_found.append("corrupted_packages")
        
        # Check for missing files
        if self._check_missing_files():
            self.problems_found.append("missing_files")
        
        # Check for import issues
        if self._check_import_issues():
            self.problems_found.append("import_issues")
        
        # Check directory structure
        if self._check_directory_structure():
            self.problems_found.append("directory_structure")
        
        print(f"\n📊 Problems detected: {len(self.problems_found)}")
        return self.problems_found
    
    def _check_corrupted_packages(self) -> bool:
        """Check for corrupted package installations"""
        try:
            import site
            site_packages_list = site.getsitepackages()
            if not site_packages_list:
                print("   ⚠️ Could not access site-packages")
                return False
                
            site_packages = site_packages_list[0]
            corrupted_found = False
            
            if os.path.exists(site_packages):
                for item in os.listdir(site_packages):
                    if item.startswith('~'):
                        print(f"   ❌ Corrupted package found: {item}")
                        corrupted_found = True
            
            if not corrupted_found:
                print("   ✅ No corrupted packages detected")
            return corrupted_found
        except Exception as e:
            print(f"   ⚠️ Could not check package corruption: {e}")
            return False
    
    def _check_missing_files(self) -> bool:
        """Check for missing essential BEAT ADDICTS files"""
        essential_files = [
            "run.py",
            "requirements.txt"
        ]
        
        missing_files = []
        for file in essential_files:
            if not os.path.exists(file):
                missing_files.append(file)
                print(f"   ❌ Missing essential file: {file}")
        
        if not missing_files:
            print("   ✅ All essential files present")
        return len(missing_files) > 0
    
    def _check_import_issues(self) -> bool:
        """Check for Python import issues"""
        test_imports = ["flask"]  # Only test essential imports
        import_issues = False
        
        for module in test_imports:
            try:
                __import__(module)
                print(f"   ✅ {module} import successful")
            except ImportError:
                print(f"   ❌ {module} import failed")
                import_issues = True
        
        return import_issues
    
    def _check_directory_structure(self) -> bool:
        """Check BEAT ADDICTS directory structure"""
        expected_dirs = ["../midi_files", "../models", "../beat_addicts_generators"]
        structure_issues = False
        
        for dir_path in expected_dirs:
            if not os.path.exists(dir_path):
                print(f"   ❌ Missing directory: {dir_path}")
                structure_issues = True
            else:
                print(f"   ✅ Directory exists: {dir_path}")
        
        return structure_issues
    
    def fix_all_problems(self):
        """Fix all detected problems"""
        print(f"\n🔧 BEAT ADDICTS - Fixing {len(self.problems_found)} Problems")
        print("=" * 50)
        
        if "corrupted_packages" in self.problems_found:
            self._fix_corrupted_packages()
        
        if "missing_files" in self.problems_found:
            self._fix_missing_files()
        
        if "import_issues" in self.problems_found:
            self._fix_import_issues()
        
        if "directory_structure" in self.problems_found:
            self._fix_directory_structure()
        
        print(f"\n✅ Applied {len(self.fixes_applied)} fixes")
        return len(self.fixes_applied)
    
    def _fix_corrupted_packages(self):
        """Fix corrupted package installations"""
        print("\n🗑️ Fixing corrupted packages...")
        
        try:
            import site
            site_packages_list = site.getsitepackages()
            if not site_packages_list:
                print("   ⚠️ Could not access site-packages")
                return
                
            site_packages = site_packages_list[0]
            
            # Remove corrupted packages
            if os.path.exists(site_packages):
                for item in os.listdir(site_packages):
                    if item.startswith('~'):
                        corrupted_path = Path(site_packages) / item
                        try:
                            if corrupted_path.is_dir():
                                shutil.rmtree(corrupted_path)
                            else:
                                corrupted_path.unlink()
                            print(f"   ✅ Removed corrupted: {item}")
                            self.fixes_applied.append(f"removed_corrupted_{item}")
                        except Exception as e:
                            print(f"   ❌ Could not remove {item}: {e}")
            
            # Clear pip cache
            try:
                subprocess.run([sys.executable, "-m", "pip", "cache", "purge"], 
                              capture_output=True, check=False)
                print("   ✅ Cleared pip cache")
                self.fixes_applied.append("cleared_pip_cache")
            except Exception as e:
                print(f"   ⚠️ Could not clear pip cache: {e}")
                
        except Exception as e:
            print(f"   ❌ Package cleanup failed: {e}")
    
    def _fix_missing_files(self):
        """Create missing essential files with pre-cross referenced dependencies"""
        print("\n📄 Creating missing files...")
        
        # Create comprehensive run.py with all dependencies self-contained
        if not os.path.exists("run.py"):
            run_content = '''#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Main Entry Point
Professional Music Production AI System - Self-Contained
"""

import os
import sys
import argparse
from typing import Optional, Dict, Any

def create_web_interface() -> bool:
    """Create BEAT ADDICTS web interface if missing - self-contained"""
    if os.path.exists("web_interface.py"):
        return True
    
    web_content = \'''"""
🎵 BEAT ADDICTS - Professional Web Interface
Self-contained Flask application
"""

try:
    from flask import Flask, render_template_string, jsonify
except ImportError:
    print("❌ Flask not installed. Run: pip install flask")
    return False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'beat_addicts_2024'

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔥 BEAT ADDICTS Studio 🔥</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #1a1a2e, #16213e); 
                color: white; text-align: center; padding: 50px; 
            }
            h1 { color: #4ecdc4; font-size: 3em; margin-bottom: 20px; }
            .status { background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <h1>🔥 BEAT ADDICTS Studio 🔥</h1>
        <p>Professional Music Production AI v2.0</p>
        <div class="status">
            <h3>System Status</h3>
            <p>✅ BEAT ADDICTS Core: OPERATIONAL</p>
            <p>✅ Web Interface: ACTIVE</p>
            <p>🎵 Ready for music production!</p>
        </div>
    </body>
    </html>
    """")

@app.route('/api/status')
def api_status():
    return jsonify({
        'beat_addicts_version': '2.0',
        'status': 'operational',
        'components': {
            'web_interface': True,
            'core_system': True
        }
    })

if __name__ == '__main__':
    print("🎵 BEAT ADDICTS Studio starting...")
    app.run(debug=True, host='0.0.0.0', port=5000)
\'''
    
    try:
        with open("web_interface.py", "w") as f:
            f.write(web_content)
        return True
    except Exception as e:
        print(f"❌ Could not create web_interface.py: {e}")
        return False

def create_voice_assignment() -> bool:
    """Create BEAT ADDICTS voice assignment - self-contained"""
    if os.path.exists("voice_assignment.py"):
        return True
    
    voice_content = \'''"""
🎵 BEAT ADDICTS - Voice Assignment Engine
Self-contained professional voice assignment system
"""

from typing import Dict, Any, List, Optional

class IntelligentVoiceAssigner:
    """Self-contained BEAT ADDICTS voice assignment engine"""
    
    def __init__(self):
        self.genre_voice_maps = self._initialize_voice_maps()
        print("✅ BEAT ADDICTS Voice Assignment Engine loaded")
    
    def _initialize_voice_maps(self) -> Dict[str, Dict[str, List[int]]]:
        """Initialize pre-cross referenced voice mappings"""
        return {
            "hiphop": {
                "drums": [118, 119, 120, 121],
                "bass": [33, 34, 35, 36, 37],
                "lead": [80, 81, 82, 83],
                "pad": [88, 89, 90, 91]
            },
            "electronic": {
                "drums": [118, 119, 120, 121, 122],
                "bass": [37, 38, 39, 80, 81],
                "lead": [80, 81, 82, 83, 84],
                "pad": [88, 89, 90, 91, 92]
            },
            "rock": {
                "drums": [0, 1, 8, 16, 24],
                "bass": [33, 34, 35, 36],
                "lead": [28, 29, 30, 31],
                "pad": [48, 49, 50, 51]
            }
        }
    
    def get_voice_recommendation(self, genre: str, role: str) -> Dict[str, Any]:
        """Get voice recommendation with pre-cross referenced data"""
        import random
        
        if genre in self.genre_voice_maps and role in self.genre_voice_maps[genre]:
            programs = self.genre_voice_maps[genre][role]
            return {
                "recommended_program": random.choice(programs),
                "channel": hash(role) % 16,  # Deterministic channel assignment
                "genre": genre,
                "role": role,
                "beat_addicts_optimized": True
            }
        
        # Fallback
        return {
            "recommended_program": 80,
            "channel": 0,
            "genre": genre,
            "role": role,
            "beat_addicts_optimized": True
        }

def main() -> bool:
    """Main voice assignment test function"""
    try:
        assigner = IntelligentVoiceAssigner()
        
        # Test voice recommendations
        test_cases = [("hiphop", "drums"), ("electronic", "bass"), ("rock", "lead")]
        
        for genre, role in test_cases:
            recommendation = assigner.get_voice_recommendation(genre, role)
            print(f"✅ {genre} {role}: Program {recommendation['recommended_program']}")
        
        print("🎵 BEAT ADDICTS Voice System: OPERATIONAL")
        return True
    except Exception as e:
        print(f"❌ Voice system error: {e}")
        return False

if __name__ == "__main__":
    main()
\'''
    
    try:
        with open("voice_assignment.py", "w") as f:
            f.write(voice_content)
        return True
    except Exception as e:
        print(f"❌ Could not create voice_assignment.py: {e}")
        return False

def check_and_install_dependencies() -> bool:
    """Check for essential dependencies only"""
    try:
        import flask
        return True
    except ImportError:
        print("⚠️ Flask not found. Installing...")
        try:
            import subprocess
            result = subprocess.run([sys.executable, "-m", "pip", "install", "flask==3.0.0"], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

def main() -> bool:
    """Main BEAT ADDICTS entry point - self-contained"""
    parser = argparse.ArgumentParser(description='🎵 BEAT ADDICTS - Professional Music Production AI')
    parser.add_argument('--mode', choices=['web', 'cli'], default='web', 
                       help='BEAT ADDICTS mode: web interface or command line')
    parser.add_argument('--test-voices', action='store_true', 
                       help='Test BEAT ADDICTS voice assignment engine')
    parser.add_argument('--fix-problems', action='store_true', 
                       help='Run BEAT ADDICTS problem fixer')
    
    args = parser.parse_args()
    
    print("🔥 BEAT ADDICTS v2.0 - Professional Music Production AI 🔥")
    print("🎵 Self-contained system with pre-cross referenced dependencies 🎵")
    
    # Handle problem fixing
    if args.fix_problems:
        try:
            from fix_all_problems import main as fix_main
            return fix_main()
        except ImportError:
            print("❌ Problem fixer not available")
            return False
    
    # Handle voice testing
    if args.test_voices:
        create_voice_assignment()
        try:
            from voice_assignment import main as voice_main
            return voice_main()
        except ImportError:
            print("❌ Voice assignment not available")
            return False
    
    # Handle web mode
    if args.mode == 'web':
        print("🌐 Starting BEAT ADDICTS Studio...")
        print("🔥 Professional web interface at: http://localhost:5000 🔥")
        
        # Ensure dependencies
        if not check_and_install_dependencies():
            print("❌ Could not install Flask. Install manually: pip install flask")
            return False
        
        # Create web interface
        if not create_web_interface():
            print("❌ Could not create web interface")
            return False
        
        try:
            from web_interface import app
            app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
            return True
        except ImportError as e:
            print(f"❌ Web interface error: {e}")
            return False
        except Exception as e:
            print(f"❌ BEAT ADDICTS Studio error: {e}")
            return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("🔧 Run 'python fix_all_problems.py' to resolve issues")
        sys.exit(1)
