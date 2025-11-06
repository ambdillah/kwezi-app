#!/usr/bin/env python3
"""
Correction orthographique section "Nature" selon le PDF de référence
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Vocabulaire de référence extrait du PDF pour la section "Nature"
REFERENCE_NATURE = {
    "pente": {"shimaore": "mlima", "kibouchi": "boungou"},
    "colline": {"shimaore": "mlima", "kibouchi": "boungou"},
    "mont": {"shimaore": "mlima", "kibouchi": "boungou"},
    "lune": {"shimaore": "mwézi", "kibouchi": "fandzava"},
    "étoile": {"shimaore": "gnora", "kibouchi": "lakintagna"},
    "sable": {"shimaore": "mtsanga", "kibouchi": "fasigni"},
    "vague": {"shimaore": "dhouja", "kibouchi": "houndza"},
    "vent": {"shimaore": "pévo", "kibouchi": "tsikou"},
    "pluie": {"shimaore": "vhoua", "kibouchi": "mahaléni"},
    "mangrove": {"shimaore": "mhonko", "kibouchi": "honkou"},
    "corail": {"shimaore": "soiyi", "kibouchi": "soiyi"},
    "barrière de corail": {"shimaore": "caléni", "kibouchi": "caléni"},
    "tempête": {"shimaore": "darouba", "kibouchi": "tsikou"},
    "rivière": {"shimaore": "mouro", "kibouchi": "mouroni"},
    "pont": {"shimaore": "daradja", "kibouchi": "daradja"},
    "nuage": {"shimaore": "wingou", "kibouchi": "vingou"},
    "arc en ciel": {"shimaore": "mcacamba", "kibouchi": ""},
    "campagne": {"shimaore": "malavouni", "kibouchi": "atihala"},
    "forêt": {"shimaore": "malavouni", "kibouchi": "atihala"},
    "caillou": {"shimaore": "bwé", "kibouchi": "vatou"},
    "pierre": {"shimaore": "bwé", "kibouchi": "vatou"},
    "rocher": {"shimaore": "bwé", "kibouchi": "vatou"},
    "plateau": {"shimaore": "bandra", "kibouchi": "kètraka"},
    "chemin": {"shimaore": "ndzia", "kibouchi": "lalagna"},
    "sentier": {"shimaore": "ndzia", "kibouchi": "lalagna"},
    "parcours": {"shimaore": "ndzia", "kibouchi": "lalagna"},
    "herbe": {"shimaore": "malavou", "kibouchi": "haitri"},
    "fleur": {"shimaore": "foulera", "kibouchi": "foulera"},
    "soleil": {"shimaore": "jouwa", "kibouchi": "zouva"},
    "mer": {"shimaore": "bahari", "kibouchi": "bahari"},
    "plage": {"shimaore": "mtsangani", "kibouchi": "fassigni"},
    "arbre": {"shimaore": "mwiri", "kibouchi": "kakazou"},
    "rue": {"shimaore": "paré", "kibouchi": "paré"},
    "route": {"shimaore": "paré", "kibouchi": "paré"},
    "bananier": {"shimaore": "trindri", "kibouchi": "voudi ni hountsi"},
    "feuille": {"shimaore": "mawoini", "kibouchi": "hayitri"},
    "branche": {"shimaore": "trahi", "kibouchi": "trahi"},
    "tornade": {"shimaore": "ouzimouyi", "kibouchi": "tsikou soulaimana"},
    "cocotier": {"shimaore": "m'nadzi", "kibouchi": "vudi ni vwaniou"},
    "arbre à pain": {"shimaore": "m'frampé", "kibouchi": "vudi ni frampé"},
    "baobab": {"shimaore": "m'bouyou", "kibouchi": "vudi ni bouyou"},
    "bambou": {"shimaore": "m'bambo", "kibouchi": "valiha"},
    "manguier": {"shimaore": "m'manga", "kibouchi": "vudi ni manga"},
    "jacquier": {"shimaore": "m'fénéssi", "kibouchi": "vudi ni finéssi"},
    "terre": {"shimaore": "trotro", "kibouchi": "fotaka"},
    "sol": {"shimaore": "tsi", "kibouchi": "tani"},
    "érosion": {"shimaore": "padza", "kibouchi": "padza"},
    "marée basse": {"shimaore": "maji yavo", "kibouchi": "ranou mèki"},
    "platier": {"shimaore": "kalé", "kibouchi": "caléni"},
    "marée haute": {"shimaore": "maji yamalé", "kibouchi": "ranou fénou"},
    "inondé": {"shimaore": "ourora", "kibouchi": "dobou"},
    "sauvage": {"shimaore": "nyéha", "kibouchi": "di"},
    "canne à sucre": {"shimaore": "mouwoi", "kibouchi": "fari"},
    "fagot": {"shimaore": "kouni", "kibouchi": "azoumati"},
    "pirogue": {"shimaore": "laka", "kibouchi": "lakana"},
    "vedette": {"shimaore": "kwassa kwassa", "kibouchi": "vidéti"},
    "école": {"shimaore": "licoli", "kibouchi": "licoli"},
    "école coranique": {"shimaore": "shioni", "kibouchi": "kioni"}
}

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

def get_nature_from_database():
    """Récupère les mots de la section 'nature' de la base"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    nature_words = list(collection.find({"section": "nature"}))
    logger.info(f"Mots 'nature' trouvés en base: {len(nature_words)}")
    
    return nature_words

def compare_and_identify_corrections():
    """Compare le vocabulaire de la base avec la référence PDF"""
    logger.info("🔍 COMPARAISON ORTHOGRAPHIQUE - NATURE")
    
    db_words = get_nature_from_database()
    corrections_needed = []
    
    logger.info(f"\n{'='*120}")
    logger.info(f"ANALYSE ORTHOGRAPHIQUE SECTION 'NATURE'")
    logger.info(f"{'='*120}")
    logger.info(f"{'Français':25} | {'Base Shimaoré':20} | {'PDF Shimaoré':20} | {'Base Kibouchi':20} | {'PDF Kibouchi':20} | {'Action'}")
    logger.info("-" * 120)
    
    # Créer un dictionnaire des mots de la base par français
    db_dict = {}
    for word in db_words:
        french = word.get('french', '').lower().strip()
        db_dict[french] = word
    
    # Comparer avec la référence PDF
    for french_ref, translations_ref in REFERENCE_NATURE.items():
        french_key = french_ref.lower().strip()
        
        shimaore_ref = translations_ref["shimaore"]
        kibouchi_ref = translations_ref["kibouchi"]
        
        if french_key in db_dict:
            db_word = db_dict[french_key]
            db_shimaore = db_word.get('shimaoré', '').strip()
            db_kibouchi = db_word.get('kibouchi', '').strip()
            
            # Vérifier si corrections nécessaires
            shimaore_needs_correction = db_shimaore != shimaore_ref
            kibouchi_needs_correction = db_kibouchi != kibouchi_ref
            
            if shimaore_needs_correction or kibouchi_needs_correction:
                action = "🔧 CORRIGER"
                corrections_needed.append({
                    'word_id': db_word['_id'],
                    'french': french_ref,
                    'old_shimaore': db_shimaore,
                    'new_shimaore': shimaore_ref,
                    'old_kibouchi': db_kibouchi,
                    'new_kibouchi': kibouchi_ref,
                    'shimaore_correction': shimaore_needs_correction,
                    'kibouchi_correction': kibouchi_needs_correction
                })
            else:
                action = "✅ OK"
            
            logger.info(f"{french_ref:25} | {db_shimaore:20} | {shimaore_ref:20} | {db_kibouchi:20} | {kibouchi_ref:20} | {action}")
            
        else:
            # Mot présent dans PDF mais pas dans base
            logger.info(f"{french_ref:25} | {'ABSENT':20} | {shimaore_ref:20} | {'ABSENT':20} | {kibouchi_ref:20} | {'➕ AJOUTER'}")
            corrections_needed.append({
                'word_id': None,
                'french': french_ref,
                'old_shimaore': '',
                'new_shimaore': shimaore_ref,
                'old_kibouchi': '',
                'new_kibouchi': kibouchi_ref,
                'shimaore_correction': True,
                'kibouchi_correction': True,
                'is_new': True
            })
    
    return corrections_needed

def apply_corrections(corrections):
    """Applique les corrections orthographiques"""
    if not corrections:
        logger.info("✅ Aucune correction nécessaire")
        return 0
    
    logger.info(f"\n🔧 APPLICATION DES CORRECTIONS - {len(corrections)} corrections")
    
    db = connect_to_database()
    collection = db['vocabulary']
    
    corrected_count = 0
    
    for correction in corrections:
        try:
            if correction.get('is_new', False):
                # Ajouter nouveau mot
                new_word = {
                    "section": "nature",
                    "french": correction['french'],
                    "shimaoré": correction['new_shimaore'],
                    "kibouchi": correction['new_kibouchi'],
                    "orthography_corrected": True,
                    "corrected_from_pdf": True
                }
                
                result = collection.insert_one(new_word)
                if result.inserted_id:
                    logger.info(f"➕ Ajouté: {correction['french']}")
                    corrected_count += 1
            else:
                # Mettre à jour mot existant
                update_data = {
                    "shimaoré": correction['new_shimaore'],
                    "kibouchi": correction['new_kibouchi'],
                    "orthography_corrected": True,
                    "corrected_from_pdf": True
                }
                
                result = collection.update_one(
                    {"_id": correction['word_id']},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    logger.info(f"🔧 Corrigé: {correction['french']}")
                    if correction['shimaore_correction']:
                        logger.info(f"   Shimaoré: '{correction['old_shimaore']}' → '{correction['new_shimaore']}'")
                    if correction['kibouchi_correction']:
                        logger.info(f"   Kibouchi: '{correction['old_kibouchi']}' → '{correction['new_kibouchi']}'")
                    corrected_count += 1
                
        except Exception as e:
            logger.error(f"Erreur correction {correction['french']}: {e}")
    
    return corrected_count

def verify_corrections():
    """Vérifie que les corrections ont été appliquées"""
    logger.info(f"\n=== VÉRIFICATION CORRECTIONS NATURE ===")
    
    db_words = get_nature_from_database()
    
    # Statistiques finales
    total_words = len(db_words)
    corrected_words = len([w for w in db_words if w.get('orthography_corrected')])
    
    logger.info(f"\n📊 STATISTIQUES FINALES:")
    logger.info(f"  Total mots nature: {total_words}")
    logger.info(f"  Corrections appliquées: {corrected_words}")
    
    return total_words, corrected_words

def main():
    """Fonction principale"""
    logger.info("🎯 CORRECTION ORTHOGRAPHIQUE - SECTION NATURE")
    
    try:
        # 1. Comparer et identifier les corrections nécessaires
        corrections = compare_and_identify_corrections()
        
        if not corrections:
            logger.info("✅ Aucune correction orthographique nécessaire pour 'Nature'")
            return True
        
        # 2. Résumé des corrections proposées
        logger.info(f"\n📋 RÉSUMÉ DES CORRECTIONS PROPOSÉES:")
        logger.info(f"  Corrections nécessaires: {len(corrections)}")
        
        shimaore_corrections = sum(1 for c in corrections if c['shimaore_correction'])
        kibouchi_corrections = sum(1 for c in corrections if c['kibouchi_correction'])
        new_words = sum(1 for c in corrections if c.get('is_new', False))
        
        logger.info(f"  Corrections shimaoré: {shimaore_corrections}")
        logger.info(f"  Corrections kibouchi: {kibouchi_corrections}")
        logger.info(f"  Nouveaux mots: {new_words}")
        
        # 3. Appliquer les corrections
        corrected_count = apply_corrections(corrections)
        
        # 4. Vérifier les corrections
        total_words, corrected_words = verify_corrections()
        
        # 5. Résumé final
        logger.info(f"\n{'='*80}")
        logger.info("RÉSUMÉ CORRECTION ORTHOGRAPHIQUE - NATURE")
        logger.info(f"{'='*80}")
        logger.info(f"✅ Corrections appliquées: {corrected_count}")
        logger.info(f"📊 Mots traités: {total_words}")
        
        logger.info(f"\n🎉 SECTION 'NATURE' TERMINÉE!")
        logger.info(f"Orthographe corrigée selon le PDF de référence.")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans la correction orthographique: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)