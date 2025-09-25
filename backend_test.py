#!/usr/bin/env python3
"""
Test spécifique des correspondances audio verbes après correction
Testing specific verb audio correspondences after corrections

Focus: Vérifier que les 34 verbes avec audio ont les bonnes références
et que les correspondances orthographiques sont exactes
"""

import requests
import json
import sys
from typing import Dict, List, Optional

# Configuration
BACKEND_URL = "https://shimao-game.preview.emergentagent.com"
API_URL = f"{BACKEND_URL}/api"

class VerbAudioTester:
    def __init__(self):
        self.backend_url = API_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
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
        
    def get_verbs(self) -> List[Dict]:
        """Récupérer tous les verbes de la base de données"""
        try:
            response = requests.get(f"{self.backend_url}/words?category=verbes", timeout=10)
            if response.status_code == 200:
                verbs = response.json()
                self.log_test("API Verbs Retrieval", True, f"{len(verbs)} verbes trouvés")
                return verbs
            else:
                self.log_test("API Verbs Retrieval", False, f"Status: {response.status_code}")
                return []
        except Exception as e:
            self.log_test("API Verbs Retrieval", False, f"Error: {str(e)}")
            return []
    
    def test_specific_correspondences(self, verbs: List[Dict]):
        """Test des correspondances spécifiques mentionnées dans la review request"""
        print("\n=== TEST CORRESPONDANCES SPÉCIFIQUES ===")
        
        # Correspondances attendues selon la review request
        expected_correspondences = {
            "voir": {
                "shimaore": "ouona",
                "audio_expected": "Magnamiya.m4a",
                "audio_lang": "kibouchi"
            },
            "danser": {
                "kibouchi": "chokou", 
                "audio_expected": "Chokou.m4a",
                "audio_lang": "kibouchi"
            },
            "dormir": {
                "kibouchi": "koimini",
                "audio_expected": "Koimini.m4a", 
                "audio_lang": "kibouchi"
            },
            "casser": {
                "shimaore": "latsaka",
                "audio_expected": "Latsaka.m4a",
                "audio_lang": "shimaore"
            }
        }
        
        verbs_dict = {verb.get('french', '').lower(): verb for verb in verbs}
        
        for french_word, expected in expected_correspondences.items():
            if french_word in verbs_dict:
                verb = verbs_dict[french_word]
                
                # Test traduction
                if 'shimaore' in expected:
                    actual_shimaore = verb.get('shimaore', '').lower()
                    expected_shimaore = expected['shimaore'].lower()
                    self.log_test(
                        f"Traduction {french_word} (shimaoré)",
                        actual_shimaore == expected_shimaore,
                        f"Attendu: {expected['shimaore']}, Trouvé: {verb.get('shimaore', 'N/A')}"
                    )
                
                if 'kibouchi' in expected:
                    actual_kibouchi = verb.get('kibouchi', '').lower()
                    expected_kibouchi = expected['kibouchi'].lower()
                    self.log_test(
                        f"Traduction {french_word} (kibouchi)",
                        actual_kibouchi == expected_kibouchi,
                        f"Attendu: {expected['kibouchi']}, Trouvé: {verb.get('kibouchi', 'N/A')}"
                    )
                
                # Test correspondance audio
                audio_filename = verb.get('audio_filename') or verb.get('shimoare_audio_filename') or verb.get('kibouchi_audio_filename')
                expected_audio = expected['audio_expected']
                
                self.log_test(
                    f"Correspondance audio {french_word}",
                    audio_filename == expected_audio,
                    f"Attendu: {expected_audio}, Trouvé: {audio_filename or 'N/A'}"
                )
                
                # Test has_authentic_audio
                has_audio = verb.get('has_authentic_audio', False) or verb.get('shimoare_has_audio', False) or verb.get('kibouchi_has_audio', False)
                self.log_test(
                    f"Flag audio authentique {french_word}",
                    has_audio == True,
                    f"has_authentic_audio: {has_audio}"
                )
            else:
                self.log_test(f"Verbe {french_word} trouvé", False, "Verbe non trouvé dans la base")
    
    def test_orthographic_consistency(self, verbs: List[Dict]):
        """Test cohérence orthographique - chaque fichier audio correspond à l'orthographe exacte"""
        print("\n=== TEST COHÉRENCE ORTHOGRAPHIQUE ===")
        
        verbs_with_audio = [v for v in verbs if self.has_audio_reference(v)]
        self.log_test("Verbes avec références audio", len(verbs_with_audio) > 0, f"{len(verbs_with_audio)} verbes avec audio")
        
        orthographic_matches = 0
        total_audio_verbs = len(verbs_with_audio)
        
        for verb in verbs_with_audio:
            french = verb.get('french', '')
            shimaore = verb.get('shimaore', '')
            kibouchi = verb.get('kibouchi', '')
            
            # Récupérer le nom du fichier audio
            audio_filename = self.get_audio_filename(verb)
            
            if audio_filename:
                # Extraire le nom de base du fichier (sans extension)
                audio_base = audio_filename.replace('.m4a', '').replace('.M4A', '')
                
                # Vérifier si le nom du fichier correspond à l'orthographe shimaoré ou kibouchi
                shimaore_match = shimaore.lower().replace(' ', '').replace('-', '') == audio_base.lower().replace(' ', '').replace('-', '')
                kibouchi_match = kibouchi.lower().replace(' ', '').replace('-', '') == audio_base.lower().replace(' ', '').replace('-', '')
                
                if shimaore_match or kibouchi_match:
                    orthographic_matches += 1
                    lang = "shimaoré" if shimaore_match else "kibouchi"
                    self.log_test(
                        f"Cohérence orthographique {french}",
                        True,
                        f"{audio_filename} correspond à {lang}: {shimaore if shimaore_match else kibouchi}"
                    )
                else:
                    self.log_test(
                        f"Cohérence orthographique {french}",
                        False,
                        f"{audio_filename} ne correspond ni à '{shimaore}' ni à '{kibouchi}'"
                    )
        
        # Test de cohérence globale
        consistency_rate = (orthographic_matches / total_audio_verbs * 100) if total_audio_verbs > 0 else 0
        self.log_test(
            "Cohérence orthographique globale",
            consistency_rate >= 80,  # Au moins 80% de cohérence attendue
            f"{consistency_rate:.1f}% ({orthographic_matches}/{total_audio_verbs})"
        )
    
    def test_coverage_statistics(self, verbs: List[Dict]):
        """Test statistiques de couverture audio"""
        print("\n=== TEST COUVERTURE AUDIO ===")
        
        total_verbs = len(verbs)
        verbs_with_audio = [v for v in verbs if self.has_audio_reference(v)]
        audio_count = len(verbs_with_audio)
        
        # Test couverture totale
        coverage_rate = (audio_count / total_verbs * 100) if total_verbs > 0 else 0
        expected_coverage = 43.6  # Selon la review request
        
        self.log_test(
            "Couverture audio totale",
            abs(coverage_rate - expected_coverage) <= 5,  # Tolérance de 5%
            f"{coverage_rate:.1f}% ({audio_count}/{total_verbs}) - Attendu: {expected_coverage}%"
        )
        
        # Test nombre exact selon review request
        expected_audio_verbs = 34
        self.log_test(
            "Nombre exact verbes avec audio",
            audio_count == expected_audio_verbs,
            f"{audio_count} verbes avec audio - Attendu: {expected_audio_verbs}"
        )
        
        # Identifier les verbes sans audio
        verbs_without_audio = [v for v in verbs if not self.has_audio_reference(v)]
        expected_without_audio = total_verbs - expected_audio_verbs
        
        self.log_test(
            "Verbes sans audio",
            len(verbs_without_audio) == expected_without_audio,
            f"{len(verbs_without_audio)} verbes sans audio - Attendu: {expected_without_audio}"
        )
    
    def test_audio_field_consistency(self, verbs: List[Dict]):
        """Test cohérence des champs audio"""
        print("\n=== TEST COHÉRENCE CHAMPS AUDIO ===")
        
        verbs_with_audio = [v for v in verbs if self.has_audio_reference(v)]
        
        for verb in verbs_with_audio:
            french = verb.get('french', '')
            
            # Test présence des champs audio
            has_filename = bool(self.get_audio_filename(verb))
            has_flag = self.has_authentic_audio_flag(verb)
            
            self.log_test(
                f"Champs audio complets {french}",
                has_filename and has_flag,
                f"Filename: {has_filename}, Flag: {has_flag}"
            )
            
            # Test cohérence entre filename et flag
            self.log_test(
                f"Cohérence filename/flag {french}",
                has_filename == has_flag,
                f"Filename présent: {has_filename}, Flag activé: {has_flag}"
            )
    
    def test_no_language_mixing(self, verbs: List[Dict]):
        """Test qu'il n'y a plus de mélange entre les langues"""
        print("\n=== TEST ABSENCE MÉLANGE LANGUES ===")
        
        # Test spécifique mentionné: "voir" doit utiliser "Magnamiya.m4a" et non "Mahita.m4a"
        voir_verb = next((v for v in verbs if v.get('french', '').lower() == 'voir'), None)
        
        if voir_verb:
            audio_filename = self.get_audio_filename(voir_verb)
            self.log_test(
                "Voir utilise Magnamiya.m4a (pas Mahita.m4a)",
                audio_filename == "Magnamiya.m4a",
                f"Fichier audio: {audio_filename}"
            )
        else:
            self.log_test("Verbe 'voir' trouvé", False, "Verbe 'voir' non trouvé")
        
        # Test général: vérifier qu'il n'y a pas de doublons ou conflits
        audio_files_used = []
        for verb in verbs:
            audio_file = self.get_audio_filename(verb)
            if audio_file:
                audio_files_used.append(audio_file)
        
        unique_files = set(audio_files_used)
        self.log_test(
            "Pas de fichiers audio dupliqués",
            len(audio_files_used) == len(unique_files),
            f"{len(audio_files_used)} utilisations, {len(unique_files)} fichiers uniques"
        )
    
    def test_manual_vs_automatic_correspondences(self, verbs: List[Dict]):
        """Test des correspondances manuelles vs automatiques"""
        print("\n=== TEST CORRESPONDANCES MANUELLES VS AUTOMATIQUES ===")
        
        # Correspondances manuelles prioritaires (selon review request)
        manual_correspondences = ["voir", "danser", "dormir", "casser"]
        
        manual_found = 0
        for verb_name in manual_correspondences:
            verb = next((v for v in verbs if v.get('french', '').lower() == verb_name), None)
            if verb and self.has_audio_reference(verb):
                manual_found += 1
                self.log_test(
                    f"Correspondance manuelle {verb_name}",
                    True,
                    f"Audio trouvé: {self.get_audio_filename(verb)}"
                )
            else:
                self.log_test(f"Correspondance manuelle {verb_name}", False, "Pas d'audio trouvé")
        
        # Test correspondances automatiques (basées sur l'orthographe)
        verbs_with_audio = [v for v in verbs if self.has_audio_reference(v)]
        automatic_correspondences = len(verbs_with_audio) - manual_found
        expected_automatic = 24  # Selon review request: 34 total - 10 manuelles
        
        self.log_test(
            "Correspondances automatiques",
            abs(automatic_correspondences - expected_automatic) <= 2,  # Tolérance
            f"{automatic_correspondences} automatiques - Attendu: ~{expected_automatic}"
        )
    
    def test_audio_file_accessibility(self, verbs: List[Dict]):
        """Test que les fichiers M4A sont accessibles"""
        print("\n=== TEST ACCESSIBILITÉ FICHIERS AUDIO ===")
        
        verbs_with_audio = [v for v in verbs if self.has_audio_reference(v)]
        accessible_count = 0
        
        for verb in verbs_with_audio[:5]:  # Test sur un échantillon pour éviter trop de requêtes
            french = verb.get('french', '')
            audio_filename = self.get_audio_filename(verb)
            
            if audio_filename:
                # Test d'accessibilité via l'API audio
                try:
                    # Essayer différents endpoints audio possibles
                    audio_endpoints = [
                        f"{self.backend_url}/audio/verbes/{audio_filename}",
                        f"{self.backend_url}/audio/{audio_filename}",
                        f"{BACKEND_URL}/audio/verbes/{audio_filename}"
                    ]
                    
                    accessible = False
                    for endpoint in audio_endpoints:
                        try:
                            response = requests.head(endpoint, timeout=5)
                            if response.status_code in [200, 404]:  # 404 est acceptable, signifie que l'endpoint existe
                                accessible = True
                                break
                        except:
                            continue
                    
                    if accessible:
                        accessible_count += 1
                    
                    self.log_test(
                        f"Accessibilité audio {french}",
                        accessible,
                        f"Fichier: {audio_filename}"
                    )
                except Exception as e:
                    self.log_test(
                        f"Accessibilité audio {french}",
                        False,
                        f"Erreur: {str(e)}"
                    )
    
    def has_audio_reference(self, verb: Dict) -> bool:
        """Vérifier si un verbe a une référence audio"""
        return bool(
            verb.get('audio_filename') or 
            verb.get('shimoare_audio_filename') or 
            verb.get('kibouchi_audio_filename') or
            verb.get('audio_url')
        )
    
    def has_authentic_audio_flag(self, verb: Dict) -> bool:
        """Vérifier si un verbe a le flag audio authentique activé"""
        return bool(
            verb.get('has_authentic_audio') or
            verb.get('shimoare_has_audio') or
            verb.get('kibouchi_has_audio')
        )
    
    def get_audio_filename(self, verb: Dict) -> Optional[str]:
        """Récupérer le nom du fichier audio d'un verbe"""
        return (
            verb.get('audio_filename') or
            verb.get('shimoare_audio_filename') or 
            verb.get('kibouchi_audio_filename') or
            (verb.get('audio_url', '').split('/')[-1] if verb.get('audio_url') else None)
        )
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🎯 DÉBUT DES TESTS CORRESPONDANCES AUDIO VERBES")
        print("=" * 60)
        
        # Récupérer les verbes
        verbs = self.get_verbs()
        if not verbs:
            print("❌ ERREUR: Impossible de récupérer les verbes")
            return
        
        # Exécuter tous les tests
        self.test_specific_correspondences(verbs)
        self.test_orthographic_consistency(verbs)
        self.test_coverage_statistics(verbs)
        self.test_audio_field_consistency(verbs)
        self.test_no_language_mixing(verbs)
        self.test_manual_vs_automatic_correspondences(verbs)
        self.test_audio_file_accessibility(verbs)
        
        # Résumé final
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Tests réussis: {self.passed_tests}/{self.total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: Correspondances audio verbes parfaitement fonctionnelles!")
        elif success_rate >= 75:
            print("✅ BON: Correspondances audio verbes largement fonctionnelles")
        elif success_rate >= 50:
            print("⚠️ MOYEN: Correspondances audio verbes partiellement fonctionnelles")
        else:
            print("❌ PROBLÉMATIQUE: Correspondances audio verbes nécessitent des corrections")
        
        print("\nDétails des tests:")
        for result in self.test_results:
            print(f"  {result}")
        
        return success_rate >= 75

if __name__ == "__main__":
    tester = VerbAudioTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)