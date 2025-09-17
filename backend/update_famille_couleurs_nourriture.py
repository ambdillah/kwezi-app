#!/usr/bin/env python3
"""
Script pour mettre à jour les sections "famille", "couleurs" et "nourriture" avec les données exactes des images fournies
"""

import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/mayotte_app")
client = MongoClient(MONGO_URL)
db = client.mayotte_app
words_collection = db.words

def update_famille_couleurs_nourriture():
    """Mettre à jour les sections famille, couleurs et nourriture avec les données exactes des images"""
    
    # Supprimer tous les mots existants des catégories "famille", "couleurs" et "nourriture"
    result_delete_famille = words_collection.delete_many({"category": "famille"})
    result_delete_couleurs = words_collection.delete_many({"category": "couleurs"})
    result_delete_nourriture = words_collection.delete_many({"category": "nourriture"})
    print(f"🗑️ Supprimé {result_delete_famille.deleted_count} anciens mots de famille")
    print(f"🗑️ Supprimé {result_delete_couleurs.deleted_count} anciennes couleurs")
    print(f"🗑️ Supprimé {result_delete_nourriture.deleted_count} anciens mots de nourriture")
    
    # SECTION FAMILLE - 20 mots exacts selon l'image
    famille_vocabulary = [
        {"french": "tante", "shimaore": "mama titi bolé", "kibouchi": "nindri heli bé", "category": "famille", "image_url": "👩", "difficulty": 1},
        {"french": "oncle maternel", "shimaore": "zama", "kibouchi": "zama", "category": "famille", "image_url": "👨", "difficulty": 2},
        {"french": "oncle paternel", "shimaore": "baba titi bolé", "kibouchi": "baba heli bé", "category": "famille", "image_url": "👨", "difficulty": 2},
        {"french": "épouse oncle maternel", "shimaore": "zena", "kibouchi": "zena", "category": "famille", "image_url": "👩", "difficulty": 2},
        {"french": "petite sœur", "shimaore": "moinagna mtroumama", "kibouchi": "zandri", "category": "famille", "image_url": "👧", "difficulty": 1},
        {"french": "petit frère", "shimaore": "moinagna mtroubaba", "kibouchi": "zandri", "category": "famille", "image_url": "👦", "difficulty": 1},
        {"french": "grande sœur", "shimaore": "zouki mtroumché", "kibouchi": "zoki viavi", "category": "famille", "image_url": "👩", "difficulty": 1},
        {"french": "grand frère", "shimaore": "zouki mtroubaba", "kibouchi": "zoki lalahi", "category": "famille", "image_url": "👨", "difficulty": 1},
        {"french": "frère", "shimaore": "mwanagna mtroubaba", "kibouchi": "anadahi", "category": "famille", "image_url": "👦", "difficulty": 1},
        {"french": "sœur", "shimaore": "mwanagna mtroumama", "kibouchi": "anabavi", "category": "famille", "image_url": "👧", "difficulty": 1},
        {"french": "ami", "shimaore": "mwandzani", "kibouchi": "mwandzani", "category": "famille", "image_url": "👫", "difficulty": 1},
        {"french": "fille/femme", "shimaore": "mtroumama", "kibouchi": "viavi", "category": "famille", "image_url": "👩", "difficulty": 1},
        {"french": "garçon/homme", "shimaore": "mtroubaba", "kibouchi": "lalahi", "category": "famille", "image_url": "👨", "difficulty": 1},
        {"french": "monsieur", "shimaore": "mogné", "kibouchi": "lalahi", "category": "famille", "image_url": "👨", "difficulty": 1},
        {"french": "grand-père", "shimaore": "bacoco", "kibouchi": "dadayi", "category": "famille", "image_url": "👴", "difficulty": 1},
        {"french": "grand-mère", "shimaore": "coco", "kibouchi": "dadi", "category": "famille", "image_url": "👵", "difficulty": 1},
        {"french": "madame", "shimaore": "bwéni", "kibouchi": "viavi", "category": "famille", "image_url": "👩", "difficulty": 1},
        {"french": "famille", "shimaore": "mdjamaza", "kibouchi": "havagna", "category": "famille", "image_url": "👨‍👩‍👧‍👦", "difficulty": 1},
        {"french": "papa", "shimaore": "baba", "kibouchi": "baba", "category": "famille", "image_url": "👨", "difficulty": 1},
        {"french": "maman", "shimaore": "mama", "kibouchi": "mama", "category": "famille", "image_url": "👩", "difficulty": 1},
    ]
    
    # SECTION COULEURS - 8 mots exacts selon l'image
    couleurs_vocabulary = [
        {"french": "bleu", "shimaore": "bilé", "kibouchi": "bilé", "category": "couleurs", "image_url": "🔵", "difficulty": 1},
        {"french": "vert", "shimaore": "dhavou", "kibouchi": "mayitsou", "category": "couleurs", "image_url": "🟢", "difficulty": 1},
        {"french": "noir", "shimaore": "nzidhou", "kibouchi": "mayintigni", "category": "couleurs", "image_url": "⚫", "difficulty": 1},
        {"french": "blanc", "shimaore": "ndjéou", "kibouchi": "malandi", "category": "couleurs", "image_url": "⚪", "difficulty": 1},
        {"french": "jaune", "shimaore": "dzindzano", "kibouchi": "tamoutamou", "category": "couleurs", "image_url": "🟡", "difficulty": 1},
        {"french": "rouge", "shimaore": "nzoukoundrou", "kibouchi": "mena", "category": "couleurs", "image_url": "🔴", "difficulty": 1},
        {"french": "gris", "shimaore": "djifou", "kibouchi": "dzofou", "category": "couleurs", "image_url": "⚫", "difficulty": 1},
        {"french": "marron", "shimaore": "trotro", "kibouchi": "fotafotaka", "category": "couleurs", "image_url": "🟤", "difficulty": 1},
    ]
    
    # SECTION NOURRITURE - 42 mots exacts selon l'image
    nourriture_vocabulary = [
        {"french": "riz", "shimaore": "tsoholé", "kibouchi": "vari", "category": "nourriture", "image_url": "🍚", "difficulty": 1},
        {"french": "eau", "shimaore": "maji", "kibouchi": "ranou", "category": "nourriture", "image_url": "💧", "difficulty": 1},
        {"french": "nourriture", "shimaore": "chaoula", "kibouchi": "hanigni", "category": "nourriture", "image_url": "🍽️", "difficulty": 1},
        {"french": "ananas", "shimaore": "nanassi", "kibouchi": "mananassi", "category": "nourriture", "image_url": "🍍", "difficulty": 1},
        {"french": "pois d'angole", "shimaore": "tsouzi", "kibouchi": "ambatri", "category": "nourriture", "image_url": "🫘", "difficulty": 1},
        {"french": "banane", "shimaore": "trovi", "kibouchi": "hountsi", "category": "nourriture", "image_url": "🍌", "difficulty": 1},
        {"french": "pain", "shimaore": "dipé", "kibouchi": "dipé", "category": "nourriture", "image_url": "🍞", "difficulty": 1},
        {"french": "gâteau", "shimaore": "mharé", "kibouchi": "moukari", "category": "nourriture", "image_url": "🍰", "difficulty": 1},
        {"french": "mangue", "shimaore": "manga", "kibouchi": "manga", "category": "nourriture", "image_url": "🥭", "difficulty": 1},
        {"french": "noix de coco", "shimaore": "nadzi", "kibouchi": "voiniou", "category": "nourriture", "image_url": "🥥", "difficulty": 1},
        {"french": "noix de coco fraîche", "shimaore": "chijavou", "kibouchi": "kidjayou", "category": "nourriture", "image_url": "🥥", "difficulty": 1},
        {"french": "lait", "shimaore": "dzia", "kibouchi": "rounounou", "category": "nourriture", "image_url": "🥛", "difficulty": 1},
        {"french": "viande", "shimaore": "nhyama", "kibouchi": "amboumati", "category": "nourriture", "image_url": "🥩", "difficulty": 1},
        {"french": "poisson", "shimaore": "fi", "kibouchi": "lokou", "category": "nourriture", "image_url": "🐟", "difficulty": 1},
        {"french": "brèdes", "shimaore": "féliki", "kibouchi": "féliki", "category": "nourriture", "image_url": "🥬", "difficulty": 1},
        {"french": "brède mafane", "shimaore": "féliki mafana", "kibouchi": "féliki mafana", "category": "nourriture", "image_url": "🥬", "difficulty": 1},
        {"french": "brède manioc", "shimaore": "mataba", "kibouchi": "féliki mouhogou", "category": "nourriture", "image_url": "🥬", "difficulty": 1},
        {"french": "brède morelle", "shimaore": "féliki nyongo", "kibouchi": "féliki angatsindra", "category": "nourriture", "image_url": "🥬", "difficulty": 1},
        {"french": "brès patate douce", "shimaore": "féliki batata", "kibouchi": "féliki batata", "category": "nourriture", "image_url": "🥬", "difficulty": 1},
        {"french": "patate douce", "shimaore": "batata", "kibouchi": "batata", "category": "nourriture", "image_url": "🍠", "difficulty": 1},
        {"french": "bouillon", "shimaore": "woubou", "kibouchi": "kouba", "category": "nourriture", "image_url": "🍲", "difficulty": 1},
        {"french": "banane au coco", "shimaore": "trovi ya nadzi", "kibouchi": "hountsi an voiniou", "category": "nourriture", "image_url": "🍌", "difficulty": 1},
        {"french": "riz au coco", "shimaore": "tsoholé ya nadzi", "kibouchi": "vari an voiniou", "category": "nourriture", "image_url": "🍚", "difficulty": 1},
        {"french": "poulet", "shimaore": "bawa", "kibouchi": "mabawa", "category": "nourriture", "image_url": "🐔", "difficulty": 1},
        {"french": "œuf", "shimaore": "joiyi", "kibouchi": "antoudi", "category": "nourriture", "image_url": "🥚", "difficulty": 1},
        {"french": "tomate", "shimaore": "tamati", "kibouchi": "matimati", "category": "nourriture", "image_url": "🍅", "difficulty": 1},
        {"french": "oignon", "shimaore": "chouroungou", "kibouchi": "doungoulou", "category": "nourriture", "image_url": "🧅", "difficulty": 1},
        {"french": "ail", "shimaore": "chouroungou foudjé", "kibouchi": "doungoulou mvoudjou", "category": "nourriture", "image_url": "🧄", "difficulty": 1},
        {"french": "orange", "shimaore": "troundra", "kibouchi": "tsoha", "category": "nourriture", "image_url": "🍊", "difficulty": 1},
        {"french": "mandarine", "shimaore": "madhandzé", "kibouchi": "tsoha madzandzi", "category": "nourriture", "image_url": "🍊", "difficulty": 1},
        {"french": "manioc", "shimaore": "mhogo", "kibouchi": "mouhogou", "category": "nourriture", "image_url": "🥔", "difficulty": 1},
        {"french": "piment", "shimaore": "poutou", "kibouchi": "pilipili", "category": "nourriture", "image_url": "🌶️", "difficulty": 1},
        {"french": "taro", "shimaore": "majimbi", "kibouchi": "majimbi", "category": "nourriture", "image_url": "🥔", "difficulty": 1},
        {"french": "sel", "shimaore": "chingo", "kibouchi": "sira", "category": "nourriture", "image_url": "🧂", "difficulty": 1},
        {"french": "poivre", "shimaore": "bvilibvili manga", "kibouchi": "vilivili", "category": "nourriture", "image_url": "🌶️", "difficulty": 1},
        {"french": "curcuma", "shimaore": "dzindzano", "kibouchi": "tamoutamou", "category": "nourriture", "image_url": "🌿", "difficulty": 1},
        {"french": "cumin", "shimaore": "massala", "kibouchi": "massala", "category": "nourriture", "image_url": "🌿", "difficulty": 1},
        {"french": "ciboulette", "shimaore": "chouroungou", "kibouchi": "doungoulou ravigni", "category": "nourriture", "image_url": "🌿", "difficulty": 1},
        {"french": "gingembre", "shimaore": "tsinguiziou", "kibouchi": "sakéyi", "category": "nourriture", "image_url": "🫚", "difficulty": 1},
        {"french": "vanille", "shimaore": "lavani", "kibouchi": "lavani", "category": "nourriture", "image_url": "🌿", "difficulty": 1},
        {"french": "tamarin", "shimaore": "ouhajou", "kibouchi": "madirou kakazou", "category": "nourriture", "image_url": "🌰", "difficulty": 1},
        {"french": "un thé", "shimaore": "maji ya moro", "kibouchi": "ranou meyi", "category": "nourriture", "image_url": "🍵", "difficulty": 1},
        {"french": "papaye", "shimaore": "papaya", "kibouchi": "poipoiya", "category": "nourriture", "image_url": "🥭", "difficulty": 1},
        {"french": "nourriture", "shimaore": "chaoula", "kibouchi": "hanigni", "category": "nourriture", "image_url": "🍽️", "difficulty": 1},
        {"french": "riz non décortiqué", "shimaore": "melé", "kibouchi": "vari tsivoidissa", "category": "nourriture", "image_url": "🌾", "difficulty": 1},
    ]
    
    # Ajouter timestamp à chaque mot
    all_vocabulary = famille_vocabulary + couleurs_vocabulary + nourriture_vocabulary
    for word in all_vocabulary:
        word["created_at"] = datetime.utcnow()
    
    # Insérer tous les nouveaux mots
    result = words_collection.insert_many(all_vocabulary)
    
    print(f"✅ Sections famille, couleurs et nourriture mises à jour : {len(result.inserted_ids)} mots ajoutés")
    print(f"📊 Famille : {len(famille_vocabulary)} mots")
    print(f"📊 Couleurs : {len(couleurs_vocabulary)} mots")
    print(f"📊 Nourriture : {len(nourriture_vocabulary)} mots")
    
    # Vérification
    total_words = words_collection.count_documents({})
    famille_count = words_collection.count_documents({"category": "famille"})
    couleurs_count = words_collection.count_documents({"category": "couleurs"})  
    nourriture_count = words_collection.count_documents({"category": "nourriture"})
    
    print(f"\n📈 STATISTIQUES MISES À JOUR :")
    print(f"   Total des mots dans la base : {total_words}")
    print(f"   Mots dans la catégorie famille : {famille_count}")
    print(f"   Mots dans la catégorie couleurs : {couleurs_count}")
    print(f"   Mots dans la catégorie nourriture : {nourriture_count}")
    
    return len(result.inserted_ids)

if __name__ == "__main__":
    print("🔄 Mise à jour des sections famille, couleurs et nourriture avec les données des images...")
    count = update_famille_couleurs_nourriture()
    print(f"✅ Terminé ! {count} mots (famille + couleurs + nourriture) mis à jour selon les images.")