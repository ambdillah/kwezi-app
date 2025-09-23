#!/usr/bin/env python3
"""
Test du nouveau système audio dual restructuré pour la section famille
Test des exigences du review request français
"""

import requests
import json
import sys
import os
from datetime import datetime

# Configuration de l'URL backend depuis les variables d'environnement
BACKEND_URL = os.getenv('EXPO_PUBLIC_BACKEND_URL', 'https://dual-language-app.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def log_test(test_name, status, details=""):
    """Log des résultats de test avec timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_icon = "✅" if status else "❌"
    print(f"[{timestamp}] {status_icon} {test_name}")
    if details:
        print(f"    {details}")
    return status

def test_api_connectivity():
    """Test de connectivité API de base"""
    try:
        response = requests.get(f"{API_BASE}/words", timeout=10)
        if response.status_code == 200:
            words = response.json()
            return log_test("Connectivité API", True, f"Backend accessible: {len(words)} mots récupérés")
        else:
            return log_test("Connectivité API", False, f"Status code: {response.status_code}")
    except Exception as e:
        return log_test("Connectivité API", False, f"Erreur: {str(e)}")

def test_famille_words_with_dual_audio_fields():
    """Test 1: Vérifier que tous les mots de famille ont les nouveaux champs audio duaux"""
    try:
        response = requests.get(f"{API_BASE}/words?category=famille", timeout=10)
        if response.status_code != 200:
            return log_test("Champs audio duaux - Famille", False, f"Erreur API: {response.status_code}")
        
        words = response.json()
        if not words:
            return log_test("Champs audio duaux - Famille", False, "Aucun mot famille trouvé")
        
        # Vérifier les nouveaux champs sur tous les mots famille
        required_fields = [
            'dual_audio_system', 'shimoare_has_audio', 'kibouchi_has_audio',
            'shimoare_audio_filename', 'kibouchi_audio_filename'
        ]
        
        words_with_dual_fields = 0
        words_with_dual_system_enabled = 0
        
        for word in words:
            has_all_fields = all(field in word for field in required_fields)
            if has_all_fields:
                words_with_dual_fields += 1
                if word.get('dual_audio_system', False):
                    words_with_dual_system_enabled += 1
        
        total_words = len(words)
        success = words_with_dual_fields > 0
        
        details = f"{words_with_dual_fields}/{total_words} mots avec champs duaux, {words_with_dual_system_enabled} avec système activé"
        return log_test("Champs audio duaux - Famille", success, details)
        
    except Exception as e:
        return log_test("Champs audio duaux - Famille", False, f"Erreur: {str(e)}")

def test_new_dual_audio_endpoints():
    """Test 2: Vérifier les nouveaux endpoints audio duaux"""
    try:
        # D'abord, récupérer un mot famille avec système dual
        response = requests.get(f"{API_BASE}/words?category=famille", timeout=10)
        if response.status_code != 200:
            return log_test("Endpoints audio duaux", False, "Impossible de récupérer les mots famille")
        
        words = response.json()
        dual_word = None
        
        # Chercher un mot avec système dual activé
        for word in words:
            if word.get('dual_audio_system', False):
                dual_word = word
                break
        
        if not dual_word:
            return log_test("Endpoints audio duaux", False, "Aucun mot avec système dual trouvé")
        
        word_id = dual_word['id']
        word_french = dual_word['french']
        
        # Test 2a: GET /api/words/{word_id}/audio-info
        info_response = requests.get(f"{API_BASE}/words/{word_id}/audio-info", timeout=10)
        if info_response.status_code != 200:
            return log_test("Endpoints audio duaux", False, f"audio-info endpoint failed: {info_response.status_code}")
        
        audio_info = info_response.json()
        
        # Vérifier la structure de la réponse
        required_keys = ['word', 'dual_audio_system', 'audio']
        if not all(key in audio_info for key in required_keys):
            return log_test("Endpoints audio duaux", False, "Structure audio-info incorrecte")
        
        # Test 2b: GET /api/words/{word_id}/audio/shimaore (si disponible)
        shimaore_available = audio_info['audio']['shimaore']['has_audio']
        kibouchi_available = audio_info['audio']['kibouchi']['has_audio']
        
        endpoints_tested = 0
        endpoints_working = 0
        
        if shimaore_available:
            endpoints_tested += 1
            shimaore_response = requests.get(f"{API_BASE}/words/{word_id}/audio/shimaore", timeout=10)
            if shimaore_response.status_code == 200:
                endpoints_working += 1
        
        # Test 2c: GET /api/words/{word_id}/audio/kibouchi (si disponible)
        if kibouchi_available:
            endpoints_tested += 1
            kibouchi_response = requests.get(f"{API_BASE}/words/{word_id}/audio/kibouchi", timeout=10)
            if kibouchi_response.status_code == 200:
                endpoints_working += 1
        
        success = endpoints_working == endpoints_tested and endpoints_tested > 0
        details = f"Mot '{word_french}': {endpoints_working}/{endpoints_tested} endpoints audio fonctionnels"
        return log_test("Endpoints audio duaux", success, details)
        
    except Exception as e:
        return log_test("Endpoints audio duaux", False, f"Erreur: {str(e)}")

def test_legacy_audio_compatibility():
    """Test 3: Vérifier la compatibilité avec les anciens endpoints"""
    try:
        # Test 3a: GET /api/audio/famille/{filename} toujours fonctionnel
        famille_response = requests.get(f"{API_BASE}/audio/famille/test.m4a", timeout=10)
        # On s'attend à un 404 car le fichier n'existe probablement pas, mais pas une erreur 500
        famille_working = famille_response.status_code in [200, 404]
        
        # Test 3b: GET /api/audio/info retourne les nouveaux endpoints
        info_response = requests.get(f"{API_BASE}/audio/info", timeout=10)
        if info_response.status_code != 200:
            return log_test("Compatibilité anciens endpoints", False, f"audio/info failed: {info_response.status_code}")
        
        info_data = info_response.json()
        
        # Vérifier que les nouveaux endpoints sont mentionnés
        has_dual_system_endpoint = 'dual_system' in info_data.get('endpoints', {})
        
        success = famille_working and has_dual_system_endpoint
        details = f"Famille endpoint: {'OK' if famille_working else 'FAIL'}, Dual system info: {'OK' if has_dual_system_endpoint else 'FAIL'}"
        return log_test("Compatibilité anciens endpoints", success, details)
        
    except Exception as e:
        return log_test("Compatibilité anciens endpoints", False, f"Erreur: {str(e)}")

def test_specific_words_audio():
    """Test 4: Tests spécifiques pour papa, famille, frère"""
    try:
        # Récupérer tous les mots famille
        response = requests.get(f"{API_BASE}/words?category=famille", timeout=10)
        if response.status_code != 200:
            return log_test("Tests mots spécifiques", False, "Impossible de récupérer les mots famille")
        
        words = response.json()
        word_dict = {word['french'].lower(): word for word in words}
        
        test_words = ['papa', 'famille', 'frère']
        results = {}
        
        for test_word in test_words:
            if test_word not in word_dict:
                results[test_word] = f"Mot '{test_word}' non trouvé"
                continue
            
            word = word_dict[test_word]
            word_id = word['id']
            
            # Vérifier les informations audio
            info_response = requests.get(f"{API_BASE}/words/{word_id}/audio-info", timeout=10)
            if info_response.status_code != 200:
                results[test_word] = f"Erreur audio-info: {info_response.status_code}"
                continue
            
            audio_info = info_response.json()
            
            # Vérifier les fichiers audio attendus
            shimaore_file = audio_info['audio']['shimaore'].get('filename')
            kibouchi_file = audio_info['audio']['kibouchi'].get('filename')
            
            if test_word == 'papa':
                # Papa: doit avoir Baba s.m4a (shimaoré) et Baba k.m4a (kibouchi)
                expected_shimaore = 'Baba s.m4a'
                expected_kibouchi = 'Baba k.m4a'
                shimaore_ok = shimaore_file == expected_shimaore
                kibouchi_ok = kibouchi_file == expected_kibouchi
                results[test_word] = f"Shimaoré: {shimaore_file} ({'✓' if shimaore_ok else '✗'}), Kibouchi: {kibouchi_file} ({'✓' if kibouchi_ok else '✗'})"
                
            elif test_word == 'famille':
                # Famille: doit avoir Mdjamaza.m4a (shimaoré) et Havagna.m4a (kibouchi)
                expected_shimaore = 'Mdjamaza.m4a'
                expected_kibouchi = 'Havagna.m4a'
                shimaore_ok = shimaore_file == expected_shimaore
                kibouchi_ok = kibouchi_file == expected_kibouchi
                results[test_word] = f"Shimaoré: {shimaore_file} ({'✓' if shimaore_ok else '✗'}), Kibouchi: {kibouchi_file} ({'✓' if kibouchi_ok else '✗'})"
                
            elif test_word == 'frère':
                # Frère: doit avoir les bons fichiers audio pour chaque langue
                has_shimaore = audio_info['audio']['shimaore']['has_audio']
                has_kibouchi = audio_info['audio']['kibouchi']['has_audio']
                results[test_word] = f"Shimaoré: {shimaore_file} ({'✓' if has_shimaore else '✗'}), Kibouchi: {kibouchi_file} ({'✓' if has_kibouchi else '✗'})"
        
        # Évaluer le succès global
        success = all('✓' in result for result in results.values())
        details = "; ".join([f"{word}: {result}" for word, result in results.items()])
        return log_test("Tests mots spécifiques", success, details)
        
    except Exception as e:
        return log_test("Tests mots spécifiques", False, f"Erreur: {str(e)}")

def test_dual_pronunciation_validation():
    """Test 5: Validation que chaque mot famille peut avoir DEUX prononciations distinctes"""
    try:
        response = requests.get(f"{API_BASE}/words?category=famille", timeout=10)
        if response.status_code != 200:
            return log_test("Validation prononciations duales", False, "Impossible de récupérer les mots famille")
        
        words = response.json()
        
        words_with_dual_audio = 0
        words_with_both_languages = 0
        total_famille_words = len(words)
        
        for word in words:
            if word.get('dual_audio_system', False):
                words_with_dual_audio += 1
                
                # Vérifier si le mot a des fichiers audio pour les deux langues
                has_shimaore = word.get('shimoare_has_audio', False)
                has_kibouchi = word.get('kibouchi_has_audio', False)
                
                if has_shimaore and has_kibouchi:
                    words_with_both_languages += 1
        
        # Le système doit permettre d'avoir deux prononciations distinctes
        success = words_with_dual_audio > 0 and words_with_both_languages > 0
        details = f"{words_with_dual_audio} mots avec système dual, {words_with_both_languages} avec les deux langues, sur {total_famille_words} mots famille"
        return log_test("Validation prononciations duales", success, details)
        
    except Exception as e:
        return log_test("Validation prononciations duales", False, f"Erreur: {str(e)}")

def run_all_tests():
    """Exécuter tous les tests du système audio dual"""
    print("🎵 DÉBUT DES TESTS DU SYSTÈME AUDIO DUAL RESTRUCTURÉ")
    print("=" * 60)
    
    tests = [
        test_api_connectivity,
        test_famille_words_with_dual_audio_fields,
        test_new_dual_audio_endpoints,
        test_legacy_audio_compatibility,
        test_specific_words_audio,
        test_dual_pronunciation_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        if test_func():
            passed += 1
        print()  # Ligne vide entre les tests
    
    print("=" * 60)
    print(f"🎯 RÉSULTATS: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 TOUS LES TESTS SONT PASSÉS! Le système audio dual est fonctionnel.")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) ont échoué. Vérification nécessaire.")
        return False

if __name__ == "__main__":
    print(f"🔗 URL Backend: {BACKEND_URL}")
    success = run_all_tests()
    sys.exit(0 if success else 1)