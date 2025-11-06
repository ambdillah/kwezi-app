from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['mayotte_app']
words_collection = db['words']

# Vérifier les 5 nouveaux verbes
nouveaux_verbes = ["Ventiler", "Couper les ongles", "Éplucher", "Soulever", "Médire"]

print("VERIFICATION DES NOUVEAUX VERBES")
print("="*80)

for verbe in nouveaux_verbes:
    word = words_collection.find_one({"french": verbe, "category": "verbes"})
    
    if word:
        print(f"\n{verbe}")
        print(f"  Shimaore: {word.get('shimaore', 'N/A')}")
        print(f"  Kibouchi: {word.get('kibouchi', 'N/A')}")
        print(f"  Audio Shimaore: {word.get('audio_filename_shimaore', 'NON DEFINI')}")
        print(f"  Audio Kibouchi: {word.get('audio_filename_kibouchi', 'NON DEFINI')}")
        print(f"  has_authentic_audio: {word.get('has_authentic_audio', False)}")
        print(f"  Emoji: {word.get('emoji', 'NON DEFINI')}")
    else:
        print(f"\nERREUR: {verbe} - NON TROUVE dans la base")

print("\n" + "="*80)
print(f"Total verbes: {words_collection.count_documents({'category': 'verbes'})}")
print(f"Verbes avec audio: {words_collection.count_documents({'category': 'verbes', 'has_authentic_audio': True})}")