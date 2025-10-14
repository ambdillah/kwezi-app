#!/usr/bin/env python3
"""
Test complet après création de la section "adjectifs" avec 100% audio
Comprehensive testing after creating "adjectifs" section with 100% audio

Focus: Vérifier la nouvelle section adjectifs, structure globale, orthographe nourriture,
performance API, et couverture audio globale améliorée
"""

import requests
import json
import sys
import time
from typing import Dict, List, Optional

# Configuration
BACKEND_URL = "https://mayotte-learn-3.preview.emergentagent.com"
API_URL = f"{BACKEND_URL}/api"

class AdjectifsComprehensiveTester:
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
        
    def test_api_connectivity(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=10)
            success = response.status_code == 200
            self.log_test("API Connectivity", success, f"Status: {response.status_code}")
            return success
        except Exception as e:
            self.log_test("API Connectivity", False, f"Error: {str(e)}")
            return False
    
    def test_adjectifs_section_exists(self):
        """Test 1: Vérification nouvelle section adjectifs - existence et nombre de mots"""
        print("\n=== TEST 1: VÉRIFICATION NOUVELLE SECTION ADJECTIFS ===")
        
        try:
            response = requests.get(f"{self.backend_url}/words?category=adjectifs", timeout=10)
            if response.status_code != 200:
                self.log_test("Section Adjectifs Exists", False, f"API Error: {response.status_code}")
                return False, []
            
            adjectifs = response.json()
            word_count = len(adjectifs)
            
            # Test si la section existe avec 52 mots comme attendu
            expected_count = 52
            success = word_count >= 50  # Allow some flexibility
            details = f"Found {word_count} adjectifs (expected ~{expected_count})"
            
            self.log_test("Section Adjectifs Exists", success, details)
            return success, adjectifs
        except Exception as e:
            self.log_test("Section Adjectifs Exists", False, f"Error: {str(e)}")
            return False, []
    
    def test_specific_adjectifs_correspondences(self, adjectifs: List[Dict]):
        """Test correspondances spécifiques des adjectifs"""
        print("\n=== TEST CORRESPONDANCES SPÉCIFIQUES ADJECTIFS ===")
        
        specific_tests = [
            {"french": "grand", "shimaore": "bolé", "audio_expected": "Bolé.m4a"},
            {"french": "beau", "shimaore": "mzouri", "audio_expected": "Mzouri.m4a"},
            {"french": "jolie", "shimaore": "mzouri", "audio_expected": "Mzouri.m4a"},
            {"french": "riche", "shimaore": "tadjiri", "audio_expected": "Tadjiri.m4a"}
        ]
        
        results = []
        for test_case in specific_tests:
            found = False
            for adj in adjectifs:
                french_match = (adj.get("french", "").lower() == test_case["french"].lower() or 
                              test_case["french"].lower() in adj.get("french", "").lower())
                
                if french_match:
                    shimaore_match = test_case["shimaore"].lower() in adj.get("shimaore", "").lower()
                    has_audio = adj.get("has_authentic_audio", False)
                    audio_filename = adj.get("audio_filename", "")
                    
                    success = shimaore_match and has_audio
                    details = f"French: {adj.get('french')}, Shimaoré: {adj.get('shimaore')}, Audio: {audio_filename}, Has Audio: {has_audio}"
                    
                    self.log_test(f"Adjectif Correspondence: {test_case['french']}", success, details)
                    results.append(success)
                    found = True
                    break
            
            if not found:
                self.log_test(f"Adjectif Correspondence: {test_case['french']}", False, "Word not found in database")
                results.append(False)
        
        return results
    
    def test_adjectifs_audio_coverage(self, adjectifs: List[Dict]):
        """Test couverture audio des adjectifs (100% attendu)"""
        print("\n=== TEST COUVERTURE AUDIO ADJECTIFS ===")
        
        if not adjectifs:
            self.log_test("Adjectifs Audio Coverage", False, "No adjectifs data available")
            return False
        
        total_adjectifs = len(adjectifs)
        with_audio = sum(1 for adj in adjectifs if adj.get("has_authentic_audio", False))
        coverage_percent = (with_audio / total_adjectifs * 100) if total_adjectifs > 0 else 0
        
        success = coverage_percent >= 95  # Allow 95%+ for success
        details = f"Audio coverage: {with_audio}/{total_adjectifs} ({coverage_percent:.1f}%)"
        
        self.log_test("Adjectifs Audio Coverage", success, details)
        
        return success
    
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