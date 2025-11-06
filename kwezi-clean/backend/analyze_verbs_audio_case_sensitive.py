#!/usr/bin/env python3
"""
Analyse spécifique des correspondances audio pour la section VERBES
avec attention particulière aux majuscules dans les noms de fichiers audio
Demande de l'utilisateur: analyser "oumengna" base de données vs "Oumengna" fichiers audio
"""

import os
import re
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

def scan_verbs_audio_files():
    """Scanne spécifiquement les fichiers audio des verbes"""
    verbs_audio_dir = "/app/frontend/assets/audio/verbes"
    
    logger.info("=== SCAN FICHIERS AUDIO VERBES ===")
    logger.info(f"Répertoire: {verbs_audio_dir}")
    
    if not os.path.exists(verbs_audio_dir):
        logger.error(f"Répertoire audio verbes non trouvé: {verbs_audio_dir}")
        return []
    
    audio_files = []
    
    for filename in os.listdir(verbs_audio_dir):
        if filename.lower().endswith(('.m4a', '.mp3', '.wav')):
            file_path = os.path.join(verbs_audio_dir, filename)
            file_size = os.path.getsize(file_path)
            
            # Analyser le nom avec attention aux majuscules
            name_without_ext = os.path.splitext(filename)[0]
            
            audio_info = {
                'filename': filename,
                'name_original': name_without_ext,  # Nom original avec majuscules/minuscules
                'name_lower': name_without_ext.lower(),  # Version minuscules pour comparaison
                'name_clean': clean_text_for_comparison(name_without_ext),  # Version nettoyée
                'size': file_size,
                'path': file_path,
                'has_uppercase': any(c.isupper() for c in name_without_ext),
                'first_char_upper': name_without_ext[0].isupper() if name_without_ext else False
            }
            
            audio_files.append(audio_info)
            
            case_indicator = "📝" if audio_info['has_uppercase'] else "📄"
            logger.info(f"  {case_indicator} {filename:35} → {name_without_ext:30} ({file_size:6} bytes)")
    
    logger.info(f"\nTotal: {len(audio_files)} fichiers audio trouvés")
    
    # Statistiques sur les majuscules
    with_uppercase = sum(1 for f in audio_files if f['has_uppercase'])
    logger.info(f"Fichiers avec majuscules: {with_uppercase}/{len(audio_files)} ({with_uppercase/len(audio_files)*100:.1f}%)")
    
    return audio_files

def get_verbs_from_database():
    """Récupère tous les verbes de la base de données"""
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("\n=== RÉCUPÉRATION VERBES BASE DE DONNÉES ===")
    
    verbs = list(collection.find(
        {"section": "verbes"}, 
        {
            "_id": 1,
            "french": 1,
            "shimaoré": 1,
            "kibouchi": 1,
            "audio_authentic": 1,
            "has_authentic_audio": 1,
            "audio_shimaoré": 1,
            "audio_kibouchi": 1
        }
    ))
    
    logger.info(f"Verbes trouvés: {len(verbs)}")
    
    # Afficher quelques exemples avec leurs traductions
    logger.info("\nExemples de verbes:")
    for i, verb in enumerate(verbs[:10]):
        french = verb.get('french', 'N/A')
        shimaore = verb.get('shimaoré', 'N/A')
        kibouchi = verb.get('kibouchi', 'N/A')
        has_audio = verb.get('has_authentic_audio', False)
        audio_file = verb.get('audio_authentic', '')
        
        audio_indicator = "🔊" if has_audio else "🔇"
        logger.info(f"  {i+1:2}. {french:15} | {shimaore:20} | {kibouchi:20} {audio_indicator}")
        if audio_file:
            logger.info(f"      → Audio: {audio_file}")
    
    return verbs

def clean_text_for_comparison(text):
    """Nettoie un texte pour la comparaison (enlève accents, espaces, ponctuation) mais préserve la casse"""
    if not text:
        return ""
    
    # Remplacer les accents mais garder la casse
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'à': 'a', 'á': 'a', 'â': 'a', 'ä': 'a',
        'À': 'A', 'Á': 'A', 'Â': 'A', 'Ä': 'A',
        'ô': 'o', 'ö': 'o', 'ò': 'o', 'ó': 'o',
        'Ô': 'O', 'Ö': 'O', 'Ò': 'O', 'Ó': 'O',
        'û': 'u', 'ù': 'u', 'ü': 'u', 'ú': 'u',
        'Û': 'U', 'Ù': 'U', 'Ü': 'U', 'Ú': 'U',
        'î': 'i', 'ï': 'i', 'ì': 'i', 'í': 'i',
        'Î': 'I', 'Ï': 'I', 'Ì': 'I', 'Í': 'I',
        'ç': 'c', 'Ç': 'C', 'ñ': 'n', 'Ñ': 'N'
    }
    
    for accented, plain in replacements.items():
        text = text.replace(accented, plain)
    
    # Enlever espaces, tirets, apostrophes, points mais préserver la casse
    text = re.sub(r'[ \-\'\.\/]', '', text)
    
    return text

def analyze_verb_audio_correspondences(audio_files, verbs):
    """Analyse spécifiquement les correspondances verbes-audio avec attention aux majuscules"""
    
    logger.info("\n=== ANALYSE CORRESPONDANCES VERBES-AUDIO ===")
    
    correspondences = []
    unmatched_audio = []
    unmatched_verbs = []
    case_sensitive_matches = []
    
    # Analyse du problème spécifique mentionné par l'utilisateur
    logger.info(f"\n🔍 RECHERCHE SPÉCIALE: 'oumengna' vs fichiers avec majuscules")
    
    oumengna_verbs = []
    oumengna_audio_candidates = []
    
    # Chercher tous les verbes contenant "oumengna" 
    for verb in verbs:
        french = verb.get('french', '')
        shimaore = verb.get('shimaoré', '').lower()
        kibouchi = verb.get('kibouchi', '').lower()
        
        if 'oumengna' in shimaore or 'oumengna' in kibouchi:
            oumengna_verbs.append({
                'verb': verb,
                'french': french,
                'shimaore': verb.get('shimaoré', ''),
                'kibouchi': verb.get('kibouchi', '')
            })
            logger.info(f"  📝 Trouvé verbe avec 'oumengna': {french} | {verb.get('shimaoré', '')} | {verb.get('kibouchi', '')}")
    
    # Chercher tous les fichiers audio contenant "oumengna" (case-insensitive)
    for audio_file in audio_files:
        if 'oumengna' in audio_file['name_lower']:
            oumengna_audio_candidates.append(audio_file)
            case_info = f"(Majuscule: {audio_file['has_uppercase']})"
            logger.info(f"  🔊 Fichier audio candidat: {audio_file['filename']} → {audio_file['name_original']} {case_info}")
    
    # Analyser toutes les correspondances possibles
    logger.info(f"\n📊 ANALYSE GÉNÉRALE:")
    
    for verb in verbs:
        french = verb.get('french', '')
        shimaore = verb.get('shimaoré', '')
        kibouchi = verb.get('kibouchi', '')
        verb_id = str(verb['_id'])
        
        # Nettoyer les traductions pour comparaison
        french_clean = clean_text_for_comparison(french).lower()
        shimaore_clean = clean_text_for_comparison(shimaore).lower()
        kibouchi_clean = clean_text_for_comparison(kibouchi).lower()
        
        matches_for_verb = []
        
        # Chercher correspondances dans les fichiers audio
        for audio_file in audio_files:
            audio_clean = audio_file['name_clean'].lower()
            audio_original = audio_file['name_original']
            
            match_type = None
            match_field = None
            
            # Correspondance exacte (case-insensitive)
            if audio_clean == french_clean:
                match_type = "exact_french"
                match_field = "french"
            elif audio_clean == shimaore_clean:
                match_type = "exact_shimaore"
                match_field = "shimaoré"
            elif audio_clean == kibouchi_clean:
                match_type = "exact_kibouchi"
                match_field = "kibouchi"
            # Correspondance partielle
            elif len(audio_clean) > 3 and audio_clean in shimaore_clean:
                match_type = "partial_shimaore"
                match_field = "shimaoré"
            elif len(audio_clean) > 3 and audio_clean in kibouchi_clean:
                match_type = "partial_kibouchi"
                match_field = "kibouchi"
            elif len(shimaore_clean) > 3 and shimaore_clean in audio_clean:
                match_type = "contains_shimaore"
                match_field = "shimaoré"
            elif len(kibouchi_clean) > 3 and kibouchi_clean in audio_clean:
                match_type = "contains_kibouchi"
                match_field = "kibouchi"
            
            if match_type:
                match_info = {
                    'verb_id': verb_id,
                    'french': french,
                    'shimaore': shimaore,
                    'kibouchi': kibouchi,
                    'audio_file': audio_file['filename'],
                    'audio_original_name': audio_original,
                    'audio_has_uppercase': audio_file['has_uppercase'],
                    'match_type': match_type,
                    'match_field': match_field,
                    'audio_size': audio_file['size']
                }
                
                matches_for_verb.append(match_info)
                correspondences.append(match_info)
                
                # Marquer les correspondances sensibles à la casse
                if audio_file['has_uppercase']:
                    case_sensitive_matches.append(match_info)
        
        if matches_for_verb:
            # Afficher les correspondances pour ce verbe
            logger.info(f"\n✅ {french:15} | {shimaore:20} | {kibouchi:20}")
            for match in matches_for_verb:
                case_icon = "🔤" if match['audio_has_uppercase'] else "📝"
                logger.info(f"   {case_icon} → {match['audio_file']:30} ({match['match_type']:15}) [{match['audio_size']:6} bytes]")
        else:
            unmatched_verbs.append(verb)
    
    # Fichiers audio non associés
    matched_files = [c['audio_file'] for c in correspondences]
    for audio_file in audio_files:
        if audio_file['filename'] not in matched_files:
            unmatched_audio.append(audio_file)
    
    return correspondences, unmatched_audio, unmatched_verbs, case_sensitive_matches, oumengna_verbs, oumengna_audio_candidates

def generate_verb_update_script(correspondences, case_sensitive_matches):
    """Génère un script de mise à jour spécifique pour les verbes"""
    
    logger.info(f"\n=== GÉNÉRATION SCRIPT MISE À JOUR VERBES ===")
    
    script_content = f"""#!/usr/bin/env python3
\"\"\"
Script de mise à jour des correspondances audio pour les VERBES
Généré automatiquement - {len(correspondences)} correspondances trouvées
Attention particulière aux majuscules dans les noms de fichiers
\"\"\"

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_database():
    mongo_url = os.getenv('MONGO_URL')
    client = MongoClient(mongo_url)
    return client['shimaoré_app']

def apply_verb_audio_correspondences():
    db = connect_to_database()
    collection = db['vocabulary']
    
    logger.info("🎯 Application des correspondances audio pour les VERBES")
    logger.info(f"Correspondances à traiter: {len(correspondences)}")
    
    # Correspondances trouvées avec attention aux majuscules
    correspondences = [
"""

    # Ajouter toutes les correspondances
    for match in correspondences:
        audio_path = f"audio/verbes/{match['audio_file']}"
        
        script_content += f"""        {{
            'verb_id': ObjectId('{match['verb_id']}'),
            'french': '{match['french']}',
            'shimaore': '{match['shimaore']}',
            'kibouchi': '{match['kibouchi']}',
            'audio_path': '{audio_path}',
            'audio_filename': '{match['audio_file']}',
            'audio_original_name': '{match['audio_original_name']}',
            'has_uppercase': {match['audio_has_uppercase']},
            'match_type': '{match['match_type']}',
            'match_field': '{match['match_field']}'
        }},
"""

    script_content += f"""    ]
    
    logger.info(f"Application de {{len(correspondences)}} correspondances...")
    
    # Statistiques
    exact_matches = sum(1 for c in correspondences if 'exact' in c['match_type'])
    partial_matches = sum(1 for c in correspondences if 'partial' in c['match_type'])
    case_sensitive = sum(1 for c in correspondences if c['has_uppercase'])
    
    logger.info(f"  - Correspondances exactes: {{exact_matches}}")
    logger.info(f"  - Correspondances partielles: {{partial_matches}}")  
    logger.info(f"  - Fichiers avec majuscules: {{case_sensitive}}")
    
    updated_count = 0
    errors = []
    
    for i, corr in enumerate(correspondences):
        try:
            # Vérifier que le fichier audio existe
            audio_file_path = f"/app/frontend/assets/{{corr['audio_path']}}"
            if not os.path.exists(audio_file_path):
                error_msg = f"Fichier audio non trouvé: {{audio_file_path}}"
                logger.warning(f"⚠️ {{error_msg}}")
                errors.append(error_msg)
                continue
            
            # Mise à jour de la base de données
            result = collection.update_one(
                {{"_id": corr['verb_id']}},
                {{
                    "$set": {{
                        "audio_authentic": corr['audio_path'],
                        "has_authentic_audio": True,
                        "audio_format": "m4a",
                        "auto_matched_verbs": True,
                        "match_type": corr['match_type'],
                        "match_field": corr['match_field'],
                        "case_sensitive_filename": corr['has_uppercase'],
                        "audio_updated_at": "{{}}".replace('{{}}', str(__import__('datetime').datetime.now()))
                    }}
                }}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                case_icon = "🔤" if corr['has_uppercase'] else "📝"
                logger.info(f"✅ {{i+1:3}}/{{len(correspondences)}} {{case_icon}} {{corr['french']:15}} → {{corr['audio_filename']}}")
            else:
                error_msg = f"Échec mise à jour verbe: {{corr['french']}}"
                logger.warning(f"❌ {{error_msg}}")
                errors.append(error_msg)
                
        except Exception as e:
            error_msg = f"Erreur traitement {{corr['french']}}: {{str(e)}}"
            logger.error(f"💥 {{error_msg}}")
            errors.append(error_msg)
    
    # Résultats finaux
    logger.info(f"\\n{'='*60}")
    logger.info(f"RÉSULTATS MISE À JOUR VERBES")
    logger.info(f"{'='*60}")
    logger.info(f"Mises à jour réussies: {{updated_count}}/{{len(correspondences)}}")
    logger.info(f"Erreurs: {{len(errors)}}")
    
    if errors:
        logger.info(f"\\nDétail des erreurs:")
        for error in errors:
            logger.info(f"  - {{error}}")
    
    # Vérification finale coverage
    total_verbs = collection.count_documents({{"section": "verbes"}})
    verbs_with_audio = collection.count_documents({{"section": "verbes", "has_authentic_audio": True}})
    coverage = (verbs_with_audio / total_verbs * 100) if total_verbs > 0 else 0
    
    logger.info(f"\\nCoverage audio finale verbes: {{verbs_with_audio}}/{{total_verbs}} ({{coverage:.1f}}%)")
    
    return updated_count, errors

if __name__ == "__main__":
    apply_verb_audio_correspondences()
"""

    # Écrire le script
    script_path = "/app/backend/apply_verbs_audio_matches.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    
    logger.info(f"Script généré: {script_path}")
    logger.info(f"Correspondances à appliquer: {len(correspondences)}")
    logger.info(f"Correspondances avec majuscules: {len(case_sensitive_matches)}")
    
    return script_path

def main():
    """Fonction principale"""
    logger.info("🎯 ANALYSE SPÉCIFIQUE VERBES - ATTENTION AUX MAJUSCULES")
    logger.info("Demande utilisateur: 'oumengna' base de données vs 'Oumengna' fichiers audio")
    
    try:
        # 1. Scanner les fichiers audio des verbes
        audio_files = scan_verbs_audio_files()
        
        if not audio_files:
            logger.error("Aucun fichier audio trouvé pour les verbes")
            return None
        
        # 2. Récupérer les verbes de la base
        verbs = get_verbs_from_database()
        
        if not verbs:
            logger.error("Aucun verbe trouvé dans la base de données")
            return None
        
        # 3. Analyser les correspondances
        correspondences, unmatched_audio, unmatched_verbs, case_sensitive_matches, oumengna_verbs, oumengna_audio_candidates = analyze_verb_audio_correspondences(audio_files, verbs)
        
        # 4. Résultats détaillés
        logger.info(f"\n{'='*80}")
        logger.info("RÉSULTATS ANALYSE VERBES-AUDIO")
        logger.info(f"{'='*80}")
        
        logger.info(f"📊 STATISTIQUES GLOBALES:")
        logger.info(f"  - Fichiers audio verbes: {len(audio_files)}")
        logger.info(f"  - Verbes en base: {len(verbs)}")
        logger.info(f"  - Correspondances trouvées: {len(correspondences)}")
        logger.info(f"  - Fichiers avec majuscules: {sum(1 for f in audio_files if f['has_uppercase'])}")
        logger.info(f"  - Correspondances avec majuscules: {len(case_sensitive_matches)}")
        
        logger.info(f"\n🔍 PROBLÈME SPÉCIFIQUE 'OUMENGNA':")
        logger.info(f"  - Verbes avec 'oumengna': {len(oumengna_verbs)}")
        logger.info(f"  - Fichiers audio candidats: {len(oumengna_audio_candidates)}")
        
        if oumengna_verbs:
            logger.info(f"  📝 Détails verbes 'oumengna':")
            for ov in oumengna_verbs:
                logger.info(f"     → {ov['french']:15} | {ov['shimaore']:20} | {ov['kibouchi']:20}")
        
        if oumengna_audio_candidates:
            logger.info(f"  🔊 Fichiers audio candidats:")
            for audio in oumengna_audio_candidates:
                case_info = "avec majuscules" if audio['has_uppercase'] else "minuscules"
                logger.info(f"     → {audio['filename']:30} ({case_info})")
        
        # 5. Correspondances sensibles à la casse
        if case_sensitive_matches:
            logger.info(f"\n🔤 CORRESPONDANCES AVEC MAJUSCULES ({len(case_sensitive_matches)}):")
            for match in case_sensitive_matches[:10]:  # Afficher les 10 premières
                logger.info(f"  → {match['french']:15} | {match['audio_file']:25} | {match['match_type']:15}")
        
        # 6. Fichiers non associés
        if unmatched_audio:
            logger.info(f"\n❌ FICHIERS AUDIO NON ASSOCIÉS ({len(unmatched_audio)}):")
            for audio in unmatched_audio[:10]:
                case_info = "🔤" if audio['has_uppercase'] else "📝"
                logger.info(f"  {case_info} {audio['filename']:30} → {audio['name_original']}")
        
        # 7. Verbes sans audio
        if unmatched_verbs:
            logger.info(f"\n🔇 VERBES SANS AUDIO ({len(unmatched_verbs)}):")
            for verb in unmatched_verbs[:10]:
                logger.info(f"  → {verb.get('french', 'N/A'):15} | {verb.get('shimaoré', 'N/A'):20} | {verb.get('kibouchi', 'N/A'):20}")
        
        # 8. Générer le script de mise à jour
        if correspondences:
            script_path = generate_verb_update_script(correspondences, case_sensitive_matches)
            
            logger.info(f"\n🎉 ANALYSE TERMINÉE!")
            logger.info(f"📄 Script généré: {script_path}")
            logger.info(f"🔄 Prêt à appliquer {len(correspondences)} correspondances")
            logger.info(f"🔤 Dont {len(case_sensitive_matches)} avec attention aux majuscules")
        else:
            logger.warning(f"\n⚠️ Aucune correspondance trouvée!")
        
        return {
            'correspondences': correspondences,
            'case_sensitive_matches': case_sensitive_matches,
            'oumengna_verbs': oumengna_verbs,
            'oumengna_audio_candidates': oumengna_audio_candidates,
            'unmatched_audio': unmatched_audio,
            'unmatched_verbs': unmatched_verbs
        }
        
    except Exception as e:
        logger.error(f"Erreur dans l'analyse verbes: {e}")
        return None

if __name__ == "__main__":
    main()