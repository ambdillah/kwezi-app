#!/usr/bin/env python3
"""
Tests complets backend avant déploiement APK - Application Kwezi
Test du backend de production: https://kwezi-backend.onrender.com
"""

import requests
import json
import sys
import time
from typing import Dict, List, Optional

# Configuration
BACKEND_URL = "https://kwezi-backend.onrender.com"
API_URL = f"{BACKEND_URL}/api"
TIMEOUT = 10

class KweziBackendTester:
    def __init__(self):
        self.backend_url = API_URL
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.critical_issues = []
        self.minor_issues = []
        
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅"
        else:
            status = "❌"
        
        result = f"{status} {test_name}"
        if details:
            result += f": {details}"
        
        self.test_results.append(result)
        print(result)
        
    def log_issue(self, issue: str, is_critical: bool = True):
        """Log critical or minor issue"""
        if is_critical:
            self.critical_issues.append(issue)
            print(f"🚨 CRITIQUE: {issue}")
        else:
            self.minor_issues.append(issue)
            print(f"⚠️ MINEUR: {issue}")
        
    def test_api_endpoints(self):
        """Test des endpoints principaux de l'API"""
        print("\n=== 1. API ENDPOINTS PRINCIPAUX ===")
        
        # 1. GET /api/health (vérifier connexion DB)
        try:
            start_time = time.time()
            response = requests.get(f"{BACKEND_URL}/api/health", timeout=TIMEOUT)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if "database" in data and data.get("database") == "connected":
                    self.log_test("GET /api/health", True, f"Connexion DB OK ({response_time:.3f}s)")
                else:
                    self.log_test("GET /api/health", False, "Connexion DB non confirmée")
                    self.log_issue("Base de données non connectée")
            else:
                self.log_test("GET /api/health", False, f"Status {response.status_code}")
                self.log_issue("Endpoint health non accessible")
        except Exception as e:
            self.log_test("GET /api/health", False, f"Erreur: {str(e)}")
            self.log_issue("Endpoint health en erreur")

        # 2. GET /api/words (vérifier les 635 mots)
        try:
            start_time = time.time()
            response = requests.get(f"{BACKEND_URL}/api/words", timeout=TIMEOUT)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                # Handle both direct array and wrapped response formats
                if isinstance(data, dict) and "words" in data:
                    words = data["words"]
                    total_count = data.get("total", len(words))
                elif isinstance(data, list):
                    words = data
                    total_count = len(words)
                else:
                    words = []
                    total_count = 0
                
                word_count = len(words)
                
                if total_count >= 635:
                    self.log_test("GET /api/words", True, f"{total_count} mots trouvés ({word_count} retournés, {response_time:.3f}s)")
                else:
                    self.log_test("GET /api/words", False, f"Seulement {total_count} mots (attendu: 635+)")
                    self.log_issue(f"Nombre de mots insuffisant: {total_count}/635")
                    
                # Stocker les mots pour tests ultérieurs
                self.words_data = words
                self.total_words = total_count
            else:
                self.log_test("GET /api/words", False, f"Status {response.status_code}")
                self.log_issue("Endpoint words non accessible")
                self.words_data = []
                self.total_words = 0
        except Exception as e:
            self.log_test("GET /api/words", False, f"Erreur: {str(e)}")
            self.log_issue("Endpoint words en erreur")
            self.words_data = []
            self.total_words = 0

        # 3. GET /api/words?category=famille
        try:
            response = requests.get(f"{BACKEND_URL}/api/words?category=famille", timeout=TIMEOUT)
            if response.status_code == 200:
                famille_words = response.json()
                self.log_test("GET /api/words?category=famille", True, f"{len(famille_words)} mots famille")
            else:
                self.log_test("GET /api/words?category=famille", False, f"Status {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/words?category=famille", False, f"Erreur: {str(e)}")

        # 4. GET /api/words?search=maman
        try:
            response = requests.get(f"{BACKEND_URL}/api/words?search=maman", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                # Handle both direct array and wrapped response formats
                if isinstance(data, dict) and "words" in data:
                    search_results = data["words"]
                elif isinstance(data, list):
                    search_results = data
                else:
                    search_results = []
                    
                found_maman = any(word.get("french", "").lower() == "maman" for word in search_results)
                if found_maman:
                    self.log_test("GET /api/words?search=maman", True, f"Recherche OK ({len(search_results)} résultats)")
                else:
                    self.log_test("GET /api/words?search=maman", False, "Mot 'maman' non trouvé")
            else:
                self.log_test("GET /api/words?search=maman", False, f"Status {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/words?search=maman", False, f"Erreur: {str(e)}")

        # 5. GET /api/sentences
        try:
            response = requests.get(f"{BACKEND_URL}/api/sentences", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                # Handle both direct array and wrapped response formats
                if isinstance(data, dict) and "sentences" in data:
                    sentences = data["sentences"]
                    total_count = data.get("total", len(sentences))
                elif isinstance(data, list):
                    sentences = data
                    total_count = len(sentences)
                else:
                    sentences = []
                    total_count = 0
                    
                if total_count >= 270:
                    self.log_test("GET /api/sentences", True, f"{total_count} phrases pour jeux")
                    self.sentences_data = sentences
                else:
                    self.log_test("GET /api/sentences", False, f"Seulement {total_count} phrases (attendu: 270+)")
                    self.log_issue(f"Nombre de phrases insuffisant: {total_count}/270")
                    self.sentences_data = sentences
            else:
                self.log_test("GET /api/sentences", False, f"Status {response.status_code}")
                self.sentences_data = []
        except Exception as e:
            self.log_test("GET /api/sentences", False, f"Erreur: {str(e)}")
            self.sentences_data = []

        # 6. GET /api/categories
        try:
            response = requests.get(f"{BACKEND_URL}/api/categories", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                # Handle both direct array and wrapped response formats
                if isinstance(data, dict) and "categories" in data:
                    categories = data["categories"]
                elif isinstance(data, list):
                    categories = data
                else:
                    categories = []
                    
                if len(categories) >= 16:
                    self.log_test("GET /api/categories", True, f"{len(categories)} catégories")
                else:
                    self.log_test("GET /api/categories", False, f"Seulement {len(categories)} catégories (attendu: 16+)")
            else:
                self.log_test("GET /api/categories", False, f"Status {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/categories", False, f"Erreur: {str(e)}")

        # 7. GET /api/exercises
        try:
            response = requests.get(f"{BACKEND_URL}/api/exercises", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                # Handle both direct array and wrapped response formats
                if isinstance(data, dict) and "exercises" in data:
                    exercises = data["exercises"]
                elif isinstance(data, list):
                    exercises = data
                else:
                    exercises = []
                    
                if len(exercises) >= 10:
                    self.log_test("GET /api/exercises", True, f"{len(exercises)} exercices")
                else:
                    self.log_test("GET /api/exercises", False, f"Seulement {len(exercises)} exercices (attendu: 10+)")
            else:
                self.log_test("GET /api/exercises", False, f"Status {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/exercises", False, f"Erreur: {str(e)}")
    
    def test_data_integrity(self):
        """Test de l'intégrité des données"""
        print("\n=== 2. INTÉGRITÉ DES DONNÉES ===")
        
        if not hasattr(self, 'words_data') or not self.words_data:
            self.log_issue("Impossible de tester l'intégrité - données mots non disponibles")
            return
            
        # Test 1: Tous les mots ont les champs requis
        complete_words = 0
        for word in self.words_data:
            if all(key in word and word[key] for key in ["french", "shimaore", "kibouchi", "category"]):
                complete_words += 1
                
        sample_size = len(self.words_data)
        if sample_size > 0:
            completion_rate = (complete_words / sample_size) * 100
            if completion_rate >= 99:
                self.log_test("Champs requis complets", True, f"{completion_rate:.1f}% des mots complets (échantillon de {sample_size})")
            else:
                self.log_test("Champs requis complets", False, f"Seulement {completion_rate:.1f}% des mots complets (échantillon de {sample_size})")
                self.log_issue(f"Données incomplètes: {completion_rate:.1f}%")
        else:
            self.log_test("Champs requis complets", False, "Aucun mot disponible pour test")
            self.log_issue("Aucune donnée disponible")

        # Test 2: Orthographe française avec accents (test via API search)
        accent_words = ["Tête", "Lèvre", "Côtes"]  # Test specific words via search
        found_accents = 0
        
        for target_word in accent_words:
            try:
                search_response = requests.get(f"{BACKEND_URL}/api/words?search={target_word.lower()}", timeout=TIMEOUT)
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    if isinstance(search_data, dict) and "words" in search_data:
                        search_results = search_data["words"]
                    else:
                        search_results = search_data if isinstance(search_data, list) else []
                    
                    found = any(word.get("french", "") == target_word for word in search_results)
                    if found:
                        found_accents += 1
                        self.log_test(f"Mot avec accent '{target_word}'", True, "Trouvé via recherche")
                    else:
                        self.log_test(f"Mot avec accent '{target_word}'", False, "Non trouvé via recherche")
                else:
                    self.log_test(f"Mot avec accent '{target_word}'", False, f"Erreur recherche: {search_response.status_code}")
            except Exception as e:
                self.log_test(f"Mot avec accent '{target_word}'", False, f"Erreur: {str(e)}")
                
        # Check if we found at least one accent word, or if we have accents in our sample data
        sample_has_accents = any(
            any(char in word.get("french", "") for char in "àâäéèêëïîôöùûüÿç") 
            for word in self.words_data
        )
        
        if found_accents >= 1 or sample_has_accents:
            self.log_test("Orthographe française", True, f"Accents français détectés (recherche: {found_accents}/{len(accent_words)}, échantillon: {sample_has_accents})")
        else:
            self.log_test("Orthographe française", False, f"Seulement {found_accents}/{len(accent_words)} mots avec accents")
            self.log_issue("Orthographe française incorrecte")

        # Test 3: Pas de doublons
        french_words = [word.get("french", "").lower() for word in self.words_data if word.get("french")]
        unique_words = set(french_words)
        duplicates = len(french_words) - len(unique_words)
        
        if duplicates == 0:
            self.log_test("Pas de doublons", True, "Aucun doublon détecté")
        else:
            self.log_test("Pas de doublons", False, f"{duplicates} doublons trouvés")
            self.log_issue(f"Doublons détectés: {duplicates}")
    
    def test_audio_system(self):
        """Test du système audio"""
        print("\n=== 3. SYSTÈME AUDIO ===")
        
        if not hasattr(self, 'words_data') or not self.words_data:
            self.log_issue("Impossible de tester l'audio - données mots non disponibles")
            return
            
        # Test 1: Champs audio présents
        audio_words = 0
        dual_audio_words = 0
        
        for word in self.words_data:
            has_audio_fields = any([
                word.get("shimoare_audio_filename"),
                word.get("kibouchi_audio_filename"),
                word.get("audio_filename_shimaore"),
                word.get("audio_filename_kibouchi")
            ])
            
            if has_audio_fields:
                audio_words += 1
                
            if word.get("dual_audio_system") == True:
                dual_audio_words += 1
                
        audio_coverage = (audio_words / len(self.words_data)) * 100
        dual_coverage = (dual_audio_words / len(self.words_data)) * 100
        
        if audio_coverage >= 50:
            self.log_test("Couverture audio", True, f"{audio_coverage:.1f}% des mots ont des références audio")
        else:
            self.log_test("Couverture audio", False, f"Seulement {audio_coverage:.1f}% de couverture audio")
            
        if dual_coverage >= 30:
            self.log_test("Système dual audio", True, f"{dual_coverage:.1f}% avec dual_audio_system")
        else:
            self.log_test("Système dual audio", False, f"Seulement {dual_coverage:.1f}% avec dual_audio_system")

        # Test 2: Exemples spécifiques via recherche API
        test_words = ["Papa", "Maman", "Famille", "Bonjour"]
        found_audio_examples = 0
        
        for test_word in test_words:
            try:
                search_response = requests.get(f"{BACKEND_URL}/api/words?search={test_word.lower()}", timeout=TIMEOUT)
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    if isinstance(search_data, dict) and "words" in search_data:
                        search_results = search_data["words"]
                    else:
                        search_results = search_data if isinstance(search_data, list) else []
                    
                    word_data = next((w for w in search_results if w.get("french", "").lower() == test_word.lower()), None)
                    if word_data:
                        has_audio = any([
                            word_data.get("shimoare_audio_filename"),
                            word_data.get("kibouchi_audio_filename"),
                            word_data.get("audio_filename_shimaore"),
                            word_data.get("audio_filename_kibouchi"),
                            word_data.get("has_authentic_audio")
                        ])
                        if has_audio:
                            found_audio_examples += 1
                            self.log_test(f"Audio '{test_word}'", True, "Références audio trouvées via recherche")
                        else:
                            self.log_test(f"Audio '{test_word}'", False, "Pas de références audio")
                    else:
                        self.log_test(f"Audio '{test_word}'", False, "Mot non trouvé via recherche")
                else:
                    self.log_test(f"Audio '{test_word}'", False, f"Erreur recherche: {search_response.status_code}")
            except Exception as e:
                self.log_test(f"Audio '{test_word}'", False, f"Erreur: {str(e)}")
                
        if found_audio_examples >= 3:
            self.log_test("Exemples audio", True, f"{found_audio_examples}/{len(test_words)} exemples avec audio")
        else:
            self.log_test("Exemples audio", False, f"Seulement {found_audio_examples}/{len(test_words)} exemples avec audio")
    
    def test_games_sentences(self):
        """Test du jeu Construire des Phrases"""
        print("\n=== 4. JEUX - CONSTRUIRE DES PHRASES ===")
        
        if not hasattr(self, 'sentences_data') or not self.sentences_data:
            self.log_issue("Impossible de tester les jeux - données phrases non disponibles")
            return
            
        # Test 1: Structure des phrases
        complete_sentences = 0
        tenses_found = set()
        difficulties_found = set()
        
        for sentence in self.sentences_data:
            if all(key in sentence for key in ["french", "shimaore", "kibouchi", "tense", "difficulty"]):
                complete_sentences += 1
                
            if "tense" in sentence:
                tenses_found.add(sentence["tense"])
                
            if "difficulty" in sentence:
                difficulties_found.add(sentence["difficulty"])
                
        structure_rate = (complete_sentences / len(self.sentences_data)) * 100
        
        if structure_rate >= 95:
            self.log_test("Structure phrases", True, f"{structure_rate:.1f}% phrases complètes")
        else:
            self.log_test("Structure phrases", False, f"Seulement {structure_rate:.1f}% phrases complètes")
            self.log_issue(f"Structure phrases incomplète: {structure_rate:.1f}%")

        # Test 2: Temps verbaux
        expected_tenses = {"present", "past", "future"}
        tenses_coverage = len(tenses_found.intersection(expected_tenses))
        
        if tenses_coverage >= 2:
            self.log_test("Temps verbaux", True, f"{tenses_coverage}/3 temps trouvés: {list(tenses_found)}")
        else:
            self.log_test("Temps verbaux", False, f"Seulement {tenses_coverage}/3 temps: {list(tenses_found)}")

        # Test 3: Niveaux de difficulté
        if len(difficulties_found) >= 2:
            self.log_test("Niveaux difficulté", True, f"Niveaux trouvés: {sorted(list(difficulties_found))}")
        else:
            self.log_test("Niveaux difficulté", False, f"Seulement {len(difficulties_found)} niveaux")
    
    def test_performance(self):
        """Test de performance et stabilité"""
        print("\n=== 5. PERFORMANCE & STABILITÉ ===")
        
        # Test 1: Temps de réponse
        endpoints_to_test = [
            "/api/words",
            "/api/categories", 
            "/api/sentences"
        ]
        
        fast_responses = 0
        
        for endpoint in endpoints_to_test:
            try:
                start_time = time.time()
                response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=TIMEOUT)
                response_time = time.time() - start_time
                
                if response.status_code == 200 and response_time < 2.0:
                    fast_responses += 1
                    self.log_test(f"Temps réponse {endpoint}", True, f"{response_time:.3f}s")
                else:
                    self.log_test(f"Temps réponse {endpoint}", False, f"{response_time:.3f}s (trop lent)")
                    
            except Exception as e:
                self.log_test(f"Temps réponse {endpoint}", False, f"Erreur: {str(e)}")
                
        if fast_responses >= 2:
            self.log_test("Performance globale", True, f"{fast_responses}/{len(endpoints_to_test)} endpoints rapides")
        else:
            self.log_test("Performance globale", False, f"Seulement {fast_responses}/{len(endpoints_to_test)} endpoints rapides")
            self.log_issue("Performance insuffisante")

        # Test 2: Requêtes consécutives (stabilité)
        consecutive_success = 0
        for i in range(3):
            try:
                response = requests.get(f"{BACKEND_URL}/api/words?category=famille", timeout=TIMEOUT)
                if response.status_code == 200:
                    consecutive_success += 1
                time.sleep(0.5)  # Petite pause entre requêtes
            except:
                pass
                
        if consecutive_success >= 2:
            self.log_test("Stabilité", True, f"{consecutive_success}/3 requêtes consécutives réussies")
        else:
            self.log_test("Stabilité", False, f"Seulement {consecutive_success}/3 requêtes réussies")
            self.log_issue("Service instable")
    
    def generate_report(self):
        """Génère le rapport final"""
        print("\n" + "="*80)
        print("📊 RAPPORT FINAL - TESTS BACKEND KWEZI")
        print("="*80)
        
        # Calcul des statistiques par catégorie
        api_passed = sum(1 for result in self.test_results if "GET /api/" in result and "✅" in result)
        api_total = sum(1 for result in self.test_results if "GET /api/" in result)
        
        data_passed = sum(1 for result in self.test_results if any(keyword in result for keyword in ["Champs requis", "Orthographe", "doublons"]) and "✅" in result)
        data_total = sum(1 for result in self.test_results if any(keyword in result for keyword in ["Champs requis", "Orthographe", "doublons"]))
        
        audio_passed = sum(1 for result in self.test_results if any(keyword in result for keyword in ["audio", "Audio"]) and "✅" in result)
        audio_total = sum(1 for result in self.test_results if any(keyword in result for keyword in ["audio", "Audio"]))
        
        games_passed = sum(1 for result in self.test_results if any(keyword in result for keyword in ["phrases", "Structure", "Temps", "difficulté"]) and "✅" in result)
        games_total = sum(1 for result in self.test_results if any(keyword in result for keyword in ["phrases", "Structure", "Temps", "difficulté"]))
        
        perf_passed = sum(1 for result in self.test_results if any(keyword in result for keyword in ["Performance", "Temps réponse", "Stabilité"]) and "✅" in result)
        perf_total = sum(1 for result in self.test_results if any(keyword in result for keyword in ["Performance", "Temps réponse", "Stabilité"]))
        
        # Affichage du résumé
        print(f"✅ API Endpoints : {api_passed}/{api_total} tests réussis")
        print(f"✅ Intégrité Données : {data_passed}/{data_total} tests réussis")
        print(f"✅ Système Audio : {audio_passed}/{audio_total} tests réussis")
        print(f"✅ Jeux : {games_passed}/{games_total} tests réussis")
        print(f"✅ Performance : {perf_passed}/{perf_total} tests réussis")
        
        # Problèmes critiques
        if self.critical_issues:
            print(f"\n🚨 PROBLÈMES CRITIQUES TROUVÉS : {len(self.critical_issues)}")
            for issue in self.critical_issues:
                print(f"   • {issue}")
        else:
            print("\n✅ Aucun problème critique détecté")
            
        # Problèmes mineurs
        if self.minor_issues:
            print(f"\n⚠️ PROBLÈMES MINEURS : {len(self.minor_issues)}")
            for issue in self.minor_issues:
                print(f"   • {issue}")
        else:
            print("\n✅ Aucun problème mineur détecté")
            
        # Verdict final
        total_critical = len(self.critical_issues)
        
        print(f"\n{'='*80}")
        if total_critical == 0:
            print("✅ PRÊT POUR DÉPLOIEMENT : OUI")
            print("Le backend est stable et fonctionnel pour le déploiement APK")
        else:
            print("❌ PRÊT POUR DÉPLOIEMENT : NON")
            print(f"⚠️ {total_critical} problème(s) critique(s) à corriger avant déploiement")
            
        print("="*80)
    
    def run_all_tests(self):
        """Exécuter tous les tests pour le déploiement APK"""
        print("🎯 TESTS COMPLETS BACKEND AVANT DÉPLOIEMENT APK")
        print(f"Backend testé: {BACKEND_URL}")
        print("="*80)
        
        try:
            self.test_api_endpoints()
            self.test_data_integrity()
            self.test_audio_system()
            self.test_games_sentences()
            self.test_performance()
            
        except KeyboardInterrupt:
            print("\n⚠️ Tests interrompus par l'utilisateur")
        except Exception as e:
            print(f"\n🚨 Erreur critique pendant les tests: {str(e)}")
            self.log_issue(f"Erreur système: {str(e)}")
        
        finally:
            self.generate_report()
            
        return len(self.critical_issues) == 0
    
def main():
    """Fonction principale"""
    tester = KweziBackendTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
    
    def run_all_tests(self):
        """Exécuter tous les tests pour la section adjectifs et fonctionnalités connexes"""
        print("🎯 DÉBUT DES TESTS COMPLETS SECTION ADJECTIFS")
        print("=" * 80)
        
        # Test 0: Basic connectivity
        if not self.test_api_connectivity():
            print("❌ API connectivity failed. Stopping tests.")
            return False
        
        # Test 1: Section adjectifs
        print("\n📝 Testing Section Adjectifs...")
        adjectifs_exists, adjectifs_data = self.test_adjectifs_section_exists()
        
        if adjectifs_exists and adjectifs_data:
            self.test_specific_adjectifs_correspondences(adjectifs_data)
            self.test_adjectifs_audio_coverage(adjectifs_data)
        
        # Test 2: Global structure
        print("\n🌍 Testing Global Structure...")
        structure_success, all_words_data = self.test_global_structure_update()
        
        # Test 3: Nourriture orthography
        print("\n🍽️ Testing Nourriture Orthography...")
        self.test_nourriture_orthography()
        
        # Test 4: API Performance
        print("\n⚡ Testing API Performance...")
        self.test_adjectifs_api_performance()
        
        # Test 5: Audio file access
        print("\n🎵 Testing Audio File Access...")
        self.test_audio_file_access()
        
        # Test 6: Global audio coverage
        if structure_success and all_words_data:
            print("\n🎧 Testing Global Audio Coverage...")
            self.test_global_audio_coverage(all_words_data)
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.total_tests - self.passed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.total_tests - self.passed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if "❌ FAIL" in result:
                    print(f"  - {result}")
        
        print("\n🎯 DETAILED RESULTS FOR MAIN AGENT:")
        
        # Critical findings for main agent
        critical_issues = []
        successes = []
        
        for result in self.test_results:
            if "❌ FAIL" in result and any(keyword in result.lower() 
                                           for keyword in ["adjectifs", "correspondence", "audio coverage"]):
                critical_issues.append(f"❌ {result}")
            elif "✅ PASS" in result:
                successes.append(f"✅ {result}")
        
        if critical_issues:
            print("\n🚨 CRITICAL ISSUES FOUND:")
            for issue in critical_issues:
                print(f"  {issue}")
        
        print(f"\n✅ SUCCESSFUL TESTS ({len(successes)}):")
        for success in successes[:10]:  # Show first 10 successes
            print(f"  {success}")
        if len(successes) > 10:
            print(f"  ... and {len(successes) - 10} more")
        
        return success_rate >= 70  # Consider 70%+ success rate as overall success

if __name__ == "__main__":
    tester = AdjectifsComprehensiveTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)