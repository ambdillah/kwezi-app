#!/usr/bin/env python3
"""
Tradition Vocabulary Test Suite for Mayotte Educational App
Tests the newly created tradition vocabulary section with all cultural elements from the tableau
"""

import requests
import json
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('EXPO_PUBLIC_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

print(f"Testing backend at: {API_BASE}")

class TraditionVocabularyTester:
    def __init__(self):
        self.session = requests.Session()
        
    def test_tradition_vocabulary_section(self):
        """Test the newly created tradition vocabulary section with all cultural elements from the tableau"""
        print("\n=== Testing Tradition Vocabulary Section ===")
        
        try:
            # 1. Test backend startup without errors after adding the new tradition section
            print("--- Testing Backend Startup After Adding Tradition Section ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Backend has syntax errors or is not responding: {response.status_code}")
                return False
            print("✅ Backend starts without syntax errors after adding tradition section")
            
            # 2. Test the new tradition category endpoint
            print("\n--- Testing /api/words?category=tradition Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=tradition")
            if response.status_code != 200:
                print(f"❌ Tradition endpoint failed: {response.status_code}")
                return False
            
            tradition_words = response.json()
            tradition_words_by_french = {word['french']: word for word in tradition_words}
            print(f"✅ /api/words?category=tradition working correctly ({len(tradition_words)} tradition elements)")
            
            # 3. Verify all 16 tradition elements from the tableau are present
            print("\n--- Testing All 16 Tradition Elements from Tableau ---")
            
            # Expected tradition elements from the review request
            expected_tradition_elements = [
                {"french": "Mariage", "shimaore": "Haroussi", "kibouchi": "Haroussi", "difficulty": 1},
                {"french": "Chant mariage traditionnel", "shimaore": "Mlélézi", "kibouchi": "Mlélézi", "difficulty": 2},
                {"french": "Petit mariage", "shimaore": "Mafounguidzo", "kibouchi": "Mafounguidzo", "difficulty": 2},
                {"french": "Grand mariage", "shimaore": "Manzaraka", "kibouchi": "Manzaraka", "difficulty": 2},
                {"french": "Chant religieux homme", "shimaore": "Moulidi/Dahira/Dinahou", "kibouchi": "Moulidi/Dahira/Dinahou", "difficulty": 2},
                {"french": "Chant religieux mixte", "shimaore": "Shengué/Madilis", "kibouchi": "Maoulida shengué/Madilis", "difficulty": 2},
                {"french": "Chant religieux femme", "shimaore": "Déba", "kibouchi": "Déba", "difficulty": 2},
                {"french": "Danse traditionnelle mixte", "shimaore": "Shigoma", "kibouchi": "Shigoma", "difficulty": 1},
                {"french": "Danse traditionnelle femme", "shimaore": "Mbiwi/Wadhaha", "kibouchi": "Mbiwi/Wadhaha", "difficulty": 1},
                {"french": "Chant traditionnelle", "shimaore": "Mgodro", "kibouchi": "Mgodro", "difficulty": 1},
                {"french": "Barbecue traditionnelle", "shimaore": "Voulé", "kibouchi": "Voulé", "difficulty": 1},
                {"french": "Tamtam bœuf", "shimaore": "Ngoma ya nyombé", "kibouchi": "Vala naoumbi", "difficulty": 2},
                {"french": "Cérémonie", "shimaore": "Shouhouli", "kibouchi": "Shouhouli", "difficulty": 1},
                {"french": "Boxe traditionnelle", "shimaore": "Mrengué", "kibouchi": "Mouringui", "difficulty": 1},
                {"french": "Camper", "shimaore": "Tobé", "kibouchi": "Mitobi", "difficulty": 1},
                {"french": "Rite de la pluie", "shimaore": "Mgourou", "kibouchi": "Mgourou", "difficulty": 2}
            ]
            
            # Check if we have at least 16 tradition elements
            if len(tradition_words) >= 16:
                print(f"✅ Tradition elements count: {len(tradition_words)} (16+ required)")
            else:
                print(f"❌ Insufficient tradition elements: {len(tradition_words)} (16+ required)")
                return False
            
            # 4. Check specific tradition elements with correct French, Shimaoré, and Kibouchi translations
            print("\n--- Testing Specific Tradition Elements with Correct Translations ---")
            
            all_elements_correct = True
            
            for element in expected_tradition_elements:
                french_word = element['french']
                if french_word in tradition_words_by_french:
                    word = tradition_words_by_french[french_word]
                    
                    # Check all fields
                    checks = [
                        (word['shimaore'], element['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], element['kibouchi'], 'Kibouchi'),
                        (word['category'], 'tradition', 'Category'),
                        (word['difficulty'], element['difficulty'], 'Difficulty')
                    ]
                    
                    element_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            element_correct = False
                            all_elements_correct = False
                    
                    if element_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (difficulty: {word['difficulty']})")
                else:
                    print(f"❌ {french_word} not found in tradition category")
                    all_elements_correct = False
            
            # 5. Integration tests - verify tradition category is properly integrated with other categories
            print("\n--- Testing Integration with Other Categories ---")
            
            # Get all words to check integration
            all_words_response = self.session.get(f"{API_BASE}/words")
            if all_words_response.status_code != 200:
                print(f"❌ Could not retrieve all words for integration test: {all_words_response.status_code}")
                return False
            
            all_words = all_words_response.json()
            categories = set(word['category'] for word in all_words)
            
            if 'tradition' in categories:
                print("✅ Tradition category properly integrated with other categories")
                print(f"All categories: {sorted(categories)}")
            else:
                print("❌ Tradition category not found in overall word list")
                all_elements_correct = False
            
            # 6. Check total word counts across all categories
            print("\n--- Testing Total Word Counts After Adding Tradition ---")
            
            total_words = len(all_words)
            tradition_count = len([w for w in all_words if w['category'] == 'tradition'])
            
            print(f"Total words across all categories: {total_words}")
            print(f"Tradition category words: {tradition_count}")
            
            if tradition_count >= 16:
                print(f"✅ Tradition category has sufficient elements: {tradition_count}")
            else:
                print(f"❌ Tradition category has insufficient elements: {tradition_count}")
                all_elements_correct = False
            
            # 7. Test API endpoints functionality for tradition category
            print("\n--- Testing API Endpoints Functionality ---")
            
            # Test individual tradition element retrieval
            api_functionality_correct = True
            sample_elements = ["Mariage", "Cérémonie", "Danse traditionnelle mixte"]
            
            for element_name in sample_elements:
                if element_name in tradition_words_by_french:
                    word_id = tradition_words_by_french[element_name]['id']
                    
                    # Test individual word retrieval
                    response = self.session.get(f"{API_BASE}/words/{word_id}")
                    if response.status_code == 200:
                        retrieved_word = response.json()
                        if retrieved_word['category'] == 'tradition':
                            print(f"✅ {element_name} API retrieval working correctly")
                        else:
                            print(f"❌ {element_name} API retrieval returned wrong category")
                            api_functionality_correct = False
                    else:
                        print(f"❌ {element_name} API retrieval failed: {response.status_code}")
                        api_functionality_correct = False
            
            # 8. Ensure data integrity
            print("\n--- Testing Data Integrity ---")
            
            # Check for duplicates in tradition category
            french_names = [word['french'] for word in tradition_words]
            unique_names = set(french_names)
            
            if len(french_names) == len(unique_names):
                print(f"✅ No duplicate entries in tradition category ({len(unique_names)} unique elements)")
                data_integrity_check = True
            else:
                duplicates = [name for name in french_names if french_names.count(name) > 1]
                print(f"❌ Duplicate entries found in tradition category: {set(duplicates)}")
                data_integrity_check = False
                all_elements_correct = False
            
            # Check that all tradition elements have required fields
            required_fields = {'id', 'french', 'shimaore', 'kibouchi', 'category', 'difficulty'}
            fields_check = True
            
            for word in tradition_words:
                if not required_fields.issubset(word.keys()):
                    print(f"❌ {word.get('french', 'Unknown')} missing required fields")
                    fields_check = False
                    all_elements_correct = False
            
            if fields_check:
                print("✅ All tradition elements have required fields")
            
            # Overall result
            integration_tests_passed = (
                all_elements_correct and 
                api_functionality_correct and 
                data_integrity_check and 
                fields_check
            )
            
            if integration_tests_passed:
                print("\n🎉 TRADITION VOCABULARY SECTION TESTING COMPLETED SUCCESSFULLY!")
                print("✅ Backend startup without errors after adding tradition section")
                print("✅ /api/words?category=tradition endpoint working correctly")
                print(f"✅ All {len(tradition_words)} tradition elements from tableau verified")
                print("✅ Specific tradition elements with correct French, Shimaoré, and Kibouchi translations:")
                print("   - Mariage: haroussi / haroussi")
                print("   - Chant mariage traditionnel: mlélézi / mlélézi")
                print("   - Petit mariage: mafounguidzo / mafounguidzo")
                print("   - Grand mariage: manzaraka / manzaraka")
                print("   - Chant religieux homme: moulidi/dahira/dinahou / moulidi/dahira/dinahou")
                print("   - Chant religieux mixte: shengué/madilis / maoulida shengué/madilis")
                print("   - Chant religieux femme: déba / déba")
                print("   - Danse traditionnelle mixte: shigoma / shigoma")
                print("   - Danse traditionnelle femme: mbiwi/wadhaha / mbiwi/wadhaha")
                print("   - Chant traditionnelle: mgodro / mgodro")
                print("   - Barbecue traditionnelle: voulé / voulé")
                print("   - Tamtam bœuf: ngoma ya nyombé / vala naoumbi")
                print("   - Cérémonie: shouhouli / shouhouli")
                print("   - Boxe traditionnelle: mrengué / mouringui")
                print("   - Camper: tobé / mitobi")
                print("   - Rite de la pluie: mgourou / mgourou")
                print("✅ Tradition category properly integrated with other categories")
                print(f"✅ Total word count after adding tradition: {total_words}")
                print(f"✅ Tradition elements count: {tradition_count}")
                print("✅ API endpoints functionality verified")
                print("✅ Data integrity confirmed - all cultural elements properly preserved")
                print("✅ This new cultural vocabulary section preserves important Mayotte traditions")
            else:
                print("\n❌ Some tradition vocabulary elements are incorrect, missing, or have integration issues")
            
            return integration_tests_passed
            
        except Exception as e:
            print(f"❌ Tradition vocabulary section test error: {e}")
            return False

if __name__ == "__main__":
    print("🌺 MAYOTTE EDUCATIONAL APP - TRADITION VOCABULARY TESTING 🌺")
    print("=" * 70)
    
    tester = TraditionVocabularyTester()
    
    # Run the tradition vocabulary test
    print("Running tradition vocabulary section test...")
    
    try:
        if tester.test_tradition_vocabulary_section():
            print("\n🎉 TRADITION VOCABULARY TESTING COMPLETED SUCCESSFULLY! 🎉")
            print("✅ All tradition elements from the tableau verified")
            print("✅ Backend integration working correctly")
            print("✅ Cultural elements properly preserved")
            print("🌺 The tradition vocabulary section is ready for educational use! 🌺")
        else:
            print("\n❌ TRADITION VOCABULARY TESTING FAILED!")
            print("Please review the issues above and fix them.")
    except Exception as e:
        print(f"\n❌ TRADITION VOCABULARY TESTING ERROR: {e}")
    
    print("=" * 70)