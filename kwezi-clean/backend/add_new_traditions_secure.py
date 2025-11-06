#!/usr/bin/env python3
"""
Script sécurisé pour ajouter 8 nouvelles traditions à la section tradition
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

# Répertoires des audios
AUDIO_SOURCE_DIR = "/tmp"
AUDIO_DEST_DIR = "/app/frontend/assets/audio/tradition"

# Nouvelles traditions avec données exactes et correspondances audio
NEW_TRADITIONS = [
    {
        'french': 'Dieu',
        'shimaore': 'moungou',
        'kibouchi': 'dragnahari',
        'category': 'tradition',
        'difficulty': 1,
        'image_url': '🙏',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Moungou.m4a',
        'audio_filename_kibouchi': 'Dragnahari.m4a',
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Faire la prière',
        'shimaore': 'ousoili',
        'kibouchi': 'mikousoili',
        'category': 'tradition',
        'difficulty': 1,
        'image_url': '🕌',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Ousoili.m4a',
        'audio_filename_kibouchi': 'Mikousoili.m4a',
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Tambour',
        'shimaore': 'ngoma',
        'kibouchi': 'azoulahi',
        'category': 'tradition',
        'difficulty': 1,
        'image_url': '🥁',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Ngoma.m4a',
        'audio_filename_kibouchi': 'Azoulahi.m4a',
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Tambourin',
        'shimaore': 'tari',
        'kibouchi': 'tari',
        'category': 'tradition',
        'difficulty': 1,
        'image_url': '🪘',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Tari s.m4a',
        'audio_filename_kibouchi': 'Tari k.m4a',
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Ballon',
        'shimaore': 'boulou',
        'kibouchi': 'boulou',
        'category': 'tradition',
        'difficulty': 1,
        'image_url': '⚽',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Boulou.m4a',
        'audio_filename_kibouchi': 'Boulou.m4a',  # Même fichier
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Ligne de pêche',
        'shimaore': 'missi',
        'kibouchi': 'mouchipi',
        'category': 'tradition',
        'difficulty': 2,
        'image_url': '🎣',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Missi.m4a',
        'audio_filename_kibouchi': 'Mouchipi.m4a',
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Filet de pêche',
        'shimaore': 'wavou/chamiya',
        'kibouchi': 'wavou/chamiya',
        'category': 'tradition',
        'difficulty': 2,
        'image_url': '🪝',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Wavou_chamiya.m4a',
        'audio_filename_kibouchi': 'Wavou_chamiya.m4a',  # Même fichier
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Voile de pêche',
        'shimaore': 'djarifa',
        'kibouchi': 'djarifa',
        'category': 'tradition',
        'difficulty': 2,
        'image_url': '⛵',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Djarifa.m4a',
        'audio_filename_kibouchi': 'Djarifa.m4a',  # Même fichier
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    }
]

# Fichiers audio à copier (unique) - 13 fichiers
AUDIO_FILES = [
    'Moungou.m4a',
    'Dragnahari.m4a',
    'Ousoili.m4a',
    'Mikousoili.m4a',
    'Ngoma.m4a',
    'Azoulahi.m4a',
    'Tari s.m4a',
    'Tari k.m4a',
    'Boulou.m4a',
    'Missi.m4a',
    'Mouchipi.m4a',
    'Wavou_chamiya.m4a',
    'Djarifa.m4a'
]

def main():
    print("=" * 80)
    print("🔄 AJOUT SÉCURISÉ DE 8 NOUVELLES TRADITIONS")
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
    for trad in NEW_TRADITIONS:
        existing = words_collection.find_one({
            'french': trad['french'],
            'category': 'tradition'
        })
        if existing:
            error_msg = f"❌ Tradition '{trad['french']}' existe déjà (ID: {existing['_id']})"
            print(f"   {error_msg}")
            errors.append(error_msg)
        else:
            print(f"   ✅ '{trad['french']}' - Nouveau")
    
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
    
    # ÉTAPE 5: Insérer les traditions dans MongoDB
    print(f"\n💾 ÉTAPE 5: Insertion dans MongoDB...")
    inserted_ids = []
    
    for trad in NEW_TRADITIONS:
        try:
            result = words_collection.insert_one(trad)
            inserted_ids.append(result.inserted_id)
            print(f"   ✅ '{trad['french']}' ajouté (ID: {result.inserted_id})")
        except Exception as e:
            error_msg = f"❌ Erreur insertion '{trad['french']}': {str(e)}"
            print(f"   {error_msg}")
            errors.append(error_msg)
    
    if errors:
        print(f"\n❌ ERREUR lors de l'insertion en base")
        return
    
    # ÉTAPE 6: Vérification finale
    print(f"\n✅ ÉTAPE 6: Vérification finale...")
    
    for trad_id in inserted_ids:
        word = words_collection.find_one({'_id': trad_id})
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
    
    # Total traditions
    total_traditions = words_collection.count_documents({'category': 'tradition'})
    print(f"\n📊 Total traditions dans la base: {total_traditions}")
    
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
        print(f"✅ 8 nouvelles traditions ajoutées")
        print(f"✅ 13 fichiers audio copiés")
        print(f"✅ Total traditions: {total_traditions}")

if __name__ == "__main__":
    main()
