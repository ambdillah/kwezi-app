#!/usr/bin/env python3
"""
CORRECTION SPÉCIFIQUE: Traduction de "non"
=========================================
Corrige la traduction de "non" en Shimaoré et Kibouchi pour "an'ha"
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from database_protection import protect_database, db_protector

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'mayotte_app')

@protect_database("fix_non_translation")
def fix_non_translation():
    """Corrige la traduction de 'non' pour 'an'ha' dans les deux langues"""
    print("🔧 CORRECTION DE LA TRADUCTION DE 'NON'")
    print("=" * 50)
    
    try:
        client = MongoClient(MONGO_URL)
        client.admin.command('ping')
        print(f"✅ Connexion MongoDB établie : {MONGO_URL}")
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB : {e}")
        return False
    
    db = client[DB_NAME]
    words_collection = db.words
    
    # Chercher le mot "non"
    print("🔍 Recherche du mot 'non'...")
    non_word = words_collection.find_one({
        "french": {"$regex": "^non$", "$options": "i"}
    })
    
    if not non_word:
        print("❌ Mot 'non' non trouvé dans la base de données")
        client.close()
        return False
    
    # Afficher la traduction actuelle
    print(f"📝 Traduction actuelle:")
    print(f"   Français: {non_word.get('french', 'N/A')}")
    print(f"   Shimaoré: {non_word.get('shimaore', 'N/A')}")
    print(f"   Kibouchi: {non_word.get('kibouchi', 'N/A')}")
    
    # Appliquer la correction
    print(f"\n🔧 Application de la correction vers 'an'ha'...")
    
    update_result = words_collection.update_one(
        {"_id": non_word["_id"]},
        {
            "$set": {
                "shimaore": "an'ha",
                "kibouchi": "an'ha"
            }
        }
    )
    
    if update_result.modified_count > 0:
        print("✅ Correction appliquée avec succès !")
        
        # Vérifier la correction
        updated_word = words_collection.find_one({"_id": non_word["_id"]})
        print(f"\n📝 Traduction corrigée:")
        print(f"   Français: {updated_word.get('french', 'N/A')}")
        print(f"   Shimaoré: {updated_word.get('shimaore', 'N/A')}")
        print(f"   Kibouchi: {updated_word.get('kibouchi', 'N/A')}")
        
        client.close()
        return True
    else:
        print("❌ Échec de la correction")
        client.close()
        return False

if __name__ == "__main__":
    print("🚀 Démarrage de la correction de la traduction de 'non'...")
    
    # Vérifier l'état initial
    print("\n🔍 Vérification de l'état de la base de données...")
    is_healthy, message = db_protector.is_database_healthy()
    if not is_healthy:
        print(f"⚠️ Problème détecté: {message}")
        print("🔄 Restauration recommandée avant correction")
        exit(1)
    
    # Appliquer la correction
    success = fix_non_translation()
    
    if success:
        print("\n🎉 CORRECTION APPLIQUÉE AVEC SUCCÈS!")
        print("✅ La traduction de 'non' a été corrigée vers 'an'ha' dans les deux langues")
        
        # Vérification finale de l'intégrité
        print("\n🔍 Vérification finale de l'intégrité...")
        is_healthy_after, message_after = db_protector.is_database_healthy()
        if is_healthy_after:
            print("✅ Base de données saine après correction")
        else:
            print(f"⚠️ Problème détecté après correction: {message_after}")
    else:
        print("\n❌ CORRECTION ÉCHOUÉE")
    
    print("\nFin du script de correction.")