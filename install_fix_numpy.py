#!/usr/bin/env python3
"""
NumPy Import Fix for Smart Music Generator AI
Fixes the common "numpy source directory" error
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print('='*60)

def check_numpy_source_conflict():
    """Check if we're in a numpy source directory"""
    print_header("CHECKING NUMPY SOURCE CONFLICT")
    
    current_dir = Path.cwd()
    potential_conflicts = [
        current_dir / "numpy",
        current_dir / "numpy.py",
        current_dir / "__pycache__" / "numpy"
    ]
    
    conflicts_found = []
    for path in potential_conflicts:
        if path.exists():
            conflicts_found.append(str(path))
            print(f"❌ Found potential conflict: {path}")
    
    if conflicts_found:
        print(f"\n⚠️ {len(conflicts_found)} potential conflicts found")
        return conflicts_found
    else:
        print("✅ No numpy source conflicts detected")
        return []

def fix_numpy_installation():
    """Fix numpy installation issues"""
    print_header("FIXING NUMPY INSTALLATION")
    
    # Step 1: Uninstall and reinstall numpy
    commands = [
        "pip uninstall numpy -y",
        "pip install --no-cache-dir numpy",
        "pip install --upgrade numpy"
    ]
    
    for cmd in commands:
        print(f"\n▶️ Running: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Success!")
            else:
                print(f"⚠️ Warning: {result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_numpy_import():
    """Test if numpy can be imported correctly"""
    print_header("TESTING NUMPY IMPORT")
    
    try:
        # Test basic import
        import numpy as np
        print("✅ NumPy basic import successful")
        
        # Test basic operations
        arr = np.array([1, 2, 3, 4, 5])
        mean_val = np.mean(arr)
        print(f"✅ NumPy operations working (mean test: {mean_val})")
        
        # Test version
        print(f"✅ NumPy version: {np.__version__}")
        
        return True
        
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ NumPy operation failed: {e}")
        return False

def create_numpy_fallback():
    """Create a fallback system for numpy functionality"""
    print_header("CREATING NUMPY FALLBACK SYSTEM")
    
    fallback_code = '''# NumPy Fallback for Smart Music Generator AI
"""
This module provides basic numpy-like functionality when numpy is not available.
"""

class NumpyFallback:
    """Fallback implementation for basic numpy operations"""
    
    @staticmethod
    def array(values):
        """Create array-like list"""
        return list(values)
    
    @staticmethod
    def mean(values):
        """Calculate mean of values"""
        return sum(values) / len(values) if values else 0
    
    @staticmethod
    def clip(value, min_val, max_val):
        """Clip value between min and max"""
        return max(min_val, min(max_val, value))
    
    @staticmethod
    def random():
        """Access to random module"""
        import random
        return random
    
    def __version__(self):
        return "fallback-1.0"

# Create numpy-like interface
numpy_fallback = NumpyFallback()
'''
    
    with open("numpy_fallback.py", "w") as f:
        f.write(fallback_code)
    
    print("✅ Created numpy_fallback.py")
    print("This provides basic functionality when numpy is unavailable")

def suggest_solutions():
    """Suggest various solutions for numpy issues"""
    print_header("SUGGESTED SOLUTIONS")
    
    solutions = [
        "1. CHANGE DIRECTORY: Move to a different directory (not numpy source)",
        "2. CLEAN INSTALL: pip uninstall numpy && pip install numpy",
        "3. USER INSTALL: pip install --user numpy",
        "4. VIRTUAL ENVIRONMENT: Create fresh venv and install there",
        "5. CONDA: Use conda install numpy instead of pip",
        "6. RESTART: Restart Python interpreter and terminal",
        "7. FALLBACK: Use the created numpy_fallback.py for basic operations"
    ]
    
    for solution in solutions:
        print(f"   {solution}")
    
    print(f"\n💡 Current directory: {os.getcwd()}")
    print("Try running from your home directory or Documents folder")

def main():
    """Main numpy fix process"""
    print("🔧 Smart Music Generator AI - NumPy Import Fix")
    print("This tool will diagnose and fix NumPy import issues")
    
    # Step 1: Check for conflicts
    conflicts = check_numpy_source_conflict()
    
    # Step 2: Test current numpy
    numpy_works = test_numpy_import()
    
    if numpy_works:
        print("\n🎉 NumPy is working correctly!")
        print("The voice assignment system should work now.")
        return True
    
    # Step 3: Try fixes
    print(f"\n🔧 NumPy not working, attempting fixes...")
    
    if conflicts:
        print("\n⚠️ Potential conflicts detected!")
        response = input("Remove conflicts and try different directory? (y/n): ")
        if response.lower() == 'y':
            print("Please move to a different directory and try again")
            print(f"Current directory: {os.getcwd()}")
            return False
    
    # Step 4: Try reinstallation
    fix_numpy_installation()
    
    # Step 5: Test again
    numpy_works = test_numpy_import()
    
    if numpy_works:
        print("\n🎉 NumPy fixed successfully!")
        return True
    
    # Step 6: Create fallback
    create_numpy_fallback()
    
    # Step 7: Suggest solutions
    suggest_solutions()
    
    print("\n⚠️ NumPy still not working, but fallback system created")
    print("The voice assignment system will work with limited functionality")
    
    return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Ready to use voice assignment system!")
        else:
            print("\n🔧 Manual intervention may be needed")
    except KeyboardInterrupt:
        print("\n\n👋 Fix cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
