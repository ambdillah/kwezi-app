#!/usr/bin/env python3
"""
Backend Testing for Mayotte Language Learning API
Focus: NOURRITURE SECTION MAJOR UPDATE - 97.7% Audio Coverage Testing

This test specifically validates the major update to the "nourriture" section
that improved audio coverage from 65.9% (29/44) to 97.7% (43/44) with 14 new words integrated.
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Get backend URL from environment
BACKEND_URL = "https://mayotte-learn-2.preview.emergentagent.com/api"

class NourritureAudioTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.failed_tests = []
        
        # Expected 14 new words with their audio files from the review request
        self.new_words_with_audio = {
            "œuf": {"shimaoré": "Joiyi.m4a", "kibouchi": "Antoudi.m4a"},
            "poulet": {"shimaoré": "Bawa.m4a", "kibouchi": "Mabawa.m4a"},
            "nourriture": {"shimaoré": "Chaoula.m4a", "kibouchi": "Hanigni.m4a"},
            "oignon": {"shimaoré": "Chouroungou.m4a", "kibouchi": "Doungoulou.m4a"},
            "orange": {"shimaoré": "Troundra.m4a", "kibouchi": "Tsoha.m4a"},
            "pois d'angole": {"shimaoré": "Tsouzi.m4a", "kibouchi": "Ambatri.m4a"},
            "poivre": {"shimaoré": "Bvilibvili manga.m4a", "kibouchi": "Vilivili.m4a"},
            "riz non décortiqué": {"shimaoré": "Mélé.m4a", "kibouchi": "Vari tsivoidissa.m4a"},
            "sel": {"shimaoré": "Chingo.m4a", "kibouchi": "Sira.m4a"},
            "tamarin": {"shimaoré": "Ouhajou.m4a", "kibouchi": "Madirou kakazou.m4a"},
            "taro": {"shimaoré": "Majimbi.m4a", "kibouchi": "Majimbi.m4a"},
            "un thé": {"shimaoré": "Maji ya moro.m4a", "kibouchi": "Ranou meyi.m4a"},
            "vanille": {"shimaoré": "Lavani.m4a", "kibouchi": "Lavani.m4a"},
            "noix de coco fraîche": {"shimaoré": "Chijavou.m4a", "kibouchi": "Kidjavou.m4a"}
        }

    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        
        if not success:
            self.failed_tests.append(test_name)

    def test_nourriture_category_words(self):
        """Test 1: Verify nourriture category has 44 words total"""
        try:
            response = requests.get(f"{self.backend_url}/words?category=nourriture", timeout=10)
            if response.status_code == 200:
                words = response.json()
                word_count = len(words)
                
                if word_count == 44:
                    self.log_test("Nourriture Category Word Count", True, f"Found {word_count}/44 words as expected")
                else:
                    self.log_test("Nourriture Category Word Count", False, f"Found {word_count}/44 words, expected exactly 44")
                
                return words
            else:
                self.log_test("Nourriture Category Word Count", False, f"API returned status {response.status_code}")
                return []
        except Exception as e:
            self.log_test("Nourriture Category Word Count", False, f"Exception: {str(e)}")
            return []

    def test_dual_audio_coverage(self, words: List[Dict]):
        """Test 2: Verify 43/44 words have dual_audio_system: true (97.7% coverage)"""
        if not words:
            self.log_test("Dual Audio Coverage 97.7%", False, "No words provided for testing")
            return
        
        words_with_dual_audio = 0
        words_without_audio = []
        
        for word in words:
            if word.get('dual_audio_system', False):
                words_with_dual_audio += 1
            else:
                words_without_audio.append(word.get('french', 'Unknown'))
        
        coverage_percentage = (words_with_dual_audio / len(words)) * 100
        
        if words_with_dual_audio == 43 and len(words) == 44:
            self.log_test("Dual Audio Coverage 97.7%", True, 
                         f"Found {words_with_dual_audio}/44 words with dual audio ({coverage_percentage:.1f}% coverage)")
        else:
            self.log_test("Dual Audio Coverage 97.7%", False, 
                         f"Found {words_with_dual_audio}/44 words with dual audio ({coverage_percentage:.1f}% coverage). Words without audio: {words_without_audio}")

    def test_new_words_integration(self, words: List[Dict]):
        """Test 3: Verify all 14 new words are present with correct translations"""
        if not words:
            self.log_test("14 New Words Integration", False, "No words provided for testing")
            return
        
        word_dict = {word['french']: word for word in words}
        found_new_words = 0
        missing_words = []
        
        for french_word in self.new_words_with_audio.keys():
            if french_word in word_dict:
                found_new_words += 1
                word_data = word_dict[french_word]
                # Verify the word has dual audio system enabled
                if not word_data.get('dual_audio_system', False):
                    self.log_test(f"New Word Audio System - {french_word}", False, 
                                 "dual_audio_system not enabled")
            else:
                missing_words.append(french_word)
        
        if found_new_words == 14:
            self.log_test("14 New Words Integration", True, 
                         f"All 14 new words found and integrated: {list(self.new_words_with_audio.keys())}")
        else:
            self.log_test("14 New Words Integration", False, 
                         f"Found {found_new_words}/14 new words. Missing: {missing_words}")

    def test_dual_audio_endpoints(self, words: List[Dict]):
        """Test 4: Test dual audio endpoints for sample new words"""
        if not words:
            self.log_test("Dual Audio Endpoints", False, "No words provided for testing")
            return
        
        word_dict = {word['french']: word for word in words}
        test_words = ["œuf", "poulet", "nourriture", "sel"]  # Sample from new words
        successful_tests = 0
        
        for french_word in test_words:
            if french_word in word_dict:
                word_data = word_dict[french_word]
                word_id = word_data.get('id')
                
                if word_id:
                    # Test Shimaoré audio endpoint
                    try:
                        shimaore_response = requests.get(f"{self.backend_url}/words/{word_id}/audio/shimaore", timeout=10)
                        kibouchi_response = requests.get(f"{self.backend_url}/words/{word_id}/audio/kibouchi", timeout=10)
                        
                        if shimaore_response.status_code == 200 and kibouchi_response.status_code == 200:
                            successful_tests += 1
                            self.log_test(f"Dual Audio Endpoints - {french_word}", True, 
                                         "Both Shimaoré and Kibouchi audio endpoints working")
                        else:
                            self.log_test(f"Dual Audio Endpoints - {french_word}", False, 
                                         f"Shimaoré: {shimaore_response.status_code}, Kibouchi: {kibouchi_response.status_code}")
                    except Exception as e:
                        self.log_test(f"Dual Audio Endpoints - {french_word}", False, f"Exception: {str(e)}")
        
        if successful_tests == len(test_words):
            self.log_test("Dual Audio Endpoints Overall", True, f"All {successful_tests} test words working")
        else:
            self.log_test("Dual Audio Endpoints Overall", False, f"Only {successful_tests}/{len(test_words)} test words working")

    def test_nourriture_audio_endpoint(self):
        """Test 5: Test GET /api/audio/nourriture/{filename} endpoint"""
        test_files = ["Joiyi.m4a", "Bawa.m4a", "Chaoula.m4a", "Chingo.m4a"]  # Sample from new files
        successful_tests = 0
        
        for filename in test_files:
            try:
                response = requests.get(f"{self.backend_url}/audio/nourriture/{filename}", timeout=10)
                if response.status_code == 200:
                    successful_tests += 1
                    self.log_test(f"Nourriture Audio Endpoint - {filename}", True, "File accessible")
                else:
                    self.log_test(f"Nourriture Audio Endpoint - {filename}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Nourriture Audio Endpoint - {filename}", False, f"Exception: {str(e)}")
        
        if successful_tests == len(test_files):
            self.log_test("Nourriture Audio Endpoint Overall", True, f"All {successful_tests} test files accessible")
        else:
            self.log_test("Nourriture Audio Endpoint Overall", False, f"Only {successful_tests}/{len(test_files)} test files accessible")

    def test_audio_info_endpoint(self):
        """Test 6: Verify GET /api/audio/info shows 83 files for nourriture"""
        try:
            response = requests.get(f"{self.backend_url}/audio/info", timeout=10)
            if response.status_code == 200:
                audio_info = response.json()
                
                if 'nourriture' in audio_info:
                    nourriture_info = audio_info['nourriture']
                    file_count = nourriture_info.get('file_count', 0)
                    
                    if file_count == 83:
                        self.log_test("Audio Info - 83 Files", True, f"Found {file_count} nourriture audio files as expected")
                    else:
                        self.log_test("Audio Info - 83 Files", False, f"Found {file_count} files, expected 83")
                else:
                    self.log_test("Audio Info - 83 Files", False, "Nourriture section not found in audio info")
            else:
                self.log_test("Audio Info - 83 Files", False, f"API returned status {response.status_code}")
        except Exception as e:
            self.log_test("Audio Info - 83 Files", False, f"Exception: {str(e)}")

    def test_audio_metadata_consistency(self, words: List[Dict]):
        """Test 7: Verify audio metadata consistency for words with dual audio"""
        if not words:
            self.log_test("Audio Metadata Consistency", False, "No words provided for testing")
            return
        
        consistent_words = 0
        inconsistent_words = []
        
        for word in words:
            if word.get('dual_audio_system', False):
                # Check if metadata fields are consistent
                shimoare_has_audio = word.get('shimoare_has_audio', False)
                kibouchi_has_audio = word.get('kibouchi_has_audio', False)
                shimoare_filename = word.get('shimoare_audio_filename')
                kibouchi_filename = word.get('kibouchi_audio_filename')
                
                # Both should have audio if dual_audio_system is true
                if shimoare_has_audio and kibouchi_has_audio and shimoare_filename and kibouchi_filename:
                    consistent_words += 1
                else:
                    inconsistent_words.append({
                        'french': word.get('french', 'Unknown'),
                        'shimoare_has_audio': shimoare_has_audio,
                        'kibouchi_has_audio': kibouchi_has_audio,
                        'shimoare_filename': shimoare_filename,
                        'kibouchi_filename': kibouchi_filename
                    })
        
        total_dual_audio_words = len([w for w in words if w.get('dual_audio_system', False)])
        
        if consistent_words == total_dual_audio_words:
            self.log_test("Audio Metadata Consistency", True, 
                         f"All {consistent_words} dual audio words have consistent metadata")
        else:
            self.log_test("Audio Metadata Consistency", False, 
                         f"Only {consistent_words}/{total_dual_audio_words} words have consistent metadata. Inconsistent: {inconsistent_words[:3]}")

    def test_specific_new_word_mappings(self, words: List[Dict]):
        """Test 8: Verify specific audio file mappings for key new words"""
        if not words:
            self.log_test("Specific Audio Mappings", False, "No words provided for testing")
            return
        
        word_dict = {word['french']: word for word in words}
        test_mappings = {
            "œuf": {"shimaoré": "Joiyi.m4a", "kibouchi": "Antoudi.m4a"},
            "poulet": {"shimaoré": "Bawa.m4a", "kibouchi": "Mabawa.m4a"},
            "sel": {"shimaoré": "Chingo.m4a", "kibouchi": "Sira.m4a"},
            "vanille": {"shimaoré": "Lavani.m4a", "kibouchi": "Lavani.m4a"}
        }
        
        correct_mappings = 0
        incorrect_mappings = []
        
        for french_word, expected_files in test_mappings.items():
            if french_word in word_dict:
                word_data = word_dict[french_word]
                shimoare_file = word_data.get('shimoare_audio_filename')
                kibouchi_file = word_data.get('kibouchi_audio_filename')
                
                if (shimoare_file == expected_files['shimaoré'] and 
                    kibouchi_file == expected_files['kibouchi']):
                    correct_mappings += 1
                else:
                    incorrect_mappings.append({
                        'word': french_word,
                        'expected_shimoare': expected_files['shimaoré'],
                        'actual_shimoare': shimoare_file,
                        'expected_kibouchi': expected_files['kibouchi'],
                        'actual_kibouchi': kibouchi_file
                    })
        
        if correct_mappings == len(test_mappings):
            self.log_test("Specific Audio Mappings", True, 
                         f"All {correct_mappings} test mappings are correct")
        else:
            self.log_test("Specific Audio Mappings", False, 
                         f"Only {correct_mappings}/{len(test_mappings)} mappings correct. Incorrect: {incorrect_mappings}")

    def run_all_tests(self):
        """Run all nourriture section audio update tests"""
        print("🍽️ STARTING NOURRITURE SECTION MAJOR UPDATE TESTING")
        print("=" * 80)
        print("Testing the major update that improved audio coverage from 65.9% to 97.7%")
        print("Expected: 43/44 words with dual audio system (14 new words integrated)")
        print("=" * 80)
        
        # Test 1: Get nourriture words
        words = self.test_nourriture_category_words()
        
        # Test 2: Verify 97.7% coverage
        self.test_dual_audio_coverage(words)
        
        # Test 3: Verify 14 new words integration
        self.test_new_words_integration(words)
        
        # Test 4: Test dual audio endpoints
        self.test_dual_audio_endpoints(words)
        
        # Test 5: Test nourriture audio endpoint
        self.test_nourriture_audio_endpoint()
        
        # Test 6: Test audio info endpoint
        self.test_audio_info_endpoint()
        
        # Test 7: Test metadata consistency
        self.test_audio_metadata_consistency(words)
        
        # Test 8: Test specific mappings
        self.test_specific_new_word_mappings(words)
        
        # Summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("🍽️ NOURRITURE SECTION MAJOR UPDATE TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t['success']])
        failed_tests = len(self.failed_tests)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\n❌ FAILED TESTS ({len(self.failed_tests)}):")
            for test in self.failed_tests:
                print(f"   - {test}")
        
        if failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! The nourriture section major update is working correctly!")
            print("✅ 97.7% audio coverage achieved (43/44 words)")
            print("✅ 14 new words successfully integrated")
            print("✅ Dual audio system functional")
            print("✅ All endpoints working correctly")
        else:
            print(f"\n⚠️  {failed_tests} TESTS FAILED - Issues need to be addressed")
        
        print("=" * 80)

def main():
    """Main test execution"""
    tester = NourritureAudioTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()