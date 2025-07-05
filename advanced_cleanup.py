#!/usr/bin/env python3
"""
🧹 BEAT ADDICTS - Advanced Directory Cleanup Tool
Organizes all scattered files into proper structure
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class BeatAddictsOrganizer:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.cleanup_report = {
            "cleanup_date": datetime.now().isoformat(),
            "files_moved": [],
            "files_removed": [],
            "directories_created": [],
            "errors": []
        }
        
    def organize_project(self):
        """Main organization function"""
        print("🧹" * 20)
        print("🎵 BEAT ADDICTS - ADVANCED DIRECTORY CLEANUP 🎵")
        print("🧹" * 20)
        print("📁 Organizing project structure...")
        print()
        
        # Create organized directory structure
        self.create_directory_structure()
        
        # Move files to appropriate locations
        self.organize_launcher_files()
        self.organize_config_files()
        self.organize_debug_files()
        self.organize_requirements_files()
        self.organize_generator_files()
        self.organize_temp_files()
        self.organize_duplicate_files()
        
        # Clean up empty directories and old files
        self.cleanup_old_files()
        
        # Generate final report
        self.generate_cleanup_report()
        
        print("✅ Directory cleanup completed!")
        
    def create_directory_structure(self):
        """Create proper directory structure"""
        print("📁 Creating organized directory structure...")
        
        directories = [
            "beat_addicts_launchers",
            "beat_addicts_config/voice_configs",
            "beat_addicts_config/requirements", 
            "beat_addicts_debug",
            "beat_addicts_temp/old_files",
            "beat_addicts_temp/backups",
            "beat_addicts_docs/reports"
        ]
        
        for dir_path in directories:
            full_path = self.project_dir / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                self.cleanup_report["directories_created"].append(str(dir_path))
                print(f"   📁 Created: {dir_path}")
                
        print("✅ Directory structure ready!")
        print()
        
    def organize_launcher_files(self):
        """Organize all launcher and runner files"""
        print("🚀 Organizing launcher files...")
        
        launcher_files = [
            "beat_addicts_launcher.py",
            "quick_start.py",
            "quick_start_no_venv.py", 
            "quick_start.bat",
            "run_beat_addicts.py",
            "run_no_venv.py",
            "run.py",
            "activate_beat_addicts.bat",
            "master_launcher.py"
        ]
        
        launcher_dir = self.project_dir / "beat_addicts_launchers"
        
        for file in launcher_files:
            source = self.project_dir / file
            if source.exists() and source.parent != launcher_dir:
                try:
                    destination = launcher_dir / file
                    shutil.move(str(source), str(destination))
                    self.cleanup_report["files_moved"].append(f"{file} -> beat_addicts_launchers/")
                    print(f"   🚀 Moved: {file}")
                except Exception as e:
                    self.cleanup_report["errors"].append(f"Could not move {file}: {e}")
                    
        print("✅ Launcher files organized!")
        print()
        
    def organize_config_files(self):
        """Organize configuration files"""
        print("⚙️ Organizing configuration files...")
        
        # Voice configs
        voice_config_files = [
            "beat_addicts_voice_config.json",
            "beat_addicts_voice_report_electronic.json",
            "beat_addicts_voice_report_hiphop.json", 
            "beat_addicts_voice_report_rock.json",
            "bot_config.json"
        ]
        
        voice_config_dir = self.project_dir / "beat_addicts_config" / "voice_configs"
        
        for file in voice_config_files:
            source = self.project_dir / file
            if source.exists():
                try:
                    destination = voice_config_dir / file
                    shutil.move(str(source), str(destination))
                    self.cleanup_report["files_moved"].append(f"{file} -> beat_addicts_config/voice_configs/")
                    print(f"   ⚙️ Moved: {file}")
                except Exception as e:
                    self.cleanup_report["errors"].append(f"Could not move {file}: {e}")
                    
        print("✅ Configuration files organized!")
        print()
        
    def organize_debug_files(self):
        """Organize debug and diagnostic files"""
        print("🔧 Organizing debug files...")
        
        debug_files = [
            "debug_production_system.py",
            "debug_report.json",
            "first_boot_debugger.py",
            "auto_boot_fix.py",
            "fix_flask_install.py",
            "fix_permissions.py",
            "fix_venv_permissions.py",
            "install_beat_addicts_deps.py",
            "output.txt"
        ]
        
        debug_dir = self.project_dir / "beat_addicts_debug"
        
        for file in debug_files:
            source = self.project_dir / file
            if source.exists():
                try:
                    destination = debug_dir / file
                    shutil.move(str(source), str(destination))
                    self.cleanup_report["files_moved"].append(f"{file} -> beat_addicts_debug/")
                    print(f"   🔧 Moved: {file}")
                except Exception as e:
                    self.cleanup_report["errors"].append(f"Could not move {file}: {e}")
                    
        print("✅ Debug files organized!")
        print()
        
    def organize_requirements_files(self):
        """Organize all requirements files"""
        print("📦 Organizing requirements files...")
        
        requirements_files = [
            "requirements.txt",
            "requirements_emergency.txt",
            "requirements_minimal.txt", 
            "requirements_simple.txt",
            "constraints.txt"
        ]
        
        requirements_dir = self.project_dir / "beat_addicts_config" / "requirements"
        
        for file in requirements_files:
            source = self.project_dir / file
            if source.exists():
                try:
                    destination = requirements_dir / file
                    shutil.move(str(source), str(destination))
                    self.cleanup_report["files_moved"].append(f"{file} -> beat_addicts_config/requirements/")
                    print(f"   📦 Moved: {file}")
                except Exception as e:
                    self.cleanup_report["errors"].append(f"Could not move {file}: {e}")
                    
        print("✅ Requirements files organized!")
        print()
        
    def organize_generator_files(self):
        """Move scattered generator files to proper location"""
        print("🎹 Organizing generator files...")
        
        # Check for generators in root directory
        generator_files = [
            "dnb_midi_generator.py"
        ]
        
        generators_dir = self.project_dir / "beat_addicts_generators"
        
        for file in generator_files:
            source = self.project_dir / file
            if source.exists():
                try:
                    destination = generators_dir / file
                    if not destination.exists():  # Don't overwrite existing
                        shutil.move(str(source), str(destination))
                        self.cleanup_report["files_moved"].append(f"{file} -> beat_addicts_generators/")
                        print(f"   🎹 Moved: {file}")
                    else:
                        # Remove duplicate
                        source.unlink()
                        self.cleanup_report["files_removed"].append(f"Duplicate: {file}")
                        print(f"   🗑️ Removed duplicate: {file}")
                except Exception as e:
                    self.cleanup_report["errors"].append(f"Could not move {file}: {e}")
                    
        print("✅ Generator files organized!")
        print()
        
    def organize_temp_files(self):
        """Move temporary and old files"""
        print("🗂️ Organizing temporary files...")
        
        temp_files = [
            "instant_bot_lyrics_1.txt",
            "instant_bot_track_1.wav",
            "beat_addicts_cleanup_report_20250705_123531.json"
        ]
        
        temp_dir = self.project_dir / "beat_addicts_temp" / "old_files"
        
        for file in temp_files:
            source = self.project_dir / file
            if source.exists():
                try:
                    destination = temp_dir / file
                    shutil.move(str(source), str(destination))
                    self.cleanup_report["files_moved"].append(f"{file} -> beat_addicts_temp/old_files/")
                    print(f"   🗂️ Moved: {file}")
                except Exception as e:
                    self.cleanup_report["errors"].append(f"Could not move {file}: {e}")
                    
        print("✅ Temporary files organized!")
        print()
        
    def organize_duplicate_files(self):
        """Handle duplicate files"""
        print("🔍 Checking for duplicate files...")
        
        # Check for duplicates between root and core
        potential_duplicates = [
            "web_interface.py",
            "debug_production_system.py"
        ]
        
        core_dir = self.project_dir / "beat_addicts_core"
        
        for file in potential_duplicates:
            root_file = self.project_dir / file
            core_file = core_dir / file
            
            if root_file.exists() and core_file.exists():
                # Keep the core version, backup the root version
                backup_dir = self.project_dir / "beat_addicts_temp" / "backups"
                backup_file = backup_dir / f"{file}.backup"
                
                try:
                    shutil.move(str(root_file), str(backup_file))
                    self.cleanup_report["files_moved"].append(f"{file} -> beat_addicts_temp/backups/ (duplicate)")
                    print(f"   📋 Backed up duplicate: {file}")
                except Exception as e:
                    self.cleanup_report["errors"].append(f"Could not backup {file}: {e}")
                    
        print("✅ Duplicates handled!")
        print()
        
    def cleanup_old_files(self):
        """Remove unnecessary old files"""
        print("🗑️ Cleaning up old files...")
        
        # Old Java file that shouldn't be here
        java_file = self.project_dir / "sunoai.java"
        if java_file.exists():
            try:
                java_file.unlink()
                self.cleanup_report["files_removed"].append("sunoai.java")
                print("   🗑️ Removed: sunoai.java")
            except Exception as e:
                self.cleanup_report["errors"].append(f"Could not remove sunoai.java: {e}")
                
        print("✅ Old files cleaned up!")
        print()
        
    def generate_cleanup_report(self):
        """Generate final cleanup report"""
        print("📊 Generating cleanup report...")
        
        report_file = self.project_dir / "beat_addicts_docs" / "reports" / f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(report_file, 'w') as f:
                json.dump(self.cleanup_report, f, indent=2)
            print(f"   📊 Report saved: {report_file.name}")
        except Exception as e:
            print(f"   ⚠️ Could not save report: {e}")
            
        # Print summary
        print("\n📈 CLEANUP SUMMARY:")
        print(f"   📁 Directories created: {len(self.cleanup_report['directories_created'])}")
        print(f"   📄 Files moved: {len(self.cleanup_report['files_moved'])}")
        print(f"   🗑️ Files removed: {len(self.cleanup_report['files_removed'])}")
        print(f"   ❌ Errors: {len(self.cleanup_report['errors'])}")
        
        if self.cleanup_report['errors']:
            print("\n⚠️ ERRORS:")
            for error in self.cleanup_report['errors']:
                print(f"   ❌ {error}")
                
    def create_new_master_launcher(self):
        """Create updated master launcher in launchers directory"""
        print("🚀 Creating updated master launcher...")
        
        launcher_content = '''#!/usr/bin/env python3
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
            print("Starting BEAT ADDICTS Studio at: http://localhost:5000")
            app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
        except ImportError as e:
            print(f"Import error: {e}")
            print("Try running setup first")
    else:
        print("Core directory not found")

if __name__ == "__main__":
    main()
'''
        
        launcher_file = self.project_dir / "beat_addicts_launchers" / "organized_launcher.py"
        try:
            with open(launcher_file, 'w', encoding='utf-8') as f:
                f.write(launcher_content)
            print(f"   🚀 Created: {launcher_file.name}")
        except Exception as e:
            print(f"   ❌ Could not create launcher: {e}")

def main():
    """Main cleanup function"""
    organizer = BeatAddictsOrganizer()
    
    try:
        organizer.organize_project()
        organizer.create_new_master_launcher()
        
        print("\n🎉 CLEANUP COMPLETED!")
        print("=" * 50)
        print("🎵 Your BEAT ADDICTS project is now organized!")
        print("📁 All files are in their proper directories")
        print("🚀 Use: python beat_addicts_launchers/organized_launcher.py")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Cleanup failed: {e}")
        print("🔧 Manual organization may be required")

if __name__ == "__main__":
    main()
