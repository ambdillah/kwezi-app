#!/usr/bin/env python3
"""
Backend Testing Suite for Mayotte Language Learning API
Focus: "Construire des phrases" game bug fix verification

This test suite specifically addresses the user's reported issue:
- Game was showing only sentences with verb "abimer" 
- Lack of variety in sentence construction
- Need to verify random mixing and increased default limit

Test Requirements from Review Request:
1. Variété des verbes: Different verbs in sentences (not just "abimer")
2. Mélange aléatoire: Order changes between calls
3. Limite par défaut: 20 sentences by default (not 10)
4. Filtrage par difficulté: difficulty=1, difficulty=2 work with mixing
5. Filtrage par temps: tense filters work (present/past/future)
6. Structure des phrases: All required fields present
7. Nombre total: 675 sentences total in database
8. Performance: Mixing doesn't affect performance significantly
"""

import requests
import json
import time
from typing import List, Dict, Any
import os
import sys
from collections import Counter

# Get backend URL from environment
BACKEND_URL = os.getenv('EXPO_PUBLIC_BACKEND_URL', 'https://mayotte-learn-2.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class SentenceGameTester:
    def __init__(self):
        self.api_base = API_BASE
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
            response = requests.get(f"{self.api_base}/../", timeout=10)
            self.log_test("API Connectivity", response.status_code == 200, 
                         f"Status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            self.log_test("API Connectivity", False, f"Error: {str(e)}")
            return False
    
    def test_sentences_endpoint_basic(self):
        """Test basic sentences endpoint functionality"""
        try:
            response = requests.get(f"{self.api_base}/sentences", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Sentences Endpoint Basic", False, 
                             f"Status: {response.status_code}")
                return False
            
            sentences = response.json()
            
            # Check if we get sentences (not empty array)
            if not sentences or len(sentences) == 0:
                self.log_test("Sentences Endpoint Basic", False, 
                             "Empty sentences array returned")
                return False
            
            self.log_test("Sentences Endpoint Basic", True, 
                         f"Returned {len(sentences)} sentences")
            return True
            
        except Exception as e:
            self.log_test("Sentences Endpoint Basic", False, f"Error: {str(e)}")
            return False
    
    def test_default_limit_20_sentences(self):
        """Test that default limit is 20 sentences (not 10)"""
        try:
            response = requests.get(f"{self.api_base}/sentences", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Default Limit 20 Sentences", False, 
                             f"Status: {response.status_code}")
                return False
            
            sentences = response.json()
            
            # Check if default returns 20 sentences
            expected_default = 20
            actual_count = len(sentences)
            
            passed = actual_count == expected_default
            self.log_test("Default Limit 20 Sentences", passed, 
                         f"Expected: {expected_default}, Got: {actual_count}")
            return passed
            
        except Exception as e:
            self.log_test("Default Limit 20 Sentences", False, f"Error: {str(e)}")
            return False
    
    def test_sentence_structure_complete(self):
        """Test that sentences have all required fields"""
        try:
            response = requests.get(f"{self.api_base}/sentences?limit=5", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Sentence Structure Complete", False, 
                             f"Status: {response.status_code}")
                return False
            
            sentences = response.json()
            
            if not sentences:
                self.log_test("Sentence Structure Complete", False, "No sentences returned")
                return False
            
            required_fields = [
                'french', 'shimaore', 'kibouchi', 'tense', 'difficulty',
                'shimaore_words', 'kibouchi_words'
            ]
            
            missing_fields = []
            for i, sentence in enumerate(sentences):
                for field in required_fields:
                    if field not in sentence:
                        missing_fields.append(f"Sentence {i+1}: missing '{field}'")
            
            if missing_fields:
                self.log_test("Sentence Structure Complete", False, 
                             f"Missing fields: {', '.join(missing_fields[:3])}")
                return False
            
            self.log_test("Sentence Structure Complete", True, 
                         f"All {len(required_fields)} required fields present in {len(sentences)} sentences")
            return True
            
        except Exception as e:
            self.log_test("Sentence Structure Complete", False, f"Error: {str(e)}")
            return False
    
    def test_verb_variety_not_just_abimer(self):
        """Test that sentences contain different verbs, not just 'abimer'"""
        try:
            response = requests.get(f"{self.api_base}/sentences?limit=50", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Verb Variety (Not Just Abimer)", False, 
                             f"Status: {response.status_code}")
                return False
            
            sentences = response.json()
            
            if not sentences:
                self.log_test("Verb Variety (Not Just Abimer)", False, "No sentences returned")
                return False
            
            # Extract verbs from French sentences
            verbs_found = set()
            abimer_count = 0
            
            for sentence in sentences:
                french_text = sentence.get('french', '').lower()
                
                # Count "abimer" occurrences
                if 'abîmer' in french_text or 'abimer' in french_text:
                    abimer_count += 1
                
                # Extract potential verbs (simple approach - look for common verb patterns)
                words = french_text.split()
                for word in words:
                    # Remove punctuation and check if it's likely a verb
                    clean_word = word.strip('.,!?;:').lower()
                    if len(clean_word) > 3:  # Basic filter for verb-like words
                        verbs_found.add(clean_word)
            
            # Check variety
            total_sentences = len(sentences)
            unique_verbs = len(verbs_found)
            abimer_percentage = (abimer_count / total_sentences) * 100 if total_sentences > 0 else 0
            
            # Pass if we have variety (not dominated by "abimer")
            variety_good = abimer_percentage < 50 and unique_verbs > 10
            
            self.log_test("Verb Variety (Not Just Abimer)", variety_good, 
                         f"Unique verbs: {unique_verbs}, Abimer: {abimer_count}/{total_sentences} ({abimer_percentage:.1f}%)")
            return variety_good
            
        except Exception as e:
            self.log_test("Verb Variety (Not Just Abimer)", False, f"Error: {str(e)}")
            return False
    
    def test_random_mixing_order_changes(self):
        """Test that sentence order changes between calls (random mixing)"""
        try:
            # Make first call
            response1 = requests.get(f"{self.api_base}/sentences?limit=10", timeout=10)
            if response1.status_code != 200:
                self.log_test("Random Mixing Order Changes", False, 
                             f"First call status: {response1.status_code}")
                return False
            
            sentences1 = response1.json()
            
            # Wait a moment and make second call
            time.sleep(0.5)
            response2 = requests.get(f"{self.api_base}/sentences?limit=10", timeout=10)
            if response2.status_code != 200:
                self.log_test("Random Mixing Order Changes", False, 
                             f"Second call status: {response2.status_code}")
                return False
            
            sentences2 = response2.json()
            
            if not sentences1 or not sentences2:
                self.log_test("Random Mixing Order Changes", False, "Empty responses")
                return False
            
            # Compare first few sentences to see if order changed
            first_sentences_1 = [s.get('french', '') for s in sentences1[:5]]
            first_sentences_2 = [s.get('french', '') for s in sentences2[:5]]
            
            # Check if order is different
            order_changed = first_sentences_1 != first_sentences_2
            
            self.log_test("Random Mixing Order Changes", order_changed, 
                         f"First call: {first_sentences_1[0][:30]}..., Second call: {first_sentences_2[0][:30]}...")
            return order_changed
            
        except Exception as e:
            self.log_test("Random Mixing Order Changes", False, f"Error: {str(e)}")
            return False
    
    def test_difficulty_filtering_with_mixing(self):
        """Test difficulty filtering works with random mixing"""
        try:
            # Test difficulty=1
            response1 = requests.get(f"{self.api_base}/sentences?difficulty=1&limit=10", timeout=10)
            if response1.status_code != 200:
                self.log_test("Difficulty Filtering (difficulty=1)", False, 
                             f"Status: {response1.status_code}")
                return False
            
            sentences1 = response1.json()
            
            # Check all sentences have difficulty=1
            difficulty1_correct = all(s.get('difficulty') == 1 for s in sentences1)
            
            # Test difficulty=2
            response2 = requests.get(f"{self.api_base}/sentences?difficulty=2&limit=10", timeout=10)
            if response2.status_code != 200:
                self.log_test("Difficulty Filtering (difficulty=2)", False, 
                             f"Status: {response2.status_code}")
                return False
            
            sentences2 = response2.json()
            
            # Check all sentences have difficulty=2
            difficulty2_correct = all(s.get('difficulty') == 2 for s in sentences2)
            
            both_passed = difficulty1_correct and difficulty2_correct
            
            self.log_test("Difficulty Filtering with Mixing", both_passed, 
                         f"Difficulty 1: {len(sentences1)} sentences, Difficulty 2: {len(sentences2)} sentences")
            return both_passed
            
        except Exception as e:
            self.log_test("Difficulty Filtering with Mixing", False, f"Error: {str(e)}")
            return False
    
    def test_tense_filtering_with_mixing(self):
        """Test tense filtering works with random mixing"""
        try:
            tenses = ['present', 'past', 'future']
            all_passed = True
            tense_counts = {}
            
            for tense in tenses:
                response = requests.get(f"{self.api_base}/sentences?tense={tense}&limit=5", timeout=10)
                
                if response.status_code != 200:
                    self.log_test(f"Tense Filtering ({tense})", False, 
                                 f"Status: {response.status_code}")
                    all_passed = False
                    continue
                
                sentences = response.json()
                
                # Check all sentences have correct tense
                tense_correct = all(s.get('tense') == tense for s in sentences)
                tense_counts[tense] = len(sentences)
                
                if not tense_correct:
                    all_passed = False
                
                self.log_test(f"Tense Filtering ({tense})", tense_correct, 
                             f"{len(sentences)} sentences")
            
            self.log_test("Tense Filtering with Mixing", all_passed, 
                         f"Present: {tense_counts.get('present', 0)}, Past: {tense_counts.get('past', 0)}, Future: {tense_counts.get('future', 0)}")
            return all_passed
            
        except Exception as e:
            self.log_test("Tense Filtering with Mixing", False, f"Error: {str(e)}")
            return False
    
    def test_total_sentences_count_675(self):
        """Test that total sentences in database is 675"""
        try:
            # Get all sentences with high limit
            response = requests.get(f"{self.api_base}/sentences?limit=1000", timeout=15)
            
            if response.status_code != 200:
                self.log_test("Total Sentences Count 675", False, 
                             f"Status: {response.status_code}")
                return False
            
            sentences = response.json()
            total_count = len(sentences)
            expected_count = 675
            
            passed = total_count == expected_count
            self.log_test("Total Sentences Count 675", passed, 
                         f"Expected: {expected_count}, Got: {total_count}")
            return passed
            
        except Exception as e:
            self.log_test("Total Sentences Count 675", False, f"Error: {str(e)}")
            return False
    
    def test_performance_with_mixing(self):
        """Test that random mixing doesn't significantly affect performance"""
        try:
            # Test multiple calls and measure time
            times = []
            
            for i in range(3):
                start_time = time.time()
                response = requests.get(f"{self.api_base}/sentences?limit=20", timeout=10)
                end_time = time.time()
                
                if response.status_code != 200:
                    self.log_test("Performance with Mixing", False, 
                                 f"Call {i+1} failed with status: {response.status_code}")
                    return False
                
                times.append(end_time - start_time)
            
            avg_time = sum(times) / len(times)
            max_time = max(times)
            
            # Performance is good if average < 2 seconds and max < 5 seconds
            performance_good = avg_time < 2.0 and max_time < 5.0
            
            self.log_test("Performance with Mixing", performance_good, 
                         f"Avg: {avg_time:.2f}s, Max: {max_time:.2f}s")
            return performance_good
            
        except Exception as e:
            self.log_test("Performance with Mixing", False, f"Error: {str(e)}")
            return False
    
    def test_combined_filtering(self):
        """Test combined difficulty and tense filtering"""
        try:
            response = requests.get(f"{self.api_base}/sentences?difficulty=1&tense=present&limit=5", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Combined Filtering", False, 
                             f"Status: {response.status_code}")
                return False
            
            sentences = response.json()
            
            if not sentences:
                self.log_test("Combined Filtering", False, "No sentences returned")
                return False
            
            # Check all sentences match both filters
            all_correct = all(
                s.get('difficulty') == 1 and s.get('tense') == 'present' 
                for s in sentences
            )
            
            self.log_test("Combined Filtering", all_correct, 
                         f"{len(sentences)} sentences with difficulty=1 and tense=present")
            return all_correct
            
        except Exception as e:
            self.log_test("Combined Filtering", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests for the Construire des phrases game"""
        print("🎮 STARTING CONSTRUIRE DES PHRASES GAME TESTING")
        print("=" * 60)
        print("Focus: Verifying bug fix for sentence variety and random mixing")
        print()
        
        # Run all tests
        tests = [
            self.test_api_connectivity,
            self.test_sentences_endpoint_basic,
            self.test_default_limit_20_sentences,
            self.test_sentence_structure_complete,
            self.test_verb_variety_not_just_abimer,
            self.test_random_mixing_order_changes,
            self.test_difficulty_filtering_with_mixing,
            self.test_tense_filtering_with_mixing,
            self.test_combined_filtering,
            self.test_total_sentences_count_675,
            self.test_performance_with_mixing
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log_test(test.__name__, False, f"Unexpected error: {str(e)}")
            print()  # Add spacing between tests
        
        # Print summary
        print("=" * 60)
        print("🎯 TEST SUMMARY")
        print("=" * 60)
        
        for result in self.test_results:
            print(result)
        
        print()
        print(f"📊 OVERALL RESULTS: {self.passed_tests}/{self.total_tests} tests passed")
        
        if self.passed_tests == self.total_tests:
            print("🎉 ALL TESTS PASSED! The 'Construire des phrases' game bug has been successfully fixed!")
            print("✅ Sentence variety issue resolved")
            print("✅ Random mixing implemented")
            print("✅ Default limit increased to 20")
            print("✅ All filtering functionality working")
        else:
            failed_count = self.total_tests - self.passed_tests
            print(f"❌ {failed_count} test(s) failed. The bug fix needs attention.")
        
        return self.passed_tests == self.total_tests

def main():
    """Main test execution"""
    print("Backend Testing Suite for Mayotte Language Learning API")
    print("Specific Focus: 'Construire des phrases' game bug fix verification")
    print()
    
    tester = SentenceGameTester()
    success = tester.run_all_tests()
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)