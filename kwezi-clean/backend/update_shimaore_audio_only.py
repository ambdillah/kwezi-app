#!/usr/bin/env python3
"""
Mise à jour des prononciations shimaoré uniquement pour la section "verbes"
avec le nouveau fichier ZIP (98 fichiers shimaoré)
Préserve les prononciations kibouchi existantes
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

def get_shimaore_audio_files():
    """Récupère tous les fichiers audio shimaoré du nouveau ZIP"""
    source_dir = "/app/backend/verbes_shimaore_extract/verbes1"
    
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
    
    logger.info(f"Fichiers audio shimaoré trouvés: {len(audio_files)}")
    return audio_files

def get_verbs_from_database():
    """Récupère tous les verbes de la base de données"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    verbs = list(collection.find({"section": "verbes"}).sort("french", 1))
    logger.info(f"Verbes en base: {len(verbs)}")
    
    return verbs

def clean_text_for_matching(text):
    """Nettoie un texte pour la correspondance"""
    if not text:
        return ""
    
    # Normaliser pour la comparaison
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

def find_shimaore_audio_match(shimaore_text, audio_files):
    """Trouve la correspondance audio pour une traduction shimaoré"""
    if not shimaore_text:
        return None
    
    text_clean = clean_text_for_matching(shimaore_text)
    
    # 1. Correspondance exacte
    for audio in audio_files:
        if audio['name_clean'] == text_clean:
            return audio['filename']
    
    # 2. Correspondance partielle stricte
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

def update_shimaore_audio_mappings():
    """Met à jour uniquement les correspondances audio shimaoré"""
    logger.info("🔄 MISE À JOUR AUDIO SHIMAORÉ UNIQUEMENT")
    
    # Récupérer les données
    audio_files = get_shimaore_audio_files()
    verbs = get_verbs_from_database()
    
    if not audio_files or not verbs:
        logger.error("Erreur: fichiers audio ou verbes manquants")
        return []
    
    # Traquer l'utilisation des fichiers
    used_files = set()
    mappings = []
    
    logger.info(f"\n{'='*100}")
    logger.info(f"MISE À JOUR AUDIO SHIMAORÉ VERBES")
    logger.info(f"{'='*100}")
    logger.info(f"{'Français':20} | {'Shimaoré':25} | {'Nouvel Audio Shimaoré':30} | {'Ancien Audio':25}")
    logger.info("-" * 100)
    
    for verb in verbs:
        french = verb.get('french', '')
        shimaore = verb.get('shimaoré', '')
        kibouchi = verb.get('kibouchi', '')
        verb_id = verb['_id']
        old_shimaore_audio = verb.get('audio_shimaoré_filename', 'Aucun')
        
        # Trouver nouvelle correspondance shimaoré
        available_files = [f for f in audio_files if f['filename'] not in used_files]
        new_shimaore_audio = find_shimaore_audio_match(shimaore, available_files)
        
        if new_shimaore_audio:
            used_files.add(new_shimaore_audio)
        
        # Si pas de correspondance, essayer dans tous les fichiers
        if shimaore and not new_shimaore_audio:
            remaining_files = [f for f in audio_files if f['filename'] not in used_files]
            new_shimaore_audio = find_shimaore_audio_match(shimaore, remaining_files)
            if new_shimaore_audio:
                used_files.add(new_shimaore_audio)
        
        # Créer le mapping (uniquement si on a trouvé un nouveau fichier)
        if new_shimaore_audio:
            mapping = {
                'verb_id': verb_id,
                'french': french,
                'shimaore': shimaore,
                'kibouchi': kibouchi,  # Préservé
                'old_shimaore_audio': old_shimaore_audio,
                'new_shimaore_audio': new_shimaore_audio,
                'kibouchi_audio': verb.get('audio_kibouchi_filename')  # Préservé
            }
            
            mappings.append(mapping)
            
            # Affichage
            change_indicator = "🆕" if old_shimaore_audio != new_shimaore_audio else "✅"
            logger.info(f"{french:20} | {shimaore:25} | {change_indicator} {new_shimaore_audio:28} | {old_shimaore_audio:25}")
        else:
            # Pas de nouveau fichier trouvé
            old_audio_display = old_shimaore_audio if old_shimaore_audio else 'Aucun'
            shimaore_display = shimaore if shimaore else 'N/A'
            logger.info(f"{french:20} | {shimaore_display:25} | ❌ Aucun nouveau fichier trouvé | {old_audio_display:25}")
    
    # Statistiques
    new_matches = sum(1 for m in mappings if m['new_shimaore_audio'] != m['old_shimaore_audio'])
    unchanged = sum(1 for m in mappings if m['new_shimaore_audio'] == m['old_shimaore_audio'])
    
    logger.info(f"\n📊 STATISTIQUES MISE À JOUR:")
    logger.info(f"  Nouvelles correspondances: {new_matches}")
    logger.info(f"  Correspondances inchangées: {unchanged}")
    logger.info(f"  Total mappings: {len(mappings)}")
    logger.info(f"  Fichiers utilisés: {len(used_files)}/{len(audio_files)}")
    
    return mappings

def apply_shimaore_updates_to_database(mappings):
    """Applique les mises à jour shimaoré à la base de données"""
    logger.info("\n🔄 APPLICATION MISES À JOUR SHIMAORÉ")
    
    db = connect_to_database()
    collection = db['vocabulary']
    
    updated_count = 0
    
    for mapping in mappings:
        try:
            # Mettre à jour uniquement les champs shimaoré
            update_data = {
                "audio_shimaoré_filename": mapping['new_shimaore_audio'],
                "audio_shimaoré_url": f"audio/verbes/{mapping['new_shimaore_audio']}",
                "has_shimaoré_audio": True,
                "shimaore_audio_updated": True
                # Les champs kibouchi sont préservés automatiquement
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

def copy_shimaore_audio_files(audio_files):
    """Copie les nouveaux fichiers audio shimaoré vers assets"""
    logger.info("\n📁 COPIE NOUVEAUX FICHIERS AUDIO SHIMAORÉ")
    
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
    
    logger.info(f"✅ {copied_count} fichiers shimaoré copiés")
    return copied_count

def verify_shimaore_update():
    """Vérifie la mise à jour shimaoré"""
    logger.info("\n=== VÉRIFICATION FINALE SHIMAORÉ ===")
    
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
            logger.info(f"    Kibouchi: {verb.get('kibouchi', 'N/A'):20} → {kibouchi_audio} (préservé)")
            
            # Vérifier que les fichiers existent
            if shimaore_audio != 'Aucun':
                file_path = f"/app/frontend/assets/audio/verbes/{shimaore_audio}"
                exists = os.path.exists(file_path)
                logger.info(f"    Fichier shimaoré: {'✅' if exists else '❌'}")
    
    return {
        'total': total_verbs,
        'shimaore': verbs_with_shimaore,
        'kibouchi': verbs_with_kibouchi,
        'both': verbs_with_both
    }

def main():
    """Fonction principale"""
    logger.info("🎯 MISE À JOUR AUDIO SHIMAORÉ VERBES - NOUVEAU ZIP")
    
    try:
        # 1. Créer les nouvelles correspondances shimaoré
        mappings = update_shimaore_audio_mappings()
        
        if not mappings:
            logger.warning("Aucune correspondance shimaoré trouvée")
            return False
        
        # 2. Copier les nouveaux fichiers audio shimaoré
        audio_files = get_shimaore_audio_files()
        copied_count = copy_shimaore_audio_files(audio_files)
        
        # 3. Appliquer les mises à jour en base
        updated_count = apply_shimaore_updates_to_database(mappings)
        
        # 4. Vérifier le résultat
        stats = verify_shimaore_update()
        
        # 5. Résumé final
        logger.info(f"\n{'='*100}")
        logger.info("RÉSUMÉ MISE À JOUR AUDIO SHIMAORÉ")
        logger.info(f"{'='*100}")
        logger.info(f"✅ Fichiers shimaoré copiés: {copied_count}")
        logger.info(f"✅ Verbes mis à jour: {updated_count}")
        logger.info(f"📊 Coverage shimaoré: {stats['shimaore']}/{stats['total']} ({stats['shimaore']/stats['total']*100:.1f}%)")
        logger.info(f"📊 Coverage kibouchi: {stats['kibouchi']}/{stats['total']} (préservé)")
        logger.info(f"🎯 Coverage complète: {stats['both']}/{stats['total']} ({stats['both']/stats['total']*100:.1f}%)")
        
        logger.info(f"\n🎉 MISE À JOUR SHIMAORÉ TERMINÉE!")
        logger.info(f"Les prononciations shimaoré ont été mises à jour selon votre nouveau ZIP.")
        logger.info(f"Les prononciations kibouchi existantes ont été préservées.")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans la mise à jour shimaoré: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)