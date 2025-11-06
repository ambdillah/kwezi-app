#!/usr/bin/env python3
"""
Analyse complète des correspondances audio avec la structure réelle de la base de données
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
        
        if os.path.isdir(category_path) and not category.endswith('_backup'):
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
    
    # Récupérer tous les mots par section
    words_by_section = {}
    
    sections = collection.distinct("section")
    
    for section in sections:
        words = list(collection.find({"section": section}, {
            "_id": 1,
            "french": 1,
            "shimaoré": 1,
            "kibouchi": 1,
            "section": 1,
            "audio_shimaoré": 1,
            "audio_kibouchi": 1,
            "has_authentic_audio": 1
        }))
        
        if words:
            words_by_section[section] = words
            logger.info(f"📚 {section:15} → {len(words):3} mots")
    
    total_words = sum(len(words) for words in words_by_section.values())
    logger.info(f"\nTotal: {total_words} mots dans {len(words_by_section)} sections")
    
    return words_by_section

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
        'unmatched_words': {},
        'matches_found': []
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
            
            # Chercher dans toutes les sections de mots (correspondance audio_category avec section ou similaire)
            for db_section, words in database_words.items():
                for word in words:
                    
                    # Vérifier correspondances avec french, shimaoré, kibouchi
                    french_clean = clean_text_for_comparison(word.get('french', ''))
                    shimaore_clean = clean_text_for_comparison(word.get('shimaoré', ''))
                    kibouchi_clean = clean_text_for_comparison(word.get('kibouchi', ''))
                    
                    # Correspondance exacte ou approximative
                    if (audio_name_clean == french_clean or 
                        audio_name_clean == shimaore_clean or 
                        audio_name_clean == kibouchi_clean or
                        (len(audio_name_clean) > 3 and audio_name_clean in shimaore_clean) or
                        (len(audio_name_clean) > 3 and audio_name_clean in kibouchi_clean) or
                        (len(shimaore_clean) > 3 and shimaore_clean in audio_name_clean) or
                        (len(kibouchi_clean) > 3 and kibouchi_clean in audio_name_clean)):
                        
                        matches_found.append({
                            'audio_file': audio_file,
                            'word': word,
                            'match_type': 'exact' if audio_name_clean in [french_clean, shimaore_clean, kibouchi_clean] else 'partial',
                            'db_section': db_section,
                            'audio_category': audio_category
                        })
                        match_found = True
                        
                        logger.info(f"  ✅ {audio_file['filename']:30} → {word.get('french', 'N/A'):20} ({word.get('shimaoré', 'N/A')}/{word.get('kibouchi', 'N/A')})")
                        
                        # Ajouter à la liste globale des correspondances
                        statistics['matches_found'].append({
                            'audio_category': audio_category,
                            'audio_filename': audio_file['filename'],
                            'word_id': str(word['_id']),
                            'french': word.get('french', ''),
                            'shimaore': word.get('shimaoré', ''),
                            'kibouchi': word.get('kibouchi', ''),
                            'section': db_section
                        })
                        break
                
                if match_found:
                    break
            
            if not match_found:
                unmatched_audio.append(audio_file)
                logger.warning(f"  ❌ {audio_file['filename']:30} → Aucune correspondance")
        
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

def generate_update_script(statistics):
    """Génère un script de mise à jour basé sur les correspondances trouvées"""
    
    logger.info("\n=== GÉNÉRATION SCRIPT DE MISE À JOUR ===")
    
    matches = statistics['matches_found']
    
    script_content = f"""#!/usr/bin/env python3
\"\"\"
Script auto-généré pour appliquer {len(matches)} correspondances audio
basé sur l'analyse case-insensitive de la structure réelle de la base
\"\"\"

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
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
    
    # Ajouter toutes les correspondances au script
    for match in matches:
        audio_path = f"audio/{match['audio_category']}/{match['audio_filename']}"
        
        script_content += f"""        {{
            'word_id': ObjectId('{match['word_id']}'),
            'french': '{match['french']}',
            'audio_path': '{audio_path}',
            'audio_filename': '{match['audio_filename']}',
            'category': '{match['audio_category']}',
            'section': '{match['section']}'
        }},
"""
    
    script_content += f"""    ]
    
    logger.info(f"Application de {{len(correspondences)}} correspondences...")
    
    updated_count = 0
    for corr in correspondences:
        # Déterminer si c'est shimaoré ou kibouchi selon le nom du fichier
        filename_lower = corr['audio_filename'].lower()
        
        # Mise à jour avec le nouveau système audio authentique
        result = collection.update_one(
            {{"_id": corr['word_id']}},
            {{
                "$set": {{
                    "audio_authentic": corr['audio_path'],
                    "has_authentic_audio": True,
                    "audio_format": "m4a",
                    "auto_matched": True,
                    "audio_updated_at": "{{}}".replace('{{}}', str(__import__('datetime').datetime.now()))
                }}
            }}
        )
        
        if result.modified_count > 0:
            updated_count += 1
            logger.info(f"✅ {{corr['french']}} → {{corr['audio_path']}}")
        else:
            logger.warning(f"❌ Échec mise à jour: {{corr['french']}}")
    
    logger.info(f"Mises à jour appliquées: {{updated_count}}/{{len(correspondences)}}")
    return updated_count

if __name__ == "__main__":
    apply_audio_correspondences()
"""
    
    # Écrire le script
    script_path = "/app/backend/apply_corrected_audio_matches.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    
    logger.info(f"Script généré: {script_path}")
    logger.info(f"Correspondances à appliquer: {len(matches)}")
    
    return script_path, len(matches)

def main():
    """Fonction principale"""
    logger.info("Début de l'analyse complète des correspondances audio (structure corrigée)")
    
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
        
        # 5. Exemples de correspondances trouvées
        if statistics['matches_found']:
            logger.info(f"\n📝 EXEMPLES DE CORRESPONDANCES:")
            for i, match in enumerate(statistics['matches_found'][:10]):  # Afficher les 10 premières
                logger.info(f"  {i+1:2}. {match['audio_filename']:25} → {match['french']:15} ({match['shimaore']}/{match['kibouchi']})")
        
        # 6. Générer le script de mise à jour
        if statistics['matches_found']:
            script_path, updates_count = generate_update_script(statistics)
            
            logger.info(f"\n🎉 ANALYSE TERMINÉE!")
            logger.info(f"📄 Script généré: {script_path}")
            logger.info(f"🔄 Prêt à appliquer {updates_count} correspondances")
        else:
            logger.warning(f"\n⚠️  Aucune correspondance trouvée!")
            logger.warning(f"Vérifiez que les noms de fichiers correspondent aux traductions dans la base")
        
        return correspondences, statistics
        
    except Exception as e:
        logger.error(f"Erreur dans l'analyse: {e}")
        return None, None

if __name__ == "__main__":
    main()