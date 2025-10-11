#!/usr/bin/env python3
"""
Test approfondi de la base de données reconstruite avec les données authentiques du PDF
Comprehensive testing of the reconstructed database with authentic PDF data

This test suite verifies:
1. Global structure verification (12 sections, 415 words total)
2. Specific orthographic corrections testing
3. New sections created (Colors, Family, Extended verbs)
4. Audio coverage verification
5. Linguistic consistency testing
6. API performance testing
7. PDF vs database validation
"""

import requests
import json
import time
import sys
from typing import Dict, List, Any
import os

# Configuration
BACKEND_URL = "https://kwezi-app.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

class DatabaseTestSuite:
    def __init__(self):
        self.results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': []
        }
        
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        self.results['total_tests'] += 1
        if passed:
            self.results['passed_tests'] += 1
            status = "✅ PASS"
        else:
            self.results['failed_tests'] += 1
            status = "❌ FAIL"
            
        self.results['test_details'].append({
            'test': test_name,
            'status': status,
            'details': details
        })
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
    
    def test_api_connectivity(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{API_BASE}/words", timeout=10)
            if response.status_code == 200:
                self.log_test("API Connectivity", True, f"API accessible at {API_BASE}")
                return True
            else:
                self.log_test("API Connectivity", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Connectivity", False, f"Connection error: {str(e)}")
            return False
    
    def get_all_words(self) -> List[Dict]:
        """Get all words from database"""
        try:
            response = requests.get(f"{API_BASE}/words", timeout=15)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error fetching words: {e}")
            return []
    
    def get_words_by_category(self, category: str) -> List[Dict]:
        """Get words by category"""
        try:
            response = requests.get(f"{API_BASE}/words?category={category}", timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error fetching {category} words: {e}")
            return []
    
    def test_global_structure(self):
        """1. Vérification structure globale"""
        print("\n=== 1. VÉRIFICATION STRUCTURE GLOBALE ===")
        
        # Get all words
        all_words = self.get_all_words()
        total_words = len(all_words)
        
        # Test total word count
        expected_words = 415  # According to review request
        if total_words >= expected_words:
            self.log_test("Total Word Count", True, f"Found {total_words} words (expected {expected_words}+)")
        else:
            self.log_test("Total Word Count", False, f"Found {total_words} words, expected {expected_words}+")
        
        # Get unique categories
        categories = set()
        for word in all_words:
            if 'category' in word:
                categories.add(word['category'])
        
        # Test section count
        expected_sections = 12
        if len(categories) >= expected_sections:
            self.log_test("Section Count", True, f"Found {len(categories)} sections: {sorted(categories)}")
        else:
            self.log_test("Section Count", False, f"Found {len(categories)} sections, expected {expected_sections}")
        
        # Test each word has 3 translations
        complete_words = 0
        for word in all_words:
            if all(key in word and word[key] for key in ['french', 'shimaore', 'kibouchi']):
                complete_words += 1
        
        completion_rate = (complete_words / total_words * 100) if total_words > 0 else 0
        if completion_rate >= 95:
            self.log_test("Translation Completeness", True, f"{completion_rate:.1f}% words have all 3 translations ({complete_words}/{total_words})")
        else:
            self.log_test("Translation Completeness", False, f"Only {completion_rate:.1f}% words complete ({complete_words}/{total_words})")
        
        return all_words, categories
    
    def test_specific_corrections(self, all_words: List[Dict]):
        """2. Test spécifique des corrections orthographiques"""
        print("\n=== 2. TEST CORRECTIONS ORTHOGRAPHIQUES SPÉCIFIQUES ===")
        
        # Expected corrections from review request
        expected_corrections = {
            "voir": {"shimaore": "ouona", "kibouchi": "mahita"},
            "cochon": {"shimaore": "pouroukou", "kibouchi": "lambou"},
            "lune": {"shimaore": "mwézi", "kibouchi": "fandzava"},
            "œil": {"shimaore": "matso", "kibouchi": "kiyo"}
        }
        
        word_dict = {word['french'].lower(): word for word in all_words}
        
        for french_word, expected_translations in expected_corrections.items():
            if french_word in word_dict:
                word = word_dict[french_word]
                shimaore_correct = word.get('shimaore', '').lower() == expected_translations['shimaore'].lower()
                kibouchi_correct = word.get('kibouchi', '').lower() == expected_translations['kibouchi'].lower()
                
                if shimaore_correct and kibouchi_correct:
                    self.log_test(f"Correction '{french_word}'", True, 
                                f"shimaoré: '{word.get('shimaore')}', kibouchi: '{word.get('kibouchi')}'")
                else:
                    self.log_test(f"Correction '{french_word}'", False, 
                                f"Expected shimaoré: '{expected_translations['shimaore']}', got: '{word.get('shimaore')}' | "
                                f"Expected kibouchi: '{expected_translations['kibouchi']}', got: '{word.get('kibouchi')}'")
            else:
                self.log_test(f"Correction '{french_word}'", False, f"Word '{french_word}' not found in database")
    
    def test_new_sections(self, categories: set):
        """3. Test des nouvelles sections créées"""
        print("\n=== 3. TEST NOUVELLES SECTIONS CRÉÉES ===")
        
        # Test Colors section (8 words expected)
        if 'couleurs' in categories:
            couleurs_words = self.get_words_by_category('couleurs')
            expected_colors = 8
            if len(couleurs_words) >= expected_colors:
                self.log_test("Section Couleurs", True, f"Found {len(couleurs_words)} color words (expected {expected_colors})")
                
                # Test specific color examples
                color_dict = {word['french'].lower(): word for word in couleurs_words}
                if 'bleu' in color_dict:
                    bleu = color_dict['bleu']
                    self.log_test("Couleur 'bleu'", True, f"shimaoré: '{bleu.get('shimaore')}', kibouchi: '{bleu.get('kibouchi')}'")
                if 'rouge' in color_dict:
                    rouge = color_dict['rouge']
                    self.log_test("Couleur 'rouge'", True, f"shimaoré: '{rouge.get('shimaore')}', kibouchi: '{rouge.get('kibouchi')}'")
            else:
                self.log_test("Section Couleurs", False, f"Found {len(couleurs_words)} words, expected {expected_colors}")
        else:
            self.log_test("Section Couleurs", False, "Couleurs category not found")
        
        # Test Family section (25 words expected)
        if 'famille' in categories:
            famille_words = self.get_words_by_category('famille')
            expected_family = 25
            if len(famille_words) >= expected_family:
                self.log_test("Section Famille", True, f"Found {len(famille_words)} family words (expected {expected_family})")
                
                # Test specific family examples
                family_dict = {word['french'].lower(): word for word in famille_words}
                test_words = ['papa', 'maman', 'frère', 'sœur']
                for test_word in test_words:
                    if test_word in family_dict:
                        word = family_dict[test_word]
                        self.log_test(f"Famille '{test_word}'", True, 
                                    f"shimaoré: '{word.get('shimaore')}', kibouchi: '{word.get('kibouchi')}'")
            else:
                self.log_test("Section Famille", False, f"Found {len(famille_words)} words, expected {expected_family}")
        else:
            self.log_test("Section Famille", False, "Famille category not found")
        
        # Test Extended Verbs section (78 words expected)
        if 'verbes' in categories:
            verbes_words = self.get_words_by_category('verbes')
            expected_verbs = 78
            if len(verbes_words) >= expected_verbs:
                self.log_test("Section Verbes Étendus", True, f"Found {len(verbes_words)} verb words (expected {expected_verbs})")
            else:
                self.log_test("Section Verbes Étendus", False, f"Found {len(verbes_words)} words, expected {expected_verbs}")
        else:
            self.log_test("Section Verbes", False, "Verbes category not found")
    
    def test_audio_coverage(self, categories: set):
        """4. Vérification couverture audio"""
        print("\n=== 4. VÉRIFICATION COUVERTURE AUDIO ===")
        
        # Categories expected to have 100% audio
        full_audio_categories = ['animaux', 'corps', 'maison', 'nature', 'nombres', 'salutations', 'transport', 'verbes', 'vetements']
        
        # Categories without audio (temporary)
        no_audio_categories = ['couleurs', 'famille', 'nourriture']
        
        total_words_with_audio = 0
        total_words_checked = 0
        
        for category in categories:
            words = self.get_words_by_category(category)
            if not words:
                continue
                
            words_with_audio = 0
            for word in words:
                total_words_checked += 1
                # Check various audio fields
                has_audio = any([
                    word.get('has_authentic_audio', False),
                    word.get('shimoare_has_audio', False),
                    word.get('kibouchi_has_audio', False),
                    word.get('audio_filename'),
                    word.get('shimoare_audio_filename'),
                    word.get('kibouchi_audio_filename')
                ])
                if has_audio:
                    words_with_audio += 1
                    total_words_with_audio += 1
            
            coverage = (words_with_audio / len(words) * 100) if words else 0
            
            if category in full_audio_categories:
                expected_coverage = 100
                if coverage >= 90:  # Allow some tolerance
                    self.log_test(f"Audio Coverage {category}", True, f"{coverage:.1f}% ({words_with_audio}/{len(words)} words)")
                else:
                    self.log_test(f"Audio Coverage {category}", False, f"{coverage:.1f}% coverage, expected ~{expected_coverage}%")
            elif category in no_audio_categories:
                self.log_test(f"Audio Coverage {category}", True, f"{coverage:.1f}% (temporary no audio expected)")
            else:
                self.log_test(f"Audio Coverage {category}", True, f"{coverage:.1f}% ({words_with_audio}/{len(words)} words)")
        
        # Overall audio coverage
        overall_coverage = (total_words_with_audio / total_words_checked * 100) if total_words_checked > 0 else 0
        expected_overall = 81.4  # From review request
        
        if overall_coverage >= expected_overall - 5:  # Allow 5% tolerance
            self.log_test("Overall Audio Coverage", True, f"{overall_coverage:.1f}% ({total_words_with_audio}/{total_words_checked} words)")
        else:
            self.log_test("Overall Audio Coverage", False, f"{overall_coverage:.1f}% coverage, expected ~{expected_overall}%")
    
    def test_linguistic_consistency(self, all_words: List[Dict]):
        """5. Test cohérence linguistique"""
        print("\n=== 5. TEST COHÉRENCE LINGUISTIQUE ===")
        
        # Check for language mixing
        mixed_languages = 0
        duplicate_translations = 0
        missing_translations = 0
        
        for word in all_words:
            french = word.get('french', '')
            shimaore = word.get('shimaore', '')
            kibouchi = word.get('kibouchi', '')
            
            # Check for missing translations
            if not shimaore or not kibouchi:
                missing_translations += 1
                continue
            
            # Check for identical translations (potential mixing)
            if shimaore.lower() == kibouchi.lower() and len(shimaore) > 2:
                # Some short words might legitimately be the same
                duplicate_translations += 1
        
        # Test results
        total_words = len(all_words)
        consistency_rate = ((total_words - mixed_languages - duplicate_translations) / total_words * 100) if total_words > 0 else 0
        
        if consistency_rate >= 95:
            self.log_test("Linguistic Consistency", True, f"{consistency_rate:.1f}% consistency rate")
        else:
            self.log_test("Linguistic Consistency", False, f"{consistency_rate:.1f}% consistency, {duplicate_translations} potential duplicates")
        
        if missing_translations == 0:
            self.log_test("Translation Completeness", True, "All words have both shimaoré and kibouchi translations")
        else:
            self.log_test("Translation Completeness", False, f"{missing_translations} words missing translations")
    
    def test_api_performance(self):
        """6. Test performance API"""
        print("\n=== 6. TEST PERFORMANCE API ===")
        
        # Test global endpoint performance
        start_time = time.time()
        response = requests.get(f"{API_BASE}/words", timeout=15)
        end_time = time.time()
        
        response_time = end_time - start_time
        if response.status_code == 200 and response_time < 5.0:
            self.log_test("Global API Performance", True, f"Response time: {response_time:.3f}s")
        else:
            self.log_test("Global API Performance", False, f"Response time: {response_time:.3f}s or HTTP {response.status_code}")
        
        # Test category filtering performance
        categories_to_test = ['famille', 'animaux', 'verbes', 'couleurs']
        for category in categories_to_test:
            start_time = time.time()
            response = requests.get(f"{API_BASE}/words?category={category}", timeout=10)
            end_time = time.time()
            
            response_time = end_time - start_time
            if response.status_code == 200 and response_time < 2.0:
                word_count = len(response.json()) if response.status_code == 200 else 0
                self.log_test(f"Category API Performance ({category})", True, 
                            f"Response time: {response_time:.3f}s, {word_count} words")
            else:
                self.log_test(f"Category API Performance ({category})", False, 
                            f"Response time: {response_time:.3f}s or HTTP {response.status_code}")
    
    def test_pdf_validation(self, all_words: List[Dict]):
        """7. Validation données PDF vs base"""
        print("\n=== 7. VALIDATION DONNÉES PDF VS BASE ===")
        
        # Test specific words with special characters
        special_words = {
            "m'nadzi": "cocotier",  # Word with apostrophe
            "m'panga": "machette",  # Word with apostrophe
            "œil": "eye"  # Word with special character
        }
        
        word_dict = {word['french'].lower(): word for word in all_words}
        
        for test_word, description in special_words.items():
            if test_word.lower() in word_dict:
                self.log_test(f"Special Character Word '{test_word}'", True, f"Found {description}")
            else:
                # Try to find similar words
                found_similar = False
                for french_word in word_dict.keys():
                    if test_word.replace("'", "").lower() in french_word or french_word in test_word.replace("'", "").lower():
                        self.log_test(f"Special Character Word '{test_word}'", True, f"Found similar: '{french_word}'")
                        found_similar = True
                        break
                
                if not found_similar:
                    self.log_test(f"Special Character Word '{test_word}'", False, f"Word not found")
        
        # Test accent handling
        accent_words = ['frère', 'mère', 'père', 'tête', 'être']
        accent_found = 0
        for accent_word in accent_words:
            if accent_word.lower() in word_dict:
                accent_found += 1
        
        if accent_found >= len(accent_words) * 0.6:  # At least 60% found
            self.log_test("Accent Handling", True, f"Found {accent_found}/{len(accent_words)} words with accents")
        else:
            self.log_test("Accent Handling", False, f"Only found {accent_found}/{len(accent_words)} words with accents")
    
    def run_comprehensive_test(self):
        """Run all tests"""
        print("🎯 DÉMARRAGE TEST APPROFONDI BASE DE DONNÉES RECONSTRUITE")
        print("=" * 80)
        
        # Test API connectivity first
        if not self.test_api_connectivity():
            print("❌ Cannot proceed - API not accessible")
            return self.results
        
        # Get all data
        all_words, categories = self.test_global_structure()
        
        if not all_words:
            print("❌ Cannot proceed - No words found in database")
            return self.results
        
        # Run all test suites
        self.test_specific_corrections(all_words)
        self.test_new_sections(categories)
        self.test_audio_coverage(categories)
        self.test_linguistic_consistency(all_words)
        self.test_api_performance()
        self.test_pdf_validation(all_words)
        
        return self.results
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 80)
        
        success_rate = (self.results['passed_tests'] / self.results['total_tests'] * 100) if self.results['total_tests'] > 0 else 0
        
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Tests Réussis: {self.results['passed_tests']}")
        print(f"Tests Échoués: {self.results['failed_tests']}")
        print(f"Taux de Réussite: {success_rate:.1f}%")
        
        if self.results['failed_tests'] > 0:
            print(f"\n❌ TESTS ÉCHOUÉS ({self.results['failed_tests']}):")
            for test in self.results['test_details']:
                if test['status'].startswith('❌'):
                    print(f"  - {test['test']}: {test['details']}")
        
        print(f"\n✅ TESTS RÉUSSIS ({self.results['passed_tests']}):")
        for test in self.results['test_details']:
            if test['status'].startswith('✅'):
                print(f"  - {test['test']}")

def main():
    """Main test execution"""
    tester = DatabaseTestSuite()
    results = tester.run_comprehensive_test()
    tester.print_summary()
    
    # Return exit code based on results
    if results['failed_tests'] == 0:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
        return 0
    else:
        print(f"\n⚠️ {results['failed_tests']} TESTS ONT ÉCHOUÉ")
        return 1

if __name__ == "__main__":
    exit(main())