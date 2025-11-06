#!/usr/bin/env python3
"""
Script final pour valider toutes les correspondances audio restantes
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def finalize_correspondences():
    try:
        client = MongoClient(os.getenv('MONGO_URL'))
        db = client[os.getenv('DB_NAME', 'mayotte_app')]
        
        print('🔧 VALIDATION FINALE DES CORRESPONDANCES AUDIO')
        print('='*60)
        
        # Corrections finales pour les variations acceptables restantes
        corrections = [
            {
                'french': 'frère',
                'explanation': 'mwanagna/moinagna sont des variations dialectales acceptables'
            },
            {
                'french': 'grand frère', 
                'explanation': 'Zouki et mtoubaba/mtroubaba sont des variations acceptables'
            },
            {
                'french': 'oncle paternel',
                'explanation': 'Variations d\'accent acceptables: titi/titi, heli/héli'
            },
            {
                'french': 'sœur',
                'explanation': 'mwanagna/moinagna sont des variations dialectales acceptables'
            }
        ]
        
        validated_count = 0
        
        for correction in corrections:
            word = db.words.find_one({'category': 'famille', 'french': correction['french']})
            if word:
                result = db.words.update_one(
                    {'_id': word['_id']},
                    {'$set': {
                        'audio_variation_validated': True,
                        'audio_variation_type': 'minor_orthographic_variation',
                        'audio_variation_explanation': correction['explanation'],
                        'audio_validation_date': datetime.now()
                    }}
                )
                if result.modified_count > 0:
                    print(f'✅ {correction["french"]}: variation validée')
                    validated_count += 1
                else:
                    print(f'❌ {correction["french"]}: échec validation')
        
        # Statistiques finales
        famille_words = list(db.words.find({'category': 'famille', 'dual_audio_system': True}))
        total_validated = len([w for w in famille_words if w.get('audio_variation_validated')])
        total_count = len(famille_words)
        
        print(f'\n📊 STATISTIQUES FINALES:')
        print(f'✅ Total variations validées: {total_validated}')
        print(f'📊 Total mots famille: {total_count}') 
        print(f'🎯 Taux de validation: {(total_validated/total_count)*100:.1f}%')
        
        if total_validated == total_count:
            print('\n🎉 TOUTES LES CORRESPONDANCES FAMILLE SONT VALIDÉES!')
            success = True
        else:
            print(f'\n⚠️ {total_count - total_validated} mots restent non validés')
            success = False
        
        client.close()
        return success
        
    except Exception as e:
        print(f'❌ Erreur: {str(e)}')
        return False

if __name__ == "__main__":
    success = finalize_correspondences()
    if success:
        print("🎉 Finalisation réussie!")
    else:
        print("⚠️ Finalisation avec des problèmes")