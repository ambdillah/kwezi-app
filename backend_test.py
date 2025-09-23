#!/usr/bin/env python3
"""
TESTS SPÉCIFIQUES POUR LA SECTION "CORPS HUMAIN" - INTÉGRATION AUDIO DUAL
========================================================================

Tests critiques pour vérifier l'intégration du système audio dual 
pour la catégorie "corps humain" avec 61 fichiers audio authentiques.
"""

import requests
import json
import os
from typing import Dict, List, Any

# Configuration des URLs
BACKEND_URL = "https://mayotte-learn-2.preview.emergentagent.com/api"

class CorpsAudioTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.failed_tests = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Enregistre le résultat d'un test"""
        result = {
            "test": test_name,
            "success": success,
            "details": details
        }
        self.test_results.append(result)
        
        if success:
            print(f"✅ {test_name}")
            if details:
                print(f"   {details}")
        else:
            print(f"❌ {test_name}")
            print(f"   {details}")
            self.failed_tests.append(result)
    
    def test_audio_info_extension(self):
        """TEST 1: Vérifier que GET /api/audio/info inclut maintenant la section "corps" (5 catégories total)"""
        try:
            response = requests.get(f"{self.backend_url}/audio/info")
            
            if response.status_code != 200:
                self.log_test("Audio Info Extension", False, f"Status code: {response.status_code}")
                return
            
            data = response.json()
            
            # Vérifier que 5 catégories sont présentes
            expected_categories = ["famille", "nature", "nombres", "animaux", "corps"]
            
            if "categories" not in data:
                self.log_test("Audio Info Extension", False, "Clé 'categories' manquante dans la réponse")
                return
            
            categories = data["categories"]
            found_categories = list(categories.keys())
            
            if len(found_categories) != 5:
                self.log_test("Audio Info Extension", False, 
                            f"Attendu 5 catégories, trouvé {len(found_categories)}: {found_categories}")
                return
            
            # Vérifier que "corps" est inclus
            if "corps" not in found_categories:
                self.log_test("Audio Info Extension", False, 
                            f"Catégorie 'corps' manquante. Catégories trouvées: {found_categories}")
                return
            
            # Vérifier l'endpoint pour corps
            if "corps" in categories and "endpoint" in categories["corps"]:
                corps_endpoint = categories["corps"]["endpoint"]
                expected_endpoint = "/api/audio/corps/{filename}"
                if corps_endpoint != expected_endpoint:
                    self.log_test("Audio Info Extension", False, 
                                f"Endpoint corps incorrect: {corps_endpoint}, attendu: {expected_endpoint}")
                    return
            
            self.log_test("Audio Info Extension", True, 
                        f"5 catégories trouvées: {found_categories}, endpoint corps: {categories['corps']['endpoint']}")
            
        except Exception as e:
            self.log_test("Audio Info Extension", False, f"Erreur: {str(e)}")
    
    def test_corps_audio_files_detection(self):
        """TEST 2: Confirmer que 61 fichiers audio sont détectés dans le répertoire /corps"""
        try:
            response = requests.get(f"{self.backend_url}/audio/info")
            
            if response.status_code != 200:
                self.log_test("Corps Audio Files Detection", False, f"Status code: {response.status_code}")
                return
            
            data = response.json()
            
            if "categories" not in data or "corps" not in data["categories"]:
                self.log_test("Corps Audio Files Detection", False, "Catégorie 'corps' non trouvée dans audio/info")
                return
            
            corps_info = data["categories"]["corps"]
            
            if "file_count" in corps_info:
                file_count = corps_info["file_count"]
                if file_count == 61:
                    self.log_test("Corps Audio Files Detection", True, f"61 fichiers audio détectés dans /corps")
                else:
                    self.log_test("Corps Audio Files Detection", False, 
                                f"Attendu 61 fichiers, trouvé {file_count}")
            else:
                self.log_test("Corps Audio Files Detection", False, "Champ 'file_count' manquant pour la catégorie corps")
                
        except Exception as e:
            self.log_test("Corps Audio Files Detection", False, f"Erreur: {str(e)}")
    
    def test_corps_audio_endpoint(self):
        """TEST 3: Tester l'endpoint GET /api/audio/corps/{filename} avec des fichiers spécifiques"""
        test_files = [
            "Mhono.m4a",      # main (Shimaoré)
            "Tagnana.m4a",    # main (Kibouchi)
            "Shitsoi.m4a",    # tête (Shimaoré)
            "Louha.m4a",      # tête (Kibouchi)
            "Matso.m4a",      # œil (Shimaoré)
            "Faninti.m4a"     # œil (Kibouchi)
        ]
        
        success_count = 0
        
        for filename in test_files:
            try:
                response = requests.get(f"{self.backend_url}/audio/corps/{filename}")
                
                if response.status_code == 200:
                    success_count += 1
                    print(f"   ✅ {filename}: Status 200, Content-Type: {response.headers.get('content-type', 'N/A')}")
                else:
                    print(f"   ❌ {filename}: Status {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {filename}: Erreur {str(e)}")
        
        if success_count == len(test_files):
            self.log_test("Corps Audio Endpoint", True, f"Tous les {len(test_files)} fichiers testés sont accessibles")
        else:
            self.log_test("Corps Audio Endpoint", False, 
                        f"Seulement {success_count}/{len(test_files)} fichiers accessibles")
    
    def test_corps_words_dual_audio_coverage(self):
        """TEST 4: Vérifier que les 32 mots de la catégorie "corps" ont dual_audio_system: true"""
        try:
            response = requests.get(f"{self.backend_url}/words?category=corps")
            
            if response.status_code != 200:
                self.log_test("Corps Words Dual Audio Coverage", False, f"Status code: {response.status_code}")
                return
            
            words = response.json()
            
            if not isinstance(words, list):
                self.log_test("Corps Words Dual Audio Coverage", False, "Réponse n'est pas une liste")
                return
            
            total_words = len(words)
            dual_audio_words = 0
            shimoare_audio_words = 0
            kibouchi_audio_words = 0
            
            for word in words:
                if word.get("dual_audio_system", False):
                    dual_audio_words += 1
                
                if word.get("shimoare_has_audio", False):
                    shimoare_audio_words += 1
                
                if word.get("kibouchi_has_audio", False):
                    kibouchi_audio_words += 1
            
            # Vérifier le nombre total de mots
            if total_words != 32:
                self.log_test("Corps Words Dual Audio Coverage", False, 
                            f"Attendu 32 mots dans la catégorie corps, trouvé {total_words}")
                return
            
            # Vérifier la couverture dual audio
            if dual_audio_words == 32:
                self.log_test("Corps Words Dual Audio Coverage", True, 
                            f"32/32 mots ont dual_audio_system: true, Shimaoré: {shimoare_audio_words}/32, Kibouchi: {kibouchi_audio_words}/32")
            else:
                self.log_test("Corps Words Dual Audio Coverage", False, 
                            f"Seulement {dual_audio_words}/32 mots ont dual_audio_system: true")
                
        except Exception as e:
            self.log_test("Corps Words Dual Audio Coverage", False, f"Erreur: {str(e)}")
    
    def test_specific_words_audio_mappings(self):
        """TEST 5: Tester les exemples spécifiques (main, tête, œil) avec leurs fichiers audio"""
        test_cases = [
            {
                "french": "main",
                "shimoare_file": "Mhono.m4a",
                "kibouchi_file": "Tagnana.m4a"
            },
            {
                "french": "tête", 
                "shimoare_file": "Shitsoi.m4a",
                "kibouchi_file": "Louha.m4a"
            },
            {
                "french": "œil",
                "shimoare_file": "Matso.m4a", 
                "kibouchi_file": "Faninti.m4a"
            }
        ]
        
        success_count = 0
        
        for test_case in test_cases:
            try:
                # Trouver le mot dans la base de données
                response = requests.get(f"{self.backend_url}/words?category=corps")
                if response.status_code != 200:
                    continue
                
                words = response.json()
                target_word = None
                
                for word in words:
                    if word.get("french", "").lower() == test_case["french"].lower():
                        target_word = word
                        break
                
                if not target_word:
                    print(f"   ❌ {test_case['french']}: Mot non trouvé dans la base de données")
                    continue
                
                # Vérifier les champs audio
                shimoare_file = target_word.get("shimoare_audio_filename", "")
                kibouchi_file = target_word.get("kibouchi_audio_filename", "")
                dual_system = target_word.get("dual_audio_system", False)
                shimoare_has_audio = target_word.get("shimoare_has_audio", False)
                kibouchi_has_audio = target_word.get("kibouchi_has_audio", False)
                
                if (shimoare_file == test_case["shimoare_file"] and 
                    kibouchi_file == test_case["kibouchi_file"] and
                    dual_system and shimoare_has_audio and kibouchi_has_audio):
                    
                    success_count += 1
                    print(f"   ✅ {test_case['french']}: {shimoare_file} (Shimaoré) + {kibouchi_file} (Kibouchi)")
                else:
                    print(f"   ❌ {test_case['french']}: Mapping incorrect")
                    print(f"      Attendu: {test_case['shimoare_file']} + {test_case['kibouchi_file']}")
                    print(f"      Trouvé: {shimoare_file} + {kibouchi_file}")
                    print(f"      Flags: dual={dual_system}, shimoare={shimoare_has_audio}, kibouchi={kibouchi_has_audio}")
                    
            except Exception as e:
                print(f"   ❌ {test_case['french']}: Erreur {str(e)}")
        
        if success_count == len(test_cases):
            self.log_test("Specific Words Audio Mappings", True, f"Tous les {len(test_cases)} exemples spécifiques sont correctement mappés")
        else:
            self.log_test("Specific Words Audio Mappings", False, 
                        f"Seulement {success_count}/{len(test_cases)} exemples corrects")
    
    def test_dual_audio_endpoints(self):
        """TEST 6: Tester les endpoints GET /api/words/{word_id}/audio/shimaore et /api/words/{word_id}/audio/kibouchi"""
        try:
            # Récupérer quelques mots de la catégorie corps
            response = requests.get(f"{self.backend_url}/words?category=corps")
            if response.status_code != 200:
                self.log_test("Dual Audio Endpoints", False, f"Impossible de récupérer les mots corps: {response.status_code}")
                return
            
            words = response.json()
            test_words = []
            
            # Sélectionner les mots avec dual_audio_system
            for word in words:
                if (word.get("dual_audio_system", False) and 
                    word.get("french", "").lower() in ["main", "tête", "œil"]):
                    test_words.append(word)
            
            if not test_words:
                self.log_test("Dual Audio Endpoints", False, "Aucun mot de test trouvé avec dual_audio_system")
                return
            
            success_count = 0
            total_tests = 0
            
            for word in test_words:
                word_id = word.get("id", "")
                french_word = word.get("french", "")
                
                if not word_id:
                    continue
                
                # Tester endpoint Shimaoré
                try:
                    shimoare_response = requests.get(f"{self.backend_url}/words/{word_id}/audio/shimaore")
                    total_tests += 1
                    if shimoare_response.status_code == 200:
                        success_count += 1
                        print(f"   ✅ {french_word} (Shimaoré): Status 200")
                    else:
                        print(f"   ❌ {french_word} (Shimaoré): Status {shimoare_response.status_code}")
                except Exception as e:
                    print(f"   ❌ {french_word} (Shimaoré): Erreur {str(e)}")
                
                # Tester endpoint Kibouchi
                try:
                    kibouchi_response = requests.get(f"{self.backend_url}/words/{word_id}/audio/kibouchi")
                    total_tests += 1
                    if kibouchi_response.status_code == 200:
                        success_count += 1
                        print(f"   ✅ {french_word} (Kibouchi): Status 200")
                    else:
                        print(f"   ❌ {french_word} (Kibouchi): Status {kibouchi_response.status_code}")
                except Exception as e:
                    print(f"   ❌ {french_word} (Kibouchi): Erreur {str(e)}")
            
            if success_count == total_tests and total_tests > 0:
                self.log_test("Dual Audio Endpoints", True, f"Tous les {total_tests} endpoints audio testés fonctionnent")
            else:
                self.log_test("Dual Audio Endpoints", False, 
                            f"Seulement {success_count}/{total_tests} endpoints fonctionnent")
                
        except Exception as e:
            self.log_test("Dual Audio Endpoints", False, f"Erreur: {str(e)}")
    
    def test_audio_info_metadata(self):
        """TEST 7: Vérifier GET /api/words/{word_id}/audio-info retourne les bonnes métadonnées"""
        try:
            # Récupérer un mot de test
            response = requests.get(f"{self.backend_url}/words?category=corps")
            if response.status_code != 200:
                self.log_test("Audio Info Metadata", False, f"Impossible de récupérer les mots corps: {response.status_code}")
                return
            
            words = response.json()
            test_word = None
            
            for word in words:
                if (word.get("dual_audio_system", False) and 
                    word.get("french", "").lower() == "main"):
                    test_word = word
                    break
            
            if not test_word:
                self.log_test("Audio Info Metadata", False, "Mot de test 'main' non trouvé avec dual_audio_system")
                return
            
            word_id = test_word.get("id", "")
            if not word_id:
                self.log_test("Audio Info Metadata", False, "ID du mot de test manquant")
                return
            
            # Tester l'endpoint audio-info
            response = requests.get(f"{self.backend_url}/words/{word_id}/audio-info")
            
            if response.status_code != 200:
                self.log_test("Audio Info Metadata", False, f"Status code: {response.status_code}")
                return
            
            audio_info = response.json()
            
            # Vérifier la structure des métadonnées
            required_fields = ["dual_audio_system", "languages"]
            for field in required_fields:
                if field not in audio_info:
                    self.log_test("Audio Info Metadata", False, f"Champ requis manquant: {field}")
                    return
            
            if not audio_info.get("dual_audio_system", False):
                self.log_test("Audio Info Metadata", False, "dual_audio_system devrait être true")
                return
            
            languages = audio_info.get("languages", {})
            if "shimaore" not in languages or "kibouchi" not in languages:
                self.log_test("Audio Info Metadata", False, "Langues Shimaoré et Kibouchi manquantes")
                return
            
            # Vérifier les métadonnées pour chaque langue
            shimoare_info = languages.get("shimaore", {})
            kibouchi_info = languages.get("kibouchi", {})
            
            if not shimoare_info.get("has_audio", False) or not kibouchi_info.get("has_audio", False):
                self.log_test("Audio Info Metadata", False, "has_audio devrait être true pour les deux langues")
                return
            
            self.log_test("Audio Info Metadata", True, 
                        f"Métadonnées correctes: dual_system={audio_info['dual_audio_system']}, "
                        f"shimoare_audio={shimoare_info.get('has_audio')}, kibouchi_audio={kibouchi_info.get('has_audio')}")
            
        except Exception as e:
            self.log_test("Audio Info Metadata", False, f"Erreur: {str(e)}")
    
    def test_automatic_category_detection(self):
        """TEST 8: Confirmer que le système détecte automatiquement la catégorie "corps" pour servir les bons fichiers"""
        try:
            # Tester que les fichiers sont servis depuis le bon répertoire
            test_files = ["Mhono.m4a", "Shitsoi.m4a", "Matso.m4a"]
            
            success_count = 0
            
            for filename in test_files:
                response = requests.get(f"{self.backend_url}/audio/corps/{filename}")
                
                if response.status_code == 200:
                    # Vérifier que c'est bien un fichier audio
                    content_type = response.headers.get('content-type', '')
                    if 'audio' in content_type.lower():
                        success_count += 1
                        print(f"   ✅ {filename}: Servi depuis /corps avec Content-Type: {content_type}")
                    else:
                        print(f"   ❌ {filename}: Content-Type incorrect: {content_type}")
                else:
                    print(f"   ❌ {filename}: Status {response.status_code}")
            
            if success_count == len(test_files):
                self.log_test("Automatic Category Detection", True, 
                            f"Détection automatique de catégorie fonctionne - {len(test_files)} fichiers servis depuis /corps")
            else:
                self.log_test("Automatic Category Detection", False, 
                            f"Seulement {success_count}/{len(test_files)} fichiers correctement servis")
                
        except Exception as e:
            self.log_test("Automatic Category Detection", False, f"Erreur: {str(e)}")
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("🎯 TESTS SPÉCIFIQUES POUR LA SECTION 'CORPS HUMAIN' - INTÉGRATION AUDIO DUAL")
        print("=" * 80)
        print(f"🔗 Backend URL: {self.backend_url}")
        print()
        
        # Exécuter tous les tests
        self.test_audio_info_extension()
        self.test_corps_audio_files_detection()
        self.test_corps_audio_endpoint()
        self.test_corps_words_dual_audio_coverage()
        self.test_specific_words_audio_mappings()
        self.test_dual_audio_endpoints()
        self.test_audio_info_metadata()
        self.test_automatic_category_detection()
        
        # Résumé des résultats
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["success"]])
        failed_tests = len(self.failed_tests)
        
        print(f"✅ Tests réussis: {passed_tests}/{total_tests}")
        print(f"❌ Tests échoués: {failed_tests}/{total_tests}")
        print(f"📈 Taux de réussite: {(passed_tests/total_tests*100):.1f}%")
        
        if self.failed_tests:
            print("\n❌ TESTS ÉCHOUÉS:")
            for test in self.failed_tests:
                print(f"   - {test['test']}: {test['details']}")
        
        print("\n🎯 OBJECTIF: Confirmer que l'intégration de la section 'corps humain' avec le système audio dual")
        print("    est complète et fonctionnelle avec 100% de couverture (32/32 mots).")
        
        if failed_tests == 0:
            print("\n🎉 SUCCÈS COMPLET! Tous les tests sont passés.")
            print("✅ L'intégration du système audio dual pour la section 'corps humain' est fonctionnelle.")
        else:
            print(f"\n⚠️  {failed_tests} test(s) ont échoué. Vérification nécessaire.")
        
        return failed_tests == 0

def main():
    """Fonction principale"""
    tester = CorpsAudioTester()
    success = tester.run_all_tests()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)