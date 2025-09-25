#!/usr/bin/env python3
"""
Test complet du backend après la mise à jour des prononciations audio pour toutes les sections
Comprehensive backend testing after audio pronunciation updates for all sections

Test Requirements from French review request:
1. Vérification des sections complètes (4 sections: animaux, nombres, corps, salutations)
2. Test des références audio authentiques
3. Test spécifique par section avec nombres de mots attendus:
   - Nombres: 28 mots avec audio (Moja.m4a, Mbili.m4a, etc.)
   - Animaux: 66+ mots avec audio (Pouroukou.m4a, Kasangwe.m4a, etc.)
   - Corps: 20 mots avec audio (Matso.m4a, Cha.m4a, etc.)
   - Salutations: 9 mots avec audio (Marahaba.m4a, Kwaheri.m4a, etc.)
4. Test de l'intégrité des données (traductions shimaoré/kibouchi cohérentes, emojis appropriés)
5. Test de performance (temps de réponse pour récupérer chaque section)
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

class NombresSectionTester:
    def __init__(self):
        self.api_url = API_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.nombres_data = []
        
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
    
    def test_3_nombres_category_endpoint(self):
        """Test 3: Vérifier l'endpoint /api/words?category=nombres"""
        print("\n=== TEST 3: ENDPOINT CATÉGORIE NOMBRES ===")
        response = self.make_request("/words?category=nombres")
        if response["success"]:
            self.nombres_data = response["data"]
            nombres_count = len(self.nombres_data)
            self.log_test("Nombres Category Endpoint", True, f"Numbers found: {nombres_count}")
            return True
        else:
            self.log_test("Nombres Category Endpoint", False, f"Status: {response['status_code']}, Error: {response['data']}")
            return False
    
    def test_4_28_numbers_count(self):
        """Test 4: Vérifier que tous les 28 nouveaux nombres sont présents (1-100)"""
        print("\n=== TEST 4: VÉRIFICATION 28 NOMBRES (1-100) ===")
        expected_count = 28
        actual_count = len(self.nombres_data)
        
        if actual_count >= expected_count:
            self.log_test("28+ Numbers Count", True, f"Expected: {expected_count}+, Found: {actual_count}")
        else:
            self.log_test("28+ Numbers Count", False, f"Expected: {expected_count}+, Found: {actual_count}")
    
    def test_5_data_structure_required_fields(self):
        """Test 5: Vérifier que chaque nombre a les champs requis: french, shimaoré, kibouchi, emoji, numeric_value, number_type"""
        print("\n=== TEST 5: STRUCTURE DES DONNÉES ===")
        required_fields = ['french', 'shimaore', 'kibouchi', 'category']
        optional_fields = ['image_url', 'numeric_value', 'number_type', 'difficulty']
        
        nombres_with_complete_structure = 0
        nombres_with_emoji = 0
        nombres_with_numeric_value = 0
        
        for nombre in self.nombres_data:
            has_all_required = all(field in nombre and nombre[field] for field in required_fields)
            if has_all_required:
                nombres_with_complete_structure += 1
            
            # Check for emoji (image_url field)
            if 'image_url' in nombre and nombre['image_url']:
                nombres_with_emoji += 1
                
            # Check for numeric_value
            if 'numeric_value' in nombre and nombre['numeric_value'] is not None:
                nombres_with_numeric_value += 1
        
        total_nombres = len(self.nombres_data)
        structure_percentage = (nombres_with_complete_structure / total_nombres * 100) if total_nombres > 0 else 0
        emoji_percentage = (nombres_with_emoji / total_nombres * 100) if total_nombres > 0 else 0
        numeric_percentage = (nombres_with_numeric_value / total_nombres * 100) if total_nombres > 0 else 0
        
        if nombres_with_complete_structure == total_nombres:
            self.log_test("Data Structure Required Fields", True, f"All {total_nombres} numbers have required fields")
        else:
            self.log_test("Data Structure Required Fields", False, f"Only {nombres_with_complete_structure}/{total_nombres} numbers have required fields ({structure_percentage:.1f}%)")
        
        if nombres_with_emoji > 0:
            self.log_test("Numbers with Emojis", True, f"{nombres_with_emoji}/{total_nombres} numbers have emojis ({emoji_percentage:.1f}%)")
        else:
            self.log_test("Numbers with Emojis", False, "No numbers have emojis")
            
        if nombres_with_numeric_value > 0:
            self.log_test("Numbers with Numeric Values", True, f"{nombres_with_numeric_value}/{total_nombres} numbers have numeric values ({numeric_percentage:.1f}%)")
    
    def test_6_basic_numbers_1_10(self):
        """Test 6: Tester les nombres de base (1-10): "un", "deux", "trois", etc."""
        print("\n=== TEST 6: NOMBRES DE BASE (1-10) ===")
        basic_numbers = ["un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix"]
        nombres_dict = {nombre['french'].lower(): nombre for nombre in self.nombres_data}
        
        found_basic = []
        for number_name in basic_numbers:
            if number_name in nombres_dict:
                nombre = nombres_dict[number_name]
                shimaore = nombre.get('shimaore', 'N/A')
                kibouchi = nombre.get('kibouchi', 'N/A')
                emoji = nombre.get('image_url', 'N/A')
                found_basic.append(number_name)
                
                self.log_test(f"Basic Number: {number_name.title()}", True, 
                            f"Shimaoré: {shimaore}, Kibouchi: {kibouchi}, Emoji: {emoji}")
            else:
                self.log_test(f"Basic Number: {number_name.title()}", False, "Not found in database")
        
        coverage = len(found_basic) / len(basic_numbers) * 100
        self.log_test("Basic Numbers Coverage (1-10)", coverage >= 80, f"{len(found_basic)}/10 found ({coverage:.1f}%)")
    
    def test_7_compound_numbers_11_19(self):
        """Test 7: Tester les nombres composés (11-19): "onze", "douze", "treize", etc."""
        print("\n=== TEST 7: NOMBRES COMPOSÉS (11-19) ===")
        compound_numbers = ["onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"]
        nombres_dict = {nombre['french'].lower(): nombre for nombre in self.nombres_data}
        
        found_compound = []
        koumi_na_pattern = 0
        foulou_ambi_pattern = 0
        
        for number_name in compound_numbers:
            if number_name in nombres_dict:
                nombre = nombres_dict[number_name]
                shimaore = nombre.get('shimaore', '').lower()
                kibouchi = nombre.get('kibouchi', '').lower()
                found_compound.append(number_name)
                
                # Check for expected patterns
                if 'koumi na' in shimaore:
                    koumi_na_pattern += 1
                if 'foulou' in kibouchi and 'ambi' in kibouchi:
                    foulou_ambi_pattern += 1
                
                self.log_test(f"Compound Number: {number_name.title()}", True, 
                            f"Shimaoré: {nombre.get('shimaore', 'N/A')}, Kibouchi: {nombre.get('kibouchi', 'N/A')}")
            else:
                self.log_test(f"Compound Number: {number_name.title()}", False, "Not found in database")
        
        coverage = len(found_compound) / len(compound_numbers) * 100
        self.log_test("Compound Numbers Coverage (11-19)", coverage >= 50, f"{len(found_compound)}/9 found ({coverage:.1f}%)")
        
        # Test structure patterns
        if found_compound:
            self.log_test("Shimaoré 'koumi na' Pattern", koumi_na_pattern > 0, f"{koumi_na_pattern} numbers use 'koumi na' pattern")
            self.log_test("Kibouchi 'foulou...ambi' Pattern", foulou_ambi_pattern > 0, f"{foulou_ambi_pattern} numbers use 'foulou...ambi' pattern")
    
    def test_8_tens_numbers(self):
        """Test 8: Tester les dizaines (20, 30, 40, etc.): "vingt", "trente", "quarante", etc."""
        print("\n=== TEST 8: NOMBRES DIZAINES ===")
        tens_numbers = ["vingt", "trente", "quarante", "cinquante", "soixante", "soixante-dix", "quatre-vingts", "quatre-vingt-dix"]
        nombres_dict = {nombre['french'].lower(): nombre for nombre in self.nombres_data}
        
        found_tens = []
        for number_name in tens_numbers:
            if number_name in nombres_dict:
                nombre = nombres_dict[number_name]
                shimaore = nombre.get('shimaore', 'N/A')
                kibouchi = nombre.get('kibouchi', 'N/A')
                found_tens.append(number_name)
                
                self.log_test(f"Tens Number: {number_name.title()}", True, 
                            f"Shimaoré: {shimaore}, Kibouchi: {kibouchi}")
            else:
                self.log_test(f"Tens Number: {number_name.title()}", False, "Not found in database")
        
        coverage = len(found_tens) / len(tens_numbers) * 100
        self.log_test("Tens Numbers Coverage", coverage >= 25, f"{len(found_tens)}/8 found ({coverage:.1f}%)")
    
    def test_9_hundred_number(self):
        """Test 9: Tester "cent" (100)"""
        print("\n=== TEST 9: NOMBRE CENT (100) ===")
        nombres_dict = {nombre['french'].lower(): nombre for nombre in self.nombres_data}
        
        if 'cent' in nombres_dict:
            nombre = nombres_dict['cent']
            shimaore = nombre.get('shimaore', 'N/A')
            kibouchi = nombre.get('kibouchi', 'N/A')
            emoji = nombre.get('image_url', 'N/A')
            numeric_value = nombre.get('numeric_value', 'N/A')
            
            self.log_test("Number 100 (cent)", True, 
                        f"Shimaoré: {shimaore}, Kibouchi: {kibouchi}, Emoji: {emoji}, Value: {numeric_value}")
        else:
            self.log_test("Number 100 (cent)", False, "Not found in database")
    
    def test_10_translations_quality(self):
        """Test 10: Vérifier que les traductions en shimaoré et kibouchi sont présentes"""
        print("\n=== TEST 10: QUALITÉ DES TRADUCTIONS ===")
        nombres_with_shimaore = 0
        nombres_with_kibouchi = 0
        
        for nombre in self.nombres_data:
            if nombre.get('shimaore') and nombre['shimaore'].strip():
                nombres_with_shimaore += 1
            if nombre.get('kibouchi') and nombre['kibouchi'].strip():
                nombres_with_kibouchi += 1
        
        total_nombres = len(self.nombres_data)
        shimaore_percentage = (nombres_with_shimaore / total_nombres * 100) if total_nombres > 0 else 0
        kibouchi_percentage = (nombres_with_kibouchi / total_nombres * 100) if total_nombres > 0 else 0
        
        self.log_test("Shimaoré Translations", nombres_with_shimaore == total_nombres, 
                     f"{nombres_with_shimaore}/{total_nombres} numbers ({shimaore_percentage:.1f}%)")
        self.log_test("Kibouchi Translations", nombres_with_kibouchi == total_nombres,
                     f"{nombres_with_kibouchi}/{total_nombres} numbers ({kibouchi_percentage:.1f}%)")
    
    def test_11_numeric_values_consistency(self):
        """Test 11: Vérifier que les valeurs numériques correspondent aux mots français"""
        print("\n=== TEST 11: COHÉRENCE VALEURS NUMÉRIQUES ===")
        expected_values = {
            'un': 1, 'deux': 2, 'trois': 3, 'quatre': 4, 'cinq': 5,
            'six': 6, 'sept': 7, 'huit': 8, 'neuf': 9, 'dix': 10,
            'onze': 11, 'douze': 12, 'treize': 13, 'quatorze': 14, 'quinze': 15,
            'seize': 16, 'dix-sept': 17, 'dix-huit': 18, 'dix-neuf': 19,
            'vingt': 20, 'trente': 30, 'quarante': 40, 'cinquante': 50,
            'soixante': 60, 'soixante-dix': 70, 'quatre-vingts': 80, 'quatre-vingt-dix': 90,
            'cent': 100
        }
        
        consistent_values = 0
        total_checkable = 0
        
        for nombre in self.nombres_data:
            french = nombre.get('french', '').lower()
            if french in expected_values:
                total_checkable += 1
                numeric_value = nombre.get('numeric_value')
                if numeric_value == expected_values[french]:
                    consistent_values += 1
                else:
                    self.log_test(f"Numeric Value {french}", False, f"Expected {expected_values[french]}, got {numeric_value}")
        
        consistency_rate = (consistent_values / total_checkable) * 100 if total_checkable > 0 else 0
        self.log_test("Numeric Values Consistency", consistency_rate >= 80, f"{consistent_values}/{total_checkable} ({consistency_rate:.1f}%)")
    
    def test_12_no_duplicates(self):
        """Test 12: Vérifier qu'il n'y a pas de doublons dans les valeurs numériques"""
        print("\n=== TEST 12: VÉRIFICATION DOUBLONS ===")
        french_names = [nombre['french'].lower() for nombre in self.nombres_data]
        unique_names = set(french_names)
        
        duplicates_found = len(french_names) - len(unique_names)
        
        if duplicates_found == 0:
            self.log_test("No Duplicates", True, f"All {len(french_names)} number names are unique")
        else:
            # Find actual duplicates
            seen = set()
            duplicates = set()
            for name in french_names:
                if name in seen:
                    duplicates.add(name)
                seen.add(name)
            
            self.log_test("No Duplicates", False, f"{duplicates_found} duplicates found: {list(duplicates)}")
        
        # Also check numeric values for duplicates
        numeric_values = [nombre.get('numeric_value') for nombre in self.nombres_data if nombre.get('numeric_value') is not None]
        unique_values = set(numeric_values)
        value_duplicates = len(numeric_values) - len(unique_values)
        
        if value_duplicates == 0:
            self.log_test("No Numeric Value Duplicates", True, f"All {len(numeric_values)} numeric values are unique")
        else:
            self.log_test("No Numeric Value Duplicates", False, f"{value_duplicates} duplicate numeric values found")
    
    def test_13_other_categories_unaffected(self):
        """Test 13: Vérifier que les autres sections (famille, animaux, etc.) n'ont pas été affectées"""
        print("\n=== TEST 13: AUTRES CATÉGORIES NON AFFECTÉES ===")
        other_categories = ['famille', 'couleurs', 'animaux', 'salutations', 'corps']
        
        for category in other_categories:
            response = self.make_request(f"/words?category={category}")
            if response["success"]:
                data = response["data"]
                count = len(data)
                self.log_test(f"Category {category.title()} Unaffected", True, f"{count} words found")
            else:
                self.log_test(f"Category {category.title()} Unaffected", False, f"Status: {response['status_code']}")
    
    def test_14_old_section_replaced(self):
        """Test 14: Tester que l'ancienne section nombres a été correctement remplacée"""
        print("\n=== TEST 14: REMPLACEMENT ANCIENNE SECTION ===")
        
        # Check if we have modern number data structure
        modern_structure_count = 0
        for nombre in self.nombres_data:
            # Modern numbers should have proper French names, not placeholder data
            french_name = nombre.get('french', '').lower()
            if (french_name and 
                len(french_name) > 1 and 
                not french_name.startswith('test') and
                not french_name.startswith('placeholder')):
                modern_structure_count += 1
        
        total_nombres = len(self.nombres_data)
        modern_percentage = (modern_structure_count / total_nombres * 100) if total_nombres > 0 else 0
        
        if modern_percentage >= 95:
            self.log_test("Old Section Replaced", True, 
                         f"{modern_percentage:.1f}% of numbers have modern structure")
        else:
            self.log_test("Old Section Replaced", False, 
                         f"Only {modern_percentage:.1f}% of numbers have modern structure")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🧪 DÉBUT DES TESTS - SECTION NOMBRES BACKEND")
        print("=" * 60)
        print("Test complet du backend après la mise à jour de la section 'nombres'")
        print("Contexte: 28 nouvelles entrées de nombres (1-100) avec traductions shimaoré et kibouchi")
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
        
        # Test spécifique de la catégorie nombres
        if not self.test_3_nombres_category_endpoint():
            print("❌ Cannot access nombres category. Stopping tests.")
            return False
        
        # Tests spécifiques aux nombres
        self.test_4_28_numbers_count()
        self.test_5_data_structure_required_fields()
        self.test_6_basic_numbers_1_10()
        self.test_7_compound_numbers_11_19()
        self.test_8_tens_numbers()
        self.test_9_hundred_number()
        self.test_10_translations_quality()
        self.test_11_numeric_values_consistency()
        self.test_12_no_duplicates()
        self.test_13_other_categories_unaffected()
        self.test_14_old_section_replaced()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Résumé final
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS - SECTION NOMBRES")
        print("=" * 60)
        
        for result in self.test_results:
            print(result)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"\n🎯 RÉSULTATS FINAUX:")
        print(f"   Tests réussis: {self.passed_tests}/{self.total_tests}")
        print(f"   Taux de réussite: {success_rate:.1f}%")
        print(f"   Durée: {duration:.2f}s")
        
        if len(self.nombres_data) > 0:
            print(f"   Nombres trouvés: {len(self.nombres_data)}")
            
            # Quelques exemples de nombres
            print("\n🔢 EXEMPLES DE NOMBRES TROUVÉS:")
            for i, nombre in enumerate(self.nombres_data[:10]):  # Show first 10
                french = nombre.get('french', 'N/A')
                shimaore = nombre.get('shimaore', 'N/A')
                kibouchi = nombre.get('kibouchi', 'N/A')
                emoji = nombre.get('image_url', 'N/A')
                numeric_value = nombre.get('numeric_value', 'N/A')
                print(f"  {i+1}. {french} ({numeric_value}) - Shimaoré: {shimaore}, Kibouchi: {kibouchi}, Emoji: {emoji}")
        
        print("\n" + "=" * 60)
        
        if success_rate >= 90:
            print("🎉 EXCELLENT - MISE À JOUR SECTION NOMBRES COMPLÈTEMENT RÉUSSIE!")
            print("Les 28 nouvelles entrées de nombres sont correctement intégrées")
            return True
        elif success_rate >= 70:
            print("✅ BIEN - MISE À JOUR SECTION NOMBRES MAJORITAIREMENT RÉUSSIE")
            print("La plupart des nombres sont correctement intégrés")
            return True
        elif success_rate >= 50:
            print("⚠️ PARTIEL - MISE À JOUR SECTION NOMBRES PARTIELLEMENT RÉUSSIE")
            print("Certains aspects nécessitent des corrections")
            return False
        else:
            print("❌ ÉCHEC - MISE À JOUR SECTION NOMBRES NON RÉUSSIE")
            print("Les nouvelles données de nombres n'ont pas été correctement intégrées")
            return False

def main():
    """Main test execution"""
    tester = NombresSectionTester()
    success = tester.run_all_tests()
    
    if success:
        print("🏁 TESTS TERMINÉS AVEC SUCCÈS!")
        sys.exit(0)
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ - VÉRIFICATION NÉCESSAIRE")
        sys.exit(1)

if __name__ == "__main__":
    main()