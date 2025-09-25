#!/usr/bin/env python3
"""
Backend Testing Suite for Mayotte Language Learning API
Testing French formatting corrections after database restoration
Focus: Verify proper French accents, capitalization, and professional formatting
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

    def test_1_corrections_accents_remises(self):
        """Test 1: Vérifier que les corrections d'accents ont été remises"""
        print("\n=== TEST 1: CORRECTIONS D'ACCENTS REMISES ===")
        
        # Get all words
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        self.log_test("Récupération des mots", True, f"{len(words)} mots trouvés")
        
        # Create word lookup dictionary (case-sensitive for accent testing)
        word_dict = {word.get("french", ""): word for word in words}
        
        # Test: Vérifier que "Frère" (avec accent) existe maintenant au lieu de "frere"
        if "Frère" in word_dict:
            self.log_test("Frère avec accent existe", True, f"Trouvé: 'Frère'")
        else:
            # Check if exists without accent
            if "frere" in [w.lower() for w in word_dict.keys()]:
                self.log_test("Frère avec accent existe", False, "Trouvé 'frere' sans accent au lieu de 'Frère'")
            else:
                self.log_test("Frère avec accent existe", False, "Mot 'Frère' non trouvé")
        
        # Test: Vérifier "École", "Tête", "Étoile", "Tempête" avec accents appropriés
        mots_avec_accents = ["École", "Tête", "Étoile", "Tempête"]
        for mot in mots_avec_accents:
            if mot in word_dict:
                self.log_test(f"{mot} avec accent existe", True, f"Trouvé: '{mot}'")
            else:
                # Check if exists without accent
                mot_sans_accent = mot.lower().replace('é', 'e').replace('è', 'e').replace('ê', 'e')
                if any(w.lower() == mot_sans_accent for w in word_dict.keys()):
                    self.log_test(f"{mot} avec accent existe", False, f"Trouvé sans accent au lieu de '{mot}'")
                else:
                    self.log_test(f"{mot} avec accent existe", False, f"Mot '{mot}' non trouvé")
        
        # Test: Vérifier "Grand-père", "Grand-mère" avec accents et tirets
        mots_composes = ["Grand-père", "Grand-mère"]
        for mot in mots_composes:
            if mot in word_dict:
                self.log_test(f"{mot} avec accent et tiret existe", True, f"Trouvé: '{mot}'")
            else:
                # Check variants
                variants_found = []
                for w in word_dict.keys():
                    if "grand" in w.lower() and ("père" in w.lower() or "mère" in w.lower()):
                        variants_found.append(w)
                
                if variants_found:
                    self.log_test(f"{mot} avec accent et tiret existe", False, f"Variantes trouvées: {variants_found}")
                else:
                    self.log_test(f"{mot} avec accent et tiret existe", False, f"Mot '{mot}' non trouvé")

    def test_2_capitalisation_appliquee(self):
        """Test 2: Vérifier que la capitalisation a été appliquée"""
        print("\n=== TEST 2: CAPITALISATION APPLIQUÉE ===")
        
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        word_dict = {word.get("french", ""): word for word in words}
        
        # Test: Vérifier que tous les mots français commencent par une majuscule
        sample_words = ["Famille", "Papa", "Maman", "Bonjour", "Merci"]
        
        for mot in sample_words:
            if mot in word_dict:
                self.log_test(f"Capitalisation correcte: {mot}", True, f"Trouvé: '{mot}'")
            else:
                # Check if exists with different capitalization
                found_variant = None
                for french_word in word_dict.keys():
                    if french_word.lower() == mot.lower():
                        found_variant = french_word
                        break
                
                if found_variant:
                    is_correct = found_variant[0].isupper()
                    self.log_test(f"Capitalisation correcte: {mot}", is_correct, 
                                f"Trouvé comme '{found_variant}' - {'correct' if is_correct else 'incorrect'}")
                else:
                    self.log_test(f"Capitalisation correcte: {mot}", False, "Mot non trouvé")
        
        # Test: Vérifier les mots composés: "Comment ça va", "Ça va bien"
        mots_composes = ["Comment ça va", "Ça va bien"]
        for mot in mots_composes:
            if mot in word_dict:
                self.log_test(f"Capitalisation mot composé: {mot}", True, f"Trouvé: '{mot}'")
            else:
                # Check variants
                variants_found = []
                for w in word_dict.keys():
                    if mot.lower() in w.lower():
                        variants_found.append(w)
                
                if variants_found:
                    correct_variants = [v for v in variants_found if v[0].isupper()]
                    self.log_test(f"Capitalisation mot composé: {mot}", len(correct_variants) > 0, 
                                f"Variantes trouvées: {variants_found}")
                else:
                    self.log_test(f"Capitalisation mot composé: {mot}", False, f"Mot '{mot}' non trouvé")
        
        # Test général: Vérifier le taux de capitalisation global
        capitalization_correct = 0
        total_checked = 0
        
        for word in words[:100]:  # Check first 100 words as sample
            french_word = word.get('french', '')
            if french_word and len(french_word) > 0:
                total_checked += 1
                if french_word[0].isupper():
                    capitalization_correct += 1
        
        if total_checked > 0:
            rate = (capitalization_correct / total_checked) * 100
            self.log_test("Taux de capitalisation global", rate >= 90, 
                        f"{rate:.1f}% des mots correctement capitalisés ({capitalization_correct}/{total_checked})")
        else:
            self.log_test("Taux de capitalisation global", False, "Aucun mot à vérifier")

    def test_3_mots_speciaux(self):
        """Test 3: Vérifier les mots spéciaux"""
        print("\n=== TEST 3: MOTS SPÉCIAUX ===")
        
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        word_dict = {word.get("french", ""): word for word in words}
        
        # Test: Vérifier "Œil" (avec caractère spécial)
        if "Œil" in word_dict:
            self.log_test("Œil avec caractère spécial existe", True, f"Trouvé: 'Œil'")
        else:
            # Check variants
            variants_found = []
            for w in word_dict.keys():
                if "œil" in w.lower() or "oeil" in w.lower():
                    variants_found.append(w)
            
            if variants_found:
                correct_variants = [v for v in variants_found if "Œ" in v]
                self.log_test("Œil avec caractère spécial existe", len(correct_variants) > 0, 
                            f"Variantes trouvées: {variants_found}")
            else:
                self.log_test("Œil avec caractère spécial existe", False, "Mot 'Œil' non trouvé")
        
        # Test: Vérifier "Petit garçon" (avec accent sur garçon)
        if "Petit garçon" in word_dict:
            self.log_test("Petit garçon avec accent existe", True, f"Trouvé: 'Petit garçon'")
        else:
            # Check variants
            variants_found = []
            for w in word_dict.keys():
                if "petit" in w.lower() and "garçon" in w.lower():
                    variants_found.append(w)
            
            if variants_found:
                correct_variants = [v for v in variants_found if "ç" in v]
                self.log_test("Petit garçon avec accent existe", len(correct_variants) > 0, 
                            f"Variantes trouvées: {variants_found}")
            else:
                # Check if exists without accent
                variants_sans_accent = []
                for w in word_dict.keys():
                    if "petit" in w.lower() and "garcon" in w.lower():
                        variants_sans_accent.append(w)
                
                if variants_sans_accent:
                    self.log_test("Petit garçon avec accent existe", False, 
                                f"Trouvé sans accent: {variants_sans_accent}")
                else:
                    self.log_test("Petit garçon avec accent existe", False, "Mot 'Petit garçon' non trouvé")

    def test_4_integrite_complete(self):
        """Test 4: Vérifier l'intégrité complète"""
        print("\n=== TEST 4: INTÉGRITÉ COMPLÈTE ===")
        
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        total_words = len(words)
        
        # Test: Vérifier que le total reste 565 mots
        expected_total = 565
        self.log_test(f"Total de {expected_total} mots maintenu", total_words == expected_total, 
                     f"Trouvé: {total_words} mots (attendu: {expected_total})")
        
        # Test: Vérifier que les traductions shimaoré et kibouchi sont intactes
        complete_translations = 0
        for word in words:
            shimaore = word.get('shimaore', '').strip()
            kibouchi = word.get('kibouchi', '').strip()
            
            if shimaore and kibouchi:
                complete_translations += 1
        
        completion_rate = (complete_translations / total_words) * 100 if total_words > 0 else 0
        self.log_test("Traductions shimaoré et kibouchi intactes", completion_rate >= 95, 
                    f"{completion_rate:.1f}% des mots ont des traductions complètes ({complete_translations}/{total_words})")
        
        # Test: Vérifier que les corrections précédentes sont préservées (escargot: "kowa", etc.)
        corrections_preservees = [
            ("escargot", "kowa", "shimaore"),
            # Add other known corrections here
        ]
        
        word_dict = {word.get("french", "").lower(): word for word in words}
        
        for mot_french, traduction_attendue, langue in corrections_preservees:
            if mot_french in word_dict:
                word = word_dict[mot_french]
                traduction_actuelle = word.get(langue, "").lower()
                
                if traduction_attendue.lower() in traduction_actuelle:
                    self.log_test(f"Correction préservée: {mot_french} -> {traduction_attendue}", True, 
                                f"{langue}: '{word.get(langue, '')}'")
                else:
                    self.log_test(f"Correction préservée: {mot_french} -> {traduction_attendue}", False, 
                                f"{langue}: '{word.get(langue, '')}' (attendu: {traduction_attendue})")
            else:
                self.log_test(f"Correction préservée: {mot_french} -> {traduction_attendue}", False, 
                            f"Mot '{mot_french}' non trouvé")

    def test_5_tests_api(self):
        """Test 5: Tests API"""
        print("\n=== TEST 5: TESTS API ===")
        
        # Test: GET /api/words (vérifier formatage)
        response = self.make_request("/words")
        if response["success"]:
            words = response["data"]
            self.log_test("GET /api/words", True, f"Récupéré {len(words)} mots avec formatage")
            
            # Vérifier quelques mots avec formatage professionnel
            sample_words = words[:10]
            formatting_issues = 0
            
            for word in sample_words:
                french = word.get('french', '')
                if french:
                    # Check basic formatting
                    if not french[0].isupper():
                        formatting_issues += 1
                    if french.endswith(' ') or french.startswith(' '):
                        formatting_issues += 1
            
            formatting_quality = ((len(sample_words) - formatting_issues) / len(sample_words) * 100) if sample_words else 0
            self.log_test("Formatage professionnel dans API", formatting_quality >= 90, 
                        f"{formatting_quality:.1f}% qualité formatage")
        else:
            self.log_test("GET /api/words", False, f"Erreur: {response['data']}")
        
        # Test: GET /api/words?category=famille (vérifier nouveaux mots avec bon formatage)
        response = self.make_request("/words?category=famille")
        if response["success"]:
            famille_words = response["data"]
            self.log_test("GET /api/words?category=famille", True, f"Récupéré {len(famille_words)} mots famille")
            
            # Vérifier formatage des mots famille
            mots_famille_attendus = ["Grand-père", "Grand-mère", "Frère"]
            mots_trouves_formates = []
            
            for word in famille_words:
                french = word.get('french', '')
                if any(mot.lower() in french.lower() for mot in mots_famille_attendus):
                    if french[0].isupper():
                        mots_trouves_formates.append(french)
            
            self.log_test("Formatage mots famille", len(mots_trouves_formates) >= 2, 
                        f"Mots famille bien formatés trouvés: {mots_trouves_formates}")
        else:
            self.log_test("GET /api/words?category=famille", False, f"Erreur: {response['data']}")
        
        # Test: Recherche spécifique de quelques mots corrigés
        mots_corriges = ["Frère", "École", "Étoile", "Grand-père", "Œil"]
        
        response = self.make_request("/words")
        if response["success"]:
            words = response["data"]
            word_dict = {word.get("french", ""): word for word in words}
            
            mots_corriges_trouves = 0
            for mot in mots_corriges:
                if mot in word_dict:
                    mots_corriges_trouves += 1
                    word_data = word_dict[mot]
                    self.log_test(f"Recherche mot corrigé: {mot}", True, 
                                f"Trouvé avec traductions: {word_data.get('shimaore', 'N/A')} / {word_data.get('kibouchi', 'N/A')}")
                else:
                    self.log_test(f"Recherche mot corrigé: {mot}", False, "Mot non trouvé avec formatage correct")
            
            self.log_test("Recherche globale mots corrigés", mots_corriges_trouves >= 3, 
                        f"Trouvé {mots_corriges_trouves}/{len(mots_corriges)} mots corrigés")
        else:
            self.log_test("Recherche mots corrigés", False, f"Erreur API: {response['data']}")

    def run_all_tests(self):
        """Run all tests"""
        print("🧪 DÉBUT DES TESTS - FORMATAGE FRANÇAIS APRÈS CORRECTION")
        print("=" * 80)
        print("Focus: Vérifier accents remis, capitalisation, mots spéciaux, intégrité 565 mots")
        print("=" * 80)
        
        start_time = time.time()
        
        # Run all test suites
        self.test_1_corrections_accents_remises()
        self.test_2_capitalisation_appliquee()
        self.test_3_mots_speciaux()
        self.test_4_integrite_complete()
        self.test_5_tests_api()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DES TESTS - FORMATAGE FRANÇAIS")
        print("=" * 80)
        
        for result in self.test_results:
            print(result)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"\n🎯 RÉSULTATS FINAUX:")
        print(f"   Tests réussis: {self.passed_tests}/{self.total_tests}")
        print(f"   Taux de réussite: {success_rate:.1f}%")
        print(f"   Durée: {duration:.2f}s")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT - FORMATAGE FRANÇAIS PROFESSIONNEL ET CORRECT!")
            return True
        elif success_rate >= 70:
            print("✅ BIEN - FORMATAGE FRANÇAIS MAJORITAIREMENT CORRECT")
            return True
        elif success_rate >= 50:
            print("⚠️ PARTIEL - FORMATAGE FRANÇAIS PARTIELLEMENT CORRECT")
            return False
        else:
            print("❌ ÉCHEC - FORMATAGE FRANÇAIS NON PROFESSIONNEL")
            return False

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)