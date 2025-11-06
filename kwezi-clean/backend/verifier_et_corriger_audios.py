"""
Script pour vérifier toutes les correspondances audio et corriger les incohérences
"""

from pymongo import MongoClient
import os
from pathlib import Path

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['mayotte_app']
words = db['words']

print("="*80)
print("VÉRIFICATION ET CORRECTION DES AUDIOS")
print("="*80)

# Répertoires audio
audio_root = Path("/app/frontend/assets/audio")

# Statistiques
stats = {
    'total_mots': 0,
    'avec_audio_ref': 0,
    'fichiers_trouves': 0,
    'fichiers_manquants': 0,
    'corrections': 0
}

categories = words.distinct('category')

for category in sorted(categories):
    print(f"\n### CATÉGORIE: {category.upper()} ###")
    
    mots = list(words.find({'category': category}))
    
    for word in mots:
        stats['total_mots'] += 1
        french = word['french']
        
        # Vérifier tous les champs audio possibles
        audio_fields = {
            'shimoare_audio_filename': word.get('shimoare_audio_filename'),
            'kibouchi_audio_filename': word.get('kibouchi_audio_filename'),
            'audio_filename_shimaore': word.get('audio_filename_shimaore'),
            'audio_filename_kibouchi': word.get('audio_filename_kibouchi'),
            'audio_filename': word.get('audio_filename')
        }
        
        # Filtrer les champs qui ont une valeur
        audio_fields = {k: v for k, v in audio_fields.items() if v}
        
        if not audio_fields:
            continue
            
        stats['avec_audio_ref'] += 1
        
        # Vérifier chaque fichier
        for field, filename in audio_fields.items():
            # Chercher le fichier dans plusieurs emplacements
            locations_to_check = [
                audio_root / filename,  # Racine
                audio_root / category / filename,  # Par catégorie
            ]
            
            file_found = False
            correct_path = None
            
            for location in locations_to_check:
                if location.exists():
                    file_found = True
                    correct_path = location
                    stats['fichiers_trouves'] += 1
                    break
            
            if not file_found:
                print(f"  ❌ {french}: Fichier manquant '{filename}' ({field})")
                stats['fichiers_manquants'] += 1

print("\n" + "="*80)
print("STATISTIQUES FINALES")
print("="*80)
print(f"Total mots: {stats['total_mots']}")
print(f"Mots avec référence audio: {stats['avec_audio_ref']}")
print(f"Fichiers trouvés: {stats['fichiers_trouves']}")
print(f"Fichiers manquants: {stats['fichiers_manquants']}")
print("="*80)
