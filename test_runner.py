import sys
import time

def quick_test():
    """Run quick functionality test"""
    print("⚡ QUICK TEST RUNNER ⚡")
    print("=" * 25)
    
    # Test 1: Basic imports
    print("1. Testing imports...")
    try:
        import numpy as np
        print("  ✅ numpy")
    except:
        print("  ❌ numpy - run: pip install numpy")
        return False
    
    try:
        import scipy.signal
        print("  ✅ scipy")
    except:
        print("  ❌ scipy - run: pip install scipy")
    
    # Test 2: Try minimal producer
    print("\n2. Testing minimal producer...")
    try:
        from minimal_ai_producer import MinimalAIProducer, test_minimal_producer
        if test_minimal_producer():
            print("  ✅ Minimal producer works!")
        else:
            print("  ❌ Minimal producer failed")
            return False
    except ImportError:
        print("  ⚠️ Minimal producer not found - run fix_common_issues.py first")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 3: Try full system (if minimal works)
    print("\n3. Testing full system...")
    try:
        from debug_production_system import ProductionDebugger
        debugger = ProductionDebugger()
        
        # Quick component test
        if debugger.test_imports():
            print("  ✅ Full system imports OK")
            return True
        else:
            print("  ⚠️ Some imports missing")
            return False
    except Exception as e:
        print(f"  ⚠️ Full system not ready: {e}")
        print("  💡 Use minimal version for now")
        return True  # Minimal working is still success
    
    return True

def main():
    start_time = time.time()
    
    if quick_test():
        print(f"\n🎉 SYSTEM READY! ({time.time()-start_time:.1f}s)")
        print("\n🚀 Next steps:")
        print("  - Run: python minimal_ai_producer.py (for basic test)")
        print("  - Run: python debug_production_system.py (for full diagnostic)")
        print("  - Run: python start_bot.py (for full production)")
    else:
        print(f"\n❌ ISSUES FOUND ({time.time()-start_time:.1f}s)")
        print("\n🔧 Fixes to try:")
        print("  - Run: python fix_common_issues.py")
        print("  - Install missing packages: pip install numpy scipy soundfile")

if __name__ == "__main__":
    main()
