#!/usr/bin/env python3
"""
CORRECTION URGENTE - Ajout des champs audio manquants pour les expressions
Les audios shimaoré ne sont pas accessibles car les champs sont mal nommés
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
print("🚨 CORRECTION URGENTE - CHAMPS AUDIO DES EXPRESSIONS")
print("=" * 80)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Définir les corrections pour les 7 expressions
corrections = [
    {
        'french': "Aujourd'hui",
        'shimoare_audio_filename': 'Léo.m4a',  # ANCIEN FORMAT (avec faute d'orthographe)
        'audio_filename_shimaore': 'Léo.m4a',  # NOUVEAU FORMAT (correct)
        'audio_filename_kibouchi': 'Nyani.m4a'
    },
    {
        'french': 'demain',
        'shimoare_audio_filename': 'Mésso.m4a',
        'audio_filename_shimaore': 'Mésso.m4a',
        'audio_filename_kibouchi': 'Amaréyi.m4a'
    },
    {
        'french': 'après demain',
        'shimoare_audio_filename': 'Bada mésso.m4a',
        'audio_filename_shimaore': 'Bada mésso.m4a',
        'audio_filename_kibouchi': 'Hafaka amaréyi.m4a'
    },
    {
        'french': 'hier',
        'shimoare_audio_filename': 'Jana.m4a',
        'audio_filename_shimaore': 'Jana.m4a',
        'audio_filename_kibouchi': 'Nimoili.m4a'
    },
    {
        'french': 'avant-hier',
        'shimoare_audio_filename': 'Zouzi.m4a',
        'audio_filename_shimaore': 'Zouzi.m4a',
        'audio_filename_kibouchi': 'Nafaka nimoili.m4a'
    },
    {
        'french': "l'année prochaine",
        'shimoare_audio_filename': 'Moihani.m4a',
        'audio_filename_shimaore': 'Moihani.m4a',
        'audio_filename_kibouchi': 'Moikani.m4a'
    },
    {
        'french': "l'année dernière",
        'shimoare_audio_filename': 'Moiha jana.m4a',
        'audio_filename_shimaore': 'Moiha jana.m4a',
        'audio_filename_kibouchi': 'Moikadjana.m4a'
    }
]

print("⚠️  PROBLÈME DÉTECTÉ:")
print("Les champs audio ont été mal nommés lors de l'ajout initial")
print("Les audios SHIMAORÉ ne sont PAS accessibles dans l'application")
print()
print("📝 CORRECTIONS À EFFECTUER:")
print("Ajouter les champs manquants avec les bons noms")
print()

successful = 0
failed = 0

for correction in corrections:
    print(f"{'='*80}")
    print(f"Correction: {correction['french']}")
    print(f"{'='*80}")
    
    word = db['words'].find_one({
        'french': correction['french'],
        'category': 'expressions'
    })
    
    if word:
        print(f"✅ Trouvé en base")
        print(f"   Avant correction:")
        print(f"      - shimoare_audio_filename (ancien format): {word.get('shimoare_audio_filename', 'N/A')}")
        print(f"      - audio_filename_shimaore (nouveau format): {word.get('audio_filename_shimaore', 'N/A')}")
        print(f"      - audio_filename_kibouchi (nouveau format): {word.get('audio_filename_kibouchi', 'N/A')}")
        
        # Préparer les mises à jour
        update_data = {
            'shimoare_audio_filename': correction['shimoare_audio_filename'],
            'audio_filename_shimaore': correction['audio_filename_shimaore'],
            'audio_filename_kibouchi': correction['audio_filename_kibouchi'],
            'updated_at': datetime.utcnow()
        }
        
        # Effectuer la mise à jour
        result = db['words'].update_one(
            {'_id': word['_id']},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            print(f"\n✅ CORRECTION RÉUSSIE:")
            print(f"   Après correction:")
            print(f"      - shimoare_audio_filename: {correction['shimoare_audio_filename']} ✅")
            print(f"      - audio_filename_shimaore: {correction['audio_filename_shimaore']} ✅")
            print(f"      - audio_filename_kibouchi: {correction['audio_filename_kibouchi']} ✅")
            successful += 1
        else:
            print(f"\n⚠️  Aucune modification (déjà correct?)")
            failed += 1
    else:
        print(f"❌ NON trouvé: {correction['french']}")
        failed += 1
    
    print()

print(f"{'='*80}")
print("RÉSUMÉ")
print(f"{'='*80}")
print(f"✅ Corrections réussies: {successful}")
print(f"❌ Échecs: {failed}")
print(f"📊 Total traité: {len(corrections)}")

# Vérification finale
print(f"\n{'='*80}")
print("VÉRIFICATION FINALE")
print(f"{'='*80}")

all_ok = True
for correction in corrections:
    word = db['words'].find_one({
        'french': correction['french'],
        'category': 'expressions'
    })
    
    if word:
        has_old = word.get('shimoare_audio_filename') == correction['shimoare_audio_filename']
        has_new_sh = word.get('audio_filename_shimaore') == correction['audio_filename_shimaore']
        has_new_ki = word.get('audio_filename_kibouchi') == correction['audio_filename_kibouchi']
        
        status = "✅" if (has_old and has_new_sh and has_new_ki) else "❌"
        print(f"{status} {correction['french']}")
        if not (has_old and has_new_sh and has_new_ki):
            print(f"   ⚠️  Champs manquants détectés")
            all_ok = False
    else:
        print(f"❌ {correction['french']}: NON TROUVÉ")
        all_ok = False

print(f"\n{'='*80}")
if all_ok:
    print("🎉 TOUTES LES CORRECTIONS EFFECTUÉES AVEC SUCCÈS !")
    print("Les audios SHIMAORÉ et KIBOUCHI sont maintenant accessibles")
else:
    print("⚠️  PROBLÈME: Certaines corrections n'ont pas été appliquées")

print(f"{'='*80}")

client.close()
