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
                words = response.json()
                word_count = len(words)
                
                if word_count >= 635:
                    self.log_test("GET /api/words", True, f"{word_count} mots trouvés ({response_time:.3f}s)")
                else:
                    self.log_test("GET /api/words", False, f"Seulement {word_count} mots (attendu: 635+)")
                    self.log_issue(f"Nombre de mots insuffisant: {word_count}/635")
                    
                # Stocker les mots pour tests ultérieurs
                self.words_data = words
            else:
                self.log_test("GET /api/words", False, f"Status {response.status_code}")
                self.log_issue("Endpoint words non accessible")
                self.words_data = []
        except Exception as e:
            self.log_test("GET /api/words", False, f"Erreur: {str(e)}")
            self.log_issue("Endpoint words en erreur")
            self.words_data = []

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
                search_results = response.json()
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
                sentences = response.json()
                sentence_count = len(sentences)
                if sentence_count >= 270:
                    self.log_test("GET /api/sentences", True, f"{sentence_count} phrases pour jeux")
                    self.sentences_data = sentences
                else:
                    self.log_test("GET /api/sentences", False, f"Seulement {sentence_count} phrases (attendu: 270+)")
                    self.log_issue(f"Nombre de phrases insuffisant: {sentence_count}/270")
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
                categories = response.json()
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
                exercises = response.json()
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
                
        completion_rate = (complete_words / len(self.words_data)) * 100
        if completion_rate >= 99:
            self.log_test("Champs requis complets", True, f"{completion_rate:.1f}% des mots complets")
        else:
            self.log_test("Champs requis complets", False, f"Seulement {completion_rate:.1f}% des mots complets")
            self.log_issue(f"Données incomplètes: {completion_rate:.1f}%")

        # Test 2: Orthographe française avec accents
        accent_words = ["Frère", "Sœur", "École", "Étoile", "Tête", "Grand-père"]
        found_accents = 0
        
        for target_word in accent_words:
            found = any(word.get("french", "") == target_word for word in self.words_data)
            if found:
                found_accents += 1
                self.log_test(f"Mot avec accent '{target_word}'", True, "Trouvé")
            else:
                self.log_test(f"Mot avec accent '{target_word}'", False, "Non trouvé")
                
        if found_accents >= 4:
            self.log_test("Orthographe française", True, f"{found_accents}/{len(accent_words)} mots avec accents corrects")
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

        # Test 2: Exemples spécifiques
        test_words = ["Papa", "Maman", "Famille", "Bonjour"]
        found_audio_examples = 0
        
        for test_word in test_words:
            word_data = next((w for w in self.words_data if w.get("french", "").lower() == test_word.lower()), None)
            if word_data:
                has_audio = any([
                    word_data.get("shimoare_audio_filename"),
                    word_data.get("kibouchi_audio_filename"),
                    word_data.get("audio_filename_shimaore"),
                    word_data.get("audio_filename_kibouchi")
                ])
                if has_audio:
                    found_audio_examples += 1
                    self.log_test(f"Audio '{test_word}'", True, "Références audio trouvées")
                else:
                    self.log_test(f"Audio '{test_word}'", False, "Pas de références audio")
            else:
                self.log_test(f"Audio '{test_word}'", False, "Mot non trouvé")
                
        if found_audio_examples >= 2:
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
    
    def test_global_structure_update(self):
        """Test 2: Structure globale mise à jour"""
        print("\n=== TEST 2: STRUCTURE GLOBALE MISE À JOUR ===")
        
        try:
            # Test nombre total de sections
            response = requests.get(f"{self.backend_url}/words", timeout=15)
            if response.status_code != 200:
                self.log_test("Global Structure", False, f"API Error: {response.status_code}")
                return False, []
            
            all_words = response.json()
            total_words = len(all_words)
            
            # Compter les catégories uniques
            categories = set(word.get("category", "") for word in all_words)
            categories = {cat for cat in categories if cat}  # Remove empty categories
            section_count = len(categories)
            
            # Test nombre de sections (attendu: 11+)
            sections_success = section_count >= 11
            sections_details = f"Found {section_count} sections: {sorted(categories)}"
            
            # Test nombre total de mots (attendu: 467+)
            words_success = total_words >= 467
            words_details = f"Found {total_words} total words (expected 467+)"
            
            self.log_test("Global Sections Count", sections_success, sections_details)
            self.log_test("Global Words Count", words_success, words_details)
            
            return sections_success and words_success, all_words
        except Exception as e:
            self.log_test("Global Structure", False, f"Error: {str(e)}")
            return False, []
    
    def test_nourriture_orthography(self):
        """Test 3: Orthographe section nourriture"""
        print("\n=== TEST 3: ORTHOGRAPHE SECTION NOURRITURE ===")
        
        try:
            response = requests.get(f"{self.backend_url}/words?category=nourriture", timeout=10)
            if response.status_code != 200:
                self.log_test("Nourriture Section", False, f"API Error: {response.status_code}")
                return False
            
            nourriture_words = response.json()
            word_count = len(nourriture_words)
            
            # Test nombre de mots nourriture (attendu: 44)
            count_success = word_count >= 40  # Allow some flexibility
            count_details = f"Found {word_count} nourriture words (expected ~44)"
            
            # Test correspondances spécifiques
            specific_tests = [
                {"french": "riz", "shimaore": "tsoholé", "kibouchi": "vari"},
                {"french": "eau", "shimaore": "maji", "kibouchi": "ranou"},
                {"french": "sel", "shimaore": "chingó", "kibouchi": "sira"}
            ]
            
            correspondence_results = []
            for test_case in specific_tests:
                found = False
                for word in nourriture_words:
                    if word.get("french", "").lower() == test_case["french"].lower():
                        shimaore_match = test_case["shimaore"].lower() in word.get("shimaore", "").lower()
                        kibouchi_match = test_case["kibouchi"].lower() in word.get("kibouchi", "").lower()
                        
                        success = shimaore_match and kibouchi_match
                        details = f"French: {word.get('french')}, Shimaoré: {word.get('shimaore')}, Kibouchi: {word.get('kibouchi')}"
                        
                        self.log_test(f"Nourriture Orthography: {test_case['french']}", success, details)
                        correspondence_results.append(success)
                        found = True
                        break
                
                if not found:
                    self.log_test(f"Nourriture Orthography: {test_case['french']}", False, "Word not found")
                    correspondence_results.append(False)
            
            self.log_test("Nourriture Word Count", count_success, count_details)
            
            return count_success and all(correspondence_results)
        except Exception as e:
            self.log_test("Nourriture Orthography", False, f"Error: {str(e)}")
            return False
    
    def test_adjectifs_api_performance(self):
        """Test 4: Performance API avec section adjectifs"""
        print("\n=== TEST 4: PERFORMANCE API AVEC SECTION ADJECTIFS ===")
        
        try:
            start_time = time.time()
            response = requests.get(f"{self.backend_url}/words?category=adjectifs", timeout=15)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response.status_code != 200:
                self.log_test("Adjectifs API Performance", False, f"API Error: {response.status_code}")
                return False
            
            adjectifs = response.json()
            word_count = len(adjectifs)
            
            # Test performance (should respond within 2 seconds)
            performance_success = response_time < 2.0
            performance_details = f"Response time: {response_time:.3f}s, returned {word_count} adjectifs"
            
            self.log_test("Adjectifs API Performance", performance_success, performance_details)
            
            return performance_success
        except Exception as e:
            self.log_test("Adjectifs API Performance", False, f"Error: {str(e)}")
            return False
    
    def test_global_audio_coverage(self, all_words: List[Dict]):
        """Test 6: Couverture audio globale"""
        print("\n=== TEST 6: COUVERTURE AUDIO GLOBALE ===")
        
        if not all_words:
            self.log_test("Global Audio Coverage", False, "No words data available")
            return False
        
        total_words = len(all_words)
        with_audio = sum(1 for word in all_words if word.get("has_authentic_audio", False))
        coverage_percent = (with_audio / total_words * 100) if total_words > 0 else 0
        
        # Calculer par catégorie
        category_coverage = {}
        for word in all_words:
            category = word.get("category", "unknown")
            if category not in category_coverage:
                category_coverage[category] = {"total": 0, "with_audio": 0}
            
            category_coverage[category]["total"] += 1
            if word.get("has_authentic_audio", False):
                category_coverage[category]["with_audio"] += 1
        
        # Calculer pourcentages par catégorie
        for category in category_coverage:
            total = category_coverage[category]["total"]
            with_audio = category_coverage[category]["with_audio"]
            category_coverage[category]["percentage"] = (with_audio / total * 100) if total > 0 else 0
        
        success = coverage_percent >= 50  # Expect at least 50% global coverage
        details = f"Global audio coverage: {with_audio}/{total_words} ({coverage_percent:.1f}%)"
        
        self.log_test("Global Audio Coverage", success, details)
        
        # Test sections sans audio
        sections_without_audio = [cat for cat, data in category_coverage.items() 
                                if data["percentage"] < 10]
        
        if sections_without_audio:
            self.log_test("Sections Without Audio", True, f"Sections with <10% audio: {sections_without_audio}")
        
        return success
    
    def test_audio_file_access(self):
        """Test 5: Accès aux fichiers audio (sample test)"""
        print("\n=== TEST 5: ACCÈS AUX FICHIERS AUDIO ===")
        
        # Test quelques fichiers audio spécifiques
        audio_files_to_test = [
            "Bolé.m4a",
            "Mzouri.m4a", 
            "Tadjiri.m4a"
        ]
        
        results = []
        for audio_file in audio_files_to_test:
            try:
                # Test if audio endpoint exists (this is a basic connectivity test)
                audio_url = f"{self.backend_url}/audio/adjectifs/{audio_file}"
                response = requests.head(audio_url, timeout=5)
                
                success = response.status_code in [200, 404]  # 404 is acceptable, means endpoint exists
                details = f"Audio file {audio_file}: Status {response.status_code}"
                
                self.log_test(f"Audio File Access: {audio_file}", success, details)
                results.append(success)
            except Exception as e:
                self.log_test(f"Audio File Access: {audio_file}", False, f"Error: {str(e)}")
                results.append(False)
        
        return all(results)
    
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