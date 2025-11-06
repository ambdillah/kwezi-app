"""
Script pour ajouter les nouveaux adjectifs dans la base de données
"""

from pymongo import MongoClient
import os

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['mayotte_app']
words_collection = db['words']

print("="*80)
print("AJOUT DES NOUVEAUX ADJECTIFS")
print("="*80)

# Liste des nouveaux adjectifs avec leurs traductions et audios
nouveaux_adjectifs = [
    {
        "french": "Sent bon",
        "shimaore": "issi nouka fétré",
        "kibouchi": "magnitri",
        "emoji": "👃✨",
        "shimoare_audio_filename": "Issi nouka fétré.m4a",
        "kibouchi_audio_filename": "Magnitri.m4a"
    },
    {
        "french": "Sent mauvais",
        "shimaore": "issi nouka nayi",
        "kibouchi": "mahimbou",
        "emoji": "👃💨",
        "shimoare_audio_filename": "Issi nouka nayi.m4a",
        "kibouchi_audio_filename": "Mahimbou.m4a"
    },
    {
        "french": "Inodore",
        "shimaore": "kayna haroufou",
        "kibouchi": "tsissi haroufou",
        "emoji": "👃",
        "shimoare_audio_filename": "Kayna haroufou.m4a",
        "kibouchi_audio_filename": "Tsissi haroufou.m4a"
    },
    {
        "french": "Malade",
        "shimaore": "oukodza",
        "kibouchi": "marari",
        "emoji": "🤒",
        "shimoare_audio_filename": "Oukodza.m4a",
        "kibouchi_audio_filename": "Marari.m4a"
    },
    {
        "french": "Guéri",
        "shimaore": "ouvona",
        "kibouchi": "dzanga",
        "emoji": "😊💪",
        "shimoare_audio_filename": "Ouvona.m4a",
        "kibouchi_audio_filename": "Dzanga.m4a"
    },
    {
        "french": "Soul",
        "shimaore": "ouléwa",
        "kibouchi": "mamou",
        "emoji": "🍺",
        "shimoare_audio_filename": "Ouléwa.m4a",
        "kibouchi_audio_filename": "Mamou.m4a"
    },
    {
        "french": "Ne voit pas",
        "shimaore": "kassi ona",
        "kibouchi": "tsi mahita",
        "emoji": "👁️❌",
        "shimoare_audio_filename": "Kassi ona.m4a",
        "kibouchi_audio_filename": "Tsi mahita.m4a"
    }
]

adjectifs_ajoutes = 0
adjectifs_deja_existants = 0

for adj in nouveaux_adjectifs:
    # Vérifier si existe déjà
    existing = words_collection.find_one({
        "french": {"$regex": f"^{adj['french']}$", "$options": "i"},
        "category": "adjectifs"
    })
    
    if existing:
        print(f"⚠️  {adj['french']} existe déjà")
        adjectifs_deja_existants += 1
    else:
        # Ajouter le nouvel adjectif
        document = {
            "french": adj['french'],
            "shimaore": adj['shimaore'],
            "kibouchi": adj['kibouchi'],
            "category": "adjectifs",
            "emoji": adj['emoji'],
            "shimoare_audio_filename": adj['shimoare_audio_filename'],
            "kibouchi_audio_filename": adj['kibouchi_audio_filename'],
            "shimoare_has_audio": True,
            "kibouchi_has_audio": True,
            "has_authentic_audio": True,
            "dual_audio_system": True
        }
        
        words_collection.insert_one(document)
        adjectifs_ajoutes += 1
        print(f"✅ {adj['french']}")
        print(f"   Shimaoré: {adj['shimaore']} → {adj['shimoare_audio_filename']}")
        print(f"   Kibouchi: {adj['kibouchi']} → {adj['kibouchi_audio_filename']}")

# Statistiques finales
total_adjectifs = words_collection.count_documents({"category": "adjectifs"})
adjectifs_avec_audio = words_collection.count_documents({
    "category": "adjectifs",
    "has_authentic_audio": True
})

print("\n" + "="*80)
print("STATISTIQUES FINALES")
print("="*80)
print(f"Adjectifs ajoutés: {adjectifs_ajoutes}")
print(f"Déjà existants: {adjectifs_deja_existants}")
print(f"Total adjectifs dans la base: {total_adjectifs}")
print(f"Adjectifs avec audio authentique: {adjectifs_avec_audio} ({adjectifs_avec_audio/total_adjectifs*100:.1f}%)")
print("="*80)

print("\n✅ Ajout des adjectifs terminé!")
