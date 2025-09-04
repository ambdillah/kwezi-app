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
                
                # Complex numbers
                {"french": "Onze", "shimaore": "Komi na moja", "kibouchi": "Foulou Areki Ambi", "category": "nombres"},
                {"french": "Douze", "shimaore": "Komi na mbili", "kibouchi": "Foulou Areki Rou", "category": "nombres"},
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
    
    def run_all_tests(self):
        """Run all tests and return summary"""
        print("🏫 Starting Mayotte Educational App Backend Tests - Final Updated Vocabulary")
        print("=" * 80)
        
        test_results = {}
        
        # Run all tests including new vocabulary verification tests
        test_results['connectivity'] = self.test_basic_connectivity()
        test_results['mongodb'] = self.test_mongodb_connection()
        test_results['init_content'] = self.test_init_base_content()
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
        print("🏫 MAYOTTE EDUCATIONAL APP TEST SUMMARY - FINAL UPDATED VOCABULARY")
        print("=" * 80)
        
        passed = sum(test_results.values())
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All backend tests passed! The final updated Mayotte vocabulary is working correctly.")
            print("✅ Comprehensive vocabulary with authentic Shimaoré and Kibouchi translations")
            print("✅ Updated greetings, pronouns, family terms, colors, food, house, nature, and verbs")
            print("✅ All 13 categories properly implemented including grammaire and verbes")
        else:
            print("⚠️ Some tests failed. Please check the detailed output above.")
        
        return test_results

if __name__ == "__main__":
    tester = MayotteEducationTester()
    results = tester.run_all_tests()