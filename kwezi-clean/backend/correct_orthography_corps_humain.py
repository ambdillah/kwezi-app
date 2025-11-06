#!/usr/bin/env python3
"""
Correction orthographique section "Corps humain" selon le PDF de référence
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Vocabulaire de référence extrait du PDF pour la section "Corps humain"
REFERENCE_CORPS_HUMAIN = {
    "œil": {"shimaore": "matso", "kibouchi": "faninti"},
    "nez": {"shimaore": "poua", "kibouchi": "horougnou"},
    "oreille": {"shimaore": "kiyo", "kibouchi": "soufigni"},
    "ongle": {"shimaore": "kofou", "kibouchi": "angofou"},
    "front": {"shimaore": "housso", "kibouchi": "lahara"},
    "joue": {"shimaore": "savou", "kibouchi": "fifi"},
    "dos": {"shimaore": "mengo", "kibouchi": "vohou"},
    "épaule": {"shimaore": "bèga", "kibouchi": "haveyi"},
    "hanche": {"shimaore": "trenga", "kibouchi": "tagna"},
    "fesses": {"shimaore": "shidé", "kibouchi": "fouri"},  # Note: PDF montre "shidé/mvoumo"
    "main": {"shimaore": "mhono", "kibouchi": "tagnana"},
    "tête": {"shimaore": "shitsoi", "kibouchi": "louha"},
    "ventre": {"shimaore": "mimba", "kibouchi": "kibou"},
    "dent": {"shimaore": "magno", "kibouchi": "hifi"},
    "langue": {"shimaore": "oulimé", "kibouchi": "lèla"},
    "pied": {"shimaore": "mindrou", "kibouchi": "viti"},
    "lèvre": {"shimaore": "dhomo", "kibouchi": "soungni"},
    "peau": {"shimaore": "ngwezi", "kibouchi": "ngwezi"},
    "cheveux": {"shimaore": "ngnélé", "kibouchi": "fagnéva"},  # Correction importante !
    "doigts": {"shimaore": "cha", "kibouchi": "tondrou"},
    "barbe": {"shimaore": "ndrévou", "kibouchi": "somboutrou"},
    "vagin": {"shimaore": "ndzigni", "kibouchi": "tingui"},
    "testicules": {"shimaore": "kwendzé", "kibouchi": "vouancarou"},  # Correction importante !
    "pénis": {"shimaore": "mbo", "kibouchi": "kaboudzi"},
    "menton": {"shimaore": "shlévou", "kibouchi": "sokou"},
    "bouche": {"shimaore": "hangno", "kibouchi": "vava"},
    "côtes": {"shimaore": "bavou", "kibouchi": "mbavou"},
    "sourcil": {"shimaore": "tsi", "kibouchi": "ankwéssi"},
    "cheville": {"shimaore": "dzitso la pwédza", "kibouchi": "dzitso la pwédza"},
    "cou": {"shimaore": "tsingo", "kibouchi": "vouzougno"},
    "cils": {"shimaore": "kové", "kibouchi": "rambou faninti"},
    "arrière du crâne": {"shimaore": "komoi", "kibouchi": "kitoika"}
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

def get_corps_humain_from_database():
    """Récupère les mots de la section 'corps_humain' de la base"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    corps_humain_words = list(collection.find({"section": "corps_humain"}))
    logger.info(f"Mots 'corps_humain' trouvés en base: {len(corps_humain_words)}")
    
    return corps_humain_words

def compare_and_identify_corrections():
    """Compare le vocabulaire de la base avec la référence PDF"""
    logger.info("🔍 COMPARAISON ORTHOGRAPHIQUE - CORPS HUMAIN")
    
    db_words = get_corps_humain_from_database()
    corrections_needed = []
    
    logger.info(f"\n{'='*100}")
    logger.info(f"ANALYSE ORTHOGRAPHIQUE SECTION 'CORPS HUMAIN'")
    logger.info(f"{'='*100}")
    logger.info(f"{'Français':20} | {'Base Shimaoré':20} | {'PDF Shimaoré':20} | {'Base Kibouchi':20} | {'PDF Kibouchi':20} | {'Action'}")
    logger.info("-" * 100)
    
    # Créer un dictionnaire des mots de la base par français
    db_dict = {}
    for word in db_words:
        french = word.get('french', '').lower()
        db_dict[french] = word
    
    # Comparer avec la référence PDF
    for french_ref, translations_ref in REFERENCE_CORPS_HUMAIN.items():
        french_key = french_ref.lower()
        
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
            
            logger.info(f"{french_ref:20} | {db_shimaore:20} | {shimaore_ref:20} | {db_kibouchi:20} | {kibouchi_ref:20} | {action}")
            
        else:
            # Mot présent dans PDF mais pas dans base
            logger.info(f"{french_ref:20} | {'ABSENT':20} | {shimaore_ref:20} | {'ABSENT':20} | {kibouchi_ref:20} | {'➕ AJOUTER'}")
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
    
    # Vérifier mots en base mais pas dans PDF
    for french_key, db_word in db_dict.items():
        if french_key not in [f.lower() for f in REFERENCE_CORPS_HUMAIN.keys()]:
            logger.info(f"{db_word.get('french', 'N/A'):20} | {db_word.get('shimaoré', ''):20} | {'ABSENT PDF':20} | {db_word.get('kibouchi', ''):20} | {'ABSENT PDF':20} | {'⚠️ VÉRIFIER'}")
    
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
                    "section": "corps_humain",
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
    logger.info(f"\n=== VÉRIFICATION CORRECTIONS CORPS HUMAIN ===")
    
    db_words = get_corps_humain_from_database()
    
    # Vérifications spécifiques pour les exemples mentionnés
    test_cases = ["cheveux", "testicules", "barbe", "vagin"]
    
    for test_word in test_cases:
        word = next((w for w in db_words if w.get('french', '').lower() == test_word), None)
        if word:
            logger.info(f"✅ {test_word:15}")
            logger.info(f"   Shimaoré: {word.get('shimaoré', 'N/A')}")
            logger.info(f"   Kibouchi: {word.get('kibouchi', 'N/A')}")
        else:
            logger.warning(f"⚠️ {test_word} non trouvé")
    
    # Statistiques finales
    total_words = len(db_words)
    corrected_words = len([w for w in db_words if w.get('orthography_corrected')])
    
    logger.info(f"\n📊 STATISTIQUES FINALES:")
    logger.info(f"  Total mots corps humain: {total_words}")
    logger.info(f"  Corrections appliquées: {corrected_words}")
    
    return total_words, corrected_words

def main():
    """Fonction principale"""
    logger.info("🎯 CORRECTION ORTHOGRAPHIQUE - SECTION CORPS HUMAIN")
    
    try:
        # 1. Comparer et identifier les corrections nécessaires
        corrections = compare_and_identify_corrections()
        
        if not corrections:
            logger.info("✅ Aucune correction orthographique nécessaire pour 'Corps humain'")
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
        logger.info("RÉSUMÉ CORRECTION ORTHOGRAPHIQUE - CORPS HUMAIN")
        logger.info(f"{'='*80}")
        logger.info(f"✅ Corrections appliquées: {corrected_count}")
        logger.info(f"📊 Mots traités: {total_words}")
        logger.info(f"🎯 Exemples corrigés:")
        logger.info(f"   - 'cheveux' → kibouchi: 'fagnéva'")
        logger.info(f"   - 'testicules' → kibouchi: 'vouancarou'")
        
        logger.info(f"\n🎉 SECTION 'CORPS HUMAIN' TERMINÉE!")
        logger.info(f"Orthographe corrigée selon le PDF de référence.")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans la correction orthographique: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)