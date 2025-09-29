#!/usr/bin/env python3
"""
Version simplifiée de mise à jour des correspondances audio des verbes
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Données extraites des tableaux
CORRECT_VERBS_TRANSLATIONS = {
    "jouer": {"shimaore": "oungadza", "kibouchi": "msoma"},
    "courir": {"shimaore": "wendra mbiya", "kibouchi": "miloumey"},
    "dire": {"shimaore": "ourongoa", "kibouchi": "mangnabara"},
    "pouvoir": {"shimaore": "ouchindra", "kibouchi": "mahaléou"},
    "vouloir": {"shimaore": "outsaha", "kibouchi": "chokou"},
    "savoir": {"shimaore": "oujoua", "kibouchi": "méhèyi"},
    "voir": {"shimaore": "ouona", "kibouchi": "mahita"},
    "devoir": {"shimaore": "oulazimou", "kibouchi": "tokotrou"},
    "venir": {"shimaore": "ouja", "kibouchi": "havi"},
    "rapprocher": {"shimaore": "outsenguéléya", "kibouchi": "magnatougno"},
    "prendre": {"shimaore": "ourenga", "kibouchi": "mangala"},
    "donner": {"shimaore": "ouva", "kibouchi": "magnamiya"},
    "parler": {"shimaore": "oulagoua", "kibouchi": "mivoulangna"},
    "mettre": {"shimaore": "outria", "kibouchi": "magnanou"},
    "passer": {"shimaore": "ouvira", "kibouchi": "mihomba"},
    "trouver": {"shimaore": "oupara", "kibouchi": "mahazou"},
    "aimer": {"shimaore": "ouvendza", "kibouchi": "mitya"},
    "croire": {"shimaore": "ouamini", "kibouchi": "koimini"},
    "penser": {"shimaore": "oufikiri", "kibouchi": "midzèri"},
    "connaître": {"shimaore": "oujoua", "kibouchi": "méhèyi"},
    "demander": {"shimaore": "oudzissa", "kibouchi": "magnoutani"},
    "répondre": {"shimaore": "oudjibou", "kibouchi": "mikoudjibou"},
    "laisser": {"shimaore": "oulicha", "kibouchi": "mangnambèla"},
    "manger": {"shimaore": "oudhya", "kibouchi": "mihagna"},
    "boire": {"shimaore": "ounoua", "kibouchi": "mindranou"},
    "lire": {"shimaore": "ousoma", "kibouchi": "midzorou"},
    "écrire": {"shimaore": "ouhanguiha", "kibouchi": "mikouandika"},
    "écouter": {"shimaore": "ouvoulikia", "kibouchi": "mitangréngni"},
    "apprendre": {"shimaore": "oufoundriha", "kibouchi": "midzorou"},
    "comprendre": {"shimaore": "ouéléwa", "kibouchi": "kouéléwa"},
    "marcher": {"shimaore": "ouendra", "kibouchi": "mandéha"},
    "entrer": {"shimaore": "ounguiya", "kibouchi": "mihididitri"},
    "sortir": {"shimaore": "oulawa", "kibouchi": "miboka"},
    "rester": {"shimaore": "ouketsi", "kibouchi": "mipétraka"},
    "vivre": {"shimaore": "ouyinchi", "kibouchi": "mikouènchi"},
    "dormir": {"shimaore": "oulala", "kibouchi": "mandri"},
    "attendre": {"shimaore": "oulindra", "kibouchi": "mandigni"},
    "suivre": {"shimaore": "oulounga", "kibouchi": "mangnaraka"},
    "tenir": {"shimaore": "oussika", "kibouchi": "mitana"},
    "ouvrir": {"shimaore": "ouboua", "kibouchi": "mampibiyangna"},
    "fermer": {"shimaore": "oubala", "kibouchi": "migadra"},
    "sembler": {"shimaore": "oufana", "kibouchi": "mampihiragna"},
    "paraître": {"shimaore": "ouwonehoua", "kibouchi": "ouhitagna"},
    "devenir": {"shimaore": "ougawouha", "kibouchi": "mivadiki"},
    "tomber": {"shimaore": "oupouliha", "kibouchi": "latsaka"},
    "se rappeler": {"shimaore": "oumaézi", "kibouchi": "koufahhamou"},
    "commencer": {"shimaore": "ouhandrissa", "kibouchi": "mitaponou"},
    "finir": {"shimaore": "oumalidza", "kibouchi": "mankéfa"},
    "réussir": {"shimaore": "ouchindra", "kibouchi": "mahaléou"},
    "essayer": {"shimaore": "oudjérébou", "kibouchi": "mikoudjérébou"},
    "attraper": {"shimaore": "oubara", "kibouchi": "missamboutrou"},
    "flatuler": {"shimaore": "oujamba", "kibouchi": "manguétoutrou"},
    "traverser": {"shimaore": "ouhiya", "kibouchi": "mitsaka"},
    "sauter": {"shimaore": "ouarouka", "kibouchi": "mivongna"},
    "frapper": {"shimaore": "ourema", "kibouchi": "mamangou"},
    "faire caca": {"shimaore": "ougna madzi", "kibouchi": "mangueri"},
    "faire pipi": {"shimaore": "ougna kojo", "kibouchi": "mamani"},
    "vomir": {"shimaore": "ouraviha", "kibouchi": "mandouwa"},
    "s'asseoir": {"shimaore": "ouketsi", "kibouchi": "mipétraka"},
    "danser": {"shimaore": "ouzina", "kibouchi": "mitsindzaka"},
    "arrêter": {"shimaore": "ouziya", "kibouchi": "mitsahatra"},
    "vendre": {"shimaore": "ouhoudza", "kibouchi": "mandafou"},
    "cracher": {"shimaore": "outra marré", "kibouchi": "mandrora"},
    "mordre": {"shimaore": "ouka magno", "kibouchi": "mangnékitri"},
    "gratter": {"shimaore": "oukouwa", "kibouchi": "mihotrou"},
    "embrasser": {"shimaore": "ounouka", "kibouchi": "mihoroukou"},
    "jeter": {"shimaore": "ouvoutsa", "kibouchi": "manopi"},
    "avertir": {"shimaore": "outahadaricha", "kibouchi": "mampahéyi"},
    "informer": {"shimaore": "oujdjudza", "kibouchi": "mangnabara"},
    "se laver le dernière": {"shimaore": "outsamba", "kibouchi": "mambouyi"},
    "se laver": {"shimaore": "ouhowa", "kibouchi": "misséki"},
    "piler": {"shimaore": "oudoudoua", "kibouchi": "mandissa"},
    "changer": {"shimaore": "ougaoudza", "kibouchi": "mamadiki"},
    "étendre au soleil": {"shimaore": "ouaniha", "kibouchi": "manapi"},
    "réchauffer": {"shimaore": "ouhelesedza", "kibouchi": "mamana"},
    "se baigner": {"shimaore": "ouhowa", "kibouchi": "misséki"},
    "faire le lit": {"shimaore": "ouhodza", "kibouchi": "mandzari koubani"},
    "faire sécher": {"shimaore": "ouhoumisa", "kibouchi": "manapi"},
    "balayer": {"shimaore": "ouhoundza", "kibouchi": "mamafa"},
    "couper": {"shimaore": "oukatra", "kibouchi": "manapaka"},
    "tremper": {"shimaore": "oulodza", "kibouchi": "mandzbougnou"},
    "se raser": {"shimaore": "oumea ndrevu", "kibouchi": "manapaka somboutrou"},
    "abîmer": {"shimaore": "oumengna", "kibouchi": "mandroubaka"},
    "acheter": {"shimaore": "ounounoua", "kibouchi": "mivanga"},
    "griller": {"shimaore": "ouwoha", "kibouchi": "mitonou"},
    "allumer": {"shimaore": "oupatsa", "kibouchi": "mikoupatza"},
    "se peigner": {"shimaore": "oupengné", "kibouchi": "mipèngni"},
    "cuisiner": {"shimaore": "oupiha", "kibouchi": "mahandrou"},
    "ranger": {"shimaore": "ourenguéldza", "kibouchi": "magnadzari"},
    "tresser": {"shimaore": "oussouka", "kibouchi": "mitali"},
    "peindre": {"shimaore": "ouvaha", "kibouchi": "magnossoutrou"},
    "essuyer": {"shimaore": "ouvangouha", "kibouchi": "mamitri"},
    "apporter": {"shimaore": "ouvinga", "kibouchi": "mandèyi"},
    "éteindre": {"shimaore": "ouzima", "kibouchi": "mamounou"},
    "tuer": {"shimaore": "ouwoula", "kibouchi": "mamounou"},
    "combler": {"shimaore": "oufitsiya", "kibouchi": "mankahampi"},
    "cultiver": {"shimaore": "oulima", "kibouchi": "mikapa"},
    "couper du bois": {"shimaore": "oupassouha kuni", "kibouchi": "mamaki azoumati"},
    "cueillir": {"shimaore": "oupoua", "kibouchi": "mampoka"},
    "planter": {"shimaore": "outabou", "kibouchi": "mamboli"},
    "creuser": {"shimaore": "outsimba", "kibouchi": "mangadi"},
    "récolter": {"shimaore": "ouvoona", "kibouchi": "mampoka"},
    "bouger": {"shimaore": "outsenguéleya", "kibouchi": "mitèki"},
    "arnaquer": {"shimaore": "ouravi", "kibouchi": "mangalatra"},
    "essorer": {"shimaore": "ouhamoua", "kibouchi": "mamèki"}
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

def clean_text_for_matching(text):
    """Nettoie un texte pour la correspondance"""
    if not text:
        return ""
    
    # Enlever espaces, accents, caractères spéciaux, normaliser
    text = text.lower()
    text = text.replace(' ', '').replace('-', '').replace('_', '').replace('/', '')
    text = text.replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('ë', 'e')
    text = text.replace('à', 'a').replace('á', 'a').replace('â', 'a').replace('ä', 'a')
    text = text.replace('ô', 'o').replace('ö', 'o').replace('ò', 'o').replace('ó', 'o')
    text = text.replace('û', 'u').replace('ù', 'u').replace('ü', 'u').replace('ú', 'u')
    text = text.replace('î', 'i').replace('ï', 'i').replace('ì', 'i').replace('í', 'i')
    text = text.replace('ç', 'c').replace('ñ', 'n')
    
    return text

def scan_and_copy_audio_files():
    """Scanne et copie les nouveaux fichiers audio"""
    source_dir = "/app/backend/extracted_verbes_updated/verbes"
    target_dir = "/app/frontend/assets/audio/verbes"
    
    logger.info("=== SCAN ET COPIE FICHIERS AUDIO ===")
    
    if not os.path.exists(source_dir):
        logger.error(f"Répertoire source non trouvé: {source_dir}")
        return []
    
    os.makedirs(target_dir, exist_ok=True)
    
    all_files = []
    copied_count = 0
    
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.m4a', '.mp3', '.wav')):
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)
            
            try:
                import shutil
                shutil.copy2(source_path, target_path)
                copied_count += 1
                
                # Ajouter à la liste des fichiers disponibles
                all_files.append(filename)
                
            except Exception as e:
                logger.warning(f"Erreur copie {filename}: {e}")
    
    logger.info(f"📁 Fichiers copiés: {copied_count}")
    logger.info(f"📊 Fichiers disponibles: {len(all_files)}")
    
    return all_files

def find_best_audio_match(translation_text, available_files):
    """Trouve le meilleur fichier audio correspondant à une traduction"""
    if not translation_text or not available_files:
        return None
    
    clean_translation = clean_text_for_matching(translation_text)
    best_match = None
    best_score = 0
    
    for filename in available_files:
        if not filename.endswith('.m4a'):
            continue
            
        # Enlever l'extension pour la comparaison
        audio_name = filename.replace('.m4a', '')
        clean_audio = clean_text_for_matching(audio_name)
        
        score = 0
        
        # Correspondance exacte
        if clean_audio == clean_translation:
            score = 100
        # Correspondance partielle
        elif clean_audio in clean_translation:
            score = 80 + len(clean_audio) * 2
        elif clean_translation in clean_audio:
            score = 70 + len(clean_translation) * 2
        # Correspondance par début de mot
        elif clean_translation.startswith(clean_audio[:6]) and len(clean_audio) > 5:
            score = 60
        elif clean_audio.startswith(clean_translation[:6]) and len(clean_translation) > 5:
            score = 55
        
        if score > best_score:
            best_score = score
            best_match = filename
    
    # Accepter seulement les matches avec un score suffisant
    if best_score >= 60:
        return best_match
    
    return None

def update_all_verbs():
    """Met à jour tous les verbes avec les nouveaux fichiers audio"""
    
    logger.info("🔄 MISE À JOUR VERBES AVEC NOUVEAUX FICHIERS")
    
    # Scanner et copier les fichiers
    available_files = scan_and_copy_audio_files()
    
    if not available_files:
        logger.error("Aucun fichier audio disponible")
        return False
    
    # Connexion base de données
    db = connect_to_database()
    collection = db['vocabulary']
    
    updated_count = 0
    shimaore_matches = 0
    kibouchi_matches = 0
    
    logger.info(f"\n{'Français':20} | {'Shimaoré':25} | {'Kibouchi':25} | {'Audio Shimaoré':25} | {'Audio Kibouchi':25}")
    logger.info("-" * 145)
    
    for french_verb, translations in CORRECT_VERBS_TRANSLATIONS.items():
        shimaore = translations["shimaore"]
        kibouchi = translations["kibouchi"]
        
        # Chercher correspondances audio
        shimaore_audio = find_best_audio_match(shimaore, available_files)
        kibouchi_audio = find_best_audio_match(kibouchi, available_files)
        
        # Éviter d'utiliser le même fichier pour deux traductions différentes (sauf si identiques)
        if (shimaore_audio == kibouchi_audio and 
            shimaore_audio and 
            clean_text_for_matching(shimaore) != clean_text_for_matching(kibouchi)):
            
            # Calculer quel match est le meilleur
            shimaore_clean = clean_text_for_matching(shimaore)
            kibouchi_clean = clean_text_for_matching(kibouchi)
            audio_clean = clean_text_for_matching(shimaore_audio.replace('.m4a', ''))
            
            shimaore_score = 0
            kibouchi_score = 0
            
            if shimaore_clean == audio_clean:
                shimaore_score = 100
            elif shimaore_clean in audio_clean:
                shimaore_score = 80
            elif audio_clean in shimaore_clean:
                shimaore_score = 70
                
            if kibouchi_clean == audio_clean:
                kibouchi_score = 100
            elif kibouchi_clean in audio_clean:
                kibouchi_score = 80
            elif audio_clean in kibouchi_clean:
                kibouchi_score = 70
            
            # Garder le meilleur match uniquement
            if shimaore_score > kibouchi_score:
                kibouchi_audio = None
            elif kibouchi_score > shimaore_score:
                shimaore_audio = None
            else:
                # Si égalité, préférer kibouchi
                shimaore_audio = None
        
        # Mettre à jour la base de données
        verb_data = {
            "section": "verbes",
            "french": french_verb,
            "shimaoré": shimaore,
            "kibouchi": kibouchi,
            "audio_shimaoré_filename": shimaore_audio,
            "audio_kibouchi_filename": kibouchi_audio,
            "audio_shimaoré_url": f"audio/verbes/{shimaore_audio}" if shimaore_audio else None,
            "audio_kibouchi_url": f"audio/verbes/{kibouchi_audio}" if kibouchi_audio else None,
            "has_shimaoré_audio": bool(shimaore_audio),
            "has_kibouchi_audio": bool(kibouchi_audio),
            "updated_with_191_files": True
        }
        
        result = collection.update_one(
            {"section": "verbes", "french": french_verb},
            {"$set": verb_data},
            upsert=True
        )
        
        if result.modified_count > 0 or result.upserted_id:
            updated_count += 1
            
            if shimaore_audio:
                shimaore_matches += 1
            if kibouchi_audio:
                kibouchi_matches += 1
            
            shimaore_status = f"✅ {shimaore_audio[:20]}..." if shimaore_audio and len(shimaore_audio) > 20 else f"{'✅ ' + shimaore_audio if shimaore_audio else '❌ Aucun'}"
            kibouchi_status = f"✅ {kibouchi_audio[:20]}..." if kibouchi_audio and len(kibouchi_audio) > 20 else f"{'✅ ' + kibouchi_audio if kibouchi_audio else '❌ Aucun'}"
            
            logger.info(f"{french_verb:20} | {shimaore:25} | {kibouchi:25} | {shimaore_status:25} | {kibouchi_status:25}")
    
    return updated_count, shimaore_matches, kibouchi_matches

def verify_results():
    """Vérifie les résultats finaux"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("\n=== VÉRIFICATION FINALE ===")
    
    # Statistiques
    total_verbs = collection.count_documents({"section": "verbes"})
    verbs_with_shimaore_audio = collection.count_documents({
        "section": "verbes",
        "has_shimaoré_audio": True
    })
    verbs_with_kibouchi_audio = collection.count_documents({
        "section": "verbes", 
        "has_kibouchi_audio": True
    })
    verbs_with_both_audio = collection.count_documents({
        "section": "verbes",
        "has_shimaoré_audio": True,
        "has_kibouchi_audio": True
    })
    
    logger.info(f"📊 STATISTIQUES FINALES:")
    logger.info(f"  Total verbes: {total_verbs}")
    logger.info(f"  Avec audio shimaoré: {verbs_with_shimaore_audio} ({verbs_with_shimaore_audio/total_verbs*100:.1f}%)")
    logger.info(f"  Avec audio kibouchi: {verbs_with_kibouchi_audio} ({verbs_with_kibouchi_audio/total_verbs*100:.1f}%)")
    logger.info(f"  Avec audio des deux: {verbs_with_both_audio} ({verbs_with_both_audio/total_verbs*100:.1f}%)")
    
    # Vérifications spécifiques
    test_verbs = ["abîmer", "voir", "danser", "dire", "jouer", "venir"]
    
    logger.info(f"\n🔍 VÉRIFICATION CAS SPÉCIFIQUES:")
    for test_verb in test_verbs:
        verb = collection.find_one({"section": "verbes", "french": test_verb})
        if verb:
            logger.info(f"  {test_verb:15}")
            logger.info(f"    Shimaoré: {verb.get('shimaoré', 'N/A'):20} → {verb.get('audio_shimaoré_filename', 'Aucun')}")
            logger.info(f"    Kibouchi: {verb.get('kibouchi', 'N/A'):20} → {verb.get('audio_kibouchi_filename', 'Aucun')}")
    
    return {
        'total': total_verbs,
        'shimaore': verbs_with_shimaore_audio,
        'kibouchi': verbs_with_kibouchi_audio,
        'both': verbs_with_both_audio
    }

def main():
    """Fonction principale"""
    logger.info("🎯 MISE À JOUR VERBES AVEC 191 NOUVEAUX FICHIERS AUDIO")
    
    try:
        # Mise à jour
        updated_count, shimaore_matches, kibouchi_matches = update_all_verbs()
        
        # Vérification
        stats = verify_results()
        
        # Résumé final
        logger.info(f"\n{'='*100}")
        logger.info("RÉSUMÉ MISE À JOUR VERBES")
        logger.info(f"{'='*100}")
        logger.info(f"✅ Verbes mis à jour: {updated_count}")
        logger.info(f"🎯 Correspondances shimaoré: {shimaore_matches}")
        logger.info(f"🎯 Correspondances kibouchi: {kibouchi_matches}")
        logger.info(f"📈 Coverage finale:")
        logger.info(f"  - Shimaoré: {stats['shimaore']}/{stats['total']} ({stats['shimaore']/stats['total']*100:.1f}%)")
        logger.info(f"  - Kibouchi: {stats['kibouchi']}/{stats['total']} ({stats['kibouchi']/stats['total']*100:.1f}%)")
        
        logger.info(f"\n🎉 MISE À JOUR TERMINÉE AVEC SUCCÈS!")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans la mise à jour: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)