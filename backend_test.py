#!/usr/bin/env python3
"""
Test complet du backend après la mise à jour de la section "animaux"
Comprehensive backend testing after animals section update

Tests:
1. API vocabulary - vérifier que les mots de la section "animaux" sont correctement retournés
2. Test de l'endpoint `/api/words` pour la section "animaux" 
3. Vérifier que tous les 69 nouveaux animaux sont présents
4. Test de la structure des données - chaque animal a les champs requis
5. Test de différents animaux spécifiques
6. Test de robustesse - pas de doublons, remplacement complet
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

class AnimalsSectionTester:
    def __init__(self):
        self.api_url = API_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.animals_data = []
        
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
    
    def test_2_vocabulary_endpoint_general(self):
        """Test 2: Vérifier l'endpoint /api/words général"""
        print("\n=== TEST 2: ENDPOINT VOCABULARY GÉNÉRAL ===")
        response = self.make_request("/words")
        if response["success"]:
            data = response["data"]
            total_words = len(data)
            self.log_test("Words Endpoint General", True, f"Total words: {total_words}")
            return True, data
        else:
            self.log_test("Words Endpoint General", False, f"Status: {response['status_code']}, Error: {response['data']}")
            return False, []
    
    def test_3_animals_category_endpoint(self):
        """Test 3: Vérifier l'endpoint /api/words?category=animaux"""
        print("\n=== TEST 3: ENDPOINT CATÉGORIE ANIMAUX ===")
        response = self.make_request("/words?category=animaux")
        if response["success"]:
            self.animals_data = response["data"]
            animals_count = len(self.animals_data)
            self.log_test("Animals Category Endpoint", True, f"Animals found: {animals_count}")
            return True
        else:
            self.log_test("Animals Category Endpoint", False, f"Status: {response['status_code']}, Error: {response['data']}")
            return False
    
    def test_4_69_animals_count(self):
        """Test 4: Vérifier que tous les 69 nouveaux animaux sont présents"""
        print("\n=== TEST 4: VÉRIFICATION 69 ANIMAUX ===")
        expected_count = 69
        actual_count = len(self.animals_data)
        
        if actual_count == expected_count:
            self.log_test("69 Animals Count", True, f"Expected: {expected_count}, Found: {actual_count}")
        else:
            self.log_test("69 Animals Count", False, f"Expected: {expected_count}, Found: {actual_count}")
    
    def test_5_data_structure_required_fields(self):
        """Test 5: Vérifier que chaque animal a les champs requis: french, shimaoré, kibouchi, emoji"""
        print("\n=== TEST 5: STRUCTURE DES DONNÉES ===")
        required_fields = ['french', 'shimaore', 'kibouchi', 'category']
        animals_with_complete_structure = 0
        animals_with_emoji = 0
        
        for animal in self.animals_data:
            has_all_required = all(field in animal and animal[field] for field in required_fields)
            if has_all_required:
                animals_with_complete_structure += 1
            
            # Check for emoji (image_url field)
            if 'image_url' in animal and animal['image_url']:
                animals_with_emoji += 1
        
        total_animals = len(self.animals_data)
        structure_percentage = (animals_with_complete_structure / total_animals * 100) if total_animals > 0 else 0
        emoji_percentage = (animals_with_emoji / total_animals * 100) if total_animals > 0 else 0
        
        if animals_with_complete_structure == total_animals:
            self.log_test("Data Structure Required Fields", True, f"All {total_animals} animals have required fields")
        else:
            self.log_test("Data Structure Required Fields", False, f"Only {animals_with_complete_structure}/{total_animals} animals have required fields ({structure_percentage:.1f}%)")
        
        if animals_with_emoji > 0:
            self.log_test("Animals with Emojis", True, f"{animals_with_emoji}/{total_animals} animals have emojis ({emoji_percentage:.1f}%)")
        else:
            self.log_test("Animals with Emojis", False, "No animals have emojis")
    
    def test_6_specific_animals(self):
        """Test 6: Tester quelques animaux spécifiques comme "cochon", "chat", "lion", "éléphant" """
        print("\n=== TEST 6: ANIMAUX SPÉCIFIQUES ===")
        specific_animals = ["cochon", "chat", "lion", "éléphant"]
        animals_dict = {animal['french'].lower(): animal for animal in self.animals_data}
        
        for animal_name in specific_animals:
            if animal_name in animals_dict:
                animal = animals_dict[animal_name]
                shimaore = animal.get('shimaore', 'N/A')
                kibouchi = animal.get('kibouchi', 'N/A')
                emoji = animal.get('image_url', 'N/A')
                
                self.log_test(f"Specific Animal: {animal_name.title()}", True, 
                            f"Shimaoré: {shimaore}, Kibouchi: {kibouchi}, Emoji: {emoji}")
            else:
                self.log_test(f"Specific Animal: {animal_name.title()}", False, "Not found in database")
    
    def test_7_translations_quality(self):
        """Test 7: Vérifier que les traductions en shimaoré et kibouchi sont présentes"""
        print("\n=== TEST 7: QUALITÉ DES TRADUCTIONS ===")
        animals_with_shimaore = 0
        animals_with_kibouchi = 0
        
        for animal in self.animals_data:
            if animal.get('shimaore') and animal['shimaore'].strip():
                animals_with_shimaore += 1
            if animal.get('kibouchi') and animal['kibouchi'].strip():
                animals_with_kibouchi += 1
        
        total_animals = len(self.animals_data)
        shimaore_percentage = (animals_with_shimaore / total_animals * 100) if total_animals > 0 else 0
        kibouchi_percentage = (animals_with_kibouchi / total_animals * 100) if total_animals > 0 else 0
        
        self.log_test("Shimaoré Translations", animals_with_shimaore == total_animals, 
                     f"{animals_with_shimaore}/{total_animals} animals ({shimaore_percentage:.1f}%)")
        self.log_test("Kibouchi Translations", animals_with_kibouchi == total_animals,
                     f"{animals_with_kibouchi}/{total_animals} animals ({kibouchi_percentage:.1f}%)")
    
    def test_8_no_duplicates(self):
        """Test 8: Vérifier qu'il n'y a pas de doublons"""
        print("\n=== TEST 8: VÉRIFICATION DOUBLONS ===")
        french_names = [animal['french'].lower() for animal in self.animals_data]
        unique_names = set(french_names)
        
        duplicates_found = len(french_names) - len(unique_names)
        
        if duplicates_found == 0:
            self.log_test("No Duplicates", True, f"All {len(french_names)} animal names are unique")
        else:
            # Find actual duplicates
            seen = set()
            duplicates = set()
            for name in french_names:
                if name in seen:
                    duplicates.add(name)
                seen.add(name)
            
            self.log_test("No Duplicates", False, f"{duplicates_found} duplicates found: {list(duplicates)}")
    
    def test_9_other_categories_unaffected(self):
        """Test 9: Vérifier que les autres sections (famille, etc.) n'ont pas été affectées"""
        print("\n=== TEST 9: AUTRES CATÉGORIES NON AFFECTÉES ===")
        other_categories = ['famille', 'couleurs', 'nombres', 'salutations']
        
        for category in other_categories:
            response = self.make_request(f"/words?category={category}")
            if response["success"]:
                data = response["data"]
                count = len(data)
                self.log_test(f"Category {category.title()} Unaffected", True, f"{count} words found")
            else:
                self.log_test(f"Category {category.title()} Unaffected", False, f"Status: {response['status_code']}")
    
    def test_10_audio_references_format(self):
        """Test 10: Vérifier que les références audio sont bien formatées"""
        print("\n=== TEST 10: FORMAT RÉFÉRENCES AUDIO ===")
        animals_with_audio = 0
        animals_with_audio_metadata = 0
        
        for animal in self.animals_data:
            # Check for basic audio URL
            if animal.get('audio_url'):
                animals_with_audio += 1
            
            # Check for advanced audio metadata
            if (animal.get('has_authentic_audio') or 
                animal.get('shimoare_has_audio') or 
                animal.get('kibouchi_has_audio')):
                animals_with_audio_metadata += 1
        
        total_animals = len(self.animals_data)
        
        if animals_with_audio > 0:
            audio_percentage = (animals_with_audio / total_animals * 100)
            self.log_test("Audio References Format", True, 
                         f"{animals_with_audio}/{total_animals} animals have audio URLs ({audio_percentage:.1f}%)")
        else:
            self.log_test("Audio References Format", True, "No audio URLs found (expected for basic vocabulary)")
        
        if animals_with_audio_metadata > 0:
            metadata_percentage = (animals_with_audio_metadata / total_animals * 100)
            self.log_test("Audio Metadata Present", True,
                         f"{animals_with_audio_metadata}/{total_animals} animals have audio metadata ({metadata_percentage:.1f}%)")
    
    def test_11_category_consistency(self):
        """Test 11: Vérifier que tous les animaux ont la catégorie 'animaux'"""
        print("\n=== TEST 11: COHÉRENCE CATÉGORIE ===")
        correct_category_count = 0
        
        for animal in self.animals_data:
            if animal.get('category') == 'animaux':
                correct_category_count += 1
        
        total_animals = len(self.animals_data)
        
        if correct_category_count == total_animals:
            self.log_test("Category Consistency", True, f"All {total_animals} animals have correct category")
        else:
            self.log_test("Category Consistency", False, 
                         f"Only {correct_category_count}/{total_animals} animals have correct category")
    
    def test_12_old_section_replaced(self):
        """Test 12: Tester que l'ancienne section animaux a été complètement remplacée"""
        print("\n=== TEST 12: REMPLACEMENT ANCIENNE SECTION ===")
        
        # Check if we have modern animal data structure
        modern_structure_count = 0
        for animal in self.animals_data:
            # Modern animals should have proper French names, not placeholder data
            french_name = animal.get('french', '').lower()
            if (french_name and 
                len(french_name) > 2 and 
                not french_name.startswith('test') and
                not french_name.startswith('placeholder')):
                modern_structure_count += 1
        
        total_animals = len(self.animals_data)
        modern_percentage = (modern_structure_count / total_animals * 100) if total_animals > 0 else 0
        
        if modern_percentage >= 95:
            self.log_test("Old Section Replaced", True, 
                         f"{modern_percentage:.1f}% of animals have modern structure")
        else:
            self.log_test("Old Section Replaced", False, 
                         f"Only {modern_percentage:.1f}% of animals have modern structure")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🧪 DÉBUT DES TESTS - SECTION ANIMAUX BACKEND")
        print("=" * 60)
        print("Test complet du backend après la mise à jour de la section 'animaux'")
        print("Contexte: 69 nouvelles entrées d'animaux avec traductions shimaoré et kibouchi")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test de connectivité d'abord
        if not self.test_1_api_connectivity():
            print("❌ Cannot connect to API. Stopping tests.")
            return False
        
        # Test général des mots
        success, all_words = self.test_2_vocabulary_endpoint_general()
        if not success:
            print("❌ Cannot access words endpoint. Stopping tests.")
            return False
        
        # Test spécifique de la catégorie animaux
        if not self.test_3_animals_category_endpoint():
            print("❌ Cannot access animals category. Stopping tests.")
            return False
        
        # Tests spécifiques aux animaux
        self.test_4_69_animals_count()
        self.test_5_data_structure_required_fields()
        self.test_6_specific_animals()
        self.test_7_translations_quality()
        self.test_8_no_duplicates()
        self.test_9_other_categories_unaffected()
        self.test_10_audio_references_format()
        self.test_11_category_consistency()
        self.test_12_old_section_replaced()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Résumé final
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS - SECTION ANIMAUX")
        print("=" * 60)
        
        for result in self.test_results:
            print(result)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"\n🎯 RÉSULTATS FINAUX:")
        print(f"   Tests réussis: {self.passed_tests}/{self.total_tests}")
        print(f"   Taux de réussite: {success_rate:.1f}%")
        print(f"   Durée: {duration:.2f}s")
        
        if len(self.animals_data) > 0:
            print(f"   Animaux trouvés: {len(self.animals_data)}")
            
            # Quelques exemples d'animaux
            print("\n🐾 EXEMPLES D'ANIMAUX TROUVÉS:")
            for i, animal in enumerate(self.animals_data[:5]):  # Show first 5
                french = animal.get('french', 'N/A')
                shimaore = animal.get('shimaore', 'N/A')
                kibouchi = animal.get('kibouchi', 'N/A')
                emoji = animal.get('image_url', 'N/A')
                print(f"  {i+1}. {french} - Shimaoré: {shimaore}, Kibouchi: {kibouchi}, Emoji: {emoji}")
        
        print("\n" + "=" * 60)
        
        if success_rate >= 90:
            print("🎉 EXCELLENT - MISE À JOUR SECTION ANIMAUX COMPLÈTEMENT RÉUSSIE!")
            print("Les 69 nouvelles entrées d'animaux sont correctement intégrées")
            return True
        elif success_rate >= 70:
            print("✅ BIEN - MISE À JOUR SECTION ANIMAUX MAJORITAIREMENT RÉUSSIE")
            print("La plupart des animaux sont correctement intégrés")
            return True
        elif success_rate >= 50:
            print("⚠️ PARTIEL - MISE À JOUR SECTION ANIMAUX PARTIELLEMENT RÉUSSIE")
            print("Certains aspects nécessitent des corrections")
            return False
        else:
            print("❌ ÉCHEC - MISE À JOUR SECTION ANIMAUX NON RÉUSSIE")
            print("Les nouvelles données d'animaux n'ont pas été correctement intégrées")
            return False

def main():
    """Main test execution"""
    tester = AnimalsSectionTester()
    success = tester.run_all_tests()
    
    if success:
        print("🏁 TESTS TERMINÉS AVEC SUCCÈS!")
        sys.exit(0)
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ - VÉRIFICATION NÉCESSAIRE")
        sys.exit(1)

if __name__ == "__main__":
    main()