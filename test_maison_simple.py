#!/usr/bin/env python3
"""
Test simple pour le vocabulaire maison mis à jour
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('EXPO_PUBLIC_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

print(f"Testing backend at: {API_BASE}")

def test_maison_vocabulary():
    """Test du vocabulaire maison"""
    print("\n=== Test du Vocabulaire Maison ===")
    
    try:
        # Test de connectivité de base
        print("1. Test de connectivité backend...")
        response = requests.get(f"{API_BASE}/words")
        if response.status_code != 200:
            print(f"❌ Backend non accessible: {response.status_code}")
            return False
        print("✅ Backend accessible")
        
        # Test endpoint maison
        print("\n2. Test endpoint /api/words?category=maison...")
        response = requests.get(f"{API_BASE}/words?category=maison")
        if response.status_code != 200:
            print(f"❌ Endpoint maison failed: {response.status_code}")
            return False
        
        maison_words = response.json()
        print(f"✅ Endpoint maison fonctionne ({len(maison_words)} éléments)")
        
        # Vérification des 8 nouveaux éléments du tableau
        print("\n3. Vérification des 8 nouveaux éléments du tableau...")
        
        nouveaux_elements = [
            {"french": "Bol", "shimaore": "Chicombé", "kibouchi": "Bacouli"},
            {"french": "Cours", "shimaore": "Mraba", "kibouchi": "Lacourou"},
            {"french": "Clôture", "shimaore": "Vala", "kibouchi": "Vala"},
            {"french": "Toilette", "shimaore": "Mrabani", "kibouchi": "Mraba"},
            {"french": "Seau", "shimaore": "Siyo", "kibouchi": "Siyo"},
            {"french": "Mur", "shimaore": "Péssi", "kibouchi": "Riba"},
            {"french": "Fondation", "shimaore": "Houra", "kibouchi": "Koura"},
            {"french": "Torche locale", "shimaore": "Gandilé/Poutroumav", "kibouchi": "Gandili/Poutroumav"}
        ]
        
        maison_by_french = {word['french']: word for word in maison_words}
        nouveaux_trouves = 0
        
        for element in nouveaux_elements:
            french = element['french']
            if french in maison_by_french:
                word = maison_by_french[french]
                if (word['shimaore'] == element['shimaore'] and 
                    word['kibouchi'] == element['kibouchi']):
                    print(f"✅ {french}: {word['shimaore']} / {word['kibouchi']}")
                    nouveaux_trouves += 1
                else:
                    print(f"❌ {french}: Traductions incorrectes")
                    print(f"   Attendu: {element['shimaore']} / {element['kibouchi']}")
                    print(f"   Trouvé: {word['shimaore']} / {word['kibouchi']}")
            else:
                print(f"❌ {french}: Non trouvé")
        
        # Vérification des éléments existants
        print("\n4. Vérification des éléments existants...")
        
        elements_existants = [
            {"french": "Maison", "shimaore": "Nyoumba", "kibouchi": "Tragnou"},
            {"french": "Porte", "shimaore": "Mlango", "kibouchi": "Varavaragena"},
            {"french": "Lit", "shimaore": "Chtrandra", "kibouchi": "Koubani"},
            {"french": "Table", "shimaore": "Latabou", "kibouchi": "Latabou"},
            {"french": "Chaise", "shimaore": "Chiri", "kibouchi": "Chiri"}
        ]
        
        existants_trouves = 0
        for element in elements_existants:
            french = element['french']
            if french in maison_by_french:
                word = maison_by_french[french]
                if (word['shimaore'] == element['shimaore'] and 
                    word['kibouchi'] == element['kibouchi']):
                    print(f"✅ {french}: {word['shimaore']} / {word['kibouchi']}")
                    existants_trouves += 1
                else:
                    print(f"⚠️ {french}: Traductions modifiées")
            else:
                print(f"❌ {french}: Non trouvé")
        
        # Test des doublons
        print("\n5. Test des doublons...")
        french_names = [word['french'] for word in maison_words]
        unique_names = set(french_names)
        
        if len(french_names) == len(unique_names):
            print(f"✅ Aucun doublon ({len(unique_names)} éléments uniques)")
        else:
            duplicates = [name for name in french_names if french_names.count(name) > 1]
            print(f"❌ Doublons trouvés: {set(duplicates)}")
        
        # Affichage de tous les éléments maison
        print(f"\n6. Liste complète des éléments maison ({len(maison_words)} total):")
        for i, word in enumerate(maison_words, 1):
            print(f"   {i:2d}. {word['french']}: {word['shimaore']} / {word['kibouchi']}")
        
        # Résumé
        print(f"\n=== RÉSUMÉ ===")
        print(f"Total éléments maison: {len(maison_words)}")
        print(f"Nouveaux éléments trouvés: {nouveaux_trouves}/8")
        print(f"Éléments existants vérifiés: {existants_trouves}/5")
        print(f"Doublons: {'Non' if len(french_names) == len(unique_names) else 'Oui'}")
        
        # Test des autres catégories
        print(f"\n7. Vérification des autres catégories...")
        all_words_response = requests.get(f"{API_BASE}/words")
        if all_words_response.status_code == 200:
            all_words = all_words_response.json()
            categories = set(word['category'] for word in all_words)
            print(f"Catégories disponibles ({len(categories)}): {sorted(categories)}")
            print(f"Total mots dans toutes les catégories: {len(all_words)}")
        
        return nouveaux_trouves >= 6  # Au moins 6 des 8 nouveaux éléments trouvés
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    print("🏠 TEST VOCABULAIRE MAISON - MAYOTTE 🏠")
    print("=" * 50)
    
    success = test_maison_vocabulary()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TEST RÉUSSI!")
    else:
        print("❌ TEST ÉCHOUÉ!")
    print("=" * 50)