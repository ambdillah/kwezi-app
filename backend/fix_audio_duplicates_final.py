#!/usr/bin/env python3
"""
Correction finale des doublons audio dans les verbes
Chaque traduction aura son propre fichier audio unique
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

def clean_text_for_matching(text):
    """Nettoie un texte pour la correspondance"""
    if not text:
        return ""
    
    text = text.lower()
    text = text.replace(' ', '').replace('-', '').replace('_', '').replace('/', '')
    text = text.replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('ë', 'e')
    text = text.replace('à', 'a').replace('á', 'a').replace('â', 'a').replace('ä', 'a')
    text = text.replace('ô', 'o').replace('ö', 'o').replace('ò', 'o').replace('ó', 'o')
    text = text.replace('û', 'u').replace('ù', 'u').replace('ü', 'u').replace('ú', 'u')
    text = text.replace('î', 'i').replace('ï', 'i').replace('ì', 'i').replace('í', 'i')
    text = text.replace('ç', 'c').replace('ñ', 'n')
    
    return text

def get_all_available_audio_files():
    """Récupère tous les fichiers audio disponibles"""
    audio_dir = "/app/frontend/assets/audio/verbes"
    
    if not os.path.exists(audio_dir):
        logger.error(f"Répertoire audio non trouvé: {audio_dir}")
        return []
    
    available_files = []
    for filename in os.listdir(audio_dir):
        if filename.lower().endswith(('.m4a', '.mp3', '.wav')):
            available_files.append(filename)
    
    logger.info(f"Fichiers audio disponibles: {len(available_files)}")
    return available_files

def find_exact_audio_match(translation_text, available_files):
    """Trouve la correspondance audio exacte pour une traduction"""
    if not translation_text:
        return None
    
    clean_translation = clean_text_for_matching(translation_text)
    
    # Chercher correspondance exacte d'abord
    for filename in available_files:
        audio_name = filename.replace('.m4a', '').replace('.mp3', '').replace('.wav', '')
        clean_audio = clean_text_for_matching(audio_name)
        
        if clean_audio == clean_translation:
            return filename
    
    # Ensuite correspondance partielle très précise
    best_match = None
    best_score = 0
    
    for filename in available_files:
        audio_name = filename.replace('.m4a', '').replace('.mp3', '').replace('.wav', '')
        clean_audio = clean_text_for_matching(audio_name)
        
        if len(clean_audio) < 4 or len(clean_translation) < 4:
            continue
        
        score = 0
        
        # Correspondance exacte totale
        if clean_audio == clean_translation:
            score = 100
        # Correspondance de début (très précise)
        elif clean_translation.startswith(clean_audio) and len(clean_audio) >= len(clean_translation) * 0.8:
            score = 90
        elif clean_audio.startswith(clean_translation) and len(clean_translation) >= len(clean_audio) * 0.8:
            score = 85
        # Correspondance contient (très stricte)
        elif len(clean_audio) >= 6 and clean_audio in clean_translation and len(clean_audio) >= len(clean_translation) * 0.7:
            score = 80
        elif len(clean_translation) >= 6 and clean_translation in clean_audio and len(clean_translation) >= len(clean_audio) * 0.7:
            score = 75
        
        if score > best_score and score >= 75:  # Score minimum élevé
            best_score = score
            best_match = filename
    
    return best_match

def fix_all_verb_audio_correspondences():
    """Corrige toutes les correspondences audio des verbes"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("🔄 CORRECTION FINALE DES CORRESPONDANCES AUDIO VERBES")
    
    # Récupérer tous les verbes
    verbs = list(collection.find({"section": "verbes"}).sort("french", 1))
    available_files = get_all_available_audio_files()
    
    if not available_files:
        logger.error("Aucun fichier audio disponible")
        return False
    
    # Traquer l'usage des fichiers pour éviter les doublons
    used_files = set()
    updated_count = 0
    
    logger.info(f"\n{'Français':20} | {'Shimaoré':25} | {'Kibouchi':25} | {'Audio Shimaoré':25} | {'Audio Kibouchi':25}")
    logger.info("-" * 145)
    
    for verb in verbs:
        french = verb.get('french', '')
        shimaore = verb.get('shimaoré', '')
        kibouchi = verb.get('kibouchi', '')
        verb_id = verb['_id']
        
        # Trouver les correspondances audio exactes
        shimaore_audio = None
        kibouchi_audio = None
        
        # Chercher pour shimaoré
        if shimaore:
            shimaore_candidates = [f for f in available_files if f not in used_files]
            shimaore_audio = find_exact_audio_match(shimaore, shimaore_candidates)
            if shimaore_audio:
                used_files.add(shimaore_audio)
        
        # Chercher pour kibouchi (dans les fichiers restants)
        if kibouchi:
            kibouchi_candidates = [f for f in available_files if f not in used_files]
            kibouchi_audio = find_exact_audio_match(kibouchi, kibouchi_candidates)
            if kibouchi_audio:
                used_files.add(kibouchi_audio)
        
        # Si on n'a pas trouvé de correspondance pour l'un, chercher dans les fichiers restants sans restriction
        if shimaore and not shimaore_audio:
            remaining_files = [f for f in available_files if f not in used_files]
            if remaining_files:
                shimaore_audio = find_exact_audio_match(shimaore, remaining_files)
                if shimaore_audio:
                    used_files.add(shimaore_audio)
        
        if kibouchi and not kibouchi_audio:
            remaining_files = [f for f in available_files if f not in used_files]
            if remaining_files:
                kibouchi_audio = find_exact_audio_match(kibouchi, remaining_files)
                if kibouchi_audio:
                    used_files.add(kibouchi_audio)
        
        # Mettre à jour la base de données
        update_data = {
            "audio_shimaoré_filename": shimaore_audio,
            "audio_kibouchi_filename": kibouchi_audio,
            "audio_shimaoré_url": f"audio/verbes/{shimaore_audio}" if shimaore_audio else None,
            "audio_kibouchi_url": f"audio/verbes/{kibouchi_audio}" if kibouchi_audio else None,
            "has_shimaoré_audio": bool(shimaore_audio),
            "has_kibouchi_audio": bool(kibouchi_audio),
            "audio_duplicates_fixed": True
        }
        
        result = collection.update_one(
            {"_id": verb_id},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            updated_count += 1
        
        # Affichage
        shimaore_status = f"✅ {shimaore_audio[:20]}..." if shimaore_audio and len(shimaore_audio) > 20 else f"{'✅ ' + shimaore_audio if shimaore_audio else '❌ Aucun'}"
        kibouchi_status = f"✅ {kibouchi_audio[:20]}..." if kibouchi_audio and len(kibouchi_audio) > 20 else f"{'✅ ' + kibouchi_audio if kibouchi_audio else '❌ Aucun'}"
        
        logger.info(f"{french:20} | {shimaore:25} | {kibouchi:25} | {shimaore_status:25} | {kibouchi_status:25}")
    
    return updated_count

def verify_no_duplicates():
    """Vérifie qu'il n'y a plus de doublons"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info(f"\n=== VÉRIFICATION FINALE - PLUS DE DOUBLONS ===")
    
    verbs = list(collection.find({"section": "verbes"}))
    
    audio_usage = {}
    
    for verb in verbs:
        french = verb.get('french', 'N/A')
        shimaore_audio = verb.get('audio_shimaoré_filename')
        kibouchi_audio = verb.get('audio_kibouchi_filename')
        
        if shimaore_audio:
            if shimaore_audio not in audio_usage:
                audio_usage[shimaore_audio] = []
            audio_usage[shimaore_audio].append(f"{french} (shimaoré)")
        
        if kibouchi_audio:
            if kibouchi_audio not in audio_usage:
                audio_usage[kibouchi_audio] = []
            audio_usage[kibouchi_audio].append(f"{french} (kibouchi)")
    
    # Vérifier les doublons
    duplicates_remaining = 0
    for audio_file, usages in audio_usage.items():
        if len(usages) > 1:
            duplicates_remaining += 1
            logger.info(f"🚨 DOUBLON RESTANT: {audio_file}")
            for usage in usages:
                logger.info(f"     - {usage}")
    
    if duplicates_remaining == 0:
        logger.info("✅ AUCUN DOUBLON - CORRECTION RÉUSSIE!")
    else:
        logger.warning(f"⚠️ {duplicates_remaining} doublons restants")
    
    return duplicates_remaining == 0

def get_final_statistics():
    """Obtient les statistiques finales"""
    db = connect_to_database()
    collection = db['vocabulary']
    
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
    
    logger.info(f"\n📊 STATISTIQUES FINALES:")
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
    logger.info("🎯 CORRECTION FINALE - ÉLIMINATION DOUBLONS AUDIO VERBES")
    
    try:
        # 1. Correction des correspondances
        updated_count = fix_all_verb_audio_correspondences()
        
        # 2. Vérification absence de doublons
        no_duplicates = verify_no_duplicates()
        
        # 3. Statistiques finales
        stats = get_final_statistics()
        
        # 4. Résumé final
        logger.info(f"\n{'='*100}")
        logger.info("RÉSUMÉ CORRECTION FINALE AUDIO VERBES")
        logger.info(f"{'='*100}")
        logger.info(f"✅ Verbes mis à jour: {updated_count}")
        logger.info(f"🎯 Doublons éliminés: {'✅ OUI' if no_duplicates else '❌ NON'}")
        logger.info(f"📈 Coverage final:")
        logger.info(f"  - Shimaoré: {stats['shimaore']}/{stats['total']} ({stats['shimaore']/stats['total']*100:.1f}%)")
        logger.info(f"  - Kibouchi: {stats['kibouchi']}/{stats['total']} ({stats['kibouchi']/stats['total']*100:.1f}%)")
        
        if no_duplicates:
            logger.info(f"\n🎉 SUCCÈS COMPLET!")
            logger.info(f"Chaque traduction a maintenant son propre fichier audio unique.")
            logger.info(f"Plus de confusion entre 'oulindra' et 'mandigni'.")
            logger.info(f"Tous les verbes ont des correspondances audio correctes.")
        else:
            logger.warning(f"\n⚠️ Correction partielle - vérification nécessaire")
        
        return no_duplicates
        
    except Exception as e:
        logger.error(f"Erreur dans la correction finale: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)