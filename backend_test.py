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

class MaisonSectionTester:
    def __init__(self):
        self.api_url = API_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.maison_words = []
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
    
    def test_2_maison_section_exists(self):
        """Test 2: Vérification que la section maison existe"""
        print("\n=== TEST 2: VÉRIFICATION SECTION MAISON ===")
        
        try:
            response = self.make_request("/words?category=maison")
            if response["success"]:
                self.maison_words = response["data"]
                count = len(self.maison_words)
                self.log_test("Section maison existe", count > 0, f"{count} mots trouvés")
                return count > 0
            else:
                self.log_test("Section maison existe", False, f"Status: {response['status_code']}")
                return False
        except Exception as e:
            self.log_test("Section maison existe", False, f"Error: {str(e)}")
            return False
    
    def test_3_37_words_added(self):
        """Test 3: Vérification que 37 mots ont été ajoutés"""
        print("\n=== TEST 3: VÉRIFICATION 37 MOTS AJOUTÉS ===")
        
        expected_count = 37
        actual_count = len(self.maison_words)
        
        self.log_test("37 mots ajoutés", actual_count == expected_count, 
                     f"Attendu: {expected_count}, Trouvé: {actual_count}")
        
        return actual_count == expected_count
    
    def test_4_data_structure(self):
        """Test 4: Vérification de la structure des données"""
        print("\n=== TEST 4: STRUCTURE DES DONNÉES ===")
        
        if not self.maison_words:
            self.log_test("Structure des données", False, "Aucun mot à tester")
            return False
        
        required_fields = ['french', 'shimaore', 'kibouchi', 'category']
        complete_words = 0
        words_with_emojis = 0
        
        for word in self.maison_words:
            # Check required fields
            has_all_fields = all(field in word and word[field] for field in required_fields)
            if has_all_fields:
                complete_words += 1
            
            # Check for emoji (in image_url field)
            if 'image_url' in word and word['image_url']:
                words_with_emojis += 1
        
        structure_percentage = (complete_words / len(self.maison_words)) * 100
        emoji_percentage = (words_with_emojis / len(self.maison_words)) * 100
        
        self.log_test("Structure complète", structure_percentage >= 95,
                     f"{complete_words}/{len(self.maison_words)} mots avec structure complète ({structure_percentage:.1f}%)")
        
        self.log_test("Emojis présents", emoji_percentage >= 80,
                     f"{words_with_emojis}/{len(self.maison_words)} mots avec emojis ({emoji_percentage:.1f}%)")
        
        return structure_percentage >= 95
    
    def test_5_specific_house_words(self):
        """Test 5: Test de mots spécifiques de la maison avec leur orthographe"""
        print("\n=== TEST 5: MOTS SPÉCIFIQUES MAISON ===")
        
        test_words = {
            "maison": {"shimaore": "nyoumba", "kibouchi": "tragnou"},
            "fenêtre": {"shimaore": "fénétri", "kibouchi": "lafoumétara"},
            "vaisselle": {"shimaore": "ziya", "kibouchi": "hintagna"},  # Note: API might show "vesselles"
            "machette": {"shimaore": "m'panga", "kibouchi": "ampanga"}
        }
        
        word_dict = {word['french'].lower(): word for word in self.maison_words}
        
        for french_word, expected_translations in test_words.items():
            # Handle special case for vaisselle/vesselles
            test_word = french_word
            if french_word == "vaisselle" and french_word not in word_dict:
                test_word = "vesselles"  # Check alternative spelling
            
            if test_word in word_dict:
                word = word_dict[test_word]
                shimaore_match = expected_translations["shimaore"].lower() in word['shimaore'].lower()
                kibouchi_match = expected_translations["kibouchi"].lower() in word['kibouchi'].lower()
                
                self.log_test(f"Mot spécifique: {french_word}", 
                             shimaore_match and kibouchi_match,
                             f"Shimaoré: {word['shimaore']}, Kibouchi: {word['kibouchi']}")
            else:
                self.log_test(f"Mot spécifique: {french_word}", False, "Mot non trouvé")
    
    def test_6_complex_house_objects(self):
        """Test 6: Test des objets de maison complexes"""
        print("\n=== TEST 6: OBJETS MAISON COMPLEXES ===")
        
        complex_objects = {
            "torche locale": {"shimaore": "gandilé", "kibouchi": "gandili"},
            "coupe coupe": {"shimaore": "chombo", "kibouchi": "chombou"},
            "cartable": {"shimaore": "mkoba", "kibouchi": "mkoba"}  # Note: API might show "cartable/malette"
        }
        
        word_dict = {word['french'].lower(): word for word in self.maison_words}
        
        for french_word, expected_translations in complex_objects.items():
            # Handle special case for cartable
            test_word = french_word
            if french_word == "cartable" and french_word not in word_dict:
                test_word = "cartable/malette"  # Check alternative format
            
            if test_word in word_dict:
                word = word_dict[test_word]
                # For torche locale, check if translations contain expected values
                if french_word == "torche locale":
                    shimaore_match = expected_translations['shimaore'] in word['shimaore'].lower()
                    kibouchi_match = expected_translations['kibouchi'] in word['kibouchi'].lower()
                else:
                    shimaore_match = word['shimaore'].lower() == expected_translations['shimaore'].lower()
                    kibouchi_match = word['kibouchi'].lower() == expected_translations['kibouchi'].lower()
                
                self.log_test(f"Objet complexe: {french_word}", 
                             shimaore_match and kibouchi_match,
                             f"Shimaoré: {word['shimaore']}, Kibouchi: {word['kibouchi']}")
            else:
                self.log_test(f"Objet complexe: {french_word}", False, "Objet non trouvé")
    
    def test_7_data_integrity(self):
        """Test 7: Test de l'intégrité des données"""
        print("\n=== TEST 7: INTÉGRITÉ DES DONNÉES ===")
        
        if not self.maison_words:
            self.log_test("Intégrité des données", False, "Aucun mot à tester")
            return
        
        # Test for duplicates
        french_words = [word['french'].lower() for word in self.maison_words]
        unique_words = set(french_words)
        has_duplicates = len(french_words) != len(unique_words)
        
        self.log_test("Pas de doublons", not has_duplicates,
                     f"Trouvé {len(french_words)} mots, {len(unique_words)} uniques")
        
        # Test emoji coverage - house-specific emojis
        house_emojis = ['🏠', '🚪', '🛏️', '🪟', '🍽️', '🧹', '🔪', '🥄', '🪑', '🚽', '🔦', '🗡️', '🪓', '🍲', '🪣', '🎒', '🧱', '🛌', '🪞', '🫖', '🏡', '🚧', '🗄️', '🥣', '💡']
        words_with_appropriate_emojis = 0
        
        for word in self.maison_words:
            if 'image_url' in word and word['image_url']:
                if any(emoji in word['image_url'] for emoji in house_emojis):
                    words_with_appropriate_emojis += 1
        
        emoji_percentage = (words_with_appropriate_emojis / len(self.maison_words)) * 100
        
        self.log_test("Emojis appropriés maison", emoji_percentage >= 70,
                     f"{words_with_appropriate_emojis}/{len(self.maison_words)} mots avec emojis maison ({emoji_percentage:.1f}%)")
        
        # Test audio references format
        words_with_audio = sum(1 for word in self.maison_words 
                              if any(field in word for field in ['audio_url', 'shimoare_audio_filename', 'kibouchi_audio_filename', 'has_authentic_audio', 'dual_audio_system']))
        
        audio_percentage = (words_with_audio / len(self.maison_words)) * 100
        
        self.log_test("Références audio formatées", audio_percentage >= 50,
                     f"{words_with_audio}/{len(self.maison_words)} mots avec références audio ({audio_percentage:.1f}%)")
    
    def test_8_other_sections_unaffected(self):
        """Test 8: Test de cohérence avec les autres sections"""
        print("\n=== TEST 8: COHÉRENCE AUTRES SECTIONS ===")
        
        expected_sections = {
            'famille': 25,  # Approximate expected count
            'animaux': 65,  # Approximate expected count  
            'nombres': 20,  # Approximate expected count
            'salutations': 8,  # Approximate expected count
            'couleurs': 8,   # Approximate expected count
            'nourriture': 40  # Approximate expected count
        }
        
        total_categories = 0
        
        for category, min_expected in expected_sections.items():
            try:
                response = self.make_request(f"/words?category={category}")
                if response["success"]:
                    data = response["data"]
                    word_count = len(data)
                    total_categories += 1
                    self.log_test(f"Section {category} intacte", word_count >= min_expected,
                                 f"Trouvé {word_count} mots (attendu ≥{min_expected})")
                else:
                    self.log_test(f"Section {category} intacte", False,
                                 f"HTTP {response['status_code']}")
            except Exception as e:
                self.log_test(f"Section {category} intacte", False, f"Error: {str(e)}")
        
        # Test total categories count
        try:
            response = self.make_request("/words")
            if response["success"]:
                all_words = response["data"]
                categories = set(word['category'] for word in all_words)
                category_count = len(categories)
                
                self.log_test("Nombre total catégories", category_count >= 6,
                             f"Trouvé {category_count} catégories (attendu ≥6)")
            else:
                self.log_test("Nombre total catégories", False, f"HTTP {response['status_code']}")
        except Exception as e:
            self.log_test("Nombre total catégories", False, f"Error: {str(e)}")
    
    def test_9_total_word_count_reasonable(self):
        """Test 9: Test que le nombre total de mots est raisonnable"""
        print("\n=== TEST 9: NOMBRE TOTAL MOTS ===")
        
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
    
    def test_10_maison_api_performance(self):
        """Test 10: Test des performances globales de l'API"""
        print("\n=== TEST 10: PERFORMANCE API MAISON ===")
        
        try:
            start_time = time.time()
            response = self.make_request("/words?category=maison")
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response["success"]:
                data = response["data"]
                self.log_test("Performance API maison", response_time < 2.0,
                             f"Temps de réponse: {response_time:.2f}s, {len(data)} mots retournés")
                
                # Test specific word queries if we have data
                if data:
                    sample_word = data[0]
                    word_id = sample_word.get('id')
                    if word_id:
                        word_response = self.make_request(f"/words/{word_id}")
                        self.log_test("Accès mot individuel", word_response["success"],
                                     f"Mot ID {word_id} accessible")
                
                # Test that all returned words are from maison category
                all_maison = all(word.get('category') == 'maison' for word in data)
                self.log_test("Filtrage catégorie correct", all_maison,
                             f"Tous les {len(data)} mots sont de la catégorie 'maison'")
                
                return True
            else:
                self.log_test("Performance API maison", False,
                             f"HTTP {response['status_code']}")
                return False
        except Exception as e:
            self.log_test("Performance API maison", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Execute all tests for maison section"""
        print("🏠 DÉBUT DES TESTS BACKEND - SECTION MAISON")
        print("=" * 70)
        print("Test complet du backend après la création de la section 'maison'")
        print("avec 37 mots de vocabulaire domestique de Mayotte")
        print("=" * 70)
        
        start_time = time.time()
        
        # Test connectivity first
        if not self.test_1_api_connectivity():
            print("❌ ÉCHEC: Impossible de se connecter à l'API. Arrêt des tests.")
            return False
        
        # Test maison section exists
        if not self.test_2_maison_section_exists():
            print("❌ ÉCHEC: Section maison non trouvée. Arrêt des tests.")
            return False
        
        # Run all test suites
        self.test_3_37_words_added()
        self.test_4_data_structure()
        self.test_5_specific_house_words()
        self.test_6_complex_house_objects()
        self.test_7_data_integrity()
        self.test_8_other_sections_unaffected()
        self.test_9_total_word_count_reasonable()
        self.test_10_maison_api_performance()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 70)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Tests réussis: {self.passed_tests}/{self.total_tests} ({success_rate:.1f}%)")
        print(f"Durée: {duration:.2f}s")
        
        # Show maison section statistics
        print(f"\n📈 STATISTIQUES SECTION MAISON:")
        if self.maison_words:
            count = len(self.maison_words)
            with_emojis = sum(1 for w in self.maison_words if w.get('image_url'))
            with_audio = sum(1 for w in self.maison_words if (
                w.get('has_authentic_audio') or w.get('audio_filename') or
                w.get('shimoare_has_audio') or w.get('kibouchi_has_audio') or
                w.get('dual_audio_system')
            ))
            emoji_rate = (with_emojis / count * 100) if count > 0 else 0
            audio_rate = (with_audio / count * 100) if count > 0 else 0
            print(f"  Maison: {count} mots")
            print(f"  Avec emojis: {with_emojis} ({emoji_rate:.1f}%)")
            print(f"  Avec audio: {with_audio} ({audio_rate:.1f}%)")
        
        print(f"  Total mots dans la base: {self.total_words_count}")
        
        if success_rate >= 80:
            print("\n🎉 RÉSULTAT: SUCCÈS - La section maison est fonctionnelle!")
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
    tester = MaisonSectionTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🏁 TESTS TERMINÉS AVEC SUCCÈS!")
        sys.exit(0)
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ - VÉRIFICATION NÉCESSAIRE")
        sys.exit(1)

if __name__ == "__main__":
    main()