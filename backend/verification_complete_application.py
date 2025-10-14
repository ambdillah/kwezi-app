#!/usr/bin/env python3
"""
VÉRIFICATION COMPLÈTE DE TOUTES LES DONNÉES
Comparaison avec le tableau de référence de l'utilisateur
Date: 14 octobre 2025
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_url = os.getenv('MONGO_URL')
client = MongoClient(mongo_url)
db = client[os.getenv('DB_NAME', 'mayotte_app')]

print("=" * 80)
print("🔍 VÉRIFICATION COMPLÈTE DE L'APPLICATION AVANT LANCEMENT")
print("=" * 80)
print()

# Données de référence du tableau utilisateur (catégorie grammaire)
reference_grammaire = {
    'Je / moi': {'shimaore': 'wami', 'kibouchi': 'zahou'},
    'Tu / toi': {'shimaore': 'wawé', 'kibouchi': 'anaou'},
    'Il / Elle / lui': {'shimaore': 'wayé', 'kibouchi': 'izi'},
    'Nous': {'shimaore': 'wassi', 'kibouchi': "at'sika"},
    'Ils / Elles / eux': {'shimaore': 'wawo', 'kibouchi': 'réou'},
    'le mien': {'shimaore': 'yangou', 'kibouchi': 'ninakahi'},
    'le tien': {'shimaore': 'yaho', 'kibouchi': 'ninaou'},
    'le sien': {'shimaore': 'yahé', 'kibouchi': 'ninazi'},
    'le leur': {'shimaore': 'yawo', 'kibouchi': 'nindréou'},
    'le nôtre': {'shimaore': 'yatrou', 'kibouchi': "nint'sika"},
    'le votre': {'shimaore': 'yangnou', 'kibouchi': 'ninaréou'},
    'Vous': {'shimaore': 'wagnou', 'kibouchi': 'anaréou'},
    'professeur': {'shimaore': 'foundi', 'kibouchi': 'foundi'},
    'guide spirituel': {'shimaore': 'cadhi', 'kibouchi': 'cadhi'},
    'Imam': {'shimaore': 'imamou', 'kibouchi': 'imamou'},
    'voisin': {'shimaore': 'djirani', 'kibouchi': 'djirani'},
    'maire': {'shimaore': 'méra', 'kibouchi': 'méra'},
    'élu': {'shimaore': 'dhoimana', 'kibouchi': 'dhoimana'},
    'pêcheur': {'shimaore': 'mlozi', 'kibouchi': 'ampamintagna'},
    'Agriculteur': {'shimaore': 'mlimizi', 'kibouchi': 'ampikapa'},
    'Éleveur': {'shimaore': 'mtsounga', 'kibouchi': 'ampitsounga'},
    'lettre / chiffre': {'shimaore': 'harouf', 'kibouchi': 'harouf'}
}

print("1️⃣  VÉRIFICATION CATÉGORIE GRAMMAIRE")
print("=" * 80)

errors_found = []
warnings_found = []
verified_ok = []

# Récupérer tous les mots de grammaire
grammaire_words = list(db['words'].find({'category': 'grammaire'}))

print(f"\nTotal mots en base (grammaire): {len(grammaire_words)}")
print(f"Mots de référence (tableau): {len(reference_grammaire)}")
print()

# Vérifier chaque mot de référence
for french, expected in reference_grammaire.items():
    # Chercher variantes possibles
    word = db['words'].find_one({
        'category': 'grammaire',
        '$or': [
            {'french': french},
            {'french': french.lower()},
            {'french': french.capitalize()},
            {'french': french.replace(' / ', '/')},  # sans espaces
            {'french': french.replace('/', ' / ')}   # avec espaces
        ]
    })
    
    if word:
        shimaore_ok = word.get('shimaore', '').lower() == expected['shimaore'].lower()
        kibouchi_ok = word.get('kibouchi', '').lower() == expected['kibouchi'].lower()
        
        if shimaore_ok and kibouchi_ok:
            verified_ok.append({
                'french': word['french'],
                'status': 'OK'
            })
            print(f"✅ {word['french']}: {word.get('shimaore')} / {word.get('kibouchi')}")
        else:
            error = {
                'french': word['french'],
                'expected_shimaore': expected['shimaore'],
                'actual_shimaore': word.get('shimaore'),
                'expected_kibouchi': expected['kibouchi'],
                'actual_kibouchi': word.get('kibouchi'),
                'shimaore_ok': shimaore_ok,
                'kibouchi_ok': kibouchi_ok
            }
            errors_found.append(error)
            print(f"❌ {word['french']}:")
            if not shimaore_ok:
                print(f"   Shimaoré: {word.get('shimaore')} ❌ (attendu: {expected['shimaore']})")
            if not kibouchi_ok:
                print(f"   Kibouchi: {word.get('kibouchi')} ❌ (attendu: {expected['kibouchi']})")
    else:
        warnings_found.append({
            'french': french,
            'issue': 'Mot de référence NON trouvé en base'
        })
        print(f"⚠️  {french}: NON TROUVÉ en base")

print(f"\n{'=' * 80}")
print("2️⃣  VÉRIFICATION DES AUTRES CATÉGORIES")
print("=" * 80)

# Vérifier toutes les catégories
categories = db['words'].distinct('category')
print(f"\nCatégories trouvées: {categories}")
print()

category_stats = {}
for cat in categories:
    count = db['words'].count_documents({'category': cat})
    category_stats[cat] = count
    
    # Vérifier qu'aucun mot n'a des traductions vides
    empty_shimaore = db['words'].count_documents({
        'category': cat,
        '$or': [
            {'shimaore': {'$exists': False}},
            {'shimaore': ''},
            {'shimaore': None}
        ]
    })
    
    empty_kibouchi = db['words'].count_documents({
        'category': cat,
        '$or': [
            {'kibouchi': {'$exists': False}},
            {'kibouchi': ''},
            {'kibouchi': None}
        ]
    })
    
    status = "✅" if (empty_shimaore == 0 and empty_kibouchi == 0) else "⚠️"
    print(f"{status} {cat}: {count} mots", end='')
    if empty_shimaore > 0 or empty_kibouchi > 0:
        print(f" (⚠️  {empty_shimaore} sans shimaoré, {empty_kibouchi} sans kibouchi)")
    else:
        print()

print(f"\n{'=' * 80}")
print("3️⃣  RAPPORT FINAL")
print("=" * 80)

print(f"\n✅ Mots vérifiés OK: {len(verified_ok)}")
print(f"❌ Erreurs trouvées: {len(errors_found)}")
print(f"⚠️  Avertissements: {len(warnings_found)}")

if errors_found:
    print(f"\n{'=' * 80}")
    print("🚨 ERREURS À CORRIGER:")
    print("=" * 80)
    for err in errors_found:
        print(f"\n❌ {err['french']}")
        print(f"   Shimaoré: {err['actual_shimaore']} → devrait être: {err['expected_shimaore']}")
        print(f"   Kibouchi: {err['actual_kibouchi']} → devrait être: {err['expected_kibouchi']}")

if warnings_found:
    print(f"\n{'=' * 80}")
    print("⚠️  AVERTISSEMENTS:")
    print("=" * 80)
    for warn in warnings_found:
        print(f"⚠️  {warn['french']}: {warn['issue']}")

print(f"\n{'=' * 80}")
print("STATUT GLOBAL:")
print("=" * 80)

if len(errors_found) == 0 and len(warnings_found) == 0:
    print("🎉 🎉 🎉 APPLICATION PRÊTE POUR LE LANCEMENT ! 🎉 🎉 🎉")
    print("✅ Aucune erreur détectée")
    print("✅ Toutes les données sont cohérentes")
elif len(errors_found) == 0:
    print("✅ Aucune erreur critique")
    print(f"⚠️  {len(warnings_found)} avertissements à vérifier")
else:
    print(f"🚨 {len(errors_found)} ERREURS CRITIQUES À CORRIGER AVANT LANCEMENT")
    print("⚠️  Application NON prête pour le lancement")

print(f"\n{'=' * 80}")

client.close()
