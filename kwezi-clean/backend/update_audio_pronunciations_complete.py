#!/usr/bin/env python3
"""
Script pour mettre à jour les prononciations audio pour les sections:
- corps humain (corps)
- nombres
- animaux 
- salutations

Met à jour les références audio dans la base de données pour pointer vers les nouveaux fichiers.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging
import glob
import re

# Charger les variables d'environnement
load_dotenv()

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_database():
    """Connexion à la base de données MongoDB"""
    try:
        mongo_url = os.getenv('MONGO_URL')
        if not mongo_url:
            raise ValueError("MONGO_URL non trouvée dans les variables d'environnement")
        
        client = MongoClient(mongo_url)
        db = client['shimaoré_app']
        logger.info("Connexion à la base de données réussie")
        return db
    except Exception as e:
        logger.error(f"Erreur de connexion à la base de données: {e}")
        raise

def normalize_filename(filename):
    """Normalise le nom de fichier pour correspondance avec les mots de la base"""
    # Enlever l'extension
    name = os.path.splitext(filename)[0]
    
    # Convertir en minuscules
    name = name.lower()
    
    # Remplacer certains caractères spéciaux
    replacements = {
        '_': ' ',
        'é': 'e',
        'è': 'e',
        'à': 'a',
        'ç': 'c',
        'ù': 'u',
        'î': 'i',
        'ô': 'o',
        'ê': 'e',
        'ë': 'e',
        'â': 'a'
    }
    
    for old, new in replacements.items():
        name = name.replace(old, new)
    
    return name.strip()

def find_matching_words(db, section, audio_files):
    """Trouve les correspondances entre fichiers audio et mots de la base"""
    collection = db['vocabulary']
    words = list(collection.find({"section": section}))
    
    matches = {}
    unmatched_audio = []
    unmatched_words = []
    
    logger.info(f"\n=== SECTION {section.upper()} ===")
    logger.info(f"Mots dans la base: {len(words)}")
    logger.info(f"Fichiers audio disponibles: {len(audio_files)}")
    
    # Normaliser les noms des fichiers audio
    normalized_audio = {}
    for file in audio_files:
        normalized = normalize_filename(file)
        normalized_audio[normalized] = file
    
    # Pour chaque mot dans la base, chercher un fichier audio correspondant
    for word in words:
        french = word.get('french', '').lower()
        shimaore = word.get('shimaoré', '').lower()
        kibouchi = word.get('kibouchi', '').lower()
        
        # Essayer différentes correspondances
        candidates = [
            french,
            shimaore,
            kibouchi,
            french.replace(' ', '_').replace('-', '_'),
            shimaore.replace(' ', '_').replace('-', '_'),
            kibouchi.replace(' ', '_').replace('-', '_')
        ]
        
        matched = False
        for candidate in candidates:
            if candidate in normalized_audio:
                matches[word['_id']] = {
                    'word': word,
                    'audio_file': normalized_audio[candidate],
                    'match_type': candidate
                }
                matched = True
                logger.info(f"  ✅ {french} -> {normalized_audio[candidate]}")
                break
        
        if not matched:
            unmatched_words.append(word)
    
    # Fichiers audio non utilisés
    used_files = [match['audio_file'] for match in matches.values()]
    for file in audio_files:
        if file not in used_files:
            unmatched_audio.append(file)
    
    logger.info(f"Correspondances trouvées: {len(matches)}")
    logger.info(f"Mots sans audio: {len(unmatched_words)}")
    logger.info(f"Fichiers audio non utilisés: {len(unmatched_audio)}")
    
    if unmatched_words:
        logger.warning("Mots sans correspondance audio:")
        for word in unmatched_words[:5]:  # Afficher les 5 premiers
            logger.warning(f"  - {word.get('french')}: {word.get('shimaoré')} / {word.get('kibouchi')}")
    
    if unmatched_audio:
        logger.warning("Fichiers audio non utilisés:")
        for file in unmatched_audio[:5]:  # Afficher les 5 premiers
            logger.warning(f"  - {file}")
    
    return matches, unmatched_words, unmatched_audio

def update_audio_references(db, section, matches):
    """Met à jour les références audio dans la base de données"""
    collection = db['vocabulary']
    updated_count = 0
    
    for word_id, match_data in matches.items():
        audio_file = match_data['audio_file']
        word = match_data['word']
        
        # Créer le chemin relatif pour l'audio
        audio_path = f"audio/{section}/{audio_file}"
        
        # Mettre à jour le document
        result = collection.update_one(
            {"_id": word_id},
            {
                "$set": {
                    "audio_authentic": audio_path,
                    "has_authentic_audio": True,
                    "audio_updated": True
                }
            }
        )
        
        if result.modified_count > 0:
            updated_count += 1
    
    logger.info(f"Références audio mises à jour: {updated_count}")
    return updated_count

def process_section(db, section, audio_dir):
    """Traite une section complète"""
    try:
        # Lister les fichiers audio
        audio_files = []
        if os.path.exists(audio_dir):
            for ext in ['*.m4a', '*.mp3', '*.wav']:
                audio_files.extend([os.path.basename(f) for f in glob.glob(os.path.join(audio_dir, ext))])
        
        if not audio_files:
            logger.warning(f"Aucun fichier audio trouvé dans {audio_dir}")
            return False
        
        # Trouver les correspondances
        matches, unmatched_words, unmatched_audio = find_matching_words(db, section, audio_files)
        
        if not matches:
            logger.error(f"Aucune correspondance trouvée pour la section {section}")
            return False
        
        # Mettre à jour les références
        updated_count = update_audio_references(db, section, matches)
        
        logger.info(f"Section {section} traitée avec succès: {updated_count} mises à jour")
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement de la section {section}: {e}")
        return False

def main():
    """Fonction principale"""
    logger.info("Début de la mise à jour des prononciations audio")
    
    try:
        # Connexion à la base de données
        db = connect_to_database()
        
        # Configuration des sections à traiter
        sections_config = {
            "corps": "/app/frontend/assets/audio/corps",
            "nombres": "/app/frontend/assets/audio/nombres", 
            "animaux": "/app/frontend/assets/audio/animaux",
            "salutations": "/app/frontend/assets/audio/salutations"
        }
        
        # Traiter chaque section
        results = {}
        for section, audio_dir in sections_config.items():
            logger.info(f"\n{'='*50}")
            logger.info(f"TRAITEMENT SECTION: {section.upper()}")
            logger.info(f"{'='*50}")
            
            success = process_section(db, section, audio_dir)
            results[section] = success
        
        # Résumé final
        logger.info(f"\n{'='*50}")
        logger.info("RÉSUMÉ FINAL")
        logger.info(f"{'='*50}")
        
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        for section, success in results.items():
            status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
            logger.info(f"{section.upper()}: {status}")
        
        logger.info(f"\nSections traitées avec succès: {success_count}/{total_count}")
        
        if success_count == total_count:
            logger.info("🎉 Toutes les prononciations audio ont été mises à jour avec succès!")
        else:
            logger.warning("⚠️ Certaines sections n'ont pas pu être mises à jour")
        
    except Exception as e:
        logger.error(f"Erreur dans le script principal: {e}")
        return 1
    
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    exit(main())