#!/usr/bin/env python3
"""
Ajout de 3 nouveaux mots dans la catégorie "maison" avec leurs audios
Date: 14 octobre 2025
Catégorie: maison
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
print("AJOUT DE 3 NOUVEAUX MOTS CATÉGORIE 'MAISON'")
print("=" * 80)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Définir les 3 nouveaux mots avec TOUTES leurs métadonnées
nouveaux_mots = [
    {
        'french': 'savon',
        'shimaore': 'sabouni',
        'kibouchi': 'sabouni',
        'shimoare_audio_filename': 'Sabouni.m4a',  # Ancien format
        'audio_filename_shimaore': 'Sabouni.m4a',  # Nouveau format
        'audio_filename_kibouchi': 'Sabouni.m4a',  # MÊME fichier (traduction identique)
        'category': 'maison',
        'difficulty': 1,
        'audio_category': 'maison',
        'dual_audio_system': True,
        'has_shimaore_audio': True,
        'has_kibouchi_audio': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'audio_source': 'authentic',
        'audio_updated_at': datetime.utcnow(),
        'note': 'Traduction identique en shimaoré et kibouchi'
    },
    {
        'french': 'brosse à dent',
        'shimaore': 'msouaki',
        'kibouchi': 'msouaki',
        'shimoare_audio_filename': 'Msouaki.m4a',
        'audio_filename_shimaore': 'Msouaki.m4a',
        'audio_filename_kibouchi': 'Msouaki.m4a',  # MÊME fichier (traduction identique)
        'category': 'maison',
        'difficulty': 1,
        'audio_category': 'maison',
        'dual_audio_system': True,
        'has_shimaore_audio': True,
        'has_kibouchi_audio': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'audio_source': 'authentic',
        'audio_updated_at': datetime.utcnow(),
        'note': 'Traduction identique en shimaoré et kibouchi'
    },
    {
        'french': 'tapis',
        'shimaore': 'djavi',
        'kibouchi': 'tsihi',
        'shimoare_audio_filename': 'Djavi.m4a',
        'audio_filename_shimaore': 'Djavi.m4a',
        'audio_filename_kibouchi': 'Tsihi.m4a',  # Fichier DIFFÉRENT
        'category': 'maison',
        'difficulty': 1,
        'audio_category': 'maison',
        'dual_audio_system': True,
        'has_shimaore_audio': True,
        'has_kibouchi_audio': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'audio_source': 'authentic',
        'audio_updated_at': datetime.utcnow(),
        'note': 'Traductions différentes en shimaoré et kibouchi'
    }
]

# Vérifier l'état initial
count_before = db['words'].count_documents({'category': 'maison'})
print(f"📊 Mots 'maison' avant ajout: {count_before}")
print()

# Ajouter chaque mot avec vérification
successful_adds = 0
failed_adds = 0
already_exists = 0

for mot in nouveaux_mots:
    print(f"{'='*80}")
    print(f"Traitement: {mot['french']}")
    print(f"{'='*80}")
    
    # Vérifier si existe déjà
    existing = db['words'].find_one({
        'french': mot['french'],
        'category': 'maison'
    })
    
    if existing:
        print(f"⚠️  Mot déjà existant:")
        print(f"   Shimaoré: {existing.get('shimaore')}")
        print(f"   Kibouchi: {existing.get('kibouchi')}")
        already_exists += 1
        continue
    
    # Vérifier que les fichiers audio existent physiquement
    audio_dir = '/app/frontend/assets/audio/maison'
    shimaore_file = os.path.join(audio_dir, mot['audio_filename_shimaore'])
    kibouchi_file = os.path.join(audio_dir, mot['audio_filename_kibouchi'])
    
    shimaore_exists = os.path.exists(shimaore_file)
    kibouchi_exists = os.path.exists(kibouchi_file)
    
    print(f"Vérification des fichiers audio:")
    print(f"   Shimaoré ({mot['audio_filename_shimaore']}): {'✅' if shimaore_exists else '❌'}")
    print(f"   Kibouchi ({mot['audio_filename_kibouchi']}): {'✅' if kibouchi_exists else '❌'}")
    
    # Si même fichier, afficher une note
    if mot['audio_filename_shimaore'] == mot['audio_filename_kibouchi']:
        print(f"   📝 Note: Même fichier audio pour shimaoré et kibouchi (traduction identique)")
    
    if not shimaore_exists or not kibouchi_exists:
        print(f"❌ ERREUR: Fichiers audio manquants!")
        failed_adds += 1
        continue
    
    # Afficher les traductions
    print(f"\nTraductions:")
    print(f"   Shimaoré: {mot['shimaore']}")
    print(f"   Kibouchi: {mot['kibouchi']}")
    if mot['shimaore'] == mot['kibouchi']:
        print(f"   📝 Traduction identique dans les deux langues")
    
    # Insérer dans la base
    try:
        result = db['words'].insert_one(mot)
        
        if result.inserted_id:
            print(f"\n✅ AJOUT RÉUSSI:")
            print(f"   ID: {result.inserted_id}")
            print(f"   Français: {mot['french']}")
            print(f"   Shimaoré: {mot['shimaore']}")
            print(f"   Kibouchi: {mot['kibouchi']}")
            print(f"   Audio shimaoré: {mot['audio_filename_shimaore']}")
            print(f"   Audio kibouchi: {mot['audio_filename_kibouchi']}")
            successful_adds += 1
        else:
            print(f"❌ Échec de l'insertion")
            failed_adds += 1
            
    except Exception as e:
        print(f"❌ ERREUR lors de l'insertion: {str(e)}")
        failed_adds += 1
    
    print()

# Vérifier l'état final
count_after = db['words'].count_documents({'category': 'maison'})

print(f"{'='*80}")
print("RÉSUMÉ")
print(f"{'='*80}")
print(f"✅ Ajouts réussis: {successful_adds}")
print(f"⚠️  Déjà existants: {already_exists}")
print(f"❌ Échecs: {failed_adds}")
print(f"📊 Total traité: {len(nouveaux_mots)}")
print()
print(f"📊 Mots 'maison' AVANT: {count_before}")
print(f"📊 Mots 'maison' APRÈS: {count_after}")
print(f"📊 Différence: +{count_after - count_before}")

# Vérification finale
print(f"\n{'='*80}")
print("VÉRIFICATION FINALE")
print(f"{'='*80}")

all_ok = True
for mot in nouveaux_mots:
    word = db['words'].find_one({
        'french': mot['french'],
        'category': 'maison'
    })
    
    if word:
        print(f"✅ {mot['french']}: {word.get('shimaore')} / {word.get('kibouchi')}")
        # Vérifier les champs audio
        has_old = word.get('shimoare_audio_filename')
        has_new_sh = word.get('audio_filename_shimaore')
        has_new_ki = word.get('audio_filename_kibouchi')
        if not (has_old and has_new_sh and has_new_ki):
            print(f"   ⚠️  Champs audio incomplets")
            all_ok = False
    else:
        print(f"❌ {mot['french']}: NON TROUVÉ")
        all_ok = False

print(f"\n{'='*80}")
if all_ok and successful_adds == len(nouveaux_mots):
    print("🎉 TOUS LES MOTS ONT ÉTÉ AJOUTÉS AVEC SUCCÈS !")
    print("✅ Total mots 'maison': 42 (39 + 3 nouveaux)")
elif already_exists > 0 and (successful_adds + already_exists) == len(nouveaux_mots):
    print("✅ TOUS LES MOTS SONT PRÉSENTS (certains existaient déjà)")
else:
    print("⚠️  PROBLÈME: Tous les mots n'ont pas été ajoutés correctement")

print(f"{'='*80}")

client.close()
