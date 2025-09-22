#!/usr/bin/env python3
"""
Script pour mettre à jour la section des nombres avec les nouvelles traductions
pour les dizaines (30-100) selon les données fournies par l'utilisateur.
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

from database_protection import DatabaseProtection

def update_nombres_section():
    """Met à jour la section des nombres avec les nouvelles traductions pour les dizaines."""
    
    # Nouvelles traductions pour les nombres (dizaines)
    nouvelles_traductions = [
        {
            "français": "trente",
            "shimaoré": "thalathini", 
            "kibouchi": "téloumpoulou"
        },
        {
            "français": "quarante",
            "shimaoré": "arbahini",
            "kibouchi": "éfampoulou"
        },
        {
            "français": "cinquante", 
            "shimaoré": "hamssini",
            "kibouchi": "dimimpoulou"
        },
        {
            "français": "soixante",
            "shimaoré": "sitini",
            "kibouchi": "tchoutampoulou"
        },
        {
            "français": "soixante-dix",
            "shimaoré": "sabouini", 
            "kibouchi": "fitoumpoulou"
        },
        {
            "français": "quatre-vingts",
            "shimaoré": "thamanini",
            "kibouchi": "valoumpoulou"
        },
        {
            "français": "quatre-vingt-dix",
            "shimaoré": "toussuini",
            "kibouchi": "civiampulou"
        },
        {
            "français": "cent",
            "shimaoré": "miya",
            "kibouchi": "zatou"
        }
    ]
    
    try:
        # Connexion à MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.vocabulary
        
        # Initialiser la protection de base de données
        db_protection = DatabaseProtection(db)
        
        print(f"🔗 Connexion à MongoDB: {mongo_url}")
        print(f"📊 Base de données: {db_name}")
        print(f"📝 Collection: vocabulary")
        print()
        
        # Créer une sauvegarde avant modification
        print("💾 Création d'une sauvegarde avant modification...")
        backup_success = db_protection.create_backup("before_update_nombres_section")
        if backup_success:
            print("✅ Sauvegarde créée avec succès")
        else:
            print("⚠️ Échec de la sauvegarde")
        print()
        
        # Mettre à jour chaque nombre
        mises_a_jour = 0
        nouveaux_mots = 0
        
        for traduction in nouvelles_traductions:
            francais = traduction["français"]
            shimatore = traduction["shimaoré"]
            kibouchi = traduction["kibouchi"]
            
            print(f"🔍 Recherche de '{francais}'...")
            
            # Rechercher le mot existant
            existing_word = collection.find_one({
                "$or": [
                    {"french": francais},
                    {"french": francais.capitalize()}
                ]
            })
            
            if existing_word:
                # Mettre à jour le mot existant
                print(f"   ✏️ Mise à jour existante: {francais}")
                print(f"      Ancien Shimaoré: {existing_word.get('shimatore', 'N/A')}")
                print(f"      Nouveau Shimaoré: {shimatore}")
                print(f"      Ancien Kibouchi: {existing_word.get('kibouchi', 'N/A')}")
                print(f"      Nouveau Kibouchi: {kibouchi}")
                
                update_data = {
                    "shimatore": shimatore,
                    "kibouchi": kibouchi,
                    "updated_at": datetime.now(),
                    "updated_by": "update_nombres_section_script"
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
                    "shimatore": shimatore,
                    "kibouchi": kibouchi,
                    "category": "Nombres",
                    "emoji": "",  # Pas d'emoji pour les nombres selon les préférences
                    "created_at": datetime.now(),
                    "created_by": "update_nombres_section_script",
                    "authentic": True
                }
                
                result = collection.insert_one(new_word)
                
                if result.inserted_id:
                    nouveaux_mots += 1
                    print(f"   ✅ Créé avec succès")
                else:
                    print(f"   ❌ Échec de création")
            
            print()
        
        # Statistiques finales
        print("=" * 60)
        print(f"📈 RÉSUMÉ DES MODIFICATIONS")
        print(f"📝 Mots mis à jour: {mises_a_jour}")
        print(f"➕ Nouveaux mots créés: {nouveaux_mots}")
        print(f"📊 Total traité: {len(nouvelles_traductions)}")
        print()
        
        # Vérification de l'intégrité
        print("🔍 Vérification de l'intégrité de la base de données...")
        integrity_ok = db_protection.check_integrity()
        if integrity_ok:
            print("✅ Intégrité vérifiée avec succès")
        else:
            print("⚠️ Problème d'intégrité détecté")
        
        print()
        print("✅ Mise à jour de la section nombres terminée avec succès!")
        
        # Fermer la connexion
        client.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Début de la mise à jour de la section nombres...")
    print()
    
    success = update_nombres_section()
    
    if success:
        print("🎉 Mise à jour terminée avec succès!")
    else:
        print("💥 Échec de la mise à jour")
        sys.exit(1)