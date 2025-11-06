#!/usr/bin/env python3
"""
Nettoyage des anciens champs audio qui interfèrent avec les nouveaux
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

def cleanup_old_audio_fields():
    """Supprime tous les anciens champs audio qui interfèrent"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("🧹 NETTOYAGE ANCIENS CHAMPS AUDIO")
    
    # Liste des anciens champs à supprimer
    old_fields_to_remove = [
        "audio_authentic",
        "has_authentic_audio", 
        "audio_shimaoré",
        "audio_kibouchi",
        "audio_format",
        "audio_updated",
        "auto_matched",
        "match_type",
        "match_field",
        "audio_match_source",
        "auto_matched_verbs",
        "updated_with_new_audio",
        "updated_with_191_files",
        "corrected_from_user_tables",
        "audio_structure_updated",
        "oumengna_problem_resolved",
        "case_sensitive_filename"
    ]
    
    logger.info(f"Champs à supprimer: {len(old_fields_to_remove)}")
    for field in old_fields_to_remove:
        logger.info(f"  - {field}")
    
    # Supprimer tous les anciens champs
    unset_query = {}
    for field in old_fields_to_remove:
        unset_query[field] = ""
    
    result = collection.update_many(
        {"section": "verbes"},
        {"$unset": unset_query}
    )
    
    logger.info(f"✅ {result.modified_count} verbes nettoyés")
    
    return result.modified_count

def verify_cleanup():
    """Vérifie que le nettoyage a bien fonctionné"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("\n=== VÉRIFICATION NETTOYAGE ===")
    
    # Vérifier "attendre" et "abîmer" spécifiquement
    test_verbs = ["attendre", "abîmer"]
    
    for verb_name in test_verbs:
        verb = collection.find_one({
            "section": "verbes",
            "french": verb_name
        })
        
        if verb:
            logger.info(f"\n🔍 {verb_name.upper()}:")
            logger.info(f"  Français: {verb.get('french', 'N/A')}")
            logger.info(f"  Shimaoré: {verb.get('shimaoré', 'N/A')}")
            logger.info(f"  Kibouchi: {verb.get('kibouchi', 'N/A')}")
            
            # Nouveaux champs (doivent exister)
            logger.info(f"✅ NOUVEAUX CHAMPS:")
            logger.info(f"  audio_shimaoré_filename: {verb.get('audio_shimaoré_filename', 'Aucun')}")
            logger.info(f"  audio_kibouchi_filename: {verb.get('audio_kibouchi_filename', 'Aucun')}")
            logger.info(f"  audio_shimaoré_url: {verb.get('audio_shimaoré_url', 'Aucun')}")
            logger.info(f"  audio_kibouchi_url: {verb.get('audio_kibouchi_url', 'Aucun')}")
            logger.info(f"  has_shimaoré_audio: {verb.get('has_shimaoré_audio', False)}")
            logger.info(f"  has_kibouchi_audio: {verb.get('has_kibouchi_audio', False)}")
            
            # Anciens champs (ne doivent plus exister)
            old_fields_present = []
            if verb.get('audio_shimaoré'):
                old_fields_present.append(f"audio_shimaoré: {verb.get('audio_shimaoré')}")
            if verb.get('audio_kibouchi'):
                old_fields_present.append(f"audio_kibouchi: {verb.get('audio_kibouchi')}")
            if verb.get('audio_authentic'):
                old_fields_present.append(f"audio_authentic: {verb.get('audio_authentic')}")
            
            if old_fields_present:
                logger.warning(f"❌ ANCIENS CHAMPS ENCORE PRÉSENTS:")
                for field in old_fields_present:
                    logger.warning(f"     {field}")
            else:
                logger.info(f"✅ Anciens champs supprimés")

def main():
    """Fonction principale"""
    logger.info("🎯 NETTOYAGE ANCIENS CHAMPS AUDIO VERBES")
    
    try:
        # 1. Nettoyer les anciens champs
        cleaned_count = cleanup_old_audio_fields()
        
        # 2. Vérifier le nettoyage
        verify_cleanup()
        
        # 3. Résumé
        logger.info(f"\n{'='*80}")
        logger.info("RÉSUMÉ NETTOYAGE")
        logger.info(f"{'='*80}")
        logger.info(f"✅ Verbes nettoyés: {cleaned_count}")
        logger.info(f"🎯 Anciens champs supprimés")
        logger.info(f"💡 L'API devrait maintenant utiliser les nouveaux champs")
        logger.info(f"🔄 Redémarrer le backend recommandé")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le nettoyage: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)