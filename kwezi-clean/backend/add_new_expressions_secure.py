#!/usr/bin/env python3
"""
Script sécurisé pour ajouter 3 nouvelles expressions à la section expressions
avec leurs fichiers audio authentiques
"""

from pymongo import MongoClient
import os
import shutil
from datetime import datetime

# Connexion MongoDB
mongo_url = "mongodb://localhost:27017/"
client = MongoClient(mongo_url)
db = client['mayotte_app']
words_collection = db['words']

# Répertoire des audios
AUDIO_SOURCE_DIR = "/tmp"
AUDIO_DEST_DIR = "/app/frontend/assets/audio/expressions"

# Nouvelles expressions avec données exactes
NEW_EXPRESSIONS = [
    {
        'french': 'Le marché',
        'shimaore': 'bazari',
        'kibouchi': 'bazari',
        'category': 'expressions',
        'difficulty': 1,
        'image_url': '🏪',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Bazari.m4a',
        'audio_filename_kibouchi': 'Bazari.m4a',  # Même fichier pour les deux langues
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Commerce',
        'shimaore': 'douka',
        'kibouchi': 'douka',
        'category': 'expressions',
        'difficulty': 1,
        'image_url': '🏬',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Douka.m4a',
        'audio_filename_kibouchi': 'Douka.m4a',  # Même fichier pour les deux langues
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Édentée',
        'shimaore': 'drongna',
        'kibouchi': 'drongna',
        'category': 'expressions',
        'difficulty': 2,
        'image_url': '😬',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Drongna s.m4a',
        'audio_filename_kibouchi': 'Drongna k.m4a',
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    }
]

# Fichiers audio à copier (unique)
AUDIO_FILES = [
    'Bazari.m4a',
    'Douka.m4a',
    'Drongna s.m4a',
    'Drongna k.m4a'
]

def main():
    print("=" * 80)
    print("🔄 AJOUT SÉCURISÉ DE 3 NOUVELLES EXPRESSIONS")
    print("=" * 80)
    
    errors = []
    
    # ÉTAPE 1: Vérifier que les fichiers audio existent
    print("\n📂 ÉTAPE 1: Vérification des fichiers audio...")
    for audio_file in AUDIO_FILES:
        source_path = os.path.join(AUDIO_SOURCE_DIR, audio_file)
        if os.path.exists(source_path):
            size = os.path.getsize(source_path) / 1024
            print(f"   ✅ {audio_file} ({size:.1f} KB)")
        else:
            error_msg = f"❌ Fichier manquant: {audio_file}"
            print(f"   {error_msg}")
            errors.append(error_msg)
    
    if errors:
        print(f"\n❌ ERREUR: {len(errors)} fichier(s) audio manquant(s)")
        return
    
    # ÉTAPE 2: Créer le répertoire de destination si nécessaire
    print(f"\n📁 ÉTAPE 2: Vérification du répertoire de destination...")
    os.makedirs(AUDIO_DEST_DIR, exist_ok=True)
    print(f"   ✅ Répertoire: {AUDIO_DEST_DIR}")
    
    # ÉTAPE 3: Vérifier les doublons
    print(f"\n🔍 ÉTAPE 3: Vérification des doublons...")
    for exp in NEW_EXPRESSIONS:
        existing = words_collection.find_one({
            'french': exp['french'],
            'category': 'expressions'
        })
        if existing:
            error_msg = f"❌ Expression '{exp['french']}' existe déjà (ID: {existing['_id']})"
            print(f"   {error_msg}")
            errors.append(error_msg)
        else:
            print(f"   ✅ '{exp['french']}' - Nouveau")
    
    if errors:
        print(f"\n❌ ERREUR: Doublons détectés. Arrêt du script.")
        return
    
    # ÉTAPE 4: Copier les fichiers audio
    print(f"\n📋 ÉTAPE 4: Copie des fichiers audio...")
    for audio_file in AUDIO_FILES:
        source_path = os.path.join(AUDIO_SOURCE_DIR, audio_file)
        dest_path = os.path.join(AUDIO_DEST_DIR, audio_file)
        
        try:
            shutil.copy2(source_path, dest_path)
            print(f"   ✅ Copié: {audio_file}")
        except Exception as e:
            error_msg = f"❌ Erreur copie {audio_file}: {str(e)}"
            print(f"   {error_msg}")
            errors.append(error_msg)
    
    if errors:
        print(f"\n❌ ERREUR lors de la copie des fichiers")
        return
    
    # ÉTAPE 5: Insérer les expressions dans MongoDB
    print(f"\n💾 ÉTAPE 5: Insertion dans MongoDB...")
    inserted_ids = []
    
    for exp in NEW_EXPRESSIONS:
        try:
            result = words_collection.insert_one(exp)
            inserted_ids.append(result.inserted_id)
            print(f"   ✅ '{exp['french']}' ajouté (ID: {result.inserted_id})")
        except Exception as e:
            error_msg = f"❌ Erreur insertion '{exp['french']}': {str(e)}"
            print(f"   {error_msg}")
            errors.append(error_msg)
    
    if errors:
        print(f"\n❌ ERREUR lors de l'insertion en base")
        return
    
    # ÉTAPE 6: Vérification finale
    print(f"\n✅ ÉTAPE 6: Vérification finale...")
    
    for exp_id in inserted_ids:
        word = words_collection.find_one({'_id': exp_id})
        if word:
            print(f"   ✅ {word['french']}")
            print(f"      - Shimaoré: {word['shimaore']} → {word['audio_filename_shimaore']}")
            print(f"      - Kibouchi: {word['kibouchi']} → {word['audio_filename_kibouchi']}")
            
            # Vérifier fichiers physiques
            shimaore_path = os.path.join(AUDIO_DEST_DIR, word['audio_filename_shimaore'])
            kibouchi_path = os.path.join(AUDIO_DEST_DIR, word['audio_filename_kibouchi'])
            
            if os.path.exists(shimaore_path) and os.path.exists(kibouchi_path):
                print(f"      - Fichiers audio: ✅ Présents")
            else:
                error_msg = f"❌ Fichiers audio manquants pour {word['french']}"
                print(f"      - {error_msg}")
                errors.append(error_msg)
    
    # Total expressions
    total_expressions = words_collection.count_documents({'category': 'expressions'})
    print(f"\n📊 Total expressions dans la base: {total_expressions}")
    
    # Résultat final
    print("\n" + "=" * 80)
    if errors:
        print("❌ SCRIPT TERMINÉ AVEC ERREURS")
        print("=" * 80)
        for error in errors:
            print(f"   • {error}")
    else:
        print("✅ AUCUNE ERREUR - Tout s'est bien passé!")
        print("=" * 80)
        print(f"✅ 3 nouvelles expressions ajoutées")
        print(f"✅ 4 fichiers audio copiés")
        print(f"✅ Total expressions: {total_expressions}")

if __name__ == "__main__":
    main()
