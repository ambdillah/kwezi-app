#!/usr/bin/env python3
"""
Correction des erreurs 500 de l'API audio
Les correspondances existent mais l'API ne peut pas servir les fichiers
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging
from bson import ObjectId

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

def test_specific_audio_route():
    """Teste une route audio spécifique pour diagnostiquer l'erreur 500"""
    logger.info("🔍 TEST ROUTE AUDIO SPÉCIFIQUE")
    
    db = connect_to_database()
    collection = db['vocabulary']
    
    # Trouver un verbe avec audio pour tester
    test_verb = collection.find_one({
        "section": "verbes",
        "has_shimaoré_audio": True,
        "audio_shimaoré_filename": {"$ne": None}
    })
    
    if test_verb:
        verb_id = str(test_verb['_id'])
        french = test_verb.get('french', 'N/A')
        shimaore_file = test_verb.get('audio_shimaoré_filename')
        
        logger.info(f"📝 Test avec verbe: {french}")
        logger.info(f"   ID: {verb_id}")
        logger.info(f"   Fichier shimaoré: {shimaore_file}")
        
        # Vérifier si le fichier existe physiquement
        if shimaore_file:
            file_path = f"/app/frontend/assets/audio/verbes/{shimaore_file}"
            exists = os.path.exists(file_path)
            file_size = os.path.getsize(file_path) if exists else 0
            
            logger.info(f"   Fichier existe: {'✅' if exists else '❌'}")
            if exists:
                logger.info(f"   Taille: {file_size} bytes")
            
            # Construire l'URL de test
            test_url = f"/api/words/{verb_id}/audio/shimaore"
            logger.info(f"   URL à tester: {test_url}")
            
            return verb_id, shimaore_file, exists
    
    return None, None, False

def check_audio_api_permissions():
    """Vérifier les permissions des fichiers audio"""
    logger.info("\n🔍 VÉRIFICATION PERMISSIONS FICHIERS AUDIO")
    
    audio_dir = "/app/frontend/assets/audio/verbes"
    
    if os.path.exists(audio_dir):
        # Vérifier permissions du répertoire
        dir_perms = oct(os.stat(audio_dir).st_mode)[-3:]
        logger.info(f"📁 Permissions répertoire: {dir_perms}")
        
        # Vérifier quelques fichiers
        files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')][:5]
        
        for file in files:
            file_path = os.path.join(audio_dir, file)
            file_perms = oct(os.stat(file_path).st_mode)[-3:]
            file_size = os.path.getsize(file_path)
            logger.info(f"📄 {file}: perms={file_perms}, taille={file_size}")
    else:
        logger.error(f"❌ Répertoire audio non trouvé: {audio_dir}")

def simulate_api_route():
    """Simule l'exécution de la route API pour identifier l'erreur"""
    logger.info("\n🔍 SIMULATION ROUTE API")
    
    try:
        db = connect_to_database()
        collection = db['vocabulary']
        
        # Simuler la route avec un verbe test
        test_verb = collection.find_one({
            "section": "verbes", 
            "french": "voir"  # Verbe qu'on sait avoir audio
        })
        
        if not test_verb:
            logger.error("❌ Verbe de test non trouvé")
            return False
        
        word_id = str(test_verb['_id'])
        lang = "shimaore"
        
        logger.info(f"🧪 Simulation pour: {test_verb.get('french')} (ID: {word_id})")
        
        # Simuler la logique de l'API
        try:
            # 1. Convertir ObjectId
            obj_id = ObjectId(word_id)
            logger.info("✅ Conversion ObjectId réussie")
            
            # 2. Récupérer le document
            word_doc = collection.find_one({"_id": obj_id})
            if not word_doc:
                logger.error("❌ Document non trouvé")
                return False
            logger.info("✅ Document trouvé")
            
            # 3. Vérifier les champs audio
            if lang == "shimaore":
                filename = word_doc.get("audio_shimaoré_filename")
                has_audio = word_doc.get("has_shimaoré_audio", False)
            else:
                filename = word_doc.get("audio_kibouchi_filename")
                has_audio = word_doc.get("has_kibouchi_audio", False)
            
            logger.info(f"   Nom fichier: {filename}")
            logger.info(f"   Has audio: {has_audio}")
            
            if not filename or not has_audio:
                logger.warning("⚠️ Pas de fichier audio configuré")
                return False
            
            # 4. Vérifier le fichier physique
            file_path = f"/app/frontend/assets/audio/verbes/{filename}"
            if not os.path.exists(file_path):
                logger.error(f"❌ Fichier physique non trouvé: {file_path}")
                return False
            
            logger.info(f"✅ Fichier physique trouvé: {file_path}")
            
            # 5. Vérifier la taille
            file_size = os.path.getsize(file_path)
            logger.info(f"✅ Taille fichier: {file_size} bytes")
            
            if file_size == 0:
                logger.error("❌ Fichier vide")
                return False
            
            logger.info("🎉 SIMULATION RÉUSSIE - L'API devrait fonctionner")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur dans la simulation: {e}")
            return False
        
    except Exception as e:
        logger.error(f"❌ Erreur générale simulation: {e}")
        return False

def check_fastapi_imports():
    """Vérifier les imports FastAPI dans server.py"""
    logger.info("\n🔍 VÉRIFICATION IMPORTS FASTAPI")
    
    server_path = "/app/backend/server.py"
    if os.path.exists(server_path):
        with open(server_path, 'r') as f:
            content = f.read()
            
        # Vérifier les imports nécessaires
        required_imports = [
            'FileResponse',
            'HTTPException',
            'ObjectId'
        ]
        
        for imp in required_imports:
            if imp in content:
                logger.info(f"✅ {imp} importé")
            else:
                logger.warning(f"⚠️ {imp} manquant")
        
        # Vérifier la route audio
        if '/api/words/{word_id}/audio/{lang}' in content:
            logger.info("✅ Route audio définie")
        else:
            logger.warning("⚠️ Route audio manquante")
            
    else:
        logger.error("❌ server.py non trouvé")

def main():
    """Fonction principale de diagnostic"""
    logger.info("🚨 DIAGNOSTIC ERREURS 500 API AUDIO")
    
    try:
        # 1. Tester une route spécifique
        verb_id, filename, file_exists = test_specific_audio_route()
        
        # 2. Vérifier permissions
        check_audio_api_permissions()
        
        # 3. Simuler l'API
        api_works = simulate_api_route()
        
        # 4. Vérifier imports FastAPI
        check_fastapi_imports()
        
        # 5. Résumé diagnostic
        logger.info(f"\n{'='*80}")
        logger.info("RÉSUMÉ DIAGNOSTIC API AUDIO")
        logger.info(f"{'='*80}")
        
        if api_works:
            logger.info("✅ La logique API semble correcte")
            logger.info("🤔 Le problème pourrait être:")
            logger.info("   1. Redémarrage nécessaire du backend")
            logger.info("   2. Cache API")  
            logger.info("   3. Problème de route FastAPI")
        else:
            logger.error("❌ Problème identifié dans la logique API")
        
        logger.info(f"\n🔧 ACTIONS RECOMMANDÉES:")
        logger.info(f"1. Redémarrer le backend")
        logger.info(f"2. Tester manuellement une URL audio")
        logger.info(f"3. Vérifier les logs backend en temps réel")
        
        return api_works
        
    except Exception as e:
        logger.error(f"Erreur dans le diagnostic: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)