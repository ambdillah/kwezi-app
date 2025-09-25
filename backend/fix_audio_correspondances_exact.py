#!/usr/bin/env python3
"""
Script pour associer précisément chaque mot shimaoré/kibouchi 
avec les bons fichiers audio basé sur l'orthographe exacte.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging
import glob
import unicodedata

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

def normalize_text_for_matching(text):
    """Normalise le texte pour la correspondance exacte"""
    if not text:
        return ""
    
    # Convertir en minuscules
    text = text.lower()
    
    # Supprimer les accents mais garder l'orthographe de base
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    
    # Supprimer les espaces en début/fin
    text = text.strip()
    
    return text

def create_audio_filename_variants(text):
    """Crée des variantes possibles du nom de fichier audio"""
    if not text:
        return []
    
    variants = []
    
    # Version de base
    base = text.strip()
    variants.append(base)
    
    # Version avec première lettre en majuscule
    if base:
        variants.append(base[0].upper() + base[1:])
    
    # Version avec suppression des espaces
    no_space = base.replace(' ', '')
    if no_space != base:
        variants.append(no_space)
        if no_space:
            variants.append(no_space[0].upper() + no_space[1:])
    
    # Version avec remplacement des espaces par underscores
    underscore = base.replace(' ', '_')
    if underscore != base:
        variants.append(underscore)
        if underscore:
            variants.append(underscore[0].upper() + underscore[1:])
    
    return list(set(variants))  # Supprimer les doublons

def find_exact_audio_matches(verbes, audio_files):
    """Trouve les correspondances exactes entre verbes et fichiers audio"""
    
    # Créer un dictionnaire des fichiers audio sans extension
    audio_dict = {}
    for audio_file in audio_files:
        base_name = os.path.splitext(audio_file)[0]
        audio_dict[normalize_text_for_matching(base_name)] = audio_file
    
    matches = {}
    unmatched_verbes = []
    unmatched_audio = list(audio_files)
    
    logger.info("=== ANALYSE DES CORRESPONDANCES EXACTES ===")
    
    for verb in verbes:
        french = verb.get('french', '')
        shimaore = verb.get('shimaoré', '')
        kibouchi = verb.get('kibouchi', '')
        
        matched_file = None
        match_source = None
        
        # Essayer d'abord avec shimaoré
        if shimaore:
            variants = create_audio_filename_variants(shimaore)
            for variant in variants:
                normalized_variant = normalize_text_for_matching(variant)
                if normalized_variant in audio_dict:
                    matched_file = audio_dict[normalized_variant]
                    match_source = f"shimaoré '{shimaore}' → '{variant}'"
                    break
        
        # Si pas trouvé, essayer avec kibouchi
        if not matched_file and kibouchi:
            variants = create_audio_filename_variants(kibouchi)
            for variant in variants:
                normalized_variant = normalize_text_for_matching(variant)
                if normalized_variant in audio_dict:
                    matched_file = audio_dict[normalized_variant]
                    match_source = f"kibouchi '{kibouchi}' → '{variant}'"
                    break
        
        if matched_file:
            matches[verb['_id']] = {
                'verb': verb,
                'audio_file': matched_file,
                'match_source': match_source,
                'french': french
            }
            if matched_file in unmatched_audio:
                unmatched_audio.remove(matched_file)
            logger.info(f"✅ {french:15} | {match_source} → {matched_file}")
        else:
            unmatched_verbes.append(verb)
            logger.warning(f"❌ {french:15} | Aucun audio trouvé pour shimaoré: '{shimaore}' ou kibouchi: '{kibouchi}'")
    
    return matches, unmatched_verbes, unmatched_audio

def create_manual_mappings():
    """Correspondances manuelles pour les cas spéciaux"""
    return {
        # Correspondances spéciales basées sur l'analyse des fichiers
        "danser": "Chokou.m4a",  # kibouchi: chokou
        "avoir": "Havi.m4a",     # kibouchi: havi  
        "dormir": "Koimini.m4a", # kibouchi: koimini
        "comprendre": "Koufahamou.m4a", # shimaoré: koufahamou
        "penser": "Kouéléwa.m4a",       # kibouchi: kouéléwa
        "casser": "Latsaka.m4a",        # shimaoré: latsaka
        "chercher": "Magnadzari.m4a",   # kibouchi: magnadzari
        "voir": "Magnamiya.m4a",        # kibouchi: magnamiya (attention: pas mahita!)
        "montrer": "Magnaraka.m4a",     # kibouchi: magnaraka
        "dire": "Magnatougnou.m4a",     # kibouchi: magnatougnou
        "faire": "Magnossoutrou.m4a",   # kibouchi: magnossoutrou
        "donner": "Magnoutani.m4a",     # kibouchi: magnoutani
        "prendre": "Magnékitri.m4a",    # kibouchi: magnékitri
        "pleurer": "Mahaléou.m4a",      # kibouchi: mahaléou
        "rire": "Mahandrou.m4a",        # kibouchi: mahandrou
        "regarder": "Mahazou.m4a",      # kibouchi: mahazou
        "finir": "Mahita.m4a"           # kibouchi: mahita
    }

def apply_manual_mappings(verbes, manual_mappings, audio_files):
    """Applique les correspondances manuelles"""
    
    manual_matches = {}
    used_files = set()
    
    # Créer un dictionnaire français → verbe
    french_to_verb = {verb.get('french', '').lower(): verb for verb in verbes}
    
    logger.info("\n=== CORRESPONDANCES MANUELLES ===")
    
    for french_word, audio_file in manual_mappings.items():
        if audio_file in audio_files and french_word.lower() in french_to_verb:
            verb = french_to_verb[french_word.lower()]
            manual_matches[verb['_id']] = {
                'verb': verb,
                'audio_file': audio_file,
                'match_source': f"manuel français '{french_word}'",
                'french': verb.get('french', '')
            }
            used_files.add(audio_file)
            logger.info(f"✅ {french_word:15} → {audio_file} (manuel)")
    
    return manual_matches, used_files

def update_verb_audio_references(db, all_matches):
    """Met à jour les références audio des verbes"""
    collection = db['vocabulary']
    updated_count = 0
    
    logger.info("\n=== MISE À JOUR RÉFÉRENCES AUDIO ===")
    
    for verb_id, match_data in all_matches.items():
        audio_file = match_data['audio_file']
        verb = match_data['verb']
        
        # Créer le chemin relatif pour l'audio
        audio_path = f"audio/verbes/{audio_file}"
        
        # Mettre à jour le document avec la référence audio exacte
        result = collection.update_one(
            {"_id": verb_id},
            {
                "$set": {
                    "audio_authentic": audio_path,
                    "has_authentic_audio": True,
                    "audio_updated": True,
                    "audio_format": "m4a",
                    "audio_match_source": match_data['match_source']
                }
            }
        )
        
        if result.modified_count > 0:
            updated_count += 1
            logger.info(f"✅ {verb.get('french'):15} → {audio_path}")
        else:
            logger.warning(f"❌ Échec mise à jour: {verb.get('french')}")
    
    logger.info(f"\nMises à jour réussies: {updated_count}")
    return updated_count

def copy_audio_files():
    """Copie les fichiers audio dans le bon répertoire"""
    source_dir = "/app/temp_verbes_audio_fix/verbes"
    target_dir = "/app/frontend/assets/audio/verbes"
    
    # Créer le répertoire cible s'il n'existe pas
    os.makedirs(target_dir, exist_ok=True)
    
    # Copier tous les fichiers
    if os.path.exists(source_dir):
        os.system(f"cp {source_dir}/* {target_dir}/")
        logger.info(f"Fichiers audio copiés de {source_dir} vers {target_dir}")
        
        # Compter les fichiers copiés
        copied_files = len([f for f in os.listdir(target_dir) if f.endswith('.m4a')])
        logger.info(f"Total fichiers copiés: {copied_files}")
        return True
    else:
        logger.error(f"Répertoire source introuvable: {source_dir}")
        return False

def main():
    """Fonction principale"""
    logger.info("Début de l'association exacte des prononciations verbes")
    
    try:
        # Copier les fichiers audio
        if not copy_audio_files():
            return 1
        
        # Connexion à la base de données
        db = connect_to_database()
        
        # Récupérer tous les verbes
        verbes = list(db['vocabulary'].find({"section": "verbes"}))
        logger.info(f"Verbes trouvés dans la base: {len(verbes)}")
        
        # Lister les fichiers audio disponibles
        audio_dir = "/app/frontend/assets/audio/verbes"
        audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
        logger.info(f"Fichiers audio disponibles: {len(audio_files)}")
        
        # 1. Correspondances manuelles (prioritaires)
        manual_mappings = create_manual_mappings()
        manual_matches, used_files = apply_manual_mappings(verbes, manual_mappings, audio_files)
        
        # 2. Correspondances automatiques pour les verbes non traités
        remaining_verbes = [v for v in verbes if v['_id'] not in manual_matches]
        remaining_audio = [f for f in audio_files if f not in used_files]
        
        auto_matches, unmatched_verbes, unmatched_audio = find_exact_audio_matches(remaining_verbes, remaining_audio)
        
        # 3. Combiner toutes les correspondances
        all_matches = {**manual_matches, **auto_matches}
        
        # 4. Mettre à jour la base de données
        updated_count = update_verb_audio_references(db, all_matches)
        
        # Statistiques finales
        total_verbes = len(verbes)
        matched_verbes = len(all_matches)
        coverage_percentage = (matched_verbes / total_verbes) * 100 if total_verbes > 0 else 0
        
        logger.info(f"\n{'='*60}")
        logger.info("RÉSUMÉ FINAL - ASSOCIATIONS AUDIO VERBES")
        logger.info(f"{'='*60}")
        logger.info(f"Total verbes: {total_verbes}")
        logger.info(f"Correspondances trouvées: {matched_verbes} ({coverage_percentage:.1f}%)")
        logger.info(f"Correspondances manuelles: {len(manual_matches)}")
        logger.info(f"Correspondances automatiques: {len(auto_matches)}")
        logger.info(f"Verbes sans audio: {len(unmatched_verbes)}")
        logger.info(f"Fichiers audio non utilisés: {len(unmatched_audio)}")
        
        if unmatched_verbes:
            logger.info("\nVerbes sans correspondance audio:")
            for verb in unmatched_verbes[:5]:
                logger.info(f"  - {verb.get('french')}: shimaoré '{verb.get('shimaoré')}', kibouchi '{verb.get('kibouchi')}'")
        
        if unmatched_audio:
            logger.info(f"\nFichiers audio non utilisés: {', '.join(unmatched_audio[:10])}")
        
        if coverage_percentage >= 80:
            logger.info("🎉 Correspondances audio verbes fixées avec succès!")
        else:
            logger.warning("⚠️ Certains verbes n'ont pas de correspondance audio")
            
    except Exception as e:
        logger.error(f"Erreur dans le script principal: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())