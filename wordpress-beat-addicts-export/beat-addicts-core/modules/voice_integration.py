"""
BEAT ADDICTS - Voice Integration with Web Interface
Complete integration of voice handling with the main system
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def integrate_voice_handler_with_web():
    """Integrate voice handler with web interface"""
    try:
        from voice_handler import BeatAddictsVoiceHandler
        from web_interface import app
        from flask import jsonify, request
        
        # Global voice handler instance
        voice_handler = BeatAddictsVoiceHandler()
        
        @app.route('/api/voice/assign', methods=['POST'])
        def assign_voice():
            """API endpoint for voice assignment"""
            try:
                data = request.get_json()
                channel = data.get('channel', 0)
                voice_id = data.get('voice_id', 'lead_synth')
                genre = data.get('genre', 'general')
                
                success = voice_handler.assign_voice_to_channel(channel, voice_id, genre)
                
                return jsonify({
                    'success': success,
                    'channel': channel,
                    'voice_id': voice_id,
                    'genre': genre
                })
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @app.route('/api/voice/profiles')
        def get_voice_profiles():
            """Get available voice profiles"""
            profiles = {}
            for voice_id, profile in voice_handler.voice_profiles.items():
                profiles[voice_id] = profile.__dict__
            
            return jsonify({
                'profiles': profiles,
                'count': len(profiles)
            })
        
        @app.route('/api/voice/process', methods=['POST'])
        def process_voices():
            """Process MIDI with voice handling"""
            try:
                data = request.get_json()
                midi_data = data.get('midi_data', [])
                lyrics = data.get('lyrics', '')
                bpm = data.get('bpm', 120)
                
                processed_notes = voice_handler.process_midi_to_voices(midi_data, lyrics, bpm)
                
                return jsonify({
                    'success': True,
                    'processed_notes': [note.__dict__ for note in processed_notes],
                    'note_count': len(processed_notes)
                })
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        print("Voice handler integrated with web interface")
        return True
        
    except ImportError as e:
        print(f"Voice integration failed: {e}")
        return False

if __name__ == "__main__":
    integrate_voice_handler_with_web()
