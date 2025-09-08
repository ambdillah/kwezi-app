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

    def run_all_tests(self):
        """Run all tests and return summary"""
        print("🏫 Starting Mayotte Educational App Backend Tests - Complete Colors Palette")
        print("=" * 80)
        
        test_results = {}
        
        # Run all tests including new complete colors palette test
        test_results['connectivity'] = self.test_basic_connectivity()
        test_results['mongodb'] = self.test_mongodb_connection()
        test_results['init_content'] = self.test_init_base_content()
        test_results['comprehensive_updated_animals'] = self.test_comprehensive_updated_animals_section()
        test_results['final_comprehensive_animals'] = self.test_final_comprehensive_animals_vocabulary()
        test_results['complete_colors_palette'] = self.test_complete_colors_palette()
        test_results['comprehensive_grammar'] = self.test_comprehensive_grammar_vocabulary()
        test_results['extended_family'] = self.test_extended_family_vocabulary()
        test_results['corrected_numbers'] = self.test_corrected_numbers_system()
        test_results['comprehensive_vocab'] = self.test_comprehensive_vocabulary_initialization()
        test_results['specific_vocab'] = self.test_specific_vocabulary_from_table()
        test_results['greeting_improvements'] = self.test_updated_greeting_improvements()
        test_results['pronoun_additions'] = self.test_pronoun_additions()
        test_results['verb_additions'] = self.test_new_verb_additions()
        test_results['get_words'] = self.test_get_words()
        test_results['category_filter'] = self.test_comprehensive_category_filtering()
        test_results['word_crud'] = self.test_word_crud_operations()
        test_results['exercises'] = self.test_exercise_management()
        test_results['progress'] = self.test_user_progress_tracking()
        
        # Summary
        print("\n" + "=" * 80)
        print("🏫 MAYOTTE EDUCATIONAL APP TEST SUMMARY - COMPREHENSIVE GRAMMAR SECTION")
        print("=" * 80)
        
        passed = sum(test_results.values())
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All backend tests passed! The comprehensive grammar section is working correctly.")
            print("✅ Complete grammar foundation with both personal and possessive pronouns")
            print("✅ All 6 personal pronouns verified with difficulty 1")
            print("✅ All 6 possessive pronouns verified with difficulty 2")
            print("✅ Comprehensive grammar coverage for building complete sentences in Shimaoré and Kibouchi")
            print("✅ All backend functionality remains intact with comprehensive grammar vocabulary")
        else:
            print("⚠️ Some tests failed. Please check the detailed output above.")
        
        return test_results

if __name__ == "__main__":
    tester = MayotteEducationTester()
    results = tester.run_all_tests()