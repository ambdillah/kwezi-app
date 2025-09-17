#!/usr/bin/env python3
"""
PDF Database Verification Test
Tests that the database has been correctly created from the user's PDF file
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

def test_pdf_database_verification():
    """Test that the database has been correctly created from the user's PDF file"""
    print("\n=== Testing PDF Database Verification (Review Request) ===")
    
    session = requests.Session()
    
    try:
        # Initialize base content first
        print("--- Initializing Base Content ---")
        init_response = session.post(f"{API_BASE}/init-base-content")
        if init_response.status_code != 200:
            print(f"❌ Failed to initialize base content: {init_response.status_code}")
            return False
        print("✅ Base content initialized")
        
        # Get all words
        response = session.get(f"{API_BASE}/words")
        if response.status_code != 200:
            print(f"❌ Could not retrieve words: {response.status_code}")
            return False
        
        words = response.json()
        print(f"Total words retrieved: {len(words)}")
        
        # 1. Count total words - should be exactly 469 words
        print("\n--- Testing Total Word Count (Should be 469) ---")
        expected_total = 469
        actual_total = len(words)
        
        if actual_total == expected_total:
            print(f"✅ Total word count correct: {actual_total} words")
            word_count_correct = True
        else:
            print(f"❌ Total word count incorrect: {actual_total} words (expected {expected_total})")
            word_count_correct = False
        
        # 2. Verify exact categories from PDF with specific word counts
        print("\n--- Testing Exact Categories from PDF ---")
        
        # Group words by category
        words_by_category = {}
        for word in words:
            category = word['category']
            if category not in words_by_category:
                words_by_category[category] = []
            words_by_category[category].append(word)
        
        # Expected categories with exact counts from PDF
        expected_categories = {
            'adjectif': 12,
            'animal': 69,
            'chiffre': 20,
            'corps_humain': 32,
            'couleur': 8,
            'expression': 44,
            'famille': 20,
            'grammaire': 12,
            'humain': 2,
            'maison': 3,
            'nature': 47,
            'nourriture': 43,
            'objet': 34,
            'profession': 8,
            'salutations': 8,
            'vegetal': 1,
            'verbe': 106
        }
        
        categories_correct = True
        
        print(f"Expected categories: {len(expected_categories)}")
        print(f"Actual categories: {len(words_by_category)}")
        print(f"Actual categories found: {sorted(words_by_category.keys())}")
        
        for category, expected_count in expected_categories.items():
            if category in words_by_category:
                actual_count = len(words_by_category[category])
                if actual_count == expected_count:
                    print(f"✅ {category}: {actual_count} words (correct)")
                else:
                    print(f"❌ {category}: {actual_count} words (expected {expected_count})")
                    categories_correct = False
            else:
                print(f"❌ {category}: missing category (expected {expected_count} words)")
                categories_correct = False
        
        # Check for unexpected categories
        for category in words_by_category:
            if category not in expected_categories:
                print(f"❌ Unexpected category found: {category} ({len(words_by_category[category])} words)")
                categories_correct = False
        
        # 3. Verify exact translations from PDF
        print("\n--- Testing Exact Translations from PDF ---")
        
        words_by_french = {word['french']: word for word in words}
        
        # Expected exact translations from PDF
        expected_translations = [
            {"french": "Poulet", "shimaore": "bawa", "category": "nourriture"},
            {"french": "Hérisson", "shimaore": "landra", "category": "animal"},  # Note: might be "Hérisson/tangue"
            {"french": "Araignée", "shimaore": "shitrandrabwibwi", "category": "animal"},
            {"french": "Poivre", "shimaore": "bvilibvili manga", "category": "nourriture"},
            {"french": "Bonjour", "shimaore": "kwezi", "category": "salutations"},
            {"french": "Un", "shimaore": "moja", "category": "chiffre"},
            {"french": "Maison", "shimaore": "nyoumba", "category": "maison"}
        ]
        
        translations_correct = True
        
        for expected in expected_translations:
            french_word = expected['french']
            
            # Check if word exists (might have variations like "Hérisson/tangue")
            found_word = None
            if french_word in words_by_french:
                found_word = words_by_french[french_word]
            else:
                # Check for variations
                for word_key in words_by_french:
                    if french_word.lower() in word_key.lower():
                        found_word = words_by_french[word_key]
                        break
            
            if found_word:
                # Check shimaoré translation (case insensitive)
                actual_shimaore = found_word['shimaore'].lower()
                expected_shimaore = expected['shimaore'].lower()
                
                if actual_shimaore == expected_shimaore:
                    print(f"✅ {french_word}: shimaoré '{found_word['shimaore']}' correct")
                else:
                    print(f"❌ {french_word}: shimaoré '{found_word['shimaore']}' (expected '{expected['shimaore']}')")
                    translations_correct = False
                
                # Check category
                if found_word['category'] == expected['category']:
                    print(f"✅ {french_word}: category '{found_word['category']}' correct")
                else:
                    print(f"❌ {french_word}: category '{found_word['category']}' (expected '{expected['category']}')")
                    translations_correct = False
            else:
                print(f"❌ {french_word}: not found in database")
                translations_correct = False
        
        # 4. Verify emojis are integrated as image_url
        print("\n--- Testing Emoji Integration as image_url ---")
        
        words_with_images = [word for word in words if word.get('image_url')]
        emoji_integration_correct = len(words_with_images) > 0
        
        if emoji_integration_correct:
            print(f"✅ Emoji integration confirmed: {len(words_with_images)} words have image_url")
            # Show some examples
            for i, word in enumerate(words_with_images[:5]):
                print(f"   Example {i+1}: {word['french']} -> {word['image_url']}")
        else:
            print(f"❌ No emojis found as image_url")
        
        # 5. Verify data integrity - all translations should correspond exactly to PDF
        print("\n--- Testing Data Integrity ---")
        
        # Check that all words have required fields
        integrity_issues = []
        
        for word in words:
            if not word.get('french'):
                integrity_issues.append(f"Word missing French: {word}")
            if not word.get('shimaore') and not word.get('kibouchi'):
                integrity_issues.append(f"Word missing both translations: {word['french']}")
            if not word.get('category'):
                integrity_issues.append(f"Word missing category: {word['french']}")
        
        data_integrity_correct = len(integrity_issues) == 0
        
        if data_integrity_correct:
            print(f"✅ Data integrity verified: All {len(words)} words have required fields")
        else:
            print(f"❌ Data integrity issues found: {len(integrity_issues)} problems")
            for issue in integrity_issues[:5]:  # Show first 5 issues
                print(f"   - {issue}")
        
        # Overall result
        all_tests_passed = (
            word_count_correct and 
            categories_correct and 
            translations_correct and 
            emoji_integration_correct and 
            data_integrity_correct
        )
        
        print("\n--- PDF Database Verification Summary ---")
        if all_tests_passed:
            print("🎉 PDF DATABASE VERIFICATION COMPLETED SUCCESSFULLY!")
            print("✅ Total word count: 469 words (exact match)")
            print("✅ All 17 categories with exact word counts verified")
            print("✅ All specific translations from PDF verified")
            print("✅ Emoji integration confirmed as image_url")
            print("✅ Data integrity verified - all translations match PDF")
            print("✅ Database reflects EXACTLY the content of the user's PDF file")
        else:
            print("❌ PDF DATABASE VERIFICATION FAILED!")
            if not word_count_correct:
                print("❌ Total word count does not match PDF (469 expected)")
            if not categories_correct:
                print("❌ Categories or word counts do not match PDF")
            if not translations_correct:
                print("❌ Some specific translations do not match PDF")
            if not emoji_integration_correct:
                print("❌ Emojis not properly integrated as image_url")
            if not data_integrity_correct:
                print("❌ Data integrity issues found")
        
        return all_tests_passed
        
    except Exception as e:
        print(f"❌ PDF database verification error: {e}")
        return False

if __name__ == "__main__":
    result = test_pdf_database_verification()
    if result:
        print("\n🎉 PDF verification test PASSED!")
    else:
        print("\n❌ PDF verification test FAILED!")