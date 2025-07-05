#!/usr/bin/env python3
"""
Project Cleanup Script
Removes unnecessary files and organizes the project structure
"""

import os
import shutil
import glob
from pathlib import Path

def cleanup_project():
    """Clean up the project directory"""
    
    project_root = Path(__file__).parent
    print(f"🧹 Cleaning up project in: {project_root}")
    
    # Files and patterns to remove
    cleanup_patterns = [
        "*.pyc",
        "*.pyo", 
        "*.pyd",
        "__pycache__",
        "*.egg-info",
        ".pytest_cache",
        ".coverage",
        "*.log",
        "*.tmp",
        "*.temp",
        "*.bak",
        "*.backup",
        "*.old",
        "Thumbs.db",
        ".DS_Store",
        "*.swp",
        "*.swo",
        "*~"
    ]
    
    # Directories to remove if empty or unnecessary
    cleanup_dirs = [
        "__pycache__",
        ".pytest_cache", 
        ".mypy_cache",
        "build",
        "dist",
        "*.egg-info"
    ]
    
    # Files to keep (whitelist)
    keep_files = {
        "music_generator.py",
        "midi_processor.py", 
        "web_interface.py",
        "run.py",
        "requirements.txt",
        "README.md",
        "cleanup.py"
    }
    
    removed_count = 0
    
    # Remove files matching cleanup patterns
    for pattern in cleanup_patterns:
        for file_path in project_root.rglob(pattern):
            try:
                if file_path.is_file():
                    file_path.unlink()
                    print(f"🗑️  Removed file: {file_path.name}")
                    removed_count += 1
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                    print(f"🗑️  Removed directory: {file_path.name}")
                    removed_count += 1
            except Exception as e:
                print(f"⚠️  Could not remove {file_path}: {e}")
    
    # Remove unnecessary directories
    for dir_pattern in cleanup_dirs:
        for dir_path in project_root.rglob(dir_pattern):
            if dir_path.is_dir():
                try:
                    shutil.rmtree(dir_path)
                    print(f"🗑️  Removed directory: {dir_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️  Could not remove directory {dir_path}: {e}")
    
    # Check for unknown Python files and warn
    python_files = list(project_root.glob("*.py"))
    for py_file in python_files:
        if py_file.name not in keep_files and not py_file.name.startswith('test_'):
            print(f"⚠️  Unknown Python file found: {py_file.name}")
            response = input(f"Remove {py_file.name}? (y/N): ")
            if response.lower() == 'y':
                py_file.unlink()
                print(f"🗑️  Removed: {py_file.name}")
                removed_count += 1
    
    # Ensure required directories exist
    required_dirs = ["models", "midi_files", "templates"]
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            print(f"📁 Created directory: {dir_name}")
    
    # Create .gitignore if it doesn't exist
    gitignore_path = project_root / ".gitignore"
    if not gitignore_path.exists():
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
models/*.h5
models/*.pkl
*.mid
*.midi
*.log

# Training data (comment out if you want to track MIDI files)
midi_files/*.mid
midi_files/*.midi
"""
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
        print("📝 Created .gitignore file")
    
    print(f"\n✅ Cleanup completed! Removed {removed_count} items.")
    print(f"📊 Project structure:")
    
    # Display clean project structure
    for item in sorted(project_root.iterdir()):
        if item.is_file():
            size = item.stat().st_size
            size_str = f"({size:,} bytes)" if size > 0 else "(empty)"
            print(f"   📄 {item.name} {size_str}")
        elif item.is_dir() and not item.name.startswith('.'):
            file_count = len(list(item.rglob('*')))
            print(f"   📁 {item.name}/ ({file_count} items)")

def verify_project_integrity():
    """Verify all required files are present and working"""
    
    project_root = Path(__file__).parent
    print(f"\n🔍 Verifying project integrity...")
    
    required_files = [
        "music_generator.py",
        "midi_processor.py",
        "web_interface.py", 
        "run.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    for file_name in required_files:
        file_path = project_root / file_name
        if not file_path.exists():
            missing_files.append(file_name)
        else:
            print(f"✅ {file_name}")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    # Check if templates directory exists and has index.html
    templates_dir = project_root / "templates"
    index_html = templates_dir / "index.html"
    if not index_html.exists():
        print("⚠️  templates/index.html is missing")
        return False
    else:
        print("✅ templates/index.html")
    
    # Try importing main modules
    import sys
    sys.path.insert(0, str(project_root))
    
    try:
        import music_generator
        print("✅ music_generator.py imports successfully")
    except ImportError as e:
        print(f"❌ music_generator.py import failed: {e}")
        return False
    
    try:
        import midi_processor  
        print("✅ midi_processor.py imports successfully")
    except ImportError as e:
        print(f"❌ midi_processor.py import failed: {e}")
        return False
    
    try:
        import web_interface
        print("✅ web_interface.py imports successfully") 
    except ImportError as e:
        print(f"❌ web_interface.py import failed: {e}")
        return False
    
    print("\n🎉 Project integrity verified! All components are working.")
    return True

if __name__ == "__main__":
    print("🎵 Smart Music Generator AI - Project Cleanup")
    print("=" * 50)
    
    cleanup_project()
    
    if verify_project_integrity():
        print("\n🚀 Project is ready to use!")
        print("Run 'python run.py' to start the web interface.")
    else:
        print("\n⚠️  Some issues found. Please check the output above.")
