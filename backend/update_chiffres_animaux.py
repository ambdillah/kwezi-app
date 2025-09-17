#!/usr/bin/env python3
"""
Script pour mettre à jour les sections "chiffres" et "animaux" avec les données exactes des images fournies
"""

import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/mayotte_app")
client = MongoClient(MONGO_URL)
db = client.mayotte_app
words_collection = db.words

def update_chiffres_and_animaux():
    """Mettre à jour les sections chiffres et animaux avec les données exactes des images"""
    
    # Supprimer tous les mots existants des catégories "nombres" et "animaux"
    result_delete_chiffres = words_collection.delete_many({"category": "nombres"})
    result_delete_animaux = words_collection.delete_many({"category": "animaux"})
    print(f"🗑️ Supprimé {result_delete_chiffres.deleted_count} anciens chiffres")
    print(f"🗑️ Supprimé {result_delete_animaux.deleted_count} anciens animaux")
    
    # SECTION CHIFFRES - 20 mots exacts selon l'image
    chiffres_vocabulary = [
        {"french": "un", "shimaore": "moja", "kibouchi": "areki", "category": "chiffre", "image_url": "1️⃣", "difficulty": 1},
        {"french": "deux", "shimaore": "mbili", "kibouchi": "aroyi", "category": "chiffre", "image_url": "2️⃣", "difficulty": 1},
        {"french": "trois", "shimaore": "trarou", "kibouchi": "telou", "category": "chiffre", "image_url": "3️⃣", "difficulty": 1},
        {"french": "quatre", "shimaore": "nhé", "kibouchi": "efatra", "category": "chiffre", "image_url": "4️⃣", "difficulty": 1},
        {"french": "cinq", "shimaore": "tsano", "kibouchi": "dimi", "category": "chiffre", "image_url": "5️⃣", "difficulty": 1},
        {"french": "six", "shimaore": "sita", "kibouchi": "tchouta", "category": "chiffre", "image_url": "6️⃣", "difficulty": 1},
        {"french": "sept", "shimaore": "saba", "kibouchi": "fitou", "category": "chiffre", "image_url": "7️⃣", "difficulty": 1},
        {"french": "huit", "shimaore": "nané", "kibouchi": "valou", "category": "chiffre", "image_url": "8️⃣", "difficulty": 1},
        {"french": "neuf", "shimaore": "chendra", "kibouchi": "civi", "category": "chiffre", "image_url": "9️⃣", "difficulty": 1},
        {"french": "dix", "shimaore": "koumi", "kibouchi": "foulou", "category": "chiffre", "image_url": "🔟", "difficulty": 1},
        {"french": "onze", "shimaore": "koumi na moja", "kibouchi": "foulou areki ambi", "category": "chiffre", "image_url": "1️⃣1️⃣", "difficulty": 2},
        {"french": "douze", "shimaore": "koumi na mbili", "kibouchi": "foulou aroyi ambi", "category": "chiffre", "image_url": "1️⃣2️⃣", "difficulty": 2},
        {"french": "treize", "shimaore": "koumi na trarou", "kibouchi": "foulou telou ambi", "category": "chiffre", "image_url": "1️⃣3️⃣", "difficulty": 2},
        {"french": "quatorze", "shimaore": "koumi na nhé", "kibouchi": "foulou efatra ambi", "category": "chiffre", "image_url": "1️⃣4️⃣", "difficulty": 2},
        {"french": "quinze", "shimaore": "koumi na tsano", "kibouchi": "foulou dimi ambi", "category": "chiffre", "image_url": "1️⃣5️⃣", "difficulty": 2},
        {"french": "seize", "shimaore": "koumi na sita", "kibouchi": "foulou tchouta ambi", "category": "chiffre", "image_url": "1️⃣6️⃣", "difficulty": 2},
        {"french": "dix-sept", "shimaore": "koumi na saba", "kibouchi": "foulou fitou ambi", "category": "chiffre", "image_url": "1️⃣7️⃣", "difficulty": 2},
        {"french": "dix-huit", "shimaore": "koumi na nané", "kibouchi": "foulou valou ambi", "category": "chiffre", "image_url": "1️⃣8️⃣", "difficulty": 2},
        {"french": "dix-neuf", "shimaore": "koumi na chendra", "kibouchi": "foulou civi ambi", "category": "chiffre", "image_url": "1️⃣9️⃣", "difficulty": 2},
        {"french": "vingt", "shimaore": "chirini", "kibouchi": "arompoulou", "category": "chiffre", "image_url": "2️⃣0️⃣", "difficulty": 2},
    ]
    
    # SECTION ANIMAUX - 68 mots exacts selon l'image
    animaux_vocabulary = [
        {"french": "cochon", "shimaore": "pouroukou", "kibouchi": "lambou", "category": "animal", "image_url": "🐷", "difficulty": 1},
        {"french": "margouillat", "shimaore": "kasangwe", "kibouchi": "kitsatsaka", "category": "animal", "image_url": "🦎", "difficulty": 1},
        {"french": "abeille", "shimaore": "niochi", "kibouchi": "antéli", "category": "animal", "image_url": "🐝", "difficulty": 1},
        {"french": "chat", "shimaore": "paha", "kibouchi": "moirou", "category": "animal", "image_url": "🐱", "difficulty": 1},
        {"french": "rat", "shimaore": "pouhou", "kibouchi": "voilavou", "category": "animal", "image_url": "🐭", "difficulty": 1},
        {"french": "escargot", "shimaore": "kwa", "kibouchi": "ancora", "category": "animal", "image_url": "🐌", "difficulty": 1},
        {"french": "lion", "shimaore": "simba", "kibouchi": "simba", "category": "animal", "image_url": "🦁", "difficulty": 1},
        {"french": "grenouille", "shimaore": "shiwatrotro", "kibouchi": "sahougnou", "category": "animal", "image_url": "🐸", "difficulty": 1},
        {"french": "oiseau", "shimaore": "gnougni", "kibouchi": "vorougnou", "category": "animal", "image_url": "🐦", "difficulty": 1},
        {"french": "chien", "shimaore": "mbwa", "kibouchi": "fadroka", "category": "animal", "image_url": "🐶", "difficulty": 1},
        {"french": "poisson", "shimaore": "fi", "kibouchi": "lokou", "category": "animal", "image_url": "🐟", "difficulty": 1},
        {"french": "maki", "shimaore": "komba", "kibouchi": "amkoumba", "category": "animal", "image_url": "🐒", "difficulty": 1},
        {"french": "chèvre", "shimaore": "mbouzi", "kibouchi": "bengui", "category": "animal", "image_url": "🐐", "difficulty": 1},
        {"french": "moustique", "shimaore": "manundi", "kibouchi": "mokou", "category": "animal", "image_url": "🦟", "difficulty": 1},
        {"french": "mouche", "shimaore": "ndzi", "kibouchi": "lalitri", "category": "animal", "image_url": "🪰", "difficulty": 1},
        {"french": "chauve souris", "shimaore": "drema", "kibouchi": "fanihi", "category": "animal", "image_url": "🦇", "difficulty": 1},
        {"french": "serpent", "shimaore": "nyoha", "kibouchi": "bibi lava", "category": "animal", "image_url": "🐍", "difficulty": 1},
        {"french": "lapin", "shimaore": "sungura", "kibouchi": "shoungoura", "category": "animal", "image_url": "🐰", "difficulty": 1},
        {"french": "canard", "shimaore": "guisi", "kibouchi": "doukitri", "category": "animal", "image_url": "🦆", "difficulty": 1},
        {"french": "mouton", "shimaore": "baribari", "kibouchi": "baribari", "category": "animal", "image_url": "🐑", "difficulty": 1},
        {"french": "crocodile", "shimaore": "vwai", "kibouchi": "vwai", "category": "animal", "image_url": "🐊", "difficulty": 1},
        {"french": "caméléon", "shimaore": "tarundru", "kibouchi": "tarondru", "category": "animal", "image_url": "🦎", "difficulty": 1},
        {"french": "zébu", "shimaore": "nyombé", "kibouchi": "aoumbi", "category": "animal", "image_url": "🐂", "difficulty": 1},
        {"french": "âne", "shimaore": "pundra", "kibouchi": "ampundra", "category": "animal", "image_url": "🫏", "difficulty": 1},
        {"french": "poule", "shimaore": "kouhou", "kibouchi": "akohou", "category": "animal", "image_url": "🐔", "difficulty": 1},
        {"french": "pigeon", "shimaore": "ndiwa", "kibouchi": "indiwa", "category": "animal", "image_url": "🕊️", "difficulty": 1},
        {"french": "fourmis", "shimaore": "tsossou", "kibouchi": "vitsiki", "category": "animal", "image_url": "🐜", "difficulty": 1},
        {"french": "chenille", "shimaore": "bazi", "kibouchi": "bibimanguidi", "category": "animal", "image_url": "🐛", "difficulty": 1},
        {"french": "papillon", "shimaore": "pelapelaka", "kibouchi": "tsipelapelaka", "category": "animal", "image_url": "🦋", "difficulty": 1},
        {"french": "ver de terre", "shimaore": "lingoui lingoui", "kibouchi": "bibi fotaka", "category": "animal", "image_url": "🪱", "difficulty": 1},
        {"french": "criquet", "shimaore": "furudji", "kibouchi": "kidzedza", "category": "animal", "image_url": "🦗", "difficulty": 1},
        {"french": "cheval", "shimaore": "poundra", "kibouchi": "farassi", "category": "animal", "image_url": "🐴", "difficulty": 1},
        {"french": "fruit du jaquier", "shimaore": "fénéssi", "kibouchi": "finéssi", "category": "animal", "image_url": "🥭", "difficulty": 1},
        {"french": "perroquet", "shimaore": "kasoukou", "kibouchi": "kararokou", "category": "animal", "image_url": "🦜", "difficulty": 1},
        {"french": "cafard", "shimaore": "kalalawi", "kibouchi": "kalalowou", "category": "animal", "image_url": "🪳", "difficulty": 1},
        {"french": "araignée", "shimaore": "shitrandrabwibwi", "kibouchi": "bibi ampamani massou", "category": "animal", "image_url": "🕷️", "difficulty": 1},
        {"french": "scorpion", "shimaore": "hala", "kibouchi": "hala", "category": "animal", "image_url": "🦂", "difficulty": 1},
        {"french": "scolopendre", "shimaore": "trambwi", "kibouchi": "trambougnou", "category": "animal", "image_url": "🐛", "difficulty": 1},
        {"french": "thon", "shimaore": "mbassi", "kibouchi": "mbassi", "category": "animal", "image_url": "🐟", "difficulty": 1},
        {"french": "requin", "shimaore": "papa", "kibouchi": "ankiou", "category": "animal", "image_url": "🦈", "difficulty": 1},
        {"french": "poulpe", "shimaore": "pwedza", "kibouchi": "pwedza", "category": "animal", "image_url": "🐙", "difficulty": 1},
        {"french": "crabe", "shimaore": "dradraka", "kibouchi": "dakatra", "category": "animal", "image_url": "🦀", "difficulty": 1},
        {"french": "tortue", "shimaore": "nyamba/katsa", "kibouchi": "fanou", "category": "animal", "image_url": "🐢", "difficulty": 1},
        {"french": "bigorno", "shimaore": "trondro", "kibouchi": "trondrou", "category": "animal", "image_url": "🐚", "difficulty": 1},
        {"french": "éléphant", "shimaore": "ndovu", "kibouchi": "ndovu", "category": "animal", "image_url": "🐘", "difficulty": 1},
        {"french": "singe", "shimaore": "djakwe", "kibouchi": "djakouayi", "category": "animal", "image_url": "🐒", "difficulty": 1},
        {"french": "souris", "shimaore": "shikwetse", "kibouchi": "voilavou", "category": "animal", "image_url": "🐭", "difficulty": 1},
        {"french": "phacochère", "shimaore": "pouruku nyeha", "kibouchi": "lambou", "category": "animal", "image_url": "🐗", "difficulty": 1},
        {"french": "lézard", "shimaore": "ngwizi", "kibouchi": "kitsatsaka", "category": "animal", "image_url": "🦎", "difficulty": 1},
        {"french": "renard", "shimaore": "mbwa nyeha", "kibouchi": "fandroka", "category": "animal", "image_url": "🦊", "difficulty": 1},
        {"french": "chameau", "shimaore": "ngamia", "kibouchi": "angamia", "category": "animal", "image_url": "🐪", "difficulty": 1},
        {"french": "escargot", "shimaore": "kowa", "kibouchi": "ankora", "category": "animal", "image_url": "🐌", "difficulty": 1},
        {"french": "hérisson/tangue", "shimaore": "landra", "kibouchi": "trandraka", "category": "animal", "image_url": "🦔", "difficulty": 1},
        {"french": "corbeau", "shimaore": "gawa/kwayi", "kibouchi": "gouaka", "category": "animal", "image_url": "🐦‍⬛", "difficulty": 1},
        {"french": "civette", "shimaore": "founga", "kibouchi": "angava", "category": "animal", "image_url": "🦝", "difficulty": 1},
        {"french": "dauphin", "shimaore": "moungoumé", "kibouchi": "fésoutrou", "category": "animal", "image_url": "🐬", "difficulty": 1},
        {"french": "baleine", "shimaore": "ndroujou", "kibouchi": "", "category": "animal", "image_url": "🐋", "difficulty": 1},
        {"french": "crevette", "shimaore": "camba", "kibouchi": "ancamba", "category": "animal", "image_url": "🦐", "difficulty": 1},
        {"french": "frelon", "shimaore": "chonga", "kibouchi": "faraka", "category": "animal", "image_url": "🐝", "difficulty": 1},
        {"french": "guêpe", "shimaore": "movou", "kibouchi": "fanintri", "category": "animal", "image_url": "🐝", "difficulty": 1},
        {"french": "bourdon", "shimaore": "vungo vungo", "kibouchi": "madjaoumbi", "category": "animal", "image_url": "🐝", "difficulty": 1},
        {"french": "puce", "shimaore": "kunguni", "kibouchi": "ancongou", "category": "animal", "image_url": "🐛", "difficulty": 1},
        {"french": "pou", "shimaore": "ndra", "kibouchi": "howou", "category": "animal", "image_url": "🐛", "difficulty": 1},
        {"french": "bouc", "shimaore": "béwé", "kibouchi": "béberou", "category": "animal", "image_url": "🐐", "difficulty": 1},
        {"french": "taureau", "shimaore": "kondzo", "kibouchi": "dzow", "category": "animal", "image_url": "🐂", "difficulty": 1},
        {"french": "bigorneau", "shimaore": "trondro", "kibouchi": "trondrou", "category": "animal", "image_url": "🐚", "difficulty": 1},
        {"french": "lambis", "shimaore": "kombé", "kibouchi": "mahombi", "category": "animal", "image_url": "🐚", "difficulty": 1},
        {"french": "cône de mer", "shimaore": "kwitsi", "kibouchi": "tsimtipaka", "category": "animal", "image_url": "🐚", "difficulty": 1},
        {"french": "mille pattes", "shimaore": "gnamaré", "kibouchi": "kamara", "category": "animal", "image_url": "🐛", "difficulty": 1},
        {"french": "oursin", "shimaore": "mjongo", "kibouchi": "acoudafitri", "category": "animal", "image_url": "🦔", "difficulty": 1},
        {"french": "huître", "shimaore": "gadzassi", "kibouchi": "vouli vavi", "category": "animal", "image_url": "🦪", "difficulty": 1},
    ]
    
    # Ajouter timestamp à chaque mot
    all_vocabulary = chiffres_vocabulary + animaux_vocabulary
    for word in all_vocabulary:
        word["created_at"] = datetime.utcnow()
    
    # Insérer tous les nouveaux mots
    result = words_collection.insert_many(all_vocabulary)
    
    print(f"✅ Sections chiffres et animaux mises à jour : {len(result.inserted_ids)} mots ajoutés")
    print(f"📊 Chiffres : {len(chiffres_vocabulary)} mots")
    print(f"📊 Animaux : {len(animaux_vocabulary)} mots")
    
    # Vérification
    total_words = words_collection.count_documents({})
    chiffres_count = words_collection.count_documents({"category": "chiffre"})
    animaux_count = words_collection.count_documents({"category": "animal"})
    
    print(f"\n📈 STATISTIQUES MISES À JOUR :")
    print(f"   Total des mots dans la base : {total_words}")
    print(f"   Mots dans la catégorie chiffre : {chiffres_count}")
    print(f"   Mots dans la catégorie animal : {animaux_count}")
    
    return len(result.inserted_ids)

if __name__ == "__main__":
    print("🔄 Mise à jour des sections chiffres et animaux avec les données des images...")
    count = update_chiffres_and_animaux()
    print(f"✅ Terminé ! {count} mots (chiffres + animaux) mis à jour selon les images.")