"""
Script pour corriger l'orthographe du verbe Médire en shimaoré
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['mayotte_app']
words_collection = db['words']

print("CORRECTION ORTHOGRAPHIQUE - VERBE MÉDIRE")
print("="*80)

# Trouver le verbe Médire
verbe = words_collection.find_one({"french": "Médire", "category": "verbes"})

if verbe:
    print(f"\n✅ Verbe trouvé: {verbe['french']}")
    print(f"   Shimaoré actuel: {verbe.get('shimaore', 'N/A')}")
    print(f"   Audio shimaoré actuel: {verbe.get('audio_filename_shimaore', 'N/A')}")
    
    # Mettre à jour l'orthographe
    result = words_collection.update_one(
        {"_id": verbe['_id']},
        {"$set": {
            "shimaore": "outséma",
            "audio_filename_shimaore": "Outséma.m4a"
        }}
    )
    
    if result.modified_count > 0:
        print("\n✅ CORRECTION EFFECTUÉE")
        
        # Vérifier la mise à jour
        verbe_updated = words_collection.find_one({"_id": verbe['_id']})
        print(f"\n   Nouveau shimaoré: {verbe_updated['shimaore']}")
        print(f"   Nouveau audio shimaoré: {verbe_updated['audio_filename_shimaore']}")
        
        # Vérifier que le fichier audio existe
        audio_path = f"/app/frontend/assets/audio/{verbe_updated['audio_filename_shimaore']}"
        if os.path.exists(audio_path):
            print(f"\n✅ Fichier audio trouvé: {audio_path}")
            size = os.path.getsize(audio_path)
            print(f"   Taille: {size/1024:.1f} KB")
        else:
            print(f"\n❌ ATTENTION: Fichier audio non trouvé: {audio_path}")
    else:
        print("\n⚠️ Aucune modification effectuée (les valeurs étaient déjà correctes)")
else:
    print("\n❌ ERREUR: Verbe 'Médire' non trouvé dans la base de données")

print("\n" + "="*80)
print("Correction terminée")
