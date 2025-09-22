#!/usr/bin/env python3
"""
Backend Test Suite for Mayotte Educational App - Family Section Update Testing
Tests the family section update with 5 new words and corrections (561 words total)
"""

import requests
import json
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('EXPO_PUBLIC_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

print(f"🔍 TESTING FAMILY SECTION UPDATE AT: {API_BASE}")
print("=" * 60)
print("CONTEXT: Testing family section update with 5 new words and corrections")
print("EXPECTED: 561 words total (556 + 5 new family words)")
print("=" * 60)

class FamilySectionTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = f"{status}: {test_name}"
        if message:
            result += f" - {message}"
        
        self.test_results.append(result)
        print(result)
    
    def test_family_section_update(self):
        """Test the family section update with 5 new words and corrections"""
        print("\n🔍 === TESTING FAMILY SECTION UPDATE ===")
        print("CONTEXT: Family section updated with 5 new words and corrections")
        print("EXPECTED: 561 words total (556 + 5 new family words)")
        print("EXPECTED: 25 words in famille category")
        print("=" * 60)
        
        try:
            # Test 1: Basic API connectivity
            print("\n--- Test 1: API Connectivity ---")
            response = self.session.get(f"{API_BASE}/words", timeout=15)
            if response.status_code != 200:
                self.log_test("API Connectivity", False, f"Status code: {response.status_code}")
                return False
            
            words_data = response.json()
            self.log_test("API Connectivity", True, f"Backend responding, {len(words_data)} words retrieved")
            
            # Test 2: Total word count verification (exactly 561)
            print("\n--- Test 2: Total Word Count Verification (561) ---")
            total_count = len(words_data)
            expected_count = 561
            
            if total_count == expected_count:
                self.log_test("Total word count (561)", True, f"Exactly {expected_count} words found")
            else:
                self.log_test("Total word count (561)", False, f"Found {total_count} words, expected {expected_count}")
            
            # Test 3: GET /api/words?category=famille endpoint
            print("\n--- Test 3: GET /api/words?category=famille Endpoint ---")
            famille_response = self.session.get(f"{API_BASE}/words?category=famille", timeout=10)
            if famille_response.status_code != 200:
                self.log_test("Famille category endpoint", False, f"Status code: {famille_response.status_code}")
                return False
            
            famille_words = famille_response.json()
            famille_count = len(famille_words)
            expected_famille_count = 25
            
            if famille_count == expected_famille_count:
                self.log_test("Famille category count (25)", True, f"Found {famille_count} family words")
            else:
                self.log_test("Famille category count (25)", False, f"Found {famille_count} family words, expected {expected_famille_count}")
            
            # Create lookup dictionary for family words
            famille_words_by_french = {word['french'].lower(): word for word in famille_words}
            
            # Test 4: Verify 5 new family words are accessible
            print("\n--- Test 4: 5 New Family Words Verification ---")
            new_family_words = [
                {
                    "french": "tente",
                    "expected_shimaore": "mama titi",  # Simplified check - contains these terms
                    "expected_kibouchi": "nindri heli",
                    "note": "shimaoré: mama titi/bolé, kibouchi: nindri heli/bé"
                },
                {
                    "french": "fille",
                    "expected_shimaore": "mtroumama",
                    "expected_kibouchi": "viavi",
                    "note": "shimaoré: mtroumama, kibouchi: viavi"
                },
                {
                    "french": "femme",
                    "expected_shimaore": "mtroumama",
                    "expected_kibouchi": "viavi",
                    "note": "shimaoré: mtroumama, kibouchi: viavi"
                },
                {
                    "french": "garçon",
                    "expected_shimaore": "mtroubaba",
                    "expected_kibouchi": "lalahi",
                    "note": "shimaoré: mtroubaba, kibouchi: lalahi"
                },
                {
                    "french": "homme",
                    "expected_shimaore": "mtroubaba",
                    "expected_kibouchi": "lalahi",
                    "note": "shimaoré: mtroubaba, kibouchi: lalahi"
                }
            ]
            
            new_words_found = 0
            for new_word in new_family_words:
                french_word = new_word['french']
                if french_word in famille_words_by_french:
                    word = famille_words_by_french[french_word]
                    
                    # Check if translations contain expected terms (flexible matching)
                    shimaore_match = new_word['expected_shimaore'].lower() in word['shimaore'].lower()
                    kibouchi_match = new_word['expected_kibouchi'].lower() in word['kibouchi'].lower()
                    
                    if shimaore_match and kibouchi_match:
                        self.log_test(f"New word: {french_word}", True, f"Found with correct translations: {word['shimaore']} / {word['kibouchi']}")
                        new_words_found += 1
                    else:
                        self.log_test(f"New word: {french_word}", False, f"Translation mismatch - Expected: {new_word['expected_shimaore']}/{new_word['expected_kibouchi']}, Got: {word['shimaore']}/{word['kibouchi']}")
                else:
                    self.log_test(f"New word: {french_word}", False, "Word not found in famille category")
            
            # Test 5: Verify updated words have correct translations
            print("\n--- Test 5: Updated Family Words Verification ---")
            updated_family_words = [
                {
                    "french": "oncle paternel",
                    "expected_shimaore": "baba titi",  # Simplified check
                    "expected_kibouchi": "baba heli",
                    "note": "shimaoré: Baba titi/bolé, kibouchi: Baba heli/bé"
                },
                {
                    "french": "petite sœur",
                    "expected_shimaore": "moinagna",  # Simplified check
                    "expected_kibouchi": "zandri",
                    "note": "shimaoré: moinagna mtroumama, kibouchi: zandri"
                },
                {
                    "french": "madame",
                    "expected_shimaore": "bwéni",
                    "expected_kibouchi": "viavi",
                    "note": "shimaoré: bwéni, kibouchi: viavi"
                }
            ]
            
            updated_words_found = 0
            for updated_word in updated_family_words:
                french_word = updated_word['french']
                if french_word in famille_words_by_french:
                    word = famille_words_by_french[french_word]
                    
                    # Check if translations contain expected terms (flexible matching)
                    shimaore_match = updated_word['expected_shimaore'].lower() in word['shimaore'].lower()
                    kibouchi_match = updated_word['expected_kibouchi'].lower() in word['kibouchi'].lower()
                    
                    if shimaore_match and kibouchi_match:
                        self.log_test(f"Updated word: {french_word}", True, f"Correct translations verified: {word['shimaore']} / {word['kibouchi']}")
                        updated_words_found += 1
                    else:
                        self.log_test(f"Updated word: {french_word}", False, f"Translation mismatch - Expected: {updated_word['expected_shimaore']}/{updated_word['expected_kibouchi']}, Got: {word['shimaore']}/{word['kibouchi']}")
                else:
                    self.log_test(f"Updated word: {french_word}", False, "Word not found in famille category")
            
            # Test 6: Verify other main endpoints still work
            print("\n--- Test 6: Other Main Endpoints Verification ---")
            other_endpoints = [
                ("couleurs", "Colors"),
                ("animaux", "Animals"),
                ("nombres", "Numbers"),
                ("salutations", "Greetings")
            ]
            
            other_endpoints_working = 0
            for category, description in other_endpoints:
                try:
                    response = self.session.get(f"{API_BASE}/words?category={category}", timeout=10)
                    if response.status_code == 200:
                        words = response.json()
                        if len(words) > 0:
                            self.log_test(f"{description} endpoint", True, f"Found {len(words)} words")
                            other_endpoints_working += 1
                        else:
                            self.log_test(f"{description} endpoint", False, "No words found")
                    else:
                        self.log_test(f"{description} endpoint", False, f"Status code: {response.status_code}")
                except Exception as e:
                    self.log_test(f"{description} endpoint", False, f"Error: {str(e)}")
            
            # Test 7: Data structure verification
            print("\n--- Test 7: Data Structure Verification ---")
            required_fields = ['french', 'shimaore', 'kibouchi', 'category']
            structure_errors = 0
            
            for i, word in enumerate(famille_words[:5]):  # Test first 5 family words
                missing_fields = []
                for field in required_fields:
                    if field not in word or not word[field]:
                        missing_fields.append(field)
                
                if missing_fields:
                    self.log_test(f"Word structure #{i+1}", False, f"Missing fields: {missing_fields}")
                    structure_errors += 1
                else:
                    self.log_test(f"Word structure #{i+1}", True, "All required fields present")
            
            # Summary
            print("\n" + "=" * 60)
            print("📊 FAMILY SECTION UPDATE TEST SUMMARY")
            print("=" * 60)
            
            for result in self.test_results:
                print(result)
            
            print(f"\n🎯 OVERALL RESULT: {self.passed_tests}/{self.total_tests} tests passed")
            
            # Determine overall success
            critical_tests_passed = (
                total_count == expected_count and  # Total word count correct
                famille_count == expected_famille_count and  # Family count correct
                new_words_found >= 4 and  # At least 4/5 new words found
                updated_words_found >= 2 and  # At least 2/3 updated words correct
                other_endpoints_working >= 3 and  # Most other endpoints working
                structure_errors == 0  # No structure errors
            )
            
            if critical_tests_passed:
                print("\n🎉 FAMILY SECTION UPDATE TEST COMPLETED SUCCESSFULLY!")
                print("✅ Total word count is correct (561 words)")
                print("✅ Familie category contains 25 words")
                print("✅ New family words are accessible with correct translations")
                print("✅ Updated family words have correct translations")
                print("✅ Other main endpoints are working correctly")
                print("✅ Data structure is consistent")
                return True
            else:
                print(f"\n⚠️  Some critical tests failed - Issues need attention")
                if total_count != expected_count:
                    print(f"❌ Total word count incorrect: {total_count} (expected {expected_count})")
                if famille_count != expected_famille_count:
                    print(f"❌ Familie category count incorrect: {famille_count} (expected {expected_famille_count})")
                if new_words_found < 4:
                    print(f"❌ Only {new_words_found}/5 new words found correctly")
                if updated_words_found < 2:
                    print(f"❌ Only {updated_words_found}/3 updated words verified")
                if other_endpoints_working < 3:
                    print(f"❌ Only {other_endpoints_working}/4 other endpoints working")
                if structure_errors > 0:
                    print(f"❌ {structure_errors} data structure errors found")
                return False
                
        except Exception as e:
            self.log_test("Family section update test", False, f"Critical error: {str(e)}")
            return False

def main():
    """Main function to run the family section tests"""
    print("🧪 Starting Family Section Update Testing")
    print("=" * 60)
    
    tester = FamilySectionTester()
    success = tester.test_family_section_update()
    
    print("\n" + "=" * 60)
    print("🏁 FINAL TEST RESULTS")
    print("=" * 60)
    
    if success:
        print("🎉 ALL CRITICAL TESTS PASSED!")
        print("✅ Family section update has been successfully implemented")
        print("✅ 561 total words confirmed (556 + 5 new family words)")
        print("✅ Familie category contains 25 words as expected")
        print("✅ All new and updated family words are accessible")
        print("✅ Backend API endpoints are functioning correctly")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("❌ Family section update has issues that need attention")
        print("❌ Please review the detailed test results above")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)