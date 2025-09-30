#!/usr/bin/env python3
"""
Backend Test Suite for "Construire des phrases" Game Corrections
Testing the corrections made to the pronoun "wassi" → "wasi" and conjugation system
"""

import requests
import json
import sys
from typing import List, Dict, Any

# Configuration
BASE_URL = "https://kwezi-db-rescue.preview.emergentagent.com"
API_BASE = f"{BASE_URL}/api"

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_test(self, name: str, passed: bool, message: str = ""):
        self.tests.append({
            "name": name,
            "passed": passed,
            "message": message
        })
        if passed:
            self.passed += 1
            print(f"✅ {name}")
            if message:
                print(f"   {message}")
        else:
            self.failed += 1
            print(f"❌ {name}")
            if message:
                print(f"   {message}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY: {self.passed}/{total} tests passed")
        print(f"{'='*60}")
        
        if self.failed > 0:
            print("\nFAILED TESTS:")
            for test in self.tests:
                if not test["passed"]:
                    print(f"❌ {test['name']}: {test['message']}")
        
        return self.failed == 0

def make_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make HTTP request to API endpoint"""
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {endpoint}: {e}")
        return {}

def test_pronoun_correction(results: TestResults):
    """Test 1: Vérifier la correction du pronom 'wassi' → 'wasi'"""
    print("\n🔍 TEST 1: Vérification correction pronom 'wassi' → 'wasi'")
    
    # Get grammar words
    grammar_words = make_request("/words?category=grammaire")
    
    if not grammar_words:
        results.add_test("Récupération mots grammaire", False, "Impossible de récupérer les mots de grammaire")
        return
    
    results.add_test("Récupération mots grammaire", True, f"{len(grammar_words)} mots trouvés")
    
    # Find "Nous" pronoun
    nous_pronoun = None
    for word in grammar_words:
        if word.get("french", "").lower() == "nous":
            nous_pronoun = word
            break
    
    if not nous_pronoun:
        results.add_test("Pronom 'Nous' trouvé", False, "Pronom 'Nous' non trouvé dans la catégorie grammaire")
        return
    
    results.add_test("Pronom 'Nous' trouvé", True, f"ID: {nous_pronoun.get('id')}")
    
    # Check if shimaore translation is "wasi" (correct) and not "wassi" (incorrect)
    shimaore_translation = nous_pronoun.get("shimaore", "").lower()
    
    if shimaore_translation == "wasi":
        results.add_test("Correction 'wassi' → 'wasi' appliquée", True, f"Traduction shimaoré: '{nous_pronoun.get('shimaore')}'")
    else:
        results.add_test("Correction 'wassi' → 'wasi' appliquée", False, f"Traduction shimaoré incorrecte: '{nous_pronoun.get('shimaore')}' (attendu: 'wasi')")
    
    # Check that no words contain "wassi" anywhere
    all_words = make_request("/words")
    wassi_found = []
    
    for word in all_words:
        french = word.get("french", "").lower()
        shimaore = word.get("shimaore", "").lower()
        kibouchi = word.get("kibouchi", "").lower()
        
        if "wassi" in french or "wassi" in shimaore or "wassi" in kibouchi:
            wassi_found.append(word)
    
    if len(wassi_found) == 0:
        results.add_test("Aucun 'wassi' dans la base", True, "Aucune occurrence de 'wassi' trouvée")
    else:
        results.add_test("Aucun 'wassi' dans la base", False, f"{len(wassi_found)} occurrences de 'wassi' trouvées")
        for word in wassi_found[:3]:  # Show first 3
            print(f"   - {word.get('french')}: {word.get('shimaore')} / {word.get('kibouchi')}")

def test_sentences_api(results: TestResults):
    """Test 2: Tester l'API de génération de phrases"""
    print("\n🔍 TEST 2: Test API génération de phrases")
    
    # Test basic sentences endpoint
    sentences = make_request("/sentences?difficulty=1&limit=5")
    
    if not sentences:
        results.add_test("API /sentences accessible", False, "Endpoint /sentences ne répond pas")
        return
    
    results.add_test("API /sentences accessible", True, f"{len(sentences)} phrases récupérées")
    
    # Check sentence structure
    if len(sentences) > 0:
        first_sentence = sentences[0]
        required_fields = ["french", "shimaore", "kibouchi", "tense", "difficulty"]
        
        missing_fields = []
        for field in required_fields:
            if field not in first_sentence:
                missing_fields.append(field)
        
        if len(missing_fields) == 0:
            results.add_test("Structure phrases complète", True, "Tous les champs requis présents")
        else:
            results.add_test("Structure phrases complète", False, f"Champs manquants: {missing_fields}")
        
        # Check for word arrays (needed for game reconstruction)
        if "shimaore_words" in first_sentence and "kibouchi_words" in first_sentence:
            results.add_test("Arrays de mots présents", True, "shimaore_words et kibouchi_words disponibles")
        else:
            results.add_test("Arrays de mots présents", False, "Arrays de mots manquants pour reconstruction du jeu")
    
    # Test filtering by difficulty
    diff2_sentences = make_request("/sentences?difficulty=2&limit=3")
    if diff2_sentences:
        results.add_test("Filtrage par difficulté", True, f"{len(diff2_sentences)} phrases difficulté 2")
    else:
        results.add_test("Filtrage par difficulté", False, "Filtrage par difficulté ne fonctionne pas")

def test_conjugation_system(results: TestResults):
    """Test 3: Vérifier le système de conjugaison avec 'wasi'"""
    print("\n🔍 TEST 3: Test système de conjugaison")
    
    # Get sentences and check for correct pronoun usage
    sentences = make_request("/sentences?limit=20")
    
    if not sentences:
        results.add_test("Récupération phrases conjugaison", False, "Impossible de récupérer les phrases")
        return
    
    results.add_test("Récupération phrases conjugaison", True, f"{len(sentences)} phrases analysées")
    
    # Look for sentences with "nous" and check if they use "wasi" correctly
    nous_sentences = []
    wassi_found_in_sentences = []
    
    for sentence in sentences:
        french = sentence.get("french", "").lower()
        shimaore = sentence.get("shimaore", "")
        kibouchi = sentence.get("kibouchi", "")
        
        if "nous" in french:
            nous_sentences.append(sentence)
            
            # Check if "wassi" is still being used (incorrect)
            if "wassi" in shimaore.lower():
                wassi_found_in_sentences.append(sentence)
    
    if len(nous_sentences) > 0:
        results.add_test("Phrases avec 'nous' trouvées", True, f"{len(nous_sentences)} phrases avec 'nous'")
        
        if len(wassi_found_in_sentences) == 0:
            results.add_test("Conjugaison utilise 'wasi'", True, "Aucune phrase n'utilise l'ancien 'wassi'")
        else:
            results.add_test("Conjugaison utilise 'wasi'", False, f"{len(wassi_found_in_sentences)} phrases utilisent encore 'wassi'")
            for sentence in wassi_found_in_sentences[:2]:  # Show first 2
                print(f"   - {sentence.get('french')}: {sentence.get('shimaore')}")
    else:
        results.add_test("Phrases avec 'nous' trouvées", False, "Aucune phrase avec 'nous' trouvée")

def test_grammar_words_integrity(results: TestResults):
    """Test 4: Vérifier l'intégrité des mots de grammaire"""
    print("\n🔍 TEST 4: Test intégrité mots de grammaire")
    
    grammar_words = make_request("/words?category=grammaire")
    
    if not grammar_words:
        results.add_test("Catégorie grammaire accessible", False, "Impossible d'accéder à la catégorie grammaire")
        return
    
    results.add_test("Catégorie grammaire accessible", True, f"{len(grammar_words)} mots de grammaire")
    
    # Check for essential pronouns
    essential_pronouns = ["je", "tu", "nous", "vous", "il/elle", "ils/elles"]
    found_pronouns = []
    
    for word in grammar_words:
        french = word.get("french", "").lower()
        if french in essential_pronouns:
            found_pronouns.append(french)
    
    missing_pronouns = [p for p in essential_pronouns if p not in found_pronouns]
    
    if len(missing_pronouns) == 0:
        results.add_test("Pronoms essentiels présents", True, f"Tous les pronoms trouvés: {found_pronouns}")
    else:
        results.add_test("Pronoms essentiels présents", False, f"Pronoms manquants: {missing_pronouns}")
    
    # Check for duplicates
    french_words = [word.get("french", "").lower() for word in grammar_words]
    duplicates = []
    seen = set()
    
    for word in french_words:
        if word in seen:
            duplicates.append(word)
        else:
            seen.add(word)
    
    if len(duplicates) == 0:
        results.add_test("Pas de doublons grammaire", True, "Aucun doublon détecté")
    else:
        results.add_test("Pas de doublons grammaire", False, f"Doublons trouvés: {set(duplicates)}")

def test_sentence_variety(results: TestResults):
    """Test 5: Vérifier la variété des phrases générées"""
    print("\n🔍 TEST 5: Test variété des phrases")
    
    sentences = make_request("/sentences?limit=15")
    
    if not sentences:
        results.add_test("Récupération phrases variété", False, "Impossible de récupérer les phrases")
        return
    
    results.add_test("Récupération phrases variété", True, f"{len(sentences)} phrases analysées")
    
    # Check verb variety by analyzing French sentences
    verbs_found = set()
    for sentence in sentences:
        french = sentence.get("french", "").lower()
        # Simple verb extraction (look for common verb patterns)
        words = french.split()
        for word in words:
            if len(word) > 3 and word not in ["nous", "vous", "ils", "elles", "avec", "dans", "pour", "sont", "avez", "ont"]:
                verbs_found.add(word)
    
    if len(verbs_found) >= 8:  # Expect at least 8 different verbs in 15 sentences
        results.add_test("Variété des verbes", True, f"{len(verbs_found)} verbes différents détectés")
    else:
        results.add_test("Variété des verbes", False, f"Seulement {len(verbs_found)} verbes différents (attendu: 8+)")
    
    # Check tense variety
    tenses = set()
    for sentence in sentences:
        tense = sentence.get("tense", "")
        if tense:
            tenses.add(tense)
    
    if len(tenses) >= 2:
        results.add_test("Variété des temps", True, f"Temps trouvés: {list(tenses)}")
    else:
        results.add_test("Variété des temps", False, f"Seulement {len(tenses)} temps différents")

def main():
    """Run all tests"""
    print("🎮 TESTS CORRECTIONS JEU 'CONSTRUIRE DES PHRASES'")
    print("=" * 60)
    print("Vérification des corrections 'wassi' → 'wasi' et système de conjugaison")
    
    results = TestResults()
    
    # Run all test suites
    test_pronoun_correction(results)
    test_sentences_api(results)
    test_conjugation_system(results)
    test_grammar_words_integrity(results)
    test_sentence_variety(results)
    
    # Print summary
    success = results.summary()
    
    if success:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("Les corrections du jeu 'Construire des phrases' sont fonctionnelles.")
    else:
        print(f"\n⚠️  {results.failed} TESTS ONT ÉCHOUÉ")
        print("Des corrections supplémentaires sont nécessaires.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())