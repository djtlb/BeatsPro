"""
🎵 BEAT ADDICTS - Professional Music Production AI Web Interface
Flask-based web application for BEAT ADDICTS Studio
"""

import os
import sys
import json
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from music_generator import SmartMusicGenerator
from werkzeug.utils import secure_filename

# Create Flask app with BEAT ADDICTS branding
app = Flask(__name__)
app.config['SECRET_KEY'] = 'beat_addicts_professional_music_ai_2024'
app.config['BEAT_ADDICTS_VERSION'] = '2.0'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Global instances
generator = SmartMusicGenerator()
training_status = {
    "is_training": False, 
    "progress": 0, 
    "message": "Ready",
    "current_epoch": 0,
    "total_epochs": 0,
    "loss": 0.0,
    "accuracy": 0.0
}

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'midi_files')
ALLOWED_EXTENSIONS = {'mid', 'midi'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('models', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def update_training_progress(epoch, total_epochs, logs):
    """Callback to update training progress"""
    global training_status
    training_status.update({
        "progress": int((epoch / total_epochs) * 100),
        "current_epoch": epoch,
        "total_epochs": total_epochs,
        "loss": logs.get('loss', 0.0),
        "accuracy": logs.get('accuracy', 0.0),
        "message": f"Training epoch {epoch}/{total_epochs}"
    })

@app.route('/')
def index():
    """BEAT ADDICTS Studio home page"""
    return render_template('index.html', 
                         version=app.config['BEAT_ADDICTS_VERSION'],
                         status=generation_status)

@app.route('/api/status')
def api_status():
    """Get BEAT ADDICTS system status"""
    try:
        # Check BEAT ADDICTS components
        has_voice_system = os.path.exists("voice_assignment.py")
        has_generators = os.path.exists("hiphop_midi_generator.py")
        has_models_dir = os.path.exists("models")
        has_midi_files = os.path.exists("midi_files")
        
        system_status = {
            'beat_addicts_version': app.config['BEAT_ADDICTS_VERSION'],
            'components': {
                'voice_system': has_voice_system,
                'generators': has_generators,
                'models_directory': has_models_dir,
                'midi_files': has_midi_files
            },
            'generation_status': generation_status,
            'ready': has_voice_system and has_generators
        }
        
        return jsonify(system_status)
    except Exception as e:
        return jsonify({'error': f'BEAT ADDICTS status check failed: {e}'}), 500

@app.route('/api/generate-training-data', methods=['POST'])
def generate_training_data():
    """Generate BEAT ADDICTS training data"""
    if generation_status['running']:
        return jsonify({'error': 'BEAT ADDICTS generation already running'}), 400
    
    try:
        data = request.get_json()
        genre = data.get('genre', 'all')
        tracks_per_subgenre = data.get('tracks', 4)
        
        # Start generation in background thread
        thread = threading.Thread(target=run_generation_task, args=(genre, tracks_per_subgenre))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'message': f'BEAT ADDICTS {genre} generation started',
            'status': 'started'
        })
        
    except Exception as e:
        return jsonify({'error': f'BEAT ADDICTS generation failed: {e}'}), 500

@app.route('/api/test-voice-system', methods=['POST'])
def test_voice_system():
    """Test BEAT ADDICTS voice assignment system"""
    try:
        # Import and test voice system
        import importlib.util
        spec = importlib.util.spec_from_file_location("voice_assignment", "voice_assignment.py")
        voice_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(voice_module)
        
        assigner = voice_module.IntelligentVoiceAssigner()
        
        # Test recommendations
        test_results = []
        test_genres = ["hiphop", "electronic", "rock"]
        
        for genre in test_genres:
            recommendation = assigner.get_voice_recommendation(genre, "drums")
            test_results.append({
                'genre': genre,
                'program': recommendation.get('recommended_program', 'N/A'),
                'channel': recommendation.get('channel', 'N/A')
            })
        
        return jsonify({
            'message': 'BEAT ADDICTS Voice System: OPERATIONAL',
            'test_results': test_results,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'message': f'BEAT ADDICTS Voice System: ERROR - {e}',
            'status': 'error'
        }), 500

@app.route('/api/system-info')
def system_info():
    """Get BEAT ADDICTS system information"""
    try:
        import platform
        
        # Check file counts
        midi_count = 0
        if os.path.exists("midi_files"):
            midi_count = len([f for f in os.listdir("midi_files") if f.endswith('.mid')])
        
        info = {
            'beat_addicts_version': app.config['BEAT_ADDICTS_VERSION'],
            'python_version': platform.python_version(),
            'platform': platform.system(),
            'working_directory': os.getcwd(),
            'midi_files_count': midi_count,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(info)
        
    except Exception as e:
        return jsonify({'error': f'System info failed: {e}'}), 500

def run_generation_task(genre, tracks_per_subgenre):
    """Run BEAT ADDICTS generation task in background"""
    global generation_status
    
    try:
        generation_status.update({
            'running': True,
            'progress': 0,
            'message': f'Starting BEAT ADDICTS {genre} generation...',
            'current_task': f'Generating {genre} training data'
        })
        
        if genre == 'all':
            # Generate all genres
            genres = ['hiphop', 'electronic', 'rock', 'country', 'dnb', 'futuristic']
            total_genres = len(genres)
            
            for i, g in enumerate(genres):
                generation_status.update({
                    'progress': int((i / total_genres) * 100),
                    'message': f'Generating BEAT ADDICTS {g.upper()} tracks...',
                    'current_task': f'{g} generation'
                })
                
                # Simulate generation (replace with actual generator calls)
                import time
                time.sleep(2)  # Simulate work
                
                generation_status['progress'] = int(((i + 1) / total_genres) * 100)
        else:
            # Generate single genre
            generation_status.update({
                'progress': 50,
                'message': f'Generating BEAT ADDICTS {genre.upper()} tracks...',
                'current_task': f'{genre} generation'
            })
            
            # Simulate generation
            import time
            time.sleep(3)
            
            generation_status['progress'] = 100
        
        generation_status.update({
            'running': False,
            'progress': 100,
            'message': f'BEAT ADDICTS {genre} generation complete!',
            'current_task': None
        })
        
    except Exception as e:
        generation_status.update({
            'running': False,
            'progress': 0,
            'message': f'BEAT ADDICTS generation failed: {e}',
            'current_task': None
        })

@app.errorhandler(404)
def not_found(error):
    """BEAT ADDICTS 404 handler"""
    return jsonify({
        'error': 'BEAT ADDICTS endpoint not found',
        'message': 'Check the BEAT ADDICTS API documentation'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """BEAT ADDICTS 500 handler"""
    return jsonify({
        'error': 'BEAT ADDICTS internal server error',
        'message': 'Check BEAT ADDICTS system logs'
    }), 500

if __name__ == '__main__':
    print("🎵 BEAT ADDICTS Studio starting...")
    print("🔥 Professional Music Production AI Web Interface 🔥")
    
    # Try to load existing model
    if generator.load_model():
        print("Existing model loaded successfully")
    else:
        print("No existing model found - training required")
    
    print("Web interface starting at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
                if allowed_file(filename):
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file_size = os.path.getsize(file_path)
                    files.append({
                        "name": filename,
                        "size": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2)
                    })
        
        return jsonify({"files": files, "total": len(files)})
        
    except Exception as e:
        return jsonify({"error": f"Failed to get file list: {str(e)}"})

if __name__ == '__main__':
    print("Starting Smart Music Generator AI...")
    print("Checking for existing model...")
    
    # Try to load existing model
    if generator.load_model():
        print("Existing model loaded successfully")
    else:
        print("No existing model found - training required")
    
    print("Web interface starting at http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
