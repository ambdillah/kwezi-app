#!/usr/bin/env python3
"""
Script pour mettre à jour la section "animaux" dans la base de données
avec les nouvelles données du vocabulaire des animaux.
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

# Nouvelles données animaux extraites de l'image
ANIMAUX_DATA = [
    {"french": "cochon", "shimaoré": "pouroukou", "kibouchi": "lambou"},
    {"french": "margouillat", "shimaoré": "kasangwe", "kibouchi": "kitsatsaka"},
    {"french": "abeille", "shimaoré": "niochi", "kibouchi": "antéli"},
    {"french": "chat", "shimaoré": "paha", "kibouchi": "moirou"},
    {"french": "rat", "shimaoré": "pouhou", "kibouchi": "voilavou"},
    {"french": "escargot", "shimaoré": "kwa", "kibouchi": "ancora"},
    {"french": "lion", "shimaoré": "simba", "kibouchi": "simba"},
    {"french": "grenouille", "shimaoré": "shiwatrotro", "kibouchi": "sahougnou"},
    {"french": "oiseau", "shimaoré": "gnougni", "kibouchi": "vorougnou"},
    {"french": "chien", "shimaoré": "mbwa", "kibouchi": "fadroka"},
    {"french": "poisson", "shimaoré": "fi", "kibouchi": "lokou"},
    {"french": "maki", "shimaoré": "komba", "kibouchi": "amkoumba"},
    {"french": "chèvre", "shimaoré": "mbouzi", "kibouchi": "bengui"},
    {"french": "moustique", "shimaoré": "manundri", "kibouchi": "mokou"},
    {"french": "mouche", "shimaoré": "ndzi", "kibouchi": "lalitri"},
    {"french": "chauve-souris", "shimaoré": "drema", "kibouchi": "fanihi"},
    {"french": "serpent", "shimaoré": "nyoha", "kibouchi": "bibi lava"},
    {"french": "lapin", "shimaoré": "sungura", "kibouchi": "shoungoura"},
    {"french": "canard", "shimaoré": "guisi", "kibouchi": "doukitri"},
    {"french": "mouton", "shimaoré": "baribari", "kibouchi": "baribari"},
    {"french": "crocodile", "shimaoré": "vwai", "kibouchi": "vwai"},
    {"french": "caméléon", "shimaoré": "tarundru", "kibouchi": "tarondru"},
    {"french": "zébu", "shimaoré": "nyombé", "kibouchi": "aoumbi"},
    {"french": "âne", "shimaoré": "pundra", "kibouchi": "ampundra"},
    {"french": "poule", "shimaoré": "kouhou", "kibouchi": "akohou"},
    {"french": "pigeon", "shimaoré": "ndiwa", "kibouchi": "ndiwa"},
    {"french": "fourmis", "shimaoré": "tsoussou", "kibouchi": "vitsiki"},
    {"french": "chenille", "shimaoré": "bazi", "kibouchi": "bibimanguidi"},
    {"french": "papillon", "shimaoré": "pelapelaka", "kibouchi": "tsipelapelaka"},
    {"french": "ver de terre", "shimaoré": "lingoui lingoui", "kibouchi": "bibi fotaka"},
    {"french": "criquet", "shimaoré": "furudji", "kibouchi": "kidzedza"},
    {"french": "cheval", "shimaoré": "poundra", "kibouchi": "farassi"},
    {"french": "perroquet", "shimaoré": "kassoukou", "kibouchi": "kararokou"},
    {"french": "cafard", "shimaoré": "kalalawi", "kibouchi": "kalalowou"},
    {"french": "araignée", "shimaoré": "shitrandrabwibwi", "kibouchi": "bibi ampamani massou"},
    {"french": "scorpion", "shimaoré": "hala", "kibouchi": "hala"},
    {"french": "scolopendre", "shimaoré": "trambwi", "kibouchi": "trambougnou"},
    {"french": "thon", "shimaoré": "mbassi", "kibouchi": "mbassi"},
    {"french": "requin", "shimaoré": "papa", "kibouchi": "ankiou"},
    {"french": "poulpe", "shimaoré": "pwedza", "kibouchi": "pwedza"},
    {"french": "crabe", "shimaoré": "dradraka", "kibouchi": "dakatra"},
    {"french": "tortue", "shimaoré": "nyamba/katsa", "kibouchi": "fanou"},
    {"french": "bigorno", "shimaoré": "trondro", "kibouchi": "trondrou"},
    {"french": "éléphant", "shimaoré": "ndovu", "kibouchi": "ndovu"},
    {"french": "singe", "shimaoré": "djakwe", "kibouchi": "djakouayi"},
    {"french": "souris", "shimaoré": "shikwetse", "kibouchi": "voilavou"},
    {"french": "phacochère", "shimaoré": "pouruku nyeha", "kibouchi": "lambou"},
    {"french": "lézard", "shimaoré": "ngwizi", "kibouchi": "kitsatsaka"},
    {"french": "renard", "shimaoré": "mbwa nyeha", "kibouchi": "fandroka di"},
    {"french": "chameau", "shimaoré": "ngamia", "kibouchi": "angamia"},
    {"french": "hérisson", "shimaoré": "landra", "kibouchi": "trandraka"},
    {"french": "corbeau", "shimaoré": "gawa/kwayi", "kibouchi": "gouaka"},
    {"french": "civette", "shimaoré": "founga", "kibouchi": "angava"},
    {"french": "dauphin", "shimaoré": "moungoumé", "kibouchi": "fésoutrou"},
    {"french": "baleine", "shimaoré": "ndroujou", "kibouchi": "balaine"},
    {"french": "crevette", "shimaoré": "camba", "kibouchi": "ancamba"},
    {"french": "frelon", "shimaoré": "chonga", "kibouchi": "faraka"},
    {"french": "guêpe", "shimaoré": "movou", "kibouchi": "fanintri"},
    {"french": "bourdon", "shimaoré": "vungo vungo", "kibouchi": "madjaoumbi"},
    {"french": "puce", "shimaoré": "kunguni", "kibouchi": "ancongou"},
    {"french": "poux", "shimaoré": "ndra", "kibouchi": "howou"},
    {"french": "bouc", "shimaoré": "béwé", "kibouchi": "bébérou"},
    {"french": "taureau", "shimaoré": "kondzo", "kibouchi": "dzow"},
    {"french": "bigorneau", "shimaoré": "trondro", "kibouchi": "trondrou"},
    {"french": "lambis", "shimaoré": "kombé", "kibouchi": "mahombi"},
    {"french": "cône de mer", "shimaoré": "kwitsi", "kibouchi": "tsimtipaka"},
    {"french": "mille-pattes", "shimaoré": "mjongo", "kibouchi": "ancoudavitri"},
    {"french": "oursin", "shimaoré": "gadzassi ya bahari", "kibouchi": "vouli vavi"},
    {"french": "huître", "shimaoré": "gadzassi", "kibouchi": "sadza"}
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

def update_animaux_section(db):
    """Met à jour la section animaux dans la base de données"""
    try:
        collection = db['vocabulary']
        
        # Supprimer l'ancienne section animaux
        result = collection.delete_many({"section": "animaux"})
        logger.info(f"Anciens enregistrements animaux supprimés: {result.deleted_count}")
        
        # Préparer les nouveaux documents
        new_documents = []
        for animal in ANIMAUX_DATA:
            # Créer les variations de emoji pour les animaux
            emoji = get_animal_emoji(animal["french"])
            
            document = {
                "section": "animaux",
                "french": animal["french"],
                "shimaoré": animal["shimaoré"],
                "kibouchi": animal["kibouchi"],
                "emoji": emoji,
                "audio_shimaoré": f"audio/{animal['french'].lower().replace(' ', '_').replace('-', '_')}_shimaoré.mp3",
                "audio_kibouchi": f"audio/{animal['french'].lower().replace(' ', '_').replace('-', '_')}_kibouchi.mp3"
            }
            new_documents.append(document)
        
        # Insérer les nouveaux documents
        if new_documents:
            result = collection.insert_many(new_documents)
            logger.info(f"Nouveaux animaux insérés: {len(result.inserted_ids)}")
            
            # Afficher un résumé
            logger.info(f"Section animaux mise à jour avec {len(new_documents)} entrées")
            
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour des animaux: {e}")
        return False

def get_animal_emoji(french_name):
    """Retourne un emoji approprié pour l'animal donné"""
    emoji_map = {
        "cochon": "🐷", "margouillat": "🦎", "abeille": "🐝", "chat": "🐱",
        "rat": "🐭", "escargot": "🐌", "lion": "🦁", "grenouille": "🐸",
        "oiseau": "🐦", "chien": "🐕", "poisson": "🐟", "maki": "🐒",
        "chèvre": "🐐", "moustique": "🦟", "mouche": "🪰", "chauve-souris": "🦇",
        "serpent": "🐍", "lapin": "🐰", "canard": "🦆", "mouton": "🐑",
        "crocodile": "🐊", "caméléon": "🦎", "zébu": "🐃", "âne": "🫏",
        "poule": "🐓", "pigeon": "🕊️", "fourmis": "🐜", "chenille": "🐛",
        "papillon": "🦋", "ver de terre": "🪱", "criquet": "🦗", "cheval": "🐎",
        "perroquet": "🦜", "cafard": "🪳", "araignée": "🕷️", "scorpion": "🦂",
        "scolopendre": "🐛", "thon": "🐟", "requin": "🦈", "poulpe": "🐙",
        "crabe": "🦀", "tortue": "🐢", "bigorno": "🐌", "éléphant": "🐘",
        "singe": "🐒", "souris": "🐭", "phacochère": "🐗", "lézard": "🦎",
        "renard": "🦊", "chameau": "🐪", "hérisson": "🦔", "corbeau": "🐦‍⬛",
        "civette": "🐱", "dauphin": "🐬", "baleine": "🐋", "crevette": "🦐",
        "frelon": "🐝", "guêpe": "🐝", "bourdon": "🐝", "puce": "🦟",
        "poux": "🦟", "bouc": "🐐", "taureau": "🐂", "bigorneau": "🐌",
        "lambis": "🐚", "cône de mer": "🐚", "mille-pattes": "🐛", "oursin": "🦔",
        "huître": "🦪"
    }
    
    return emoji_map.get(french_name, "🐾")

def main():
    """Fonction principale"""
    logger.info("Début de la mise à jour de la section animaux")
    
    try:
        # Connexion à la base de données
        db = connect_to_database()
        
        # Mise à jour de la section animaux
        success = update_animaux_section(db)
        
        if success:
            logger.info("Mise à jour de la section animaux terminée avec succès")
        else:
            logger.error("Échec de la mise à jour de la section animaux")
            
    except Exception as e:
        logger.error(f"Erreur dans le script principal: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())