#!/usr/bin/env python3
"""
Mise à jour des références audio pour la section famille
Associe les nouveaux fichiers audio aux mots correspondants
"""

import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def connect_to_database():
    """Se connecte à la base de données MongoDB"""
    MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/mayotte_app')
    DB_NAME = os.getenv('DB_NAME', 'mayotte_app')
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
    return db.words

def normalize_filename(text):
    """Normalise un nom de fichier en supprimant les espaces et caractères spéciaux"""
    # Remplacer les espaces par des tirets et supprimer les caractères problématiques
    normalized = text.replace(' ', '-')
    normalized = normalized.replace('/', '-')
    normalized = normalized.replace('_', '-')
    return normalized

def create_audio_mappings():
    """Crée le mapping entre les mots famille et les fichiers audio"""
    
    # Mapping des traductions aux fichiers audio (basé sur les fichiers disponibles)
    audio_mappings = {
        # Pronoms et relations de base
        "mdjamaza": "Mdjamaza.m4a",              # Famille
        "baba": ["Baba k.m4a", "Baba s.m4a"],   # Papa (kibouchi/shimaoré)
        "mama": "Mama.m4a",                      # Maman
        "mwanagna": "Moinagna.m4a",              # Frère/Sœur
        "anadahi": "Anadahi.m4a",                # Frère (kibouchi)
        "anabavi": "Anabavi.m4a",                # Sœur (kibouchi)
        "havagna": "Havagna.m4a",                # Famille (kibouchi)
        
        # Grands-parents
        "bacoco": "Bacoco.m4a",                  # Grand-père (shimaoré)
        "coco": "Coco.m4a",                      # Grand-mère (shimaoré)
        "dadayi": "Dadayi.m4a",                  # Grand-père (kibouchi)
        "dadi": "Dadi.m4a",                      # Grand-mère (kibouchi)
        
        # Oncles et tantes
        "mama titi bolé": "Mama titi-bolé.m4a", # Tante maternelle (shimaoré)
        "baba titi bolé": "Baba titi-bolé.m4a", # Oncle paternel (shimaoré)
        "nindri heli bé": "Ninfndri héli-bé.m4a", # Tante maternelle (kibouchi)
        "baba heli bé": "Baba héli-bé.m4a",     # Oncle paternel (kibouchi)
        "zama": "Zama.m4a",                      # Oncle maternel
        "zena": "Zena.m4a",                      # Épouse oncle maternel
        "zéna": "Zéna.m4a",                      # Tante paternelle
        
        # Âges et genres
        "mtroubaba": "Mtroubaba.m4a",            # Garçon/Homme (shimaoré)
        "mtroumama": "Mtroumama.m4a",            # Fille/Femme (shimaoré)
        "lalahi": "Lalahi.m4a",                  # Garçon/Homme (kibouchi)
        "viavi": "Viavi.m4a",                    # Fille/Femme (kibouchi)
        
        # Petits et grands
        "moinagna mtroubaba": "Moinagna mtroubaba.m4a",   # Petit frère (shimaoré)
        "moinagna mtroumama": "Moinagna mtroumama.m4a",   # Petite sœur (shimaoré)
        "zandri lalahi": "Tseki lalahi.m4a",              # Petit frère (kibouchi) - utilise Tseki
        "zandri viavi": "Zoki viavi.m4a",                 # Petite sœur (kibouchi)
        
        "zouki mtoubaba": "Zouki mtroubaba.m4a",          # Grand frère (shimaoré)
        "zouki mtroumché": "Zouki mtroumché.m4a",         # Grande sœur (shimaoré)
        "zoki lalahi": "Zoki lalahi.m4a",                 # Grand frère (kibouchi)
        "zoki viavi": "Zoki viavi.m4a",                   # Grande sœur (kibouchi)
        
        # Jeunes
        "mwana mtroubaba": "Moina mtroubaba.m4a",         # Petit garçon (shimaoré)
        "mwana mtroumama": "Moina mtroumama.m4a",         # Petite fille (shimaoré)
        "zaza lalahi": "Zaza lalahi.m4a",                 # Petit garçon (kibouchi)
        "zaza viavi": "Zaza viavi.m4a",                   # Petite fille (kibouchi)
        "shababi": "Chababi.m4a",                         # Jeune adulte
        
        # Autres
        "mwandzani": "Mwandzani.m4a",            # Ami
        "mogné": "Mongné.m4a",                   # Monsieur
        "bvéni": "Bweni.m4a",                    # Madame
    }
    
    return audio_mappings

def update_famille_audio_references():
    """Met à jour les références audio pour tous les mots de famille"""
    collection = connect_to_database()
    audio_mappings = create_audio_mappings()
    
    print("=== MISE À JOUR DES RÉFÉRENCES AUDIO FAMILLE ===")
    
    # Obtenir tous les mots de famille
    famille_words = list(collection.find({"category": "famille"}))
    
    updates_count = 0
    
    for word in famille_words:
        shimaoré = word.get('shimaore', '').lower()
        kibouchi = word.get('kibouchi', '').lower()
        french = word.get('french', '')
        
        audio_files = []
        
        # Chercher dans les mappings shimaoré
        if shimaoré in audio_mappings:
            file_ref = audio_mappings[shimaoré]
            if isinstance(file_ref, list):
                audio_files.extend(file_ref)
            else:
                audio_files.append(file_ref)
        
        # Chercher dans les mappings kibouchi
        if kibouchi in audio_mappings and kibouchi != shimaoré:
            file_ref = audio_mappings[kibouchi]
            if isinstance(file_ref, list):
                audio_files.extend(file_ref)
            else:
                audio_files.append(file_ref)
        
        if audio_files:
            # Mettre à jour avec les nouvelles références audio
            update_data = {
                "audio_files": list(set(audio_files)),  # Supprimer les doublons
                "has_audio": True,
                "audio_updated_at": datetime.utcnow(),
                "audio_source": "famille_maj_20250925"
            }
            
            collection.update_one(
                {"_id": word["_id"]},
                {"$set": update_data}
            )
            
            print(f"✓ {french}: {', '.join(audio_files)}")
            updates_count += 1
        else:
            print(f"- {french}: Aucun audio trouvé pour '{shimaoré}' / '{kibouchi}'")
    
    return updates_count

def verify_audio_updates():
    """Vérifie que les mises à jour audio sont correctes"""
    collection = connect_to_database()
    
    print(f"\n=== VÉRIFICATION DES RÉFÉRENCES AUDIO ===")
    
    # Compter les mots avec audio
    with_audio = collection.count_documents({"category": "famille", "has_audio": True})
    total_famille = collection.count_documents({"category": "famille"})
    
    print(f"Mots avec audio: {with_audio}/{total_famille}")
    
    # Lister quelques exemples
    examples = collection.find(
        {"category": "famille", "has_audio": True}
    ).limit(10)
    
    print(f"\nExemples de mots avec audio:")
    for word in examples:
        audio_files = word.get('audio_files', [])
        print(f"  {word['french']}: {', '.join(audio_files)}")
    
    # Vérifier les nouveaux fichiers spécifiques
    test_words = [
        "Tante maternelle",
        "Oncle maternel", 
        "Petite sœur",
        "Grand frère",
        "Petit garçon"
    ]
    
    print(f"\nVérification mots clés:")
    for french_word in test_words:
        word = collection.find_one({"french": french_word, "category": "famille"})
        if word and word.get('has_audio'):
            audio_files = word.get('audio_files', [])
            print(f"✓ {french_word}: {', '.join(audio_files)}")
        else:
            print(f"✗ {french_word}: Pas d'audio")

def main():
    """Fonction principale"""
    print("=== MISE À JOUR RÉFÉRENCES AUDIO FAMILLE ===")
    print("Association des nouveaux fichiers audio MAJ\n")
    
    try:
        # Mettre à jour les références audio
        updates_count = update_famille_audio_references()
        
        print(f"\n✅ MISE À JOUR AUDIO TERMINÉE:")
        print(f"  - {updates_count} mots mis à jour avec références audio")
        
        # Vérification
        verify_audio_updates()
        
        print(f"\n🎉 AUDIO FAMILLE MIS À JOUR AVEC SUCCÈS !")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        raise

if __name__ == "__main__":
    main()