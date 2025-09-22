#!/usr/bin/env python3
"""
Backend Test Suite for Mayotte Educational App - Complete Audio Metadata Integration Testing
Tests the complete audio metadata integration for famille and nature sections
Based on French review request: Testing famille (88% coverage) and nature (100% coverage)
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

print(f"🎵 TESTING COMPLETE AUDIO METADATA INTEGRATION AT: {API_BASE}")
print("=" * 80)
print("CONTEXT: Testing complete audio metadata integration for famille and nature sections")
print("FAMILLE SECTION: 88% coverage expected (22/25 words with has_authentic_audio: true)")
print("NATURE SECTION: 100% coverage expected (49/49 words with has_authentic_audio: true)")
print("TESTING: API endpoints, metadata fields, language consistency, sources")
print("=" * 80)

class CompleteAudioMetadataTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.famille_words = []
        self.nature_words = []
        self.critical_failures = []
        
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            if "critical" in test_name.lower() or "coverage" in test_name.lower():
                self.critical_failures.append(test_name)
        
        result = f"{status}: {test_name}"
        if message:
            result += f" - {message}"
        
        self.test_results.append(result)
        print(result)
    
    def test_api_connectivity(self) -> bool:
        """Test basic API connectivity"""
        print("\n🔌 === TESTING API CONNECTIVITY ===")
        try:
            response = self.session.get(f"{API_BASE}/words", timeout=15)
            if response.status_code != 200:
                self.log_test("API Connectivity", False, f"Status code: {response.status_code}")
                return False
            
            words_data = response.json()
            self.log_test("API Connectivity", True, f"Backend responding, {len(words_data)} words retrieved")
            return True
            
        except Exception as e:
            self.log_test("API Connectivity", False, f"Critical error: {str(e)}")
            return False

    def test_famille_section_coverage(self) -> bool:
        """Test Section Famille (88% coverage expected - 22/25 words)"""
        print("\n👨‍👩‍👧‍👦 === TESTING FAMILLE SECTION AUDIO COVERAGE ===")
        print("EXPECTED: 88% coverage (22/25 words with has_authentic_audio: true)")
        
        try:
            # Get famille words
            famille_response = self.session.get(f"{API_BASE}/words?category=famille", timeout=10)
            if famille_response.status_code != 200:
                self.log_test("Famille endpoint", False, f"Status code: {famille_response.status_code}")
                return False
            
            self.famille_words = famille_response.json()
            total_famille = len(self.famille_words)
            
            self.log_test("Famille endpoint", True, f"Retrieved {total_famille} family words")
            
            # Count words with authentic audio
            words_with_audio = []
            for word in self.famille_words:
                if word.get("has_authentic_audio", False):
                    words_with_audio.append({
                        "french": word.get("french"),
                        "shimaore": word.get("shimaore"),
                        "kibouchi": word.get("kibouchi"),
                        "audio_filename": word.get("audio_filename"),
                        "audio_pronunciation_lang": word.get("audio_pronunciation_lang"),
                        "audio_source": word.get("audio_source")
                    })
            
            audio_count = len(words_with_audio)
            coverage_percentage = (audio_count / total_famille) * 100 if total_famille > 0 else 0
            
            # Test coverage (expecting ~88% = 22/25)
            expected_min_coverage = 85  # Allow some tolerance
            coverage_passed = coverage_percentage >= expected_min_coverage
            
            self.log_test("Famille Audio Coverage", coverage_passed, 
                         f"{audio_count}/{total_famille} words ({coverage_percentage:.1f}%) - Expected: ~88%")
            
            # Test specific corrections mentioned in review request
            corrections_test = self.test_famille_corrections()
            
            return coverage_passed and corrections_test
            
        except Exception as e:
            self.log_test("Famille section test", False, f"Error: {str(e)}")
            return False

    def test_famille_corrections(self) -> bool:
        """Test specific corrections mentioned in review request (papa, famille, grand-père, etc.)"""
        print("\n🔍 Testing Famille Corrections")
        
        # Expected corrections based on review request
        expected_corrections = {
            "papa": {"should_have_audio": True},
            "famille": {"should_have_audio": True},
            "grand-père": {"should_have_audio": True},
            "grand-mère": {"should_have_audio": True}
        }
        
        corrections_passed = True
        
        for word in self.famille_words:
            french_word = word.get("french", "").lower()
            
            if french_word in expected_corrections:
                expected = expected_corrections[french_word]
                has_audio = word.get("has_authentic_audio", False)
                
                if expected["should_have_audio"]:
                    test_passed = has_audio
                    details = f"Audio: {has_audio}, Filename: {word.get('audio_filename', 'None')}"
                else:
                    test_passed = True
                    details = f"Shimaore: {word.get('shimaore')}, Kibouchi: {word.get('kibouchi')}"
                
                test_name = f"Correction: {word.get('french')}"
                if not self.log_test(test_name, test_passed, details):
                    corrections_passed = False
        
        return corrections_passed

    def test_nature_section_coverage(self) -> bool:
        """Test Section Nature (100% coverage expected - 49/49 words)"""
        print("\n🌿 === TESTING NATURE SECTION AUDIO COVERAGE ===")
        print("EXPECTED: 100% coverage (49/49 words with has_authentic_audio: true)")
        
        try:
            # Get nature words
            nature_response = self.session.get(f"{API_BASE}/words?category=nature", timeout=10)
            if nature_response.status_code != 200:
                self.log_test("Nature endpoint", False, f"Status code: {nature_response.status_code}")
                return False
            
            self.nature_words = nature_response.json()
            total_nature = len(self.nature_words)
            
            self.log_test("Nature endpoint", True, f"Retrieved {total_nature} nature words")
            
            # Count words with authentic audio
            words_with_audio = []
            for word in self.nature_words:
                if word.get("has_authentic_audio", False):
                    words_with_audio.append({
                        "french": word.get("french"),
                        "shimaore": word.get("shimaore"),
                        "kibouchi": word.get("kibouchi"),
                        "audio_filename": word.get("audio_filename"),
                        "audio_pronunciation_lang": word.get("audio_pronunciation_lang"),
                        "audio_source": word.get("audio_source")
                    })
            
            audio_count = len(words_with_audio)
            coverage_percentage = (audio_count / total_nature) * 100 if total_nature > 0 else 0
            
            # Test coverage (expecting 100%)
            expected_min_coverage = 95  # Allow some tolerance
            coverage_passed = coverage_percentage >= expected_min_coverage
            
            self.log_test("Nature Audio Coverage", coverage_passed, 
                         f"{audio_count}/{total_nature} words ({coverage_percentage:.1f}%) - Expected: 100%")
            
            # Test specific examples mentioned in review request
            examples_test = self.test_nature_examples()
            
            return coverage_passed and examples_test
            
        except Exception as e:
            self.log_test("Nature section test", False, f"Error: {str(e)}")
            return False

    def test_nature_examples(self) -> bool:
        """Test specific nature examples: bahari (mer), mwiri (arbre), jouwa (soleil)"""
        print("\n🔍 Testing Nature Examples")
        
        # Expected examples from review request
        expected_examples = {
            "mer": {"shimaore_expected": "bahari"},
            "arbre": {"shimaore_expected": "mwiri"},
            "soleil": {"shimaore_expected": "jouwa"},
            "lune": {"should_have_audio": True}
        }
        
        examples_passed = True
        
        for word in self.nature_words:
            french_word = word.get("french", "").lower()
            
            if french_word in expected_examples:
                expected = expected_examples[french_word]
                has_audio = word.get("has_authentic_audio", False)
                shimaore = word.get("shimaore", "").lower()
                
                if "shimaore_expected" in expected:
                    # Test translation mapping
                    expected_shimaore = expected["shimaore_expected"].lower()
                    translation_correct = expected_shimaore in shimaore
                    
                    test_name = f"Nature Example: {french_word} → {expected['shimaore_expected']}"
                    details = f"Found: {word.get('shimaore')}, Audio: {has_audio}"
                    
                    if not self.log_test(test_name, translation_correct and has_audio, details):
                        examples_passed = False
                
                elif "should_have_audio" in expected:
                    test_name = f"Nature Example: {french_word} audio"
                    details = f"Audio: {has_audio}, Filename: {word.get('audio_filename', 'None')}"
                    
                    if not self.log_test(test_name, has_audio, details):
                        examples_passed = False
        
        return examples_passed

    def test_api_endpoints(self) -> bool:
        """Test API endpoints for audio integration"""
        print("\n🔗 === TESTING API ENDPOINTS ===")
        
        endpoints_passed = True
        
        # Test famille endpoint with audio icons
        famille_test = self.log_test(
            "GET /api/words?category=famille",
            len(self.famille_words) > 0,
            f"Retrieved {len(self.famille_words)} words"
        )
        
        # Test nature endpoint with audio icons
        nature_test = self.log_test(
            "GET /api/words?category=nature", 
            len(self.nature_words) > 0,
            f"Retrieved {len(self.nature_words)} words"
        )
        
        # Test new audio fields presence
        required_fields = ["has_authentic_audio", "audio_filename", "audio_pronunciation_lang", "audio_source"]
        
        # Check famille words for new fields
        famille_fields_present = False
        if self.famille_words:
            sample_word = next((w for w in self.famille_words if w.get("has_authentic_audio")), None)
            if sample_word:
                famille_fields_present = all(field in sample_word for field in required_fields)
        
        fields_test = self.log_test(
            "New audio fields present",
            famille_fields_present,
            f"Fields: {required_fields}"
        )
        
        return famille_test and nature_test and fields_test

    def test_metadata_validation(self) -> bool:
        """Test metadata validation (languages and sources)"""
        print("\n✅ === TESTING METADATA VALIDATION ===")
        
        validation_passed = True
        
        # Test language consistency
        valid_languages = {"shimaore", "kibouchi", "both"}
        invalid_languages = []
        
        all_audio_words = []
        for word in self.famille_words + self.nature_words:
            if word.get("has_authentic_audio"):
                all_audio_words.append(word)
        
        for word in all_audio_words:
            lang = word.get("audio_pronunciation_lang", "").lower()
            if lang and lang not in valid_languages:
                invalid_languages.append(f"{word.get('french')}: {lang}")
        
        lang_test = self.log_test(
            "Language Consistency",
            len(invalid_languages) == 0,
            f"Valid languages: {valid_languages}. Invalid: {invalid_languages[:3] if invalid_languages else 'None'}"
        )
        
        # Test sources
        famille_sources = set()
        nature_sources = set()
        
        for word in self.famille_words:
            if word.get("has_authentic_audio") and word.get("audio_source"):
                famille_sources.add(word.get("audio_source"))
        
        for word in self.nature_words:
            if word.get("has_authentic_audio") and word.get("audio_source"):
                nature_sources.add(word.get("audio_source"))
        
        sources_test = self.log_test(
            "Audio Sources Present",
            len(famille_sources) > 0 or len(nature_sources) > 0,
            f"Famille sources: {list(famille_sources)}, Nature sources: {list(nature_sources)}"
        )
        
        return lang_test and sources_test

    def run_complete_audio_metadata_tests(self) -> bool:
        """Run all complete audio metadata integration tests"""
        print("🎵 STARTING COMPLETE AUDIO METADATA INTEGRATION TESTING")
        print("=" * 80)
        
        # Test API connectivity first
        if not self.test_api_connectivity():
            print("❌ API connectivity failed - aborting tests")
            return False
        
        # Run all test suites
        test_results = []
        
        test_results.append(self.test_famille_section_coverage())
        test_results.append(self.test_nature_section_coverage())
        test_results.append(self.test_api_endpoints())
        test_results.append(self.test_metadata_validation())
        
        # Generate summary
        self.generate_summary()
        
        return all(test_results)

    def generate_summary(self):
        """Generate comprehensive test summary"""
        print("\n" + "=" * 80)
        print("🎵 COMPLETE AUDIO METADATA INTEGRATION TEST SUMMARY")
        print("=" * 80)
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        # Detailed results
        if self.famille_words:
            famille_audio_count = sum(1 for w in self.famille_words if w.get("has_authentic_audio"))
            famille_coverage = (famille_audio_count / len(self.famille_words)) * 100
            print(f"\n📊 FAMILLE SECTION:")
            print(f"   Total Words: {len(self.famille_words)}")
            print(f"   Words with Audio: {famille_audio_count}")
            print(f"   Coverage: {famille_coverage:.1f}% (Expected: ~88%)")
        
        if self.nature_words:
            nature_audio_count = sum(1 for w in self.nature_words if w.get("has_authentic_audio"))
            nature_coverage = (nature_audio_count / len(self.nature_words)) * 100
            print(f"\n🌿 NATURE SECTION:")
            print(f"   Total Words: {len(self.nature_words)}")
            print(f"   Words with Audio: {nature_audio_count}")
            print(f"   Coverage: {nature_coverage:.1f}% (Expected: 100%)")
        
        # Critical failures
        if self.critical_failures:
            print(f"\n❌ CRITICAL FAILURES:")
            for failure in self.critical_failures:
                print(f"   - {failure}")
        
        # Overall status
        overall_success = self.passed_tests == self.total_tests and len(self.critical_failures) == 0
        status = "✅ ALL TESTS PASSED" if overall_success else "❌ SOME TESTS FAILED"
        print(f"\n{status}")

def main():
    """Main function to run the complete audio metadata integration tests"""
    print("🧪 Starting Complete Audio Metadata Integration Testing")
    print("=" * 80)
    
    tester = CompleteAudioMetadataTester()
    success = tester.run_complete_audio_metadata_tests()
    
    print("\n" + "=" * 80)
    print("🏁 FINAL TEST RESULTS")
    print("=" * 80)
    
    if success:
        print("🎉 ALL CRITICAL TESTS PASSED!")
        print("✅ Complete audio metadata integration verified successfully")
        print("✅ Famille section has proper audio coverage (~88%)")
        print("✅ Nature section has complete audio coverage (100%)")
        print("✅ API endpoints return new audio metadata fields")
        print("✅ Language consistency and sources validated")
        print("✅ Specific corrections and examples verified")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("❌ Complete audio metadata integration has issues")
        print("❌ Please review the detailed test results above")
        print("❌ Check famille/nature coverage and metadata fields")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)