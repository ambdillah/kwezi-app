#!/usr/bin/env python3
"""
Test direct de l'API audio avec les vrais IDs
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import requests
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
        return db
    except Exception as e:
        logger.error(f"Erreur de connexion à la base de données: {e}")
        raise

def test_api_with_real_ids():
    """Teste l'API avec de vrais IDs"""
    logger.info("🧪 TEST API AUDIO AVEC VRAIS IDS")
    
    db = connect_to_database()
    collection = db['vocabulary']
    
    # Récupérer quelques verbes avec audio
    test_verbs = list(collection.find({
        "section": "verbes",
        "has_shimaoré_audio": True,
        "audio_shimaoré_filename": {"$ne": None}
    }).limit(3))
    
    logger.info(f"Verbes de test trouvés: {len(test_verbs)}")
    
    for verb in test_verbs:
        verb_id = str(verb['_id'])
        french = verb.get('french', 'N/A')
        shimaore_file = verb.get('audio_shimaoré_filename')
        
        logger.info(f"\n🧪 Test verbe: {french}")
        logger.info(f"   ID: {verb_id}")
        logger.info(f"   Fichier: {shimaore_file}")
        
        # Tester l'API
        api_url = f"http://localhost:8001/api/words/{verb_id}/audio/shimaore"
        
        try:
            response = requests.get(api_url, timeout=5)
            
            logger.info(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                logger.info(f"   ✅ API FONCTIONNE!")
                logger.info(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
                logger.info(f"   Content-Length: {len(response.content)} bytes")
                
                # Sauvegarder un fichier test
                test_file = f"/tmp/test_{french}.m4a"
                with open(test_file, 'wb') as f:
                    f.write(response.content)
                logger.info(f"   📁 Fichier sauvé: {test_file}")
                
            else:
                logger.error(f"   ❌ ERREUR: {response.text}")
                
        except Exception as e:
            logger.error(f"   ❌ Exception: {e}")

def test_api_info_endpoint():
    """Teste l'endpoint d'info audio"""
    logger.info("\n🧪 TEST ENDPOINT INFO AUDIO")
    
    db = connect_to_database()
    collection = db['vocabulary']
    
    test_verb = collection.find_one({
        "section": "verbes",
        "french": "voir"
    })
    
    if test_verb:
        verb_id = str(test_verb['_id'])
        api_url = f"http://localhost:8001/api/words/{verb_id}/audio"
        
        try:
            response = requests.get(api_url, timeout=5)
            logger.info(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Info API fonctionne:")
                logger.info(f"   Dual system: {data.get('dual_audio_system', False)}")
                logger.info(f"   Shimaoré: {data.get('audio', {}).get('shimaore', {})}")
                logger.info(f"   Kibouchi: {data.get('audio', {}).get('kibouchi', {})}")
            else:
                logger.error(f"❌ Erreur info API: {response.text}")
                
        except Exception as e:
            logger.error(f"❌ Exception info API: {e}")

def main():
    """Fonction principale"""
    logger.info("🎯 TEST DIRECT API AUDIO")
    
    try:
        test_api_with_real_ids()
        test_api_info_endpoint()
        
        logger.info(f"\n{'='*60}")
        logger.info("CONCLUSION TEST API")
        logger.info(f"{'='*60}")
        logger.info("Si l'API fonctionne en local mais pas dans l'app,")
        logger.info("le problème est côté frontend (cache, URLs, etc.)")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)