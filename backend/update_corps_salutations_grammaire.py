#!/usr/bin/env python3
"""
Script pour mettre à jour les sections "corps", "salutations" et "grammaire" avec les données exactes des images fournies
"""

import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/mayotte_app")
client = MongoClient(MONGO_URL)
db = client.mayotte_app
words_collection = db.words

def update_corps_salutations_grammaire():
    """Mettre à jour les sections corps, salutations et grammaire avec les données exactes des images"""
    
    # Supprimer tous les mots existants des catégories "corps", "salutations" et "grammaire"
    result_delete_corps = words_collection.delete_many({"category": "corps"})
    result_delete_salutations = words_collection.delete_many({"category": "salutations"})
    result_delete_grammaire = words_collection.delete_many({"category": "grammaire"})
    print(f"🗑️ Supprimé {result_delete_corps.deleted_count} anciens mots de corps")
    print(f"🗑️ Supprimé {result_delete_salutations.deleted_count} anciennes salutations")
    print(f"🗑️ Supprimé {result_delete_grammaire.deleted_count} anciens mots de grammaire")
    
    # SECTION CORPS HUMAIN - 32 mots exacts selon l'image
    corps_vocabulary = [
        {"french": "œil", "shimaore": "matso", "kibouchi": "faninti", "category": "corps", "image_url": "👁️", "difficulty": 1},
        {"french": "nez", "shimaore": "poua", "kibouchi": "horougnou", "category": "corps", "image_url": "👃", "difficulty": 1},
        {"french": "oreille", "shimaore": "kiyo", "kibouchi": "soufigni", "category": "corps", "image_url": "👂", "difficulty": 1},
        {"french": "ongle", "shimaore": "kofou", "kibouchi": "angofou", "category": "corps", "image_url": "💅", "difficulty": 1},
        {"french": "front", "shimaore": "housso", "kibouchi": "lahara", "category": "corps", "image_url": "🤔", "difficulty": 1},
        {"french": "joue", "shimaore": "savou", "kibouchi": "fifi", "category": "corps", "image_url": "😊", "difficulty": 1},
        {"french": "dos", "shimaore": "mengo", "kibouchi": "vohou", "category": "corps", "image_url": "🫸", "difficulty": 1},
        {"french": "épaule", "shimaore": "bèga", "kibouchi": "haveyi", "category": "corps", "image_url": "💪", "difficulty": 1},
        {"french": "hanche", "shimaore": "trenga", "kibouchi": "tahezagna", "category": "corps", "image_url": "🫴", "difficulty": 1},
        {"french": "fesses", "shimaore": "shidzé/mvoumo", "kibouchi": "fouri", "category": "corps", "image_url": "🍑", "difficulty": 1},
        {"french": "main", "shimaore": "mhono", "kibouchi": "tanagna", "category": "corps", "image_url": "✋", "difficulty": 1},
        {"french": "tête", "shimaore": "shitsoi", "kibouchi": "louha", "category": "corps", "image_url": "🗣️", "difficulty": 1},
        {"french": "ventre", "shimaore": "mimba", "kibouchi": "kibou", "category": "corps", "image_url": "🤰", "difficulty": 1},
        {"french": "dent", "shimaore": "magno", "kibouchi": "hifi", "category": "corps", "image_url": "🦷", "difficulty": 1},
        {"french": "langue", "shimaore": "oulimé", "kibouchi": "lela", "category": "corps", "image_url": "👅", "difficulty": 1},
        {"french": "pied", "shimaore": "mindrou", "kibouchi": "viti", "category": "corps", "image_url": "🦶", "difficulty": 1},
        {"french": "lèvre", "shimaore": "dhomo", "kibouchi": "soungni", "category": "corps", "image_url": "👄", "difficulty": 1},
        {"french": "peau", "shimaore": "ngwezi", "kibouchi": "ngwezi", "category": "corps", "image_url": "🫱", "difficulty": 1},
        {"french": "cheveux", "shimaore": "gnélé", "kibouchi": "fagneya", "category": "corps", "image_url": "💇", "difficulty": 1},
        {"french": "doigts", "shimaore": "cha", "kibouchi": "tondrou", "category": "corps", "image_url": "👆", "difficulty": 1},
        {"french": "barbe", "shimaore": "ndrévou", "kibouchi": "somboutrou", "category": "corps", "image_url": "🧔", "difficulty": 1},
        {"french": "vagin", "shimaore": "ndzigni", "kibouchi": "tingui", "category": "corps", "image_url": "🫦", "difficulty": 2},
        {"french": "testicules", "shimaore": "kwendzé", "kibouchi": "vouangarou", "category": "corps", "image_url": "🥎", "difficulty": 2},
        {"french": "pénis", "shimaore": "mbo", "kibouchi": "kaboudzi", "category": "corps", "image_url": "🌶️", "difficulty": 2},
        {"french": "menton", "shimaore": "shlévou", "kibouchi": "sokou", "category": "corps", "image_url": "🫸", "difficulty": 1},
        {"french": "bouche", "shimaore": "hangno", "kibouchi": "vava", "category": "corps", "image_url": "👄", "difficulty": 1},
        {"french": "côtes", "shimaore": "bavou", "kibouchi": "mbavou", "category": "corps", "image_url": "🫁", "difficulty": 1},
        {"french": "sourcil", "shimaore": "tsi", "kibouchi": "ankwéssi", "category": "corps", "image_url": "🤨", "difficulty": 1},
        {"french": "cheville", "shimaore": "dzitso la pwédza", "kibouchi": "dzitso la pwédza", "category": "corps", "image_url": "🦶", "difficulty": 1},
        {"french": "cou", "shimaore": "tsingo", "kibouchi": "vouzougnou", "category": "corps", "image_url": "🗣️", "difficulty": 1},
        {"french": "cils", "shimaore": "kove", "kibouchi": "rambou faninti", "category": "corps", "image_url": "👁️", "difficulty": 1},
        {"french": "arrière du crâne", "shimaore": "komoi", "kibouchi": "kiroika", "category": "corps", "image_url": "🤯", "difficulty": 1},
    ]
    
    # SECTION SALUTATIONS - 8 mots exacts selon l'image
    salutations_vocabulary = [
        {"french": "bonjour", "shimaore": "kwezi", "kibouchi": "kwezi", "category": "salutations", "image_url": "☀️", "difficulty": 1},
        {"french": "comment ça va", "shimaore": "jéjé", "kibouchi": "akori", "category": "salutations", "image_url": "❓", "difficulty": 1},
        {"french": "oui", "shimaore": "ewa", "kibouchi": "iya", "category": "salutations", "image_url": "✅", "difficulty": 1},
        {"french": "non", "shimaore": "anha", "kibouchi": "anha", "category": "salutations", "image_url": "❌", "difficulty": 1},
        {"french": "ça va bien", "shimaore": "fétré", "kibouchi": "tsara", "category": "salutations", "image_url": "😊", "difficulty": 1},
        {"french": "merci", "shimaore": "marahaba", "kibouchi": "marahaba", "category": "salutations", "image_url": "🙏", "difficulty": 1},
        {"french": "bonne nuit", "shimaore": "oukou wa hairi", "kibouchi": "haloui tsara", "category": "salutations", "image_url": "🌙", "difficulty": 1},
        {"french": "au revoir", "shimaore": "kwaheri", "kibouchi": "maeva", "category": "salutations", "image_url": "👋", "difficulty": 1},
    ]
    
    # SECTION GRAMMAIRE - 21 mots exacts selon l'image
    grammaire_vocabulary = [
        {"french": "je", "shimaore": "wami", "kibouchi": "zahou", "category": "grammaire", "image_url": "👤", "difficulty": 1},
        {"french": "tu", "shimaore": "wawé", "kibouchi": "anaou", "category": "grammaire", "image_url": "👤", "difficulty": 1},
        {"french": "il/elle", "shimaore": "wayé", "kibouchi": "izi", "category": "grammaire", "image_url": "👤", "difficulty": 1},
        {"french": "nous", "shimaore": "wassi", "kibouchi": "atsika", "category": "grammaire", "image_url": "👥", "difficulty": 1},
        {"french": "ils/elles", "shimaore": "wawo", "kibouchi": "réou", "category": "grammaire", "image_url": "👥", "difficulty": 1},
        {"french": "le mien", "shimaore": "yangou", "kibouchi": "ninakahi", "category": "grammaire", "image_url": "👤", "difficulty": 2},
        {"french": "le tien", "shimaore": "yaho", "kibouchi": "ninaou", "category": "grammaire", "image_url": "👤", "difficulty": 2},
        {"french": "le sien", "shimaore": "yahé", "kibouchi": "ninazi", "category": "grammaire", "image_url": "👤", "difficulty": 2},
        {"french": "le leur", "shimaore": "yawo", "kibouchi": "nindréou", "category": "grammaire", "image_url": "👥", "difficulty": 2},
        {"french": "le nôtre", "shimaore": "yatrou", "kibouchi": "nintsika", "category": "grammaire", "image_url": "👥", "difficulty": 2},
        {"french": "le vôtre", "shimaore": "yangnou", "kibouchi": "ninaréou", "category": "grammaire", "image_url": "👥", "difficulty": 2},
        {"french": "vous", "shimaore": "wagnou", "kibouchi": "anaréou", "category": "grammaire", "image_url": "👥", "difficulty": 1},
        {"french": "professeur", "shimaore": "foundi", "kibouchi": "foundi", "category": "grammaire", "image_url": "👨‍🏫", "difficulty": 1},
        {"french": "guide spirituel", "shimaore": "cadhi", "kibouchi": "cadhi", "category": "grammaire", "image_url": "👨‍🦲", "difficulty": 1},
        {"french": "imam", "shimaore": "imamou", "kibouchi": "imamou", "category": "grammaire", "image_url": "👨‍🦲", "difficulty": 1},
        {"french": "voisin", "shimaore": "djirani", "kibouchi": "djirani", "category": "grammaire", "image_url": "🏠", "difficulty": 1},
        {"french": "maire", "shimaore": "méra", "kibouchi": "méra", "category": "grammaire", "image_url": "🏛️", "difficulty": 1},
        {"french": "élu", "shimaore": "dhoimana", "kibouchi": "dhoimana", "category": "grammaire", "image_url": "🗳️", "difficulty": 1},
        {"french": "pêcheur", "shimaore": "mlozi", "kibouchi": "ampamintagna", "category": "grammaire", "image_url": "🎣", "difficulty": 1},
        {"french": "agriculteur", "shimaore": "mlimizi", "kibouchi": "ampikapa", "category": "grammaire", "image_url": "👨‍🌾", "difficulty": 1},
        {"french": "éleveur", "shimaore": "mtsounga", "kibouchi": "ampitsounga", "category": "grammaire", "image_url": "🐄", "difficulty": 1},
    ]
    
    # Ajouter timestamp à chaque mot
    all_vocabulary = corps_vocabulary + salutations_vocabulary + grammaire_vocabulary
    for word in all_vocabulary:
        word["created_at"] = datetime.utcnow()
    
    # Insérer tous les nouveaux mots
    result = words_collection.insert_many(all_vocabulary)
    
    print(f"✅ Sections corps, salutations et grammaire mises à jour : {len(result.inserted_ids)} mots ajoutés")
    print(f"📊 Corps humain : {len(corps_vocabulary)} mots")
    print(f"📊 Salutations : {len(salutations_vocabulary)} mots")
    print(f"📊 Grammaire : {len(grammaire_vocabulary)} mots")
    
    # Vérification
    total_words = words_collection.count_documents({})
    corps_count = words_collection.count_documents({"category": "corps"})
    salutations_count = words_collection.count_documents({"category": "salutations"})  
    grammaire_count = words_collection.count_documents({"category": "grammaire"})
    
    print(f"\n📈 STATISTIQUES MISES À JOUR :")
    print(f"   Total des mots dans la base : {total_words}")
    print(f"   Mots dans la catégorie corps : {corps_count}")
    print(f"   Mots dans la catégorie salutations : {salutations_count}")
    print(f"   Mots dans la catégorie grammaire : {grammaire_count}")
    
    return len(result.inserted_ids)

if __name__ == "__main__":
    print("🔄 Mise à jour des sections corps, salutations et grammaire avec les données des images...")
    count = update_corps_salutations_grammaire()
    print(f"✅ Terminé ! {count} mots (corps + salutations + grammaire) mis à jour selon les images.")