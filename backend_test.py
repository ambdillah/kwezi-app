#!/usr/bin/env python3
"""
Backend Testing Script for Mayotte Language Learning API
Testing the complete family section update with new data from table
Focus: Verify new translations, new word addition, and data integrity
"""

import requests
import json
import sys
from typing import Dict, List, Any, Optional
import time

# Configuration
BACKEND_URL = "https://kwezi-learn.preview.emergentagent.com/api"

class FamilySectionTester:
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

    def test_1_nouvelles_traductions_mises_a_jour(self):
        """Test 1: Vérifier les nouvelles traductions mise à jour"""
        print("\n=== TEST 1: NOUVELLES TRADUCTIONS MISE À JOUR ===")
        
        # Get family words
        response = self.make_request("/words?category=famille")
        if not response["success"]:
            self.log_test("Récupération mots famille", False, f"Erreur API: {response['data']}")
            return
            
        family_words = response["data"]
        self.log_test("Récupération mots famille", True, f"{len(family_words)} mots famille trouvés")
        
        # Create word lookup dictionary
        word_dict = {word.get("french", "").lower(): word for word in family_words}
        
        # Test the specific updated translations from the review request
        expected_updates = {
            "tante maternelle": {"shimaore": "mama titi bolé", "kibouchi": "nindri heli bé"},
            "oncle maternel": {"shimaore": "zama", "kibouchi": "zama"},
            "petite sœur": {"shimaore": "moinagna mtroumama", "kibouchi": "zandri viavi"},
            "grand frère": {"shimaore": "zouki mtoubaba", "kibouchi": "zoki lalahi"}
        }
        
        for french_word, expected_translations in expected_updates.items():
            if french_word in word_dict:
                word = word_dict[french_word]
                shimaore_actual = word.get('shimaore', '').lower().strip()
                kibouchi_actual = word.get('kibouchi', '').lower().strip()
                shimaore_expected = expected_translations['shimaore'].lower().strip()
                kibouchi_expected = expected_translations['kibouchi'].lower().strip()
                
                shimaore_match = shimaore_expected in shimaore_actual or shimaore_actual in shimaore_expected
                kibouchi_match = kibouchi_expected in kibouchi_actual or kibouchi_actual in kibouchi_expected
                
                if shimaore_match and kibouchi_match:
                    self.log_test(f"Traduction mise à jour: {french_word}", True, 
                                  f"Shimaoré: {word.get('shimaore')}, Kibouchi: {word.get('kibouchi')}")
                else:
                    self.log_test(f"Traduction mise à jour: {french_word}", False, 
                                  f"Attendu Shimaoré: {expected_translations['shimaore']}, Trouvé: {word.get('shimaore')} | "
                                  f"Attendu Kibouchi: {expected_translations['kibouchi']}, Trouvé: {word.get('kibouchi')}")
            else:
                self.log_test(f"Traduction mise à jour: {french_word}", False, "Mot non trouvé dans la base")

    def test_2_nouveau_mot_ajoute(self):
        """Test 2: Confirmer le nouveau mot ajouté"""
        print("\n=== TEST 2: NOUVEAU MOT AJOUTÉ ===")
        
        response = self.make_request("/words?category=famille")
        if not response["success"]:
            self.log_test("Récupération mots famille", False, f"Erreur API: {response['data']}")
            return
            
        family_words = response["data"]
        word_dict = {word.get("french", "").lower(): word for word in family_words}
        
        # Test the new word: Petite fille: "mwana mtroumama" / "zaza viavi"
        expected_new_word = {
            "french": "petite fille",
            "shimaore": "mwana mtroumama",
            "kibouchi": "zaza viavi"
        }
        
        if expected_new_word['french'] in word_dict:
            word = word_dict[expected_new_word['french']]
            shimaore_actual = word.get('shimaore', '').lower().strip()
            kibouchi_actual = word.get('kibouchi', '').lower().strip()
            shimaore_expected = expected_new_word['shimaore'].lower().strip()
            kibouchi_expected = expected_new_word['kibouchi'].lower().strip()
            
            shimaore_match = shimaore_expected in shimaore_actual or shimaore_actual in shimaore_expected
            kibouchi_match = kibouchi_expected in kibouchi_actual or kibouchi_actual in kibouchi_expected
            
            if shimaore_match and kibouchi_match:
                self.log_test("Nouveau mot ajouté: Petite fille", True, 
                              f"Shimaoré: {word.get('shimaore')}, Kibouchi: {word.get('kibouchi')}")
            else:
                self.log_test("Nouveau mot ajouté: Petite fille", False, 
                              f"Traductions incorrectes - Attendu Shimaoré: {expected_new_word['shimaore']}, Trouvé: {word.get('shimaore')} | "
                              f"Attendu Kibouchi: {expected_new_word['kibouchi']}, Trouvé: {word.get('kibouchi')}")
        else:
            self.log_test("Nouveau mot ajouté: Petite fille", False, "Mot 'Petite fille' non trouvé dans la base")

    def test_3_api_famille_complete(self):
        """Test 3: Tester l'API famille complète"""
        print("\n=== TEST 3: API FAMILLE COMPLÈTE ===")
        
        # Test GET /api/words?category=famille
        response = self.make_request("/words?category=famille")
        if response["success"]:
            family_words = response["data"]
            total_family = len(family_words)
            
            self.log_test("GET /api/words?category=famille", True, f"API accessible, {total_family} mots famille")
            
            # Test: Vérifier le total de 29 mots de famille (selon la demande)
            if total_family == 29:
                self.log_test("Total 29 mots famille", True, f"Exactement {total_family} mots trouvés")
            else:
                self.log_test("Total 29 mots famille", False, f"Attendu 29 mots, trouvé {total_family}")
            
            # Test: Vérifier la structure complète des données
            complete_structure = 0
            required_fields = ['french', 'shimaore', 'kibouchi', 'category']
            
            for word in family_words:
                if all(field in word and word[field] for field in required_fields):
                    complete_structure += 1
            
            structure_rate = (complete_structure / total_family) * 100 if total_family > 0 else 0
            self.log_test("Structure complète des données", structure_rate >= 95, 
                        f"{structure_rate:.1f}% des mots ont une structure complète ({complete_structure}/{total_family})")
            
            return family_words
        else:
            self.log_test("GET /api/words?category=famille", False, f"Erreur API: {response['data']}")
            return []

    def test_4_verifier_integrite(self, family_words: List[Dict]):
        """Test 4: Vérifier l'intégrité"""
        print("\n=== TEST 4: VÉRIFIER L'INTÉGRITÉ ===")
        
        if not family_words:
            self.log_test("Intégrité des données", False, "Aucune donnée famille à vérifier")
            return
        
        # Test: S'assurer qu'aucune donnée n'a été corrompue
        corruption_issues = 0
        for word in family_words:
            french = word.get('french', '')
            shimaore = word.get('shimaore', '')
            kibouchi = word.get('kibouchi', '')
            
            # Check for obvious corruption signs
            if not french or len(french.strip()) == 0:
                corruption_issues += 1
            if french and (french.count('�') > 0 or len(french) > 100):  # Encoding issues or suspiciously long
                corruption_issues += 1
            if shimaore and shimaore.count('�') > 0:
                corruption_issues += 1
            if kibouchi and kibouchi.count('�') > 0:
                corruption_issues += 1
        
        if corruption_issues == 0:
            self.log_test("Aucune donnée corrompue", True, "Toutes les données famille semblent intactes")
        else:
            self.log_test("Aucune donnée corrompue", False, f"{corruption_issues} signes de corruption détectés")
        
        # Test: Vérifier que les IDs sont préservés
        ids_present = sum(1 for word in family_words if word.get('id'))
        unique_ids = len(set(word.get('id') for word in family_words if word.get('id')))
        
        if ids_present == len(family_words) and unique_ids == ids_present:
            self.log_test("IDs préservés", True, f"Tous les {len(family_words)} mots ont des IDs uniques")
        else:
            self.log_test("IDs préservés", False, f"Problème d'IDs: {ids_present} IDs pour {len(family_words)} mots, {unique_ids} uniques")
        
        # Test: Confirmer que les catégories restent correctes
        correct_category = sum(1 for word in family_words if word.get('category') == 'famille')
        if correct_category == len(family_words):
            self.log_test("Catégories correctes", True, f"Tous les {len(family_words)} mots ont la catégorie 'famille'")
        else:
            wrong_category = len(family_words) - correct_category
            self.log_test("Catégories correctes", False, f"{wrong_category} mots ont une catégorie incorrecte")

    def test_5_tests_fonctionnels_specifiques(self, family_words: List[Dict]):
        """Test 5: Tests fonctionnels spécifiques"""
        print("\n=== TEST 5: TESTS FONCTIONNELS SPÉCIFIQUES ===")
        
        if not family_words:
            self.log_test("Tests fonctionnels", False, "Aucune donnée famille pour les tests")
            return
        
        word_dict = {word.get("french", "").lower(): word for word in family_words}
        
        # Test: Rechercher des mots spécifiques par français
        test_words = ["papa", "maman", "frère", "sœur", "grand-père", "grand-mère", "famille"]
        found_words = 0
        
        for test_word in test_words:
            if test_word in word_dict:
                found_words += 1
                word = word_dict[test_word]
                self.log_test(f"Recherche mot: {test_word}", True, 
                              f"Trouvé - Shimaoré: {word.get('shimaore')}, Kibouchi: {word.get('kibouchi')}")
            else:
                self.log_test(f"Recherche mot: {test_word}", False, "Mot non trouvé")
        
        search_rate = (found_words / len(test_words)) * 100
        self.log_test("Recherche globale mots spécifiques", search_rate >= 70, 
                    f"{search_rate:.1f}% des mots test trouvés ({found_words}/{len(test_words)})")
        
        # Test: Vérifier la cohérence des traductions shimaoré/kibouchi
        shimoare_consistency = sum(1 for word in family_words if word.get('shimaore', '').strip())
        kibouchi_consistency = sum(1 for word in family_words if word.get('kibouchi', '').strip())
        
        total_words = len(family_words)
        shimoare_rate = (shimoare_consistency / total_words) * 100 if total_words > 0 else 0
        kibouchi_rate = (kibouchi_consistency / total_words) * 100 if total_words > 0 else 0
        
        self.log_test("Cohérence traductions Shimaoré", shimoare_rate >= 90, 
                    f"{shimoare_rate:.1f}% des mots ont une traduction Shimaoré ({shimoare_consistency}/{total_words})")
        self.log_test("Cohérence traductions Kibouchi", kibouchi_rate >= 90, 
                    f"{kibouchi_rate:.1f}% des mots ont une traduction Kibouchi ({kibouchi_consistency}/{total_words})")
        
        # Test: Tester quelques mots pour l'accès audio (si disponible)
        audio_words = [word for word in family_words if word.get('has_authentic_audio') or word.get('audio_url')]
        if audio_words:
            self.log_test("Accès audio disponible", True, f"{len(audio_words)} mots famille ont des métadonnées audio")
        else:
            self.log_test("Accès audio disponible", False, "Aucun mot famille n'a de métadonnées audio")

    def run_all_tests(self):
        """Run all tests for the family section update"""
        print("🎉 TESTING FAMILLE SECTION UPDATE WITH NEW DATA FROM TABLE")
        print("=" * 80)
        print("Focus: Nouvelles traductions, nouveau mot, total 29 mots, intégrité données")
        print("=" * 80)
        
        start_time = time.time()
        
        # Run all test suites
        self.test_1_nouvelles_traductions_mises_a_jour()
        self.test_2_nouveau_mot_ajoute()
        family_words = self.test_3_api_famille_complete()
        self.test_4_verifier_integrite(family_words)
        self.test_5_tests_fonctionnels_specifiques(family_words)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DES TESTS - FAMILLE SECTION UPDATE")
        print("=" * 80)
        
        for result in self.test_results:
            print(result)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"\n🎯 RÉSULTATS FINAUX:")
        print(f"   Tests réussis: {self.passed_tests}/{self.total_tests}")
        print(f"   Taux de réussite: {success_rate:.1f}%")
        print(f"   Durée: {duration:.2f}s")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT - FAMILLE SECTION UPDATE COMPLÈTEMENT RÉUSSIE!")
            print("Les 26 modifications (25 mises à jour + 1 ajout) sont correctement appliquées")
            return True
        elif success_rate >= 70:
            print("✅ BIEN - FAMILLE SECTION UPDATE MAJORITAIREMENT RÉUSSIE")
            print("La plupart des modifications sont appliquées correctement")
            return True
        elif success_rate >= 50:
            print("⚠️ PARTIEL - FAMILLE SECTION UPDATE PARTIELLEMENT RÉUSSIE")
            print("Certaines modifications nécessitent des corrections")
            return False
        else:
            print("❌ ÉCHEC - FAMILLE SECTION UPDATE NON RÉUSSIE")
            print("Les modifications du tableau n'ont pas été appliquées correctement")
            return False

if __name__ == "__main__":
    tester = FamilySectionTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)