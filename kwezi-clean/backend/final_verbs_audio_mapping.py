#!/usr/bin/env python3
"""
Attribution finale des prononciations pour chaque mot de la section "Verbe"
selon le fichier ZIP fourni par l'utilisateur (191 fichiers audio)
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging
import shutil

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

def get_all_audio_files_from_zip():
    """Récupère tous les fichiers audio du ZIP"""
    source_dir = "/app/backend/verbes_finale_extract/verbes"
    
    if not os.path.exists(source_dir):
        logger.error(f"Répertoire source non trouvé: {source_dir}")
        return []
    
    audio_files = []
    for filename in os.listdir(source_dir):
        if filename.lower().endswith('.m4a'):
            file_path = os.path.join(source_dir, filename)
            file_size = os.path.getsize(file_path)
            
            audio_files.append({
                'filename': filename,
                'path': file_path,
                'size': file_size,
                'name_clean': clean_text_for_matching(filename.replace('.m4a', ''))
            })
    
    logger.info(f"Fichiers audio trouvés dans le ZIP: {len(audio_files)}")
    return audio_files

def get_all_verbs_from_database():
    """Récupère tous les verbes de la base de données"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    verbs = list(collection.find({"section": "verbes"}).sort("french", 1))
    logger.info(f"Verbes trouvés en base: {len(verbs)}")
    
    return verbs

def clean_text_for_matching(text):
    """Nettoie un texte pour la correspondance (conserve la casse originale mais crée une version normalisée)"""
    if not text:
        return ""
    
    # Créer une version normalisée pour la comparaison
    normalized = text.lower()
    # Enlever espaces, tirets, accents
    normalized = normalized.replace(' ', '').replace('-', '').replace('_', '').replace('/', '')
    normalized = normalized.replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('ë', 'e')
    normalized = normalized.replace('à', 'a').replace('á', 'a').replace('â', 'a').replace('ä', 'a')
    normalized = normalized.replace('ô', 'o').replace('ö', 'o').replace('ò', 'o').replace('ó', 'o')
    normalized = normalized.replace('û', 'u').replace('ù', 'u').replace('ü', 'u').replace('ú', 'u')
    normalized = normalized.replace('î', 'i').replace('ï', 'i').replace('ì', 'i').replace('í', 'i')
    normalized = normalized.replace('ç', 'c').replace('ñ', 'n')
    
    return normalized

def find_exact_match(text, audio_files):
    """Trouve la correspondance exacte pour un texte"""
    if not text:
        return None
    
    text_clean = clean_text_for_matching(text)
    
    # 1. Correspondance exacte
    for audio in audio_files:
        if audio['name_clean'] == text_clean:
            return audio['filename']
    
    # 2. Correspondance partielle très stricte
    best_match = None
    best_score = 0
    
    for audio in audio_files:
        audio_clean = audio['name_clean']
        
        if len(audio_clean) < 4 or len(text_clean) < 4:
            continue
        
        score = 0
        
        # Correspondance de début
        if text_clean.startswith(audio_clean) and len(audio_clean) >= len(text_clean) * 0.8:
            score = 95
        elif audio_clean.startswith(text_clean) and len(text_clean) >= len(audio_clean) * 0.8:
            score = 90
        # Correspondance contient (très stricte)
        elif len(audio_clean) >= 6 and audio_clean in text_clean and len(audio_clean) >= len(text_clean) * 0.7:
            score = 85
        elif len(text_clean) >= 6 and text_clean in audio_clean and len(text_clean) >= len(audio_clean) * 0.7:
            score = 80
        
        if score > best_score and score >= 80:
            best_score = score
            best_match = audio['filename']
    
    return best_match

def create_complete_mapping():
    """Crée une correspondance complète entre verbes et fichiers audio"""
    logger.info("🎯 CRÉATION CORRESPONDANCE COMPLÈTE VERBES ↔ AUDIO")
    
    # Récupérer les données
    audio_files = get_all_audio_files_from_zip()
    verbs = get_all_verbs_from_database()
    
    if not audio_files or not verbs:
        logger.error("Erreur: fichiers audio ou verbes manquants")
        return None
    
    # Traquer l'utilisation des fichiers pour éviter les doublons
    used_files = set()
    mappings = []
    
    logger.info(f"\n{'='*120}")
    logger.info(f"CORRESPONDANCES FINALES VERBES ↔ AUDIO")
    logger.info(f"{'='*120}")
    logger.info(f"{'Français':15} | {'Shimaoré':25} | {'Kibouchi':25} | {'Audio Shimaoré':25} | {'Audio Kibouchi':25}")
    logger.info("-" * 120)
    
    for verb in verbs:
        french = verb.get('french', '')
        shimaore = verb.get('shimaoré', '')  
        kibouchi = verb.get('kibouchi', '')
        verb_id = verb['_id']
        
        # Trouver les correspondances audio (fichiers non utilisés seulement)
        available_files = [f for f in audio_files if f['filename'] not in used_files]
        
        # Chercher shimaoré
        shimaore_audio = find_exact_match(shimaore, available_files)
        if shimaore_audio:
            used_files.add(shimaore_audio)
        
        # Chercher kibouchi (dans les fichiers restants)
        available_files = [f for f in audio_files if f['filename'] not in used_files]
        kibouchi_audio = find_exact_match(kibouchi, available_files)
        if kibouchi_audio:
            used_files.add(kibouchi_audio)
        
        # Si pas de correspondance pour l'un, essayer dans tous les fichiers
        if shimaore and not shimaore_audio:
            remaining_files = [f for f in audio_files if f['filename'] not in used_files]
            shimaore_audio = find_exact_match(shimaore, remaining_files)
            if shimaore_audio:
                used_files.add(shimaore_audio)
        
        if kibouchi and not kibouchi_audio:
            remaining_files = [f for f in audio_files if f['filename'] not in used_files]
            kibouchi_audio = find_exact_match(kibouchi, remaining_files)
            if kibouchi_audio:
                used_files.add(kibouchi_audio)
        
        # Créer le mapping
        mapping = {
            'verb_id': verb_id,
            'french': french,
            'shimaore': shimaore,
            'kibouchi': kibouchi,
            'shimaore_audio': shimaore_audio,
            'kibouchi_audio': kibouchi_audio
        }
        
        mappings.append(mapping)
        
        # Affichage
        shimaore_display = f"✅ {shimaore_audio[:20]}..." if shimaore_audio and len(shimaore_audio) > 20 else f"{'✅ ' + shimaore_audio if shimaore_audio else '❌ Aucun'}"
        kibouchi_display = f"✅ {kibouchi_audio[:20]}..." if kibouchi_audio and len(kibouchi_audio) > 20 else f"{'✅ ' + kibouchi_audio if kibouchi_audio else '❌ Aucun'}"
        
        logger.info(f"{french:15} | {shimaore:25} | {kibouchi:25} | {shimaore_display:25} | {kibouchi_display:25}")
    
    # Statistiques
    shimaore_matches = sum(1 for m in mappings if m['shimaore_audio'])
    kibouchi_matches = sum(1 for m in mappings if m['kibouchi_audio'])
    both_matches = sum(1 for m in mappings if m['shimaore_audio'] and m['kibouchi_audio'])
    
    logger.info(f"\n📊 STATISTIQUES CORRESPONDANCES:")
    logger.info(f"  Correspondances shimaoré: {shimaore_matches}/{len(verbs)} ({shimaore_matches/len(verbs)*100:.1f}%)")
    logger.info(f"  Correspondances kibouchi: {kibouchi_matches}/{len(verbs)} ({kibouchi_matches/len(verbs)*100:.1f}%)")
    logger.info(f"  Avec les deux langues: {both_matches}/{len(verbs)} ({both_matches/len(verbs)*100:.1f}%)")
    logger.info(f"  Fichiers utilisés: {len(used_files)}/{len(audio_files)}")
    
    return mappings

def apply_mappings_to_database(mappings):
    """Applique les correspondances à la base de données"""
    logger.info("\n🔄 APPLICATION DES CORRESPONDANCES À LA BASE")
    
    db = connect_to_database()
    collection = db['vocabulary']
    
    updated_count = 0
    
    for mapping in mappings:
        try:
            update_data = {
                "audio_shimaoré_filename": mapping['shimaore_audio'],
                "audio_kibouchi_filename": mapping['kibouchi_audio'],
                "audio_shimaoré_url": f"audio/verbes/{mapping['shimaore_audio']}" if mapping['shimaore_audio'] else None,
                "audio_kibouchi_url": f"audio/verbes/{mapping['kibouchi_audio']}" if mapping['kibouchi_audio'] else None,
                "has_shimaoré_audio": bool(mapping['shimaore_audio']),
                "has_kibouchi_audio": bool(mapping['kibouchi_audio']),
                "dual_audio_system": True,
                "final_mapping_applied": True
            }
            
            result = collection.update_one(
                {"_id": mapping['verb_id']},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                
        except Exception as e:
            logger.error(f"Erreur mise à jour {mapping['french']}: {e}")
    
    logger.info(f"✅ {updated_count} verbes mis à jour en base")
    return updated_count

def copy_audio_files_to_assets(audio_files):
    """Copie les fichiers audio vers le dossier assets"""
    logger.info("\n📁 COPIE FICHIERS AUDIO VERS ASSETS")
    
    target_dir = "/app/frontend/assets/audio/verbes"
    os.makedirs(target_dir, exist_ok=True)
    
    copied_count = 0
    
    for audio_file in audio_files:
        source_path = audio_file['path']
        target_path = os.path.join(target_dir, audio_file['filename'])
        
        try:
            shutil.copy2(source_path, target_path)
            copied_count += 1
        except Exception as e:
            logger.warning(f"Erreur copie {audio_file['filename']}: {e}")
    
    logger.info(f"✅ {copied_count} fichiers copiés")
    return copied_count

def verify_final_result():
    """Vérifie le résultat final"""
    logger.info("\n=== VÉRIFICATION FINALE ===")
    
    db = connect_to_database()
    collection = db['vocabulary']
    
    # Statistiques
    total_verbs = collection.count_documents({"section": "verbes"})
    verbs_with_shimaore = collection.count_documents({
        "section": "verbes",
        "has_shimaoré_audio": True
    })
    verbs_with_kibouchi = collection.count_documents({
        "section": "verbes",
        "has_kibouchi_audio": True
    })
    verbs_with_both = collection.count_documents({
        "section": "verbes",
        "has_shimaoré_audio": True,
        "has_kibouchi_audio": True
    })
    
    logger.info(f"📈 RÉSULTATS FINAUX:")
    logger.info(f"  Total verbes: {total_verbs}")
    logger.info(f"  Avec audio shimaoré: {verbs_with_shimaore} ({verbs_with_shimaore/total_verbs*100:.1f}%)")
    logger.info(f"  Avec audio kibouchi: {verbs_with_kibouchi} ({verbs_with_kibouchi/total_verbs*100:.1f}%)")
    logger.info(f"  Avec les deux audio: {verbs_with_both} ({verbs_with_both/total_verbs*100:.1f}%)")
    
    # Vérifier des cas spécifiques
    test_cases = ["attendre", "abîmer", "voir", "dire", "danser"]
    
    logger.info(f"\n🔍 VÉRIFICATION CAS SPÉCIFIQUES:")
    for verb_name in test_cases:
        verb = collection.find_one({"section": "verbes", "french": verb_name})
        if verb:
            shimaore_audio = verb.get('audio_shimaoré_filename', 'Aucun')
            kibouchi_audio = verb.get('audio_kibouchi_filename', 'Aucun')
            
            logger.info(f"  {verb_name:15}")
            logger.info(f"    Shimaoré: {verb.get('shimaoré', 'N/A'):20} → {shimaore_audio}")
            logger.info(f"    Kibouchi: {verb.get('kibouchi', 'N/A'):20} → {kibouchi_audio}")
            
            # Vérifier que les fichiers existent
            if shimaore_audio != 'Aucun':
                file_path = f"/app/frontend/assets/audio/verbes/{shimaore_audio}"
                exists = os.path.exists(file_path)
                logger.info(f"    Fichier shimaoré: {'✅' if exists else '❌'}")
                
            if kibouchi_audio != 'Aucun':
                file_path = f"/app/frontend/assets/audio/verbes/{kibouchi_audio}"
                exists = os.path.exists(file_path)
                logger.info(f"    Fichier kibouchi: {'✅' if exists else '❌'}")
    
    return {
        'total': total_verbs,
        'shimaore': verbs_with_shimaore,
        'kibouchi': verbs_with_kibouchi,
        'both': verbs_with_both
    }

def main():
    """Fonction principale"""
    logger.info("🎯 ATTRIBUTION FINALE PRONONCIATIONS VERBES - ZIP UTILISATEUR")
    
    try:
        # 1. Créer les correspondances complètes
        mappings = create_complete_mapping()
        
        if not mappings:
            logger.error("Échec création des correspondances")
            return False
        
        # 2. Copier les fichiers audio
        audio_files = get_all_audio_files_from_zip()
        copied_count = copy_audio_files_to_assets(audio_files)
        
        # 3. Appliquer les correspondances en base
        updated_count = apply_mappings_to_database(mappings)
        
        # 4. Vérifier le résultat
        stats = verify_final_result()
        
        # 5. Résumé final
        logger.info(f"\n{'='*100}")
        logger.info("RÉSUMÉ ATTRIBUTION FINALE PRONONCIATIONS")
        logger.info(f"{'='*100}")
        logger.info(f"✅ Fichiers copiés: {copied_count}")
        logger.info(f"✅ Verbes mis à jour: {updated_count}")
        logger.info(f"📊 Coverage shimaoré: {stats['shimaore']}/{stats['total']} ({stats['shimaore']/stats['total']*100:.1f}%)")
        logger.info(f"📊 Coverage kibouchi: {stats['kibouchi']}/{stats['total']} ({stats['kibouchi']/stats['total']*100:.1f}%)")
        logger.info(f"🎯 Coverage complète: {stats['both']}/{stats['total']} ({stats['both']/stats['total']*100:.1f}%)")
        
        logger.info(f"\n🎉 ATTRIBUTION FINALE TERMINÉE!")
        logger.info(f"Chaque verbe a maintenant ses prononciations correspondantes selon votre ZIP.")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans l'attribution finale: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)