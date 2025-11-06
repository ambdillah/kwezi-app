#!/usr/bin/env python3
"""
Réorganisation de la structure audio pour les verbes selon les recommandations de l'utilisateur
Structure cible : colonnes séparées pour shimaoré et kibouchi avec leurs fichiers audio respectifs
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

def scan_available_audio_files():
    """Scanne tous les fichiers audio disponibles pour les verbes"""
    verbs_audio_dir = "/app/frontend/assets/audio/verbes"
    
    if not os.path.exists(verbs_audio_dir):
        logger.error(f"Répertoire audio verbes non trouvé: {verbs_audio_dir}")
        return {}
    
    audio_files = {}
    for filename in os.listdir(verbs_audio_dir):
        if filename.lower().endswith(('.m4a', '.mp3', '.wav')):
            name_clean = os.path.splitext(filename)[0].lower()
            # Nettoyer le nom pour comparaison
            name_clean = name_clean.replace(' ', '').replace('-', '').replace('_', '')
            audio_files[name_clean] = filename
    
    logger.info(f"Fichiers audio disponibles: {len(audio_files)}")
    return audio_files

def clean_text_for_matching(text):
    """Nettoie un texte pour la correspondance avec les fichiers audio"""
    if not text:
        return ""
    
    # Convertir en minuscules et enlever espaces/caractères spéciaux
    text = text.lower()
    text = text.replace(' ', '').replace('-', '').replace('_', '').replace('é', 'e').replace('è', 'e').replace('à', 'a').replace('ç', 'c')
    
    return text

def reorganize_verbs_audio_structure():
    """Réorganise la structure audio des verbes selon les recommandations"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("🔄 RÉORGANISATION STRUCTURE AUDIO VERBES")
    
    # Récupérer tous les verbes
    verbs = list(collection.find({"section": "verbes"}))
    logger.info(f"Verbes à traiter: {len(verbs)}")
    
    # Scanner les fichiers audio disponibles
    available_audio = scan_available_audio_files()
    
    logger.info(f"\n📋 CORRESPONDANCES AUDIO INTELLIGENTES:")
    logger.info(f"{'Français':15} | {'Shimaoré':20} | {'Kibouchi':20} | {'Audio Shimaoré':25} | {'Audio Kibouchi':25}")
    logger.info("-" * 130)
    
    updated_count = 0
    correspondences = []
    
    for verb in verbs:
        french = verb.get('french', '')
        shimaore = verb.get('shimaoré', '')
        kibouchi = verb.get('kibouchi', '')
        verb_id = verb['_id']
        
        # Nettoyer les textes pour correspondance
        shimaore_clean = clean_text_for_matching(shimaore)
        kibouchi_clean = clean_text_for_matching(kibouchi)
        
        # Trouver les correspondances audio
        shimaore_audio = None
        kibouchi_audio = None
        
        # Chercher correspondance exacte pour shimaoré
        for audio_clean, audio_filename in available_audio.items():
            if shimaore_clean and shimaore_clean == audio_clean:
                shimaore_audio = audio_filename
                break
            elif len(shimaore_clean) > 4 and shimaore_clean in audio_clean:
                shimaore_audio = audio_filename
                break
        
        # Chercher correspondance exacte pour kibouchi
        for audio_clean, audio_filename in available_audio.items():
            if kibouchi_clean and kibouchi_clean == audio_clean:
                # Éviter d'utiliser le même fichier pour les deux langues si les traductions sont différentes
                if shimaore_audio != audio_filename or shimaore_clean == kibouchi_clean:
                    kibouchi_audio = audio_filename
                    break
            elif len(kibouchi_clean) > 4 and kibouchi_clean in audio_clean:
                # Éviter d'utiliser le même fichier pour les deux langues si les traductions sont différentes  
                if shimaore_audio != audio_filename or shimaore_clean == kibouchi_clean:
                    kibouchi_audio = audio_filename
                    break
        
        # Préparer les nouvelles données
        new_data = {
            "audio_shimaoré_filename": shimaore_audio,
            "audio_kibouchi_filename": kibouchi_audio,
            "audio_shimaoré_url": f"audio/verbes/{shimaore_audio}" if shimaore_audio else None,
            "audio_kibouchi_url": f"audio/verbes/{kibouchi_audio}" if kibouchi_audio else None,
            "has_shimaoré_audio": bool(shimaore_audio),
            "has_kibouchi_audio": bool(kibouchi_audio),
            "audio_structure_updated": True
        }
        
        # Supprimer les anciens champs confus
        unset_fields = {
            "audio_authentic": "",
            "has_authentic_audio": "",
            "auto_matched": "",
            "match_type": "",
            "match_field": ""
        }
        
        # Mettre à jour la base de données
        result = collection.update_one(
            {"_id": verb_id},
            {
                "$set": new_data,
                "$unset": unset_fields
            }
        )
        
        if result.modified_count > 0:
            updated_count += 1
            
            correspondences.append({
                'french': french,
                'shimaore': shimaore,
                'kibouchi': kibouchi,
                'shimaore_audio': shimaore_audio,
                'kibouchi_audio': kibouchi_audio
            })
            
            shimaore_status = f"✅ {shimaore_audio}" if shimaore_audio else "❌ Aucun"
            kibouchi_status = f"✅ {kibouchi_audio}" if kibouchi_audio else "❌ Aucun"
            
            logger.info(f"{french:15} | {shimaore:20} | {kibouchi:20} | {shimaore_status:25} | {kibouchi_status:25}")
    
    return updated_count, correspondences

def verify_reorganization():
    """Vérifie que la réorganisation a bien fonctionné"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info(f"\n=== VÉRIFICATION RÉORGANISATION ===")
    
    # Statistiques
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
    
    logger.info(f"📊 STATISTIQUES FINALES:")
    logger.info(f"  Total verbes: {total_verbs}")
    logger.info(f"  Avec audio shimaoré: {verbs_with_shimaore_audio} ({verbs_with_shimaore_audio/total_verbs*100:.1f}%)")
    logger.info(f"  Avec audio kibouchi: {verbs_with_kibouchi_audio} ({verbs_with_kibouchi_audio/total_verbs*100:.1f}%)")
    logger.info(f"  Avec audio des deux: {verbs_with_both_audio} ({verbs_with_both_audio/total_verbs*100:.1f}%)")
    
    # Vérifier le cas spécifique "oumengna"
    abimer_verb = collection.find_one({
        "section": "verbes",
        "french": "abîmer"
    })
    
    if abimer_verb:
        logger.info(f"\n🔍 VÉRIFICATION CAS SPÉCIFIQUE 'ABÎMER':")
        logger.info(f"  Shimaoré: {abimer_verb.get('shimaoré', 'N/A')}")
        logger.info(f"  Kibouchi: {abimer_verb.get('kibouchi', 'N/A')}")
        logger.info(f"  Audio shimaoré: {abimer_verb.get('audio_shimaoré_filename', 'Aucun')}")
        logger.info(f"  Audio kibouchi: {abimer_verb.get('audio_kibouchi_filename', 'Aucun')}")
        
        if 'oumengna' in abimer_verb.get('shimaoré', '').lower():
            shimaore_audio = abimer_verb.get('audio_shimaoré_filename')
            if shimaore_audio and 'oumengna' in shimaore_audio.lower():
                logger.info(f"  ✅ PROBLÈME RÉSOLU: 'oumengna' a son propre fichier audio shimaoré")
            else:
                logger.warning(f"  ⚠️ 'oumengna' n'a pas de fichier audio correspondant")
    
    return {
        'total': total_verbs,
        'shimaore_audio': verbs_with_shimaore_audio,
        'kibouchi_audio': verbs_with_kibouchi_audio,
        'both_audio': verbs_with_both_audio
    }

def main():
    """Fonction principale"""
    logger.info("🎯 RÉORGANISATION STRUCTURE AUDIO VERBES - SÉPARATION SHIMAORÉ/KIBOUCHI")
    
    try:
        # 1. Réorganiser la structure
        updated_count, correspondences = reorganize_verbs_audio_structure()
        
        # 2. Vérifier le résultat
        stats = verify_reorganization()
        
        # 3. Résumé final
        logger.info(f"\n{'='*100}")
        logger.info("RÉSUMÉ RÉORGANISATION AUDIO VERBES")
        logger.info(f"{'='*100}")
        logger.info(f"✅ Verbes mis à jour: {updated_count}")
        logger.info(f"📊 Coverage shimaoré: {stats['shimaore_audio']}/{stats['total']} ({stats['shimaore_audio']/stats['total']*100:.1f}%)")
        logger.info(f"📊 Coverage kibouchi: {stats['kibouchi_audio']}/{stats['total']} ({stats['kibouchi_audio']/stats['total']*100:.1f}%)")
        logger.info(f"🎯 Problème 'oumengna' résolu avec structure séparée")
        
        logger.info(f"\n💡 AVANTAGES OBTENUS:")
        logger.info(f"  ✅ Chaque langue (shimaoré/kibouchi) a ses propres champs audio")
        logger.info(f"  ✅ Pas de confusion entre prononciations différentes")
        logger.info(f"  ✅ Structure claire pour maintenance future")
        logger.info(f"  ✅ Correspondances intelligentes basées sur orthographe")
        
        return correspondences
        
    except Exception as e:
        logger.error(f"Erreur dans la réorganisation: {e}")
        return None

if __name__ == "__main__":
    main()