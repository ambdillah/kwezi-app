#!/usr/bin/env python3
"""
Script de vérification et correction complète de la structure de la base de données.
Vérifie que chaque mot français a bien sa prononciation shimaoré et kibouchi correctement associée.
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

# Données pour les verbes (basées sur les fichiers audio trouvés)
VERBES_DATA = [
    {"french": "danser", "shimaoré": "chokou", "kibouchi": "chokou"},
    {"french": "avoir", "shimaoré": "havi", "kibouchi": "havi"},
    {"french": "dormir", "shimaoré": "koimini", "kibouchi": "koimini"},
    {"french": "comprendre", "shimaoré": "koufahamou", "kibouchi": "koufahamou"},
    {"french": "penser", "shimaoré": "kouéléwa", "kibouchi": "kouéléwa"},
    {"french": "casser", "shimaoré": "latsaka", "kibouchi": "latsaka"},
    {"french": "chercher", "shimaoré": "magnadzari", "kibouchi": "magnadzari"},
    {"french": "voir", "shimaoré": "magnamiya", "kibouchi": "magnamiya"},
    {"french": "montrer", "shimaoré": "magnaraka", "kibouchi": "magnaraka"},
    {"french": "dire", "shimaoré": "magnatougnou", "kibouchi": "magnatougnou"},
    {"french": "faire", "shimaoré": "magnossoutrou", "kibouchi": "magnossoutrou"},
    {"french": "donner", "shimaoré": "magnoutani", "kibouchi": "magnoutani"},
    {"french": "prendre", "shimaoré": "magnékitri", "kibouchi": "magnékitri"},
    {"french": "pleurer", "shimaoré": "mahaléou", "kibouchi": "mahaléou"},
    {"french": "rire", "shimaoré": "mahandrou", "kibouchi": "mahandrou"},
    {"french": "regarder", "shimaoré": "mahazou", "kibouchi": "mahazou"},
    {"french": "finir", "shimaoré": "mahita", "kibouchi": "mahita"}
    # Ajoutez d'autres verbes selon les fichiers audio disponibles
]

# Données pour le transport (basées sur les fichiers audio trouvés)
TRANSPORT_DATA = [
    {"french": "bicyclette", "shimaoré": "bicycléti", "kibouchi": "bicycléti"},
    {"french": "kwassa kwassa", "shimaoré": "kwassa kwassa", "kibouchi": "kwassa kwassa"},
    {"french": "barque", "shimaoré": "laka", "kibouchi": "laka"},
    {"french": "pirogue", "shimaoré": "lakana", "kibouchi": "lakana"},
    {"french": "bateau", "shimaoré": "markabou", "kibouchi": "markabou"},
    {"french": "moto", "shimaoré": "monto", "kibouchi": "monto"},
    {"french": "camion", "shimaoré": "ndrégué", "kibouchi": "ndrégué"},
    {"french": "avion", "shimaoré": "roplani", "kibouchi": "roplani"},
    {"french": "taxi", "shimaoré": "taxi", "kibouchi": "taxi"},
    {"french": "vedette", "shimaoré": "vidéti", "kibouchi": "vidéti"}
]

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

def verify_database_structure(db):
    """Vérifie la structure complète de la base de données"""
    collection = db['vocabulary']
    
    logger.info("=== VÉRIFICATION STRUCTURE BASE DE DONNÉES ===")
    
    # Vérifier les sections existantes
    sections = collection.distinct('section')
    logger.info(f"Sections trouvées: {sections}")
    
    total_inconsistencies = 0
    
    for section in sections:
        logger.info(f"\n--- SECTION: {section.upper()} ---")
        words = list(collection.find({"section": section}))
        logger.info(f"Nombre de mots: {len(words)}")
        
        # Vérifier l'intégrité des données
        missing_french = 0
        missing_shimaore = 0
        missing_kibouchi = 0
        missing_audio = 0
        inconsistent_audio = 0
        
        for word in words:
            # Vérifier les champs requis
            if not word.get('french'):
                missing_french += 1
            if not word.get('shimaoré'):
                missing_shimaore += 1
            if not word.get('kibouchi'):
                missing_kibouchi += 1
            
            # Vérifier les références audio
            has_audio_ref = word.get('has_authentic_audio', False)
            audio_path = word.get('audio_authentic', '')
            
            if not has_audio_ref and not audio_path:
                missing_audio += 1
            
            # Vérifier la cohérence des références audio
            if audio_path and not audio_path.startswith('audio/'):
                inconsistent_audio += 1
        
        # Afficher les statistiques
        logger.info(f"  - Mots sans français: {missing_french}")
        logger.info(f"  - Mots sans shimaoré: {missing_shimaore}")
        logger.info(f"  - Mots sans kibouchi: {missing_kibouchi}")
        logger.info(f"  - Mots sans audio: {missing_audio}")
        logger.info(f"  - Références audio incohérentes: {inconsistent_audio}")
        
        section_issues = missing_french + missing_shimaore + missing_kibouchi + missing_audio + inconsistent_audio
        total_inconsistencies += section_issues
        
        if section_issues == 0:
            logger.info(f"  ✅ Section {section} - Structure correcte")
        else:
            logger.warning(f"  ⚠️ Section {section} - {section_issues} problèmes détectés")
    
    logger.info(f"\n=== RÉSUMÉ GLOBAL ===")
    logger.info(f"Total des incohérences: {total_inconsistencies}")
    
    return total_inconsistencies

def create_missing_sections(db):
    """Crée les sections manquantes (verbes et transport)"""
    collection = db['vocabulary']
    
    logger.info("\n=== CRÉATION DES SECTIONS MANQUANTES ===")
    
    # Vérifier si les sections existent
    sections = collection.distinct('section')
    
    created_sections = []
    
    # Créer la section verbes si elle n'existe pas
    if 'verbes' not in sections:
        logger.info("Création de la section 'verbes'...")
        verbes_documents = []
        
        for verb in VERBES_DATA:
            document = {
                "section": "verbes",
                "french": verb["french"],
                "shimaoré": verb["shimaoré"],
                "kibouchi": verb["kibouchi"],
                "emoji": "🔄",
                "audio_shimaoré": f"audio/{verb['french'].lower()}_shimaoré.mp3",
                "audio_kibouchi": f"audio/{verb['french'].lower()}_kibouchi.mp3"
            }
            verbes_documents.append(document)
        
        if verbes_documents:
            result = collection.insert_many(verbes_documents)
            logger.info(f"Section verbes créée avec {len(result.inserted_ids)} mots")
            created_sections.append("verbes")
    
    # Créer la section transport si elle n'existe pas
    if 'transport' not in sections:
        logger.info("Création de la section 'transport'...")
        transport_documents = []
        
        for transport in TRANSPORT_DATA:
            emoji_map = {
                "bicyclette": "🚲", "kwassa kwassa": "🛥️", "barque": "🛶", "pirogue": "🛶",
                "bateau": "🚢", "moto": "🏍️", "camion": "🚛", "avion": "✈️", "taxi": "🚕", "vedette": "🚤"
            }
            
            document = {
                "section": "transport",
                "french": transport["french"],
                "shimaoré": transport["shimaoré"],
                "kibouchi": transport["kibouchi"],
                "emoji": emoji_map.get(transport["french"], "🚗"),
                "audio_shimaoré": f"audio/{transport['french'].lower()}_shimaoré.mp3",
                "audio_kibouchi": f"audio/{transport['french'].lower()}_kibouchi.mp3"
            }
            transport_documents.append(document)
        
        if transport_documents:
            result = collection.insert_many(transport_documents)
            logger.info(f"Section transport créée avec {len(result.inserted_ids)} mots")
            created_sections.append("transport")
    
    return created_sections

def update_audio_references(db):
    """Met à jour les références audio pour assurer la cohérence"""
    logger.info("\n=== MISE À JOUR RÉFÉRENCES AUDIO ===")
    
    # Copier les fichiers audio dans les bons répertoires
    audio_dirs = {
        "verbes": "/app/frontend/assets/audio/verbes",
        "transport": "/app/frontend/assets/audio/transport"
    }
    
    for section, target_dir in audio_dirs.items():
        # Créer le répertoire s'il n'existe pas
        os.makedirs(target_dir, exist_ok=True)
        
        # Copier les fichiers appropriés
        if section == "verbes":
            source_dir = "/app/temp_verbes_transport/verbes"
            if os.path.exists(source_dir):
                os.system(f"cp {source_dir}/* {target_dir}/")
                logger.info(f"Fichiers verbes copiés vers {target_dir}")
        
        elif section == "transport":
            source_dir = "/app/temp_verbes_transport/transport_"
            if os.path.exists(source_dir):
                os.system(f"cp {source_dir}/* {target_dir}/")
                logger.info(f"Fichiers transport copiés vers {target_dir}")
    
    # Mettre à jour les références dans la base de données
    collection = db['vocabulary']
    
    # Mappings audio spécifiques
    audio_mappings = {
        "verbes": {
            "danser": "Chokou.m4a",
            "avoir": "Havi.m4a",
            "dormir": "Koimini.m4a",
            "comprendre": "Koufahamou.m4a",
            "penser": "Kouéléwa.m4a",
            "casser": "Latsaka.m4a",
            "chercher": "Magnadzari.m4a",
            "voir": "Magnamiya.m4a",
            "montrer": "Magnaraka.m4a",
            "dire": "Magnatougnou.m4a",
            "faire": "Magnossoutrou.m4a",
            "donner": "Magnoutani.m4a",
            "prendre": "Magnékitri.m4a",
            "pleurer": "Mahaléou.m4a",
            "rire": "Mahandrou.m4a",
            "regarder": "Mahazou.m4a",
            "finir": "Mahita.m4a"
        },
        "transport": {
            "bicyclette": "Bicycléti.m4a",
            "kwassa kwassa": "Kwassa kwassa.m4a",
            "barque": "Laka.m4a",
            "pirogue": "Lakana.m4a",
            "bateau": "Markabou.m4a",
            "moto": "Monto.m4a",
            "camion": "Ndrégué.m4a",
            "avion": "Roplani.m4a",
            "taxi": "Taxi.m4a",
            "vedette": "Vidéti.m4a"
        }
    }
    
    total_updated = 0
    
    for section, mappings in audio_mappings.items():
        words = collection.find({"section": section})
        
        for word in words:
            french = word.get('french', '').lower()
            
            if french in mappings:
                audio_file = mappings[french]
                audio_path = f"audio/{section}/{audio_file}"
                
                result = collection.update_one(
                    {"_id": word['_id']},
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
                    total_updated += 1
                    logger.info(f"✅ {word.get('french')} → {audio_path}")
    
    logger.info(f"Total des références audio mises à jour: {total_updated}")
    return total_updated

def generate_database_report(db):
    """Génère un rapport détaillé de la base de données"""
    collection = db['vocabulary']
    
    logger.info("\n" + "="*60)
    logger.info("RAPPORT FINAL DE LA BASE DE DONNÉES")
    logger.info("="*60)
    
    sections = collection.distinct('section')
    total_words = 0
    total_with_audio = 0
    
    for section in sections:
        count = collection.count_documents({"section": section})
        with_audio = collection.count_documents({
            "section": section, 
            "has_authentic_audio": True
        })
        
        total_words += count
        total_with_audio += with_audio
        
        coverage = (with_audio / count) * 100 if count > 0 else 0
        
        logger.info(f"{section.upper():<15} | {count:>3} mots | {with_audio:>3} avec audio | {coverage:>5.1f}%")
    
    global_coverage = (total_with_audio / total_words) * 100 if total_words > 0 else 0
    
    logger.info("-" * 60)
    logger.info(f"{'TOTAL':<15} | {total_words:>3} mots | {total_with_audio:>3} avec audio | {global_coverage:>5.1f}%")
    logger.info("=" * 60)
    
    # Vérification de la cohérence
    logger.info("\nVÉRIFICATION COHÉRENCE:")
    
    # Mots avec structure complète
    complete_words = collection.count_documents({
        "french": {"$exists": True, "$ne": ""},
        "shimaoré": {"$exists": True, "$ne": ""},
        "kibouchi": {"$exists": True, "$ne": ""}
    })
    
    completeness = (complete_words / total_words) * 100 if total_words > 0 else 0
    
    logger.info(f"- Mots avec structure complète (FR/SH/KB): {complete_words}/{total_words} ({completeness:.1f}%)")
    
    # Mots avec émojis
    with_emoji = collection.count_documents({"emoji": {"$exists": True, "$ne": ""}})
    emoji_percentage = (with_emoji / total_words) * 100 if total_words > 0 else 0
    logger.info(f"- Mots avec émojis: {with_emoji}/{total_words} ({emoji_percentage:.1f}%)")
    
    return {
        "total_words": total_words,
        "total_with_audio": total_with_audio,
        "global_coverage": global_coverage,
        "completeness": completeness,
        "sections": len(sections)
    }

def main():
    """Fonction principale"""
    logger.info("Début de la vérification et correction de la base de données")
    
    try:
        # Connexion à la base de données
        db = connect_to_database()
        
        # 1. Vérifier la structure actuelle
        inconsistencies = verify_database_structure(db)
        
        # 2. Créer les sections manquantes
        created_sections = create_missing_sections(db)
        
        # 3. Mettre à jour les références audio
        updated_audio = update_audio_references(db)
        
        # 4. Vérification finale
        final_inconsistencies = verify_database_structure(db)
        
        # 5. Générer le rapport final
        report = generate_database_report(db)
        
        # Résumé des actions
        logger.info(f"\n{'='*60}")
        logger.info("RÉSUMÉ DES ACTIONS EFFECTUÉES")
        logger.info(f"{'='*60}")
        logger.info(f"- Sections créées: {created_sections}")
        logger.info(f"- Références audio mises à jour: {updated_audio}")
        logger.info(f"- Incohérences résolues: {inconsistencies - final_inconsistencies}")
        logger.info(f"- Couverture audio globale: {report['global_coverage']:.1f}%")
        logger.info(f"- Structure des données: {report['completeness']:.1f}% complète")
        
        if final_inconsistencies == 0:
            logger.info("🎉 Base de données entièrement cohérente!")
        else:
            logger.warning(f"⚠️ {final_inconsistencies} incohérences restantes à résoudre")
            
    except Exception as e:
        logger.error(f"Erreur dans le script principal: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())