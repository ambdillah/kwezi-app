#!/usr/bin/env python3
"""
Script pour créer les sections manquantes dans la base de données:
- corps (corps humain)
- salutations

En se basant sur les fichiers audio disponibles pour identifier les mots.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging
import glob

# Charger les variables d'environnement
load_dotenv()

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

def get_emoji_for_body_part(name):
    """Retourne un emoji approprié pour une partie du corps"""
    body_parts_emojis = {
        # Tête et visage
        "angofou": "👤", "ankwéssi": "👤", "cha": "👤", "dhomo": "👤", 
        "hangno": "👤", "haveyi": "👤", "hifi": "👤", "horougnou": "👤", 
        "poua": "👤", "shidzé-mvoumo": "👤", "shitsoi": "👤", "tsingo": "👤",
        
        # Membres et corps
        "bavou": "🦵", "bèga": "🦵", "fagnéva": "💪", "faninti": "🤚", 
        "fifi": "💪", "fouri": "🦵", "kiyo": "👁️", "kofou": "🦴", 
        "komoi": "🦴", "kové": "🦴", "kwendzé": "🦴", "lahara": "🦴",
        "louha": "🦴", "lèla": "🦴", "magno": "🦴", "matso": "👁️", 
        "mbavou": "🦵", "mbo": "🦵", "mengo": "🦴", "mhono": "🤚", 
        "mimba": "🦴", "mindrou": "🦴", "ndrévou": "🦴", "ndzigni": "🦴", 
        "ngnélé": "🦴", "ngwezi": "🦴", "oulimé": "🦴", "rambou": "🤚",
        
        # Corps général
        "savou": "🦴", "shlévou": "🦴", "sokou": "🦴", "somboutrou": "🦴", 
        "soufigni": "🦴", "soungni": "🦴", "tagnana": "🦴", "tahezagna": "🦴", 
        "tingui": "🦴", "tondrou": "🦴", "trenga": "🦴", "tsi": "🦴",
        "vava": "🦴", "viti": "🦴", "vohou": "🦴", "vouancarou": "🦴", 
        "vouzougnou": "🦴", "housso": "🦴", "kaboudzi": "🦴", "kibou": "🦴", 
        "kitoika": "🦴"
    }
    
    name_lower = name.lower().replace('.m4a', '')
    return body_parts_emojis.get(name_lower, "🦴")

def get_emoji_for_greeting(name):
    """Retourne un emoji approprié pour une salutation"""
    greetings_emojis = {
        "akori": "👋", "an_ha": "👋", "ewa": "👋", "fétré": "👋", 
        "haligni": "👋", "iya": "👋", "jéjé": "👋", "kwaheri": "👋", 
        "kwezi": "👋", "maeva": "👋", "maèva": "👋", "marahaba": "👋", 
        "oukou": "👋", "tsara": "👋"
    }
    
    name_lower = name.lower().replace('.m4a', '').replace('_', ' ')
    return greetings_emojis.get(name_lower, "👋")

def create_corps_section(db):
    """Crée la section corps humain basée sur les fichiers audio"""
    
    # Mapping basé sur l'analyse des noms de fichiers et la connaissance du shimaoré/kibouchi
    corps_data = [
        {"french": "œil", "shimaoré": "matso", "kibouchi": "kiyo", "audio_file": "Matso.m4a"},
        {"french": "bouche", "shimaoré": "cha", "kibouchi": "cha", "audio_file": "Cha.m4a"},
        {"french": "nez", "shimaoré": "poua", "kibouchi": "poua", "audio_file": "Poua.m4a"},
        {"french": "tête", "shimaoré": "dhomo", "kibouchi": "tsingo", "audio_file": "Dhomo.m4a"},
        {"french": "cheveux", "shimaoré": "tsingo", "kibouchi": "tsingo", "audio_file": "Tsingo.m4a"},
        {"french": "main", "shimaoré": "faninti", "kibouchi": "mhono", "audio_file": "Faninti.m4a"},
        {"french": "pied", "shimaoré": "bavou", "kibouchi": "bavou", "audio_file": "Bavou.m4a"},
        {"french": "jambe", "shimaoré": "mbavou", "kibouchi": "mbavou", "audio_file": "Mbavou.m4a"},
        {"french": "bras", "shimaoré": "mbo", "kibouchi": "mbo", "audio_file": "Mbo.m4a"},
        {"french": "cou", "shimaoré": "shitsoi", "kibouchi": "shitsoi", "audio_file": "Shitsoi.m4a"},
        {"french": "dos", "shimaoré": "shlévou", "kibouchi": "shlévou", "audio_file": "Shlévou.m4a"},
        {"french": "ventre", "shimaoré": "sokou", "kibouchi": "sokou", "audio_file": "Sokou.m4a"},
        {"french": "cœur", "shimaoré": "soufigni", "kibouchi": "soufigni", "audio_file": "Soufigni.m4a"},
        {"french": "oreille", "shimaoré": "soungni", "kibouchi": "soungni", "audio_file": "Soungni.m4a"},
        {"french": "dent", "shimaoré": "mengo", "kibouchi": "mengo", "audio_file": "Mengo.m4a"},
        {"french": "langue", "shimaoré": "lèla", "kibouchi": "lèla", "audio_file": "Lèla.m4a"},
        {"french": "doigt", "shimaoré": "tingui", "kibouchi": "tingui", "audio_file": "Tingui.m4a"},
        {"french": "ongle", "shimaoré": "dzitso la pwédza", "kibouchi": "dzitso la pwédza", "audio_file": "Dzitso la pwédza.m4a"},
        {"french": "genou", "shimaoré": "trenga", "kibouchi": "trenga", "audio_file": "Trenga.m4a"},
        {"french": "coude", "shimaoré": "kové", "kibouchi": "kové", "audio_file": "Kové.m4a"}
    ]
    
    collection = db['vocabulary']
    
    # Supprimer l'ancienne section si elle existe
    result = collection.delete_many({"section": "corps"})
    logger.info(f"Anciens enregistrements corps supprimés: {result.deleted_count}")
    
    # Préparer les nouveaux documents
    new_documents = []
    for item in corps_data:
        emoji = get_emoji_for_body_part(item["audio_file"])
        
        document = {
            "section": "corps",
            "french": item["french"],
            "shimaoré": item["shimaoré"],
            "kibouchi": item["kibouchi"],
            "emoji": emoji,
            "audio_authentic": f"audio/corps/{item['audio_file']}",
            "has_authentic_audio": True,
            "audio_updated": True
        }
        new_documents.append(document)
    
    # Insérer les nouveaux documents
    if new_documents:
        result = collection.insert_many(new_documents)
        logger.info(f"Section corps créée avec {len(result.inserted_ids)} entrées")
        return len(result.inserted_ids)
    
    return 0

def create_salutations_section(db):
    """Crée la section salutations basée sur les fichiers audio"""
    
    salutations_data = [
        {"french": "bonjour", "shimaoré": "marahaba", "kibouchi": "akori", "audio_file": "Marahaba.m4a"},
        {"french": "bonsoir", "shimaoré": "haligni tsara", "kibouchi": "haligni tsara", "audio_file": "Haligni tsara.m4a"},
        {"french": "au revoir", "shimaoré": "kwaheri", "kibouchi": "kwaheri", "audio_file": "Kwaheri.m4a"},
        {"french": "bien", "shimaoré": "tsara", "kibouchi": "tsara", "audio_file": "Tsara.m4a"},
        {"french": "bienvenue", "shimaoré": "maeva", "kibouchi": "maeva", "audio_file": "Maeva.m4a"},
        {"french": "merci", "shimaoré": "iya", "kibouchi": "iya", "audio_file": "Iya.m4a"},
        {"french": "excusez-moi", "shimaoré": "jéjé", "kibouchi": "jéjé", "audio_file": "Jéjé.m4a"},
        {"french": "comment allez-vous", "shimaoré": "oukou wa hairi", "kibouchi": "oukou wa hairi", "audio_file": "Oukou wa hairi.m4a"},
        {"french": "salut", "shimaoré": "kwezi", "kibouchi": "kwezi", "audio_file": "Kwezi.m4a"}
    ]
    
    collection = db['vocabulary']
    
    # Supprimer l'ancienne section si elle existe
    result = collection.delete_many({"section": "salutations"})
    logger.info(f"Anciens enregistrements salutations supprimés: {result.deleted_count}")
    
    # Préparer les nouveaux documents
    new_documents = []
    for item in salutations_data:
        emoji = get_emoji_for_greeting(item["audio_file"])
        
        document = {
            "section": "salutations",
            "french": item["french"],
            "shimaoré": item["shimaoré"],
            "kibouchi": item["kibouchi"],
            "emoji": emoji,
            "audio_authentic": f"audio/salutations/{item['audio_file']}",
            "has_authentic_audio": True,
            "audio_updated": True
        }
        new_documents.append(document)
    
    # Insérer les nouveaux documents
    if new_documents:
        result = collection.insert_many(new_documents)
        logger.info(f"Section salutations créée avec {len(result.inserted_ids)} entrées")
        return len(result.inserted_ids)
    
    return 0

def main():
    """Fonction principale"""
    logger.info("Début de la création des sections manquantes")
    
    try:
        # Connexion à la base de données
        db = connect_to_database()
        
        # Créer les sections
        corps_count = create_corps_section(db)
        salutations_count = create_salutations_section(db)
        
        logger.info(f"\n{'='*50}")
        logger.info("RÉSUMÉ DE CRÉATION")
        logger.info(f"{'='*50}")
        logger.info(f"Section corps: {corps_count} mots créés")
        logger.info(f"Section salutations: {salutations_count} mots créés")
        logger.info(f"Total: {corps_count + salutations_count} mots ajoutés")
        
        if corps_count > 0 and salutations_count > 0:
            logger.info("🎉 Toutes les sections ont été créées avec succès!")
        else:
            logger.warning("⚠️ Certaines sections n'ont pas pu être créées")
        
    except Exception as e:
        logger.error(f"Erreur dans le script principal: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())