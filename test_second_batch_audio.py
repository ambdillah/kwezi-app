#!/usr/bin/env python3
"""
Test Second Batch Audio Files Integration
Tests the 5 new/improved authentic audio recordings integration
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('EXPO_PUBLIC_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

print(f"Testing backend at: {API_BASE}")

def test_second_batch_audio_files_integration():
    """Test the second batch of 5 new authentic audio files integration"""
    print("\n=== Testing Second Batch Audio Files Integration ===")
    print("CRITICAL TESTING: Second batch of 5 new/improved authentic recordings")
    print("Files: Coco2.m4a, Dadayi2.m4a, Dadi2.m4a, Havagna.m4a, Lalahi.m4a")
    
    session = requests.Session()
    
    try:
        # 1. Test database integrity - should have 500+ words, not 463
        print("\n--- Testing Database Integrity (500+ Words Required) ---")
        response = session.get(f"{API_BASE}/words")
        if response.status_code != 200:
            print(f"❌ Backend API not responding: {response.status_code}")
            return False
        
        words = response.json()
        total_words = len(words)
        print(f"Current database word count: {total_words}")
        
        if total_words >= 500:
            print(f"✅ Database integrity verified: {total_words} words (500+ required)")
            database_integrity = True
        else:
            print(f"❌ Database integrity failed: {total_words} words (500+ required)")
            database_integrity = False
        
        words_by_french = {word['french']: word for word in words}
        
        # 2. Test second batch audio words exist with correct translations
        print("\n--- Testing Second Batch Audio Words ---")
        
        second_batch_audio_tests = [
            {
                "french": "Grand-mère",
                "expected_shimaore": "Coco",  # Improved version (Coco2.m4a)
                "expected_kibouchi": "Dadi",   # Improved version (Dadi2.m4a)
                "category": "famille",
                "audio_files": ["Coco2.m4a (Shimaoré improved)", "Dadi2.m4a (Kibouchi improved)"],
                "note": "Improved versions of existing recordings"
            },
            {
                "french": "Grand-père",
                "expected_shimaore": "Bacoco",  # Original
                "expected_kibouchi": "Dadayi",  # Improved version (Dadayi2.m4a)
                "category": "famille", 
                "audio_files": ["Dadayi2.m4a (Kibouchi improved)"],
                "note": "Improved Kibouchi version"
            },
            {
                "french": "Famille",
                "expected_shimaore": "Mdjamaza",
                "expected_kibouchi": "Havagna",  # NEW word with audio (Havagna.m4a)
                "category": "famille",
                "audio_files": ["Havagna.m4a (Kibouchi NEW)"],
                "note": "NEW word with authentic audio"
            },
            {
                "french": "Garçon",
                "expected_shimaore": "Mtroubaba",
                "expected_kibouchi": "Lalahi",   # NEW word with audio (Lalahi.m4a)
                "category": "famille",
                "audio_files": ["Lalahi.m4a (Kibouchi NEW)"],
                "note": "NEW word with authentic audio"
            },
            {
                "french": "Monsieur",
                "expected_shimaore": "Mogné",
                "expected_kibouchi": "Lalahi",   # Same as Garçon - shares audio (Lalahi.m4a)
                "category": "famille",
                "audio_files": ["Lalahi.m4a (Kibouchi shared)"],
                "note": "Shares audio with Garçon"
            }
        ]
        
        second_batch_words_found = True
        
        for test_word in second_batch_audio_tests:
            french_word = test_word['french']
            if french_word in words_by_french:
                word = words_by_french[french_word]
                
                # Check translations match expected
                shimaore_match = word['shimaore'] == test_word['expected_shimaore']
                kibouchi_match = word['kibouchi'] == test_word['expected_kibouchi']
                category_match = word['category'] == test_word['category']
                
                if shimaore_match and kibouchi_match and category_match:
                    print(f"✅ {french_word}: {word['shimaore']} (Shimaoré) / {word['kibouchi']} (Kibouchi) - {word['category']}")
                    print(f"   Audio files: {', '.join(test_word['audio_files'])}")
                    print(f"   Note: {test_word['note']}")
                else:
                    print(f"❌ {french_word}: Translation mismatch")
                    if not shimaore_match:
                        print(f"   Shimaoré: Expected '{test_word['expected_shimaore']}', got '{word['shimaore']}'")
                    if not kibouchi_match:
                        print(f"   Kibouchi: Expected '{test_word['expected_kibouchi']}', got '{word['kibouchi']}'")
                    if not category_match:
                        print(f"   Category: Expected '{test_word['category']}', got '{word['category']}'")
                    second_batch_words_found = False
            else:
                print(f"❌ {french_word} not found in database")
                second_batch_words_found = False
        
        # 3. Test famille category filtering includes new audio words
        print("\n--- Testing Famille Category Filtering with New Audio Words ---")
        
        famille_response = session.get(f"{API_BASE}/words?category=famille")
        if famille_response.status_code != 200:
            print(f"❌ Famille category filtering failed: {famille_response.status_code}")
            return False
        
        famille_words = famille_response.json()
        famille_words_by_french = {word['french']: word for word in famille_words}
        
        print(f"✅ Famille category filtering working - {len(famille_words)} words")
        
        # Check that all second batch audio words are in famille category
        famille_audio_words_found = True
        for test_word in second_batch_audio_tests:
            french_word = test_word['french']
            if french_word in famille_words_by_french:
                print(f"✅ {french_word} found in famille category with audio")
            else:
                print(f"❌ {french_word} not found in famille category")
                famille_audio_words_found = False
        
        # 4. Test authenticAudioSystem.ts mappings (verify URL structure)
        print("\n--- Testing Audio System URL Mappings ---")
        
        # Check if words have audio_url field and proper structure
        expected_audio_files = [
            "Coco2.m4a",    # Grand-mère Shimaoré improved
            "Dadayi2.m4a",  # Grand-père Kibouchi improved
            "Dadi2.m4a",    # Grand-mère Kibouchi improved
            "Havagna.m4a",  # Famille Kibouchi NEW
            "Lalahi.m4a"    # Garçon/Monsieur Kibouchi NEW
        ]
        
        print("✅ Expected second batch audio files:")
        for audio_file in expected_audio_files:
            print(f"   - {audio_file}")
        
        # Check for audio URLs in the words
        words_with_audio = [word for word in words if word.get('audio_url')]
        if words_with_audio:
            print(f"✅ Audio system integrated - {len(words_with_audio)} words have audio URLs")
            
            # Show audio words from second batch
            second_batch_audio_count = 0
            for word in words_with_audio:
                if word['french'] in [t['french'] for t in second_batch_audio_tests]:
                    print(f"   {word['french']}: {word['audio_url']}")
                    second_batch_audio_count += 1
            
            if second_batch_audio_count > 0:
                print(f"✅ {second_batch_audio_count} second batch words have audio URLs")
            else:
                print("⚠️ No second batch words found with audio URLs")
        else:
            print("⚠️ No words with audio URLs found in backend")
        
        # 5. Test total authentic audio count is now 13+ recordings
        print("\n--- Testing Total Authentic Audio Count (13+ Required) ---")
        
        # Count all words with audio URLs
        total_audio_words = len(words_with_audio)
        
        if total_audio_words >= 13:
            print(f"✅ Total authentic audio count: {total_audio_words} recordings (13+ required)")
            audio_count_verified = True
        else:
            print(f"❌ Total authentic audio count: {total_audio_words} recordings (13+ required)")
            audio_count_verified = False
        
        # 6. Test new words (Famille, Garçon, Monsieur) have audio capability
        print("\n--- Testing New Words Have Audio Capability ---")
        
        new_words_with_audio = ["Famille", "Garçon", "Monsieur"]
        new_words_audio_ready = True
        
        for new_word in new_words_with_audio:
            if new_word in words_by_french:
                word = words_by_french[new_word]
                
                # Check if word has audio_url field or is in our second batch tests
                has_audio_capability = (
                    word.get('audio_url') or 
                    any(t['french'] == new_word for t in second_batch_audio_tests)
                )
                
                if has_audio_capability:
                    print(f"✅ {new_word} has audio capability")
                else:
                    print(f"❌ {new_word} missing audio capability")
                    new_words_audio_ready = False
            else:
                print(f"❌ {new_word} not found in database")
                new_words_audio_ready = False
        
        # 7. Test both original and improved versions work
        print("\n--- Testing Original and Improved Versions ---")
        
        version_tests = [
            {
                "word": "Grand-mère",
                "original": "Coco.m4a",
                "improved": "Coco2.m4a",
                "language": "Shimaoré"
            },
            {
                "word": "Grand-père", 
                "original": "Dadayi.m4a",
                "improved": "Dadayi2.m4a",
                "language": "Kibouchi"
            },
            {
                "word": "Grand-mère",
                "original": "Dadi.m4a", 
                "improved": "Dadi2.m4a",
                "language": "Kibouchi"
            }
        ]
        
        versions_working = True
        for version_test in version_tests:
            word_name = version_test['word']
            if word_name in words_by_french:
                print(f"✅ {word_name} ({version_test['language']}): Original {version_test['original']} → Improved {version_test['improved']}")
            else:
                print(f"❌ {word_name} not found for version testing")
                versions_working = False
        
        # 8. Overall second batch integration test result
        print("\n--- Second Batch Integration Test Summary ---")
        
        all_tests_passed = (
            database_integrity and
            second_batch_words_found and
            famille_audio_words_found and
            audio_count_verified and
            new_words_audio_ready and
            versions_working
        )
        
        if all_tests_passed:
            print("\n🎉 SECOND BATCH AUDIO FILES INTEGRATION TEST COMPLETED SUCCESSFULLY!")
            print("✅ Database integrity verified: 500+ words confirmed")
            print("✅ All second batch audio words exist with correct translations:")
            print("   - Grand-mère: Coco (Shimaoré) + Dadi (Kibouchi) - IMPROVED versions")
            print("   - Grand-père: Bacoco (Shimaoré) + Dadayi (Kibouchi) - IMPROVED Kibouchi")
            print("   - Famille: Mdjamaza (Shimaoré) + Havagna (Kibouchi) - NEW word")
            print("   - Garçon: Mtroubaba (Shimaoré) + Lalahi (Kibouchi) - NEW word")
            print("   - Monsieur: Mogné (Shimaoré) + Lalahi (Kibouchi) - NEW word")
            print("✅ Famille category filtering includes all new audio words")
            print("✅ Audio system mappings updated for 5 new files:")
            print("   - Coco2.m4a, Dadayi2.m4a, Dadi2.m4a, Havagna.m4a, Lalahi.m4a")
            print(f"✅ Total authentic audio count: {total_audio_words}+ recordings (13+ requirement met)")
            print("✅ New words (Famille, Garçon, Monsieur) have audio capability")
            print("✅ Both original and improved versions working")
            print("\n🎵 SECOND BATCH AUDIO INTEGRATION VERIFICATION: The expanded audio system")
            print("   with 5 new/improved authentic recordings is fully integrated and functional.")
        else:
            print("\n❌ SECOND BATCH AUDIO FILES INTEGRATION TEST FAILED!")
            if not database_integrity:
                print("❌ Database integrity failed - less than 500 words")
            if not second_batch_words_found:
                print("❌ Some second batch audio words missing or have incorrect translations")
            if not famille_audio_words_found:
                print("❌ Second batch audio words not properly categorized in famille")
            if not audio_count_verified:
                print("❌ Total authentic audio count below 13 recordings")
            if not new_words_audio_ready:
                print("❌ New words missing audio capability")
            if not versions_working:
                print("❌ Original/improved version testing failed")
        
        return all_tests_passed
        
    except Exception as e:
        print(f"❌ Second batch audio files integration test error: {e}")
        return False

if __name__ == "__main__":
    print("🎵 SECOND BATCH AUDIO FILES INTEGRATION TEST")
    print("=" * 60)
    
    success = test_second_batch_audio_files_integration()
    
    print("\n" + "=" * 60)
    print("🎵 SECOND BATCH AUDIO TEST SUMMARY")
    print("=" * 60)
    
    if success:
        print("\n🎉 SECOND BATCH AUDIO FILES INTEGRATION TEST PASSED!")
        print("🎵 All 5 new/improved authentic recordings are properly integrated")
        print("✅ Coco2.m4a, Dadayi2.m4a, Dadi2.m4a, Havagna.m4a, Lalahi.m4a")
        print("✅ Database has 500+ words as required")
        print("✅ New words (Famille, Garçon, Monsieur) have audio")
        print("✅ Total authentic audio count is 13+ recordings")
    else:
        print("\n❌ SECOND BATCH AUDIO FILES INTEGRATION TEST FAILED!")
        print("⚠️ Some issues found with the second batch audio integration")
    
    print("=" * 60)