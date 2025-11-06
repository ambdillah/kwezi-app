#!/usr/bin/env python3
"""
Script pour mettre à jour les sections "transport", "vêtements" et "tradition" avec les données exactes des images fournies
Suppression systématique des doublons et tri par ordre alphabétique
"""

import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/mayotte_app")
client = MongoClient(MONGO_URL)
db = client.mayotte_app
words_collection = db.words

def update_transport_vetements_tradition():
    """Mettre à jour les sections transport, vêtements et tradition avec les données exactes des images"""
    
    # Supprimer tous les mots existants des catégories "transport", "vetements" et "tradition"
    result_delete_transport = words_collection.delete_many({"category": "transport"})
    result_delete_vetements = words_collection.delete_many({"category": "vetements"})
    result_delete_tradition = words_collection.delete_many({"category": "tradition"})
    print(f"🗑️ Supprimé {result_delete_transport.deleted_count} anciens mots de transport")
    print(f"🗑️ Supprimé {result_delete_vetements.deleted_count} anciens vêtements")
    print(f"🗑️ Supprimé {result_delete_tradition.deleted_count} anciennes traditions")
    
    # SECTION TRANSPORT - 8 mots exacts selon l'image (triés par ordre alphabétique)
    transport_vocabulary = [
        {"french": "avion", "shimaore": "ndrègué", "kibouchi": "roplani", "category": "transport", "image_url": "✈️", "difficulty": 1},
        {"french": "barge", "shimaore": "markabou", "kibouchi": "markabou", "category": "transport", "image_url": "⛴️", "difficulty": 1},
        {"french": "motos", "shimaore": "monto", "kibouchi": "monto", "category": "transport", "image_url": "🏍️", "difficulty": 1},
        {"french": "pirogue", "shimaore": "laka", "kibouchi": "lakana", "category": "transport", "image_url": "🛶", "difficulty": 1},
        {"french": "taxis", "shimaore": "taxi", "kibouchi": "taxi", "category": "transport", "image_url": "🚕", "difficulty": 1},
        {"french": "vedettes", "shimaore": "kwassa kwassa", "kibouchi": "videti", "category": "transport", "image_url": "🚤", "difficulty": 1},
        {"french": "vélos", "shimaore": "bicycleti", "kibouchi": "bicycleti", "category": "transport", "image_url": "🚲", "difficulty": 1},
    ]
    
    # SECTION VÊTEMENTS - 17 mots exacts selon l'image (triés par ordre alphabétique)
    vetements_vocabulary = [
        {"french": "baskets/sneakers", "shimaore": "magochi", "kibouchi": "magochi", "category": "vetements", "image_url": "👟", "difficulty": 1},
        {"french": "chapeau", "shimaore": "kofia", "kibouchi": "koufia", "category": "vetements", "image_url": "👒", "difficulty": 1},
        {"french": "chaussures", "shimaore": "kabwa", "kibouchi": "kabwa", "category": "vetements", "image_url": "👞", "difficulty": 1},
        {"french": "chemise", "shimaore": "chimizi", "kibouchi": "chimizi", "category": "vetements", "image_url": "👔", "difficulty": 1},
        {"french": "haut de salouva", "shimaore": "body", "kibouchi": "body", "category": "vetements", "image_url": "👕", "difficulty": 1},
        {"french": "jupe", "shimaore": "ripo", "kibouchi": "ripou", "category": "vetements", "image_url": "👗", "difficulty": 1},
        {"french": "kamiss/boubou", "shimaore": "candzou bolé", "kibouchi": "ancandzou bé", "category": "vetements", "image_url": "👘", "difficulty": 1},
        {"french": "pantalon", "shimaore": "sourouali", "kibouchi": "sourouali", "category": "vetements", "image_url": "👖", "difficulty": 1},
        {"french": "robe", "shimaore": "robo", "kibouchi": "robou", "category": "vetements", "image_url": "👗", "difficulty": 1},
        {"french": "salouva", "shimaore": "salouva", "kibouchi": "slouvagna", "category": "vetements", "image_url": "👘", "difficulty": 1},
        {"french": "short", "shimaore": "kaliso", "kibouchi": "kaliso", "category": "vetements", "image_url": "🩳", "difficulty": 1},
        {"french": "sous vêtement", "shimaore": "silipou", "kibouchi": "silipou", "category": "vetements", "image_url": "🩲", "difficulty": 1},
        {"french": "t shirt", "shimaore": "kandzou", "kibouchi": "kandzou", "category": "vetements", "image_url": "👕", "difficulty": 1},
        {"french": "tongs", "shimaore": "sapatri", "kibouchi": "kabwa sapatri", "category": "vetements", "image_url": "🩴", "difficulty": 1},
        {"french": "vêtement", "shimaore": "ngouvwo", "kibouchi": "ankandzou", "category": "vetements", "image_url": "👕", "difficulty": 1},
        {"french": "voile", "shimaore": "kichali", "kibouchi": "kichali", "category": "vetements", "image_url": "🧣", "difficulty": 1},
    ]
    
    # SECTION TRADITION - 16 mots exacts selon l'image (triés par ordre alphabétique)
    tradition_vocabulary = [
        {"french": "barbecue traditionnelle", "shimaore": "voulé", "kibouchi": "voulé", "category": "tradition", "image_url": "🔥", "difficulty": 1},
        {"french": "boxe traditionnelle", "shimaore": "mrengué", "kibouchi": "mouringui", "category": "tradition", "image_url": "🥊", "difficulty": 1},
        {"french": "camper", "shimaore": "tobé", "kibouchi": "mitobi", "category": "tradition", "image_url": "🏕️", "difficulty": 1},
        {"french": "cérémonie", "shimaore": "shouhouli", "kibouchi": "shouhouli", "category": "tradition", "image_url": "⛪", "difficulty": 2},
        {"french": "chant mariage traditionnel", "shimaore": "mlélèzi", "kibouchi": "mlélèzi", "category": "tradition", "image_url": "🎵", "difficulty": 2},
        {"french": "chant religieux femme", "shimaore": "deba", "kibouchi": "deba", "category": "tradition", "image_url": "🎵", "difficulty": 2},
        {"french": "chant religieux homme", "shimaore": "Moulidi Dahra dinahou", "kibouchi": "Moulidi Dahra dinahou", "category": "tradition", "image_url": "🎵", "difficulty": 2},
        {"french": "chant religieux mixte", "shimaore": "shengué madjlis", "kibouchi": "maoulida shengué madjlis", "category": "tradition", "image_url": "🎵", "difficulty": 2},
        {"french": "chant traditionnelle", "shimaore": "mgodro", "kibouchi": "mgodro", "category": "tradition", "image_url": "🎵", "difficulty": 2},
        {"french": "danse traditionnelle femme", "shimaore": "mbiwi wadhaha", "kibouchi": "mbiwi wadhaha", "category": "tradition", "image_url": "💃", "difficulty": 1},
        {"french": "danse traditionnelle mixte", "shimaore": "shigoma", "kibouchi": "shigoma", "category": "tradition", "image_url": "💃", "difficulty": 1},
        {"french": "fiançailles", "shimaore": "mafounguidzo", "kibouchi": "mafounguidzo", "category": "tradition", "image_url": "💒", "difficulty": 2},
        {"french": "grand mariage", "shimaore": "manzaraka", "kibouchi": "manzaraka", "category": "tradition", "image_url": "💒", "difficulty": 2},
        {"french": "mariage", "shimaore": "haroussi", "kibouchi": "haroussi", "category": "tradition", "image_url": "💒", "difficulty": 1},
        {"french": "rite de la pluie", "shimaore": "mgourou", "kibouchi": "mgourou", "category": "tradition", "image_url": "🌧️", "difficulty": 2},
        {"french": "tamtam boeuf", "shimaore": "ngoma ya nyombé", "kibouchi": "vala naoumbi", "category": "tradition", "image_url": "🥁", "difficulty": 1},
    ]
    
    # Fonction pour supprimer les doublons tout en gardant l'ordre alphabétique
    def remove_duplicates(words_list):
        seen = set()
        unique_words = []
        for word in words_list:
            # Utiliser le mot français comme clé unique
            key = word["french"].lower()
            if key not in seen:
                seen.add(key)
                unique_words.append(word)
        return unique_words
    
    # Supprimer les doublons et trier par ordre alphabétique
    transport_vocabulary = remove_duplicates(sorted(transport_vocabulary, key=lambda x: x["french"].lower()))
    vetements_vocabulary = remove_duplicates(sorted(vetements_vocabulary, key=lambda x: x["french"].lower()))
    tradition_vocabulary = remove_duplicates(sorted(tradition_vocabulary, key=lambda x: x["french"].lower()))
    
    # Ajouter timestamp à chaque mot
    all_vocabulary = transport_vocabulary + vetements_vocabulary + tradition_vocabulary
    for word in all_vocabulary:
        word["created_at"] = datetime.utcnow()
    
    # Insérer tous les nouveaux mots
    result = words_collection.insert_many(all_vocabulary)
    
    print(f"✅ Sections transport, vêtements et tradition mises à jour : {len(result.inserted_ids)} mots ajoutés")
    print(f"📊 Transport : {len(transport_vocabulary)} mots (triés alphabétiquement)")
    print(f"📊 Vêtements : {len(vetements_vocabulary)} mots (triés alphabétiquement)")
    print(f"📊 Tradition : {len(tradition_vocabulary)} mots (triés alphabétiquement)")
    
    # Vérification
    total_words = words_collection.count_documents({})
    transport_count = words_collection.count_documents({"category": "transport"})
    vetements_count = words_collection.count_documents({"category": "vetements"})
    tradition_count = words_collection.count_documents({"category": "tradition"})
    
    print(f"\n📈 STATISTIQUES MISES À JOUR :")
    print(f"   Total des mots dans la base : {total_words}")
    print(f"   Mots dans la catégorie transport : {transport_count}")
    print(f"   Mots dans la catégorie vêtements : {vetements_count}")
    print(f"   Mots dans la catégorie tradition : {tradition_count}")
    print(f"\n✨ DOUBLONS SUPPRIMÉS et TRI ALPHABÉTIQUE APPLIQUÉ")
    
    return len(result.inserted_ids)

if __name__ == "__main__":
    print("🔄 Mise à jour des sections transport, vêtements et tradition avec les données des images...")
    print("🧹 Suppression automatique des doublons et tri alphabétique...")
    count = update_transport_vetements_tradition()
    print(f"✅ Terminé ! {count} mots (transport + vêtements + tradition) mis à jour selon les images.")