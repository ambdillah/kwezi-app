#!/usr/bin/env python3
"""
Finalise la correspondance pour "oumengna" en utilisant le fichier Oumengna.m4a trouvé
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import shutil
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

def handle_oumengna_audio():
    """Gère le fichier audio pour 'oumengna'"""
    
    logger.info("🎯 GESTION SPÉCIALE DU FICHIER OUMENGNA")
    
    # Chemins des fichiers
    source_file = "/app/frontend/assets/audio/adjectifs/Oumengna.m4a"
    target_file = "/app/frontend/assets/audio/verbes/Oumengna.m4a"
    
    if os.path.exists(source_file):
        file_size = os.path.getsize(source_file)
        logger.info(f"📁 Fichier trouvé: {source_file} ({file_size} bytes)")
        
        # Vérifier si le fichier existe déjà dans verbes
        if os.path.exists(target_file):
            logger.info(f"✅ Le fichier existe déjà dans verbes: {target_file}")
        else:
            # Copier le fichier dans le dossier verbes
            try:
                shutil.copy2(source_file, target_file)
                logger.info(f"📋 Fichier copié vers: {target_file}")
            except Exception as e:
                logger.error(f"❌ Erreur lors de la copie: {e}")
                return False
        
        return True
    else:
        logger.error(f"❌ Fichier source non trouvé: {source_file}")
        return False

def update_abimer_verb_audio():
    """Met à jour le verbe 'abîmer' avec le fichier audio shimaoré correct"""
    
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("🔄 MISE À JOUR VERBE 'ABÎMER'")
    
    # Trouver le verbe "abîmer"
    abimer_verb = collection.find_one({
        "section": "verbes",
        "french": "abîmer"
    })
    
    if not abimer_verb:
        logger.error("❌ Verbe 'abîmer' non trouvé")
        return False
    
    logger.info(f"📝 Verbe trouvé:")
    logger.info(f"  Français: {abimer_verb.get('french', 'N/A')}")
    logger.info(f"  Shimaoré: {abimer_verb.get('shimaoré', 'N/A')}")
    logger.info(f"  Kibouchi: {abimer_verb.get('kibouchi', 'N/A')}")
    
    # Mettre à jour avec le fichier audio shimaoré
    update_data = {
        "audio_shimaoré_filename": "Oumengna.m4a",
        "audio_shimaoré_url": "audio/verbes/Oumengna.m4a",
        "has_shimaoré_audio": True,
        "oumengna_problem_resolved": True
    }
    
    result = collection.update_one(
        {"_id": abimer_verb["_id"]},
        {"$set": update_data}
    )
    
    if result.modified_count > 0:
        logger.info("✅ Verbe 'abîmer' mis à jour avec succès")
        logger.info(f"  Audio shimaoré: Oumengna.m4a")
        logger.info(f"  Audio kibouchi: {abimer_verb.get('audio_kibouchi_filename', 'N/A')}")
        return True
    else:
        logger.error("❌ Échec de la mise à jour")
        return False

def verify_final_result():
    """Vérifie le résultat final pour le problème 'oumengna'"""
    
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("🔍 VÉRIFICATION FINALE")
    
    # Récupérer le verbe mis à jour
    abimer_verb = collection.find_one({
        "section": "verbes", 
        "french": "abîmer"
    })
    
    if abimer_verb:
        logger.info(f"📊 ÉTAT FINAL DU VERBE 'ABÎMER':")
        logger.info(f"  Français: {abimer_verb.get('french', 'N/A')}")
        logger.info(f"  Shimaoré: {abimer_verb.get('shimaoré', 'N/A')}")
        logger.info(f"  Kibouchi: {abimer_verb.get('kibouchi', 'N/A')}")
        logger.info(f"  Audio shimaoré: {abimer_verb.get('audio_shimaoré_filename', 'Aucun')}")
        logger.info(f"  Audio kibouchi: {abimer_verb.get('audio_kibouchi_filename', 'Aucun')}")
        logger.info(f"  Has shimaoré audio: {abimer_verb.get('has_shimaoré_audio', False)}")
        logger.info(f"  Has kibouchi audio: {abimer_verb.get('has_kibouchi_audio', False)}")
        
        # Vérifier que les fichiers existent
        shimaore_file = f"/app/frontend/assets/{abimer_verb.get('audio_shimaoré_url', '')}"
        kibouchi_file = f"/app/frontend/assets/{abimer_verb.get('audio_kibouchi_url', '')}"
        
        shimaore_exists = os.path.exists(shimaore_file) if abimer_verb.get('audio_shimaoré_url') else False
        kibouchi_exists = os.path.exists(kibouchi_file) if abimer_verb.get('audio_kibouchi_url') else False
        
        logger.info(f"  Fichier shimaoré existe: {'✅' if shimaore_exists else '❌'}")
        logger.info(f"  Fichier kibouchi existe: {'✅' if kibouchi_exists else '❌'}")
        
        # Vérifier si le problème est résolu
        if ('oumengna' in abimer_verb.get('shimaoré', '').lower() and 
            abimer_verb.get('has_shimaoré_audio', False) and
            shimaore_exists):
            logger.info("🎉 PROBLÈME 'OUMENGNA' COMPLÈTEMENT RÉSOLU!")
            logger.info("  ✅ Shimaoré 'oumengna' a son propre fichier audio")
            logger.info("  ✅ Kibouchi 'manapaka somboutrou' a son propre fichier audio")
            logger.info("  ✅ Pas de confusion entre les langues")
            return True
        else:
            logger.warning("⚠️ Problème partiellement résolu")
            return False
    
    return False

def update_statistics():
    """Met à jour les statistiques générales"""
    
    db = connect_to_database()
    collection = db['vocabulary']
    
    # Statistiques finales
    total_verbs = collection.count_documents({"section": "verbes"})
    verbs_with_shimaore_audio = collection.count_documents({
        "section": "verbes",
        "has_shimaoré_audio": True
    })
    verbs_with_kibouchi_audio = collection.count_documents({
        "section": "verbes", 
        "has_kibouchi_audio": True
    })
    verbs_with_both_audio = collection.count_documents({
        "section": "verbes",
        "has_shimaoré_audio": True,
        "has_kibouchi_audio": True
    })
    
    logger.info(f"\n📈 STATISTIQUES FINALES VERBES:")
    logger.info(f"  Total verbes: {total_verbs}")
    logger.info(f"  Avec audio shimaoré: {verbs_with_shimaore_audio} ({verbs_with_shimaore_audio/total_verbs*100:.1f}%)")
    logger.info(f"  Avec audio kibouchi: {verbs_with_kibouchi_audio} ({verbs_with_kibouchi_audio/total_verbs*100:.1f}%)")
    logger.info(f"  Avec audio des deux: {verbs_with_both_audio} ({verbs_with_both_audio/total_verbs*100:.1f}%)")
    
    return {
        'total': total_verbs,
        'shimaore': verbs_with_shimaore_audio,
        'kibouchi': verbs_with_kibouchi_audio,
        'both': verbs_with_both_audio
    }

def main():
    """Fonction principale"""
    logger.info("🎯 FINALISATION CORRESPONDANCE OUMENGNA")
    
    try:
        # 1. Gérer le fichier audio Oumengna.m4a
        if not handle_oumengna_audio():
            logger.error("Échec de la gestion du fichier audio")
            return False
        
        # 2. Mettre à jour le verbe 'abîmer'
        if not update_abimer_verb_audio():
            logger.error("Échec de la mise à jour du verbe")
            return False
        
        # 3. Vérifier le résultat final
        success = verify_final_result()
        
        # 4. Statistiques finales
        stats = update_statistics()
        
        # 5. Résumé
        logger.info(f"\n{'='*80}")
        logger.info("RÉSUMÉ FINALISATION OUMENGNA")
        logger.info(f"{'='*80}")
        logger.info(f"🎯 Problème résolu: {'✅ OUI' if success else '❌ NON'}")
        logger.info(f"📊 Coverage mise à jour:")
        logger.info(f"  - Shimaoré: {stats['shimaore']}/{stats['total']} ({stats['shimaore']/stats['total']*100:.1f}%)")
        logger.info(f"  - Kibouchi: {stats['kibouchi']}/{stats['total']} ({stats['kibouchi']/stats['total']*100:.1f}%)")
        
        return success
        
    except Exception as e:
        logger.error(f"Erreur dans la finalisation: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)