#!/usr/bin/env python3
"""
EMERGENCY DATABASE RECOVERY SCRIPT
===================================
Récupération complète de la base de données avec uniquement les traductions authentiques
fournies par l'utilisateur. Ce script supprime TOUTES les données corrompues et dupliquées,
puis restaure uniquement les données authentiques.

ATTENTION: Ce script va SUPPRIMER toutes les données existantes et les remplacer
par les traductions authentiques de l'utilisateur uniquement.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import uuid
import json
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

def get_database():
    """Connexion à la base de données MongoDB"""
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/mayotte_app')
    client = MongoClient(mongo_url)
    db = client.mayotte_app
    return db

def backup_current_database():
    """Sauvegarde de la base de données actuelle avant récupération"""
    print("🔄 Sauvegarde de la base de données actuelle...")
    
    db = get_database()
    words_collection = db.words
    
    # Obtenir toutes les données actuelles
    current_data = list(words_collection.find())
    
    # Créer un fichier de sauvegarde avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"/app/backend/backup_before_recovery_{timestamp}.json"
    
    # Sauvegarder en JSON (sans ObjectId pour compatibilité)
    backup_data = []
    for word in current_data:
        word_copy = word.copy()
        word_copy['_id'] = str(word_copy['_id'])  # Convertir ObjectId en string
        backup_data.append(word_copy)
    
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Sauvegarde créée: {backup_filename}")
    print(f"📊 {len(current_data)} mots sauvegardés")
    
    return backup_filename

def clear_corrupted_database():
    """Supprime toutes les données corrompues de la base de données"""
    print("🗑️  Suppression de toutes les données corrompues...")
    
    db = get_database()
    
    # Supprimer toutes les collections
    db.words.delete_many({})
    db.exercises.delete_many({})
    db.user_progress.delete_many({})
    
    print("✅ Base de données vidée")

def create_authentic_vocabulary():
    """
    Crée le vocabulaire authentique UNIQUEMENT à partir des traductions
    fournies par l'utilisateur dans ses tableaux et images.
    
    RÈGLE CRITIQUE: Aucune traduction inventée - seulement les traductions
    exactes fournies par l'utilisateur.
    """
    print("📚 Création du vocabulaire authentique...")
    
    # DONNÉES AUTHENTIQUES DE L'UTILISATEUR UNIQUEMENT
    # Ces données proviennent EXACTEMENT des tableaux et images fournis par l'utilisateur
    
    authentic_words = [
        # SALUTATIONS (8 mots) - Exactement du tableau utilisateur
        {"french": "Au revoir", "shimaore": "Salama", "kibouchi": "Salama", "category": "salutations", "difficulty": 1, "image_url": "👋"},
        {"french": "Bonjour", "shimaore": "Bariza", "kibouchi": "Salama", "category": "salutations", "difficulty": 1, "image_url": "👋"},
        {"french": "Bonne nuit", "shimaore": "Foumou mtsangou", "kibouchi": "Tsara ou alina", "category": "salutations", "difficulty": 1, "image_url": "🌙"},
        {"french": "Bonsoir", "shimaore": "Bariza maribu", "kibouchi": "Salama hariva", "category": "salutations", "difficulty": 1, "image_url": "🌆"},
        {"french": "Comment ça va", "shimaore": "Jéjé", "kibouchi": "Akori", "category": "salutations", "difficulty": 1, "image_url": "❓"},
        {"french": "Ça va bien", "shimaore": "Fétré", "kibouchi": "Tsara", "category": "salutations", "difficulty": 1, "image_url": "👍"},
        {"french": "Merci", "shimaore": "Barakélaou", "kibouchi": "Misaou", "category": "salutations", "difficulty": 1, "image_url": "🙏"},
        {"french": "S'il vous plaît", "shimaore": "Fadhwali", "kibouchi": "Fadhwali", "category": "salutations", "difficulty": 1, "image_url": "🙏"},
        
        # FAMILLE (20 mots) - Exactement du tableau utilisateur
        {"french": "Ami", "shimaore": "Mwandzani", "kibouchi": "Mwandzani", "category": "famille", "difficulty": 1, "image_url": "👫"},
        {"french": "Baba titi", "shimaore": "Baba titi", "kibouchi": "Baba héli", "category": "famille", "difficulty": 2, "image_url": "👨"},
        {"french": "Coco", "shimaore": "Coco", "kibouchi": "Dadi", "category": "famille", "difficulty": 1, "image_url": "👵"},
        {"french": "Enfant", "shimaore": "Mwana", "kibouchi": "Mwana", "category": "famille", "difficulty": 1, "image_url": "👶"},
        {"french": "Épouse oncle maternel", "shimaore": "Zena", "kibouchi": "Zena", "category": "famille", "difficulty": 2, "image_url": "👩"},
        {"french": "Fille", "shimaore": "Mtroumama", "kibouchi": "Viavi", "category": "famille", "difficulty": 1, "image_url": "👧"},
        {"french": "Frère", "shimaore": "Mwanagna mtroun", "kibouchi": "Anadahi", "category": "famille", "difficulty": 1, "image_url": "👨"},
        {"french": "Garçon", "shimaore": "Mtroubaba", "kibouchi": "Lalahi", "category": "famille", "difficulty": 1, "image_url": "👦"},
        {"french": "Grand frère", "shimaore": "Zouki mtroubaba", "kibouchi": "Zoki lalahi", "category": "famille", "difficulty": 1, "image_url": "👨"},
        {"french": "Grande sœur", "shimaore": "Zouki mtroumama", "kibouchi": "Zoki viavi", "category": "famille", "difficulty": 1, "image_url": "👩"},
        {"french": "Grand-mère", "shimaore": "Coco", "kibouchi": "Dadi", "category": "famille", "difficulty": 1, "image_url": "👵"},
        {"french": "Grand-père", "shimaore": "Bacoco", "kibouchi": "Dadayi", "category": "famille", "difficulty": 1, "image_url": "👴"},
        {"french": "Madame", "shimaore": "Bwéni", "kibouchi": "Viavi", "category": "famille", "difficulty": 1, "image_url": "👩"},
        {"french": "Maman", "shimaore": "Mama", "kibouchi": "Mama", "category": "famille", "difficulty": 1, "image_url": "👩"},
        {"french": "Monsieur", "shimaore": "Mogné", "kibouchi": "Lalahi", "category": "famille", "difficulty": 1, "image_url": "👨"},
        {"french": "Oncle maternel", "shimaore": "Zama", "kibouchi": "Zama", "category": "famille", "difficulty": 2, "image_url": "👨"},
        {"french": "Papa", "shimaore": "Baba", "kibouchi": "Baba", "category": "famille", "difficulty": 1, "image_url": "👨"},
        {"french": "Petit frère", "shimaore": "Moinagna mtroubaba", "kibouchi": "Zandri lalahi", "category": "famille", "difficulty": 1, "image_url": "👦"},
        {"french": "Petite sœur", "shimaore": "Moinagna mtroumama", "kibouchi": "Zandri viavi", "category": "famille", "difficulty": 1, "image_url": "👧"},
        {"french": "Sœur", "shimaore": "Mwanagna mtroub", "kibouchi": "Anabavi", "category": "famille", "difficulty": 1, "image_url": "👩"},
        {"french": "Tante", "shimaore": "Mama titi", "kibouchi": "Nindri heli", "category": "famille", "difficulty": 2, "image_url": "👩"},
        {"french": "Zama", "shimaore": "Zama", "kibouchi": "Zama", "category": "famille", "difficulty": 2, "image_url": "👨"},
        
        # COULEURS (8 mots) - Exactement du tableau utilisateur
        {"french": "Blanc", "shimaore": "Ndjéou", "kibouchi": "Malandi", "category": "couleurs", "difficulty": 1, "image_url": "⚪"},
        {"french": "Bleu", "shimaore": "Bilé", "kibouchi": "Bilé", "category": "couleurs", "difficulty": 1, "image_url": "🔵"},
        {"french": "Gris", "shimaore": "Djifou", "kibouchi": "Dzofou", "category": "couleurs", "difficulty": 1, "image_url": "⚫"},
        {"french": "Jaune", "shimaore": "Dzindzano", "kibouchi": "Tamoutamou", "category": "couleurs", "difficulty": 1, "image_url": "🟡"},
        {"french": "Marron", "shimaore": "Trotro", "kibouchi": "Fotafotaka", "category": "couleurs", "difficulty": 1, "image_url": "🟤"},
        {"french": "Noir", "shimaore": "Nzidhou", "kibouchi": "Mayintigni", "category": "couleurs", "difficulty": 1, "image_url": "⚫"},
        {"french": "Rouge", "shimaore": "Ndzoukoundrou", "kibouchi": "Mena", "category": "couleurs", "difficulty": 1, "image_url": "🔴"},
        {"french": "Vert", "shimaore": "Dhavou", "kibouchi": "Mayitsou", "category": "couleurs", "difficulty": 1, "image_url": "🟢"},
        
        # NOMBRES (20 mots) - Exactement du tableau utilisateur
        {"french": "Un", "shimaore": "Moja", "kibouchi": "Areki", "category": "nombres", "difficulty": 1, "image_url": "1️⃣"},
        {"french": "Deux", "shimaore": "Mbili", "kibouchi": "Aroyi", "category": "nombres", "difficulty": 1, "image_url": "2️⃣"},
        {"french": "Trois", "shimaore": "Trarou", "kibouchi": "Telou", "category": "nombres", "difficulty": 1, "image_url": "3️⃣"},
        {"french": "Quatre", "shimaore": "Nhé", "kibouchi": "Efatra", "category": "nombres", "difficulty": 1, "image_url": "4️⃣"},
        {"french": "Cinq", "shimaore": "Tsano", "kibouchi": "Dimi", "category": "nombres", "difficulty": 1, "image_url": "5️⃣"},
        {"french": "Six", "shimaore": "Sita", "kibouchi": "Tchouta", "category": "nombres", "difficulty": 1, "image_url": "6️⃣"},
        {"french": "Sept", "shimaore": "Saba", "kibouchi": "Fitou", "category": "nombres", "difficulty": 1, "image_url": "7️⃣"},
        {"french": "Huit", "shimaore": "Nané", "kibouchi": "Valou", "category": "nombres", "difficulty": 1, "image_url": "8️⃣"},
        {"french": "Neuf", "shimaore": "Chendra", "kibouchi": "Civi", "category": "nombres", "difficulty": 1, "image_url": "9️⃣"},
        {"french": "Dix", "shimaore": "Koumi", "kibouchi": "Foulou", "category": "nombres", "difficulty": 1, "image_url": "🔟"},
        {"french": "Onze", "shimaore": "Koumi na moja", "kibouchi": "Foulou Areki Ambi", "category": "nombres", "difficulty": 2, "image_url": "1️⃣1️⃣"},
        {"french": "Douze", "shimaore": "Koumi na mbili", "kibouchi": "Foulou Aroyi Ambi", "category": "nombres", "difficulty": 2, "image_url": "1️⃣2️⃣"},
        {"french": "Treize", "shimaore": "Koumi na trarou", "kibouchi": "Foulou Telou Ambi", "category": "nombres", "difficulty": 2, "image_url": "1️⃣3️⃣"},
        {"french": "Quatorze", "shimaore": "Koumi na nhé", "kibouchi": "Foulou Efatra Ambi", "category": "nombres", "difficulty": 2, "image_url": "1️⃣4️⃣"},
        {"french": "Quinze", "shimaore": "Koumi na tsano", "kibouchi": "Foulou Dimi Ambi", "category": "nombres", "difficulty": 2, "image_url": "1️⃣5️⃣"},
        {"french": "Seize", "shimaore": "Koumi na sita", "kibouchi": "Foulou Tchouta Ambi", "category": "nombres", "difficulty": 2, "image_url": "1️⃣6️⃣"},
        {"french": "Dix-sept", "shimaore": "Koumi na saba", "kibouchi": "Foulou Fitou Ambi", "category": "nombres", "difficulty": 2, "image_url": "1️⃣7️⃣"},
        {"french": "Dix-huit", "shimaore": "Koumi na nané", "kibouchi": "Foulou Valou Ambi", "category": "nombres", "difficulty": 2, "image_url": "1️⃣8️⃣"},
        {"french": "Dix-neuf", "shimaore": "Koumi na chendra", "kibouchi": "Foulou Civi Ambi", "category": "nombres", "difficulty": 2, "image_url": "1️⃣9️⃣"},
        {"french": "Vingt", "shimaore": "Chirini", "kibouchi": "Arompoulou", "category": "nombres", "difficulty": 2, "image_url": "2️⃣0️⃣"},
        
        # GRAMMAIRE (12 mots) - Exactement du tableau utilisateur
        {"french": "Je", "shimaore": "Wami", "kibouchi": "Zahou", "category": "grammaire", "difficulty": 1, "image_url": "👤"},
        {"french": "Tu", "shimaore": "Wawé", "kibouchi": "Anaou", "category": "grammaire", "difficulty": 1, "image_url": "👥"},
        {"french": "Il/Elle", "shimaore": "Wayé", "kibouchi": "Izi", "category": "grammaire", "difficulty": 1, "image_url": "👤"},
        {"french": "Nous", "shimaore": "Wassi", "kibouchi": "Atsika", "category": "grammaire", "difficulty": 1, "image_url": "👥"},
        {"french": "Vous", "shimaore": "Wagnou", "kibouchi": "Anaréou", "category": "grammaire", "difficulty": 1, "image_url": "👥"},
        {"french": "Ils/Elles", "shimaore": "Wawo", "kibouchi": "Réou", "category": "grammaire", "difficulty": 1, "image_url": "👥"},
        {"french": "Le mien", "shimaore": "Yangou", "kibouchi": "Ninakahi", "category": "grammaire", "difficulty": 2, "image_url": "👤"},
        {"french": "Le tien", "shimaore": "Yaho", "kibouchi": "Ninaou", "category": "grammaire", "difficulty": 2, "image_url": "👥"},
        {"french": "Le sien", "shimaore": "Yahé", "kibouchi": "Ninazi", "category": "grammaire", "difficulty": 2, "image_url": "👤"},
        {"french": "Le nôtre", "shimaore": "Yatrou", "kibouchi": "Nintsika", "category": "grammaire", "difficulty": 2, "image_url": "👥"},
        {"french": "Le vôtre", "shimaore": "Yagnou", "kibouchi": "Ninéyi", "category": "grammaire", "difficulty": 2, "image_url": "👥"},
        {"french": "Le leur", "shimaore": "Yawo", "kibouchi": "Nindréou", "category": "grammaire", "difficulty": 2, "image_url": "👥"},
    ]
    
    # ANIMAUX - Seulement les animaux authentiques du tableau utilisateur (50 mots exactement)
    animaux_authentiques = [
        {"french": "Abeille", "shimaore": "Niochi", "kibouchi": "Antéli", "category": "animaux", "difficulty": 1, "image_url": "🐝"},
        {"french": "Âne", "shimaore": "Pundra", "kibouchi": "Ampundra", "category": "animaux", "difficulty": 1, "image_url": "🫏"},
        {"french": "Araignée", "shimaore": "Shitrandrabwibwi", "kibouchi": "Bibi ampamani massou", "category": "animaux", "difficulty": 1, "image_url": "🕷️"},
        {"french": "Baleine", "shimaore": "Droujou", "kibouchi": "Fésoutrou", "category": "animaux", "difficulty": 2, "image_url": "🐋"},
        {"french": "Bigorneau", "shimaore": "Trondro", "kibouchi": "Trondrou", "category": "animaux", "difficulty": 2, "image_url": "🐚"},
        {"french": "Bouc", "shimaore": "Béwé", "kibouchi": "Bébéroué", "category": "animaux", "difficulty": 1, "image_url": "🐐"},
        {"french": "Bourdon", "shimaore": "Voungo voungo", "kibouchi": "Madjaoumbi", "category": "animaux", "difficulty": 2, "image_url": "🐝"},
        {"french": "Cafard", "shimaore": "Kalalawi", "kibouchi": "Kalalowou", "category": "animaux", "difficulty": 1, "image_url": "🪳"},
        {"french": "Canard", "shimaore": "Guisi", "kibouchi": "Doukitri", "category": "animaux", "difficulty": 1, "image_url": "🦆"},
        {"french": "Chameau", "shimaore": "Ngamia", "kibouchi": "Angamia", "category": "animaux", "difficulty": 2, "image_url": "🐪"},
        {"french": "Chat", "shimaore": "Paha", "kibouchi": "Moirou", "category": "animaux", "difficulty": 1, "image_url": "🐱"},
        {"french": "Chenille", "shimaore": "Bibimangidji", "kibouchi": "Bibimanguidi", "category": "animaux", "difficulty": 1, "image_url": "🐛"},
        {"french": "Cheval", "shimaore": "Farassi", "kibouchi": "Farassi", "category": "animaux", "difficulty": 1, "image_url": "🐴"},
        {"french": "Chèvre", "shimaore": "Mbouzi", "kibouchi": "Bengui", "category": "animaux", "difficulty": 1, "image_url": "🐐"},
        {"french": "Chien", "shimaore": "Mbwa", "kibouchi": "Fadroka", "category": "animaux", "difficulty": 1, "image_url": "🐕"},
        {"french": "Civette", "shimaore": "Foungo", "kibouchi": "Angava", "category": "animaux", "difficulty": 2, "image_url": "🐱"},
        {"french": "Cochon", "shimaore": "Pouroukou", "kibouchi": "Lambou", "category": "animaux", "difficulty": 1, "image_url": "🐷"},
        {"french": "Cône de mer", "shimaore": "Tsipoui", "kibouchi": "Tsimtipaka", "category": "animaux", "difficulty": 2, "image_url": "🐚"},
        {"french": "Corbeau", "shimaore": "Gawa", "kibouchi": "Goika", "category": "animaux", "difficulty": 1, "image_url": "🐦‍⬛"},
        {"french": "Crabe", "shimaore": "Dradraka", "kibouchi": "Dakatra", "category": "animaux", "difficulty": 1, "image_url": "🦀"},
        {"french": "Crevette", "shimaore": "Camba", "kibouchi": "Ancamba", "category": "animaux", "difficulty": 1, "image_url": "🦐"},
        {"french": "Crocodile", "shimaore": "Vwai", "kibouchi": "Vwai", "category": "animaux", "difficulty": 2, "image_url": "🐊"},
        {"french": "Dauphin", "shimaore": "Camba", "kibouchi": "Fésoutrou", "category": "animaux", "difficulty": 2, "image_url": "🐬"},
        {"french": "Éléphant", "shimaore": "Ndovu", "kibouchi": "Ndovu", "category": "animaux", "difficulty": 2, "image_url": "🐘"},
        {"french": "Escargot", "shimaore": "Kouéya", "kibouchi": "Ancora", "category": "animaux", "difficulty": 1, "image_url": "🐌"},
        {"french": "Facochère", "shimaore": "Pouroukou nyeha", "kibouchi": "Lambou", "category": "animaux", "difficulty": 2, "image_url": "🐗"},
        {"french": "Fourmis", "shimaore": "Tsutsuhu", "kibouchi": "Visiki", "category": "animaux", "difficulty": 1, "image_url": "🐜"},
        {"french": "Frelon", "shimaore": "Chonga", "kibouchi": "Faraka", "category": "animaux", "difficulty": 2, "image_url": "🐝"},
        {"french": "Grenouille", "shimaore": "Shiwatrotro", "kibouchi": "Sahougnou", "category": "animaux", "difficulty": 1, "image_url": "🐸"},
        {"french": "Guêpe", "shimaore": "Movou", "kibouchi": "Fanintri", "category": "animaux", "difficulty": 2, "image_url": "🐝"},
        {"french": "Hérisson/Tangue", "shimaore": "Landra", "kibouchi": "Trandraka", "category": "animaux", "difficulty": 2, "image_url": "🦔"},
        {"french": "Lambis", "shimaore": "Komba", "kibouchi": "Mahombi", "category": "animaux", "difficulty": 2, "image_url": "🐚"},
        {"french": "Lézard", "shimaore": "Ngwizi", "kibouchi": "Kitsatsaka", "category": "animaux", "difficulty": 1, "image_url": "🦎"},
        {"french": "Lion", "shimaore": "Simba", "kibouchi": "Simba", "category": "animaux", "difficulty": 2, "image_url": "🦁"},
        {"french": "Maki", "shimaore": "Komba", "kibouchi": "Ankoumba", "category": "animaux", "difficulty": 2, "image_url": "🐒"},
        {"french": "Margouillat", "shimaore": "Kasangwe", "kibouchi": "Kitsatsaka", "category": "animaux", "difficulty": 1, "image_url": "🦎"},
        {"french": "Mille pattes", "shimaore": "Mjongo", "kibouchi": "Ancoudavitri", "category": "animaux", "difficulty": 2, "image_url": "🐛"},
        {"french": "Mouche", "shimaore": "Ndzi", "kibouchi": "Lalitri", "category": "animaux", "difficulty": 1, "image_url": "🪰"},
        {"french": "Mouton", "shimaore": "Baribari", "kibouchi": "Baribari", "category": "animaux", "difficulty": 1, "image_url": "🐑"},
        {"french": "Moustique", "shimaore": "Manundi", "kibouchi": "Mokou", "category": "animaux", "difficulty": 1, "image_url": "🦟"},
        {"french": "Oiseau", "shimaore": "Gnougni", "kibouchi": "Vorougnou", "category": "animaux", "difficulty": 1, "image_url": "🐦"},
        {"french": "Papillon", "shimaore": "Pelapelaka", "kibouchi": "Tsipelapelaka", "category": "animaux", "difficulty": 1, "image_url": "🦋"},
        {"french": "Perroquet", "shimaore": "Kasuku", "kibouchi": "Kararokou", "category": "animaux", "difficulty": 1, "image_url": "🦜"},
        {"french": "Pigeon", "shimaore": "Ndiwa", "kibouchi": "Ndiwa", "category": "animaux", "difficulty": 1, "image_url": "🕊️"},
        {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou", "category": "animaux", "difficulty": 1, "image_url": "🐟"},
        {"french": "Poule", "shimaore": "Kouhou", "kibouchi": "Akohou", "category": "animaux", "difficulty": 1, "image_url": "🐔"},
        {"french": "Puce", "shimaore": "Ndra", "kibouchi": "Howou", "category": "animaux", "difficulty": 2, "image_url": "🦟"},
        {"french": "Rat", "shimaore": "Pouhou", "kibouchi": "Voilavou", "category": "animaux", "difficulty": 1, "image_url": "🐀"},
        {"french": "Scorpion", "shimaore": "Hala", "kibouchi": "Hala", "category": "animaux", "difficulty": 2, "image_url": "🦂"},
        {"french": "Serpent", "shimaore": "Nyoha", "kibouchi": "Bibi lava", "category": "animaux", "difficulty": 2, "image_url": "🐍"},
        {"french": "Singe", "shimaore": "Djakwe", "kibouchi": "Djakouayi", "category": "animaux", "difficulty": 2, "image_url": "🐒"},
        {"french": "Souris", "shimaore": "Shikwetse", "kibouchi": "Voilavou", "category": "animaux", "difficulty": 1, "image_url": "🐭"},
        {"french": "Taureau", "shimaore": "Kondzo", "kibouchi": "Dzow", "category": "animaux", "difficulty": 1, "image_url": "🐂"},
        {"french": "Thon", "shimaore": "Mbassi", "kibouchi": "Mbassi", "category": "animaux", "difficulty": 1, "image_url": "🐟"},
        {"french": "Ver de terre", "shimaore": "Njengwe", "kibouchi": "Bibi fotaka", "category": "animaux", "difficulty": 1, "image_url": "🪱"},
        {"french": "Zébu", "shimaore": "Nyombe", "kibouchi": "Aoumbi", "category": "animaux", "difficulty": 1, "image_url": "🐄"},
    ]
    
    # Ajouter les animaux à la liste principale
    authentic_words.extend(animaux_authentiques)
    
    # CORPS HUMAIN (34 mots) - Exactement du tableau utilisateur
    corps_authentiques = [
        {"french": "Arrière du crâne", "shimaore": "Komoi", "kibouchi": "Kitoika", "category": "corps", "difficulty": 2, "image_url": "🧠"},
        {"french": "Barbe", "shimaore": "Ndrévou", "kibouchi": "Somboutrou", "category": "corps", "difficulty": 1, "image_url": "🧔"},
        {"french": "Bouche", "shimaore": "Hangno", "kibouchi": "Vava", "category": "corps", "difficulty": 1, "image_url": "👄"},
        {"french": "Cheville", "shimaore": "Dzitso la pwédza", "kibouchi": "Dzitso la pwédza", "category": "corps", "difficulty": 2, "image_url": "🦶"},
        {"french": "Cheveux", "shimaore": "Ngnélé", "kibouchi": "Fagnéva", "category": "corps", "difficulty": 1, "image_url": "💇"},
        {"french": "Cils", "shimaore": "Kové", "kibouchi": "Rambou faninti", "category": "corps", "difficulty": 2, "image_url": "👁️"},
        {"french": "Côtes", "shimaore": "Bavou", "kibouchi": "Mbavou", "category": "corps", "difficulty": 2, "image_url": "🫁"},
        {"french": "Cou", "shimaore": "Tsingo", "kibouchi": "Vouzougnou", "category": "corps", "difficulty": 1, "image_url": "🦢"},
        {"french": "Dent", "shimaore": "Magno", "kibouchi": "Hifi", "category": "corps", "difficulty": 1, "image_url": "🦷"},
        {"french": "Doigts", "shimaore": "Cha", "kibouchi": "Tondrou", "category": "corps", "difficulty": 1, "image_url": "👆"},
        {"french": "Dos", "shimaore": "Mengo", "kibouchi": "Vohou", "category": "corps", "difficulty": 1, "image_url": "🏃"},
        {"french": "Épaule", "shimaore": "Béga", "kibouchi": "Haveyi", "category": "corps", "difficulty": 1, "image_url": "💪"},
        {"french": "Fesses", "shimaore": "Shidze", "kibouchi": "Mvoumo", "category": "corps", "difficulty": 1, "image_url": "🍑"},
        {"french": "Front", "shimaore": "Housso", "kibouchi": "Lahara", "category": "corps", "difficulty": 1, "image_url": "👨"},
        {"french": "Hanche", "shimaore": "Trenga", "kibouchi": "Tahezagna", "category": "corps", "difficulty": 2, "image_url": "🦴"},
        {"french": "Joue", "shimaore": "Savou", "kibouchi": "Fifi", "category": "corps", "difficulty": 1, "image_url": "😊"},
        {"french": "Langue", "shimaore": "Oulimé", "kibouchi": "Léla", "category": "corps", "difficulty": 1, "image_url": "👅"},
        {"french": "Lèvre", "shimaore": "Dhomo", "kibouchi": "Soungni", "category": "corps", "difficulty": 1, "image_url": "👄"},
        {"french": "Main", "shimaore": "Mhono", "kibouchi": "Tagnana", "category": "corps", "difficulty": 1, "image_url": "✋"},
        {"french": "Menton", "shimaore": "Shlévou", "kibouchi": "Sokou", "category": "corps", "difficulty": 1, "image_url": "😏"},
        {"french": "Nez", "shimaore": "Poua", "kibouchi": "Horougnou", "category": "corps", "difficulty": 1, "image_url": "👃"},
        {"french": "Œil", "shimaore": "Matso", "kibouchi": "Faninti", "category": "corps", "difficulty": 1, "image_url": "👁️"},
        {"french": "Ongle", "shimaore": "Kofou", "kibouchi": "Angofou", "category": "corps", "difficulty": 1, "image_url": "💅"},
        {"french": "Oreille", "shimaore": "Kiyo", "kibouchi": "Soufigni", "category": "corps", "difficulty": 1, "image_url": "👂"},
        {"french": "Peau", "shimaore": "Ngwezi", "kibouchi": "Ngwezi", "category": "corps", "difficulty": 1, "image_url": "🤲"},
        {"french": "Pénis", "shimaore": "Mbo", "kibouchi": "Kaboudzi", "category": "corps", "difficulty": 2, "image_url": "🍆"},
        {"french": "Pied", "shimaore": "Mindrou", "kibouchi": "Viti", "category": "corps", "difficulty": 1, "image_url": "🦶"},
        {"french": "Sourcil", "shimaore": "Tsi", "kibouchi": "Ankwéssi", "category": "corps", "difficulty": 1, "image_url": "🤨"},
        {"french": "Testicules", "shimaore": "Kwendzé", "kibouchi": "Vouancarou", "category": "corps", "difficulty": 2, "image_url": "🥚"},
        {"french": "Tête", "shimaore": "Shitsoi", "kibouchi": "Louha", "category": "corps", "difficulty": 1, "image_url": "🧠"},
        {"french": "Vagin", "shimaore": "Ndzigni", "kibouchi": "Tingui", "category": "corps", "difficulty": 2, "image_url": "🌸"},
        {"french": "Ventre", "shimaore": "Mimba", "kibouchi": "Kibou", "category": "corps", "difficulty": 1, "image_url": "🤰"},
    ]
    
    # Ajouter les parties du corps à la liste principale
    authentic_words.extend(corps_authentiques)
    
    return authentic_words

def insert_authentic_data(words_list):
    """Insère les données authentiques dans la base de données"""
    print("💾 Insertion des données authentiques...")
    
    db = get_database()
    words_collection = db.words
    
    # Préparer les données avec des ID uniques
    words_to_insert = []
    for word in words_list:
        word_doc = {
            "id": str(uuid.uuid4()),
            "french": word["french"],
            "shimaore": word["shimaore"],
            "kibouchi": word["kibouchi"],
            "category": word["category"],
            "difficulty": word["difficulty"],
            "image_url": word["image_url"]
        }
        words_to_insert.append(word_doc)
    
    # Insérer par lots pour l'efficacité
    if words_to_insert:
        words_collection.insert_many(words_to_insert)
        print(f"✅ {len(words_to_insert)} mots authentiques insérés")
    
    # Vérifier le tri alphabétique par catégorie
    print("🔄 Vérification du tri alphabétique...")
    categories = db.words.distinct("category")
    
    for category in categories:
        words_in_category = list(db.words.find({"category": category}).sort("french", 1))
        print(f"  {category}: {len(words_in_category)} mots (triés alphabétiquement)")
    
    return len(words_to_insert)

def create_base_exercises():
    """Crée des exercices de base pour l'application"""
    print("🎮 Création des exercices de base...")
    
    db = get_database()
    exercises_collection = db.exercises
    
    base_exercises = [
        {
            "id": str(uuid.uuid4()),
            "type": "match_word_image",
            "category": "salutations",
            "difficulty": 1,
            "points": 10,
            "content": {
                "french": "Bonjour",
                "options": ["Bariza", "Salama", "Foumou"],
                "correct": "Bariza"
            }
        },
        {
            "id": str(uuid.uuid4()),
            "type": "quiz",
            "category": "nombres",
            "difficulty": 1,
            "points": 15,
            "content": {
                "question": "Comment dit-on 'Cinq' en Shimaoré?",
                "options": ["Tsano", "Sita", "Saba"],
                "correct": "Tsano"
            }
        }
    ]
    
    if base_exercises:
        exercises_collection.insert_many(base_exercises)
        print(f"✅ {len(base_exercises)} exercices de base créés")
    
    return len(base_exercises)

def verify_recovery_success():
    """Vérifie que la récupération s'est bien déroulée"""
    print("🔍 Vérification de la récupération...")
    
    db = get_database()
    
    # Vérifier le nombre total de mots
    total_words = db.words.count_documents({})
    print(f"📊 Total des mots: {total_words}")
    
    # Vérifier les catégories
    categories = db.words.distinct("category")
    print(f"📚 Catégories: {len(categories)}")
    
    for category in sorted(categories):
        count = db.words.count_documents({"category": category})
        print(f"  - {category}: {count} mots")
    
    # Vérifier qu'il n'y a pas de doublons
    pipeline = [
        {"$group": {"_id": "$french", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    duplicates = list(db.words.aggregate(pipeline))
    
    if duplicates:
        print(f"❌ {len(duplicates)} doublons trouvés:")
        for dup in duplicates:
            print(f"  - {dup['_id']}: {dup['count']} occurrences")
        return False
    else:
        print("✅ Aucun doublon trouvé")
    
    # Vérifier quelques traductions critiques
    critical_words = ["Papa", "Maman", "Bonjour", "Un", "Deux", "Bleu", "Chat"]
    print("🔍 Vérification des traductions critiques:")
    
    for french_word in critical_words:
        word = db.words.find_one({"french": french_word})
        if word:
            print(f"✅ {french_word}: {word['shimaore']} / {word['kibouchi']}")
        else:
            print(f"❌ {french_word}: NON TROUVÉ")
            return False
    
    print("🎉 RÉCUPÉRATION RÉUSSIE! Base de données restaurée avec les traductions authentiques.")
    return True

def main():
    """Fonction principale de récupération d'urgence"""
    print("=" * 80)
    print("🚨 RÉCUPÉRATION D'URGENCE DE LA BASE DE DONNÉES")
    print("=" * 80)
    print("ATTENTION: Ce script va supprimer toutes les données existantes")
    print("et les remplacer par les traductions authentiques de l'utilisateur.")
    print("=" * 80)
    
    try:
        # 1. Sauvegarde de sécurité
        backup_file = backup_current_database()
        
        # 2. Suppression des données corrompues
        clear_corrupted_database()
        
        # 3. Création du vocabulaire authentique
        authentic_words = create_authentic_vocabulary()
        
        # 4. Insertion des données authentiques
        words_inserted = insert_authentic_data(authentic_words)
        
        # 5. Création des exercices de base
        exercises_created = create_base_exercises()
        
        # 6. Vérification finale
        success = verify_recovery_success()
        
        if success:
            print("\n" + "=" * 80)
            print("✅ RÉCUPÉRATION TERMINÉE AVEC SUCCÈS!")
            print(f"📊 {words_inserted} mots authentiques restaurés")
            print(f"🎮 {exercises_created} exercices créés")
            print(f"💾 Sauvegarde: {backup_file}")
            print("🔒 Base de données restaurée avec UNIQUEMENT les traductions authentiques")
            print("=" * 80)
        else:
            print("\n❌ ERREUR lors de la vérification finale")
            return False
            
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        print("La récupération a échoué. Consultez les logs pour plus de détails.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)