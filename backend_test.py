#!/usr/bin/env python3
"""
Backend Testing Suite for Mayotte Language Learning API
Testing PDF vocabulary corrections after shimaoré-kibouchi updates
Focus: Verify 565 words total, orthographic corrections, and new words added
"""

import requests
import json
import sys
from typing import Dict, List, Any, Optional
import time

# Configuration
BACKEND_URL = "https://kwezi-learn.preview.emergentagent.com/api"

class BackendTester:
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
        
    def make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Make HTTP request to backend"""
        url = f"{self.backend_url}{endpoint}"
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

    def test_1_corrections_orthographiques_appliquees(self):
        """Test 1: Vérifier que les corrections orthographiques ont été appliquées"""
        print("\n=== TEST 1: CORRECTIONS ORTHOGRAPHIQUES APPLIQUÉES ===")
        
        # Get all words
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        self.log_test("Récupération des mots", True, f"{len(words)} mots trouvés")
        
        # Create word lookup dictionary
        word_dict = {word.get("french", "").lower(): word for word in words}
        
        # Test: Mots français sans accents existent maintenant (etoile, ecole, etc.)
        words_without_accents = ["etoile", "ecole"]
        for word_french in words_without_accents:
            if word_french in word_dict:
                self.log_test(f"Mot sans accent '{word_french}' existe", True, f"Trouvé: {word_dict[word_french].get('french', '')}")
            else:
                self.log_test(f"Mot sans accent '{word_french}' existe", False, f"Mot '{word_french}' non trouvé")
        
        # Test: Correction escargot - shimaore doit être "kowa" (au lieu de "kwa")
        if "escargot" in word_dict:
            escargot = word_dict["escargot"]
            shimaore = escargot.get("shimaore", "").lower()
            if "kowa" in shimaore:
                self.log_test("Correction escargot -> 'kowa'", True, f"Shimaore: '{escargot.get('shimaore', '')}'")
            else:
                self.log_test("Correction escargot -> 'kowa'", False, f"Shimaore: '{escargot.get('shimaore', '')}' (devrait contenir 'kowa')")
        else:
            self.log_test("Correction escargot -> 'kowa'", False, "Mot 'escargot' non trouvé")
        
        # Test: Correction oursin - shimaore doit être "gadzassi ya bahari" pour différencier de huître
        if "oursin" in word_dict:
            oursin = word_dict["oursin"]
            shimaore = oursin.get("shimaore", "").lower()
            if "gadzassi ya bahari" in shimaore:
                self.log_test("Correction oursin -> 'gadzassi ya bahari'", True, f"Shimaore: '{oursin.get('shimaore', '')}'")
            else:
                self.log_test("Correction oursin -> 'gadzassi ya bahari'", False, f"Shimaore: '{oursin.get('shimaore', '')}' (devrait être 'gadzassi ya bahari')")
        else:
            self.log_test("Correction oursin -> 'gadzassi ya bahari'", False, "Mot 'oursin' non trouvé")
        
        # Test: Correction nous - shimaore doit être "wasi" (au lieu de "wassi")
        if "nous" in word_dict:
            nous = word_dict["nous"]
            shimaore = nous.get("shimaore", "").lower()
            if shimaore == "wasi":
                self.log_test("Correction nous -> 'wasi'", True, f"Shimaore: '{nous.get('shimaore', '')}'")
            else:
                self.log_test("Correction nous -> 'wasi'", False, f"Shimaore: '{nous.get('shimaore', '')}' (devrait être 'wasi')")
        else:
            self.log_test("Correction nous -> 'wasi'", False, "Mot 'nous' non trouvé")

    def test_2_corrections_orthographiques(self):
        """Test 2: Vérifier les corrections orthographiques"""
        print("\n=== TEST 2: CORRECTIONS ORTHOGRAPHIQUES ===")
        
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        
        # Test: French words should not have accents
        french_accent_issues = []
        accent_chars = ['é', 'è', 'ê', 'à', 'ù', 'ô', 'î', 'ç', 'ü', 'ï']
        
        for word in words:
            french = word.get("french", "")
            if any(char in french for char in accent_chars):
                french_accent_issues.append(french)
        
        self.log_test("Accents français supprimés", len(french_accent_issues) == 0,
                     f"Mots avec accents: {french_accent_issues[:10]}" if french_accent_issues else "Aucun accent trouvé")
        
        # Test specific corrections mentioned
        test_corrections = [
            ("etoile", "étoile"),  # étoile -> etoile
            ("ecole", "école"),    # école -> ecole
        ]
        
        for corrected, original in test_corrections:
            found_corrected = any(word.get("french", "").lower() == corrected for word in words)
            found_original = any(word.get("french", "").lower() == original for word in words)
            
            self.log_test(f"Correction {original} -> {corrected}", found_corrected and not found_original,
                         f"Trouvé '{corrected}': {found_corrected}, Trouvé '{original}': {found_original}")
        
        # Test: Shimaoré words should be normalized
        shimaore_accent_issues = []
        for word in words:
            shimaore = word.get("shimaore", "")
            if any(char in shimaore for char in accent_chars):
                shimaore_accent_issues.append(f"{word.get('french', '')} -> {shimaore}")
        
        self.log_test("Accents shimaoré normalisés", len(shimaore_accent_issues) <= 5,  # Allow some exceptions
                     f"Mots shimaoré avec accents: {len(shimaore_accent_issues)}")

    def test_3_integration_complete_pdf(self):
        """Test 3: Vérifier l'intégration complète du PDF"""
        print("\n=== TEST 3: INTÉGRATION COMPLÈTE DU PDF ===")
        
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        total_words = len(words)
        
        # Test: Total should be 211 words
        self.log_test("Total 211 mots", total_words == 211, f"Trouvé {total_words} mots (attendu: 211)")
        
        # Test: Check categories
        categories = {}
        for word in words:
            category = word.get("category", "unknown")
            categories[category] = categories.get(category, 0) + 1
        
        expected_categories = [
            "animaux", "corps", "couleurs", "education", "famille", 
            "grammaire", "nature", "nombres", "salutations", "transport"
        ]
        
        found_categories = list(categories.keys())
        missing_categories = [cat for cat in expected_categories if cat not in found_categories]
        
        self.log_test("10 catégories présentes", len(missing_categories) == 0,
                     f"Catégories manquantes: {missing_categories}" if missing_categories else f"Toutes les catégories présentes: {found_categories}")
        
        # Test: Check numbers 11-20 are present
        numbers_11_20 = [
            "onze", "douze", "treize", "quatorze", "quinze",
            "seize", "dix-sept", "dix-huit", "dix-neuf", "vingt"
        ]
        
        found_numbers = []
        for number in numbers_11_20:
            if any(word.get("french", "").lower() == number for word in words):
                found_numbers.append(number)
        
        self.log_test("Nombres 11-20 présents", len(found_numbers) == len(numbers_11_20),
                     f"Nombres trouvés: {len(found_numbers)}/{len(numbers_11_20)} - {found_numbers}")
        
        # Test: Check kibouchi translations added
        words_with_kibouchi = sum(1 for word in words if word.get("kibouchi", "").strip())
        kibouchi_percentage = (words_with_kibouchi / total_words * 100) if total_words > 0 else 0
        
        self.log_test("45 traductions kibouchi ajoutées", words_with_kibouchi >= 45,
                     f"{words_with_kibouchi} mots avec kibouchi ({kibouchi_percentage:.1f}%)")

    def test_4_couverture_traductions(self):
        """Test 4: Vérifier la couverture des traductions"""
        print("\n=== TEST 4: COUVERTURE DES TRADUCTIONS ===")
        
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        total_words = len(words)
        
        # Test: 100% shimaoré coverage
        words_with_shimaore = sum(1 for word in words if word.get("shimaore", "").strip())
        shimaore_percentage = (words_with_shimaore / total_words * 100) if total_words > 0 else 0
        
        self.log_test("100% couverture shimaoré", shimaore_percentage == 100,
                     f"{words_with_shimaore}/{total_words} mots avec shimaoré ({shimaore_percentage:.1f}%)")
        
        # Test: ~26.5% kibouchi coverage (56/211)
        words_with_kibouchi = sum(1 for word in words if word.get("kibouchi", "").strip())
        kibouchi_percentage = (words_with_kibouchi / total_words * 100) if total_words > 0 else 0
        expected_kibouchi = 56
        
        self.log_test("26.5% couverture kibouchi", abs(words_with_kibouchi - expected_kibouchi) <= 5,
                     f"{words_with_kibouchi}/{total_words} mots avec kibouchi ({kibouchi_percentage:.1f}%) - attendu: ~{expected_kibouchi}")
        
        # Test specific new kibouchi translations
        specific_tests = [
            ("pente", "boungou"),
            ("ecole", "licoli"), 
            ("chat", "moirou")
        ]
        
        for french_word, expected_kibouchi in specific_tests:
            word_found = None
            for word in words:
                if word.get("french", "").lower() == french_word:
                    word_found = word
                    break
            
            if word_found:
                actual_kibouchi = word_found.get("kibouchi", "").lower()
                has_expected = expected_kibouchi.lower() in actual_kibouchi
                self.log_test(f"Traduction kibouchi '{french_word}' -> '{expected_kibouchi}'", has_expected,
                             f"Trouvé: '{actual_kibouchi}'")
            else:
                self.log_test(f"Mot '{french_word}' présent", False, "Mot non trouvé")

    def test_5_coherence_base(self):
        """Test 5: Vérifier la cohérence de la base de données"""
        print("\n=== TEST 5: COHÉRENCE DE LA BASE ===")
        
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        
        # Test: No duplicates (already tested but important for coherence)
        french_words = set()
        duplicates = []
        for word in words:
            french = word.get("french", "").lower().strip()
            if french in french_words:
                duplicates.append(french)
            else:
                french_words.add(french)
        
        self.log_test("Aucun doublon", len(duplicates) == 0,
                     f"Doublons: {duplicates}" if duplicates else "Base cohérente")
        
        # Test: All words have required fields
        missing_fields = []
        for i, word in enumerate(words):
            required_fields = ["french", "shimaore", "category"]
            for field in required_fields:
                if not word.get(field, "").strip():
                    missing_fields.append(f"Mot {i+1}: champ '{field}' manquant")
        
        self.log_test("Champs requis présents", len(missing_fields) == 0,
                     f"Champs manquants: {len(missing_fields)}" if missing_fields else "Tous les champs requis présents")
        
        # Test: Data structure consistency
        structure_issues = []
        for i, word in enumerate(words):
            # Check if word has basic structure
            if not isinstance(word, dict):
                structure_issues.append(f"Mot {i+1}: structure invalide")
                continue
                
            # Check field types
            string_fields = ["french", "shimaore", "kibouchi", "category"]
            for field in string_fields:
                if field in word and not isinstance(word[field], str):
                    structure_issues.append(f"Mot {i+1}: {field} n'est pas une chaîne")
        
        self.log_test("Structure de données cohérente", len(structure_issues) == 0,
                     f"Problèmes de structure: {len(structure_issues)}")
        
        # Test: API endpoints working
        endpoints_to_test = [
            "/words?category=famille",
            "/words?category=couleurs", 
            "/words?category=animaux",
            "/words?category=nombres"
        ]
        
        working_endpoints = 0
        for endpoint in endpoints_to_test:
            response = self.make_request(endpoint)
            if response["success"]:
                working_endpoints += 1
        
        self.log_test("Endpoints API fonctionnels", working_endpoints == len(endpoints_to_test),
                     f"{working_endpoints}/{len(endpoints_to_test)} endpoints fonctionnels")

    def run_all_tests(self):
        """Run all tests"""
        print("🧪 DÉBUT DES TESTS - ANALYSE ET CORRECTION DU PDF VOCABULAIRE SHIMAORÉ-KIBOUCHI")
        print("=" * 80)
        
        start_time = time.time()
        
        # Run all test suites
        self.test_1_doublons_elimines()
        self.test_2_corrections_orthographiques()
        self.test_3_integration_complete_pdf()
        self.test_4_couverture_traductions()
        self.test_5_coherence_base()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 80)
        
        for result in self.test_results:
            print(result)
        
        print(f"\n🎯 RÉSULTATS FINAUX:")
        print(f"   Tests réussis: {self.passed_tests}/{self.total_tests}")
        print(f"   Taux de réussite: {(self.passed_tests/self.total_tests*100):.1f}%")
        print(f"   Durée: {duration:.2f}s")
        
        if self.passed_tests == self.total_tests:
            print("🎉 TOUS LES TESTS SONT PASSÉS - INTÉGRATION PDF RÉUSSIE!")
            return True
        else:
            failed_tests = self.total_tests - self.passed_tests
            print(f"⚠️  {failed_tests} TEST(S) ÉCHOUÉ(S) - CORRECTIONS NÉCESSAIRES")
            return False

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)