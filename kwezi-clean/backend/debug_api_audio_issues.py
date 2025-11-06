#!/usr/bin/env python3
"""
Debug des problèmes API audio - vérifier si les changements sont réellement appliqués
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

def debug_specific_verbs():
    """Debug des verbes spécifiques mentionnés par l'utilisateur"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("=== DEBUG VERBES SPÉCIFIQUES ===")
    
    # 1. Vérifier "attendre" (oulindra/mandigni)
    logger.info("\n🔍 VERBE 'ATTENDRE' (problème oulindra/mandigni)")
    
    attendre = collection.find_one({
        "section": "verbes",
        "french": "attendre"
    })
    
    if attendre:
        logger.info("Document MongoDB complet:")
        for key, value in attendre.items():
            if 'audio' in key.lower() or key in ['french', 'shimaoré', 'kibouchi', 'has_shimaoré_audio', 'has_kibouchi_audio']:
                logger.info(f"  {key:30} → {value}")
        
        # Vérifier les fichiers physiques
        shimaoré_file = attendre.get('audio_shimaoré_filename')
        kibouchi_file = attendre.get('audio_kibouchi_filename')
        
        if shimaoré_file:
            file_path = f"/app/frontend/assets/audio/verbes/{shimaoré_file}"
            exists = os.path.exists(file_path)
            logger.info(f"  Fichier shimaoré existe: {'✅' if exists else '❌'} {file_path}")
            
        if kibouchi_file:
            file_path = f"/app/frontend/assets/audio/verbes/{kibouchi_file}"
            exists = os.path.exists(file_path)
            logger.info(f"  Fichier kibouchi existe: {'✅' if exists else '❌'} {file_path}")
    
    # 2. Vérifier "abîmer" (oumengna/mandroubaka)
    logger.info("\n🔍 VERBE 'ABÎMER' (problème oumengna/mandroubaka)")
    
    abimer = collection.find_one({
        "section": "verbes",
        "french": "abîmer"
    })
    
    if abimer:
        logger.info("Document MongoDB complet:")
        for key, value in abimer.items():
            if 'audio' in key.lower() or key in ['french', 'shimaoré', 'kibouchi', 'has_shimaoré_audio', 'has_kibouchi_audio']:
                logger.info(f"  {key:30} → {value}")
        
        # Vérifier les fichiers physiques
        shimaoré_file = abimer.get('audio_shimaoré_filename')
        kibouchi_file = abimer.get('audio_kibouchi_filename')
        
        if shimaoré_file:
            file_path = f"/app/frontend/assets/audio/verbes/{shimaoré_file}"
            exists = os.path.exists(file_path)
            logger.info(f"  Fichier shimaoré existe: {'✅' if exists else '❌'} {file_path}")
            
        if kibouchi_file:
            file_path = f"/app/frontend/assets/audio/verbes/{kibouchi_file}"
            exists = os.path.exists(file_path)
            logger.info(f"  Fichier kibouchi existe: {'✅' if exists else '❌'} {file_path}")

def check_api_endpoints():
    """Vérifier les endpoints de l'API"""
    logger.info("\n=== VÉRIFICATION ENDPOINTS API ===")
    
    # Trouver les IDs des verbes problématiques
    db = connect_to_database()
    collection = db['vocabulary']
    
    attendre = collection.find_one({"section": "verbes", "french": "attendre"})
    abimer = collection.find_one({"section": "verbes", "french": "abîmer"})
    
    if attendre:
        verb_id = str(attendre['_id'])
        logger.info(f"\n📡 ENDPOINTS pour 'attendre' (ID: {verb_id}):")
        logger.info(f"  Shimaoré: /api/words/{verb_id}/audio/shimaore")
        logger.info(f"  Kibouchi: /api/words/{verb_id}/audio/kibouchi")
        
        # Vérifier quel fichier devrait être servi
        shimaoré_expected = attendre.get('audio_shimaoré_filename', 'Aucun')
        kibouchi_expected = attendre.get('audio_kibouchi_filename', 'Aucun')
        
        logger.info(f"  Fichier shimaoré attendu: {shimaoré_expected}")
        logger.info(f"  Fichier kibouchi attendu: {kibouchi_expected}")
    
    if abimer:
        verb_id = str(abimer['_id'])
        logger.info(f"\n📡 ENDPOINTS pour 'abîmer' (ID: {verb_id}):")
        logger.info(f"  Shimaoré: /api/words/{verb_id}/audio/shimaore")
        logger.info(f"  Kibouchi: /api/words/{verb_id}/audio/kibouchi")
        
        # Vérifier quel fichier devrait être servi
        shimaoré_expected = abimer.get('audio_shimaoré_filename', 'Aucun')
        kibouchi_expected = abimer.get('audio_kibouchi_filename', 'Aucun')
        
        logger.info(f"  Fichier shimaoré attendu: {shimaoré_expected}")
        logger.info(f"  Fichier kibouchi attendu: {kibouchi_expected}")

def check_backend_api_logic():
    """Vérifier la logique de l'API backend"""
    logger.info("\n=== VÉRIFICATION LOGIQUE API BACKEND ===")
    
    # Chercher les fichiers de l'API
    api_files = [
        "/app/backend/main.py",
        "/app/backend/app.py",
        "/app/backend/server.py"
    ]
    
    for api_file in api_files:
        if os.path.exists(api_file):
            logger.info(f"📄 Fichier API trouvé: {api_file}")
            
            # Lire le contenu pour voir la logique audio
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Chercher les routes audio
            if '/audio/' in content or 'audio' in content:
                logger.info(f"  → Contient de la logique audio")
            
            if 'shimaoré' in content or 'shimaore' in content:
                logger.info(f"  → Gère le shimaoré")
                
            if 'kibouchi' in content:
                logger.info(f"  → Gère le kibouchi")

def check_old_audio_fields():
    """Vérifier s'il reste des anciens champs audio qui interfèrent"""
    logger.info("\n=== VÉRIFICATION ANCIENS CHAMPS AUDIO ===")
    
    db = connect_to_database()
    collection = db['vocabulary']
    
    # Chercher les verbes avec des anciens champs
    verbs_with_old_fields = collection.find({
        "section": "verbes",
        "$or": [
            {"audio_authentic": {"$exists": True, "$ne": None}},
            {"has_authentic_audio": {"$exists": True}},
            {"audio_shimaoré": {"$exists": True}},
            {"audio_kibouchi": {"$exists": True}}
        ]
    })
    
    old_fields_count = 0
    
    for verb in verbs_with_old_fields:
        french = verb.get('french', 'N/A')
        old_fields = []
        
        if verb.get('audio_authentic'):
            old_fields.append(f"audio_authentic: {verb.get('audio_authentic')}")
        if verb.get('has_authentic_audio'):
            old_fields.append(f"has_authentic_audio: {verb.get('has_authentic_audio')}")
        if verb.get('audio_shimaoré') and verb.get('audio_shimaoré') != verb.get('audio_shimaoré_url'):
            old_fields.append(f"audio_shimaoré: {verb.get('audio_shimaoré')}")
        if verb.get('audio_kibouchi') and verb.get('audio_kibouchi') != verb.get('audio_kibouchi_url'):
            old_fields.append(f"audio_kibouchi: {verb.get('audio_kibouchi')}")
        
        if old_fields:
            old_fields_count += 1
            logger.info(f"🚨 {french} a des anciens champs:")
            for field in old_fields:
                logger.info(f"    - {field}")
    
    if old_fields_count == 0:
        logger.info("✅ Aucun ancien champ problématique trouvé")
    else:
        logger.warning(f"⚠️ {old_fields_count} verbes ont des anciens champs qui peuvent interférer")

def main():
    """Fonction principale"""
    logger.info("🔍 DEBUG API AUDIO - PROBLÈMES PERSISTANTS")
    
    try:
        # 1. Vérifier les documents dans la base
        debug_specific_verbs()
        
        # 2. Vérifier les endpoints API
        check_api_endpoints()
        
        # 3. Vérifier la logique backend
        check_backend_api_logic()
        
        # 4. Vérifier les anciens champs
        check_old_audio_fields()
        
        logger.info(f"\n💡 RECOMMANDATIONS:")
        logger.info(f"1. Redémarrer le backend pour purger le cache")
        logger.info(f"2. Vérifier que l'API utilise les nouveaux champs")
        logger.info(f"3. Supprimer les anciens champs qui interfèrent")
        logger.info(f"4. Tester les endpoints directement")
        
    except Exception as e:
        logger.error(f"Erreur dans le debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()