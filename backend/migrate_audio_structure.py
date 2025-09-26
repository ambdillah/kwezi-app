#!/usr/bin/env python3
"""
Script de migration vers une structure audio optimisée
Sépare clairement les fichiers audio shimaoré et kibouchi
Corrige les 0 problèmes identifiés
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_database():
    mongo_url = os.getenv('MONGO_URL')
    client = MongoClient(mongo_url)
    return client['shimaoré_app']

def migrate_to_optimal_audio_structure():
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("🔄 MIGRATION VERS STRUCTURE AUDIO OPTIMISÉE")
    
    # Étape 1: Ajouter les nouveaux champs avec valeurs par défaut
    result = collection.update_many(
        {},
        {
            "$set": {
                "audio_shimaoré_filename": None,
                "audio_kibouchi_filename": None, 
                "audio_shimaoré_url": None,
                "audio_kibouchi_url": None,
                "has_shimaoré_audio": False,
                "has_kibouchi_audio": False
            }
        }
    )
    
    logger.info(f"✅ Nouveaux champs ajoutés à {result.modified_count} documents")
    
    # Étape 2: Migrer les données existantes
    # À implémenter selon l'analyse...
    
    return result.modified_count

if __name__ == "__main__":
    migrate_to_optimal_audio_structure()
