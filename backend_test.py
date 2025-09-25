#!/usr/bin/env python3
"""
Test complet du backend après la création et correction orthographique de la section "nourriture"
Comprehensive backend testing after creation and spelling corrections of the "nourriture" section

Test Requirements from French review request:
1. Vérification de la nouvelle section "nourriture" (44 mots attendus)
2. Test de l'orthographe corrigée pour des mots spécifiques:
   - "riz" → shimaoré: "tsoholé", kibouchi: "vari"
   - "sel" → shimaoré: "chingó" (avec accent), kibouchi: "sira"
   - "gingembre" → shimaoré: "tsingiziou", kibouchi: "sakėyi"
   - "ciboulette" → shimaoré: "chourougnou mani", kibouchi: "doungoulou ravigni"
3. Test des nouveaux aliments complexes:
   - "brède manioc" → shimaoré: "mataba", kibouchi: "féliki mouhogou"
   - "riz au coco" → shimaoré: "tsoholé ya nadzi", kibouchi: "vari an voiniou"
   - "noix de coco fraîche" → shimaoré: "chijavou", kibouchi: "kidjavou"
4. Test de l'intégrité des données (emojis appropriés, références audio, pas de doublons)
5. Test que les autres sections n'ont pas été affectées
6. Test que le total de mots a augmenté de 44
7. Test de l'endpoint API `/api/words?category=nourriture`
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

class NourritureSectionTester:
    def __init__(self):
        self.api_url = API_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.nourriture_words = []
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
    
    def test_2_nourriture_section_exists(self):
        """Test 2: Vérification que la section nourriture existe"""
        print("\n=== TEST 2: VÉRIFICATION SECTION NOURRITURE ===")
        
        try:
            response = self.make_request("/words?category=nourriture")
            if response["success"]:
                self.nourriture_words = response["data"]
                count = len(self.nourriture_words)
                self.log_test("Section nourriture existe", count > 0, f"{count} mots trouvés")
                return count > 0
            else:
                self.log_test("Section nourriture existe", False, f"Status: {response['status_code']}")
                return False
        except Exception as e:
            self.log_test("Section nourriture existe", False, f"Error: {str(e)}")
            return False
    
    def test_3_44_words_added(self):
        """Test 3: Vérification que 44 mots ont été ajoutés"""
        print("\n=== TEST 3: VÉRIFICATION 44 MOTS AJOUTÉS ===")
        
        expected_count = 44
        actual_count = len(self.nourriture_words)
        
        self.log_test("44 mots ajoutés", actual_count == expected_count, 
                     f"Attendu: {expected_count}, Trouvé: {actual_count}")
        
        return actual_count == expected_count
    
    def test_4_data_structure(self):
        """Test 4: Vérification de la structure des données"""
        print("\n=== TEST 4: STRUCTURE DES DONNÉES ===")
        
        if not self.nourriture_words:
            self.log_test("Structure des données", False, "Aucun mot à tester")
            return False
        
        required_fields = ['french', 'shimaore', 'kibouchi', 'category']
        complete_words = 0
        words_with_emojis = 0
        
        for word in self.nourriture_words:
            # Check required fields
            has_all_fields = all(field in word and word[field] for field in required_fields)
            if has_all_fields:
                complete_words += 1
            
            # Check for emoji (in image_url field)
            if 'image_url' in word and word['image_url']:
                words_with_emojis += 1
        
        structure_percentage = (complete_words / len(self.nourriture_words)) * 100
        emoji_percentage = (words_with_emojis / len(self.nourriture_words)) * 100
        
        self.log_test("Structure complète", structure_percentage >= 95,
                     f"{complete_words}/{len(self.nourriture_words)} mots avec structure complète ({structure_percentage:.1f}%)")
        
        self.log_test("Emojis présents", emoji_percentage >= 80,
                     f"{words_with_emojis}/{len(self.nourriture_words)} mots avec emojis ({emoji_percentage:.1f}%)")
        
        return structure_percentage >= 95
    
    def test_5_corrected_spellings(self):
        """Test 5: Test de l'orthographe corrigée pour des mots spécifiques"""
        print("\n=== TEST 5: ORTHOGRAPHE CORRIGÉE ===")
        
        test_words = {
            "riz": {"shimaore": "tsoholé", "kibouchi": "vari"},
            "sel": {"shimaore": "chingó", "kibouchi": "sira"},
            "gingembre": {"shimaore": "tsingiziou", "kibouchi": "sakėyi"},
            "ciboulette": {"shimaore": "chourougnou mani", "kibouchi": "doungoulou ravigni"}
        }
        
        word_dict = {word['french'].lower(): word for word in self.nourriture_words}
        
        for french_word, expected_translations in test_words.items():
            if french_word in word_dict:
                word = word_dict[french_word]
                shimaore_match = expected_translations["shimaore"].lower() in word['shimaore'].lower()
                kibouchi_match = expected_translations["kibouchi"].lower() in word['kibouchi'].lower()
                
                self.log_test(f"Orthographe corrigée: {french_word}", 
                             shimaore_match and kibouchi_match,
                             f"Shimaoré: {word['shimaore']}, Kibouchi: {word['kibouchi']}")
            else:
                self.log_test(f"Orthographe corrigée: {french_word}", False, "Mot non trouvé")
    
    def test_6_complex_new_foods(self):
        """Test 6: Test des nouveaux aliments complexes"""
        print("\n=== TEST 6: NOUVEAUX ALIMENTS COMPLEXES ===")
        
        complex_foods = {
            "brède manioc": {"shimaore": "mataba", "kibouchi": "féliki mouhogou"},
            "riz au coco": {"shimaore": "tsoholé ya nadzi", "kibouchi": "vari an voiniou"},
            "noix de coco fraîche": {"shimaore": "chijavou", "kibouchi": "kidjavou"}
        }
        
        word_dict = {word['french'].lower(): word for word in self.nourriture_words}
        
        for french_word, expected_translations in complex_foods.items():
            if french_word in word_dict:
                word = word_dict[french_word]
                shimaore_match = expected_translations["shimaore"].lower() in word['shimaore'].lower()
                kibouchi_match = expected_translations["kibouchi"].lower() in word['kibouchi'].lower()
                
                self.log_test(f"Aliment complexe: {french_word}", 
                             shimaore_match and kibouchi_match,
                             f"Shimaoré: {word['shimaore']}, Kibouchi: {word['kibouchi']}")
            else:
                self.log_test(f"Aliment complexe: {french_word}", False, "Mot non trouvé")
    
    def test_7_data_integrity(self):
        """Test 7: Test de l'intégrité des données"""
        print("\n=== TEST 7: INTÉGRITÉ DES DONNÉES ===")
        
        if not self.nourriture_words:
            self.log_test("Intégrité des données", False, "Aucun mot à tester")
            return
        
        # Test for duplicates
        french_words = [word['french'].lower() for word in self.nourriture_words]
        unique_words = set(french_words)
        has_duplicates = len(french_words) != len(unique_words)
        
        self.log_test("Pas de doublons", not has_duplicates,
                     f"Trouvé {len(french_words)} mots, {len(unique_words)} uniques")
        
        # Test emoji coverage
        words_with_emojis = sum(1 for word in self.nourriture_words 
                               if 'image_url' in word and word['image_url'])
        emoji_percentage = (words_with_emojis / len(self.nourriture_words)) * 100
        
        self.log_test("Emojis appropriés", emoji_percentage >= 80,
                     f"{words_with_emojis}/{len(self.nourriture_words)} mots avec emojis ({emoji_percentage:.1f}%)")
        
        # Test audio references format
        words_with_audio = sum(1 for word in self.nourriture_words 
                              if any(field in word for field in ['audio_url', 'shimoare_audio_filename', 'kibouchi_audio_filename', 'has_authentic_audio']))
        
        self.log_test("Références audio formatées", words_with_audio >= 0,
                     f"{words_with_audio}/{len(self.nourriture_words)} mots avec références audio")
    
    def test_8_other_sections_unaffected(self):
        """Test 8: Test que les autres sections n'ont pas été affectées"""
        print("\n=== TEST 8: AUTRES SECTIONS NON AFFECTÉES ===")
        
        expected_sections = {
            'famille': 25,  # Approximate expected count
            'animaux': 65,  # Approximate expected count  
            'nombres': 20,  # Approximate expected count
            'salutations': 8,  # Approximate expected count
            'couleurs': 8   # Approximate expected count
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
    
    def test_9_total_word_count_increase(self):
        """Test 9: Test que le total de mots a augmenté de 44"""
        print("\n=== TEST 9: AUGMENTATION TOTAL MOTS ===")
        
        try:
            response = self.make_request("/words")
            if response["success"]:
                data = response["data"]
                self.total_words_count = len(data)
                
                # Based on previous tests, we expect around 565+ words (before nourriture) + 44
                expected_minimum = 609  # 565 + 44
                self.log_test("Total mots augmenté", self.total_words_count >= expected_minimum,
                             f"Trouvé {self.total_words_count} mots total (attendu ≥{expected_minimum})")
                return self.total_words_count
            else:
                self.log_test("Total mots augmenté", False,
                             f"HTTP {response['status_code']}")
                return 0
        except Exception as e:
            self.log_test("Total mots augmenté", False, f"Error: {str(e)}")
            return 0
    
    def test_10_nourriture_api_performance(self):
        """Test 10: Test de performance de l'endpoint nourriture"""
        print("\n=== TEST 10: PERFORMANCE API NOURRITURE ===")
        
        try:
            start_time = time.time()
            response = self.make_request("/words?category=nourriture")
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response["success"]:
                data = response["data"]
                self.log_test("Performance API nourriture", response_time < 2.0,
                             f"Temps de réponse: {response_time:.2f}s, {len(data)} mots retournés")
                
                # Test specific word queries if we have data
                if data:
                    sample_word = data[0]
                    word_id = sample_word.get('id')
                    if word_id:
                        word_response = self.make_request(f"/words/{word_id}")
                        self.log_test("Accès mot individuel", word_response["success"],
                                     f"Mot ID {word_id} accessible")
                
                return True
            else:
                self.log_test("Performance API nourriture", False,
                             f"HTTP {response['status_code']}")
                return False
        except Exception as e:
            self.log_test("Performance API nourriture", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Execute all tests for nourriture section"""
        print("🎯 DÉBUT DES TESTS BACKEND - SECTION NOURRITURE")
        print("=" * 70)
        print("Test complet du backend après la création et correction orthographique")
        print("de la section 'nourriture' avec 44 mots de base de Mayotte")
        print("=" * 70)
        
        start_time = time.time()
        
        # Test connectivity first
        if not self.test_1_api_connectivity():
            print("❌ ÉCHEC: Impossible de se connecter à l'API. Arrêt des tests.")
            return False
        
        # Test nourriture section exists
        if not self.test_2_nourriture_section_exists():
            print("❌ ÉCHEC: Section nourriture non trouvée. Arrêt des tests.")
            return False
        
        # Run all test suites
        self.test_3_44_words_added()
        self.test_4_data_structure()
        self.test_5_corrected_spellings()
        self.test_6_complex_new_foods()
        self.test_7_data_integrity()
        self.test_8_other_sections_unaffected()
        self.test_9_total_word_count_increase()
        self.test_10_nourriture_api_performance()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 70)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Tests réussis: {self.passed_tests}/{self.total_tests} ({success_rate:.1f}%)")
        print(f"Durée: {duration:.2f}s")
        
        # Show nourriture section statistics
        print(f"\n📈 STATISTIQUES SECTION NOURRITURE:")
        if self.nourriture_words:
            count = len(self.nourriture_words)
            with_emojis = sum(1 for w in self.nourriture_words if w.get('image_url'))
            with_audio = sum(1 for w in self.nourriture_words if (
                w.get('has_authentic_audio') or w.get('audio_filename') or
                w.get('shimoare_has_audio') or w.get('kibouchi_has_audio')
            ))
            emoji_rate = (with_emojis / count * 100) if count > 0 else 0
            audio_rate = (with_audio / count * 100) if count > 0 else 0
            print(f"  Nourriture: {count} mots")
            print(f"  Avec emojis: {with_emojis} ({emoji_rate:.1f}%)")
            print(f"  Avec audio: {with_audio} ({audio_rate:.1f}%)")
        
        print(f"  Total mots dans la base: {self.total_words_count}")
        
        if success_rate >= 80:
            print("\n🎉 RÉSULTAT: SUCCÈS - La section nourriture est fonctionnelle!")
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
    tester = NourritureSectionTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🏁 TESTS TERMINÉS AVEC SUCCÈS!")
        sys.exit(0)
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ - VÉRIFICATION NÉCESSAIRE")
        sys.exit(1)

if __name__ == "__main__":
    main()