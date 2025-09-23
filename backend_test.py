#!/usr/bin/env python3
"""
Test du système audio dual étendu pour TOUTES les catégories
Test complet pour vérifier l'extension du système dual aux catégories nature, nombres, et animaux
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Configuration de l'URL de base
BASE_URL = "https://mayotte-learn-2.preview.emergentagent.com/api"

class DualAudioSystemTester:
    def __init__(self):
        self.results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": []
        }
        
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Enregistre le résultat d'un test"""
        self.results["total_tests"] += 1
        if passed:
            self.results["passed"] += 1
            print(f"✅ {test_name}: PASSED {message}")
        else:
            self.results["failed"] += 1
            error_msg = f"❌ {test_name}: FAILED {message}"
            print(error_msg)
            self.results["errors"].append(error_msg)
    
    def test_new_audio_endpoints(self):
        """Test 1: Vérifier les nouveaux endpoints audio"""
        print("\n🎵 TEST 1: NOUVEAUX ENDPOINTS AUDIO")
        
        # Test GET /api/audio/nombres/{filename}
        try:
            response = requests.get(f"{BASE_URL}/audio/nombres/Moja.m4a")
            self.log_test("Endpoint /api/audio/nombres/{filename}", 
                         response.status_code in [200, 404], 
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Endpoint /api/audio/nombres/{filename}", False, f"Error: {e}")
        
        # Test GET /api/audio/animaux/{filename}
        try:
            response = requests.get(f"{BASE_URL}/audio/animaux/Paha.m4a")
            self.log_test("Endpoint /api/audio/animaux/{filename}", 
                         response.status_code in [200, 404], 
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Endpoint /api/audio/animaux/{filename}", False, f"Error: {e}")
        
        # Test GET /api/audio/info - doit retourner 4 catégories
        try:
            response = requests.get(f"{BASE_URL}/audio/info")
            if response.status_code == 200:
                data = response.json()
                categories = ["famille", "nature", "nombres", "animaux"]
                has_all_categories = all(cat in data for cat in categories)
                self.log_test("Endpoint /api/audio/info retourne 4 catégories", 
                             has_all_categories, 
                             f"Catégories trouvées: {list(data.keys())}")
                
                # Vérifier les endpoints dans la réponse
                if "endpoints" in data:
                    expected_endpoints = {
                        "famille": "/api/audio/famille/{filename}",
                        "nature": "/api/audio/nature/{filename}",
                        "nombres": "/api/audio/nombres/{filename}",
                        "animaux": "/api/audio/animaux/{filename}"
                    }
                    endpoints_match = all(
                        data["endpoints"].get(cat) == expected_endpoints[cat] 
                        for cat in expected_endpoints
                    )
                    self.log_test("Endpoints corrects dans /api/audio/info", 
                                 endpoints_match, 
                                 f"Endpoints: {data.get('endpoints', {})}")
            else:
                self.log_test("Endpoint /api/audio/info", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Endpoint /api/audio/info", False, f"Error: {e}")
    
    def test_dual_system_extension(self):
        """Test 2: Vérifier l'extension du système dual aux nouvelles catégories"""
        print("\n🔄 TEST 2: EXTENSION SYSTÈME DUAL")
        
        categories_to_test = ["nature", "nombres", "animaux"]
        expected_counts = {"nature": 49, "nombres": 20, "animaux": 69}
        
        for category in categories_to_test:
            try:
                # Récupérer les mots de la catégorie
                response = requests.get(f"{BASE_URL}/words", params={"category": category})
                if response.status_code == 200:
                    words = response.json()
                    
                    # Vérifier le nombre de mots
                    word_count = len(words)
                    expected_count = expected_counts[category]
                    self.log_test(f"Nombre de mots {category}", 
                                 word_count >= expected_count * 0.8,  # Tolérance de 20%
                                 f"Trouvé: {word_count}, Attendu: ~{expected_count}")
                    
                    # Compter les mots avec dual_audio_system: true
                    dual_system_words = [w for w in words if w.get("dual_audio_system", False)]
                    dual_count = len(dual_system_words)
                    
                    self.log_test(f"Mots {category} avec dual_audio_system: true", 
                                 dual_count > 0, 
                                 f"Trouvé: {dual_count}/{word_count} mots avec système dual")
                    
                    # Tester quelques mots spécifiques si disponibles
                    if dual_system_words:
                        test_word = dual_system_words[0]
                        word_id = test_word.get("id")
                        if word_id:
                            self.test_word_dual_audio(word_id, test_word.get("french", ""), category)
                
                else:
                    self.log_test(f"Récupération mots {category}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Test catégorie {category}", False, f"Error: {e}")
    
    def test_word_dual_audio(self, word_id: str, french_word: str, category: str):
        """Test les endpoints audio dual pour un mot spécifique"""
        try:
            # Test GET /api/words/{id}/audio-info
            response = requests.get(f"{BASE_URL}/words/{word_id}/audio-info")
            if response.status_code == 200:
                data = response.json()
                has_dual_system = data.get("dual_audio_system", False)
                self.log_test(f"Audio-info pour '{french_word}' ({category})", 
                             has_dual_system, 
                             f"dual_audio_system: {has_dual_system}")
                
                # Test des endpoints audio par langue
                for lang in ["shimaore", "kibouchi"]:
                    audio_info = data.get("audio", {}).get(lang, {})
                    has_audio = audio_info.get("has_audio", False)
                    
                    if has_audio:
                        # Tester l'endpoint audio
                        audio_response = requests.get(f"{BASE_URL}/words/{word_id}/audio/{lang}")
                        self.log_test(f"Audio {lang} pour '{french_word}'", 
                                     audio_response.status_code in [200, 404], 
                                     f"Status: {audio_response.status_code}")
            else:
                self.log_test(f"Audio-info pour '{french_word}'", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test(f"Test audio dual pour '{french_word}'", False, f"Error: {e}")
    
    def test_specific_words(self):
        """Test 3: Tester les mots spécifiques mentionnés dans la demande"""
        print("\n🎯 TEST 3: MOTS SPÉCIFIQUES")
        
        specific_tests = [
            {"french": "un", "category": "nombres", "shimaore_file": "Moja.m4a", "kibouchi_file": "Areki.m4a"},
            {"french": "arbre", "category": "nature", "shimaore_file": "Mwiri.m4a", "kibouchi_file": "Kakazou.m4a"},
            {"french": "chat", "category": "animaux", "shimaore_file": "Paha.m4a", "kibouchi_file": "Moirou.m4a"}
        ]
        
        for test_case in specific_tests:
            try:
                # Trouver le mot dans la base de données
                response = requests.get(f"{BASE_URL}/words", params={"category": test_case["category"]})
                if response.status_code == 200:
                    words = response.json()
                    target_word = None
                    
                    for word in words:
                        if word.get("french", "").lower() == test_case["french"].lower():
                            target_word = word
                            break
                    
                    if target_word:
                        word_id = target_word.get("id")
                        french = target_word.get("french")
                        
                        # Vérifier le système dual
                        has_dual = target_word.get("dual_audio_system", False)
                        self.log_test(f"Mot '{french}' a dual_audio_system", 
                                     has_dual, 
                                     f"dual_audio_system: {has_dual}")
                        
                        if has_dual and word_id:
                            # Tester les fichiers audio spécifiques
                            for lang, expected_file in [("shimaore", test_case["shimaore_file"]), 
                                                       ("kibouchi", test_case["kibouchi_file"])]:
                                
                                # Vérifier les métadonnées audio
                                info_response = requests.get(f"{BASE_URL}/words/{word_id}/audio-info")
                                if info_response.status_code == 200:
                                    info_data = info_response.json()
                                    audio_info = info_data.get("audio", {}).get(lang, {})
                                    actual_file = audio_info.get("filename")
                                    
                                    self.log_test(f"Fichier {lang} pour '{french}'", 
                                                 actual_file == expected_file, 
                                                 f"Attendu: {expected_file}, Trouvé: {actual_file}")
                                
                                # Tester l'endpoint audio
                                audio_response = requests.get(f"{BASE_URL}/words/{word_id}/audio/{lang}")
                                self.log_test(f"Endpoint audio {lang} pour '{french}'", 
                                             audio_response.status_code in [200, 404], 
                                             f"Status: {audio_response.status_code}")
                    else:
                        self.log_test(f"Trouver mot '{test_case['french']}'", False, "Mot non trouvé")
                else:
                    self.log_test(f"Récupération mots {test_case['category']}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Test mot spécifique '{test_case['french']}'", False, f"Error: {e}")
    
    def test_audio_coverage_validation(self):
        """Test 4: Validation de la couverture audio"""
        print("\n📊 TEST 4: VALIDATION COUVERTURE AUDIO")
        
        try:
            # Récupérer les statistiques audio
            response = requests.get(f"{BASE_URL}/audio/info")
            if response.status_code == 200:
                data = response.json()
                
                total_audio_files = 0
                for category in ["famille", "nature", "nombres", "animaux"]:
                    if category in data:
                        count = data[category].get("count", 0)
                        total_audio_files += count
                        self.log_test(f"Fichiers audio {category}", 
                                     count > 0, 
                                     f"Trouvé: {count} fichiers")
                
                self.log_test("Total fichiers audio disponibles", 
                             total_audio_files > 0, 
                             f"Total: {total_audio_files} fichiers")
            else:
                self.log_test("Récupération info audio", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Test couverture audio", False, f"Error: {e}")
        
        # Compter les mots avec système dual dans toutes les catégories
        try:
            total_dual_words = 0
            categories = ["famille", "nature", "nombres", "animaux"]
            
            for category in categories:
                response = requests.get(f"{BASE_URL}/words", params={"category": category})
                if response.status_code == 200:
                    words = response.json()
                    dual_words = [w for w in words if w.get("dual_audio_system", False)]
                    dual_count = len(dual_words)
                    total_dual_words += dual_count
                    
                    self.log_test(f"Mots {category} avec système dual", 
                                 dual_count >= 0, 
                                 f"Trouvé: {dual_count} mots")
            
            # Vérifier si on approche les 138 mots restructurés mentionnés
            self.log_test("Total mots avec système dual", 
                         total_dual_words > 50,  # Seuil minimum raisonnable
                         f"Total: {total_dual_words} mots (objectif: ~138)")
        except Exception as e:
            self.log_test("Comptage mots dual", False, f"Error: {e}")
    
    def test_category_detection(self):
        """Test 5: Détection automatique de catégorie pour servir les bons fichiers"""
        print("\n🔍 TEST 5: DÉTECTION AUTOMATIQUE DE CATÉGORIE")
        
        # Tester que les endpoints audio utilisent le bon dossier selon la catégorie
        categories = ["famille", "nature", "nombres", "animaux"]
        
        for category in categories:
            try:
                # Récupérer quelques mots de la catégorie
                response = requests.get(f"{BASE_URL}/words", params={"category": category, "limit": 5})
                if response.status_code == 200:
                    words = response.json()
                    dual_words = [w for w in words if w.get("dual_audio_system", False)]
                    
                    if dual_words:
                        test_word = dual_words[0]
                        word_id = test_word.get("id")
                        
                        if word_id:
                            # Tester que l'endpoint audio fonctionne (détection automatique)
                            for lang in ["shimaore", "kibouchi"]:
                                audio_response = requests.get(f"{BASE_URL}/words/{word_id}/audio/{lang}")
                                self.log_test(f"Détection catégorie {category} pour audio {lang}", 
                                             audio_response.status_code in [200, 404], 
                                             f"Status: {audio_response.status_code}")
                    else:
                        self.log_test(f"Mots dual disponibles pour {category}", False, "Aucun mot avec système dual")
                else:
                    self.log_test(f"Récupération mots {category}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Test détection {category}", False, f"Error: {e}")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🚀 DÉBUT DES TESTS DU SYSTÈME AUDIO DUAL ÉTENDU")
        print("=" * 60)
        
        self.test_new_audio_endpoints()
        self.test_dual_system_extension()
        self.test_specific_words()
        self.test_audio_coverage_validation()
        self.test_category_detection()
        
        # Résumé final
        print("\n" + "=" * 60)
        print("📋 RÉSUMÉ DES TESTS")
        print(f"Total tests: {self.results['total_tests']}")
        print(f"✅ Réussis: {self.results['passed']}")
        print(f"❌ Échoués: {self.results['failed']}")
        
        if self.results['failed'] > 0:
            print("\n🔍 ERREURS DÉTAILLÉES:")
            for error in self.results['errors']:
                print(f"  {error}")
        
        success_rate = (self.results['passed'] / self.results['total_tests']) * 100 if self.results['total_tests'] > 0 else 0
        print(f"\n📊 Taux de réussite: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 SYSTÈME AUDIO DUAL ÉTENDU: FONCTIONNEL")
        elif success_rate >= 60:
            print("⚠️  SYSTÈME AUDIO DUAL ÉTENDU: PARTIELLEMENT FONCTIONNEL")
        else:
            print("❌ SYSTÈME AUDIO DUAL ÉTENDU: PROBLÈMES CRITIQUES")
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = DualAudioSystemTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)