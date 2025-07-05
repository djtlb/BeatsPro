import numpy as np
import traceback
import time
import os
import sys
from datetime import datetime
import json

class ProductionDebugger:
    def __init__(self):
        self.test_results = []
        self.errors_found = []
        self.performance_metrics = {}
        
    def test_imports(self):
        """Test all module imports"""
        print("🔍 Testing imports...")
        
        modules_to_test = [
            ('numpy', 'np'),
            ('scipy.signal', 'signal'),
            ('scipy.io.wavfile', 'write'),
            ('json', None),
            ('random', None),
            ('threading', None),
            ('time', None)
        ]
        
        missing_modules = []
        
        for module_name, alias in modules_to_test:
            try:
                if alias:
                    exec(f"import {module_name} as {alias}")
                else:
                    exec(f"import {module_name}")
                print(f"✅ {module_name}")
            except ImportError as e:
                missing_modules.append(module_name)
                print(f"❌ {module_name}: {e}")
        
        if missing_modules:
            print(f"\n⚠️  Install missing modules: pip install {' '.join(missing_modules)}")
            return False
        
        return True
    
    def test_ai_components(self):
        """Test AI music production components"""
        print("\n🧠 Testing AI components...")
        
        try:
            # Test NeuralMusicAI
            from ai_music_producer import NeuralMusicAI, ProductionSettings
            ai = NeuralMusicAI(sample_rate=44100)  # Lower sample rate for testing
            print("✅ NeuralMusicAI initialized")
            
            # Test basic generation
            test_kick = ai.generate_neural_808(60, 0.5)
            if len(test_kick) > 0 and not np.all(test_kick == 0):
                print("✅ 808 generation working")
            else:
                print("❌ 808 generation failed")
                return False
            
            # Test drum pattern
            drums = ai.generate_intelligent_drums(2.0)  # Short test
            if len(drums) > 0:
                print("✅ Drum generation working")
            else:
                print("❌ Drum generation failed")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ AI component error: {e}")
            traceback.print_exc()
            return False
    
    def test_rap_generator(self):
        """Test rap lyrics generation"""
        print("\n📝 Testing rap generator...")
        
        try:
            from modern_rap_generator import ModernRapGenerator
            gen = ModernRapGenerator()
            
            # Test verse generation
            verse = gen.generate_bars("aggressive", 4)
            if len(verse) == 4:
                print("✅ Verse generation working")
            else:
                print("❌ Verse generation failed")
                return False
            
            # Test full song
            song = gen.create_full_song("Test Track")
            if "verse1" in song and "hook" in song:
                print("✅ Full song generation working")
            else:
                print("❌ Full song generation failed")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Rap generator error: {e}")
            traceback.print_exc()
            return False
    
    def test_audio_engine(self):
        """Test premium audio engine"""
        print("\n🎵 Testing audio engine...")
        
        try:
            from premium_audio_engine import PremiumAudioEngine
            engine = PremiumAudioEngine(sample_rate=44100)
            
            # Test individual components
            kick = engine.generate_808_kick()
            snare = engine.generate_trap_snare()
            hihat = engine.generate_modern_hihat()
            
            if all(len(x) > 0 for x in [kick, snare, hihat]):
                print("✅ Individual drum samples working")
            else:
                print("❌ Drum sample generation failed")
                return False
            
            # Test pattern creation
            pattern = engine.create_trap_pattern(2.0)  # Short test
            if len(pattern) > 0 and not np.all(pattern == 0):
                print("✅ Pattern creation working")
            else:
                print("❌ Pattern creation failed")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Audio engine error: {e}")
            traceback.print_exc()
            return False
    
    def test_production_bot(self):
        """Test full production bot"""
        print("\n🤖 Testing production bot...")
        
        try:
            from ai_production_bot import AIProductionBot
            bot = AIProductionBot()
            
            # Test preset loading
            if bot.load_preset("hyperpop_2025"):
                print("✅ Preset loading working")
            else:
                print("❌ Preset loading failed")
                return False
            
            # Test quick production (very short)
            start_time = time.time()
            track = bot._produce_full_track(1.0)  # 1 second test
            end_time = time.time()
            
            if len(track) > 0 and not np.all(track == 0):
                print(f"✅ Production working ({end_time-start_time:.2f}s)")
                self.performance_metrics['production_time'] = end_time - start_time
            else:
                print("❌ Production failed")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Production bot error: {e}")
            traceback.print_exc()
            return False
    
    def performance_benchmark(self):
        """Benchmark production performance"""
        print("\n⚡ Performance benchmark...")
        
        try:
            from ai_production_bot import AIProductionBot
            bot = AIProductionBot()
            bot.load_preset("drill_uk")
            
            # Benchmark different durations
            test_durations = [1.0, 2.0, 4.0]
            
            for duration in test_durations:
                start_time = time.time()
                track = bot._produce_full_track(duration)
                end_time = time.time()
                
                production_time = end_time - start_time
                real_time_factor = production_time / duration
                
                print(f"  {duration}s track: {production_time:.2f}s ({real_time_factor:.1f}x real-time)")
                
                # Quality check
                if len(track) > 0 and np.max(np.abs(track)) > 0.01:
                    print(f"  ✅ Quality check passed")
                else:
                    print(f"  ❌ Quality check failed")
            
            return True
            
        except Exception as e:
            print(f"❌ Benchmark error: {e}")
            return False
    
    def test_file_operations(self):
        """Test file I/O operations"""
        print("\n💾 Testing file operations...")
        
        try:
            # Test audio export
            test_audio = np.random.uniform(-0.5, 0.5, 44100)  # 1 second of test audio
            
            from premium_audio_engine import PremiumAudioEngine
            engine = PremiumAudioEngine()
            
            test_filename = "debug_test_audio"
            engine.export_wav(test_audio, f"{test_filename}.wav")
            
            # Check if file was created
            if os.path.exists(f"{test_filename}.wav"):
                print("✅ Audio export working")
                # Clean up
                os.remove(f"{test_filename}.wav")
            else:
                print("❌ Audio export failed")
                return False
            
            # Test JSON export
            test_data = {"test": "data", "timestamp": datetime.now().isoformat()}
            with open("debug_test.json", 'w') as f:
                json.dump(test_data, f)
            
            if os.path.exists("debug_test.json"):
                print("✅ JSON export working")
                os.remove("debug_test.json")
            else:
                print("❌ JSON export failed")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ File operations error: {e}")
            return False
    
    def run_full_diagnostic(self):
        """Run complete diagnostic suite"""
        print("🩺 RUNNING FULL DIAGNOSTIC")
        print("=" * 50)
        
        tests = [
            ("Import Test", self.test_imports),
            ("AI Components", self.test_ai_components),
            ("Rap Generator", self.test_rap_generator),
            ("Audio Engine", self.test_audio_engine),
            ("Production Bot", self.test_production_bot),
            ("File Operations", self.test_file_operations),
            ("Performance Benchmark", self.performance_benchmark)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}")
            print("-" * 30)
            
            try:
                if test_func():
                    passed_tests += 1
                    self.test_results.append({"test": test_name, "status": "PASSED"})
                else:
                    self.test_results.append({"test": test_name, "status": "FAILED"})
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                self.test_results.append({"test": test_name, "status": "CRASHED", "error": str(e)})
        
        # Generate report
        self.generate_diagnostic_report(passed_tests, total_tests)
        
        return passed_tests == total_tests
    
    def generate_diagnostic_report(self, passed, total):
        """Generate diagnostic report"""
        print(f"\n📊 DIAGNOSTIC REPORT")
        print("=" * 30)
        print(f"Tests Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL SYSTEMS GO! Production bot is 10/10!")
        else:
            print("⚠️  Issues found. Check failed tests above.")
        
        # Save detailed report
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total,
                "passed_tests": passed,
                "success_rate": (passed/total)*100
            },
            "test_results": self.test_results,
            "performance_metrics": self.performance_metrics,
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform
            }
        }
        
        report_file = f"diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📋 Detailed report saved: {report_file}")

if __name__ == "__main__":
    debugger = ProductionDebugger()
    debugger.run_full_diagnostic()
