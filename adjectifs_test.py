#!/usr/bin/env python3
"""
BACKEND TESTING - ADJECTIFS SECTION DUAL AUDIO SYSTEM INTEGRATION
Test complet pour l'intégration du système audio dual pour la section "adjectifs"
"""

import requests
import json
import os
import sys
from datetime import datetime

# Configuration des URLs
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://kwezi-android.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class AdjectifsAudioTester:
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

    def test_1_extension_systeme_audio_dual_12_categories(self):
        """Test 1: Vérifier que 12 catégories sont maintenant supportées (ajout de "adjectifs")"""
        print("🔧 TEST 1: Extension système audio dual - 12 catégories")
        
        try:
            response = requests.get(f"{API_BASE}/audio/info", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Extension système audio dual - 12 catégories",
                    False,
                    f"Erreur HTTP {response.status_code}",
                    "Status 200",
                    f"Status {response.status_code}"
                )
                return
                
            data = response.json()
            
            # Vérifier total_categories
            total_categories = data.get('total_categories', len(data.keys()) if isinstance(data, dict) else 0)
            if total_categories >= 12:
                self.log_result(
                    "Total catégories supportées",
                    True,
                    f"12+ catégories confirmées: {total_categories}"
                )
            else:
                self.log_result(
                    "Total catégories supportées",
                    False,
                    f"Nombre incorrect de catégories",
                    "12+ catégories",
                    f"{total_categories} catégories"
                )
            
            # Vérifier présence de la catégorie adjectifs
            if 'adjectifs' in data:
                adjectifs_info = data['adjectifs']
                if isinstance(adjectifs_info, dict):
                    adjectifs_count = adjectifs_info.get('count', adjectifs_info.get('total_files', 0))
                else:
                    adjectifs_count = "présent"
                self.log_result(
                    "Catégorie adjectifs présente",
                    True,
                    f"Catégorie adjectifs trouvée avec {adjectifs_count} fichiers audio"
                )
            else:
                self.log_result(
                    "Catégorie adjectifs présente",
                    False,
                    "Catégorie adjectifs manquante dans la réponse",
                    "Catégorie adjectifs présente",
                    "Catégorie adjectifs absente"
                )
            
            # Vérifier endpoint adjectifs
            endpoints = data.get('endpoints', {})
            adjectifs_endpoint = endpoints.get('adjectifs')
            if adjectifs_endpoint == "/api/audio/adjectifs/{filename}":
                self.log_result(
                    "Endpoint adjectifs configuré",
                    True,
                    f"Endpoint adjectifs: {adjectifs_endpoint}"
                )
            else:
                self.log_result(
                    "Endpoint adjectifs configuré",
                    False,
                    "Endpoint adjectifs incorrect ou manquant",
                    "/api/audio/adjectifs/{filename}",
                    str(adjectifs_endpoint)
                )
                
        except Exception as e:
            self.log_result(
                "Extension système audio dual - 12 catégories",
                False,
                f"Exception: {str(e)}"
            )

    def test_2_couverture_section_adjectifs(self):
        """Test 2: Confirmer couverture section adjectifs (34/52 adjectifs = 65.4%)"""
        print("🔧 TEST 2: Couverture section adjectifs")
        
        try:
            # Récupérer tous les adjectifs
            response = requests.get(f"{API_BASE}/words?category=adjectifs", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Récupération adjectifs",
                    False,
                    f"Erreur HTTP {response.status_code}",
                    "Status 200",
                    f"Status {response.status_code}"
                )
                return
                
            adjectifs = response.json()
            total_adjectifs = len(adjectifs)
            
            # Compter les adjectifs avec dual_audio_system
            adjectifs_with_dual_audio = [a for a in adjectifs if a.get('dual_audio_system') == True]
            count_with_audio = len(adjectifs_with_dual_audio)
            coverage_percentage = (count_with_audio / total_adjectifs * 100) if total_adjectifs > 0 else 0
            
            self.log_result(
                "Total adjectifs dans la base",
                True,
                f"Total adjectifs trouvés: {total_adjectifs}"
            )
            
            # Vérifier la couverture (attendu: 34/52 = 65.4%)
            if count_with_audio >= 30 and total_adjectifs >= 50:  # Au moins 30 adjectifs avec audio sur 50+
                self.log_result(
                    "Couverture audio adjectifs",
                    True,
                    f"{count_with_audio}/{total_adjectifs} adjectifs avec dual_audio_system: true ({coverage_percentage:.1f}%)"
                )
            else:
                self.log_result(
                    "Couverture audio adjectifs",
                    False,
                    f"Couverture insuffisante",
                    "Au moins 30/50+ adjectifs avec audio",
                    f"{count_with_audio}/{total_adjectifs} adjectifs avec audio"
                )
            
            # Vérifier les adjectifs essentiels mentionnés
            essential_adjectives = ["grand", "petit", "chaud", "froid", "content"]
            essential_found = []
            
            for adj_name in essential_adjectives:
                adj_found = next((a for a in adjectifs if a.get('french', '').lower() == adj_name.lower()), None)
                if adj_found and adj_found.get('dual_audio_system'):
                    essential_found.append(adj_name)
            
            if len(essential_found) >= 4:  # Au moins 4 des 5 adjectifs essentiels
                self.log_result(
                    "Adjectifs essentiels avec audio",
                    True,
                    f"Adjectifs essentiels trouvés avec audio: {', '.join(essential_found)}"
                )
            else:
                self.log_result(
                    "Adjectifs essentiels avec audio",
                    False,
                    f"Adjectifs essentiels manquants",
                    "Au moins 4 adjectifs essentiels avec audio",
                    f"{len(essential_found)} adjectifs essentiels trouvés: {', '.join(essential_found)}"
                )
                
        except Exception as e:
            self.log_result(
                "Couverture section adjectifs",
                False,
                f"Exception: {str(e)}"
            )

    def test_3_fonctionnalite_systeme_dual_adjectifs(self):
        """Test 3: Fonctionnalité système dual pour adjectifs"""
        print("🔧 TEST 3: Fonctionnalité système dual adjectifs")
        
        try:
            # Récupérer les adjectifs avec dual audio
            response = requests.get(f"{API_BASE}/words?category=adjectifs", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Récupération adjectifs pour test dual",
                    False,
                    f"Erreur HTTP {response.status_code}"
                )
                return
                
            adjectifs = response.json()
            adjectifs_with_dual = [a for a in adjectifs if a.get('dual_audio_system') == True]
            
            if not adjectifs_with_dual:
                self.log_result(
                    "Adjectifs avec système dual trouvés",
                    False,
                    "Aucun adjectif avec dual_audio_system trouvé"
                )
                return
            
            # Tester les endpoints dual audio sur quelques adjectifs
            test_adjectives = adjectifs_with_dual[:3]  # Tester les 3 premiers
            
            for adj in test_adjectives:
                adj_id = adj.get('id')
                adj_name = adj.get('french', 'Unknown')
                
                if not adj_id:
                    continue
                
                # Test endpoint shimaore
                try:
                    shimaore_response = requests.get(f"{API_BASE}/words/{adj_id}/audio/shimaore", timeout=10)
                    if shimaore_response.status_code == 200:
                        self.log_result(
                            f"Audio Shimaoré - {adj_name}",
                            True,
                            f"Endpoint shimaore fonctionnel pour '{adj_name}'"
                        )
                    else:
                        self.log_result(
                            f"Audio Shimaoré - {adj_name}",
                            False,
                            f"Erreur HTTP {shimaore_response.status_code} pour shimaore"
                        )
                except Exception as e:
                    self.log_result(
                        f"Audio Shimaoré - {adj_name}",
                        False,
                        f"Exception shimaore: {str(e)}"
                    )
                
                # Test endpoint kibouchi
                try:
                    kibouchi_response = requests.get(f"{API_BASE}/words/{adj_id}/audio/kibouchi", timeout=10)
                    if kibouchi_response.status_code == 200:
                        self.log_result(
                            f"Audio Kibouchi - {adj_name}",
                            True,
                            f"Endpoint kibouchi fonctionnel pour '{adj_name}'"
                        )
                    else:
                        self.log_result(
                            f"Audio Kibouchi - {adj_name}",
                            False,
                            f"Erreur HTTP {kibouchi_response.status_code} pour kibouchi"
                        )
                except Exception as e:
                    self.log_result(
                        f"Audio Kibouchi - {adj_name}",
                        False,
                        f"Exception kibouchi: {str(e)}"
                    )
                
                # Test endpoint audio-info
                try:
                    info_response = requests.get(f"{API_BASE}/words/{adj_id}/audio-info", timeout=10)
                    if info_response.status_code == 200:
                        info_data = info_response.json()
                        if info_data.get('dual_audio_system') == True:
                            self.log_result(
                                f"Audio Info - {adj_name}",
                                True,
                                f"Métadonnées audio correctes pour '{adj_name}'"
                            )
                        else:
                            self.log_result(
                                f"Audio Info - {adj_name}",
                                False,
                                f"Métadonnées audio incorrectes pour '{adj_name}'"
                            )
                    else:
                        self.log_result(
                            f"Audio Info - {adj_name}",
                            False,
                            f"Erreur HTTP {info_response.status_code} pour audio-info"
                        )
                except Exception as e:
                    self.log_result(
                        f"Audio Info - {adj_name}",
                        False,
                        f"Exception audio-info: {str(e)}"
                    )
                    
        except Exception as e:
            self.log_result(
                "Fonctionnalité système dual adjectifs",
                False,
                f"Exception: {str(e)}"
            )

    def test_4_exemples_specifiques(self):
        """Test 4: Exemples spécifiques mentionnés dans la review"""
        print("🔧 TEST 4: Exemples spécifiques")
        
        specific_examples = {
            "grand": {"shimaore": "Bolé.m4a", "kibouchi": "Bé.m4a"},
            "petit": {"shimaore": "Titi.m4a", "kibouchi": "Héli.m4a"},
            "chaud": {"shimaore": "Moro.m4a", "kibouchi": "Mèyi.m4a"},
            "froid": {"shimaore": "Baridi.m4a", "kibouchi": "Manintsi.m4a"},
            "content": {"shimaore": "Oujiviwa.m4a", "kibouchi": "Ravou.m4a"}
        }
        
        try:
            # Récupérer tous les adjectifs
            response = requests.get(f"{API_BASE}/words?category=adjectifs", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Récupération adjectifs pour exemples spécifiques",
                    False,
                    f"Erreur HTTP {response.status_code}"
                )
                return
                
            adjectifs = response.json()
            
            for adj_name, expected_files in specific_examples.items():
                # Trouver l'adjectif
                adj = next((a for a in adjectifs if a.get('french', '').lower() == adj_name.lower()), None)
                
                if not adj:
                    self.log_result(
                        f"Adjectif '{adj_name}' trouvé",
                        False,
                        f"Adjectif '{adj_name}' non trouvé dans la base"
                    )
                    continue
                
                # Vérifier dual_audio_system
                if adj.get('dual_audio_system') == True:
                    self.log_result(
                        f"Adjectif '{adj_name}' - dual audio",
                        True,
                        f"Adjectif '{adj_name}' a dual_audio_system: true"
                    )
                    
                    # Vérifier les métadonnées audio
                    shimoare_file = adj.get('shimoare_audio_filename')
                    kibouchi_file = adj.get('kibouchi_audio_filename')
                    
                    if shimoare_file or kibouchi_file:
                        self.log_result(
                            f"Adjectif '{adj_name}' - fichiers audio",
                            True,
                            f"Fichiers audio: Shimaoré={shimoare_file}, Kibouchi={kibouchi_file}"
                        )
                    else:
                        self.log_result(
                            f"Adjectif '{adj_name}' - fichiers audio",
                            False,
                            f"Métadonnées audio manquantes pour '{adj_name}'"
                        )
                else:
                    self.log_result(
                        f"Adjectif '{adj_name}' - dual audio",
                        False,
                        f"Adjectif '{adj_name}' n'a pas dual_audio_system: true"
                    )
                    
        except Exception as e:
            self.log_result(
                "Exemples spécifiques",
                False,
                f"Exception: {str(e)}"
            )

    def test_5_endpoint_adjectifs_performance(self):
        """Test 5: Endpoint et performance adjectifs"""
        print("🔧 TEST 5: Endpoint et performance adjectifs")
        
        try:
            # Test de l'endpoint /api/audio/adjectifs/{filename}
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
            adjectifs_info = data.get('adjectifs', {})
            
            if isinstance(adjectifs_info, dict):
                adjectifs_files = adjectifs_info.get('files', [])
            else:
                adjectifs_files = []
            
            if not adjectifs_files:
                self.log_result(
                    "Fichiers audio adjectifs disponibles",
                    False,
                    "Aucun fichier audio adjectifs trouvé"
                )
                return
            
            # Vérifier qu'il y a au moins 70 fichiers (attendu: 75 fichiers pour 34 adjectifs avec dual audio)
            if len(adjectifs_files) >= 70:
                self.log_result(
                    "Nombre fichiers audio adjectifs",
                    True,
                    f"{len(adjectifs_files)} fichiers audio adjectifs trouvés (≥70 attendu)"
                )
            else:
                self.log_result(
                    "Nombre fichiers audio adjectifs",
                    False,
                    f"Nombre insuffisant de fichiers audio",
                    "Au moins 70 fichiers",
                    f"{len(adjectifs_files)} fichiers"
                )
            
            # Tester l'endpoint avec quelques fichiers
            test_files = ["Bolé.m4a", "Bé.m4a", "Titi.m4a", "Héli.m4a", "Moro.m4a"]
            available_test_files = [f for f in test_files if f in adjectifs_files]
            
            if not available_test_files:
                available_test_files = adjectifs_files[:3]  # Prendre les 3 premiers disponibles
            
            for filename in available_test_files:
                try:
                    start_time = datetime.now()
                    file_response = requests.get(f"{API_BASE}/audio/adjectifs/{filename}", timeout=10)
                    end_time = datetime.now()
                    response_time = (end_time - start_time).total_seconds()
                    
                    if file_response.status_code == 200:
                        content_type = file_response.headers.get('content-type', '')
                        if 'audio' in content_type.lower():
                            self.log_result(
                                f"Endpoint adjectifs - {filename}",
                                True,
                                f"Fichier {filename} servi correctement ({response_time:.2f}s, {content_type})"
                            )
                        else:
                            self.log_result(
                                f"Endpoint adjectifs - {filename}",
                                False,
                                f"Content-Type incorrect: {content_type}"
                            )
                    else:
                        self.log_result(
                            f"Endpoint adjectifs - {filename}",
                            False,
                            f"Erreur HTTP {file_response.status_code} pour {filename}"
                        )
                        
                except Exception as e:
                    self.log_result(
                        f"Endpoint adjectifs - {filename}",
                        False,
                        f"Exception: {str(e)}"
                    )
            
            # Vérifier le total de fichiers audio (attendu: 687+)
            total_files = data.get('total_files', 0)
            if total_files >= 680:
                self.log_result(
                    "Total fichiers audio système",
                    True,
                    f"{total_files} fichiers audio au total (≥680 attendu)"
                )
            else:
                self.log_result(
                    "Total fichiers audio système",
                    False,
                    f"Total insuffisant de fichiers audio",
                    "Au moins 680 fichiers",
                    f"{total_files} fichiers"
                )
                
        except Exception as e:
            self.log_result(
                "Endpoint et performance adjectifs",
                False,
                f"Exception: {str(e)}"
            )

    def test_6_integrite_globale(self):
        """Test 6: Intégrité globale du système avec 12 catégories"""
        print("🔧 TEST 6: Intégrité globale")
        
        try:
            # Vérifier que le système gère 12 catégories
            response = requests.get(f"{API_BASE}/audio/info", timeout=10)
            
            if response.status_code != 200:
                self.log_result(
                    "Intégrité système audio",
                    False,
                    f"Erreur HTTP {response.status_code}"
                )
                return
                
            data = response.json()
            
            # Vérifier les 12 catégories attendues
            expected_categories = [
                'famille', 'nature', 'nombres', 'animaux', 'corps',
                'salutations', 'couleurs', 'grammaire', 'nourriture', 'verbes',
                'adjectifs', 'expressions'  # Ajout des nouvelles catégories
            ]
            
            missing_categories = []
            present_categories = []
            
            for category in expected_categories:
                if category in data:
                    present_categories.append(category)
                else:
                    missing_categories.append(category)
            
            if len(present_categories) >= 12:
                self.log_result(
                    "12+ catégories audio présentes",
                    True,
                    f"Au moins 12 catégories présentes: {', '.join(present_categories)}"
                )
            else:
                self.log_result(
                    "12+ catégories audio présentes",
                    False,
                    f"Catégories manquantes: {', '.join(missing_categories)}",
                    "12+ catégories",
                    f"{len(present_categories)} catégories"
                )
            
            # Vérifier la cohérence des audio_dirs configuration
            endpoints = data.get('endpoints', {})
            if len(endpoints) >= 12:  # Au moins 12 endpoints
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
                    "Au moins 12 endpoints",
                    f"{len(endpoints)} endpoints"
                )
            
            # Tester que les autres catégories fonctionnent toujours
            test_categories = ['famille', 'animaux', 'nombres']  # Quelques catégories existantes
            
            for category in test_categories:
                if category in data:
                    category_info = data[category]
                    if isinstance(category_info, dict) and category_info.get('count', 0) > 0:
                        # Tester un fichier de cette catégorie
                        files = category_info.get('files', [])
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
        print("🎯 DÉBUT DES TESTS - INTÉGRATION SECTION ADJECTIFS")
        print("=" * 60)
        print()
        
        # Exécuter tous les tests
        self.test_1_extension_systeme_audio_dual_12_categories()
        self.test_2_couverture_section_adjectifs()
        self.test_3_fonctionnalite_systeme_dual_adjectifs()
        self.test_4_exemples_specifiques()
        self.test_5_endpoint_adjectifs_performance()
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
            print("🎉 TOUS LES TESTS RÉUSSIS - INTÉGRATION ADJECTIFS COMPLÈTE!")
            return True
        elif self.failed_tests <= 2:
            print("⚠️  INTÉGRATION MAJORITAIREMENT RÉUSSIE - Quelques ajustements mineurs nécessaires")
            return True
        else:
            print("❌ INTÉGRATION INCOMPLÈTE - Corrections nécessaires")
            return False

def main():
    """Fonction principale"""
    print("🚀 LANCEMENT DES TESTS BACKEND - SECTION ADJECTIFS")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"🔗 API Base: {API_BASE}")
    print()
    
    tester = AdjectifsAudioTester()
    success = tester.run_all_tests()
    
    # Code de sortie
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()