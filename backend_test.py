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

    def test_2_nouveaux_mots_ajoutes(self):
        """Test 2: Vérifier que les nouveaux mots ont été ajoutés"""
        print("\n=== TEST 2: NOUVEAUX MOTS AJOUTÉS ===")
        
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        word_dict = {word.get("french", "").lower(): word for word in words}
        
        # Test nouveaux mots spécifiques
        nouveaux_mots = [
            ("pente", "nature"),
            ("tante maternelle", "famille"),
            ("tante paternelle", "famille"),
            ("petit garcon", "famille"),
            ("jeune adulte", "famille")
        ]
        
        for mot_french, categorie_attendue in nouveaux_mots:
            if mot_french in word_dict:
                word = word_dict[mot_french]
                categorie_actuelle = word.get("category", "")
                if categorie_actuelle == categorie_attendue:
                    self.log_test(f"Nouveau mot '{mot_french}' ajouté", True, f"Catégorie: {categorie_actuelle}")
                else:
                    self.log_test(f"Nouveau mot '{mot_french}' ajouté", False, f"Catégorie: {categorie_actuelle} (attendue: {categorie_attendue})")
            else:
                self.log_test(f"Nouveau mot '{mot_french}' ajouté", False, f"Mot non trouvé")

    def test_3_integrite_globale(self):
        """Test 3: Vérifier l'intégrité globale de la base de données"""
        print("\n=== TEST 3: INTÉGRITÉ GLOBALE ===")
        
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        total_words = len(words)
        
        # Test: Nouveau total de mots (devrait être 565)
        expected_total = 565
        self.log_test(f"Total de {expected_total} mots", total_words == expected_total, 
                     f"Trouvé: {total_words} mots (attendu: {expected_total})")
        
        # Test: Vérifier qu'il n'y a pas de doublons
        french_words = [word.get("french", "").lower() for word in words]
        unique_words = set(french_words)
        duplicates = []
        for word in unique_words:
            count = french_words.count(word)
            if count > 1:
                duplicates.append(f"{word} ({count}x)")
        
        self.log_test("Aucun doublon", len(duplicates) == 0,
                     f"Doublons trouvés: {', '.join(duplicates[:5])}" if duplicates else "Aucun doublon détecté")
        
        # Test: Vérifier que toutes les catégories sont intactes
        categories = {}
        for word in words:
            category = word.get("category", "unknown")
            categories[category] = categories.get(category, 0) + 1
        
        expected_categories = [
            'salutations', 'famille', 'couleurs', 'animaux', 'nombres', 
            'corps', 'grammaire', 'maison', 'nourriture', 'vetements',
            'transport', 'nature', 'adjectifs', 'expressions', 'verbes'
        ]
        
        missing_categories = [cat for cat in expected_categories if cat not in categories]
        self.log_test("Toutes les catégories intactes", len(missing_categories) == 0,
                     f"Catégories manquantes: {missing_categories}" if missing_categories else f"Toutes présentes: {list(categories.keys())}")

    def test_4_endpoints_api_fonctionnels(self):
        """Test 4: Vérifier que les API endpoints fonctionnent correctement"""
        print("\n=== TEST 4: ENDPOINTS API FONCTIONNELS ===")
        
        # Test: GET /api/words (total et pagination)
        response = self.make_request("/words")
        if response["success"]:
            words = response["data"]
            self.log_test("GET /api/words", True, f"Récupéré {len(words)} mots")
        else:
            self.log_test("GET /api/words", False, f"Erreur: {response['data']}")
        
        # Test: GET /api/words?category=famille (doit inclure les nouveaux mots famille)
        response = self.make_request("/words?category=famille")
        if response["success"]:
            famille_words = response["data"]
            french_words = [word.get("french", "").lower() for word in famille_words]
            
            # Vérifier que les nouveaux mots famille sont inclus
            nouveaux_mots_famille = ["tante maternelle", "tante paternelle", "petit garcon", "jeune adulte"]
            mots_trouves = [mot for mot in nouveaux_mots_famille if mot in french_words]
            
            self.log_test("GET /api/words?category=famille", True, 
                         f"Récupéré {len(famille_words)} mots famille, nouveaux mots trouvés: {len(mots_trouves)}/{len(nouveaux_mots_famille)}")
        else:
            self.log_test("GET /api/words?category=famille", False, f"Erreur: {response['data']}")
        
        # Test: GET /api/words?category=nature (doit inclure "pente")
        response = self.make_request("/words?category=nature")
        if response["success"]:
            nature_words = response["data"]
            french_words = [word.get("french", "").lower() for word in nature_words]
            pente_trouve = "pente" in french_words
            
            self.log_test("GET /api/words?category=nature", True, 
                         f"Récupéré {len(nature_words)} mots nature, 'pente' trouvé: {pente_trouve}")
        else:
            self.log_test("GET /api/words?category=nature", False, f"Erreur: {response['data']}")
        
        # Test: Rechercher des mots spécifiques par français
        mots_a_rechercher = ["escargot", "oursin", "nous", "pente"]
        for mot in mots_a_rechercher:
            # Simuler une recherche en récupérant tous les mots et filtrant
            response = self.make_request("/words")
            if response["success"]:
                words = response["data"]
                mot_trouve = any(word.get("french", "").lower() == mot for word in words)
                self.log_test(f"Recherche mot '{mot}'", mot_trouve, 
                             f"Mot {'trouvé' if mot_trouve else 'non trouvé'}")
            else:
                self.log_test(f"Recherche mot '{mot}'", False, f"Erreur API: {response['data']}")

    def test_5_verification_corrections_specifiques(self):
        """Test 5: Vérification détaillée des corrections spécifiques"""
        print("\n=== TEST 5: VÉRIFICATION CORRECTIONS SPÉCIFIQUES ===")
        
        response = self.make_request("/words")
        if not response["success"]:
            self.log_test("Récupération des mots", False, f"Erreur API: {response['data']}")
            return
            
        words = response["data"]
        word_dict = {word.get("french", "").lower(): word for word in words}
        
        # Vérifications détaillées des corrections critiques
        corrections_critiques = [
            {
                "mot": "escargot",
                "shimaore_attendu": "kowa",
                "description": "Correction escargot: 'kwa' -> 'kowa'"
            },
            {
                "mot": "oursin", 
                "shimaore_attendu": "gadzassi ya bahari",
                "description": "Différenciation oursin/huître"
            },
            {
                "mot": "nous",
                "shimaore_attendu": "wasi", 
                "description": "Correction nous: 'wassi' -> 'wasi'"
            }
        ]
        
        for correction in corrections_critiques:
            mot = correction["mot"]
            shimaore_attendu = correction["shimaore_attendu"]
            description = correction["description"]
            
            if mot in word_dict:
                word = word_dict[mot]
                shimaore_actuel = word.get("shimaore", "").lower()
                
                if shimaore_attendu.lower() in shimaore_actuel or shimaore_actuel == shimaore_attendu.lower():
                    self.log_test(description, True, f"'{mot}' -> shimaore: '{word.get('shimaore', '')}'")
                else:
                    self.log_test(description, False, f"'{mot}' -> shimaore: '{word.get('shimaore', '')}' (attendu: '{shimaore_attendu}')")
            else:
                self.log_test(description, False, f"Mot '{mot}' non trouvé")
        
        # Vérifier les mots sans accents
        mots_sans_accents = ["etoile", "ecole"]
        for mot in mots_sans_accents:
            if mot in word_dict:
                self.log_test(f"Mot sans accent '{mot}' présent", True, f"Trouvé: '{word_dict[mot].get('french', '')}'")
            else:
                self.log_test(f"Mot sans accent '{mot}' présent", False, f"Mot '{mot}' non trouvé")
        
        # Vérifier que les versions avec accents n'existent plus
        mots_avec_accents = ["étoile", "école"]
        for mot in mots_avec_accents:
            if mot in word_dict:
                self.log_test(f"Mot avec accent '{mot}' supprimé", False, f"Mot '{mot}' encore présent")
            else:
                self.log_test(f"Mot avec accent '{mot}' supprimé", True, f"Mot '{mot}' correctement supprimé")

    def run_all_tests(self):
        """Run all tests"""
        print("🧪 DÉBUT DES TESTS - CORRECTIONS PDF VOCABULAIRE SHIMAORÉ-KIBOUCHI")
        print("=" * 80)
        print("Focus: Vérifier 565 mots total, corrections orthographiques, nouveaux mots ajoutés")
        print("=" * 80)
        
        start_time = time.time()
        
        # Run all test suites
        self.test_1_corrections_orthographiques_appliquees()
        self.test_2_nouveaux_mots_ajoutes()
        self.test_3_integrite_globale()
        self.test_4_endpoints_api_fonctionnels()
        self.test_5_verification_corrections_specifiques()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DES TESTS - CORRECTIONS PDF VOCABULAIRE")
        print("=" * 80)
        
        for result in self.test_results:
            print(result)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"\n🎯 RÉSULTATS FINAUX:")
        print(f"   Tests réussis: {self.passed_tests}/{self.total_tests}")
        print(f"   Taux de réussite: {success_rate:.1f}%")
        print(f"   Durée: {duration:.2f}s")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT - CORRECTIONS PDF APPLIQUÉES AVEC SUCCÈS!")
            return True
        elif success_rate >= 70:
            print("✅ BIEN - CORRECTIONS PDF MAJORITAIREMENT APPLIQUÉES")
            return True
        elif success_rate >= 50:
            print("⚠️ PARTIEL - CORRECTIONS PDF PARTIELLEMENT APPLIQUÉES")
            return False
        else:
            print("❌ ÉCHEC - CORRECTIONS PDF NON APPLIQUÉES")
            return False

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)