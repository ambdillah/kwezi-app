#!/usr/bin/env python3
"""
Script pour mettre à jour la section "nombres" dans la base de données
avec les nouvelles données du vocabulaire des nombres.
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

# Nouvelles données nombres extraites de l'image
NOMBRES_DATA = [
    {"french": "un", "shimaoré": "moja", "kibouchi": "areki", "number_type": "cardinal", "numeric_value": 1},
    {"french": "deux", "shimaoré": "mbili", "kibouchi": "Aroyi", "number_type": "cardinal", "numeric_value": 2},
    {"french": "trois", "shimaoré": "trarou", "kibouchi": "Telou", "number_type": "cardinal", "numeric_value": 3},
    {"french": "quatre", "shimaoré": "nhé", "kibouchi": "Efatra", "number_type": "cardinal", "numeric_value": 4},
    {"french": "cinq", "shimaoré": "tsano", "kibouchi": "Dimi", "number_type": "cardinal", "numeric_value": 5},
    {"french": "six", "shimaoré": "sita", "kibouchi": "Tchouta", "number_type": "cardinal", "numeric_value": 6},
    {"french": "sept", "shimaoré": "saba", "kibouchi": "Fitou", "number_type": "cardinal", "numeric_value": 7},
    {"french": "huit", "shimaoré": "nané", "kibouchi": "Valou", "number_type": "cardinal", "numeric_value": 8},
    {"french": "neuf", "shimaoré": "chendra", "kibouchi": "Civi", "number_type": "cardinal", "numeric_value": 9},
    {"french": "dix", "shimaoré": "koumi", "kibouchi": "Foulou", "number_type": "cardinal", "numeric_value": 10},
    {"french": "onze", "shimaoré": "koumi na moja", "kibouchi": "Foulou Areki Ambi", "number_type": "cardinal", "numeric_value": 11},
    {"french": "douze", "shimaoré": "koumi na mbili", "kibouchi": "Foulou Aroyi Ambi", "number_type": "cardinal", "numeric_value": 12},
    {"french": "treize", "shimaoré": "koumi na trarou", "kibouchi": "Foulou Telou Ambi", "number_type": "cardinal", "numeric_value": 13},
    {"french": "quatorze", "shimaoré": "koumi na nhé", "kibouchi": "Foulou Efatra Ambi", "number_type": "cardinal", "numeric_value": 14},
    {"french": "quinze", "shimaoré": "koumi na tsano", "kibouchi": "Foulou Dimi Ambi", "number_type": "cardinal", "numeric_value": 15},
    {"french": "seize", "shimaoré": "koumi na sita", "kibouchi": "Foulou tchouta Ambi", "number_type": "cardinal", "numeric_value": 16},
    {"french": "dix-sept", "shimaoré": "koumi na saba", "kibouchi": "Foulou fitou Ambi", "number_type": "cardinal", "numeric_value": 17},
    {"french": "dix-huit", "shimaoré": "koumi na nané", "kibouchi": "Foulou valou Ambi", "number_type": "cardinal", "numeric_value": 18},
    {"french": "dix-neuf", "shimaoré": "koumi na chendra", "kibouchi": "Foulou civi Ambi", "number_type": "cardinal", "numeric_value": 19},
    {"french": "vingt", "shimaoré": "chirini", "kibouchi": "arompoulou", "number_type": "cardinal", "numeric_value": 20},
    {"french": "trente", "shimaoré": "thalathini", "kibouchi": "téloumpoulou", "number_type": "cardinal", "numeric_value": 30},
    {"french": "quarante", "shimaoré": "arbahini", "kibouchi": "éfampoulou", "number_type": "cardinal", "numeric_value": 40},
    {"french": "cinquante", "shimaoré": "hamssini", "kibouchi": "dimimpoulou", "number_type": "cardinal", "numeric_value": 50},
    {"french": "soixante", "shimaoré": "sitini", "kibouchi": "tchoutampoulou", "number_type": "cardinal", "numeric_value": 60},
    {"french": "soixante-dix", "shimaoré": "sabouini", "kibouchi": "fitoumpoulou", "number_type": "cardinal", "numeric_value": 70},
    {"french": "quatre-vingts", "shimaoré": "thamanini", "kibouchi": "valoumpoulou", "number_type": "cardinal", "numeric_value": 80},
    {"french": "quatre-vingt-dix", "shimaoré": "toussuini", "kibouchi": "civiampulou", "number_type": "cardinal", "numeric_value": 90},
    {"french": "cent", "shimaoré": "miya", "kibouchi": "zatou", "number_type": "cardinal", "numeric_value": 100}
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

def update_nombres_section(db):
    """Met à jour la section nombres dans la base de données"""
    try:
        collection = db['vocabulary']
        
        # Supprimer l'ancienne section nombres
        result = collection.delete_many({"section": "nombres"})
        logger.info(f"Anciens enregistrements nombres supprimés: {result.deleted_count}")
        
        # Préparer les nouveaux documents
        new_documents = []
        for number in NOMBRES_DATA:
            # Créer l'emoji pour les nombres
            emoji = get_number_emoji(number["numeric_value"])
            
            document = {
                "section": "nombres",
                "french": number["french"],
                "shimaoré": number["shimaoré"],
                "kibouchi": number["kibouchi"],
                "emoji": emoji,
                "number_type": number["number_type"],
                "numeric_value": number["numeric_value"],
                "audio_shimaoré": f"audio/{number['french'].lower().replace(' ', '_').replace('-', '_')}_shimaoré.mp3",
                "audio_kibouchi": f"audio/{number['french'].lower().replace(' ', '_').replace('-', '_')}_kibouchi.mp3"
            }
            new_documents.append(document)
        
        # Insérer les nouveaux documents
        if new_documents:
            result = collection.insert_many(new_documents)
            logger.info(f"Nouveaux nombres insérés: {len(result.inserted_ids)}")
            
            # Afficher un résumé
            logger.info(f"Section nombres mise à jour avec {len(new_documents)} entrées")
            logger.info(f"Plage numérique couverte: 1-100 (nombres cardinaux)")
            
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour des nombres: {e}")
        return False

def get_number_emoji(numeric_value):
    """Retourne un emoji approprié pour le nombre donné"""
    # Emojis pour les nombres 1-10
    emoji_map = {
        1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣",
        6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"
    }
    
    # Emojis pour les nombres spéciaux
    if numeric_value in emoji_map:
        return emoji_map[numeric_value]
    elif numeric_value == 100:
        return "💯"
    elif numeric_value >= 20:
        # Pour les dizaines (20, 30, 40, etc.)
        return "🔢"
    else:
        # Pour 11-19
        return "🔢"

def validate_number_data():
    """Valide les données des nombres avant insertion"""
    logger.info("Validation des données des nombres...")
    
    # Vérifier qu'il n'y a pas de doublons
    french_words = [n["french"] for n in NOMBRES_DATA]
    numeric_values = [n["numeric_value"] for n in NOMBRES_DATA]
    
    if len(set(french_words)) != len(french_words):
        logger.error("Doublons détectés dans les mots français")
        return False
    
    if len(set(numeric_values)) != len(numeric_values):
        logger.error("Doublons détectés dans les valeurs numériques")
        return False
    
    # Vérifier que tous les nombres ont les champs requis
    for number in NOMBRES_DATA:
        required_fields = ["french", "shimaoré", "kibouchi", "numeric_value"]
        for field in required_fields:
            if not number.get(field):
                logger.error(f"Champ manquant '{field}' pour {number.get('french', 'nombre inconnu')}")
                return False
    
    logger.info(f"Validation réussie pour {len(NOMBRES_DATA)} nombres")
    return True

def main():
    """Fonction principale"""
    logger.info("Début de la mise à jour de la section nombres")
    
    try:
        # Validation des données
        if not validate_number_data():
            logger.error("Échec de la validation des données")
            return 1
        
        # Connexion à la base de données
        db = connect_to_database()
        
        # Mise à jour de la section nombres
        success = update_nombres_section(db)
        
        if success:
            logger.info("Mise à jour de la section nombres terminée avec succès")
            logger.info("Les nombres de 1 à 100 sont maintenant disponibles en shimaoré et kibouchi")
        else:
            logger.error("Échec de la mise à jour de la section nombres")
            
    except Exception as e:
        logger.error(f"Erreur dans le script principal: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())