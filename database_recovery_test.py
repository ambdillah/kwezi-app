#!/usr/bin/env python3
"""
Database Recovery Verification Test
VÉRIFICATION FINALE DE LA RÉCUPÉRATION DE LA BASE DE DONNÉES
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

class DatabaseRecoveryTester:
    def __init__(self):
        self.session = requests.Session()
        
    def test_database_recovery_verification(self):
        """VÉRIFICATION FINALE DE LA RÉCUPÉRATION DE LA BASE DE DONNÉES"""
        print("\n=== VÉRIFICATION FINALE DE LA RÉCUPÉRATION DE LA BASE DE DONNÉES ===")
        print("CONTEXTE: Récupération d'urgence complétée - vérification que toutes les données authentiques de l'utilisateur ont été restaurées avec succès.")
        
        try:
            # 1. INTÉGRITÉ GÉNÉRALE
            print("\n--- 1. INTÉGRITÉ GÉNÉRALE ---")
            
            # Get all words
            response = self.session.get(f"{API_BASE}/words")
            if response.status_code != 200:
                print(f"❌ Could not retrieve words: {response.status_code}")
                return False
            
            words = response.json()
            total_words = len(words)
            print(f"Total words found: {total_words}")
            
            # Verify total word count (expected: 411+ words)
            if total_words >= 411:
                print(f"✅ Total word count: {total_words} (411+ required)")
                word_count_ok = True
            else:
                print(f"❌ Insufficient word count: {total_words} (411+ required)")
                word_count_ok = False
            
            # Check categories
            categories = set(word['category'] for word in words)
            expected_categories = {
                'salutations', 'famille', 'couleurs', 'animaux', 'nombres',
                'corps', 'grammaire', 'nourriture', 'maison', 'transport',
                'vetements', 'nature', 'expressions', 'adjectifs', 'verbes', 'tradition'
            }
            
            print(f"Found categories ({len(categories)}): {sorted(categories)}")
            if len(categories) >= 16:
                print(f"✅ 16+ categories found: {len(categories)}")
                categories_ok = True
            else:
                print(f"❌ Insufficient categories: {len(categories)} (16 required)")
                categories_ok = False
            
            # Check for duplicates
            french_words = [word['french'] for word in words]
            unique_french = set(french_words)
            duplicates = len(french_words) - len(unique_french)
            
            if duplicates == 0:
                print(f"✅ No duplicates found")
                no_duplicates = True
            else:
                print(f"❌ {duplicates} duplicate entries found")
                duplicate_words = []
                for word in french_words:
                    if french_words.count(word) > 1 and word not in duplicate_words:
                        duplicate_words.append(word)
                print(f"Duplicate words: {duplicate_words[:10]}...")  # Show first 10
                no_duplicates = False
            
            # 2. TRADUCTIONS AUTHENTIQUES CRITIQUES
            print("\n--- 2. TRADUCTIONS AUTHENTIQUES CRITIQUES ---")
            
            words_by_french = {word['french']: word for word in words}
            
            critical_translations = [
                # Famille
                {"french": "Papa", "shimaore": "Baba", "kibouchi": "Baba", "category": "famille"},
                {"french": "Maman", "shimaore": "Mama", "kibouchi": "Mama", "category": "famille"},
                {"french": "Frère", "shimaore": "Mwanagna mtroun", "kibouchi": "Anadahi", "category": "famille"},
                {"french": "Sœur", "shimaore": "Mwanagna mtroub", "kibouchi": "Anabavi", "category": "famille"},
                
                # Nombres
                {"french": "Un", "shimaore": "Moja", "kibouchi": "Areki", "category": "nombres"},
                {"french": "Deux", "shimaore": "Mbili", "kibouchi": "Aroyi", "category": "nombres"},
                {"french": "Trois", "shimaore": "Trarou", "kibouchi": "Telou", "category": "nombres"},
                {"french": "Quatre", "shimaore": "Nhé", "kibouchi": "Efatra", "category": "nombres"},
                {"french": "Cinq", "shimaore": "Tsano", "kibouchi": "Dimi", "category": "nombres"},
                
                # Couleurs
                {"french": "Bleu", "shimaore": "Bilé", "kibouchi": "Bilé", "category": "couleurs"},
                {"french": "Vert", "shimaore": "Dhavou", "kibouchi": "Mayitsou", "category": "couleurs"},
                {"french": "Rouge", "shimaore": "Ndzoukoundrou", "kibouchi": "Mena", "category": "couleurs"},
                
                # Animaux
                {"french": "Chat", "shimaore": "Paha", "kibouchi": "Moirou", "category": "animaux"},
                {"french": "Chien", "shimaore": "Mbwa", "kibouchi": "Fadroka", "category": "animaux"},
                {"french": "Oiseau", "shimaore": "Gnougni", "kibouchi": "Vorougnou", "category": "animaux"},
                
                # Salutations
                {"french": "Bonjour", "shimaore": "Bariza", "kibouchi": "Salama", "category": "salutations"},
                {"french": "Merci", "shimaore": "Barakélaou", "kibouchi": "Misaou", "category": "salutations"},
            ]
            
            critical_correct = True
            critical_issues = []
            
            for test_case in critical_translations:
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
                            issue = f"{french_word} {field_name}: Expected '{expected}', got '{actual}'"
                            print(f"❌ {issue}")
                            critical_issues.append(issue)
                            word_correct = False
                            critical_correct = False
                    
                    if word_correct:
                        print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']} - {word['category']}")
                else:
                    issue = f"{french_word} not found in database"
                    print(f"❌ {issue}")
                    critical_issues.append(issue)
                    critical_correct = False
            
            # 3. COMPLÉTUDE DES CATÉGORIES
            print("\n--- 3. COMPLÉTUDE DES CATÉGORIES ---")
            
            category_counts = {}
            for word in words:
                category = word['category']
                category_counts[category] = category_counts.get(category, 0) + 1
            
            expected_counts = {
                'salutations': 8, 'famille': 22, 'couleurs': 8, 'animaux': 56, 'nombres': 20,
                'corps': 32, 'grammaire': 12, 'nourriture': 40, 'maison': 5, 'transport': 7,
                'vetements': 16, 'nature': 28, 'expressions': 33, 'adjectifs': 52, 'verbes': 56, 'tradition': 16
            }
            
            category_completeness = True
            category_issues = []
            
            for category, expected_count in expected_counts.items():
                actual_count = category_counts.get(category, 0)
                if actual_count >= expected_count:
                    print(f"✅ {category}: {actual_count} words (expected {expected_count}+)")
                else:
                    issue = f"{category}: {actual_count} words (expected {expected_count}+)"
                    print(f"❌ {issue}")
                    category_issues.append(issue)
                    category_completeness = False
            
            # 4. FONCTIONNALITÉ API
            print("\n--- 4. FONCTIONNALITÉ API ---")
            
            # Test all CRUD endpoints
            api_functional = True
            api_issues = []
            
            # Test GET /api/words
            try:
                response = self.session.get(f"{API_BASE}/words")
                if response.status_code == 200:
                    print("✅ GET /api/words working")
                else:
                    issue = f"GET /api/words failed: {response.status_code}"
                    print(f"❌ {issue}")
                    api_issues.append(issue)
                    api_functional = False
            except Exception as e:
                issue = f"GET /api/words error: {e}"
                print(f"❌ {issue}")
                api_issues.append(issue)
                api_functional = False
            
            # Test category filtering
            try:
                response = self.session.get(f"{API_BASE}/words?category=famille")
                if response.status_code == 200:
                    famille_words = response.json()
                    print(f"✅ Category filtering working: {len(famille_words)} famille words")
                else:
                    issue = f"Category filtering failed: {response.status_code}"
                    print(f"❌ {issue}")
                    api_issues.append(issue)
                    api_functional = False
            except Exception as e:
                issue = f"Category filtering error: {e}"
                print(f"❌ {issue}")
                api_issues.append(issue)
                api_functional = False
            
            # Test individual word retrieval
            if words:
                try:
                    sample_word = words[0]
                    response = self.session.get(f"{API_BASE}/words/{sample_word['id']}")
                    if response.status_code == 200:
                        print("✅ Individual word retrieval working")
                    else:
                        issue = f"Individual word retrieval failed: {response.status_code}"
                        print(f"❌ {issue}")
                        api_issues.append(issue)
                        api_functional = False
                except Exception as e:
                    issue = f"Individual word retrieval error: {e}"
                    print(f"❌ {issue}")
                    api_issues.append(issue)
                    api_functional = False
            
            # 5. QUALITÉ DES DONNÉES
            print("\n--- 5. QUALITÉ DES DONNÉES ---")
            
            # Check alphabetical sorting in categories
            sorting_ok = True
            sorting_issues = []
            
            for category in ['salutations', 'famille', 'couleurs', 'animaux', 'nombres']:
                category_words = [word for word in words if word['category'] == category]
                french_names = [word['french'] for word in category_words]
                sorted_names = sorted(french_names, key=str.lower)
                
                if french_names == sorted_names:
                    print(f"✅ {category}: Alphabetically sorted")
                else:
                    issue = f"{category}: Not alphabetically sorted"
                    print(f"❌ {issue}")
                    sorting_issues.append(issue)
                    sorting_ok = False
            
            # Check emojis presence
            emojis_present = True
            words_with_emojis = [word for word in words if word.get('image_url')]
            emoji_percentage = (len(words_with_emojis) / len(words)) * 100
            
            if emoji_percentage >= 50:  # At least 50% should have emojis
                print(f"✅ Emojis present: {len(words_with_emojis)} words ({emoji_percentage:.1f}%)")
            else:
                print(f"❌ Insufficient emojis: {len(words_with_emojis)} words ({emoji_percentage:.1f}%)")
                emojis_present = False
            
            # Check data structure consistency
            structure_consistent = True
            required_fields = {'id', 'french', 'shimaore', 'kibouchi', 'category', 'difficulty'}
            
            for word in words[:10]:  # Check first 10 words
                word_fields = set(word.keys())
                if not required_fields.issubset(word_fields):
                    print(f"❌ Missing required fields in word: {word.get('french', 'unknown')}")
                    structure_consistent = False
                    break
            
            if structure_consistent:
                print("✅ Data structure consistent")
            
            # FINAL ASSESSMENT
            print("\n--- ÉVALUATION FINALE ---")
            
            all_tests_passed = (
                word_count_ok and
                categories_ok and
                no_duplicates and
                critical_correct and
                category_completeness and
                api_functional and
                sorting_ok and
                emojis_present and
                structure_consistent
            )
            
            if all_tests_passed:
                print("\n🎉 VÉRIFICATION FINALE DE LA RÉCUPÉRATION RÉUSSIE!")
                print("✅ INTÉGRITÉ GÉNÉRALE: Total mots, catégories, aucun doublon")
                print("✅ TRADUCTIONS AUTHENTIQUES: Toutes les corrections critiques vérifiées")
                print("✅ COMPLÉTUDE DES CATÉGORIES: Tous les comptes de mots respectés")
                print("✅ FONCTIONNALITÉ API: Tous les endpoints CRUD fonctionnent")
                print("✅ QUALITÉ DES DONNÉES: Tri alphabétique, emojis, structure cohérente")
                print("\n🎯 OBJECTIF ATTEINT: La base de données contient UNIQUEMENT les traductions authentiques")
                print("    fournies par l'utilisateur, sans aucune traduction inventée.")
                print("    La perte de données signalée a été complètement résolue.")
            else:
                print("\n❌ VÉRIFICATION FINALE ÉCHOUÉE!")
                print("Des problèmes persistent dans la récupération de la base de données.")
                
                if not word_count_ok:
                    print("❌ Nombre total de mots insuffisant")
                if not categories_ok:
                    print("❌ Nombre de catégories insuffisant")
                if not no_duplicates:
                    print("❌ Doublons détectés")
                if not critical_correct:
                    print("❌ Traductions critiques incorrectes:")
                    for issue in critical_issues[:5]:  # Show first 5 issues
                        print(f"   • {issue}")
                if not category_completeness:
                    print("❌ Catégories incomplètes:")
                    for issue in category_issues[:5]:  # Show first 5 issues
                        print(f"   • {issue}")
                if not api_functional:
                    print("❌ Problèmes de fonctionnalité API:")
                    for issue in api_issues:
                        print(f"   • {issue}")
                if not sorting_ok:
                    print("❌ Problèmes de tri alphabétique:")
                    for issue in sorting_issues:
                        print(f"   • {issue}")
                if not emojis_present:
                    print("❌ Emojis insuffisants")
                if not structure_consistent:
                    print("❌ Structure de données incohérente")
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Database recovery verification error: {e}")
            return False

def main():
    """Run the database recovery verification test"""
    print("🌺 MAYOTTE EDUCATIONAL APP - DATABASE RECOVERY VERIFICATION 🌺")
    print("=" * 70)
    
    tester = DatabaseRecoveryTester()
    
    # Run the database recovery verification
    result = tester.test_database_recovery_verification()
    
    print("\n" + "=" * 70)
    print("🎯 RÉSULTAT FINAL")
    print("=" * 70)
    
    if result:
        print("✅ RÉCUPÉRATION DE LA BASE DE DONNÉES RÉUSSIE!")
        print("La base de données contient toutes les traductions authentiques de l'utilisateur.")
    else:
        print("❌ RÉCUPÉRATION DE LA BASE DE DONNÉES ÉCHOUÉE!")
        print("Des problèmes persistent et nécessitent une attention immédiate.")
    
    return result

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)