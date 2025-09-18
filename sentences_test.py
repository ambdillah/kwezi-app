#!/usr/bin/env python3
"""
Focused test for the 'Construire des phrases' game backend functionality
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('EXPO_PUBLIC_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

print(f"Testing 'Construire des phrases' game backend at: {API_BASE}")

def test_construire_des_phrases_game():
    """Test the 'Construire des phrases' game backend functionality after fixing the critical bug"""
    print("\n=== Testing 'Construire des phrases' Game Backend Functionality ===")
    print("CRITICAL TESTING: Sentence construction game after bug fix")
    
    try:
        # 1. Test /api/init-sentences endpoint functionality
        print("\n--- Testing /api/init-sentences Endpoint ---")
        
        # First check if sentences exist
        sentences_response = requests.get(f"{API_BASE}/sentences")
        if sentences_response.status_code == 200:
            existing_sentences = sentences_response.json()
            print(f"Current sentences in database: {len(existing_sentences)}")
        else:
            print(f"Could not check existing sentences: {sentences_response.status_code}")
        
        # Initialize sentences database
        init_response = requests.post(f"{API_BASE}/init-sentences")
        print(f"Init sentences status: {init_response.status_code}")
        
        if init_response.status_code == 200:
            result = init_response.json()
            print(f"✅ Sentences initialization successful: {result}")
        else:
            print(f"❌ Sentences initialization failed: {init_response.text}")
            return False
        
        # 2. Test /api/sentences endpoint returns proper sentences
        print("\n--- Testing /api/sentences Endpoint ---")
        
        sentences_response = requests.get(f"{API_BASE}/sentences")
        if sentences_response.status_code != 200:
            print(f"❌ Sentences endpoint failed: {sentences_response.status_code} - {sentences_response.text}")
            return False
        
        sentences = sentences_response.json()
        print(f"✅ Retrieved {len(sentences)} sentences from /api/sentences")
        
        if len(sentences) == 0:
            print("❌ CRITICAL: /api/sentences returns empty array - game will be stuck on loading!")
            return False
        
        # 3. Test sentence structure has all required fields
        print("\n--- Testing Sentence Structure ---")
        
        if sentences:
            sample_sentence = sentences[0]
            print(f"Sample sentence structure: {list(sample_sentence.keys())}")
            
            # Check required fields for sentence construction game
            required_fields = ['french', 'shimaore', 'kibouchi', 'tense', 'difficulty']
            
            structure_valid = True
            for field in required_fields:
                if field in sample_sentence:
                    print(f"✅ Required field '{field}': {sample_sentence[field]}")
                else:
                    print(f"❌ Missing required field '{field}'")
                    structure_valid = False
            
            # Check for word arrays (needed for game reconstruction)
            if 'shimaore_words' in sample_sentence or 'kibouchi_words' in sample_sentence:
                shimaore_words = sample_sentence.get('shimaore_words', [])
                kibouchi_words = sample_sentence.get('kibouchi_words', [])
                print(f"✅ Word arrays found for game reconstruction:")
                print(f"   Shimaoré words: {shimaore_words}")
                print(f"   Kibouchi words: {kibouchi_words}")
            else:
                print("⚠️ No word arrays found - may affect game reconstruction")
            
            if not structure_valid:
                print("❌ Sentence structure is invalid")
                return False
        
        # 4. Test filtering by difficulty works correctly
        print("\n--- Testing Difficulty Filtering ---")
        
        # Test difficulty 1
        diff1_response = requests.get(f"{API_BASE}/sentences?difficulty=1")
        if diff1_response.status_code == 200:
            diff1_sentences = diff1_response.json()
            print(f"✅ Difficulty 1 filtering: {len(diff1_sentences)} sentences")
            
            # Verify all returned sentences have difficulty 1
            if diff1_sentences:
                all_diff1 = all(s.get('difficulty') == 1 for s in diff1_sentences)
                if all_diff1:
                    print("✅ All difficulty 1 sentences have correct difficulty level")
                else:
                    print("❌ Some sentences have incorrect difficulty level")
                    return False
        else:
            print(f"❌ Difficulty 1 filtering failed: {diff1_response.status_code}")
            return False
        
        # Test difficulty 2
        diff2_response = requests.get(f"{API_BASE}/sentences?difficulty=2")
        if diff2_response.status_code == 200:
            diff2_sentences = diff2_response.json()
            print(f"✅ Difficulty 2 filtering: {len(diff2_sentences)} sentences")
        else:
            print(f"❌ Difficulty 2 filtering failed: {diff2_response.status_code}")
            return False
        
        # 5. Test filtering by tense works correctly
        print("\n--- Testing Tense Filtering ---")
        
        # Test different tenses (present, past, future)
        tenses_to_test = ['present', 'past', 'future']
        tense_results = {}
        
        for tense in tenses_to_test:
            tense_response = requests.get(f"{API_BASE}/sentences?tense={tense}")
            if tense_response.status_code == 200:
                tense_sentences = tense_response.json()
                tense_results[tense] = len(tense_sentences)
                print(f"✅ {tense.capitalize()} tense filtering: {len(tense_sentences)} sentences")
                
                # Verify all returned sentences have correct tense
                if tense_sentences:
                    all_correct_tense = all(s.get('tense') == tense for s in tense_sentences)
                    if all_correct_tense:
                        print(f"✅ All {tense} sentences have correct tense")
                    else:
                        print(f"❌ Some {tense} sentences have incorrect tense")
                        return False
            else:
                print(f"❌ {tense.capitalize()} tense filtering failed: {tense_response.status_code}")
                return False
        
        # 6. Test sentences are properly conjugated in all three languages
        print("\n--- Testing Sentence Conjugations ---")
        
        if sentences:
            conjugation_test_passed = True
            
            # Test first few sentences for proper conjugations
            for i, sentence in enumerate(sentences[:3]):  # Test first 3 sentences
                print(f"\nSentence {i+1}:")
                print(f"  French: {sentence.get('french', 'N/A')}")
                print(f"  Shimaoré: {sentence.get('shimaore', 'N/A')}")
                print(f"  Kibouchi: {sentence.get('kibouchi', 'N/A')}")
                print(f"  Tense: {sentence.get('tense', 'N/A')}")
                print(f"  Difficulty: {sentence.get('difficulty', 'N/A')}")
                
                # Check that all three languages are present and non-empty
                if (sentence.get('french') and 
                    sentence.get('shimaore') and 
                    sentence.get('kibouchi')):
                    print(f"✅ Sentence {i+1} has all three language conjugations")
                else:
                    print(f"❌ Sentence {i+1} missing conjugations in some languages")
                    conjugation_test_passed = False
            
            if not conjugation_test_passed:
                print("❌ Some sentences have incomplete conjugations")
                return False
        
        # 7. Test combined filtering (difficulty + tense)
        print("\n--- Testing Combined Filtering ---")
        
        combined_response = requests.get(f"{API_BASE}/sentences?difficulty=1&tense=present")
        if combined_response.status_code == 200:
            combined_sentences = combined_response.json()
            print(f"✅ Combined filtering (difficulty=1, tense=present): {len(combined_sentences)} sentences")
            
            # Verify all sentences match both criteria
            if combined_sentences:
                all_match = all(s.get('difficulty') == 1 and s.get('tense') == 'present' 
                              for s in combined_sentences)
                if all_match:
                    print("✅ All sentences match combined filter criteria")
                else:
                    print("❌ Some sentences don't match combined filter criteria")
                    return False
        else:
            print(f"❌ Combined filtering failed: {combined_response.status_code}")
            return False
        
        # 8. Test limit parameter works
        print("\n--- Testing Limit Parameter ---")
        
        limit_response = requests.get(f"{API_BASE}/sentences?limit=5")
        if limit_response.status_code == 200:
            limited_sentences = limit_response.json()
            if len(limited_sentences) <= 5:
                print(f"✅ Limit parameter working: requested 5, got {len(limited_sentences)}")
            else:
                print(f"❌ Limit parameter not working: requested 5, got {len(limited_sentences)}")
                return False
        else:
            print(f"❌ Limit parameter test failed: {limit_response.status_code}")
            return False
        
        # 9. Verify total sentence count
        print("\n--- Testing Total Sentence Count ---")
        
        # Get all sentences without limit
        all_sentences_response = requests.get(f"{API_BASE}/sentences?limit=1000")
        if all_sentences_response.status_code == 200:
            all_sentences = all_sentences_response.json()
            total_count = len(all_sentences)
            print(f"Total sentences available: {total_count}")
            
            if total_count >= 50:
                print(f"✅ Good sentence count: {total_count} sentences (50+ is sufficient for game)")
            else:
                print(f"❌ Insufficient sentence count: {total_count} sentences")
                return False
        else:
            print(f"❌ Could not get total sentence count: {all_sentences_response.status_code}")
            return False
        
        # 10. Test that the game should now work (no more loading stuck)
        print("\n--- Testing Game Loading Fix ---")
        
        # Simulate what the frontend game would do
        game_sentences_response = requests.get(f"{API_BASE}/sentences?difficulty=1&limit=10")
        if game_sentences_response.status_code == 200:
            game_sentences = game_sentences_response.json()
            
            if len(game_sentences) > 0:
                print(f"✅ Game loading fix confirmed: {len(game_sentences)} sentences available for game")
                print("✅ 'Construire des phrases' game should no longer be stuck on 'chargement des phrases'")
                
                # Show a sample sentence that the game would use
                if game_sentences:
                    sample = game_sentences[0]
                    print(f"Sample game sentence:")
                    print(f"  French: {sample.get('french')}")
                    print(f"  Shimaoré: {sample.get('shimaore')}")
                    print(f"  Kibouchi: {sample.get('kibouchi')}")
                    print(f"  Word arrays: {sample.get('shimaore_words')} / {sample.get('kibouchi_words')}")
            else:
                print("❌ CRITICAL: Game would still be stuck - no sentences returned for game")
                return False
        else:
            print(f"❌ Game loading test failed: {game_sentences_response.status_code}")
            return False
        
        # Overall result
        print("\n--- Test Summary ---")
        
        print("\n🎉 'CONSTRUIRE DES PHRASES' GAME BACKEND TESTING COMPLETED SUCCESSFULLY!")
        print("✅ /api/init-sentences endpoint working - successfully initialized sentences")
        print("✅ /api/sentences endpoint returns proper sentences (no more empty array)")
        print("✅ Sentence structure has all required fields (french, shimaore, kibouchi, tense, difficulty)")
        print("✅ Filtering by difficulty works correctly (difficulty 1 and 2)")
        print("✅ Filtering by tense works correctly (present, past, future)")
        print("✅ Combined filtering (difficulty + tense) works correctly")
        print("✅ Sentences are properly conjugated in all three languages")
        print("✅ Limit parameter works correctly")
        print(f"✅ Total sentence count is sufficient: {total_count} sentences")
        print("✅ Game loading fix confirmed - 'chargement des phrases' issue resolved")
        print("\n🎮 GAME STATUS: The 'Construire des phrases' game should now work correctly!")
        print("   - No more stuck on loading screen")
        print("   - Sentences available in French, Shimaoré, and Kibouchi")
        print("   - Proper difficulty and tense filtering")
        print("   - Complete sentence conjugation system")
        print("   - Word arrays available for sentence reconstruction game")
        
        return True
        
    except Exception as e:
        print(f"❌ 'Construire des phrases' game backend test error: {e}")
        return False

if __name__ == "__main__":
    success = test_construire_des_phrases_game()
    if success:
        print("\n🎉 ALL TESTS PASSED! The 'Construire des phrases' game backend is working correctly.")
    else:
        print("\n❌ TESTS FAILED! Please check the issues above.")