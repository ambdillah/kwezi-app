#!/usr/bin/env python3
"""
Script de test pour vérifier le nouveau système audio réel
"""

import requests
import json

def test_real_audio_system():
    """Teste si le nouveau système audio fonctionne correctement."""
    
    api_base = "http://localhost:8001/api"
    
    print("🔧 TEST DU NOUVEAU SYSTÈME AUDIO RÉEL")
    print("=" * 50)
    
    try:
        # Test 1: Récupérer quelques mots de chaque catégorie
        print("\n1. Test des mots avec audio - FAMILLE:")
        famille_response = requests.get(f"{api_base}/words?category=famille")
        if famille_response.status_code == 200:
            famille_words = famille_response.json()
            
            audio_words = [w for w in famille_words if w.get('has_authentic_audio')]
            print(f"   {len(audio_words)}/25 mots famille avec audio")
            
            # Afficher quelques exemples
            for word in audio_words[:3]:
                print(f"   - {word['french']}: {word.get('audio_filename', 'N/A')} ({word.get('audio_pronunciation_lang', 'N/A')})")
        
        print("\n2. Test des mots avec audio - NATURE:")
        nature_response = requests.get(f"{api_base}/words?category=nature")
        if nature_response.status_code == 200:
            nature_words = nature_response.json()
            
            audio_words = [w for w in nature_words if w.get('has_authentic_audio')]
            print(f"   {len(audio_words)}/49 mots nature avec audio")
            
            # Afficher quelques exemples
            for word in audio_words[:3]:
                print(f"   - {word['french']}: {word.get('audio_filename', 'N/A')} ({word.get('audio_pronunciation_lang', 'N/A')})")
        
        print("\n3. Vérification des fichiers critiques:")
        
        # Mots tests pour famille
        test_famille = ["papa", "famille", "ami", "grand-père"]
        for french_word in test_famille:
            word = next((w for w in famille_words if w['french'].lower() == french_word.lower()), None)
            if word:
                has_audio = word.get('has_authentic_audio', False)
                filename = word.get('audio_filename', 'N/A')
                print(f"   👨‍👩‍👧‍👦 {french_word}: {'✅' if has_audio else '❌'} {filename}")
            else:
                print(f"   👨‍👩‍👧‍👦 {french_word}: ❌ Non trouvé")
        
        # Mots tests pour nature
        test_nature = ["arbre", "mer", "soleil", "lune"]
        for french_word in test_nature:
            word = next((w for w in nature_words if w['french'].lower() == french_word.lower()), None)
            if word:
                has_audio = word.get('has_authentic_audio', False)
                filename = word.get('audio_filename', 'N/A')
                print(f"   🌿 {french_word}: {'✅' if has_audio else '❌'} {filename}")
            else:
                print(f"   🌿 {french_word}: ❌ Non trouvé")
        
        print("\n4. RÉSUMÉ:")
        famille_audio_count = len([w for w in famille_words if w.get('has_authentic_audio')])
        nature_audio_count = len([w for w in nature_words if w.get('has_authentic_audio')])
        
        print(f"   📊 Famille: {famille_audio_count}/25 mots avec audio ({famille_audio_count/25*100:.1f}%)")
        print(f"   📊 Nature: {nature_audio_count}/49 mots avec audio ({nature_audio_count/49*100:.1f}%)")
        print(f"   📊 Total: {famille_audio_count + nature_audio_count} mots avec audio authentique")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de test: {str(e)}")
        return False

if __name__ == "__main__":
    test_real_audio_system()