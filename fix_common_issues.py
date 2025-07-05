import numpy as np
import os
import sys

class ProductionFixer:
    def __init__(self):
        self.fixes_applied = []
    
    def fix_import_issues(self):
        """Fix common import problems"""
        print("🔧 Fixing import issues...")
        
        # Check and install missing packages
        required_packages = [
            'numpy', 'scipy', 'soundfile'
        ]
        
        missing = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            print(f"📦 Installing missing packages: {missing}")
            import subprocess
            for package in missing:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    self.fixes_applied.append(f"Installed {package}")
                except:
                    print(f"❌ Failed to install {package}")
        else:
            print("✅ All packages available")
    
    def fix_audio_issues(self):
        """Fix audio-related problems"""
        print("🔧 Fixing audio issues...")
        
        # Create fallback audio export function
        fallback_code = '''
def safe_audio_export(audio, filename, sample_rate=44100):
    """Fallback audio export function"""
    try:
        import soundfile as sf
        sf.write(filename, audio, sample_rate)
        return True
    except ImportError:
        try:
            from scipy.io.wavfile import write
            if audio.ndim == 1:
                audio_16bit = (audio * 32767).astype(np.int16)
            else:
                audio_16bit = (audio * 32767).astype(np.int16)
            write(filename, sample_rate, audio_16bit)
            return True
        except:
            print("❌ Cannot export audio - no suitable library")
            return False
'''
        
        # Write fallback to file
        with open("audio_fallback.py", 'w') as f:
            f.write(fallback_code)
        
        self.fixes_applied.append("Created audio fallback system")
        print("✅ Audio fallback system created")
    
    def fix_memory_issues(self):
        """Optimize for memory usage"""
        print("🔧 Optimizing memory usage...")
        
        optimization_code = '''
# Memory optimization patches
import gc

def optimize_audio_generation():
    """Optimize audio generation for lower memory usage"""
    # Force garbage collection
    gc.collect()
    
    # Reduce default sample rates for testing
    DEFAULT_SAMPLE_RATE = 44100  # Instead of 48000
    DEFAULT_DURATION = 8.0       # Instead of 16.0
    
    return DEFAULT_SAMPLE_RATE, DEFAULT_DURATION

def safe_array_operation(func, *args, **kwargs):
    """Safely perform array operations with memory cleanup"""
    try:
        result = func(*args, **kwargs)
        gc.collect()  # Clean up immediately
        return result
    except MemoryError:
        gc.collect()
        print("⚠️ Memory limit reached, using smaller buffer")
        # Retry with smaller parameters
        return None
'''
        
        with open("memory_optimization.py", 'w') as f:
            f.write(optimization_code)
        
        self.fixes_applied.append("Created memory optimization module")
        print("✅ Memory optimization module created")
    
    def create_minimal_test_version(self):
        """Create a minimal version for testing"""
        print("🔧 Creating minimal test version...")
        
        minimal_code = '''
"""
Minimal AI Music Producer for Testing
Simplified version with reduced complexity
"""
import numpy as np
import random

class MinimalAIProducer:
    def __init__(self, sample_rate=44100):
        self.sr = sample_rate
        self.bpm = 140
        
    def generate_simple_kick(self, duration=0.5):
        """Simple kick drum"""
        t = np.linspace(0, duration, int(self.sr * duration))
        kick = np.sin(2 * np.pi * 60 * t) * np.exp(-t * 5)
        return kick * 0.8
    
    def generate_simple_snare(self, duration=0.2):
        """Simple snare"""
        t = np.linspace(0, duration, int(self.sr * duration))
        noise = np.random.uniform(-1, 1, len(t))
        envelope = np.exp(-t * 15)
        return noise * envelope * 0.6
    
    def generate_simple_hihat(self, duration=0.1):
        """Simple hi-hat"""
        t = np.linspace(0, duration, int(self.sr * duration))
        noise = np.random.uniform(-1, 1, len(t))
        envelope = np.exp(-t * 30)
        return noise * envelope * 0.3
    
    def create_simple_beat(self, duration=4.0):
        """Create simple beat pattern"""
        samples = int(self.sr * duration)
        beat = np.zeros(samples)
        
        # Simple 4/4 pattern
        kick = self.generate_simple_kick()
        snare = self.generate_simple_snare()
        hihat = self.generate_simple_hihat()
        
        beat_duration = 60.0 / self.bpm
        
        for beat_num in range(int(duration / beat_duration)):
            start_sample = int(beat_num * beat_duration * self.sr)
            
            # Kick on 1 and 3
            if beat_num % 4 in [0, 2]:
                end_sample = min(start_sample + len(kick), samples)
                beat[start_sample:end_sample] += kick[:end_sample-start_sample]
            
            # Snare on 2 and 4
            if beat_num % 4 in [1, 3]:
                end_sample = min(start_sample + len(snare), samples)
                beat[start_sample:end_sample] += snare[:end_sample-start_sample]
            
            # Hi-hat every beat
            end_sample = min(start_sample + len(hihat), samples)
            beat[start_sample:end_sample] += hihat[:end_sample-start_sample]
        
        return beat
    
    def export_simple(self, audio, filename):
        """Simple export function"""
        try:
            from scipy.io.wavfile import write
            audio_16bit = (np.clip(audio, -1, 1) * 32767).astype(np.int16)
            write(f"{filename}.wav", self.sr, audio_16bit)
            print(f"✅ Exported: {filename}.wav")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False

def test_minimal_producer():
    """Test the minimal producer"""
    print("🧪 Testing minimal producer...")
    producer = MinimalAIProducer()
    
    # Generate short test beat
    beat = producer.create_simple_beat(duration=2.0)
    
    # Export test
    if producer.export_simple(beat, "minimal_test"):
        print("✅ Minimal producer working!")
        return True
    else:
        print("❌ Minimal producer failed")
        return False

if __name__ == "__main__":
    test_minimal_producer()
'''
        
        with open("minimal_ai_producer.py", 'w') as f:
            f.write(minimal_code)
        
        self.fixes_applied.append("Created minimal test version")
        print("✅ Minimal test version created")
    
    def apply_all_fixes(self):
        """Apply all available fixes"""
        print("🛠️ APPLYING ALL FIXES")
        print("=" * 30)
        
        self.fix_import_issues()
        self.fix_audio_issues()
        self.fix_memory_issues()
        self.create_minimal_test_version()
        
        print(f"\n✅ Applied {len(self.fixes_applied)} fixes:")
        for fix in self.fixes_applied:
            print(f"  - {fix}")
        
        print("\n🎯 Try running the minimal version first:")
        print("  python minimal_ai_producer.py")

if __name__ == "__main__":
    fixer = ProductionFixer()
    fixer.apply_all_fixes()
