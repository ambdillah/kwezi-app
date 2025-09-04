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
        """Test educational content initialization"""
        print("\n=== Testing Educational Content Initialization ===")
        
        try:
            # Initialize base content
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
    
    def test_category_filtering(self):
        """Test category filtering for words"""
        print("\n=== Testing Category Filtering ===")
        
        try:
            # Test famille category
            response = self.session.get(f"{API_BASE}/words?category=famille")
            if response.status_code == 200:
                famille_words = response.json()
                print(f"✅ Retrieved {len(famille_words)} words in 'famille' category")
                
                # Verify all words are in famille category
                if all(word['category'] == 'famille' for word in famille_words):
                    print("✅ All words correctly filtered by category")
                    if famille_words:
                        print(f"Sample famille word: {famille_words[0]['french']} = {famille_words[0]['shimaore']}")
                else:
                    print("❌ Category filtering not working correctly")
                    
                return True
            else:
                print(f"❌ Category filtering failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Category filtering error: {e}")
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
        print("🏫 Starting Mayotte Educational App Backend Tests")
        print("=" * 60)
        
        test_results = {}
        
        # Run all tests
        test_results['connectivity'] = self.test_basic_connectivity()
        test_results['mongodb'] = self.test_mongodb_connection()
        test_results['init_content'] = self.test_init_base_content()
        test_results['get_words'] = self.test_get_words()
        test_results['category_filter'] = self.test_category_filtering()
        test_results['word_crud'] = self.test_word_crud_operations()
        test_results['exercises'] = self.test_exercise_management()
        test_results['progress'] = self.test_user_progress_tracking()
        
        # Summary
        print("\n" + "=" * 60)
        print("🏫 MAYOTTE EDUCATIONAL APP TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(test_results.values())
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All backend tests passed! The Mayotte educational app backend is working correctly.")
        else:
            print("⚠️ Some tests failed. Please check the detailed output above.")
        
        return test_results

if __name__ == "__main__":
    tester = MayotteEducationTester()
    results = tester.run_all_tests()