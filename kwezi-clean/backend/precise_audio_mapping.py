#!/usr/bin/env python3
"""
MAPPING PRÉCIS DES FICHIERS AUDIO SELON LES ZIP FOURNIS
=======================================================
Ce script analyse minutieusement chaque fichier audio et le mappe
à la traduction correspondante dans la base de données.
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
import glob
from datetime import datetime
import shutil

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URL)
db = client['shimaoré_app']

print("🔍 MAPPING PRÉCIS DES FICHIERS AUDIO")
print("=" * 60)

# Créer les répertoires de destination pour les fichiers audio
audio_destination = "/app/frontend/assets/audio"
os.makedirs(f"{audio_destination}/animaux", exist_ok=True)
os.makedirs(f"{audio_destination}/adjectifs", exist_ok=True)

# Fonction de nettoyage des noms de fichiers
def clean_filename(filename):
    """Nettoie le nom de fichier pour le mapping"""
    return filename.replace('.m4a', '').replace('(1)', '').replace('_', ' ').strip()

def normalize_text(text):
    """Normalise le texte pour la comparaison"""
    return text.lower().replace("'", "'").replace("'", "'").strip()

# ===============================
# PHASE 1: TRAITEMENT DES ANIMAUX
# ===============================
print("\n1. 🐾 TRAITEMENT DES ANIMAUX")
print("-" * 40)

# Lister tous les fichiers audio animaux
animaux_files = glob.glob("/app/backend/audio_mapping_work/animaux_extracted/Animaux_/*.m4a")
print(f"   📁 {len(animaux_files)} fichiers audio trouvés")

# Récupérer tous les animaux de la base
animaux_db = list(db.vocabulary.find({"section": "animaux"}))
print(f"   🗄️  {len(animaux_db)} animaux dans la base de données")

matched_count = 0
unmatched_files = []
updated_animals = []

for audio_file in animaux_files:
    filename = os.path.basename(audio_file)
    clean_name = clean_filename(filename)
    
    # Chercher une correspondance dans la base de données
    matched = False
    
    # Essayer de matcher avec shimaoré
    for animal in animaux_db:
        shimaoré = normalize_text(animal.get('shimaoré', ''))
        kibouchi = normalize_text(animal.get('kibouchi', ''))
        french = normalize_text(animal.get('french', ''))
        clean_audio_name = normalize_text(clean_name)
        
        if (clean_audio_name == shimaoré or 
            clean_audio_name == kibouchi or
            shimaoré in clean_audio_name or 
            kibouchi in clean_audio_name or
            clean_audio_name in shimaoré or 
            clean_audio_name in kibouchi):
            
            # COPIER le fichier vers la destination
            dest_file = f"{audio_destination}/animaux/{filename}"
            shutil.copy2(audio_file, dest_file)
            
            # Déterminer si c'est shimaoré ou kibouchi
            audio_field = ""
            if clean_audio_name == shimaoré or shimaoré in clean_audio_name or clean_audio_name in shimaoré:
                audio_field = "shimaoré_audio"
            elif clean_audio_name == kibouchi or kibouchi in clean_audio_name or clean_audio_name in kibouchi:
                audio_field = "kibouchi_audio"
            else:
                # Si incertain, utiliser shimaoré par défaut
                audio_field = "shimaoré_audio"
            
            # Mettre à jour la base de données
            db.vocabulary.update_one(
                {"_id": animal["_id"]},
                {
                    "$set": {
                        audio_field: filename,
                        "has_authentic_audio": True,
                        "audio_updated": True,
                        "audio_source": "user_provided_zip"
                    }
                }
            )
            
            updated_animals.append({
                "french": animal['french'],
                "shimaoré": animal['shimaoré'],
                "kibouchi": animal['kibouchi'],
                "audio_file": filename,
                "audio_field": audio_field,
                "match_reason": f"{clean_audio_name} → {audio_field}"
            })
            
            matched_count += 1
            matched = True
            print(f"   ✅ {animal['french']:20} → {filename:30} ({audio_field})")
            break
    
    if not matched:
        unmatched_files.append((filename, clean_name))
        print(f"   ❌ Non mappé: {filename} ({clean_name})")

print(f"\n   📊 Résultat animaux: {matched_count}/{len(animaux_files)} fichiers mappés")

# ===============================
# PHASE 2: TRAITEMENT DES ADJECTIFS
# ===============================
print("\n2. 📝 TRAITEMENT DES ADJECTIFS")
print("-" * 40)

# Lister tous les fichiers audio adjectifs
adjectifs_files = glob.glob("/app/backend/audio_mapping_work/adjectifs_extracted/adjectifs_/*.m4a")
print(f"   📁 {len(adjectifs_files)} fichiers audio trouvés")

# Récupérer tous les adjectifs de la base
adjectifs_db = list(db.vocabulary.find({"section": "adjectifs"}))
print(f"   🗄️  {len(adjectifs_db)} adjectifs dans la base de données")

matched_adj_count = 0
unmatched_adj_files = []
updated_adjectives = []

for audio_file in adjectifs_files:
    filename = os.path.basename(audio_file)
    clean_name = clean_filename(filename)
    
    # Chercher une correspondance dans la base de données
    matched = False
    
    for adjectif in adjectifs_db:
        shimaoré = normalize_text(adjectif.get('shimaoré', ''))
        kibouchi = normalize_text(adjectif.get('kibouchi', ''))
        french = normalize_text(adjectif.get('french', ''))
        clean_audio_name = normalize_text(clean_name)
        
        if (clean_audio_name == shimaoré or 
            clean_audio_name == kibouchi or
            shimaoré in clean_audio_name or 
            kibouchi in clean_audio_name or
            clean_audio_name in shimaoré or 
            clean_audio_name in kibouchi):
            
            # COPIER le fichier vers la destination
            dest_file = f"{audio_destination}/adjectifs/{filename}"
            shutil.copy2(audio_file, dest_file)
            
            # Déterminer si c'est shimaoré ou kibouchi
            audio_field = ""
            if clean_audio_name == shimaoré or shimaoré in clean_audio_name or clean_audio_name in shimaoré:
                audio_field = "shimaoré_audio"
            elif clean_audio_name == kibouchi or kibouchi in clean_audio_name or clean_audio_name in kibouchi:
                audio_field = "kibouchi_audio"
            else:
                # Si incertain, utiliser shimaoré par défaut
                audio_field = "shimaoré_audio"
            
            # Mettre à jour la base de données
            db.vocabulary.update_one(
                {"_id": adjectif["_id"]},
                {
                    "$set": {
                        audio_field: filename,
                        "has_authentic_audio": True,
                        "audio_updated": True,
                        "audio_source": "user_provided_zip"
                    }
                }
            )
            
            updated_adjectives.append({
                "french": adjectif['french'],
                "shimaoré": adjectif['shimaoré'],
                "kibouchi": adjectif['kibouchi'],
                "audio_file": filename,
                "audio_field": audio_field,
                "match_reason": f"{clean_audio_name} → {audio_field}"
            })
            
            matched_adj_count += 1
            matched = True
            print(f"   ✅ {adjectif['french']:20} → {filename:35} ({audio_field})")
            break
    
    if not matched:
        unmatched_adj_files.append((filename, clean_name))
        print(f"   ❌ Non mappé: {filename} ({clean_name})")

print(f"\n   📊 Résultat adjectifs: {matched_adj_count}/{len(adjectifs_files)} fichiers mappés")

# ===============================
# PHASE 3: RAPPORT FINAL
# ===============================
print("\n" + "=" * 60)
print("📋 RAPPORT FINAL DU MAPPING")
print("=" * 60)

print(f"\n✅ SUCCÈS:")
print(f"   🐾 Animaux: {matched_count}/{len(animaux_files)} fichiers mappés")
print(f"   📝 Adjectifs: {matched_adj_count}/{len(adjectifs_files)} fichiers mappés")
print(f"   🎯 Total: {matched_count + matched_adj_count}/{len(animaux_files) + len(adjectifs_files)} fichiers traités")

if unmatched_files or unmatched_adj_files:
    print(f"\n⚠️ FICHIERS NON MAPPÉS:")
    if unmatched_files:
        print(f"   🐾 Animaux non mappés:")
        for filename, clean_name in unmatched_files[:10]:  # Limiter l'affichage
            print(f"      - {filename}")
    
    if unmatched_adj_files:
        print(f"   📝 Adjectifs non mappés:")
        for filename, clean_name in unmatched_adj_files[:10]:
            print(f"      - {filename}")

print(f"\n🎉 MAPPING TERMINÉ!")
print(f"   Fichiers copiés vers: {audio_destination}")
print(f"   Base de données mise à jour avec les liens audio")

# Vérification finale
total_with_audio = db.vocabulary.count_documents({
    "$or": [
        {"shimaoré_audio": {"$exists": True}},
        {"kibouchi_audio": {"$exists": True}}
    ]
})
print(f"\n📊 Vérification: {total_with_audio} mots ont maintenant des fichiers audio")