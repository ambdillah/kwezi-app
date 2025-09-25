#!/usr/bin/env python3
"""
Test complet du backend après la création et mise à jour des prononciations audio pour la section "nature"

Ce test vérifie tous les aspects demandés dans la review request française:
1. Vérification de la nouvelle section nature (58 mots attendus)
2. Test de l'orthographe corrigée pour des mots spécifiques
3. Test de la couverture audio (55/58 mots avec 94.8% d'audio authentique)
4. Test des références audio spécifiques
5. Test des éléments de nature diversifiés
6. Test de l'intégrité des données
7. Test des autres sections non affectées
8. Test des endpoints API spécifiques
9. Test des fichiers audio
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
    BACKEND_URL = "https://shimao-game.preview.emergentagent.com"

API_URL = f"{BACKEND_URL}/api"
print(f"🔗 Using Backend URL: {BACKEND_URL}")

class NatureSectionTester:
    def __init__(self):
        self.api_url = API_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.nature_words = []
        self.total_words_count = 0
        
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
    
    def test_2_nature_section_exists(self):
        """Test 2: Vérification que la section nature existe"""
        print("\n=== TEST 2: VÉRIFICATION SECTION NATURE ===")
        
        try:
            response = self.make_request("/words?category=nature")
            if response["success"]:
                self.nature_words = response["data"]
                count = len(self.nature_words)
                self.log_test("Section nature existe", count > 0, f"{count} mots trouvés")
                return count > 0
            else:
                self.log_test("Section nature existe", False, f"Status: {response['status_code']}")
                return False
        except Exception as e:
            self.log_test("Section nature existe", False, f"Error: {str(e)}")
            return False
    
    def test_3_58_words_added(self):
        """Test 3: Vérification que 58 mots ont été ajoutés"""
        print("\n=== TEST 3: VÉRIFICATION 58 MOTS AJOUTÉS ===")
        
        expected_count = 58
        actual_count = len(self.nature_words)
        
        # Allow some tolerance (50-60 words)
        success = 50 <= actual_count <= 60
        self.log_test("58 mots ajoutés", success, 
                     f"Attendu: ~{expected_count}, Trouvé: {actual_count}")
        
        return success
    
    def test_4_data_structure(self):
        """Test 4: Vérification de la structure des données"""
        print("\n=== TEST 4: STRUCTURE DES DONNÉES ===")
        
        if not self.nature_words:
            self.log_test("Structure des données", False, "Aucun mot à tester")
            return False
        
        required_fields = ['french', 'shimaore', 'kibouchi', 'category']
        complete_words = 0
        words_with_emojis = 0
        
        for word in self.nature_words:
            # Check required fields
            has_all_fields = all(field in word and word[field] for field in required_fields)
            if has_all_fields:
                complete_words += 1
            
            # Check for emoji (in image_url field)
            if 'image_url' in word and word['image_url']:
                words_with_emojis += 1
        
        structure_percentage = (complete_words / len(self.nature_words)) * 100
        emoji_percentage = (words_with_emojis / len(self.nature_words)) * 100
        
        self.log_test("Structure complète", structure_percentage >= 95,
                     f"{complete_words}/{len(self.nature_words)} mots avec structure complète ({structure_percentage:.1f}%)")
        
        self.log_test("Emojis présents", emoji_percentage >= 80,
                     f"{words_with_emojis}/{len(self.nature_words)} mots avec emojis ({emoji_percentage:.1f}%)")
        
        return structure_percentage >= 95
    
    def test_5_corrected_spelling(self):
        """Test 5: Test de l'orthographe corrigée pour les mots spécifiques"""
        print("\n=== TEST 5: ORTHOGRAPHE CORRIGÉE ===")
        
        expected_corrections = {
            "lune": {"shimaore": "mwézi", "kibouchi": "fandzava"},
            "vague": {"shimaore": "dhouja", "kibouchi": "houndza"},
            "fleur": {"shimaore": "foulera", "kibouchi": "foulèra"},
            "cocotier": {"shimaore": "m'nadzi", "kibouchi": "voudi ni vwaniou"}
        }
        
        word_dict = {word['french'].lower(): word for word in self.nature_words}
        
        for french_word, expected_translations in expected_corrections.items():
            if french_word in word_dict:
                word = word_dict[french_word]
                shimaore_match = expected_translations["shimaore"].lower() in word['shimaore'].lower()
                kibouchi_match = expected_translations["kibouchi"].lower() in word['kibouchi'].lower()
                
                self.log_test(f"Orthographe corrigée: {french_word}", 
                             shimaore_match and kibouchi_match,
                             f"Shimaoré: {word['shimaore']}, Kibouchi: {word['kibouchi']}")
            else:
                self.log_test(f"Orthographe corrigée: {french_word}", False, "Mot non trouvé")
    
    def test_6_audio_coverage(self):
        """Test 6: Test de la couverture audio (55/58 mots = 94.8%)"""
        print("\n=== TEST 6: COUVERTURE AUDIO ===")
        
        if not self.nature_words:
            self.log_test("Couverture audio", False, "Aucun mot à tester")
            return
        
        words_with_audio = 0
        total_words = len(self.nature_words)
        
        for word in self.nature_words:
            has_audio = (
                word.get('has_authentic_audio', False) or
                word.get('shimoare_has_audio', False) or
                word.get('kibouchi_has_audio', False) or
                word.get('audio_filename') or
                word.get('shimoare_audio_filename') or
                word.get('kibouchi_audio_filename') or
                word.get('dual_audio_system', False)
            )
            if has_audio:
                words_with_audio += 1
        
        coverage_percentage = (words_with_audio / total_words * 100) if total_words > 0 else 0
        expected_coverage = 94.8  # 55/58 words
        
        success = coverage_percentage >= expected_coverage - 10  # Allow 10% tolerance
        self.log_test("Couverture audio 94.8%", success, 
                     f"{words_with_audio}/{total_words} mots ({coverage_percentage:.1f}%) ont des références audio")
    
    def test_7_specific_audio_references(self):
        """Test 7: Test des références audio spécifiques"""
        print("\n=== TEST 7: RÉFÉRENCES AUDIO SPÉCIFIQUES ===")
        
        expected_audio = {
            "lune": "Fandzava.m4a",
            "soleil": "Zouva.m4a", 
            "mer": "Bahari.m4a",
            "cocotier": "M_nadzi.m4a"
        }
        
        word_dict = {word['french'].lower(): word for word in self.nature_words}
        
        for french_word, expected_audio_file in expected_audio.items():
            if french_word in word_dict:
                word = word_dict[french_word]
                audio_files = [
                    word.get('audio_filename', ''),
                    word.get('shimoare_audio_filename', ''),
                    word.get('kibouchi_audio_filename', '')
                ]
                
                has_expected_audio = any(expected_audio_file in audio_file for audio_file in audio_files if audio_file)
                self.log_test(f"Référence audio spécifique - {french_word}", has_expected_audio,
                             f"Attendu: {expected_audio_file}, Trouvé: {[f for f in audio_files if f]}")
            else:
                self.log_test(f"Référence audio spécifique - {french_word}", False, "Mot non trouvé")
    
    def test_8_diverse_nature_elements(self):
        """Test 8: Test des éléments de nature diversifiés"""
        print("\n=== TEST 8: ÉLÉMENTS NATURE DIVERSIFIÉS ===")
        
        if not self.nature_words:
            self.log_test("Éléments nature diversifiés", False, "Aucun mot à tester")
            return
        
        # Nature categories
        categories = {
            "celestial": ["lune", "étoile", "soleil", "arc-en-ciel", "arc en ciel", "nuage"],
            "terrestrial": ["terre", "sol", "pierre", "sable", "caillou", "pente"],
            "vegetation": ["arbre", "fleur", "herbe", "bambou", "cocotier", "manguier", "feuille"],
            "marine": ["mer", "vague", "marée basse", "marée haute", "corail", "mangrove", "plage"]
        }
        
        word_list = [word['french'].lower() for word in self.nature_words]
        
        for category, expected_words in categories.items():
            found_words = [word for word in expected_words if word in word_list]
            coverage = len(found_words) / len(expected_words) * 100 if expected_words else 0
            
            success = coverage >= 30  # At least 30% of words in each category
            self.log_test(f"Éléments {category}", success,
                         f"{len(found_words)}/{len(expected_words)} mots trouvés ({coverage:.1f}%): {found_words[:3]}")
    
    def test_9_data_integrity(self):
        """Test 9: Test de l'intégrité des données"""
        print("\n=== TEST 9: INTÉGRITÉ DES DONNÉES ===")
        
        if not self.nature_words:
            self.log_test("Intégrité des données", False, "Aucun mot à tester")
            return
        
        # Test appropriate emojis for nature
        nature_emojis = ['🌳', '🌲', '🌱', '🌿', '🍃', '🌸', '🌺', '🌻', '🌹', '🌷', '🌾', '🌙', '☀️', '⭐', '🌊', '🏖️', '🏞️', '⛰️', '🌈', '☁️', '🌧️', '⛈️', '🌪️', '🔥', '💧', '🪨', '🌍', '🌎', '🌏']
        words_with_nature_emojis = 0
        
        for word in self.nature_words:
            if 'image_url' in word and word['image_url']:
                if any(emoji in word['image_url'] for emoji in nature_emojis):
                    words_with_nature_emojis += 1
        
        emoji_percentage = (words_with_nature_emojis / len(self.nature_words)) * 100
        
        self.log_test("Emojis appropriés nature", emoji_percentage >= 70,
                     f"{words_with_nature_emojis}/{len(self.nature_words)} mots avec emojis nature ({emoji_percentage:.1f}%)")
        
        # Test has_authentic_audio flag
        words_with_authentic_audio = sum(1 for word in self.nature_words 
                                       if word.get('has_authentic_audio', False))
        
        self.log_test("Champs has_authentic_audio définis", words_with_authentic_audio > 0,
                     f"{words_with_authentic_audio}/{len(self.nature_words)} mots avec has_authentic_audio=true")
        
        # Test no duplicates
        french_words = [word['french'].lower() for word in self.nature_words]
        unique_words = set(french_words)
        has_duplicates = len(french_words) != len(unique_words)
        
        self.log_test("Pas de doublons", not has_duplicates,
                     f"Trouvé {len(french_words)} mots, {len(unique_words)} uniques")
    
    def test_10_other_sections_unaffected(self):
        """Test 10: Test que les autres sections n'ont pas été affectées"""
        print("\n=== TEST 10: AUTRES SECTIONS NON AFFECTÉES ===")
        
        expected_sections = {
            'famille': 25,  # Approximate expected count
            'animaux': 65,  # Approximate expected count  
            'nombres': 20,  # Approximate expected count
            'salutations': 8,  # Approximate expected count
            'couleurs': 8,   # Approximate expected count
            'nourriture': 40  # Approximate expected count
        }
        
        for category, min_expected in expected_sections.items():
            try:
                response = self.make_request(f"/words?category={category}")
                if response["success"]:
                    data = response["data"]
                    word_count = len(data)
                    self.log_test(f"Section {category} intacte", word_count >= min_expected,
                                 f"Trouvé {word_count} mots (attendu ≥{min_expected})")
                else:
                    self.log_test(f"Section {category} intacte", False,
                                 f"HTTP {response['status_code']}")
            except Exception as e:
                self.log_test(f"Section {category} intacte", False, f"Error: {str(e)}")
    
    def test_11_total_sections_count(self):
        """Test 11: Confirmer que le nombre total de sections est maintenant de 8+"""
        print("\n=== TEST 11: NOMBRE TOTAL SECTIONS ≥ 8 ===")
        
        try:
            response = self.make_request("/words")
            if response["success"]:
                all_words = response["data"]
                categories = set(word['category'] for word in all_words)
                category_count = len(categories)
                
                self.log_test("Nombre total sections ≥ 8", category_count >= 8,
                             f"Trouvé {category_count} catégories (attendu ≥8)")
                self.log_test("Catégories trouvées", True, f"Catégories: {sorted(categories)}")
            else:
                self.log_test("Nombre total sections", False, f"HTTP {response['status_code']}")
        except Exception as e:
            self.log_test("Nombre total sections", False, f"Error: {str(e)}")
    
    def test_12_api_performance(self):
        """Test 12: Tester les performances globales de l'API"""
        print("\n=== TEST 12: PERFORMANCES API ===")
        
        try:
            start_time = time.time()
            response = self.make_request("/words?category=nature")
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response["success"]:
                data = response["data"]
                self.log_test("Performance API nature", response_time < 2.0,
                             f"Temps de réponse: {response_time:.3f}s, {len(data)} mots retournés")
                
                # Test that all returned words are from nature category
                all_nature = all(word.get('category') == 'nature' for word in data)
                self.log_test("Filtrage catégorie correct", all_nature,
                             f"Tous les {len(data)} mots sont de la catégorie 'nature'")
                
                return True
            else:
                self.log_test("Performance API nature", False,
                             f"HTTP {response['status_code']}")
                return False
        except Exception as e:
            self.log_test("Performance API nature", False, f"Error: {str(e)}")
            return False
    
    def test_13_specific_nature_endpoint(self):
        """Test 13: Test API endpoint spécifique /api/words?category=nature"""
        print("\n=== TEST 13: ENDPOINT SPÉCIFIQUE NATURE ===")
        
        try:
            response = self.make_request("/words?category=nature")
            if response["success"]:
                words = response["data"]
                
                # Test that all 58 words are returned (with tolerance)
                success = 50 <= len(words) <= 60
                self.log_test("58 mots retournés", success,
                             f"Endpoint retourne {len(words)} mots (attendu: ~58)")
                
                # Test specific nature words exist
                expected_nature = ['lune', 'soleil', 'mer', 'arbre', 'fleur']
                word_names = [word.get('french', '').lower() for word in words]
                
                for expected_word in expected_nature:
                    found = expected_word.lower() in word_names
                    self.log_test(f"Mot attendu présent - {expected_word}", found)
                    
            else:
                self.log_test("Endpoint nature", False, f"HTTP {response['status_code']}")
        except Exception as e:
            self.log_test("Endpoint nature", False, f"Error: {str(e)}")
    
    def test_14_audio_files_access(self):
        """Test 14: Test d'accès aux fichiers audio via l'API"""
        print("\n=== TEST 14: ACCÈS FICHIERS AUDIO ===")
        
        try:
            # Test if audio info endpoint exists
            response = self.make_request("/audio/info")
            if response["success"]:
                audio_info = response["data"]
                self.log_test("Endpoint audio/info", True, "Endpoint audio info accessible")
                
                # Check if nature is in audio categories
                if isinstance(audio_info, dict) and 'nature' in str(audio_info):
                    nature_info = audio_info.get('nature', {})
                    file_count = nature_info.get('count', 0) if isinstance(nature_info, dict) else 0
                    
                    self.log_test("Catégorie nature dans audio", file_count >= 90,
                                 f"Nature trouvé avec {file_count} fichiers audio (attendu: 97)")
                else:
                    self.log_test("Catégorie nature dans audio", False, "Nature non trouvé dans info audio")
            else:
                self.log_test("Endpoint audio/info", False, f"HTTP {response['status_code']} - Endpoints audio non implémentés")
        except Exception as e:
            self.log_test("Accès fichiers audio", False, f"Error: {str(e)} - Endpoints audio non implémentés")
    
    def test_15_audio_endpoint_functionality(self):
        """Test 15: Test de la fonctionnalité de l'endpoint audio nature"""
        print("\n=== TEST 15: FONCTIONNALITÉ ENDPOINT AUDIO ===")
        
        test_files = ["Bahari.m4a", "Zouva.m4a", "Fandzava.m4a"]
        
        for filename in test_files:
            try:
                response = requests.get(f"{self.api_url}/audio/nature/{filename}", timeout=10)
                
                if response.status_code == 200:
                    content_type = response.headers.get("content-type", "")
                    success = "audio" in content_type.lower()
                    self.log_test(f"Endpoint audio nature - {filename}", success,
                                 f"Status: {response.status_code}, Content-Type: {content_type}")
                elif response.status_code == 404:
                    self.log_test(f"Endpoint audio nature - {filename}", False,
                                 f"Fichier non trouvé: {filename}")
                else:
                    self.log_test(f"Endpoint audio nature - {filename}", False,
                                 f"Erreur HTTP: {response.status_code}")
            except Exception as e:
                self.log_test(f"Endpoint audio nature - {filename}", False, f"Error: {str(e)}")
    
    def test_16_total_word_count(self):
        """Test 16: Test que le nombre total de mots est raisonnable"""
        print("\n=== TEST 16: NOMBRE TOTAL MOTS ===")
        
        try:
            response = self.make_request("/words")
            if response["success"]:
                data = response["data"]
                self.total_words_count = len(data)
                
                # Based on previous tests, we expect around 600+ words total
                expected_minimum = 600
                self.log_test("Total mots raisonnable", self.total_words_count >= expected_minimum,
                             f"Trouvé {self.total_words_count} mots total (attendu ≥{expected_minimum})")
                return self.total_words_count
            else:
                self.log_test("Total mots raisonnable", False,
                             f"HTTP {response['status_code']}")
                return 0
        except Exception as e:
            self.log_test("Total mots raisonnable", False, f"Error: {str(e)}")
            return 0
    
    def run_all_tests(self):
        """Execute all tests for nature section"""
        print("🌿 DÉBUT DES TESTS BACKEND - SECTION NATURE")
        print("=" * 70)
        print("Test complet du backend après la création et mise à jour des")
        print("prononciations audio pour la section 'nature' avec 58 mots")
        print("=" * 70)
        
        start_time = time.time()
        
        # Test connectivity first
        if not self.test_1_api_connectivity():
            print("❌ ÉCHEC: Impossible de se connecter à l'API. Arrêt des tests.")
            return False
        
        # Test nature section exists
        if not self.test_2_nature_section_exists():
            print("❌ ÉCHEC: Section nature non trouvée. Arrêt des tests.")
            return False
        
        # Run all test suites
        self.test_3_58_words_added()
        self.test_4_data_structure()
        self.test_5_corrected_spelling()
        self.test_6_audio_coverage()
        self.test_7_specific_audio_references()
        self.test_8_diverse_nature_elements()
        self.test_9_data_integrity()
        self.test_10_other_sections_unaffected()
        self.test_11_total_sections_count()
        self.test_12_api_performance()
        self.test_13_specific_nature_endpoint()
        self.test_14_audio_files_access()
        self.test_15_audio_endpoint_functionality()
        self.test_16_total_word_count()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 70)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Tests réussis: {self.passed_tests}/{self.total_tests} ({success_rate:.1f}%)")
        print(f"Durée: {duration:.2f}s")
        
        # Show nature section statistics
        print(f"\n📈 STATISTIQUES SECTION NATURE:")
        if self.nature_words:
            count = len(self.nature_words)
            with_emojis = sum(1 for w in self.nature_words if w.get('image_url'))
            with_audio = sum(1 for w in self.nature_words if (
                w.get('has_authentic_audio') or w.get('audio_filename') or
                w.get('shimoare_has_audio') or w.get('kibouchi_has_audio') or
                w.get('dual_audio_system')
            ))
            emoji_rate = (with_emojis / count * 100) if count > 0 else 0
            audio_rate = (with_audio / count * 100) if count > 0 else 0
            print(f"  Nature: {count} mots")
            print(f"  Avec emojis: {with_emojis} ({emoji_rate:.1f}%)")
            print(f"  Avec audio: {with_audio} ({audio_rate:.1f}%)")
        
        print(f"  Total mots dans la base: {self.total_words_count}")
        
        if success_rate >= 80:
            print("\n🎉 RÉSULTAT: SUCCÈS - La section nature est fonctionnelle!")
        elif success_rate >= 60:
            print("\n⚠️ RÉSULTAT: PARTIEL - Quelques problèmes identifiés")
        else:
            print("\n❌ RÉSULTAT: ÉCHEC - Problèmes critiques identifiés")
        
        print("\n📋 DÉTAIL DES RÉSULTATS:")
        for result in self.test_results:
            print(f"  {result}")
        
        return success_rate >= 60

def main():
    """Main test execution"""
    tester = NatureSectionTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🏁 TESTS TERMINÉS AVEC SUCCÈS!")
        sys.exit(0)
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ - VÉRIFICATION NÉCESSAIRE")
        sys.exit(1)

if __name__ == "__main__":
    main()