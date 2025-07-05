#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Corrupted Package Fixer
Fix invalid distributions like ~umpy in virtual environment
"""

import os
import sys
import subprocess
import shutil
import site
from pathlib import Path

def fix_corrupted_numpy():
    """Fix the corrupted ~umpy distribution"""
    print("🔧 BEAT ADDICTS - Fixing Corrupted Package Installation")
    print("=" * 60)
    
    # Step 1: Find and remove corrupted packages
    print("🗑️ Step 1: Removing corrupted packages...")
    
    try:
        # Get site-packages directory
        site_packages = site.getsitepackages()[0]
        print(f"   📁 Site-packages: {site_packages}")
        
        # Look for corrupted packages
        corrupted_patterns = ["~umpy", "~cipy", "~ensorflow", "~ido", "~ask"]
        
        for pattern in corrupted_patterns:
            corrupted_path = Path(site_packages) / pattern
            if corrupted_path.exists():
                print(f"   🗑️ Found corrupted package: {pattern}")
                try:
                    if corrupted_path.is_dir():
                        shutil.rmtree(corrupted_path)
                    else:
                        corrupted_path.unlink()
                    print(f"   ✅ Removed {pattern}")
                except Exception as e:
                    print(f"   ❌ Could not remove {pattern}: {e}")
            else:
                print(f"   ✅ No {pattern} corruption found")
                
    except Exception as e:
        print(f"   ⚠️ Could not access site-packages: {e}")
    
    # Step 2: Uninstall problematic packages
    print("\n🔧 Step 2: Uninstalling problematic packages...")
    
    packages_to_remove = ["numpy", "scipy", "tensorflow", "mido", "flask"]
    
    for package in packages_to_remove:
        try:
            print(f"   Uninstalling {package}...")
            result = subprocess.run([sys.executable, "-m", "pip", "uninstall", package, "-y"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ {package} uninstalled")
            else:
                print(f"   ⚠️ {package} not found or already removed")
        except Exception as e:
            print(f"   ⚠️ Error uninstalling {package}: {e}")
    
    # Step 3: Clear pip cache
    print("\n🧹 Step 3: Clearing pip cache...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "cache", "purge"], 
                      capture_output=True, text=True)
        print("   ✅ Pip cache cleared")
    except Exception as e:
        print(f"   ⚠️ Could not clear cache: {e}")
    
    # Step 4: Reinstall clean packages
    print("\n📦 Step 4: Installing clean packages...")
    
    clean_packages = [
        "numpy==1.26.4",
        "flask==3.0.0", 
        "werkzeug==3.0.1",
        "jinja2==3.1.2",
        "colorama==0.4.6",
        "tqdm==4.66.1"
    ]
    
    for package in clean_packages:
        try:
            print(f"   Installing {package}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", package, "--no-cache-dir"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ {package} installed successfully")
            else:
                print(f"   ❌ {package} failed: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error installing {package}: {e}")
    
    # Step 5: Verify installation
    print("\n🧪 Step 5: Verifying installation...")
    
    test_imports = ["numpy", "flask", "colorama", "tqdm"]
    
    for module in test_imports:
        try:
            __import__(module)
            print(f"   ✅ {module} import successful")
        except ImportError:
            print(f"   ❌ {module} import failed")
    
    print("\n🎉 BEAT ADDICTS package cleanup complete!")
    print("✅ Corrupted distributions should be fixed")
    print("🚀 Try running: python run.py")

def main():
    """Main function to fix corrupted packages"""
    try:
        fix_corrupted_numpy()
        return True
    except Exception as e:
        print(f"❌ Package fix failed: {e}")
        return False

if __name__ == "__main__":
    main()
