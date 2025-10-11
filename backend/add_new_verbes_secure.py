"""
Script SÉCURISÉ pour ajouter les nouveaux verbes
Avec vérifications multiples pour éviter toute erreur
"""

from pymongo import MongoClient
import os

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['mayotte_app']
words_collection = db['words']

print("="*80)
print("AJOUT SÉCURISÉ DES NOUVEAUX VERBES")
print("="*80)

# Liste des 4 nouveaux verbes avec TOUTES les informations
nouveaux_verbes = [
    {
        "french": "Entérer",
        "shimaore": "oudziha",
        "kibouchi": "mandévigni",
        "emoji": "⚰️",
        "audio_filename_shimaore": "Oudziha.m4a",
        "audio_filename_kibouchi": "Mandévigni.m4a"
    },
    {
        "french": "Masser",
        "shimaore": "ouhandra",
        "kibouchi": "manéritéri",
        "emoji": "💆",
        "audio_filename_shimaore": "Ouhandra.m4a",
        "audio_filename_kibouchi": "Manéritéri.m4a"
    },
    {
        "french": "Pêcher",
        "shimaore": "oulowa",
        "kibouchi": "mamintagna",
        "emoji": "🎣",
        "audio_filename_shimaore": "Oulowa.m4a",
        "audio_filename_kibouchi": "Mamintagna.m4a"
    },
    {
        "french": "Voyager",
        "shimaore": "oupachiya",
        "kibouchi": "mihondragna",
        "emoji": "✈️",
        "audio_filename_shimaore": "Oupachiya.m4a",
        "audio_filename_kibouchi": "Mihondragna.m4a"
    }
]

verbes_ajoutes = 0
verbes_deja_existants = 0
erreurs = []

for verbe in nouveaux_verbes:
    print(f"\n--- Traitement: {verbe['french']} ---")
    
    # VÉRIFICATION 1: Le verbe existe-t-il déjà?
    existing = words_collection.find_one({
        "french": {"$regex": f"^{verbe['french']}$", "$options": "i"},
        "category": "verbes"
    })
    
    if existing:
        print(f"⚠️  EXISTE DÉJÀ (ignoré pour sécurité)")
        verbes_deja_existants += 1
        continue
    
    # VÉRIFICATION 2: Les fichiers audio existent-ils?
    audio_shim_path = f"/app/frontend/assets/audio/{verbe['audio_filename_shimaore']}"
    audio_kib_path = f"/app/frontend/assets/audio/{verbe['audio_filename_kibouchi']}"
    
    if not os.path.exists(audio_shim_path):
        erreur = f"❌ Fichier shimaoré manquant: {verbe['audio_filename_shimaore']}"
        print(erreur)
        erreurs.append(erreur)
        continue
    
    if not os.path.exists(audio_kib_path):
        erreur = f"❌ Fichier kibouchi manquant: {verbe['audio_filename_kibouchi']}"
        print(erreur)
        erreurs.append(erreur)
        continue
    
    print(f"✓ Fichiers audio vérifiés présents")
    
    # AJOUT du verbe
    document = {
        "french": verbe['french'],
        "shimaore": verbe['shimaore'],
        "kibouchi": verbe['kibouchi'],
        "category": "verbes",
        "emoji": verbe['emoji'],
        "audio_filename_shimaore": verbe['audio_filename_shimaore'],
        "audio_filename_kibouchi": verbe['audio_filename_kibouchi'],
        "has_authentic_audio": True,
        "dual_audio_system": True
    }
    
    try:
        result = words_collection.insert_one(document)
        verbes_ajoutes += 1
        print(f"✅ AJOUTÉ avec succès (ID: {result.inserted_id})")
        print(f"   Shimaoré: {verbe['shimaore']} → {verbe['audio_filename_shimaore']}")
        print(f"   Kibouchi: {verbe['kibouchi']} → {verbe['audio_filename_kibouchi']}")
    except Exception as e:
        erreur = f"❌ Erreur lors de l'ajout: {e}"
        print(erreur)
        erreurs.append(erreur)

# Statistiques finales
total_verbes = words_collection.count_documents({"category": "verbes"})

print("\n" + "="*80)
print("RÉSULTATS FINAUX")
print("="*80)
print(f"✅ Verbes ajoutés: {verbes_ajoutes}")
print(f"⚠️  Déjà existants: {verbes_deja_existants}")
print(f"❌ Erreurs: {len(erreurs)}")
print(f"📚 Total verbes dans la base: {total_verbes}")
print("="*80)

if erreurs:
    print("\n⚠️  ERREURS DÉTECTÉES:")
    for err in erreurs:
        print(f"  {err}")
else:
    print("\n✅ AUCUNE ERREUR - Tout s'est bien passé!")
