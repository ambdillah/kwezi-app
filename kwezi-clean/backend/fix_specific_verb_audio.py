#!/usr/bin/env python3
"""
Script pour corriger précisément les correspondances audio des verbes spécifiques
mentionnés par l'utilisateur : voir, danser, dormir, casser.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

# Charger les variables d'environnement
load_dotenv()

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Correspondances EXACTES demandées par l'utilisateur
EXACT_VERB_MAPPINGS = {
    "voir": {
        "shimaoré": "ouona",
        "kibouchi": "mahita", 
        "audio_file": "Magnamiya.m4a",  # L'utilisateur veut cette correspondance
        "note": "Audio basé sur kibouchi mais utilisateur demande Magnamiya"
    },
    "danser": {
        "shimaoré": "ouzina",
        "kibouchi": "chokou",  # L'utilisateur veut cette traduction
        "audio_file": "Chokou.m4a",
        "note": "Corriger kibouchi de 'mitsindzaka' vers 'chokou'"
    },
    "dormir": {
        "shimaoré": "oulala",
        "kibouchi": "koimini",  # L'utilisateur veut cette correspondance
        "audio_file": "Koimini.m4a",
        "note": "Ajouter correspondance audio Koimini"
    },
    "casser": {
        "shimaoré": "latsaka",
        "kibouchi": "latsaka",
        "audio_file": "Latsaka.m4a",
        "note": "S'assurer que le verbe existe et a la bonne audio"
    }
}

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

def fix_specific_verbs(db):
    """Corrige les verbes spécifiques selon les exigences de l'utilisateur"""
    collection = db['vocabulary']
    
    logger.info("=== CORRECTION DES VERBES SPÉCIFIQUES ===")
    
    fixed_count = 0
    
    for french_verb, correct_data in EXACT_VERB_MAPPINGS.items():
        logger.info(f"\n--- Traitement de '{french_verb}' ---")
        
        # Chercher le verbe dans la base
        verb_doc = collection.find_one({
            "section": "verbes",
            "french": french_verb
        })
        
        if verb_doc:
            # Le verbe existe, le mettre à jour
            logger.info(f"Verbe '{french_verb}' trouvé - Mise à jour")
            
            # Construire les nouvelles données
            update_data = {
                "shimaoré": correct_data["shimaoré"],
                "kibouchi": correct_data["kibouchi"],
                "audio_authentic": f"audio/verbes/{correct_data['audio_file']}",
                "has_authentic_audio": True,
                "audio_updated": True,
                "audio_format": "m4a",
                "user_corrected": True,
                "correction_note": correct_data["note"]
            }
            
            # Appliquer la mise à jour
            result = collection.update_one(
                {"_id": verb_doc["_id"]},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"✅ {french_verb}: Shimaoré '{correct_data['shimaoré']}', Kibouchi '{correct_data['kibouchi']}' → {correct_data['audio_file']}")
                fixed_count += 1
            else:
                logger.warning(f"❌ Échec mise à jour: {french_verb}")
                
        else:
            # Le verbe n'existe pas, le créer
            logger.info(f"Verbe '{french_verb}' non trouvé - Création")
            
            new_verb = {
                "section": "verbes",
                "french": french_verb,
                "shimaoré": correct_data["shimaoré"],
                "kibouchi": correct_data["kibouchi"],
                "emoji": "🔄",
                "audio_authentic": f"audio/verbes/{correct_data['audio_file']}",
                "has_authentic_audio": True,
                "audio_updated": True,
                "audio_format": "m4a",
                "user_corrected": True,
                "correction_note": correct_data["note"],
                "pdf_reference": True
            }
            
            result = collection.insert_one(new_verb)
            
            if result.inserted_id:
                logger.info(f"✅ {french_verb}: Créé avec Shimaoré '{correct_data['shimaoré']}', Kibouchi '{correct_data['kibouchi']}' → {correct_data['audio_file']}")
                fixed_count += 1
            else:
                logger.warning(f"❌ Échec création: {french_verb}")
    
    return fixed_count

def verify_audio_files():
    """Vérifie que les fichiers audio existent"""
    audio_dir = "/app/frontend/assets/audio/verbes"
    
    logger.info("\n=== VÉRIFICATION FICHIERS AUDIO ===")
    
    for french_verb, data in EXACT_VERB_MAPPINGS.items():
        audio_file = data["audio_file"]
        full_path = os.path.join(audio_dir, audio_file)
        
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            logger.info(f"✅ {french_verb}: {audio_file} trouvé ({size} bytes)")
        else:
            logger.warning(f"❌ {french_verb}: {audio_file} MANQUANT dans {audio_dir}")

def test_corrected_verbs(db):
    """Teste que les corrections ont été appliquées"""
    collection = db['vocabulary']
    
    logger.info("\n=== TEST DES CORRECTIONS APPLIQUÉES ===")
    
    success_count = 0
    
    for french_verb, expected_data in EXACT_VERB_MAPPINGS.items():
        verb_doc = collection.find_one({
            "section": "verbes",
            "french": french_verb
        })
        
        if verb_doc:
            shimaore_ok = verb_doc.get("shimaoré") == expected_data["shimaoré"]
            kibouchi_ok = verb_doc.get("kibouchi") == expected_data["kibouchi"]
            audio_ok = verb_doc.get("audio_authentic") == f"audio/verbes/{expected_data['audio_file']}"
            has_audio_ok = verb_doc.get("has_authentic_audio") == True
            
            if shimaore_ok and kibouchi_ok and audio_ok and has_audio_ok:
                logger.info(f"✅ {french_verb}: PARFAIT - Toutes les correspondances correctes")
                success_count += 1
            else:
                logger.warning(f"❌ {french_verb}: PROBLÈME - Vérifications échouées:")
                if not shimaore_ok:
                    logger.warning(f"    Shimaoré: attendu '{expected_data['shimaoré']}', trouvé '{verb_doc.get('shimaoré')}'")
                if not kibouchi_ok:
                    logger.warning(f"    Kibouchi: attendu '{expected_data['kibouchi']}', trouvé '{verb_doc.get('kibouchi')}'")
                if not audio_ok:
                    logger.warning(f"    Audio: attendu 'audio/verbes/{expected_data['audio_file']}', trouvé '{verb_doc.get('audio_authentic')}'")
                if not has_audio_ok:
                    logger.warning(f"    Has_audio: attendu True, trouvé {verb_doc.get('has_authentic_audio')}")
        else:
            logger.warning(f"❌ {french_verb}: Verbe non trouvé après correction!")
    
    return success_count

def main():
    """Fonction principale"""
    logger.info("Début des corrections spécifiques des verbes audio")
    
    try:
        # Vérifier les fichiers audio
        verify_audio_files()
        
        # Connexion à la base de données
        db = connect_to_database()
        
        # Appliquer les corrections
        fixed_count = fix_specific_verbs(db)
        
        # Tester les corrections
        success_count = test_corrected_verbs(db)
        
        # Résumé final
        logger.info(f"\n{'='*60}")
        logger.info("RÉSUMÉ CORRECTIONS SPÉCIFIQUES")
        logger.info(f"{'='*60}")
        logger.info(f"Verbes traités: {len(EXACT_VERB_MAPPINGS)}")
        logger.info(f"Corrections appliquées: {fixed_count}")
        logger.info(f"Vérifications réussies: {success_count}")
        
        for french_verb, data in EXACT_VERB_MAPPINGS.items():
            logger.info(f"  - {french_verb}: shimaoré '{data['shimaoré']}' | kibouchi '{data['kibouchi']}' → {data['audio_file']}")
        
        if success_count == len(EXACT_VERB_MAPPINGS):
            logger.info("🎉 TOUTES les correspondances spécifiques sont maintenant PARFAITES!")
            logger.info("Plus de frustration - chaque verbe a sa bonne prononciation!")
        else:
            logger.warning(f"⚠️ {len(EXACT_VERB_MAPPINGS) - success_count} verbes nécessitent encore des corrections")
            
    except Exception as e:
        logger.error(f"Erreur dans le script principal: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())