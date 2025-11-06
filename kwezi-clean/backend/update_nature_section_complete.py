#!/usr/bin/env python3
"""
Script pour mettre à jour la section "nature" dans la base de données
avec les nouvelles données du vocabulaire de la nature en shimaoré et kibouchi.
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

# Nouvelles données nature avec orthographe corrigée
NATURE_DATA_CORRECTED = [
    {"french": "pente", "shimaoré": "mlima", "kibouchi": "boungou"},
    {"french": "colline", "shimaoré": "mlima", "kibouchi": "boungou"},
    {"french": "mont", "shimaoré": "mlima", "kibouchi": "boungou"},
    {"french": "lune", "shimaoré": "mwézi", "kibouchi": "fandzava"},
    {"french": "étoile", "shimaoré": "gnora", "kibouchi": "lakintagna"},
    {"french": "sable", "shimaoré": "mtsanga", "kibouchi": "fasigni"},
    {"french": "vague", "shimaoré": "dhouja", "kibouchi": "houndza"},
    {"french": "vent", "shimaoré": "pévo", "kibouchi": "tsikou"},
    {"french": "pluie", "shimaoré": "vhoua", "kibouchi": "mahaléni"},
    {"french": "mangrove", "shimaoré": "mhonko", "kibouchi": "honkou"},
    {"french": "corail", "shimaoré": "soiyi", "kibouchi": "soiyi"},
    {"french": "barrière de corail", "shimaoré": "caléni", "kibouchi": "caléni"},
    {"french": "tempête", "shimaoré": "darouba", "kibouchi": "tsikou"},
    {"french": "rivière", "shimaoré": "mouro", "kibouchi": "mouroni"},
    {"french": "pont", "shimaoré": "daradja", "kibouchi": "daradja"},
    {"french": "nuage", "shimaoré": "wingou", "kibouchi": "vingou"},
    {"french": "arc-en-ciel", "shimaoré": "mcacamba", "kibouchi": "vingou"},
    {"french": "campagne", "shimaoré": "malavouni", "kibouchi": "atihala"},
    {"french": "forêt", "shimaoré": "malavouni", "kibouchi": "atihala"},
    {"french": "caillou", "shimaoré": "bwé", "kibouchi": "vatou"},
    {"french": "pierre", "shimaoré": "bwé", "kibouchi": "vatou"},
    {"french": "rocher", "shimaoré": "bwé", "kibouchi": "vatou"},
    {"french": "plateau", "shimaoré": "bandra", "kibouchi": "kètraka"},
    {"french": "chemin", "shimaoré": "ndzia", "kibouchi": "lalagna"},
    {"french": "sentier", "shimaoré": "ndzia", "kibouchi": "lalagna"},
    {"french": "parcours", "shimaoré": "ndzia", "kibouchi": "lalagna"},
    {"french": "herbe", "shimaoré": "malavou", "kibouchi": "haitri"},
    {"french": "fleur", "shimaoré": "foulera", "kibouchi": "foulèra"},
    {"french": "soleil", "shimaoré": "jouwa", "kibouchi": "zouva"},
    {"french": "mer", "shimaoré": "bahari", "kibouchi": "bahari"},
    {"french": "plage", "shimaoré": "mtsangani", "kibouchi": "fassigni"},
    {"french": "arbre", "shimaoré": "mwiri", "kibouchi": "kakazou"},
    {"french": "rue", "shimaoré": "paré", "kibouchi": "paré"},
    {"french": "route", "shimaoré": "paré", "kibouchi": "paré"},
    {"french": "bananier", "shimaoré": "trindri", "kibouchi": "voudi ni hountsi"},
    {"french": "feuille", "shimaoré": "mawoini", "kibouchi": "hayitri"},
    {"french": "branche", "shimaoré": "trahi", "kibouchi": "trahi"},
    {"french": "tornade", "shimaoré": "ouzimouyi", "kibouchi": "tsikou soulaimana"},
    {"french": "cocotier", "shimaoré": "m'nadzi", "kibouchi": "voudi ni vwaniou"},
    {"french": "arbre à pain", "shimaoré": "m'frampé", "kibouchi": "voudi ni frampé"},
    {"french": "baobab", "shimaoré": "m'bouyou", "kibouchi": "voudi ni bouyou"},
    {"french": "bambou", "shimaoré": "m'bambo", "kibouchi": "valiha"},
    {"french": "manguier", "shimaoré": "m'manga", "kibouchi": "voudi ni manga"},
    {"french": "jacquier", "shimaoré": "m'fénéssi", "kibouchi": "voudi ni finéssi"},
    {"french": "terre", "shimaoré": "trotrotro", "kibouchi": "fotaka"},
    {"french": "sol", "shimaoré": "tsi", "kibouchi": "tani"},
    {"french": "érosion", "shimaoré": "padza", "kibouchi": "padza"},
    {"french": "marée basse", "shimaoré": "maji yavo", "kibouchi": "ranou mèki"},
    {"french": "platier", "shimaoré": "kalé", "kibouchi": "kaléni"},
    {"french": "marée haute", "shimaoré": "maji yamalé", "kibouchi": "ranou fénou"},
    {"french": "inondé", "shimaoré": "ourora", "kibouchi": "dobou"},
    {"french": "sauvage", "shimaoré": "nyéha", "kibouchi": "di"},
    {"french": "canne à sucre", "shimaoré": "mouwoi", "kibouchi": "fari"},
    {"french": "fagot", "shimaoré": "kouni", "kibouchi": "azoumati"},
    {"french": "pirogue", "shimaoré": "laka", "kibouchi": "lakana"},
    {"french": "vedette", "shimaoré": "kwassa kwassa", "kibouchi": "vidéti"},
    {"french": "école", "shimaoré": "licoli", "kibouchi": "licoli"},
    {"french": "école coranique", "shimaoré": "shioni", "kibouchi": "kioni"}
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

def get_nature_emoji(french_name):
    """Retourne un emoji approprié pour l'élément de nature donné"""
    emoji_map = {
        "pente": "⛰️", "colline": "⛰️", "mont": "🏔️", "lune": "🌙", "étoile": "⭐",
        "sable": "🏖️", "vague": "🌊", "vent": "💨", "pluie": "🌧️", "mangrove": "🌿",
        "corail": "🪸", "barrière de corail": "🪸", "tempête": "⛈️", "rivière": "🏞️",
        "pont": "🌉", "nuage": "☁️", "arc-en-ciel": "🌈", "campagne": "🌾", "forêt": "🌲",
        "caillou": "🪨", "pierre": "🪨", "rocher": "🪨", "plateau": "🏔️",
        "chemin": "🛤️", "sentier": "🛤️", "parcours": "🛤️", "herbe": "🌿", "fleur": "🌸",
        "soleil": "☀️", "mer": "🌊", "plage": "🏖️", "arbre": "🌳", "rue": "🛣️", "route": "🛣️",
        "bananier": "🌴", "feuille": "🍃", "branche": "🌿", "tornade": "🌪️",
        "cocotier": "🥥", "arbre à pain": "🌳", "baobab": "🌳", "bambou": "🎋",
        "manguier": "🌳", "jacquier": "🌳", "terre": "🌍", "sol": "🌱",
        "érosion": "🏔️", "marée basse": "🌊", "platier": "🪨", "marée haute": "🌊",
        "inondé": "🌊", "sauvage": "🌿", "canne à sucre": "🌾", "fagot": "🪵",
        "pirogue": "🛶", "vedette": "🚤", "école": "🏫", "école coranique": "🏫"
    }
    
    return emoji_map.get(french_name.lower(), "🌿")

def compare_and_update_nature(db):
    """Compare et met à jour l'orthographe des mots de nature"""
    collection = db['vocabulary']
    
    # Récupérer les mots actuels de la section nature
    current_words = list(collection.find({"section": "nature"}))
    logger.info(f"Mots actuels dans la section nature: {len(current_words)}")
    
    corrections_count = 0
    additions_count = 0
    
    # Créer un dictionnaire pour faciliter les comparaisons
    current_dict = {word.get('french', '').lower(): word for word in current_words}
    
    logger.info("\n=== ANALYSE DES CORRECTIONS ORTHOGRAPHIQUES ===")
    
    for corrected_word in NATURE_DATA_CORRECTED:
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
                emoji = get_nature_emoji(corrected_word['french'])
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
            
            emoji = get_nature_emoji(corrected_word['french'])
            
            # Créer le nom de fichier audio de manière séparée
            audio_base_name = corrected_word['french'].lower().replace(' ', '_').replace("'", '_').replace('-', '_').replace('à', 'a').replace('é', 'e').replace('è', 'e')
            
            new_document = {
                "section": "nature",
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
    logger.info("Début de la mise à jour de la section nature")
    
    try:
        # Connexion à la base de données
        db = connect_to_database()
        
        # Comparer et mettre à jour
        corrections, additions = compare_and_update_nature(db)
        
        if corrections > 0 or additions > 0:
            logger.info(f"🎉 Mise à jour de la section nature terminée avec succès!")
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