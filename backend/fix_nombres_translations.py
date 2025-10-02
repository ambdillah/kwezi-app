#!/usr/bin/env python3
"""
Script pour CORRIGER les traductions incorrectes des NOMBRES
Basé sur le PDF vocabulaire shimaoré kibouchi FR1.pdf
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connexion MongoDB
MONGO_URL = os.getenv('MONGO_URL')
DB_NAME = os.getenv('DB_NAME', 'mayotte_app')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
words_collection = db.words

# Corrections des NOMBRES selon le PDF
CORRECTIONS_NOMBRES = {
    'un': {'shimaore': 'moja', 'kibouchi': 'areki'},
    'deux': {'shimaore': 'mbili', 'kibouchi': 'Aroyi'},
    'trois': {'shimaore': 'trarou', 'kibouchi': 'Telou'},
    'quatre': {'shimaore': 'nhé', 'kibouchi': 'Efatra'},
    'cinq': {'shimaore': 'tsano', 'kibouchi': 'Dimi'},
    'six': {'shimaore': 'sita', 'kibouchi': 'Tchouta'},
    'sept': {'shimaore': 'saba', 'kibouchi': 'Fitou'},
    'huit': {'shimaore': 'nané', 'kibouchi': 'Valou'},
    'neuf': {'shimaore': 'chendra', 'kibouchi': 'Civi'},  # CORRECTION : neuf = Civi, PAS foulou !
    'dix': {'shimaore': 'koumi', 'kibouchi': 'Foulo'},   # CORRECTION : dix = Foulo
    'onze': {'shimaore': 'koumi na moja', 'kibouchi': 'Foulo Areki Ambi'},
    'douze': {'shimaore': 'koumi na mbili', 'kibouchi': 'Foulo Aroyi Ambi'},
    'treize': {'shimaore': 'koumi na trarou', 'kibouchi': 'Foulo Telou Ambi'},
    'quatorze': {'shimaore': 'koumi na nhé', 'kibouchi': 'Foulo Efatra Ambi'},
    'quinze': {'shimaore': 'koumi na tsano', 'kibouchi': 'Foulo Dimi Ambi'},
}

print("🔧 CORRECTION DES TRADUCTIONS DE NOMBRES")
print("=" * 70)

corrected_count = 0
errors = []

for french, corrections in CORRECTIONS_NOMBRES.items():
    # Vérifier l'état actuel
    word = words_collection.find_one({'french': french, 'category': 'nombres'})
    
    if not word:
        print(f"⚠️  '{french}' non trouvé dans la catégorie nombres")
        errors.append(french)
        continue
    
    current_sh = word.get('shimaore', '')
    current_kb = word.get('kibouchi', '')
    expected_sh = corrections['shimaore']
    expected_kb = corrections['kibouchi']
    
    needs_correction = (current_sh != expected_sh or current_kb != expected_kb)
    
    if needs_correction:
        print(f"\n🔄 {french}:")
        if current_sh != expected_sh:
            print(f"   Shimaoré: '{current_sh}' → '{expected_sh}'")
        if current_kb != expected_kb:
            print(f"   Kibouchi: '{current_kb}' → '{expected_kb}'")
        
        # Appliquer la correction
        result = words_collection.update_one(
            {'_id': word['_id']},
            {'$set': {
                'shimaore': expected_sh,
                'kibouchi': expected_kb
            }}
        )
        
        if result.modified_count > 0:
            corrected_count += 1
            print(f"   ✅ Corrigé")
        else:
            print(f"   ❌ Échec de la correction")
            errors.append(french)
    else:
        print(f"✓ {french} : Déjà correct")

print(f"\n{'=' * 70}")
print(f"📊 RÉSULTATS:")
print(f"  ✅ Nombres corrigés: {corrected_count}")
print(f"  ❌ Erreurs: {len(errors)}")

if errors:
    print(f"\n⚠️  Mots avec problèmes:")
    for e in errors:
        print(f"    - {e}")

# Vérification finale
print(f"\n📋 VÉRIFICATION FINALE:")
test_words = ['neuf', 'dix']
for french in test_words:
    word = words_collection.find_one({'french': french, 'category': 'nombres'})
    if word:
        print(f"\n  {french}:")
        print(f"    Shimaoré: {word.get('shimaore')}")
        print(f"    Kibouchi: {word.get('kibouchi')}")
        print(f"    Audio Shimaoré: {word.get('audio_shimaore', 'Aucun')}")
        print(f"    Audio Kibouchi: {word.get('audio_kibouchi', 'Aucun')}")

client.close()
print(f"\n✅ Correction terminée!")
