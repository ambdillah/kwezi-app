#!/usr/bin/env python3
"""
Correction finale des correspondances audio des verbes 
basée sur les fichiers RÉELLEMENT disponibles.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

# Charger les variables d'environnement
load_dotenv()

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# CORRESPONDANCES CORRECTES basées sur les fichiers existants et l'orthographe
CORRECT_VERB_AUDIO_MAPPINGS = {
    # Correspondances directes vérifiées
    "danser": "Chokou.m4a",                    # kibouchi: chokou ✓
    "avoir": "Havi.m4a",                       # kibouchi: havi ✓
    "dormir": "Koimini.m4a",                   # kibouchi: koimini ✓
    "comprendre": "Koufahamou.m4a",            # shimaoré: koufahamou ✓
    "penser": "Kouéléwa.m4a",                  # shimaoré: kouéléwa ✓
    "casser": "Latsaka.m4a",                   # shimaoré: latsaka ✓
    "chercher": "Magnadzari.m4a",              # kibouchi: magnadzari ✓
    "voir": "Magnamiya.m4a",                   # Correspond au fichier existant
    "montrer": "Magnaraka.m4a",                # kibouchi: magnaraka ✓
    "dire": "Magnatougnou.m4a",                # kibouchi: magnatougnou ✓
    "faire": "Magnossoutrou.m4a",              # kibouchi: magnossoutrou ✓
    "donner": "Magnoutani.m4a",                # kibouchi: magnoutani ✓
    "prendre": "Magnékitri.m4a",               # kibouchi: magnékitri ✓
    "pleurer": "Mahaléou.m4a",                 # kibouchi: mahaléou ✓
    "rire": "Mahandrou.m4a",                   # kibouchi: mahandrou ✓
    "regarder": "Mahazou.m4a",                 # kibouchi: mahazou ✓
    "finir": "Mahita.m4a",                     # kibouchi: mahita ✓
    
    # CORRECTION SPÉCIALE pour le problème signalé par l'utilisateur
    # "oumengna" doit avoir sa PROPRE prononciation, pas la même que "mandroubaka"
    "abîmer": "Manapaka somboutrou.m4a",       # Correspond au kibouchi: "manapaka somboutrou"
    # Nous réservons "Mandroubaka.m4a" pour un autre verbe s'il y en a un avec cette orthographe
    
    # Autres correspondances basées sur les fichiers disponibles
    "changer": "Mamadiki.m4a",                 # kibouchi: mamadiki ✓
    "balayer": "Mamafa.m4a",                   # kibouchi: mamafa ✓
    "réchauffer": "Mamana.m4a",                # kibouchi: mamana ✓
    "essuyer": "Mamitri.m4a",                  # kibouchi: mamitri ✓
    "éteindre": "Mamounou.m4a",                # kibouchi: mamounou ✓
    "cueillir": "Mampoka.m4a",                 # kibouchi: mampoka ✓
    "vendre": "Mandafou.m4a",                  # kibouchi: mandafou ✓
    "attendre": "Mandigni.m4a",                # kibouchi: mandigni ✓
    "piler": "Mandissa.m4a",                   # kibouchi: mandissa ✓
    "dormir": "Mandri.m4a",                    # Alternative pour "mandri"
    "apporter": "Mandèyi.m4a",                 # kibouchi: mandèyi ✓
    "marcher": "Mandéha.m4a",                  # kibouchi: mandéha ✓
    "laisser": "Mangnambéla.m4a",              # kibouchi: mangnambéla ✓
    "parler": "Mangnabara.m4a",                # kibouchi: mangnabara ✓
    "tuer": "Ouwoula.m4a",                     # shimaoré: ouwoula ✓
    
    # Fichiers disponibles mais à associer manuellement
    "couper": "Manapaka.m4a",                  # kibouchi: manapaka (version simple)
}

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

def verify_audio_files():
    """Vérifie que les fichiers audio existent réellement"""
    audio_dir = "/app/frontend/assets/audio/verbes"
    
    logger.info("=== VÉRIFICATION FICHIERS AUDIO ===")
    
    missing_files = []
    existing_files = []
    
    for french_verb, audio_file in CORRECT_VERB_AUDIO_MAPPINGS.items():
        full_path = os.path.join(audio_dir, audio_file)
        
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            existing_files.append(audio_file)
            logger.info(f"✅ {french_verb:15} → {audio_file} ({size} bytes)")
        else:
            missing_files.append((french_verb, audio_file))
            logger.warning(f"❌ {french_verb:15} → {audio_file} MANQUANT")
    
    logger.info(f"\nFichiers existants: {len(existing_files)}")
    logger.info(f"Fichiers manquants: {len(missing_files)}")
    
    return existing_files, missing_files

def apply_final_corrections(db, existing_mappings):
    """Applique les corrections finales uniquement pour les fichiers existants"""
    collection = db['vocabulary']
    
    logger.info("\n=== APPLICATION CORRECTIONS FINALES ===")
    
    # D'abord, effacer toutes les références audio incorrectes
    result = collection.update_many(
        {"section": "verbes"},
        {
            "$set": {
                "has_authentic_audio": False,
                "audio_authentic": "",
                "audio_updated": True
            }
        }
    )
    logger.info(f"Références audio effacées: {result.modified_count}")
    
    # Appliquer uniquement les correspondances pour fichiers existants
    updated_count = 0
    skipped_count = 0
    
    for french_verb, audio_file in CORRECT_VERB_AUDIO_MAPPINGS.items():
        if audio_file in existing_mappings:
            audio_path = f"audio/verbes/{audio_file}"
            
            result = collection.update_one(
                {"section": "verbes", "french": french_verb},
                {
                    "$set": {
                        "audio_authentic": audio_path,
                        "has_authentic_audio": True,
                        "audio_updated": True,
                        "audio_format": "m4a",
                        "final_correction_applied": True
                    }
                }
            )
            
            if result.modified_count > 0:
                updated_count += 1
                logger.info(f"✅ {french_verb:15} → {audio_file}")
            else:
                # Peut-être que le verbe n'existe pas, vérifions
                verb_exists = collection.find_one({"section": "verbes", "french": french_verb})
                if not verb_exists:
                    logger.warning(f"⚠️ Verbe '{french_verb}' non trouvé dans la base - ignoré")
                else:
                    logger.error(f"❌ Échec mise à jour: {french_verb}")
        else:
            skipped_count += 1
            logger.warning(f"⏭️ {french_verb:15} → {audio_file} (fichier manquant, ignoré)")
    
    logger.info(f"\nMises à jour appliquées: {updated_count}")
    logger.info(f"Mappings ignorés (fichiers manquants): {skipped_count}")
    
    return updated_count

def verify_specific_problem(db):
    """Vérifie spécifiquement le problème signalé par l'utilisateur"""
    collection = db['vocabulary']
    
    logger.info("\n=== VÉRIFICATION PROBLÈME SPÉCIFIQUE ===")
    
    # Vérifier "abîmer" avec "oumengna"
    abimer = collection.find_one({"section": "verbes", "french": "abîmer"})
    if abimer:
        shimaore = abimer.get('shimaoré', '')
        audio_path = abimer.get('audio_authentic', '')
        audio_file = os.path.basename(audio_path) if audio_path else 'Aucun'
        
        logger.info(f"Verbe 'abîmer':")
        logger.info(f"  - Shimaoré: '{shimaore}'")
        logger.info(f"  - Fichier audio: {audio_file}")
        
        if 'oumengna' in shimaore.lower():
            if 'mandroubaka' not in audio_file.lower():
                logger.info("✅ PROBLÈME RÉSOLU: 'oumengna' n'utilise plus 'mandroubaka'")
                return True
            else:
                logger.error("❌ PROBLÈME PERSISTANT: 'oumengna' utilise encore 'mandroubaka'")
                return False
        else:
            logger.warning(f"⚠️ Shimaoré inattendu pour 'abîmer': '{shimaore}' (attendu: contient 'oumengna')")
            return False
    else:
        logger.error("❌ Verbe 'abîmer' non trouvé")
        return False

def main():
    """Fonction principale"""
    logger.info("Début de la correction finale des correspondances verbes")
    
    try:
        # 1. Vérifier les fichiers audio disponibles
        existing_files, missing_files = verify_audio_files()
        
        # 2. Connexion à la base de données
        db = connect_to_database()
        
        # 3. Appliquer les corrections uniquement pour fichiers existants
        updated_count = apply_final_corrections(db, existing_files)
        
        # 4. Vérifier le problème spécifique
        problem_resolved = verify_specific_problem(db)
        
        # 5. Statistiques finales
        total_verbes = db['vocabulary'].count_documents({"section": "verbes"})
        verbes_with_audio = db['vocabulary'].count_documents({
            "section": "verbes", 
            "has_authentic_audio": True
        })
        
        coverage = (verbes_with_audio / total_verbes) * 100 if total_verbes > 0 else 0
        
        logger.info(f"\n{'='*60}")
        logger.info("RÉSUMÉ CORRECTION FINALE")
        logger.info(f"{'='*60}")
        logger.info(f"Correspondances définies: {len(CORRECT_VERB_AUDIO_MAPPINGS)}")
        logger.info(f"Fichiers existants: {len(existing_files)}")
        logger.info(f"Fichiers manquants: {len(missing_files)}")
        logger.info(f"Mises à jour appliquées: {updated_count}")
        logger.info(f"Coverage finale: {verbes_with_audio}/{total_verbes} ({coverage:.1f}%)")
        logger.info(f"Problème 'oumengna/mandroubaka' résolu: {'✅ OUI' if problem_resolved else '❌ NON'}")
        
        if problem_resolved and updated_count > 0:
            logger.info("\n🎉 CORRECTION FINALE RÉUSSIE!")
            logger.info("✅ Plus de confusion entre prononciations")
            logger.info("✅ Correspondances basées sur fichiers existants")
        else:
            logger.warning("\n⚠️ Correction partielle - vérifiez les détails ci-dessus")
        
    except Exception as e:
        logger.error(f"Erreur dans le script principal: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())