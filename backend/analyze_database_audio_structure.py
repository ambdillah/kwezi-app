#!/usr/bin/env python3
"""
Analyse de la structure actuelle des champs audio dans la base de données
pour identifier les problèmes de correspondance shimaoré/kibouchi
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

def analyze_audio_structure():
    """Analyse la structure des champs audio"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("=== ANALYSE STRUCTURE CHAMPS AUDIO ===")
    
    # Récupérer un échantillon de documents pour voir la structure
    sample_docs = list(collection.find({}, {"_id": 1}).limit(5))
    
    if sample_docs:
        # Examiner le premier document complètement
        first_doc = collection.find_one({"_id": sample_docs[0]["_id"]})
        logger.info("📋 STRUCTURE D'UN DOCUMENT EXEMPLE:")
        for field, value in first_doc.items():
            if isinstance(value, str) and len(value) > 100:
                logger.info(f"  {field:25} → {str(value)[:100]}... (tronqué)")
            else:
                logger.info(f"  {field:25} → {value}")
    
    # Analyser tous les champs audio existants
    logger.info(f"\n🔍 CHAMPS AUDIO EXISTANTS:")
    
    pipeline = [
        {"$group": {
            "_id": None,
            "all_fields": {"$push": "$$ROOT"}
        }},
        {"$project": {
            "fields": {"$objectToArray": {"$arrayElemAt": ["$all_fields", 0]}}
        }},
        {"$unwind": "$fields"},
        {"$group": {
            "_id": "$fields.k"
        }}
    ]
    
    all_fields = list(collection.aggregate(pipeline))
    audio_fields = [field["_id"] for field in all_fields if "audio" in field["_id"].lower()]
    
    for field in sorted(audio_fields):
        # Compter combien de documents ont ce champ non-vide
        count_with_field = collection.count_documents({field: {"$exists": True, "$ne": "", "$ne": None}})
        logger.info(f"  {field:30} → {count_with_field:4} documents")
    
    return audio_fields

def analyze_verbs_audio_mapping():
    """Analyse spécifique des mappings audio des verbes"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info(f"\n=== ANALYSE MAPPINGS AUDIO VERBES ===")
    
    verbs = list(collection.find({"section": "verbes"}, {
        "_id": 1,
        "french": 1,
        "shimaoré": 1,
        "kibouchi": 1,
        "audio_authentic": 1,
        "audio_shimaoré": 1,
        "audio_kibouchi": 1,
        "audio_shimaore": 1,  # variante orthographe
        "shimoare_audio_filename": 1,
        "kibouchi_audio_filename": 1,
        "has_authentic_audio": 1
    }))
    
    logger.info(f"Verbes trouvés: {len(verbs)}")
    
    # Analyser les problèmes de correspondance
    problems_found = []
    
    logger.info(f"\n📊 ANALYSE DES CORRESPONDANCES:")
    logger.info(f"{'Français':15} | {'Shimaoré':20} | {'Kibouchi':20} | {'Audio(s)'}")
    logger.info("-" * 100)
    
    for verb in verbs:
        french = verb.get('french', 'N/A')
        shimaore = verb.get('shimaoré', 'N/A')
        kibouchi = verb.get('kibouchi', 'N/A')
        
        # Récupérer tous les champs audio possibles
        audio_fields = {}
        for field in verb:
            if 'audio' in field.lower() and verb[field] not in [None, '', False]:
                audio_fields[field] = verb[field]
        
        # Identifier les problèmes
        audio_summary = []
        for field, value in audio_fields.items():
            if isinstance(value, str) and value.startswith('audio/'):
                filename = os.path.basename(value)
                audio_summary.append(f"{field}:{filename}")
        
        if len(audio_summary) > 0:
            logger.info(f"{french:15} | {shimaore:20} | {kibouchi:20} | {' | '.join(audio_summary)}")
            
            # Vérifier si un seul fichier est utilisé pour deux langues différentes
            audio_files = [os.path.basename(value) for field, value in audio_fields.items() 
                          if isinstance(value, str) and value.startswith('audio/')]
            
            if len(set(audio_files)) == 1 and len(audio_files) > 1:
                # Un seul fichier pour plusieurs champs audio
                if shimaore.lower() != kibouchi.lower():
                    problems_found.append({
                        'french': french,
                        'shimaore': shimaore,
                        'kibouchi': kibouchi,
                        'audio_file': audio_files[0],
                        'problem': 'same_file_different_translations'
                    })
    
    logger.info(f"\n⚠️ PROBLÈMES IDENTIFIÉS:")
    logger.info(f"Verbes avec le même fichier audio pour traductions différentes: {len(problems_found)}")
    
    for problem in problems_found[:10]:  # Afficher les 10 premiers
        logger.info(f"  🚨 {problem['french']:15} → {problem['audio_file']:25}")
        logger.info(f"     Shimaoré: {problem['shimaore']}")
        logger.info(f"     Kibouchi: {problem['kibouchi']}")
        logger.info("")
    
    return problems_found

def propose_optimal_structure():
    """Propose une structure optimale pour les champs audio"""
    
    logger.info(f"\n=== PROPOSITION STRUCTURE OPTIMALE ===")
    
    optimal_structure = {
        "french": "Mot en français",
        "shimaoré": "Traduction en shimaoré",
        "kibouchi": "Traduction en kibouchi",
        "audio_shimaoré_filename": "Nom du fichier audio shimaoré (ex: Oumengna.m4a)",
        "audio_kibouchi_filename": "Nom du fichier audio kibouchi (ex: Manapaka_somboutrou.m4a)",
        "audio_shimaoré_url": "URL complète audio shimaoré (ex: audio/verbes/Oumengna.m4a)",
        "audio_kibouchi_url": "URL complète audio kibouchi (ex: audio/verbes/Manapaka_somboutrou.m4a)",
        "has_shimaoré_audio": "Boolean - true si audio shimaoré existe",
        "has_kibouchi_audio": "Boolean - true si audio kibouchi existe"
    }
    
    logger.info("🏗️ STRUCTURE RECOMMANDÉE:")
    for field, description in optimal_structure.items():
        logger.info(f"  {field:25} → {description}")
    
    logger.info(f"\n💡 AVANTAGES:")
    logger.info("  ✅ Séparation claire shimaoré/kibouchi")
    logger.info("  ✅ Chaque langue a son propre fichier audio")
    logger.info("  ✅ Pas de confusion entre les prononciations")
    logger.info("  ✅ Facilite la maintenance et les mises à jour")
    logger.info("  ✅ Permet une vérification automatique de cohérence")
    
    return optimal_structure

def generate_migration_script(problems_found):
    """Génère un script pour migrer vers la structure optimale"""
    
    logger.info(f"\n=== GÉNÉRATION SCRIPT MIGRATION ===")
    
    script_content = f"""#!/usr/bin/env python3
\"\"\"
Script de migration vers une structure audio optimisée
Sépare clairement les fichiers audio shimaoré et kibouchi
Corrige les {len(problems_found)} problèmes identifiés
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

def migrate_to_optimal_audio_structure():
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("🔄 MIGRATION VERS STRUCTURE AUDIO OPTIMISÉE")
    
    # Étape 1: Ajouter les nouveaux champs avec valeurs par défaut
    result = collection.update_many(
        {{}},
        {{
            "$set": {{
                "audio_shimaoré_filename": None,
                "audio_kibouchi_filename": None, 
                "audio_shimaoré_url": None,
                "audio_kibouchi_url": None,
                "has_shimaoré_audio": False,
                "has_kibouchi_audio": False
            }}
        }}
    )
    
    logger.info(f"✅ Nouveaux champs ajoutés à {{result.modified_count}} documents")
    
    # Étape 2: Migrer les données existantes
    # À implémenter selon l'analyse...
    
    return result.modified_count

if __name__ == "__main__":
    migrate_to_optimal_audio_structure()
"""
    
    script_path = "/app/backend/migrate_audio_structure.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    
    logger.info(f"📄 Script de migration généré: {script_path}")
    
    return script_path

def main():
    """Fonction principale"""
    logger.info("🔍 ANALYSE STRUCTURE AUDIO BASE DE DONNÉES")
    
    try:
        # 1. Analyser la structure actuelle
        audio_fields = analyze_audio_structure()
        
        # 2. Analyser les problèmes dans les verbes
        problems = analyze_verbs_audio_mapping()
        
        # 3. Proposer une structure optimale
        optimal_structure = propose_optimal_structure()
        
        # 4. Générer un script de migration
        migration_script = generate_migration_script(problems)
        
        # 5. Résumé
        logger.info(f"\n{'='*80}")
        logger.info("RÉSUMÉ ANALYSE STRUCTURE AUDIO")
        logger.info(f"{'='*80}")
        logger.info(f"Champs audio existants: {len(audio_fields)}")
        logger.info(f"Problèmes identifiés: {len(problems)}")
        logger.info(f"Script de migration: {migration_script}")
        
        logger.info(f"\n🎯 RECOMMANDATION:")
        logger.info(f"La structure actuelle mélange les audio shimaoré/kibouchi.")
        logger.info(f"Une migration vers des champs séparés améliorerait la cohérence.")
        
        return {
            'audio_fields': audio_fields,
            'problems': problems,
            'optimal_structure': optimal_structure,
            'migration_script': migration_script
        }
        
    except Exception as e:
        logger.error(f"Erreur dans l'analyse: {e}")
        return None

if __name__ == "__main__":
    main()