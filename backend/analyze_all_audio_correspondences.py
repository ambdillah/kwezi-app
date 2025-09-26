#!/usr/bin/env python3
"""
Analyse complète de tous les fichiers audio et correspondances avec la base de données
en tenant compte des majuscules/minuscules
"""

import os
import re
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

def scan_all_audio_files():
    """Scanne tous les fichiers audio dans toutes les catégories"""
    audio_base_dir = "/app/frontend/assets/audio"
    all_audio_files = {}
    
    logger.info("=== SCAN DE TOUS LES FICHIERS AUDIO ===")
    
    # Parcourir tous les dossiers audio
    for category in os.listdir(audio_base_dir):
        category_path = os.path.join(audio_base_dir, category)
        
        if os.path.isdir(category_path):
            files_in_category = []
            
            for filename in os.listdir(category_path):
                if filename.lower().endswith(('.m4a', '.mp3', '.wav')):
                    file_size = os.path.getsize(os.path.join(category_path, filename))
                    files_in_category.append({
                        'filename': filename,
                        'size': file_size,
                        'name_clean': os.path.splitext(filename)[0],  # Nom sans extension
                        'name_lower': os.path.splitext(filename)[0].lower()  # Nom en minuscules
                    })
            
            if files_in_category:
                all_audio_files[category] = files_in_category
                logger.info(f"📁 {category:15} → {len(files_in_category):3} fichiers")
    
    total_files = sum(len(files) for files in all_audio_files.values())
    logger.info(f"\nTotal: {total_files} fichiers audio trouvés dans {len(all_audio_files)} catégories")
    
    return all_audio_files

def get_all_database_words():
    """Récupère tous les mots de la base de données avec leurs traductions"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("=== RÉCUPÉRATION MOTS BASE DE DONNÉES ===")
    
    # Récupérer tous les mots par catégorie
    words_by_category = {}
    
    categories = collection.distinct("category")
    
    for category in categories:
        words = list(collection.find({"category": category}, {
            "_id": 1,
            "french": 1,
            "shimaore": 1,
            "kibouchi": 1,
            "category": 1,
            "audio_authentic": 1,
            "has_authentic_audio": 1
        }))
        
        if words:
            words_by_category[category] = words
            logger.info(f"📚 {category:15} → {len(words):3} mots")
    
    total_words = sum(len(words) for words in words_by_category.values())
    logger.info(f"\nTotal: {total_words} mots dans {len(words_by_category)} catégories")
    
    return words_by_category

def clean_text_for_comparison(text):
    """Nettoie un texte pour la comparaison (enlève accents, espaces, ponctuation)"""
    if not text:
        return ""
    
    # Convertir en minuscules
    text = text.lower()
    
    # Remplacer les accents
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'á': 'a', 'â': 'a', 'ä': 'a',
        'ô': 'o', 'ö': 'o', 'ò': 'o', 'ó': 'o',
        'û': 'u', 'ù': 'u', 'ü': 'u', 'ú': 'u',
        'î': 'i', 'ï': 'i', 'ì': 'i', 'í': 'i',
        'ç': 'c', 'ñ': 'n'
    }
    
    for accented, plain in replacements.items():
        text = text.replace(accented, plain)
    
    # Enlever espaces, tirets, apostrophes, points
    text = re.sub(r'[ \-\'\.\/]', '', text)
    
    return text

def find_audio_correspondences(audio_files, database_words):
    """Trouve les correspondances entre fichiers audio et mots de la base"""
    
    logger.info("\n=== ANALYSE DES CORRESPONDANCES ===")
    
    all_correspondences = {}
    statistics = {
        'total_matches': 0,
        'by_category': {},
        'unmatched_audio': {},
        'unmatched_words': {}
    }
    
    # Pour chaque catégorie dans les fichiers audio
    for audio_category, audio_list in audio_files.items():
        
        logger.info(f"\n🔍 Analyse catégorie: {audio_category}")
        
        matches_found = []
        unmatched_audio = []
        
        # Pour chaque fichier audio dans cette catégorie
        for audio_file in audio_list:
            audio_name_clean = clean_text_for_comparison(audio_file['name_clean'])
            match_found = False
            
            # Chercher dans toutes les catégories de mots (pas seulement celle correspondante)
            for db_category, words in database_words.items():
                for word in words:
                    
                    # Vérifier correspondances avec french, shimaore, kibouchi
                    french_clean = clean_text_for_comparison(word.get('french', ''))
                    shimaore_clean = clean_text_for_comparison(word.get('shimaore', ''))
                    kibouchi_clean = clean_text_for_comparison(word.get('kibouchi', ''))
                    
                    # Correspondance exacte ou approximative
                    if (audio_name_clean == french_clean or 
                        audio_name_clean == shimaore_clean or 
                        audio_name_clean == kibouchi_clean or
                        audio_name_clean in shimaore_clean or
                        audio_name_clean in kibouchi_clean or
                        shimaore_clean in audio_name_clean or
                        kibouchi_clean in audio_name_clean):
                        
                        matches_found.append({
                            'audio_file': audio_file,
                            'word': word,
                            'match_type': 'exact' if audio_name_clean in [french_clean, shimaore_clean, kibouchi_clean] else 'partial',
                            'db_category': db_category
                        })
                        match_found = True
                        
                        logger.info(f"  ✅ {audio_file['filename']:25} → {word.get('french', 'N/A'):15} ({word.get('shimaore', 'N/A')}/{word.get('kibouchi', 'N/A')})")
                        break
                
                if match_found:
                    break
            
            if not match_found:
                unmatched_audio.append(audio_file)
                logger.warning(f"  ❌ {audio_file['filename']:25} → Aucune correspondance")
        
        # Statistiques pour cette catégorie
        statistics['by_category'][audio_category] = {
            'total_audio': len(audio_list),
            'matches': len(matches_found),
            'unmatched': len(unmatched_audio),
            'coverage': (len(matches_found) / len(audio_list) * 100) if audio_list else 0
        }
        
        all_correspondences[audio_category] = {
            'matches': matches_found,
            'unmatched_audio': unmatched_audio
        }
        
        statistics['total_matches'] += len(matches_found)
        statistics['unmatched_audio'][audio_category] = unmatched_audio
        
        logger.info(f"Résultats {audio_category}: {len(matches_found)}/{len(audio_list)} correspondances ({len(matches_found)/len(audio_list)*100:.1f}%)")
    
    return all_correspondences, statistics

def generate_update_script(correspondences, statistics):
    """Génère un script de mise à jour basé sur les correspondances trouvées"""
    
    logger.info("\n=== GÉNÉRATION SCRIPT DE MISE À JOUR ===")
    
    script_content = """#!/usr/bin/env python3
\"\"\"
Script auto-généré pour appliquer les correspondances audio
basé sur l'analyse case-insensitive
\"\"\"

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_database():
    mongo_url = os.getenv('MONGO_URL')
    client = MongoClient(mongo_url)
    return client['shimaoré_app']

def apply_audio_correspondences():
    db = connect_to_database()
    collection = db['vocabulary']
    
    # Correspondances trouvées automatiquement
    correspondences = [
"""
    
    total_updates = 0
    
    # Ajouter toutes les correspondances au script
    for category, data in correspondences.items():
        for match in data['matches']:
            word = match['word']
            audio_file = match['audio_file']['filename']
            
            script_content += f"""        {{
            'word_id': '{word['_id']}',
            'french': '{word.get('french', '')}',
            'audio_path': 'audio/{category}/{audio_file}',
            'category': '{category}'
        }},
"""
            total_updates += 1
    
    script_content += f"""    ]
    
    logger.info(f"Application de {{len(correspondences)}} correspondances...")
    
    updated_count = 0
    for corr in correspondences:
        result = collection.update_one(
            {{"_id": corr['word_id']}},
            {{
                "$set": {{
                    "audio_authentic": corr['audio_path'],
                    "has_authentic_audio": True,
                    "audio_format": "m4a",
                    "auto_matched": True
                }}
            }}
        )
        
        if result.modified_count > 0:
            updated_count += 1
            logger.info(f"✅ {{corr['french']}} → {{corr['audio_path']}}")
    
    logger.info(f"Mises à jour appliquées: {{updated_count}}/{{len(correspondences)}}")
    return updated_count

if __name__ == "__main__":
    apply_audio_correspondences()
"""
    
    # Écrire le script
    script_path = "/app/backend/apply_case_insensitive_audio_matches.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    
    logger.info(f"Script généré: {script_path}")
    logger.info(f"Correspondances à appliquer: {total_updates}")
    
    return script_path, total_updates

def main():
    """Fonction principale"""
    logger.info("Début de l'analyse complète des correspondances audio")
    
    try:
        # 1. Scanner tous les fichiers audio
        audio_files = scan_all_audio_files()
        
        # 2. Récupérer tous les mots de la base
        database_words = get_all_database_words()
        
        # 3. Analyser les correspondances
        correspondences, statistics = find_audio_correspondences(audio_files, database_words)
        
        # 4. Afficher les statistiques détaillées
        logger.info(f"\n{'='*70}")
        logger.info("STATISTIQUES GLOBALES")
        logger.info(f"{'='*70}")
        
        for category, stats in statistics['by_category'].items():
            logger.info(f"{category:15} → {stats['matches']:3}/{stats['total_audio']:3} correspondances ({stats['coverage']:5.1f}%)")
        
        logger.info(f"\nTotal correspondances trouvées: {statistics['total_matches']}")
        
        # 5. Générer le script de mise à jour
        script_path, updates_count = generate_update_script(correspondences, statistics)
        
        logger.info(f"\n🎉 ANALYSE TERMINÉE!")
        logger.info(f"📄 Script généré: {script_path}")
        logger.info(f"🔄 Prêt à appliquer {updates_count} correspondances")
        
        return correspondences, statistics
        
    except Exception as e:
        logger.error(f"Erreur dans l'analyse: {e}")
        return None, None

if __name__ == "__main__":
    main()