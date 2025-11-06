#!/usr/bin/env python3
"""
Backend Testing Script for Mayotte Language Learning API
Testing focus: Family section new words and corrections verification
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Configuration
BACKEND_URL = "https://langapp-debug.preview.emergentagent.com/api"

class FamilyWordsTestSuite:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test(self, test_name: str, passed: bool, details: str = ""):
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
        
        self.test_results.append(result)
        print(result)
        
    def test_api_connectivity(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{self.backend_url.replace('/api', '')}/", timeout=10)
            self.log_test("API Connectivity", response.status_code == 200, 
                         f"Status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            self.log_test("API Connectivity", False, f"Error: {str(e)}")
            return False
    
    def get_all_words(self) -> List[Dict]:
        """Get all words from API"""
        try:
            response = requests.get(f"{self.backend_url}/words", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting words: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error getting words: {str(e)}")
            return []
    
    def get_family_words(self) -> List[Dict]:
        """Get family category words from API"""
        try:
            response = requests.get(f"{self.backend_url}/words?category=famille", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting family words: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error getting family words: {str(e)}")
            return []
    
    def test_new_words_added(self):
        """Test that the 4 new family words have been added"""
        print("\n🔍 TESTING NEW WORDS ADDED:")
        
        family_words = self.get_family_words()
        if not family_words:
            self.log_test("Get Family Words", False, "Could not retrieve family words")
            return
        
        # Expected new words based on the review request
        expected_new_words = [
            {
                "french": "tante paternelle",
                "shimaore": "nguivavi", 
                "kibouchi": "angouvavi"
            },
            {
                "french": "petit garcon", 
                "shimaore": "mwana mtroubaba",
                "kibouchi": "zaza lalahi"
            },
            {
                "french": "jeune adulte",
                "shimaore": "chababi",
                "kibouchi": "chababai"
            },
            {
                "french": "frere/soeur",
                "shimaore": "moinagna",
                "kibouchi": ""  # pas de kibouchi selon la demande
            }
        ]
        
        # Create a lookup dictionary for family words
        family_lookup = {}
        for word in family_words:
            french_key = word.get('french', '').lower()
            family_lookup[french_key] = word
        
        # Test each expected new word
        for expected_word in expected_new_words:
            french_key = expected_word['french'].lower()
            
            if french_key in family_lookup:
                found_word = family_lookup[french_key]
                
                # Check shimaoré translation
                shimaore_match = found_word.get('shimaore', '').lower() == expected_word['shimaore'].lower()
                
                # Check kibouchi translation (handle empty case)
                if expected_word['kibouchi']:
                    kibouchi_match = found_word.get('kibouchi', '').lower() == expected_word['kibouchi'].lower()
                else:
                    # For "frere/soeur" which has no kibouchi translation
                    kibouchi_match = True
                
                if shimaore_match and kibouchi_match:
                    self.log_test(f"New word '{expected_word['french']}'", True, 
                                f"Shimaoré: {found_word.get('shimaore')}, Kibouchi: {found_word.get('kibouchi')}")
                else:
                    self.log_test(f"New word '{expected_word['french']}'", False, 
                                f"Translation mismatch - Expected Shimaoré: {expected_word['shimaore']}, Got: {found_word.get('shimaore')} | Expected Kibouchi: {expected_word['kibouchi']}, Got: {found_word.get('kibouchi')}")
            else:
                self.log_test(f"New word '{expected_word['french']}'", False, "Word not found in database")
    
    def test_tante_correction(self):
        """Test that 'Tante' has been corrected to 'tante maternelle'"""
        print("\n🔍 TESTING TANTE CORRECTION:")
        
        family_words = self.get_family_words()
        if not family_words:
            self.log_test("Get Family Words for Tante Test", False, "Could not retrieve family words")
            return
        
        # Check that simple "Tante" or "tante" no longer exists
        simple_tante_found = False
        tante_maternelle_found = False
        tante_maternelle_correct = False
        
        for word in family_words:
            french_word = word.get('french', '').lower()
            
            # Check for simple "tante"
            if french_word == "tante":
                simple_tante_found = True
                
            # Check for "tante maternelle"
            if french_word == "tante maternelle":
                tante_maternelle_found = True
                shimaore = word.get('shimaore', '').lower()
                if shimaore == "mama titi":
                    tante_maternelle_correct = True
        
        # Test results
        self.log_test("No simple 'Tante' word exists", not simple_tante_found, 
                     "Simple 'tante' found in database" if simple_tante_found else "No simple 'tante' found")
        
        self.log_test("'Tante maternelle' exists", tante_maternelle_found,
                     "Found 'tante maternelle'" if tante_maternelle_found else "Missing 'tante maternelle'")
        
        if tante_maternelle_found:
            self.log_test("'Tante maternelle' has correct translation", tante_maternelle_correct,
                         "Shimaoré: 'mama titi'" if tante_maternelle_correct else "Incorrect shimaoré translation")
    
    def test_family_section_integrity(self):
        """Test family section integrity - should have 32 words"""
        print("\n🔍 TESTING FAMILY SECTION INTEGRITY:")
        
        family_words = self.get_family_words()
        if not family_words:
            self.log_test("Get Family Words for Integrity Test", False, "Could not retrieve family words")
            return
        
        # Test word count
        word_count = len(family_words)
        self.log_test("Family category has 32 words", word_count == 32, 
                     f"Found {word_count} words (expected 32)")
        
        # Test data structure for each word
        required_fields = ['french', 'shimaore', 'kibouchi', 'category']
        structure_issues = []
        
        for i, word in enumerate(family_words):
            for field in required_fields:
                if field not in word or word[field] is None:
                    structure_issues.append(f"Word {i+1}: Missing {field}")
            
            # Check category is 'famille'
            if word.get('category') != 'famille':
                structure_issues.append(f"Word {i+1}: Wrong category '{word.get('category')}'")
        
        self.log_test("All words have required structure", len(structure_issues) == 0,
                     f"{len(structure_issues)} structure issues found" if structure_issues else "All words properly structured")
        
        if structure_issues and len(structure_issues) <= 5:  # Show first 5 issues
            for issue in structure_issues[:5]:
                print(f"  - {issue}")
    
    def test_api_functionality(self):
        """Test API functionality for searching specific words"""
        print("\n🔍 TESTING API FUNCTIONALITY:")
        
        # Test GET /api/words endpoint
        try:
            response = requests.get(f"{self.backend_url}/words", timeout=10)
            self.log_test("GET /api/words endpoint", response.status_code == 200,
                         f"Status: {response.status_code}")
            
            if response.status_code == 200:
                all_words = response.json()
                self.log_test("API returns valid JSON", isinstance(all_words, list),
                             f"Returned {type(all_words)} with {len(all_words) if isinstance(all_words, list) else 0} items")
        except Exception as e:
            self.log_test("GET /api/words endpoint", False, f"Error: {str(e)}")
        
        # Test GET /api/words?category=famille endpoint
        try:
            response = requests.get(f"{self.backend_url}/words?category=famille", timeout=10)
            self.log_test("GET /api/words?category=famille endpoint", response.status_code == 200,
                         f"Status: {response.status_code}")
            
            if response.status_code == 200:
                family_words = response.json()
                self.log_test("Family category filtering works", isinstance(family_words, list) and len(family_words) > 0,
                             f"Returned {len(family_words) if isinstance(family_words, list) else 0} family words")
        except Exception as e:
            self.log_test("GET /api/words?category=famille endpoint", False, f"Error: {str(e)}")
    
    def test_emoji_assignment(self):
        """Test that emojis are correctly assigned"""
        print("\n🔍 TESTING EMOJI ASSIGNMENT:")
        
        family_words = self.get_family_words()
        if not family_words:
            self.log_test("Get Family Words for Emoji Test", False, "Could not retrieve family words")
            return
        
        words_with_emojis = 0
        words_without_emojis = 0
        
        for word in family_words:
            has_emoji = False
            
            # Check for emoji in image_url field
            if word.get('image_url') and word['image_url'].strip():
                has_emoji = True
                words_with_emojis += 1
            else:
                words_without_emojis += 1
        
        emoji_coverage = (words_with_emojis / len(family_words)) * 100 if family_words else 0
        
        self.log_test("Words have emoji assignment", words_with_emojis > 0,
                     f"{words_with_emojis}/{len(family_words)} words have emojis ({emoji_coverage:.1f}% coverage)")
    
    def search_specific_new_words(self):
        """Search for specific new words to verify they exist"""
        print("\n🔍 SEARCHING FOR SPECIFIC NEW WORDS:")
        
        all_words = self.get_all_words()
        if not all_words:
            self.log_test("Get All Words for Search", False, "Could not retrieve words")
            return
        
        # Create search index
        word_index = {}
        for word in all_words:
            french_key = word.get('french', '').lower()
            word_index[french_key] = word
        
        # Search for specific new words
        search_terms = [
            "tante paternelle",
            "petit garcon", 
            "jeune adulte",
            "frere/soeur",
            "tante maternelle"
        ]
        
        for term in search_terms:
            if term.lower() in word_index:
                found_word = word_index[term.lower()]
                self.log_test(f"Search for '{term}'", True,
                             f"Found: {found_word.get('french')} - Shimaoré: {found_word.get('shimaore')}, Kibouchi: {found_word.get('kibouchi')}")
            else:
                self.log_test(f"Search for '{term}'", False, "Word not found in database")
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 STARTING FAMILY WORDS AND CORRECTIONS TESTING")
        print("=" * 60)
        
        # Test API connectivity first
        if not self.test_api_connectivity():
            print("❌ Cannot connect to API. Stopping tests.")
            return
        
        # Run all test suites
        self.test_new_words_added()
        self.test_tante_correction()
        self.test_family_section_integrity()
        self.test_api_functionality()
        self.test_emoji_assignment()
        self.search_specific_new_words()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 OVERALL RESULT: SUCCESS")
        else:
            print("❌ OVERALL RESULT: NEEDS ATTENTION")
        
        print("\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            print(f"  {result}")
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = FamilyWordsTestSuite()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)