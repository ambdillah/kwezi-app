#!/usr/bin/env python3
"""
Script pour intégrer les prononciations audio de la section famille
depuis le Google Drive partagé dans la base de données.
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
import re

# Ajouter le chemin du backend au PYTHONPATH
sys.path.append('/app/backend')

# Charger les variables d'environnement
load_dotenv()

from database_protection import DatabaseProtector

def create_download_url(drive_url):
    """Convertit une URL Google Drive en URL de téléchargement direct."""
    # Extraire l'ID du fichier depuis l'URL Google Drive
    match = re.search(r'/file/d/([a-zA-Z0-9-_]+)', drive_url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return None

def integrate_famille_audio():
    """Intègre les fichiers audio de famille dans la base de données."""
    
    # Correspondances entre fichiers audio et mots français
    audio_mappings = {
        "Anabavi.m4a": {"french": "sœur", "pronunciation_lang": "kibouchi"},
        "Anadahi.m4a": {"french": "frère", "pronunciation_lang": "kibouchi"},
        "Baba héli-bé.m4a": {"french": "oncle paternel", "pronunciation_lang": "kibouchi"},
        "Baba k.m4a": {"french": "papa", "pronunciation_lang": "kibouchi", "note": "version courte"},
        "Baba s.m4a": {"french": "papa", "pronunciation_lang": "shimaore", "note": "version courte"},
        "Baba titi-bolé.m4a": {"french": "oncle paternel", "pronunciation_lang": "shimaore"},
        "Bacoco.m4a": {"french": "grand-père", "pronunciation_lang": "shimaore"},
        "Bweni.m4a": {"french": "madame", "pronunciation_lang": "shimaore"},
        "Coco.m4a": {"french": "grand-mère", "pronunciation_lang": "shimaore"},
        "Dadayi.m4a": {"french": "grand-père", "pronunciation_lang": "kibouchi"},
        "Dadi.m4a": {"french": "grand-mère", "pronunciation_lang": "kibouchi"},
        "Havagna.m4a": {"french": "famille", "pronunciation_lang": "kibouchi"},
        "Lalahi.m4a": {"french": "homme", "pronunciation_lang": "kibouchi"},
        "Mama titi-bolé.m4a": {"french": "tente", "pronunciation_lang": "shimaore"},
        "Mama.m4a": {"french": "maman", "pronunciation_lang": "both"},
        "Mdjamaza.m4a": {"french": "famille", "pronunciation_lang": "shimaore"},
        "Moina boueni.m4a": {"french": "petite sœur", "pronunciation_lang": "shimaore", "note": "variante"},
        "Moina.m4a": {"french": "petit", "pronunciation_lang": "shimaore", "note": "adjectif"},
        "Moinagna mtroubaba.m4a": {"french": "petit frère", "pronunciation_lang": "shimaore"},
        "Moinagna mtroumama.m4a": {"french": "petite sœur", "pronunciation_lang": "shimaore"},
        "Mongné.m4a": {"french": "monsieur", "pronunciation_lang": "shimaore"},
        "Mtroubaba.m4a": {"french": "garçon", "pronunciation_lang": "shimaore"},
        "Mtroumama.m4a": {"french": "fille", "pronunciation_lang": "shimaore"},
        "Mwanagna.m4a": {"french": "enfant", "pronunciation_lang": "shimaore", "note": "générique"},
        "Mwandzani.m4a": {"french": "ami", "pronunciation_lang": "both"},
        "Ninfndri héli-bé.m4a": {"french": "tente", "pronunciation_lang": "kibouchi"},
        "Tseki lalahi.m4a": {"french": "grand frère", "pronunciation_lang": "kibouchi", "note": "variante"},
        "Viavi.m4a": {"french": "femme", "pronunciation_lang": "kibouchi"},
        "Zama.m4a": {"french": "oncle maternel", "pronunciation_lang": "both"},
        "Zena.m4a": {"french": "épouse oncle maternel", "pronunciation_lang": "both"},
        "Zoki lalahi.m4a": {"french": "grand frère", "pronunciation_lang": "kibouchi"},
        "Zoki viavi.m4a": {"french": "grande sœur", "pronunciation_lang": "kibouchi"},
        "Zouki mtroubaba.m4a": {"french": "grand frère", "pronunciation_lang": "shimaore"},
        "Zouki mtroumché.m4a": {"french": "grande sœur", "pronunciation_lang": "shimaore"},
        "Zouki.m4a": {"french": "grand", "pronunciation_lang": "shimaore", "note": "adjectif"}
    }
    
    try:
        # Connexion à MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.words
        
        # Initialiser la protection de base de données
        db_protection = DatabaseProtector()
        
        print(f"🔗 Connexion à MongoDB: {mongo_url}")
        print(f"📊 Base de données: {db_name}")
        print(f"🎵 Fichiers audio à intégrer: {len(audio_mappings)}")
        print()
        
        # Créer une sauvegarde avant modification
        print("💾 Création d'une sauvegarde avant modification...")
        backup_path = db_protection.create_backup("before_integrate_famille_audio")
        if backup_path:
            print("✅ Sauvegarde créée avec succès")
        else:
            print("⚠️ Échec de la sauvegarde")
        print()
        
        # Créer le répertoire pour les fichiers audio
        audio_dir = "/app/frontend/assets/audio/famille"
        os.makedirs(audio_dir, exist_ok=True)
        print(f"📁 Répertoire audio créé: {audio_dir}")
        print()
        
        # Traiter chaque fichier audio
        mises_a_jour = 0
        fichiers_telecharges = 0
        
        for filename, mapping in audio_mappings.items():
            french_word = mapping["french"]
            pronunciation_lang = mapping["pronunciation_lang"]
            note = mapping.get("note", "")
            
            print(f"🎵 Traitement de {filename} pour '{french_word}'...")
            
            # Rechercher le mot dans la base de données
            existing_word = collection.find_one({
                "french": {"$regex": f"^{french_word}$", "$options": "i"},
                "category": "famille"
            })
            
            if existing_word:
                print(f"   ✅ Mot trouvé: {french_word}")
                
                # URL de téléchargement Google Drive
                # Pour l'instant, nous allons juste stocker les métadonnées
                # Le téléchargement réel nécessiterait des URLs directes
                
                # Construire le chemin audio local
                audio_path = f"/assets/audio/famille/{filename}"
                
                # Mettre à jour avec les informations audio
                update_data = {
                    "audio_url": audio_path,
                    "audio_filename": filename,
                    "audio_pronunciation_lang": pronunciation_lang,
                    "audio_note": note,
                    "audio_updated_at": datetime.now(),
                    "audio_source": "google_drive_famille",
                    "has_authentic_audio": True
                }
                
                result = collection.update_one(
                    {"_id": existing_word["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    mises_a_jour += 1
                    print(f"   ✅ Métadonnées audio mises à jour")
                    print(f"      Langue: {pronunciation_lang}")
                    if note:
                        print(f"      Note: {note}")
                else:
                    print(f"   ⚠️ Aucune modification effectuée")
                    
            else:
                print(f"   ❌ Mot '{french_word}' non trouvé dans la catégorie famille")
            
            print()
        
        # Statistiques finales
        print("=" * 60)
        print(f"📈 RÉSUMÉ DE L'INTÉGRATION AUDIO")
        print(f"🎵 Fichiers audio traités: {len(audio_mappings)}")
        print(f"📝 Mots mis à jour: {mises_a_jour}")
        print(f"📁 Fichiers téléchargés: {fichiers_telecharges}")
        print()
        
        # Instructions pour finaliser l'intégration
        print("📋 PROCHAINES ÉTAPES POUR FINALISER :")
        print("1. Les métadonnées audio ont été ajoutées à la base de données")
        print("2. Pour télécharger les fichiers réels, vous devrez :")
        print("   - Télécharger manuellement chaque fichier depuis Google Drive")
        print(f"   - Les placer dans le répertoire: {audio_dir}")
        print("   - Ou utiliser l'API Google Drive avec authentification")
        print()
        
        print("✅ Intégration des métadonnées audio terminée avec succès!")
        
        # Fermer la connexion
        client.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'intégration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def list_famille_words_with_audio():
    """Liste tous les mots de famille avec leurs informations audio."""
    try:
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.words
        
        print("📋 MOTS DE FAMILLE AVEC AUDIO INTÉGRÉ :")
        print("=" * 60)
        
        famille_words = collection.find({"category": "famille", "has_authentic_audio": True})
        
        for word in famille_words:
            french = word.get('french', 'N/A')
            audio_filename = word.get('audio_filename', 'N/A')
            audio_lang = word.get('audio_pronunciation_lang', 'N/A')
            audio_note = word.get('audio_note', '')
            
            print(f"🎵 {french}:")
            print(f"   Fichier: {audio_filename}")
            print(f"   Langue: {audio_lang}")
            if audio_note:
                print(f"   Note: {audio_note}")
            print()
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    print("🚀 Début de l'intégration des prononciations famille...")
    print("🎵 Source: Google Drive - Famille")
    print()
    
    success = integrate_famille_audio()
    
    if success:
        print("🎉 Intégration terminée avec succès!")
        print()
        list_famille_words_with_audio()
    else:
        print("💥 Échec de l'intégration")
        sys.exit(1)