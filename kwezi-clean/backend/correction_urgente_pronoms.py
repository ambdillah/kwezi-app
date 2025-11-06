#!/usr/bin/env python3
"""
CORRECTION URGENTE - Restauration des pronoms corrects
Les traductions avaient été INVERSÉES par erreur !
Date: 14 octobre 2025
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

mongo_url = os.getenv('MONGO_URL')
client = MongoClient(mongo_url)
db = client[os.getenv('DB_NAME', 'mayotte_app')]

print("=" * 80)
print("🚨 CORRECTION URGENTE - RESTAURATION DES PRONOMS CORRECTS 🚨")
print("=" * 80)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# VRAIES traductions correctes d'après le tableau de l'utilisateur
corrections_urgentes = [
    {
        'french': 'Je / moi',
        'correct_shimaore': 'wami',
        'correct_kibouchi': 'zahou',
        'wrong_shimaore': 'Nani',  # Ce qui a été mis par erreur
        'wrong_kibouchi': 'Ma'     # Ce qui a été mis par erreur
    },
    {
        'french': 'Tu / toi',
        'correct_shimaore': 'wawé',
        'correct_kibouchi': 'anaou',
        'wrong_shimaore': 'Wé',
        'wrong_kibouchi': 'Ya'
    },
    {
        'french': 'Il / Elle / lui',
        'correct_shimaore': 'wayé',
        'correct_kibouchi': 'izi',
        'wrong_shimaore': 'Ye',
        'wrong_kibouchi': 'Na'
    },
    {
        'french': 'Nous',
        'correct_shimaore': 'wassi',  # Attention : "wassi" pas "wasi"
        'correct_kibouchi': "at'sika",  # Attention : "at'sika" pas "atsika"
        'wrong_shimaore': 'Rihi',
        'wrong_kibouchi': 'Gali'
    },
    {
        'french': 'Ils / Elles / eux',
        'correct_shimaore': 'wawo',
        'correct_kibouchi': 'réou',
        'wrong_shimaore': 'Bé',
        'wrong_kibouchi': 'Nao'
    }
]

print("⚠️  ERREUR DÉTECTÉE : Les traductions avaient été inversées !")
print("⚠️  Restauration des VRAIES traductions d'après le tableau utilisateur")
print()

successful = 0
failed = 0

for correction in corrections_urgentes:
    print(f"\n{'='*80}")
    print(f"Correction: {correction['french']}")
    print(f"{'='*80}")
    
    # Trouver l'entrée avec les MAUVAISES traductions
    word = db['words'].find_one({
        'french': correction['french'],
        'category': 'grammaire'
    })
    
    if word:
        print(f"✅ Trouvé en base")
        print(f"   Traductions INCORRECTES actuelles:")
        print(f"      Shimaoré: {word.get('shimaore')} (devrait être {correction['correct_shimaore']})")
        print(f"      Kibouchi: {word.get('kibouchi')} (devrait être {correction['correct_kibouchi']})")
        
        # RESTAURER les VRAIES traductions
        result = db['words'].update_one(
            {'_id': word['_id']},
            {'$set': {
                'shimaore': correction['correct_shimaore'],
                'kibouchi': correction['correct_kibouchi'],
                'updated_at': datetime.utcnow(),
                'correction_note': 'Restauration des traductions correctes après erreur'
            }}
        )
        
        if result.modified_count > 0:
            print(f"\n✅ ✅ ✅ CORRIGÉ AVEC SUCCÈS !")
            print(f"   Traductions CORRECTES restaurées:")
            print(f"      Shimaoré: {correction['correct_shimaore']} ✅")
            print(f"      Kibouchi: {correction['correct_kibouchi']} ✅")
            successful += 1
        else:
            print(f"\n⚠️  Aucune modification (déjà correct?)")
            failed += 1
    else:
        print(f"❌ NON trouvé: {correction['french']}")
        failed += 1

print(f"\n{'='*80}")
print("RÉSUMÉ DE LA CORRECTION URGENTE")
print(f"{'='*80}")
print(f"✅ Corrections réussies: {successful}")
print(f"❌ Échecs: {failed}")
print(f"📊 Total traité: {len(corrections_urgentes)}")

# Vérifier le résultat final
print(f"\n{'='*80}")
print("VÉRIFICATION POST-CORRECTION")
print(f"{'='*80}")

for correction in corrections_urgentes:
    word = db['words'].find_one({
        'french': correction['french'],
        'category': 'grammaire'
    })
    if word:
        shimaore_ok = word.get('shimaore') == correction['correct_shimaore']
        kibouchi_ok = word.get('kibouchi') == correction['correct_kibouchi']
        
        status = "✅" if (shimaore_ok and kibouchi_ok) else "❌"
        print(f"\n{status} {correction['french']}")
        print(f"   Shimaoré: {word.get('shimaore')} {'✅' if shimaore_ok else '❌ ERREUR'}")
        print(f"   Kibouchi: {word.get('kibouchi')} {'✅' if kibouchi_ok else '❌ ERREUR'}")

print(f"\n{'='*80}")
print("CORRECTION URGENTE TERMINÉE")
print(f"{'='*80}")

client.close()
