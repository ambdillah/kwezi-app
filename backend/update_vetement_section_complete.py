#!/usr/bin/env python3
"""
Script pour mettre à jour la section "vêtement" dans la base de données
avec les nouvelles données du vocabulaire des vêtements en shimaoré et kibouchi.
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

# Nouvelles données vêtement avec orthographe corrigée
VETEMENT_DATA_CORRECTED = [
    {"french": "vêtement", "shimaoré": "ngouwo", "kibouchi": "ankandzou"},
    {"french": "salouva", "shimaoré": "salouva", "kibouchi": "salouvagna"},
    {"french": "chemise", "shimaoré": "chimizi", "kibouchi": "chimizi"},
    {"french": "pantalon", "shimaoré": "sourouali", "kibouchi": "sourouali"},
    {"french": "short", "shimaoré": "kaliso", "kibouchi": "kaliso"},
    {"french": "sous-vêtement", "shimaoré": "silipou", "kibouchi": "silipou"},
    {"french": "chapeau", "shimaoré": "kofia", "kibouchi": "kofia"},
    {"french": "kamiss", "shimaoré": "kandzou bolé", "kibouchi": "ankandzou bé"},
    {"french": "boubou", "shimaoré": "kandzou bolé", "kibouchi": "ankandzou bé"},
    {"french": "haut de salouva", "shimaoré": "body", "kibouchi": "body"},
    {"french": "t-shirt", "shimaoré": "kandzou", "kibouchi": "ankandzou"},
    {"french": "chaussures", "shimaoré": "kabwa", "kibouchi": "kabwa"},
    {"french": "baskets", "shimaoré": "magochi", "kibouchi": "magochi"},
    {"french": "tongs", "shimaoré": "sapatri", "kibouchi": "kabwa sapatri"},
    {"french": "jupe", "shimaoré": "jipo", "kibouchi": "jipou"},
    {"french": "robe", "shimaoré": "robo", "kibouchi": "robou"},
    {"french": "voile", "shimaoré": "kichali", "kibouchi": "kichali"}
]

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

def get_clothing_emoji(french_name):
    """Retourne un emoji approprié pour le vêtement donné"""
    emoji_map = {
        "vêtement": "👕", "salouva": "👗", "chemise": "👔", "pantalon": "👖", 
        "short": "🩳", "sous-vêtement": "🩲", "chapeau": "🎩", "kamiss": "👕",
        "boubou": "👘", "haut de salouva": "👚", "t-shirt": "👕", 
        "chaussures": "👞", "baskets": "👟", "tongs": "🩴", "jupe": "👗",
        "robe": "👗", "voile": "🧕"
    }
    
    return emoji_map.get(french_name.lower(), "👕")

def compare_and_update_vetement(db):
    """Compare et met à jour l'orthographe des mots de vêtement"""
    collection = db['vocabulary']
    
    # Récupérer les mots actuels de la section vêtement
    current_words = list(collection.find({"section": "vetements"}))
    logger.info(f"Mots actuels dans la section vêtements: {len(current_words)}")
    
    corrections_count = 0
    additions_count = 0
    
    # Créer un dictionnaire pour faciliter les comparaisons
    current_dict = {word.get('french', '').lower(): word for word in current_words}
    
    logger.info("\n=== ANALYSE DES CORRECTIONS ORTHOGRAPHIQUES ===")
    
    for corrected_word in VETEMENT_DATA_CORRECTED:
        french_key = corrected_word['french'].lower()
        
        if french_key in current_dict:
            # Le mot existe, vérifier s'il y a des corrections
            current_word = current_dict[french_key]
            current_shimaore = current_word.get('shimaoré', '')
            current_kibouchi = current_word.get('kibouchi', '')
            
            corrected_shimaore = corrected_word['shimaoré']
            corrected_kibouchi = corrected_word['kibouchi']
            
            needs_update = False
            changes = []
            
            if current_shimaore != corrected_shimaore:
                changes.append(f"shimaoré: '{current_shimaore}' → '{corrected_shimaore}'")
                needs_update = True
                
            if current_kibouchi != corrected_kibouchi:
                changes.append(f"kibouchi: '{current_kibouchi}' → '{corrected_kibouchi}'")
                needs_update = True
            
            if needs_update:
                logger.info(f"📝 CORRECTION - {corrected_word['french']}: {' | '.join(changes)}")
                
                # Mettre à jour le document
                emoji = get_clothing_emoji(corrected_word['french'])
                result = collection.update_one(
                    {"_id": current_word['_id']},
                    {
                        "$set": {
                            "shimaoré": corrected_shimaore,
                            "kibouchi": corrected_kibouchi,
                            "emoji": emoji,
                            "orthography_updated": True
                        }
                    }
                )
                
                if result.modified_count > 0:
                    corrections_count += 1
            else:
                logger.info(f"✅ OK - {corrected_word['french']}: Orthographe correcte")
        else:
            # Nouveau mot à ajouter
            logger.info(f"➕ NOUVEAU - {corrected_word['french']}: Ajout à la base de données")
            
            emoji = get_clothing_emoji(corrected_word['french'])
            
            # Créer le nom de fichier audio de manière séparée
            audio_base_name = corrected_word['french'].lower().replace(' ', '_').replace("'", '_').replace('-', '_')
            
            new_document = {
                "section": "vetements",
                "french": corrected_word['french'],
                "shimaoré": corrected_word['shimaoré'],
                "kibouchi": corrected_word['kibouchi'],
                "emoji": emoji,
                "audio_shimaoré": f"audio/{audio_base_name}_shimaoré.mp3",
                "audio_kibouchi": f"audio/{audio_base_name}_kibouchi.mp3"
            }
            
            result = collection.insert_one(new_document)
            if result.inserted_id:
                additions_count += 1
    
    logger.info(f"\n=== RÉSUMÉ DES MODIFICATIONS ===")
    logger.info(f"Corrections orthographiques appliquées: {corrections_count}")
    logger.info(f"Nouveaux mots ajoutés: {additions_count}")
    logger.info(f"Total des modifications: {corrections_count + additions_count}")
    
    return corrections_count, additions_count

def main():
    """Fonction principale"""
    logger.info("Début de la mise à jour de la section vêtement")
    
    try:
        # Connexion à la base de données
        db = connect_to_database()
        
        # Comparer et mettre à jour
        corrections, additions = compare_and_update_vetement(db)
        
        if corrections > 0 or additions > 0:
            logger.info(f"🎉 Mise à jour de la section vêtement terminée avec succès!")
            logger.info(f"   - {corrections} corrections appliquées")
            logger.info(f"   - {additions} nouveaux mots ajoutés")
        else:
            logger.info("ℹ️ Aucune correction nécessaire - l'orthographe était déjà correcte")
            
    except Exception as e:
        logger.error(f"Erreur dans le script principal: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())