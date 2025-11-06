#!/usr/bin/env python3
"""
DIAGNOSTIC D'URGENCE - ÉTAT DE LA BASE DE DONNÉES
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
        logger.info(f"Tentative connexion: {mongo_url}")
        client = MongoClient(mongo_url)
        
        # Tester la connexion
        client.admin.command('ping')
        logger.info("✅ Connexion MongoDB réussie")
        
        db = client['shimaoré_app']
        return db, client
    except Exception as e:
        logger.error(f"❌ Erreur connexion MongoDB: {e}")
        raise

def check_database_status():
    """Vérifier l'état complet de la base de données"""
    logger.info("🔍 DIAGNOSTIC COMPLET BASE DE DONNÉES")
    
    try:
        db, client = connect_to_database()
        
        # Lister toutes les bases de données
        databases = client.list_database_names()
        logger.info(f"Bases de données disponibles: {databases}")
        
        # Vérifier si 'shimaoré_app' existe
        if 'shimaoré_app' in databases:
            logger.info("✅ Base 'shimaoré_app' existe")
            
            # Lister les collections dans cette base
            collections = db.list_collection_names()
            logger.info(f"Collections dans 'shimaoré_app': {collections}")
            
            # Vérifier la collection 'vocabulary'
            if 'vocabulary' in collections:
                logger.info("✅ Collection 'vocabulary' existe")
                
                # Compter les documents
                total_docs = db['vocabulary'].count_documents({})
                logger.info(f"📊 Total documents dans 'vocabulary': {total_docs}")
                
                if total_docs == 0:
                    logger.error("🚨 COLLECTION VIDE - TOUS LES DONNÉES PERDUES")
                    return "EMPTY"
                
                # Compter par section
                sections = db['vocabulary'].distinct("section")
                logger.info(f"Sections trouvées: {sections}")
                
                for section in sections:
                    count = db['vocabulary'].count_documents({"section": section})
                    logger.info(f"  - {section}: {count} mots")
                
                # Vérifier spécifiquement les verbes
                verbs_count = db['vocabulary'].count_documents({"section": "verbes"})
                logger.info(f"\n🎯 VERBES: {verbs_count} documents")
                
                if verbs_count == 0:
                    logger.error("🚨 SECTION VERBES VIDE")
                else:
                    # Vérifier quelques verbes spécifiques
                    test_verbs = ["voir", "attendre", "abîmer", "danser"]
                    for verb in test_verbs:
                        doc = db['vocabulary'].find_one({"section": "verbes", "french": verb})
                        if doc:
                            logger.info(f"  ✅ '{verb}' trouvé: {doc.get('shimaoré', 'N/A')} / {doc.get('kibouchi', 'N/A')}")
                        else:
                            logger.error(f"  ❌ '{verb}' MANQUANT")
                
                return "PARTIAL" if verbs_count < 50 else "OK"
                
            else:
                logger.error("❌ Collection 'vocabulary' N'EXISTE PAS")
                
                # Vérifier s'il y a d'autres collections
                for coll in collections:
                    count = db[coll].count_documents({})
                    logger.info(f"  Collection '{coll}': {count} documents")
                
                return "NO_VOCABULARY"
        else:
            logger.error("❌ Base 'shimaoré_app' N'EXISTE PAS")
            return "NO_DATABASE"
            
    except Exception as e:
        logger.error(f"❌ Erreur vérification base: {e}")
        return "ERROR"

def check_backup_files():
    """Vérifier les fichiers de sauvegarde disponibles"""
    logger.info("\n🔍 VÉRIFICATION SAUVEGARDES DISPONIBLES")
    
    backend_dir = "/app/backend"
    backup_files = []
    
    for file in os.listdir(backend_dir):
        if 'backup' in file.lower() and file.endswith('.json'):
            file_path = os.path.join(backend_dir, file)
            file_size = os.path.getsize(file_path)
            backup_files.append((file, file_size))
    
    if backup_files:
        logger.info(f"✅ {len(backup_files)} sauvegardes trouvées:")
        for backup_file, size in sorted(backup_files):
            logger.info(f"  - {backup_file}: {size:,} bytes")
        return backup_files
    else:
        logger.error("❌ AUCUNE SAUVEGARDE TROUVÉE")
        return []

def check_mongodb_service():
    """Vérifier si MongoDB fonctionne"""
    logger.info("\n🔍 VÉRIFICATION SERVICE MONGODB")
    
    try:
        # Tester la connexion directe
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        logger.info("✅ MongoDB service fonctionne")
        
        # Lister les bases
        dbs = client.list_database_names()
        logger.info(f"Bases disponibles: {dbs}")
        
        return True
    except Exception as e:
        logger.error(f"❌ MongoDB ne répond pas: {e}")
        return False

def emergency_restore_plan():
    """Plan d'urgence pour restaurer les données"""
    logger.info(f"\n🚨 PLAN DE RESTAURATION D'URGENCE")
    
    backup_files = check_backup_files()
    
    if backup_files:
        # Trouver la sauvegarde la plus récente et la plus grande
        latest_backup = max(backup_files, key=lambda x: x[1])  # Plus grande taille
        logger.info(f"💡 RESTAURATION RECOMMANDÉE:")
        logger.info(f"   Fichier: {latest_backup[0]}")
        logger.info(f"   Taille: {latest_backup[1]:,} bytes")
        
        restore_script = f"""
# SCRIPT DE RESTAURATION D'URGENCE
cd /app/backend
python -c "
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv('MONGO_URL'))
db = client['shimaoré_app']

# Charger la sauvegarde
with open('{latest_backup[0]}', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Restaurer les données
if isinstance(data, list):
    result = db['vocabulary'].insert_many(data)
    print(f'Restauré {{len(result.inserted_ids)}} documents')
else:
    print(f'Format de sauvegarde invalide')
"
"""
        
        logger.info(f"\n📋 SCRIPT DE RESTAURATION GÉNÉRÉ")
        
        # Sauvegarder le script
        with open("/app/backend/restore_emergency.py", "w") as f:
            f.write(restore_script)
        
        return True
    else:
        logger.error("❌ IMPOSSIBLE - AUCUNE SAUVEGARDE DISPONIBLE")
        return False

def main():
    """Diagnostic d'urgence principal"""
    logger.info("🚨 DIAGNOSTIC D'URGENCE - PERTE BASE DE DONNÉES SIGNALÉE")
    
    try:
        # 1. Vérifier MongoDB
        mongodb_ok = check_mongodb_service()
        
        if not mongodb_ok:
            logger.error("❌ MONGODB INACCESSIBLE - PROBLÈME SYSTÈME")
            return False
        
        # 2. Vérifier l'état de la base
        db_status = check_database_status()
        
        # 3. Résumé du diagnostic
        logger.info(f"\n{'='*80}")
        logger.info("RÉSUMÉ DIAGNOSTIC")
        logger.info(f"{'='*80}")
        
        if db_status == "OK":
            logger.info("✅ BASE DE DONNÉES NORMALE - FAUSSE ALERTE")
        elif db_status == "PARTIAL":
            logger.warning("⚠️ BASE DE DONNÉES PARTIELLE - DONNÉES PARTIELLES")
        elif db_status == "EMPTY":
            logger.error("🚨 BASE DE DONNÉES VIDE - PERTE TOTALE CONFIRMÉE")
            emergency_restore_plan()
        elif db_status == "NO_VOCABULARY":
            logger.error("🚨 COLLECTION VOCABULARY MANQUANTE")
            emergency_restore_plan()
        elif db_status == "NO_DATABASE":
            logger.error("🚨 BASE SHIMAORÉ_APP MANQUANTE")
            emergency_restore_plan()
        else:
            logger.error("🚨 ERREUR SYSTÈME")
        
        return db_status in ["OK", "PARTIAL"]
        
    except Exception as e:
        logger.error(f"Erreur critique diagnostic: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)