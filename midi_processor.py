import numpy as np
import pretty_midi
import mido
import os
from typing import List, Dict, Tuple, Optional, Set
import pickle
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from pathlib import Path

# Setup logging
logger = logging.getLogger(__name__)

class EnhancedMIDIProcessor:
    """Advanced MIDI processor with performance optimizations and enhanced features"""
    
    def __init__(self):
        self.note_to_int = {}
        self.int_to_note = {}
        self.vocab_size = 0
        self.time_quantization = 0.0625  # 1/16 note for better precision
        self.max_velocity = 127
        self.velocity_bins = 32  # Increased resolution
        self.pitch_range = (21, 108)  # Full piano range
        self.max_duration = 8.0  # Maximum note duration in seconds
        self.min_duration = 0.05  # Minimum note duration
        
        # Caching for performance
        self._file_cache = {}
        self._validation_cache = {}
        
        # Enhanced token types
        self.special_tokens = {
            'PAD': 0,
            'START': 1, 
            'END': 2,
            'TIME_STEP': 3,
            'CHORD_START': 4,
            'CHORD_END': 5
        }
        
        # Initialize vocabulary with special tokens
        for token_name, token_id in self.special_tokens.items():
            self.note_to_int[token_name] = token_id
            self.int_to_note[token_id] = token_name
        
        self.vocab_size = len(self.special_tokens)
    
    def _get_file_hash(self, file_path: str) -> str:
        """Generate hash for file caching"""
        stat = os.stat(file_path)
        return hashlib.md5(f"{file_path}_{stat.st_mtime}_{stat.st_size}".encode()).hexdigest()
    
    def validate_midi_file(self, midi_path: str, use_cache: bool = True) -> bool:
        """Enhanced MIDI validation with caching"""
        if not os.path.exists(midi_path):
            return False
        
        # Check cache
        if use_cache:
            file_hash = self._get_file_hash(midi_path)
            if file_hash in self._validation_cache:
                return self._validation_cache[file_hash]
        
        try:
            # File size check
            file_size = os.path.getsize(midi_path)
            if file_size < 100 or file_size > 10000000:  # 100B to 10MB
                result = False
            else:
                # Try loading with pretty_midi
                try:
                    midi_data = pretty_midi.PrettyMIDI(midi_path)
                    result = (
                        len(midi_data.instruments) > 0 and
                        midi_data.get_end_time() > 1.0 and  # At least 1 second
                        any(len(inst.notes) > 0 for inst in midi_data.instruments if not inst.is_drum)
                    )
                except:
                    # Fallback to mido
                    try:
                        mid = mido.MidiFile(midi_path)
                        result = len(mid.tracks) > 0 and any(
                            any(msg.type in ['note_on', 'note_off'] for msg in track)
                            for track in mid.tracks
                        )
                    except:
                        result = False
            
            # Cache result
            if use_cache:
                self._validation_cache[file_hash] = result
            
            return result
            
        except Exception as e:
            logger.warning(f"Validation error for {midi_path}: {e}")
            return False
    
    def midi_to_tokens(self, midi_path: str, use_cache: bool = True) -> List[int]:
        """Enhanced MIDI to tokens conversion with advanced features"""
        
        # Check cache
        if use_cache:
            file_hash = self._get_file_hash(midi_path)
            if file_hash in self._file_cache:
                return self._file_cache[file_hash]
        
        if not self.validate_midi_file(midi_path):
            logger.warning(f"Invalid MIDI file: {midi_path}")
            return []
        
        try:
            # Primary method: pretty_midi
            midi_data = pretty_midi.PrettyMIDI(midi_path)
            notes = self._extract_notes_pretty_midi(midi_data)
            
        except Exception as e:
            try:
                # Fallback method: mido
                logger.info(f"pretty_midi failed for {midi_path}, trying mido...")
                notes = self._extract_notes_mido(midi_path)
            except Exception as e2:
                logger.error(f"Both MIDI libraries failed for {midi_path}: {e}, {e2}")
                return []
        
        if not notes:
            return []
        
        # Advanced tokenization
        tokens = self._notes_to_advanced_tokens(notes)
        
        # Cache result
        if use_cache and len(tokens) > 0:
            self._file_cache[file_hash] = tokens
            # Limit cache size
            if len(self._file_cache) > 100:
                oldest_key = next(iter(self._file_cache))
                del self._file_cache[oldest_key]
        
        return tokens
    
    def _extract_notes_pretty_midi(self, midi_data: pretty_midi.PrettyMIDI) -> List[Dict]:
        """Enhanced note extraction with better filtering"""
        notes = []
        
        for instrument in midi_data.instruments:
            if instrument.is_drum:
                continue
            
            for note in instrument.notes:
                # Enhanced filtering
                if (self.pitch_range[0] <= note.pitch <= self.pitch_range[1] and
                    self.min_duration <= (note.end - note.start) <= self.max_duration and
                    note.velocity > 0):
                    
                    notes.append({
                        'pitch': note.pitch,
                        'start': note.start,
                        'duration': note.end - note.start,
                        'velocity': note.velocity,
                        'instrument': instrument.program
                    })
        
        return notes
    
    def _extract_notes_mido(self, midi_path: str) -> List[Dict]:
        """Enhanced mido extraction with better timing"""
        mid = mido.MidiFile(midi_path)
        notes = []
        
        for track in mid.tracks:
            track_time = 0
            active_notes = {}
            tempo = 500000  # Default tempo
            
            for msg in track:
                track_time += msg.time
                
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                elif msg.type == 'note_on' and msg.velocity > 0:
                    active_notes[msg.note] = {
                        'start': mido.tick2second(track_time, mid.ticks_per_beat, tempo),
                        'velocity': msg.velocity
                    }
                elif msg.type in ['note_off', 'note_on'] and (msg.type == 'note_off' or msg.velocity == 0):
                    if msg.note in active_notes:
                        start_info = active_notes[msg.note]
                        start_time = start_info['start']
                        end_time = mido.tick2second(track_time, mid.ticks_per_beat, tempo)
                        duration = end_time - start_time
                        
                        if (self.pitch_range[0] <= msg.note <= self.pitch_range[1] and
                            self.min_duration <= duration <= self.max_duration):
                            
                            notes.append({
                                'pitch': msg.note,
                                'start': start_time,
                                'duration': duration,
                                'velocity': start_info['velocity'],
                                'instrument': 0  # Default piano
                            })
                        
                        del active_notes[msg.note]
        
        return notes
    
    def _notes_to_advanced_tokens(self, notes: List[Dict]) -> List[int]:
        """Convert notes to advanced token sequence with chord detection"""
        
        if not notes:
            return []
        
        # Sort by start time
        notes.sort(key=lambda x: x['start'])
        
        tokens = [self._get_token('START')]
        current_time = 0
        chord_threshold = 0.1  # Notes within 100ms are considered a chord
        
        i = 0
        while i < len(notes):
            note = notes[i]
            
            # Add time steps if needed
            time_gap = note['start'] - current_time
            if time_gap > self.time_quantization:
                time_steps = int(time_gap / self.time_quantization)
                for _ in range(min(time_steps, 32)):  # Limit time steps
                    tokens.append(self._get_token('TIME_STEP'))
            
            # Check for chord (simultaneous notes)
            chord_notes = [note]
            j = i + 1
            while (j < len(notes) and 
                   abs(notes[j]['start'] - note['start']) < chord_threshold):
                chord_notes.append(notes[j])
                j += 1
            
            # Process chord or single note
            if len(chord_notes) > 1:
                tokens.append(self._get_token('CHORD_START'))
                for chord_note in chord_notes:
                    note_token = self._create_note_token(chord_note)
                    tokens.append(note_token)
                tokens.append(self._get_token('CHORD_END'))
            else:
                note_token = self._create_note_token(note)
                tokens.append(note_token)
            
            # Update current time
            current_time = max(n['start'] + n['duration'] for n in chord_notes)
            i = j
        
        tokens.append(self._get_token('END'))
        
        # Limit sequence length
        return tokens[:4096]
    
    def _create_note_token(self, note: Dict) -> int:
        """Create enhanced note token with more musical information"""
        
        # Quantize parameters
        pitch = max(self.pitch_range[0], min(self.pitch_range[1], note['pitch']))
        duration_bin = min(63, int(note['duration'] / self.time_quantization))
        velocity_bin = min(self.velocity_bins - 1, note['velocity'] // (128 // self.velocity_bins))
        instrument_bin = min(15, note.get('instrument', 0) // 8)  # Group instruments
        
        # Create composite token with musical structure
        # Format: NOTE_pitch_duration_velocity_instrument
        token_str = f"NOTE_{pitch}_{duration_bin}_{velocity_bin}_{instrument_bin}"
        
        return self._get_token(token_str)
    
    def _get_token(self, token_str: str) -> int:
        """Enhanced token management with vocabulary size control"""
        if token_str not in self.note_to_int:
            # Limit vocabulary size to prevent memory issues
            if len(self.note_to_int) >= 8192:  # Increased limit
                return self.note_to_int.get('PAD', 0)  # Return PAD token if vocab full
            
            self.note_to_int[token_str] = len(self.note_to_int)
            self.int_to_note[len(self.int_to_note)] = token_str
        
        self.vocab_size = len(self.note_to_int)
        return self.note_to_int[token_str]
    
    def tokens_to_midi(self, tokens: List[int], output_path: str, tempo: int = 120,
                      program: int = 0) -> bool:
        """Enhanced token to MIDI conversion with better musical structure"""
        
        try:
            midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
            instrument = pretty_midi.Instrument(program=program)
            
            current_time = 0.0
            chord_mode = False
            chord_notes = []
            chord_start_time = 0.0
            
            for token in tokens:
                if token >= len(self.int_to_note):
                    continue
                
                token_str = self.int_to_note[token]
                
                if token_str == 'START':
                    current_time = 0.0
                elif token_str == 'END':
                    break
                elif token_str == 'TIME_STEP':
                    current_time += self.time_quantization
                elif token_str == 'CHORD_START':
                    chord_mode = True
                    chord_notes = []
                    chord_start_time = current_time
                elif token_str == 'CHORD_END':
                    # Add all chord notes simultaneously
                    for note_info in chord_notes:
                        note = pretty_midi.Note(
                            velocity=note_info['velocity'],
                            pitch=note_info['pitch'],
                            start=chord_start_time,
                            end=chord_start_time + note_info['duration']
                        )
                        instrument.notes.append(note)
                    chord_mode = False
                    chord_notes = []
                elif token_str.startswith('NOTE_'):
                    note_info = self._parse_note_token(token_str)
                    if note_info:
                        if chord_mode:
                            chord_notes.append(note_info)
                        else:
                            note = pretty_midi.Note(
                                velocity=note_info['velocity'],
                                pitch=note_info['pitch'],
                                start=current_time,
                                end=current_time + note_info['duration']
                            )
                            instrument.notes.append(note)
            
            # Sort notes by start time for better playback
            instrument.notes.sort(key=lambda x: x.start)
            
            midi.instruments.append(instrument)
            midi.write(output_path)
            
            # Validate generated file
            if os.path.exists(output_path) and os.path.getsize(output_path) > 100:
                logger.info(f"Generated MIDI file: {output_path} ({len(instrument.notes)} notes)")
                return True
            else:
                return False
            
        except Exception as e:
            logger.error(f"Error creating MIDI file: {e}")
            return False
    
    def _parse_note_token(self, token_str: str) -> Optional[Dict]:
        """Parse enhanced note token back to note information"""
        try:
            parts = token_str.split('_')
            if len(parts) >= 5 and parts[0] == 'NOTE':
                pitch = int(parts[1])
                duration_bin = int(parts[2])
                velocity_bin = int(parts[3])
                # instrument_bin = int(parts[4])  # For future use
                
                duration = duration_bin * self.time_quantization
                velocity = min(127, max(1, velocity_bin * (128 // self.velocity_bins) + 64))
                
                if (self.pitch_range[0] <= pitch <= self.pitch_range[1] and
                    0.1 <= duration <= self.max_duration):
                    
                    return {
                        'pitch': pitch,
                        'duration': duration,
                        'velocity': velocity
                    }
            
            return None
            
        except (ValueError, IndexError):
            return None
    
    def process_multiple_files(self, file_paths: List[str], max_workers: int = 4) -> List[List[int]]:
        """Process multiple MIDI files in parallel for better performance"""
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all files for processing
            future_to_file = {
                executor.submit(self.midi_to_tokens, file_path): file_path 
                for file_path in file_paths
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    tokens = future.result()
                    if tokens:  # Only add non-empty results
                        results.append(tokens)
                        logger.info(f"Processed {os.path.basename(file_path)}: {len(tokens)} tokens")
                    else:
                        logger.warning(f"No tokens extracted from {file_path}")
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
        
        logger.info(f"Successfully processed {len(results)} out of {len(file_paths)} files")
        return results
    
    def save_vocabulary(self, path: str):
        """Enhanced vocabulary saving with metadata"""
        vocab_data = {
            'version': '2.0',
            'note_to_int': self.note_to_int,
            'int_to_note': self.int_to_note,
            'vocab_size': self.vocab_size,
            'time_quantization': self.time_quantization,
            'velocity_bins': self.velocity_bins,
            'pitch_range': self.pitch_range,
            'special_tokens': self.special_tokens,
            'max_duration': self.max_duration,
            'min_duration': self.min_duration,
            'created': str(Path(path).stat().st_mtime) if Path(path).exists() else 'unknown'
        }
        
        with open(path, 'w') as f:
            json.dump(vocab_data, f, indent=2)
        
        logger.info(f"Vocabulary saved: {self.vocab_size} tokens")
    
    def load_vocabulary(self, path: str) -> bool:
        """Enhanced vocabulary loading with version compatibility"""
        try:
            with open(path, 'r') as f:
                vocab_data = json.load(f)
            
            version = vocab_data.get('version', '1.0')
            logger.info(f"Loading vocabulary version {version}")
            
            # Load core vocabulary
            self.note_to_int = {k: int(v) for k, v in vocab_data['note_to_int'].items()}
            self.int_to_note = {int(k): v for k, v in vocab_data['int_to_note'].items()}
            self.vocab_size = vocab_data['vocab_size']
            
            # Load enhanced parameters
            self.time_quantization = vocab_data.get('time_quantization', 0.125)
            self.velocity_bins = vocab_data.get('velocity_bins', 16)
            self.pitch_range = tuple(vocab_data.get('pitch_range', [21, 108]))
            self.max_duration = vocab_data.get('max_duration', 8.0)
            self.min_duration = vocab_data.get('min_duration', 0.05)
            
            # Update special tokens if available
            if 'special_tokens' in vocab_data:
                self.special_tokens.update(vocab_data['special_tokens'])
            
            logger.info(f"Vocabulary loaded successfully: {self.vocab_size} tokens")
            return True
            
        except Exception as e:
            logger.error(f"Error loading vocabulary: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get processor statistics and information"""
        return {
            'vocab_size': self.vocab_size,
            'time_quantization': self.time_quantization,
            'velocity_bins': self.velocity_bins,
            'pitch_range': self.pitch_range,
            'cache_size': len(self._file_cache),
            'special_tokens': len(self.special_tokens),
            'version': '2.0'
        }
    
    def clear_cache(self):
        """Clear all caches to free memory"""
        self._file_cache.clear()
        self._validation_cache.clear()
        logger.info("Processor caches cleared")
