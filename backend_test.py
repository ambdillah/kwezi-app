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

class AudioPronunciationTester:
    def __init__(self):
        self.api_url = API_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.section_data = {}
        
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
    
    def test_2_sections_completes(self):
        """Test 2: Vérification des sections complètes (4 sections attendues)"""
        print("\n=== TEST 2: VÉRIFICATION DES SECTIONS COMPLÈTES ===")
        
        expected_sections = ["animaux", "nombres", "corps", "salutations"]
        
        try:
            # Test global words endpoint
            response = self.make_request("/words")
            if not response["success"]:
                self.log_test("Global words endpoint", False, f"Status: {response['status_code']}")
                return False
            
            words = response["data"]
            self.log_test("Global words endpoint", True, f"Total words: {len(words)}")
            
            # Count words by category and test each section
            for section in expected_sections:
                section_response = self.make_request(f"/words?category={section}")
                if section_response["success"]:
                    section_words = section_response["data"]
                    self.section_data[section] = section_words
                    count = len(section_words)
                    self.log_test(f"Section {section} accessible", True, f"{count} mots trouvés")
                else:
                    self.log_test(f"Section {section} accessible", False, f"Status: {section_response['status_code']}")
                    self.section_data[section] = []
            
            return True
            
        except Exception as e:
            self.log_test("Sections complètes test", False, f"Error: {str(e)}")
            return False
    
    def test_3_audio_authentiques(self):
        """Test 3: Test des références audio authentiques"""
        print("\n=== TEST 3: TEST DES RÉFÉRENCES AUDIO AUTHENTIQUES ===")
        
        try:
            total_words_with_audio = 0
            total_words = 0
            
            for section, words in self.section_data.items():
                words_with_audio = 0
                for word in words:
                    total_words += 1
                    # Check for various audio fields
                    has_audio = (
                        word.get('has_authentic_audio') or
                        word.get('audio_filename') or
                        word.get('shimoare_has_audio') or
                        word.get('kibouchi_has_audio') or
                        word.get('dual_audio_system')
                    )
                    if has_audio:
                        words_with_audio += 1
                        total_words_with_audio += 1
                
                if len(words) > 0:
                    audio_percentage = (words_with_audio / len(words)) * 100
                    self.log_test(f"Section {section} - références audio", words_with_audio > 0, 
                                f"{words_with_audio}/{len(words)} mots avec audio ({audio_percentage:.1f}%)")
                else:
                    self.log_test(f"Section {section} - références audio", False, "Aucun mot dans la section")
            
            # Global audio coverage
            if total_words > 0:
                global_audio_percentage = (total_words_with_audio / total_words) * 100
                self.log_test("Couverture audio globale", total_words_with_audio > 0, 
                            f"{total_words_with_audio}/{total_words} mots avec audio ({global_audio_percentage:.1f}%)")
            
            return True
            
        except Exception as e:
            self.log_test("Audio authentiques test", False, f"Error: {str(e)}")
            return False
    
    def test_4_section_nombres(self):
        """Test 4: Test spécifique section nombres (28 mots attendus)"""
        print("\n=== TEST 4: TEST SPÉCIFIQUE SECTION NOMBRES ===")
        
        expected_count = 28
        expected_audio_files = ["Moja.m4a", "Mbili.m4a"]
        
        nombres = self.section_data.get("nombres", [])
        actual_count = len(nombres)
        
        # Test word count
        if actual_count >= expected_count:
            self.log_test("Nombres - nombre de mots", True, f"{actual_count}/{expected_count}+ mots")
        else:
            self.log_test("Nombres - nombre de mots", False, f"{actual_count}/{expected_count}+ mots (insuffisant)")
        
        # Test data structure
        complete_structure = 0
        with_audio = 0
        with_translations = 0
        
        for nombre in nombres:
            # Check required fields
            if all(field in nombre and nombre[field] for field in ['french', 'shimaore', 'kibouchi', 'category']):
                complete_structure += 1
            
            # Check audio
            if (nombre.get('has_authentic_audio') or nombre.get('audio_filename') or 
                nombre.get('shimoare_has_audio') or nombre.get('kibouchi_has_audio')):
                with_audio += 1
            
            # Check translations
            if nombre.get('shimaore') and nombre.get('kibouchi'):
                with_translations += 1
        
        if actual_count > 0:
            structure_rate = (complete_structure / actual_count) * 100
            audio_rate = (with_audio / actual_count) * 100
            translation_rate = (with_translations / actual_count) * 100
            
            self.log_test("Nombres - structure complète", structure_rate >= 90, 
                        f"{complete_structure}/{actual_count} ({structure_rate:.1f}%)")
            self.log_test("Nombres - avec audio", audio_rate > 0, 
                        f"{with_audio}/{actual_count} ({audio_rate:.1f}%)")
            self.log_test("Nombres - traductions complètes", translation_rate >= 90, 
                        f"{with_translations}/{actual_count} ({translation_rate:.1f}%)")
        
        # Test specific examples
        nombres_dict = {n.get('french', '').lower(): n for n in nombres}
        basic_numbers = ["un", "deux", "trois", "quatre", "cinq"]
        found_basic = sum(1 for num in basic_numbers if num in nombres_dict)
        
        self.log_test("Nombres - exemples de base (1-5)", found_basic >= 3, 
                    f"{found_basic}/5 nombres de base trouvés")
        
        return True
    
    def test_5_section_animaux(self):
        """Test 5: Test spécifique section animaux (66+ mots attendus)"""
        print("\n=== TEST 5: TEST SPÉCIFIQUE SECTION ANIMAUX ===")
        
        expected_count = 66
        expected_examples = ["pouroukou", "kasangwe", "chat", "chien"]
        
        animaux = self.section_data.get("animaux", [])
        actual_count = len(animaux)
        
        # Test word count
        if actual_count >= expected_count:
            self.log_test("Animaux - nombre de mots", True, f"{actual_count}/{expected_count}+ mots")
        else:
            self.log_test("Animaux - nombre de mots", False, f"{actual_count}/{expected_count}+ mots (insuffisant)")
        
        # Test data quality
        with_emojis = sum(1 for animal in animaux if animal.get('image_url'))
        with_audio = sum(1 for animal in animaux if (
            animal.get('has_authentic_audio') or animal.get('audio_filename') or
            animal.get('shimoare_has_audio') or animal.get('kibouchi_has_audio')
        ))
        
        if actual_count > 0:
            emoji_rate = (with_emojis / actual_count) * 100
            audio_rate = (with_audio / actual_count) * 100
            
            self.log_test("Animaux - avec emojis", emoji_rate >= 50, 
                        f"{with_emojis}/{actual_count} ({emoji_rate:.1f}%)")
            self.log_test("Animaux - avec audio", audio_rate > 0, 
                        f"{with_audio}/{actual_count} ({audio_rate:.1f}%)")
        
        # Test specific examples
        animaux_dict = {a.get('french', '').lower(): a for a in animaux}
        found_examples = sum(1 for example in expected_examples if example in animaux_dict)
        
        self.log_test("Animaux - exemples spécifiques", found_examples >= 2, 
                    f"{found_examples}/4 exemples trouvés")
        
        return True
    
    def test_6_section_corps(self):
        """Test 6: Test spécifique section corps (20 mots attendus)"""
        print("\n=== TEST 6: TEST SPÉCIFIQUE SECTION CORPS ===")
        
        expected_count = 20
        expected_examples = ["matso", "cha", "tête", "main"]
        
        corps = self.section_data.get("corps", [])
        actual_count = len(corps)
        
        # Test word count
        if actual_count >= expected_count:
            self.log_test("Corps - nombre de mots", True, f"{actual_count}/{expected_count}+ mots")
        else:
            self.log_test("Corps - nombre de mots", False, f"{actual_count}/{expected_count}+ mots (insuffisant)")
        
        # Test audio coverage
        with_audio = sum(1 for mot in corps if (
            mot.get('has_authentic_audio') or mot.get('audio_filename') or
            mot.get('shimoare_has_audio') or mot.get('kibouchi_has_audio')
        ))
        
        if actual_count > 0:
            audio_rate = (with_audio / actual_count) * 100
            self.log_test("Corps - avec audio", audio_rate > 0, 
                        f"{with_audio}/{actual_count} ({audio_rate:.1f}%)")
        
        # Test specific examples
        corps_dict = {c.get('french', '').lower(): c for c in corps}
        found_examples = sum(1 for example in expected_examples if example in corps_dict)
        
        self.log_test("Corps - exemples spécifiques", found_examples >= 2, 
                    f"{found_examples}/4 exemples trouvés")
        
        return True
    
    def test_7_section_salutations(self):
        """Test 7: Test spécifique section salutations (9 mots attendus)"""
        print("\n=== TEST 7: TEST SPÉCIFIQUE SECTION SALUTATIONS ===")
        
        expected_count = 9
        expected_examples = ["marahaba", "kwaheri", "bonjour", "merci"]
        
        salutations = self.section_data.get("salutations", [])
        actual_count = len(salutations)
        
        # Test word count
        if actual_count >= expected_count:
            self.log_test("Salutations - nombre de mots", True, f"{actual_count}/{expected_count}+ mots")
        else:
            self.log_test("Salutations - nombre de mots", False, f"{actual_count}/{expected_count}+ mots (insuffisant)")
        
        # Test audio coverage
        with_audio = sum(1 for salut in salutations if (
            salut.get('has_authentic_audio') or salut.get('audio_filename') or
            salut.get('shimoare_has_audio') or salut.get('kibouchi_has_audio')
        ))
        
        if actual_count > 0:
            audio_rate = (with_audio / actual_count) * 100
            self.log_test("Salutations - avec audio", audio_rate > 0, 
                        f"{with_audio}/{actual_count} ({audio_rate:.1f}%)")
        
        # Test specific examples
        salutations_dict = {s.get('french', '').lower(): s for s in salutations}
        found_examples = sum(1 for example in expected_examples if example in salutations_dict)
        
        self.log_test("Salutations - exemples spécifiques", found_examples >= 2, 
                    f"{found_examples}/4 exemples trouvés")
        
        return True
    
    def test_8_integrite_donnees(self):
        """Test 8: Test de l'intégrité des données"""
        print("\n=== TEST 8: TEST DE L'INTÉGRITÉ DES DONNÉES ===")
        
        try:
            total_words = 0
            complete_translations = 0
            with_emojis = 0
            duplicates_found = 0
            french_words = set()
            
            for section, words in self.section_data.items():
                for word in words:
                    total_words += 1
                    
                    # Check translations
                    if word.get('shimaore') and word.get('kibouchi'):
                        complete_translations += 1
                    
                    # Check emojis
                    if word.get('image_url'):
                        with_emojis += 1
                    
                    # Check duplicates
                    french = word.get('french', '').lower()
                    if french in french_words:
                        duplicates_found += 1
                    else:
                        french_words.add(french)
            
            if total_words > 0:
                translation_rate = (complete_translations / total_words) * 100
                emoji_rate = (with_emojis / total_words) * 100
                
                self.log_test("Intégrité - traductions complètes", translation_rate >= 80, 
                            f"{complete_translations}/{total_words} ({translation_rate:.1f}%)")
                self.log_test("Intégrité - emojis appropriés", emoji_rate >= 30, 
                            f"{with_emojis}/{total_words} ({emoji_rate:.1f}%)")
                self.log_test("Intégrité - absence de doublons", duplicates_found == 0, 
                            f"{duplicates_found} doublons trouvés")
            
            return True
            
        except Exception as e:
            self.log_test("Intégrité données test", False, f"Error: {str(e)}")
            return False
    
    def test_9_performance(self):
        """Test 9: Test de performance"""
        print("\n=== TEST 9: TEST DE PERFORMANCE ===")
        
        endpoints_to_test = [
            "/words",
            "/words?category=animaux",
            "/words?category=nombres", 
            "/words?category=corps",
            "/words?category=salutations"
        ]
        
        try:
            for endpoint in endpoints_to_test:
                start_time = time.time()
                response = self.make_request(endpoint)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                if response["success"]:
                    data = response["data"]
                    data_size = len(data) if isinstance(data, list) else 1
                    
                    # Consider response time acceptable if under 3 seconds
                    if response_time < 3.0:
                        self.log_test(f"Performance {endpoint}", True, 
                                    f"{response_time:.2f}s pour {data_size} éléments")
                    else:
                        self.log_test(f"Performance {endpoint}", False, 
                                    f"{response_time:.2f}s (trop lent)")
                else:
                    self.log_test(f"Performance {endpoint}", False, 
                                f"Status: {response['status_code']}")
            
            return True
            
        except Exception as e:
            self.log_test("Performance test", False, f"Error: {str(e)}")
            return False
    
    def test_10_audio_endpoints(self):
        """Test 10: Test des endpoints audio spécifiques"""
        print("\n=== TEST 10: TEST DES ENDPOINTS AUDIO ===")
        
        # Test audio info endpoint
        try:
            response = self.make_request("/audio/info")
            if response["success"]:
                audio_info = response["data"]
                self.log_test("Endpoint audio/info", True, "Informations audio disponibles")
                
                # Check if expected categories are present
                if isinstance(audio_info, dict):
                    categories_found = 0
                    expected_categories = ['animaux', 'nombres', 'corps', 'salutations']
                    
                    for category in expected_categories:
                        # Check various possible structures
                        if (category in str(audio_info).lower() or 
                            (isinstance(audio_info, dict) and 'categories' in audio_info and 
                             category in audio_info.get('categories', {}))):
                            categories_found += 1
                            self.log_test(f"Catégorie audio {category}", True, "Disponible")
                        else:
                            self.log_test(f"Catégorie audio {category}", False, "Non trouvée")
                    
                    self.log_test("Couverture catégories audio", categories_found >= 2, 
                                f"{categories_found}/4 catégories trouvées")
            else:
                self.log_test("Endpoint audio/info", False, f"Status: {response['status_code']}")
        
        except Exception as e:
            self.log_test("Audio endpoints test", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Execute all tests"""
        print("🎯 DÉBUT DES TESTS BACKEND - MISE À JOUR AUDIO PRONONCIATIONS")
        print("=" * 70)
        print("Test complet du backend après la mise à jour des prononciations audio")
        print("Contexte: 4 sections (animaux, nombres, corps, salutations) avec audio authentique")
        print("=" * 70)
        
        start_time = time.time()
        
        # Test connectivity first
        if not self.test_1_api_connectivity():
            print("❌ ÉCHEC: Impossible de se connecter à l'API. Arrêt des tests.")
            return False
        
        # Run all test suites
        self.test_2_sections_completes()
        self.test_3_audio_authentiques()
        self.test_4_section_nombres()
        self.test_5_section_animaux()
        self.test_6_section_corps()
        self.test_7_section_salutations()
        self.test_8_integrite_donnees()
        self.test_9_performance()
        self.test_10_audio_endpoints()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 70)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Tests réussis: {self.passed_tests}/{self.total_tests} ({success_rate:.1f}%)")
        print(f"Durée: {duration:.2f}s")
        
        # Show section statistics
        print(f"\n📈 STATISTIQUES PAR SECTION:")
        for section, words in self.section_data.items():
            count = len(words)
            with_audio = sum(1 for w in words if (
                w.get('has_authentic_audio') or w.get('audio_filename') or
                w.get('shimoare_has_audio') or w.get('kibouchi_has_audio')
            ))
            audio_rate = (with_audio / count * 100) if count > 0 else 0
            print(f"  {section.title()}: {count} mots, {with_audio} avec audio ({audio_rate:.1f}%)")
        
        if success_rate >= 80:
            print("\n🎉 RÉSULTAT: SUCCÈS - La mise à jour audio est fonctionnelle!")
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
    tester = AudioPronunciationTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🏁 TESTS TERMINÉS AVEC SUCCÈS!")
        sys.exit(0)
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ - VÉRIFICATION NÉCESSAIRE")
        sys.exit(1)

if __name__ == "__main__":
    main()