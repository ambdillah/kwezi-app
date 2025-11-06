"""
Script pour mettre à jour les audios manquants et supprimer le doublon "montre moi"
"""

from pymongo import MongoClient
import os
import shutil
from pathlib import Path

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['mayotte_app']
words_collection = db['words']

print("="*80)
print("MISE À JOUR AUDIOS EXPRESSIONS + SUPPRESSION DOUBLON")
print("="*80)

# 1. Copier les fichiers audio
print("\n📁 Copie des fichiers audio...")
audio_files = {
    'Mwézi.m4a': '/tmp/Mwézi.m4a',
    'Fandzava.m4a': '/tmp/Fandzava.m4a',
    'Karibou.m4a': '/tmp/Karibou.m4a',
    'Lavitri.m4a': '/tmp/Lavitri.m4a'
}

dest_dir = Path("/app/frontend/assets/audio")
dest_dir.mkdir(parents=True, exist_ok=True)

for filename, source_path in audio_files.items():
    if os.path.exists(source_path):
        dest_path = dest_dir / filename
        shutil.copy2(source_path, dest_path)
        print(f"  ✅ Copié: {filename}")
    else:
        print(f"  ❌ Fichier source non trouvé: {filename}")

# 2. Mettre à jour "Mois" avec les deux audios
print("\n🔄 Mise à jour: Mois")
result = words_collection.update_one(
    {"french": "Mois", "category": "expressions"},
    {"$set": {
        "audio_filename_shimaore": "Mwézi.m4a",
        "audio_filename_kibouchi": "Fandzava.m4a",
        "has_authentic_audio": True,
        "dual_audio_system": True
    }}
)
if result.modified_count > 0:
    print("  ✅ Mois mis à jour avec Mwézi.m4a et Fandzava.m4a")
else:
    print("  ⚠️ Aucune modification (déjà à jour?)")

# 3. Mettre à jour "Tout prêt" avec audio shimaoré
print("\n🔄 Mise à jour: Tout prêt")
result = words_collection.update_one(
    {"french": "Tout prêt", "category": "expressions"},
    {"$set": {
        "audio_filename_shimaore": "Karibou.m4a",
        "has_authentic_audio": True,
        "dual_audio_system": True
    }}
)
if result.modified_count > 0:
    print("  ✅ Tout prêt mis à jour avec Karibou.m4a (shimaoré)")
else:
    print("  ⚠️ Aucune modification")

# 4. Mettre à jour "Loin" avec audio kibouchi
print("\n🔄 Mise à jour: Loin")
result = words_collection.update_one(
    {"french": "Loin", "category": "expressions"},
    {"$set": {
        "audio_filename_kibouchi": "Lavitri.m4a",
        "has_authentic_audio": True,
        "dual_audio_system": True
    }}
)
if result.modified_count > 0:
    print("  ✅ Loin mis à jour avec Lavitri.m4a (kibouchi)")
else:
    print("  ⚠️ Aucune modification")

# 5. Supprimer le doublon "montre moi" (minuscules, ID: 68dcebe2f013000b31f8528c)
print("\n🗑️  Suppression du doublon 'montre moi'")
from bson import ObjectId

# Garder "Montre-moi" (avec majuscule et tiret) et supprimer "montre moi"
doublon_id = ObjectId("68dcebe2f013000b31f8528c")
result = words_collection.delete_one({"_id": doublon_id})

if result.deleted_count > 0:
    print("  ✅ Doublon 'montre moi' supprimé (ID: 68dcebe2f013000b31f8528c)")
else:
    print("  ⚠️ Doublon déjà supprimé ou introuvable")

# 6. Statistiques finales
print("\n" + "="*80)
print("📊 STATISTIQUES FINALES")
print("="*80)

total_expressions = words_collection.count_documents({"category": "expressions"})
expressions_avec_audio = words_collection.count_documents({
    "category": "expressions",
    "has_authentic_audio": True
})

print(f"Total expressions: {total_expressions}")
print(f"Expressions avec audio authentique: {expressions_avec_audio} ({expressions_avec_audio/total_expressions*100:.1f}%)")
print("="*80)

print("\n✅ Mise à jour terminée!")
