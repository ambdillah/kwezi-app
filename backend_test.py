#!/usr/bin/env python3
"""
Backend Testing Suite for Mayotte Language Learning API
Testing PDF vocabulary shimaoré-kibouchi analysis and corrections
"""

import requests
import json
import sys
from typing import Dict, List, Any
import time

# Configuration
BACKEND_URL = "https://shimakibo-learn.preview.emergentagent.com/api"

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

    def test_1_doublons_elimines(self):
        """Test 1: Vérifier que les doublons ont été éliminés"""
        print("\n=== TEST 1: DOUBLONS ÉLIMINÉS ===")
        
        # Get all words
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        self.log_test("Récupération des mots", True, f"{len(words)} mots trouvés")
        
        # Check for duplicates by French word
        french_words = {}
        duplicates_found = []
        
        for word in words:
            french = word.get("french", "").lower()
            if french in french_words:
                duplicates_found.append(french)
            else:
                french_words[french] = word
        
        # Test: No duplicates should exist
        self.log_test("Absence de doublons", len(duplicates_found) == 0, 
                     f"Doublons trouvés: {duplicates_found}" if duplicates_found else "Aucun doublon détecté")
        
        # Test specific cases mentioned in review
        # 1. Only "bigorneau" should exist (not "tortue" duplicate)
        bigorneau_count = sum(1 for word in words if word.get("french", "").lower() == "bigorneau")
        tortue_count = sum(1 for word in words if word.get("french", "").lower() == "tortue")
        
        self.log_test("Bigorneau unique", bigorneau_count == 1, f"Bigorneau trouvé {bigorneau_count} fois")
        self.log_test("Tortue présente", tortue_count >= 1, f"Tortue trouvé {tortue_count} fois")
        
        # 2. Only one "escargot" with translation "kowa"
        escargot_words = [word for word in words if word.get("french", "").lower() == "escargot"]
        escargot_with_kowa = [word for word in escargot_words if "kowa" in word.get("shimaore", "").lower()]
        
        self.log_test("Escargot unique", len(escargot_words) == 1, f"{len(escargot_words)} escargot(s) trouvé(s)")
        self.log_test("Escargot avec 'kowa'", len(escargot_with_kowa) >= 1, 
                     f"Escargot avec kowa: {escargot_with_kowa[0].get('shimaore', '') if escargot_with_kowa else 'Non trouvé'}")
        
        # 3. "oursin" and "huître" have distinct translations
        oursin_words = [word for word in words if word.get("french", "").lower() == "oursin"]
        huitre_words = [word for word in words if word.get("french", "").lower() == "huître"]
        
        if oursin_words and huitre_words:
            oursin_translation = oursin_words[0].get("shimaore", "")
            huitre_translation = huitre_words[0].get("shimaore", "")
            distinct_translations = oursin_translation != huitre_translation
            
            self.log_test("Oursin/Huître traductions distinctes", distinct_translations,
                         f"Oursin: {oursin_translation}, Huître: {huitre_translation}")
        else:
            self.log_test("Oursin/Huître présents", False, "Oursin ou Huître manquant")

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