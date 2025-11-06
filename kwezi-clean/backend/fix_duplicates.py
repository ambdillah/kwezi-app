#!/usr/bin/env python3
"""
CORRECTION DES DOUBLONS
======================
Supprime les doublons identifiés dans la base de données
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def get_database():
    """Connexion à la base de données MongoDB"""
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/mayotte_app')
    client = MongoClient(mongo_url)
    db = client.mayotte_app
    return db

def remove_duplicates():
    """Supprime les doublons en gardant la meilleure version"""
    print("🔧 Suppression des doublons...")
    
    db = get_database()
    words_collection = db.words
    
    # Trouver les doublons
    pipeline = [
        {"$group": {"_id": "$french", "count": {"$sum": 1}, "docs": {"$push": "$$ROOT"}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    
    duplicates = list(words_collection.aggregate(pipeline))
    
    for duplicate in duplicates:
        french_word = duplicate['_id']
        docs = duplicate['docs']
        
        print(f"🔍 Traitement de '{french_word}' ({len(docs)} occurrences)")
        
        # Garder le premier document et supprimer les autres
        keep_doc = docs[0]
        for doc in docs[1:]:
            words_collection.delete_one({"_id": doc["_id"]})
            print(f"  ❌ Supprimé: {doc['french']} (ID: {doc['_id']})")
        
        print(f"  ✅ Gardé: {keep_doc['french']} - {keep_doc['shimaore']}/{keep_doc['kibouchi']}")
    
    print(f"✅ {len(duplicates)} doublons corrigés")

def verify_no_duplicates():
    """Vérifie qu'il n'y a plus de doublons"""
    print("🔍 Vérification finale des doublons...")
    
    db = get_database()
    words_collection = db.words
    
    pipeline = [
        {"$group": {"_id": "$french", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    
    duplicates = list(words_collection.aggregate(pipeline))
    
    if duplicates:
        print(f"❌ {len(duplicates)} doublons restants:")
        for dup in duplicates:
            print(f"  - {dup['_id']}: {dup['count']} occurrences")
        return False
    else:
        print("✅ Aucun doublon trouvé")
        
        # Afficher les statistiques finales
        total_words = words_collection.count_documents({})
        categories = words_collection.distinct("category")
        
        print(f"📊 Total des mots: {total_words}")
        print(f"📚 Catégories: {len(categories)}")
        
        for category in sorted(categories):
            count = words_collection.count_documents({"category": category})
            print(f"  - {category}: {count} mots")
        
        return True

def main():
    """Fonction principale"""
    print("=" * 50)
    print("🔧 CORRECTION DES DOUBLONS")
    print("=" * 50)
    
    try:
        remove_duplicates()
        success = verify_no_duplicates()
        
        if success:
            print("\n✅ CORRECTION TERMINÉE AVEC SUCCÈS!")
            print("🎉 Plus aucun doublon dans la base de données")
        else:
            print("\n❌ Des doublons persistent")
            return False
            
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)