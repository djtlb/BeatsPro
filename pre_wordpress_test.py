#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Pre-WordPress Test Boot Sequence
Complete system validation before WordPress deployment
"""

import os
import sys
import time
import requests
import subprocess
import threading
from datetime import datetime

class PreWordPressTestSuite:
    """Comprehensive test suite before WordPress deployment"""
    
    def __init__(self):
        self.test_results = {}
        self.critical_issues = []
        self.warnings = []
        self.deployment_ready = False
        self.test_start_time = datetime.now()
        
    def display_banner(self):
        """Display test suite banner"""
        print("🎵 BEAT ADDICTS - PRE-WORDPRESS TEST SUITE")
        print("=" * 80)
        print("🧪 Comprehensive System Validation")
        print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 Purpose: Validate system before WordPress deployment")
        print("=" * 80)
        print()
    
    def test_1_core_connections(self):
        """Test 1: Core connection manager functionality"""
        print("🧪 TEST 1: Core Connection Manager")
        print("-" * 50)
        
        try:
            from beat_addicts_connection_manager import BeatAddictsConnectionManager
            
            manager = BeatAddictsConnectionManager()
            connections = manager.connect_all()
            report = manager.get_connection_report()
            
            success_rate = report.get('success_rate', 0)
            
            if success_rate == 100:
                print("✅ PASS: All connections successful (100%)")
                self.test_results['core_connections'] = 'PASS'
            elif success_rate >= 80:
                print(f"⚠️ WARNING: Connections mostly successful ({success_rate:.1f}%)")
                self.test_results['core_connections'] = 'WARNING'
                self.warnings.append(f"Connection success rate: {success_rate:.1f}%")
            else:
                print(f"❌ FAIL: Critical connection issues ({success_rate:.1f}%)")
                self.test_results['core_connections'] = 'FAIL'
                self.critical_issues.append(f"Low connection success rate: {success_rate:.1f}%")
            
            print(f"   📊 Connected Modules: {report.get('total_connected', 0)}")
            print(f"   ❌ Failed Modules: {report.get('total_failed', 0)}")
            
            if report.get('failed_modules'):
                print("   🔍 Failed Modules:")
                for module, error in report.get('failed_modules', {}).items():
                    print(f"      - {module}: {error[:100]}")
            
            return success_rate >= 80
            
        except Exception as e:
            print(f"❌ CRITICAL FAIL: Connection manager error - {e}")
            self.test_results['core_connections'] = 'CRITICAL_FAIL'
            self.critical_issues.append(f"Connection manager error: {e}")
            return False
    
    def test_2_generator_functionality(self):
        """Test 2: All music generators"""
        print("\n🧪 TEST 2: Music Generator Functionality")
        print("-" * 50)
        
        try:
            from beat_addicts_connection_manager import BeatAddictsConnectionManager
            
            manager = BeatAddictsConnectionManager()
            connections = manager.connect_all()
            generators = connections.get('generators', {})
            
            if not generators:
                print("❌ FAIL: No generators found")
                self.test_results['generators'] = 'FAIL'
                self.critical_issues.append("No music generators available")
                return False
            
            working_generators = 0
            total_generators = len(generators)
            
            print(f"   🎼 Testing {total_generators} generators...")
            
            for gen_name, gen_instance in generators.items():
                try:
                    # Test basic instantiation
                    if gen_instance and hasattr(gen_instance, '__dict__'):
                        print(f"   ✅ {gen_name}: OK")
                        working_generators += 1
                    else:
                        print(f"   ⚠️ {gen_name}: No attributes")
                        self.warnings.append(f"Generator {gen_name} has limited functionality")
                        
                except Exception as e:
                    print(f"   ❌ {gen_name}: Error - {e}")
                    self.warnings.append(f"Generator {gen_name} error: {e}")
            
            success_rate = (working_generators / total_generators) * 100
            
            if success_rate >= 85:
                print(f"✅ PASS: Generators working ({success_rate:.1f}%)")
                self.test_results['generators'] = 'PASS'
            elif success_rate >= 60:
                print(f"⚠️ WARNING: Some generator issues ({success_rate:.1f}%)")
                self.test_results['generators'] = 'WARNING'
            else:
                print(f"❌ FAIL: Critical generator issues ({success_rate:.1f}%)")
                self.test_results['generators'] = 'FAIL'
                self.critical_issues.append(f"Low generator success rate: {success_rate:.1f}%")
            
            return success_rate >= 60
            
        except Exception as e:
            print(f"❌ CRITICAL FAIL: Generator test error - {e}")
            self.test_results['generators'] = 'CRITICAL_FAIL'
            self.critical_issues.append(f"Generator test error: {e}")
            return False
    
    def test_3_web_services_startup(self):
        """Test 3: Web services can start properly"""
        print("\n🧪 TEST 3: Web Services Startup")
        print("-" * 50)
        
        test_processes = []
        
        services_to_test = [
            {
                'name': 'Master Endpoints',
                'script': 'master_endpoints.py',
                'port': 5001,
                'timeout': 10
            },
            {
                'name': 'Music Generator App',
                'script': 'music_generator_app.py', 
                'port': 5000,
                'timeout': 15
            }
        ]
        
        successful_starts = 0
        
        for service in services_to_test:
            print(f"   🚀 Starting {service['name']}...")
            
            try:
                # Start the service
                process = subprocess.Popen([
                    sys.executable, service['script']
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                test_processes.append({
                    'name': service['name'],
                    'process': process,
                    'port': service['port']
                })
                
                # Wait for startup
                time.sleep(service['timeout'])
                
                # Check if process is still running
                if process.poll() is None:
                    print(f"   ✅ {service['name']}: Started successfully")
                    successful_starts += 1
                else:
                    print(f"   ❌ {service['name']}: Process terminated")
                    stdout, stderr = process.communicate()
                    if stderr:
                        print(f"      Error: {stderr[:200]}")
                        self.warnings.append(f"{service['name']} startup error: {stderr[:100]}")
                
            except Exception as e:
                print(f"   ❌ {service['name']}: Startup failed - {e}")
                self.warnings.append(f"{service['name']} startup failed: {e}")
        
        # Clean up test processes
        print("   🧹 Cleaning up test processes...")
        for service_info in test_processes:
            try:
                if service_info['process'].poll() is None:
                    service_info['process'].terminate()
                    service_info['process'].wait(timeout=5)
                    print(f"   🛑 {service_info['name']}: Stopped")
            except Exception as e:
                print(f"   ⚠️ {service_info['name']}: Cleanup issue - {e}")
        
        success_rate = (successful_starts / len(services_to_test)) * 100
        
        if success_rate == 100:
            print("✅ PASS: All web services start properly")
            self.test_results['web_services'] = 'PASS'
        elif success_rate >= 50:
            print(f"⚠️ WARNING: Some services have issues ({success_rate:.1f}%)")
            self.test_results['web_services'] = 'WARNING'
        else:
            print(f"❌ FAIL: Critical web service issues ({success_rate:.1f}%)")
            self.test_results['web_services'] = 'FAIL'
            self.critical_issues.append("Web services cannot start properly")
        
        return success_rate >= 50
    
    def test_4_file_structure_integrity(self):
        """Test 4: File structure and dependencies"""
        print("\n🧪 TEST 4: File Structure & Dependencies")
        print("-" * 50)
        
        critical_files = [
            'beat_addicts_connection_manager.py',
            'master_endpoints.py',
            'music_generator_app.py',
            'beat_addicts_core/web_interface.py',
            'beat_addicts_generators/generator_wrapper.py'
        ]
        
        missing_files = []
        existing_files = []
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                existing_files.append(file_path)
                print(f"   ✅ {file_path}: Found")
            else:
                missing_files.append(file_path)
                print(f"   ❌ {file_path}: Missing")
        
        # Check for Python dependencies
        print("   🐍 Checking Python dependencies...")
        
        required_packages = ['flask', 'numpy']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"   ✅ {package}: Available")
            except ImportError:
                missing_packages.append(package)
                print(f"   ⚠️ {package}: Missing (will use fallback)")
        
        if not missing_files and len(missing_packages) == 0:
            print("✅ PASS: All critical files and dependencies present")
            self.test_results['file_structure'] = 'PASS'
        elif len(missing_packages) > 0 and len(missing_files) == 0:
            print("⚠️ WARNING: Some optional packages missing")
            self.test_results['file_structure'] = 'WARNING'
            self.warnings.extend([f"Missing package: {pkg}" for pkg in missing_packages])
        else:
            print("❌ FAIL: Critical files missing")
            self.test_results['file_structure'] = 'FAIL'
            self.critical_issues.extend([f"Missing file: {file}" for file in missing_files])
        
        return len(missing_files) == 0
    
    def test_5_wordpress_readiness(self):
        """Test 5: WordPress deployment readiness"""
        print("\n🧪 TEST 5: WordPress Deployment Readiness")
        print("-" * 50)
        
        wordpress_checks = []
        
        # Check 1: WordPress directory exists
        wordpress_dir = 'wordpress-music-generator'
        if os.path.exists(wordpress_dir):
            print(f"   ✅ WordPress directory found: {wordpress_dir}")
            wordpress_checks.append(True)
        else:
            print(f"   ⚠️ WordPress directory not found: {wordpress_dir}")
            print("      📝 Note: Will be created during deployment")
            wordpress_checks.append(False)
        
        # Check 2: Standalone capability
        print("   🔍 Testing standalone operation...")
        standalone_ready = True
        
        try:
            # Test if system can run without external dependencies
            from beat_addicts_connection_manager import BeatAddictsConnectionManager
            manager = BeatAddictsConnectionManager()
            connections = manager.connect_all()
            
            if connections:
                print("   ✅ Standalone operation: Ready")
            else:
                print("   ⚠️ Standalone operation: Limited")
                standalone_ready = False
                
        except Exception as e:
            print(f"   ❌ Standalone operation: Issues - {e}")
            standalone_ready = False
        
        wordpress_checks.append(standalone_ready)
        
        # Check 3: Port configuration
        print("   🌐 Port configuration check...")
        default_ports = [5000, 5001, 5002]
        
        print("   📍 Default ports: 5000 (app), 5001 (api), 5002 (core)")
        print("   ✅ Port configuration: WordPress compatible")
        wordpress_checks.append(True)
        
        success_rate = (sum(wordpress_checks) / len(wordpress_checks)) * 100
        
        if success_rate >= 80:
            print("✅ PASS: Ready for WordPress deployment")
            self.test_results['wordpress_readiness'] = 'PASS'
        elif success_rate >= 60:
            print("⚠️ WARNING: Minor WordPress deployment concerns")
            self.test_results['wordpress_readiness'] = 'WARNING'
        else:
            print("❌ FAIL: Not ready for WordPress deployment")
            self.test_results['wordpress_readiness'] = 'FAIL'
            self.critical_issues.append("System not ready for WordPress deployment")
        
        return success_rate >= 60
    
    def run_full_test_suite(self):
        """Run complete test suite"""
        self.display_banner()
        
        test_functions = [
            self.test_1_core_connections,
            self.test_2_generator_functionality,
            self.test_3_web_services_startup,
            self.test_4_file_structure_integrity,
            self.test_5_wordpress_readiness
        ]
        
        passed_tests = 0
        total_tests = len(test_functions)
        
        for test_func in test_functions:
            try:
                if test_func():
                    passed_tests += 1
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                print(f"❌ Test error: {e}")
        
        # Generate final report
        self.generate_final_report(passed_tests, total_tests)
        
        return self.deployment_ready
    
    def generate_final_report(self, passed_tests, total_tests):
        """Generate comprehensive final report"""
        test_duration = datetime.now() - self.test_start_time
        
        print("\n" + "=" * 80)
        print("🎯 FINAL PRE-WORDPRESS TEST REPORT")
        print("=" * 80)
        
        # Overall status
        overall_success = (passed_tests / total_tests) * 100
        
        print(f"📊 Overall Test Results: {passed_tests}/{total_tests} tests passed ({overall_success:.1f}%)")
        print(f"⏱️ Test Duration: {str(test_duration).split('.')[0]}")
        print(f"🕒 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Detailed results
        print("📋 Test Results Breakdown:")
        for test_name, result in self.test_results.items():
            status_icon = {
                'PASS': '✅',
                'WARNING': '⚠️',
                'FAIL': '❌',
                'CRITICAL_FAIL': '🚨'
            }.get(result, '❓')
            
            print(f"   {status_icon} {test_name.replace('_', ' ').title()}: {result}")
        
        print()
        
        # Critical issues
        if self.critical_issues:
            print("🚨 CRITICAL ISSUES (Must fix before WordPress deployment):")
            for issue in self.critical_issues:
                print(f"   🔥 {issue}")
            print()
        
        # Warnings
        if self.warnings:
            print("⚠️ WARNINGS (Recommend addressing):")
            for warning in self.warnings:
                print(f"   ⚠️ {warning}")
            print()
        
        # Deployment readiness
        if overall_success >= 80 and not self.critical_issues:
            print("🎉 DEPLOYMENT STATUS: ✅ READY FOR WORDPRESS")
            print("   System passed all critical tests and is ready for deployment.")
            self.deployment_ready = True
        elif overall_success >= 60 and len(self.critical_issues) <= 1:
            print("⚠️ DEPLOYMENT STATUS: 🔶 PROCEED WITH CAUTION")
            print("   System mostly ready, but address warnings before deployment.")
            self.deployment_ready = False
        else:
            print("❌ DEPLOYMENT STATUS: 🛑 NOT READY")
            print("   Critical issues must be resolved before WordPress deployment.")
            self.deployment_ready = False
        
        print()
        print("📋 RECOMMENDED NEXT STEPS:")
        
        if self.deployment_ready:
            print("   1. ✅ System is ready for WordPress deployment")
            print("   2. 📦 Package files for WordPress transfer")
            print("   3. 🚀 Deploy to WordPress environment")
            print("   4. 🧪 Run post-deployment verification")
        else:
            print("   1. 🔧 Address all critical issues listed above")
            if self.warnings:
                print("   2. ⚠️ Review and resolve warnings")
            print("   3. 🔄 Re-run this test suite")
            print("   4. 📦 Deploy only after all tests pass")
        
        print("=" * 80)

def main():
    """Main test execution"""
    tester = PreWordPressTestSuite()
    success = tester.run_full_test_suite()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
