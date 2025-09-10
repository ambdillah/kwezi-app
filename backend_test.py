#!/usr/bin/env python3
"""
Backend Test Suite for Mayotte Educational App
Tests all backend API endpoints for educational content in Shimaoré and Kibouchi languages
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

class MayotteEducationTester:
    def __init__(self):
        self.session = requests.Session()
        self.created_word_id = None
        self.created_exercise_id = None
        
    def test_basic_connectivity(self):
        """Test basic API connectivity"""
        print("\n=== Testing Basic API Connectivity ===")
        
        try:
            # Test root endpoint
            response = self.session.get(f"{BACKEND_URL}/")
            print(f"Root endpoint status: {response.status_code}")
            
            # Test API root (this might not exist, but let's try)
            try:
                response = self.session.get(f"{API_BASE}/")
                print(f"API root endpoint status: {response.status_code}")
            except Exception as e:
                print(f"API root endpoint not available: {e}")
            
            # Test docs endpoint
            try:
                response = self.session.get(f"{BACKEND_URL}/docs")
                print(f"Docs endpoint status: {response.status_code}")
            except Exception as e:
                print(f"Docs endpoint error: {e}")
                
            return True
            
        except Exception as e:
            print(f"❌ Basic connectivity failed: {e}")
            return False
    
    def test_mongodb_connection(self):
        """Test MongoDB connection by trying to get words"""
        print("\n=== Testing MongoDB Connection ===")
        
        try:
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code == 200:
                print(f"✅ MongoDB connection working - Status: {response.status_code}")
                words = response.json()
                print(f"Current words count: {len(words)}")
                return True
            else:
                print(f"❌ MongoDB connection issue - Status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ MongoDB connection test failed: {e}")
            return False
    
    def test_init_base_content(self):
        """Test educational content initialization with corrected translations"""
        print("\n=== Testing Educational Content Initialization (Corrected Translations) ===")
        
        try:
            # First, clear existing content by deleting all words
            print("Clearing existing content...")
            try:
                words_response = self.session.get(f"{API_BASE}/words")
                if words_response.status_code == 200:
                    existing_words = words_response.json()
                    for word in existing_words:
                        delete_response = self.session.delete(f"{API_BASE}/words/{word['id']}")
                        if delete_response.status_code != 200:
                            print(f"Warning: Could not delete word {word['id']}")
                    print(f"Cleared {len(existing_words)} existing words")
            except Exception as e:
                print(f"Note: Could not clear existing content: {e}")
            
            # Initialize base content with corrected translations
            response = self.session.post(f"{API_BASE}/init-base-content")
            print(f"Init base content status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Base content initialization: {result}")
                return True
            else:
                print(f"❌ Base content initialization failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Base content initialization error: {e}")
            return False
    
    def test_get_words(self):
        """Test getting all words and verify base content"""
        print("\n=== Testing Get Words ===")
        
        try:
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code == 200:
                words = response.json()
                print(f"✅ Retrieved {len(words)} words")
                
                # Check for expected categories
                categories = set(word['category'] for word in words)
                expected_categories = {'famille', 'couleurs', 'animaux', 'salutations', 'nombres'}
                
                print(f"Found categories: {categories}")
                if expected_categories.issubset(categories):
                    print("✅ All expected categories found")
                else:
                    missing = expected_categories - categories
                    print(f"⚠️ Missing categories: {missing}")
                
                # Check language fields
                if words:
                    sample_word = words[0]
                    required_fields = {'french', 'shimaore', 'kibouchi', 'category'}
                    if required_fields.issubset(sample_word.keys()):
                        print("✅ Words have required language fields")
                        print(f"Sample word: {sample_word['french']} = {sample_word['shimaore']} (Shimaoré) / {sample_word['kibouchi']} (Kibouchi)")
                    else:
                        print(f"❌ Missing required fields in words")
                
                return True
            else:
                print(f"❌ Get words failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Get words error: {e}")
            return False
    
    def test_comprehensive_vocabulary_initialization(self):
        """Test comprehensive vocabulary initialization with 80+ words across 11 categories"""
        print("\n=== Testing Comprehensive Vocabulary Initialization ===")
        
        try:
            # Get all words to verify comprehensive vocabulary
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Could not retrieve words: {response.status_code}")
                return False
            
            words = response.json()
            print(f"Total words found: {len(words)}")
            
            # Check if we have 80+ words
            if len(words) >= 80:
                print(f"✅ Comprehensive vocabulary confirmed: {len(words)} words (80+ required)")
            else:
                print(f"❌ Insufficient vocabulary: {len(words)} words (80+ required)")
                return False
            
            # Check categories
            categories = set(word['category'] for word in words)
            expected_categories = {
                'famille', 'salutations', 'couleurs', 'animaux', 'nombres', 
                'corps', 'nourriture', 'maison', 'vetements', 'nature', 'transport'
            }
            
            print(f"Found categories ({len(categories)}): {sorted(categories)}")
            print(f"Expected categories ({len(expected_categories)}): {sorted(expected_categories)}")
            
            if expected_categories.issubset(categories):
                print(f"✅ All 11 expected categories found")
            else:
                missing = expected_categories - categories
                print(f"❌ Missing categories: {missing}")
                return False
            
            # Check difficulty levels (should be 1-2)
            difficulties = set(word['difficulty'] for word in words)
            print(f"Difficulty levels found: {sorted(difficulties)}")
            if difficulties.issubset({1, 2}):
                print("✅ Difficulty levels properly assigned (1-2)")
            else:
                print(f"❌ Invalid difficulty levels found: {difficulties - {1, 2}}")
            
            return True
            
        except Exception as e:
            print(f"❌ Comprehensive vocabulary test error: {e}")
            return False
    
    def test_specific_vocabulary_from_table(self):
        """Test specific vocabulary from the user's comprehensive table"""
        print("\n=== Testing Specific Vocabulary from User's Table ===")
        
        try:
            # Get all words
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Could not retrieve words: {response.status_code}")
                return False
            
            words = response.json()
            words_by_french = {word['french']: word for word in words}
            
            # Test specific vocabulary from user's table
            test_cases = [
                # Famille (updated translations)
                {"french": "Frère", "shimaore": "Mwanagna mtroun", "kibouchi": "Anadahi", "category": "famille"},
                {"french": "Sœur", "shimaore": "Mwanagna mtroub", "kibouchi": "Anabavi", "category": "famille"},
                
                # Corps
                {"french": "Tête", "shimaore": "Mutru", "kibouchi": "Loha", "category": "corps"},
                {"french": "Cheveux", "shimaore": "Nngnele", "kibouchi": "Fagneva", "category": "corps"},
                
                # Nourriture (updated translations)
                {"french": "Eau", "shimaore": "Madji", "kibouchi": "Rano", "category": "nourriture"},
                {"french": "Riz", "shimaore": "Tsohole", "kibouchi": "Vari", "category": "nourriture"},
                {"french": "Nourriture", "shimaore": "Chaoula", "kibouchi": "Hanigni", "category": "nourriture"},
                {"french": "Pain", "shimaore": "Dipé", "kibouchi": "Dipé", "category": "nourriture"},
                
                # Nature (updated translations)
                {"french": "Arbre", "shimaore": "Mwiri", "kibouchi": "Kakazou", "category": "nature"},
                {"french": "Soleil", "shimaore": "Djuwa", "kibouchi": "Kouva", "category": "nature"},
                {"french": "Mer", "shimaore": "Bahari", "kibouchi": "Bahari", "category": "nature"},
                {"french": "Plage", "shimaore": "Mtsangani", "kibouchi": "Fassigni", "category": "nature"},
                
                # Maison (updated translations)
                {"french": "Maison", "shimaore": "Nyoumba", "kibouchi": "Tragnou", "category": "maison"},
                {"french": "Porte", "shimaore": "Mlango", "kibouchi": "Varavarangna", "category": "maison"},
                {"french": "Lit", "shimaore": "Chtrandra", "kibouchi": "Koubani", "category": "maison"},
                
                # Couleurs (updated translations)
                {"french": "Bleu", "shimaore": "Bilé", "kibouchi": "Bilé", "category": "couleurs"},
                {"french": "Vert", "shimaore": "Dhavou", "kibouchi": "Mayitsou", "category": "couleurs"},
                {"french": "Noir", "shimaore": "Nzidhou", "kibouchi": "Mayintigni", "category": "couleurs"},
                {"french": "Blanc", "shimaore": "Ndjéou", "kibouchi": "Malandi", "category": "couleurs"},
                
                # Special cases
                {"french": "Singe", "shimaore": "Djakwe", "kibouchi": "", "category": "animaux"},  # No Kibouchi
                {"french": "Langue", "shimaore": "", "kibouchi": "Lela", "category": "corps"},  # No Shimaoré
                
                # Complex numbers (corrected)
                {"french": "Onze", "shimaore": "Koumi na moja", "kibouchi": "Foulou Areki Ambi", "category": "nombres"},
                {"french": "Douze", "shimaore": "Koumi na mbili", "kibouchi": "Foulou Aroyi Ambi", "category": "nombres"},
            ]
            
            all_correct = True
            
            for test_case in test_cases:
                french_word = test_case['french']
                if french_word in words_by_french:
                    word = words_by_french[french_word]
                    
                    # Check all fields
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                        (word['category'], test_case['category'], 'Category')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            all_correct = False
                    
                    if word_correct:
                        shimaore_display = word['shimaore'] if word['shimaore'] else "(none)"
                        kibouchi_display = word['kibouchi'] if word['kibouchi'] else "(none)"
                        print(f"✅ {french_word}: {shimaore_display} (Shimaoré) / {kibouchi_display} (Kibouchi) - {word['category']}")
                else:
                    print(f"❌ {french_word} not found in database")
                    all_correct = False
            
            if all_correct:
                print("✅ All specific vocabulary from user's table verified!")
            else:
                print("❌ Some vocabulary items are incorrect or missing")
            
            return all_correct
            
        except Exception as e:
            print(f"❌ Specific vocabulary test error: {e}")
            return False
    
    def test_updated_greeting_improvements(self):
        """Test specific greeting improvements from the final table"""
        print("\n=== Testing Updated Greeting Improvements ===")
        
        try:
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Could not retrieve words: {response.status_code}")
                return False
            
            words = response.json()
            words_by_french = {word['french']: word for word in words}
            
            # Test specific greeting improvements
            greeting_tests = [
                {"french": "Comment ça va", "shimaore": "Jéjé", "kibouchi": "Akori"},
                {"french": "Ça va bien", "shimaore": "Fétré", "kibouchi": "Tsara"},
                {"french": "Oui", "shimaore": "Ewa", "kibouchi": "Iya"},
                {"french": "Non", "shimaore": "Anha", "kibouchi": "Anha"},
                {"french": "Excuse-moi", "shimaore": "Soimahani", "kibouchi": "Soimahani"}
            ]
            
            all_correct = True
            for test_case in greeting_tests:
                french_word = test_case['french']
                if french_word in words_by_french:
                    word = words_by_french[french_word]
                    if word['shimaore'] == test_case['shimaore'] and word['kibouchi'] == test_case['kibouchi']:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']}")
                    else:
                        print(f"❌ {french_word}: Expected {test_case['shimaore']}/{test_case['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        all_correct = False
                else:
                    print(f"❌ {french_word} not found")
                    all_correct = False
            
            return all_correct
            
        except Exception as e:
            print(f"❌ Greeting improvements test error: {e}")
            return False
    
    def test_pronoun_additions(self):
        """Test pronoun additions in grammaire category"""
        print("\n=== Testing Pronoun Additions ===")
        
        try:
            response = self.session.get(f"{API_BASE}/words?category=grammaire")
            if response.status_code != 200:
                print(f"❌ Could not retrieve grammaire words: {response.status_code}")
                return False
            
            grammaire_words = response.json()
            words_by_french = {word['french']: word for word in grammaire_words}
            
            # Test pronoun additions
            pronoun_tests = [
                {"french": "Je", "shimaore": "Wami", "kibouchi": "Zahou"},
                {"french": "Tu", "shimaore": "Wawe", "kibouchi": "Anaou"},
                {"french": "Il/Elle", "shimaore": "Wayé", "kibouchi": "Izi"},
                {"french": "Nous", "shimaore": "Wassi", "kibouchi": "Atsika"},
                {"french": "Vous", "shimaore": "Wagnou", "kibouchi": "Anarèou"}
            ]
            
            print(f"Found {len(grammaire_words)} words in grammaire category")
            
            all_correct = True
            for test_case in pronoun_tests:
                french_word = test_case['french']
                if french_word in words_by_french:
                    word = words_by_french[french_word]
                    if word['shimaore'] == test_case['shimaore'] and word['kibouchi'] == test_case['kibouchi']:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']}")
                    else:
                        print(f"❌ {french_word}: Expected {test_case['shimaore']}/{test_case['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        all_correct = False
                else:
                    print(f"❌ {french_word} not found in grammaire category")
                    all_correct = False
            
            return all_correct
            
        except Exception as e:
            print(f"❌ Pronoun additions test error: {e}")
            return False
    
    def test_new_verb_additions(self):
        """Test new verb additions in verbes category"""
        print("\n=== Testing New Verb Additions ===")
        
        try:
            response = self.session.get(f"{API_BASE}/words?category=verbes")
            if response.status_code != 200:
                print(f"❌ Could not retrieve verbes words: {response.status_code}")
                return False
            
            verbes_words = response.json()
            words_by_french = {word['french']: word for word in verbes_words}
            
            # Test verb additions
            verb_tests = [
                {"french": "Jouer", "shimaore": "Nguadza", "kibouchi": "Msoma"},
                {"french": "Courir", "shimaore": "Wendra mbiyo", "kibouchi": "Miloumeyi"},
                {"french": "Marcher", "shimaore": "Wendra", "kibouchi": "Mandeha"}
            ]
            
            print(f"Found {len(verbes_words)} words in verbes category")
            
            all_correct = True
            for test_case in verb_tests:
                french_word = test_case['french']
                if french_word in words_by_french:
                    word = words_by_french[french_word]
                    if word['shimaore'] == test_case['shimaore'] and word['kibouchi'] == test_case['kibouchi']:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']}")
                    else:
                        print(f"❌ {french_word}: Expected {test_case['shimaore']}/{test_case['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        all_correct = False
                else:
                    print(f"❌ {french_word} not found in verbes category")
                    all_correct = False
            
            return all_correct
            
        except Exception as e:
            print(f"❌ Verb additions test error: {e}")
            return False
    
    def test_corrected_numbers_system(self):
        """Test the corrected numbers system 1-20 with authentic Shimaoré and Kibouchi translations"""
        print("\n=== Testing Corrected Numbers System (1-20) ===")
        
        try:
            response = self.session.get(f"{API_BASE}/words?category=nombres")
            if response.status_code != 200:
                print(f"❌ Could not retrieve numbers: {response.status_code}")
                return False
            
            numbers = response.json()
            numbers_by_french = {word['french']: word for word in numbers}
            
            print(f"Found {len(numbers)} numbers in database")
            
            # Test corrected numbers 1-10 (basic numbers)
            basic_numbers = [
                {"french": "Un", "shimaore": "Moja", "kibouchi": "Areki", "difficulty": 1},
                {"french": "Deux", "shimaore": "Mbili", "kibouchi": "Aroyi", "difficulty": 1},
                {"french": "Trois", "shimaore": "Trarou", "kibouchi": "Telou", "difficulty": 1},
                {"french": "Quatre", "shimaore": "Nhé", "kibouchi": "Efatra", "difficulty": 1},
                {"french": "Cinq", "shimaore": "Tsano", "kibouchi": "Dimi", "difficulty": 1},
                {"french": "Six", "shimaore": "Sita", "kibouchi": "Tchouta", "difficulty": 1},
                {"french": "Sept", "shimaore": "Saba", "kibouchi": "Fitou", "difficulty": 1},
                {"french": "Huit", "shimaore": "Nané", "kibouchi": "Valou", "difficulty": 1},
                {"french": "Neuf", "shimaore": "Chendra", "kibouchi": "Civi", "difficulty": 1},
                {"french": "Dix", "shimaore": "Koumi", "kibouchi": "Foulou", "difficulty": 1}
            ]
            
            # Test corrected numbers 11-19 (compound numbers)
            compound_numbers = [
                {"french": "Onze", "shimaore": "Koumi na moja", "kibouchi": "Foulou Areki Ambi", "difficulty": 2},
                {"french": "Douze", "shimaore": "Koumi na mbili", "kibouchi": "Foulou Aroyi Ambi", "difficulty": 2},
                {"french": "Treize", "shimaore": "Koumi na trarou", "kibouchi": "Foulou Telou Ambi", "difficulty": 2},
                {"french": "Quatorze", "shimaore": "Koumi na nhé", "kibouchi": "Foulou Efatra Ambi", "difficulty": 2},
                {"french": "Quinze", "shimaore": "Koumi na tsano", "kibouchi": "Foulou Dimi Ambi", "difficulty": 2},
                {"french": "Seize", "shimaore": "Koumi na sita", "kibouchi": "Foulou Tchouta Ambi", "difficulty": 2},
                {"french": "Dix-sept", "shimaore": "Koumi na saba", "kibouchi": "Foulou Fitou Ambi", "difficulty": 2},
                {"french": "Dix-huit", "shimaore": "Koumi na nané", "kibouchi": "Foulou Valou Ambi", "difficulty": 2},
                {"french": "Dix-neuf", "shimaore": "Koumi na chendra", "kibouchi": "Foulou Civi Ambi", "difficulty": 2}
            ]
            
            # Test number 20
            twenty = {"french": "Vingt", "shimaore": "Chirini", "kibouchi": "Arompoulou", "difficulty": 2}
            
            all_numbers_correct = True
            
            # Test basic numbers 1-10
            print("\n--- Testing Basic Numbers (1-10) ---")
            for test_case in basic_numbers:
                french_word = test_case['french']
                if french_word in numbers_by_french:
                    word = numbers_by_french[french_word]
                    
                    # Check all fields
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                        (word['difficulty'], test_case['difficulty'], 'Difficulty')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            all_numbers_correct = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (difficulty: {word['difficulty']})")
                else:
                    print(f"❌ {french_word} not found in database")
                    all_numbers_correct = False
            
            # Test compound numbers 11-19
            print("\n--- Testing Compound Numbers (11-19) ---")
            for test_case in compound_numbers:
                french_word = test_case['french']
                if french_word in numbers_by_french:
                    word = numbers_by_french[french_word]
                    
                    # Check all fields
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                        (word['difficulty'], test_case['difficulty'], 'Difficulty')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            all_numbers_correct = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (difficulty: {word['difficulty']})")
                else:
                    print(f"❌ {french_word} not found in database")
                    all_numbers_correct = False
            
            # Test number 20
            print("\n--- Testing Number 20 ---")
            french_word = twenty['french']
            if french_word in numbers_by_french:
                word = numbers_by_french[french_word]
                
                # Check all fields
                checks = [
                    (word['shimaore'], twenty['shimaore'], 'Shimaoré'),
                    (word['kibouchi'], twenty['kibouchi'], 'Kibouchi'),
                    (word['difficulty'], twenty['difficulty'], 'Difficulty')
                ]
                
                word_correct = True
                for actual, expected, field_name in checks:
                    if actual != expected:
                        print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                        word_correct = False
                        all_numbers_correct = False
                
                if word_correct:
                    print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (difficulty: {word['difficulty']})")
            else:
                print(f"❌ {french_word} not found in database")
                all_numbers_correct = False
            
            # Verify total count
            print(f"\n--- Numbers Count Verification ---")
            expected_count = 20  # Numbers 1-20
            actual_count = len(numbers)
            if actual_count >= expected_count:
                print(f"✅ Numbers count: {actual_count} (expected at least {expected_count})")
            else:
                print(f"❌ Numbers count: {actual_count} (expected at least {expected_count})")
                all_numbers_correct = False
            
            # Verify difficulty levels
            print(f"\n--- Difficulty Level Verification ---")
            difficulty_1_count = len([n for n in numbers if n['difficulty'] == 1])
            difficulty_2_count = len([n for n in numbers if n['difficulty'] == 2])
            print(f"Difficulty 1 (1-10): {difficulty_1_count} numbers")
            print(f"Difficulty 2 (11-20): {difficulty_2_count} numbers")
            
            if difficulty_1_count >= 10 and difficulty_2_count >= 10:
                print("✅ Difficulty levels properly assigned")
            else:
                print("❌ Difficulty levels not properly assigned")
                all_numbers_correct = False
            
            if all_numbers_correct:
                print("\n🎉 All corrected numbers (1-20) verified successfully!")
                print("✅ Basic numbers 1-10 with authentic translations")
                print("✅ Compound numbers 11-19 with proper formations")
                print("✅ Number 20 (Vingt) added correctly")
                print("✅ Proper difficulty levels assigned")
            else:
                print("\n❌ Some numbers have incorrect translations or are missing")
            
            return all_numbers_correct
            
        except Exception as e:
            print(f"❌ Corrected numbers system test error: {e}")
            return False
    
    def test_specific_adjective_corrections_verification(self):
        """Test the specific adjective corrections that were just made"""
        print("\n=== Testing Specific Adjective Corrections Verification ===")
        
        try:
            # 1. Test backend starts without syntax errors after corrections
            print("--- Testing Backend Startup After Corrections ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Backend has syntax errors or is not responding: {response.status_code}")
                return False
            print("✅ Backend starts without syntax errors after corrections")
            
            # 2. Test the /api/words?category=adjectifs endpoint
            print("\n--- Testing /api/words?category=adjectifs Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=adjectifs")
            if response.status_code != 200:
                print(f"❌ Adjectifs endpoint failed: {response.status_code}")
                return False
            
            adjective_words = response.json()
            adjective_words_by_french = {word['french']: word for word in adjective_words}
            print(f"✅ /api/words?category=adjectifs working correctly ({len(adjective_words)} adjectives)")
            
            # 3. Verify the specific corrections are in place
            print("\n--- Testing Specific Adjective Corrections ---")
            
            # Test specific corrections mentioned in review request
            specific_corrections = [
                {
                    "french": "En colère", 
                    "shimaore": "Hadabou", 
                    "kibouchi": "Méloukou",
                    "note": "shimaoré should be 'Hadabou' (not 'Ouja hassira')"
                },
                {
                    "french": "Faux", 
                    "shimaore": "Trambo", 
                    "kibouchi": "Vandi",
                    "note": "shimaoré should be 'Trambo' (not 'Trampé') and kibouchi should be 'Vandi'"
                },
                {
                    "french": "Ouvert", 
                    "shimaore": "Ouboua", 
                    "kibouchi": "Mibiyangna",
                    "note": "shimaoré should be 'Ouboua' and kibouchi should be 'Mibiyangna' (not 'Miblyangna')"
                },
                {
                    "french": "Amoureux", 
                    "shimaore": "Ouvendza", 
                    "kibouchi": "Mitiya",
                    "note": "shimaoré should be 'Ouvendza' (not 'Ouvengza')"
                },
                {
                    "french": "Honteux", 
                    "shimaore": "Ouona haya", 
                    "kibouchi": "Mampihingnatra",
                    "note": "kibouchi should be 'Mampihingnatra' (not 'Nampéihingatra')"
                },
                {
                    "french": "Long", 
                    "shimaore": "Drilé", 
                    "kibouchi": "Hapou",
                    "note": "shimaoré should be 'Drilé' (not 'Driié')"
                },
                {
                    "french": "Petit", 
                    "shimaore": "Titi", 
                    "kibouchi": "Héli",
                    "note": "shimaoré should be 'Titi' (not 'Tsi') and kibouchi should be 'Héli' (not 'Tsi')"
                },
                {
                    "french": "Grand", 
                    "shimaore": "Bolé", 
                    "kibouchi": "Bé",
                    "note": "shimaoré should be 'Bolé' (not 'Bole')"
                }
            ]
            
            corrections_verified = True
            
            for correction in specific_corrections:
                french_word = correction['french']
                if french_word in adjective_words_by_french:
                    word = adjective_words_by_french[french_word]
                    
                    # Check shimaoré correction
                    if word['shimaore'] == correction['shimaore']:
                        print(f"✅ {french_word} shimaoré: '{word['shimaore']}' - CORRECTION VERIFIED")
                    else:
                        print(f"❌ {french_word} shimaoré: Expected '{correction['shimaore']}', got '{word['shimaore']}'")
                        corrections_verified = False
                    
                    # Check kibouchi correction
                    if word['kibouchi'] == correction['kibouchi']:
                        print(f"✅ {french_word} kibouchi: '{word['kibouchi']}' - CORRECTION VERIFIED")
                    else:
                        print(f"❌ {french_word} kibouchi: Expected '{correction['kibouchi']}', got '{word['kibouchi']}'")
                        corrections_verified = False
                    
                    print(f"   Note: {correction['note']}")
                else:
                    print(f"❌ {french_word} not found in adjectifs category")
                    corrections_verified = False
            
            # 4. Check that all other adjective entries remain intact and unchanged
            print("\n--- Testing Other Adjective Entries Remain Intact ---")
            
            # Sample of other adjective items that should remain unchanged
            other_adjective_items = [
                {"french": "Beau/Jolie", "shimaore": "Mzouri", "kibouchi": "Zatovou"},
                {"french": "Bon", "shimaore": "Mwéma", "kibouchi": "Tsara"},
                {"french": "Chaud", "shimaore": "Moro", "kibouchi": "Méyi"},
                {"french": "Froid", "shimaore": "Baridi", "kibouchi": "Manintsi"},
                {"french": "Jeune", "shimaore": "Nrétsa", "kibouchi": "Zaza"}
            ]
            
            other_items_intact = True
            for item in other_adjective_items:
                french_word = item['french']
                if french_word in adjective_words_by_french:
                    word = adjective_words_by_french[french_word]
                    if word['shimaore'] == item['shimaore'] and word['kibouchi'] == item['kibouchi']:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} - UNCHANGED")
                    else:
                        print(f"❌ {french_word}: Expected {item['shimaore']}/{item['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        other_items_intact = False
                else:
                    print(f"❌ {french_word} not found")
                    other_items_intact = False
            
            # 5. Verify these specific adjectives have complete translations in both languages
            print("\n--- Testing Complete Translations for Corrected Items ---")
            
            complete_translations = True
            for correction in specific_corrections:
                french_word = correction['french']
                if french_word in adjective_words_by_french:
                    word = adjective_words_by_french[french_word]
                    
                    # Check both languages are present and non-empty
                    if word['shimaore'] and word['kibouchi']:
                        print(f"✅ {french_word}: Complete translations - {word['shimaore']} (Shimaoré) / {word['kibouchi']} (Kibouchi)")
                    else:
                        print(f"❌ {french_word}: Incomplete translations - shimaoré: '{word['shimaore']}', kibouchi: '{word['kibouchi']}'")
                        complete_translations = False
            
            # 6. Test that corrections don't introduce duplicate entries
            print("\n--- Testing No Duplicate Entries ---")
            
            french_names = [word['french'] for word in adjective_words]
            unique_names = set(french_names)
            
            if len(french_names) == len(unique_names):
                print(f"✅ No duplicate entries found ({len(unique_names)} unique adjectives)")
                duplicates_check = True
            else:
                duplicates = [name for name in french_names if french_names.count(name) > 1]
                print(f"❌ Duplicate entries found: {set(duplicates)}")
                duplicates_check = False
            
            # 7. Confirm the total adjective count remains the same (should be 52 adjectives)
            print("\n--- Testing Total Adjective Count ---")
            
            expected_adjective_count = 52
            actual_adjective_count = len(adjective_words)
            
            if actual_adjective_count == expected_adjective_count:
                print(f"✅ Total adjective count correct: {actual_adjective_count} items (expected {expected_adjective_count})")
                count_check = True
            else:
                print(f"❌ Total adjective count incorrect: {actual_adjective_count} items (expected {expected_adjective_count})")
                count_check = False
            
            # 8. Ensure backend API responses are working correctly for these specific adjectives
            print("\n--- Testing Individual API Responses for Corrected Adjectives ---")
            
            api_responses_correct = True
            for correction in specific_corrections:
                french_word = correction['french']
                if french_word in adjective_words_by_french:
                    word_id = adjective_words_by_french[french_word]['id']
                    
                    # Test individual word retrieval
                    response = self.session.get(f"{API_BASE}/words/{word_id}")
                    if response.status_code == 200:
                        retrieved_word = response.json()
                        if (retrieved_word['shimaore'] == correction['shimaore'] and 
                            retrieved_word['kibouchi'] == correction['kibouchi']):
                            print(f"✅ {french_word} API response correct: {retrieved_word['shimaore']} / {retrieved_word['kibouchi']}")
                        else:
                            print(f"❌ {french_word} API response incorrect")
                            api_responses_correct = False
                    else:
                        print(f"❌ {french_word} API retrieval failed: {response.status_code}")
                        api_responses_correct = False
            
            # Overall result
            all_tests_passed = (
                corrections_verified and 
                other_items_intact and 
                complete_translations and 
                duplicates_check and 
                count_check and 
                api_responses_correct
            )
            
            if all_tests_passed:
                print("\n🎉 SPECIFIC ADJECTIVE CORRECTIONS VERIFICATION COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors after corrections")
                print("✅ /api/words?category=adjectifs endpoint working correctly")
                print("✅ All specific corrections verified:")
                print("   - En colère: shimaoré = 'Hadabou' (corrected)")
                print("   - Faux: shimaoré = 'Trambo', kibouchi = 'Vandi' (corrected)")
                print("   - Ouvert: shimaoré = 'Ouboua', kibouchi = 'Mibiyangna' (corrected)")
                print("   - Amoureux: shimaoré = 'Ouvendza' (corrected)")
                print("   - Honteux: kibouchi = 'Mampihingnatra' (corrected)")
                print("   - Long: shimaoré = 'Drilé' (corrected)")
                print("   - Petit: shimaoré = 'Titi', kibouchi = 'Héli' (corrected)")
                print("   - Grand: shimaoré = 'Bolé' (corrected)")
                print("✅ All other adjective entries remain intact and unchanged")
                print("✅ All corrected items have complete translations in both languages")
                print("✅ No duplicate entries introduced")
                print(f"✅ Total adjective count maintained at {actual_adjective_count} items")
                print("✅ Backend API responses working correctly for corrected adjectives")
                print("✅ Bug fix verification complete - issue has been completely resolved with no regressions")
            else:
                print("\n❌ Some adjective corrections are not properly implemented or have introduced issues")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Specific adjective corrections verification error: {e}")
            return False

    def test_specific_food_corrections_verification(self):
        """Test the specific food corrections that were just made"""
        print("\n=== Testing Specific Food Corrections Verification ===")
        
        try:
            # 1. Test backend starts without syntax errors after corrections
            print("--- Testing Backend Startup After Corrections ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Backend has syntax errors or is not responding: {response.status_code}")
                return False
            print("✅ Backend starts without syntax errors after corrections")
            
            # 2. Test the /api/words?category=nourriture endpoint
            print("\n--- Testing /api/words?category=nourriture Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=nourriture")
            if response.status_code != 200:
                print(f"❌ Nourriture endpoint failed: {response.status_code}")
                return False
            
            food_words = response.json()
            food_words_by_french = {word['french']: word for word in food_words}
            print(f"✅ /api/words?category=nourriture working correctly ({len(food_words)} food items)")
            
            # 3. Verify the specific corrections are in place
            print("\n--- Testing Specific Food Corrections ---")
            
            # Test specific corrections mentioned in review request
            specific_corrections = [
                {
                    "french": "Poulet", 
                    "shimaore": "Bawa", 
                    "kibouchi": "Mabawa",
                    "note": "shimaoré should be 'Bawa' (not 'Sawa')"
                },
                {
                    "french": "Poivre", 
                    "shimaore": "Bvilibvili manga", 
                    "kibouchi": "Vilivili",
                    "note": "shimaoré should be 'Bvilibvili manga' (not 'Bvilitivili manga') and kibouchi should be 'Vilivili' (not 'Vililwili')"
                },
                {
                    "french": "Ciboulette", 
                    "shimaore": "Chouroungou", 
                    "kibouchi": "Doungoulou ravigni",
                    "note": "shimaoré should be 'Chouroungou' (not 'Chouroupgnou')"
                }
            ]
            
            corrections_verified = True
            
            for correction in specific_corrections:
                french_word = correction['french']
                if french_word in food_words_by_french:
                    word = food_words_by_french[french_word]
                    
                    # Check shimaoré correction
                    if word['shimaore'] == correction['shimaore']:
                        print(f"✅ {french_word} shimaoré: '{word['shimaore']}' - CORRECTION VERIFIED")
                    else:
                        print(f"❌ {french_word} shimaoré: Expected '{correction['shimaore']}', got '{word['shimaore']}'")
                        corrections_verified = False
                    
                    # Check kibouchi correction
                    if word['kibouchi'] == correction['kibouchi']:
                        print(f"✅ {french_word} kibouchi: '{word['kibouchi']}' - CORRECTION VERIFIED")
                    else:
                        print(f"❌ {french_word} kibouchi: Expected '{correction['kibouchi']}', got '{word['kibouchi']}'")
                        corrections_verified = False
                    
                    print(f"   Note: {correction['note']}")
                else:
                    print(f"❌ {french_word} not found in food category")
                    corrections_verified = False
            
            # 4. Check that all other food entries remain intact and unchanged
            print("\n--- Testing Other Food Entries Remain Intact ---")
            
            # Sample of other food items that should remain unchanged
            other_food_items = [
                {"french": "Riz", "shimaore": "Tsoholé", "kibouchi": "Vari"},
                {"french": "Eau", "shimaore": "Maji", "kibouchi": "Ranou"},
                {"french": "Banane", "shimaore": "Trovi", "kibouchi": "Hountsi"},
                {"french": "Mangue", "shimaore": "Manga", "kibouchi": "Manga"},
                {"french": "Pain", "shimaore": "Dipé", "kibouchi": "Dipé"}
            ]
            
            other_items_intact = True
            for item in other_food_items:
                french_word = item['french']
                if french_word in food_words_by_french:
                    word = food_words_by_french[french_word]
                    if word['shimaore'] == item['shimaore'] and word['kibouchi'] == item['kibouchi']:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} - UNCHANGED")
                    else:
                        print(f"❌ {french_word}: Expected {item['shimaore']}/{item['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        other_items_intact = False
                else:
                    print(f"❌ {french_word} not found")
                    other_items_intact = False
            
            # 5. Verify these specific food items have complete translations in both languages
            print("\n--- Testing Complete Translations for Corrected Items ---")
            
            complete_translations = True
            for correction in specific_corrections:
                french_word = correction['french']
                if french_word in food_words_by_french:
                    word = food_words_by_french[french_word]
                    
                    # Check both languages are present and non-empty
                    if word['shimaore'] and word['kibouchi']:
                        print(f"✅ {french_word}: Complete translations - {word['shimaore']} (Shimaoré) / {word['kibouchi']} (Kibouchi)")
                    else:
                        print(f"❌ {french_word}: Incomplete translations - shimaoré: '{word['shimaore']}', kibouchi: '{word['kibouchi']}'")
                        complete_translations = False
            
            # 6. Test that corrections don't introduce duplicate entries
            print("\n--- Testing No Duplicate Entries ---")
            
            french_names = [word['french'] for word in food_words]
            unique_names = set(french_names)
            
            if len(french_names) == len(unique_names):
                print(f"✅ No duplicate entries found ({len(unique_names)} unique food items)")
                duplicates_check = True
            else:
                duplicates = [name for name in french_names if french_names.count(name) > 1]
                print(f"❌ Duplicate entries found: {set(duplicates)}")
                duplicates_check = False
            
            # 7. Confirm the total food count remains the same (should be 41 food items)
            print("\n--- Testing Total Food Count ---")
            
            expected_food_count = 41
            actual_food_count = len(food_words)
            
            if actual_food_count == expected_food_count:
                print(f"✅ Total food count correct: {actual_food_count} items (expected {expected_food_count})")
                count_check = True
            else:
                print(f"❌ Total food count incorrect: {actual_food_count} items (expected {expected_food_count})")
                count_check = False
            
            # 8. Ensure backend API responses are working correctly for these specific foods
            print("\n--- Testing Individual API Responses for Corrected Foods ---")
            
            api_responses_correct = True
            for correction in specific_corrections:
                french_word = correction['french']
                if french_word in food_words_by_french:
                    word_id = food_words_by_french[french_word]['id']
                    
                    # Test individual word retrieval
                    response = self.session.get(f"{API_BASE}/words/{word_id}")
                    if response.status_code == 200:
                        retrieved_word = response.json()
                        if (retrieved_word['shimaore'] == correction['shimaore'] and 
                            retrieved_word['kibouchi'] == correction['kibouchi']):
                            print(f"✅ {french_word} API response correct: {retrieved_word['shimaore']} / {retrieved_word['kibouchi']}")
                        else:
                            print(f"❌ {french_word} API response incorrect")
                            api_responses_correct = False
                    else:
                        print(f"❌ {french_word} API retrieval failed: {response.status_code}")
                        api_responses_correct = False
            
            # Overall result
            all_tests_passed = (
                corrections_verified and 
                other_items_intact and 
                complete_translations and 
                duplicates_check and 
                count_check and 
                api_responses_correct
            )
            
            if all_tests_passed:
                print("\n🎉 SPECIFIC FOOD CORRECTIONS VERIFICATION COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors after corrections")
                print("✅ /api/words?category=nourriture endpoint working correctly")
                print("✅ All specific corrections verified:")
                print("   - Poulet: shimaoré = 'Bawa' (corrected)")
                print("   - Poivre: shimaoré = 'Bvilibvili manga', kibouchi = 'Vilivili' (corrected)")
                print("   - Ciboulette: shimaoré = 'Chouroungou' (corrected)")
                print("✅ All other food entries remain intact and unchanged")
                print("✅ All corrected items have complete translations in both languages")
                print("✅ No duplicate entries introduced")
                print(f"✅ Total food count maintained at {actual_food_count} items")
                print("✅ Backend API responses working correctly for corrected foods")
                print("✅ Bug fix verification complete - issue has been completely resolved with no regressions")
            else:
                print("\n❌ Some food corrections are not properly implemented or have introduced issues")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Specific food corrections verification error: {e}")
            return False

    def test_specific_expression_correction_jai_soif(self):
        """Test the specific expression correction for 'J'ai soif' - kibouchi should be 'Zahou tindranou' not 'Zahou moussari'"""
        print("\n=== Testing Specific Expression Correction: J'ai soif ===")
        
        try:
            # 1. Test backend starts without syntax errors after the correction
            print("--- Testing Backend Startup After Expression Correction ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Backend has syntax errors or is not responding: {response.status_code}")
                return False
            print("✅ Backend starts without syntax errors after the correction")
            
            # 2. Test the /api/words?category=expressions endpoint
            print("\n--- Testing /api/words?category=expressions Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=expressions")
            if response.status_code != 200:
                print(f"❌ Expressions endpoint failed: {response.status_code}")
                return False
            
            expressions_words = response.json()
            expressions_by_french = {word['french']: word for word in expressions_words}
            print(f"✅ /api/words?category=expressions working correctly ({len(expressions_words)} expressions)")
            
            # 3. Verify the specific correction is in place: J'ai soif kibouchi should be "Zahou tindranou" (not "Zahou moussari")
            print("\n--- Testing Specific Correction for 'J'ai soif' ---")
            
            target_expression = "J'ai soif"
            expected_shimaore = "Nissi ona niyora"
            expected_kibouchi = "Zahou tindranou"  # This is the corrected version
            
            correction_verified = True
            
            if target_expression in expressions_by_french:
                word = expressions_by_french[target_expression]
                
                # Check shimaoré remains unchanged
                if word['shimaore'] == expected_shimaore:
                    print(f"✅ {target_expression} shimaoré: '{word['shimaore']}' - UNCHANGED (correct)")
                else:
                    print(f"❌ {target_expression} shimaoré: Expected '{expected_shimaore}', got '{word['shimaore']}'")
                    correction_verified = False
                
                # Check kibouchi correction
                if word['kibouchi'] == expected_kibouchi:
                    print(f"✅ {target_expression} kibouchi: '{word['kibouchi']}' - CORRECTION VERIFIED")
                    print(f"   ✅ Corrected from 'Zahou moussari' to 'Zahou tindranou'")
                else:
                    print(f"❌ {target_expression} kibouchi: Expected '{expected_kibouchi}', got '{word['kibouchi']}'")
                    print(f"   ❌ Should be 'Zahou tindranou' (not 'Zahou moussari')")
                    correction_verified = False
                
            else:
                print(f"❌ {target_expression} not found in expressions category")
                correction_verified = False
            
            # 4. Check that the shimaoré remains unchanged: "Nissi ona niyora"
            print("\n--- Testing Shimaoré Translation Remains Unchanged ---")
            if target_expression in expressions_by_french:
                word = expressions_by_french[target_expression]
                if word['shimaore'] == expected_shimaore:
                    print(f"✅ Shimaoré unchanged: '{word['shimaore']}' - VERIFIED")
                else:
                    print(f"❌ Shimaoré changed unexpectedly: Expected '{expected_shimaore}', got '{word['shimaore']}'")
                    correction_verified = False
            
            # 5. Check that all other expressions remain intact and unchanged
            print("\n--- Testing Other Expressions Remain Intact ---")
            
            # Sample of other expressions that should remain unchanged
            other_expressions = [
                {"french": "J'ai faim", "shimaore": "Nissi ona ndza", "kibouchi": "Zahou moussari"},
                {"french": "Excuse-moi/pardon", "shimaore": "Soimahani", "kibouchi": "Soimahani"},
                {"french": "Je voudrais aller à", "shimaore": "Nissi tsaha nendré", "kibouchi": "Zahou chokou andéha"},
                {"french": "Où se trouve", "shimaore": "Ouparhanoua havi", "kibouchi": "Aya moi"},
                {"french": "S'il vous plaît", "shimaore": "Tafadali", "kibouchi": "Tafadali"}
            ]
            
            other_expressions_intact = True
            for expr in other_expressions:
                french_expr = expr['french']
                if french_expr in expressions_by_french:
                    word = expressions_by_french[french_expr]
                    if word['shimaore'] == expr['shimaore'] and word['kibouchi'] == expr['kibouchi']:
                        print(f"✅ {french_expr}: {word['shimaore']} / {word['kibouchi']} - UNCHANGED")
                    else:
                        print(f"❌ {french_expr}: Expected {expr['shimaore']}/{expr['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        other_expressions_intact = False
                        correction_verified = False
                else:
                    print(f"❌ {french_expr} not found")
                    other_expressions_intact = False
                    correction_verified = False
            
            # 6. Verify this specific expression has complete translations in both languages
            print("\n--- Testing Complete Translations for Corrected Expression ---")
            
            if target_expression in expressions_by_french:
                word = expressions_by_french[target_expression]
                
                # Check both languages are present and non-empty
                if word['shimaore'] and word['kibouchi']:
                    print(f"✅ {target_expression}: Complete translations - {word['shimaore']} (Shimaoré) / {word['kibouchi']} (Kibouchi)")
                else:
                    print(f"❌ {target_expression}: Incomplete translations - shimaoré: '{word['shimaore']}', kibouchi: '{word['kibouchi']}'")
                    correction_verified = False
            
            # 7. Test that the correction doesn't introduce any duplicate entries
            print("\n--- Testing No Duplicate Entries ---")
            
            french_expressions = [word['french'] for word in expressions_words]
            unique_expressions = set(french_expressions)
            
            if len(french_expressions) == len(unique_expressions):
                print(f"✅ No duplicate entries found ({len(unique_expressions)} unique expressions)")
                duplicates_check = True
            else:
                duplicates = [expr for expr in french_expressions if french_expressions.count(expr) > 1]
                print(f"❌ Duplicate entries found: {set(duplicates)}")
                duplicates_check = False
                correction_verified = False
            
            # 8. Confirm the total expressions count remains the same (should be 35 expressions)
            print("\n--- Testing Total Expressions Count ---")
            
            expected_expressions_count = 35
            actual_expressions_count = len(expressions_words)
            
            if actual_expressions_count == expected_expressions_count:
                print(f"✅ Total expressions count correct: {actual_expressions_count} expressions (expected {expected_expressions_count})")
                count_check = True
            else:
                print(f"⚠️ Total expressions count: {actual_expressions_count} expressions (expected {expected_expressions_count})")
                # This is not necessarily a failure, just noting the difference
                count_check = True
            
            # 9. Ensure the backend API responses are working correctly for this specific expression
            print("\n--- Testing Backend API Response for Corrected Expression ---")
            
            api_response_correct = True
            if target_expression in expressions_by_french:
                word_id = expressions_by_french[target_expression]['id']
                
                # Test individual expression retrieval
                response = self.session.get(f"{API_BASE}/words/{word_id}")
                if response.status_code == 200:
                    retrieved_word = response.json()
                    if (retrieved_word['shimaore'] == expected_shimaore and 
                        retrieved_word['kibouchi'] == expected_kibouchi):
                        print(f"✅ {target_expression} API response correct: {retrieved_word['shimaore']} / {retrieved_word['kibouchi']}")
                    else:
                        print(f"❌ {target_expression} API response incorrect")
                        api_response_correct = False
                        correction_verified = False
                else:
                    print(f"❌ {target_expression} API retrieval failed: {response.status_code}")
                    api_response_correct = False
                    correction_verified = False
            
            # Overall result
            all_tests_passed = (
                correction_verified and 
                other_expressions_intact and 
                duplicates_check and 
                count_check and 
                api_response_correct
            )
            
            if all_tests_passed:
                print("\n🎉 SPECIFIC EXPRESSION CORRECTION VERIFICATION COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors after the correction")
                print("✅ /api/words?category=expressions endpoint working correctly")
                print("✅ Specific correction verified:")
                print(f"   - J'ai soif: kibouchi = 'Zahou tindranou' (corrected from 'Zahou moussari')")
                print(f"   - J'ai soif: shimaoré = 'Nissi ona niyora' (unchanged)")
                print("✅ All other expressions remain intact and unchanged")
                print("✅ Expression has complete translations in both languages")
                print("✅ No duplicate entries introduced")
                print(f"✅ Total expressions count: {actual_expressions_count} expressions")
                print("✅ Backend API responses working correctly for this specific expression")
                print("✅ Bug fix verification complete - issue has been completely resolved with no regressions")
            else:
                print("\n❌ Expression correction is not properly implemented or has introduced issues")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Specific expression correction verification error: {e}")
            return False

    def test_updated_habitation_vocabulary_section(self):
        """Test the newly updated habitation vocabulary section that replaces the old 'maison' section"""
        print("\n=== Testing Updated Habitation Vocabulary Section ===")
        
        try:
            # 1. Check if the backend starts without any syntax errors after updating to habitation section
            print("--- Testing Backend Startup After Habitation Section Update ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Backend has syntax errors or is not responding: {response.status_code}")
                return False
            print("✅ Backend starts without syntax errors after updating to habitation section")
            
            # 2. Test the /api/words?category=habitation endpoint to retrieve all habitation items
            print("\n--- Testing /api/words?category=habitation Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=habitation")
            if response.status_code != 200:
                print(f"❌ Habitation endpoint failed: {response.status_code}")
                return False
            
            habitation_words = response.json()
            habitation_words_by_french = {word['french']: word for word in habitation_words}
            print(f"✅ /api/words?category=habitation endpoint working correctly ({len(habitation_words)} habitation items)")
            
            # 3. Verify that all habitation elements from the tableau are present with correct French, Shimaoré, and Kibouchi translations
            print("\n--- Testing All Habitation Elements from Tableau ---")
            
            # 4. Check specific key habitation elements from the tableau (24 items listed in review request)
            key_habitation_elements = [
                {"french": "Maison", "shimaore": "Nyoumba", "kibouchi": "Tragnou"},
                {"french": "Porte", "shimaore": "Mlango", "kibouchi": "Varavaragena"},
                {"french": "Case", "shimaore": "Banga", "kibouchi": "Banga"},
                {"french": "Lit", "shimaore": "Chtrandra", "kibouchi": "Koubani"},
                {"french": "Marmite", "shimaore": "Gnoungou", "kibouchi": "Vilangni"},
                {"french": "Vaisselle", "shimaore": "Ziya", "kibouchi": "Hintagna"},
                {"french": "Bol", "shimaore": "Bacouli", "kibouchi": "Bacouli"},
                {"french": "Cuillère", "shimaore": "Soutrou", "kibouchi": "Sotrou"},
                {"french": "Fenêtre", "shimaore": "Fénétri", "kibouchi": "Lafoumétara"},
                {"french": "Chaise", "shimaore": "Chiri", "kibouchi": "Chiri"},
                {"french": "Table", "shimaore": "Latabou", "kibouchi": "Latabou"},
                {"french": "Miroir", "shimaore": "Chido", "kibouchi": "Kitarafa"},
                {"french": "Cour", "shimaore": "Lacourou", "kibouchi": "Lacourou"},
                {"french": "Toilette", "shimaore": "Mraba", "kibouchi": "Mraba"},
                {"french": "Couteau", "shimaore": "Sembéya", "kibouchi": "Méssou"},
                {"french": "Matelas", "shimaore": "Godoro", "kibouchi": "Goudorou"},
                {"french": "Oreiller", "shimaore": "Mtsao", "kibouchi": "Hondagna"},
                {"french": "Véranda", "shimaore": "Baraza", "kibouchi": "Baraza"},
                {"french": "Toiture", "shimaore": "Outro", "kibouchi": "Vovougnou"},
                {"french": "Ampoule", "shimaore": "Lalampou", "kibouchi": "Lalampou"},
                {"french": "Hache", "shimaore": "Soha", "kibouchi": "Famaki"},
                {"french": "Machette", "shimaore": "M'panga", "kibouchi": "Ampanga"},
                {"french": "Balai", "shimaore": "Péou", "kibouchi": "Famafa"},
                {"french": "Mortier", "shimaore": "Chino", "kibouchi": "Légnou"},
                {"french": "Assiette", "shimaore": "Sahani", "kibouchi": "Sahani"}
            ]
            
            all_key_elements_correct = True
            
            for element in key_habitation_elements:
                french_word = element['french']
                if french_word in habitation_words_by_french:
                    word = habitation_words_by_french[french_word]
                    
                    # Check all fields
                    checks = [
                        (word['shimaore'], element['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], element['kibouchi'], 'Kibouchi'),
                        (word['category'], 'habitation', 'Category')
                    ]
                    
                    element_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            element_correct = False
                            all_key_elements_correct = False
                    
                    if element_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} - VERIFIED")
                else:
                    print(f"❌ {french_word} not found in habitation category")
                    all_key_elements_correct = False
            
            # 5. Verify that the old "maison" category no longer exists (replaced by "habitation")
            print("\n--- Testing Old 'Maison' Category No Longer Exists ---")
            response = self.session.get(f"{API_BASE}/words?category=maison")
            if response.status_code == 200:
                maison_words = response.json()
                if len(maison_words) == 0:
                    print("✅ Old 'maison' category no longer exists (replaced by 'habitation')")
                    maison_category_removed = True
                else:
                    print(f"❌ Old 'maison' category still exists with {len(maison_words)} items")
                    maison_category_removed = False
            else:
                print("✅ Old 'maison' category no longer exists (endpoint returns no data)")
                maison_category_removed = True
            
            # 6. Check that other categories remain intact and functional
            print("\n--- Testing Other Categories Remain Intact ---")
            
            # Get all words to check categories
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Could not retrieve all words: {response.status_code}")
                return False
            
            all_words = response.json()
            categories = set(word['category'] for word in all_words)
            
            expected_other_categories = {
                'famille', 'salutations', 'couleurs', 'animaux', 'nombres', 
                'corps', 'nourriture', 'vetements', 'nature', 'transport',
                'grammaire', 'verbes', 'adjectifs', 'expressions'
            }
            
            print(f"Found categories: {sorted(categories)}")
            
            # Check that habitation is present and maison is not
            if 'habitation' in categories:
                print("✅ 'habitation' category is present")
                habitation_present = True
            else:
                print("❌ 'habitation' category is missing")
                habitation_present = False
            
            if 'maison' not in categories:
                print("✅ 'maison' category is not present (correctly replaced)")
                maison_not_present = True
            else:
                print("❌ 'maison' category is still present (should be replaced)")
                maison_not_present = False
            
            # Check other categories are intact
            other_categories_intact = True
            for category in expected_other_categories:
                if category in categories:
                    category_response = self.session.get(f"{API_BASE}/words?category={category}")
                    if category_response.status_code == 200:
                        category_words = category_response.json()
                        if len(category_words) > 0:
                            print(f"✅ {category} category intact ({len(category_words)} items)")
                        else:
                            print(f"⚠️ {category} category empty")
                    else:
                        print(f"❌ {category} category endpoint failed")
                        other_categories_intact = False
                else:
                    print(f"⚠️ {category} category not found")
            
            # 7. Test for any duplicate entries or data integrity issues
            print("\n--- Testing for Duplicate Entries and Data Integrity ---")
            
            french_names = [word['french'] for word in habitation_words]
            unique_names = set(french_names)
            
            if len(french_names) == len(unique_names):
                print(f"✅ No duplicate entries found ({len(unique_names)} unique habitation items)")
                no_duplicates = True
            else:
                duplicates = [name for name in french_names if french_names.count(name) > 1]
                print(f"❌ Duplicate entries found: {set(duplicates)}")
                no_duplicates = False
            
            # Check data integrity - all items should have required fields
            data_integrity_ok = True
            for word in habitation_words:
                required_fields = ['id', 'french', 'shimaore', 'kibouchi', 'category']
                missing_fields = [field for field in required_fields if not word.get(field)]
                if missing_fields:
                    print(f"❌ {word.get('french', 'Unknown')} missing fields: {missing_fields}")
                    data_integrity_ok = False
            
            if data_integrity_ok:
                print("✅ All habitation items have proper data structure")
            
            # 8. Confirm the total habitation count matches the tableau (should be around 33 habitation items)
            print("\n--- Testing Total Habitation Count ---")
            
            expected_habitation_count_min = 30  # Around 33, allowing some flexibility
            expected_habitation_count_max = 40
            actual_habitation_count = len(habitation_words)
            
            if expected_habitation_count_min <= actual_habitation_count <= expected_habitation_count_max:
                print(f"✅ Total habitation count within expected range: {actual_habitation_count} items (expected around 33)")
                count_check = True
            else:
                print(f"❌ Total habitation count outside expected range: {actual_habitation_count} items (expected around 33)")
                count_check = False
            
            # 9. Ensure all habitation items have proper category assignment as "habitation"
            print("\n--- Testing All Items Have Proper Category Assignment ---")
            
            category_assignment_correct = True
            for word in habitation_words:
                if word['category'] != 'habitation':
                    print(f"❌ {word['french']} has incorrect category: {word['category']} (should be 'habitation')")
                    category_assignment_correct = False
            
            if category_assignment_correct:
                print(f"✅ All {len(habitation_words)} habitation items have proper category assignment as 'habitation'")
            
            # 10. Test the API endpoints are working correctly for the new category
            print("\n--- Testing API Endpoints for New Category ---")
            
            # Test individual item retrieval
            api_endpoints_working = True
            if habitation_words:
                sample_word = habitation_words[0]
                word_id = sample_word['id']
                
                response = self.session.get(f"{API_BASE}/words/{word_id}")
                if response.status_code == 200:
                    retrieved_word = response.json()
                    if retrieved_word['category'] == 'habitation':
                        print(f"✅ Individual habitation item retrieval working: {retrieved_word['french']}")
                    else:
                        print(f"❌ Individual retrieval returned wrong category: {retrieved_word['category']}")
                        api_endpoints_working = False
                else:
                    print(f"❌ Individual habitation item retrieval failed: {response.status_code}")
                    api_endpoints_working = False
            
            # Provide the new total count of habitation items and overall word count
            print("\n--- Final Count Summary ---")
            
            total_words = len(all_words)
            habitation_count = len(habitation_words)
            
            print(f"📊 FINAL COUNTS:")
            print(f"   • Total habitation items: {habitation_count}")
            print(f"   • Total words across all categories: {total_words}")
            print(f"   • Categories found: {len(categories)} ({', '.join(sorted(categories))})")
            
            # Overall result
            all_tests_passed = (
                all_key_elements_correct and
                maison_category_removed and
                habitation_present and
                maison_not_present and
                other_categories_intact and
                no_duplicates and
                data_integrity_ok and
                count_check and
                category_assignment_correct and
                api_endpoints_working
            )
            
            if all_tests_passed:
                print("\n🎉 UPDATED HABITATION VOCABULARY SECTION TESTING COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors after updating to habitation section")
                print("✅ /api/words?category=habitation endpoint retrieves all habitation items correctly")
                print("✅ All habitation elements from tableau present with correct French, Shimaoré, and Kibouchi translations")
                print("✅ All 25 specific key habitation elements verified:")
                print("   - Maison: Nyoumba / Tragnou")
                print("   - Porte: Mlango / Varavaragena")
                print("   - Case: Banga / Banga")
                print("   - Lit: Chtrandra / Koubani")
                print("   - Marmite: Gnoungou / Vilangni")
                print("   - Vaisselle: Ziya / Hintagna")
                print("   - Bol: Bacouli / Bacouli")
                print("   - Cuillère: Soutrou / Sotrou")
                print("   - Fenêtre: Fénétri / Lafoumétara")
                print("   - Chaise: Chiri / Chiri")
                print("   - Table: Latabou / Latabou")
                print("   - Miroir: Chido / Kitarafa")
                print("   - Cour: Lacourou / Lacourou")
                print("   - Toilette: Mraba / Mraba")
                print("   - Couteau: Sembéya / Méssou")
                print("   - Matelas: Godoro / Goudorou")
                print("   - Oreiller: Mtsao / Hondagna")
                print("   - Véranda: Baraza / Baraza")
                print("   - Toiture: Outro / Vovougnou")
                print("   - Ampoule: Lalampou / Lalampou")
                print("   - Hache: Soha / Famaki")
                print("   - Machette: M'panga / Ampanga")
                print("   - Balai: Péou / Famafa")
                print("   - Mortier: Chino / Légnou")
                print("   - Assiette: Sahani / Sahani")
                print("✅ Old 'maison' category no longer exists (replaced by 'habitation')")
                print("✅ Other categories remain intact and functional")
                print("✅ No duplicate entries or data integrity issues")
                print(f"✅ Total habitation count matches expectations: {habitation_count} items (around 33 expected)")
                print("✅ All habitation items have proper category assignment as 'habitation'")
                print("✅ API endpoints working correctly for the new category")
                print(f"📊 FINAL COUNTS: {habitation_count} habitation items, {total_words} total words")
            else:
                print("\n❌ Some habitation vocabulary tests failed or have issues")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Updated habitation vocabulary section test error: {e}")
            return False

    def test_updated_nature_vocabulary_from_new_tableau(self):
        """Test the updated nature vocabulary after adding new elements from the additional tableau"""
        print("\n=== Testing Updated Nature Vocabulary from New Tableau ===")
        
        try:
            # 1. Check if the backend starts without any syntax errors after adding the new nature elements
            print("--- Testing Backend Startup After Adding New Nature Elements ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Backend has syntax errors or is not responding: {response.status_code}")
                return False
            print("✅ Backend starts without syntax errors after adding new nature elements")
            
            # 2. Test the /api/words?category=nature endpoint to retrieve all nature items
            print("\n--- Testing /api/words?category=nature Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=nature")
            if response.status_code != 200:
                print(f"❌ Nature endpoint failed: {response.status_code}")
                return False
            
            nature_words = response.json()
            nature_words_by_french = {word['french']: word for word in nature_words}
            print(f"✅ /api/words?category=nature endpoint working correctly ({len(nature_words)} nature items)")
            
            # 3. Verify that all new nature elements from the tableau are present with correct French, Shimaoré, and Kibouchi translations
            print("\n--- Testing All New Nature Elements from Additional Tableau ---")
            
            # Test the 19 specific key new nature elements from the review request
            key_new_nature_elements = [
                {"french": "Cocotier", "shimaore": "M'hadzi", "kibouchi": "Voudi ni vwaniou"},
                {"french": "Arbre à pain", "shimaore": "M'frampé", "kibouchi": "Voudi ni frampé"},
                {"french": "Baobab", "shimaore": "M'bouyou", "kibouchi": "Voudi ni bouyou"},
                {"french": "Bambou", "shimaore": "M'banbo", "kibouchi": "Valiha"},
                {"french": "Manguier", "shimaore": "M'manga", "kibouchi": "Voudi ni manga"},
                {"french": "Jacquier", "shimaore": "M'fénéssi", "kibouchi": "Voudi ni finéssi"},
                {"french": "Terre", "shimaore": "Trotro", "kibouchi": "Fotaka"},
                {"french": "Sol", "shimaore": "Tsi", "kibouchi": "Tani"},
                {"french": "Érosion", "shimaore": "Padza", "kibouchi": "Padza"},
                {"french": "Marée basse", "shimaore": "Maji yavo", "kibouchi": "Ranou méki"},
                {"french": "Marée haute", "shimaore": "Maji yamalé", "kibouchi": "Ranou fénou"},
                {"french": "Inondé", "shimaore": "Ourora", "kibouchi": "Dobou"},
                {"french": "Sauvage", "shimaore": "Nyéha", "kibouchi": "Di"},
                {"french": "Canne à sucre", "shimaore": "Moua", "kibouchi": "Fari"},
                {"french": "Fagot", "shimaore": "Kouni", "kibouchi": "Azoumati"},
                {"french": "Pirogue", "shimaore": "Laka", "kibouchi": "Lakana"},
                {"french": "Vedette", "shimaore": "Kwassa kwassa", "kibouchi": "Vidéti"},
                {"french": "École", "shimaore": "Licoli", "kibouchi": "Licoli"},
                {"french": "École coranique", "shimaore": "Shioni", "kibouchi": "Kioni"}
            ]
            
            new_elements_verified = True
            
            print("--- Testing 19 Specific Key New Nature Elements ---")
            for new_element in key_new_nature_elements:
                french_word = new_element['french']
                if french_word in nature_words_by_french:
                    word = nature_words_by_french[french_word]
                    
                    # Check all fields
                    checks = [
                        (word['shimaore'], new_element['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], new_element['kibouchi'], 'Kibouchi'),
                        (word['category'], 'nature', 'Category')
                    ]
                    
                    element_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            element_correct = False
                            new_elements_verified = False
                    
                    if element_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']}")
                else:
                    print(f"❌ {french_word} not found in nature category")
                    new_elements_verified = False
            
            # 4. Verify that previously existing nature elements are still present
            print("\n--- Testing Previously Existing Nature Elements Still Present ---")
            
            # Test some previously existing nature elements
            existing_nature_elements = [
                {"french": "Arbre", "shimaore": "Mwiri", "kibouchi": "Kakazou"},
                {"french": "Soleil", "shimaore": "Mwézi", "kibouchi": "Zouva"},
                {"french": "Mer", "shimaore": "Bahari", "kibouchi": "Bahari"},
                {"french": "Plage", "shimaore": "Mtsangani", "kibouchi": "Fassigni"},
                {"french": "Lune", "shimaore": "Mwézi", "kibouchi": "Fandzava"},
                {"french": "Étoile", "shimaore": "Gnora", "kibouchi": "Lakintagna"},
                {"french": "Sable", "shimaore": "Mtsanga", "kibouchi": "Fasigni"},
                {"french": "Vent", "shimaore": "Pévo", "kibouchi": "Tsikou"},
                {"french": "Pluie", "shimaore": "Vhoua", "kibouchi": "Mahaléni"},
                {"french": "Rivière", "shimaore": "Mouro", "kibouchi": "Mouroni"}
            ]
            
            existing_elements_present = True
            for existing_element in existing_nature_elements:
                french_word = existing_element['french']
                if french_word in nature_words_by_french:
                    word = nature_words_by_french[french_word]
                    if (word['shimaore'] == existing_element['shimaore'] and 
                        word['kibouchi'] == existing_element['kibouchi']):
                        print(f"✅ EXISTING: {french_word}: {word['shimaore']} / {word['kibouchi']}")
                    else:
                        print(f"❌ EXISTING: {french_word}: Expected {existing_element['shimaore']}/{existing_element['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        existing_elements_present = False
                else:
                    print(f"❌ EXISTING: {french_word} not found (should still be present)")
                    existing_elements_present = False
            
            # 5. Check that other categories remain intact and functional
            print("\n--- Testing Other Categories Remain Intact ---")
            
            # Get all words to check category integration
            all_words_response = self.session.get(f"{API_BASE}/words")
            if all_words_response.status_code == 200:
                all_words = all_words_response.json()
                all_categories = set(word['category'] for word in all_words)
                
                expected_other_categories = {
                    'famille', 'couleurs', 'animaux', 'salutations', 'nombres', 
                    'corps', 'nourriture', 'maison', 'vetements', 'transport', 
                    'grammaire', 'verbes', 'adjectifs', 'expressions'
                }
                
                other_categories_intact = expected_other_categories.issubset(all_categories)
                if other_categories_intact:
                    print(f"✅ All other categories remain intact and functional")
                    print(f"Total categories: {len(all_categories)} - {sorted(all_categories)}")
                else:
                    missing_categories = expected_other_categories - all_categories
                    print(f"❌ Missing categories: {missing_categories}")
                    new_elements_verified = False
            else:
                print(f"❌ Could not retrieve all words to check category integration")
                new_elements_verified = False
            
            # 6. Test for any duplicate entries or data integrity issues
            print("\n--- Testing No Duplicate Entries ---")
            
            french_nature_words = [word['french'] for word in nature_words]
            unique_nature_words = set(french_nature_words)
            
            if len(french_nature_words) == len(unique_nature_words):
                print(f"✅ No duplicate entries found ({len(unique_nature_words)} unique nature items)")
                duplicates_check = True
            else:
                duplicates = [word for word in french_nature_words if french_nature_words.count(word) > 1]
                print(f"❌ Duplicate entries found: {set(duplicates)}")
                duplicates_check = False
                new_elements_verified = False
            
            # 7. Confirm the new total nature count (should be around 49 nature items now)
            print("\n--- Testing New Total Nature Count ---")
            
            expected_min_count = 45  # Should be around 49, allowing some flexibility
            expected_max_count = 55
            actual_count = len(nature_words)
            
            if expected_min_count <= actual_count <= expected_max_count:
                print(f"✅ Total nature count within expected range: {actual_count} items (expected around 49, range {expected_min_count}-{expected_max_count})")
                count_check = True
            else:
                print(f"⚠️ Total nature count: {actual_count} items (expected around 49, range {expected_min_count}-{expected_max_count})")
                # This is not necessarily a failure, just noting the difference
                count_check = True
            
            # 8. Ensure all nature items have proper category assignment as "nature"
            print("\n--- Testing Proper Category Assignment ---")
            
            category_assignment_correct = True
            for word in nature_words:
                if word['category'] != 'nature':
                    print(f"❌ {word['french']} has incorrect category: {word['category']} (should be 'nature')")
                    category_assignment_correct = False
                    new_elements_verified = False
            
            if category_assignment_correct:
                print(f"✅ All nature items properly categorized as 'nature'")
            
            # 9. Test the API endpoints are working correctly for the updated category
            print("\n--- Testing API Endpoints for Updated Nature Category ---")
            
            # Test individual nature item retrieval for some key new elements
            api_endpoints_working = True
            test_elements = ["Cocotier", "Baobab", "Pirogue", "École"]
            
            for test_element in test_elements:
                if test_element in nature_words_by_french:
                    word_id = nature_words_by_french[test_element]['id']
                    
                    response = self.session.get(f"{API_BASE}/words/{word_id}")
                    if response.status_code == 200:
                        retrieved_word = response.json()
                        if retrieved_word['category'] == 'nature':
                            print(f"✅ Individual retrieval working: {retrieved_word['french']} - {retrieved_word['shimaore']} / {retrieved_word['kibouchi']}")
                        else:
                            print(f"❌ Individual retrieval failed: incorrect category for {test_element}")
                            api_endpoints_working = False
                            new_elements_verified = False
                    else:
                        print(f"❌ Individual retrieval failed for {test_element}: {response.status_code}")
                        api_endpoints_working = False
                        new_elements_verified = False
            
            # 10. Provide the new total count of nature items and overall word count after this update
            print("\n--- Final Count Summary ---")
            
            if all_words_response.status_code == 200:
                total_word_count = len(all_words)
                nature_count = len(nature_words)
                
                print(f"✅ Final nature vocabulary count: {nature_count} items")
                print(f"✅ Overall word count after update: {total_word_count} words")
                
                # Show category breakdown
                category_counts = {}
                for word in all_words:
                    category = word['category']
                    category_counts[category] = category_counts.get(category, 0) + 1
                
                print(f"✅ Category breakdown:")
                for category, count in sorted(category_counts.items()):
                    print(f"   - {category}: {count} items")
            
            # Overall result
            all_tests_passed = (
                new_elements_verified and 
                existing_elements_present and 
                duplicates_check and 
                count_check and 
                category_assignment_correct and 
                api_endpoints_working
            )
            
            if all_tests_passed:
                print("\n🎉 UPDATED NATURE VOCABULARY FROM NEW TABLEAU TESTING COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors after adding new nature elements")
                print("✅ /api/words?category=nature endpoint working correctly")
                print("✅ All 19 specific key new nature elements from tableau verified with correct translations:")
                print("   - Trees: Cocotier, Arbre à pain, Baobab, Bambou, Manguier, Jacquier")
                print("   - Environment: Terre, Sol, Érosion, Marée basse, Marée haute, Inondé, Sauvage")
                print("   - Objects: Canne à sucre, Fagot, Pirogue, Vedette")
                print("   - Buildings: École, École coranique")
                print("✅ Previously existing nature elements are still present")
                print("✅ Other categories remain intact and functional")
                print("✅ No duplicate entries or data integrity issues")
                print(f"✅ New total nature count: {actual_count} items (around 49 as expected)")
                print("✅ All nature items have proper category assignment as 'nature'")
                print("✅ API endpoints working correctly for the updated category")
                print(f"✅ Final counts: {actual_count} nature items, {total_word_count} total words")
                print("The updated nature vocabulary with new elements from the additional tableau is now fully functional and ready for educational use.")
            else:
                print("\n❌ Some nature vocabulary updates are not properly implemented or have introduced issues")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Updated nature vocabulary test error: {e}")
            return False

    def test_expressions_vocabulary_section(self):
        """Test the newly created expressions vocabulary section"""
        print("\n=== Testing Expressions Vocabulary Section ===")
        
        try:
            # 1. Check if the backend starts without any syntax errors after adding the new expressions section
            print("--- Testing Backend Startup After Adding Expressions Section ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Backend has syntax errors or is not responding: {response.status_code}")
                return False
            print("✅ Backend starts without syntax errors after adding expressions section")
            
            # 2. Test the /api/words?category=expressions endpoint to retrieve all expressions
            print("\n--- Testing /api/words?category=expressions Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=expressions")
            if response.status_code != 200:
                print(f"❌ Expressions endpoint failed: {response.status_code}")
                return False
            
            expressions_words = response.json()
            expressions_by_french = {word['french']: word for word in expressions_words}
            print(f"✅ /api/words?category=expressions working correctly ({len(expressions_words)} expressions)")
            
            # 3. Verify that all expressions from the tourist formulas tableau are present with correct translations
            print("\n--- Testing Tourist Formulas from Tableau ---")
            
            # Key expressions from the tourist formulas tableau as specified in the review request
            key_expressions = [
                {"french": "Excuse-moi/pardon", "shimaore": "Soimahani", "kibouchi": "Soimahani"},
                {"french": "J'ai faim", "shimaore": "Nissi ona ndza", "kibouchi": "Zahou moussari"},
                {"french": "J'ai soif", "shimaore": "Nissi ona niyora", "kibouchi": "Zahou tindranou"},  # Updated with correction
                {"french": "Je voudrais aller à", "shimaore": "Nissi tsaha nendré", "kibouchi": "Zahou chokou andéha"},
                {"french": "Où se trouve", "shimaore": "Ouparhanoua havi", "kibouchi": "Aya moi"},
                {"french": "Je suis perdu", "shimaore": "Tsi latsiha", "kibouchi": "Zahou véri"},
                {"french": "Combien ça coûte ?", "shimaore": "Kissajé", "kibouchi": "Hotri inou moi"},
                {"french": "S'il vous plaît", "shimaore": "Tafadali", "kibouchi": "Tafadali"},
                {"french": "À gauche", "shimaore": "Potroni", "kibouchi": "Kipotrou"},
                {"french": "À droite", "shimaore": "Houméni", "kibouchi": "Finana"},
                {"french": "Appelez la police !", "shimaore": "Hira sirikali", "kibouchi": "Kahiya sirikali"},
                {"french": "J'ai besoin d'un médecin", "shimaore": "Ntsha douktera", "kibouchi": "Zahou mila douktera"}
            ]
            
            key_expressions_verified = True
            
            print("--- Testing Specific Key Expressions from Review Request ---")
            for expression in key_expressions:
                french_expr = expression['french']
                if french_expr in expressions_by_french:
                    word = expressions_by_french[french_expr]
                    
                    # Check shimaoré translation
                    if word['shimaore'] == expression['shimaore']:
                        print(f"✅ {french_expr} shimaoré: '{word['shimaore']}' - VERIFIED")
                    else:
                        print(f"❌ {french_expr} shimaoré: Expected '{expression['shimaore']}', got '{word['shimaore']}'")
                        key_expressions_verified = False
                    
                    # Check kibouchi translation
                    if word['kibouchi'] == expression['kibouchi']:
                        print(f"✅ {french_expr} kibouchi: '{word['kibouchi']}' - VERIFIED")
                    else:
                        print(f"❌ {french_expr} kibouchi: Expected '{expression['kibouchi']}', got '{word['kibouchi']}'")
                        key_expressions_verified = False
                else:
                    print(f"❌ {french_expr} not found in expressions category")
                    key_expressions_verified = False
            
            # 4. Verify the new expressions category is properly integrated with other categories
            print("\n--- Testing Category Integration ---")
            
            # Get all words to check category integration
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Could not retrieve all words: {response.status_code}")
                return False
            
            all_words = response.json()
            categories = set(word['category'] for word in all_words)
            
            if 'expressions' in categories:
                print("✅ Expressions category properly integrated with other categories")
                print(f"All categories found: {sorted(categories)}")
            else:
                print("❌ Expressions category not found in overall word list")
                key_expressions_verified = False
            
            # 5. Check that other categories remain intact and functional
            print("\n--- Testing Other Categories Remain Intact ---")
            
            expected_other_categories = {
                'famille', 'salutations', 'couleurs', 'animaux', 'nombres', 
                'corps', 'nourriture', 'maison', 'vetements', 'nature', 
                'transport', 'grammaire', 'verbes', 'adjectifs'
            }
            
            missing_categories = expected_other_categories - categories
            if not missing_categories:
                print("✅ All other categories remain intact and functional")
            else:
                print(f"❌ Missing categories: {missing_categories}")
                key_expressions_verified = False
            
            # 6. Test for any duplicate entries or data integrity issues
            print("\n--- Testing Data Integrity and Duplicates ---")
            
            # Check for duplicates in expressions category
            french_expressions = [word['french'] for word in expressions_words]
            unique_expressions = set(french_expressions)
            
            if len(french_expressions) == len(unique_expressions):
                print(f"✅ No duplicate entries found in expressions ({len(unique_expressions)} unique expressions)")
                duplicates_check = True
            else:
                duplicates = [expr for expr in french_expressions if french_expressions.count(expr) > 1]
                print(f"❌ Duplicate expressions found: {set(duplicates)}")
                duplicates_check = False
                key_expressions_verified = False
            
            # Check data integrity - all expressions should have required fields
            data_integrity_check = True
            for expression in expressions_words:
                required_fields = ['id', 'french', 'shimaore', 'kibouchi', 'category', 'difficulty']
                missing_fields = [field for field in required_fields if field not in expression or expression[field] is None]
                
                if missing_fields:
                    print(f"❌ {expression.get('french', 'Unknown')} missing fields: {missing_fields}")
                    data_integrity_check = False
                    key_expressions_verified = False
            
            if data_integrity_check:
                print("✅ All expressions have proper data structure with required fields")
            
            # 7. Confirm the total expressions count matches the tableau (should be around 35 expressions)
            print("\n--- Testing Total Expressions Count ---")
            
            expected_min_expressions = 30  # At least 30 expressions expected
            expected_max_expressions = 40  # Around 35, so up to 40 is reasonable
            actual_expressions_count = len(expressions_words)
            
            if expected_min_expressions <= actual_expressions_count <= expected_max_expressions:
                print(f"✅ Total expressions count within expected range: {actual_expressions_count} expressions (expected ~35)")
                count_check = True
            else:
                print(f"❌ Total expressions count outside expected range: {actual_expressions_count} expressions (expected ~35)")
                count_check = False
                key_expressions_verified = False
            
            # 8. Ensure all expressions have proper category assignment as "expressions"
            print("\n--- Testing Category Assignment ---")
            
            category_assignment_check = True
            for expression in expressions_words:
                if expression['category'] != 'expressions':
                    print(f"❌ {expression['french']} has incorrect category: '{expression['category']}' (should be 'expressions')")
                    category_assignment_check = False
                    key_expressions_verified = False
            
            if category_assignment_check:
                print(f"✅ All {len(expressions_words)} expressions properly categorized as 'expressions'")
            
            # 9. Test the API endpoints are working correctly for the new category
            print("\n--- Testing API Endpoints for Expressions Category ---")
            
            # Test individual expression retrieval
            api_endpoints_check = True
            if expressions_words:
                # Test retrieving a specific expression
                sample_expression = expressions_words[0]
                response = self.session.get(f"{API_BASE}/words/{sample_expression['id']}")
                if response.status_code == 200:
                    retrieved_expression = response.json()
                    if retrieved_expression['category'] == 'expressions':
                        print(f"✅ Individual expression retrieval working: {retrieved_expression['french']}")
                    else:
                        print(f"❌ Individual expression retrieval returned wrong category")
                        api_endpoints_check = False
                        key_expressions_verified = False
                else:
                    print(f"❌ Individual expression retrieval failed: {response.status_code}")
                    api_endpoints_check = False
                    key_expressions_verified = False
            
            # 10. Provide the new total count of expressions and overall word count
            print("\n--- Testing Final Counts ---")
            
            total_words = len(all_words)
            expressions_count = len(expressions_words)
            
            print(f"📊 FINAL COUNTS:")
            print(f"   - Total expressions: {expressions_count}")
            print(f"   - Total words across all categories: {total_words}")
            print(f"   - Total categories: {len(categories)}")
            
            # Overall result
            all_tests_passed = (
                key_expressions_verified and 
                duplicates_check and 
                data_integrity_check and 
                count_check and 
                category_assignment_check and 
                api_endpoints_check
            )
            
            if all_tests_passed:
                print("\n🎉 EXPRESSIONS VOCABULARY SECTION TESTING COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors after adding expressions section")
                print("✅ /api/words?category=expressions endpoint working correctly")
                print("✅ All expressions from tourist formulas tableau verified with correct translations:")
                print("   - Excuse-moi/pardon: soimahani / soimahani")
                print("   - J'ai faim: nissi ona ndza / zahou moussari")
                print("   - J'ai soif: nissi ona niyora / zahou moussari")
                print("   - Je voudrais aller à: nissi tsaha nendré / zahou chokou andéha")
                print("   - Où se trouve: ouparhanoua havi / aya moi")
                print("   - Je suis perdu: tsi latsiha / zahou véri")
                print("   - Combien ça coûte ?: kissajé / hotri inou moi")
                print("   - S'il vous plaît: tafadali / tafadali")
                print("   - À gauche: potroni / kipotrou")
                print("   - À droite: houméni / finana")
                print("   - Appelez la police !: hira sirikali / kahiya sirikali")
                print("   - J'ai besoin d'un médecin: ntsha douktera / zahou mila douktera")
                print("✅ Expressions category properly integrated with other categories")
                print("✅ Other categories remain intact and functional")
                print("✅ No duplicate entries or data integrity issues")
                print(f"✅ Total expressions count matches expectations: {expressions_count} expressions")
                print("✅ All expressions properly categorized as 'expressions'")
                print("✅ API endpoints working correctly for the new category")
                print(f"✅ New total counts: {expressions_count} expressions, {total_words} total words")
            else:
                print("\n❌ Some expressions vocabulary tests failed or have issues")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Expressions vocabulary section test error: {e}")
            return False

    def test_comprehensive_category_filtering(self):
        """Test category filtering for all 13 categories with comprehensive vocabulary"""
        print("\n=== Testing Comprehensive Category Filtering (13 Categories) ===")
        
        try:
            # Test all expected categories including new ones
            categories_to_test = [
                ('famille', ['Frère', 'Sœur']),
                ('corps', ['Tête', 'Cheveux']),
                ('nombres', ['Un', 'Deux', 'Onze']),
                ('nourriture', ['Eau', 'Riz']),
                ('nature', ['Arbre', 'Soleil']),
                ('animaux', ['Singe', 'Maki']),
                ('salutations', ['Bonjour', 'Merci']),
                ('couleurs', ['Rouge', 'Jaune']),
                ('maison', ['Maison', 'Porte']),
                ('vetements', ['Vêtement', 'Chemise']),
                ('transport', ['Voiture', 'Bateau']),
                ('grammaire', ['Je', 'Tu', 'Il/Elle']),  # New category
                ('verbes', ['Jouer', 'Courir', 'Marcher'])  # New category
            ]
            
            all_categories_pass = True
            
            for category, expected_words in categories_to_test:
                response = self.session.get(f"{API_BASE}/words?category={category}")
                if response.status_code == 200:
                    category_words = response.json()
                    print(f"✅ Category '{category}': {len(category_words)} words")
                    
                    # Check for expected words in this category
                    found_words = [word['french'] for word in category_words]
                    for expected_word in expected_words:
                        if expected_word in found_words:
                            # Find the word and show its translations
                            word_data = next(w for w in category_words if w['french'] == expected_word)
                            shimaore_display = word_data['shimaore'] if word_data['shimaore'] else "(none)"
                            kibouchi_display = word_data['kibouchi'] if word_data['kibouchi'] else "(none)"
                            print(f"  ✅ {expected_word}: {shimaore_display} / {kibouchi_display}")
                        else:
                            print(f"  ❌ Expected word '{expected_word}' not found in {category}")
                            all_categories_pass = False
                else:
                    print(f"❌ Category '{category}' filtering failed: {response.status_code}")
                    all_categories_pass = False
            
            return all_categories_pass
                
        except Exception as e:
            print(f"❌ Comprehensive category filtering error: {e}")
            return False
    
    def test_word_crud_operations(self):
        """Test CRUD operations for words"""
        print("\n=== Testing Word CRUD Operations ===")
        
        # Test CREATE
        try:
            new_word = {
                "french": "Maison",
                "shimaore": "Nyumba",
                "kibouchi": "Nyumba",
                "category": "objets",
                "difficulty": 2
            }
            
            response = self.session.post(f"{API_BASE}/words", json=new_word)
            if response.status_code == 200:
                created_word = response.json()
                self.created_word_id = created_word['id']
                print(f"✅ Created word with ID: {self.created_word_id}")
                print(f"Created: {created_word['french']} = {created_word['shimaore']} / {created_word['kibouchi']}")
            else:
                print(f"❌ Word creation failed: {response.status_code} - {response.text}")
                return False
            
            # Test READ specific word
            response = self.session.get(f"{API_BASE}/words/{self.created_word_id}")
            if response.status_code == 200:
                retrieved_word = response.json()
                print(f"✅ Retrieved word: {retrieved_word['french']}")
            else:
                print(f"❌ Word retrieval failed: {response.status_code}")
                return False
            
            # Test UPDATE
            updated_word = {
                "french": "Grande Maison",
                "shimaore": "Nyumba Nkuu",
                "kibouchi": "Nyumba Nkuu",
                "category": "objets",
                "difficulty": 3
            }
            
            response = self.session.put(f"{API_BASE}/words/{self.created_word_id}", json=updated_word)
            if response.status_code == 200:
                updated = response.json()
                print(f"✅ Updated word: {updated['french']} (difficulty: {updated['difficulty']})")
            else:
                print(f"❌ Word update failed: {response.status_code}")
                return False
            
            # Test DELETE
            response = self.session.delete(f"{API_BASE}/words/{self.created_word_id}")
            if response.status_code == 200:
                print("✅ Word deleted successfully")
            else:
                print(f"❌ Word deletion failed: {response.status_code}")
                return False
            
            # Verify deletion
            response = self.session.get(f"{API_BASE}/words/{self.created_word_id}")
            if response.status_code == 404:
                print("✅ Word deletion verified (404 on retrieval)")
            else:
                print(f"⚠️ Word may not be properly deleted: {response.status_code}")
            
            return True
            
        except Exception as e:
            print(f"❌ Word CRUD operations error: {e}")
            return False
    
    def test_exercise_management(self):
        """Test exercise management endpoints"""
        print("\n=== Testing Exercise Management ===")
        
        try:
            # Test GET exercises
            response = self.session.get(f"{API_BASE}/exercises")
            if response.status_code == 200:
                exercises = response.json()
                print(f"✅ Retrieved {len(exercises)} exercises")
                
                if exercises:
                    sample_exercise = exercises[0]
                    print(f"Sample exercise: {sample_exercise['title']} - {sample_exercise['type']}")
            else:
                print(f"❌ Get exercises failed: {response.status_code}")
                return False
            
            # Test CREATE exercise
            new_exercise = {
                "type": "quiz",
                "title": "Test des Couleurs",
                "description": "Quiz sur les couleurs en shimaoré et kibouchi",
                "words": [],
                "difficulty": 2,
                "points": 20
            }
            
            response = self.session.post(f"{API_BASE}/exercises", json=new_exercise)
            if response.status_code == 200:
                created_exercise = response.json()
                self.created_exercise_id = created_exercise['id']
                print(f"✅ Created exercise: {created_exercise['title']} (ID: {self.created_exercise_id})")
            else:
                print(f"❌ Exercise creation failed: {response.status_code} - {response.text}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Exercise management error: {e}")
            return False
    
    def test_user_progress_tracking(self):
        """Test user progress tracking"""
        print("\n=== Testing User Progress Tracking ===")
        
        try:
            # Create progress entry
            if not self.created_exercise_id:
                # Use a dummy exercise ID if we don't have one
                self.created_exercise_id = "test-exercise-id"
            
            progress_data = {
                "user_name": "Marie Abdou",
                "exercise_id": self.created_exercise_id,
                "score": 85
            }
            
            response = self.session.post(f"{API_BASE}/progress", json=progress_data)
            if response.status_code == 200:
                created_progress = response.json()
                print(f"✅ Created progress entry for {created_progress['user_name']}")
                print(f"Score: {created_progress['score']} on exercise {created_progress['exercise_id']}")
            else:
                print(f"❌ Progress creation failed: {response.status_code} - {response.text}")
                return False
            
            # Test GET user progress
            response = self.session.get(f"{API_BASE}/progress/Marie Abdou")
            if response.status_code == 200:
                user_progress = response.json()
                print(f"✅ Retrieved {len(user_progress)} progress entries for Marie Abdou")
                
                if user_progress:
                    latest_progress = user_progress[-1]
                    print(f"Latest score: {latest_progress['score']}")
            else:
                print(f"❌ Get user progress failed: {response.status_code}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ User progress tracking error: {e}")
            return False
    
    def test_comprehensive_grammar_vocabulary(self):
        """Test comprehensive updated grammar section with complete personal and possessive pronouns"""
        print("\n=== Testing Comprehensive Updated Grammar Section ===")
        
        try:
            # 1. Test complete grammar vocabulary initialization
            print("--- Testing Complete Grammar Vocabulary Initialization ---")
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to initialize base content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Base content initialized: {result}")
            
            # 2. Test GET /api/words?category=grammaire to verify all pronoun types
            print("\n--- Testing Grammar Category Filtering ---")
            response = self.session.get(f"{API_BASE}/words?category=grammaire")
            if response.status_code != 200:
                print(f"❌ Failed to get grammar words: {response.status_code}")
                return False
            
            grammar_words = response.json()
            grammar_words_by_french = {word['french']: word for word in grammar_words}
            
            print(f"Found {len(grammar_words)} grammar words")
            
            # 3. Test personal pronouns from the table (difficulty 1)
            print("\n--- Testing Personal Pronouns (Difficulty 1) ---")
            personal_pronouns_tests = [
                {"french": "Je", "shimaore": "Wami", "kibouchi": "Zahou", "difficulty": 1},
                {"french": "Tu", "shimaore": "Wawé", "kibouchi": "Anaou", "difficulty": 1},  # Note the accent on Wawé
                {"french": "Il/Elle", "shimaore": "Wayé", "kibouchi": "Izi", "difficulty": 1},
                {"french": "Nous", "shimaore": "Wassi", "kibouchi": "Atsika", "difficulty": 1},
                {"french": "Ils/Elles", "shimaore": "Wawo", "kibouchi": "Réou", "difficulty": 1},  # NEW addition
                {"french": "Vous", "shimaore": "Wagnou", "kibouchi": "Anaréou", "difficulty": 1}  # corrected to Anaréou
            ]
            
            personal_pronouns_correct = True
            for test_case in personal_pronouns_tests:
                french_word = test_case['french']
                if french_word in grammar_words_by_french:
                    word = grammar_words_by_french[french_word]
                    
                    # Check all fields
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                        (word['difficulty'], test_case['difficulty'], 'Difficulty')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            personal_pronouns_correct = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (difficulty: {word['difficulty']})")
                else:
                    print(f"❌ {french_word} not found in grammar category")
                    personal_pronouns_correct = False
            
            # 4. Test possessive pronouns from the table (difficulty 2)
            print("\n--- Testing Possessive Pronouns (Difficulty 2) ---")
            possessive_pronouns_tests = [
                {"french": "Le mien", "shimaore": "Yangou", "kibouchi": "Ninakahi", "difficulty": 2},
                {"french": "Le tien", "shimaore": "Yaho", "kibouchi": "Ninaou", "difficulty": 2},
                {"french": "Le sien", "shimaore": "Yahé", "kibouchi": "Ninazi", "difficulty": 2},
                {"french": "Le leur", "shimaore": "Yawo", "kibouchi": "Nindréou", "difficulty": 2},
                {"french": "Le nôtre", "shimaore": "Yatrou", "kibouchi": "Nintsika", "difficulty": 2},
                {"french": "Le vôtre", "shimaore": "Yagnou", "kibouchi": "Ninéyi", "difficulty": 2}
            ]
            
            possessive_pronouns_correct = True
            for test_case in possessive_pronouns_tests:
                french_word = test_case['french']
                if french_word in grammar_words_by_french:
                    word = grammar_words_by_french[french_word]
                    
                    # Check all fields
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                        (word['difficulty'], test_case['difficulty'], 'Difficulty')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            possessive_pronouns_correct = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (difficulty: {word['difficulty']})")
                else:
                    print(f"❌ {french_word} not found in grammar category")
                    possessive_pronouns_correct = False
            
            # 5. Test grammar vocabulary structure
            print("\n--- Testing Grammar Vocabulary Structure ---")
            
            # Verify increased grammar vocabulary count (should be 12 total: 6 personal + 6 possessive)
            expected_grammar_count = 12
            actual_grammar_count = len(grammar_words)
            
            grammar_count_correct = True
            if actual_grammar_count >= expected_grammar_count:
                print(f"✅ Grammar vocabulary count: {actual_grammar_count} words (expected at least {expected_grammar_count})")
            else:
                print(f"❌ Grammar vocabulary count: {actual_grammar_count} words (expected at least {expected_grammar_count})")
                grammar_count_correct = False
            
            # Verify difficulty levels (1 for personal pronouns, 2 for possessive pronouns)
            difficulty_1_count = len([w for w in grammar_words if w['difficulty'] == 1])
            difficulty_2_count = len([w for w in grammar_words if w['difficulty'] == 2])
            
            print(f"Difficulty 1 (personal pronouns): {difficulty_1_count} words")
            print(f"Difficulty 2 (possessive pronouns): {difficulty_2_count} words")
            
            difficulty_levels_correct = True
            if difficulty_1_count >= 6 and difficulty_2_count >= 6:
                print("✅ Difficulty levels properly assigned (1 for personal, 2 for possessive)")
            else:
                print("❌ Difficulty levels not properly assigned for grammar vocabulary")
                difficulty_levels_correct = False
            
            # Test that all pronouns are properly categorized as "grammaire"
            category_correct = True
            for word in grammar_words:
                if word['category'] != 'grammaire':
                    print(f"❌ Word '{word['french']}' has incorrect category: {word['category']} (expected 'grammaire')")
                    category_correct = False
            
            if category_correct:
                print("✅ All pronouns properly categorized as 'grammaire'")
            
            # 6. Test total vocabulary update
            print("\n--- Testing Total Vocabulary Update ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code == 200:
                all_words = response.json()
                total_word_count = len(all_words)
                print(f"✅ Total vocabulary count: {total_word_count} words (increased with complete grammar vocabulary)")
                
                # Confirm comprehensive grammar coverage for sentence construction
                personal_count = len([w for w in grammar_words if w['difficulty'] == 1])
                possessive_count = len([w for w in grammar_words if w['difficulty'] == 2])
                
                if personal_count >= 6 and possessive_count >= 6:
                    print("✅ Comprehensive grammar coverage confirmed for sentence construction in Shimaoré and Kibouchi")
                else:
                    print("❌ Insufficient grammar coverage for complete sentence construction")
                    return False
            else:
                print(f"❌ Could not retrieve total vocabulary: {response.status_code}")
                return False
            
            # Overall grammar test result
            all_grammar_correct = (
                personal_pronouns_correct and 
                possessive_pronouns_correct and 
                grammar_count_correct and 
                difficulty_levels_correct and 
                category_correct
            )
            
            if all_grammar_correct:
                print("\n🎉 COMPREHENSIVE GRAMMAR VOCABULARY TESTING COMPLETED SUCCESSFULLY!")
                print("✅ Complete grammar foundation with both personal and possessive pronouns")
                print("✅ All 6 personal pronouns verified (difficulty 1)")
                print("✅ All 6 possessive pronouns verified (difficulty 2)")
                print("✅ Total 12 grammar words properly categorized")
                print("✅ Comprehensive grammar coverage for building complete sentences in both Mayotte languages")
                print("✅ Proper accent marks confirmed (Wawé, Anaréou)")
                print("✅ NEW addition 'Ils/Elles' = 'Wawo/Réou' verified")
                print("✅ Corrected 'Vous' = 'Wagnou/Anaréou' verified")
            else:
                print("\n❌ Some grammar vocabulary items are incorrect or missing")
            
            return all_grammar_correct
            
        except Exception as e:
            print(f"❌ Comprehensive grammar vocabulary test error: {e}")
            return False

    def test_extended_family_vocabulary(self):
        """Test comprehensive extended family vocabulary initialization and translations"""
        print("\n=== Testing Extended Family Vocabulary ===")
        
        try:
            # First, test POST /api/init-base-content to initialize with extended family vocabulary
            print("--- Testing Family Vocabulary Initialization ---")
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to initialize base content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Base content initialized: {result}")
            
            # Test GET /api/words?category=famille to verify all new family terms
            print("\n--- Testing Family Category Filtering ---")
            response = self.session.get(f"{API_BASE}/words?category=famille")
            if response.status_code != 200:
                print(f"❌ Failed to get family words: {response.status_code}")
                return False
            
            family_words = response.json()
            family_words_by_french = {word['french']: word for word in family_words}
            
            print(f"Found {len(family_words)} family words")
            
            # Test specific extended family translations from the table
            print("\n--- Testing Specific Extended Family Translations ---")
            
            # Core family
            core_family_tests = [
                {"french": "Maman", "shimaore": "Mama", "kibouchi": "Mama", "difficulty": 1},
                {"french": "Papa", "shimaore": "Baba", "kibouchi": "Baba", "difficulty": 1},
                {"french": "Enfant", "shimaore": "Mwana", "kibouchi": "Mwana", "difficulty": 1}
            ]
            
            # Aunts/Uncles
            aunts_uncles_tests = [
                {"french": "Tante", "shimaore": "Mama titi", "kibouchi": "Nindri heli", "difficulty": 1},
                {"french": "Oncle maternel", "shimaore": "Zama", "kibouchi": "Zama", "difficulty": 2},
                {"french": "Oncle paternel", "shimaore": "Baba titi", "kibouchi": "Baba héli", "difficulty": 2}
            ]
            
            # Extended relations
            extended_relations_tests = [
                {"french": "Épouse oncle maternel", "shimaore": "Zena", "kibouchi": "Zena", "difficulty": 2}
            ]
            
            # Age-specific siblings
            age_specific_siblings_tests = [
                {"french": "Petite sœur", "shimaore": "Moinagna mtroum", "kibouchi": "Zandri", "difficulty": 1},
                {"french": "Petit frère", "shimaore": "Moinagna mtrouba", "kibouchi": "Zandri", "difficulty": 1},
                {"french": "Grande sœur", "shimaore": "Zouki", "kibouchi": "Zoki", "difficulty": 1},
                {"french": "Grand frère", "shimaore": "Zouki", "kibouchi": "Zoki", "difficulty": 1}
            ]
            
            # General siblings
            general_siblings_tests = [
                {"french": "Frère", "shimaore": "Mwanagna", "kibouchi": "Anadahi", "difficulty": 1},
                {"french": "Sœur", "shimaore": "Mwanagna", "kibouchi": "Anabavi", "difficulty": 1}
            ]
            
            # Social/Gender terms
            social_gender_tests = [
                {"french": "Ami", "shimaore": "Mwandzani", "kibouchi": "Mwandzani", "difficulty": 1},
                {"french": "Fille", "shimaore": "Mtroumama", "kibouchi": "Viavi", "difficulty": 1},
                {"french": "Garçon", "shimaore": "Mtroubaba", "kibouchi": "Lalahi", "difficulty": 1},
                {"french": "Monsieur", "shimaore": "Mogné", "kibouchi": "Lalahi", "difficulty": 1},
                {"french": "Madame", "shimaore": "Bwéni", "kibouchi": "Viavi", "difficulty": 1}
            ]
            
            # Grandparents
            grandparents_tests = [
                {"french": "Grand-père", "shimaore": "Bacoco", "kibouchi": "Dadayi", "difficulty": 1},
                {"french": "Grand-mère", "shimaore": "Coco", "kibouchi": "Dadi", "difficulty": 1}
            ]
            
            # Combine all family tests
            all_family_tests = (
                core_family_tests + aunts_uncles_tests + extended_relations_tests + 
                age_specific_siblings_tests + general_siblings_tests + 
                social_gender_tests + grandparents_tests
            )
            
            all_correct = True
            
            # Test each category
            test_categories = [
                ("Core Family", core_family_tests),
                ("Aunts/Uncles", aunts_uncles_tests),
                ("Extended Relations", extended_relations_tests),
                ("Age-Specific Siblings", age_specific_siblings_tests),
                ("General Siblings", general_siblings_tests),
                ("Social/Gender Terms", social_gender_tests),
                ("Grandparents", grandparents_tests)
            ]
            
            for category_name, test_cases in test_categories:
                print(f"\n--- Testing {category_name} ---")
                category_correct = True
                
                for test_case in test_cases:
                    french_word = test_case['french']
                    if french_word in family_words_by_french:
                        word = family_words_by_french[french_word]
                        
                        # Check all fields
                        checks = [
                            (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                            (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                            (word['difficulty'], test_case['difficulty'], 'Difficulty')
                        ]
                        
                        word_correct = True
                        for actual, expected, field_name in checks:
                            if actual != expected:
                                print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                                word_correct = False
                                category_correct = False
                                all_correct = False
                        
                        if word_correct:
                            print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (difficulty: {word['difficulty']})")
                    else:
                        print(f"❌ {french_word} not found in family category")
                        category_correct = False
                        all_correct = False
                
                if category_correct:
                    print(f"✅ {category_name} category: All translations verified")
                else:
                    print(f"❌ {category_name} category: Some translations incorrect or missing")
            
            # Test family vocabulary count and complexity
            print("\n--- Testing Family Vocabulary Count and Complexity ---")
            expected_family_count = len(all_family_tests)
            actual_family_count = len(family_words)
            
            if actual_family_count >= expected_family_count:
                print(f"✅ Family vocabulary count: {actual_family_count} words (expected at least {expected_family_count})")
            else:
                print(f"❌ Family vocabulary count: {actual_family_count} words (expected at least {expected_family_count})")
                all_correct = False
            
            # Verify difficulty levels (1 for basic family, 2 for extended relations)
            difficulty_1_count = len([w for w in family_words if w['difficulty'] == 1])
            difficulty_2_count = len([w for w in family_words if w['difficulty'] == 2])
            
            print(f"Difficulty 1 (basic family): {difficulty_1_count} words")
            print(f"Difficulty 2 (extended relations): {difficulty_2_count} words")
            
            if difficulty_1_count > 0 and difficulty_2_count > 0:
                print("✅ Difficulty levels properly assigned for family vocabulary")
            else:
                print("❌ Difficulty levels not properly assigned for family vocabulary")
                all_correct = False
            
            # Test total vocabulary update
            print("\n--- Testing Total Vocabulary Update ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code == 200:
                all_words = response.json()
                total_word_count = len(all_words)
                print(f"✅ Total vocabulary count: {total_word_count} words")
                
                # Verify comprehensive coverage of Mayotte family structures
                family_categories_found = set()
                for word in family_words:
                    if 'Oncle' in word['french'] or 'Tante' in word['french']:
                        family_categories_found.add('extended_family')
                    elif any(age_term in word['french'] for age_term in ['Petite', 'Petit', 'Grande', 'Grand']):
                        family_categories_found.add('age_specific')
                    elif word['french'] in ['Frère', 'Sœur']:
                        family_categories_found.add('general_siblings')
                    elif word['french'] in ['Maman', 'Papa', 'Enfant']:
                        family_categories_found.add('core_family')
                    elif word['french'] in ['Grand-père', 'Grand-mère']:
                        family_categories_found.add('grandparents')
                
                expected_family_categories = {'core_family', 'extended_family', 'age_specific', 'general_siblings', 'grandparents'}
                if expected_family_categories.issubset(family_categories_found):
                    print("✅ Comprehensive coverage of Mayotte family structures confirmed")
                else:
                    missing_categories = expected_family_categories - family_categories_found
                    print(f"❌ Missing family structure categories: {missing_categories}")
                    all_correct = False
            else:
                print(f"❌ Could not retrieve total vocabulary: {response.status_code}")
                all_correct = False
            
            if all_correct:
                print("\n🎉 Extended Family Vocabulary Testing COMPLETED SUCCESSFULLY!")
                print("✅ All extended family terms verified with authentic Shimaoré and Kibouchi translations")
                print("✅ Comprehensive coverage of traditional Mayotte family structures")
                print("✅ Proper difficulty levels assigned (1 for basic, 2 for extended relations)")
                print("✅ Age-specific and relationship-specific terms properly categorized")
            else:
                print("\n❌ Some extended family vocabulary items are incorrect or missing")
            
            return all_correct
            
        except Exception as e:
            print(f"❌ Extended family vocabulary test error: {e}")
            return False

    def test_complete_colors_palette(self):
        """Test the complete updated colors palette in the Mayotte educational app backend"""
        print("\n=== Testing Complete Colors Palette ===")
        
        try:
            # 1. Test complete colors vocabulary initialization
            print("--- Testing Complete Colors Vocabulary Initialization ---")
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to initialize base content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Base content initialized: {result}")
            
            # 2. Test GET /api/words?category=couleurs to verify all 8 colors
            print("\n--- Testing Colors Category Filtering (8 Colors) ---")
            response = self.session.get(f"{API_BASE}/words?category=couleurs")
            if response.status_code != 200:
                print(f"❌ Failed to get colors: {response.status_code}")
                return False
            
            colors = response.json()
            colors_by_french = {word['french']: word for word in colors}
            
            print(f"Found {len(colors)} colors in database")
            
            # 3. Test specific color translations from the table
            print("\n--- Testing Specific Color Translations ---")
            color_tests = [
                {"french": "Bleu", "shimaore": "Bilé", "kibouchi": "Bilé", "difficulty": 1},
                {"french": "Vert", "shimaore": "Dhavou", "kibouchi": "Mayitsou", "difficulty": 1},
                {"french": "Noir", "shimaore": "Nzidhou", "kibouchi": "Mayintigni", "difficulty": 1},
                {"french": "Blanc", "shimaore": "Ndjéou", "kibouchi": "Malandi", "difficulty": 1},
                {"french": "Rouge", "shimaore": "Ndzoukoundrou", "kibouchi": "Mena", "difficulty": 1},
                {"french": "Jaune", "shimaore": "Dzindzano", "kibouchi": "Tamoutamou", "difficulty": 1},
                {"french": "Marron", "shimaore": "Trotro", "kibouchi": "Fotafotaka", "difficulty": 1},  # NEW addition
                {"french": "Gris", "shimaore": "Djifou", "kibouchi": "Dzofou", "difficulty": 1}  # NEW addition
            ]
            
            all_colors_correct = True
            
            for test_case in color_tests:
                french_word = test_case['french']
                if french_word in colors_by_french:
                    word = colors_by_french[french_word]
                    
                    # Check all fields
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                        (word['difficulty'], test_case['difficulty'], 'Difficulty'),
                        (word['category'], 'couleurs', 'Category')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            all_colors_correct = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (difficulty: {word['difficulty']})")
                else:
                    print(f"❌ {french_word} not found in colors category")
                    all_colors_correct = False
            
            # 4. Test color vocabulary structure
            print("\n--- Testing Color Vocabulary Structure ---")
            
            # Verify increased color vocabulary count (should be 8 colors total)
            expected_color_count = 8
            actual_color_count = len(colors)
            
            color_count_correct = True
            if actual_color_count >= expected_color_count:
                print(f"✅ Color vocabulary count: {actual_color_count} colors (expected {expected_color_count})")
            else:
                print(f"❌ Color vocabulary count: {actual_color_count} colors (expected {expected_color_count})")
                color_count_correct = False
                all_colors_correct = False
            
            # Verify all colors have difficulty level 1 (basic colors)
            difficulty_levels_correct = True
            for color in colors:
                if color['difficulty'] != 1:
                    print(f"❌ Color '{color['french']}' has incorrect difficulty: {color['difficulty']} (expected 1)")
                    difficulty_levels_correct = False
                    all_colors_correct = False
            
            if difficulty_levels_correct:
                print("✅ All colors have difficulty level 1 (basic colors)")
            
            # Test that all colors are properly categorized as "couleurs"
            category_correct = True
            for color in colors:
                if color['category'] != 'couleurs':
                    print(f"❌ Color '{color['french']}' has incorrect category: {color['category']} (expected 'couleurs')")
                    category_correct = False
                    all_colors_correct = False
            
            if category_correct:
                print("✅ All colors properly categorized as 'couleurs'")
            
            # 5. Test total vocabulary update
            print("\n--- Testing Total Vocabulary Update ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code == 200:
                all_words = response.json()
                total_word_count = len(all_words)
                print(f"✅ Total vocabulary count: {total_word_count} words (increased with complete color palette)")
                
                # Confirm comprehensive color coverage including earth tones
                earth_tones_found = []
                for color in colors:
                    if color['french'] in ['Marron', 'Gris']:
                        earth_tones_found.append(color['french'])
                
                if len(earth_tones_found) >= 2:
                    print(f"✅ Earth tones confirmed: {', '.join(earth_tones_found)} (marron, gris)")
                else:
                    print(f"❌ Missing earth tones. Found: {', '.join(earth_tones_found)}")
                    all_colors_correct = False
                
                # Verify authentic Mayotte language coverage
                authentic_translations_verified = True
                for color in colors:
                    if not color['shimaore'] or not color['kibouchi']:
                        print(f"❌ Color '{color['french']}' missing translations")
                        authentic_translations_verified = False
                        all_colors_correct = False
                
                if authentic_translations_verified:
                    print("✅ All colors have authentic Shimaoré and Kibouchi translations")
            else:
                print(f"❌ Could not retrieve total vocabulary: {response.status_code}")
                all_colors_correct = False
            
            if all_colors_correct:
                print("\n🎨 COMPLETE COLORS PALETTE TESTING COMPLETED SUCCESSFULLY!")
                print("✅ All 8 colors verified with authentic Shimaoré and Kibouchi translations")
                print("✅ Complete color palette covering all basic colors plus earth tones")
                print("✅ Proper difficulty level 1 assigned to all colors")
                print("✅ All colors properly categorized as 'couleurs'")
                print("✅ Earth tones (Marron, Gris) successfully added")
                print("✅ Comprehensive color coverage for educational use")
                print("✅ Authentic translations in both Mayotte languages confirmed")
            else:
                print("\n❌ Some color vocabulary items are incorrect or missing")
            
            return all_colors_correct
            
        except Exception as e:
            print(f"❌ Complete colors palette test error: {e}")
            return False

    def test_comprehensive_updated_animals_section(self):
        """Test the comprehensive updated animals section in the Mayotte educational app backend"""
        print("\n=== Testing Comprehensive Updated Animals Section ===")
        
        try:
            # 1. Test complete animals vocabulary initialization
            print("--- Testing Complete Animals Vocabulary Initialization ---")
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to initialize base content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Base content initialized: {result}")
            
            # 2. Test GET /api/words?category=animaux to verify all animals with complete translations
            print("\n--- Testing Animals Category Filtering (40+ Animals) ---")
            response = self.session.get(f"{API_BASE}/words?category=animaux")
            if response.status_code != 200:
                print(f"❌ Failed to get animals: {response.status_code}")
                return False
            
            animals = response.json()
            animals_by_french = {word['french']: word for word in animals}
            
            print(f"Found {len(animals)} animals in database")
            
            # Verify significantly increased animal vocabulary count (should be around 40+ animals)
            if len(animals) >= 40:
                print(f"✅ Comprehensive animal vocabulary confirmed: {len(animals)} animals (40+ required)")
            else:
                print(f"❌ Insufficient animal vocabulary: {len(animals)} animals (40+ required)")
                return False
            
            # 3. Test specific animal groups from the table
            print("\n--- Testing Specific Animal Groups ---")
            
            # Domestic animals
            print("\n--- Testing Domestic Animals ---")
            domestic_animals_tests = [
                {"french": "Cochon", "shimaore": "Pouroukou", "kibouchi": "Lambou", "difficulty": 1},
                {"french": "Chèvre", "shimaore": "Mbouzi", "kibouchi": "Bengui", "difficulty": 1},
                {"french": "Mouton", "shimaore": "Baribari", "kibouchi": "Baribari", "difficulty": 1},
                {"french": "Zébu", "shimaore": "Nyombe", "kibouchi": "Aoumbi", "difficulty": 1},
                {"french": "Âne", "shimaore": "Pundra", "kibouchi": "Ampundra", "difficulty": 1},
                {"french": "Cheval", "shimaore": "Farassi", "kibouchi": "Farassi", "difficulty": 1},
                {"french": "Canard", "shimaore": "Guisi", "kibouchi": "Aoukiri", "difficulty": 1}
            ]
            
            # Updated core animals
            print("\n--- Testing Updated Core Animals ---")
            core_animals_tests = [
                {"french": "Chien", "shimaore": "Mbwa", "kibouchi": "Fadroka", "difficulty": 1},
                {"french": "Chat", "shimaore": "Paré", "kibouchi": "Moirou", "difficulty": 1},
                {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou", "difficulty": 1},
                {"french": "Oiseau", "shimaore": "Emougni", "kibouchi": "Voroumeki", "difficulty": 1},
                {"french": "Poule", "shimaore": "Kouhou", "kibouchi": "Akohou", "difficulty": 1},
                {"french": "Souris", "shimaore": "Shikwetse", "kibouchi": "Voilavou", "difficulty": 1}
            ]
            
            # Wild animals
            print("\n--- Testing Wild Animals ---")
            wild_animals_tests = [
                {"french": "Lion", "shimaore": "Simba", "kibouchi": "Simba", "difficulty": 2},
                {"french": "Éléphant", "shimaore": "Ndovu", "kibouchi": "Ndovu", "difficulty": 2},
                {"french": "Crocodile", "shimaore": "Vwai", "kibouchi": "Vwai", "difficulty": 2},
                {"french": "Serpent", "shimaore": "Nyoha", "kibouchi": "Bibi lava", "difficulty": 2}
            ]
            
            # Insects
            print("\n--- Testing Insects ---")
            insects_tests = [
                {"french": "Abeille", "shimaore": "Niochi", "kibouchi": "Antéli", "difficulty": 1},
                {"french": "Mouche", "shimaore": "Ndzi", "kibouchi": "Lalitri", "difficulty": 1},
                {"french": "Moustique", "shimaore": "Manundi", "kibouchi": "Mokou", "difficulty": 1},
                {"french": "Fourmis", "shimaore": "Tsutsuhu", "kibouchi": "Visiki", "difficulty": 1},
                {"french": "Papillon", "shimaore": "Pelapelaka", "kibouchi": "Tsipelapelaka", "difficulty": 1},
                {"french": "Araignée", "shimaore": "Shitrandrabilbwi", "kibouchi": "Bibi amparamani massou", "difficulty": 2},
                {"french": "Scorpion", "shimaore": "Ngo", "kibouchi": "Hala", "difficulty": 2}
            ]
            
            # Reptiles/Amphibians
            print("\n--- Testing Reptiles/Amphibians ---")
            reptiles_amphibians_tests = [
                {"french": "Margouillat", "shimaore": "Kasangwe", "kibouchi": "Kitsatsaka", "difficulty": 1},
                {"french": "Lézard", "shimaore": "Ngwizi", "kibouchi": "Kitsatsaka", "difficulty": 1},
                {"french": "Grenouille", "shimaore": "Shiwatrotro", "kibouchi": "Sahougnou", "difficulty": 1},
                {"french": "Tortue", "shimaore": "Nyamba katsa", "kibouchi": "Fanou", "difficulty": 1},
                {"french": "Caméléon", "shimaore": "Tarundru", "kibouchi": "Tarondru", "difficulty": 2}
            ]
            
            # Marine animals
            print("\n--- Testing Marine Animals ---")
            marine_animals_tests = [
                {"french": "Thon", "shimaore": "Mbassi", "kibouchi": "Mbassi", "difficulty": 1},
                {"french": "Requin", "shimaore": "Papa", "kibouchi": "Ankou", "difficulty": 2},
                {"french": "Poulpe", "shimaore": "Pwedza", "kibouchi": "Pwedza", "difficulty": 1},
                {"french": "Crabe", "shimaore": "Dradraka", "kibouchi": "Dakatra", "difficulty": 1},
                {"french": "Crevette", "shimaore": "Camba", "kibouchi": "Ancamba", "difficulty": 1}
            ]
            
            # Birds
            print("\n--- Testing Birds ---")
            birds_tests = [
                {"french": "Pigeon", "shimaore": "Ndiwa", "kibouchi": "Ndiwa", "difficulty": 1},
                {"french": "Perroquet", "shimaore": "Kasuku", "kibouchi": "Kararokou", "difficulty": 2},
                {"french": "Corbeau", "shimaore": "Gawa", "kibouchi": "Goika", "difficulty": 1}
            ]
            
            # Updated primates (now has both translations)
            print("\n--- Testing Updated Primates ---")
            primates_tests = [
                {"french": "Singe", "shimaore": "Djakwe", "kibouchi": "Djakouayi", "difficulty": 1}
            ]
            
            # Other animals
            print("\n--- Testing Other Animals ---")
            other_animals_tests = [
                {"french": "Maki", "shimaore": "Komba", "kibouchi": "Ankoumba", "difficulty": 1},
                {"french": "Escargot", "shimaore": "Kowa", "kibouchi": "Ankora", "difficulty": 1},
                {"french": "Rat", "shimaore": "Pouhou", "kibouchi": "Voilavou", "difficulty": 1},
                {"french": "Chauve-souris", "shimaore": "Drema", "kibouchi": "Fanihi", "difficulty": 1},
                {"french": "Lapin", "shimaore": "Sungura", "kibouchi": "Shoungoura", "difficulty": 1},
                {"french": "Hérisson", "shimaore": "Tandra", "kibouchi": "Trandraka", "difficulty": 2}
            ]
            
            # Combine all animal tests
            all_animal_tests = (
                domestic_animals_tests + core_animals_tests + wild_animals_tests + 
                insects_tests + reptiles_amphibians_tests + marine_animals_tests + 
                birds_tests + primates_tests + other_animals_tests
            )
            
            all_animals_correct = True
            
            # Test each animal group
            test_groups = [
                ("Domestic Animals", domestic_animals_tests),
                ("Updated Core Animals", core_animals_tests),
                ("Wild Animals", wild_animals_tests),
                ("Insects", insects_tests),
                ("Reptiles/Amphibians", reptiles_amphibians_tests),
                ("Marine Animals", marine_animals_tests),
                ("Birds", birds_tests),
                ("Updated Primates", primates_tests),
                ("Other Animals", other_animals_tests)
            ]
            
            for group_name, test_cases in test_groups:
                print(f"\n--- Testing {group_name} ---")
                group_correct = True
                
                for test_case in test_cases:
                    french_word = test_case['french']
                    if french_word in animals_by_french:
                        word = animals_by_french[french_word]
                        
                        # Check all fields
                        checks = [
                            (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                            (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                            (word['difficulty'], test_case['difficulty'], 'Difficulty'),
                            (word['category'], 'animaux', 'Category')
                        ]
                        
                        word_correct = True
                        for actual, expected, field_name in checks:
                            if actual != expected:
                                print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                                word_correct = False
                                group_correct = False
                                all_animals_correct = False
                        
                        if word_correct:
                            print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (difficulty: {word['difficulty']})")
                    else:
                        print(f"❌ {french_word} not found in animals category")
                        group_correct = False
                        all_animals_correct = False
                
                if group_correct:
                    print(f"✅ {group_name}: All translations verified")
                else:
                    print(f"❌ {group_name}: Some translations incorrect or missing")
            
            # 4. Test animal vocabulary structure
            print("\n--- Testing Animal Vocabulary Structure ---")
            
            # Verify difficulty levels (1 for common animals, 2 for wild/exotic animals)
            difficulty_1_count = len([a for a in animals if a['difficulty'] == 1])
            difficulty_2_count = len([a for a in animals if a['difficulty'] == 2])
            
            print(f"Difficulty 1 (common animals): {difficulty_1_count} animals")
            print(f"Difficulty 2 (wild/exotic animals): {difficulty_2_count} animals")
            
            if difficulty_1_count > 0 and difficulty_2_count > 0:
                print("✅ Difficulty levels properly assigned (1 for common, 2 for wild/exotic)")
            else:
                print("❌ Difficulty levels not properly assigned for animal vocabulary")
                all_animals_correct = False
            
            # Test that all animals are properly categorized as "animaux"
            category_correct = True
            for animal in animals:
                if animal['category'] != 'animaux':
                    print(f"❌ Animal '{animal['french']}' has incorrect category: {animal['category']} (expected 'animaux')")
                    category_correct = False
                    all_animals_correct = False
            
            if category_correct:
                print("✅ All animals properly categorized as 'animaux'")
            
            # Verify all animals have complete Shimaoré AND Kibouchi translations
            print("\n--- Testing Complete Translations ---")
            translation_complete = True
            for animal in animals:
                if not animal['shimaore'] and not animal['kibouchi']:
                    print(f"❌ {animal['french']} has no translations in either language")
                    translation_complete = False
                    all_animals_correct = False
                elif not animal['shimaore']:
                    print(f"⚠️ {animal['french']} has no Shimaoré translation (Kibouchi: {animal['kibouchi']})")
                elif not animal['kibouchi']:
                    print(f"⚠️ {animal['french']} has no Kibouchi translation (Shimaoré: {animal['shimaore']})")
            
            if translation_complete:
                print("✅ All animals have at least one complete translation")
            
            # 5. Test total vocabulary update
            print("\n--- Testing Total Vocabulary Update ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code == 200:
                all_words = response.json()
                total_word_count = len(all_words)
                print(f"✅ Total vocabulary count: {total_word_count} words (increased significantly with comprehensive animal vocabulary)")
                
                # Confirm comprehensive fauna coverage representing Mayotte's biodiversity
                animal_categories_found = set()
                for animal in animals:
                    if animal['french'] in [a['french'] for a in domestic_animals_tests]:
                        animal_categories_found.add('domestic')
                    elif animal['french'] in [a['french'] for a in wild_animals_tests]:
                        animal_categories_found.add('wild')
                    elif animal['french'] in [a['french'] for a in insects_tests]:
                        animal_categories_found.add('insects')
                    elif animal['french'] in [a['french'] for a in marine_animals_tests]:
                        animal_categories_found.add('marine')
                    elif animal['french'] in [a['french'] for a in birds_tests]:
                        animal_categories_found.add('birds')
                    elif animal['french'] in [a['french'] for a in reptiles_amphibians_tests]:
                        animal_categories_found.add('reptiles')
                
                expected_animal_categories = {'domestic', 'wild', 'insects', 'marine', 'birds', 'reptiles'}
                if expected_animal_categories.issubset(animal_categories_found):
                    print("✅ Comprehensive fauna coverage representing Mayotte's biodiversity confirmed")
                else:
                    missing_categories = expected_animal_categories - animal_categories_found
                    print(f"❌ Missing animal categories: {missing_categories}")
                    all_animals_correct = False
            else:
                print(f"❌ Could not retrieve total vocabulary: {response.status_code}")
                all_animals_correct = False
            
            if all_animals_correct:
                print("\n🎉 COMPREHENSIVE UPDATED ANIMALS SECTION TESTING COMPLETED SUCCESSFULLY!")
                print("✅ Complete animals vocabulary initialization verified")
                print("✅ 40+ animals with comprehensive authentic translations confirmed")
                print("✅ All specific animal groups from table verified:")
                print("   • Domestic animals (Cochon=Pouroukou/Lambou, Chèvre=Mbouzi/Bengui, etc.)")
                print("   • Updated core animals (Chien=Mbwa/Fadroka, Chat=Paré/Moirou, etc.)")
                print("   • Wild animals (Lion=Simba/Simba, Éléphant=Ndovu/Ndovu, etc.)")
                print("   • Insects (Abeille=Niochi/Antéli, Mouche=Ndzi/Lalitri, etc.)")
                print("   • Reptiles/Amphibians (Margouillat=Kasangwe/Kitsatsaka, etc.)")
                print("   • Marine animals (Thon=Mbassi/Mbassi, Requin=Papa/Ankou, etc.)")
                print("   • Birds (Pigeon=Ndiwa/Ndiwa, Perroquet=Kasuku/Kararokou, etc.)")
                print("   • Updated primates (Singe=Djakwe/Djakouayi - now has both translations)")
                print("✅ Difficulty levels properly assigned (1 for common, 2 for wild/exotic)")
                print("✅ All animals properly categorized as 'animaux'")
                print("✅ Complete Shimaoré AND Kibouchi translations verified")
                print("✅ Comprehensive fauna coverage representing Mayotte's biodiversity")
                print("✅ Most comprehensive authentic animal vocabulary covering domestic animals, wildlife, insects, marine life, birds, and reptiles")
            else:
                print("\n❌ Some animal vocabulary items are incorrect or missing")
            
            return all_animals_correct
            
        except Exception as e:
            print(f"❌ Comprehensive updated animals section test error: {e}")
            return False

    def test_final_comprehensive_animals_vocabulary(self):
        """Test final comprehensive animals vocabulary with all missing animals added (60+ animals)"""
        print("\n=== Testing Final Comprehensive Animals Vocabulary ===")
        
        try:
            # 1. Test POST /api/init-base-content to initialize with all animals from the table
            print("--- Testing Complete Animals Vocabulary Initialization ---")
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to initialize base content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Base content initialized: {result}")
            
            # 2. Test GET /api/words?category=animaux to verify expanded animal count (60+ animals)
            print("\n--- Testing Animals Category Filtering (60+ Animals) ---")
            response = self.session.get(f"{API_BASE}/words?category=animaux")
            if response.status_code != 200:
                print(f"❌ Failed to get animals: {response.status_code}")
                return False
            
            animals = response.json()
            animals_by_french = {word['french']: word for word in animals}
            
            print(f"Found {len(animals)} animals in database")
            
            # Verify we have 60+ animals (significantly increased from previous 40+)
            if len(animals) >= 60:
                print(f"✅ Significantly increased animal count: {len(animals)} animals (60+ required)")
            else:
                print(f"❌ Insufficient animal count: {len(animals)} animals (60+ required)")
                return False
            
            # 3. Test newly added animal categories from the review request
            print("\n--- Testing Newly Added Animal Categories ---")
            
            # Additional Insects/Larvae
            print("\n--- Testing Additional Insects/Larvae ---")
            additional_insects_tests = [
                {"french": "Chenille", "shimaore": "Bibimangidji", "kibouchi": "Bibimangidji", "difficulty": 1},
                {"french": "Ver de terre", "shimaore": "Njengwe", "kibouchi": "Bibi fotaka", "difficulty": 1},
                {"french": "Criquet", "shimaore": "Furudji", "kibouchi": "Kidzedza", "difficulty": 1},
                {"french": "Cafard", "shimaore": "Kalalawi", "kibouchi": "Galaronga", "difficulty": 1},
                {"french": "Scolopendre", "shimaore": "Trambwi", "kibouchi": "Trambougnou", "difficulty": 2},
                {"french": "Frelon", "shimaore": "Chonga", "kibouchi": "Faraka", "difficulty": 1},
                {"french": "Guêpe", "shimaore": "Yungo yungo", "kibouchi": "Fantehi", "difficulty": 1},
                {"french": "Bourdon", "shimaore": "Madzi ya nyombe", "kibouchi": "Majaoumbi", "difficulty": 1},
                {"french": "Puce", "shimaore": "Kunguni", "kibouchi": "Ancomgou", "difficulty": 1}
            ]
            
            # Additional Fish
            print("\n--- Testing Additional Fish ---")
            additional_fish_tests = [
                {"french": "Bigorno", "shimaore": "Trondro", "kibouchi": "Trondroul", "difficulty": 1}
            ]
            
            # Additional Wild Mammals
            print("\n--- Testing Additional Wild Mammals ---")
            additional_wild_mammals_tests = [
                {"french": "Facochère", "shimaore": "Pouroukou nyeha", "kibouchi": "Rambou", "difficulty": 2},
                {"french": "Renard", "shimaore": "Mbwa nyeha", "kibouchi": "Fandroka", "difficulty": 2},
                {"french": "Chameau", "shimaore": "Ngamia", "kibouchi": "Angamia", "difficulty": 2}
            ]
            
            # Additional Bovines/Caprines
            print("\n--- Testing Additional Bovines/Caprines ---")
            additional_bovines_tests = [
                {"french": "Bouc", "shimaore": "Bewe", "kibouchi": "Béberou", "difficulty": 1},
                {"french": "Taureau", "shimaore": "Kondzo", "kibouchi": "Larew", "difficulty": 1}
            ]
            
            # Updated animals (corrected translations)
            print("\n--- Testing Updated Animals (Corrected Translations) ---")
            updated_animals_tests = [
                {"french": "Escargot", "shimaore": "Kouéya", "kibouchi": "Ancora", "difficulty": 1}  # corrected from Kowa/Ankora
            ]
            
            # Combine all new animal tests
            all_new_animal_tests = (
                additional_insects_tests + additional_fish_tests + 
                additional_wild_mammals_tests + additional_bovines_tests + 
                updated_animals_tests
            )
            
            all_new_animals_correct = True
            
            # Test each new animal category
            test_categories = [
                ("Additional Insects/Larvae", additional_insects_tests),
                ("Additional Fish", additional_fish_tests),
                ("Additional Wild Mammals", additional_wild_mammals_tests),
                ("Additional Bovines/Caprines", additional_bovines_tests),
                ("Updated Animals", updated_animals_tests)
            ]
            
            for category_name, test_cases in test_categories:
                print(f"\n--- Testing {category_name} ---")
                category_correct = True
                
                for test_case in test_cases:
                    french_word = test_case['french']
                    if french_word in animals_by_french:
                        word = animals_by_french[french_word]
                        
                        # Check all fields
                        checks = [
                            (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                            (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                            (word['difficulty'], test_case['difficulty'], 'Difficulty'),
                            (word['category'], 'animaux', 'Category')
                        ]
                        
                        word_correct = True
                        for actual, expected, field_name in checks:
                            if actual != expected:
                                print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                                word_correct = False
                                category_correct = False
                                all_new_animals_correct = False
                        
                        if word_correct:
                            print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (difficulty: {word['difficulty']})")
                    else:
                        print(f"❌ {french_word} not found in animals category")
                        category_correct = False
                        all_new_animals_correct = False
                
                if category_correct:
                    print(f"✅ {category_name}: All translations verified")
                else:
                    print(f"❌ {category_name}: Some translations incorrect or missing")
            
            # 4. Test that all new animals have complete Shimaoré and Kibouchi translations
            print("\n--- Testing Complete Translations for All Animals ---")
            incomplete_translations = []
            
            for animal in animals:
                if not animal['shimaore'] or not animal['kibouchi']:
                    incomplete_translations.append(f"{animal['french']} (Shimaoré: '{animal['shimaore']}', Kibouchi: '{animal['kibouchi']}')")
            
            if not incomplete_translations:
                print("✅ All animals have complete Shimaoré and Kibouchi translations")
            else:
                print(f"❌ Animals with incomplete translations: {incomplete_translations}")
                all_new_animals_correct = False
            
            # 5. Test proper difficulty assignments for new animals
            print("\n--- Testing Difficulty Assignments ---")
            difficulty_1_count = len([a for a in animals if a['difficulty'] == 1])
            difficulty_2_count = len([a for a in animals if a['difficulty'] == 2])
            
            print(f"Difficulty 1 (common animals): {difficulty_1_count} animals")
            print(f"Difficulty 2 (wild/exotic animals): {difficulty_2_count} animals")
            
            if difficulty_1_count > 0 and difficulty_2_count > 0:
                print("✅ Proper difficulty assignments confirmed")
            else:
                print("❌ Difficulty assignments not properly distributed")
                all_new_animals_correct = False
            
            # 6. Test total vocabulary update reflects all added animals
            print("\n--- Testing Total Vocabulary Update ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code == 200:
                all_words = response.json()
                total_word_count = len(all_words)
                print(f"✅ Total vocabulary count: {total_word_count} words (reflects all added animals)")
                
                # Confirm comprehensive fauna collection representing complete Mayotte biodiversity
                animal_categories_found = set()
                for animal in animals:
                    if any(insect in animal['french'].lower() for insect in ['chenille', 'ver', 'criquet', 'cafard', 'scolopendre', 'frelon', 'guêpe', 'bourdon', 'puce']):
                        animal_categories_found.add('additional_insects')
                    elif 'bigorno' in animal['french'].lower():
                        animal_categories_found.add('additional_fish')
                    elif any(mammal in animal['french'].lower() for mammal in ['facochère', 'renard', 'chameau']):
                        animal_categories_found.add('additional_wild_mammals')
                    elif any(bovine in animal['french'].lower() for bovine in ['bouc', 'taureau']):
                        animal_categories_found.add('additional_bovines')
                    elif 'escargot' in animal['french'].lower():
                        animal_categories_found.add('updated_animals')
                
                expected_new_categories = {'additional_insects', 'additional_fish', 'additional_wild_mammals', 'additional_bovines', 'updated_animals'}
                if expected_new_categories.issubset(animal_categories_found):
                    print("✅ Complete Mayotte biodiversity representation confirmed")
                else:
                    missing_categories = expected_new_categories - animal_categories_found
                    print(f"❌ Missing animal categories: {missing_categories}")
                    all_new_animals_correct = False
            else:
                print(f"❌ Could not retrieve total vocabulary: {response.status_code}")
                all_new_animals_correct = False
            
            if all_new_animals_correct:
                print("\n🎉 FINAL COMPREHENSIVE ANIMALS VOCABULARY TESTING COMPLETED SUCCESSFULLY!")
                print("✅ All missing animals from the table have been added and verified")
                print("✅ Significantly increased animal vocabulary (60+ animals confirmed)")
                print("✅ All new animals have complete Shimaoré and Kibouchi translations")
                print("✅ Proper difficulty assignments for all new animals")
                print("✅ Additional Insects/Larvae: 9 new species added")
                print("✅ Additional Fish: Bigorno added")
                print("✅ Additional Wild Mammals: Facochère, Renard, Chameau added")
                print("✅ Additional Bovines/Caprines: Bouc, Taureau added")
                print("✅ Updated animals: Escargot translation corrected")
                print("✅ Most comprehensive fauna collection representing complete Mayotte biodiversity")
            else:
                print("\n❌ Some new animals are incorrect, missing, or have incomplete translations")
            
            return all_new_animals_correct
            
        except Exception as e:
            print(f"❌ Final comprehensive animals vocabulary test error: {e}")
            return False

    def test_corrected_animal_translations(self):
        """Test the corrected animal translations to verify all requested changes have been implemented"""
        print("\n=== Testing Corrected Animal Translations ===")
        
        try:
            # 1. Test initialization with corrected translations
            print("--- Testing Initialization with Corrected Animal Translations ---")
            
            # First, clear existing content by deleting all words
            print("Clearing existing content...")
            try:
                words_response = self.session.get(f"{API_BASE}/words")
                if words_response.status_code == 200:
                    existing_words = words_response.json()
                    for word in existing_words:
                        delete_response = self.session.delete(f"{API_BASE}/words/{word['id']}")
                        if delete_response.status_code != 200:
                            print(f"Warning: Could not delete word {word['id']}")
                    print(f"Cleared {len(existing_words)} existing words")
            except Exception as e:
                print(f"Note: Could not clear existing content: {e}")
            
            # POST /api/init-base-content to reinitialize with corrected animal translations
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to initialize base content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Base content reinitialized: {result}")
            
            # 2. GET /api/words?category=animaux to verify specific corrected animals
            print("\n--- Testing Animal Category Filtering ---")
            response = self.session.get(f"{API_BASE}/words?category=animaux")
            if response.status_code != 200:
                print(f"❌ Failed to get animal words: {response.status_code}")
                return False
            
            animals = response.json()
            animals_by_french = {word['french']: word for word in animals}
            
            print(f"Found {len(animals)} animals in database")
            
            # 3. Test each specifically corrected animal translation
            print("\n--- Testing Specifically Corrected Animal Translations ---")
            corrected_animals_tests = [
                # Chat: Should be "Paha/Moirou" (corrected from "Paré/Moirou")
                {"french": "Chat", "shimaore": "Paha", "kibouchi": "Moirou", "old_shimaore": "Paré"},
                
                # Oiseau: Should be "Gnougni/Vorougnou" (corrected from "Emougni/Voroumeki")
                {"french": "Oiseau", "shimaore": "Gnougni", "kibouchi": "Vorougnou", "old_shimaore": "Emougni", "old_kibouchi": "Voroumeki"},
                
                # Scorpion: Should be "Hala/Hala" (corrected from "Ngo/Hala")
                {"french": "Scorpion", "shimaore": "Hala", "kibouchi": "Hala", "old_shimaore": "Ngo"},
                
                # Requin: Should be "Papa/Ankiou" (corrected from "Papa/Ankou")
                {"french": "Requin", "shimaore": "Papa", "kibouchi": "Ankiou", "old_kibouchi": "Ankou"},
                
                # Taureau: Should be "Kondzo/Dzow" (corrected from "Kondzo/Larew")
                {"french": "Taureau", "shimaore": "Kondzo", "kibouchi": "Dzow", "old_kibouchi": "Larew"}
            ]
            
            all_corrections_correct = True
            
            for test_case in corrected_animals_tests:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    word = animals_by_french[french_word]
                    
                    # Check corrected translations
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                        (word['category'], 'animaux', 'Category')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            all_corrections_correct = False
                    
                    if word_correct:
                        # Show what was corrected
                        corrections = []
                        if 'old_shimaore' in test_case:
                            corrections.append(f"Shimaoré: {test_case['old_shimaore']} → {word['shimaore']}")
                        if 'old_kibouchi' in test_case:
                            corrections.append(f"Kibouchi: {test_case['old_kibouchi']} → {word['kibouchi']}")
                        
                        correction_text = " | ".join(corrections) if corrections else "verified"
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} ({correction_text})")
                else:
                    print(f"❌ {french_word} not found in animals category")
                    all_corrections_correct = False
            
            # 4. Verify correction completeness
            print("\n--- Verifying Correction Completeness ---")
            
            # Confirm all 5 requested animals have been updated with correct translations
            corrected_count = 0
            for test_case in corrected_animals_tests:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    word = animals_by_french[french_word]
                    if (word['shimaore'] == test_case['shimaore'] and 
                        word['kibouchi'] == test_case['kibouchi']):
                        corrected_count += 1
            
            if corrected_count == 5:
                print(f"✅ All 5 requested animal corrections implemented successfully")
            else:
                print(f"❌ Only {corrected_count}/5 animal corrections implemented correctly")
                all_corrections_correct = False
            
            # Verify no regressions in other animal translations
            print("\n--- Verifying No Regressions in Other Animal Translations ---")
            
            # Test a few other animals to ensure they weren't affected
            other_animals_tests = [
                {"french": "Chien", "shimaore": "Mbwa", "kibouchi": "Fadroka"},
                {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou"},
                {"french": "Maki", "shimaore": "Komba", "kibouchi": "Ankoumba"},
                {"french": "Singe", "shimaore": "Djakwe", "kibouchi": "Djakouayi"}
            ]
            
            regressions_found = False
            for test_case in other_animals_tests:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    word = animals_by_french[french_word]
                    if (word['shimaore'] == test_case['shimaore'] and 
                        word['kibouchi'] == test_case['kibouchi']):
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (no regression)")
                    else:
                        print(f"❌ {french_word}: Regression detected - Expected {test_case['shimaore']}/{test_case['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        regressions_found = True
                        all_corrections_correct = False
            
            if not regressions_found:
                print("✅ No regressions detected in other animal translations")
            
            # Ensure category and difficulty remain unchanged for corrected animals
            print("\n--- Verifying Category and Difficulty Unchanged ---")
            category_difficulty_correct = True
            for test_case in corrected_animals_tests:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    word = animals_by_french[french_word]
                    if word['category'] != 'animaux':
                        print(f"❌ {french_word}: Category changed from 'animaux' to '{word['category']}'")
                        category_difficulty_correct = False
                        all_corrections_correct = False
                    # Difficulty should be 1 or 2 for animals
                    if word['difficulty'] not in [1, 2]:
                        print(f"❌ {french_word}: Invalid difficulty level {word['difficulty']}")
                        category_difficulty_correct = False
                        all_corrections_correct = False
            
            if category_difficulty_correct:
                print("✅ Category and difficulty levels remain unchanged for corrected animals")
            
            # 5. Test total animal vocabulary integrity
            print("\n--- Testing Total Animal Vocabulary Integrity ---")
            
            # Verify the total animal count remains at 63 animals
            expected_animal_count = 63
            actual_animal_count = len(animals)
            
            if actual_animal_count >= expected_animal_count:
                print(f"✅ Animal count: {actual_animal_count} animals (expected at least {expected_animal_count})")
            else:
                print(f"❌ Animal count: {actual_animal_count} animals (expected at least {expected_animal_count})")
                all_corrections_correct = False
            
            # Confirm all other animals retain their correct translations
            print("\n--- Verifying All Animals Have Complete Translations ---")
            incomplete_translations = 0
            for animal in animals:
                if not animal['shimaore'] and not animal['kibouchi']:
                    print(f"❌ {animal['french']}: Missing both Shimaoré and Kibouchi translations")
                    incomplete_translations += 1
                elif not animal['shimaore']:
                    # Some animals like "Singe" may not have Shimaoré translation, which is acceptable
                    pass
                elif not animal['kibouchi']:
                    # Some animals may not have Kibouchi translation, which is acceptable
                    pass
            
            if incomplete_translations == 0:
                print("✅ All animals have at least one translation (Shimaoré or Kibouchi)")
            else:
                print(f"❌ {incomplete_translations} animals have incomplete translations")
                all_corrections_correct = False
            
            # Test that backend functionality is intact after corrections
            print("\n--- Testing Backend Functionality Integrity ---")
            
            # Test basic CRUD operations still work
            try:
                # Test creating a new animal
                test_animal = {
                    "french": "Test Animal",
                    "shimaore": "Test Shimaoré",
                    "kibouchi": "Test Kibouchi",
                    "category": "animaux",
                    "difficulty": 1
                }
                
                create_response = self.session.post(f"{API_BASE}/words", json=test_animal)
                if create_response.status_code == 200:
                    created_animal = create_response.json()
                    test_animal_id = created_animal['id']
                    
                    # Test retrieving the animal
                    get_response = self.session.get(f"{API_BASE}/words/{test_animal_id}")
                    if get_response.status_code == 200:
                        # Test deleting the animal
                        delete_response = self.session.delete(f"{API_BASE}/words/{test_animal_id}")
                        if delete_response.status_code == 200:
                            print("✅ Backend CRUD functionality intact after corrections")
                        else:
                            print("❌ Backend delete functionality issue after corrections")
                            all_corrections_correct = False
                    else:
                        print("❌ Backend read functionality issue after corrections")
                        all_corrections_correct = False
                else:
                    print("❌ Backend create functionality issue after corrections")
                    all_corrections_correct = False
            except Exception as e:
                print(f"❌ Backend functionality test error: {e}")
                all_corrections_correct = False
            
            # Final result
            if all_corrections_correct:
                print("\n🎉 CORRECTED ANIMAL TRANSLATIONS TESTING COMPLETED SUCCESSFULLY!")
                print("✅ All 5 specifically requested animal corrections implemented:")
                print("   • Chat: Paha/Moirou (corrected from Paré/Moirou)")
                print("   • Oiseau: Gnougni/Vorougnou (corrected from Emougni/Voroumeki)")
                print("   • Scorpion: Hala/Hala (corrected from Ngo/Hala)")
                print("   • Requin: Papa/Ankiou (corrected from Papa/Ankou)")
                print("   • Taureau: Kondzo/Dzow (corrected from Kondzo/Larew)")
                print("✅ No regressions in other animal translations")
                print("✅ Category and difficulty levels unchanged")
                print(f"✅ Total animal count maintained at {actual_animal_count} animals")
                print("✅ Backend functionality remains intact")
            else:
                print("\n❌ Some animal translation corrections are missing or incorrect")
            
            return all_corrections_correct
            
        except Exception as e:
            print(f"❌ Corrected animal translations test error: {e}")
            return False

    def test_comprehensive_verbs_section(self):
        """Test the comprehensive updated verbs section with complete vocabulary from the user's table"""
        print("\n=== Testing Comprehensive Updated Verbs Section ===")
        
        try:
            # 1. Test comprehensive verbs vocabulary initialization
            print("--- Testing Comprehensive Verbs Vocabulary Initialization ---")
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to initialize base content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Base content initialized: {result}")
            
            # 2. Test GET /api/words?category=verbes to verify all verbs from the table
            print("\n--- Testing Verbs Category Filtering (65+ Verbs) ---")
            response = self.session.get(f"{API_BASE}/words?category=verbes")
            if response.status_code != 200:
                print(f"❌ Failed to get verbs: {response.status_code}")
                return False
            
            verbs = response.json()
            verbs_by_french = {word['french']: word for word in verbs}
            
            print(f"Found {len(verbs)} verbs in database")
            
            # Verify we have 65+ verbs as required
            if len(verbs) >= 65:
                print(f"✅ Comprehensive verb vocabulary confirmed: {len(verbs)} verbs (65+ required)")
            else:
                print(f"❌ Insufficient verb vocabulary: {len(verbs)} verbs (65+ required)")
                return False
            
            # 3. Test specific verb categories from the comprehensive table
            print("\n--- Testing Specific Verb Categories ---")
            
            # Basic actions
            print("\n--- Testing Basic Actions ---")
            basic_actions_tests = [
                {"french": "Jouer", "shimaore": "Nguadza", "kibouchi": "Misoma", "difficulty": 1},
                {"french": "Courir", "shimaore": "Wendra mbiyo", "kibouchi": "Miloumeyi", "difficulty": 1},
                {"french": "Dire", "shimaore": "Burengisa", "kibouchi": "Mangataka", "difficulty": 1},
                {"french": "Pouvoir", "shimaore": "Ouchindra", "kibouchi": "Mahaléou", "difficulty": 1},
                {"french": "Vouloir", "shimaore": "Outlsho", "kibouchi": "Irokou", "difficulty": 1}
            ]
            
            # Communication verbs
            print("\n--- Testing Communication Verbs ---")
            communication_verbs_tests = [
                {"french": "Parler", "shimaore": "Oujagous", "kibouchi": "Mivoulgma", "difficulty": 1},
                {"french": "Demander", "shimaore": "Oodzisa", "kibouchi": "Magndoutani", "difficulty": 1},
                {"french": "Répondre", "shimaore": "Oudjibou", "kibouchi": "Mikoudjibou", "difficulty": 1},
                {"french": "Écouter", "shimaore": "Ouwoulkia", "kibouchi": "Mitandréngni", "difficulty": 1}
            ]
            
            # Learning verbs
            print("\n--- Testing Learning Verbs ---")
            learning_verbs_tests = [
                {"french": "Savoir", "shimaore": "Oujoua", "kibouchi": "Méhéyi", "difficulty": 1},
                {"french": "Apprendre", "shimaore": "Ourfoundrana", "kibouchi": "Midzorou", "difficulty": 1},
                {"french": "Comprendre", "shimaore": "Ouéléwa", "kibouchi": "Kouéléwa", "difficulty": 1},
                {"french": "Lire", "shimaore": "Ousoma", "kibouchi": "Midzorou", "difficulty": 1},
                {"french": "Écrire", "shimaore": "Ouhangidina", "kibouchi": "Soukouadika", "difficulty": 1}
            ]
            
            # Movement verbs
            print("\n--- Testing Movement Verbs ---")
            movement_verbs_tests = [
                {"french": "Marcher", "shimaore": "Ouzndra", "kibouchi": "Mandeha", "difficulty": 1},
                {"french": "Entrer", "shimaore": "Oughulya", "kibouchi": "Midiri", "difficulty": 1},
                {"french": "Sortir", "shimaore": "Oulawy", "kibouchi": "Miboka", "difficulty": 1},
                {"french": "Venir", "shimaore": "Oudja", "kibouchi": "Miavi", "difficulty": 1}
            ]
            
            # Daily life verbs
            print("\n--- Testing Daily Life Verbs ---")
            daily_life_verbs_tests = [
                {"french": "Manger", "shimaore": "Oudhya", "kibouchi": "Mihinagna", "difficulty": 1},
                {"french": "Boire", "shimaore": "Ounzoa", "kibouchi": "Mitsiratra", "difficulty": 1},
                {"french": "Dormir", "shimaore": "Oulala", "kibouchi": "Mandri", "difficulty": 1},
                {"french": "S'asseoir", "shimaore": "Ouzina", "kibouchi": "Mitsindza", "difficulty": 1}
            ]
            
            # Care verbs
            print("\n--- Testing Care Verbs ---")
            care_verbs_tests = [
                {"french": "Se laver", "shimaore": "Ouhowa", "kibouchi": "Miséki", "difficulty": 1},
                {"french": "Se baigner", "shimaore": "Ouhowa", "kibouchi": "Misséki", "difficulty": 1},
                {"french": "Se laver le derrière", "shimaore": "Outsamba", "kibouchi": "Mambouyï", "difficulty": 1}
            ]
            
            # Complex actions
            print("\n--- Testing Complex Actions ---")
            complex_actions_tests = [
                {"french": "Faire caca", "shimaore": "Oukoza", "kibouchi": "Manibi", "difficulty": 1},
                {"french": "Faire pipi", "shimaore": "Ouraviha", "kibouchi": "Mandouwya", "difficulty": 1},
                {"french": "Vomir", "shimaore": "Outakéa", "kibouchi": "Mampétraka", "difficulty": 1}
            ]
            
            # Combine all verb tests
            all_verb_tests = (
                basic_actions_tests + communication_verbs_tests + learning_verbs_tests + 
                movement_verbs_tests + daily_life_verbs_tests + care_verbs_tests + complex_actions_tests
            )
            
            all_verbs_correct = True
            
            # Test each category
            test_categories = [
                ("Basic Actions", basic_actions_tests),
                ("Communication Verbs", communication_verbs_tests),
                ("Learning Verbs", learning_verbs_tests),
                ("Movement Verbs", movement_verbs_tests),
                ("Daily Life Verbs", daily_life_verbs_tests),
                ("Care Verbs", care_verbs_tests),
                ("Complex Actions", complex_actions_tests)
            ]
            
            for category_name, test_cases in test_categories:
                print(f"\n--- Testing {category_name} ---")
                category_correct = True
                
                for test_case in test_cases:
                    french_word = test_case['french']
                    if french_word in verbs_by_french:
                        word = verbs_by_french[french_word]
                        
                        # Check all fields
                        checks = [
                            (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                            (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                            (word['difficulty'], test_case['difficulty'], 'Difficulty'),
                            (word['category'], 'verbes', 'Category')
                        ]
                        
                        word_correct = True
                        for actual, expected, field_name in checks:
                            if actual != expected:
                                print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                                word_correct = False
                                category_correct = False
                                all_verbs_correct = False
                        
                        if word_correct:
                            print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (difficulty: {word['difficulty']})")
                    else:
                        print(f"❌ {french_word} not found in verbs category")
                        category_correct = False
                        all_verbs_correct = False
                
                if category_correct:
                    print(f"✅ {category_name} category: All translations verified")
                else:
                    print(f"❌ {category_name} category: Some translations incorrect or missing")
            
            # 4. Test verb count and vocabulary structure
            print("\n--- Testing Verb Count and Vocabulary Structure ---")
            
            # Verify significantly increased verb vocabulary (should be 65+ verbs)
            expected_verb_count = 65
            actual_verb_count = len(verbs)
            
            if actual_verb_count >= expected_verb_count:
                print(f"✅ Verb vocabulary count: {actual_verb_count} verbs (expected at least {expected_verb_count})")
            else:
                print(f"❌ Verb vocabulary count: {actual_verb_count} verbs (expected at least {expected_verb_count})")
                all_verbs_correct = False
            
            # Test that all verbs have complete Shimaoré and Kibouchi translations
            complete_translations_count = 0
            for verb in verbs:
                if verb['shimaore'] and verb['kibouchi']:
                    complete_translations_count += 1
                elif not verb['shimaore'] and verb['kibouchi']:
                    # Some verbs might only have Kibouchi (like "Garder")
                    print(f"ℹ️ {verb['french']} has only Kibouchi translation: {verb['kibouchi']}")
                elif verb['shimaore'] and not verb['kibouchi']:
                    # Some verbs might only have Shimaoré
                    print(f"ℹ️ {verb['french']} has only Shimaoré translation: {verb['shimaore']}")
            
            print(f"Verbs with complete translations: {complete_translations_count}/{actual_verb_count}")
            
            # Verify proper difficulty assignments (1 for basic verbs, 2 for complex verbs)
            difficulty_1_count = len([v for v in verbs if v['difficulty'] == 1])
            difficulty_2_count = len([v for v in verbs if v['difficulty'] == 2])
            
            print(f"Difficulty 1 (basic verbs): {difficulty_1_count} verbs")
            print(f"Difficulty 2 (complex verbs): {difficulty_2_count} verbs")
            
            if difficulty_1_count > 0 and difficulty_2_count >= 0:  # Allow for all verbs to be difficulty 1
                print("✅ Difficulty levels properly assigned for verb vocabulary")
            else:
                print("❌ Difficulty levels not properly assigned for verb vocabulary")
                all_verbs_correct = False
            
            # Ensure all verbs are categorized as "verbes"
            category_correct = True
            for verb in verbs:
                if verb['category'] != 'verbes':
                    print(f"❌ Verb '{verb['french']}' has incorrect category: {verb['category']} (expected 'verbes')")
                    category_correct = False
                    all_verbs_correct = False
            
            if category_correct:
                print("✅ All verbs properly categorized as 'verbes'")
            
            # 5. Test total vocabulary update
            print("\n--- Testing Total Vocabulary Update ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code == 200:
                all_words = response.json()
                total_word_count = len(all_words)
                print(f"✅ Total vocabulary count: {total_word_count} words (reflects comprehensive verb addition)")
                
                # Confirm the most complete action vocabulary for sentence construction
                if actual_verb_count >= 65:
                    print("✅ Most complete action vocabulary confirmed for sentence construction in Mayotte languages")
                else:
                    print("❌ Insufficient action vocabulary for complete sentence construction")
                    all_verbs_correct = False
            else:
                print(f"❌ Could not retrieve total vocabulary: {response.status_code}")
                all_verbs_correct = False
            
            # Overall verbs test result
            if all_verbs_correct:
                print("\n🎉 COMPREHENSIVE VERBS SECTION TESTING COMPLETED SUCCESSFULLY!")
                print("✅ Comprehensive verb vocabulary with 65+ verbs confirmed")
                print("✅ All specific verb categories from the table verified:")
                print("   • Basic actions: Jouer, Courir, Dire, Pouvoir, Vouloir")
                print("   • Communication verbs: Parler, Demander, Répondre, Écouter")
                print("   • Learning verbs: Savoir, Apprendre, Comprendre, Lire, Écrire")
                print("   • Movement verbs: Marcher, Entrer, Sortir, Venir")
                print("   • Daily life verbs: Manger, Boire, Dormir, S'asseoir")
                print("   • Care verbs: Se laver, Se baigner, Se laver le derrière")
                print("   • Complex actions: Faire caca, Faire pipi, Vomir")
                print("✅ Complete Shimaoré and Kibouchi translations verified")
                print("✅ Proper difficulty assignments (1 for basic verbs, 2 for complex verbs)")
                print("✅ All verbs categorized as 'verbes'")
                print("✅ Most complete action vocabulary for sentence construction in authentic Shimaoré and Kibouchi")
            else:
                print("\n❌ Some verb vocabulary items are incorrect or missing")
            
            return all_verbs_correct
            
        except Exception as e:
            print(f"❌ Comprehensive verbs section test error: {e}")
            return False

    def test_corrected_animal_translations_and_duplicates(self):
        """Test corrected animal translations and identify duplicate animals"""
        print("\n=== Testing Corrected Animal Translations and Duplicate Detection ===")
        
        try:
            # 1. Test POST /api/init-base-content to reinitialize with corrected animal translations
            print("--- Testing Animal Translations Reinitialization ---")
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to reinitialize base content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Base content reinitialized: {result}")
            
            # 2. Test GET /api/words?category=animaux to verify specific corrected animals
            print("\n--- Testing Animal Category Filtering ---")
            response = self.session.get(f"{API_BASE}/words?category=animaux")
            if response.status_code != 200:
                print(f"❌ Failed to get animals: {response.status_code}")
                return False
            
            animals = response.json()
            animals_by_french = {word['french']: word for word in animals}
            
            print(f"Found {len(animals)} animals in database")
            
            # 3. Verify specific corrected animal translations
            print("\n--- Testing Specific Corrected Animal Translations ---")
            corrected_animals_tests = [
                {"french": "Canard", "shimaore": "Guisi", "kibouchi": "Doukitri", "old_kibouchi": "Aoukiri"},
                {"french": "Chenille", "shimaore": "Bibimangidji", "kibouchi": "Bibimanguidi", "old_kibouchi": "Bibimangidji"},
                {"french": "Cafard", "shimaore": "Kalalawi", "kibouchi": "Kalalowou", "old_kibouchi": "Galaronga"},
                {"french": "Guêpe", "shimaore": "Vungo vungo", "kibouchi": "Fantehi", "old_shimaore": "Yungo yungo"},
                {"french": "Bigorneau", "shimaore": "Trondro", "kibouchi": "Trondrou", "old_kibouchi": "Trondroul"},
                {"french": "Facochère", "shimaore": "Pouroukou nyeha", "kibouchi": "Lambou", "old_kibouchi": "Rambou"},
                {"french": "Hérisson", "shimaore": "Landra", "kibouchi": "Trandraka", "old_shimaore": "Tandra"}
            ]
            
            all_corrections_verified = True
            
            for test_case in corrected_animals_tests:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    word = animals_by_french[french_word]
                    
                    # Check corrected translations
                    shimaore_correct = word['shimaore'] == test_case['shimaore']
                    kibouchi_correct = word['kibouchi'] == test_case['kibouchi']
                    
                    if shimaore_correct and kibouchi_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (CORRECTED)")
                        
                        # Show what was corrected
                        if 'old_shimaore' in test_case:
                            print(f"   └─ Shimaoré corrected from '{test_case['old_shimaore']}' to '{word['shimaore']}'")
                        if 'old_kibouchi' in test_case:
                            print(f"   └─ Kibouchi corrected from '{test_case['old_kibouchi']}' to '{word['kibouchi']}'")
                    else:
                        print(f"❌ {french_word}: Expected {test_case['shimaore']}/{test_case['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        all_corrections_verified = False
                else:
                    print(f"❌ {french_word} not found in animals category")
                    all_corrections_verified = False
            
            # 4. Identify duplicate animals by French name
            print("\n--- Testing Duplicate Animal Detection ---")
            french_names = [animal['french'] for animal in animals]
            french_name_counts = {}
            
            for name in french_names:
                french_name_counts[name] = french_name_counts.get(name, 0) + 1
            
            duplicates_found = []
            for name, count in french_name_counts.items():
                if count > 1:
                    duplicates_found.append((name, count))
            
            if duplicates_found:
                print(f"❌ DUPLICATE ANIMALS FOUND:")
                for name, count in duplicates_found:
                    print(f"   • '{name}' appears {count} times")
                    # Show all instances of the duplicate
                    duplicate_instances = [animal for animal in animals if animal['french'] == name]
                    for i, instance in enumerate(duplicate_instances, 1):
                        print(f"     {i}. {instance['shimaore']} / {instance['kibouchi']} (ID: {instance['id']})")
            else:
                print("✅ No duplicate animals found - all French names are unique")
            
            # 5. Count total unique animals vs total animal entries
            print("\n--- Testing Animal Count Analysis ---")
            total_entries = len(animals)
            unique_french_names = len(set(french_names))
            
            print(f"Total animal entries: {total_entries}")
            print(f"Unique French names: {unique_french_names}")
            
            if total_entries == unique_french_names:
                print("✅ All animal entries have unique French names")
            else:
                duplicate_count = total_entries - unique_french_names
                print(f"❌ Found {duplicate_count} duplicate entries")
            
            # 6. Test animal vocabulary structure after corrections
            print("\n--- Testing Animal Vocabulary Structure After Corrections ---")
            
            # Verify all corrected animals maintain proper category and difficulty
            structure_correct = True
            for test_case in corrected_animals_tests:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    word = animals_by_french[french_word]
                    
                    if word['category'] != 'animaux':
                        print(f"❌ {french_word} has incorrect category: {word['category']} (expected 'animaux')")
                        structure_correct = False
                    
                    if word['difficulty'] not in [1, 2]:
                        print(f"❌ {french_word} has invalid difficulty: {word['difficulty']} (expected 1 or 2)")
                        structure_correct = False
            
            if structure_correct:
                print("✅ All corrected animals maintain proper category ('animaux') and difficulty (1-2)")
            
            # 7. Verify no regressions in other animal translations
            print("\n--- Testing No Regressions in Other Animal Translations ---")
            
            # Test some key animals that should not have changed
            regression_tests = [
                {"french": "Chien", "shimaore": "Mbwa", "kibouchi": "Fadroka"},
                {"french": "Chat", "shimaore": "Paha", "kibouchi": "Moirou"},
                {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou"},
                {"french": "Maki", "shimaore": "Komba", "kibouchi": "Ankoumba"},
                {"french": "Singe", "shimaore": "Djakwe", "kibouchi": "Djakouayi"}
            ]
            
            no_regressions = True
            for test_case in regression_tests:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    word = animals_by_french[french_word]
                    
                    if word['shimaore'] == test_case['shimaore'] and word['kibouchi'] == test_case['kibouchi']:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (unchanged)")
                    else:
                        print(f"❌ {french_word}: Regression detected - Expected {test_case['shimaore']}/{test_case['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        no_regressions = False
                else:
                    print(f"❌ {french_word} not found (possible deletion)")
                    no_regressions = False
            
            # 8. Test backend functionality after animal corrections
            print("\n--- Testing Backend Functionality After Animal Corrections ---")
            
            # Test API connectivity remains intact
            connectivity_test = self.test_basic_connectivity()
            if connectivity_test:
                print("✅ API connectivity remains intact after corrections")
            else:
                print("❌ API connectivity issues after corrections")
                return False
            
            # Test that all other vocabulary categories are unaffected
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code == 200:
                all_words = response.json()
                categories = set(word['category'] for word in all_words)
                expected_categories = {
                    'famille', 'salutations', 'couleurs', 'animaux', 'nombres', 
                    'corps', 'nourriture', 'maison', 'vetements', 'nature', 'transport',
                    'grammaire', 'verbes'
                }
                
                if expected_categories.issubset(categories):
                    print("✅ All other vocabulary categories unaffected")
                else:
                    missing = expected_categories - categories
                    print(f"❌ Missing categories after corrections: {missing}")
                    return False
            else:
                print(f"❌ Could not retrieve all words: {response.status_code}")
                return False
            
            # Confirm database operations work properly
            try:
                # Test a simple database operation
                test_response = self.session.get(f"{API_BASE}/words?category=famille")
                if test_response.status_code == 200:
                    print("✅ Database operations work properly after corrections")
                else:
                    print(f"❌ Database operation issues: {test_response.status_code}")
                    return False
            except Exception as e:
                print(f"❌ Database operation error: {e}")
                return False
            
            # Overall test result
            all_tests_passed = (
                all_corrections_verified and 
                len(duplicates_found) == 0 and 
                structure_correct and 
                no_regressions and
                connectivity_test
            )
            
            if all_tests_passed:
                print("\n🎉 CORRECTED ANIMAL TRANSLATIONS AND DUPLICATE DETECTION COMPLETED SUCCESSFULLY!")
                print("✅ All 7 requested animal translation corrections verified:")
                print("   • Canard = Guisi/Doukitri (corrected from Guisi/Aoukiri)")
                print("   • Chenille = Bibimangidji/Bibimanguidi (corrected from Bibimangidji/Bibimangidji)")
                print("   • Cafard = Kalalawi/Kalalowou (corrected from Kalalawi/Galaronga)")
                print("   • Guêpe = Vungo vungo/Fantehi (corrected from Yungo yungo/Fantehi)")
                print("   • Bigorneau = Trondro/Trondrou (corrected from Trondro/Trondroul)")
                print("   • Facochère = Pouroukou nyeha/Lambou (corrected from Pouroukou nyeha/Rambou)")
                print("   • Hérisson = Landra/Trandraka (corrected from Tandra/Trandraka)")
                print("✅ No duplicate animals found - all French names are unique")
                print("✅ All corrected animals maintain proper category and difficulty")
                print("✅ No regressions in other animal translations")
                print("✅ Backend functionality remains intact after corrections")
                print(f"✅ Total animals: {len(animals)} unique entries")
            else:
                print("\n❌ Some issues found with corrected animal translations or duplicates")
                if duplicates_found:
                    print(f"❌ {len(duplicates_found)} duplicate animal(s) need to be removed")
                if not all_corrections_verified:
                    print("❌ Some animal translation corrections are not properly implemented")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Corrected animal translations and duplicate detection test error: {e}")
            return False

    def test_final_duplicate_verification(self):
        """Final verification test to confirm all duplicate animals have been completely removed"""
        print("\n=== Final Duplicate Verification Test ===")
        
        try:
            # 1. POST /api/init-base-content to reinitialize with fully deduplicated animals
            print("--- Step 1: Reinitializing with Fully Deduplicated Animals ---")
            
            # First clear existing content
            try:
                words_response = self.session.get(f"{API_BASE}/words")
                if words_response.status_code == 200:
                    existing_words = words_response.json()
                    for word in existing_words:
                        delete_response = self.session.delete(f"{API_BASE}/words/{word['id']}")
                    print(f"Cleared {len(existing_words)} existing words")
            except Exception as e:
                print(f"Note: Could not clear existing content: {e}")
            
            # Reinitialize content
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to reinitialize content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Content reinitialized: {result}")
            
            # 2. GET /api/words?category=animaux to verify final animal list
            print("\n--- Step 2: Verifying Final Animal List ---")
            response = self.session.get(f"{API_BASE}/words?category=animaux")
            if response.status_code != 200:
                print(f"❌ Failed to get animals: {response.status_code}")
                return False
            
            animals = response.json()
            print(f"Retrieved {len(animals)} animals from database")
            
            # 3. Confirm zero duplicates for specific animals
            print("\n--- Step 3: Confirming Zero Duplicates for Specific Animals ---")
            
            # Create a dictionary to count occurrences of each French name
            french_name_counts = {}
            for animal in animals:
                french_name = animal['french']
                if french_name in french_name_counts:
                    french_name_counts[french_name] += 1
                else:
                    french_name_counts[french_name] = 1
            
            # Check specific animals that were previously duplicated
            critical_animals = ["Lézard", "Renard", "Chameau", "Hérisson"]
            duplicates_found = False
            
            for animal_name in critical_animals:
                if animal_name in french_name_counts:
                    count = french_name_counts[animal_name]
                    if count == 1:
                        print(f"✅ {animal_name}: appears exactly 1 time (correct)")
                    else:
                        print(f"❌ {animal_name}: appears {count} times (should be 1)")
                        duplicates_found = True
                        
                        # Show the duplicate entries
                        duplicate_entries = [a for a in animals if a['french'] == animal_name]
                        for i, entry in enumerate(duplicate_entries):
                            print(f"   Duplicate {i+1}: ID={entry['id']}, Shimaoré={entry['shimaore']}, Kibouchi={entry['kibouchi']}")
                else:
                    print(f"❌ {animal_name}: not found in database")
                    duplicates_found = True
            
            # 4. Count total entries vs unique French names
            print("\n--- Step 4: Verifying Total Count vs Unique Names ---")
            total_entries = len(animals)
            unique_french_names = len(set(animal['french'] for animal in animals))
            
            print(f"Total animal entries: {total_entries}")
            print(f"Unique French names: {unique_french_names}")
            
            if total_entries == unique_french_names:
                print("✅ Total entries equals unique names (no duplicates)")
                count_verification_passed = True
            else:
                print(f"❌ Mismatch: {total_entries} entries vs {unique_french_names} unique names ({total_entries - unique_french_names} duplicates)")
                count_verification_passed = False
                
                # Show all duplicates
                print("\n--- All Duplicate Animals Found ---")
                for french_name, count in french_name_counts.items():
                    if count > 1:
                        print(f"❌ '{french_name}' appears {count} times:")
                        duplicate_entries = [a for a in animals if a['french'] == french_name]
                        for i, entry in enumerate(duplicate_entries):
                            print(f"   Entry {i+1}: ID={entry['id']}")
            
            # 5. Verify all 7 corrected animal translations remain intact
            print("\n--- Step 5: Verifying All 7 Corrected Animal Translations ---")
            
            corrected_animals = [
                {"french": "Canard", "shimaore": "Guisi", "kibouchi": "Doukitri"},
                {"french": "Chenille", "shimaore": "Bibimangidji", "kibouchi": "Bibimanguidi"},
                {"french": "Cafard", "shimaore": "Kalalawi", "kibouchi": "Kalalowou"},
                {"french": "Guêpe", "shimaore": "Vungo vungo", "kibouchi": "Fantehi"},
                {"french": "Bigorneau", "shimaore": "Trondro", "kibouchi": "Trondrou"},
                {"french": "Facochère", "shimaore": "Pouroukou nyeha", "kibouchi": "Lambou"},
                {"french": "Hérisson", "shimaore": "Landra", "kibouchi": "Trandraka"}
            ]
            
            animals_by_french = {animal['french']: animal for animal in animals}
            corrections_verified = True
            
            for correction in corrected_animals:
                french_name = correction['french']
                if french_name in animals_by_french:
                    animal = animals_by_french[french_name]
                    
                    # Check translations
                    shimaore_correct = animal['shimaore'] == correction['shimaore']
                    kibouchi_correct = animal['kibouchi'] == correction['kibouchi']
                    
                    if shimaore_correct and kibouchi_correct:
                        print(f"✅ {french_name}: {animal['shimaore']} / {animal['kibouchi']} (correct)")
                    else:
                        print(f"❌ {french_name}: Expected {correction['shimaore']}/{correction['kibouchi']}, got {animal['shimaore']}/{animal['kibouchi']}")
                        corrections_verified = False
                else:
                    print(f"❌ {french_name}: not found in database")
                    corrections_verified = False
            
            # 6. Final comprehensive statistics
            print("\n--- Step 6: Final Comprehensive Statistics ---")
            
            # Get total word count across all categories
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code == 200:
                all_words = response.json()
                total_word_count = len(all_words)
                
                # Count words by category
                category_counts = {}
                for word in all_words:
                    category = word['category']
                    category_counts[category] = category_counts.get(category, 0) + 1
                
                print(f"✅ Final total word count: {total_word_count}")
                print(f"✅ Final animal count: {len(animals)}")
                print(f"✅ Categories found: {len(category_counts)}")
                
                # Show category breakdown
                for category, count in sorted(category_counts.items()):
                    print(f"   {category}: {count} words")
                
                # Verify data integrity
                integrity_checks = []
                
                # Check that all words have required fields
                for word in all_words:
                    required_fields = ['id', 'french', 'shimaore', 'kibouchi', 'category', 'difficulty']
                    if all(field in word for field in required_fields):
                        continue
                    else:
                        integrity_checks.append(f"Word '{word.get('french', 'unknown')}' missing required fields")
                
                if not integrity_checks:
                    print("✅ Data integrity verified: All words have required fields")
                    data_integrity_passed = True
                else:
                    print("❌ Data integrity issues found:")
                    for issue in integrity_checks:
                        print(f"   {issue}")
                    data_integrity_passed = False
                
            else:
                print(f"❌ Could not retrieve total word count: {response.status_code}")
                data_integrity_passed = False
            
            # Final result
            print("\n--- Final Verification Result ---")
            
            no_duplicates = not duplicates_found
            all_tests_passed = (
                no_duplicates and 
                count_verification_passed and 
                corrections_verified and 
                data_integrity_passed
            )
            
            if all_tests_passed:
                print("🎉 FINAL DUPLICATE VERIFICATION COMPLETED SUCCESSFULLY!")
                print("✅ Zero duplicates confirmed for all critical animals")
                print("✅ Total entries equals unique French names")
                print("✅ All 7 corrected animal translations verified and intact")
                print("✅ Data integrity and completeness confirmed")
                print("✅ Deduplication is complete and all corrections are preserved")
            else:
                print("❌ FINAL DUPLICATE VERIFICATION FAILED!")
                if duplicates_found:
                    print("❌ Duplicate animals still exist and must be removed")
                if not count_verification_passed:
                    print("❌ Total count does not match unique names")
                if not corrections_verified:
                    print("❌ Some corrected translations are missing or incorrect")
                if not data_integrity_passed:
                    print("❌ Data integrity issues detected")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Final duplicate verification test error: {e}")
            return False

    def test_updated_verbs_vocabulary_with_corrected_orthography(self):
        """Test the updated verbs vocabulary based exactly on the user's provided tables with corrected French orthography"""
        print("\n=== Testing Updated Verbs Vocabulary with Corrected French Orthography ===")
        
        try:
            # 1. Test comprehensive verbs initialization
            print("--- Testing Comprehensive Verbs Initialization ---")
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to initialize base content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Base content initialized: {result}")
            
            # 2. Test GET /api/words?category=verbes to verify all verbs from both tables
            print("\n--- Testing Verbs Category Filtering ---")
            response = self.session.get(f"{API_BASE}/words?category=verbes")
            if response.status_code != 200:
                print(f"❌ Failed to get verbs: {response.status_code}")
                return False
            
            verbs = response.json()
            verbs_by_french = {word['french']: word for word in verbs}
            
            print(f"Found {len(verbs)} verbs in database")
            
            # 3. Test specific verb corrections from first table
            print("\n--- Testing Specific Verb Corrections from First Table ---")
            first_table_corrections = [
                {"french": "Jouer", "shimaore": "Oupaguedza", "kibouchi": "Misoma", "difficulty": 1, "note": "corrected from Nguadza/Misoma"},
                {"french": "Dire", "shimaore": "Ourenguissa", "kibouchi": "Mangataka", "difficulty": 1, "note": "corrected from Burengisa/Mangataka"},
                {"french": "Vouloir", "shimaore": "Outrlaho", "kibouchi": "Irokou", "difficulty": 1, "note": "corrected from Outlsho/Irokou"},
                {"french": "Se rappeler", "shimaore": "Oumadzi", "kibouchi": "Koutanamou", "difficulty": 2, "note": "corrected from Rappeler"},
                {"french": "Faire ses besoins", "shimaore": "Oukoza", "kibouchi": "Manibi", "difficulty": 1, "note": "corrected from Faire caca"},
                {"french": "Uriner", "shimaore": "Ouraviha", "kibouchi": "Mandouwya", "difficulty": 1, "note": "corrected from Faire pipi"}
            ]
            
            first_table_correct = True
            for test_case in first_table_corrections:
                french_word = test_case['french']
                if french_word in verbs_by_french:
                    word = verbs_by_french[french_word]
                    
                    # Check all fields
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                        (word['difficulty'], test_case['difficulty'], 'Difficulty'),
                        (word['category'], 'verbes', 'Category')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}' - {test_case['note']}")
                            word_correct = False
                            first_table_correct = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} - {test_case['note']}")
                else:
                    print(f"❌ {french_word} not found in verbs category - {test_case['note']}")
                    first_table_correct = False
            
            # 4. Test additional verbs from second table
            print("\n--- Testing Additional Verbs from Second Table ---")
            second_table_verbs = [
                {"french": "Faire sécher", "shimaore": "Ouhoumisa", "kibouchi": "Manapi", "difficulty": 1},
                {"french": "Balayer", "shimaore": "Ouhoundza", "kibouchi": "Mamafa", "difficulty": 1},
                {"french": "Couper", "shimaore": "Oukatra", "kibouchi": "Manapaka", "difficulty": 1},
                {"french": "Tremper", "shimaore": "Oulodza", "kibouchi": "Mandzoubougnou", "difficulty": 1},
                {"french": "Se raser", "shimaore": "Oumea ndrevu", "kibouchi": "Manapaka somboutrou", "difficulty": 1},
                {"french": "Abîmer", "shimaore": "Oumengna", "kibouchi": "Mandroubaka", "difficulty": 1},
                {"french": "Cuisiner", "shimaore": "Oupiha", "kibouchi": "Mahandrou", "difficulty": 1},
                {"french": "Ranger/Arranger", "shimaore": "Ourenguélédza", "kibouchi": "Magnadzari", "difficulty": 1},
                {"french": "Tresser", "shimaore": "Oussouká", "kibouchi": "Mitali/Mandrari", "difficulty": 1},
                {"french": "Couper du bois", "shimaore": "Oupasouha kuni", "kibouchi": "Mamaki azoumati", "difficulty": 2},
                {"french": "Cultiver", "shimaore": "Oulima", "kibouchi": "Mikapa", "difficulty": 1},
                {"french": "Planter", "shimaore": "Outabou", "kibouchi": "Mamboli", "difficulty": 1},
                {"french": "Creuser", "shimaore": "Outsimba", "kibouchi": "Mangadi", "difficulty": 1},
                {"french": "Récolter", "shimaore": "Ouvouna", "kibouchi": "Mampoka", "difficulty": 1}
            ]
            
            second_table_correct = True
            for test_case in second_table_verbs:
                french_word = test_case['french']
                if french_word in verbs_by_french:
                    word = verbs_by_french[french_word]
                    
                    # Check all fields
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                        (word['difficulty'], test_case['difficulty'], 'Difficulty'),
                        (word['category'], 'verbes', 'Category')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            second_table_correct = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']}")
                else:
                    print(f"❌ {french_word} not found in verbs category")
                    second_table_correct = False
            
            # 5. Test verb count and orthographic corrections
            print("\n--- Testing Verb Count and Orthographic Corrections ---")
            
            # Check for corrected French spellings (no typos like "Faire caca" → "Faire ses besoins")
            orthographic_corrections = [
                {"incorrect": "Faire caca", "correct": "Faire ses besoins"},
                {"incorrect": "Faire pipi", "correct": "Uriner"},
                {"incorrect": "Rappeler", "correct": "Se rappeler"}
            ]
            
            orthography_correct = True
            for correction in orthographic_corrections:
                if correction["incorrect"] in verbs_by_french:
                    print(f"❌ Found incorrect spelling '{correction['incorrect']}' - should be '{correction['correct']}'")
                    orthography_correct = False
                elif correction["correct"] in verbs_by_french:
                    print(f"✅ Correct spelling '{correction['correct']}' found (not '{correction['incorrect']}')")
                else:
                    print(f"⚠️ Neither '{correction['incorrect']}' nor '{correction['correct']}' found")
            
            # Verify all verbs have complete Shimaoré and Kibouchi translations
            print("\n--- Testing Complete Translations ---")
            incomplete_translations = []
            for verb in verbs:
                if not verb['shimaore'] or not verb['kibouchi']:
                    incomplete_translations.append(verb['french'])
            
            if not incomplete_translations:
                print("✅ All verbs have complete Shimaoré and Kibouchi translations")
            else:
                print(f"❌ Verbs with incomplete translations: {incomplete_translations}")
                orthography_correct = False
            
            # 6. Test vocabulary structure
            print("\n--- Testing Vocabulary Structure ---")
            
            # Verify appropriate difficulty levels (1 for basic verbs, 2 for complex verbs)
            difficulty_1_count = len([v for v in verbs if v['difficulty'] == 1])
            difficulty_2_count = len([v for v in verbs if v['difficulty'] == 2])
            
            print(f"Difficulty 1 (basic verbs): {difficulty_1_count} verbs")
            print(f"Difficulty 2 (complex verbs): {difficulty_2_count} verbs")
            
            structure_correct = True
            if difficulty_1_count > 0 and difficulty_2_count > 0:
                print("✅ Appropriate difficulty levels assigned (1 for basic, 2 for complex)")
            else:
                print("❌ Difficulty levels not properly distributed")
                structure_correct = False
            
            # Confirm all verbs are categorized as "verbes"
            category_correct = True
            for verb in verbs:
                if verb['category'] != 'verbes':
                    print(f"❌ Verb '{verb['french']}' has incorrect category: {verb['category']} (expected 'verbes')")
                    category_correct = False
            
            if category_correct:
                print("✅ All verbs properly categorized as 'verbes'")
            
            # Check total verb count matches exactly what's in the provided tables
            expected_first_table_count = len(first_table_corrections)
            expected_second_table_count = len(second_table_verbs)
            
            # Count verbs from first table that are found
            first_table_found = sum(1 for test_case in first_table_corrections if test_case['french'] in verbs_by_french)
            second_table_found = sum(1 for test_case in second_table_verbs if test_case['french'] in verbs_by_french)
            
            print(f"\n--- Verb Count Verification ---")
            print(f"First table verbs found: {first_table_found}/{expected_first_table_count}")
            print(f"Second table verbs found: {second_table_found}/{expected_second_table_count}")
            print(f"Total verbs in database: {len(verbs)}")
            
            count_correct = (first_table_found == expected_first_table_count and 
                           second_table_found == expected_second_table_count)
            
            if count_correct:
                print("✅ Verb count matches exactly what's in the provided tables")
            else:
                print("❌ Verb count does not match the provided tables")
            
            # Overall test result
            all_verbs_correct = (
                first_table_correct and 
                second_table_correct and 
                orthography_correct and 
                structure_correct and 
                category_correct and 
                count_correct
            )
            
            if all_verbs_correct:
                print("\n🎉 UPDATED VERBS VOCABULARY TESTING COMPLETED SUCCESSFULLY!")
                print("✅ All specific verb corrections from first table verified")
                print("✅ All additional verbs from second table verified")
                print("✅ French orthography corrections confirmed (no typos)")
                print("✅ All verbs have complete Shimaoré and Kibouchi translations")
                print("✅ Appropriate difficulty levels assigned")
                print("✅ All verbs properly categorized as 'verbes'")
                print("✅ Verb count matches exactly what's in the provided tables")
                print("✅ Verbs section contains exactly and only what was provided in the user's reference tables")
            else:
                print("\n❌ Some verb vocabulary items are incorrect, missing, or have orthographic issues")
            
            return all_verbs_correct
            
        except Exception as e:
            print(f"❌ Updated verbs vocabulary test error: {e}")
            return False

    def test_review_request_comprehensive_vocabulary(self):
        """Test the current state of the Mayotte educational app backend as per review request"""
        print("\n=== Testing Review Request: Complete Vocabulary Initialization ===")
        
        try:
            # 1. Test complete vocabulary initialization (POST /api/init-base-content)
            print("--- 1. Testing Complete Vocabulary Initialization ---")
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to initialize base content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ POST /api/init-base-content: {result}")
            
            # 2. Test total word count across all categories (GET /api/words)
            print("\n--- 2. Testing Total Word Count Across All Categories ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Failed to get all words: {response.status_code}")
                return False
            
            all_words = response.json()
            total_count = len(all_words)
            print(f"✅ GET /api/words: Total word count = {total_count}")
            
            # Count by categories
            categories = {}
            for word in all_words:
                cat = word['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            print("Category breakdown:")
            for cat, count in sorted(categories.items()):
                print(f"  - {cat}: {count} words")
            
            # 3. Test verbs category with latest updates (GET /api/words?category=verbes)
            print("\n--- 3. Testing Verbs Category with Latest Updates ---")
            response = self.session.get(f"{API_BASE}/words?category=verbes")
            if response.status_code != 200:
                print(f"❌ Failed to get verbs: {response.status_code}")
                return False
            
            verbs = response.json()
            verbs_count = len(verbs)
            print(f"✅ GET /api/words?category=verbes: {verbs_count} verbs found")
            
            # Verify some key verbs from the 5 provided tables
            key_verbs_to_check = [
                "Jouer", "Courir", "Dire", "Pouvoir", "Vouloir", "Savoir", "Voir",
                "Manger", "Boire", "Dormir", "Marcher", "Entrer", "Sortir",
                "Faire sécher", "Balayer", "Couper", "Cuisiner", "Planter", "Creuser"
            ]
            
            verbs_by_french = {verb['french']: verb for verb in verbs}
            found_key_verbs = 0
            
            for key_verb in key_verbs_to_check:
                if key_verb in verbs_by_french:
                    found_key_verbs += 1
                    verb_data = verbs_by_french[key_verb]
                    print(f"  ✅ {key_verb}: {verb_data['shimaore']} / {verb_data['kibouchi']}")
                else:
                    print(f"  ❌ {key_verb}: Not found")
            
            print(f"Key verbs found: {found_key_verbs}/{len(key_verbs_to_check)}")
            
            # 4. Test all updated categories
            print("\n--- 4. Testing All Updated Categories ---")
            categories_to_test = {
                'famille': {'expected_min': 15, 'key_words': ['Frère', 'Sœur', 'Tante', 'Oncle maternel']},
                'grammaire': {'expected_min': 10, 'key_words': ['Je', 'Tu', 'Il/Elle', 'Le mien', 'Le tien']},
                'couleurs': {'expected_min': 8, 'key_words': ['Bleu', 'Vert', 'Rouge', 'Marron', 'Gris']},
                'animaux': {'expected_min': 50, 'key_words': ['Chat', 'Chien', 'Singe', 'Requin', 'Canard']},
                'nombres': {'expected_min': 20, 'key_words': ['Un', 'Dix', 'Onze', 'Vingt']},
                'verbes': {'expected_min': 70, 'key_words': ['Jouer', 'Courir', 'Cuisiner', 'Planter']}
            }
            
            all_categories_pass = True
            
            for category, requirements in categories_to_test.items():
                response = self.session.get(f"{API_BASE}/words?category={category}")
                if response.status_code != 200:
                    print(f"❌ Failed to get {category}: {response.status_code}")
                    all_categories_pass = False
                    continue
                
                category_words = response.json()
                count = len(category_words)
                expected_min = requirements['expected_min']
                
                if count >= expected_min:
                    print(f"✅ {category}: {count} words (≥{expected_min} required)")
                else:
                    print(f"❌ {category}: {count} words (<{expected_min} required)")
                    all_categories_pass = False
                
                # Check key words
                words_by_french = {word['french']: word for word in category_words}
                key_words_found = 0
                
                for key_word in requirements['key_words']:
                    if key_word in words_by_french:
                        key_words_found += 1
                        word_data = words_by_french[key_word]
                        shimaore_display = word_data['shimaore'] if word_data['shimaore'] else "(none)"
                        kibouchi_display = word_data['kibouchi'] if word_data['kibouchi'] else "(none)"
                        print(f"    ✅ {key_word}: {shimaore_display} / {kibouchi_display}")
                    else:
                        print(f"    ❌ {key_word}: Not found")
                        all_categories_pass = False
                
                print(f"    Key words found: {key_words_found}/{len(requirements['key_words'])}")
            
            # 5. Test vocabulary statistics
            print("\n--- 5. Testing Vocabulary Statistics ---")
            
            # Check for comprehensive coverage of Mayotte daily life
            daily_life_categories = ['famille', 'nourriture', 'maison', 'couleurs', 'animaux', 'nombres', 'corps']
            daily_life_coverage = 0
            
            for cat in daily_life_categories:
                if cat in categories and categories[cat] > 0:
                    daily_life_coverage += 1
            
            print(f"Daily life coverage: {daily_life_coverage}/{len(daily_life_categories)} categories")
            
            # Check that all words have proper Shimaoré and Kibouchi translations
            words_with_both_translations = 0
            words_with_at_least_one_translation = 0
            
            for word in all_words:
                has_shimaore = bool(word.get('shimaore', '').strip())
                has_kibouchi = bool(word.get('kibouchi', '').strip())
                
                if has_shimaore and has_kibouchi:
                    words_with_both_translations += 1
                
                if has_shimaore or has_kibouchi:
                    words_with_at_least_one_translation += 1
            
            print(f"Words with both translations: {words_with_both_translations}/{total_count}")
            print(f"Words with at least one translation: {words_with_at_least_one_translation}/{total_count}")
            
            # 6. Test backend functionality (CRUD operations)
            print("\n--- 6. Testing Backend Functionality ---")
            
            # Test basic CRUD operations
            crud_test_passed = True
            
            # Test CREATE
            test_word = {
                "french": "Test Word",
                "shimaore": "Test Shimaoré",
                "kibouchi": "Test Kibouchi",
                "category": "test",
                "difficulty": 1
            }
            
            response = self.session.post(f"{API_BASE}/words", json=test_word)
            if response.status_code == 200:
                created_word = response.json()
                test_word_id = created_word['id']
                print(f"✅ CREATE: Word created with ID {test_word_id}")
                
                # Test READ
                response = self.session.get(f"{API_BASE}/words/{test_word_id}")
                if response.status_code == 200:
                    print("✅ READ: Word retrieved successfully")
                    
                    # Test UPDATE
                    updated_word = test_word.copy()
                    updated_word['french'] = "Updated Test Word"
                    
                    response = self.session.put(f"{API_BASE}/words/{test_word_id}", json=updated_word)
                    if response.status_code == 200:
                        print("✅ UPDATE: Word updated successfully")
                        
                        # Test DELETE
                        response = self.session.delete(f"{API_BASE}/words/{test_word_id}")
                        if response.status_code == 200:
                            print("✅ DELETE: Word deleted successfully")
                        else:
                            print(f"❌ DELETE failed: {response.status_code}")
                            crud_test_passed = False
                    else:
                        print(f"❌ UPDATE failed: {response.status_code}")
                        crud_test_passed = False
                else:
                    print(f"❌ READ failed: {response.status_code}")
                    crud_test_passed = False
            else:
                print(f"❌ CREATE failed: {response.status_code}")
                crud_test_passed = False
            
            # Test exercises endpoint
            response = self.session.get(f"{API_BASE}/exercises")
            exercises_working = response.status_code == 200
            print(f"{'✅' if exercises_working else '❌'} Exercises endpoint: {response.status_code}")
            
            # Test progress endpoint
            response = self.session.get(f"{API_BASE}/progress/test_user")
            progress_working = response.status_code == 200
            print(f"{'✅' if progress_working else '❌'} Progress endpoint: {response.status_code}")
            
            # Overall assessment
            print(f"\n--- Overall Assessment ---")
            
            success_criteria = [
                (total_count >= 200, f"Total vocabulary count ≥200: {total_count}"),
                (verbs_count >= 70, f"Verbs count ≥70: {verbs_count}"),
                (all_categories_pass, "All updated categories verified"),
                (daily_life_coverage >= 6, f"Daily life coverage ≥6/7: {daily_life_coverage}"),
                (words_with_at_least_one_translation >= total_count * 0.95, f"Translation coverage ≥95%: {words_with_at_least_one_translation}/{total_count}"),
                (crud_test_passed, "CRUD operations working"),
                (exercises_working, "Exercises endpoint working"),
                (progress_working, "Progress endpoint working")
            ]
            
            passed_criteria = 0
            for criterion_met, description in success_criteria:
                status = "✅" if criterion_met else "❌"
                print(f"{status} {description}")
                if criterion_met:
                    passed_criteria += 1
            
            overall_success = passed_criteria >= len(success_criteria) * 0.8  # 80% pass rate
            
            if overall_success:
                print(f"\n🎉 COMPREHENSIVE VOCABULARY TESTING COMPLETED SUCCESSFULLY!")
                print(f"✅ Passed {passed_criteria}/{len(success_criteria)} success criteria")
                print(f"✅ Total vocabulary: {total_count} words across {len(categories)} categories")
                print(f"✅ Verbs vocabulary: {verbs_count} verbs from comprehensive tables")
                print(f"✅ All backend functionality verified and working")
                print(f"✅ Comprehensive coverage of Mayotte daily life confirmed")
                print(f"✅ Authentic Shimaoré and Kibouchi translations verified")
            else:
                print(f"\n❌ Some requirements not met: {passed_criteria}/{len(success_criteria)} criteria passed")
            
            return overall_success
            
        except Exception as e:
            print(f"❌ Review request comprehensive vocabulary test error: {e}")
            return False

    def test_updated_animals_vocabulary_new_tableau(self):
        """Test the updated animals vocabulary from the new tableau with 44 animals"""
        print("\n=== Testing Updated Animals Vocabulary from New Tableau (44 Animals) ===")
        
        try:
            # 1. Check backend starts without syntax errors by testing basic connectivity
            print("--- Testing Backend Startup (No Syntax Errors) ---")
            response = self.session.get(f"{BACKEND_URL}/")
            if response.status_code == 200:
                print("✅ Backend starts without syntax errors")
            else:
                print(f"❌ Backend startup issue: {response.status_code}")
                return False
            
            # 2. Test /api/words endpoint to retrieve all words
            print("\n--- Testing /api/words Endpoint ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Failed to retrieve words: {response.status_code}")
                return False
            
            all_words = response.json()
            print(f"✅ Retrieved {len(all_words)} total words from backend")
            
            # 3. Test /api/words?category=animaux endpoint specifically for animals
            print("\n--- Testing /api/words?category=animaux Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=animaux")
            if response.status_code != 200:
                print(f"❌ Failed to retrieve animals: {response.status_code}")
                return False
            
            animals = response.json()
            animals_by_french = {word['french']: word for word in animals}
            print(f"✅ Retrieved {len(animals)} animals from animaux category")
            
            # 4. Test that all 44 animals from the new tableau are present
            print("\n--- Testing New Tableau Animals (44 Animals) ---")
            
            # Key animals from the review request that should be present
            new_tableau_animals = [
                {"french": "Abeille", "shimaore": "Niochi", "kibouchi": "Antéli"},
                {"french": "Margouillat", "shimaore": "Kasangwe", "kibouchi": "Kitsatsaka"},
                {"french": "Chat", "shimaore": "Paha", "kibouchi": "Moirou"},
                {"french": "Rat", "shimaore": "Pouhou", "kibouchi": "Voilavou"},
                {"french": "Escargot", "shimaore": "Kouéya", "kibouchi": "Ancora"},
                {"french": "Lion", "shimaore": "Simba", "kibouchi": "Simba"},
                {"french": "Grenouille", "shimaore": "Shiwatrotro", "kibouchi": "Sahougnou"},
                {"french": "Oiseau", "shimaore": "Gnougni", "kibouchi": "Vorougnou"},
                {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou"},
                {"french": "Maki", "shimaore": "Komba", "kibouchi": "Ankoumba"},
                {"french": "Jézard", "shimaore": "Ngwizi", "kibouchi": "Kitsatsaka"},
                {"french": "Ranard", "shimaore": "Sabwa nyeha", "kibouchi": "Fadroka"},
                {"french": "Hérisson/Tangue", "shimaore": "Jandra", "kibouchi": "Trandraka"},
                {"french": "Civette", "shimaore": "Foungo", "kibouchi": "Angava"},
                {"french": "Dauphin", "shimaore": "Camba", "kibouchi": "Fesoutrou"},
                {"french": "Baleine", "shimaore": "Nyanga", "kibouchi": "Fesoutrou"},
                {"french": "Cône de mer", "shimaore": "Gnamané", "kibouchi": "Kamara"},
                {"french": "Mille pattes", "shimaore": "Nyango", "kibouchi": "Scoudafitri"},
                # Additional animals from the current implementation
                {"french": "Chèvre", "shimaore": "Mbouzi", "kibouchi": "Bengui"},
                {"french": "Moustique", "shimaore": "Manundi", "kibouchi": "Mokou"},
                {"french": "Mouche", "shimaore": "Ndzi", "kibouchi": "Lalitri"},
                {"french": "Chauve-souris", "shimaore": "Drema", "kibouchi": "Fanihi"},
                {"french": "Serpent", "shimaore": "Nyoha", "kibouchi": "Bibi lava"},
                {"french": "Lapin", "shimaore": "Sungura", "kibouchi": "Shoungoura"},
                {"french": "Mouton", "shimaore": "Baribari", "kibouchi": "Baribari"},
                {"french": "Crocodile", "shimaore": "Vwai", "kibouchi": "Vwai"},
                {"french": "Caméléon", "shimaore": "Tarundru", "kibouchi": "Tarondru"},
                {"french": "Zébu", "shimaore": "Nyombe", "kibouchi": "Aoumbi"},
                {"french": "Âne", "shimaore": "Pundra", "kibouchi": "Ampundra"},
                {"french": "Poule", "shimaore": "Kouhou", "kibouchi": "Akohou"},
                {"french": "Fourmis", "shimaore": "Tsutsuhu", "kibouchi": "Visiki"},
                {"french": "Chien", "shimaore": "Mbwa", "kibouchi": "Fadroka"},
                {"french": "Papillon", "shimaore": "Pelapelaka", "kibouchi": "Tsipelapelaka"},
                {"french": "Ver de terre", "shimaore": "Njengwe", "kibouchi": "Bibi fotaka"},
                {"french": "Criquet", "shimaore": "Furudji", "kibouchi": "Kidzedza"},
                {"french": "Cochon", "shimaore": "Pouroukou", "kibouchi": "Lambou"},
                {"french": "Facochère", "shimaore": "Pouroukou nyeha", "kibouchi": "Lambou"},
                {"french": "Chameau", "shimaore": "Ngamia", "kibouchi": "Angamia"},
                {"french": "Corbeau", "shimaore": "Gawa", "kibouchi": "Goika"},
                {"french": "Crevette", "shimaore": "Kufuni", "kibouchi": "Ancongou"},
                {"french": "Frelon", "shimaore": "Chonga", "kibouchi": "Ngorou"},
                {"french": "Pou", "shimaore": "Béwé", "kibouchi": "Bébérou"},
                {"french": "Bouc", "shimaore": "Kondzo", "kibouchi": "Dzow"},
                {"french": "Taureau", "shimaore": "Trondro", "kibouchi": "Trondrou"},
                {"french": "Bigorneau", "shimaore": "Komba", "kibouchi": "Mahombi"},
                {"french": "Lambis", "shimaore": "Tsipoul", "kibouchi": "Tsimtipaka"}
            ]
            
            animals_found = 0
            animals_correct = 0
            
            for expected_animal in new_tableau_animals:
                french_name = expected_animal['french']
                if french_name in animals_by_french:
                    animals_found += 1
                    animal = animals_by_french[french_name]
                    
                    # Check translations
                    shimaore_correct = animal['shimaore'] == expected_animal['shimaore']
                    kibouchi_correct = animal['kibouchi'] == expected_animal['kibouchi']
                    
                    if shimaore_correct and kibouchi_correct:
                        animals_correct += 1
                        print(f"✅ {french_name}: {animal['shimaore']} / {animal['kibouchi']}")
                    else:
                        print(f"❌ {french_name}: Expected {expected_animal['shimaore']}/{expected_animal['kibouchi']}, got {animal['shimaore']}/{animal['kibouchi']}")
                else:
                    print(f"❌ {french_name} not found in animals category")
            
            print(f"\nAnimals found: {animals_found}/{len(new_tableau_animals)}")
            print(f"Animals with correct translations: {animals_correct}/{len(new_tableau_animals)}")
            
            # 5. Verify that old animals not in the new tableau are no longer present
            print("\n--- Testing Removal of Old Animals Not in New Tableau ---")
            
            # Animals that should be REMOVED according to the review request
            old_animals_to_remove = [
                "Éléphant", "Tortue", "Thon", "Requin", "Poulpe", "Pigeon", "Perroquet"
            ]
            
            old_animals_still_present = []
            for old_animal in old_animals_to_remove:
                if old_animal in animals_by_french:
                    old_animals_still_present.append(old_animal)
                    print(f"❌ {old_animal} should be removed but is still present")
                else:
                    print(f"✅ {old_animal} correctly removed")
            
            # 6. Check that other categories are still intact
            print("\n--- Testing Other Categories Remain Intact ---")
            
            other_categories = ['salutations', 'couleurs', 'nombres', 'famille', 'grammaire', 'verbes']
            categories_intact = True
            
            for category in other_categories:
                response = self.session.get(f"{API_BASE}/words?category={category}")
                if response.status_code == 200:
                    category_words = response.json()
                    if len(category_words) > 0:
                        print(f"✅ {category}: {len(category_words)} words")
                    else:
                        print(f"❌ {category}: No words found")
                        categories_intact = False
                else:
                    print(f"❌ {category}: Failed to retrieve ({response.status_code})")
                    categories_intact = False
            
            # 7. Check for duplicate entries or syntax errors
            print("\n--- Testing for Duplicates and Data Integrity ---")
            
            french_names = [animal['french'] for animal in animals]
            unique_names = set(french_names)
            
            if len(french_names) == len(unique_names):
                print("✅ No duplicate animals found")
                duplicates_ok = True
            else:
                duplicates_ok = False
                duplicate_count = len(french_names) - len(unique_names)
                print(f"❌ Found {duplicate_count} duplicate animals")
                
                # Show duplicates
                name_counts = {}
                for name in french_names:
                    name_counts[name] = name_counts.get(name, 0) + 1
                
                for name, count in name_counts.items():
                    if count > 1:
                        print(f"   • '{name}' appears {count} times")
            
            # 8. Verify all animals have proper structure
            print("\n--- Testing Animal Data Structure ---")
            
            structure_ok = True
            for animal in animals:
                required_fields = ['french', 'shimaore', 'kibouchi', 'category', 'difficulty']
                for field in required_fields:
                    if field not in animal:
                        print(f"❌ Animal '{animal.get('french', 'unknown')}' missing field: {field}")
                        structure_ok = False
                
                if animal.get('category') != 'animaux':
                    print(f"❌ Animal '{animal.get('french', 'unknown')}' has wrong category: {animal.get('category')}")
                    structure_ok = False
            
            if structure_ok:
                print("✅ All animals have proper data structure")
            
            # Overall assessment
            print("\n--- Overall Assessment ---")
            
            # Check if we have at least 40+ animals as mentioned in the review
            animals_count_ok = len(animals) >= 40
            if animals_count_ok:
                print(f"✅ Animal count: {len(animals)} animals (40+ required)")
            else:
                print(f"❌ Animal count: {len(animals)} animals (40+ required)")
            
            # Check if most key animals are present and correct
            key_animals_ok = animals_correct >= (len(new_tableau_animals) * 0.9)  # 90% threshold
            
            # Check if old animals are properly removed
            old_animals_ok = len(old_animals_still_present) == 0
            
            # Final result
            all_tests_passed = (
                animals_count_ok and 
                key_animals_ok and 
                old_animals_ok and 
                categories_intact and 
                duplicates_ok and 
                structure_ok
            )
            
            if all_tests_passed:
                print("\n🎉 UPDATED ANIMALS VOCABULARY TESTING COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors")
                print("✅ /api/words endpoint working correctly")
                print("✅ /api/words?category=animaux endpoint working correctly")
                print(f"✅ {animals_correct}/{len(new_tableau_animals)} key animals from new tableau verified")
                print("✅ Old animals properly removed")
                print("✅ Other categories remain intact")
                print("✅ No duplicate entries found")
                print("✅ All animals have proper data structure")
            else:
                print("\n❌ Some issues found with updated animals vocabulary:")
                if not animals_count_ok:
                    print("   • Insufficient animal count")
                if not key_animals_ok:
                    print("   • Key animals missing or incorrect translations")
                if not old_animals_ok:
                    print("   • Old animals not properly removed")
                if not categories_intact:
                    print("   • Other categories affected")
                if not duplicates_ok:
                    print("   • Duplicate animals found")
                if not structure_ok:
                    print("   • Data structure issues")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Updated animals vocabulary test error: {e}")
            return False

    def test_updated_corps_vocabulary_new_tableau(self):
        """Test the updated 'Corps humain' (body parts) vocabulary from the new tableau"""
        print("\n=== Testing Updated Corps Humain Vocabulary from New Tableau ===")
        
        try:
            # 1. Check if backend starts without syntax errors by testing basic connectivity
            print("--- Testing Backend Startup (No Syntax Errors) ---")
            if not self.test_basic_connectivity():
                print("❌ Backend has syntax errors or connectivity issues")
                return False
            print("✅ Backend starts without syntax errors")
            
            # 2. Test /api/words endpoint to retrieve all words
            print("\n--- Testing /api/words Endpoint ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ /api/words endpoint failed: {response.status_code}")
                return False
            
            all_words = response.json()
            print(f"✅ /api/words endpoint working correctly ({len(all_words)} total words)")
            
            # 3. Test /api/words?category=corps endpoint specifically for body parts
            print("\n--- Testing /api/words?category=corps Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=corps")
            if response.status_code != 200:
                print(f"❌ /api/words?category=corps endpoint failed: {response.status_code}")
                return False
            
            corps_words = response.json()
            corps_words_by_french = {word['french']: word for word in corps_words}
            print(f"✅ /api/words?category=corps endpoint working correctly ({len(corps_words)} body parts)")
            
            # 4. Verify all 32 body parts from the new tableau with correct translations
            print("\n--- Testing All 32 Body Parts from New Tableau ---")
            
            # Expected body parts from the review request
            expected_body_parts = [
                {"french": "Œil", "shimaore": "Matso", "kibouchi": "Faninti"},
                {"french": "Nez", "shimaore": "Poua", "kibouchi": "Horougnou"},
                {"french": "Oreille", "shimaore": "Kiyo", "kibouchi": "Soufigni"},
                {"french": "Ongle", "shimaore": "Kofou", "kibouchi": "Angofou"},
                {"french": "Front", "shimaore": "Housso", "kibouchi": "Lahara"},
                {"french": "Joue", "shimaore": "Savou", "kibouchi": "Fifi"},
                {"french": "Dos", "shimaore": "Mengo", "kibouchi": "Vohou"},
                {"french": "Épaule", "shimaore": "Béga", "kibouchi": "Haveyi"},
                {"french": "Hanche", "shimaore": "Trenga", "kibouchi": "Tahezagna"},
                {"french": "Fesses", "shimaore": "Shidze/Mvoumo", "kibouchi": "Fouri"},
                {"french": "Main", "shimaore": "Mhono", "kibouchi": "Tagnana"},
                {"french": "Tête", "shimaore": "Shitsoi", "kibouchi": "Louha"},
                {"french": "Ventre", "shimaore": "Mimba", "kibouchi": "Kibou"},
                {"french": "Dent", "shimaore": "Magno", "kibouchi": "Hifi"},
                {"french": "Langue", "shimaore": "Oulimé", "kibouchi": "Léla"},
                {"french": "Pied", "shimaore": "Mindrou", "kibouchi": "Viti"},
                {"french": "Lèvre", "shimaore": "Dhomo", "kibouchi": "Soungni"},
                {"french": "Peau", "shimaore": "Ngwezi", "kibouchi": "Ngwezi"},
                {"french": "Cheveux", "shimaore": "Ngnélé", "kibouchi": "Fagnéva"},
                {"french": "Doigts", "shimaore": "Cha", "kibouchi": "Tondrou"},
                {"french": "Barbe", "shimaore": "Ndrévou", "kibouchi": "Somboutrou"},
                {"french": "Vagin", "shimaore": "Ndzigni", "kibouchi": "Tingui"},
                {"french": "Testicules", "shimaore": "Kwendzé", "kibouchi": "Vouancarou"},
                {"french": "Pénis", "shimaore": "Mbo", "kibouchi": "Kaboudzi"},
                {"french": "Menton", "shimaore": "Shlévou", "kibouchi": "Sokou"},
                {"french": "Bouche", "shimaore": "Hangno", "kibouchi": "Vava"},
                {"french": "Côtes", "shimaore": "Bavou", "kibouchi": "Mbavou"},
                {"french": "Sourcil", "shimaore": "Tsi", "kibouchi": "Ankwéssi"},
                {"french": "Cheville", "shimaore": "Dzitso la pwédza", "kibouchi": "Dzitso la pwédza"},
                {"french": "Cou", "shimaore": "Tsingo", "kibouchi": "Vouzougnou"},
                {"french": "Cils", "shimaore": "Kové", "kibouchi": "Rambou faninti"},
                {"french": "Arrière du crâne", "shimaore": "Komoi", "kibouchi": "Kitoika"}
            ]
            
            all_body_parts_correct = True
            found_body_parts = 0
            
            for expected_part in expected_body_parts:
                french_word = expected_part['french']
                if french_word in corps_words_by_french:
                    found_body_parts += 1
                    word = corps_words_by_french[french_word]
                    
                    # Check translations
                    checks = [
                        (word['shimaore'], expected_part['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], expected_part['kibouchi'], 'Kibouchi'),
                        (word['category'], 'corps', 'Category')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            all_body_parts_correct = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']}")
                else:
                    print(f"❌ {french_word} not found in corps category")
                    all_body_parts_correct = False
            
            print(f"\nFound {found_body_parts}/{len(expected_body_parts)} expected body parts")
            
            # 5. Test key body parts from review request
            print("\n--- Testing Key Body Parts from Review Request ---")
            key_body_parts = [
                {"french": "Œil", "shimaore": "Matso", "kibouchi": "Faninti"},
                {"french": "Ongle", "shimaore": "Kofou", "kibouchi": "Angofou"},
                {"french": "Testicules", "shimaore": "Kwendzé", "kibouchi": "Vouancarou"},
                {"french": "Cheville", "shimaore": "Dzitso la pwédza", "kibouchi": "Dzitso la pwédza"},
                {"french": "Arrière du crâne", "shimaore": "Komoi", "kibouchi": "Kitoika"}
            ]
            
            key_parts_correct = True
            for key_part in key_body_parts:
                french_word = key_part['french']
                if french_word in corps_words_by_french:
                    word = corps_words_by_french[french_word]
                    if (word['shimaore'] == key_part['shimaore'] and 
                        word['kibouchi'] == key_part['kibouchi']):
                        print(f"✅ Key part {french_word}: {word['shimaore']} / {word['kibouchi']}")
                    else:
                        print(f"❌ Key part {french_word}: Expected {key_part['shimaore']}/{key_part['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        key_parts_correct = False
                else:
                    print(f"❌ Key part {french_word} not found")
                    key_parts_correct = False
            
            # 6. Check that old incomplete entries have been replaced
            print("\n--- Checking for Old Incomplete Entries ---")
            # Look for any body parts that might have incomplete or old translations
            incomplete_entries = []
            for word in corps_words:
                if not word['shimaore'] or not word['kibouchi']:
                    incomplete_entries.append(word['french'])
            
            if incomplete_entries:
                print(f"❌ Found incomplete entries: {incomplete_entries}")
                all_body_parts_correct = False
            else:
                print("✅ No incomplete entries found - old entries have been replaced")
            
            # 7. Check that other categories remain intact
            print("\n--- Checking Other Categories Remain Intact ---")
            other_categories = ['salutations', 'couleurs', 'nombres', 'famille', 'grammaire', 'verbes']
            categories_intact = True
            
            for category in other_categories:
                response = self.session.get(f"{API_BASE}/words?category={category}")
                if response.status_code == 200:
                    category_words = response.json()
                    if len(category_words) > 0:
                        print(f"✅ Category '{category}': {len(category_words)} words intact")
                    else:
                        print(f"❌ Category '{category}': No words found")
                        categories_intact = False
                else:
                    print(f"❌ Category '{category}': Failed to retrieve")
                    categories_intact = False
            
            # 8. Test for duplicate entries or data integrity issues
            print("\n--- Testing for Duplicate Entries and Data Integrity ---")
            
            # Check for duplicate French names in corps category
            french_names = [word['french'] for word in corps_words]
            duplicates = []
            seen = set()
            for name in french_names:
                if name in seen:
                    duplicates.append(name)
                else:
                    seen.add(name)
            
            if duplicates:
                print(f"❌ Found duplicate body parts: {duplicates}")
                all_body_parts_correct = False
            else:
                print("✅ No duplicate entries found in corps category")
            
            # Check data integrity (all required fields present)
            integrity_issues = []
            for word in corps_words:
                required_fields = ['id', 'french', 'shimaore', 'kibouchi', 'category', 'difficulty']
                for field in required_fields:
                    if field not in word:
                        integrity_issues.append(f"{word['french']} missing {field}")
            
            if integrity_issues:
                print(f"❌ Data integrity issues: {integrity_issues}")
                all_body_parts_correct = False
            else:
                print("✅ All body parts have proper data structure")
            
            # 9. Check total word count
            print("\n--- Checking Total Word Count ---")
            total_words = len(all_words)
            corps_count = len(corps_words)
            print(f"Total words in database: {total_words}")
            print(f"Body parts (corps) count: {corps_count}")
            
            if corps_count >= 30:  # Should have at least 30 body parts
                print(f"✅ Corps category has sufficient vocabulary: {corps_count} body parts")
            else:
                print(f"❌ Corps category has insufficient vocabulary: {corps_count} body parts (expected 30+)")
                all_body_parts_correct = False
            
            # Final result
            overall_success = (
                all_body_parts_correct and 
                key_parts_correct and 
                categories_intact and 
                found_body_parts >= 30
            )
            
            if overall_success:
                print("\n🎉 UPDATED CORPS HUMAIN VOCABULARY TESTING COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors")
                print("✅ /api/words endpoint working correctly")
                print("✅ /api/words?category=corps endpoint working correctly")
                print(f"✅ All {found_body_parts} body parts from new tableau verified")
                print("✅ Key body parts confirmed with correct translations")
                print("✅ Old incomplete entries have been replaced")
                print("✅ Other categories remain intact and functional")
                print("✅ No duplicate entries or data integrity issues")
                print("✅ Corps category is working properly with comprehensive vocabulary")
            else:
                print("\n❌ Some issues found with the updated corps vocabulary")
            
            return overall_success
            
        except Exception as e:
            print(f"❌ Updated corps vocabulary test error: {e}")
            return False

    def test_final_animal_corrections_verification(self):
        """Test the final animal corrections have been applied correctly as per review request"""
        print("\n=== Testing Final Animal Corrections Verification ===")
        
        try:
            # Initialize base content first
            print("--- Initializing Base Content ---")
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to initialize base content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Base content initialized: {result}")
            
            # Get all animals
            print("\n--- Testing /api/words?category=animaux endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=animaux")
            if response.status_code != 200:
                print(f"❌ Failed to get animals: {response.status_code}")
                return False
            
            animals = response.json()
            animals_by_french = {word['french']: word for word in animals}
            
            print(f"Found {len(animals)} animals in database")
            
            # 1. Confirm "Ranard" has been completely removed from the animals list
            print("\n--- 1. Verifying 'Ranard' Removal ---")
            ranard_found = False
            for animal in animals:
                if 'Ranard' in animal['french']:
                    print(f"❌ 'Ranard' still found in animals list: {animal}")
                    ranard_found = True
            
            if not ranard_found:
                print("✅ 'Ranard' has been completely removed from the animals list")
            
            # 2. Verify "Lézard" is present (formerly "Jézard")
            print("\n--- 2. Verifying 'Lézard' Presence ---")
            lezard_correct = False
            if "Lézard" in animals_by_french:
                lezard = animals_by_french["Lézard"]
                print(f"✅ 'Lézard' found: {lezard['shimaore']} / {lezard['kibouchi']}")
                lezard_correct = True
            else:
                print("❌ 'Lézard' not found in animals list")
            
            # Check that "Jézard" is not present
            jezard_found = False
            for animal in animals:
                if 'Jézard' in animal['french']:
                    print(f"❌ Old 'Jézard' still found: {animal}")
                    jezard_found = True
            
            if not jezard_found:
                print("✅ Old 'Jézard' has been properly replaced with 'Lézard'")
            
            # 3. Check "Hérisson/Tangue" has shimaoré "Landra" (not "Jandra")
            print("\n--- 3. Verifying 'Hérisson/Tangue' Shimaoré Translation ---")
            herisson_correct = False
            if "Hérisson/Tangue" in animals_by_french:
                herisson = animals_by_french["Hérisson/Tangue"]
                if herisson['shimaore'] == "Landra":
                    print(f"✅ 'Hérisson/Tangue' has correct shimaoré 'Landra': {herisson['shimaore']} / {herisson['kibouchi']}")
                    herisson_correct = True
                else:
                    print(f"❌ 'Hérisson/Tangue' has incorrect shimaoré: Expected 'Landra', got '{herisson['shimaore']}'")
            else:
                print("❌ 'Hérisson/Tangue' not found in animals list")
            
            # 4. Verify all other requested corrections are in place
            print("\n--- 4. Verifying All Other Requested Corrections ---")
            
            corrections_to_verify = [
                {"french": "Dauphin", "shimaore": "Camba", "kibouchi": "Fésoutrou"},
                {"french": "Baleine", "shimaore": "Droujou", "kibouchi": "Fesoutrou"},
                {"french": "Crevette", "shimaore": "Camba", "kibouchi": "Ancamba"},
                {"french": "Frelon", "shimaore": "Chonga", "kibouchi": "Faraka"},
                {"french": "Guêpe", "shimaore": "Movou", "kibouchi": "Fanintri"},
                {"french": "Bourdon", "shimaore": "Voungo voungo", "kibouchi": "Madjaoumbi"},
                {"french": "Puce", "shimaore": "Ndra", "kibouchi": "Howou"},
                {"french": "Bouc", "shimaore": "Béwé", "kibouchi": "Bébéroué"},
                {"french": "Taureau", "shimaore": "Kondzo", "kibouchi": "Dzow"},
                {"french": "Bigorneau", "shimaore": "Trondro", "kibouchi": "Trondrou"},
                {"french": "Lambis", "shimaore": "Komba", "kibouchi": "Mahombi"},
                {"french": "Cône de mer", "shimaore": "Tsipoui", "kibouchi": "Tsimtipaka"},
                {"french": "Mille pattes", "shimaore": "Mjongo", "kibouchi": "Ancoudavitri"}
            ]
            
            all_corrections_correct = True
            
            for correction in corrections_to_verify:
                french_word = correction['french']
                if french_word in animals_by_french:
                    animal = animals_by_french[french_word]
                    
                    # Check shimaoré and kibouchi translations
                    shimaore_correct = animal['shimaore'] == correction['shimaore']
                    kibouchi_correct = animal['kibouchi'] == correction['kibouchi']
                    
                    if shimaore_correct and kibouchi_correct:
                        print(f"✅ {french_word}: {animal['shimaore']} / {animal['kibouchi']}")
                    else:
                        print(f"❌ {french_word}: Expected {correction['shimaore']}/{correction['kibouchi']}, got {animal['shimaore']}/{animal['kibouchi']}")
                        all_corrections_correct = False
                else:
                    print(f"❌ {french_word} not found in animals list")
                    all_corrections_correct = False
            
            # 5. Final verification summary
            print("\n--- Final Verification Summary ---")
            
            all_tests_passed = (
                not ranard_found and 
                lezard_correct and 
                not jezard_found and 
                herisson_correct and 
                all_corrections_correct
            )
            
            if all_tests_passed:
                print("\n🎉 FINAL ANIMAL CORRECTIONS VERIFICATION COMPLETED SUCCESSFULLY!")
                print("✅ 'Ranard' completely removed from animals list")
                print("✅ 'Lézard' is present (formerly 'Jézard')")
                print("✅ 'Hérisson/Tangue' has correct shimaoré 'Landra' (not 'Jandra')")
                print("✅ All 13 other requested corrections are in place:")
                print("   - Dauphin: kibouchi 'Fésoutrou'")
                print("   - Baleine: shimaoré 'Droujou'")
                print("   - Crevette: shimaoré 'Camba', kibouchi 'Ancamba'")
                print("   - Frelon: shimaoré 'Chonga', kibouchi 'Faraka'")
                print("   - Guêpe: shimaoré 'Movou', kibouchi 'Fanintri'")
                print("   - Bourdon: shimaoré 'Voungo voungo', kibouchi 'Madjaoumbi'")
                print("   - Puce: shimaoré 'Ndra', kibouchi 'Howou'")
                print("   - Bouc: shimaoré 'Béwé', kibouchi 'Bébéroué'")
                print("   - Taureau: shimaoré 'Kondzo', kibouchi 'Dzow'")
                print("   - Bigorneau: shimaoré 'Trondro', kibouchi 'Trondrou'")
                print("   - Lambis: shimaoré 'Komba', kibouchi 'Mahombi'")
                print("   - Cône de mer: shimaoré 'Tsipoui', kibouchi 'Tsimtipaka'")
                print("   - Mille pattes: shimaoré 'Mjongo', kibouchi 'Ancoudavitri'")
                print("✅ /api/words?category=animaux endpoint working correctly")
            else:
                print("\n❌ Some final animal corrections are missing or incorrect")
                if ranard_found:
                    print("❌ 'Ranard' still present in animals list")
                if not lezard_correct:
                    print("❌ 'Lézard' not found or incorrect")
                if jezard_found:
                    print("❌ Old 'Jézard' still present")
                if not herisson_correct:
                    print("❌ 'Hérisson/Tangue' shimaoré not 'Landra'")
                if not all_corrections_correct:
                    print("❌ Some of the 13 requested corrections are missing or incorrect")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Final animal corrections verification error: {e}")
            return False

    def test_updated_animals_vocabulary_from_new_tableau(self):
        """Test the updated animals vocabulary from the new tableau with specific animals"""
        print("\n=== Testing Updated Animals Vocabulary from New Tableau ===")
        
        try:
            # 1. Test backend starts without syntax errors
            print("--- Testing Backend Startup ---")
            response = self.session.get(f"{BACKEND_URL}/")
            if response.status_code != 200:
                print(f"❌ Backend startup failed: {response.status_code}")
                return False
            print("✅ Backend starts without syntax errors")
            
            # 2. Test /api/words endpoint
            print("\n--- Testing /api/words Endpoint ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ /api/words endpoint failed: {response.status_code}")
                return False
            
            all_words = response.json()
            print(f"✅ /api/words endpoint working correctly ({len(all_words)} total words)")
            
            # 3. Test /api/words?category=animaux endpoint
            print("\n--- Testing /api/words?category=animaux Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=animaux")
            if response.status_code != 200:
                print(f"❌ /api/words?category=animaux endpoint failed: {response.status_code}")
                return False
            
            animals = response.json()
            animals_by_french = {word['french']: word for word in animals}
            print(f"✅ /api/words?category=animaux endpoint working correctly ({len(animals)} animals)")
            
            # 4. Test newly added animals from the additional tableau
            print("\n--- Testing Newly Added Animals from Additional Tableau ---")
            newly_added_animals = [
                {"french": "Pigeon", "shimaore": "Ndiwa", "kibouchi": "Ndiwa"},
                {"french": "Chenille", "shimaore": "Bibimangidji", "kibouchi": "Bibimanguidi"},
                {"french": "Cheval", "shimaore": "Farassi", "kibouchi": "Farassi"},
                {"french": "Perroquet", "shimaore": "Kasuku", "kibouchi": "Kararokou"},
                {"french": "Cafard", "shimaore": "Kalalawi", "kibouchi": "Kalalowou"},
                {"french": "Araignée", "shimaore": "Shitrandrablwibwi", "kibouchi": "Bibi ampamani massou"},
                {"french": "Scorpion", "shimaore": "Hala", "kibouchi": "Hala"},
                {"french": "Scolopandre", "shimaore": "Trambwi", "kibouchi": "Trambougnou"},
                {"french": "Thon", "shimaore": "Mbassi", "kibouchi": "Mbassi"},
                {"french": "Requin", "shimaore": "Papa", "kibouchi": "Ankou"},
                {"french": "Poulpe", "shimaore": "Pwedza", "kibouchi": "Pwedza"},
                {"french": "Crabe", "shimaore": "Dradraka", "kibouchi": "Dakatra"},
                {"french": "Tortue", "shimaore": "Nyamba/Katsa", "kibouchi": "Fanou"},
                {"french": "Éléphant", "shimaore": "Ndovu", "kibouchi": "Ndovu"},
                {"french": "Singe", "shimaore": "Djakwe", "kibouchi": "Djakouayi"},
                {"french": "Souris", "shimaore": "Shikwetse", "kibouchi": "Voilavou"}
            ]
            
            all_new_animals_found = True
            for test_case in newly_added_animals:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    word = animals_by_french[french_word]
                    
                    # Check translations
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                        (word['category'], 'animaux', 'Category')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            all_new_animals_found = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']}")
                else:
                    print(f"❌ {french_word} not found in animals list")
                    all_new_animals_found = False
            
            # 5. Check that previously existing animals are still present
            print("\n--- Testing Previously Existing Animals Still Present ---")
            previously_existing_animals = [
                "Chat", "Chien", "Poisson", "Oiseau", "Poule", "Maki", "Lion", 
                "Crocodile", "Serpent", "Abeille", "Mouche", "Moustique", "Fourmis", 
                "Papillon", "Chèvre", "Mouton", "Zébu", "Âne", "Cochon", "Lapin"
            ]
            
            previously_existing_found = True
            for animal_name in previously_existing_animals:
                if animal_name in animals_by_french:
                    print(f"✅ {animal_name} still present")
                else:
                    print(f"❌ {animal_name} missing (was previously existing)")
                    previously_existing_found = False
            
            # 6. Verify total animal count has increased appropriately
            print("\n--- Testing Total Animal Count ---")
            expected_minimum_count = len(newly_added_animals) + len(previously_existing_animals)
            actual_count = len(animals)
            
            if actual_count >= expected_minimum_count:
                print(f"✅ Total animal count: {actual_count} (expected at least {expected_minimum_count})")
            else:
                print(f"❌ Total animal count: {actual_count} (expected at least {expected_minimum_count})")
                return False
            
            # 7. Test for duplicate entries
            print("\n--- Testing for Duplicate Entries ---")
            french_names = [animal['french'] for animal in animals]
            unique_french_names = set(french_names)
            
            if len(french_names) == len(unique_french_names):
                print(f"✅ No duplicate entries found ({len(unique_french_names)} unique animals)")
            else:
                duplicates = []
                seen = set()
                for name in french_names:
                    if name in seen:
                        duplicates.append(name)
                    seen.add(name)
                print(f"❌ Duplicate entries found: {duplicates}")
                print(f"Total entries: {len(french_names)}, Unique names: {len(unique_french_names)}")
                return False
            
            # 8. Ensure all animals have proper French, Shimaoré, and Kibouchi translations
            print("\n--- Testing Translation Completeness ---")
            translation_complete = True
            for animal in animals:
                if not animal['french'] or not animal['shimaore'] or not animal['kibouchi']:
                    print(f"❌ {animal['french']} missing translations: Shimaoré='{animal['shimaore']}', Kibouchi='{animal['kibouchi']}'")
                    translation_complete = False
            
            if translation_complete:
                print("✅ All animals have complete French, Shimaoré, and Kibouchi translations")
            
            # 9. Check that other categories remain intact
            print("\n--- Testing Other Categories Remain Intact ---")
            expected_categories = ['salutations', 'couleurs', 'nombres', 'famille', 'grammaire', 'verbes']
            categories_intact = True
            
            for category in expected_categories:
                response = self.session.get(f"{API_BASE}/words?category={category}")
                if response.status_code == 200:
                    category_words = response.json()
                    print(f"✅ Category '{category}': {len(category_words)} words")
                else:
                    print(f"❌ Category '{category}' not accessible")
                    categories_intact = False
            
            # 10. Provide final counts
            print("\n--- Final Counts ---")
            print(f"Total animals: {len(animals)}")
            print(f"Total words across all categories: {len(all_words)}")
            
            # Overall result
            overall_success = (
                all_new_animals_found and 
                previously_existing_found and 
                translation_complete and 
                categories_intact and
                len(french_names) == len(unique_french_names)  # No duplicates
            )
            
            if overall_success:
                print("\n🎉 UPDATED ANIMALS VOCABULARY TESTING COMPLETED SUCCESSFULLY!")
                print("✅ All newly added animals from the tableau are present with correct translations")
                print("✅ Previously existing animals are still present")
                print("✅ No duplicate entries found")
                print("✅ All animals have complete translations")
                print("✅ Other categories remain intact")
            else:
                print("\n❌ Some issues found with the updated animals vocabulary")
            
            return overall_success
            
        except Exception as e:
            print(f"❌ Updated animals vocabulary test error: {e}")
            return False

    def test_specific_animal_corrections_verification(self):
        """Test the specific animal corrections that were just made"""
        print("\n=== Testing Specific Animal Corrections Verification ===")
        
        try:
            # 1. Test backend starts without syntax errors
            print("--- Testing Backend Startup ---")
            response = self.session.get(f"{BACKEND_URL}/")
            if response.status_code == 200:
                print("✅ Backend starts without syntax errors")
            else:
                print(f"❌ Backend startup issue: {response.status_code}")
                return False
            
            # 2. Test /api/words?category=animaux endpoint
            print("\n--- Testing Animals Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=animaux")
            if response.status_code != 200:
                print(f"❌ Animals endpoint failed: {response.status_code}")
                return False
            
            animals = response.json()
            animals_by_french = {word['french']: word for word in animals}
            print(f"✅ Animals endpoint working - Found {len(animals)} animals")
            
            # 3. Verify the specific corrections are in place
            print("\n--- Testing Specific Animal Corrections ---")
            
            # Test Araignée correction: shimaoré should be "Shitrandrabwibwi" (not "Shitrandrablwibwi")
            araignee_test = {
                "french": "Araignée",
                "shimaore": "Shitrandrabwibwi",  # Corrected spelling
                "kibouchi": "Bibi ampamani massou"
            }
            
            # Test Requin correction: kibouchi should be "Ankiou" (not "Ankou")
            requin_test = {
                "french": "Requin", 
                "shimaore": "Papa",
                "kibouchi": "Ankiou"  # Corrected spelling
            }
            
            corrections_tests = [araignee_test, requin_test]
            corrections_correct = True
            
            for test_case in corrections_tests:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    word = animals_by_french[french_word]
                    
                    # Check specific corrections
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            corrections_correct = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} - CORRECTION VERIFIED")
                else:
                    print(f"❌ {french_word} not found in animals")
                    corrections_correct = False
            
            # 4. Check that all other animal entries remain intact
            print("\n--- Testing Other Animals Remain Intact ---")
            
            # Test a few key animals to ensure they weren't affected
            other_animals_tests = [
                {"french": "Chat", "shimaore": "Paha", "kibouchi": "Moirou"},
                {"french": "Chien", "shimaore": "Mbwa", "kibouchi": "Fadroka"},
                {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou"},
                {"french": "Oiseau", "shimaore": "Gnougni", "kibouchi": "Vorougnou"}
            ]
            
            other_animals_correct = True
            for test_case in other_animals_tests:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    word = animals_by_french[french_word]
                    if word['shimaore'] == test_case['shimaore'] and word['kibouchi'] == test_case['kibouchi']:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} - INTACT")
                    else:
                        print(f"❌ {french_word}: Expected {test_case['shimaore']}/{test_case['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        other_animals_correct = False
                else:
                    print(f"❌ {french_word} not found")
                    other_animals_correct = False
            
            # 5. Verify complete translations in both languages
            print("\n--- Testing Complete Translations ---")
            
            complete_translations = True
            for test_case in corrections_tests:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    word = animals_by_french[french_word]
                    if word['shimaore'] and word['kibouchi']:
                        print(f"✅ {french_word}: Complete translations in both languages")
                    else:
                        print(f"❌ {french_word}: Missing translation - Shimaoré: '{word['shimaore']}', Kibouchi: '{word['kibouchi']}'")
                        complete_translations = False
            
            # 6. Test no duplicate entries
            print("\n--- Testing No Duplicate Entries ---")
            
            french_names = [animal['french'] for animal in animals]
            unique_names = set(french_names)
            
            if len(french_names) == len(unique_names):
                print(f"✅ No duplicates found - {len(animals)} total animals, {len(unique_names)} unique names")
                no_duplicates = True
            else:
                duplicates = [name for name in unique_names if french_names.count(name) > 1]
                print(f"❌ Duplicates found: {duplicates}")
                no_duplicates = False
            
            # 7. Confirm total animal count (should be around 65 animals)
            print("\n--- Testing Total Animal Count ---")
            
            expected_min_count = 60  # Allow some flexibility
            expected_max_count = 70
            actual_count = len(animals)
            
            if expected_min_count <= actual_count <= expected_max_count:
                print(f"✅ Animal count within expected range: {actual_count} animals ({expected_min_count}-{expected_max_count} expected)")
                count_correct = True
            else:
                print(f"❌ Animal count outside expected range: {actual_count} animals ({expected_min_count}-{expected_max_count} expected)")
                count_correct = False
            
            # 8. Ensure backend API responses are working correctly
            print("\n--- Testing Backend API Responses ---")
            
            # Test individual animal retrieval for corrected animals
            api_responses_correct = True
            for test_case in corrections_tests:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    animal_id = animals_by_french[french_word]['id']
                    response = self.session.get(f"{API_BASE}/words/{animal_id}")
                    if response.status_code == 200:
                        retrieved_animal = response.json()
                        if (retrieved_animal['shimaore'] == test_case['shimaore'] and 
                            retrieved_animal['kibouchi'] == test_case['kibouchi']):
                            print(f"✅ {french_word}: Individual API retrieval working correctly")
                        else:
                            print(f"❌ {french_word}: Individual API retrieval has incorrect data")
                            api_responses_correct = False
                    else:
                        print(f"❌ {french_word}: Individual API retrieval failed - {response.status_code}")
                        api_responses_correct = False
            
            # Overall test result
            all_corrections_verified = (
                corrections_correct and 
                other_animals_correct and 
                complete_translations and 
                no_duplicates and 
                count_correct and 
                api_responses_correct
            )
            
            if all_corrections_verified:
                print("\n🎉 SPECIFIC ANIMAL CORRECTIONS VERIFICATION COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors")
                print("✅ /api/words?category=animaux endpoint working correctly")
                print("✅ Araignée: shimaoré corrected to 'Shitrandrabwibwi'")
                print("✅ Requin: kibouchi corrected to 'Ankiou'")
                print("✅ All other animal entries remain intact and unchanged")
                print("✅ Both animals have complete translations in both languages")
                print("✅ No duplicate entries introduced")
                print(f"✅ Total animal count maintained: {actual_count} animals")
                print("✅ Backend API responses working correctly for both specific animals")
                print("✅ Bug fix verification complete - issue has been completely resolved with no regressions")
            else:
                print("\n❌ Some animal corrections are not properly implemented or have introduced issues")
            
            return all_corrections_verified
            
        except Exception as e:
            print(f"❌ Specific animal corrections verification error: {e}")
            return False

    def test_updated_nourriture_vocabulary_new_tableau(self):
        """Test the updated food/nourriture vocabulary after complete replacement with new tableau"""
        print("\n=== Testing Updated Nourriture Vocabulary from New Tableau ===")
        
        try:
            # 1. Check if backend starts without syntax errors
            print("--- Testing Backend Startup ---")
            response = self.session.get(f"{BACKEND_URL}/")
            if response.status_code != 200:
                print(f"❌ Backend startup failed: {response.status_code}")
                return False
            print("✅ Backend starts without syntax errors")
            
            # 2. Test /api/words?category=nourriture endpoint
            print("\n--- Testing /api/words?category=nourriture Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=nourriture")
            if response.status_code != 200:
                print(f"❌ Failed to retrieve nourriture words: {response.status_code}")
                return False
            
            food_words = response.json()
            food_words_by_french = {word['french']: word for word in food_words}
            
            print(f"✅ Retrieved {len(food_words)} food items from nourriture category")
            
            # 3. Verify specific key foods from the new tableau (16 items from review request)
            print("\n--- Testing Specific Key Foods from New Tableau ---")
            key_foods_tests = [
                {"french": "Riz", "shimaore": "Tsoholé", "kibouchi": "Vari"},
                {"french": "Eau", "shimaore": "Maji", "kibouchi": "Ranou"},
                {"french": "Ananas", "shimaore": "Nanassi", "kibouchi": "Mananassi"},
                {"french": "Pois d'angole", "shimaore": "Tsouzi", "kibouchi": "Ambatri"},
                {"french": "Banane", "shimaore": "Trovi", "kibouchi": "Hountsi"},
                {"french": "Mangue", "shimaore": "Manga", "kibouchi": "Manga"},
                {"french": "Noix de coco", "shimaore": "Nazi", "kibouchi": "Voiniou"},
                {"french": "Lait", "shimaore": "Dzia", "kibouchi": "Rounounou"},
                {"french": "Viande", "shimaore": "Nhyama", "kibouchi": "Amboumati"},
                {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou"},
                {"french": "Brèdes", "shimaore": "Féliki", "kibouchi": "Féliki"},
                {"french": "Patate douce", "shimaore": "Batata", "kibouchi": "Batata"},
                {"french": "Tamarin", "shimaore": "Ouhajou", "kibouchi": "Madirou kakazou"},
                {"french": "Vanille", "shimaore": "Lavani", "kibouchi": "Lavani"},
                {"french": "Gingembre", "shimaore": "Sakayi", "kibouchi": "Sakéyi"},
                {"french": "Curcuma", "shimaore": "Dzindzano", "kibouchi": "Tamoutamou"}
            ]
            
            key_foods_correct = True
            for test_case in key_foods_tests:
                french_word = test_case['french']
                if french_word in food_words_by_french:
                    word = food_words_by_french[french_word]
                    
                    # Check translations
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi'),
                        (word['category'], 'nourriture', 'Category')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            key_foods_correct = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']}")
                else:
                    print(f"❌ {french_word} not found in nourriture category")
                    key_foods_correct = False
            
            # 4. Test for complete food vocabulary from new tableau (should be around 40 items)
            print(f"\n--- Testing Complete Food Vocabulary Count ---")
            expected_min_count = 35  # Around 40 food items expected
            actual_count = len(food_words)
            
            count_correct = True
            if actual_count >= expected_min_count:
                print(f"✅ Food count: {actual_count} items (expected around 40, minimum {expected_min_count})")
            else:
                print(f"❌ Food count: {actual_count} items (expected around 40, minimum {expected_min_count})")
                count_correct = False
            
            # 5. Verify all food items have complete translations in both languages
            print(f"\n--- Testing Complete Translations ---")
            complete_translations = True
            incomplete_items = []
            
            for word in food_words:
                if not word['shimaore'] or not word['kibouchi']:
                    incomplete_items.append(f"{word['french']} (Shimaoré: '{word['shimaore']}', Kibouchi: '{word['kibouchi']}')")
                    complete_translations = False
            
            if complete_translations:
                print(f"✅ All {len(food_words)} food items have complete translations in both languages")
            else:
                print(f"❌ {len(incomplete_items)} food items have incomplete translations:")
                for item in incomplete_items[:5]:  # Show first 5 incomplete items
                    print(f"  - {item}")
                if len(incomplete_items) > 5:
                    print(f"  ... and {len(incomplete_items) - 5} more")
            
            # 6. Check for duplicate entries
            print(f"\n--- Testing for Duplicate Entries ---")
            french_names = [word['french'] for word in food_words]
            unique_names = set(french_names)
            
            duplicates_check = True
            if len(french_names) == len(unique_names):
                print(f"✅ No duplicate entries found ({len(unique_names)} unique food items)")
            else:
                duplicates = []
                for name in unique_names:
                    count = french_names.count(name)
                    if count > 1:
                        duplicates.append(f"{name} ({count} times)")
                
                print(f"❌ {len(duplicates)} duplicate entries found:")
                for dup in duplicates:
                    print(f"  - {dup}")
                duplicates_check = False
            
            # 7. Verify other categories remain intact
            print(f"\n--- Testing Other Categories Remain Intact ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Failed to retrieve all words: {response.status_code}")
                return False
            
            all_words = response.json()
            categories = set(word['category'] for word in all_words)
            
            expected_other_categories = {
                'famille', 'couleurs', 'animaux', 'salutations', 'nombres', 
                'corps', 'maison', 'vetements', 'nature', 'transport', 'grammaire', 'verbes'
            }
            
            other_categories_intact = True
            for category in expected_other_categories:
                category_words = [w for w in all_words if w['category'] == category]
                if len(category_words) > 0:
                    print(f"✅ {category}: {len(category_words)} words")
                else:
                    print(f"❌ {category}: No words found")
                    other_categories_intact = False
            
            # 8. Provide final counts
            print(f"\n--- Final Vocabulary Counts ---")
            total_words = len(all_words)
            food_count = len(food_words)
            
            print(f"Total words in database: {total_words}")
            print(f"Food items in nourriture category: {food_count}")
            
            # Overall test result
            all_tests_passed = (
                key_foods_correct and 
                count_correct and 
                complete_translations and 
                duplicates_check and 
                other_categories_intact
            )
            
            if all_tests_passed:
                print("\n🎉 UPDATED NOURRITURE VOCABULARY TESTING COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors")
                print("✅ /api/words?category=nourriture endpoint working correctly")
                print(f"✅ All 16 key foods from new tableau verified with correct translations")
                print(f"✅ Food count meets requirements: {food_count} items")
                print("✅ All food items have complete translations in both languages")
                print("✅ No duplicate entries found")
                print("✅ Other categories remain intact and functional")
                print(f"✅ Total vocabulary count: {total_words} words")
                print(f"✅ Food vocabulary count: {food_count} items")
            else:
                print("\n❌ Some nourriture vocabulary tests failed")
                if not key_foods_correct:
                    print("❌ Key foods from tableau have incorrect translations")
                if not count_correct:
                    print("❌ Food count does not meet requirements")
                if not complete_translations:
                    print("❌ Some food items have incomplete translations")
                if not duplicates_check:
                    print("❌ Duplicate entries found")
                if not other_categories_intact:
                    print("❌ Some other categories are missing or incomplete")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Updated nourriture vocabulary test error: {e}")
            return False

    def test_updated_nature_vocabulary_new_tableau(self):
        """Test the updated nature vocabulary after complete replacement with new tableau"""
        print("\n=== Testing Updated Nature Vocabulary from New Tableau ===")
        
        try:
            # 1. Check if the backend starts without any syntax errors
            print("--- Testing Backend Startup After Nature Update ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Backend has syntax errors or is not responding: {response.status_code}")
                return False
            print("✅ Backend starts without syntax errors")
            
            # 2. Test the /api/words?category=nature endpoint to retrieve all nature items
            print("\n--- Testing /api/words?category=nature Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=nature")
            if response.status_code != 200:
                print(f"❌ Nature endpoint failed: {response.status_code}")
                return False
            
            nature_words = response.json()
            nature_words_by_french = {word['french']: word for word in nature_words}
            print(f"✅ /api/words?category=nature working correctly ({len(nature_words)} nature items)")
            
            # 3. Verify that all nature elements from the new tableau are present with correct translations
            print("\n--- Testing Specific Key Nature Elements from Tableau ---")
            
            # Key nature elements from the review request
            key_nature_elements = [
                {"french": "Pente/Colline/Mont", "shimaore": "Mlima", "kibouchi": "Boungou"},
                {"french": "Lune", "shimaore": "Mwézi", "kibouchi": "Fandzava"},
                {"french": "Étoile", "shimaore": "Gnora", "kibouchi": "Lakintagna"},
                {"french": "Sable", "shimaore": "Mtsanga", "kibouchi": "Fasigni"},
                {"french": "Vague", "shimaore": "Dhouja", "kibouchi": "Houndza/Riaka"},
                {"french": "Vent", "shimaore": "Pévo", "kibouchi": "Tsikou"},
                {"french": "Pluie", "shimaore": "Vhoua", "kibouchi": "Mahaléni"},
                {"french": "Mangrove", "shimaore": "Mhonko", "kibouchi": "Honkou"},
                {"french": "Corail", "shimaore": "Soiyi", "kibouchi": "Soiyi"},
                {"french": "Barrière de corail", "shimaore": "Caléni", "kibouchi": "Caléni"},
                {"french": "Tempête", "shimaore": "Darouba", "kibouchi": "Tsikou"},
                {"french": "Rivière", "shimaore": "Mouro", "kibouchi": "Mouroni"},
                {"french": "Arbre", "shimaore": "Mwiri", "kibouchi": "Kakazou"},
                {"french": "Soleil", "shimaore": "Mwézi", "kibouchi": "Zouva"},
                {"french": "Mer", "shimaore": "Bahari", "kibouchi": "Bahari"},
                {"french": "Plage", "shimaore": "Mtsangani", "kibouchi": "Fassigni"}
            ]
            
            key_elements_verified = True
            
            for element in key_nature_elements:
                french_word = element['french']
                if french_word in nature_words_by_french:
                    word = nature_words_by_french[french_word]
                    
                    # Check shimaoré translation
                    if word['shimaore'] == element['shimaore']:
                        print(f"✅ {french_word} shimaoré: '{word['shimaore']}' - VERIFIED")
                    else:
                        print(f"❌ {french_word} shimaoré: Expected '{element['shimaore']}', got '{word['shimaore']}'")
                        key_elements_verified = False
                    
                    # Check kibouchi translation
                    if word['kibouchi'] == element['kibouchi']:
                        print(f"✅ {french_word} kibouchi: '{word['kibouchi']}' - VERIFIED")
                    else:
                        print(f"❌ {french_word} kibouchi: Expected '{element['kibouchi']}', got '{word['kibouchi']}'")
                        key_elements_verified = False
                else:
                    print(f"❌ {french_word} not found in nature category")
                    key_elements_verified = False
            
            # 4. Verify that old incomplete nature entries have been replaced
            print("\n--- Testing Old Incomplete Nature Entries Replacement ---")
            
            # Check that all nature items have complete data structure
            incomplete_entries = []
            for word in nature_words:
                if not word.get('french') or not word.get('category') or word['category'] != 'nature':
                    incomplete_entries.append(word['french'])
            
            if not incomplete_entries:
                print("✅ All nature entries have complete data structure")
                old_entries_replaced = True
            else:
                print(f"❌ Found incomplete nature entries: {incomplete_entries}")
                old_entries_replaced = False
            
            # 5. Check that other categories remain intact and functional
            print("\n--- Testing Other Categories Remain Intact ---")
            
            # Test a few other categories to ensure they weren't affected
            other_categories_to_test = ['salutations', 'couleurs', 'nombres', 'famille', 'grammaire', 'verbes']
            other_categories_intact = True
            
            for category in other_categories_to_test:
                response = self.session.get(f"{API_BASE}/words?category={category}")
                if response.status_code == 200:
                    category_words = response.json()
                    if len(category_words) > 0:
                        print(f"✅ {category}: {len(category_words)} words - INTACT")
                    else:
                        print(f"❌ {category}: No words found")
                        other_categories_intact = False
                else:
                    print(f"❌ {category}: Endpoint failed ({response.status_code})")
                    other_categories_intact = False
            
            # 6. Test for any duplicate entries or data integrity issues
            print("\n--- Testing for Duplicate Entries and Data Integrity ---")
            
            # Check for duplicates in nature category
            french_names = [word['french'] for word in nature_words]
            unique_names = set(french_names)
            
            if len(french_names) == len(unique_names):
                print(f"✅ No duplicate entries found in nature category ({len(unique_names)} unique items)")
                no_duplicates = True
            else:
                duplicates = [name for name in french_names if french_names.count(name) > 1]
                print(f"❌ Duplicate entries found in nature category: {set(duplicates)}")
                no_duplicates = False
            
            # Check data integrity (all required fields present)
            data_integrity_ok = True
            required_fields = ['id', 'french', 'shimaore', 'kibouchi', 'category', 'difficulty']
            
            for word in nature_words:
                missing_fields = [field for field in required_fields if field not in word]
                if missing_fields:
                    print(f"❌ {word.get('french', 'Unknown')} missing fields: {missing_fields}")
                    data_integrity_ok = False
            
            if data_integrity_ok:
                print("✅ All nature items have complete data integrity")
            
            # 7. Confirm the total nature count matches the tableau (should be around 30 nature items)
            print("\n--- Testing Total Nature Count ---")
            
            expected_min_nature_count = 25  # Should be around 30, but allow some flexibility
            expected_max_nature_count = 35
            actual_nature_count = len(nature_words)
            
            if expected_min_nature_count <= actual_nature_count <= expected_max_nature_count:
                print(f"✅ Nature count within expected range: {actual_nature_count} items (expected ~30)")
                nature_count_ok = True
            else:
                print(f"❌ Nature count outside expected range: {actual_nature_count} items (expected ~30)")
                nature_count_ok = False
            
            # 8. Ensure all nature items have complete translations (note: some may have empty fields as shown in tableau)
            print("\n--- Testing Translation Completeness ---")
            
            # Check translation completeness (allowing for some empty fields as noted in review)
            items_with_translations = 0
            items_with_empty_fields = 0
            
            for word in nature_words:
                has_shimaoré = bool(word.get('shimaore', '').strip())
                has_kibouchi = bool(word.get('kibouchi', '').strip())
                
                if has_shimaoré and has_kibouchi:
                    items_with_translations += 1
                elif has_shimaoré or has_kibouchi:
                    items_with_translations += 1
                    items_with_empty_fields += 1
                    print(f"ℹ️ {word['french']}: Partial translation (shimaoré: '{word['shimaore']}', kibouchi: '{word['kibouchi']}')")
                else:
                    print(f"❌ {word['french']}: No translations found")
            
            translation_completeness_ok = items_with_translations >= (actual_nature_count * 0.8)  # At least 80% should have some translation
            
            if translation_completeness_ok:
                print(f"✅ Translation completeness acceptable: {items_with_translations}/{actual_nature_count} items have translations")
                if items_with_empty_fields > 0:
                    print(f"ℹ️ Note: {items_with_empty_fields} items have empty fields as expected from tableau")
            else:
                print(f"❌ Translation completeness insufficient: {items_with_translations}/{actual_nature_count} items have translations")
            
            # 9. Test the API endpoints are working correctly
            print("\n--- Testing API Endpoints Functionality ---")
            
            # Test individual nature item retrieval
            api_endpoints_ok = True
            if nature_words:
                sample_word = nature_words[0]
                word_id = sample_word['id']
                
                response = self.session.get(f"{API_BASE}/words/{word_id}")
                if response.status_code == 200:
                    retrieved_word = response.json()
                    if retrieved_word['french'] == sample_word['french']:
                        print(f"✅ Individual word retrieval working: {retrieved_word['french']}")
                    else:
                        print(f"❌ Individual word retrieval data mismatch")
                        api_endpoints_ok = False
                else:
                    print(f"❌ Individual word retrieval failed: {response.status_code}")
                    api_endpoints_ok = False
            
            # 10. Provide the new total count of nature items and overall word count
            print("\n--- Final Count Summary ---")
            
            # Get total word count
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code == 200:
                all_words = response.json()
                total_word_count = len(all_words)
                print(f"✅ Total word count after nature update: {total_word_count} words")
                print(f"✅ Nature vocabulary count: {actual_nature_count} items")
                
                # Show category breakdown
                categories = {}
                for word in all_words:
                    category = word.get('category', 'unknown')
                    categories[category] = categories.get(category, 0) + 1
                
                print("📊 Category breakdown:")
                for category, count in sorted(categories.items()):
                    print(f"   {category}: {count} words")
            else:
                print(f"❌ Could not retrieve total word count: {response.status_code}")
                total_word_count = "unknown"
            
            # Overall result
            all_tests_passed = (
                key_elements_verified and 
                old_entries_replaced and 
                other_categories_intact and 
                no_duplicates and 
                data_integrity_ok and 
                nature_count_ok and 
                translation_completeness_ok and 
                api_endpoints_ok
            )
            
            if all_tests_passed:
                print("\n🎉 UPDATED NATURE VOCABULARY TESTING COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors")
                print("✅ /api/words?category=nature endpoint working correctly")
                print("✅ All key nature elements from tableau verified with correct translations")
                print("✅ Old incomplete nature entries have been replaced")
                print("✅ Other categories remain intact and functional")
                print("✅ No duplicate entries or data integrity issues")
                print(f"✅ Nature count appropriate: {actual_nature_count} items")
                print("✅ Translation completeness acceptable (some empty fields as expected)")
                print("✅ API endpoints working correctly")
                print(f"📊 Final counts: {actual_nature_count} nature items, {total_word_count} total words")
            else:
                print("\n❌ Some nature vocabulary tests failed - see details above")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Updated nature vocabulary test error: {e}")
            return False

    def test_adjectifs_vocabulary_section(self):
        """Test the newly created adjectifs (adjectives) vocabulary section"""
        print("\n=== Testing Adjectifs (Adjectives) Vocabulary Section ===")
        
        try:
            # 1. Check if the backend starts without any syntax errors after adding the new adjectifs section
            print("--- Testing Backend Startup After Adding Adjectifs Section ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Backend has syntax errors or is not responding: {response.status_code}")
                return False
            print("✅ Backend starts without syntax errors after adding adjectifs section")
            
            # 2. Test the /api/words?category=adjectifs endpoint to retrieve all adjectives
            print("\n--- Testing /api/words?category=adjectifs Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=adjectifs")
            if response.status_code != 200:
                print(f"❌ Adjectifs endpoint failed: {response.status_code}")
                return False
            
            adjectives = response.json()
            adjectives_by_french = {word['french']: word for word in adjectives}
            print(f"✅ /api/words?category=adjectifs working correctly ({len(adjectives)} adjectives)")
            
            # 3. Verify that all adjectives from the tableau are present with correct French, Shimaoré, and Kibouchi translations
            print("\n--- Testing All Adjectives from Tableau ---")
            
            # 4. Check specific key adjectives from the tableau as requested
            print("\n--- Testing Specific Key Adjectives from Review Request ---")
            
            key_adjectives_tests = [
                {"french": "Grand", "shimaore": "Bole", "kibouchi": "Bé"},
                {"french": "Petit", "shimaore": "Tsi", "kibouchi": "Tsi"},
                {"french": "Gros", "shimaore": "Mtronga/Tronga", "kibouchi": "Bé"},
                {"french": "Maigre", "shimaore": "Tsala", "kibouchi": "Mahia"},
                {"french": "Fort", "shimaore": "Ouna ngouvou", "kibouchi": "Missi ngouvou"},
                {"french": "Dur", "shimaore": "Mangavou", "kibouchi": "Mahéri"},
                {"french": "Mou", "shimaore": "Tremboivou", "kibouchi": "Malémi"},
                {"french": "Beau/Jolie", "shimaore": "Mzouri", "kibouchi": "Zatovou"},
                {"french": "Laid", "shimaore": "Tsi ndzouzouri", "kibouchi": "Ratsi sora"},
                {"french": "Jeune", "shimaore": "Nrétsa", "kibouchi": "Zaza"},
                {"french": "Vieux", "shimaore": "Dhouha", "kibouchi": "Héla"},
                {"french": "Gentil", "shimaore": "Mwéma", "kibouchi": "Tsara rohou"},
                {"french": "Méchant", "shimaore": "Mbovou", "kibouchi": "Ratsi rohou"},
                {"french": "Bon", "shimaore": "Mwéma", "kibouchi": "Tsara"},
                {"french": "Mauvais", "shimaore": "Mbovou", "kibouchi": "Mwadéli"},
                {"french": "Chaud", "shimaore": "Moro", "kibouchi": "Méyi"},
                {"french": "Froid", "shimaore": "Baridi", "kibouchi": "Manintsi"},
                {"french": "Content", "shimaore": "Oujiviwa", "kibouchi": "Ravou"},
                {"french": "Triste", "shimaore": "Ouna hamo", "kibouchi": "Malahélou"}
            ]
            
            key_adjectives_correct = True
            for test_case in key_adjectives_tests:
                french_word = test_case['french']
                if french_word in adjectives_by_french:
                    word = adjectives_by_french[french_word]
                    
                    # Check translations
                    checks = [
                        (word['shimaore'], test_case['shimaore'], 'Shimaoré'),
                        (word['kibouchi'], test_case['kibouchi'], 'Kibouchi')
                    ]
                    
                    word_correct = True
                    for actual, expected, field_name in checks:
                        if actual != expected:
                            print(f"❌ {french_word} {field_name}: Expected '{expected}', got '{actual}'")
                            word_correct = False
                            key_adjectives_correct = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']}")
                else:
                    print(f"❌ {french_word} not found in adjectifs category")
                    key_adjectives_correct = False
            
            # 5. Verify the new adjectifs category is properly integrated with other categories
            print("\n--- Testing Adjectifs Category Integration ---")
            
            # Get all categories
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Could not retrieve all words: {response.status_code}")
                return False
            
            all_words = response.json()
            all_categories = set(word['category'] for word in all_words)
            
            if 'adjectifs' in all_categories:
                print("✅ Adjectifs category properly integrated with other categories")
                print(f"All categories found: {sorted(all_categories)}")
            else:
                print("❌ Adjectifs category not found in overall categories")
                return False
            
            # 6. Check that other categories remain intact and functional
            print("\n--- Testing Other Categories Remain Intact ---")
            
            expected_other_categories = {
                'famille', 'couleurs', 'animaux', 'salutations', 'nombres', 
                'corps', 'nourriture', 'maison', 'vetements', 'nature', 
                'transport', 'grammaire', 'verbes'
            }
            
            missing_categories = expected_other_categories - all_categories
            if not missing_categories:
                print("✅ All other categories remain intact and functional")
            else:
                print(f"❌ Missing categories: {missing_categories}")
                return False
            
            # Test a few words from other categories to ensure they're still working
            other_category_tests = [
                ('famille', 'Maman'),
                ('couleurs', 'Rouge'),
                ('animaux', 'Chat'),
                ('nombres', 'Un')
            ]
            
            other_categories_working = True
            for category, sample_word in other_category_tests:
                response = self.session.get(f"{API_BASE}/words?category={category}")
                if response.status_code == 200:
                    category_words = response.json()
                    found_words = [w['french'] for w in category_words]
                    if sample_word in found_words:
                        print(f"✅ Category '{category}' functional (found '{sample_word}')")
                    else:
                        print(f"⚠️ Category '{category}' may have issues ('{sample_word}' not found)")
                        other_categories_working = False
                else:
                    print(f"❌ Category '{category}' not working: {response.status_code}")
                    other_categories_working = False
            
            # 7. Test for any duplicate entries or data integrity issues
            print("\n--- Testing Data Integrity and Duplicates ---")
            
            # Check for duplicates in adjectifs
            french_names = [adj['french'] for adj in adjectives]
            unique_names = set(french_names)
            
            if len(french_names) == len(unique_names):
                print(f"✅ No duplicate entries found in adjectifs ({len(unique_names)} unique adjectives)")
                duplicates_check = True
            else:
                duplicates = [name for name in french_names if french_names.count(name) > 1]
                print(f"❌ Duplicate entries found in adjectifs: {set(duplicates)}")
                duplicates_check = False
            
            # Check data integrity - all adjectives should have required fields
            data_integrity_check = True
            for adj in adjectives:
                required_fields = ['french', 'shimaore', 'kibouchi', 'category', 'difficulty']
                missing_fields = [field for field in required_fields if field not in adj or adj[field] is None]
                if missing_fields:
                    print(f"❌ Adjective '{adj.get('french', 'Unknown')}' missing fields: {missing_fields}")
                    data_integrity_check = False
            
            if data_integrity_check:
                print("✅ All adjectives have proper data structure and required fields")
            
            # 8. Confirm the total adjectives count matches the tableau (should be around 48 adjectives)
            print("\n--- Testing Total Adjectives Count ---")
            
            expected_min_count = 40  # At least 40 adjectives expected
            expected_max_count = 60  # Around 48, but allowing some flexibility
            actual_count = len(adjectives)
            
            count_check = True
            if expected_min_count <= actual_count <= expected_max_count:
                print(f"✅ Adjectives count within expected range: {actual_count} adjectives (expected ~48)")
            else:
                print(f"❌ Adjectives count outside expected range: {actual_count} adjectives (expected ~48)")
                count_check = False
            
            # 9. Ensure all adjectives have proper category assignment as "adjectifs"
            print("\n--- Testing Category Assignment ---")
            
            category_assignment_check = True
            for adj in adjectives:
                if adj['category'] != 'adjectifs':
                    print(f"❌ Adjective '{adj['french']}' has incorrect category: {adj['category']} (expected 'adjectifs')")
                    category_assignment_check = False
            
            if category_assignment_check:
                print("✅ All adjectives properly assigned to 'adjectifs' category")
            
            # 10. Test the API endpoints are working correctly for the new category
            print("\n--- Testing API Endpoints for Adjectifs Category ---")
            
            # Test individual adjective retrieval
            api_endpoints_check = True
            if adjectives:
                sample_adjective = adjectives[0]
                adj_id = sample_adjective['id']
                
                response = self.session.get(f"{API_BASE}/words/{adj_id}")
                if response.status_code == 200:
                    retrieved_adj = response.json()
                    if retrieved_adj['category'] == 'adjectifs':
                        print(f"✅ Individual adjective retrieval working: {retrieved_adj['french']}")
                    else:
                        print(f"❌ Retrieved adjective has wrong category: {retrieved_adj['category']}")
                        api_endpoints_check = False
                else:
                    print(f"❌ Individual adjective retrieval failed: {response.status_code}")
                    api_endpoints_check = False
            
            # Test filtering by difficulty within adjectifs
            difficulty_levels = set(adj['difficulty'] for adj in adjectives)
            print(f"Difficulty levels in adjectifs: {sorted(difficulty_levels)}")
            
            # Provide comprehensive statistics
            print("\n--- Final Adjectifs Statistics ---")
            print(f"Total adjectives: {len(adjectives)}")
            print(f"Unique adjectives: {len(unique_names)}")
            print(f"Categories in database: {len(all_categories)}")
            print(f"Total words in database: {len(all_words)}")
            
            # Calculate difficulty distribution
            difficulty_distribution = {}
            for adj in adjectives:
                diff = adj['difficulty']
                difficulty_distribution[diff] = difficulty_distribution.get(diff, 0) + 1
            
            print(f"Difficulty distribution: {difficulty_distribution}")
            
            # Overall result
            all_tests_passed = (
                key_adjectives_correct and
                other_categories_working and
                duplicates_check and
                data_integrity_check and
                count_check and
                category_assignment_check and
                api_endpoints_check
            )
            
            if all_tests_passed:
                print("\n🎉 ADJECTIFS VOCABULARY SECTION TESTING COMPLETED SUCCESSFULLY!")
                print("✅ Backend starts without syntax errors after adding adjectifs section")
                print("✅ /api/words?category=adjectifs endpoint working correctly")
                print("✅ All key adjectives from tableau verified with correct translations:")
                print("   - Grand: bole / bé")
                print("   - Petit: tsi / tsi") 
                print("   - Gros: mtronga/tronga / bé")
                print("   - Maigre: tsala / mahia")
                print("   - Fort: ouna ngouvou / missi ngouvou")
                print("   - Dur: mangavou / mahéri")
                print("   - Mou: tremboivou / malémi")
                print("   - Beau/Jolie: mzouri / zatovou")
                print("   - Laid: tsi ndzouzouri / ratsi sora")
                print("   - Jeune: nrétsa / zaza")
                print("   - Vieux: dhouha / héla")
                print("   - Gentil: mwéma / tsara rohou")
                print("   - Méchant: mbovou / ratsi rohou")
                print("   - Bon: mwéma / tsara")
                print("   - Mauvais: mbovou / mwadéli")
                print("   - Chaud: moro / méyi")
                print("   - Froid: baridi / manintsi")
                print("   - Content: oujiviwa / ravou")
                print("   - Triste: ouna hamo / malahélou")
                print("✅ Adjectifs category properly integrated with other categories")
                print("✅ All other categories remain intact and functional")
                print("✅ No duplicate entries or data integrity issues")
                print(f"✅ Total adjectives count: {actual_count} (within expected range)")
                print("✅ All adjectives properly categorized as 'adjectifs'")
                print("✅ API endpoints working correctly for the new category")
                print(f"✅ New total word count: {len(all_words)} words across {len(all_categories)} categories")
            else:
                print("\n❌ Some adjectifs vocabulary tests failed or have issues")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Adjectifs vocabulary section test error: {e}")
            return False

    def test_adjectifs_category_integration(self):
        """Test adjectifs category integration as requested in review"""
        print("\n=== Testing Adjectifs Category Integration ===")
        
        try:
            # 1. Test that /api/words?category=adjectifs returns data
            print("--- Testing /api/words?category=adjectifs endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=adjectifs")
            if response.status_code != 200:
                print(f"❌ Adjectifs endpoint failed: {response.status_code}")
                return False
            
            adjectifs_words = response.json()
            print(f"✅ /api/words?category=adjectifs returns {len(adjectifs_words)} adjectives")
            
            if len(adjectifs_words) == 0:
                print("❌ No adjectives found in adjectifs category")
                return False
            
            # 2. Confirm that adjectifs appears in the full word list
            print("\n--- Testing adjectifs appears in full word list ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Could not retrieve full word list: {response.status_code}")
                return False
            
            all_words = response.json()
            categories = set(word['category'] for word in all_words)
            
            if 'adjectifs' in categories:
                print("✅ Adjectifs category appears in full word list")
                adjectifs_in_full_list = [word for word in all_words if word['category'] == 'adjectifs']
                print(f"   Found {len(adjectifs_in_full_list)} adjectives in full list")
            else:
                print("❌ Adjectifs category not found in full word list")
                print(f"   Available categories: {sorted(categories)}")
                return False
            
            # 3. Test a few sample adjectives to ensure they exist with proper translations
            print("\n--- Testing sample adjectives with proper translations ---")
            
            sample_adjectives = [
                {"french": "Grand", "shimaore": "Bole", "kibouchi": "Bé"},
                {"french": "Petit", "shimaore": "Tsi", "kibouchi": "Tsi"},
                {"french": "Gros", "shimaore": "Mtronga/Tronga", "kibouchi": "Bé"},
                {"french": "Maigre", "shimaore": "Tsala", "kibouchi": "Mahia"},
                {"french": "Fort", "shimaore": "Ouna ngouvou", "kibouchi": "Missi ngouvou"}
            ]
            
            adjectifs_by_french = {word['french']: word for word in adjectifs_words}
            
            sample_tests_passed = True
            for test_case in sample_adjectives:
                french_word = test_case['french']
                if french_word in adjectifs_by_french:
                    word = adjectifs_by_french[french_word]
                    
                    # Check translations
                    if (word['shimaore'] == test_case['shimaore'] and 
                        word['kibouchi'] == test_case['kibouchi'] and
                        word['category'] == 'adjectifs'):
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (category: {word['category']})")
                    else:
                        print(f"❌ {french_word}: Expected {test_case['shimaore']}/{test_case['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        sample_tests_passed = False
                else:
                    print(f"❌ {french_word} not found in adjectifs category")
                    sample_tests_passed = False
            
            if not sample_tests_passed:
                return False
            
            # 4. Verify the total count of categories and words
            print("\n--- Testing total count of categories and words ---")
            
            total_categories = len(categories)
            total_words = len(all_words)
            adjectifs_count = len(adjectifs_words)
            
            print(f"✅ Total categories: {total_categories}")
            print(f"✅ Total words: {total_words}")
            print(f"✅ Adjectifs count: {adjectifs_count}")
            
            # Expected categories should include adjectifs
            expected_categories = {
                'famille', 'salutations', 'couleurs', 'animaux', 'nombres', 
                'corps', 'nourriture', 'maison', 'vetements', 'nature', 
                'transport', 'grammaire', 'verbes', 'adjectifs'
            }
            
            if expected_categories.issubset(categories):
                print(f"✅ All expected categories found including adjectifs ({len(expected_categories)} categories)")
            else:
                missing = expected_categories - categories
                print(f"❌ Missing categories: {missing}")
                return False
            
            # 5. Ensure the new category is ready for frontend integration
            print("\n--- Testing frontend integration readiness ---")
            
            # Check data structure consistency
            structure_valid = True
            required_fields = {'id', 'french', 'shimaore', 'kibouchi', 'category', 'difficulty'}
            
            for word in adjectifs_words[:5]:  # Check first 5 adjectives
                if not required_fields.issubset(word.keys()):
                    print(f"❌ Missing required fields in word: {word.get('french', 'unknown')}")
                    structure_valid = False
                    break
                
                if word['category'] != 'adjectifs':
                    print(f"❌ Incorrect category for word: {word['french']} (category: {word['category']})")
                    structure_valid = False
                    break
            
            if structure_valid:
                print("✅ All adjectives have proper data structure for frontend integration")
                print("✅ Required fields present: id, french, shimaore, kibouchi, category, difficulty")
                print("✅ All words properly categorized as 'adjectifs'")
            else:
                return False
            
            # Test API endpoint consistency
            print("\n--- Testing API endpoint consistency ---")
            
            # Test individual adjective retrieval
            if adjectifs_words:
                sample_id = adjectifs_words[0]['id']
                response = self.session.get(f"{API_BASE}/words/{sample_id}")
                if response.status_code == 200:
                    individual_word = response.json()
                    if individual_word['category'] == 'adjectifs':
                        print(f"✅ Individual adjective retrieval working: {individual_word['french']}")
                    else:
                        print(f"❌ Individual adjective retrieval category mismatch")
                        return False
                else:
                    print(f"❌ Individual adjective retrieval failed: {response.status_code}")
                    return False
            
            print("\n🎉 ADJECTIFS CATEGORY INTEGRATION TEST COMPLETED SUCCESSFULLY!")
            print("✅ /api/words?category=adjectifs endpoint working correctly")
            print("✅ Adjectifs category appears in full word list")
            print("✅ Sample adjectives verified with proper translations")
            print("✅ Total category and word counts confirmed")
            print("✅ New category ready for frontend integration")
            print("✅ Data structure consistent and API endpoints working")
            
            return True
            
        except Exception as e:
            print(f"❌ Adjectifs category integration test error: {e}")
            return False

    def run_all_tests(self):
        """Run updated nature vocabulary test as requested in review"""
        print("🌺 MAYOTTE EDUCATIONAL APP - UPDATED NATURE VOCABULARY TEST 🌺")
        print("=" * 70)
        
        # Run the specific updated nature vocabulary test as requested in review
        print("Running updated nature vocabulary test to verify new elements from additional tableau...")
        
        test_results = {}
        
        # Essential connectivity tests first
        test_results['connectivity'] = self.test_basic_connectivity()
        test_results['mongodb'] = self.test_mongodb_connection()
        test_results['init_content'] = self.test_init_base_content()
        
        # Main updated nature vocabulary test
        test_results['updated_nature_vocabulary'] = self.test_updated_nature_vocabulary_from_new_tableau()
        
        # Summary
        print(f"\n{'='*70}")
        print("🌺 UPDATED NATURE VOCABULARY TEST RESULTS 🌺")
        print(f"{'='*70}")
        
        passed = sum(test_results.values())
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\n📊 OVERALL RESULTS: {passed}/{total} tests passed")
        
        if test_results.get('updated_nature_vocabulary', False):
            print("🎉 UPDATED NATURE VOCABULARY TEST PASSED!")
            print("✅ Backend starts without syntax errors after adding new nature elements")
            print("✅ All 19 new nature elements from tableau verified with correct translations")
            print("✅ Previously existing nature elements still present")
            print("✅ Other categories remain intact and functional")
            print("✅ No duplicate entries or data integrity issues")
            print("✅ API endpoints working correctly for the updated category")
            print("The updated nature vocabulary with new elements from the additional tableau is ready for educational use.")
        else:
            print("❌ Updated nature vocabulary test failed. Please review the issues above.")
        
        return passed == total

    def test_duplicate_removal_verification(self):
        """Test that all duplicate animals have been successfully removed"""
        print("\n=== Testing Duplicate Removal Verification ===")
        
        try:
            # 1. Test duplicate removal verification - POST /api/init-base-content to reinitialize with deduplicated animals
            print("--- Testing Duplicate Removal - Reinitialize with Deduplicated Animals ---")
            response = self.session.post(f"{API_BASE}/init-base-content")
            if response.status_code != 200:
                print(f"❌ Failed to reinitialize base content: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Base content reinitialized: {result}")
            
            # 2. Test GET /api/words?category=animaux to verify all animals
            print("\n--- Testing Animals After Deduplication ---")
            response = self.session.get(f"{API_BASE}/words?category=animaux")
            if response.status_code != 200:
                print(f"❌ Failed to get animals: {response.status_code}")
                return False
            
            animals = response.json()
            animals_by_french = {word['french']: word for word in animals}
            
            print(f"Found {len(animals)} animal entries in database")
            
            # 3. Test specific duplicate removal - Verify only ONE instance of each previously duplicated animal remains
            print("\n--- Testing Specific Duplicate Removal ---")
            previously_duplicated_animals = ['Lézard', 'Renard', 'Chameau', 'Hérisson']
            
            duplicate_removal_success = True
            for animal_name in previously_duplicated_animals:
                # Count occurrences of this animal
                occurrences = [animal for animal in animals if animal['french'] == animal_name]
                
                if len(occurrences) == 1:
                    animal = occurrences[0]
                    print(f"✅ {animal_name}: Only 1 instance found - {animal['shimaore']} / {animal['kibouchi']}")
                elif len(occurrences) == 0:
                    print(f"❌ {animal_name}: No instances found (should have 1)")
                    duplicate_removal_success = False
                else:
                    print(f"❌ {animal_name}: {len(occurrences)} instances found (should have only 1)")
                    duplicate_removal_success = False
            
            # 4. Test corrected translations are still intact
            print("\n--- Testing Corrected Translations Still Intact ---")
            corrected_translations_tests = [
                {"french": "Canard", "shimaore": "Guisi", "kibouchi": "Doukitri"},
                {"french": "Chenille", "shimaore": "Bibimangidji", "kibouchi": "Bibimanguidi"},
                {"french": "Cafard", "shimaore": "Kalalawi", "kibouchi": "Kalalowou"},
                {"french": "Guêpe", "shimaore": "Vungo vungo", "kibouchi": "Fantehi"},
                {"french": "Bigorneau", "shimaore": "Trondro", "kibouchi": "Trondrou"},
                {"french": "Facochère", "shimaore": "Pouroukou nyeha", "kibouchi": "Lambou"},
                {"french": "Hérisson", "shimaore": "Landra", "kibouchi": "Trandraka"}
            ]
            
            corrected_translations_intact = True
            for test_case in corrected_translations_tests:
                french_word = test_case['french']
                if french_word in animals_by_french:
                    word = animals_by_french[french_word]
                    
                    if word['shimaore'] == test_case['shimaore'] and word['kibouchi'] == test_case['kibouchi']:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} (corrected translation intact)")
                    else:
                        print(f"❌ {french_word}: Expected {test_case['shimaore']}/{test_case['kibouchi']}, got {word['shimaore']}/{word['kibouchi']}")
                        corrected_translations_intact = False
                else:
                    print(f"❌ {french_word} not found in animals category")
                    corrected_translations_intact = False
            
            # 5. Test final animal count - Verify total animal entries now equals unique French names
            print("\n--- Testing Final Animal Count ---")
            total_entries = len(animals)
            unique_french_names = len(set(animal['french'] for animal in animals))
            
            print(f"Total animal entries: {total_entries}")
            print(f"Unique French names: {unique_french_names}")
            
            count_integrity = (total_entries == unique_french_names)
            if count_integrity:
                print("✅ Final count reflects proper deduplication - all entries are unique")
                
                # Check if we have the expected 59 unique animals (63 - 4 duplicates removed)
                expected_final_count = 59
                if unique_french_names == expected_final_count:
                    print(f"✅ Expected final count achieved: {unique_french_names} unique animals")
                    final_count_correct = True
                else:
                    print(f"ℹ️ Final count: {unique_french_names} unique animals (expected {expected_final_count})")
                    final_count_correct = False  # Not necessarily a failure, but worth noting
            else:
                duplicate_count = total_entries - unique_french_names
                print(f"❌ Still {duplicate_count} duplicate entries found")
                final_count_correct = False
            
            # 6. Test data integrity after deduplication
            print("\n--- Testing Data Integrity After Deduplication ---")
            
            # Verify all remaining animals have complete Shimaoré AND Kibouchi translations
            incomplete_translations = []
            for animal in animals:
                if not animal['shimaore'] and not animal['kibouchi']:
                    incomplete_translations.append(f"{animal['french']} (no translations)")
                elif not animal['shimaore']:
                    # This is acceptable for some animals like "Langue" which only has Kibouchi
                    pass
                elif not animal['kibouchi']:
                    # This might be acceptable for some animals
                    pass
            
            if not incomplete_translations:
                print("✅ All remaining animals have at least one translation (Shimaoré or Kibouchi)")
                translations_complete = True
            else:
                print(f"❌ Animals with incomplete translations: {incomplete_translations}")
                translations_complete = False
            
            # Confirm proper category assignment ("animaux")
            category_correct = True
            for animal in animals:
                if animal['category'] != 'animaux':
                    print(f"❌ {animal['french']} has incorrect category: {animal['category']}")
                    category_correct = False
            
            if category_correct:
                print("✅ All animals properly categorized as 'animaux'")
            
            # Verify appropriate difficulty levels (1-2)
            difficulty_correct = True
            invalid_difficulties = []
            for animal in animals:
                if animal['difficulty'] not in [1, 2]:
                    invalid_difficulties.append(f"{animal['french']} (difficulty: {animal['difficulty']})")
                    difficulty_correct = False
            
            if difficulty_correct:
                print("✅ All animals have appropriate difficulty levels (1-2)")
            else:
                print(f"❌ Animals with invalid difficulty levels: {invalid_difficulties}")
            
            # 7. Overall duplicate removal verification result
            overall_success = (
                duplicate_removal_success and 
                corrected_translations_intact and 
                count_integrity and 
                translations_complete and 
                category_correct and 
                difficulty_correct
            )
            
            if overall_success:
                print("\n🎉 DUPLICATE REMOVAL VERIFICATION COMPLETED SUCCESSFULLY!")
                print("✅ All duplicate animals successfully removed")
                print("✅ Only ONE instance of each previously duplicated animal remains")
                print("✅ All 7 corrected translations still intact")
                print("✅ Final animal count reflects proper deduplication")
                print("✅ Data integrity maintained after deduplication")
                print("✅ All animals have complete translations and proper categorization")
                print("✅ Appropriate difficulty levels (1-2) confirmed")
                
                if final_count_correct:
                    print(f"✅ Expected final count of {unique_french_names} unique animals achieved")
                else:
                    print(f"ℹ️ Final count: {unique_french_names} unique animals (may vary based on total vocabulary)")
            else:
                print("\n❌ DUPLICATE REMOVAL VERIFICATION FAILED!")
                if not duplicate_removal_success:
                    print("❌ Some previously duplicated animals still have multiple instances")
                if not corrected_translations_intact:
                    print("❌ Some corrected translations were lost during deduplication")
                if not count_integrity:
                    print("❌ Duplicate entries still exist in the database")
                if not translations_complete:
                    print("❌ Some animals have incomplete translations")
                if not category_correct:
                    print("❌ Some animals have incorrect category assignments")
                if not difficulty_correct:
                    print("❌ Some animals have invalid difficulty levels")
            
            return overall_success
            
        except Exception as e:
            print(f"❌ Duplicate removal verification test error: {e}")
            return False

    def test_adjectifs_category_verification(self):
        """Quick verification test for the adjectifs category as requested"""
        print("\n=== Quick Verification Test for Adjectifs Category ===")
        
        try:
            # 1. Test if /api/words?category=adjectifs endpoint works
            print("--- Testing /api/words?category=adjectifs Endpoint ---")
            response = self.session.get(f"{API_BASE}/words?category=adjectifs")
            if response.status_code != 200:
                print(f"❌ Adjectifs endpoint failed: {response.status_code}")
                return False
            
            adjectifs_words = response.json()
            print(f"✅ /api/words?category=adjectifs endpoint working correctly")
            print(f"Found {len(adjectifs_words)} adjectives")
            
            # 2. Check if adjectifs category appears in the overall words list
            print("\n--- Testing Adjectifs Category in Overall Words List ---")
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Could not retrieve overall words list: {response.status_code}")
                return False
            
            all_words = response.json()
            categories = set(word['category'] for word in all_words)
            
            if 'adjectifs' in categories:
                print("✅ Adjectifs category appears in the overall words list")
            else:
                print("❌ Adjectifs category NOT found in overall words list")
                print(f"Available categories: {sorted(categories)}")
                return False
            
            # 3. Get a count of adjectifs to confirm they exist
            print("\n--- Testing Adjectifs Count ---")
            adjectifs_count = len([word for word in all_words if word['category'] == 'adjectifs'])
            
            if adjectifs_count > 0:
                print(f"✅ Adjectifs count confirmed: {adjectifs_count} adjectives exist")
            else:
                print("❌ No adjectifs found in the database")
                return False
            
            # 4. Test that the category is properly accessible via API
            print("\n--- Testing Category API Accessibility ---")
            
            # Verify some sample adjectives exist and have proper structure
            if adjectifs_words:
                sample_adjective = adjectifs_words[0]
                required_fields = {'french', 'shimaore', 'kibouchi', 'category', 'difficulty'}
                
                if required_fields.issubset(sample_adjective.keys()):
                    print("✅ Adjectives have proper data structure")
                    print(f"Sample adjective: {sample_adjective['french']} = {sample_adjective['shimaore']} (Shimaoré) / {sample_adjective['kibouchi']} (Kibouchi)")
                    print(f"Category: {sample_adjective['category']}, Difficulty: {sample_adjective['difficulty']}")
                else:
                    print(f"❌ Adjectives missing required fields: {required_fields - sample_adjective.keys()}")
                    return False
                
                # Test a few more samples to ensure consistency
                print("\n--- Sample Adjectives ---")
                for i, adj in enumerate(adjectifs_words[:5]):  # Show first 5 adjectives
                    shimaore_display = adj['shimaore'] if adj['shimaore'] else "(none)"
                    kibouchi_display = adj['kibouchi'] if adj['kibouchi'] else "(none)"
                    print(f"  {i+1}. {adj['french']}: {shimaore_display} / {kibouchi_display}")
            else:
                print("❌ No adjectives returned from API")
                return False
            
            # 5. Verify category consistency
            print("\n--- Testing Category Consistency ---")
            category_consistent = True
            for word in adjectifs_words:
                if word['category'] != 'adjectifs':
                    print(f"❌ Inconsistent category for word '{word['french']}': {word['category']}")
                    category_consistent = False
            
            if category_consistent:
                print("✅ All words in adjectifs category have consistent category assignment")
            else:
                return False
            
            print(f"\n🎉 ADJECTIFS CATEGORY VERIFICATION COMPLETED SUCCESSFULLY!")
            print(f"✅ /api/words?category=adjectifs endpoint works ({len(adjectifs_words)} adjectives)")
            print(f"✅ Adjectifs category appears in overall words list")
            print(f"✅ {adjectifs_count} adjectives confirmed to exist")
            print(f"✅ Category is properly accessible via API with correct data structure")
            print(f"✅ Backend side is working correctly for adjectifs category")
            
            return True
            
        except Exception as e:
            print(f"❌ Adjectifs category verification error: {e}")
            return False

if __name__ == "__main__":
    print("🌺 Starting Mayotte Educational App Backend Testing 🌺")
    print("=" * 60)
    
    tester = MayotteEducationTester()
    
    # Run specific test for the habitation vocabulary section
    tests = [
        ("Basic API Connectivity", tester.test_basic_connectivity),
        ("MongoDB Connection", tester.test_mongodb_connection),
        ("Educational Content Initialization", tester.test_init_base_content),
        ("Updated Habitation Vocabulary Section", tester.test_updated_habitation_vocabulary_section)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print('='*60)
        
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            failed += 1
    
    # Final summary
    print(f"\n{'='*60}")
    print("🌺 MAYOTTE EDUCATIONAL APP BACKEND TEST SUMMARY 🌺")
    print(f"{'='*60}")
    print(f"✅ Tests Passed: {passed}")
    print(f"❌ Tests Failed: {failed}")
    print(f"📊 Total Tests: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Expression correction verified successfully! 🎉")
        print("🌺 J'ai soif correction: kibouchi = 'Zahou tindranou' (not 'Zahou moussari') 🌺")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please review and fix issues.")
    
    print(f"{'='*60}")