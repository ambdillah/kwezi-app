#!/usr/bin/env python3
"""
Ajout de 7 nouvelles expressions temporelles avec leurs audios
Date: 14 octobre 2025
Catégorie: expressions
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
print("AJOUT DE 7 NOUVELLES EXPRESSIONS TEMPORELLES")
print("=" * 80)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Définir les 7 nouvelles expressions avec TOUTES leurs métadonnées
nouvelles_expressions = [
    {
        'french': "Aujourd'hui",
        'shimaore': 'léo',
        'kibouchi': 'nyani',
        'shimaore_audio_filename': 'Léo.m4a',
        'kibouchi_audio_filename': 'Nyani.m4a',
        'category': 'expressions',
        'difficulty': 1,
        'audio_category': 'expressions',
        'dual_audio_system': True,
        'has_shimaore_audio': True,
        'has_kibouchi_audio': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'audio_source': 'authentic',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'demain',
        'shimaore': 'mésso',
        'kibouchi': 'amaréyi',
        'shimaore_audio_filename': 'Mésso.m4a',
        'kibouchi_audio_filename': 'Amaréyi.m4a',
        'category': 'expressions',
        'difficulty': 1,
        'audio_category': 'expressions',
        'dual_audio_system': True,
        'has_shimaore_audio': True,
        'has_kibouchi_audio': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'audio_source': 'authentic',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'après demain',
        'shimaore': 'bada mésso',
        'kibouchi': 'hafaaka amaréyi',
        'shimaore_audio_filename': 'Bada mésso.m4a',
        'kibouchi_audio_filename': 'Hafaka amaréyi.m4a',
        'category': 'expressions',
        'difficulty': 2,
        'audio_category': 'expressions',
        'dual_audio_system': True,
        'has_shimaore_audio': True,
        'has_kibouchi_audio': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'audio_source': 'authentic',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'hier',
        'shimaore': 'jana',
        'kibouchi': 'nimoili',
        'shimaore_audio_filename': 'Jana.m4a',
        'kibouchi_audio_filename': 'Nimoili.m4a',
        'category': 'expressions',
        'difficulty': 1,
        'audio_category': 'expressions',
        'dual_audio_system': True,
        'has_shimaore_audio': True,
        'has_kibouchi_audio': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'audio_source': 'authentic',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'avant-hier',
        'shimaore': 'zouzi',
        'kibouchi': 'nafaka nimoili',
        'shimaore_audio_filename': 'Zouzi.m4a',
        'kibouchi_audio_filename': 'Nafaka nimoili.m4a',
        'category': 'expressions',
        'difficulty': 2,
        'audio_category': 'expressions',
        'dual_audio_system': True,
        'has_shimaore_audio': True,
        'has_kibouchi_audio': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'audio_source': 'authentic',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': "l'année prochaine",
        'shimaore': 'moihani',
        'kibouchi': 'moikani',
        'shimaore_audio_filename': 'Moihani.m4a',
        'kibouchi_audio_filename': 'Moikani.m4a',
        'category': 'expressions',
        'difficulty': 2,
        'audio_category': 'expressions',
        'dual_audio_system': True,
        'has_shimaore_audio': True,
        'has_kibouchi_audio': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'audio_source': 'authentic',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': "l'année dernière",
        'shimaore': 'moiha jana',
        'kibouchi': 'moikadjana',
        'shimaore_audio_filename': 'Moiha jana.m4a',
        'kibouchi_audio_filename': 'Moikadjana.m4a',
        'category': 'expressions',
        'difficulty': 2,
        'audio_category': 'expressions',
        'dual_audio_system': True,
        'has_shimaore_audio': True,
        'has_kibouchi_audio': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'audio_source': 'authentic',
        'audio_updated_at': datetime.utcnow()
    }
]

# Vérifier l'état initial
count_before = db['words'].count_documents({'category': 'expressions'})
print(f"📊 Expressions avant ajout: {count_before}")
print()

# Ajouter chaque expression avec vérification
successful_adds = 0
failed_adds = 0
already_exists = 0

for expr in nouvelles_expressions:
    print(f"{'='*80}")
    print(f"Traitement: {expr['french']}")
    print(f"{'='*80}")
    
    # Vérifier si existe déjà
    existing = db['words'].find_one({
        'french': expr['french'],
        'category': 'expressions'
    })
    
    if existing:
        print(f"⚠️  Expression déjà existante:")
        print(f"   Shimaoré: {existing.get('shimaore')}")
        print(f"   Kibouchi: {existing.get('kibouchi')}")
        already_exists += 1
        continue
    
    # Vérifier que les fichiers audio existent
    audio_dir = '/app/frontend/assets/audio/expressions'
    shimaore_file = os.path.join(audio_dir, expr['shimaore_audio_filename'])
    kibouchi_file = os.path.join(audio_dir, expr['kibouchi_audio_filename'])
    
    shimaore_exists = os.path.exists(shimaore_file)
    kibouchi_exists = os.path.exists(kibouchi_file)
    
    print(f"Vérification des fichiers audio:")
    print(f"   Shimaoré ({expr['shimaore_audio_filename']}): {'✅' if shimaore_exists else '❌'}")
    print(f"   Kibouchi ({expr['kibouchi_audio_filename']}): {'✅' if kibouchi_exists else '❌'}")
    
    if not shimaore_exists or not kibouchi_exists:
        print(f"❌ ERREUR: Fichiers audio manquants!")
        failed_adds += 1
        continue
    
    # Insérer dans la base
    try:
        result = db['words'].insert_one(expr)
        
        if result.inserted_id:
            print(f"\n✅ AJOUT RÉUSSI:")
            print(f"   ID: {result.inserted_id}")
            print(f"   Français: {expr['french']}")
            print(f"   Shimaoré: {expr['shimaore']}")
            print(f"   Kibouchi: {expr['kibouchi']}")
            print(f"   Audio shimaoré: {expr['shimaore_audio_filename']}")
            print(f"   Audio kibouchi: {expr['kibouchi_audio_filename']}")
            successful_adds += 1
        else:
            print(f"❌ Échec de l'insertion")
            failed_adds += 1
            
    except Exception as e:
        print(f"❌ ERREUR lors de l'insertion: {str(e)}")
        failed_adds += 1
    
    print()

# Vérifier l'état final
count_after = db['words'].count_documents({'category': 'expressions'})

print(f"{'='*80}")
print("RÉSUMÉ")
print(f"{'='*80}")
print(f"✅ Ajouts réussis: {successful_adds}")
print(f"⚠️  Déjà existantes: {already_exists}")
print(f"❌ Échecs: {failed_adds}")
print(f"📊 Total traité: {len(nouvelles_expressions)}")
print()
print(f"📊 Expressions AVANT: {count_before}")
print(f"📊 Expressions APRÈS: {count_after}")
print(f"📊 Différence: +{count_after - count_before}")

# Vérifier que toutes les expressions sont maintenant en base
print(f"\n{'='*80}")
print("VÉRIFICATION FINALE")
print(f"{'='*80}")

all_ok = True
for expr in nouvelles_expressions:
    word = db['words'].find_one({
        'french': expr['french'],
        'category': 'expressions'
    })
    
    if word:
        print(f"✅ {expr['french']}: {word.get('shimaore')} / {word.get('kibouchi')}")
    else:
        print(f"❌ {expr['french']}: NON TROUVÉ")
        all_ok = False

print(f"\n{'='*80}")
if all_ok and successful_adds == len(nouvelles_expressions):
    print("🎉 TOUTES LES EXPRESSIONS ONT ÉTÉ AJOUTÉES AVEC SUCCÈS !")
elif already_exists > 0 and (successful_adds + already_exists) == len(nouvelles_expressions):
    print("✅ TOUTES LES EXPRESSIONS SONT PRÉSENTES (certaines existaient déjà)")
else:
    print("⚠️  PROBLÈME: Toutes les expressions n'ont pas été ajoutées correctement")

print(f"{'='*80}")

client.close()
