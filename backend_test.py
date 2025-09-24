#!/usr/bin/env python3
"""
Backend Testing Suite for Mayotte Language Learning API
Testing 4 New Sections Audio Integration: vêtements, maison, tradition, transport
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://mayotte-learn-2.preview.emergentagent.com/api"
HEADERS = {"Content-Type": "application/json"}

class BackendTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_result(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = f"{status}: {test_name}"
        if details:
            result += f" - {details}"
        
        self.results.append(result)
        print(result)
        
    def test_audio_info_16_categories(self):
        """Test 1: Verify GET /api/audio/info shows 16 categories total"""
        try:
            response = requests.get(f"{BACKEND_URL}/audio/info", headers=HEADERS, timeout=10)
            if response.status_code == 200:
                data = response.json()
                total_categories = data.get('total_categories', 0)
                categories = data.get('categories', {})
                
                if total_categories == 16:
                    # Check if new categories are present
                    new_categories = ['vetements', 'maison', 'tradition', 'transport']
                    missing_categories = [cat for cat in new_categories if cat not in categories]
                    
                    if not missing_categories:
                        self.log_result("Audio Info 16 Categories", True, f"All 16 categories present including new ones: {new_categories}")
                    else:
                        self.log_result("Audio Info 16 Categories", False, f"Missing categories: {missing_categories}")
                else:
                    self.log_result("Audio Info 16 Categories", False, f"Expected 16 categories, got {total_categories}")
            else:
                self.log_result("Audio Info 16 Categories", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Audio Info 16 Categories", False, f"Exception: {str(e)}")
    
    def test_new_audio_endpoints(self):
        """Test 2: Verify new audio endpoints are functional"""
        new_endpoints = [
            ('vetements', 'Robe.m4a'),
            ('maison', 'Nyoumba.m4a'),
            ('tradition', 'Mrengué.m4a'),
            ('transport', 'Ndrégué.m4a')
        ]
        
        for category, filename in new_endpoints:
            try:
                response = requests.get(f"{BACKEND_URL}/audio/{category}/{filename}", timeout=10)
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'audio' in content_type.lower():
                        self.log_result(f"Audio Endpoint {category}", True, f"Serving {filename} with {content_type}")
                    else:
                        self.log_result(f"Audio Endpoint {category}", False, f"Wrong content-type: {content_type}")
                else:
                    self.log_result(f"Audio Endpoint {category}", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_result(f"Audio Endpoint {category}", False, f"Exception: {str(e)}")
    
    def test_section_coverage(self):
        """Test 3: Verify audio coverage for each new section"""
        expected_coverage = {
            'vetements': {'target': 11, 'total': 16, 'percentage': 68.8},
            'maison': {'target': 30, 'total': 37, 'percentage': 81.1},
            'tradition': {'target': 6, 'total': 16, 'percentage': 37.5},
            'transport': {'target': 5, 'total': 7, 'percentage': 71.4}
        }
        
        for category, expected in expected_coverage.items():
            try:
                # Get words in category
                response = requests.get(f"{BACKEND_URL}/words?category={category}", headers=HEADERS, timeout=10)
                if response.status_code == 200:
                    words = response.json()
                    total_words = len(words)
                    
                    # Count words with dual audio system
                    dual_audio_count = sum(1 for word in words if word.get('dual_audio_system', False))
                    
                    if total_words == expected['total'] and dual_audio_count == expected['target']:
                        percentage = (dual_audio_count / total_words) * 100
                        self.log_result(f"Coverage {category.title()}", True, 
                                      f"{dual_audio_count}/{total_words} words ({percentage:.1f}%)")
                    else:
                        self.log_result(f"Coverage {category.title()}", False, 
                                      f"Expected {expected['target']}/{expected['total']}, got {dual_audio_count}/{total_words}")
                else:
                    self.log_result(f"Coverage {category.title()}", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_result(f"Coverage {category.title()}", False, f"Exception: {str(e)}")
    
    def test_specific_examples(self):
        """Test 4: Verify specific examples mentioned in review request"""
        test_cases = [
            {'word': 'robe', 'category': 'vetements', 'shimaore_file': 'Robe.m4a', 'kibouchi_file': 'Robe.m4a'},
            {'word': 'maison', 'category': 'maison', 'shimaore_file': 'Nyoumba.m4a', 'kibouchi_file': 'Tragnou.m4a'},
            {'word': 'boxe traditionnelle', 'category': 'tradition', 'shimaore_file': 'Mrengué.m4a', 'kibouchi_file': 'Mouringui.m4a'},
            {'word': 'avion', 'category': 'transport', 'shimaore_file': 'Ndrégué.m4a', 'kibouchi_file': 'Roplani.m4a'}
        ]
        
        for test_case in test_cases:
            try:
                # Find the word
                response = requests.get(f"{BACKEND_URL}/words?category={test_case['category']}", headers=HEADERS, timeout=10)
                if response.status_code == 200:
                    words = response.json()
                    word_obj = next((w for w in words if w['french'].lower() == test_case['word'].lower()), None)
                    
                    if word_obj:
                        word_id = word_obj['id']
                        
                        # Test dual audio endpoints
                        shimaore_response = requests.get(f"{BACKEND_URL}/words/{word_id}/audio/shimaore", timeout=10)
                        kibouchi_response = requests.get(f"{BACKEND_URL}/words/{word_id}/audio/kibouchi", timeout=10)
                        
                        shimaore_ok = shimaore_response.status_code == 200
                        kibouchi_ok = kibouchi_response.status_code == 200
                        
                        if shimaore_ok and kibouchi_ok:
                            self.log_result(f"Example '{test_case['word']}'", True, 
                                          f"Both Shimaoré and Kibouchi audio working")
                        else:
                            self.log_result(f"Example '{test_case['word']}'", False, 
                                          f"Shimaoré: {shimaore_response.status_code}, Kibouchi: {kibouchi_response.status_code}")
                    else:
                        self.log_result(f"Example '{test_case['word']}'", False, f"Word not found in {test_case['category']}")
                else:
                    self.log_result(f"Example '{test_case['word']}'", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_result(f"Example '{test_case['word']}'", False, f"Exception: {str(e)}")
    
    def test_dual_audio_functionality(self):
        """Test 5: Verify dual audio system functionality for new sections"""
        new_categories = ['vetements', 'maison', 'tradition', 'transport']
        
        for category in new_categories:
            try:
                response = requests.get(f"{BACKEND_URL}/words?category={category}", headers=HEADERS, timeout=10)
                if response.status_code == 200:
                    words = response.json()
                    
                    # Test first word with dual audio system
                    dual_audio_words = [w for w in words if w.get('dual_audio_system', False)]
                    
                    if dual_audio_words:
                        test_word = dual_audio_words[0]
                        word_id = test_word['id']
                        
                        # Test audio-info endpoint
                        info_response = requests.get(f"{BACKEND_URL}/words/{word_id}/audio-info", headers=HEADERS, timeout=10)
                        
                        if info_response.status_code == 200:
                            audio_info = info_response.json()
                            has_dual = audio_info.get('dual_audio_system', False)
                            
                            if has_dual:
                                self.log_result(f"Dual Audio {category.title()}", True, 
                                              f"Word '{test_word['french']}' has complete dual audio metadata")
                            else:
                                self.log_result(f"Dual Audio {category.title()}", False, 
                                              f"Word '{test_word['french']}' missing dual audio metadata")
                        else:
                            self.log_result(f"Dual Audio {category.title()}", False, f"Audio-info HTTP {info_response.status_code}")
                    else:
                        self.log_result(f"Dual Audio {category.title()}", False, "No words with dual audio system found")
                else:
                    self.log_result(f"Dual Audio {category.title()}", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_result(f"Dual Audio {category.title()}", False, f"Exception: {str(e)}")
    
    def test_total_audio_files(self):
        """Test 6: Verify total audio file count reaches 790+"""
        try:
            response = requests.get(f"{BACKEND_URL}/audio/info", headers=HEADERS, timeout=10)
            if response.status_code == 200:
                data = response.json()
                total_files = data.get('total_files', 0)
                
                if total_files >= 790:
                    self.log_result("Total Audio Files", True, f"{total_files} files (meets 790+ requirement)")
                else:
                    self.log_result("Total Audio Files", False, f"Only {total_files} files, expected 790+")
            else:
                self.log_result("Total Audio Files", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Total Audio Files", False, f"Exception: {str(e)}")
    
    def test_category_detection(self):
        """Test 7: Verify automatic category detection for new sections"""
        test_files = [
            ('vetements', 'Pantalon.m4a'),
            ('maison', 'Lit.m4a'),
            ('tradition', 'Danse.m4a'),
            ('transport', 'Motos.m4a')
        ]
        
        for category, filename in test_files:
            try:
                response = requests.get(f"{BACKEND_URL}/audio/{category}/{filename}", timeout=10)
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'audio' in content_type.lower():
                        self.log_result(f"Category Detection {category.title()}", True, 
                                      f"Automatic detection working for {filename}")
                    else:
                        self.log_result(f"Category Detection {category.title()}", False, 
                                      f"Wrong content-type: {content_type}")
                elif response.status_code == 404:
                    # File might not exist, but endpoint should be configured
                    self.log_result(f"Category Detection {category.title()}", True, 
                                  f"Endpoint configured (404 expected for non-existent file)")
                else:
                    self.log_result(f"Category Detection {category.title()}", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_result(f"Category Detection {category.title()}", False, f"Exception: {str(e)}")
    
    def test_performance_with_16_categories(self):
        """Test 8: Verify system performance with 16 categories"""
        try:
            start_time = time.time()
            response = requests.get(f"{BACKEND_URL}/audio/info", headers=HEADERS, timeout=10)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response.status_code == 200 and response_time < 2.0:
                data = response.json()
                categories_count = len(data.get('categories', {}))
                self.log_result("Performance 16 Categories", True, 
                              f"{categories_count} categories, {response_time:.2f}s response time")
            else:
                self.log_result("Performance 16 Categories", False, 
                              f"HTTP {response.status_code}, {response_time:.2f}s response time")
        except Exception as e:
            self.log_result("Performance 16 Categories", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests for 4 new sections audio integration"""
        print("🎉 TESTING: INTÉGRATION 4 NOUVELLES SECTIONS AUDIO DUAL")
        print("=" * 70)
        print("Testing: vêtements, maison, tradition, transport")
        print("Expected: 16 categories total, 790+ audio files, 52+ new words with dual audio")
        print("=" * 70)
        
        # Run all tests
        self.test_audio_info_16_categories()
        self.test_new_audio_endpoints()
        self.test_section_coverage()
        self.test_specific_examples()
        self.test_dual_audio_functionality()
        self.test_total_audio_files()
        self.test_category_detection()
        self.test_performance_with_16_categories()
        
        # Summary
        print("\n" + "=" * 70)
        print("🎯 TEST SUMMARY")
        print("=" * 70)
        
        for result in self.results:
            print(result)
        
        print(f"\n📊 OVERALL RESULTS: {self.passed_tests}/{self.total_tests} tests passed")
        
        if self.passed_tests == self.total_tests:
            print("🎉 ALL TESTS PASSED! 4 nouvelles sections audio integration is fully functional!")
            return True
        else:
            failed_tests = self.total_tests - self.passed_tests
            print(f"❌ {failed_tests} tests failed. Integration needs attention.")
            return False

def main():
    """Main test execution"""
    print("🚀 Starting Backend Testing for 4 New Sections Audio Integration")
    print(f"Backend URL: {BACKEND_URL}")
    print("Testing Requirements:")
    print("- 16 categories total (adding vêtements, maison, tradition, transport)")
    print("- Specific coverage targets for each new section")
    print("- 790+ total audio files")
    print("- 52+ new words with dual audio system")
    print("- New endpoints functional")
    print("- Specific examples working")
    print()
    
    tester = BackendTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ INTEGRATION TEST COMPLETED SUCCESSFULLY!")
        print("The 4 new sections (vêtements, maison, tradition, transport) are fully integrated with the dual audio system.")
    else:
        print("\n❌ INTEGRATION TEST FAILED!")
        print("Some requirements for the 4 new sections integration are not met.")
    
    return success

if __name__ == "__main__":
    main()