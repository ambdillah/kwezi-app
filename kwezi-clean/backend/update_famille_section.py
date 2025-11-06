#!/usr/bin/env python3
"""
Script pour mettre à jour la section famille avec les nouvelles traductions
selon les données fournies par l'utilisateur.
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

def update_famille_section():
    """Met à jour la section famille avec les nouvelles traductions."""
    
    # Nouvelles traductions pour la famille
    nouvelles_traductions = [
        {
            "français": "Tente",
            "shimaoré": "mama titi/bolé", 
            "kibouchi": "nindri heli/bé"
        },
        {
            "français": "oncle maternel",
            "shimaoré": "zama",
            "kibouchi": "zama"
        },
        {
            "français": "oncle paternel", 
            "shimaoré": "Baba titi/bolé",
            "kibouchi": "Baba heli/bé"
        },
        {
            "français": "épouse oncle maternel",
            "shimaoré": "zena",
            "kibouchi": "zena"
        },
        {
            "français": "petite sœur",
            "shimaoré": "moinagna mtroumama", 
            "kibouchi": "zandri"
        },
        {
            "français": "petit frère",
            "shimaoré": "moinagna mtroubaba",
            "kibouchi": "zandri"
        },
        {
            "français": "grande sœur",
            "shimaoré": "Zouki mtroumché",
            "kibouchi": "zoki viavi"
        },
        {
            "français": "grand frère",
            "shimaoré": "Zouki mtoubaba",
            "kibouchi": "zoki lalahi"
        },
        {
            "français": "frère",
            "shimaoré": "mwanagna mtroubaba",
            "kibouchi": "anadahi"
        },
        {
            "français": "sœur",
            "shimaoré": "mwanagna mtroumama",
            "kibouchi": "anabavi"
        },
        {
            "français": "ami",
            "shimaoré": "mwandzani",
            "kibouchi": "mwandzani"
        },
        {
            "français": "fille",
            "shimaoré": "mtroumama",
            "kibouchi": "viavi"
        },
        {
            "français": "femme",
            "shimaoré": "mtroumama",
            "kibouchi": "viavi"
        },
        {
            "français": "garçon",
            "shimaoré": "mtroubaba",
            "kibouchi": "lalahi"
        },
        {
            "français": "homme",
            "shimaoré": "mtroubaba",
            "kibouchi": "lalahi"
        },
        {
            "français": "monsieur",
            "shimaoré": "mogné",
            "kibouchi": "lalahi"
        },
        {
            "français": "grand-père",
            "shimaoré": "bacoco",
            "kibouchi": "dadayi"
        },
        {
            "français": "grand-mère",
            "shimaoré": "coco",
            "kibouchi": "dadi"
        },
        {
            "français": "madame",
            "shimaoré": "bvéni",
            "kibouchi": "viavi"
        },
        {
            "français": "famille",
            "shimaoré": "mdjamaza",
            "kibouchi": "havagna"
        },
        {
            "français": "papa",
            "shimaoré": "baba",
            "kibouchi": "baba"
        },
        {
            "français": "maman",
            "shimaoré": "mama",
            "kibouchi": "mama"
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
        print(f"📝 Collection: words")
        print()
        
        # Créer une sauvegarde avant modification
        print("💾 Création d'une sauvegarde avant modification...")
        backup_path = db_protection.create_backup("before_update_famille_section")
        if backup_path:
            print("✅ Sauvegarde créée avec succès")
        else:
            print("⚠️ Échec de la sauvegarde")
        print()
        
        # Vérifier l'état actuel
        current_count = collection.count_documents({})
        print(f"📊 État actuel: {current_count} mots dans la base")
        print()
        
        # Mettre à jour chaque terme de famille
        mises_a_jour = 0
        nouveaux_mots = 0
        
        for traduction in nouvelles_traductions:
            francais = traduction["français"].lower().strip()
            shimaore = traduction["shimaoré"]
            kibouchi = traduction["kibouchi"]
            
            print(f"🔍 Recherche de '{francais}'...")
            
            # Rechercher le mot existant (insensible à la casse)
            existing_word = collection.find_one({
                "$or": [
                    {"french": {"$regex": f"^{francais}$", "$options": "i"}},
                    {"french": {"$regex": f"^{francais.capitalize()}$", "$options": "i"}}
                ]
            })
            
            if existing_word:
                # Mettre à jour le mot existant
                print(f"   ✏️ Mise à jour existante: {francais}")
                print(f"      Ancien Shimaoré: {existing_word.get('shimaore', 'N/A')}")
                print(f"      Nouveau Shimaoré: {shimaore}")
                print(f"      Ancien Kibouchi: {existing_word.get('kibouchi', 'N/A')}")
                print(f"      Nouveau Kibouchi: {kibouchi}")
                
                update_data = {
                    "shimaore": shimaore,
                    "kibouchi": kibouchi,
                    "updated_at": datetime.now(),
                    "updated_by": "update_famille_section_script"
                }
                
                result = collection.update_one(
                    {"_id": existing_word["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    mises_a_jour += 1
                    print(f"   ✅ Mis à jour avec succès")
                else:
                    print(f"   ⚠️ Aucune modification effectuée")
                    
            else:
                # Créer un nouveau mot
                print(f"   ➕ Création nouveau mot: {francais}")
                
                new_word = {
                    "french": francais,
                    "shimaore": shimaore,
                    "kibouchi": kibouchi,
                    "category": "famille",
                    "emoji": "",  # Pas d'emoji selon les préférences
                    "created_at": datetime.now(),
                    "created_by": "update_famille_section_script",
                    "authentic": True
                }
                
                result = collection.insert_one(new_word)
                
                if result.inserted_id:
                    nouveaux_mots += 1
                    print(f"   ✅ Créé avec succès")
                else:
                    print(f"   ❌ Échec de création")
            
            print()
        
        # Vérifier l'état final
        final_count = collection.count_documents({})
        
        # Statistiques finales
        print("=" * 60)
        print(f"📈 RÉSUMÉ DES MODIFICATIONS")
        print(f"📝 Mots mis à jour: {mises_a_jour}")
        print(f"➕ Nouveaux mots créés: {nouveaux_mots}")
        print(f"📊 Total traité: {len(nouvelles_traductions)}")
        print(f"📊 État final: {final_count} mots dans la base")
        print()
        
        # Vérification de l'intégrité
        print("🔍 Vérification de l'intégrité de la base de données...")
        is_healthy, message = db_protection.is_database_healthy()
        if is_healthy:
            print("✅ Intégrité vérifiée avec succès")
        else:
            print(f"⚠️ Problème d'intégrité détecté: {message}")
        
        print()
        print("✅ Mise à jour de la section famille terminée avec succès!")
        
        # Fermer la connexion
        client.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Début de la mise à jour de la section famille...")
    print()
    
    success = update_famille_section()
    
    if success:
        print("🎉 Mise à jour terminée avec succès!")
    else:
        print("💥 Échec de la mise à jour")
        sys.exit(1)