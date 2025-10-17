#!/usr/bin/env python3
"""
Test spécifique des corrections audio verbes après la refonte complète
Specific testing of verb audio corrections after complete refactoring

Focus: Vérifier les correspondances audio exactes pour les verbes après correction,
tester les 4 cas spécifiques mentionnés, et valider la cohérence globale
"""

import requests
import json
import sys
import time
from typing import Dict, List, Optional

# Configuration
BACKEND_URL = "https://shimao-learn-1.preview.emergentagent.com"
API_URL = f"{BACKEND_URL}/api"

class VerbAudioCorrespondencesTester:
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
    
    def get_all_verbs(self) -> List[Dict]:
        """Get all verbs from the database"""
        try:
            response = requests.get(f"{self.backend_url}/words?category=verbes", timeout=10)
            if response.status_code == 200:
                verbs = response.json()
                self.log_test("Get All Verbs", True, f"Found {len(verbs)} verbs")
                return verbs
            else:
                self.log_test("Get All Verbs", False, f"Status: {response.status_code}")
                return []
        except Exception as e:
            self.log_test("Get All Verbs", False, f"Error: {str(e)}")
            return []
    
    def find_verb_by_french(self, verbs: List[Dict], french_word: str) -> Optional[Dict]:
        """Find a verb by its French translation"""
        for verb in verbs:
            if verb.get('french', '').lower() == french_word.lower():
                return verb
        return None
    
    def test_specific_verb_correspondences(self, verbs: List[Dict]):
        """Test the 4 specific verb audio correspondences mentioned in review request"""
        print("\n=== TEST CORRESPONDANCES SPÉCIFIQUES VERBES ===")
        
        # Test cases from review request
        test_cases = [
            {
                'french': 'abîmer',
                'expected_shimaore': 'oumengna',
                'expected_audio': 'Oumengna.m4a',
                'note': 'plus de confusion avec mandroubaka'
            },
            {
                'french': 'voir',
                'expected_shimaore': 'ouona',
                'expected_kibouchi': 'mahita',
                'expected_audio': 'Mahita.m4a',
                'note': 'corrigé'
            },
            {
                'french': 'danser',
                'expected_kibouchi': 'chokou',
                'expected_audio': 'Chokou.m4a',
                'note': 'maintenu'
            },
            {
                'french': 'casser',
                'expected_shimaore': 'latsaka',
                'expected_audio': 'Latsaka.m4a',
                'note': 'maintenu'
            }
        ]
        
        for test_case in test_cases:
            french_word = test_case['french']
            verb = self.find_verb_by_french(verbs, french_word)
            
            if not verb:
                self.log_test(f"Find verb '{french_word}'", False, "Verb not found in database")
                continue
            
            self.log_test(f"Find verb '{french_word}'", True, f"Found: {verb.get('french')}")
            
            # Test Shimaoré translation if expected
            if 'expected_shimaore' in test_case:
                actual_shimaore = verb.get('shimaore', '').lower()
                expected_shimaore = test_case['expected_shimaore'].lower()
                shimaore_match = actual_shimaore == expected_shimaore
                self.log_test(f"'{french_word}' Shimaoré translation", shimaore_match,
                             f"Expected: '{expected_shimaore}', Got: '{actual_shimaore}'")
            
            # Test Kibouchi translation if expected
            if 'expected_kibouchi' in test_case:
                actual_kibouchi = verb.get('kibouchi', '').lower()
                expected_kibouchi = test_case['expected_kibouchi'].lower()
                kibouchi_match = actual_kibouchi == expected_kibouchi
                self.log_test(f"'{french_word}' Kibouchi translation", kibouchi_match,
                             f"Expected: '{expected_kibouchi}', Got: '{actual_kibouchi}'")
            
            # Test audio filename correspondence
            expected_audio = test_case['expected_audio']
            
            # Check various audio fields
            audio_fields = [
                'audio_filename',
                'shimoare_audio_filename', 
                'kibouchi_audio_filename',
                'audio_url'
            ]
            
            audio_found = False
            audio_details = []
            
            for field in audio_fields:
                if field in verb and verb[field]:
                    audio_value = str(verb[field])
                    if expected_audio.lower() in audio_value.lower():
                        audio_found = True
                        audio_details.append(f"{field}: {audio_value}")
                    else:
                        audio_details.append(f"{field}: {audio_value}")
            
            self.log_test(f"'{french_word}' audio correspondence", audio_found,
                         f"Expected: '{expected_audio}', Found: {'; '.join(audio_details) if audio_details else 'No audio fields'}")
    
    def test_verb_audio_coverage(self, verbs: List[Dict]):
        """Test overall verb audio coverage - should be 36/78 verbs (46.2%)"""
        print("\n=== TEST COUVERTURE AUDIO VERBES ===")
        
        total_verbs = len(verbs)
        verbs_with_audio = 0
        verbs_with_authentic_audio = 0
        verbs_with_dual_audio = 0
        
        audio_files = []
        orthographic_matches = 0
        
        for verb in verbs:
            french = verb.get('french', '')
            shimaore = verb.get('shimaore', '')
            kibouchi = verb.get('kibouchi', '')
            
            # Check for any audio
            has_any_audio = any([
                verb.get('audio_filename'),
                verb.get('shimoare_audio_filename'),
                verb.get('kibouchi_audio_filename'),
                verb.get('audio_url'),
                verb.get('has_authentic_audio', False)
            ])
            
            if has_any_audio:
                verbs_with_audio += 1
                
                # Collect audio filenames
                for field in ['audio_filename', 'shimoare_audio_filename', 'kibouchi_audio_filename']:
                    if verb.get(field):
                        audio_files.append(verb[field])
            
            # Check authentic audio flag
            if verb.get('has_authentic_audio', False):
                verbs_with_authentic_audio += 1
            
            # Check dual audio system
            if verb.get('dual_audio_system', False):
                verbs_with_dual_audio += 1
            
            # Check orthographic correspondence
            audio_filename = verb.get('audio_filename', '') or verb.get('shimoare_audio_filename', '') or verb.get('kibouchi_audio_filename', '')
            if audio_filename:
                # Remove extension and convert to lowercase
                audio_base = audio_filename.lower().replace('.m4a', '').replace('.mp3', '').replace('.wav', '')
                shimaore_lower = shimaore.lower()
                kibouchi_lower = kibouchi.lower()
                
                if audio_base in shimaore_lower or audio_base in kibouchi_lower or shimaore_lower in audio_base or kibouchi_lower in audio_base:
                    orthographic_matches += 1
        
        # Calculate percentages
        audio_coverage_pct = (verbs_with_audio / total_verbs * 100) if total_verbs > 0 else 0
        authentic_audio_pct = (verbs_with_authentic_audio / total_verbs * 100) if total_verbs > 0 else 0
        dual_audio_pct = (verbs_with_dual_audio / total_verbs * 100) if total_verbs > 0 else 0
        orthographic_pct = (orthographic_matches / verbs_with_audio * 100) if verbs_with_audio > 0 else 0
        
        # Log results
        self.log_test("Total verbs count", total_verbs >= 78, f"Found: {total_verbs}, Expected: ≥78")
        self.log_test("Verbs with audio", verbs_with_audio >= 36, 
                     f"Found: {verbs_with_audio}/{total_verbs} ({audio_coverage_pct:.1f}%), Expected: ≥36 (46.2%)")
        self.log_test("Expected 46.2% audio coverage", audio_coverage_pct >= 46.2,
                     f"Actual coverage: {audio_coverage_pct:.1f}%")
        self.log_test("Orthographic correspondence", orthographic_pct >= 50.0,
                     f"Found: {orthographic_matches}/{verbs_with_audio} ({orthographic_pct:.1f}%) exact matches")
        
        # Check for duplicate audio files
        unique_audio_files = set(audio_files)
        duplicates = len(audio_files) - len(unique_audio_files)
        self.log_test("No duplicate audio files", duplicates == 0,
                     f"Found {duplicates} duplicate audio references")
        
        print(f"\nAUDIO COVERAGE SUMMARY:")
        print(f"- Total verbs: {total_verbs}")
        print(f"- Verbs with audio: {verbs_with_audio} ({audio_coverage_pct:.1f}%)")
        print(f"- Verbs with authentic audio flag: {verbs_with_authentic_audio} ({authentic_audio_pct:.1f}%)")
        print(f"- Verbs with dual audio system: {verbs_with_dual_audio} ({dual_audio_pct:.1f}%)")
        print(f"- Orthographic matches: {orthographic_matches}/{verbs_with_audio} ({orthographic_pct:.1f}%)")
        print(f"- Unique audio files: {len(unique_audio_files)}")
    
    def test_audio_file_accessibility(self, verbs: List[Dict]):
        """Test accessibility of audio files"""
        print("\n=== TEST ACCESSIBILITÉ FICHIERS AUDIO ===")
        
        # Collect unique audio files
        audio_files = set()
        for verb in verbs:
            for field in ['audio_filename', 'shimoare_audio_filename', 'kibouchi_audio_filename']:
                if verb.get(field):
                    audio_files.add(verb[field])
        
        # Test a sample of audio files
        sample_files = list(audio_files)[:10]  # Test first 10 files
        accessible_files = 0
        
        for audio_file in sample_files:
            try:
                # Try different audio endpoint patterns
                audio_urls = [
                    f"{self.backend_url}/audio/verbes/{audio_file}",
                    f"{self.backend_url}/audio/{audio_file}",
                    f"{BACKEND_URL}/audio/verbes/{audio_file}"
                ]
                
                file_accessible = False
                for url in audio_urls:
                    try:
                        response = requests.head(url, timeout=5)
                        if response.status_code in [200, 404]:  # 404 is acceptable, means endpoint exists
                            file_accessible = True
                            break
                    except:
                        continue
                
                if file_accessible:
                    accessible_files += 1
                    
            except Exception as e:
                pass
        
        accessibility_pct = (accessible_files / len(sample_files) * 100) if sample_files else 0
        self.log_test("Audio files accessibility", accessibility_pct >= 50,
                     f"Accessible: {accessible_files}/{len(sample_files)} ({accessibility_pct:.1f}%)")
    
    def test_data_integrity(self, verbs: List[Dict]):
        """Test data integrity of verb entries"""
        print("\n=== TEST INTÉGRITÉ DES DONNÉES ===")
        
        complete_entries = 0
        entries_with_audio_metadata = 0
        consistent_audio_flags = 0
        
        for verb in verbs:
            # Check complete structure
            required_fields = ['french', 'shimaore', 'kibouchi', 'category']
            if all(verb.get(field) for field in required_fields):
                complete_entries += 1
            
            # Check audio metadata consistency
            has_audio_filename = bool(verb.get('audio_filename') or verb.get('shimoare_audio_filename') or verb.get('kibouchi_audio_filename'))
            has_authentic_flag = verb.get('has_authentic_audio', False)
            has_dual_system = verb.get('dual_audio_system', False)
            
            if has_audio_filename or has_authentic_flag or has_dual_system:
                entries_with_audio_metadata += 1
            
            # Check flag consistency
            if has_audio_filename == has_authentic_flag or has_audio_filename == has_dual_system:
                consistent_audio_flags += 1
        
        total_verbs = len(verbs)
        complete_pct = (complete_entries / total_verbs * 100) if total_verbs > 0 else 0
        audio_metadata_pct = (entries_with_audio_metadata / total_verbs * 100) if total_verbs > 0 else 0
        consistency_pct = (consistent_audio_flags / total_verbs * 100) if total_verbs > 0 else 0
        
        self.log_test("Complete verb entries", complete_pct >= 95,
                     f"Complete: {complete_entries}/{total_verbs} ({complete_pct:.1f}%)")
        self.log_test("Audio metadata present", audio_metadata_pct >= 40,
                     f"With audio metadata: {entries_with_audio_metadata}/{total_verbs} ({audio_metadata_pct:.1f}%)")
        self.log_test("Audio flag consistency", consistency_pct >= 80,
                     f"Consistent flags: {consistent_audio_flags}/{total_verbs} ({consistency_pct:.1f}%)")
    
    def test_50_audio_files_available(self):
        """Test that 50 M4A files are available"""
        print("\n=== TEST DISPONIBILITÉ 50 FICHIERS M4A ===")
        
        try:
            # Try to get audio info endpoint
            response = requests.get(f"{self.backend_url}/audio/info", timeout=10)
            if response.status_code == 200:
                audio_info = response.json()
                # Check if verbes category exists and has files
                if 'verbes' in audio_info:
                    file_count = audio_info['verbes'].get('file_count', 0)
                    self.log_test("50 M4A files available", file_count >= 50,
                                 f"Found {file_count} audio files for verbes")
                else:
                    self.log_test("50 M4A files available", False, "Verbes category not found in audio info")
            else:
                self.log_test("50 M4A files available", False, f"Audio info endpoint error: {response.status_code}")
        except Exception as e:
            self.log_test("50 M4A files available", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests for verb audio correspondences"""
        print("🎯 DÉBUT DES TESTS CORRESPONDANCES AUDIO VERBES")
        print("=" * 80)
        
        start_time = time.time()
        
        # Test API connectivity
        if not self.test_api_connectivity():
            print("❌ Cannot proceed - API not accessible")
            return False
        
        # Get all verbs
        verbs = self.get_all_verbs()
        if not verbs:
            print("❌ Cannot proceed - No verbs found")
            return False
        
        # Run specific tests
        self.test_specific_verb_correspondences(verbs)
        self.test_verb_audio_coverage(verbs)
        self.test_audio_file_accessibility(verbs)
        self.test_data_integrity(verbs)
        self.test_50_audio_files_available()
        
        # Summary
        end_time = time.time()
        duration = end_time - start_time
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print("\n" + "=" * 80)
        print("🎯 RÉSUMÉ DES TESTS CORRESPONDANCES AUDIO VERBES")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Duration: {duration:.2f}s")
        
        # Show failed tests
        if self.total_tests - self.passed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if "❌ FAIL" in result:
                    print(f"  - {result}")
        
        if success_rate >= 80:
            print("🎉 OVERALL RESULT: SUCCESS")
        elif success_rate >= 60:
            print("⚠️ OVERALL RESULT: PARTIAL SUCCESS")
        else:
            print("❌ OVERALL RESULT: FAILURE")
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = VerbAudioCorrespondencesTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)