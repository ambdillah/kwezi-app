#!/usr/bin/env python3
"""
Script auto-généré pour appliquer les correspondances audio
basé sur l'analyse case-insensitive
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

def apply_audio_correspondences():
    db = connect_to_database()
    collection = db['vocabulary']
    
    # Correspondances trouvées automatiquement
    correspondences = [
    ]
    
    logger.info(f"Application de {len(correspondences)} correspondances...")
    
    updated_count = 0
    for corr in correspondences:
        result = collection.update_one(
            {"_id": corr['word_id']},
            {
                "$set": {
                    "audio_authentic": corr['audio_path'],
                    "has_authentic_audio": True,
                    "audio_format": "m4a",
                    "auto_matched": True
                }
            }
        )
        
        if result.modified_count > 0:
            updated_count += 1
            logger.info(f"✅ {corr['french']} → {corr['audio_path']}")
    
    logger.info(f"Mises à jour appliquées: {updated_count}/{len(correspondences)}")
    return updated_count

if __name__ == "__main__":
    apply_audio_correspondences()
