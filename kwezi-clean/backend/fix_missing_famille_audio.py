#!/usr/bin/env python3
"""
Script pour ajouter les métadonnées audio manquantes pour la section famille
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# Ajouter le chemin du backend au PYTHONPATH
sys.path.append('/app/backend')

# Charger les variables d'environnement
load_dotenv()

from database_protection import DatabaseProtector

def fix_missing_famille_audio():
    """Ajoute les métadonnées audio manquantes pour les mots famille sans icône."""
    
    # Correspondances pour les mots manquants
    missing_audio_mappings = [
        # Fichiers audio inutilisés qui correspondent aux mots manquants
        {
            "french": "tente",  # Déjà dans la base avec Ninfndri héli-bé.m4a
            "add_metadata": {
                "audio_filename": "Mama titi-bolé.m4a",  # Version shimaoré
                "audio_pronunciation_lang": "shimaore",
                "audio_source": "google_drive_famille_completion"
            }
        },
        {
            "french": "grand-mère",  # Ajouter version shimaoré
            "add_metadata": {
                "audio_filename": "Coco.m4a", 
                "audio_pronunciation_lang": "both",  # Déjà Dadi.m4a (kibouchi), ajouter Coco.m4a
                "audio_source": "google_drive_famille_completion",
                "note": "Version shimaoré Coco.m4a en plus de Dadi.m4a"
            }
        },
        {
            "french": "grand-père",  # Ajouter version shimaoré
            "add_metadata": {
                "audio_filename": "Bacoco.m4a",
                "audio_pronunciation_lang": "both",  # Déjà Dadayi.m4a (kibouchi), ajouter Bacoco.m4a
                "audio_source": "google_drive_famille_completion",
                "note": "Version shimaoré Bacoco.m4a en plus de Dadayi.m4a"
            }
        },
        {
            "french": "famille",  # Ajouter version shimaoré
            "add_metadata": {
                "audio_filename": "Havagna.m4a", 
                "audio_pronunciation_lang": "both",  # Déjà Mdjamaza.m4a (shimaoré), ajouter Havagna.m4a
                "audio_source": "google_drive_famille_completion",
                "note": "Version kibouchi Havagna.m4a en plus de Mdjamaza.m4a"
            }
        },
        {
            "french": "oncle paternel",  # Ajouter version kibouchi
            "add_metadata": {
                "audio_filename": "Baba héli-bé.m4a",
                "audio_pronunciation_lang": "both",  # Déjà Baba titi-bolé.m4a (shimaoré)
                "audio_source": "google_drive_famille_completion",
                "note": "Version kibouchi Baba héli-bé.m4a"
            }
        },
        {
            "french": "papa",  # Ajouter version kibouchi
            "add_metadata": {
                "audio_filename": "Baba k.m4a",
                "audio_pronunciation_lang": "both",  # Déjà Baba s.m4a (shimaoré)
                "audio_source": "google_drive_famille_completion",
                "note": "Version kibouchi Baba k.m4a"
            }
        },
        {
            "french": "grande sœur",  # Ajouter version kibouchi
            "add_metadata": {
                "audio_filename": "Zoki viavi.m4a",
                "audio_pronunciation_lang": "both",  # Déjà Zouki mtroumché.m4a (shimaoré)
                "audio_source": "google_drive_famille_completion",
                "note": "Version kibouchi Zoki viavi.m4a"
            }
        },
        {
            "french": "grand frère",  # Ajouter version kibouchi
            "add_metadata": {
                "audio_filename": "Zoki lalahi.m4a",
                "audio_pronunciation_lang": "both",  # Déjà Zouki mtroubaba.m4a (shimaoré)
                "audio_source": "google_drive_famille_completion",
                "note": "Version kibouchi Zoki lalahi.m4a"
            }
        }
    ]
    
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
        print()
        
        # Créer une sauvegarde avant modification
        print("💾 Création d'une sauvegarde avant modification...")
        backup_path = db_protection.create_backup("before_fix_missing_famille_audio")
        if backup_path:
            print("✅ Sauvegarde créée avec succès")
        else:
            print("⚠️ Échec de la sauvegarde")
        print()
        
        # Traiter chaque correspondance manquante
        updates_made = 0
        
        for mapping in missing_audio_mappings:
            french_word = mapping["french"]
            metadata = mapping["add_metadata"]
            
            print(f"🔍 Traitement de '{french_word}'...")
            
            # Rechercher le mot dans la base
            existing_word = collection.find_one({
                "french": {"$regex": f"^{french_word}$", "$options": "i"},
                "category": "famille"
            })
            
            if existing_word:
                print(f"   ✅ Mot trouvé: {french_word}")
                
                # Si le mot a déjà des métadonnées audio, améliorer plutôt que remplacer
                if existing_word.get("has_authentic_audio"):
                    print(f"   📝 Amélioration métadonnées existantes")
                    if "note" in metadata:
                        print(f"      Note: {metadata['note']}")
                    
                    # Mettre à jour avec les nouvelles informations
                    update_data = {
                        "audio_updated_at": datetime.now(),
                        "audio_completion_by": "fix_missing_famille_audio_script"
                    }
                    
                    # Ajouter les nouveaux champs
                    for key, value in metadata.items():
                        if key != "note":
                            update_data[key] = value
                    
                else:
                    print(f"   ➕ Ajout métadonnées audio complètes")
                    
                    # Ajouter toutes les métadonnées audio
                    update_data = {
                        "has_authentic_audio": True,
                        "audio_updated_at": datetime.now(),
                        "audio_added_by": "fix_missing_famille_audio_script"
                    }
                    
                    # Ajouter les nouveaux champs
                    for key, value in metadata.items():
                        if key != "note":
                            update_data[key] = value
                
                # Effectuer la mise à jour
                result = collection.update_one(
                    {"_id": existing_word["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    updates_made += 1
                    print(f"   ✅ Mis à jour avec succès")
                else:
                    print(f"   ⚠️ Aucune modification effectuée")
                    
            else:
                print(f"   ❌ Mot '{french_word}' non trouvé dans la catégorie famille")
            
            print()
        
        # Vérifier l'état final
        final_famille_with_audio = collection.count_documents({
            "category": "famille", 
            "has_authentic_audio": True
        })
        
        # Statistiques finales
        print("=" * 60)
        print(f"📈 RÉSUMÉ DES CORRECTIONS AUDIO FAMILLE")
        print(f"📝 Mots mis à jour: {updates_made}")
        print(f"📊 Total mots famille avec audio: {final_famille_with_audio}")
        print(f"🎯 Correspondances traitées: {len(missing_audio_mappings)}")
        print()
        
        print("✅ Correction des métadonnées audio famille terminée!")
        
        # Fermer la connexion
        client.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 CORRECTION DES MÉTADONNÉES AUDIO FAMILLE MANQUANTES")
    print("🎯 Objectif: Ajouter les icônes 🎵 manquantes pour la section famille")
    print("=" * 60)
    print()
    
    success = fix_missing_famille_audio()
    
    if success:
        print("🎉 Correction terminée avec succès!")
        print("📱 Les icônes audio devraient maintenant apparaître pour plus de mots famille")
    else:
        print("💥 Échec de la correction")
        sys.exit(1)