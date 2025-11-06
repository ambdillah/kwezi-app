"""
Script pour ajouter les 4 nouveaux mots de matériaux dans la section nature
"""

from pymongo import MongoClient
import os

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['mayotte_app']
words_collection = db['words']

print("="*80)
print("AJOUT DES NOUVEAUX MOTS - MATÉRIAUX (NATURE)")
print("="*80)

# Liste des nouveaux mots avec leurs traductions et audios
nouveaux_mots = [
    {
        "french": "Métal",
        "shimaore": "chouma",
        "kibouchi": "vi",
        "emoji": "🔩",
        "shimoare_audio_filename": "Chouma.m4a",
        "kibouchi_audio_filename": "Vi.m4a"
    },
    {
        "french": "Aluminium",
        "shimaore": "bhati",
        "kibouchi": "bhati",
        "emoji": "🥫",
        "shimoare_audio_filename": "Bhati.m4a",
        "kibouchi_audio_filename": "Bhati.m4a"
    },
    {
        "french": "Verre",
        "shimaore": "véra",
        "kibouchi": "vèra",
        "emoji": "🍷",
        "shimoare_audio_filename": "Véra.m4a",
        "kibouchi_audio_filename": "Vèra.m4a"
    },
    {
        "french": "Plastique",
        "shimaore": "mpira",
        "kibouchi": "ampira",
        "emoji": "♻️",
        "shimoare_audio_filename": "Mpira.m4a",
        "kibouchi_audio_filename": "Ampira.m4a"
    }
]

mots_ajoutes = 0
mots_deja_existants = 0

for mot in nouveaux_mots:
    # Vérifier si existe déjà
    existing = words_collection.find_one({
        "french": {"$regex": f"^{mot['french']}$", "$options": "i"},
        "category": "nature"
    })
    
    if existing:
        print(f"⚠️  {mot['french']} existe déjà")
        mots_deja_existants += 1
    else:
        # Ajouter le nouveau mot
        document = {
            "french": mot['french'],
            "shimaore": mot['shimaore'],
            "kibouchi": mot['kibouchi'],
            "category": "nature",
            "emoji": mot['emoji'],
            "shimoare_audio_filename": mot['shimoare_audio_filename'],
            "kibouchi_audio_filename": mot['kibouchi_audio_filename'],
            "shimoare_has_audio": True,
            "kibouchi_has_audio": True,
            "has_authentic_audio": True,
            "dual_audio_system": True
        }
        
        words_collection.insert_one(document)
        mots_ajoutes += 1
        print(f"✅ {mot['french']}")
        print(f"   Shimaoré: {mot['shimaore']} → {mot['shimoare_audio_filename']}")
        print(f"   Kibouchi: {mot['kibouchi']} → {mot['kibouchi_audio_filename']}")

# Statistiques finales
total_nature = words_collection.count_documents({"category": "nature"})
nature_avec_audio = words_collection.count_documents({
    "category": "nature",
    "has_authentic_audio": True
})

print("\n" + "="*80)
print("STATISTIQUES FINALES")
print("="*80)
print(f"Mots ajoutés: {mots_ajoutes}")
print(f"Déjà existants: {mots_deja_existants}")
print(f"Total mots nature: {total_nature}")
print(f"Avec audio authentique: {nature_avec_audio} ({nature_avec_audio/total_nature*100:.1f}%)")
print("="*80)

print("\n✅ Ajout des mots nature terminé!")
