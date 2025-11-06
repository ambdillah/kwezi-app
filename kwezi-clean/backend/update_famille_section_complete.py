#!/usr/bin/env python3
"""
Mise à jour complète de la section famille avec les nouvelles données du tableau
Intègre toutes les corrections et nouveaux mots de famille
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

def backup_famille_words():
    """Crée une sauvegarde des mots de famille"""
    collection = connect_to_database()
    famille_words = list(collection.find({"category": "famille"}))
    
    backup_filename = f"/app/backend/backup_famille_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    import json
    # Convertir ObjectId en string pour JSON
    for word in famille_words:
        if '_id' in word:
            word['_id'] = str(word['_id'])
        for key, value in word.items():
            if isinstance(value, datetime):
                word[key] = value.isoformat()
    
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(famille_words, f, ensure_ascii=False, indent=2)
    
    print(f"Sauvegarde créée: {backup_filename}")
    return backup_filename

def update_famille_vocabulary():
    """Met à jour le vocabulaire de famille avec les nouvelles données"""
    collection = connect_to_database()
    
    # Nouvelles données de famille du tableau (corrigées et complètes)
    famille_updates = [
        {
            "french": "Tante maternelle",
            "shimaore": "mama titi bolé", 
            "kibouchi": "nindri heli bé",
            "category": "famille",
            "difficulty": 2
        },
        {
            "french": "Oncle maternel",
            "shimaore": "zama",
            "kibouchi": "zama", 
            "category": "famille",
            "difficulty": 2
        },
        {
            "french": "Oncle paternel",
            "shimaore": "Baba titi bolé",
            "kibouchi": "Baba heli bé",
            "category": "famille", 
            "difficulty": 2
        },
        {
            "french": "Épouse oncle maternel",
            "shimaore": "zena",
            "kibouchi": "zena",
            "category": "famille",
            "difficulty": 3
        },
        {
            "french": "Petite sœur",
            "shimaore": "moinagna mtroumama",
            "kibouchi": "zandri viavi",
            "category": "famille",
            "difficulty": 2
        },
        {
            "french": "Petit frère", 
            "shimaore": "moinagna mtroubaba",
            "kibouchi": "zandri lalahi",
            "category": "famille",
            "difficulty": 2
        },
        {
            "french": "Grande sœur",
            "shimaore": "Zouki mtroumché",
            "kibouchi": "zoki viavi", 
            "category": "famille",
            "difficulty": 2
        },
        {
            "french": "Grand frère",
            "shimaore": "Zouki mtoubaba",
            "kibouchi": "zoki lalahi",
            "category": "famille",
            "difficulty": 2
        },
        {
            "french": "Frère", 
            "shimaore": "mwanagna",
            "kibouchi": "anadahi",
            "category": "famille",
            "difficulty": 1
        },
        {
            "french": "Sœur",
            "shimaore": "mwanagna", 
            "kibouchi": "anabavi",
            "category": "famille",
            "difficulty": 1
        },
        {
            "french": "Ami",
            "shimaore": "mwandzani",
            "kibouchi": "mwandzani",
            "category": "famille", 
            "difficulty": 1
        },
        {
            "french": "Fille",
            "shimaore": "mtroumama",
            "kibouchi": "viavi",
            "category": "famille",
            "difficulty": 1
        },
        {
            "french": "Femme",
            "shimaore": "mtroumama", 
            "kibouchi": "viavi",
            "category": "famille",
            "difficulty": 1
        },
        {
            "french": "Garçon",
            "shimaore": "mtroubaba",
            "kibouchi": "lalahi", 
            "category": "famille",
            "difficulty": 1
        },
        {
            "french": "Homme",
            "shimaore": "mtroubaba",
            "kibouchi": "lalahi",
            "category": "famille",
            "difficulty": 1
        },
        {
            "french": "Monsieur",
            "shimaore": "mogné",
            "kibouchi": "lalahi",
            "category": "famille",
            "difficulty": 2
        },
        {
            "french": "Grand-père",
            "shimaore": "bacoco", 
            "kibouchi": "dadayi",
            "category": "famille",
            "difficulty": 1
        },
        {
            "french": "Grand-mère",
            "shimaore": "coco",
            "kibouchi": "dadi",
            "category": "famille",
            "difficulty": 1
        },
        {
            "french": "Madame",
            "shimaore": "bvéni",
            "kibouchi": "viavi", 
            "category": "famille",
            "difficulty": 2
        },
        {
            "french": "Famille",
            "shimaore": "mdjamaza",
            "kibouchi": "havagna",
            "category": "famille",
            "difficulty": 1
        },
        {
            "french": "Papa",
            "shimaore": "baba",
            "kibouchi": "baba",
            "category": "famille", 
            "difficulty": 1
        },
        {
            "french": "Maman",
            "shimaore": "mama",
            "kibouchi": "mama",
            "category": "famille",
            "difficulty": 1
        },
        {
            "french": "Tante paternelle",
            "shimaore": "zéna",
            "kibouchi": "zéna",
            "category": "famille",
            "difficulty": 2
        },
        {
            "french": "Jeune adulte", 
            "shimaore": "shababi",
            "kibouchi": "shababi",
            "category": "famille",
            "difficulty": 2
        },
        {
            "french": "Petit garçon",
            "shimaore": "mwana mtroubaba",
            "kibouchi": "zaza lalahi",
            "category": "famille",
            "difficulty": 1
        },
        {
            "french": "Petite fille",
            "shimaore": "mwana mtroumama", 
            "kibouchi": "zaza viavi",
            "category": "famille",
            "difficulty": 1
        }
    ]
    
    updates_count = 0
    additions_count = 0
    
    print("=== MISE À JOUR DE LA SECTION FAMILLE ===")
    
    for word_data in famille_updates:
        # Vérifier si le mot existe déjà
        existing_word = collection.find_one({
            "french": word_data["french"],
            "category": "famille"
        })
        
        if existing_word:
            # Mettre à jour le mot existant
            update_data = {
                "shimaore": word_data["shimaore"],
                "kibouchi": word_data["kibouchi"], 
                "difficulty": word_data["difficulty"],
                "updated_at": datetime.utcnow(),
                "updated_from_tableau": True
            }
            
            collection.update_one(
                {"_id": existing_word["_id"]},
                {"$set": update_data}
            )
            
            print(f"✓ MIS À JOUR: {word_data['french']}")
            print(f"   Shimaoré: {word_data['shimaore']}")
            print(f"   Kibouchi: {word_data['kibouchi']}")
            updates_count += 1
            
        else:
            # Ajouter le nouveau mot
            new_word = {
                "french": word_data["french"],
                "shimaore": word_data["shimaore"], 
                "kibouchi": word_data["kibouchi"],
                "category": word_data["category"],
                "difficulty": word_data["difficulty"],
                "created_at": datetime.utcnow(),
                "added_from_tableau": True,
                "image_url": None,
                "audio_url": None
            }
            
            collection.insert_one(new_word)
            
            print(f"✓ AJOUTÉ: {word_data['french']}")
            print(f"   Shimaoré: {word_data['shimaore']}") 
            print(f"   Kibouchi: {word_data['kibouchi']}")
            additions_count += 1
    
    return updates_count, additions_count

def verify_famille_update():
    """Vérifie que la mise à jour s'est bien passée"""
    collection = connect_to_database()
    
    print("\n=== VÉRIFICATION DE LA MISE À JOUR ===")
    
    # Compter les mots de famille
    famille_count = collection.count_documents({"category": "famille"})
    print(f"Total mots de famille: {famille_count}")
    
    # Vérifier quelques mots clés
    test_words = [
        "Tante maternelle",
        "Oncle maternel", 
        "Petite sœur",
        "Grand frère",
        "Petite fille"
    ]
    
    print(f"\nVérification des nouveaux mots:")
    for french_word in test_words:
        word = collection.find_one({"french": french_word, "category": "famille"})
        if word:
            print(f"✓ {french_word}: {word['shimaore']} / {word['kibouchi']}")
        else:
            print(f"✗ {french_word}: NON TROUVÉ")
    
    # Lister tous les mots de famille
    print(f"\nTous les mots de famille:")
    all_famille = collection.find({"category": "famille"}).sort("french", 1)
    for word in all_famille:
        print(f"  {word['french']}: {word['shimaore']} / {word['kibouchi']}")

def main():
    """Fonction principale"""
    print("=== MISE À JOUR COMPLÈTE SECTION FAMILLE ===")
    print("Intégration des nouvelles données du tableau\n")
    
    # Créer sauvegarde
    backup_file = backup_famille_words()
    
    try:
        # Appliquer les mises à jour
        updates, additions = update_famille_vocabulary()
        
        print(f"\n✅ MISE À JOUR TERMINÉE:")
        print(f"  - Mots mis à jour: {updates}")
        print(f"  - Mots ajoutés: {additions}")
        print(f"  - Total modifications: {updates + additions}")
        
        # Vérification
        verify_famille_update()
        
        print(f"\n🎉 SECTION FAMILLE MISE À JOUR AVEC SUCCÈS !")
        print(f"Sauvegarde disponible: {backup_file}")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        print(f"Restaurez la sauvegarde si nécessaire: {backup_file}")
        raise

if __name__ == "__main__":
    main()