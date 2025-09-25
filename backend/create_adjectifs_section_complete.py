#!/usr/bin/env python3
"""
Script pour créer la section "adjectifs" avec les données du tableau fourni
et intégrer les prononciations audio.
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

# Données adjectifs extraites du tableau
ADJECTIFS_DATA = [
    {"french": "grand", "shimaoré": "bolé", "kibouchi": "bé"},
    {"french": "petit", "shimaoré": "titi", "kibouchi": "héli"},
    {"french": "gros", "shimaoré": "mtronga/tronga", "kibouchi": "bé"},
    {"french": "maigre", "shimaoré": "tsala", "kibouchi": "mahia"},
    {"french": "fort", "shimaoré": "ouna ngouvou", "kibouchi": "missi ngouvou"},
    {"french": "dur", "shimaoré": "mangavou", "kibouchi": "mahéri"},
    {"french": "mou", "shimaoré": "trémboivou", "kibouchi": "malémi"},
    {"french": "beau/jolie", "shimaoré": "mzouri", "kibouchi": "zatovou"},
    {"french": "laid", "shimaoré": "tsi ndzouzouri", "kibouchi": "ratsi sora"},
    {"french": "jeune", "shimaoré": "nrétsa", "kibouchi": "zaza"},
    {"french": "vieux", "shimaoré": "dhouha", "kibouchi": "héla"},
    {"french": "gentil", "shimaoré": "mwéma", "kibouchi": "tsara rohou"},
    {"french": "méchant", "shimaoré": "mbovou", "kibouchi": "ratsi rohou"},
    {"french": "intelligent", "shimaoré": "mstanrabou", "kibouchi": "tsara louha"},
    {"french": "bête", "shimaoré": "dhaba", "kibouchi": "dhaba"},
    {"french": "riche", "shimaoré": "tadjiri", "kibouchi": "tadjiri"},
    {"french": "pauvre", "shimaoré": "maskini", "kibouchi": "maskini"},
    {"french": "sérieux", "shimaoré": "kassidi", "kibouchi": "koussoudi"},
    {"french": "drôle", "shimaoré": "outsésa", "kibouchi": "mampimohi"},
    {"french": "calme", "shimaoré": "baridi", "kibouchi": "malémi"},
    {"french": "nerveux", "shimaoré": "oussikitiha", "kibouchi": "téhi téhitri"},
    {"french": "bon", "shimaoré": "mwéma", "kibouchi": "tsara"},
    {"french": "mauvais", "shimaoré": "mbovou", "kibouchi": "mwadéli"},
    {"french": "chaud", "shimaoré": "moro", "kibouchi": "mèyi"},
    {"french": "froid", "shimaoré": "baridi", "kibouchi": "manintsi"},
    {"french": "lourd", "shimaoré": "ndziro", "kibouchi": "mavèchatra"},
    {"french": "léger", "shimaoré": "ndzangou", "kibouchi": "mayivagna"},
    {"french": "propre", "shimaoré": "irahara", "kibouchi": "madiou"},
    {"french": "sale", "shimaoré": "trotro", "kibouchi": "maloutou"},
    {"french": "nouveau", "shimaoré": "piya", "kibouchi": "vowou"},
    {"french": "ancien", "shimaoré": "halé", "kibouchi": "kèyi"},
    {"french": "facile", "shimaoré": "ndzangou", "kibouchi": "mora"},
    {"french": "difficile", "shimaoré": "ndziro", "kibouchi": "mahéri"},
    {"french": "important", "shimaoré": "mouhimou", "kibouchi": "mouhimou"},
    {"french": "inutile", "shimaoré": "kassina mana", "kibouchi": "tsissi fotouni"},
    {"french": "faux", "shimaoré": "trambo", "kibouchi": "vandi"},
    {"french": "vrai", "shimaoré": "kwéli", "kibouchi": "ankitigni"},
    {"french": "ouvert", "shimaoré": "ouboua", "kibouchi": "mibiyangna"},
    {"french": "fermé", "shimaoré": "oubala", "kibouchi": "migadra"},
    {"french": "content", "shimaoré": "oufourahi", "kibouchi": "ravou"},
    {"french": "triste", "shimaoré": "ouna hamo", "kibouchi": "malahélou"},
    {"french": "fatigué", "shimaoré": "ouléméwa", "kibouchi": "vaha"},
    {"french": "colère", "shimaoré": "hadabou", "kibouchi": "méloukou"},
    {"french": "fâché", "shimaoré": "ouja hassira", "kibouchi": "méloukou"},
    {"french": "amoureux", "shimaoré": "ouvendza", "kibouchi": "mitiya"},
    {"french": "inquiet", "shimaoré": "ouna hamo", "kibouchi": "miyéfitri/kouchanga"},
    {"french": "fier", "shimaoré": "oujiviwa", "kibouchi": "ravou"},
    {"french": "honteux", "shimaoré": "ouona haya", "kibouchi": "mampihingnatra"},
    {"french": "surpris", "shimaoré": "oumarouha", "kibouchi": "tèhitri"},
    {"french": "satisfait", "shimaoré": "oufourahi", "kibouchi": "ravou"},
    {"french": "long", "shimaoré": "drilé", "kibouchi": "habou"},
    {"french": "court", "shimaoré": "koutri", "kibouchi": "fohiki"}
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

def get_adjective_emoji(french_name):
    """Retourne un emoji approprié pour l'adjectif donné"""
    emoji_map = {
        "grand": "📏", "petit": "🤏", "gros": "🟡", "maigre": "📏", "fort": "💪", 
        "dur": "🪨", "mou": "🧽", "beau/jolie": "😍", "laid": "😵", "jeune": "👶", 
        "vieux": "👴", "gentil": "😊", "méchant": "😡", "intelligent": "🧠", "bête": "🤪",
        "riche": "💰", "pauvre": "💸", "sérieux": "😐", "drôle": "😂", "calme": "😌",
        "nerveux": "😰", "bon": "👍", "mauvais": "👎", "chaud": "🔥", "froid": "❄️",
        "lourd": "⚖️", "léger": "🪶", "propre": "✨", "sale": "💩", "nouveau": "🆕",
        "ancien": "🕰️", "facile": "✅", "difficile": "❌", "important": "⭐", "inutile": "🗑️",
        "faux": "❌", "vrai": "✅", "ouvert": "🔓", "fermé": "🔒", "content": "😊",
        "triste": "😢", "fatigué": "😴", "colère": "😡", "fâché": "😠", "amoureux": "😍",
        "inquiet": "😟", "fier": "😤", "honteux": "😳", "surpris": "😲", "satisfait": "😌",
        "long": "📏", "court": "📐"
    }
    
    return emoji_map.get(french_name.lower(), "📝")

def copy_audio_files():
    """Copie les fichiers audio dans le bon répertoire"""
    source_dir = "/app/temp_adjectifs_audio/adjectifs_"
    target_dir = "/app/frontend/assets/audio/adjectifs"
    
    # Créer le répertoire cible s'il n'existe pas
    os.makedirs(target_dir, exist_ok=True)
    
    # Copier tous les fichiers
    if os.path.exists(source_dir):
        os.system(f"cp {source_dir}/* {target_dir}/")
        logger.info(f"Fichiers audio copiés de {source_dir} vers {target_dir}")
        
        # Compter les fichiers copiés
        copied_files = len([f for f in os.listdir(target_dir) if f.endswith('.m4a')])
        logger.info(f"Total fichiers audio copiés: {copied_files}")
        return True
    else:
        logger.error(f"Répertoire source introuvable: {source_dir}")
        return False

def normalize_text_for_matching(text):
    """Normalise le texte pour la correspondance avec les fichiers audio"""
    if not text:
        return ""
    
    text = text.lower()
    # Remplacements spéciaux
    replacements = {
        '/': '_', '(': '', ')': '', ' ': '_',
        'é': 'e', 'è': 'e', 'à': 'a', 'ç': 'c'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text.strip()

def find_audio_correspondences(adjectifs, audio_files):
    """Trouve les correspondances entre adjectifs et fichiers audio"""
    
    # Créer un dictionnaire des fichiers audio sans extension
    audio_dict = {}
    for audio_file in audio_files:
        base_name = os.path.splitext(audio_file)[0]
        normalized = normalize_text_for_matching(base_name)
        audio_dict[normalized] = audio_file
    
    matches = {}
    unmatched_adjectifs = []
    
    logger.info("=== ANALYSE DES CORRESPONDANCES AUDIO ADJECTIFS ===")
    
    for adj in adjectifs:
        french = adj["french"]
        shimaore = adj["shimaoré"]
        kibouchi = adj["kibouchi"]
        
        matched_file = None
        match_source = None
        
        # Essayer différentes variantes
        variants = [shimaore, kibouchi]
        
        for variant in variants:
            if variant:
                # Normaliser et chercher
                normalized_variant = normalize_text_for_matching(variant)
                if normalized_variant in audio_dict:
                    matched_file = audio_dict[normalized_variant]
                    match_source = f"'{variant}'"
                    break
        
        if matched_file:
            matches[french] = {
                'adjectif': adj,
                'audio_file': matched_file,
                'match_source': match_source
            }
            logger.info(f"✅ {french:15} | {match_source} → {matched_file}")
        else:
            unmatched_adjectifs.append(adj)
            logger.warning(f"❌ {french:15} | Aucun audio trouvé")
    
    return matches, unmatched_adjectifs

def create_adjectifs_section(db):
    """Crée la section adjectifs dans la base de données"""
    collection = db['vocabulary']
    
    # Supprimer l'ancienne section adjectifs si elle existe
    result = collection.delete_many({"section": "adjectifs"})
    logger.info(f"Anciens enregistrements adjectifs supprimés: {result.deleted_count}")
    
    # Lister les fichiers audio disponibles
    audio_dir = "/app/frontend/assets/audio/adjectifs"
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')] if os.path.exists(audio_dir) else []
    
    # Trouver les correspondances audio
    matches, unmatched = find_audio_correspondences(ADJECTIFS_DATA, audio_files)
    
    # Préparer les nouveaux documents
    new_documents = []
    for adj_data in ADJECTIFS_DATA:
        french = adj_data["french"]
        emoji = get_adjective_emoji(french)
        
        # Vérifier s'il y a une correspondance audio
        has_audio = french in matches
        audio_path = ""
        if has_audio:
            audio_path = f"audio/adjectifs/{matches[french]['audio_file']}"
        
        document = {
            "section": "adjectifs",
            "french": french,
            "shimaoré": adj_data["shimaoré"],
            "kibouchi": adj_data["kibouchi"],
            "emoji": emoji,
            "has_authentic_audio": has_audio,
            "audio_authentic": audio_path if has_audio else "",
            "audio_updated": has_audio,
            "audio_format": "m4a" if has_audio else "",
            "audio_shimaoré": f"audio/{french.lower().replace(' ', '_').replace('/', '_')}_shimaoré.mp3",
            "audio_kibouchi": f"audio/{french.lower().replace(' ', '_').replace('/', '_')}_kibouchi.mp3"
        }
        new_documents.append(document)
    
    # Insérer les nouveaux documents
    if new_documents:
        result = collection.insert_many(new_documents)
        logger.info(f"Section adjectifs créée avec {len(result.inserted_ids)} mots")
        
        # Statistiques
        with_audio = len(matches)
        coverage = (with_audio / len(new_documents)) * 100 if new_documents else 0
        
        logger.info(f"Adjectifs avec audio: {with_audio}/{len(new_documents)} ({coverage:.1f}%)")
        
        return len(result.inserted_ids), with_audio
    
    return 0, 0

def main():
    """Fonction principale"""
    logger.info("Début de la création de la section adjectifs")
    
    try:
        # Copier les fichiers audio
        if not copy_audio_files():
            return 1
        
        # Connexion à la base de données
        db = connect_to_database()
        
        # Créer la section adjectifs
        total_created, with_audio = create_adjectifs_section(db)
        
        # Résumé final
        logger.info(f"\n{'='*60}")
        logger.info("RÉSUMÉ CRÉATION SECTION ADJECTIFS")
        logger.info(f"{'='*60}")
        logger.info(f"Total adjectifs créés: {total_created}")
        logger.info(f"Avec audio authentique: {with_audio}")
        logger.info(f"Couverture audio: {(with_audio/total_created)*100:.1f}%" if total_created > 0 else "0%")
        logger.info(f"Fichiers audio disponibles: 91")
        
        if total_created > 0:
            logger.info("🎉 Section adjectifs créée avec succès!")
        else:
            logger.warning("⚠️ Échec de la création de la section adjectifs")
            
    except Exception as e:
        logger.error(f"Erreur dans le script principal: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())