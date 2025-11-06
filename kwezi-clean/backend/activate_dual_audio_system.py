#!/usr/bin/env python3
"""
Active le système audio dual pour tous les verbes
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

def activate_dual_audio_system():
    """Active le système dual audio pour tous les verbes"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("🔄 ACTIVATION SYSTÈME AUDIO DUAL POUR VERBES")
    
    # Activer le système dual pour tous les verbes
    result = collection.update_many(
        {"section": "verbes"},
        {"$set": {"dual_audio_system": True}}
    )
    
    logger.info(f"✅ Système dual activé pour {result.modified_count} verbes")
    
    return result.modified_count

def verify_dual_system():
    """Vérifie que le système dual est activé"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("\n=== VÉRIFICATION SYSTÈME DUAL ===")
    
    # Vérifier spécifiquement attendre et abîmer
    test_verbs = ["attendre", "abîmer"]
    
    for verb_name in test_verbs:
        verb = collection.find_one({
            "section": "verbes",
            "french": verb_name
        })
        
        if verb:
            dual_system = verb.get("dual_audio_system", False)
            has_shimaore = verb.get("has_shimaoré_audio", False)
            has_kibouchi = verb.get("has_kibouchi_audio", False)
            
            logger.info(f"\n🔍 {verb_name.upper()}:")
            logger.info(f"  dual_audio_system: {'✅' if dual_system else '❌'} {dual_system}")
            logger.info(f"  has_shimaoré_audio: {'✅' if has_shimaore else '❌'} {has_shimaore}")
            logger.info(f"  has_kibouchi_audio: {'✅' if has_kibouchi else '❌'} {has_kibouchi}")
            
            if dual_system and (has_shimaore or has_kibouchi):
                logger.info(f"  → API PRÊTE pour {verb_name}")
            else:
                logger.warning(f"  → API PAS PRÊTE pour {verb_name}")

def main():
    """Fonction principale"""
    logger.info("🎯 ACTIVATION SYSTÈME AUDIO DUAL VERBES")
    
    try:
        # 1. Activer le système dual
        activated_count = activate_dual_audio_system()
        
        # 2. Vérifier l'activation
        verify_dual_system()
        
        # 3. Résumé
        logger.info(f"\n{'='*80}")
        logger.info("RÉSUMÉ ACTIVATION SYSTÈME DUAL")
        logger.info(f"{'='*80}")
        logger.info(f"✅ Système dual activé pour: {activated_count} verbes")
        logger.info(f"🎯 L'API peut maintenant servir les audio via /api/words/{'{word_id}'}/audio/{'{lang}'}")
        logger.info(f"💡 Test avec: /api/words/WORD_ID/audio/shimaore ou /api/words/WORD_ID/audio/kibouchi")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans l'activation: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)