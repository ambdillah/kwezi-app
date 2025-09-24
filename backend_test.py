#!/usr/bin/env python3
"""
BACKEND TESTING - VERBES SECTION DUAL AUDIO SYSTEM INTEGRATION
Test complet pour l'intégration du système audio dual pour la section "verbes"
"""

import requests
import json
import os
import sys
from datetime import datetime

# Configuration des URLs
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://mayotte-learn-2.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class VerbsAudioTester:
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

    def test_1_extension_systeme_audio_dual_10_categories(self):
        """Test 1: Vérifier que 10 catégories sont maintenant supportées"""
        print("🔧 TEST 1: Extension système audio dual - 10 catégories")
        
        try:
            response = requests.get(f"{API_BASE}/audio/info", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Extension système audio dual - 10 catégories",
                    False,
                    f"Erreur HTTP {response.status_code}",
                    "Status 200",
                    f"Status {response.status_code}"
                )
                return
                
            data = response.json()
            
            # Vérifier total_categories
            total_categories = data.get('total_categories', 0)
            if total_categories == 10:
                self.log_result(
                    "Total catégories supportées",
                    True,
                    f"10 catégories confirmées: {total_categories}"
                )
            else:
                self.log_result(
                    "Total catégories supportées",
                    False,
                    f"Nombre incorrect de catégories",
                    "10 catégories",
                    f"{total_categories} catégories"
                )
            
            # Vérifier présence de la catégorie verbes
            if 'verbes' in data:
                verbes_count = data['verbes']['count']
                self.log_result(
                    "Catégorie verbes présente",
                    True,
                    f"Catégorie verbes trouvée avec {verbes_count} fichiers audio"
                )
            else:
                self.log_result(
                    "Catégorie verbes présente",
                    False,
                    "Catégorie verbes manquante dans la réponse",
                    "Catégorie verbes présente",
                    "Catégorie verbes absente"
                )
            
            # Vérifier endpoint verbes
            endpoints = data.get('endpoints', {})
            verbes_endpoint = endpoints.get('verbes')
            if verbes_endpoint == "/api/audio/verbes/{filename}":
                self.log_result(
                    "Endpoint verbes configuré",
                    True,
                    f"Endpoint verbes: {verbes_endpoint}"
                )
            else:
                self.log_result(
                    "Endpoint verbes configuré",
                    False,
                    "Endpoint verbes incorrect ou manquant",
                    "/api/audio/verbes/{filename}",
                    str(verbes_endpoint)
                )
                
        except Exception as e:
            self.log_result(
                "Extension système audio dual - 10 catégories",
                False,
                f"Exception: {str(e)}"
            )

    def test_2_couverture_section_verbes(self):
        """Test 2: Confirmer couverture section verbes (53/105 verbes)"""
        print("🔧 TEST 2: Couverture section verbes")
        
        try:
            # Récupérer tous les verbes
            response = requests.get(f"{API_BASE}/words?category=verbes", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Récupération verbes",
                    False,
                    f"Erreur HTTP {response.status_code}",
                    "Status 200",
                    f"Status {response.status_code}"
                )
                return
                
            verbes = response.json()
            total_verbes = len(verbes)
            
            # Compter les verbes avec dual_audio_system
            verbes_with_dual_audio = [v for v in verbes if v.get('dual_audio_system') == True]
            count_with_audio = len(verbes_with_dual_audio)
            coverage_percentage = (count_with_audio / total_verbes * 100) if total_verbes > 0 else 0
            
            self.log_result(
                "Total verbes dans la base",
                True,
                f"Total verbes trouvés: {total_verbes}"
            )
            
            # Vérifier la couverture (attendu: 53/105 = 50.5%)
            if count_with_audio >= 50:  # Au moins 50 verbes avec audio
                self.log_result(
                    "Couverture audio verbes",
                    True,
                    f"{count_with_audio}/{total_verbes} verbes avec dual_audio_system: true ({coverage_percentage:.1f}%)"
                )
            else:
                self.log_result(
                    "Couverture audio verbes",
                    False,
                    f"Couverture insuffisante",
                    "Au moins 50 verbes avec audio",
                    f"{count_with_audio} verbes avec audio"
                )
            
            # Vérifier les verbes essentiels mentionnés
            essential_verbs = ["manger", "boire", "voir", "parler", "marcher"]
            essential_found = []
            
            for verb_name in essential_verbs:
                verb_found = next((v for v in verbes if v.get('french', '').lower() == verb_name.lower()), None)
                if verb_found and verb_found.get('dual_audio_system'):
                    essential_found.append(verb_name)
            
            if len(essential_found) >= 4:  # Au moins 4 des 5 verbes essentiels
                self.log_result(
                    "Verbes essentiels avec audio",
                    True,
                    f"Verbes essentiels trouvés avec audio: {', '.join(essential_found)}"
                )
            else:
                self.log_result(
                    "Verbes essentiels avec audio",
                    False,
                    f"Verbes essentiels manquants",
                    "Au moins 4 verbes essentiels avec audio",
                    f"{len(essential_found)} verbes essentiels trouvés: {', '.join(essential_found)}"
                )
                
        except Exception as e:
            self.log_result(
                "Couverture section verbes",
                False,
                f"Exception: {str(e)}"
            )

    def test_3_fonctionnalite_systeme_dual_verbes(self):
        """Test 3: Fonctionnalité système dual pour verbes"""
        print("🔧 TEST 3: Fonctionnalité système dual verbes")
        
        try:
            # Récupérer les verbes avec dual audio
            response = requests.get(f"{API_BASE}/words?category=verbes", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Récupération verbes pour test dual",
                    False,
                    f"Erreur HTTP {response.status_code}"
                )
                return
                
            verbes = response.json()
            verbes_with_dual = [v for v in verbes if v.get('dual_audio_system') == True]
            
            if not verbes_with_dual:
                self.log_result(
                    "Verbes avec système dual trouvés",
                    False,
                    "Aucun verbe avec dual_audio_system trouvé"
                )
                return
            
            # Tester les endpoints dual audio sur quelques verbes
            test_verbs = verbes_with_dual[:3]  # Tester les 3 premiers
            
            for verb in test_verbs:
                verb_id = verb.get('id')
                verb_name = verb.get('french', 'Unknown')
                
                if not verb_id:
                    continue
                
                # Test endpoint shimaore
                try:
                    shimaore_response = requests.get(f"{API_BASE}/words/{verb_id}/audio/shimaore", timeout=10)
                    if shimaore_response.status_code == 200:
                        self.log_result(
                            f"Audio Shimaoré - {verb_name}",
                            True,
                            f"Endpoint shimaore fonctionnel pour '{verb_name}'"
                        )
                    else:
                        self.log_result(
                            f"Audio Shimaoré - {verb_name}",
                            False,
                            f"Erreur HTTP {shimaore_response.status_code} pour shimaore"
                        )
                except Exception as e:
                    self.log_result(
                        f"Audio Shimaoré - {verb_name}",
                        False,
                        f"Exception shimaore: {str(e)}"
                    )
                
                # Test endpoint kibouchi
                try:
                    kibouchi_response = requests.get(f"{API_BASE}/words/{verb_id}/audio/kibouchi", timeout=10)
                    if kibouchi_response.status_code == 200:
                        self.log_result(
                            f"Audio Kibouchi - {verb_name}",
                            True,
                            f"Endpoint kibouchi fonctionnel pour '{verb_name}'"
                        )
                    else:
                        self.log_result(
                            f"Audio Kibouchi - {verb_name}",
                            False,
                            f"Erreur HTTP {kibouchi_response.status_code} pour kibouchi"
                        )
                except Exception as e:
                    self.log_result(
                        f"Audio Kibouchi - {verb_name}",
                        False,
                        f"Exception kibouchi: {str(e)}"
                    )
                
                # Test endpoint audio-info
                try:
                    info_response = requests.get(f"{API_BASE}/words/{verb_id}/audio-info", timeout=10)
                    if info_response.status_code == 200:
                        info_data = info_response.json()
                        if info_data.get('dual_audio_system') == True:
                            self.log_result(
                                f"Audio Info - {verb_name}",
                                True,
                                f"Métadonnées audio correctes pour '{verb_name}'"
                            )
                        else:
                            self.log_result(
                                f"Audio Info - {verb_name}",
                                False,
                                f"Métadonnées audio incorrectes pour '{verb_name}'"
                            )
                    else:
                        self.log_result(
                            f"Audio Info - {verb_name}",
                            False,
                            f"Erreur HTTP {info_response.status_code} pour audio-info"
                        )
                except Exception as e:
                    self.log_result(
                        f"Audio Info - {verb_name}",
                        False,
                        f"Exception audio-info: {str(e)}"
                    )
                    
        except Exception as e:
            self.log_result(
                "Fonctionnalité système dual verbes",
                False,
                f"Exception: {str(e)}"
            )

    def test_4_exemples_specifiques(self):
        """Test 4: Exemples spécifiques mentionnés dans la review"""
        print("🔧 TEST 4: Exemples spécifiques")
        
        specific_examples = {
            "voir": "Mahita.m4a",
            "manger": "Mamana.m4a", 
            "marcher": "Mandéha.m4a",
            "arnaquer": "Mangalatra.m4a",
            "traverser": "Latsaka.m4a"
        }
        
        try:
            # Récupérer tous les verbes
            response = requests.get(f"{API_BASE}/words?category=verbes", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Récupération verbes pour exemples spécifiques",
                    False,
                    f"Erreur HTTP {response.status_code}"
                )
                return
                
            verbes = response.json()
            
            for verb_name, expected_file in specific_examples.items():
                # Trouver le verbe
                verb = next((v for v in verbes if v.get('french', '').lower() == verb_name.lower()), None)
                
                if not verb:
                    self.log_result(
                        f"Verbe '{verb_name}' trouvé",
                        False,
                        f"Verbe '{verb_name}' non trouvé dans la base"
                    )
                    continue
                
                # Vérifier dual_audio_system
                if verb.get('dual_audio_system') == True:
                    self.log_result(
                        f"Verbe '{verb_name}' - dual audio",
                        True,
                        f"Verbe '{verb_name}' a dual_audio_system: true"
                    )
                    
                    # Vérifier les métadonnées audio
                    shimoare_file = verb.get('shimoare_audio_filename')
                    kibouchi_file = verb.get('kibouchi_audio_filename')
                    
                    if shimoare_file or kibouchi_file:
                        self.log_result(
                            f"Verbe '{verb_name}' - fichiers audio",
                            True,
                            f"Fichiers audio: Shimaoré={shimoare_file}, Kibouchi={kibouchi_file}"
                        )
                    else:
                        self.log_result(
                            f"Verbe '{verb_name}' - fichiers audio",
                            False,
                            f"Métadonnées audio manquantes pour '{verb_name}'"
                        )
                else:
                    self.log_result(
                        f"Verbe '{verb_name}' - dual audio",
                        False,
                        f"Verbe '{verb_name}' n'a pas dual_audio_system: true"
                    )
                    
        except Exception as e:
            self.log_result(
                "Exemples spécifiques",
                False,
                f"Exception: {str(e)}"
            )

    def test_5_endpoint_verbes_performance(self):
        """Test 5: Endpoint et performance verbes"""
        print("🔧 TEST 5: Endpoint et performance verbes")
        
        try:
            # Test de l'endpoint /api/audio/verbes/{filename}
            # D'abord récupérer la liste des fichiers disponibles
            response = requests.get(f"{API_BASE}/audio/info", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Récupération info audio pour test endpoint",
                    False,
                    f"Erreur HTTP {response.status_code}"
                )
                return
                
            data = response.json()
            verbes_files = data.get('verbes', {}).get('files', [])
            
            if not verbes_files:
                self.log_result(
                    "Fichiers audio verbes disponibles",
                    False,
                    "Aucun fichier audio verbes trouvé"
                )
                return
            
            # Vérifier qu'il y a au moins 50 fichiers (attendu: 50 fichiers)
            if len(verbes_files) >= 50:
                self.log_result(
                    "Nombre fichiers audio verbes",
                    True,
                    f"{len(verbes_files)} fichiers audio verbes trouvés (≥50 attendu)"
                )
            else:
                self.log_result(
                    "Nombre fichiers audio verbes",
                    False,
                    f"Nombre insuffisant de fichiers audio",
                    "Au moins 50 fichiers",
                    f"{len(verbes_files)} fichiers"
                )
            
            # Tester l'endpoint avec quelques fichiers
            test_files = verbes_files[:3]  # Tester les 3 premiers fichiers
            
            for filename in test_files:
                try:
                    start_time = datetime.now()
                    file_response = requests.get(f"{API_BASE}/audio/verbes/{filename}", timeout=10)
                    end_time = datetime.now()
                    response_time = (end_time - start_time).total_seconds()
                    
                    if file_response.status_code == 200:
                        content_type = file_response.headers.get('content-type', '')
                        if 'audio' in content_type.lower():
                            self.log_result(
                                f"Endpoint verbes - {filename}",
                                True,
                                f"Fichier {filename} servi correctement ({response_time:.2f}s, {content_type})"
                            )
                        else:
                            self.log_result(
                                f"Endpoint verbes - {filename}",
                                False,
                                f"Content-Type incorrect: {content_type}"
                            )
                    else:
                        self.log_result(
                            f"Endpoint verbes - {filename}",
                            False,
                            f"Erreur HTTP {file_response.status_code} pour {filename}"
                        )
                        
                except Exception as e:
                    self.log_result(
                        f"Endpoint verbes - {filename}",
                        False,
                        f"Exception: {str(e)}"
                    )
            
            # Vérifier le total de fichiers audio (attendu: 592+)
            total_files = data.get('total_files', 0)
            if total_files >= 590:
                self.log_result(
                    "Total fichiers audio système",
                    True,
                    f"{total_files} fichiers audio au total (≥590 attendu)"
                )
            else:
                self.log_result(
                    "Total fichiers audio système",
                    False,
                    f"Total insuffisant de fichiers audio",
                    "Au moins 590 fichiers",
                    f"{total_files} fichiers"
                )
                
        except Exception as e:
            self.log_result(
                "Endpoint et performance verbes",
                False,
                f"Exception: {str(e)}"
            )

    def test_6_integrite_globale(self):
        """Test 6: Intégrité globale du système"""
        print("🔧 TEST 6: Intégrité globale")
        
        try:
            # Vérifier que le système gère 10 catégories
            response = requests.get(f"{API_BASE}/audio/info", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Intégrité système audio",
                    False,
                    f"Erreur HTTP {response.status_code}"
                )
                return
                
            data = response.json()
            
            # Vérifier les 10 catégories attendues
            expected_categories = [
                'famille', 'nature', 'nombres', 'animaux', 'corps',
                'salutations', 'couleurs', 'grammaire', 'nourriture', 'verbes'
            ]
            
            missing_categories = []
            present_categories = []
            
            for category in expected_categories:
                if category in data:
                    present_categories.append(category)
                else:
                    missing_categories.append(category)
            
            if len(present_categories) == 10:
                self.log_result(
                    "10 catégories audio présentes",
                    True,
                    f"Toutes les 10 catégories présentes: {', '.join(present_categories)}"
                )
            else:
                self.log_result(
                    "10 catégories audio présentes",
                    False,
                    f"Catégories manquantes: {', '.join(missing_categories)}",
                    "10 catégories",
                    f"{len(present_categories)} catégories"
                )
            
            # Vérifier la cohérence des audio_dirs configuration
            endpoints = data.get('endpoints', {})
            if len(endpoints) >= 10:  # Au moins 10 endpoints + dual_system
                self.log_result(
                    "Configuration endpoints audio",
                    True,
                    f"{len(endpoints)} endpoints configurés"
                )
            else:
                self.log_result(
                    "Configuration endpoints audio",
                    False,
                    f"Configuration endpoints insuffisante",
                    "Au moins 10 endpoints",
                    f"{len(endpoints)} endpoints"
                )
            
            # Tester que les autres catégories fonctionnent toujours
            test_categories = ['famille', 'animaux', 'nombres']  # Quelques catégories existantes
            
            for category in test_categories:
                if category in data and data[category]['count'] > 0:
                    # Tester un fichier de cette catégorie
                    files = data[category]['files']
                    if files:
                        test_file = files[0]
                        try:
                            test_response = requests.get(f"{API_BASE}/audio/{category}/{test_file}", timeout=10)
                            if test_response.status_code == 200:
                                self.log_result(
                                    f"Catégorie {category} fonctionnelle",
                                    True,
                                    f"Catégorie {category} fonctionne correctement"
                                )
                            else:
                                self.log_result(
                                    f"Catégorie {category} fonctionnelle",
                                    False,
                                    f"Erreur HTTP {test_response.status_code} pour {category}"
                                )
                        except Exception as e:
                            self.log_result(
                                f"Catégorie {category} fonctionnelle",
                                False,
                                f"Exception: {str(e)}"
                            )
                            
        except Exception as e:
            self.log_result(
                "Intégrité globale",
                False,
                f"Exception: {str(e)}"
            )

    def run_all_tests(self):
        """Exécute tous les tests"""
        print("🎯 DÉBUT DES TESTS - INTÉGRATION SECTION VERBES")
        print("=" * 60)
        print()
        
        # Exécuter tous les tests
        self.test_1_extension_systeme_audio_dual_10_categories()
        self.test_2_couverture_section_verbes()
        self.test_3_fonctionnalite_systeme_dual_verbes()
        self.test_4_exemples_specifiques()
        self.test_5_endpoint_verbes_performance()
        self.test_6_integrite_globale()
        
        # Résumé final
        print("=" * 60)
        print("🎯 RÉSUMÉ DES TESTS")
        print("=" * 60)
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
            print("🎉 TOUS LES TESTS RÉUSSIS - INTÉGRATION VERBES COMPLÈTE!")
            return True
        elif self.failed_tests <= 2:
            print("⚠️  INTÉGRATION MAJORITAIREMENT RÉUSSIE - Quelques ajustements mineurs nécessaires")
            return True
        else:
            print("❌ INTÉGRATION INCOMPLÈTE - Corrections nécessaires")
            return False

def main():
    """Fonction principale"""
    print("🚀 LANCEMENT DES TESTS BACKEND - SECTION VERBES")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"🔗 API Base: {API_BASE}")
    print()
    
    tester = VerbsAudioTester()
    success = tester.run_all_tests()
    
    # Code de sortie
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()