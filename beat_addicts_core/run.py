# filepath: c:\Users\sally\Downloads\sunoai-1.0.7-rebuild\beat_addicts_core\run.py
#!/usr/bin/env python3
"""🎵 BEAT ADDICTS - Main Runner"""

import sys

def main():
    print("BEAT ADDICTS v2.0")
    
    # Try to install Flask if missing
    try:
        import flask
    except ImportError:
        print("Installing Flask...")
        import subprocess
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "flask"], check=True)
            import flask
        except Exception:
            try:
                subprocess.run(["pip", "install", "flask"], check=True)
                import flask
            except Exception:
                print("❌ Could not install Flask automatically")
                print("Manual install: pip install flask")
                return False
    
    try:
        from web_interface import app
        print("Starting at: http://localhost:5000")
        app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run: python fix_flask_install.py")
        return False
    return True

if __name__ == "__main__":
    main()
