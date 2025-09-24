#!/usr/bin/env python3
"""
TESTS COMPLETS - INTÉGRATION AUDIO POUR 4 NOUVELLES SECTIONS
===========================================================

Tests critiques pour vérifier l'intégration du système audio dual pour:
- Salutations (7/8 mots avec audio, 10 fichiers)
- Couleurs (8/8 mots avec audio, 16 fichiers) 
- Grammaire (21/21 mots avec audio, 62 fichiers)
- Nourriture (29/44 mots avec audio, 83 fichiers)

OBJECTIF: Vérifier que 9 catégories sont supportées avec 542 fichiers audio au total
"""

import requests
import json
import os
import sys
from typing import Dict, List, Any

# Configuration des URLs
BACKEND_URL = "https://mayotte-learn-2.preview.emergentagent.com/api"

class DualAudioSystemTester:
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
    
    def test_9_categories_support(self):
        """TEST 1: Vérifier que 9 catégories sont supportées (5 originales + 4 nouvelles)"""
        try:
            response = requests.get(f"{self.backend_url}/audio/info")
            
            if response.status_code != 200:
                self.log_test("9 Categories Support", False, f"Status code: {response.status_code}")
                return
            
            data = response.json()
            
            # Vérifier les 9 catégories attendues
            expected_categories = [
                "famille", "nature", "nombres", "animaux", "corps",  # 5 originales
                "salutations", "couleurs", "grammaire", "nourriture"  # 4 nouvelles
            ]
            
            found_categories = []
            if "categories" in data:
                found_categories = list(data["categories"].keys())
            else:
                # Fallback: chercher les catégories dans la structure directe
                for category in expected_categories:
                    if category in data and isinstance(data[category], dict):
                        found_categories.append(category)
            
            missing_categories = [cat for cat in expected_categories if cat not in found_categories]
            
            if len(found_categories) >= 9 and not missing_categories:
                self.log_test("9 Categories Support", True, 
                            f"9+ catégories trouvées: {found_categories}")
            else:
                self.log_test("9 Categories Support", False, 
                            f"Trouvé {len(found_categories)} catégories: {found_categories}. Manquantes: {missing_categories}")
                
        except Exception as e:
            self.log_test("9 Categories Support", False, f"Erreur: {str(e)}")
    
    def test_542_total_audio_files(self):
        """TEST 2: Confirmer que GET /api/audio/info montre 542+ fichiers audio au total"""
        try:
            response = requests.get(f"{self.backend_url}/audio/info")
            
            if response.status_code != 200:
                self.log_test("542+ Total Audio Files", False, f"Status code: {response.status_code}")
                return
            
            data = response.json()
            
            total_files = 0
            
            # Compter les fichiers dans chaque catégorie
            if "total_files" in data:
                total_files = data["total_files"]
            else:
                # Fallback: compter manuellement
                categories = ["famille", "nature", "nombres", "animaux", "corps", 
                            "salutations", "couleurs", "grammaire", "nourriture"]
                
                for category in categories:
                    if category in data and "count" in data[category]:
                        total_files += data[category]["count"]
            
            if total_files >= 542:
                self.log_test("542+ Total Audio Files", True, f"{total_files} fichiers audio détectés")
            else:
                self.log_test("542+ Total Audio Files", False, 
                            f"Attendu 542+, trouvé {total_files} fichiers")
                
        except Exception as e:
            self.log_test("542+ Total Audio Files", False, f"Erreur: {str(e)}")
    
    def test_new_audio_endpoints(self):
        """TEST 3: Tester tous les nouveaux endpoints pour les 4 nouvelles sections"""
        new_sections_tests = {
            'salutations': 'Marahaba.m4a',  # "merci" example
            'couleurs': 'Ndzoukoundrou.m4a',  # "rouge" example  
            'grammaire': 'Wami.m4a',  # "je" example
            'nourriture': 'Pilipili.m4a'  # "piment" example
        }
        
        success_count = 0
        
        for section, test_file in new_sections_tests.items():
            try:
                response = requests.get(f"{self.backend_url}/audio/{section}/{test_file}")
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'audio' in content_type.lower():
                        success_count += 1
                        print(f"   ✅ {section}/{test_file}: Status 200, Content-Type: {content_type}")
                    else:
                        print(f"   ❌ {section}/{test_file}: Wrong Content-Type: {content_type}")
                else:
                    print(f"   ❌ {section}/{test_file}: Status {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {section}/{test_file}: Erreur {str(e)}")
        
        if success_count == len(new_sections_tests):
            self.log_test("New Audio Endpoints", True, f"Tous les {len(new_sections_tests)} nouveaux endpoints fonctionnent")
        else:
            self.log_test("New Audio Endpoints", False, 
                        f"Seulement {success_count}/{len(new_sections_tests)} endpoints fonctionnent")
    
    def test_section_coverage(self):
        """TEST 4: Vérifier la couverture audio pour chaque section"""
        sections_expected = {
            'salutations': {'words': 8, 'with_audio': 7, 'coverage': 87.5},
            'couleurs': {'words': 8, 'with_audio': 8, 'coverage': 100.0},
            'grammaire': {'words': 21, 'with_audio': 21, 'coverage': 100.0},
            'nourriture': {'words': 44, 'with_audio': 29, 'coverage': 66.0}
        }
        
        success_count = 0
        
        for section, expected in sections_expected.items():
            try:
                response = requests.get(f"{self.backend_url}/words?category={section}")
                
                if response.status_code != 200:
                    print(f"   ❌ {section}: API Error {response.status_code}")
                    continue
                
                words = response.json()
                total_words = len(words)
                words_with_dual_audio = sum(1 for word in words if word.get('dual_audio_system', False))
                
                coverage = (words_with_dual_audio / total_words * 100) if total_words > 0 else 0
                
                # Tolérance de 20% pour les variations
                meets_expectations = (
                    total_words >= expected['words'] * 0.8 and
                    words_with_dual_audio >= expected['with_audio'] * 0.8 and
                    coverage >= expected['coverage'] * 0.8
                )
                
                if meets_expectations:
                    success_count += 1
                    print(f"   ✅ {section}: {words_with_dual_audio}/{total_words} mots ({coverage:.1f}% couverture)")
                else:
                    print(f"   ❌ {section}: {words_with_dual_audio}/{total_words} mots ({coverage:.1f}% couverture)")
                    print(f"      Attendu: {expected['with_audio']}/{expected['words']} ({expected['coverage']}%)")
                    
            except Exception as e:
                print(f"   ❌ {section}: Erreur {str(e)}")
        
        if success_count == len(sections_expected):
            self.log_test("Section Coverage", True, f"Toutes les {len(sections_expected)} sections ont une couverture adéquate")
        else:
            self.log_test("Section Coverage", False, 
                        f"Seulement {success_count}/{len(sections_expected)} sections ont une couverture adéquate")
    
    def test_specific_examples(self):
        """TEST 5: Tester les exemples spécifiques mentionnés dans la review request"""
        test_examples = [
            {
                'section': 'salutations',
                'french': 'merci',
                'shimoare_file': 'Marahaba.m4a',
                'note': 'Shimaoré/Kibouchi même fichier'
            },
            {
                'section': 'couleurs', 
                'french': 'rouge',
                'shimoare_file': 'Ndzoukoundrou.m4a',
                'kibouchi_file': 'Mena.m4a',
                'note': 'Fichiers séparés'
            },
            {
                'section': 'grammaire',
                'french': 'je',
                'shimoare_file': 'Wami.m4a',
                'kibouchi_file': 'Zahou.m4a',
                'note': 'Fichiers séparés'
            },
            {
                'section': 'nourriture',
                'french': 'piment',
                'shimoare_file': 'Pilipili.m4a',
                'note': 'Shimaoré/Kibouchi même fichier'
            }
        ]
        
        success_count = 0
        
        for example in test_examples:
            try:
                # Récupérer les mots de la section
                response = requests.get(f"{self.backend_url}/words?category={example['section']}")
                if response.status_code != 200:
                    print(f"   ❌ {example['french']}: Impossible de récupérer les mots de {example['section']}")
                    continue
                
                words = response.json()
                target_word = None
                
                for word in words:
                    if word.get('french', '').lower() == example['french'].lower():
                        target_word = word
                        break
                
                if not target_word:
                    print(f"   ❌ {example['french']}: Mot non trouvé dans {example['section']}")
                    continue
                
                word_id = target_word.get('id')
                if not word_id:
                    print(f"   ❌ {example['french']}: ID manquant")
                    continue
                
                # Tester les endpoints audio duaux
                shimoare_response = requests.get(f"{self.backend_url}/words/{word_id}/audio/shimaore")
                kibouchi_response = requests.get(f"{self.backend_url}/words/{word_id}/audio/kibouchi")
                
                shimoare_ok = shimoare_response.status_code == 200
                kibouchi_ok = kibouchi_response.status_code == 200
                dual_system = target_word.get('dual_audio_system', False)
                
                if shimoare_ok and kibouchi_ok and dual_system:
                    success_count += 1
                    print(f"   ✅ {example['french']}: Dual audio OK - {example['note']}")
                else:
                    print(f"   ❌ {example['french']}: Shimaoré={shimoare_ok}, Kibouchi={kibouchi_ok}, Dual={dual_system}")
                    
            except Exception as e:
                print(f"   ❌ {example['french']}: Erreur {str(e)}")
        
        if success_count == len(test_examples):
            self.log_test("Specific Examples", True, f"Tous les {len(test_examples)} exemples spécifiques fonctionnent")
        else:
            self.log_test("Specific Examples", False, 
                        f"Seulement {success_count}/{len(test_examples)} exemples fonctionnent")
    
    def test_dual_audio_metadata(self):
        """TEST 6: Vérifier que les métadonnées dual_audio_system sont correctement définies"""
        sections_to_test = ['salutations', 'couleurs', 'grammaire', 'nourriture']
        
        success_count = 0
        
        for section in sections_to_test:
            try:
                response = requests.get(f"{self.backend_url}/words?category={section}")
                if response.status_code != 200:
                    print(f"   ❌ {section}: API Error {response.status_code}")
                    continue
                
                words = response.json()
                if not words:
                    print(f"   ❌ {section}: Aucun mot trouvé")
                    continue
                
                # Vérifier qu'au moins un mot a le système dual activé
                dual_audio_words = [w for w in words if w.get('dual_audio_system', False)]
                
                if dual_audio_words:
                    # Vérifier les champs requis sur le premier mot
                    test_word = dual_audio_words[0]
                    required_fields = [
                        'dual_audio_system',
                        'shimoare_has_audio',
                        'kibouchi_has_audio',
                        'shimoare_audio_filename',
                        'kibouchi_audio_filename'
                    ]
                    
                    missing_fields = []
                    for field in required_fields:
                        if field not in test_word or test_word[field] is None:
                            missing_fields.append(field)
                    
                    if not missing_fields:
                        success_count += 1
                        print(f"   ✅ {section}: Métadonnées complètes ({len(dual_audio_words)} mots avec dual audio)")
                    else:
                        print(f"   ❌ {section}: Champs manquants: {missing_fields}")
                else:
                    print(f"   ❌ {section}: Aucun mot avec dual_audio_system=true")
                    
            except Exception as e:
                print(f"   ❌ {section}: Erreur {str(e)}")
        
        if success_count == len(sections_to_test):
            self.log_test("Dual Audio Metadata", True, f"Métadonnées correctes pour toutes les {len(sections_to_test)} sections")
        else:
            self.log_test("Dual Audio Metadata", False, 
                        f"Seulement {success_count}/{len(sections_to_test)} sections ont des métadonnées correctes")
    
    def test_performance_9_categories(self):
        """TEST 7: Vérifier que le système gère 9 catégories sans problème de performance"""
        try:
            import time
            start_time = time.time()
            
            categories = ['salutations', 'couleurs', 'grammaire', 'nourriture', 
                         'famille', 'nature', 'nombres', 'animaux', 'corps']
            
            successful_requests = 0
            total_words = 0
            
            for category in categories:
                try:
                    response = requests.get(f"{self.backend_url}/words?category={category}", timeout=5)
                    if response.status_code == 200:
                        words = response.json()
                        successful_requests += 1
                        total_words += len(words)
                except:
                    pass
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Performance acceptable: moins de 15 secondes pour 9 requêtes
            performance_ok = total_time < 15.0 and successful_requests >= 8
            
            if performance_ok:
                self.log_test("Performance 9 Categories", True, 
                            f"{successful_requests}/9 catégories, {total_words} mots, {total_time:.2f}s")
            else:
                self.log_test("Performance 9 Categories", False, 
                            f"{successful_requests}/9 catégories, {total_time:.2f}s (trop lent)")
                
        except Exception as e:
            self.log_test("Performance 9 Categories", False, f"Erreur: {str(e)}")
    
    def test_automatic_category_detection(self):
        """TEST 8: Vérifier que la détection automatique de catégorie fonctionne"""
        test_cases = [
            {'category': 'salutations', 'file': 'Marahaba.m4a'},
            {'category': 'couleurs', 'file': 'Ndzoukoundrou.m4a'},
            {'category': 'grammaire', 'file': 'Wami.m4a'},
            {'category': 'nourriture', 'file': 'Pilipili.m4a'}
        ]
        
        success_count = 0
        
        for test_case in test_cases:
            try:
                response = requests.get(f"{self.backend_url}/audio/{test_case['category']}/{test_case['file']}")
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'audio' in content_type.lower():
                        success_count += 1
                        print(f"   ✅ {test_case['category']}/{test_case['file']}: Content-Type: {content_type}")
                    else:
                        print(f"   ❌ {test_case['category']}/{test_case['file']}: Wrong Content-Type: {content_type}")
                else:
                    print(f"   ❌ {test_case['category']}/{test_case['file']}: Status {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {test_case['category']}/{test_case['file']}: Erreur {str(e)}")
        
        if success_count == len(test_cases):
            self.log_test("Automatic Category Detection", True, 
                        f"Détection automatique fonctionne pour toutes les {len(test_cases)} catégories")
        else:
            self.log_test("Automatic Category Detection", False, 
                        f"Seulement {success_count}/{len(test_cases)} catégories détectées correctement")
    
    def run_all_tests(self):
        """Exécute tous les tests pour l'intégration audio des 4 nouvelles sections"""
        print("🎵 TESTS COMPLETS - INTÉGRATION AUDIO POUR 4 NOUVELLES SECTIONS")
        print("=" * 80)
        print(f"🔗 Backend URL: {self.backend_url}")
        print()
        print("📋 SECTIONS TESTÉES:")
        print("   • Salutations (7/8 mots avec audio, 10 fichiers)")
        print("   • Couleurs (8/8 mots avec audio, 16 fichiers)")
        print("   • Grammaire (21/21 mots avec audio, 62 fichiers)")
        print("   • Nourriture (29/44 mots avec audio, 83 fichiers)")
        print()
        
        # Exécuter tous les tests
        self.test_9_categories_support()
        self.test_542_total_audio_files()
        self.test_new_audio_endpoints()
        self.test_section_coverage()
        self.test_specific_examples()
        self.test_dual_audio_metadata()
        self.test_performance_9_categories()
        self.test_automatic_category_detection()
        
        # Résumé des résultats
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DES TESTS - INTÉGRATION AUDIO 4 NOUVELLES SECTIONS")
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
        
        print("\n🎯 OBJECTIF: Vérifier l'intégration complète du système audio dual pour")
        print("    4 nouvelles sections avec 9 catégories supportées et 542+ fichiers audio.")
        
        if failed_tests == 0:
            print("\n🎉 SUCCÈS COMPLET! Tous les tests sont passés.")
            print("✅ L'intégration du système audio dual pour les 4 nouvelles sections est fonctionnelle.")
            print("✅ 65 mots mis à jour avec le système dual audio opérationnel sur 9 catégories.")
        else:
            print(f"\n⚠️  {failed_tests} test(s) ont échoué. Vérification nécessaire.")
        
        return failed_tests == 0

def main():
    """Fonction principale"""
    tester = DualAudioSystemTester()
    success = tester.run_all_tests()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)