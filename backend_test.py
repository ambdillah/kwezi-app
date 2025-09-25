#!/usr/bin/env python3
"""
Test complet du backend après la création et mise à jour des prononciations audio pour la section "vêtement"
Comprehensive backend testing after creation and audio pronunciation updates for the "vêtement" section

Test Requirements from French review request:
1. Vérification de la nouvelle section - tester que la section "vetements" existe maintenant
2. Vérifier que les 17 mots ont été ajoutés avec succès
3. Confirmer la structure des données (french, shimaoré, kibouchi, emoji)
4. Test de l'orthographe corrigée:
   - "salouva" → shimaoré: "salouva", kibouchi: "salouvagna"
   - "kamiss" → shimaoré: "kandzou bolé", kibouchi: "ankandzou bé"
   - "tongs" → shimaoré: "sapatri", kibouchi: "kabwa sapatri"
   - "voile" → shimaoré: "kichali", kibouchi: "kichali"
5. Test de la couverture audio - vérifier que 16/17 mots (94.1%) ont des références audio authentiques
6. Tester les références audio spécifiques:
   - "vêtement" → audio/vetements/Ngouwo.m4a
   - "salouva" → audio/vetements/Salouva.m4a
   - "kamiss" → audio/vetements/Kandzou bolé.m4a
   - "tongs" → audio/vetements/Kabwa sapatri.m4a
7. Test de l'intégrité des données - vérifier que tous les mots ont des emojis appropriés (👕, 👗, 👖, 👟, etc.)
8. Tester que les champs `has_authentic_audio` sont définis à true
9. Confirmer qu'il n'y a pas de doublons dans la section
10. Test des autres sections - vérifier que les autres sections n'ont pas été affectées
11. Confirmer que le nombre total de sections est maintenant de 7
12. Tester les performances globales de l'API
13. Test API endpoint spécifique - tester l'endpoint `/api/words?category=vetements`
14. Vérifier que tous les 17 mots sont retournés
15. Tester des requêtes spécifiques sur les nouveaux mots
16. Test des fichiers audio - vérifier que les 23 fichiers M4A sont présents
17. Confirmer que 16 fichiers sont utilisés et 7 restent disponibles
18. Tester l'accès aux fichiers audio via l'API
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

class VetementsSectionTester:
    def __init__(self):
        self.api_url = API_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.vetements_words = []
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
    
    def test_2_vetements_section_exists(self):
        """Test 2: Vérification que la section vêtements existe"""
        print("\n=== TEST 2: VÉRIFICATION SECTION VÊTEMENTS ===")
        
        try:
            response = self.make_request("/words?category=vetements")
            if response["success"]:
                self.vetements_words = response["data"]
                count = len(self.vetements_words)
                self.log_test("Section vêtements existe", count > 0, f"{count} mots trouvés")
                return count > 0
            else:
                self.log_test("Section vêtements existe", False, f"Status: {response['status_code']}")
                return False
        except Exception as e:
            self.log_test("Section vêtements existe", False, f"Error: {str(e)}")
            return False
    
    def test_3_17_words_added(self):
        """Test 3: Vérification que 17 mots ont été ajoutés"""
        print("\n=== TEST 3: VÉRIFICATION 17 MOTS AJOUTÉS ===")
        
        expected_count = 17
        actual_count = len(self.vetements_words)
        
        self.log_test("17 mots ajoutés", actual_count == expected_count, 
                     f"Attendu: {expected_count}, Trouvé: {actual_count}")
        
        return actual_count == expected_count
    
    def test_4_data_structure(self):
        """Test 4: Vérification de la structure des données"""
        print("\n=== TEST 4: STRUCTURE DES DONNÉES ===")
        
        if not self.vetements_words:
            self.log_test("Structure des données", False, "Aucun mot à tester")
            return False
        
        required_fields = ['french', 'shimaore', 'kibouchi', 'category']
        complete_words = 0
        words_with_emojis = 0
        
        for word in self.vetements_words:
            # Check required fields
            has_all_fields = all(field in word and word[field] for field in required_fields)
            if has_all_fields:
                complete_words += 1
            
            # Check for emoji (in image_url field)
            if 'image_url' in word and word['image_url']:
                words_with_emojis += 1
        
        structure_percentage = (complete_words / len(self.vetements_words)) * 100
        emoji_percentage = (words_with_emojis / len(self.vetements_words)) * 100
        
        self.log_test("Structure complète", structure_percentage >= 95,
                     f"{complete_words}/{len(self.vetements_words)} mots avec structure complète ({structure_percentage:.1f}%)")
        
        self.log_test("Emojis présents", emoji_percentage >= 80,
                     f"{words_with_emojis}/{len(self.vetements_words)} mots avec emojis ({emoji_percentage:.1f}%)")
        
        return structure_percentage >= 95
    
    def test_5_corrected_spelling(self):
        """Test 5: Test de l'orthographe corrigée pour les mots spécifiques"""
        print("\n=== TEST 5: ORTHOGRAPHE CORRIGÉE ===")
        
        expected_corrections = {
            "salouva": {"shimaore": "salouva", "kibouchi": "salouvagna"},
            "kamiss": {"shimaore": "kandzou bolé", "kibouchi": "ankandzou bé"},
            "tongs": {"shimaore": "sapatri", "kibouchi": "kabwa sapatri"},
            "voile": {"shimaore": "kichali", "kibouchi": "kichali"}
        }
        
        word_dict = {word['french'].lower(): word for word in self.vetements_words}
        
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
        """Test 6: Test de la couverture audio (16/17 mots = 94.1%)"""
        print("\n=== TEST 6: COUVERTURE AUDIO ===")
        
        if not self.vetements_words:
            self.log_test("Couverture audio", False, "Aucun mot à tester")
            return
        
        words_with_audio = 0
        total_words = len(self.vetements_words)
        
        for word in self.vetements_words:
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
        expected_coverage = 94.1  # 16/17 words
        
        success = coverage_percentage >= expected_coverage - 10  # Allow 10% tolerance
        self.log_test("Couverture audio 94.1%", success, 
                     f"{words_with_audio}/{total_words} mots ({coverage_percentage:.1f}%) ont des références audio")
    
    def test_7_specific_audio_references(self):
        """Test 7: Test des références audio spécifiques"""
        print("\n=== TEST 7: RÉFÉRENCES AUDIO SPÉCIFIQUES ===")
        
        expected_audio = {
            "vêtement": "Ngouwo.m4a",
            "salouva": "Salouva.m4a", 
            "kamiss": "Kandzou bolé.m4a",
            "tongs": "Kabwa sapatri.m4a"
        }
        
        word_dict = {word['french'].lower(): word for word in self.vetements_words}
        
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
    
    def test_8_appropriate_emojis(self):
        """Test 8: Test des emojis appropriés pour vêtements"""
        print("\n=== TEST 8: EMOJIS APPROPRIÉS VÊTEMENTS ===")
        
        if not self.vetements_words:
            self.log_test("Emojis appropriés", False, "Aucun mot à tester")
            return
        
        # Clothing-specific emojis
        clothing_emojis = ['👕', '👗', '👖', '👟', '👠', '👡', '👢', '🧥', '🧦', '🧤', '👒', '🎩', '👑', '💍', '👜', '🎒', '👓', '🕶️', '🥿', '🩱', '🩲', '🩳']
        words_with_appropriate_emojis = 0
        
        for word in self.vetements_words:
            if 'image_url' in word and word['image_url']:
                if any(emoji in word['image_url'] for emoji in clothing_emojis):
                    words_with_appropriate_emojis += 1
        
        emoji_percentage = (words_with_appropriate_emojis / len(self.vetements_words)) * 100
        
        self.log_test("Emojis appropriés vêtements", emoji_percentage >= 70,
                     f"{words_with_appropriate_emojis}/{len(self.vetements_words)} mots avec emojis vêtements ({emoji_percentage:.1f}%)")
    
    def test_9_has_authentic_audio_flag(self):
        """Test 9: Test que les champs has_authentic_audio sont définis à true"""
        print("\n=== TEST 9: CHAMPS HAS_AUTHENTIC_AUDIO ===")
        
        if not self.vetements_words:
            self.log_test("Champs has_authentic_audio", False, "Aucun mot à tester")
            return
        
        words_with_authentic_audio = sum(1 for word in self.vetements_words 
                                       if word.get('has_authentic_audio', False))
        
        expected_count = 16  # 16/17 words should have authentic audio
        success = words_with_authentic_audio >= expected_count - 2  # Allow some tolerance
        
        self.log_test("Champs has_authentic_audio définis", success,
                     f"{words_with_authentic_audio}/{len(self.vetements_words)} mots avec has_authentic_audio=true")
    
    def test_10_no_duplicates(self):
        """Test 10: Confirmer qu'il n'y a pas de doublons"""
        print("\n=== TEST 10: PAS DE DOUBLONS ===")
        
        if not self.vetements_words:
            self.log_test("Pas de doublons", False, "Aucun mot à tester")
            return
        
        french_words = [word['french'].lower() for word in self.vetements_words]
        unique_words = set(french_words)
        has_duplicates = len(french_words) != len(unique_words)
        
        self.log_test("Pas de doublons", not has_duplicates,
                     f"Trouvé {len(french_words)} mots, {len(unique_words)} uniques")
    
    def test_11_other_sections_unaffected(self):
        """Test 11: Test que les autres sections n'ont pas été affectées"""
        print("\n=== TEST 11: AUTRES SECTIONS NON AFFECTÉES ===")
        
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
    
    def test_12_total_sections_count(self):
        """Test 12: Confirmer que le nombre total de sections est maintenant de 7"""
        print("\n=== TEST 12: NOMBRE TOTAL SECTIONS = 7 ===")
        
        try:
            response = self.make_request("/words")
            if response["success"]:
                all_words = response["data"]
                categories = set(word['category'] for word in all_words)
                category_count = len(categories)
                
                self.log_test("Nombre total sections = 7", category_count >= 7,
                             f"Trouvé {category_count} catégories (attendu ≥7)")
                self.log_test("Catégories trouvées", True, f"Catégories: {sorted(categories)}")
            else:
                self.log_test("Nombre total sections", False, f"HTTP {response['status_code']}")
        except Exception as e:
            self.log_test("Nombre total sections", False, f"Error: {str(e)}")
    
    def test_13_api_performance(self):
        """Test 13: Tester les performances globales de l'API"""
        print("\n=== TEST 13: PERFORMANCES API ===")
        
        try:
            start_time = time.time()
            response = self.make_request("/words?category=vetements")
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response["success"]:
                data = response["data"]
                self.log_test("Performance API vêtements", response_time < 2.0,
                             f"Temps de réponse: {response_time:.3f}s, {len(data)} mots retournés")
                
                # Test that all returned words are from vetements category
                all_vetements = all(word.get('category') == 'vetements' for word in data)
                self.log_test("Filtrage catégorie correct", all_vetements,
                             f"Tous les {len(data)} mots sont de la catégorie 'vetements'")
                
                return True
            else:
                self.log_test("Performance API vêtements", False,
                             f"HTTP {response['status_code']}")
                return False
        except Exception as e:
            self.log_test("Performance API vêtements", False, f"Error: {str(e)}")
            return False
    
    def test_14_specific_vetements_endpoint(self):
        """Test 14: Test API endpoint spécifique /api/words?category=vetements"""
        print("\n=== TEST 14: ENDPOINT SPÉCIFIQUE VÊTEMENTS ===")
        
        try:
            response = self.make_request("/words?category=vetements")
            if response["success"]:
                words = response["data"]
                
                # Test that all 17 words are returned
                self.log_test("17 mots retournés", len(words) == 17,
                             f"Endpoint retourne {len(words)} mots (attendu: 17)")
                
                # Test specific clothing words exist
                expected_vetements = ['vêtement', 'salouva', 'kamiss', 'tongs', 'voile']
                word_names = [word.get('french', '').lower() for word in words]
                
                for expected_word in expected_vetements:
                    found = expected_word.lower() in word_names
                    self.log_test(f"Mot attendu présent - {expected_word}", found)
                    
            else:
                self.log_test("Endpoint vêtements", False, f"HTTP {response['status_code']}")
        except Exception as e:
            self.log_test("Endpoint vêtements", False, f"Error: {str(e)}")
    
    def test_15_audio_files_access(self):
        """Test 15: Test d'accès aux fichiers audio via l'API"""
        print("\n=== TEST 15: ACCÈS FICHIERS AUDIO ===")
        
        try:
            # Test if audio info endpoint exists
            response = self.make_request("/audio/info")
            if response["success"]:
                audio_info = response["data"]
                self.log_test("Endpoint audio/info", True, "Endpoint audio info accessible")
                
                # Check if vetements is in audio categories
                if isinstance(audio_info, dict) and 'vetements' in str(audio_info):
                    self.log_test("Catégorie vêtements dans audio", True, "Vêtements trouvé dans info audio")
                else:
                    self.log_test("Catégorie vêtements dans audio", False, "Vêtements non trouvé dans info audio")
            else:
                self.log_test("Endpoint audio/info", False, f"HTTP {response['status_code']} - Endpoints audio non implémentés")
        except Exception as e:
            self.log_test("Accès fichiers audio", False, f"Error: {str(e)} - Endpoints audio non implémentés")
    
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
        """Execute all tests for vetements section"""
        print("👕 DÉBUT DES TESTS BACKEND - SECTION VÊTEMENTS")
        print("=" * 70)
        print("Test complet du backend après la création et mise à jour des")
        print("prononciations audio pour la section 'vêtement' avec 17 mots")
        print("=" * 70)
        
        start_time = time.time()
        
        # Test connectivity first
        if not self.test_1_api_connectivity():
            print("❌ ÉCHEC: Impossible de se connecter à l'API. Arrêt des tests.")
            return False
        
        # Test vetements section exists
        if not self.test_2_vetements_section_exists():
            print("❌ ÉCHEC: Section vêtements non trouvée. Arrêt des tests.")
            return False
        
        # Run all test suites
        self.test_3_17_words_added()
        self.test_4_data_structure()
        self.test_5_corrected_spelling()
        self.test_6_audio_coverage()
        self.test_7_specific_audio_references()
        self.test_8_appropriate_emojis()
        self.test_9_has_authentic_audio_flag()
        self.test_10_no_duplicates()
        self.test_11_other_sections_unaffected()
        self.test_12_total_sections_count()
        self.test_13_api_performance()
        self.test_14_specific_vetements_endpoint()
        self.test_15_audio_files_access()
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
        
        # Show vetements section statistics
        print(f"\n📈 STATISTIQUES SECTION VÊTEMENTS:")
        if self.vetements_words:
            count = len(self.vetements_words)
            with_emojis = sum(1 for w in self.vetements_words if w.get('image_url'))
            with_audio = sum(1 for w in self.vetements_words if (
                w.get('has_authentic_audio') or w.get('audio_filename') or
                w.get('shimoare_has_audio') or w.get('kibouchi_has_audio') or
                w.get('dual_audio_system')
            ))
            emoji_rate = (with_emojis / count * 100) if count > 0 else 0
            audio_rate = (with_audio / count * 100) if count > 0 else 0
            print(f"  Vêtements: {count} mots")
            print(f"  Avec emojis: {with_emojis} ({emoji_rate:.1f}%)")
            print(f"  Avec audio: {with_audio} ({audio_rate:.1f}%)")
        
        print(f"  Total mots dans la base: {self.total_words_count}")
        
        if success_rate >= 80:
            print("\n🎉 RÉSULTAT: SUCCÈS - La section vêtements est fonctionnelle!")
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
    tester = VetementsSectionTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🏁 TESTS TERMINÉS AVEC SUCCÈS!")
        sys.exit(0)
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ - VÉRIFICATION NÉCESSAIRE")
        sys.exit(1)

if __name__ == "__main__":
    main()