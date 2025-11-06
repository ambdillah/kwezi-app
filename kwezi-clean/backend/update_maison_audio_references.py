#!/usr/bin/env python3
"""
Script pour mettre à jour les références audio pour la section "maison"
avec les nouveaux fichiers audio M4A fournis par l'utilisateur.
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

def normalize_for_matching(text):
    """Normalise le texte pour la correspondance avec les fichiers audio"""
    return text.lower().replace(' ', '').replace('_', '').replace('-', '').replace("'", '').replace('é', 'e').replace('è', 'e')

def find_audio_matches(db, audio_dir):
    """Trouve les correspondances entre les mots de la base et les fichiers audio"""
    collection = db['vocabulary']
    
    # Récupérer tous les mots de la section maison
    words = list(collection.find({"section": "maison"}))
    logger.info(f"Mots dans la section maison: {len(words)}")
    
    # Lister tous les fichiers audio
    audio_files = []
    for ext in ['*.m4a', '*.mp3', '*.wav']:
        audio_files.extend([os.path.basename(f) for f in glob.glob(os.path.join(audio_dir, ext))])
    
    logger.info(f"Fichiers audio disponibles: {len(audio_files)}")
    
    matches = {}
    unmatched_words = []
    used_files = set()
    
    logger.info("\n=== ANALYSE DES CORRESPONDANCES AUDIO ===")
    
    for word in words:
        french = word.get('french', '')
        shimaore = word.get('shimaoré', '')
        kibouchi = word.get('kibouchi', '')
        
        # Normaliser les termes pour la recherche
        french_norm = normalize_for_matching(french)
        shimaore_norm = normalize_for_matching(shimaore)
        kibouchi_norm = normalize_for_matching(kibouchi)
        
        # Chercher des correspondances dans les fichiers audio
        matched_files = []
        
        for audio_file in audio_files:
            if audio_file in used_files:
                continue
                
            audio_norm = normalize_for_matching(os.path.splitext(audio_file)[0])
            
            # Correspondance directe ou partielle
            if (audio_norm == french_norm or 
                audio_norm == shimaore_norm or 
                audio_norm == kibouchi_norm or
                french_norm in audio_norm or
                shimaore_norm in audio_norm or
                kibouchi_norm in audio_norm):
                matched_files.append(audio_file)
        
        if matched_files:
            # Prendre le premier match (ou le plus spécifique)
            best_match = matched_files[0]
            matches[word['_id']] = {
                'word': word,
                'audio_file': best_match,
                'french': french,
                'shimaore': shimaore,
                'kibouchi': kibouchi
            }
            used_files.add(best_match)
            logger.info(f"✅ {french} → {best_match}")
        else:
            unmatched_words.append(word)
            logger.warning(f"❌ Pas d'audio trouvé pour: {french} (shimaoré: {shimaore}, kibouchi: {kibouchi})")
    
    # Fichiers audio non utilisés
    unused_files = [f for f in audio_files if f not in used_files]
    
    logger.info(f"\n=== RÉSUMÉ CORRESPONDANCES ===")
    logger.info(f"Correspondances trouvées: {len(matches)}")
    logger.info(f"Mots sans audio: {len(unmatched_words)}")
    logger.info(f"Fichiers audio non utilisés: {len(unused_files)}")
    
    if unused_files:
        logger.info("Fichiers audio non utilisés:")
        for file in unused_files[:10]:  # Afficher les 10 premiers
            logger.info(f"  - {file}")
    
    return matches, unmatched_words, unused_files

def update_audio_references(db, matches):
    """Met à jour les références audio dans la base de données"""
    collection = db['vocabulary']
    updated_count = 0
    
    logger.info("\n=== MISE À JOUR DES RÉFÉRENCES AUDIO ===")
    
    for word_id, match_data in matches.items():
        audio_file = match_data['audio_file']
        word = match_data['word']
        
        # Créer le chemin relatif pour l'audio
        audio_path = f"audio/maison/{audio_file}"
        
        # Mettre à jour le document avec la référence audio authentique
        result = collection.update_one(
            {"_id": word_id},
            {
                "$set": {
                    "audio_authentic": audio_path,
                    "has_authentic_audio": True,
                    "audio_updated": True,
                    "audio_format": "m4a"
                }
            }
        )
        
        if result.modified_count > 0:
            updated_count += 1
            logger.info(f"✅ {word.get('french')} → {audio_path}")
        else:
            logger.warning(f"❌ Échec mise à jour: {word.get('french')}")
    
    logger.info(f"\nMises à jour réussies: {updated_count}")
    return updated_count

def main():
    """Fonction principale"""
    logger.info("Début de la mise à jour des références audio pour la section maison")
    
    try:
        # Chemin vers les fichiers audio
        audio_dir = "/app/frontend/assets/audio/maison"
        
        if not os.path.exists(audio_dir):
            logger.error(f"Répertoire audio non trouvé: {audio_dir}")
            return 1
        
        # Connexion à la base de données
        db = connect_to_database()
        
        # Trouver les correspondances
        matches, unmatched_words, unused_files = find_audio_matches(db, audio_dir)
        
        if not matches:
            logger.error("Aucune correspondance trouvée")
            return 1
        
        # Mettre à jour les références
        updated_count = update_audio_references(db, matches)
        
        # Statistiques finales
        total_words = len(matches) + len(unmatched_words)
        coverage_percentage = (updated_count / total_words) * 100 if total_words > 0 else 0
        
        logger.info(f"\n{'='*50}")
        logger.info("RÉSUMÉ FINAL")
        logger.info(f"{'='*50}")
        logger.info(f"Mots avec audio authentique: {updated_count}/{total_words} ({coverage_percentage:.1f}%)")
        logger.info(f"Fichiers audio disponibles: {len(matches) + len(unused_files)}")
        logger.info(f"Couverture audio: {'Excellente' if coverage_percentage >= 80 else 'Partielle' if coverage_percentage >= 50 else 'Limitée'}")
        
        if updated_count > 0:
            logger.info("🎉 Mise à jour des prononciations audio réussie!")
        else:
            logger.warning("⚠️ Aucune mise à jour effectuée")
            
    except Exception as e:
        logger.error(f"Erreur dans le script principal: {e}")
        return 1
    
    return 0 if updated_count > 0 else 1

if __name__ == "__main__":
    exit(main())