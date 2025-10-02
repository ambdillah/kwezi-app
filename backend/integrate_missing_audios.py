#!/usr/bin/env python3
"""
Script pour intégrer les 11 audios manquants depuis le ZIP
"""

import zipfile
import urllib.request
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import re
import shutil

load_dotenv()

# Connexion MongoDB
MONGO_URL = os.getenv('MONGO_URL')
DB_NAME = os.getenv('DB_NAME', 'mayotte_app')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
words_collection = db.words

# Liste des 11 mots nécessitant audio
mots_necessitant_audio = [
    'Vedettes', 'Ciboulette', 'terre', 'manguier', 'jacquier',
    'cocotier', 'baobab', 'bananier', 'Léger', 'Inutile', 'Honteux'
]

print("📥 Téléchargement du ZIP...")
zip_url = "https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/m2xnqjpx_drive-download%27.zip"
zip_path = "/tmp/audios_manquants.zip"
extract_path = "/tmp/audios_manquants/"

urllib.request.urlretrieve(zip_url, zip_path)

print("📦 Extraction des fichiers...")
os.makedirs(extract_path, exist_ok=True)
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Lister tous les fichiers audio extraits
print("\n📂 Fichiers extraits:")
audio_files = []
for root, dirs, files in os.walk(extract_path):
    for file in files:
        if file.lower().endswith(('.mp3', '.m4a', '.wav', '.ogg')):
            full_path = os.path.join(root, file)
            audio_files.append({
                'filename': file,
                'full_path': full_path
            })
            print(f"  ✓ {file}")

print(f"\n📊 Total: {len(audio_files)} fichiers audio trouvés")

# Fonction de normalisation
def normalize_name(name):
    name = name.lower()
    name = re.sub(r'\.(mp3|m4a|wav|ogg)$', '', name, flags=re.IGNORECASE)
    name = name.replace('_', ' ').replace('-', ' ')
    name = re.sub(r'[^\w\s]', '', name)
    name = ' '.join(name.split())
    return name

# Créer un mapping
audio_map = {}
for audio in audio_files:
    normalized = normalize_name(audio['filename'])
    audio_map[normalized] = audio

print("\n🔄 Mapping des fichiers audio:")
for key in sorted(audio_map.keys()):
    print(f"  {key} → {audio_map[key]['filename']}")

# Déterminer la catégorie pour chaque mot
print("\n🗂️  Catégories des mots:")
categories_map = {}
for french in mots_necessitant_audio:
    word = words_collection.find_one({'french': french})
    if word:
        category = word.get('category', 'unknown')
        categories_map[french] = category
        print(f"  {french} → {category}")

# Mapping manuel intelligent
print("\n🔗 Mapping des audios aux mots:")
updated_count = 0
not_matched = []

for french in mots_necessitant_audio:
    word = words_collection.find_one({'french': french})
    
    if not word:
        print(f"  ❌ {french}: mot non trouvé")
        not_matched.append(french)
        continue
    
    shimaore = word.get('shimaore', '')
    kibouchi = word.get('kibouchi', '')
    category = categories_map.get(french, 'unknown')
    
    # Chercher le fichier audio correspondant
    search_terms = [
        normalize_name(french),
        normalize_name(shimaore),
        normalize_name(kibouchi)
    ]
    
    matched_audio = None
    for term in search_terms:
        if not term:
            continue
        if term in audio_map:
            matched_audio = audio_map[term]
            break
        # Recherche partielle
        for audio_key, audio_data in audio_map.items():
            if term in audio_key or audio_key in term:
                matched_audio = audio_data
                break
        if matched_audio:
            break
    
    if matched_audio:
        # Copier le fichier dans le bon dossier
        target_dir = f"/app/frontend/assets/audio/{category}/"
        os.makedirs(target_dir, exist_ok=True)
        
        target_filename = matched_audio['filename']
        target_path = os.path.join(target_dir, target_filename)
        shutil.copy2(matched_audio['full_path'], target_path)
        
        # Mettre à jour la base
        audio_path = f"{category}/{target_filename}"
        result = words_collection.update_one(
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
        
        if result.modified_count > 0:
            print(f"  ✅ {french} → {target_filename} (catégorie: {category})")
            updated_count += 1
        else:
            print(f"  ⚠️  {french}: échec mise à jour BD")
    else:
        print(f"  ❌ {french}: aucun audio trouvé")
        not_matched.append(french)

print(f"\n📊 RÉSULTATS:")
print(f"  ✅ Audios intégrés: {updated_count}")
print(f"  ❌ Non trouvés: {len(not_matched)}")

if not_matched:
    print(f"\n⚠️  Mots sans audio:")
    for m in not_matched:
        print(f"    - {m}")

client.close()
print("\n✅ Intégration terminée!")
