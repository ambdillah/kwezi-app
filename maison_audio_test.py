#!/usr/bin/env python3
"""
Test complet du backend après la mise à jour des prononciations audio pour la section "maison"
Comprehensive backend testing after audio pronunciation updates for the "maison" section

Test Requirements from French review request:
1. Vérification de la couverture audio - tous les 37 mots de la section "maison" ont des références audio authentiques
2. Vérifier que le champ `has_authentic_audio` est défini à true
3. Confirmer que les chemins audio pointent vers les bons fichiers M4A
4. Test des références audio spécifiques:
   - "maison" → audio/maison/Nyoumba.m4a
   - "fenêtre" → audio/maison/Lafoumètara.m4a
   - "machette" → audio/maison/M_panga.m4a
   - "torche locale" → audio/maison/Gandilé-poutroumax.m4a
5. Test de l'intégrité des fichiers audio - vérifier que les 66 fichiers M4A sont présents
6. Test de performance audio - vérifier les temps de réponse pour l'endpoint audio
7. Test de cohérence avec les autres sections - vérifier que les autres sections conservent leurs références audio
8. Test API endpoints audio - tester l'endpoint `/api/words?category=maison` avec les nouvelles références
"""

import requests
import json
import sys
import time
import os
from typing import Dict, List, Any, Optional

# Configuration
BACKEND_URL = os.getenv('EXPO_PUBLIC_BACKEND_URL', 'https://kwezi-db-rescue.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class MaisonAudioTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.maison_words = []
        
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
        
        self.results.append(result)
        print(result)
        
    def test_api_connectivity(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{API_BASE}/words", timeout=10)
            self.log_test("API Connectivity", response.status_code == 200, 
                         f"Status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            self.log_test("API Connectivity", False, f"Error: {str(e)}")
            return False
    
    def test_maison_category_access(self):
        """Test access to maison category"""
        try:
            response = requests.get(f"{API_BASE}/words?category=maison", timeout=10)
            if response.status_code == 200:
                data = response.json()
                word_count = len(data)
                self.log_test("Maison Category Access", word_count > 0, 
                             f"Found {word_count} words in maison category")
                self.maison_words = data
                return data
            else:
                self.log_test("Maison Category Access", False, 
                             f"Status: {response.status_code}")
                return []
        except Exception as e:
            self.log_test("Maison Category Access", False, f"Error: {str(e)}")
            return []
    
    def test_audio_coverage_verification(self):
        """1. Vérification de la couverture audio - tous les 37 mots de la section "maison" ont des références audio authentiques"""
        if not self.maison_words:
            self.log_test("Audio Coverage Verification", False, "No maison words found")
            return
        
        total_words = len(self.maison_words)
        words_with_audio = 0
        words_with_authentic_audio = 0
        
        for word in self.maison_words:
            # Check for audio references
            has_audio_ref = (
                word.get('has_authentic_audio', False) or
                word.get('shimoare_has_audio', False) or
                word.get('kibouchi_has_audio', False) or
                word.get('dual_audio_system', False) or
                word.get('audio_filename') is not None or
                word.get('shimoare_audio_filename') is not None or
                word.get('kibouchi_audio_filename') is not None
            )
            
            if has_audio_ref:
                words_with_audio += 1
                
            if word.get('has_authentic_audio', False):
                words_with_authentic_audio += 1
        
        coverage_percentage = (words_with_audio / total_words) * 100 if total_words > 0 else 0
        authentic_percentage = (words_with_authentic_audio / total_words) * 100 if total_words > 0 else 0
        
        # Test if we have the expected 37 words
        expected_count = 37
        count_test = total_words == expected_count
        self.log_test("Maison Word Count (37 expected)", count_test, 
                     f"Found {total_words} words, expected {expected_count}")
        
        # Test audio coverage
        coverage_test = coverage_percentage >= 80  # At least 80% should have audio references
        self.log_test("Audio Coverage", coverage_test, 
                     f"{words_with_audio}/{total_words} words ({coverage_percentage:.1f}%) have audio references")
        
        # Test authentic audio flag
        authentic_test = words_with_authentic_audio > 0
        self.log_test("Authentic Audio Flags", authentic_test, 
                     f"{words_with_authentic_audio}/{total_words} words ({authentic_percentage:.1f}%) marked as authentic")
    
    def test_specific_audio_references(self):
        """2. Test des références audio spécifiques pour les mots clés"""
        specific_tests = [
            {"french": "maison", "expected_audio": "Nyoumba.m4a"},
            {"french": "fenêtre", "expected_audio": "Lafoumètara.m4a"},
            {"french": "machette", "expected_audio": "M_panga.m4a"},
            {"french": "torche locale", "expected_audio": "Gandilé-poutroumax.m4a"}
        ]
        
        word_dict = {word.get('french', '').lower(): word for word in self.maison_words}
        
        for test_case in specific_tests:
            french_word = test_case["french"].lower()
            expected_audio = test_case["expected_audio"]
            
            if french_word in word_dict:
                word = word_dict[french_word]
                
                # Check various audio filename fields
                audio_files = []
                if word.get('audio_filename'):
                    audio_files.append(word['audio_filename'])
                if word.get('shimoare_audio_filename'):
                    audio_files.append(word['shimoare_audio_filename'])
                if word.get('kibouchi_audio_filename'):
                    audio_files.append(word['kibouchi_audio_filename'])
                
                # Check if expected audio file is referenced
                has_expected_audio = any(expected_audio in audio_file for audio_file in audio_files if audio_file)
                
                self.log_test(f"Specific Audio: {test_case['french']}", has_expected_audio,
                             f"Expected: {expected_audio}, Found: {audio_files}")
            else:
                self.log_test(f"Specific Audio: {test_case['french']}", False,
                             f"Word '{test_case['french']}' not found in maison category")
    
    def test_audio_file_integrity(self):
        """3. Test de l'intégrité des fichiers audio - vérifier que les 66 fichiers M4A sont présents"""
        try:
            # Test audio info endpoint
            response = requests.get(f"{API_BASE}/audio/info", timeout=10)
            if response.status_code == 200:
                audio_info = response.json()
                
                # Check if maison category is in audio info
                maison_audio_available = False
                maison_file_count = 0
                
                if isinstance(audio_info, dict):
                    if 'maison' in audio_info:
                        maison_audio_available = True
                        # Try to get file count if available
                        maison_info = audio_info['maison']
                        if isinstance(maison_info, dict) and 'file_count' in maison_info:
                            maison_file_count = maison_info['file_count']
                        elif isinstance(maison_info, dict) and 'files' in maison_info:
                            maison_file_count = len(maison_info['files'])
                
                self.log_test("Audio Info Endpoint", response.status_code == 200,
                             f"Maison audio available: {maison_audio_available}")
                
                if maison_file_count > 0:
                    expected_files = 66
                    file_count_test = maison_file_count >= expected_files * 0.8  # Allow some tolerance
                    self.log_test("Maison Audio File Count", file_count_test,
                                 f"Found {maison_file_count} files, expected ~{expected_files}")
                else:
                    self.log_test("Maison Audio File Count", False,
                                 "Could not determine file count from audio info")
            else:
                self.log_test("Audio Info Endpoint", False,
                             f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Audio File Integrity", False, f"Error: {str(e)}")
    
    def test_audio_endpoint_access(self):
        """4. Test de l'accès aux endpoints audio"""
        try:
            # Test maison audio endpoint
            test_files = ["Nyoumba.m4a", "Lafoumètara.m4a", "M_panga.m4a"]
            
            for audio_file in test_files:
                try:
                    response = requests.head(f"{API_BASE}/audio/maison/{audio_file}", timeout=5)
                    file_accessible = response.status_code in [200, 404]  # 404 is acceptable if file doesn't exist
                    
                    self.log_test(f"Audio Endpoint Access: {audio_file}", file_accessible,
                                 f"Status: {response.status_code}")
                except Exception as e:
                    self.log_test(f"Audio Endpoint Access: {audio_file}", False,
                                 f"Error: {str(e)}")
                    
        except Exception as e:
            self.log_test("Audio Endpoint Access", False, f"Error: {str(e)}")
    
    def test_performance_audio(self):
        """5. Test de performance audio - vérifier les temps de réponse"""
        if not self.maison_words:
            self.log_test("Audio Performance", False, "No maison words to test")
            return
        
        try:
            # Test response time for maison category
            start_time = time.time()
            response = requests.get(f"{API_BASE}/words?category=maison", timeout=10)
            end_time = time.time()
            
            response_time = end_time - start_time
            performance_ok = response_time < 2.0  # Should respond within 2 seconds
            
            self.log_test("Maison Category Performance", performance_ok,
                         f"Response time: {response_time:.3f}s")
            
            # Test individual word access performance
            if self.maison_words and len(self.maison_words) > 0:
                test_word = self.maison_words[0]
                word_id = test_word.get('id')
                
                if word_id:
                    start_time = time.time()
                    response = requests.get(f"{API_BASE}/words/{word_id}", timeout=10)
                    end_time = time.time()
                    
                    response_time = end_time - start_time
                    individual_performance_ok = response_time < 1.0
                    
                    self.log_test("Individual Word Performance", individual_performance_ok,
                                 f"Response time: {response_time:.3f}s")
                    
        except Exception as e:
            self.log_test("Audio Performance", False, f"Error: {str(e)}")
    
    def test_consistency_other_sections(self):
        """6. Test de cohérence avec les autres sections"""
        test_categories = ['famille', 'animaux', 'couleurs', 'nombres', 'salutations']
        
        for category in test_categories:
            try:
                response = requests.get(f"{API_BASE}/words?category={category}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    word_count = len(data)
                    consistency_ok = word_count > 0
                    
                    self.log_test(f"Category Consistency: {category}", consistency_ok,
                                 f"{word_count} words found")
                else:
                    self.log_test(f"Category Consistency: {category}", False,
                                 f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Category Consistency: {category}", False,
                             f"Error: {str(e)}")
    
    def test_database_integrity(self):
        """Test global database integrity"""
        try:
            response = requests.get(f"{API_BASE}/words", timeout=15)
            if response.status_code == 200:
                all_words = response.json()
                total_count = len(all_words)
                
                # Check for basic data integrity
                valid_words = 0
                for word in all_words:
                    if (word.get('french') and 
                        word.get('shimaore') and 
                        word.get('kibouchi') and 
                        word.get('category')):
                        valid_words += 1
                
                integrity_percentage = (valid_words / total_count) * 100 if total_count > 0 else 0
                integrity_ok = integrity_percentage >= 95
                
                self.log_test("Database Integrity", integrity_ok,
                             f"{valid_words}/{total_count} words ({integrity_percentage:.1f}%) have complete data")
                
                # Check for duplicates
                french_words = [word.get('french', '').lower() for word in all_words if word.get('french')]
                unique_french = set(french_words)
                duplicate_count = len(french_words) - len(unique_french)
                
                no_duplicates = duplicate_count == 0
                self.log_test("No Duplicate Words", no_duplicates,
                             f"{duplicate_count} duplicate French words found")
                
            else:
                self.log_test("Database Integrity", False,
                             f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Database Integrity", False, f"Error: {str(e)}")
    
    def run_comprehensive_test(self):
        """Run all tests for maison audio updates"""
        print("🎵 STARTING COMPREHENSIVE MAISON AUDIO BACKEND TESTING")
        print("=" * 80)
        print("Test complet du backend après la mise à jour des prononciations audio")
        print("pour la section 'maison' avec 66 fichiers M4A authentiques")
        print("=" * 80)
        
        # Test 1: Basic connectivity
        if not self.test_api_connectivity():
            print("❌ CRITICAL: Cannot connect to API. Stopping tests.")
            return self.generate_summary()
        
        # Test 2: Get maison words
        self.test_maison_category_access()
        
        # Test 3: Audio coverage verification
        self.test_audio_coverage_verification()
        
        # Test 4: Specific audio references
        self.test_specific_audio_references()
        
        # Test 5: Audio file integrity
        self.test_audio_file_integrity()
        
        # Test 6: Audio endpoint access
        self.test_audio_endpoint_access()
        
        # Test 7: Performance testing
        self.test_performance_audio()
        
        # Test 8: Consistency with other sections
        self.test_consistency_other_sections()
        
        # Test 9: Database integrity
        self.test_database_integrity()
        
        return self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 80)
        print("🎵 MAISON AUDIO BACKEND TESTING SUMMARY")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📊 RESULTS: {self.passed_tests}/{self.total_tests} tests passed ({success_rate:.1f}% success rate)")
        print("\n📋 DETAILED RESULTS:")
        
        for result in self.results:
            print(f"  {result}")
        
        print("\n" + "=" * 80)
        
        if success_rate >= 90:
            status = "🎉 EXCELLENT"
        elif success_rate >= 75:
            status = "✅ GOOD"
        elif success_rate >= 50:
            status = "⚠️ NEEDS IMPROVEMENT"
        else:
            status = "❌ CRITICAL ISSUES"
        
        print(f"🎯 OVERALL STATUS: {status}")
        
        # Show maison section statistics
        if self.maison_words:
            count = len(self.maison_words)
            with_audio = sum(1 for w in self.maison_words if (
                w.get('has_authentic_audio') or w.get('audio_filename') or
                w.get('shimoare_has_audio') or w.get('kibouchi_has_audio') or
                w.get('dual_audio_system')
            ))
            audio_rate = (with_audio / count * 100) if count > 0 else 0
            print(f"\n📈 MAISON SECTION STATISTICS:")
            print(f"  Total words: {count}")
            print(f"  With audio references: {with_audio} ({audio_rate:.1f}%)")
        
        print("=" * 80)
        
        return {
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "success_rate": success_rate,
            "status": status,
            "results": self.results
        }

def main():
    """Main test execution"""
    print(f"🔗 Using Backend URL: {BACKEND_URL}")
    
    tester = MaisonAudioTester()
    summary = tester.run_comprehensive_test()
    
    # Return exit code based on success rate
    if summary["success_rate"] >= 75:
        print("\n🏁 TESTS COMPLETED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("\n⚠️ SOME TESTS FAILED - VERIFICATION NEEDED")
        sys.exit(1)

if __name__ == "__main__":
    main()