#!/usr/bin/env python3
"""
Database Restoration Testing Suite
Tests database restoration and 8 new numbers addition (556 words total)
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('EXPO_PUBLIC_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

class DatabaseRestorationTester:
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
    
    def test_database_restoration_verification(self):
        """Test database restoration after clean backup and 8 new numbers addition"""
        print("\n🔍 === TESTING DATABASE RESTORATION VERIFICATION ===")
        print("CONTEXT: Database was corrupted with 2872 words (massive duplication)")
        print("SOLUTION: Restored from clean backup (548 words) + added 8 new numbers")
        print("EXPECTED: Exactly 556 words total (548 + 8)")
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
            
            # Test 2: Total word count verification (exactly 556)
            print("\n--- Test 2: Total Word Count Verification ---")
            total_count = len(words_data)
            expected_count = 556
            
            if total_count == expected_count:
                self.log_test("Total word count (556)", True, f"Exactly {expected_count} words found")
            else:
                self.log_test("Total word count (556)", False, f"Found {total_count} words, expected {expected_count}")
            
            # Test 3: No Pydantic errors (Field required shimaore)
            print("\n--- Test 3: Pydantic Structure Verification ---")
            pydantic_errors = []
            required_fields = ['french', 'shimaore', 'kibouchi', 'category']
            
            for i, word in enumerate(words_data):
                for field in required_fields:
                    if field not in word or word[field] is None:
                        pydantic_errors.append(f"Word {i+1} ({word.get('french', 'Unknown')}): Missing {field}")
            
            if not pydantic_errors:
                self.log_test("No Pydantic errors", True, "All words have required fields (french, shimaore, kibouchi, category)")
            else:
                error_summary = pydantic_errors[:3]  # Show first 3 errors
                if len(pydantic_errors) > 3:
                    error_summary.append(f"... and {len(pydantic_errors) - 3} more")
                self.log_test("No Pydantic errors", False, f"{len(pydantic_errors)} errors found: {'; '.join(error_summary)}")
            
            # Test 4: 8 new numbers verification
            print("\n--- Test 4: 8 New Numbers Verification ---")
            numbers = [word for word in words_data if word.get('category') == 'nombres']
            numbers_count = len(numbers)
            
            # Expected numbers (should include at least 1-20 plus potentially more)
            expected_basic_numbers = [
                "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", 
                "neuf", "dix", "onze", "douze", "treize", "quatorze", "quinze", 
                "seize", "dix-sept", "dix-huit", "dix-neuf", "vingt"
            ]
            
            found_numbers = [num['french'].lower() for num in numbers]
            missing_numbers = [num for num in expected_basic_numbers if num not in found_numbers]
            
            if numbers_count >= 20 and not missing_numbers:
                self.log_test("8 new numbers accessible", True, f"Found {numbers_count} numbers including all expected 1-20")
            else:
                self.log_test("8 new numbers accessible", False, f"Only {numbers_count} numbers found, missing: {missing_numbers[:5]}")
            
            # Test 5: Main categories intact
            print("\n--- Test 5: Main Categories Verification ---")
            categories = {}
            for word in words_data:
                category = word.get('category', 'unknown')
                if category not in categories:
                    categories[category] = 0
                categories[category] += 1
            
            expected_categories = [
                'salutations', 'famille', 'couleurs', 'animaux', 'nombres', 
                'corps', 'grammaire', 'maison', 'nourriture', 'verbes'
            ]
            
            found_categories = list(categories.keys())
            missing_categories = [cat for cat in expected_categories if cat not in found_categories]
            
            if not missing_categories:
                category_summary = [f"{cat}: {categories.get(cat, 0)}" for cat in expected_categories]
                self.log_test("Main categories intact", True, f"All {len(expected_categories)} categories present - " + "; ".join(category_summary[:5]))
            else:
                self.log_test("Main categories intact", False, f"Missing categories: {missing_categories}")
            
            # Test 6: Data structure consistency
            print("\n--- Test 6: Data Structure Consistency ---")
            
            # Check for duplicates
            french_words = [word.get('french', '') for word in words_data]
            duplicates = []
            seen = set()
            
            for french_word in french_words:
                if french_word in seen and french_word not in duplicates:
                    duplicates.append(french_word)
                seen.add(french_word)
            
            if duplicates:
                self.log_test("No duplicates", False, f"Found {len(duplicates)} duplicates: {duplicates[:5]}")
            else:
                self.log_test("No duplicates", True, "No duplicate French words found")
            
            # Test 7: Numbers API access
            print("\n--- Test 7: Numbers API Access ---")
            try:
                numbers_response = self.session.get(f"{API_BASE}/words?category=nombres", timeout=10)
                if numbers_response.status_code == 200:
                    api_numbers = numbers_response.json()
                    if len(api_numbers) > 0:
                        self.log_test("Numbers API access", True, f"Retrieved {len(api_numbers)} numbers via category filter")
                        
                        # Test individual number access
                        if api_numbers and 'id' in api_numbers[0]:
                            test_id = api_numbers[0]['id']
                            detail_response = self.session.get(f"{API_BASE}/words/{test_id}", timeout=5)
                            if detail_response.status_code == 200:
                                self.log_test("Individual number access", True, f"Can access individual numbers by ID")
                            else:
                                self.log_test("Individual number access", False, f"Cannot access individual numbers: {detail_response.status_code}")
                    else:
                        self.log_test("Numbers API access", False, "No numbers returned from category filter")
                else:
                    self.log_test("Numbers API access", False, f"Category filter failed: {numbers_response.status_code}")
            except Exception as e:
                self.log_test("Numbers API access", False, f"Error: {str(e)}")
            
            # Summary
            print("\n" + "=" * 60)
            print("📊 DATABASE RESTORATION TEST SUMMARY")
            print("=" * 60)
            
            for result in self.test_results:
                print(result)
            
            print(f"\n🎯 OVERALL RESULT: {self.passed_tests}/{self.total_tests} tests passed")
            
            if self.passed_tests == self.total_tests:
                print("🎉 ALL TESTS PASSED - Database restoration successful!")
                print("✅ Database correctly restored to 556 words (548 + 8 new numbers)")
                print("✅ No Pydantic errors (Field required shimaore)")
                print("✅ All 8 new numbers accessible via API")
                print("✅ Main categories intact")
                print("✅ Data structure consistent")
                return True
            else:
                print(f"⚠️  {self.total_tests - self.passed_tests} tests failed - Issues need attention")
                return False
                
        except Exception as e:
            self.log_test("Database restoration test", False, f"Critical error: {str(e)}")
            return False

def main():
    """Main test execution for database restoration verification"""
    print("🔍 STARTING DATABASE RESTORATION TESTING")
    print("=" * 60)
    print("CONTEXT: Testing corrected database after restoration from clean backup")
    print("PROBLEM: Database was corrupted with 2872 words (massive duplication)")
    print("SOLUTION: Restored from clean backup (548 words) + added 8 new numbers")
    print("EXPECTED: Exactly 556 words total (548 + 8)")
    print("=" * 60)
    
    tester = DatabaseRestorationTester()
    success = tester.test_database_restoration_verification()
    
    if success:
        print("\n🎉 DATABASE RESTORATION VERIFICATION COMPLETED SUCCESSFULLY!")
        print("✅ All requirements from review request verified")
        print("✅ Database correctly restored to 556 words")
        print("✅ No Pydantic errors found")
        print("✅ All 8 new numbers accessible")
        print("✅ Main categories intact")
        print("✅ Data structure consistent")
        return True
    else:
        print("\n❌ DATABASE RESTORATION VERIFICATION FAILED!")
        print("⚠️  Issues found that need attention")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)