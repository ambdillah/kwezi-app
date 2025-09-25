#!/usr/bin/env python3
"""
Script pour corriger l'orthographe en shimaoré et kibouchi 
de la section "nourriture" basé sur l'image fournie par l'utilisateur.
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

# Nouvelles données nourriture avec orthographe corrigée
NOURRITURE_DATA_CORRECTED = [
    {"french": "riz", "shimaoré": "tsoholé", "kibouchi": "vari"},
    {"french": "eau", "shimaoré": "maji", "kibouchi": "ranou"},
    {"french": "ananas", "shimaoré": "nanassi", "kibouchi": "mananassi"},
    {"french": "pois d'angole", "shimaoré": "tsouzi", "kibouchi": "ambatri"},
    {"french": "banane", "shimaoré": "trovi", "kibouchi": "hountsi"},
    {"french": "pain", "shimaoré": "dipé", "kibouchi": "dipé"},
    {"french": "gâteau", "shimaoré": "mharé", "kibouchi": "moukari"},
    {"french": "mangue", "shimaoré": "manga", "kibouchi": "manga"},
    {"french": "noix de coco", "shimaoré": "nadzi", "kibouchi": "voiniou"},
    {"french": "noix de coco fraîche", "shimaoré": "chijavou", "kibouchi": "kidjavou"},
    {"french": "lait", "shimaoré": "dzia", "kibouchi": "rounounou"},
    {"french": "viande", "shimaoré": "nhyama", "kibouchi": "amboumati"},
    {"french": "poisson", "shimaoré": "fi", "kibouchi": "lokou"},
    {"french": "brèdes", "shimaoré": "féliki", "kibouchi": "féliki"},
    {"french": "brède mafane", "shimaoré": "féliki mafana", "kibouchi": "féliki mafana"},
    {"french": "brède manioc", "shimaoré": "mataba", "kibouchi": "féliki mouhogou"},
    {"french": "brède morelle", "shimaoré": "féliki nyongo", "kibouchi": "féliki angnatsindra"},
    {"french": "brèdes patate douce", "shimaoré": "féliki batata", "kibouchi": "féliki batata"},
    {"french": "patate douce", "shimaoré": "batata", "kibouchi": "batata"},
    {"french": "bouillon", "shimaoré": "woubou", "kibouchi": "kouba"},
    {"french": "banane au coco", "shimaoré": "trovi ya nadzi", "kibouchi": "hountsi an voiniou"},
    {"french": "riz au coco", "shimaoré": "tsoholé ya nadzi", "kibouchi": "vari an voiniou"},
    {"french": "poulet", "shimaoré": "bawa", "kibouchi": "mabawa"},
    {"french": "œuf", "shimaoré": "joiyi", "kibouchi": "antoudi"},
    {"french": "tomate", "shimaoré": "tamati", "kibouchi": "matimati"},
    {"french": "oignon", "shimaoré": "chouroungou", "kibouchi": "doungoulou"},
    {"french": "ail", "shimaoré": "chouroungou voudjé", "kibouchi": "doungoulou mvoudjou"},
    {"french": "orange", "shimaoré": "troundra", "kibouchi": "tsoha"},
    {"french": "mandarine", "shimaoré": "madhandzé", "kibouchi": "tsoha madzandzi"},
    {"french": "manioc", "shimaoré": "mhogo", "kibouchi": "mouhogou"},
    {"french": "piment", "shimaoré": "poutou", "kibouchi": "pilipili"},
    {"french": "taro", "shimaoré": "majimbi", "kibouchi": "majimbi"},
    {"french": "sel", "shimaoré": "chingó", "kibouchi": "sira"},
    {"french": "poivre", "shimaoré": "bvilibvili manga", "kibouchi": "vilivili"},
    {"french": "curcuma", "shimaoré": "dzindzano", "kibouchi": "tamoutamou"},
    {"french": "cumin", "shimaoré": "massala", "kibouchi": "massala"},
    {"french": "ciboulette", "shimaoré": "chourougnou mani", "kibouchi": "doungoulou ravigni"},
    {"french": "gingembre", "shimaoré": "tsingiziou", "kibouchi": "sakėyi"},
    {"french": "vanille", "shimaoré": "lavani", "kibouchi": "lavani"},
    {"french": "tamarin", "shimaoré": "ouhajou", "kibouchi": "madirou kakazou"},
    {"french": "un thé", "shimaoré": "maji ya moro", "kibouchi": "ranou meyi"},
    {"french": "papaye", "shimaoré": "papaya", "kibouchi": "poipoiya"},
    {"french": "nourriture", "shimaoré": "chaoula", "kibouchi": "hanigni"},
    {"french": "riz non décortiqué", "shimaoré": "mélé", "kibouchi": "vari tsivoidissa"}
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

def get_food_emoji(french_name):
    """Retourne un emoji approprié pour l'aliment donné"""
    emoji_map = {
        "riz": "🍚", "eau": "💧", "ananas": "🍍", "pois d'angole": "🫘", 
        "banane": "🍌", "pain": "🍞", "gâteau": "🎂", "mangue": "🥭",
        "noix de coco": "🥥", "noix de coco fraîche": "🥥", "lait": "🥛", 
        "viande": "🥩", "poisson": "🐟", "brèdes": "🥬", "brède mafane": "🥬",
        "brède manioc": "🥬", "brède morelle": "🥬", "brèdes patate douce": "🥬",
        "patate douce": "🍠", "bouillon": "🍲", "banane au coco": "🍌",
        "riz au coco": "🍚", "poulet": "🐔", "œuf": "🥚", "tomate": "🍅",
        "oignon": "🧅", "ail": "🧄", "orange": "🍊", "mandarine": "🍊",
        "manioc": "🥔", "piment": "🌶️", "taro": "🥔", "sel": "🧂",
        "poivre": "🫚", "curcuma": "🫚", "cumin": "🫚", "ciboulette": "🌿",
        "gingembre": "🫚", "vanille": "🌿", "tamarin": "🍇", "un thé": "🍵",
        "papaye": "🥭", "nourriture": "🍽️", "riz non décortiqué": "🌾"
    }
    
    return emoji_map.get(french_name.lower(), "🍽️")

def compare_and_update_nourriture(db):
    """Compare et met à jour l'orthographe des mots de nourriture"""
    collection = db['vocabulary']
    
    # Récupérer les mots actuels de la section nourriture
    current_words = list(collection.find({"section": "nourriture"}))
    logger.info(f"Mots actuels dans la section nourriture: {len(current_words)}")
    
    corrections_count = 0
    additions_count = 0
    
    # Créer un dictionnaire pour faciliter les comparaisons
    current_dict = {word.get('french', '').lower(): word for word in current_words}
    
    logger.info("\n=== ANALYSE DES CORRECTIONS ORTHOGRAPHIQUES ===")
    
    for corrected_word in NOURRITURE_DATA_CORRECTED:
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
                emoji = get_food_emoji(corrected_word['french'])
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
            
            emoji = get_food_emoji(corrected_word['french'])
            
            # Créer le nom de fichier audio de manière séparée
            audio_base_name = corrected_word['french'].lower().replace(' ', '_').replace("'", '_')
            
            new_document = {
                "section": "nourriture",
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
    logger.info("Début de la révision orthographique de la section nourriture")
    
    try:
        # Connexion à la base de données
        db = connect_to_database()
        
        # Comparer et mettre à jour
        corrections, additions = compare_and_update_nourriture(db)
        
        if corrections > 0 or additions > 0:
            logger.info(f"🎉 Révision orthographique terminée avec succès!")
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