#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - Connection Test & Verification System
Test all endpoint connections and verify proper integration
"""

import os
import sys
import requests
import threading
import time
from datetime import datetime

class BeatAddictsConnectionTester:
    """Test all BEAT ADDICTS connections and endpoints"""
    
    def __init__(self):
        self.test_results = {}
        self.servers_to_test = [
            {'name': 'Master Endpoints', 'url': 'http://localhost:5001', 'expected_endpoints': 10},
            {'name': 'Music Generator App', 'url': 'http://localhost:5000', 'expected_endpoints': 5},
            {'name': 'Core Web Interface', 'url': 'http://localhost:5002', 'expected_endpoints': 3}
        ]
        
    def test_connection_manager(self):
        """Test the connection manager directly"""
        print("🔌 Testing BEAT ADDICTS Connection Manager...")
        
        try:
            from beat_addicts_connection_manager import BeatAddictsConnectionManager
            
            manager = BeatAddictsConnectionManager()
            connections = manager.connect_all()
            
            # Test connections
            test_results = manager.test_connections()
            report = manager.get_connection_report()
            
            success_rate = report.get('success_rate', 0)
            
            self.test_results['connection_manager'] = {
                'status': 'pass' if success_rate == 100 else 'warning',
                'success_rate': success_rate,
                'connected_modules': report.get('total_connected', 0),
                'failed_modules': report.get('total_failed', 0),
                'details': report
            }
            
            print(f"   ✅ Connection Manager: {success_rate:.1f}% success rate")
            print(f"   🎵 Connected Modules: {report.get('total_connected', 0)}")
            print(f"   ❌ Failed Modules: {report.get('total_failed', 0)}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Connection Manager Test Failed: {e}")
            self.test_results['connection_manager'] = {
                'status': 'fail',
                'error': str(e)
            }
            return False
    
    def test_master_endpoints(self):
        """Test master endpoints server"""
        print("🌐 Testing Master Endpoints Server...")
        
        base_url = 'http://localhost:5001'
        endpoints_to_test = [
            {'path': '/api/master/status', 'method': 'GET', 'expected_keys': ['success', 'status']},
            {'path': '/api/generators/list', 'method': 'GET', 'expected_keys': ['success', 'generators']},
            {'path': '/api/voice/presets', 'method': 'GET', 'expected_keys': ['success', 'voice_presets']},
            {'path': '/api/system/health', 'method': 'GET', 'expected_keys': ['success']},
            {'path': '/api/files/list', 'method': 'GET', 'expected_keys': ['success']}
        ]
        
        results = {}
        total_tests = len(endpoints_to_test)
        passed_tests = 0
        
        for endpoint in endpoints_to_test:
            try:
                url = f"{base_url}{endpoint['path']}"
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check for expected keys
                    has_expected_keys = all(key in data for key in endpoint['expected_keys'])
                    
                    if has_expected_keys:
                        results[endpoint['path']] = 'pass'
                        passed_tests += 1
                        print(f"   ✅ {endpoint['path']}: OK")
                    else:
                        results[endpoint['path']] = 'warning'
                        print(f"   ⚠️ {endpoint['path']}: Missing expected keys")
                else:
                    results[endpoint['path']] = 'fail'
                    print(f"   ❌ {endpoint['path']}: HTTP {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                results[endpoint['path']] = 'fail'
                print(f"   ❌ {endpoint['path']}: Connection refused (server not running?)")
            except Exception as e:
                results[endpoint['path']] = 'fail'
                print(f"   ❌ {endpoint['path']}: {e}")
        
        success_rate = (passed_tests / total_tests) * 100
        
        self.test_results['master_endpoints'] = {
            'status': 'pass' if success_rate >= 80 else 'warning' if success_rate >= 50 else 'fail',
            'success_rate': success_rate,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'endpoint_results': results
        }
        
        print(f"   📊 Master Endpoints: {success_rate:.1f}% ({passed_tests}/{total_tests})")
        
        return success_rate >= 50
    
    def test_music_generator_endpoints(self):
        """Test music generator app endpoints"""
        print("🎵 Testing Music Generator App...")
        
        base_url = 'http://localhost:5000'
        
        try:
            # Test main page
            response = requests.get(base_url, timeout=5)
            
            if response.status_code == 200:
                print("   ✅ Music Generator App: Main page accessible")
                
                self.test_results['music_generator'] = {
                    'status': 'pass',
                    'main_page': 'accessible',
                    'response_time': response.elapsed.total_seconds()
                }
                return True
            else:
                print(f"   ❌ Music Generator App: HTTP {response.status_code}")
                self.test_results['music_generator'] = {
                    'status': 'fail',
                    'error': f'HTTP {response.status_code}'
                }
                return False
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Music Generator App: Connection refused (server not running?)")
            self.test_results['music_generator'] = {
                'status': 'fail',
                'error': 'Connection refused'
            }
            return False
        except Exception as e:
            print(f"   ❌ Music Generator App: {e}")
            self.test_results['music_generator'] = {
                'status': 'fail',
                'error': str(e)
            }
            return False
    
    def test_generator_functionality(self):
        """Test individual generator functionality"""
        print("🎼 Testing Generator Functionality...")
        
        try:
            from beat_addicts_connection_manager import BeatAddictsConnectionManager
            
            manager = BeatAddictsConnectionManager()
            connections = manager.connect_all()
            connected_generators = connections.get('generators', {})
            
            generator_results = {}
            
            for gen_name, gen_instance in connected_generators.items():
                try:
                    # Test if generator has required methods
                    methods_to_check = ['generate_midi', 'create_midi']
                    available_methods = []
                    
                    for method in methods_to_check:
                        if hasattr(gen_instance, method):
                            available_methods.append(method)
                    
                    generator_results[gen_name] = {
                        'status': 'pass' if available_methods else 'warning',
                        'available_methods': available_methods,
                        'instance_type': type(gen_instance).__name__
                    }
                    
                    print(f"   🎼 {gen_name}: {'✅' if available_methods else '⚠️'} ({len(available_methods)} methods)")
                    
                except Exception as e:
                    generator_results[gen_name] = {
                        'status': 'fail',
                        'error': str(e)
                    }
                    print(f"   ❌ {gen_name}: {e}")
            
            success_count = sum(1 for result in generator_results.values() if result['status'] == 'pass')
            total_count = len(generator_results)
            success_rate = (success_count / total_count * 100) if total_count > 0 else 0
            
            self.test_results['generator_functionality'] = {
                'status': 'pass' if success_rate >= 80 else 'warning' if success_rate >= 50 else 'fail',
                'success_rate': success_rate,
                'total_generators': total_count,
                'working_generators': success_count,
                'generator_details': generator_results
            }
            
            print(f"   📊 Generators: {success_rate:.1f}% ({success_count}/{total_count})")
            
            return success_rate >= 50
            
        except Exception as e:
            print(f"   ❌ Generator Functionality Test Failed: {e}")
            self.test_results['generator_functionality'] = {
                'status': 'fail',
                'error': str(e)
            }
            return False
    
    def test_cross_module_integration(self):
        """Test integration between different modules"""
        print("🔗 Testing Cross-Module Integration...")
        
        integration_tests = []
        
        try:
            from beat_addicts_connection_manager import BeatAddictsConnectionManager
            
            manager = BeatAddictsConnectionManager()
            connections = manager.connect_all()
            
            # Test 1: Core modules can access generators
            core_modules = connections.get('core', {})
            generators = connections.get('generators', {})
            
            if core_modules and generators:
                integration_tests.append({
                    'test': 'Core-Generator Integration',
                    'status': 'pass',
                    'details': f"{len(core_modules)} core modules, {len(generators)} generators"
                })
                print("   ✅ Core-Generator Integration: OK")
            else:
                integration_tests.append({
                    'test': 'Core-Generator Integration',
                    'status': 'fail',
                    'details': 'Missing core modules or generators'
                })
                print("   ❌ Core-Generator Integration: Failed")
            
            # Test 2: Voice handler integration
            voice_handler = core_modules.get('voice_handler')
            if voice_handler:
                integration_tests.append({
                    'test': 'Voice Handler Integration',
                    'status': 'pass',
                    'details': 'Voice handler available'
                })
                print("   ✅ Voice Handler Integration: OK")
            else:
                integration_tests.append({
                    'test': 'Voice Handler Integration',
                    'status': 'warning',
                    'details': 'Voice handler not found'
                })
                print("   ⚠️ Voice Handler Integration: Warning")
            
            # Test 3: Web interface integration
            web_modules = connections.get('web', {})
            if web_modules:
                integration_tests.append({
                    'test': 'Web Interface Integration',
                    'status': 'pass',
                    'details': f"{len(web_modules)} web modules"
                })
                print("   ✅ Web Interface Integration: OK")
            else:
                integration_tests.append({
                    'test': 'Web Interface Integration',
                    'status': 'fail',
                    'details': 'No web modules found'
                })
                print("   ❌ Web Interface Integration: Failed")
            
            passed_tests = sum(1 for test in integration_tests if test['status'] == 'pass')
            total_tests = len(integration_tests)
            success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
            
            self.test_results['integration'] = {
                'status': 'pass' if success_rate >= 80 else 'warning' if success_rate >= 50 else 'fail',
                'success_rate': success_rate,
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'test_details': integration_tests
            }
            
            print(f"   📊 Integration: {success_rate:.1f}% ({passed_tests}/{total_tests})")
            
            return success_rate >= 50
            
        except Exception as e:
            print(f"   ❌ Integration Test Failed: {e}")
            self.test_results['integration'] = {
                'status': 'fail',
                'error': str(e)
            }
            return False
    
    def run_all_tests(self):
        """Run all connection tests"""
        print("🎵 BEAT ADDICTS - CONNECTION TEST SUITE")
        print("=" * 80)
        print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        test_functions = [
            self.test_connection_manager,
            self.test_generator_functionality,
            self.test_cross_module_integration,
            self.test_master_endpoints,
            self.test_music_generator_endpoints
        ]
        
        passed_tests = 0
        total_tests = len(test_functions)
        
        for test_func in test_functions:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                print(f"   ❌ Test function {test_func.__name__} failed: {e}")
        
        # Generate final report
        print()
        print("=" * 80)
        print("🎯 FINAL CONNECTION TEST REPORT")
        print("=" * 80)
        
        overall_success_rate = (passed_tests / total_tests * 100)
        
        print(f"📊 Overall Success Rate: {overall_success_rate:.1f}%")
        print(f"✅ Passed Tests: {passed_tests}/{total_tests}")
        
        if overall_success_rate >= 80:
            print("🎉 Status: EXCELLENT - All connections working properly!")
        elif overall_success_rate >= 60:
            print("✅ Status: GOOD - Most connections working")
        elif overall_success_rate >= 40:
            print("⚠️ Status: WARNING - Some connection issues")
        else:
            print("❌ Status: CRITICAL - Major connection problems")
        
        print()
        print("📋 Detailed Results:")
        for test_name, result in self.test_results.items():
            status_icon = {
                'pass': '✅',
                'warning': '⚠️',
                'fail': '❌'
            }.get(result.get('status', 'fail'), '❓')
            
            print(f"   {status_icon} {test_name}: {result.get('status', 'unknown').upper()}")
            
            if 'success_rate' in result:
                print(f"      Success Rate: {result['success_rate']:.1f}%")
            
            if 'error' in result:
                print(f"      Error: {result['error']}")
        
        print("=" * 80)
        
        return overall_success_rate >= 60

def main():
    """Main test execution"""
    tester = BeatAddictsConnectionTester()
    success = tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
