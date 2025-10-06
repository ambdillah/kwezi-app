"""
Script pour mettre à jour la section verbes avec les nouveaux verbes
et leurs fichiers audio fournis par l'utilisateur.
"""

import sys
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import shutil
from pathlib import Path

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['mayotte_app']
words_collection = db['words']

# Données des nouveaux verbes extraites de l'image
nouveaux_verbes = [
    {
        "french": "Ventiler",
        "shimaore": "oupépeya",
        "kibouchi": "micoupoucoupoukou",
        "audio_shimaore": "Oupépéya.m4a",
        "audio_kibouchi": "Micoupoucoupoukou.m4a",
        "emoji": "🌬️"
    },
    {
        "french": "Couper les ongles",
        "shimaore": "oukatra kofou",
        "kibouchi": "manapaka angofou",
        "audio_shimaore": "Oukatra kofou.m4a",
        "audio_kibouchi": "Manapaka angofou.m4a",
        "emoji": "💅"
    },
    {
        "french": "Éplucher",
        "shimaore": "oukouwa",
        "kibouchi": "magnofi",
        "audio_shimaore": None,  # Pas d'audio trouvé pour shimaoré
        "audio_kibouchi": "Magnofi.m4a",
        "emoji": "🥔"
    },
    {
        "french": "Soulever",
        "shimaore": "oudzoua",
        "kibouchi": "magnoundzougou",
        "audio_shimaore": "Oudzoua.m4a",
        "audio_kibouchi": "Magnoundzougnou.m4a",
        "emoji": "🏋️"
    },
    {
        "french": "Médire",
        "shimaore": "outséman",
        "kibouchi": "mtsikou",
        "audio_shimaore": "Outséma.m4a",
        "audio_kibouchi": "Mtsikou.m4a",
        "emoji": "🗣️"
    }
]

def copier_fichiers_audio():
    """Copier les fichiers audio du dossier temporaire vers le dossier assets/audio"""
    source_dir = Path("/tmp/verbes_audio")
    dest_dir = Path("/app/frontend/assets/audio")
    
    if not dest_dir.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
    
    fichiers_copies = []
    for file in source_dir.glob("*.m4a"):
        dest_file = dest_dir / file.name
        shutil.copy2(file, dest_file)
        fichiers_copies.append(file.name)
        print(f"✅ Copié: {file.name}")
    
    return fichiers_copies

def mettre_a_jour_verbes():
    """Mettre à jour ou ajouter les verbes dans la base de données"""
    
    print("\n🔄 Mise à jour de la section verbes...\n")
    
    # Copier les fichiers audio
    print("📁 Copie des fichiers audio...")
    fichiers_copies = copier_fichiers_audio()
    print(f"✅ {len(fichiers_copies)} fichiers audio copiés\n")
    
    verbes_ajoutes = 0
    verbes_mis_a_jour = 0
    
    for verbe in nouveaux_verbes:
        french = verbe['french']
        
        # Vérifier si le verbe existe déjà
        existing = words_collection.find_one({
            "french": {"$regex": f"^{french}$", "$options": "i"},
            "category": "verbes"
        })
        
        # Préparer le document
        document = {
            "french": french,
            "shimaore": verbe['shimaore'],
            "kibouchi": verbe['kibouchi'],
            "category": "verbes",
            "emoji": verbe['emoji']
        }
        
        # Ajouter les champs audio si disponibles
        if verbe['audio_shimaore']:
            document['audio_filename_shimaore'] = verbe['audio_shimaore']
            document['has_authentic_audio'] = True
        
        if verbe['audio_kibouchi']:
            document['audio_filename_kibouchi'] = verbe['audio_kibouchi']
            document['has_authentic_audio'] = True
        
        if existing:
            # Mettre à jour le verbe existant
            words_collection.update_one(
                {"_id": existing['_id']},
                {"$set": document}
            )
            verbes_mis_a_jour += 1
            print(f"🔄 Mis à jour: {french}")
            audio_shim = f"✅ {verbe['audio_shimaore']}" if verbe['audio_shimaore'] else "❌ pas d'audio"
            audio_kib = f"✅ {verbe['audio_kibouchi']}" if verbe['audio_kibouchi'] else "❌ pas d'audio"
            print(f"   Shimaoré: {verbe['shimaore']} {audio_shim}")
            print(f"   Kibouchi: {verbe['kibouchi']} {audio_kib}")
        else:
            # Ajouter le nouveau verbe
            words_collection.insert_one(document)
        
        print()
    
    # Statistiques finales
    total_verbes = words_collection.count_documents({"category": "verbes"})
    verbes_avec_audio = words_collection.count_documents({
        "category": "verbes",
        "has_authentic_audio": True
    })
    
    print("\n" + "="*60)
    print("📊 STATISTIQUES FINALES")
    print("="*60)
    print(f"✅ Verbes ajoutés: {verbes_ajoutes}")
    print(f"🔄 Verbes mis à jour: {verbes_mis_a_jour}")
    print(f"📚 Total verbes dans la base: {total_verbes}")
    print(f"🔊 Verbes avec audio authentique: {verbes_avec_audio} ({verbes_avec_audio/total_verbes*100:.1f}%)")
    print(f"📁 Fichiers audio copiés: {len(fichiers_copies)}")
    print("="*60)

if __name__ == "__main__":
    try:
        mettre_a_jour_verbes()
        print("\n✅ Mise à jour de la section verbes terminée avec succès!")
    except Exception as e:
        print(f"\n❌ Erreur lors de la mise à jour: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
