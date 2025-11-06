from pymongo import MongoClient
import os

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['mayotte_app']
words = db['words']

# Vérifier la structure d'un verbe
print("=== STRUCTURE ACTUELLE DE LA BASE DE DONNÉES ===\n")
verbe_example = words.find_one({"french": "Ventiler"})
if verbe_example:
    print("Exemple de structure pour 'Ventiler':")
    for key, value in verbe_example.items():
        if key != '_id':
            print(f"  {key}: {value}")

print("\n=== ORDRE DES VERBES ACTUELS (15 premiers) ===")
verbes_list = list(words.find({"category": "verbes"}).limit(15))
for i, v in enumerate(verbes_list, 1):
    print(f"{i}. {v['french']}")

print("\n=== ORDRE DES VERBES ACTUELS (15 derniers) ===")
total_verbes = words.count_documents({"category": "verbes"})
verbes_last = list(words.find({"category": "verbes"}).skip(total_verbes - 15))
for i, v in enumerate(verbes_last, total_verbes - 14):
    print(f"{i}. {v['french']}")

print(f"\n=== TOTAL: {total_verbes} verbes ===")
