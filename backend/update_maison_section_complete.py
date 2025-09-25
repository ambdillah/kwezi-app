#!/usr/bin/env python3
"""
Script pour mettre à jour la section "maison" dans la base de données
avec les nouvelles données du vocabulaire de la maison en shimaoré et kibouchi.
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

# Nouvelles données maison avec orthographe corrigée
MAISON_DATA_CORRECTED = [
    {"french": "maison", "shimaoré": "nyoumba", "kibouchi": "tragnou"},
    {"french": "porte", "shimaoré": "mlango", "kibouchi": "varavaragna"},
    {"french": "case", "shimaoré": "banga", "kibouchi": "banga"},
    {"french": "lit", "shimaoré": "chtrandra", "kibouchi": "koubani"},
    {"french": "marmite", "shimaoré": "gnoungou", "kibouchi": "vilangni"},
    {"french": "vaisselle", "shimaoré": "ziya", "kibouchi": "hintagna"},
    {"french": "bol", "shimaoré": "chicombé", "kibouchi": "bacouli"},
    {"french": "cuillère", "shimaoré": "soutrou", "kibouchi": "sotrou"},
    {"french": "fenêtre", "shimaoré": "fénétri", "kibouchi": "lafoumètara"},
    {"french": "chaise", "shimaoré": "chiri", "kibouchi": "chiri"},
    {"french": "table", "shimaoré": "latabou", "kibouchi": "latabou"},
    {"french": "miroir", "shimaoré": "chido", "kibouchi": "kitarafa"},
    {"french": "cour", "shimaoré": "mraba", "kibouchi": "lacourou"},
    {"french": "clôture", "shimaoré": "vala", "kibouchi": "vala"},
    {"french": "toilette", "shimaoré": "mrabani", "kibouchi": "mraba"},
    {"french": "seau", "shimaoré": "siyo", "kibouchi": "siyo"},
    {"french": "louche", "shimaoré": "chiwi", "kibouchi": "pow"},
    {"french": "couteau", "shimaoré": "sembéya", "kibouchi": "méssou"},
    {"french": "matelas", "shimaoré": "godoro", "kibouchi": "goudorou"},
    {"french": "oreiller", "shimaoré": "mtsao", "kibouchi": "hondagna"},
    {"french": "buffet", "shimaoré": "biffé", "kibouchi": "biffé"},
    {"french": "mur", "shimaoré": "péssi", "kibouchi": "riba"},
    {"french": "véranda", "shimaoré": "baraza", "kibouchi": "baraza"},
    {"french": "toiture", "shimaoré": "outro", "kibouchi": "vovougnou"},
    {"french": "ampoule", "shimaoré": "lalampou", "kibouchi": "lalampou"},
    {"french": "lumière", "shimaoré": "mwengué", "kibouchi": "mwengué"},
    {"french": "torche", "shimaoré": "pongé", "kibouchi": "pongi"},
    {"french": "hache", "shimaoré": "soha", "kibouchi": "famaki"},
    {"french": "machette", "shimaoré": "m'panga", "kibouchi": "ampanga"},
    {"french": "coupe-coupe", "shimaoré": "chombo", "kibouchi": "chombou"},
    {"french": "cartable", "shimaoré": "mkoba", "kibouchi": "mkoba"},
    {"french": "sac", "shimaoré": "gouni", "kibouchi": "gouni"},
    {"french": "balai", "shimaoré": "péou", "kibouchi": "famafa"},
    {"french": "mortier", "shimaoré": "chino", "kibouchi": "légnou"},
    {"french": "assiette", "shimaoré": "sahani", "kibouchi": "sahani"},
    {"french": "fondation", "shimaoré": "houra", "kibouchi": "koura"},
    {"french": "torche locale", "shimaoré": "gandilé", "kibouchi": "gandili"}
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

def get_house_emoji(french_name):
    """Retourne un emoji approprié pour l'objet de maison donné"""
    emoji_map = {
        "maison": "🏠", "porte": "🚪", "case": "🏘️", "lit": "🛏️", "marmite": "🍲", 
        "vaisselle": "🍽️", "bol": "🥣", "cuillère": "🥄", "fenêtre": "🪟", 
        "chaise": "🪑", "table": "🪑", "miroir": "🪞", "cour": "🏡", "clôture": "🚧",
        "toilette": "🚽", "seau": "🪣", "louche": "🥄", "couteau": "🔪", 
        "matelas": "🛏️", "oreiller": "🛏️", "buffet": "🗄️", "mur": "🧱",
        "véranda": "🏡", "toiture": "🏠", "ampoule": "💡", "lumière": "💡",
        "torche": "🔦", "hache": "🪓", "machette": "🗡️", "coupe-coupe": "🗡️",
        "cartable": "🎒", "sac": "🎒", "balai": "🧹", "mortier": "🫚",
        "assiette": "🍽️", "fondation": "🏗️", "torche locale": "🔦"
    }
    
    return emoji_map.get(french_name.lower(), "🏠")

def compare_and_update_maison(db):
    """Compare et met à jour l'orthographe des mots de maison"""
    collection = db['vocabulary']
    
    # Récupérer les mots actuels de la section maison
    current_words = list(collection.find({"section": "maison"}))
    logger.info(f"Mots actuels dans la section maison: {len(current_words)}")
    
    corrections_count = 0
    additions_count = 0
    
    # Créer un dictionnaire pour faciliter les comparaisons
    current_dict = {word.get('french', '').lower(): word for word in current_words}
    
    logger.info("\n=== ANALYSE DES CORRECTIONS ORTHOGRAPHIQUES ===")
    
    for corrected_word in MAISON_DATA_CORRECTED:
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
                emoji = get_house_emoji(corrected_word['french'])
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
            
            emoji = get_house_emoji(corrected_word['french'])
            
            # Créer le nom de fichier audio de manière séparée
            audio_base_name = corrected_word['french'].lower().replace(' ', '_').replace("'", '_').replace('-', '_')
            
            new_document = {
                "section": "maison",
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
    logger.info("Début de la mise à jour de la section maison")
    
    try:
        # Connexion à la base de données
        db = connect_to_database()
        
        # Comparer et mettre à jour
        corrections, additions = compare_and_update_maison(db)
        
        if corrections > 0 or additions > 0:
            logger.info(f"🎉 Mise à jour de la section maison terminée avec succès!")
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