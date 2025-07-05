#!/usr/bin/env python3
"""
Quick Start Script for Smart Music Generator AI
Automates the setup process for new users
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_step(step_num, title, description=""):
    """Print formatted step information"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {title}")
    if description:
        print(f"{description}")
    print('='*60)

def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"\nRunning: {command}")
    if description:
        print(f"Purpose: {description}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def check_python():
    """Check Python installation"""
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✅ Python found: {version}")
        return True
    except:
        print("❌ Python not found or not accessible")
        return False

def main():
    """Run the complete setup process"""
    
    print("🎵 Smart Music Generator AI - Quick Start Setup")
    print("This script will set up everything you need to start generating music!")
    
    # Check if we're in the right directory
    if not os.path.exists("run.py"):
        print("\n❌ Error: Please run this script from the project directory")
        print("Navigate to: C:\\Users\\sally\\Downloads\\sunoai-1.0.7-rebuild")
        return False
    
    # Option to run debug test first
    print("\n" + "="*60)
    run_debug = input("Run comprehensive debug test first? (recommended) (y/n): ").lower().strip()
    
    if run_debug in ['y', 'yes']:
        print("\n🔍 Running debug test...")
        try:
            from debug_test import ProjectDebugger
            debugger = ProjectDebugger()
            debug_success = debugger.run_full_test()
            
            if not debug_success:
                print("\n⚠️ Debug test found issues. Continue anyway? (y/n): ", end="")
                continue_anyway = input().lower().strip()
                if continue_anyway not in ['y', 'yes']:
                    print("Setup cancelled. Please fix issues first.")
                    return False
        except ImportError:
            print("⚠️ Debug test not available, continuing with setup...")
    
    # Step 1: Check Python
    print_step(1, "CHECKING PYTHON INSTALLATION")
    if not check_python():
        print("Please install Python 3.8+ from https://python.org")
        return False
    
    # Step 2: Install dependencies
    print_step(2, "INSTALLING DEPENDENCIES", 
               "Installing TensorFlow, Flask, and MIDI libraries...")
    if not run_command("pip install -r requirements.txt", 
                      "Install all required Python packages"):
        print("❌ Failed to install dependencies")
        print("Try running: pip install --upgrade pip")
        return False
    
    # Step 3: Generate training data
    print_step(3, "GENERATING DNB TRAINING DATA",
               "Creating 112 authentic Drum & Bass MIDI files...")
    if not run_command(f'"{sys.executable}" run.py --create-dnb',
                      "Generate comprehensive DNB training dataset"):
        print("❌ Failed to generate training data")
        return False
    
    # Check if files were created
    midi_dir = Path("midi_files")
    if midi_dir.exists():
        midi_files = list(midi_dir.glob("*.mid"))
        print(f"✅ Generated {len(midi_files)} MIDI training files")
    else:
        print("⚠️ MIDI files directory not found")
    
    # Step 4: Provide next steps
    print_step(4, "SETUP COMPLETE! 🎉")
    print("\n🚀 Your Smart Music Generator AI is ready!")
    print("\nNEXT STEPS:")
    print("1. Run: python run.py")
    print("2. Open browser to: http://localhost:5000")
    print("3. Upload the generated MIDI files")
    print("4. Click 'Start Training' (30-40 epochs recommended)")
    print("5. Generate your first AI music!")
    
    # Offer to run final test
    print("\n" + "="*60)
    final_test = input("Run final system test? (y/n): ").lower().strip()
    
    if final_test in ['y', 'yes']:
        try:
            from debug_test import ProjectDebugger
            debugger = ProjectDebugger()
            debugger.test_environment()
            debugger.test_dependencies()
            debugger.test_file_structure()
            print("✅ Final system test completed!")
        except:
            print("⚠️ Final test unavailable, but setup should be working")
    
    # Ask if user wants to start the web interface
    print("\n" + "="*60)
    response = input("Start the web interface now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🌐 Starting web interface...")
        print("Opening http://localhost:5000 in your browser...")
        
        # Start the web interface
        try:
            # Open browser after a short delay
            import threading
            def open_browser():
                time.sleep(2)
                webbrowser.open('http://localhost:5000')
            
            threading.Thread(target=open_browser).start()
            
            # Start the server
            subprocess.run(f'"{sys.executable}" run.py', shell=True)
            
        except KeyboardInterrupt:
            print("\n👋 Web interface stopped. You can restart anytime with: python run.py")
    else:
        print(f"\n📝 To start later, run: {sys.executable} run.py")
        print("Then open: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup failed. Please check the error messages above.")
            print("For help, check the README.md file or documentation.")
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your Python installation and try again.")
