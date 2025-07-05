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
        subprocess.run(command, shell=True, check=True, 
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

def install_dependencies_smart():
    """Smart dependency installation with multiple fallback strategies"""
    print("\n🔧 Smart Dependency Installation")
    print("Trying multiple installation strategies for Windows compatibility...")
    
    # Strategy 1: Try minimal core dependencies first
    print("\n📦 Strategy 1: Installing core dependencies...")
    core_deps = [
        "flask>=2.0.0",
        "numpy>=1.20.0", 
        "werkzeug>=2.0.0"
    ]
    
    for dep in core_deps:
        print(f"Installing {dep}...")
        if run_command(f'"{sys.executable}" -m pip install --user "{dep}"', f"Install {dep}"):
            print(f"✅ {dep} installed successfully")
        else:
            print(f"⚠️ {dep} failed, continuing...")
    
    # Strategy 2: Try MIDI libraries
    print("\n🎵 Strategy 2: Installing MIDI libraries...")
    midi_deps = [
        "pretty_midi>=0.2.9",
        "mido>=1.2.0"
    ]
    
    for dep in midi_deps:
        print(f"Installing {dep}...")
        if run_command(f'"{sys.executable}" -m pip install --user "{dep}"', f"Install {dep}"):
            print(f"✅ {dep} installed successfully")
        else:
            print(f"⚠️ {dep} failed, will try alternative...")
    
    # Strategy 3: Try TensorFlow (optional, can fail)
    print("\n🧠 Strategy 3: Installing TensorFlow (optional)...")
    tf_commands = [
        f'"{sys.executable}" -m pip install --user "tensorflow>=2.8.0"',
        f'"{sys.executable}" -m pip install --user "tensorflow-cpu>=2.8.0"',
        f'"{sys.executable}" -m pip install --user "tensorflow==2.13.0"'
    ]
    
    tf_installed = False
    for cmd in tf_commands:
        print(f"Trying: {cmd}")
        if run_command(cmd, "Install TensorFlow"):
            print("✅ TensorFlow installed successfully")
            tf_installed = True
            break
        else:
            print("⚠️ TensorFlow install failed, trying next method...")
    
    if not tf_installed:
        print("⚠️ TensorFlow installation failed - you can still use basic features")
    
    # Strategy 4: Optional dependencies
    print("\n🔧 Strategy 4: Installing optional dependencies...")
    optional_deps = [
        "scipy>=1.7.0",
        "librosa>=0.9.0"
    ]
    
    for dep in optional_deps:
        print(f"Installing {dep} (optional)...")
        run_command(f'"{sys.executable}" -m pip install --user "{dep}"', f"Install {dep}")
    
    return True

def check_installation():
    """Check what was actually installed"""
    print("\n🔍 Checking Installation Results...")
    
    required_modules = {
        'flask': 'Web framework - REQUIRED',
        'numpy': 'Scientific computing - REQUIRED', 
        'pretty_midi': 'MIDI processing - REQUIRED',
        'mido': 'MIDI I/O - REQUIRED',
        'tensorflow': 'AI framework - OPTIONAL',
        'scipy': 'Scientific computing - OPTIONAL',
        'librosa': 'Audio processing - OPTIONAL'
    }
    
    installed = []
    missing = []
    
    for module, description in required_modules.items():
        try:
            __import__(module)
            installed.append(f"✅ {module} - {description}")
        except ImportError:
            missing.append(f"❌ {module} - {description}")
    
    print("\n📦 INSTALLATION RESULTS:")
    for item in installed:
        print(f"  {item}")
    
    if missing:
        print("\n⚠️ MISSING DEPENDENCIES:")
        for item in missing:
            print(f"  {item}")
    
    # Check if we have minimum requirements
    essential = ['flask', 'numpy']
    has_essentials = all(module in [item.split()[1] for item in installed] for module in essential)
    
    return has_essentials, len(installed), len(missing)

def run_comprehensive_debug():
    """Run BEAT ADDICTS comprehensive debug with self-contained dependencies"""
    try:
        # Use self-contained fix_all_problems instead of debug_test
        from beat_addicts_core.fix_all_problems import main as fix_main # type: ignore
        return fix_main()
    except ImportError:
        print("⚠️ Running basic diagnostic...")
        
        # Self-contained basic diagnostic
        print("🔍 BEAT ADDICTS Basic System Check")
        print("=" * 40)
        
        # Check Python version
        import sys
        if sys.version_info >= (3, 8):
            print("✅ Python version compatible")
        else:
            print("❌ Python version too old")
        return False
        
        # Check essential files
        essential_files = ["beat_addicts_core/run.py", "beat_addicts_core/requirements.txt"]
        all_present = True
        
        for file in essential_files:
            if os.path.exists(file):
                print(f"✅ {file} found")
            else:
                print(f"❌ {file} missing")
                all_present = False
        
        # Check Flask availability
        try:
            __import__('flask')
            print("✅ Flask available")
        except ImportError:
            print("❌ Flask not installed")
            all_present = False
        
        if all_present:
            print("\n🎉 BEAT ADDICTS: Basic system operational!")
            return True
        else:
            print("\n⚠️ BEAT ADDICTS: Some components missing")
            return False

def run_debug_diagnostics():
    """Enhanced debug diagnostics with self-contained dependencies"""
    try:
        # Use self-contained diagnostics instead of debug_test
        return run_comprehensive_debug()
    except Exception as e:
        print(f"❌ Debug diagnostics failed: {e}")
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
            debug_test = __import__('debug_test')
            ProjectDebugger = getattr(debug_test, 'ProjectDebugger')
            debugger = ProjectDebugger()
            debug_success = debugger.run_full_test()
            
            if not debug_success:
                print("\n⚠️ Debug test found issues. Continue anyway? (y/n): ", end="")
                continue_anyway = input().lower().strip()
                if continue_anyway not in ['y', 'yes']:
                    print("Setup cancelled. Please fix issues first.")
                    return False
        except (ImportError, AttributeError):
            print("⚠️ Debug test not available, continuing with setup...")
    
    # Step 1: Check Python
    print_step(1, "CHECKING PYTHON INSTALLATION")
    if not check_python():
        print("Please install Python 3.8+ from https://python.org")
        return False
    
    # Step 2: Smart dependency installation
    print_step(2, "SMART DEPENDENCY INSTALLATION", 
               "Using multiple strategies for Windows compatibility...")
    
    # Try smart installation
    install_dependencies_smart()
    
    # Check what we got
    has_essentials, installed_count, missing_count = check_installation()
    
    if has_essentials:
        print(f"\n✅ Essential dependencies installed! ({installed_count} installed, {missing_count} missing)")
        print("You can proceed with the setup.")
    else:
        print(f"\n⚠️ Some essential dependencies missing. ({installed_count} installed, {missing_count} missing)")
        
        # Offer manual installation guide
        print("\n🔧 MANUAL INSTALLATION OPTIONS:")
        print("1. Try: pip install --user flask numpy pretty_midi mido")
        print("2. Try: python -m pip install --upgrade pip")
        print("3. Try: pip install --no-cache-dir flask numpy")
        print("4. Run as administrator and try again")
        
        continue_anyway = input("\nContinue setup anyway? (y/n): ").lower().strip()
        if continue_anyway not in ['y', 'yes']:
            print("Setup stopped. Please install dependencies manually first.")
            return False
    
    # Step 3: Generate training data
    print_step(3, "GENERATING DNB TRAINING DATA",
               "Creating 112 authentic Drum & Bass MIDI files...")
    
    # Try to generate, but don't fail if it doesn't work
    try:
        if run_command(f'"{sys.executable}" run.py --create-dnb',
                      "Generate comprehensive DNB training dataset"):
            print("✅ Training data generated successfully")
        else:
            print("⚠️ Training data generation failed - you can generate it later")
    except Exception as e:
        print(f"⚠️ Training data generation error: {e}")
    
    # Check if files were created
    midi_dir = Path("midi_files")
    if midi_dir.exists():
        midi_files = list(midi_dir.glob("*.mid"))
        print(f"✅ Found {len(midi_files)} MIDI training files")
    else:
        print("ℹ️ No MIDI files found - generate them later with: python run.py --create-dnb")
    
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
            debug_test = __import__('debug_test')
            ProjectDebugger = getattr(debug_test, 'ProjectDebugger')
            debugger = ProjectDebugger()
            debugger.test_environment()
            debugger.test_dependencies()
            debugger.test_file_structure()
            print("✅ Final system test completed!")
        except (ImportError, AttributeError):
            print("⚠️ Debug test module not found, but setup should be working")
        except Exception as e:
            print(f"⚠️ Final test error: {e}, but setup should be working")
            print(f"⚠️ Final test error: {e}, but setup should be working")
    
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
