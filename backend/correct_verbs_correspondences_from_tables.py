#!/usr/bin/env python3
"""
Correction des correspondances audio des verbes selon les tableaux fournis par l'utilisateur
Association correcte entre français, shimaoré, kibouchi et fichiers audio
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Données extraites des tableaux fournis par l'utilisateur
CORRECT_VERBS_TRANSLATIONS = {
    # Tableau 1
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
    
    # Tableau 2
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

# Fichiers audio disponibles
AVAILABLE_AUDIO_FILES = [
    "Chokou.m4a", "Havi.m4a", "Koimini.m4a", "Koufahamou.m4a", "Kouéléwa.m4a",
    "Latsaka.m4a", "Magnadzari.m4a", "Magnamiya.m4a", "Magnaraka.m4a", 
    "Magnatougnou.m4a", "Magnossoutrou.m4a", "Magnoutani.m4a", "Magnékitri.m4a",
    "Mahaléou.m4a", "Mahandrou.m4a", "Mahazou.m4a", "Mahita.m4a", "Mamadiki.m4a",
    "Mamafa.m4a", "Mamaki azoumati.m4a", "Mamana.m4a", "Mamangou.m4a", "Mamani.m4a",
    "Mambouyi.m4a", "Mamitri.m4a", "Mamounou.m4a", "Mampahéyi.m4a", "Mampibiyangna.m4a",
    "Mampihiragna.m4a", "Mampoka.m4a", "Maméki.m4a", "Manapaka somboutrou.m4a",
    "Manapaka.m4a", "Manapi.m4a", "Mandafou.m4a", "Mandigni.m4a", "Mandissa.m4a",
    "Mandouwa.m4a", "Mandri.m4a", "Mandrora.m4a", "Mandroubaka.m4a", "Mandzari koubani.m4a",
    "Mandzoubougnou.m4a", "Mandèyi.m4a", "Mandéha.m4a", "Mangala.m4a", "Mangalatra.m4a",
    "Mangnabara.m4a", "Mangnambéla.m4a", "Ouwoula.m4a"
]

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
    
    # Enlever espaces, accents, caractères spéciaux
    text = text.lower()
    text = text.replace(' ', '').replace('-', '').replace('_', '').replace('é', 'e').replace('è', 'e').replace('à', 'a').replace('ç', 'c').replace('/', '')
    
    return text

def find_audio_for_translation(translation_text, available_files):
    """Trouve le fichier audio correspondant à une traduction"""
    if not translation_text:
        return None
    
    clean_translation = clean_text_for_matching(translation_text)
    
    # Correspondance exacte
    for audio_file in available_files:
        clean_audio = clean_text_for_matching(audio_file.replace('.m4a', ''))
        if clean_translation == clean_audio:
            return audio_file
    
    # Correspondance partielle (le texte de traduction contient le nom du fichier)
    for audio_file in available_files:
        clean_audio = clean_text_for_matching(audio_file.replace('.m4a', ''))
        if len(clean_audio) > 3 and clean_audio in clean_translation:
            return audio_file
    
    # Correspondance partielle inverse (le nom du fichier contient la traduction)
    for audio_file in available_files:
        clean_audio = clean_text_for_matching(audio_file.replace('.m4a', ''))
        if len(clean_translation) > 3 and clean_translation in clean_audio:
            return audio_file
    
    return None

def correct_all_verb_correspondences():
    """Corrige toutes les correspondances des verbes selon les tableaux"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("🔄 CORRECTION CORRESPONDANCES VERBES SELON TABLEAUX UTILISATEUR")
    
    updated_count = 0
    correspondences_found = []
    correspondences_missing = []
    
    logger.info(f"{'Français':20} | {'Shimaoré':25} | {'Kibouchi':25} | {'Audio Shimaoré':20} | {'Audio Kibouchi':20}")
    logger.info("-" * 130)
    
    for french_verb, translations in CORRECT_VERBS_TRANSLATIONS.items():
        shimaore = translations["shimaore"]
        kibouchi = translations["kibouchi"]
        
        # Trouver les fichiers audio correspondants
        shimaore_audio = find_audio_for_translation(shimaore, AVAILABLE_AUDIO_FILES)
        kibouchi_audio = find_audio_for_translation(kibouchi, AVAILABLE_AUDIO_FILES)
        
        # Si on trouve le même fichier pour les deux langues ET que les traductions sont différentes,
        # on attribue le fichier à la langue qui correspond le mieux
        if shimaore_audio == kibouchi_audio and shimaore.lower() != kibouchi.lower():
            # Vérifier quelle traduction correspond le mieux au fichier
            if shimaore_audio:
                clean_audio = clean_text_for_matching(shimaore_audio.replace('.m4a', ''))
                clean_shimaore = clean_text_for_matching(shimaore)
                clean_kibouchi = clean_text_for_matching(kibouchi)
                
                # Si shimaoré correspond mieux, garder pour shimaoré
                if clean_shimaore == clean_audio or clean_audio in clean_shimaore:
                    kibouchi_audio = None
                # Si kibouchi correspond mieux, garder pour kibouchi
                elif clean_kibouchi == clean_audio or clean_audio in clean_kibouchi:
                    shimaore_audio = None
        
        # Mettre à jour ou créer le verbe dans la base
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
            "corrected_from_user_tables": True
        }
        
        # Essayer de mettre à jour le verbe existant
        result = collection.update_one(
            {"section": "verbes", "french": french_verb},
            {"$set": verb_data},
            upsert=True
        )
        
        if result.modified_count > 0 or result.upserted_id:
            updated_count += 1
            
            shimaore_status = f"✅ {shimaore_audio}" if shimaore_audio else "❌ Aucun"
            kibouchi_status = f"✅ {kibouchi_audio}" if kibouchi_audio else "❌ Aucun"
            
            logger.info(f"{french_verb:20} | {shimaore:25} | {kibouchi:25} | {shimaore_status:20} | {kibouchi_status:20}")
            
            correspondences_found.append({
                'french': french_verb,
                'shimaore': shimaore,
                'kibouchi': kibouchi,
                'shimaore_audio': shimaore_audio,
                'kibouchi_audio': kibouchi_audio
            })
        else:
            correspondences_missing.append(french_verb)
    
    return updated_count, correspondences_found, correspondences_missing

def copy_new_audio_files():
    """Copie les nouveaux fichiers audio du ZIP vers le dossier verbes"""
    source_dir = "/app/backend/extracted_verbes/verbes"
    target_dir = "/app/frontend/assets/audio/verbes"
    
    logger.info("📁 COPIE DES NOUVEAUX FICHIERS AUDIO")
    
    copied_files = []
    skipped_files = []
    
    for filename in AVAILABLE_AUDIO_FILES:
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename)
        
        if os.path.exists(source_path):
            try:
                import shutil
                shutil.copy2(source_path, target_path)
                copied_files.append(filename)
                logger.info(f"  ✅ Copié: {filename}")
            except Exception as e:
                logger.error(f"  ❌ Erreur copie {filename}: {e}")
                skipped_files.append(filename)
        else:
            if os.path.exists(target_path):
                logger.info(f"  📁 Existe déjà: {filename}")
            else:
                logger.warning(f"  ⚠️ Fichier source manquant: {filename}")
                skipped_files.append(filename)
    
    logger.info(f"Fichiers copiés: {len(copied_files)}")
    logger.info(f"Fichiers ignorés: {len(skipped_files)}")
    
    return copied_files, skipped_files

def verify_corrections():
    """Vérifie que les corrections ont été appliquées correctement"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("\n=== VÉRIFICATION CORRECTIONS ===")
    
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
    
    # Vérifier des cas spécifiques
    test_verbs = ["abîmer", "voir", "danser", "dire", "couper"]
    
    logger.info(f"\n🔍 VÉRIFICATION CAS SPÉCIFIQUES:")
    for verb_french in test_verbs:
        verb = collection.find_one({"section": "verbes", "french": verb_french})
        if verb:
            logger.info(f"  {verb_french:15}")
            logger.info(f"    Shimaoré: {verb.get('shimaoré', 'N/A')} → {verb.get('audio_shimaoré_filename', 'Aucun')}")
            logger.info(f"    Kibouchi: {verb.get('kibouchi', 'N/A')} → {verb.get('audio_kibouchi_filename', 'Aucun')}")
        else:
            logger.warning(f"  ⚠️ Verbe '{verb_french}' non trouvé")
    
    return {
        'total': total_verbs,
        'shimaore': verbs_with_shimaore_audio,
        'kibouchi': verbs_with_kibouchi_audio,
        'both': verbs_with_both_audio
    }

def main():
    """Fonction principale"""
    logger.info("🎯 CORRECTION CORRESPONDANCES VERBES SELON TABLEAUX UTILISATEUR")
    
    try:
        # 1. Copier les nouveaux fichiers audio
        copied_files, skipped_files = copy_new_audio_files()
        
        # 2. Corriger toutes les correspondances
        updated_count, correspondences_found, correspondences_missing = correct_all_verb_correspondences()
        
        # 3. Vérifier les corrections
        stats = verify_corrections()
        
        # 4. Résumé final
        logger.info(f"\n{'='*100}")
        logger.info("RÉSUMÉ CORRECTION CORRESPONDANCES VERBES")
        logger.info(f"{'='*100}")
        logger.info(f"✅ Verbes corrigés: {updated_count}")
        logger.info(f"📁 Fichiers audio copiés: {len(copied_files)}")
        logger.info(f"🎯 Correspondances trouvées: {len(correspondences_found)}")
        logger.info(f"❌ Correspondances manquantes: {len(correspondences_missing)}")
        logger.info(f"📊 Coverage final:")
        logger.info(f"  - Shimaoré: {stats['shimaore']}/{stats['total']} ({stats['shimaore']/stats['total']*100:.1f}%)")
        logger.info(f"  - Kibouchi: {stats['kibouchi']}/{stats['total']} ({stats['kibouchi']/stats['total']*100:.1f}%)")
        
        if correspondences_missing:
            logger.info(f"\n⚠️ VERBES SANS CORRESPONDANCE AUDIO:")
            for verb in correspondences_missing[:10]:
                logger.info(f"  - {verb}")
        
        logger.info(f"\n🎉 CORRECTION TERMINÉE!")
        logger.info(f"Les correspondances audio des verbes ont été corrigées selon vos tableaux.")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans la correction: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)