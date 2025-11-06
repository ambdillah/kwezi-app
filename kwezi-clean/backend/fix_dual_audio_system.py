"""
Script pour ajouter le flag dual_audio_system aux verbes qui ont des audios
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['mayotte_app']
words_collection = db['words']

print("AJOUT DU FLAG dual_audio_system AUX VERBES")
print("="*80)

# Trouver tous les verbes qui ont des fichiers audio mais pas le flag dual_audio_system
verbes_to_fix = words_collection.find({
    "category": "verbes",
    "$or": [
        {"audio_filename_shimaore": {"$exists": True}},
        {"audio_filename_kibouchi": {"$exists": True}}
    ]
})

count_fixed = 0
for verbe in verbes_to_fix:
    # Ajouter le flag dual_audio_system
    words_collection.update_one(
        {"_id": verbe['_id']},
        {"$set": {"dual_audio_system": True}}
    )
    count_fixed += 1
    print(f"✅ {verbe['french']}: dual_audio_system ajouté")

print(f"\n{count_fixed} verbes mis à jour avec le flag dual_audio_system")

# Vérifier les stats finales
total_verbes = words_collection.count_documents({"category": "verbes"})
verbes_dual = words_collection.count_documents({"category": "verbes", "dual_audio_system": True})

print(f"\nStats finales:")
print(f"  Total verbes: {total_verbes}")
print(f"  Verbes avec dual_audio_system: {verbes_dual}")
