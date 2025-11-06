#!/usr/bin/env python3
"""
Corriger les sections de la base de données selon les spécifications utilisateur
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URL)
db = client['shimaoré_app']

print('=== CORRECTION DES SECTIONS ===')

# 1. Fusionner 'corps' dans 'corps_humain'
corps_words = list(db.vocabulary.find({'section': 'corps'}))
print(f'Fusion de {len(corps_words)} mots de "corps" vers "corps_humain"')

for word in corps_words:
    db.vocabulary.update_one(
        {'_id': word['_id']}, 
        {'$set': {'section': 'corps_humain'}}
    )

print('✅ Section "corps" fusionnée dans "corps_humain"')

# 2. Corriger 'vetements' en 'vêtements'
result = db.vocabulary.update_many(
    {'section': 'vetements'},
    {'$set': {'section': 'vêtements'}}
)
print(f'✅ {result.modified_count} mots mis à jour de "vetements" vers "vêtements"')

# 3. Rechercher des expressions et grammaire mal classées
print(f'\n=== RECHERCHE DE MOTS MAL CLASSÉS ===')

# Expressions courantes qui pourraient être mal classées
expressions_patterns = [
    'avoir faim', 'avoir soif', 'avoir peur', 'avoir mal', 'avoir sommeil',
    'il y a', "il n'y a pas", 'beaucoup', 'peu', 'très bien', 'pas grave',
    'de rien', "s'il vous plaît", 'peut-être', 'comment ça va', 'ça va bien',
    'excuse-moi', 'je suis désolé', "j'ai oublié", 'je ne sais pas',
    'je ne comprends pas', "qu'est-ce que c'est", "qu'est-ce qu'il y a"
]

# Grammaire (pronoms, possessifs)
grammaire_patterns = [
    'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
    'le mien', 'le tien', 'le sien', 'le nôtre', 'le vôtre', 'le leur'
]

# Chercher les expressions
for pattern in expressions_patterns:
    found = list(db.vocabulary.find({
        'french': {'$regex': f'^{pattern}$', '$options': 'i'},
        'section': {'$ne': 'expressions'}
    }))
    
    for word in found:
        print(f'EXPRESSION trouvée dans "{word["section"]}": {word["french"]} = {word.get("shimaoré", "")} / {word.get("kibouchi", "")}')
        # Déplacer vers expressions
        db.vocabulary.update_one(
            {'_id': word['_id']},
            {'$set': {'section': 'expressions'}}
        )

# Chercher la grammaire  
for pattern in grammaire_patterns:
    found = list(db.vocabulary.find({
        'french': {'$regex': f'^{pattern}$', '$options': 'i'},
        'section': {'$ne': 'grammaire'}
    }))
    
    for word in found:
        print(f'GRAMMAIRE trouvée dans "{word["section"]}": {word["french"]} = {word.get("shimaoré", "")} / {word.get("kibouchi", "")}')
        # Déplacer vers grammaire
        db.vocabulary.update_one(
            {'_id': word['_id']},
            {'$set': {'section': 'grammaire'}}
        )

# Vérifications finales
print(f'\n=== ÉTAT FINAL DES SECTIONS ===')
sections = db.vocabulary.distinct('section')
expected_sections = ['adjectifs', 'animaux', 'corps_humain', 'couleurs', 'famille', 'maison', 'nature', 'nombres', 'nourriture', 'salutations', 'transport', 'verbes', 'vêtements', 'expressions', 'grammaire']

for section in sorted(sections):
    count = db.vocabulary.count_documents({'section': section})
    status = "✅" if section in expected_sections else "❌"
    print(f'  {status} {section}: {count} mots')

total = db.vocabulary.count_documents({})
print(f'\nTotal: {total} mots')

print(f'\n=== SECTIONS ATTENDUES vs ACTUELLES ===')
missing = set(expected_sections) - set(sections)
extra = set(sections) - set(expected_sections)

if missing:
    print(f'❌ Sections toujours manquantes: {missing}')
else:
    print('✅ Toutes les sections attendues sont présentes')

if extra:
    print(f'⚠️ Sections en trop: {extra}')
else:
    print('✅ Aucune section en trop')

print('\n=== CORRECTION TERMINÉE ===')