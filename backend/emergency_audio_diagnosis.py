#!/usr/bin/env python3
"""
DIAGNOSTIC D'URGENCE - Vérification des correspondances audio perdues
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

def check_current_audio_state():
    """Vérifier l'état actuel des correspondances audio"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("🚨 DIAGNOSTIC D'URGENCE - ÉTAT ACTUEL DES AUDIO")
    
    # Vérifier les verbes spécifiquement
    verbs = list(collection.find({"section": "verbes"}))
    
    logger.info(f"\n=== ANALYSE VERBES ===")
    logger.info(f"Total verbes: {len(verbs)}")
    
    # Compter les verbes avec/sans audio
    verbs_with_shimaore_audio = 0
    verbs_with_kibouchi_audio = 0
    verbs_without_any_audio = 0
    
    logger.info(f"\n{'Français':20} | {'Shimaoré Audio':25} | {'Kibouchi Audio':25} | {'État'}")
    logger.info("-" * 100)
    
    for verb in verbs:
        french = verb.get('french', 'N/A')
        shimaore_audio = verb.get('audio_shimaoré_filename', 'Aucun')
        kibouchi_audio = verb.get('audio_kibouchi_filename', 'Aucun')
        
        has_shimaore = shimaore_audio != 'Aucun' and shimaore_audio is not None
        has_kibouchi = kibouchi_audio != 'Aucun' and kibouchi_audio is not None
        
        if has_shimaore:
            verbs_with_shimaore_audio += 1
        if has_kibouchi:
            verbs_with_kibouchi_audio += 1
        if not has_shimaore and not has_kibouchi:
            verbs_without_any_audio += 1
        
        if not has_shimaore and not has_kibouchi:
            status = "🚨 SANS AUDIO"
        elif has_shimaore and has_kibouchi:
            status = "✅ COMPLET"
        else:
            status = "⚠️ PARTIEL"
        
        logger.info(f"{french:20} | {shimaore_audio:25} | {kibouchi_audio:25} | {status}")
    
    logger.info(f"\n📊 STATISTIQUES:")
    logger.info(f"  Verbes avec audio shimaoré: {verbs_with_shimaore_audio}")
    logger.info(f"  Verbes avec audio kibouchi: {verbs_with_kibouchi_audio}")
    logger.info(f"  Verbes SANS AUCUN audio: {verbs_without_any_audio}")
    
    return verbs_with_shimaore_audio, verbs_with_kibouchi_audio, verbs_without_any_audio

def check_audio_files_on_disk():
    """Vérifier les fichiers audio présents sur le disque"""
    logger.info(f"\n=== VÉRIFICATION FICHIERS AUDIO SUR DISQUE ===")
    
    audio_dir = "/app/frontend/assets/audio/verbes"
    if os.path.exists(audio_dir):
        files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
        logger.info(f"Fichiers .m4a trouvés: {len(files)}")
        
        # Afficher quelques exemples
        logger.info("Exemples de fichiers:")
        for i, file in enumerate(sorted(files)[:20]):
            logger.info(f"  {i+1}. {file}")
        
        if len(files) > 20:
            logger.info(f"  ... et {len(files) - 20} autres fichiers")
        
        return len(files)
    else:
        logger.error(f"❌ Répertoire audio non trouvé: {audio_dir}")
        return 0

def check_backup_files():
    """Vérifier s'il existe des fichiers de sauvegarde"""
    logger.info(f"\n=== VÉRIFICATION FICHIERS DE SAUVEGARDE ===")
    
    backend_dir = "/app/backend"
    backup_files = []
    
    for file in os.listdir(backend_dir):
        if 'backup' in file.lower() and file.endswith('.json'):
            backup_files.append(file)
    
    if backup_files:
        logger.info(f"✅ Fichiers de sauvegarde trouvés: {len(backup_files)}")
        for backup in sorted(backup_files):
            file_path = os.path.join(backend_dir, backup)
            file_size = os.path.getsize(file_path)
            logger.info(f"  - {backup} ({file_size} bytes)")
    else:
        logger.warning("⚠️ Aucun fichier de sauvegarde trouvé")
    
    return backup_files

def check_zip_extracts():
    """Vérifier les extraits des ZIP"""
    logger.info(f"\n=== VÉRIFICATION EXTRAITS ZIP PRÉCÉDENTS ===")
    
    backend_dir = "/app/backend"
    zip_dirs = []
    
    for item in os.listdir(backend_dir):
        if 'extract' in item.lower() and os.path.isdir(os.path.join(backend_dir, item)):
            zip_dirs.append(item)
    
    if zip_dirs:
        logger.info(f"✅ Répertoires d'extraction trouvés: {len(zip_dirs)}")
        for zip_dir in sorted(zip_dirs):
            dir_path = os.path.join(backend_dir, zip_dir)
            # Compter les fichiers .m4a
            m4a_count = 0
            for root, dirs, files in os.walk(dir_path):
                m4a_count += len([f for f in files if f.endswith('.m4a')])
            logger.info(f"  - {zip_dir}: {m4a_count} fichiers .m4a")
    else:
        logger.warning("⚠️ Aucun répertoire d'extraction trouvé")
    
    return zip_dirs

def main():
    """Fonction principale de diagnostic"""
    logger.info("🚨 DIAGNOSTIC D'URGENCE - CORRESPONDANCES AUDIO PERDUES")
    
    try:
        # 1. Vérifier l'état actuel en base
        shimaore_count, kibouchi_count, no_audio_count = check_current_audio_state()
        
        # 2. Vérifier les fichiers sur disque
        disk_files_count = check_audio_files_on_disk()
        
        # 3. Vérifier les sauvegardes
        backup_files = check_backup_files()
        
        # 4. Vérifier les extraits ZIP
        zip_dirs = check_zip_extracts()
        
        # 5. Résumé du problème
        logger.info(f"\n{'='*80}")
        logger.info("RÉSUMÉ DU PROBLÈME")
        logger.info(f"{'='*80}")
        
        if no_audio_count > 50:  # Si plus de 50 verbes n'ont pas d'audio
            logger.error(f"🚨 PROBLÈME CONFIRMÉ:")
            logger.error(f"  {no_audio_count} verbes SANS AUCUN audio")
            logger.error(f"  Seuls {shimaore_count} verbes ont audio shimaoré")
            logger.error(f"  Seuls {kibouchi_count} verbes ont audio kibouchi")
        
        logger.info(f"\n💡 RESSOURCES DISPONIBLES POUR RESTAURATION:")
        logger.info(f"  - Fichiers audio sur disque: {disk_files_count}")
        logger.info(f"  - Fichiers de sauvegarde: {len(backup_files)}")
        logger.info(f"  - Répertoires ZIP: {len(zip_dirs)}")
        
        # Diagnostic des causes possibles
        logger.info(f"\n⚠️ CAUSES POSSIBLES:")
        if no_audio_count > 50:
            logger.warning(f"  1. Écrasement lors des corrections orthographiques")
            logger.warning(f"  2. Suppression accidentelle des champs audio")
            logger.warning(f"  3. Erreur dans les scripts de mise à jour")
        
        logger.info(f"\n🔧 PLAN DE RESTAURATION RECOMMANDÉ:")
        logger.info(f"  1. Restaurer depuis la sauvegarde la plus récente")
        logger.info(f"  2. Réappliquer les fichiers ZIP avec les audio authentiques")
        logger.info(f"  3. Implémenter des protections anti-écrasement")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le diagnostic: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)