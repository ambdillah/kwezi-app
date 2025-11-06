#!/usr/bin/env python3
"""
Script de mise à jour des correspondances audio pour les VERBES
Généré automatiquement - 41 correspondances trouvées
Attention particulière aux majuscules dans les noms de fichiers
"""

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
    logger.info(f"Correspondances à traiter: 41")
    
    # Correspondances trouvées avec attention aux majuscules
    correspondences = [
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79c96'),
            'french': 'dire',
            'shimaore': 'ourongoa',
            'kibouchi': 'mangnabara',
            'audio_path': 'audio/verbes/Mangnabara.m4a',
            'audio_filename': 'Mangnabara.m4a',
            'audio_original_name': 'Mangnabara',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79c97'),
            'french': 'pouvoir',
            'shimaore': 'ouchindra',
            'kibouchi': 'mahaléou',
            'audio_path': 'audio/verbes/Mahaléou.m4a',
            'audio_filename': 'Mahaléou.m4a',
            'audio_original_name': 'Mahaléou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79c98'),
            'french': 'vouloir',
            'shimaore': 'outsaha',
            'kibouchi': 'chokou',
            'audio_path': 'audio/verbes/Chokou.m4a',
            'audio_filename': 'Chokou.m4a',
            'audio_original_name': 'Chokou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79c9a'),
            'french': 'voir',
            'shimaore': 'ouona',
            'kibouchi': 'mahita',
            'audio_path': 'audio/verbes/Mahita.m4a',
            'audio_filename': 'Mahita.m4a',
            'audio_original_name': 'Mahita',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79c9c'),
            'french': 'venir',
            'shimaore': 'ouja',
            'kibouchi': 'havi',
            'audio_path': 'audio/verbes/Havi.m4a',
            'audio_filename': 'Havi.m4a',
            'audio_original_name': 'Havi',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79c9d'),
            'french': 'approcher',
            'shimaore': 'outsenguéléya',
            'kibouchi': 'magnatougnou',
            'audio_path': 'audio/verbes/Magnatougnou.m4a',
            'audio_filename': 'Magnatougnou.m4a',
            'audio_original_name': 'Magnatougnou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79c9e'),
            'french': 'prendre',
            'shimaore': 'ourenga',
            'kibouchi': 'mangala',
            'audio_path': 'audio/verbes/Mangala.m4a',
            'audio_filename': 'Mangala.m4a',
            'audio_original_name': 'Mangala',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79c9e'),
            'french': 'prendre',
            'shimaore': 'ourenga',
            'kibouchi': 'mangala',
            'audio_path': 'audio/verbes/Mangalatra.m4a',
            'audio_filename': 'Mangalatra.m4a',
            'audio_original_name': 'Mangalatra',
            'has_uppercase': True,
            'match_type': 'contains_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79c9f'),
            'french': 'donner',
            'shimaore': 'ouva',
            'kibouchi': 'magnamiya',
            'audio_path': 'audio/verbes/Magnamiya.m4a',
            'audio_filename': 'Magnamiya.m4a',
            'audio_original_name': 'Magnamiya',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79ca3'),
            'french': 'trouver',
            'shimaore': 'oupara',
            'kibouchi': 'mahazou',
            'audio_path': 'audio/verbes/Mahazou.m4a',
            'audio_filename': 'Mahazou.m4a',
            'audio_original_name': 'Mahazou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79ca5'),
            'french': 'croire',
            'shimaore': 'ouamini',
            'kibouchi': 'koimini',
            'audio_path': 'audio/verbes/Koimini.m4a',
            'audio_filename': 'Koimini.m4a',
            'audio_original_name': 'Koimini',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79ca8'),
            'french': 'demander',
            'shimaore': 'oudzissa',
            'kibouchi': 'magnoutani',
            'audio_path': 'audio/verbes/Magnoutani.m4a',
            'audio_filename': 'Magnoutani.m4a',
            'audio_original_name': 'Magnoutani',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79caa'),
            'french': 'laisser',
            'shimaore': 'oulicha',
            'kibouchi': 'mangnambéla',
            'audio_path': 'audio/verbes/Mangnambéla.m4a',
            'audio_filename': 'Mangnambéla.m4a',
            'audio_original_name': 'Mangnambéla',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cb1'),
            'french': 'comprendre',
            'shimaore': 'ouéléwa',
            'kibouchi': 'kouéléwa',
            'audio_path': 'audio/verbes/Kouéléwa.m4a',
            'audio_filename': 'Kouéléwa.m4a',
            'audio_original_name': 'Kouéléwa',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cb2'),
            'french': 'marcher',
            'shimaore': 'ouendra',
            'kibouchi': 'mandéha',
            'audio_path': 'audio/verbes/Mandéha.m4a',
            'audio_filename': 'Mandéha.m4a',
            'audio_original_name': 'Mandéha',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cb7'),
            'french': 'dormir',
            'shimaore': 'oulala',
            'kibouchi': 'koimini',
            'audio_path': 'audio/verbes/Koimini.m4a',
            'audio_filename': 'Koimini.m4a',
            'audio_original_name': 'Koimini',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cb8'),
            'french': 'attendre',
            'shimaore': 'oulindra',
            'kibouchi': 'mandigni',
            'audio_path': 'audio/verbes/Mandigni.m4a',
            'audio_filename': 'Mandigni.m4a',
            'audio_original_name': 'Mandigni',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cbd'),
            'french': 'sembler',
            'shimaore': 'oufana',
            'kibouchi': 'mampihiragna',
            'audio_path': 'audio/verbes/Mampihiragna.m4a',
            'audio_filename': 'Mampihiragna.m4a',
            'audio_original_name': 'Mampihiragna',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cbf'),
            'french': 'casser',
            'shimaore': 'latsaka',
            'kibouchi': 'latsaka',
            'audio_path': 'audio/verbes/Latsaka.m4a',
            'audio_filename': 'Latsaka.m4a',
            'audio_original_name': 'Latsaka',
            'has_uppercase': True,
            'match_type': 'exact_shimaore',
            'match_field': 'shimaoré'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cc0'),
            'french': 'se rappeler',
            'shimaore': 'oumaézi',
            'kibouchi': 'koufahamou',
            'audio_path': 'audio/verbes/Koufahamou.m4a',
            'audio_filename': 'Koufahamou.m4a',
            'audio_original_name': 'Koufahamou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cc3'),
            'french': 'réussir',
            'shimaore': 'ouchindra',
            'kibouchi': 'mahaléou',
            'audio_path': 'audio/verbes/Mahaléou.m4a',
            'audio_filename': 'Mahaléou.m4a',
            'audio_original_name': 'Mahaléou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cc6'),
            'french': 'danser',
            'shimaore': 'ouzina',
            'kibouchi': 'chokou',
            'audio_path': 'audio/verbes/Chokou.m4a',
            'audio_filename': 'Chokou.m4a',
            'audio_original_name': 'Chokou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cc8'),
            'french': 'vendre',
            'shimaore': 'ouhoudza',
            'kibouchi': 'mandafou',
            'audio_path': 'audio/verbes/Mandafou.m4a',
            'audio_filename': 'Mandafou.m4a',
            'audio_original_name': 'Mandafou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79ccc'),
            'french': 'piler',
            'shimaore': 'oudoudoua',
            'kibouchi': 'mandissa',
            'audio_path': 'audio/verbes/Mandissa.m4a',
            'audio_filename': 'Mandissa.m4a',
            'audio_original_name': 'Mandissa',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79ccd'),
            'french': 'changer',
            'shimaore': 'ougaoudza',
            'kibouchi': 'mamadiki',
            'audio_path': 'audio/verbes/Mamadiki.m4a',
            'audio_filename': 'Mamadiki.m4a',
            'audio_original_name': 'Mamadiki',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cce'),
            'french': 'réchauffer',
            'shimaore': 'ouhelesedza',
            'kibouchi': 'mamana',
            'audio_path': 'audio/verbes/Mamana.m4a',
            'audio_filename': 'Mamana.m4a',
            'audio_original_name': 'Mamana',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79ccf'),
            'french': 'balayer',
            'shimaore': 'ouhoundza',
            'kibouchi': 'mamafa',
            'audio_path': 'audio/verbes/Mamafa.m4a',
            'audio_filename': 'Mamafa.m4a',
            'audio_original_name': 'Mamafa',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cd0'),
            'french': 'couper',
            'shimaore': 'oukatra',
            'kibouchi': 'manapaka',
            'audio_path': 'audio/verbes/Manapaka somboutrou.m4a',
            'audio_filename': 'Manapaka somboutrou.m4a',
            'audio_original_name': 'Manapaka somboutrou',
            'has_uppercase': True,
            'match_type': 'contains_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cd0'),
            'french': 'couper',
            'shimaore': 'oukatra',
            'kibouchi': 'manapaka',
            'audio_path': 'audio/verbes/Manapaka.m4a',
            'audio_filename': 'Manapaka.m4a',
            'audio_original_name': 'Manapaka',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cd1'),
            'french': 'abîmer',
            'shimaore': 'oumengna',
            'kibouchi': 'manapaka somboutrou',
            'audio_path': 'audio/verbes/Manapaka somboutrou.m4a',
            'audio_filename': 'Manapaka somboutrou.m4a',
            'audio_original_name': 'Manapaka somboutrou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cd1'),
            'french': 'abîmer',
            'shimaore': 'oumengna',
            'kibouchi': 'manapaka somboutrou',
            'audio_path': 'audio/verbes/Manapaka.m4a',
            'audio_filename': 'Manapaka.m4a',
            'audio_original_name': 'Manapaka',
            'has_uppercase': True,
            'match_type': 'partial_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cd5'),
            'french': 'cuisiner',
            'shimaore': 'oupiha',
            'kibouchi': 'mahandrou',
            'audio_path': 'audio/verbes/Mahandrou.m4a',
            'audio_filename': 'Mahandrou.m4a',
            'audio_original_name': 'Mahandrou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cd6'),
            'french': 'ranger',
            'shimaore': 'ourenguélédza',
            'kibouchi': 'magnadzari',
            'audio_path': 'audio/verbes/Magnadzari.m4a',
            'audio_filename': 'Magnadzari.m4a',
            'audio_original_name': 'Magnadzari',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cd8'),
            'french': 'peindre',
            'shimaore': 'ouvaha',
            'kibouchi': 'magnossoutrou',
            'audio_path': 'audio/verbes/Magnossoutrou.m4a',
            'audio_filename': 'Magnossoutrou.m4a',
            'audio_original_name': 'Magnossoutrou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cd9'),
            'french': 'essuyer',
            'shimaore': 'ouvangouha',
            'kibouchi': 'mamitri',
            'audio_path': 'audio/verbes/Mamitri.m4a',
            'audio_filename': 'Mamitri.m4a',
            'audio_original_name': 'Mamitri',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cda'),
            'french': 'apporter',
            'shimaore': 'ouvinga',
            'kibouchi': 'mandèyi',
            'audio_path': 'audio/verbes/Mandèyi.m4a',
            'audio_filename': 'Mandèyi.m4a',
            'audio_original_name': 'Mandèyi',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cdb'),
            'french': 'éteindre',
            'shimaore': 'ouzima',
            'kibouchi': 'mamounou',
            'audio_path': 'audio/verbes/Mamounou.m4a',
            'audio_filename': 'Mamounou.m4a',
            'audio_original_name': 'Mamounou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cdc'),
            'french': 'tuer',
            'shimaore': 'ouwoula',
            'kibouchi': 'mamounou',
            'audio_path': 'audio/verbes/Ouwoula.m4a',
            'audio_filename': 'Ouwoula.m4a',
            'audio_original_name': 'Ouwoula',
            'has_uppercase': True,
            'match_type': 'exact_shimaore',
            'match_field': 'shimaoré'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cdc'),
            'french': 'tuer',
            'shimaore': 'ouwoula',
            'kibouchi': 'mamounou',
            'audio_path': 'audio/verbes/Mamounou.m4a',
            'audio_filename': 'Mamounou.m4a',
            'audio_original_name': 'Mamounou',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79cde'),
            'french': 'cueillir',
            'shimaore': 'oupoua',
            'kibouchi': 'mampoka',
            'audio_path': 'audio/verbes/Mampoka.m4a',
            'audio_filename': 'Mampoka.m4a',
            'audio_original_name': 'Mampoka',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
        {
            'verb_id': ObjectId('68d52eff53dfba3e80a79ce1'),
            'french': 'récolter',
            'shimaore': 'ouvouna',
            'kibouchi': 'mampoka',
            'audio_path': 'audio/verbes/Mampoka.m4a',
            'audio_filename': 'Mampoka.m4a',
            'audio_original_name': 'Mampoka',
            'has_uppercase': True,
            'match_type': 'exact_kibouchi',
            'match_field': 'kibouchi'
        },
    ]
    
    logger.info(f"Application de {len(correspondences)} correspondances...")
    
    # Statistiques
    exact_matches = sum(1 for c in correspondences if 'exact' in c['match_type'])
    partial_matches = sum(1 for c in correspondences if 'partial' in c['match_type'])
    case_sensitive = sum(1 for c in correspondences if c['has_uppercase'])
    
    logger.info(f"  - Correspondances exactes: {exact_matches}")
    logger.info(f"  - Correspondances partielles: {partial_matches}")  
    logger.info(f"  - Fichiers avec majuscules: {case_sensitive}")
    
    updated_count = 0
    errors = []
    
    for i, corr in enumerate(correspondences):
        try:
            # Vérifier que le fichier audio existe
            audio_file_path = f"/app/frontend/assets/{corr['audio_path']}"
            if not os.path.exists(audio_file_path):
                error_msg = f"Fichier audio non trouvé: {audio_file_path}"
                logger.warning(f"⚠️ {error_msg}")
                errors.append(error_msg)
                continue
            
            # Mise à jour de la base de données
            result = collection.update_one(
                {"_id": corr['verb_id']},
                {
                    "$set": {
                        "audio_authentic": corr['audio_path'],
                        "has_authentic_audio": True,
                        "audio_format": "m4a",
                        "auto_matched_verbs": True,
                        "match_type": corr['match_type'],
                        "match_field": corr['match_field'],
                        "case_sensitive_filename": corr['has_uppercase'],
                        "audio_updated_at": "{}".replace('{}', str(__import__('datetime').datetime.now()))
                    }
                }
            )
            
            if result.modified_count > 0:
                updated_count += 1
                case_icon = "🔤" if corr['has_uppercase'] else "📝"
                logger.info(f"✅ {i+1:3}/{len(correspondences)} {case_icon} {corr['french']:15} → {corr['audio_filename']}")
            else:
                error_msg = f"Échec mise à jour verbe: {corr['french']}"
                logger.warning(f"❌ {error_msg}")
                errors.append(error_msg)
                
        except Exception as e:
            error_msg = f"Erreur traitement {corr['french']}: {str(e)}"
            logger.error(f"💥 {error_msg}")
            errors.append(error_msg)
    
    # Résultats finaux
    logger.info(f"\n============================================================")
    logger.info(f"RÉSULTATS MISE À JOUR VERBES")
    logger.info(f"============================================================")
    logger.info(f"Mises à jour réussies: {updated_count}/{len(correspondences)}")
    logger.info(f"Erreurs: {len(errors)}")
    
    if errors:
        logger.info(f"\nDétail des erreurs:")
        for error in errors:
            logger.info(f"  - {error}")
    
    # Vérification finale coverage
    total_verbs = collection.count_documents({"section": "verbes"})
    verbs_with_audio = collection.count_documents({"section": "verbes", "has_authentic_audio": True})
    coverage = (verbs_with_audio / total_verbs * 100) if total_verbs > 0 else 0
    
    logger.info(f"\nCoverage audio finale verbes: {verbs_with_audio}/{total_verbs} ({coverage:.1f}%)")
    
    return updated_count, errors

if __name__ == "__main__":
    apply_verb_audio_correspondences()
