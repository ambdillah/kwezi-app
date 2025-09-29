#!/usr/bin/env python3
"""
Analyse des problèmes actuels dans les correspondances audio des verbes
Vérification détaillée des cas mentionnés par l'utilisateur
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

def analyze_current_database_structure():
    """Analyse la structure actuelle de la base de données des verbes"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("=== ANALYSE STRUCTURE ACTUELLE BASE DE DONNÉES ===")
    
    verbs = list(collection.find({"section": "verbes"}).sort("french", 1))
    
    logger.info(f"Total verbes trouvés: {len(verbs)}")
    
    # Créer un tableau organisé
    logger.info(f"\n{'='*120}")
    logger.info("TABLEAU ORGANISÉ - STRUCTURE ACTUELLE")
    logger.info(f"{'='*120}")
    logger.info(f"{'Français':15} | {'Shimaoré':20} | {'Audio Shimaoré':25} | {'Kibouchi':20} | {'Audio Kibouchi':25}")
    logger.info("-" * 120)
    
    problems_found = []
    duplicate_audio_files = {}
    missing_audio = []
    
    for verb in verbs:
        french = verb.get('french', 'N/A')
        shimaore = verb.get('shimaoré', 'N/A')
        kibouchi = verb.get('kibouchi', 'N/A')
        shimaore_audio = verb.get('audio_shimaoré_filename', 'Aucun')
        kibouchi_audio = verb.get('audio_kibouchi_filename', 'Aucun')
        
        # Afficher la ligne du tableau
        shimaore_display = shimaore if shimaore != 'N/A' else 'N/A'
        kibouchi_display = kibouchi if kibouchi != 'N/A' else 'N/A'
        shimaore_audio_display = shimaore_audio if shimaore_audio != 'Aucun' else 'Aucun'
        kibouchi_audio_display = kibouchi_audio if kibouchi_audio != 'Aucun' else 'Aucun'
        
        logger.info(f"{french:15} | {shimaore_display:20} | {shimaore_audio_display:25} | {kibouchi_display:20} | {kibouchi_audio_display:25}")
        
        # Détecter les problèmes
        
        # 1. Même fichier audio pour deux traductions différentes
        if (shimaore_audio != 'Aucun' and kibouchi_audio != 'Aucun' and 
            shimaore_audio == kibouchi_audio and shimaore.lower() != kibouchi.lower()):
            problems_found.append({
                'type': 'duplicate_audio',
                'french': french,
                'shimaore': shimaore,
                'kibouchi': kibouchi,
                'audio_file': shimaore_audio
            })
        
        # 2. Compter l'usage de chaque fichier audio
        if shimaore_audio != 'Aucun':
            if shimaore_audio not in duplicate_audio_files:
                duplicate_audio_files[shimaore_audio] = []
            duplicate_audio_files[shimaore_audio].append(f"{french} (shimaoré: {shimaore})")
            
        if kibouchi_audio != 'Aucun':
            if kibouchi_audio not in duplicate_audio_files:
                duplicate_audio_files[kibouchi_audio] = []
            duplicate_audio_files[kibouchi_audio].append(f"{french} (kibouchi: {kibouchi})")
        
        # 3. Vérifications spéciales pour les cas mentionnés
        if french == "attendre" and shimaore == "oulindra":
            logger.info(f"\n🔍 CAS SPÉCIAL 'ATTENDRE/OULINDRA':")
            logger.info(f"  Shimaoré: {shimaore} → {shimaore_audio}")
            logger.info(f"  Kibouchi: {kibouchi} → {kibouchi_audio}")
        
        if "ouzia" in shimaore.lower() or "ouziya" in shimaore.lower():
            logger.info(f"\n🔍 CAS SPÉCIAL 'OUZIA/OUZIYA':")
            logger.info(f"  Français: {french}")
            logger.info(f"  Shimaoré: {shimaore} → {shimaore_audio}")
            logger.info(f"  Kibouchi: {kibouchi} → {kibouchi_audio}")
    
    return problems_found, duplicate_audio_files

def check_available_audio_files():
    """Vérifie les fichiers audio réellement disponibles"""
    audio_dir = "/app/frontend/assets/audio/verbes"
    
    logger.info(f"\n=== FICHIERS AUDIO DISPONIBLES ===")
    
    if not os.path.exists(audio_dir):
        logger.error(f"Répertoire audio non trouvé: {audio_dir}")
        return []
    
    available_files = []
    
    for filename in sorted(os.listdir(audio_dir)):
        if filename.lower().endswith(('.m4a', '.mp3', '.wav')):
            file_path = os.path.join(audio_dir, filename)
            file_size = os.path.getsize(file_path)
            available_files.append(filename)
            
            # Chercher spécialement les fichiers mentionnés
            name_lower = filename.lower()
            if 'oulindra' in name_lower:
                logger.info(f"📁 TROUVÉ: {filename} ({file_size} bytes) - pour 'oulindra'")
            if 'mandigni' in name_lower:
                logger.info(f"📁 TROUVÉ: {filename} ({file_size} bytes) - pour 'mandigni'")
            if 'ouziya' in name_lower or 'ouzia' in name_lower:
                logger.info(f"📁 TROUVÉ: {filename} ({file_size} bytes) - pour 'ouziya'")
    
    logger.info(f"Total fichiers audio disponibles: {len(available_files)}")
    
    return available_files

def find_specific_issues():
    """Recherche les problèmes spécifiques mentionnés par l'utilisateur"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info(f"\n=== RECHERCHE PROBLÈMES SPÉCIFIQUES ===")
    
    # 1. Problème "oulindra" vs "mandigni"
    logger.info(f"\n🔍 PROBLÈME 1: 'oulindra' vs 'mandigni'")
    
    oulindra_verb = collection.find_one({
        "section": "verbes",
        "shimaoré": {"$regex": "oulindra", "$options": "i"}
    })
    
    mandigni_verb = collection.find_one({
        "section": "verbes",
        "kibouchi": {"$regex": "mandigni", "$options": "i"}
    })
    
    if oulindra_verb:
        logger.info(f"  Verbe avec 'oulindra': {oulindra_verb.get('french', 'N/A')}")
        logger.info(f"    Shimaoré: {oulindra_verb.get('shimaoré', 'N/A')} → {oulindra_verb.get('audio_shimaoré_filename', 'Aucun')}")
        logger.info(f"    Kibouchi: {oulindra_verb.get('kibouchi', 'N/A')} → {oulindra_verb.get('audio_kibouchi_filename', 'Aucun')}")
    
    if mandigni_verb:
        logger.info(f"  Verbe avec 'mandigni': {mandigni_verb.get('french', 'N/A')}")
        logger.info(f"    Shimaoré: {mandigni_verb.get('shimaoré', 'N/A')} → {mandigni_verb.get('audio_shimaoré_filename', 'Aucun')}")
        logger.info(f"    Kibouchi: {mandigni_verb.get('kibouchi', 'N/A')} → {mandigni_verb.get('audio_kibouchi_filename', 'Aucun')}")
    
    # Vérifier s'ils utilisent le même fichier
    if (oulindra_verb and mandigni_verb and 
        oulindra_verb.get('audio_shimaoré_filename') == mandigni_verb.get('audio_kibouchi_filename')):
        logger.info(f"  ❌ PROBLÈME CONFIRMÉ: Même fichier audio utilisé!")
        logger.info(f"     Fichier en commun: {oulindra_verb.get('audio_shimaoré_filename')}")
    
    # 2. Problème "ouziya" manquant
    logger.info(f"\n🔍 PROBLÈME 2: 'ouziya' manquant")
    
    ouziya_verb = collection.find_one({
        "section": "verbes",
        "shimaoré": {"$regex": "ouziya", "$options": "i"}
    })
    
    if ouziya_verb:
        logger.info(f"  Verbe avec 'ouziya': {ouziya_verb.get('french', 'N/A')}")
        logger.info(f"    Shimaoré: {ouziya_verb.get('shimaoré', 'N/A')} → {ouziya_verb.get('audio_shimaoré_filename', 'Aucun')}")
        
        if ouziya_verb.get('audio_shimaoré_filename', 'Aucun') == 'Aucun':
            logger.info(f"  ❌ PROBLÈME CONFIRMÉ: Pas d'audio pour 'ouziya'")
            
            # Chercher si le fichier existe
            audio_dir = "/app/frontend/assets/audio/verbes"
            for filename in os.listdir(audio_dir):
                if 'ouziya' in filename.lower():
                    logger.info(f"     📁 FICHIER TROUVÉ: {filename}")
    else:
        logger.info(f"  ⚠️ Verbe avec 'ouziya' non trouvé dans la base")

def check_audio_file_duplicates(duplicate_audio_files):
    """Analyse les fichiers audio utilisés plusieurs fois"""
    logger.info(f"\n=== FICHIERS AUDIO UTILISÉS PLUSIEURS FOIS ===")
    
    duplicates_found = False
    
    for audio_file, usages in duplicate_audio_files.items():
        if len(usages) > 1:
            duplicates_found = True
            logger.info(f"\n🚨 FICHIER DUPLIQUÉ: {audio_file}")
            logger.info(f"   Utilisé par {len(usages)} mots:")
            for usage in usages:
                logger.info(f"     - {usage}")
    
    if not duplicates_found:
        logger.info("✅ Aucun fichier audio dupliqué trouvé")
    
    return duplicates_found

def main():
    """Fonction principale"""
    logger.info("🔍 ANALYSE DES PROBLÈMES AUDIO VERBES")
    
    try:
        # 1. Analyser la structure actuelle
        problems, duplicate_files = analyze_current_database_structure()
        
        # 2. Vérifier les fichiers disponibles
        available_files = check_available_audio_files()
        
        # 3. Rechercher les problèmes spécifiques
        find_specific_issues()
        
        # 4. Analyser les doublons
        duplicates_exist = check_audio_file_duplicates(duplicate_files)
        
        # 5. Résumé
        logger.info(f"\n{'='*80}")
        logger.info("RÉSUMÉ ANALYSE")
        logger.info(f"{'='*80}")
        logger.info(f"Problèmes détectés: {len(problems)}")
        logger.info(f"Fichiers audio disponibles: {len(available_files)}")
        logger.info(f"Fichiers dupliqués: {'Oui' if duplicates_exist else 'Non'}")
        
        logger.info(f"\n💡 RECOMMANDATIONS:")
        logger.info(f"1. Corriger les correspondances pour que chaque traduction ait son propre fichier")
        logger.info(f"2. Vérifier que 'ouziya' ait bien son fichier audio")  
        logger.info(f"3. S'assurer qu'aucun fichier ne soit utilisé pour deux traductions différentes")
        
        return len(problems) == 0
        
    except Exception as e:
        logger.error(f"Erreur dans l'analyse: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)