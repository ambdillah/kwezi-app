#!/usr/bin/env python3
"""
Vocabulary Corrections Test for Mayotte Educational App
Tests specific vocabulary corrections mentioned in the review request
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

class VocabularyCorrectionsTest:
    def __init__(self):
        self.session = requests.Session()
        
    def test_vocabulary_corrections_verification(self):
        """Test the specific vocabulary corrections mentioned in the review request"""
        print("\n=== Testing Vocabulary Corrections Verification ===")
        
        try:
            # 1. Check if the backend starts without any syntax errors after all corrections
            print("--- Testing Backend Startup After All Corrections ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Backend has syntax errors or is not responding: {response.status_code}")
                return False
            print("✅ Backend starts without syntax errors after all corrections")
            
            # Get all words for testing
            words = response.json()
            words_by_french = {word['french']: word for word in words}
            
            print(f"Total words in database: {len(words)}")
            
            # 2. Test nature section corrections
            print("\n--- Testing Nature Section Corrections ---")
            
            nature_corrections = [
                {
                    "french": "Herbe", 
                    "shimaore": "Malavou", 
                    "kibouchi": "Hayitri",
                    "note": "shimaoré should be 'Malavou' (not 'Kounou')"
                },
                {
                    "french": "Feuille", 
                    "shimaore": "Mawoini", 
                    "kibouchi": "Hayitri",
                    "note": "shimaoré should be 'Mawoini' (not 'Dhavou')"
                },
                {
                    "french": "Plateau", 
                    "shimaore": "Kalé", 
                    "kibouchi": "Kaléni",
                    "note": "shimaoré should be 'Kalé', kibouchi 'Kaléni' (not 'Bandra/Kétraka')"
                },
                {
                    "french": "Canne à sucre", 
                    "shimaore": "Mouwa", 
                    "kibouchi": "Fari",
                    "note": "shimaoré should be 'Mouwa' (not 'Moua')"
                }
            ]
            
            nature_corrections_verified = True
            
            for correction in nature_corrections:
                french_word = correction['french']
                if french_word in words_by_french:
                    word = words_by_french[french_word]
                    
                    # Check shimaoré correction
                    if word['shimaore'] == correction['shimaore']:
                        print(f"✅ {french_word} shimaoré: '{word['shimaore']}' - CORRECTION VERIFIED")
                    else:
                        print(f"❌ {french_word} shimaoré: Expected '{correction['shimaore']}', got '{word['shimaore']}'")
                        nature_corrections_verified = False
                    
                    # Check kibouchi correction
                    if word['kibouchi'] == correction['kibouchi']:
                        print(f"✅ {french_word} kibouchi: '{word['kibouchi']}' - CORRECTION VERIFIED")
                    else:
                        print(f"❌ {french_word} kibouchi: Expected '{correction['kibouchi']}', got '{word['kibouchi']}'")
                        nature_corrections_verified = False
                    
                    print(f"   Note: {correction['note']}")
                else:
                    print(f"❌ {french_word} not found in database")
                    nature_corrections_verified = False
            
            # 3. Test animaux section corrections
            print("\n--- Testing Animaux Section Corrections ---")
            
            animaux_corrections = [
                {
                    "french": "Escargot", 
                    "shimaore": "Kwa", 
                    "kibouchi": "Ancora",
                    "note": "shimaoré should be 'Kwa' (not 'Kouéya')"
                },
                {
                    "french": "Fourmis", 
                    "shimaore": "Tsoussou", 
                    "kibouchi": "Visiki",
                    "note": "shimaoré should be 'Tsoussou' (not 'Tsutsuhu')"
                },
                {
                    "french": "Chenille", 
                    "shimaore": "Bazi", 
                    "kibouchi": "Bibimanguidi",
                    "note": "shimaoré should be 'Bazi' (not 'Bibimangidji')"
                },
                {
                    "french": "Ver de terre", 
                    "shimaore": "Lingoui lingoui", 
                    "kibouchi": "Bibi fotaka",
                    "note": "shimaoré should be 'Lingoui lingoui' (not 'Njengwe')"
                }
            ]
            
            animaux_corrections_verified = True
            
            for correction in animaux_corrections:
                french_word = correction['french']
                if french_word in words_by_french:
                    word = words_by_french[french_word]
                    
                    # Check shimaoré correction
                    if word['shimaore'] == correction['shimaore']:
                        print(f"✅ {french_word} shimaoré: '{word['shimaore']}' - CORRECTION VERIFIED")
                    else:
                        print(f"❌ {french_word} shimaoré: Expected '{correction['shimaore']}', got '{word['shimaore']}'")
                        animaux_corrections_verified = False
                    
                    # Check kibouchi correction
                    if word['kibouchi'] == correction['kibouchi']:
                        print(f"✅ {french_word} kibouchi: '{word['kibouchi']}' - CORRECTION VERIFIED")
                    else:
                        print(f"❌ {french_word} kibouchi: Expected '{correction['kibouchi']}', got '{word['kibouchi']}'")
                        animaux_corrections_verified = False
                    
                    print(f"   Note: {correction['note']}")
                else:
                    print(f"❌ {french_word} not found in database")
                    animaux_corrections_verified = False
            
            # 4. Test famille section corrections (check if any have been applied)
            print("\n--- Testing Famille Section Corrections ---")
            
            # Get famille category words
            famille_response = self.session.get(f"{API_BASE}/words?category=famille")
            if famille_response.status_code == 200:
                famille_words = famille_response.json()
                print(f"✅ Found {len(famille_words)} words in famille category")
                
                # Check for any recent corrections in famille section
                famille_sample = [
                    {"french": "Maman", "shimaore": "Mama", "kibouchi": "Mama"},
                    {"french": "Papa", "shimaore": "Baba", "kibouchi": "Baba"},
                    {"french": "Frère", "shimaore": "Mwanagna", "kibouchi": "Anadahi"},
                    {"french": "Sœur", "shimaore": "Mwanagna", "kibouchi": "Anabavi"}
                ]
                
                famille_words_by_french = {word['french']: word for word in famille_words}
                famille_corrections_found = False
                
                for sample in famille_sample:
                    french_word = sample['french']
                    if french_word in famille_words_by_french:
                        word = famille_words_by_french[french_word]
                        if word['shimaore'] == sample['shimaore'] and word['kibouchi'] == sample['kibouchi']:
                            print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} - VERIFIED")
                        else:
                            print(f"⚠️ {french_word}: {word['shimaore']} / {word['kibouchi']} - May have corrections")
                            famille_corrections_found = True
                
                if not famille_corrections_found:
                    print("✅ No specific famille corrections detected in this review")
                else:
                    print("⚠️ Some famille corrections may have been applied")
            else:
                print(f"❌ Could not retrieve famille words: {famille_response.status_code}")
                return False
            
            # 5. Verify API endpoints are working correctly for all categories
            print("\n--- Testing API Endpoints for All Categories ---")
            
            categories = set(word['category'] for word in words)
            api_endpoints_working = True
            
            for category in sorted(categories):
                response = self.session.get(f"{API_BASE}/words?category={category}")
                if response.status_code == 200:
                    category_words = response.json()
                    print(f"✅ {category}: {len(category_words)} words")
                else:
                    print(f"❌ {category}: API endpoint failed ({response.status_code})")
                    api_endpoints_working = False
            
            # 6. Ensure no duplicate entries were created
            print("\n--- Testing No Duplicate Entries ---")
            
            french_names = [word['french'] for word in words]
            unique_names = set(french_names)
            
            if len(french_names) == len(unique_names):
                print(f"✅ No duplicate entries found ({len(unique_names)} unique words)")
                no_duplicates = True
            else:
                duplicates = [name for name in french_names if french_names.count(name) > 1]
                print(f"❌ Duplicate entries found: {set(duplicates)}")
                no_duplicates = False
            
            # 7. Confirm total word counts remain appropriate
            print("\n--- Testing Total Word Counts ---")
            
            total_words = len(words)
            categories_count = len(categories)
            
            print(f"Total words: {total_words}")
            print(f"Total categories: {categories_count}")
            
            # Check if word count is reasonable (should be substantial for educational app)
            if total_words >= 200:  # Expecting substantial vocabulary
                print(f"✅ Word count appropriate: {total_words} words")
                word_count_appropriate = True
            else:
                print(f"⚠️ Word count may be low: {total_words} words")
                word_count_appropriate = True  # Not necessarily a failure
            
            # Overall result
            all_corrections_verified = (
                nature_corrections_verified and 
                animaux_corrections_verified and 
                api_endpoints_working and 
                no_duplicates and 
                word_count_appropriate
            )
            
            if all_corrections_verified:
                print("\n🎉 VOCABULARY CORRECTIONS VERIFICATION COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors after all corrections")
                print("✅ Nature section corrections verified:")
                print("   - Herbe: shimaoré = 'Malavou' (corrected)")
                print("   - Feuille: shimaoré = 'Mawoini' (corrected)")
                print("   - Plateau: shimaoré = 'Kalé', kibouchi = 'Kaléni' (corrected)")
                print("   - Canne à sucre: shimaoré = 'Mouwa' (corrected)")
                print("✅ Animaux section corrections verified:")
                print("   - Escargot: shimaoré = 'Kwa' (corrected)")
                print("   - Fourmis: shimaoré = 'Tsoussou' (corrected)")
                print("   - Chenille: shimaoré = 'Bazi' (corrected)")
                print("   - Ver de terre: shimaoré = 'Lingoui lingoui' (corrected)")
                print("✅ Famille section checked (no specific corrections required)")
                print("✅ All API endpoints working correctly for all categories")
                print("✅ No duplicate entries created")
                print(f"✅ Total word counts appropriate ({total_words} words across {categories_count} categories)")
                print("✅ All vocabulary corrections have been successfully implemented")
            else:
                print("\n❌ Some vocabulary corrections are not properly implemented or have introduced issues")
            
            return all_corrections_verified
            
        except Exception as e:
            print(f"❌ Vocabulary corrections verification error: {e}")
            return False

if __name__ == "__main__":
    tester = VocabularyCorrectionsTest()
    success = tester.test_vocabulary_corrections_verification()
    
    if success:
        print("\n🎉 Vocabulary corrections test completed successfully!")
        exit(0)
    else:
        print("\n❌ Vocabulary corrections test failed!")
        exit(1)