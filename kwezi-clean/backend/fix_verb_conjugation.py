#!/usr/bin/env python3
"""
Correction CIBLÉE des verbes à l'infinitif dans les phrases françaises
UNIQUEMENT le champ 'french' est modifié, aucun impact sur shimaoré/kibouchi
Date: 14 octobre 2025
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

mongo_url = os.getenv('MONGO_URL')
client = MongoClient(mongo_url)
db = client[os.getenv('DB_NAME', 'mayotte_app')]

print("=" * 80)
print("🔧 CORRECTION CIBLÉE - Conjugaison des verbes français")
print("=" * 80)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Corrections à appliquer (UNIQUEMENT le français)
corrections = [
    # Je
    {
        '_id': '68de375f0fe3734a45d523e3',
        'old': 'je amener/apporter',
        'new': "j'amène/apporte"
    },
    {
        '_id': '68de375f0fe3734a45d523e4',
        'old': 'je amener/apporter',
        'new': "j'amenais/apportais"
    },
    # Tu
    {
        '_id': '68de375f0fe3734a45d523e5',
        'old': 'tu amener/apportes',
        'new': 'tu amènes/apportes'
    },
    {
        '_id': '68de375f0fe3734a45d523e6',
        'old': 'tu amener/apporter',
        'new': 'tu amenais/apportais'
    },
    {
        '_id': '68de375f0fe3734a45d523e7',
        'old': 'tu amener/apporter',
        'new': 'tu amèneras/apporteras'
    },
    # Il/Elle
    {
        '_id': '68de375f0fe3734a45d523e8',
        'old': 'il amener/apporte',
        'new': 'il amène/apporte'
    },
    {
        '_id': '68de375f0fe3734a45d523e9',
        'old': 'il amener/apporter',
        'new': 'il amenait/apportait'
    },
    {
        '_id': '68de375f0fe3734a45d523ea',
        'old': 'il amener/apporter',
        'new': 'il amènera/apportera'
    },
    # Nous
    {
        '_id': '68de375f0fe3734a45d523eb',
        'old': 'nous amener/apportons',
        'new': 'nous amenons/apportons'
    },
    {
        '_id': '68de375f0fe3734a45d523ec',
        'old': 'nous amener/apporter',
        'new': 'nous amenions/apportions'
    },
    {
        '_id': '68de375f0fe3734a45d523ed',
        'old': 'nous amener/apporter',
        'new': 'nous amènerons/apporterons'
    },
    # Vous
    {
        '_id': '68de375f0fe3734a45d523ee',
        'old': 'vous amener/apportez',
        'new': 'vous amenez/apportez'
    },
    {
        '_id': '68de375f0fe3734a45d523ef',
        'old': 'vous amener/apporter',
        'new': 'vous ameniez/apportiez'
    },
    {
        '_id': '68de375f0fe3734a45d523f0',
        'old': 'vous amener/apporter',
        'new': 'vous amènerez/apporterez'
    },
    # Ils/Elles
    {
        '_id': '68de375f0fe3734a45d523f1',
        'old': 'ils amener/apportent',
        'new': 'ils amènent/apportent'
    },
    {
        '_id': '68de375f0fe3734a45d523f2',
        'old': 'ils amener/apporter',
        'new': 'ils amenaient/apportaient'
    },
    {
        '_id': '68de375f0fe3734a45d523f3',
        'old': 'ils amener/apporter',
        'new': 'ils amèneront/apporteront'
    },
]

print("⚠️  IMPORTANT:")
print("   - Seul le champ 'french' sera modifié")
print("   - Aucun impact sur 'shimaore' et 'kibouchi'")
print("   - Aucun impact sur les autres phrases")
print()

successful = 0
failed = 0
not_found = 0

for correction in corrections:
    from bson import ObjectId
    
    try:
        # Convertir l'ID string en ObjectId
        obj_id = ObjectId(correction['_id'])
        
        # Trouver la phrase
        sentence = db['sentences'].find_one({'_id': obj_id})
        
        if not sentence:
            print(f"❌ Phrase non trouvée: {correction['_id']}")
            not_found += 1
            continue
        
        print(f"📝 Correction: {correction['_id'][:10]}...")
        print(f"   AVANT: {sentence.get('french')}")
        print(f"   APRÈS: {correction['new']}")
        
        # Appliquer UNIQUEMENT la correction du français
        result = db['sentences'].update_one(
            {'_id': obj_id},
            {
                '$set': {
                    'french': correction['new'],
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        if result.modified_count > 0:
            print(f"   ✅ Corrigé")
            successful += 1
        else:
            print(f"   ⚠️  Aucune modification (déjà correct?)")
        
        print()
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        failed += 1

print("=" * 80)
print("RÉSUMÉ")
print("=" * 80)
print(f"✅ Corrections réussies: {successful}")
print(f"⚠️  Non trouvées: {not_found}")
print(f"❌ Échecs: {failed}")
print(f"📊 Total traité: {len(corrections)}")

# Vérification finale
print(f"\n{'='*80}")
print("VÉRIFICATION FINALE")
print(f"{'='*80}")

still_wrong = db['sentences'].count_documents({
    'french': {'$regex': '^(Je|Tu|Il|Elle|Nous|Vous|Ils|Elles) amener', '$options': 'i'}
})

print(f"\nPhrases encore à l'infinitif: {still_wrong}")

if still_wrong == 0:
    print("🎉 TOUTES LES PHRASES SONT CORRECTEMENT CONJUGUÉES !")
else:
    print(f"⚠️  Il reste {still_wrong} phrases à corriger")

print(f"\n{'='*80}")
print("CORRECTION TERMINÉE")
print(f"{'='*80}")

client.close()
