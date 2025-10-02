#!/usr/bin/env python3
"""
Script pour mettre à jour les audio des catégories FAMILLE, NOMBRES et ANIMAUX
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

# Configuration des ZIP à traiter
CATEGORIES_CONFIG = {
    'famille': {
        'zip_url': 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/srue4z02_Famille%27-20251002T110012Z-1-001.zip',
        'extract_path': '/tmp/famille_audio/',
        'target_dir': '/app/frontend/assets/audio/famille/'
    },
    'nombres': {
        'zip_url': 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/2g6wajga_Nombres%27-20251002T110234Z-1-001.zip',
        'extract_path': '/tmp/nombres_audio/',
        'target_dir': '/app/frontend/assets/audio/nombres/'
    },
    'animaux': {
        'zip_url': 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/cfml94rf_Animaux%27-20251002T110307Z-1-001.zip',
        'extract_path': '/tmp/animaux_audio/',
        'target_dir': '/app/frontend/assets/audio/animaux/'
    }
}

def normalize_name(name):
    """Normalise un nom pour la correspondance"""
    name = name.lower()
    # Enlever les extensions
    name = re.sub(r'\.(mp3|m4a|wav|ogg)$', '', name, flags=re.IGNORECASE)
    # Enlever les underscores, tirets et espaces
    name = name.replace('_', ' ').replace('-', ' ')
    # Enlever les caractères spéciaux sauf lettres et chiffres
    name = re.sub(r'[^\w\s]', '', name)
    # Réduire les espaces multiples
    name = ' '.join(name.split())
    return name

def find_audio_match(word_french, word_shimaore, word_kibouchi, audio_map):
    """Trouve le fichier audio correspondant"""
    search_terms = [
        normalize_name(word_french),
        normalize_name(word_shimaore) if word_shimaore else "",
        normalize_name(word_kibouchi) if word_kibouchi else ""
    ]
    
    for term in search_terms:
        if not term:
            continue
            
        if term in audio_map:
            return audio_map[term]
        
        # Recherche partielle
        for audio_key, audio_data in audio_map.items():
            if term in audio_key or audio_key in term:
                return audio_data
    
    return None

def process_category(category_name, config):
    """Traite une catégorie complète"""
    print(f"\n{'='*70}")
    print(f"📂 TRAITEMENT DE LA CATÉGORIE: {category_name.upper()}")
    print(f"{'='*70}")
    
    # Télécharger et extraire le ZIP
    print(f"📥 Téléchargement du ZIP...")
    zip_path = f"/tmp/{category_name}_audio.zip"
    extract_path = config['extract_path']
    
    urllib.request.urlretrieve(config['zip_url'], zip_path)
    
    print(f"📦 Extraction des fichiers...")
    os.makedirs(extract_path, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    # Lister tous les fichiers audio extraits
    print(f"\n📂 Fichiers extraits:")
    audio_files = []
    for root, dirs, files in os.walk(extract_path):
        for file in files:
            if file.lower().endswith(('.mp3', '.m4a', '.wav', '.ogg')):
                full_path = os.path.join(root, file)
                audio_files.append({
                    'filename': file,
                    'full_path': full_path,
                    'relative_path': file
                })
                print(f"  ✓ {file}")
    
    print(f"\n📊 Total: {len(audio_files)} fichiers audio trouvés")
    
    # Créer un mapping des fichiers audio
    audio_map = {}
    for audio in audio_files:
        normalized = normalize_name(audio['filename'])
        audio_map[normalized] = audio
    
    # Récupérer tous les mots de la catégorie
    words = list(words_collection.find({"category": category_name}))
    print(f"\n📚 {len(words)} mots dans la catégorie '{category_name}'")
    
    # Mettre à jour les mots
    print(f"\n🔄 Mise à jour de la base de données:")
    updated_count = 0
    not_found = []
    
    for word in words:
        french = word.get('french', '')
        shimaore = word.get('shimaore', '')
        kibouchi = word.get('kibouchi', '')
        
        # Chercher le fichier audio correspondant
        audio_match = find_audio_match(french, shimaore, kibouchi, audio_map)
        
        if audio_match:
            # Construire le chemin pour les assets
            audio_path = f"{category_name}/{audio_match['relative_path']}"
            
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
    
    # Copier les fichiers audio dans le bon dossier
    print(f"\n📁 Copie des fichiers audio...")
    target_dir = config['target_dir']
    os.makedirs(target_dir, exist_ok=True)
    
    for audio in audio_files:
        target_path = os.path.join(target_dir, audio['filename'])
        shutil.copy2(audio['full_path'], target_path)
        print(f"  ✓ {audio['filename']}")
    
    print(f"\n📊 RÉSULTATS POUR {category_name.upper()}:")
    print(f"  ✅ Mis à jour: {updated_count}")
    print(f"  ❌ Non trouvés: {len(not_found)}")
    
    if not_found:
        print(f"\n⚠️  Mots sans correspondance:")
        for word in not_found:
            print(f"    - {word}")
    
    return updated_count, not_found

# Traiter toutes les catégories
print(f"\n🚀 DÉBUT DU TRAITEMENT DE 3 CATÉGORIES")
print(f"{'='*70}\n")

total_updated = 0
all_not_found = {}

for category_name, config in CATEGORIES_CONFIG.items():
    updated, not_found = process_category(category_name, config)
    total_updated += updated
    if not_found:
        all_not_found[category_name] = not_found

# Résumé final
print(f"\n\n{'='*70}")
print(f"🎉 RÉSUMÉ FINAL")
print(f"{'='*70}")
print(f"\n📊 Total mots mis à jour: {total_updated}")

if all_not_found:
    print(f"\n⚠️  Mots non trouvés par catégorie:")
    for cat, words in all_not_found.items():
        print(f"\n  {cat.upper()} ({len(words)} mots):")
        for word in words:
            print(f"    - {word}")
else:
    print(f"\n✅ TOUS les mots ont été mis à jour avec succès!")

# Vérification finale
print(f"\n📈 STATUT FINAL PAR CATÉGORIE:")
for category_name in CATEGORIES_CONFIG.keys():
    total = words_collection.count_documents({'category': category_name})
    with_audio_sh = words_collection.count_documents({'category': category_name, 'shimoare_has_audio': True})
    with_audio_kb = words_collection.count_documents({'category': category_name, 'kibouchi_has_audio': True})
    
    print(f"\n  {category_name.upper()}:")
    print(f"    Total: {total}")
    print(f"    Avec audio Shimaoré: {with_audio_sh} ({int(with_audio_sh/total*100)}%)")
    print(f"    Avec audio Kibouchi: {with_audio_kb} ({int(with_audio_kb/total*100)}%)")

client.close()
print(f"\n✅ Traitement terminé!")
