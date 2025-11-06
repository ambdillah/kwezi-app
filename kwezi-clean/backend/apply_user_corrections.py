#!/usr/bin/env python3
"""
Script pour appliquer les corrections et suppressions selon l'image fournie
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

print("🔧 APPLICATION DES CORRECTIONS ET SUPPRESSIONS")
print("=" * 70)

# SUPPRESSIONS
suppressions = ['Pente', 'Tante', 'Homme', 'Fille', 'Femme']

print("\n🗑️  SUPPRESSIONS:")
for french in suppressions:
    result = words_collection.delete_one({'french': french})
    if result.deleted_count > 0:
        print(f"  ✅ '{french}' supprimé")
    else:
        print(f"  ⚠️  '{french}' non trouvé")

# CORRECTIONS (fautes d'orthographe et autres)
corrections = {
    # Note: "aile de poulet" doit être remplacé selon ton commentaire
    # Je vais te demander par quoi le remplacer
    'Vedettes': {
        'note': 'Vérifier traduction',
        'action': 'check'
    },
    'Ciboulette': {
        'shimaore': 'chourougnou ya mani',  # Vérifier orthographe
        'kibouchi': 'doungoulou ravigni'
    },
    'terre': {
        'shimaore': 'trotro',  # Correction: trotto → trotro
        'kibouchi': 'fotaka'
    },
    'manguier': {
        'shimaore': 'm\'manga',  # Apostrophe correcte
        'kibouchi': 'vudi ni manga'
    },
    'jacquier': {
        'shimaore': 'm\'fénissi',  # Apostrophe correcte
        'kibouchi': 'vudi ni finéssi'  # Correction: finéssi
    },
    'cocotier': {
        'shimaore': 'm\'nadzi',  # Apostrophe correcte
        'kibouchi': 'vudi ni vwaniou'
    },
    'baobab': {
        'shimaore': 'm\'bouyou',  # Apostrophe correcte
        'kibouchi': 'vudi ni bouyou'
    },
    'bananier': {
        'shimaore': 'trindri',
        'kibouchi': 'vudi ni hountsi'
    },
    'Fourmis': {
        'shimaore': 'tsoussou',
        'kibouchi': 'vitsiki'
    },
    'Léger': {
        'shimaore': 'ndzangou',
        'kibouchi': 'mayivagna'
    },
    'Inutile': {
        'shimaore': 'kassina mana',
        'kibouchi': 'tsissi fotouni'
    },
    'Honteux': {
        'shimaore': 'ouona haya',
        'kibouchi': 'mamphingnatra'
    }
}

print("\n✏️  CORRECTIONS:")
corrected_count = 0
not_found = []

for french, correction in corrections.items():
    if correction.get('action') == 'check':
        print(f"  ⚠️  '{french}': {correction.get('note')}")
        continue
    
    word = words_collection.find_one({'french': french})
    
    if not word:
        print(f"  ❌ '{french}' non trouvé dans la base")
        not_found.append(french)
        continue
    
    update_data = {}
    changes = []
    
    if 'shimaore' in correction:
        if word.get('shimaore') != correction['shimaore']:
            update_data['shimaore'] = correction['shimaore']
            changes.append(f"shimaoré: '{word.get('shimaore')}' → '{correction['shimaore']}'")
    
    if 'kibouchi' in correction:
        if word.get('kibouchi') != correction['kibouchi']:
            update_data['kibouchi'] = correction['kibouchi']
            changes.append(f"kibouchi: '{word.get('kibouchi')}' → '{correction['kibouchi']}'")
    
    if update_data:
        result = words_collection.update_one(
            {'_id': word['_id']},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            print(f"  ✅ '{french}':")
            for change in changes:
                print(f"      {change}")
            corrected_count += 1
        else:
            print(f"  ⚠️  '{french}': Échec de la mise à jour")
    else:
        print(f"  ✓ '{french}': Déjà correct")

# Recherche d'audios manquants
print("\n\n🔍 RECHERCHE DES AUDIOS MANQUANTS:")
print("=" * 70)

mots_a_verifier = list(corrections.keys())
audios_manquants = []

for french in mots_a_verifier:
    word = words_collection.find_one({'french': french})
    if word:
        audio_sh = word.get('audio_shimaore', '')
        audio_kb = word.get('audio_kibouchi', '')
        
        if not audio_sh or not audio_kb:
            audios_manquants.append({
                'french': french,
                'shimaore': word.get('shimaore'),
                'kibouchi': word.get('kibouchi'),
                'audio_sh': audio_sh,
                'audio_kb': audio_kb
            })

if audios_manquants:
    print(f"\n⚠️  {len(audios_manquants)} mots sans audio complet:")
    for word in audios_manquants:
        print(f"\n  📝 {word['french']}:")
        print(f"      Shimaoré: {word['shimaore']} {'(✗ audio manquant)' if not word['audio_sh'] else '(✓ audio présent)'}")
        print(f"      Kibouchi: {word['kibouchi']} {'(✗ audio manquant)' if not word['audio_kb'] else '(✓ audio présent)'}")
else:
    print("  ✅ Tous les mots ont des audios")

# QUESTION SPÉCIALE: "aile de poulet"
print("\n\n❓ QUESTION:")
print("=" * 70)
print("Le mot 'aile de poulet' est marqué 'à corriger'.")
word_poulet = words_collection.find_one({'french': 'aile de poulet'})
if word_poulet:
    print(f"  Actuellement: {word_poulet.get('shimaore')} / {word_poulet.get('kibouchi')}")
    print(f"  ⚠️  Par quoi veux-tu le remplacer ?")
    print(f"      Options possibles:")
    print(f"      1. Corriger juste les traductions")
    print(f"      2. Remplacer par un autre mot (poulet entier, cuisse, etc.)")

# Résumé final
print("\n\n📊 RÉSUMÉ:")
print("=" * 70)
print(f"  ✅ Suppressions: {len(suppressions)} mots")
print(f"  ✅ Corrections: {corrected_count} mots")
print(f"  ⚠️  Audios manquants: {len(audios_manquants)} mots")
print(f"  ❌ Mots non trouvés: {len(not_found)}")

if not_found:
    print(f"\n  Mots non trouvés:")
    for m in not_found:
        print(f"    - {m}")

client.close()
print("\n✅ Script terminé!")
