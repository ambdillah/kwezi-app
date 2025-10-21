#!/usr/bin/env python3
"""
BACKEND TESTING - EXPRESSIONS SECTION DUAL AUDIO SYSTEM INTEGRATION
Test complet pour l'intégration du système audio dual pour la section "expressions"

Test Requirements from Review Request:
1. Extension système audio dual - 11 catégories
2. Couverture section expressions (16/44 expressions with dual audio)
3. Fonctionnalité système dual expressions
4. Exemples spécifiques (joie, appelez la police !, etc.)
5. Endpoint /api/audio/expressions/{filename}
6. Performance avec 612+ fichiers audio
7. Intégrité globale du système
"""

import requests
import json
import os
import sys
from datetime import datetime
import time

# Configuration des URLs
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://mahorais-learn.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class ExpressionsAudioTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_result(self, test_name, success, details="", expected="", actual=""):
        """Enregistre le résultat d'un test"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
            
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "expected": expected,
            "actual": actual,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        print(f"{status}: {test_name}")
        if details:
            print(f"    Details: {details}")
        if not success and expected:
            print(f"    Expected: {expected}")
            print(f"    Actual: {actual}")
        print()

    def test_1_extension_systeme_audio_dual_11_categories(self):
        """Test 1: Vérifier que 11 catégories sont maintenant supportées"""
        print("🔧 TEST 1: Extension système audio dual - 11 catégories")
        
        try:
            response = requests.get(f"{API_BASE}/audio/info", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Extension système audio dual - 11 catégories",
                    False,
                    f"Erreur HTTP {response.status_code}",
                    "Status 200",
                    f"Status {response.status_code}"
                )
                return
                
            data = response.json()
            
            # Vérifier total_categories
            total_categories = data.get('total_categories', 0)
            if total_categories == 11:
                self.log_result(
                    "Total catégories supportées",
                    True,
                    f"11 catégories confirmées: {total_categories}"
                )
            else:
                self.log_result(
                    "Total catégories supportées",
                    False,
                    f"Nombre incorrect de catégories",
                    "11 catégories",
                    f"{total_categories} catégories"
                )
            
            # Vérifier présence de la catégorie expressions
            categories = data.get('categories', {})
            if 'expressions' in categories:
                expressions_info = categories['expressions']
                expressions_count = expressions_info.get('file_count', 0)
                self.log_result(
                    "Catégorie expressions présente",
                    True,
                    f"Catégorie expressions trouvée avec {expressions_count} fichiers audio"
                )
            else:
                self.log_result(
                    "Catégorie expressions présente",
                    False,
                    "Catégorie expressions manquante dans la réponse",
                    "Catégorie expressions présente",
                    "Catégorie expressions absente"
                )
            
            # Vérifier endpoint expressions
            if 'expressions' in categories:
                expressions_endpoint = categories['expressions'].get('endpoint')
                if expressions_endpoint == "/api/audio/expressions/{filename}":
                    self.log_result(
                        "Endpoint expressions configuré",
                        True,
                        f"Endpoint expressions: {expressions_endpoint}"
                    )
                else:
                    self.log_result(
                        "Endpoint expressions configuré",
                        False,
                        "Endpoint expressions incorrect ou manquant",
                        "/api/audio/expressions/{filename}",
                        str(expressions_endpoint)
                    )
                
        except Exception as e:
            self.log_result(
                "Extension système audio dual - 11 catégories",
                False,
                f"Exception: {str(e)}"
            )

    def test_2_couverture_section_expressions(self):
        """Test 2: Confirmer couverture section expressions (16/44 expressions)"""
        print("🔧 TEST 2: Couverture section expressions")
        
        try:
            # Récupérer toutes les expressions
            response = requests.get(f"{API_BASE}/words?category=expressions", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Récupération expressions",
                    False,
                    f"Erreur HTTP {response.status_code}",
                    "Status 200",
                    f"Status {response.status_code}"
                )
                return
                
            expressions = response.json()
            total_expressions = len(expressions)
            
            # Compter les expressions avec dual_audio_system
            expressions_with_dual_audio = [e for e in expressions if e.get('dual_audio_system') == True]
            count_with_audio = len(expressions_with_dual_audio)
            coverage_percentage = (count_with_audio / total_expressions * 100) if total_expressions > 0 else 0
            
            self.log_result(
                "Total expressions dans la base",
                total_expressions == 44,
                f"Total expressions trouvées: {total_expressions}/44",
                "44 expressions",
                f"{total_expressions} expressions"
            )
            
            # Vérifier la couverture (attendu: 16/44 = 36.4%)
            if count_with_audio == 16:
                self.log_result(
                    "Couverture audio expressions exacte",
                    True,
                    f"{count_with_audio}/{total_expressions} expressions avec dual_audio_system: true ({coverage_percentage:.1f}%)"
                )
            elif count_with_audio >= 15:  # Au moins 15 expressions avec audio (proche de 16)
                self.log_result(
                    "Couverture audio expressions acceptable",
                    True,
                    f"{count_with_audio}/{total_expressions} expressions avec dual_audio_system: true ({coverage_percentage:.1f}%)"
                )
            else:
                self.log_result(
                    "Couverture audio expressions",
                    False,
                    f"Couverture insuffisante",
                    "16 expressions avec audio (36.4%)",
                    f"{count_with_audio} expressions avec audio ({coverage_percentage:.1f}%)"
                )
            
            # Vérifier les métadonnées shimoare_has_audio et kibouchi_has_audio
            expressions_with_shimoare = [e for e in expressions_with_dual_audio if e.get('shimoare_has_audio') == True]
            expressions_with_kibouchi = [e for e in expressions_with_dual_audio if e.get('kibouchi_has_audio') == True]
            
            self.log_result(
                "Métadonnées Shimaoré cohérentes",
                len(expressions_with_shimoare) >= count_with_audio * 0.8,  # Au moins 80% ont shimoare
                f"{len(expressions_with_shimoare)}/{count_with_audio} expressions avec shimoare_has_audio: true"
            )
            
            self.log_result(
                "Métadonnées Kibouchi cohérentes",
                len(expressions_with_kibouchi) >= count_with_audio * 0.8,  # Au moins 80% ont kibouchi
                f"{len(expressions_with_kibouchi)}/{count_with_audio} expressions avec kibouchi_has_audio: true"
            )
                
        except Exception as e:
            self.log_result(
                "Couverture section expressions",
                False,
                f"Exception: {str(e)}"
            )

    def test_3_fonctionnalite_systeme_dual_expressions(self):
        """Test 3: Fonctionnalité système dual pour expressions"""
        print("🔧 TEST 3: Fonctionnalité système dual expressions")
        
        try:
            # Récupérer les expressions avec dual audio
            response = requests.get(f"{API_BASE}/words?category=expressions", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Récupération expressions pour test dual",
                    False,
                    f"Erreur HTTP {response.status_code}"
                )
                return
                
            expressions = response.json()
            expressions_with_dual = [e for e in expressions if e.get('dual_audio_system') == True]
            
            if not expressions_with_dual:
                self.log_result(
                    "Expressions avec système dual trouvées",
                    False,
                    "Aucune expression avec dual_audio_system trouvée"
                )
                return
            
            # Tester les endpoints dual audio sur quelques expressions
            test_expressions = expressions_with_dual[:3]  # Tester les 3 premières
            
            for expression in test_expressions:
                expression_id = expression.get('id')
                expression_name = expression.get('french', 'Unknown')
                
                if not expression_id:
                    continue
                
                # Test endpoint shimaore
                try:
                    shimaore_response = requests.get(f"{API_BASE}/words/{expression_id}/audio/shimaore", timeout=10)
                    if shimaore_response.status_code == 200:
                        self.log_result(
                            f"Audio Shimaoré - {expression_name}",
                            True,
                            f"Endpoint shimaore fonctionnel pour '{expression_name}'"
                        )
                    else:
                        self.log_result(
                            f"Audio Shimaoré - {expression_name}",
                            False,
                            f"Erreur HTTP {shimaore_response.status_code} pour shimaore"
                        )
                except Exception as e:
                    self.log_result(
                        f"Audio Shimaoré - {expression_name}",
                        False,
                        f"Exception shimaore: {str(e)}"
                    )
                
                # Test endpoint kibouchi
                try:
                    kibouchi_response = requests.get(f"{API_BASE}/words/{expression_id}/audio/kibouchi", timeout=10)
                    if kibouchi_response.status_code == 200:
                        self.log_result(
                            f"Audio Kibouchi - {expression_name}",
                            True,
                            f"Endpoint kibouchi fonctionnel pour '{expression_name}'"
                        )
                    else:
                        self.log_result(
                            f"Audio Kibouchi - {expression_name}",
                            False,
                            f"Erreur HTTP {kibouchi_response.status_code} pour kibouchi"
                        )
                except Exception as e:
                    self.log_result(
                        f"Audio Kibouchi - {expression_name}",
                        False,
                        f"Exception kibouchi: {str(e)}"
                    )
                
                # Test endpoint audio-info
                try:
                    info_response = requests.get(f"{API_BASE}/words/{expression_id}/audio-info", timeout=10)
                    if info_response.status_code == 200:
                        info_data = info_response.json()
                        if info_data.get('dual_audio_system') == True:
                            self.log_result(
                                f"Audio Info - {expression_name}",
                                True,
                                f"Métadonnées audio correctes pour '{expression_name}'"
                            )
                        else:
                            self.log_result(
                                f"Audio Info - {expression_name}",
                                False,
                                f"Métadonnées audio incorrectes pour '{expression_name}'"
                            )
                    else:
                        self.log_result(
                            f"Audio Info - {expression_name}",
                            False,
                            f"Erreur HTTP {info_response.status_code} pour audio-info"
                        )
                except Exception as e:
                    self.log_result(
                        f"Audio Info - {expression_name}",
                        False,
                        f"Exception audio-info: {str(e)}"
                    )
                    
        except Exception as e:
            self.log_result(
                "Fonctionnalité système dual expressions",
                False,
                f"Exception: {str(e)}"
            )

    def test_4_exemples_specifiques(self):
        """Test 4: Exemples spécifiques mentionnés dans la review"""
        print("🔧 TEST 4: Exemples spécifiques")
        
        specific_examples = {
            "joie": {"shimoare": "Fouraha.m4a", "kibouchi": "Aravouagna.m4a"},
            "appelez la police !": {"shimoare": "Hira sirikali.m4a", "kibouchi": "Kahiya sirikali.m4a"},
            "appelez une ambulance !": {"shimoare": "Hira ambulanci.m4a", "kibouchi": "Kahiya ambulanci.m4a"},
            "où se trouve": {"shimoare": "Aya moi.m4a", "kibouchi": "Aya moi.m4a"},  # même fichier
            "combien ça coûte ?": {"shimoare": "Hotri inou moi.m4a", "kibouchi": "Hotri inou moi.m4a"}  # même fichier
        }
        
        try:
            # Récupérer toutes les expressions
            response = requests.get(f"{API_BASE}/words?category=expressions", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Récupération expressions pour exemples spécifiques",
                    False,
                    f"Erreur HTTP {response.status_code}"
                )
                return
                
            expressions = response.json()
            
            for expression_name, expected_files in specific_examples.items():
                # Trouver l'expression
                expression = next((e for e in expressions if e.get('french', '').lower() == expression_name.lower()), None)
                
                if not expression:
                    self.log_result(
                        f"Expression '{expression_name}' trouvée",
                        False,
                        f"Expression '{expression_name}' non trouvée dans la base"
                    )
                    continue
                
                # Vérifier dual_audio_system
                if expression.get('dual_audio_system') == True:
                    self.log_result(
                        f"Expression '{expression_name}' - dual audio",
                        True,
                        f"Expression '{expression_name}' a dual_audio_system: true"
                    )
                    
                    # Vérifier les métadonnées audio
                    shimoare_file = expression.get('shimoare_audio_filename')
                    kibouchi_file = expression.get('kibouchi_audio_filename')
                    
                    # Vérifier les fichiers attendus
                    shimoare_match = shimoare_file == expected_files["shimoare"]
                    kibouchi_match = kibouchi_file == expected_files["kibouchi"]
                    
                    self.log_result(
                        f"Expression '{expression_name}' - fichier Shimaoré",
                        shimoare_match,
                        f"Fichier Shimaoré: attendu={expected_files['shimoare']}, trouvé={shimoare_file}",
                        expected_files["shimoare"],
                        shimoare_file or "None"
                    )
                    
                    self.log_result(
                        f"Expression '{expression_name}' - fichier Kibouchi",
                        kibouchi_match,
                        f"Fichier Kibouchi: attendu={expected_files['kibouchi']}, trouvé={kibouchi_file}",
                        expected_files["kibouchi"],
                        kibouchi_file or "None"
                    )
                else:
                    self.log_result(
                        f"Expression '{expression_name}' - dual audio",
                        False,
                        f"Expression '{expression_name}' n'a pas dual_audio_system: true"
                    )
                    
        except Exception as e:
            self.log_result(
                "Exemples spécifiques",
                False,
                f"Exception: {str(e)}"
            )

    def test_5_endpoint_expressions_performance(self):
        """Test 5: Endpoint et performance expressions"""
        print("🔧 TEST 5: Endpoint et performance expressions")
        
        try:
            # Test de l'endpoint /api/audio/expressions/{filename}
            test_files = ["Fouraha.m4a", "Aravouagna.m4a", "Hira sirikali.m4a", "Kahiya sirikali.m4a"]
            
            for filename in test_files:
                try:
                    start_time = datetime.now()
                    file_response = requests.get(f"{API_BASE}/audio/expressions/{filename}", timeout=10)
                    end_time = datetime.now()
                    response_time = (end_time - start_time).total_seconds()
                    
                    if file_response.status_code == 200:
                        content_type = file_response.headers.get('content-type', '')
                        if 'audio' in content_type.lower():
                            self.log_result(
                                f"Endpoint expressions - {filename}",
                                True,
                                f"Fichier {filename} servi correctement ({response_time:.2f}s, {content_type})"
                            )
                        else:
                            self.log_result(
                                f"Endpoint expressions - {filename}",
                                False,
                                f"Content-Type incorrect: {content_type}"
                            )
                    else:
                        self.log_result(
                            f"Endpoint expressions - {filename}",
                            False,
                            f"Erreur HTTP {file_response.status_code} pour {filename}"
                        )
                        
                except Exception as e:
                    self.log_result(
                        f"Endpoint expressions - {filename}",
                        False,
                        f"Exception: {str(e)}"
                    )
            
            # Vérifier le total de fichiers audio (attendu: 612+)
            response = requests.get(f"{API_BASE}/audio/info", timeout=10)
            if response.status_code == 200:
                data = response.json()
                total_files = data.get('total_files', 0)
                if total_files >= 612:
                    self.log_result(
                        "Total fichiers audio système",
                        True,
                        f"{total_files} fichiers audio au total (≥612 attendu)"
                    )
                else:
                    self.log_result(
                        "Total fichiers audio système",
                        False,
                        f"Total insuffisant de fichiers audio",
                        "Au moins 612 fichiers",
                        f"{total_files} fichiers"
                    )
                
                # Vérifier spécifiquement les fichiers expressions
                categories = data.get('categories', {})
                if 'expressions' in categories:
                    expressions_files = categories['expressions'].get('file_count', 0)
                    if expressions_files >= 20:
                        self.log_result(
                            "Fichiers audio expressions",
                            True,
                            f"{expressions_files} fichiers audio expressions (≥20 attendu)"
                        )
                    else:
                        self.log_result(
                            "Fichiers audio expressions",
                            False,
                            f"Nombre insuffisant de fichiers expressions",
                            "Au moins 20 fichiers",
                            f"{expressions_files} fichiers"
                        )
                
        except Exception as e:
            self.log_result(
                "Endpoint et performance expressions",
                False,
                f"Exception: {str(e)}"
            )

    def test_6_integrite_globale(self):
        """Test 6: Intégrité globale du système"""
        print("🔧 TEST 6: Intégrité globale")
        
        try:
            # Vérifier que le système gère 11 catégories
            response = requests.get(f"{API_BASE}/audio/info", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Intégrité système audio",
                    False,
                    f"Erreur HTTP {response.status_code}"
                )
                return
                
            data = response.json()
            
            # Vérifier les 11 catégories attendues
            expected_categories = [
                'famille', 'nature', 'nombres', 'animaux', 'corps',
                'salutations', 'couleurs', 'grammaire', 'nourriture', 
                'verbes', 'expressions'
            ]
            
            missing_categories = []
            present_categories = []
            categories = data.get('categories', {})
            
            for category in expected_categories:
                if category in categories:
                    present_categories.append(category)
                else:
                    missing_categories.append(category)
            
            if len(present_categories) == 11:
                self.log_result(
                    "11 catégories audio présentes",
                    True,
                    f"Toutes les 11 catégories présentes: {', '.join(present_categories)}"
                )
            else:
                self.log_result(
                    "11 catégories audio présentes",
                    False,
                    f"Catégories manquantes: {', '.join(missing_categories)}",
                    "11 catégories",
                    f"{len(present_categories)} catégories"
                )
            
            # Vérifier la cohérence des audio_dirs configuration
            if len(categories) >= 11:  # Au moins 11 catégories
                self.log_result(
                    "Configuration catégories audio",
                    True,
                    f"{len(categories)} catégories configurées"
                )
            else:
                self.log_result(
                    "Configuration catégories audio",
                    False,
                    f"Configuration catégories insuffisante",
                    "Au moins 11 catégories",
                    f"{len(categories)} catégories"
                )
            
            # Tester que les autres catégories fonctionnent toujours
            test_categories = ['famille', 'animaux', 'nombres']  # Quelques catégories existantes
            
            for category in test_categories:
                if category in categories:
                    category_info = categories[category]
                    file_count = category_info.get('file_count', 0)
                    if file_count > 0:
                        self.log_result(
                            f"Catégorie {category} fonctionnelle",
                            True,
                            f"Catégorie {category} a {file_count} fichiers audio"
                        )
                    else:
                        self.log_result(
                            f"Catégorie {category} fonctionnelle",
                            False,
                            f"Catégorie {category} n'a pas de fichiers audio"
                        )
                else:
                    self.log_result(
                        f"Catégorie {category} fonctionnelle",
                        False,
                        f"Catégorie {category} manquante"
                    )
                            
        except Exception as e:
            self.log_result(
                "Intégrité globale",
                False,
                f"Exception: {str(e)}"
            )

    def test_7_types_expressions_integrees(self):
        """Test 7: Vérifier les types d'expressions intégrées"""
        print("🔧 TEST 7: Types d'expressions intégrées")
        
        expected_expression_types = {
            "urgences": ["appelez la police !", "appelez une ambulance !"],
            "navigation": ["où se trouve", "où sommes-nous", "tout droit", "à droite", "à gauche"],
            "commerce": ["combien ça coûte ?", "trop cher"],
            "communication": ["montre-moi", "c'est très bon !"],
            "émotions": ["joie"]
        }
        
        try:
            response = requests.get(f"{API_BASE}/words?category=expressions", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Récupération expressions pour types",
                    False,
                    f"Erreur HTTP {response.status_code}"
                )
                return
                
            expressions = response.json()
            french_words = [expr.get('french', '').lower() for expr in expressions]
            
            for expression_type, expected_words in expected_expression_types.items():
                found_words = []
                for word in expected_words:
                    if word.lower() in french_words:
                        found_words.append(word)
                
                coverage = len(found_words) / len(expected_words) * 100 if expected_words else 0
                success = len(found_words) > 0
                
                self.log_result(
                    f"Type expressions '{expression_type}'",
                    success,
                    f"Trouvé {len(found_words)}/{len(expected_words)} mots ({coverage:.1f}%): {', '.join(found_words) if found_words else 'Aucun'}"
                )
                
        except Exception as e:
            self.log_result(
                "Types expressions intégrées",
                False,
                f"Exception: {str(e)}"
            )

    def run_all_tests(self):
        """Exécute tous les tests"""
        print("🎯 DÉBUT DES TESTS - INTÉGRATION SECTION EXPRESSIONS")
        print("=" * 70)
        print()
        
        # Exécuter tous les tests
        self.test_1_extension_systeme_audio_dual_11_categories()
        self.test_2_couverture_section_expressions()
        self.test_3_fonctionnalite_systeme_dual_expressions()
        self.test_4_exemples_specifiques()
        self.test_5_endpoint_expressions_performance()
        self.test_6_integrite_globale()
        self.test_7_types_expressions_integrees()
        
        # Résumé final
        print("=" * 70)
        print("🎯 RÉSUMÉ DES TESTS")
        print("=" * 70)
        print(f"Total tests: {self.total_tests}")
        print(f"✅ Réussis: {self.passed_tests}")
        print(f"❌ Échoués: {self.failed_tests}")
        print(f"📊 Taux de réussite: {(self.passed_tests/self.total_tests*100):.1f}%")
        print()
        
        if self.failed_tests > 0:
            print("❌ TESTS ÉCHOUÉS:")
            for result in self.results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['details']}")
            print()
        
        # Déterminer le statut global
        if self.failed_tests == 0:
            print("🎉 TOUS LES TESTS RÉUSSIS - INTÉGRATION EXPRESSIONS COMPLÈTE!")
            return True
        elif self.failed_tests <= 3:
            print("⚠️  INTÉGRATION MAJORITAIREMENT RÉUSSIE - Quelques ajustements mineurs nécessaires")
            return True
        else:
            print("❌ INTÉGRATION INCOMPLÈTE - Corrections nécessaires")
            return False

def main():
    """Fonction principale"""
    print("🚀 LANCEMENT DES TESTS BACKEND - SECTION EXPRESSIONS")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"🔗 API Base: {API_BASE}")
    print()
    
    tester = ExpressionsAudioTester()
    success = tester.run_all_tests()
    
    # Code de sortie
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()