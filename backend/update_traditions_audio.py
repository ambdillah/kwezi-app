#!/usr/bin/env python3
"""
Script pour mettre à jour les audio de la catégorie TRADITIONS
"""

import zipfile
import urllib.request
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import re

load_dotenv()

# Connexion MongoDB
MONGO_URL = os.getenv('MONGO_URL')
DB_NAME = os.getenv('DB_NAME', 'mayotte_app')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
words_collection = db.words

# Télécharger et extraire le ZIP
print("📥 Téléchargement du ZIP...")
zip_url = "https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/h8ii37ll_traditions%27-20251002T054935Z-1-001.zip"
zip_path = "/tmp/traditions_audio.zip"
extract_path = "/tmp/traditions_audio/"

urllib.request.urlretrieve(zip_url, zip_path)

print("📦 Extraction des fichiers...")
os.makedirs(extract_path, exist_ok=True)
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Lister tous les fichiers extraits
print("\n📂 Fichiers extraits:")
audio_files = []
for root, dirs, files in os.walk(extract_path):
    for file in files:
        if file.lower().endswith(('.mp3', '.m4a', '.wav', '.ogg')):
            full_path = os.path.join(root, file)
            # Créer le chemin relatif depuis assets/audio/traditions/
            relative_path = file
            audio_files.append({
                'filename': file,
                'full_path': full_path,
                'relative_path': relative_path
            })
            print(f"  ✓ {file}")

print(f"\n📊 Total: {len(audio_files)} fichiers audio trouvés")

# Récupérer tous les mots de la catégorie "traditions"
traditions_words = list(words_collection.find({"category": "traditions"}))
print(f"\n📚 {len(traditions_words)} mots dans la catégorie 'traditions'")

# Fonction pour nettoyer et normaliser les noms
def normalize_name(name):
    """Normalise un nom pour la correspondance"""
    name = name.lower()
    # Enlever les extensions
    name = re.sub(r'\.(mp3|m4a|wav|ogg)$', '', name, flags=re.IGNORECASE)
    # Enlever les underscores et espaces
    name = name.replace('_', ' ').replace('-', ' ')
    # Enlever les caractères spéciaux
    name = re.sub(r'[^\w\s]', '', name)
    # Réduire les espaces multiples
    name = ' '.join(name.split())
    return name

# Créer un mapping des fichiers audio
audio_map = {}
for audio in audio_files:
    normalized = normalize_name(audio['filename'])
    audio_map[normalized] = audio

print("\n🔍 Mapping des fichiers:")
for key in sorted(audio_map.keys()):
    print(f"  {key} → {audio_map[key]['filename']}")

# Fonction pour trouver le meilleur match
def find_audio_match(word_french, word_shimaore, word_kibouchi):
    """Trouve le fichier audio correspondant"""
    search_terms = [
        normalize_name(word_french),
        normalize_name(word_shimaore) if word_shimaore else "",
        normalize_name(word_kibouchi) if word_kibouchi else ""
    ]
    
    for term in search_terms:
        if term in audio_map:
            return audio_map[term]
        
        # Recherche partielle
        for audio_key, audio_data in audio_map.items():
            if term in audio_key or audio_key in term:
                return audio_data
    
    return None

# Mettre à jour les mots avec les nouveaux chemins audio
print("\n🔄 Mise à jour de la base de données:")
updated_count = 0
not_found = []

for word in traditions_words:
    french = word.get('french', '')
    shimaore = word.get('shimaore', '')
    kibouchi = word.get('kibouchi', '')
    
    # Chercher le fichier audio correspondant
    audio_match = find_audio_match(french, shimaore, kibouchi)
    
    if audio_match:
        # Construire le chemin pour les assets
        audio_path = f"traditions/{audio_match['relative_path']}"
        
        # Mettre à jour dans la base
        words_collection.update_one(
            {'_id': word['_id']},
            {
                '$set': {
                    'audio_shimaore': audio_path,
                    'audio_kibouchi': audio_path,
                    'shimoare_has_audio': True,
                    'kibouchi_has_audio': True
                }
            }
        )
        updated_count += 1
        print(f"  ✅ {french} → {audio_match['filename']}")
    else:
        not_found.append(french)
        print(f"  ❌ {french} - AUCUN FICHIER TROUVÉ")

print(f"\n📊 RÉSULTATS:")
print(f"  ✅ Mis à jour: {updated_count}")
print(f"  ❌ Non trouvés: {len(not_found)}")

if not_found:
    print(f"\n⚠️  Mots sans correspondance:")
    for word in not_found:
        print(f"    - {word}")

# Copier les fichiers audio dans le bon dossier
print(f"\n📁 Copie des fichiers audio...")
target_dir = "/app/frontend/assets/audio/traditions/"
os.makedirs(target_dir, exist_ok=True)

import shutil
for audio in audio_files:
    target_path = os.path.join(target_dir, audio['filename'])
    shutil.copy2(audio['full_path'], target_path)
    print(f"  ✓ {audio['filename']}")

print(f"\n✅ Tous les fichiers copiés dans {target_dir}")

client.close()
print("\n🎉 Mise à jour terminée!")
