"""
Script pour corriger l'orthographe des expressions afin de correspondre
EXACTEMENT aux noms des fichiers audio (sans trémas, avec bons accents)
"""

from pymongo import MongoClient
import os

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['mayotte_app']
words_collection = db['words']

print("="*80)
print("CORRECTION ORTHOGRAPHIQUE DES EXPRESSIONS")
print("="*80)

# Corrections à appliquer : (français, langue, mauvaise_orthographe, bonne_orthographe)
corrections = [
    # Enlever les trémas
    ("Vendredi", "shimaore", "idjïmoi", "idjimoi"),
    ("Enceinte", "shimaore", "oumïra", "oumira"),
    ("Enceinte", "kibouchi", "ankïbou", "ankibou"),
    ("C'est acide", "kibouchi", "matsïkou", "matsikou"),
    
    # Corriger les accents
    ("C'est amer", "kibouchi", "maféki", "mafèki"),
    
    # Enlever l'apostrophe
    ("Épreuve", "shimaore", "mti'hano", "mtihano"),
]

corrections_appliquees = 0

for french, langue, mauvaise, bonne in corrections:
    # Trouver l'expression
    expr = words_collection.find_one({
        "french": french,
        "category": "expressions"
    })
    
    if expr:
        champ = langue  # "shimaore" ou "kibouchi"
        valeur_actuelle = expr.get(champ)
        
        if valeur_actuelle == mauvaise:
            # Mettre à jour avec la bonne orthographe
            words_collection.update_one(
                {"_id": expr['_id']},
                {"$set": {champ: bonne}}
            )
            print(f"✅ {french} ({langue}): '{mauvaise}' → '{bonne}'")
            corrections_appliquees += 1
        elif valeur_actuelle == bonne:
            print(f"✓  {french} ({langue}): déjà correct ('{bonne}')")
        else:
            print(f"⚠️  {french} ({langue}): valeur inattendue '{valeur_actuelle}'")
    else:
        print(f"❌ Expression '{french}' non trouvée")

print("\n" + "="*80)
print(f"RÉSULTAT: {corrections_appliquees} corrections appliquées")
print("="*80)

# Vérifier la correspondance avec les fichiers audio
print("\n" + "="*80)
print("VÉRIFICATION CORRESPONDANCE AVEC FICHIERS AUDIO")
print("="*80)

expressions_a_verifier = [
    "Vendredi", "Enceinte", "C'est amer", "C'est acide", "Épreuve"
]

for french in expressions_a_verifier:
    expr = words_collection.find_one({"french": french, "category": "expressions"})
    if expr:
        print(f"\n{french}:")
        
        # Shimaoré
        shim = expr.get('shimaore')
        audio_shim = expr.get('audio_filename_shimaore')
        if audio_shim:
            expected_base = shim.capitalize()
            actual_base = audio_shim.replace('.m4a', '')
            match = expected_base.lower() == actual_base.lower()
            print(f"  Shimaoré: {shim}")
            print(f"  Audio: {audio_shim} {'✅' if match else '❌ NON MATCH'}")
        
        # Kibouchi
        kib = expr.get('kibouchi')
        audio_kib = expr.get('audio_filename_kibouchi')
        if audio_kib:
            expected_base = kib.capitalize()
            actual_base = audio_kib.replace('.m4a', '')
            match = expected_base.lower() == actual_base.lower()
            print(f"  Kibouchi: {kib}")
            print(f"  Audio: {audio_kib} {'✅' if match else '❌ NON MATCH'}")

print("\n✅ Correction terminée")
