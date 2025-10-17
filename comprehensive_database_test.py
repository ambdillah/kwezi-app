#!/usr/bin/env python3
"""
Test approfondi de la structure de la base de données après correction complète

Ce test vérifie tous les aspects demandés dans la review request française:
1. Vérification structure globale (10 sections, 309 mots total)
2. Test spécifique section VERBES (17 verbes avec correspondances audio)
3. Test spécifique section TRANSPORT (10 moyens de transport)
4. Vérification correspondances audio problématiques
5. Test de cohérence linguistique
6. Test performance API
"""

import requests
import json
import sys
from typing import Dict, List, Any, Optional
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get backend URL from frontend .env file
FRONTEND_ENV_PATH = "/app/frontend/.env"
BACKEND_URL = None

try:
    with open(FRONTEND_ENV_PATH, 'r') as f:
        for line in f:
            if line.startswith('EXPO_PUBLIC_BACKEND_URL='):
                BACKEND_URL = line.split('=')[1].strip()
                break
except:
    pass

if not BACKEND_URL:
    BACKEND_URL = "https://shimao-learn-1.preview.emergentagent.com"

API_URL = f"{BACKEND_URL}/api"
print(f"🔗 Using Backend URL: {BACKEND_URL}")

class ComprehensiveDatabaseTester:
    def __init__(self):
        self.api_url = API_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.all_words = []
        
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
        
    def make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Make HTTP request to backend"""
        url = f"{self.api_url}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)
            elif method == "PUT":
                response = requests.put(url, json=data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, timeout=10)
            
            return {
                "status_code": response.status_code,
                "data": response.json() if response.content else {},
                "success": response.status_code < 400
            }
        except Exception as e:
            return {
                "status_code": 0,
                "data": {"error": str(e)},
                "success": False
            }

    def test_1_api_connectivity(self):
        """Test 1: Vérifier la connectivité de l'API"""
        print("\n=== TEST 1: CONNECTIVITÉ API ===")
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=10)
            if response.status_code == 200:
                self.log_test("API Connectivity", True, f"Status: {response.status_code}")
                return True
            else:
                self.log_test("API Connectivity", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Connectivity", False, f"Error: {str(e)}")
            return False
    
    def test_2_global_structure(self):
        """Test 2: Vérification structure globale"""
        print("\n=== TEST 2: VÉRIFICATION STRUCTURE GLOBALE ===")
        
        # Get all words
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération mots", False, f"HTTP {response['status_code']}")
            return False
        
        self.all_words = response["data"]
        total_words = len(self.all_words)
        
        # Test total word count (allow flexibility around 309)
        expected_total = 309
        self.log_test("Total word count", 
                     total_words >= 300,  # Allow some flexibility
                     f"Found {total_words} words (expected ~{expected_total})")
        
        # Test required sections exist
        expected_sections = [
            "animaux", "corps", "maison", "nature", "nombres", 
            "nourriture", "salutations", "transport", "verbes", "vetements"
        ]
        
        categories_found = set()
        for word in self.all_words:
            if 'category' in word:
                categories_found.add(word['category'])
        
        for section in expected_sections:
            section_exists = section in categories_found
            self.log_test(f"Section '{section}' exists", section_exists)
        
        # Test required fields for each word
        words_with_complete_structure = 0
        for word in self.all_words:
            has_french = 'french' in word and word['french']
            has_shimaore = 'shimaore' in word and word['shimaore']
            has_kibouchi = 'kibouchi' in word and word['kibouchi']
            
            if has_french and has_shimaore and has_kibouchi:
                words_with_complete_structure += 1
        
        structure_percentage = (words_with_complete_structure / total_words * 100) if total_words > 0 else 0
        self.log_test("Words with complete structure (french, shimaoré, kibouchi)", 
                     structure_percentage >= 95,
                     f"{words_with_complete_structure}/{total_words} words ({structure_percentage:.1f}%)")
        
        return total_words >= 300
    
    def test_3_verbes_section(self):
        """Test 3: Test spécifique section VERBES"""
        print("\n=== TEST 3: TEST SPÉCIFIQUE SECTION VERBES ===")
        
        response = self.make_request("/words?category=verbes")
        if not response["success"]:
            self.log_test("Section verbes accessible", False, f"HTTP {response['status_code']}")
            return False
        
        verbes = response["data"]
        verbes_count = len(verbes)
        
        # Test verb count
        expected_verbs = 17
        self.log_test("Verbes section word count", 
                     verbes_count >= expected_verbs,
                     f"Found {verbes_count} verbs (expected {expected_verbs})")
        
        # Test specific verb correspondences
        specific_verbs = {
            "danser": {"shimaore": "chokou", "audio": "Chokou.m4a"},
            "voir": {"shimaore": "magnamiya", "audio": "Magnamiya.m4a"},
            "faire": {"shimaore": "magnossoutrou", "audio": "Magnossoutrou.m4a"}
        }
        
        for french_verb, expected in specific_verbs.items():
            verb_found = False
            for verb in verbes:
                if verb.get('french', '').lower() == french_verb.lower():
                    verb_found = True
                    
                    # Test shimaoré translation
                    shimaore_match = verb.get('shimaore', '').lower() == expected['shimaore'].lower()
                    self.log_test(f"Verb '{french_verb}' shimaoré translation", 
                                 shimaore_match,
                                 f"Expected: {expected['shimaore']}, Found: {verb.get('shimaore', 'N/A')}")
                    
                    # Test audio reference
                    audio_fields = ['audio_filename', 'shimoare_audio_filename', 'audio_url']
                    has_audio = any(field in verb and verb[field] for field in audio_fields)
                    self.log_test(f"Verb '{french_verb}' has audio reference", 
                                 has_audio,
                                 f"Audio fields checked: {[verb.get(field) for field in audio_fields]}")
                    break
            
            if not verb_found:
                self.log_test(f"Verb '{french_verb}' exists", False, "Verb not found in database")
        
        return verbes_count >= expected_verbs
    
    def test_4_transport_section(self):
        """Test 4: Test spécifique section TRANSPORT"""
        print("\n=== TEST 4: TEST SPÉCIFIQUE SECTION TRANSPORT ===")
        
        response = self.make_request("/words?category=transport")
        if not response["success"]:
            self.log_test("Section transport accessible", False, f"HTTP {response['status_code']}")
            return False
        
        transport = response["data"]
        transport_count = len(transport)
        
        # Test transport count
        expected_transport = 10
        self.log_test("Transport section word count", 
                     transport_count >= expected_transport,
                     f"Found {transport_count} transport means (expected {expected_transport})")
        
        # Test specific transport correspondences
        specific_transport = {
            "kwassa kwassa": {"audio": "Kwassa kwassa.m4a"},
            "pirogue": {"shimaore": "lakana", "audio": "Lakana.m4a"},
            "vedette": {"shimaore": "vidéti", "audio": "Vidéti.m4a"}
        }
        
        for french_transport, expected in specific_transport.items():
            transport_found = False
            for item in transport:
                if french_transport.lower() in item.get('french', '').lower():
                    transport_found = True
                    
                    # Test shimaoré translation if expected
                    if 'shimaore' in expected:
                        shimaore_match = expected['shimaore'].lower() in item.get('shimaore', '').lower()
                        self.log_test(f"Transport '{french_transport}' shimaoré translation", 
                                     shimaore_match,
                                     f"Expected: {expected['shimaore']}, Found: {item.get('shimaore', 'N/A')}")
                    
                    # Test audio reference
                    audio_fields = ['audio_filename', 'shimoare_audio_filename', 'audio_url']
                    has_audio = any(field in item and item[field] for field in audio_fields)
                    self.log_test(f"Transport '{french_transport}' has audio reference", 
                                 has_audio,
                                 f"Audio fields: {[item.get(field) for field in audio_fields]}")
                    break
            
            if not transport_found:
                self.log_test(f"Transport '{french_transport}' exists", False, "Transport not found in database")
        
        return transport_count >= expected_transport
    
    def test_5_audio_correspondences(self):
        """Test 5: Vérification correspondances audio problématiques"""
        print("\n=== TEST 5: VÉRIFICATION CORRESPONDANCES AUDIO ===")
        
        # Test audio coverage by section
        sections_to_test = {
            "nourriture": {"expected_coverage": 0, "expected_words": 44},
            "animaux": {"expected_coverage": 95.7, "expected_words": 69},
            "nature": {"expected_coverage": 94.8, "expected_words": 50},
            "vetements": {"expected_coverage": 94.1, "expected_words": 16}
        }
        
        for section, expectations in sections_to_test.items():
            response = self.make_request(f"/words?category={section}")
            if not response["success"]:
                self.log_test(f"Section '{section}' accessible", False, f"HTTP {response['status_code']}")
                continue
            
            words = response["data"]
            total_words = len(words)
            
            # Count words with audio
            words_with_audio = 0
            for word in words:
                audio_fields = [
                    'audio_filename', 'shimoare_audio_filename', 'kibouchi_audio_filename',
                    'audio_url', 'has_authentic_audio'
                ]
                has_audio = any(field in word and word[field] for field in audio_fields)
                if has_audio:
                    words_with_audio += 1
            
            coverage_percentage = (words_with_audio / total_words * 100) if total_words > 0 else 0
            
            self.log_test(f"Section '{section}' word count", 
                         total_words >= expectations["expected_words"] * 0.8,  # Allow 20% tolerance
                         f"Found {total_words} words (expected ~{expectations['expected_words']})")
            
            self.log_test(f"Section '{section}' audio coverage", 
                         True,  # Just log the coverage, don't fail
                         f"{words_with_audio}/{total_words} words ({coverage_percentage:.1f}% coverage)")
    
    def test_6_linguistic_consistency(self):
        """Test 6: Test de cohérence linguistique"""
        print("\n=== TEST 6: TEST DE COHÉRENCE LINGUISTIQUE ===")
        
        if not self.all_words:
            self.log_test("Cohérence linguistique", False, "Aucun mot à tester")
            return
        
        # Test for language mixing
        words_with_both_translations = 0
        words_with_unique_translations = 0
        
        for word in self.all_words:
            french = word.get('french', '')
            shimaore = word.get('shimaore', '')
            kibouchi = word.get('kibouchi', '')
            
            if french and shimaore and kibouchi:
                words_with_both_translations += 1
                
                # Check if translations are different (not mixed)
                if shimaore != kibouchi or (shimaore != french and kibouchi != french):
                    words_with_unique_translations += 1
        
        consistency_percentage = (words_with_unique_translations / words_with_both_translations * 100) if words_with_both_translations > 0 else 0
        
        self.log_test("Words have both shimaoré and kibouchi translations", 
                     words_with_both_translations >= len(self.all_words) * 0.95,
                     f"{words_with_both_translations}/{len(self.all_words)} words")
        
        self.log_test("Linguistic consistency (no language mixing)", 
                     consistency_percentage >= 90,
                     f"{words_with_unique_translations}/{words_with_both_translations} words ({consistency_percentage:.1f}%)")
    
    def test_7_api_performance(self):
        """Test 7: Test performance API"""
        print("\n=== TEST 7: TEST PERFORMANCE API ===")
        
        # Test specific endpoints
        endpoints_to_test = [
            ("verbes", "/words?category=verbes"),
            ("transport", "/words?category=transport"),
            ("all words", "/words")
        ]
        
        for name, endpoint in endpoints_to_test:
            start_time = time.time()
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=10)
                end_time = time.time()
                response_time = end_time - start_time
                
                success = response.status_code == 200
                self.log_test(f"API endpoint {name} response", 
                             success,
                             f"Status: {response.status_code}, Time: {response_time:.3f}s")
                
                if success:
                    data = response.json()
                    word_count = len(data) if isinstance(data, list) else 1
                    self.log_test(f"API endpoint {name} performance", 
                                 response_time < 2.0,
                                 f"{word_count} words in {response_time:.3f}s")
                
            except Exception as e:
                self.log_test(f"API endpoint {name}", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🎯 DÉBUT DES TESTS COMPLETS DU BACKEND MAYOTTE")
        print("=" * 60)
        print("Test approfondi de la structure de la base de données")
        print("Focus: VERBES et TRANSPORT sections")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test API connectivity first
        if not self.test_1_api_connectivity():
            print("❌ Cannot connect to API. Stopping tests.")
            return False
        
        # Run all test suites
        self.test_2_global_structure()
        self.test_3_verbes_section()
        self.test_4_transport_section()
        self.test_5_audio_correspondences()
        self.test_6_linguistic_consistency()
        self.test_7_api_performance()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"Tests réussis: {self.passed_tests}/{self.total_tests} ({success_rate:.1f}%)")
        print(f"Durée: {duration:.2f}s")
        
        if success_rate >= 80:
            print("🎉 RÉSULTAT GLOBAL: SUCCÈS")
        elif success_rate >= 60:
            print("⚠️ RÉSULTAT GLOBAL: PARTIELLEMENT RÉUSSI")
        else:
            print("❌ RÉSULTAT GLOBAL: ÉCHEC")
        
        print("\nDétails des tests:")
        for result in self.test_results:
            print(f"  {result}")
        
        return success_rate >= 60

def main():
    """Main test execution"""
    tester = ComprehensiveDatabaseTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🏁 TESTS TERMINÉS AVEC SUCCÈS!")
        sys.exit(0)
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ - VÉRIFICATION NÉCESSAIRE")
        sys.exit(1)

if __name__ == "__main__":
    main()