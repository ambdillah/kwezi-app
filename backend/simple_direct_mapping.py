#!/usr/bin/env python3
"""
Script pour faire un mapping DIRECT et SIMPLE entre fichiers audio et mots
Pas de complexité - juste correspondance orthographique directe
"""

import os
import sys
import requests
import zipfile
import tempfile
import shutil
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# Ajouter le chemin du backend au PYTHONPATH
sys.path.append('/app/backend')

# Charger les variables d'environnement
load_dotenv()

def extract_new_famille_zip():
    """Extrait le nouveau ZIP famille."""
    
    zip_url = "https://customer-assets.emergentagent.com/job_shimaware/artifacts/793ea1d3_Famille-20250922T102326Z-1-001.zip"
    destination_dir = "/app/frontend/assets/audio/famille"
    
    # Sauvegarder l'ancien répertoire si il existe
    if os.path.exists(destination_dir):
        backup_dir = f"{destination_dir}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.move(destination_dir, backup_dir)
        print(f"📁 Ancien répertoire sauvegardé: {backup_dir}")
    
    # Créer le nouveau répertoire
    os.makedirs(destination_dir, exist_ok=True)
    print(f"📁 Nouveau répertoire créé: {destination_dir}")
    
    try:
        print("📥 Téléchargement du nouveau ZIP famille...")
        response = requests.get(zip_url, stream=True)
        
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        temp_zip.write(chunk)
                temp_zip_path = temp_zip.name
            
            # Extraire
            extracted_files = []
            with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                for file_path in zip_ref.namelist():
                    filename = os.path.basename(file_path)
                    if filename.endswith('.m4a') and filename != '':
                        with zip_ref.open(file_path) as source:
                            target_path = os.path.join(destination_dir, filename)
                            with open(target_path, 'wb') as target:
                                shutil.copyfileobj(source, target)
                        extracted_files.append(filename)
            
            os.unlink(temp_zip_path)
            return sorted(extracted_files)
            
        else:
            print(f"❌ Échec téléchargement: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Erreur extraction: {str(e)}")
        return []

def direct_audio_mapping():
    """Fait un mapping DIRECT entre fichiers audio et mots de la base."""
    
    try:
        # Extraire le nouveau ZIP
        print("🚀 MAPPING DIRECT AUDIO FAMILLE")
        print("=" * 50)
        print("Approche: Correspondance orthographique directe")
        print()
        
        extracted_files = extract_new_famille_zip()
        if not extracted_files:
            print("❌ Aucun fichier extrait")
            return False
        
        print(f"📂 {len(extracted_files)} fichiers audio extraits:")
        for filename in extracted_files:
            print(f"   - {filename}")
        print()
        
        # Connexion base de données
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.words
        
        # Récupérer TOUS les mots de toutes les catégories
        all_words = list(collection.find({}))
        print(f"📊 {len(all_words)} mots dans la base de données")
        print()
        
        # ÉTAPE 1: Reset - supprimer tous les anciens mappings audio
        print("🧹 RESET: Suppression des anciens mappings audio...")
        reset_result = collection.update_many(
            {},
            {"$unset": {
                "has_authentic_audio": "",
                "audio_filename": "",
                "audio_pronunciation_lang": "",
                "audio_source": "",
                "audio_updated_at": "",
                "audio_shimoare_filename": "",
                "audio_kibouchi_filename": "",
                "audio_shimoare_available": "",
                "audio_kibouchi_available": ""
            }}
        )
        print(f"✅ {reset_result.modified_count} mots réinitialisés")
        print()
        
        # ÉTAPE 2: Mapping direct
        print("🎯 MAPPING DIRECT FICHIER → MOT")
        print("-" * 40)
        
        mappings_created = 0
        
        for filename in extracted_files:
            # Extraire le nom de base (sans .m4a)
            base_name = filename.replace('.m4a', '')
            
            print(f"🔍 Recherche pour '{base_name}'...")
            
            # Chercher correspondance EXACTE dans toutes les traductions
            matches = []
            
            for word in all_words:
                # Vérifier dans toutes les traductions possibles
                french = word.get('french', '').lower()
                shimaore = word.get('shimaore', '').lower()
                kibouchi = word.get('kibouchi', '').lower()
                
                base_name_lower = base_name.lower()
                
                # Correspondance exacte
                if (base_name_lower == french or 
                    base_name_lower == shimaore or 
                    base_name_lower == kibouchi or
                    base_name_lower.replace(' ', '') == shimaore.replace(' ', '') or
                    base_name_lower.replace(' ', '') == kibouchi.replace(' ', '')):
                    
                    matches.append({
                        'word': word,
                        'match_type': 'exact',
                        'matched_field': 'français' if base_name_lower == french else 
                                       'shimaoré' if base_name_lower in shimaore else 'kibouchi'
                    })
            
            if matches:
                # Prendre la première correspondance exacte
                best_match = matches[0]
                word = best_match['word']
                match_type = best_match['matched_field']
                
                print(f"   ✅ CORRESPONDANCE TROUVÉE:")
                print(f"      Mot français: {word['french']}")
                print(f"      Shimaoré: {word['shimaore']}")
                print(f"      Kibouchi: {word['kibouchi']}")
                print(f"      Correspondance: {match_type}")
                
                # Déterminer la langue du fichier
                audio_lang = "both"  # Par défaut
                if match_type == "shimaoré":
                    audio_lang = "shimaore"
                elif match_type == "kibouchi":
                    audio_lang = "kibouchi"
                
                # Appliquer le mapping
                update_data = {
                    "has_authentic_audio": True,
                    "audio_filename": filename,
                    "audio_pronunciation_lang": audio_lang,
                    "audio_source": "direct_mapping_famille_new",
                    "audio_updated_at": datetime.now(),
                    "direct_mapping_applied": True
                }
                
                result = collection.update_one(
                    {"_id": word["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    mappings_created += 1
                    print(f"      → Mapping créé avec succès")
                else:
                    print(f"      → Échec de création du mapping")
            else:
                print(f"   ❌ AUCUNE CORRESPONDANCE pour '{base_name}'")
            
            print()
        
        # Statistiques finales
        print("=" * 50)
        print(f"📈 RÉSUMÉ DU MAPPING DIRECT")
        print(f"📂 Fichiers traités: {len(extracted_files)}")
        print(f"✅ Mappings créés: {mappings_created}")
        print(f"❌ Fichiers sans correspondance: {len(extracted_files) - mappings_created}")
        print()
        
        # Vérification finale
        audio_words = list(collection.find({"has_authentic_audio": True}))
        print(f"🎵 Total mots avec audio après mapping: {len(audio_words)}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = direct_audio_mapping()
    
    if success:
        print("🎉 MAPPING DIRECT TERMINÉ AVEC SUCCÈS!")
        print("📱 Les fichiers audio sont maintenant mappés directement")
    else:
        print("💥 ÉCHEC DU MAPPING DIRECT")
        sys.exit(1)