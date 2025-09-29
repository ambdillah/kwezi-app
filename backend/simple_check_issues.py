#!/usr/bin/env python3
"""
Vérification simple des problèmes mentionnés par l'utilisateur
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_database():
    """Connexion à la base de données MongoDB"""
    try:
        mongo_url = os.getenv('MONGO_URL')
        client = MongoClient(mongo_url)
        db = client['shimaoré_app']
        logger.info("Connexion à la base de données réussie")
        return db
    except Exception as e:
        logger.error(f"Erreur de connexion à la base de données: {e}")
        raise

def check_specific_problems():
    """Vérifie les problèmes spécifiques mentionnés"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("=== VÉRIFICATION PROBLÈMES SPÉCIFIQUES ===")
    
    # 1. Problème "oulindra" vs "mandigni"
    logger.info("\n🔍 PROBLÈME 1: 'oulindra' - même audio que 'mandigni'")
    
    attendre_verb = collection.find_one({
        "section": "verbes",
        "french": "attendre"
    })
    
    if attendre_verb:
        logger.info(f"Verbe 'attendre' trouvé:")
        logger.info(f"  Français: {attendre_verb.get('french', 'N/A')}")
        logger.info(f"  Shimaoré: {attendre_verb.get('shimaoré', 'N/A')}")
        logger.info(f"  Kibouchi: {attendre_verb.get('kibouchi', 'N/A')}")
        logger.info(f"  Audio shimaoré: {attendre_verb.get('audio_shimaoré_filename', 'Aucun')}")
        logger.info(f"  Audio kibouchi: {attendre_verb.get('audio_kibouchi_filename', 'Aucun')}")
        
        # Vérifier si le même fichier est utilisé
        shimaore_audio = attendre_verb.get('audio_shimaoré_filename')
        kibouchi_audio = attendre_verb.get('audio_kibouchi_filename')
        
        if shimaore_audio == kibouchi_audio and shimaore_audio:
            logger.info(f"  ❌ PROBLÈME CONFIRMÉ: Même fichier {shimaore_audio} pour shimaoré et kibouchi")
        else:
            logger.info(f"  ✅ Pas de problème de duplication")
    
    # 2. Problème "ouziya" manquant
    logger.info("\n🔍 PROBLÈME 2: 'ouziya' - audio manquant")
    
    arreter_verb = collection.find_one({
        "section": "verbes",
        "french": "arrêter"
    })
    
    if arreter_verb:
        logger.info(f"Verbe 'arrêter' trouvé:")
        logger.info(f"  Français: {arreter_verb.get('french', 'N/A')}")
        logger.info(f"  Shimaoré: {arreter_verb.get('shimaoré', 'N/A')}")
        logger.info(f"  Kibouchi: {arreter_verb.get('kibouchi', 'N/A')}")
        logger.info(f"  Audio shimaoré: {arreter_verb.get('audio_shimaoré_filename', 'Aucun')}")
        logger.info(f"  Audio kibouchi: {arreter_verb.get('audio_kibouchi_filename', 'Aucun')}")
        
        shimaore_audio = arreter_verb.get('audio_shimaoré_filename')
        if not shimaore_audio or shimaore_audio == 'Aucun':
            logger.info(f"  ❌ PROBLÈME CONFIRMÉ: Pas d'audio pour 'ouziya'")
        else:
            logger.info(f"  ✅ Audio disponible: {shimaore_audio}")

def check_available_files():
    """Vérifie les fichiers disponibles"""
    audio_dir = "/app/frontend/assets/audio/verbes"
    
    logger.info(f"\n=== FICHIERS AUDIO DISPONIBLES ===")
    
    if not os.path.exists(audio_dir):
        logger.error(f"Répertoire audio non trouvé: {audio_dir}")
        return
    
    # Chercher spécifiquement les fichiers mentionnés
    files_found = []
    
    for filename in os.listdir(audio_dir):
        if filename.lower().endswith(('.m4a', '.mp3', '.wav')):
            name_lower = filename.lower()
            
            if 'oulindra' in name_lower:
                files_found.append(f"📁 {filename} - pour 'oulindra'")
            if 'mandigni' in name_lower:
                files_found.append(f"📁 {filename} - pour 'mandigni'")
            if 'ouziya' in name_lower or 'ouzia' in name_lower:
                files_found.append(f"📁 {filename} - pour 'ouziya'")
    
    if files_found:
        logger.info("Fichiers pertinents trouvés:")
        for file_info in files_found:
            logger.info(f"  {file_info}")
    else:
        logger.info("Aucun fichier spécifique trouvé")

def find_duplicate_audio_usage():
    """Trouve les fichiers audio utilisés plusieurs fois"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info(f"\n=== RECHERCHE DOUBLONS AUDIO ===")
    
    verbs = list(collection.find({"section": "verbes"}))
    
    audio_usage = {}
    
    for verb in verbs:
        french = verb.get('french', 'N/A')
        shimaore_audio = verb.get('audio_shimaoré_filename')
        kibouchi_audio = verb.get('audio_kibouchi_filename')
        
        if shimaore_audio and shimaore_audio != 'Aucun':
            if shimaore_audio not in audio_usage:
                audio_usage[shimaore_audio] = []
            audio_usage[shimaore_audio].append(f"{french} (shimaoré)")
        
        if kibouchi_audio and kibouchi_audio != 'Aucun':
            if kibouchi_audio not in audio_usage:
                audio_usage[kibouchi_audio] = []
            audio_usage[kibouchi_audio].append(f"{french} (kibouchi)")
    
    # Afficher les doublons
    duplicates_found = False
    for audio_file, usages in audio_usage.items():
        if len(usages) > 1:
            duplicates_found = True
            logger.info(f"\n🚨 FICHIER DUPLIQUÉ: {audio_file}")
            for usage in usages:
                logger.info(f"     - {usage}")
    
    if not duplicates_found:
        logger.info("✅ Aucun fichier audio dupliqué trouvé")

def main():
    """Fonction principale"""
    logger.info("🔍 VÉRIFICATION SIMPLE DES PROBLÈMES AUDIO")
    
    try:
        check_specific_problems()
        check_available_files()
        find_duplicate_audio_usage()
        
        logger.info(f"\n✅ ANALYSE TERMINÉE")
        
    except Exception as e:
        logger.error(f"Erreur dans l'analyse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()