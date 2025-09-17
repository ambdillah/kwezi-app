#!/usr/bin/env python3
"""
Script pour mettre à jour uniquement la section "nature" avec les données exactes de l'image fournie
"""

import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/mayotte_app")
client = MongoClient(MONGO_URL)
db = client.mayotte_app
words_collection = db.words

def update_nature_section():
    """Mettre à jour uniquement la section nature avec les données exactes de l'image"""
    
    # Supprimer tous les mots existants de la catégorie "nature"
    result_delete = words_collection.delete_many({"category": "nature"})
    print(f"🗑️ Supprimé {result_delete.deleted_count} anciens mots de la catégorie nature")
    
    # Nouveau vocabulaire de nature exact selon l'image fournie
    nature_vocabulary = [
        {"french": "pente/colline/mont", "shimaore": "mlima", "kibouchi": "boungou", "category": "nature", "image_url": "⛰️", "difficulty": 1},
        {"french": "lune", "shimaore": "mwézi", "kibouchi": "fandzava", "category": "nature", "image_url": "🌙", "difficulty": 1},
        {"french": "étoile", "shimaore": "gnora", "kibouchi": "lakintagna", "category": "nature", "image_url": "⭐", "difficulty": 1},
        {"french": "sable", "shimaore": "mtsanga", "kibouchi": "fasigni", "category": "nature", "image_url": "🏖️", "difficulty": 1},
        {"french": "vague", "shimaore": "dhouja", "kibouchi": "houndza/riaka", "category": "nature", "image_url": "🌊", "difficulty": 1},
        {"french": "vent", "shimaore": "pévo", "kibouchi": "tsikou", "category": "nature", "image_url": "🌬️", "difficulty": 1},
        {"french": "pluie", "shimaore": "vhoua", "kibouchi": "mahaléni", "category": "nature", "image_url": "🌧️", "difficulty": 1},
        {"french": "mangrove", "shimaore": "mhonko", "kibouchi": "honkou", "category": "nature", "image_url": "🌿", "difficulty": 1},
        {"french": "corail", "shimaore": "soiyi", "kibouchi": "soiyi", "category": "nature", "image_url": "🪸", "difficulty": 1},
        {"french": "barrière de corail", "shimaore": "caléni", "kibouchi": "caléni", "category": "nature", "image_url": "🪸", "difficulty": 2},
        {"french": "tempête", "shimaore": "darouba", "kibouchi": "tsikou", "category": "nature", "image_url": "⛈️", "difficulty": 1},
        {"french": "rivière", "shimaore": "mouro", "kibouchi": "mouroni", "category": "nature", "image_url": "🏞️", "difficulty": 1},
        {"french": "pont", "shimaore": "daradja", "kibouchi": "daradja", "category": "nature", "image_url": "🌉", "difficulty": 1},
        {"french": "nuage", "shimaore": "wingou", "kibouchi": "vingou", "category": "nature", "image_url": "☁️", "difficulty": 1},
        {"french": "arc en ciel", "shimaore": "mcacamba", "kibouchi": "", "category": "nature", "image_url": "🌈", "difficulty": 1},
        {"french": "campagne/forêt", "shimaore": "malavouni", "kibouchi": "atihala", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "caillou/pierre/rocher", "shimaore": "bwé", "kibouchi": "vatou", "category": "nature", "image_url": "🪨", "difficulty": 1},
        {"french": "plateau", "shimaore": "bandra", "kibouchi": "kètraka", "category": "nature", "image_url": "🏔️", "difficulty": 1},
        {"french": "chemin/sentier/parcours", "shimaore": "ndzia", "kibouchi": "lalagna", "category": "nature", "image_url": "🛤️", "difficulty": 1},
        {"french": "herbe", "shimaore": "malavou", "kibouchi": "haitri", "category": "nature", "image_url": "🌱", "difficulty": 1},
        {"french": "fleur", "shimaore": "foulera", "kibouchi": "foulera", "category": "nature", "image_url": "🌸", "difficulty": 1},
        {"french": "soleil", "shimaore": "jouwa", "kibouchi": "zouva", "category": "nature", "image_url": "☀️", "difficulty": 1},
        {"french": "mer", "shimaore": "bahari", "kibouchi": "bahari", "category": "nature", "image_url": "🌊", "difficulty": 1},
        {"french": "plage", "shimaore": "mtsangani", "kibouchi": "fassigni", "category": "nature", "image_url": "🏖️", "difficulty": 1},
        {"french": "arbre", "shimaore": "mwiri", "kibouchi": "kakazou", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "rue/route", "shimaore": "paré", "kibouchi": "paré", "category": "nature", "image_url": "🛣️", "difficulty": 1},
        {"french": "bananier", "shimaore": "trindri", "kibouchi": "voudi ni hountsi", "category": "nature", "image_url": "🌴", "difficulty": 1},
        {"french": "feuille", "shimaore": "mawoini", "kibouchi": "hayitri", "category": "nature", "image_url": "🍃", "difficulty": 1},
        {"french": "branche", "shimaore": "trahi", "kibouchi": "trahi", "category": "nature", "image_url": "🌿", "difficulty": 1},
        {"french": "tornade", "shimaore": "ouzimouyi", "kibouchi": "tsikou soulaimana", "category": "nature", "image_url": "🌪️", "difficulty": 1},
        {"french": "cocotier", "shimaore": "m'nadzi", "kibouchi": "voudi ni vwaniou", "category": "nature", "image_url": "🌴", "difficulty": 1},
        {"french": "arbre à pain", "shimaore": "m'frampé", "kibouchi": "voudi ni frampé", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "baobab", "shimaore": "m'bouyou", "kibouchi": "voudi ni bouyou", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "bambou", "shimaore": "m'banbo", "kibouchi": "valiha", "category": "nature", "image_url": "🎋", "difficulty": 1},
        {"french": "manguier", "shimaore": "m'manga", "kibouchi": "voudi ni manga", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "jacquier", "shimaore": "m'fénéssi", "kibouchi": "voudi ni finéssi", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "terre", "shimaore": "trotro", "kibouchi": "fotaka", "category": "nature", "image_url": "🌍", "difficulty": 1},
        {"french": "sol", "shimaore": "chivandré ya tsi", "kibouchi": "tani", "category": "nature", "image_url": "🌍", "difficulty": 1},
        {"french": "érosion", "shimaore": "padza", "kibouchi": "padza", "category": "nature", "image_url": "🌊", "difficulty": 2},
        {"french": "marée basse", "shimaore": "maji yavo", "kibouchi": "ranou mèki", "category": "nature", "image_url": "🌊", "difficulty": 2},
        {"french": "platier", "shimaore": "kalé", "kibouchi": "kaléni", "category": "nature", "image_url": "🪨", "difficulty": 2},
        {"french": "marée haute", "shimaore": "maji yamalé", "kibouchi": "ranou fénou", "category": "nature", "image_url": "🌊", "difficulty": 2},
        {"french": "inondé", "shimaore": "ourora", "kibouchi": "dobou", "category": "nature", "image_url": "🌊", "difficulty": 2},
        {"french": "sauvage", "shimaore": "nyéha", "kibouchi": "di", "category": "nature", "image_url": "🌿", "difficulty": 1},
        {"french": "canne à sucre", "shimaore": "mouwoi", "kibouchi": "fari", "category": "nature", "image_url": "🌾", "difficulty": 1},
        {"french": "fagot", "shimaore": "kouni", "kibouchi": "azoumati", "category": "nature", "image_url": "🪵", "difficulty": 1},
        {"french": "pirogue", "shimaore": "laka", "kibouchi": "laka", "category": "nature", "image_url": "🛶", "difficulty": 1},
        {"french": "vedette", "shimaore": "kwassa kwassa", "kibouchi": "vidéti", "category": "nature", "image_url": "🚤", "difficulty": 1},
        {"french": "école", "shimaore": "licoli", "kibouchi": "licoli", "category": "nature", "image_url": "🏫", "difficulty": 1},
        {"french": "école coranique", "shimaore": "shioni", "kibouchi": "kioni", "category": "nature", "image_url": "🕌", "difficulty": 1},
    ]
    
    # Ajouter timestamp à chaque mot
    for word in nature_vocabulary:
        word["created_at"] = datetime.utcnow()
    
    # Insérer tous les nouveaux mots de nature
    result = words_collection.insert_many(nature_vocabulary)
    
    print(f"✅ Section nature mise à jour : {len(result.inserted_ids)} mots ajoutés")
    print(f"📊 Nouveaux mots de nature : {len(nature_vocabulary)} mots exacts selon l'image")
    
    # Vérification
    total_words = words_collection.count_documents({})
    nature_count = words_collection.count_documents({"category": "nature"})
    
    print(f"\n📈 STATISTIQUES MISES À JOUR :")
    print(f"   Total des mots dans la base : {total_words}")
    print(f"   Mots dans la catégorie nature : {nature_count}")
    
    return len(result.inserted_ids)

if __name__ == "__main__":
    print("🔄 Mise à jour de la section nature avec les données de l'image...")
    count = update_nature_section()
    print(f"✅ Terminé ! {count} mots de nature mis à jour selon l'image.")