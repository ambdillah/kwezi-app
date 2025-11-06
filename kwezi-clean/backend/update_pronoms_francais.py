#!/usr/bin/env python3
"""
Script pour mettre à jour les pronoms français dans la base de données
Basé sur l'image fournie par l'utilisateur
Date: 14 octobre 2025
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

# Connexion MongoDB
mongo_url = os.getenv('MONGO_URL')
client = MongoClient(mongo_url)
db = client[os.getenv('DB_NAME', 'mayotte_app')]

print("=" * 70)
print("MISE À JOUR DES PRONOMS FRANÇAIS")
print("=" * 70)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Définir les mises à jour basées sur l'image
updates = [
    {
        'old_french': 'Je',
        'new_french': 'Je / moi',
        'new_shimaore': 'Nani',
        'new_kibouchi': 'Ma',
        'action': 'update'
    },
    {
        'old_french': 'Tu',
        'new_french': 'Tu / toi',
        'new_shimaore': 'Wé',
        'new_kibouchi': 'Ya',
        'action': 'update'
    },
    {
        'old_french': 'Il/elle',
        'new_french': 'Il / Elle / lui',
        'new_shimaore': 'Ye',
        'new_kibouchi': 'Na',
        'action': 'update'
    },
    {
        'old_french': 'Nous',
        'new_french': 'Nous',
        'new_shimaore': 'Rihi',  # ou "Izou"
        'new_kibouchi': 'Gali',
        'action': 'update'
    },
    {
        'old_french': 'Ils/elles',
        'new_french': 'Ils / Elles / eux',
        'new_shimaore': 'Bé',  # ou "Vanyè"
        'new_kibouchi': 'Nao',
        'action': 'update'
    }
]

# Effectuer les mises à jour
successful_updates = 0
failed_updates = 0

for update in updates:
    print(f"\n{'='*70}")
    print(f"Mise à jour: '{update['old_french']}' → '{update['new_french']}'")
    print(f"{'='*70}")
    
    # Chercher l'entrée existante
    existing = db['words'].find_one({
        'french': update['old_french'],
        'category': 'grammaire'
    })
    
    if existing:
        print(f"✅ Trouvé en base:")
        print(f"   Ancien français: {existing['french']}")
        print(f"   Ancien shimaoré: {existing.get('shimaore', 'N/A')}")
        print(f"   Ancien kibouchi: {existing.get('kibouchi', 'N/A')}")
        
        # Préparer les nouvelles valeurs
        update_data = {
            'french': update['new_french'],
            'shimaore': update['new_shimaore'],
            'kibouchi': update['new_kibouchi'],
            'updated_at': datetime.utcnow()
        }
        
        # Effectuer la mise à jour
        result = db['words'].update_one(
            {'_id': existing['_id']},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            print(f"\n✅ MISE À JOUR RÉUSSIE:")
            print(f"   Nouveau français: {update['new_french']}")
            print(f"   Nouveau shimaoré: {update['new_shimaore']}")
            print(f"   Nouveau kibouchi: {update['new_kibouchi']}")
            successful_updates += 1
        else:
            print(f"\n⚠️ Aucune modification effectuée (données identiques?)")
            failed_updates += 1
    else:
        print(f"❌ NON trouvé en base: '{update['old_french']}'")
        print(f"   Recherche alternative...")
        
        # Essayer de trouver avec une variante
        alt_search = db['words'].find_one({
            'category': 'grammaire',
            '$or': [
                {'french': {'$regex': update['old_french'], '$options': 'i'}},
                {'french': update['new_french']}
            ]
        })
        
        if alt_search:
            print(f"   ✅ Trouvé variante: '{alt_search['french']}'")
            print(f"   Mise à jour de cette variante...")
            
            update_data = {
                'french': update['new_french'],
                'shimaore': update['new_shimaore'],
                'kibouchi': update['new_kibouchi'],
                'updated_at': datetime.utcnow()
            }
            
            result = db['words'].update_one(
                {'_id': alt_search['_id']},
                {'$set': update_data}
            )
            
            if result.modified_count > 0:
                print(f"   ✅ Mise à jour réussie")
                successful_updates += 1
            else:
                failed_updates += 1
        else:
            print(f"   ❌ Aucune variante trouvée")
            failed_updates += 1

# Résumé final
print(f"\n{'='*70}")
print("RÉSUMÉ DES MISES À JOUR")
print(f"{'='*70}")
print(f"✅ Mises à jour réussies: {successful_updates}")
print(f"❌ Échecs: {failed_updates}")
print(f"📊 Total pronoms traités: {len(updates)}")

# Afficher l'état final
print(f"\n{'='*70}")
print("ÉTAT FINAL DES PRONOMS")
print(f"{'='*70}")

pronoms_finaux = list(db['words'].find({
    'category': 'grammaire',
    'french': {'$in': [u['new_french'] for u in updates]}
}).sort('french', 1))

for pron in pronoms_finaux:
    print(f"\n✅ {pron['french']}")
    print(f"   Shimaoré: {pron.get('shimaore', 'N/A')}")
    print(f"   Kibouchi: {pron.get('kibouchi', 'N/A')}")

print(f"\n{'='*70}")
print("SCRIPT TERMINÉ")
print(f"{'='*70}")

client.close()
