from flask import Flask, render_template, request, jsonify, send_file
import os
import threading
import time
from music_generator import SmartMusicGenerator
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
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
    return render_template('index.html')

@app.route('/upload_midi', methods=['POST'])
def upload_midi():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files provided"})
        
        files = request.files.getlist('files')
        uploaded_files = []
        errors = []
        
        for file in files:
            if file.filename == '':
                continue
                
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Ensure unique filename
                counter = 1
                original_filename = filename
                while os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
                    name, ext = os.path.splitext(original_filename)
                    filename = f"{name}_{counter}{ext}"
                    counter += 1
                
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                # Validate the uploaded file
                if generator.processor.validate_midi_file(file_path):
                    uploaded_files.append(filename)
                else:
                    os.remove(file_path)  # Remove invalid file
                    errors.append(f"Invalid MIDI file: {file.filename}")
            else:
                errors.append(f"Invalid file type: {file.filename}")
        
        response = {}
        if uploaded_files:
            response["success"] = f"Successfully uploaded {len(uploaded_files)} files: {', '.join(uploaded_files)}"
        if errors:
            response["warnings"] = errors
        
        if not uploaded_files and not errors:
            response["error"] = "No valid files were uploaded"
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"})

@app.route('/train', methods=['POST'])
def train_model():
    global training_status
    
    if training_status["is_training"]:
        return jsonify({"error": "Training already in progress"})
    
    try:
        # Get parameters
        epochs = int(request.form.get('epochs', 20))
        batch_size = int(request.form.get('batch_size', 16))
        
        # Get MIDI files
        midi_files = generator.get_sample_midi_files(UPLOAD_FOLDER)
        
        if not midi_files:
            return jsonify({
                "error": "No valid MIDI files found. Please upload MIDI files first."
            })
        
        print(f"Found {len(midi_files)} valid MIDI files")
        
        def train_thread():
            global training_status
            try:
                training_status = {
                    "is_training": True, 
                    "progress": 0, 
                    "message": "Initializing training...",
                    "current_epoch": 0,
                    "total_epochs": epochs,
                    "loss": 0.0,
                    "accuracy": 0.0
                }
                
                # Train model
                history = generator.train(
                    midi_files, 
                    epochs=epochs, 
                    batch_size=batch_size,
                    progress_callback=update_training_progress
                )
                
                training_status = {
                    "is_training": False, 
                    "progress": 100, 
                    "message": "Training completed successfully!",
                    "current_epoch": epochs,
                    "total_epochs": epochs,
                    "loss": history.history['loss'][-1],
                    "accuracy": history.history['accuracy'][-1]
                }
                
            except Exception as e:
                print(f"Training error: {e}")
                training_status = {
                    "is_training": False, 
                    "progress": 0, 
                    "message": f"Training failed: {str(e)}",
                    "current_epoch": 0,
                    "total_epochs": epochs,
                    "loss": 0.0,
                    "accuracy": 0.0
                }
        
        threading.Thread(target=train_thread, daemon=True).start()
        return jsonify({"success": "Training started"})
        
    except Exception as e:
        return jsonify({"error": f"Failed to start training: {str(e)}"})

@app.route('/training_status')
def get_training_status():
    return jsonify(training_status)

@app.route('/generate', methods=['POST'])
def generate_music():
    try:
        # Load model if not loaded
        if not generator.is_trained:
            if not generator.load_model():
                return jsonify({
                    "error": "No trained model found. Please train the model first."
                })
        
        # Get parameters
        style = request.form.get('style', '')
        length = int(request.form.get('length', 500))
        temperature = float(request.form.get('temperature', 0.8))
        
        # Validate parameters
        length = max(50, min(2000, length))  # Limit length
        temperature = max(0.1, min(2.0, temperature))  # Limit temperature
        
        print(f"Generating music: length={length}, temperature={temperature}")
        
        # Generate music
        midi_path = generator.generate(
            style_prompt=style,
            length=length, 
            temperature=temperature
        )
        
        filename = os.path.basename(midi_path)
        
        return jsonify({
            "success": "Music generated successfully",
            "file": filename,
            "download_url": f"/download/{filename}",
            "file_size": os.path.getsize(midi_path)
        })
        
    except Exception as e:
        print(f"Generation error: {e}")
        return jsonify({"error": f"Generation failed: {str(e)}"})

@app.route('/download/<filename>')
def download_file(filename):
    try:
        # Security check
        filename = secure_filename(filename)
        file_path = os.path.join('models', filename)
        
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({"error": f"Download failed: {str(e)}"}), 500

@app.route('/model_info')
def get_model_info():
    """Get information about the current model"""
    try:
        if generator.is_trained:
            info = {
                "trained": True,
                "vocab_size": generator.processor.vocab_size,
                "model_exists": os.path.exists(os.path.join('models', 'music_model.h5'))
            }
        else:
            info = {
                "trained": False,
                "model_exists": os.path.exists(os.path.join('models', 'music_model.h5'))
            }
        
        return jsonify(info)
        
    except Exception as e:
        return jsonify({"error": f"Failed to get model info: {str(e)}"})

@app.route('/uploaded_files')
def get_uploaded_files():
    """Get list of uploaded MIDI files"""
    try:
        files = []
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
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
