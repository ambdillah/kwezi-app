#!/usr/bin/env python3
"""
SCRIPT DE RESTAURATION DÉFINITIVE DE LA BASE DE DONNÉES AUTHENTIQUE
================================================================
Ce script utilise UNIQUEMENT les données authentiques fournies par l'utilisateur
dans le PDF "vocabulaire shimaoré kibouchi FR.pdf"

AUCUNE donnée inventée ou erronée ne sera utilisée.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import uuid
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'test_database')

def get_mongo_client():
    """Connexion à MongoDB"""
    try:
        client = MongoClient(MONGO_URL)
        client.admin.command('ping')
        print(f"✅ Connexion MongoDB établie : {MONGO_URL}")
        return client
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB : {e}")
        return None

def clear_database(db):
    """Vider complètement la base de données"""
    try:
        # Supprimer toutes les collections
        collections = db.list_collection_names()
        for collection_name in collections:
            db[collection_name].drop()
            print(f"🗑️ Collection '{collection_name}' supprimée")
        print("✅ Base de données complètement vidée")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du vidage de la base : {e}")
        return False

def create_authentic_vocabulary():
    """
    Créer le vocabulaire authentique basé UNIQUEMENT sur le PDF de l'utilisateur
    
    DONNÉES AUTHENTIQUES EXTRAITES DU PDF "vocabulaire shimaoré kibouchi FR.pdf"
    """
    
    # Base de données authentique extraite du PDF utilisateur
    authentic_words = [
        # NATURE (46 mots)
        {"french": "Pente/Colline/Mont", "shimaore": "Mlima", "kibouchi": "Boungou", "category": "nature", "emoji": "⛰️"},
        {"french": "Lune", "shimaore": "Mwézi", "kibouchi": "Fandzava", "category": "nature", "emoji": "🌙"},
        {"french": "Étoile", "shimaore": "Gnora", "kibouchi": "Lakintagna", "category": "nature", "emoji": "⭐"},
        {"french": "Sable", "shimaore": "Mtsanga", "kibouchi": "Fasigni", "category": "nature", "emoji": "🏖️"},
        {"french": "Vague", "shimaore": "Dhouja", "kibouchi": "Houndza/Riaka", "category": "nature", "emoji": "🌊"},
        {"french": "Vent", "shimaore": "Pévo", "kibouchi": "Tsikou", "category": "nature", "emoji": "💨"},
        {"french": "Pluie", "shimaore": "Vhoua", "kibouchi": "Mahaléni", "category": "nature", "emoji": "🌧️"},
        {"french": "Mangrove", "shimaore": "Mhonko", "kibouchi": "Honkou", "category": "nature", "emoji": "🌿"},
        {"french": "Corail", "shimaore": "Soiyi", "kibouchi": "Soiyi", "category": "nature", "emoji": "🪸"},
        {"french": "Barrière de corail", "shimaore": "Caléni", "kibouchi": "Caléni", "category": "nature", "emoji": "🏝️"},
        {"french": "Tempête", "shimaore": "Darouba", "kibouchi": "Tsikou", "category": "nature", "emoji": "⛈️"},
        {"french": "Rivière", "shimaore": "Mouro", "kibouchi": "Mouroni", "category": "nature", "emoji": "🏞️"},
        {"french": "Pont", "shimaore": "Daradja", "kibouchi": "Daradja", "category": "nature", "emoji": "🌉"},
        {"french": "Nuage", "shimaore": "Wingou", "kibouchi": "Vingou", "category": "nature", "emoji": "☁️"},
        {"french": "Arc-en-ciel", "shimaore": "Mcacamba", "kibouchi": "Atihala", "category": "nature", "emoji": "🌈"},
        {"french": "Campagne/Forêt", "shimaore": "Malavouni", "kibouchi": "Vatou", "category": "nature", "emoji": "🌲"},
        {"french": "Caillou/Pierre/Rocher", "shimaore": "Bwé", "kibouchi": "Kètraka", "category": "nature", "emoji": "🪨"},
        {"french": "Plateau", "shimaore": "Bandra", "kibouchi": "Lalagna", "category": "nature", "emoji": "🏔️"},
        {"french": "Herbe", "shimaore": "Ndzia", "kibouchi": "Haitri", "category": "nature", "emoji": "🌱"},
        {"french": "Fleur", "shimaore": "Foulera", "kibouchi": "Foulera", "category": "nature", "emoji": "🌺"},
        {"french": "Soleil", "shimaore": "Jouwa", "kibouchi": "Zouva", "category": "nature", "emoji": "☀️"},
        {"french": "Mer", "shimaore": "Bahari", "kibouchi": "Bahari", "category": "nature", "emoji": "🌊"},
        {"french": "Plage", "shimaore": "Mtsangani", "kibouchi": "Fassigni", "category": "nature", "emoji": "🏖️"},
        {"french": "Arbre", "shimaore": "Mwiri", "kibouchi": "Kakazou", "category": "nature", "emoji": "🌳"},
        {"french": "Rue/Route", "shimaore": "Paré", "kibouchi": "Paré", "category": "nature", "emoji": "🛣️"},
        {"french": "Bananier", "shimaore": "Trindri", "kibouchi": "Voudi ni hountsi", "category": "nature", "emoji": "🌴"},
        {"french": "Feuille", "shimaore": "Mawoini", "kibouchi": "Hayitri", "category": "nature", "emoji": "🍃"},
        {"french": "Branche", "shimaore": "Trahi", "kibouchi": "Trahi", "category": "nature", "emoji": "🌿"},
        {"french": "Tornade", "shimaore": "Ouzimouyi", "kibouchi": "Tsikou soulaimana", "category": "nature", "emoji": "🌪️"},
        {"french": "Cocotier", "shimaore": "M'nadzi", "kibouchi": "Voudi ni vwaniou", "category": "nature", "emoji": "🥥"},
        {"french": "Arbre à pain", "shimaore": "M'frampé", "kibouchi": "Voudi ni frampé", "category": "nature", "emoji": "🌳"},
        {"french": "Baobab", "shimaore": "M'bouyou", "kibouchi": "Voudi ni bouyou", "category": "nature", "emoji": "🌳"},
        {"french": "Bambou", "shimaore": "M'banbo", "kibouchi": "Valiha", "category": "nature", "emoji": "🎋"},
        {"french": "Manguier", "shimaore": "M'manga", "kibouchi": "Voudi ni manga", "category": "nature", "emoji": "🌳"},
        {"french": "Jacquier", "shimaore": "M'fénési", "kibouchi": "Voudi ni finési", "category": "nature", "emoji": "🌳"},
        {"french": "Terre", "shimaore": "Sol", "kibouchi": "Fotaka", "category": "nature", "emoji": "🌍"},
        {"french": "Érosion", "shimaore": "Chivandré ya tsi", "kibouchi": "Tani", "category": "nature", "emoji": "🏞️"},
        {"french": "Marée basse", "shimaore": "Maji yavo", "kibouchi": "Padza", "category": "nature", "emoji": "🌊"},
        {"french": "Platier", "shimaore": "Padza", "kibouchi": "Ranou mèki", "category": "nature", "emoji": "🏝️"},
        {"french": "Marée haute", "shimaore": "Maji yamalé", "kibouchi": "Kaléni", "category": "nature", "emoji": "🌊"},
        {"french": "Inondé", "shimaore": "Kalé", "kibouchi": "Ranou fénou", "category": "nature", "emoji": "🌊"},
        {"french": "Sauvage", "shimaore": "Ourora", "kibouchi": "Dobou", "category": "nature", "emoji": "🦁"},
        {"french": "Canne à sucre", "shimaore": "Nyéha", "kibouchi": "Di", "category": "nature", "emoji": "🎋"},
        {"french": "Fagot", "shimaore": "Mouwoi", "kibouchi": "Fari", "category": "nature", "emoji": "🪵"},
        {"french": "Pirogue", "shimaore": "Kouni", "kibouchi": "Azoumati", "category": "nature", "emoji": "🛶"},
        {"french": "Vedette", "shimaore": "Kwassa kwassa", "kibouchi": "Lakana", "category": "nature", "emoji": "🚤"},
        
        # CHIFFRES (20 mots) - Données complètes du PDF
        {"french": "Un", "shimaore": "Moja", "kibouchi": "Areki", "category": "nombres", "emoji": "1️⃣"},
        {"french": "Deux", "shimaore": "Mbili", "kibouchi": "Aroyi", "category": "nombres", "emoji": "2️⃣"},
        {"french": "Trois", "shimaore": "Trarou", "kibouchi": "Telou", "category": "nombres", "emoji": "3️⃣"},
        {"french": "Quatre", "shimaore": "Nhé", "kibouchi": "Efatra", "category": "nombres", "emoji": "4️⃣"},
        {"french": "Cinq", "shimaore": "Tsano", "kibouchi": "Dimi", "category": "nombres", "emoji": "5️⃣"},
        {"french": "Six", "shimaore": "Sita", "kibouchi": "Tchouta", "category": "nombres", "emoji": "6️⃣"},
        {"french": "Sept", "shimaore": "Saba", "kibouchi": "Fitou", "category": "nombres", "emoji": "7️⃣"},
        {"french": "Huit", "shimaore": "Nané", "kibouchi": "Valou", "category": "nombres", "emoji": "8️⃣"},
        {"french": "Neuf", "shimaore": "Chendra", "kibouchi": "Civi", "category": "nombres", "emoji": "9️⃣"},
        {"french": "Dix", "shimaore": "Koumi", "kibouchi": "Foulou", "category": "nombres", "emoji": "🔟"},
        {"french": "Onze", "shimaore": "Koumi na moja", "kibouchi": "Foulou Areki Ambi", "category": "nombres", "emoji": "1️⃣1️⃣"},
        {"french": "Douze", "shimaore": "Koumi na mbili", "kibouchi": "Foulou Aroyi Ambi", "category": "nombres", "emoji": "1️⃣2️⃣"},
        {"french": "Treize", "shimaore": "Koumi na trarou", "kibouchi": "Foulou Telou Ambi", "category": "nombres", "emoji": "1️⃣3️⃣"},
        {"french": "Quatorze", "shimaore": "Koumi na nhé", "kibouchi": "Foulou Efatra Ambi", "category": "nombres", "emoji": "1️⃣4️⃣"},
        {"french": "Quinze", "shimaore": "Koumi na tsano", "kibouchi": "Foulou Dimi Ambi", "category": "nombres", "emoji": "1️⃣5️⃣"},
        {"french": "Seize", "shimaore": "Koumi na sita", "kibouchi": "Foulou Tchouta Ambi", "category": "nombres", "emoji": "1️⃣6️⃣"},
        {"french": "Dix-sept", "shimaore": "Koumi na saba", "kibouchi": "Foulou Fitou Ambi", "category": "nombres", "emoji": "1️⃣7️⃣"},
        {"french": "Dix-huit", "shimaore": "Koumi na nané", "kibouchi": "Foulou Valou Ambi", "category": "nombres", "emoji": "1️⃣8️⃣"},
        {"french": "Dix-neuf", "shimaore": "Koumi na chendra", "kibouchi": "Foulou Civi Ambi", "category": "nombres", "emoji": "1️⃣9️⃣"},
        {"french": "Vingt", "shimaore": "Chirini", "kibouchi": "Arompoulou", "category": "nombres", "emoji": "2️⃣0️⃣"},
        
        # ANIMAUX (65+ mots) - Données complètes du PDF
        {"french": "Cochon", "shimaore": "Pouroukou", "kibouchi": "Lambou", "category": "animaux", "emoji": "🐷"},
        {"french": "Margouillat", "shimaore": "Kasangwe", "kibouchi": "Kitsatsaka", "category": "animaux", "emoji": "🦎"},
        {"french": "Abeille", "shimaore": "Niochi", "kibouchi": "Antéli", "category": "animaux", "emoji": "🐝"},
        {"french": "Chat", "shimaore": "Paha", "kibouchi": "Moirou", "category": "animaux", "emoji": "🐱"},
        {"french": "Rat", "shimaore": "Pouhou", "kibouchi": "Voilavou", "category": "animaux", "emoji": "🐀"},
        {"french": "Escargot", "shimaore": "Kowa", "kibouchi": "Ankora", "category": "animaux", "emoji": "🐌"},
        {"french": "Lion", "shimaore": "Simba", "kibouchi": "Simba", "category": "animaux", "emoji": "🦁"},
        {"french": "Grenouille", "shimaore": "Shiwatrotro", "kibouchi": "Sahougnou", "category": "animaux", "emoji": "🐸"},
        {"french": "Oiseau", "shimaore": "Gnougni", "kibouchi": "Vorougnou", "category": "animaux", "emoji": "🐦"},
        {"french": "Chien", "shimaore": "Mbwa", "kibouchi": "Fadroka", "category": "animaux", "emoji": "🐕"},
        {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou", "category": "animaux", "emoji": "🐟"},
        {"french": "Chèvre", "shimaore": "Mbouzi", "kibouchi": "Bengui", "category": "animaux", "emoji": "🐐"},
        {"french": "Moustique", "shimaore": "Manundi", "kibouchi": "Mokou", "category": "animaux", "emoji": "🦟"},
        {"french": "Mouche", "shimaore": "Ndzi", "kibouchi": "Lalitri", "category": "animaux", "emoji": "🪰"},
        {"french": "Chauve-souris", "shimaore": "Drema", "kibouchi": "Anganga", "category": "animaux", "emoji": "🦇"},
        {"french": "Serpent", "shimaore": "Nyoha", "kibouchi": "Bibi lava", "category": "animaux", "emoji": "🐍"},
        {"french": "Lapin", "shimaore": "Sungura", "kibouchi": "Borondry", "category": "animaux", "emoji": "🐰"},
        {"french": "Canard", "shimaore": "Guisi", "kibouchi": "Doukitri", "category": "animaux", "emoji": "🦆"},
        {"french": "Mouton", "shimaore": "Baribari", "kibouchi": "Baribari", "category": "animaux", "emoji": "🐑"},
        {"french": "Crocodile", "shimaore": "Vwai", "kibouchi": "Vwai", "category": "animaux", "emoji": "🐊"},
        {"french": "Caméléon", "shimaore": "Tarundru", "kibouchi": "Toundrou", "category": "animaux", "emoji": "🦎"},
        {"french": "Zébu", "shimaore": "Nyombé", "kibouchi": "Aoumbi", "category": "animaux", "emoji": "🐂"},
        {"french": "Âne", "shimaore": "Pundra", "kibouchi": "Ampundra", "category": "animaux", "emoji": "🫏"},
        {"french": "Poule", "shimaore": "Kouhou", "kibouchi": "Akohou", "category": "animaux", "emoji": "🐔"},
        {"french": "Pigeon", "shimaore": "Ndiwa", "kibouchi": "Ndiwa", "category": "animaux", "emoji": "🕊️"},
        {"french": "Fourmis", "shimaore": "Tsutsuhu", "kibouchi": "Visiki", "category": "animaux", "emoji": "🐜"},
        {"french": "Chenille", "shimaore": "Bibimangidji", "kibouchi": "Bibimanguidi", "category": "animaux", "emoji": "🐛"},
        {"french": "Papillon", "shimaore": "Pelapelaka", "kibouchi": "Tsipelapelaka", "category": "animaux", "emoji": "🦋"},
        {"french": "Ver de terre", "shimaore": "Njengwe", "kibouchi": "Bibi fotaka", "category": "animaux", "emoji": "🪱"},
        {"french": "Criquet", "shimaore": "Furudji", "kibouchi": "Kidzedza", "category": "animaux", "emoji": "🦗"},
        {"french": "Cheval", "shimaore": "Farassi", "kibouchi": "Farassi", "category": "animaux", "emoji": "🐴"},
        {"french": "Perroquet", "shimaore": "Kasuku", "kibouchi": "Kararokou", "category": "animaux", "emoji": "🦜"},
        {"french": "Cafard", "shimaore": "Kalalawi", "kibouchi": "Kalalowou", "category": "animaux", "emoji": "🪳"},
        {"french": "Araignée", "shimaore": "Shitrandrabwibwi", "kibouchi": "Bibi amparamani massou", "category": "animaux", "emoji": "🕷️"},
        {"french": "Scorpion", "shimaore": "Hala", "kibouchi": "Hala", "category": "animaux", "emoji": "🦂"},
        {"french": "Scolopendre", "shimaore": "Trambwi", "kibouchi": "Trambougnou", "category": "animaux", "emoji": "🐛"},
        {"french": "Thon", "shimaore": "Mbassi", "kibouchi": "Mbassi", "category": "animaux", "emoji": "🐟"},
        {"french": "Requin", "shimaore": "Papa", "kibouchi": "Ankiou", "category": "animaux", "emoji": "🦈"},
        {"french": "Poulpe", "shimaore": "Pwedza", "kibouchi": "Pwedza", "category": "animaux", "emoji": "🐙"},
        {"french": "Crabe", "shimaore": "Dradraka", "kibouchi": "Dakatra", "category": "animaux", "emoji": "🦀"},
        {"french": "Tortue", "shimaore": "Nyamba/Katsa", "kibouchi": "Fanou", "category": "animaux", "emoji": "🐢"},
        {"french": "Éléphant", "shimaore": "Ndovu", "kibouchi": "Ndovu", "category": "animaux", "emoji": "🐘"},
        {"french": "Lézard", "shimaore": "Ngwizi", "kibouchi": "Kitsatsaka", "category": "animaux", "emoji": "🦎"},
        {"french": "Singe", "shimaore": "Djakwe", "kibouchi": "Djakouayi", "category": "animaux", "emoji": "🐒"},
        {"french": "Souris", "shimaore": "Shikwetse", "kibouchi": "Voilavou", "category": "animaux", "emoji": "🐭"},
        {"french": "Facochère", "shimaore": "Pouroukou nyeha", "kibouchi": "Lambou", "category": "animaux", "emoji": "🐗"},
        {"french": "Renard", "shimaore": "Sabwa nyeha", "kibouchi": "Fadroka", "category": "animaux", "emoji": "🦊"},
        {"french": "Hérisson/Tangue", "shimaore": "Landra", "kibouchi": "Trandraka", "category": "animaux", "emoji": "🦔"},
        {"french": "Corbeau", "shimaore": "Gawa", "kibouchi": "Goika", "category": "animaux", "emoji": "🐦‍⬛"},
        {"french": "Civette", "shimaore": "Foungo", "kibouchi": "Angava", "category": "animaux", "emoji": "🐾"},
        {"french": "Dauphin", "shimaore": "Camba", "kibouchi": "Fésoutrou", "category": "animaux", "emoji": "🐬"},
        {"french": "Baleine", "shimaore": "Droujou", "kibouchi": "Fésoutrou", "category": "animaux", "emoji": "🐋"},
        {"french": "Crevette", "shimaore": "Camba", "kibouchi": "Ancamba", "category": "animaux", "emoji": "🦐"},
        {"french": "Frelon", "shimaore": "Chonga", "kibouchi": "Faraka", "category": "animaux", "emoji": "🐝"},
        {"french": "Guêpe", "shimaore": "Vungo vungo", "kibouchi": "Fantehi", "category": "animaux", "emoji": "🐝"},
        {"french": "Bourdon", "shimaore": "Madzi ya nyombe", "kibouchi": "Majaoumbi", "category": "animaux", "emoji": "🐝"},
        {"french": "Puce", "shimaore": "Kunguni", "kibouchi": "Ancomgou", "category": "animaux", "emoji": "🪲"},
        {"french": "Bouc", "shimaore": "Bewe", "kibouchi": "Béberou", "category": "animaux", "emoji": "🐐"},
        {"french": "Taureau", "shimaore": "Kondzo", "kibouchi": "Dzow", "category": "animaux", "emoji": "🐂"},
        {"french": "Bigorneau", "shimaore": "Trondro", "kibouchi": "Trondrou", "category": "animaux", "emoji": "🐚"},
        {"french": "Lambis", "shimaore": "Komba", "kibouchi": "Mahombi", "category": "animaux", "emoji": "🐚"},
        {"french": "Cône de mer", "shimaore": "Gnamané", "kibouchi": "Kamara", "category": "animaux", "emoji": "🐚"},
        {"french": "Mille-pattes", "shimaore": "Nyango", "kibouchi": "Scoudafitri", "category": "animaux", "emoji": "🐛"},
        
        # CORPS HUMAIN (32 mots) - Données complètes du PDF  
        {"french": "Œil", "shimaore": "Matso", "kibouchi": "Faninti", "category": "corps", "emoji": "👁️"},
        {"french": "Nez", "shimaore": "Poua", "kibouchi": "Horougnou", "category": "corps", "emoji": "👃"},
        {"french": "Oreille", "shimaore": "Kiyo", "kibouchi": "Soufigni", "category": "corps", "emoji": "👂"},
        {"french": "Ongle", "shimaore": "Kofou", "kibouchi": "Angofou", "category": "corps", "emoji": "💅"},
        {"french": "Front", "shimaore": "Housso", "kibouchi": "Lahara", "category": "corps", "emoji": "🧠"},
        {"french": "Joue", "shimaore": "Savou", "kibouchi": "Fifi", "category": "corps", "emoji": "😊"},
        {"french": "Dos", "shimaore": "Mengo", "kibouchi": "Vohou", "category": "corps", "emoji": "🫏"},
        {"french": "Épaule", "shimaore": "Béga", "kibouchi": "Haveyi", "category": "corps", "emoji": "💪"},
        {"french": "Hanche", "shimaore": "Trenga", "kibouchi": "Tahezagna", "category": "corps", "emoji": "🦵"},
        {"french": "Fesses", "shimaore": "Shidze/Mvoumo", "kibouchi": "Fouri", "category": "corps", "emoji": "🍑"},
        {"french": "Main", "shimaore": "Mhono", "kibouchi": "Tagnana", "category": "corps", "emoji": "✋"},
        {"french": "Tête", "shimaore": "Shitsoi", "kibouchi": "Louha", "category": "corps", "emoji": "🗣️"},
        {"french": "Ventre", "shimaore": "Mimba", "kibouchi": "Kibou", "category": "corps", "emoji": "🤰"},
        {"french": "Dent", "shimaore": "Magno", "kibouchi": "Hifi", "category": "corps", "emoji": "🦷"},
        {"french": "Langue", "shimaore": "Oulimé", "kibouchi": "Léla", "category": "corps", "emoji": "👅"},
        {"french": "Pied", "shimaore": "Mindrou", "kibouchi": "Viti", "category": "corps", "emoji": "🦶"},
        {"french": "Lèvre", "shimaore": "Dhomo", "kibouchi": "Soungni", "category": "corps", "emoji": "👄"},
        {"french": "Peau", "shimaore": "Ngwezi", "kibouchi": "Ngwezi", "category": "corps", "emoji": "🧴"},
        {"french": "Cheveux", "shimaore": "Ngnélé", "kibouchi": "Fagnéva", "category": "corps", "emoji": "💇"},
        {"french": "Doigts", "shimaore": "Cha", "kibouchi": "Tondrou", "category": "corps", "emoji": "👉"},
        {"french": "Barbe", "shimaore": "Ndrévou", "kibouchi": "Somboutrou", "category": "corps", "emoji": "🧔"},
        {"french": "Vagin", "shimaore": "Ndzigni", "kibouchi": "Tingui", "category": "corps", "emoji": "🚺"},
        {"french": "Testicules", "shimaore": "Kwendzé", "kibouchi": "Vouancarou", "category": "corps", "emoji": "🚹"},
        {"french": "Pénis", "shimaore": "Mbo", "kibouchi": "Kaboudzi", "category": "corps", "emoji": "🚹"},
        {"french": "Menton", "shimaore": "Shlévou", "kibouchi": "Sokou", "category": "corps", "emoji": "🧔"},
        {"french": "Bouche", "shimaore": "Hangno", "kibouchi": "Vava", "category": "corps", "emoji": "👄"},
        {"french": "Côtes", "shimaore": "Bavou", "kibouchi": "Mbavou", "category": "corps", "emoji": "🦴"},
        {"french": "Sourcil", "shimaore": "Tsi", "kibouchi": "Ankwéssi", "category": "corps", "emoji": "🤨"},
        {"french": "Cheville", "shimaore": "Dzitso la pwédza", "kibouchi": "Dzitso la pwédza", "category": "corps", "emoji": "🦶"},
        {"french": "Cou", "shimaore": "Tsingo", "kibouchi": "Vouzougnou", "category": "corps", "emoji": "🦒"},
        {"french": "Cils", "shimaore": "Kové", "kibouchi": "Rambou faninti", "category": "corps", "emoji": "👁️"},
        {"french": "Arrière du crâne", "shimaore": "Komoi", "kibouchi": "Kitoika", "category": "corps", "emoji": "🧠"},
        
        # SALUTATIONS (8 mots) - Données complètes du PDF
        {"french": "Bonjour", "shimaore": "Kwezi", "kibouchi": "Kwezi", "category": "salutations", "emoji": "👋"},
        {"french": "Comment ça va", "shimaore": "Jéjé", "kibouchi": "Akori", "category": "salutations", "emoji": "❓"},
        {"french": "Oui", "shimaore": "Ewa", "kibouchi": "Iya", "category": "salutations", "emoji": "✅"},
        {"french": "Non", "shimaore": "Anha", "kibouchi": "Anha", "category": "salutations", "emoji": "❌"},
        {"french": "Ça va bien", "shimaore": "Fétré", "kibouchi": "Tsara", "category": "salutations", "emoji": "👍"},
        {"french": "Merci", "shimaore": "Marahaba", "kibouchi": "Misaotra", "category": "salutations", "emoji": "🙏"},
        {"french": "Bonne nuit", "shimaore": "Oukou wa hairi", "kibouchi": "Alasitri tsara", "category": "salutations", "emoji": "🌙"},
        {"french": "Au revoir", "shimaore": "Kwaheri", "kibouchi": "Djalabé", "category": "salutations", "emoji": "👋"},
        
        # GRAMMAIRE (20 mots) - Données complètes du PDF
        {"french": "Je", "shimaore": "Wami", "kibouchi": "Zahou", "category": "grammaire", "emoji": "👤"},
        {"french": "Tu", "shimaore": "Wawé", "kibouchi": "Anaou", "category": "grammaire", "emoji": "👤"},
        {"french": "Il/Elle", "shimaore": "Wayé", "kibouchi": "Izi", "category": "grammaire", "emoji": "👤"},
        {"french": "Nous", "shimaore": "Wassi", "kibouchi": "Atsika", "category": "grammaire", "emoji": "👥"},
        {"french": "Ils/Elles", "shimaore": "Wawo", "kibouchi": "Réou", "category": "grammaire", "emoji": "👥"},
        {"french": "Le mien", "shimaore": "Yangou", "kibouchi": "Ninakahi", "category": "grammaire", "emoji": "👆"},
        {"french": "Le tien", "shimaore": "Yaho", "kibouchi": "Ninaou", "category": "grammaire", "emoji": "👆"},
        {"french": "Le sien", "shimaore": "Yahé", "kibouchi": "Ninazi", "category": "grammaire", "emoji": "👆"},
        {"french": "Le leur", "shimaore": "Yawo", "kibouchi": "Nindréou", "category": "grammaire", "emoji": "👆"},
        {"french": "Le nôtre", "shimaore": "Yatrou", "kibouchi": "Nintsika", "category": "grammaire", "emoji": "👆"},
        {"french": "Le vôtre", "shimaore": "Yangnou", "kibouchi": "Ninéyi", "category": "grammaire", "emoji": "👆"},
        {"french": "Vous", "shimaore": "Wagnou", "kibouchi": "Anaréou", "category": "grammaire", "emoji": "👥"},
        {"french": "Professeur", "shimaore": "Foundi", "kibouchi": "Foundi", "category": "grammaire", "emoji": "🧑‍🏫"},
        {"french": "Imam", "shimaore": "Imamou", "kibouchi": "Imamou", "category": "grammaire", "emoji": "🕌"},
        {"french": "Voisin", "shimaore": "Djirani", "kibouchi": "Djirani", "category": "grammaire", "emoji": "🏠"},
        {"french": "Maire", "shimaore": "Méra", "kibouchi": "Méra", "category": "grammaire", "emoji": "🏛️"},
        {"french": "Élu", "shimaore": "Dhoimana", "kibouchi": "Dhoimana", "category": "grammaire", "emoji": "🗳️"},
        {"french": "Pêcheur", "shimaore": "Mlozi", "kibouchi": "Mlozi", "category": "grammaire", "emoji": "🎣"},
        {"french": "Agriculteur", "shimaore": "Mlimizi", "kibouchi": "Mlimizi", "category": "grammaire", "emoji": "🚜"},
        {"french": "Éleveur", "shimaore": "Mtsounga", "kibouchi": "Mtsounga", "category": "grammaire", "emoji": "🐄"},
        
        # FAMILLE (20 mots) - Données complètes du PDF
        {"french": "Tante", "shimaore": "Mama titi", "kibouchi": "Nindri heli", "category": "famille", "emoji": "👩"},
        {"french": "Oncle maternel", "shimaore": "Zama", "kibouchi": "Zama", "category": "famille", "emoji": "👨"},
        {"french": "Oncle paternel", "shimaore": "Baba titi", "kibouchi": "Baba héli", "category": "famille", "emoji": "👨"},
        {"french": "Épouse oncle maternel", "shimaore": "Zena", "kibouchi": "Zena", "category": "famille", "emoji": "👩"},
        {"french": "Petite sœur", "shimaore": "Moinagna mtroumama", "kibouchi": "Zandri", "category": "famille", "emoji": "👧"},
        {"french": "Petit frère", "shimaore": "Moinagna mtroubaba", "kibouchi": "Zandri", "category": "famille", "emoji": "👦"},
        {"french": "Grande sœur", "shimaore": "Zouki mtroumché", "kibouchi": "Zoki viavi", "category": "famille", "emoji": "👩"},
        {"french": "Grand frère", "shimaore": "Zouki mtroubaba", "kibouchi": "Zoki lalahi", "category": "famille", "emoji": "👨"},
        {"french": "Frère", "shimaore": "Mwanagna mtroubaba", "kibouchi": "Anadahi", "category": "famille", "emoji": "👨"},
        {"french": "Sœur", "shimaore": "Mwanagna mtroumama", "kibouchi": "Anabavi", "category": "famille", "emoji": "👩"},
        {"french": "Ami", "shimaore": "Mwandzani", "kibouchi": "Mwandzani", "category": "famille", "emoji": "👫"},
        {"french": "Fille", "shimaore": "Mtroumama", "kibouchi": "Viavi", "category": "famille", "emoji": "👧"},
        {"french": "Garçon", "shimaore": "Mtroubaba", "kibouchi": "Lalahi", "category": "famille", "emoji": "👦"},
        {"french": "Monsieur", "shimaore": "Mogné", "kibouchi": "Lalahi", "category": "famille", "emoji": "👨"},
        {"french": "Grand-père", "shimaore": "Bacoco", "kibouchi": "Dadayi", "category": "famille", "emoji": "👴"},
        {"french": "Grand-mère", "shimaore": "Coco", "kibouchi": "Dadi", "category": "famille", "emoji": "👵"},
        {"french": "Madame", "shimaore": "Bwéni", "kibouchi": "Viavi", "category": "famille", "emoji": "👩"},
        {"french": "Famille", "shimaore": "Mdjamaza", "kibouchi": "Havagna", "category": "famille", "emoji": "👨‍👩‍👧‍👦"},
        {"french": "Papa", "shimaore": "Baba", "kibouchi": "Baba", "category": "famille", "emoji": "👨"},
        {"french": "Maman", "shimaore": "Mama", "kibouchi": "Mama", "category": "famille", "emoji": "👩"},
        
        # COULEURS (8 mots) - Données complètes du PDF
        {"french": "Bleu", "shimaore": "Bilé", "kibouchi": "Bilé", "category": "couleurs", "emoji": "🔵"},
        {"french": "Vert", "shimaore": "Dhavou", "kibouchi": "Mayitsou", "category": "couleurs", "emoji": "🟢"},
        {"french": "Noir", "shimaore": "Nzidhou", "kibouchi": "Mayintigni", "category": "couleurs", "emoji": "⚫"},
        {"french": "Blanc", "shimaore": "Ndjéou", "kibouchi": "Malandi", "category": "couleurs", "emoji": "⚪"},
        {"french": "Jaune", "shimaore": "Dzindzano", "kibouchi": "Tamoutamou", "category": "couleurs", "emoji": "🟡"},
        {"french": "Rouge", "shimaore": "Nzoukoundrou", "kibouchi": "Mena", "category": "couleurs", "emoji": "🔴"},
        {"french": "Gris", "shimaore": "Djifou", "kibouchi": "Dzofou", "category": "couleurs", "emoji": "🔘"},
        {"french": "Marron", "shimaore": "Trotro", "kibouchi": "Fotafotaka", "category": "couleurs", "emoji": "🤎"},
        
        # NOURRITURE (40+ mots) - Données complètes du PDF
        {"french": "Riz", "shimaore": "Tsoholé", "kibouchi": "Vari", "category": "nourriture", "emoji": "🍚"},
        {"french": "Eau", "shimaore": "Maji", "kibouchi": "Ranou", "category": "nourriture", "emoji": "💧"},
        {"french": "Ananas", "shimaore": "Nanassi", "kibouchi": "Mananassi", "category": "nourriture", "emoji": "🍍"},
        {"french": "Pois d'angole", "shimaore": "Tsouzi", "kibouchi": "Ambatri", "category": "nourriture", "emoji": "🫘"},
        {"french": "Banane", "shimaore": "Trovi", "kibouchi": "Hountsi", "category": "nourriture", "emoji": "🍌"},
        {"french": "Pain", "shimaore": "Dipé", "kibouchi": "Dipé", "category": "nourriture", "emoji": "🍞"},
        {"french": "Gâteau", "shimaore": "Mharé", "kibouchi": "Kouékou", "category": "nourriture", "emoji": "🎂"},
        {"french": "Mangue", "shimaore": "Manga", "kibouchi": "Manga", "category": "nourriture", "emoji": "🥭"},
        {"french": "Noix de coco", "shimaore": "Nadzi", "kibouchi": "Voiniou", "category": "nourriture", "emoji": "🥥"},
        {"french": "Noix de coco fraîche", "shimaore": "Chijavou", "kibouchi": "Kidjavou", "category": "nourriture", "emoji": "🥥"},
        {"french": "Lait", "shimaore": "Dzia", "kibouchi": "Rounounou", "category": "nourriture", "emoji": "🥛"},
        {"french": "Viande", "shimaore": "Nhyama", "kibouchi": "Amboumati", "category": "nourriture", "emoji": "🥩"},
        {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou", "category": "nourriture", "emoji": "🐟"},
        {"french": "Brèdes", "shimaore": "Féliki", "kibouchi": "Féliki", "category": "nourriture", "emoji": "🥬"},
        {"french": "Brède mafane", "shimaore": "Féliki mafana", "kibouchi": "Féliki mafana", "category": "nourriture", "emoji": "🥬"},
        {"french": "Brède manioc", "shimaore": "Mataba", "kibouchi": "Mataba", "category": "nourriture", "emoji": "🥬"},
        {"french": "Brède morelle", "shimaore": "Féliki nyongo", "kibouchi": "Féliki nyongo", "category": "nourriture", "emoji": "🥬"},
        {"french": "Brèdes patate douce", "shimaore": "Féliki batata", "kibouchi": "Féliki batata", "category": "nourriture", "emoji": "🥬"},
        {"french": "Patate douce", "shimaore": "Batata", "kibouchi": "Batata", "category": "nourriture", "emoji": "🍠"},
        {"french": "Bouillon", "shimaore": "Woubou", "kibouchi": "Woubou", "category": "nourriture", "emoji": "🍲"},
        {"french": "Banane au coco", "shimaore": "Trovi ya nadzi", "kibouchi": "Hountsi an voiniou", "category": "nourriture", "emoji": "🍌"},
        {"french": "Riz au coco", "shimaore": "Tsoholé ya nadzi", "kibouchi": "Vari an voiniou", "category": "nourriture", "emoji": "🍚"},
        {"french": "Poulet", "shimaore": "Bawa", "kibouchi": "Akohou", "category": "nourriture", "emoji": "🍗"},
        {"french": "Œuf", "shimaore": "Joiyi", "kibouchi": "Atoudou", "category": "nourriture", "emoji": "🥚"},
        {"french": "Tomate", "shimaore": "Tamati", "kibouchi": "Tamati", "category": "nourriture", "emoji": "🍅"},
        {"french": "Oignon", "shimaore": "Chouroungou", "kibouchi": "Doungoulou", "category": "nourriture", "emoji": "🧅"},
        {"french": "Ail", "shimaore": "Chouroungou foudjé", "kibouchi": "Doungoulou toungoula", "category": "nourriture", "emoji": "🧄"},
        {"french": "Orange", "shimaore": "Troundra", "kibouchi": "Troundra", "category": "nourriture", "emoji": "🍊"},
        {"french": "Mandarine", "shimaore": "Madhandzé", "kibouchi": "Madhandzé", "category": "nourriture", "emoji": "🍊"},
        {"french": "Manioc", "shimaore": "Mhogo", "kibouchi": "Mhogo", "category": "nourriture", "emoji": "🥔"},
        {"french": "Piment", "shimaore": "Poutou", "kibouchi": "Poutou", "category": "nourriture", "emoji": "🌶️"},
        {"french": "Taro", "shimaore": "Majimbi", "kibouchi": "Majimbi", "category": "nourriture", "emoji": "🥔"},
        {"french": "Sel", "shimaore": "Chingou", "kibouchi": "Soui", "category": "nourriture", "emoji": "🧂"},
        {"french": "Poivre", "shimaore": "Bvilibvili manga", "kibouchi": "Vilivili", "category": "nourriture", "emoji": "🧂"},
        {"french": "Curcuma", "shimaore": "Dzindzano", "kibouchi": "Tamoutamou", "category": "nourriture", "emoji": "🧄"},
        {"french": "Cumin", "shimaore": "Massala", "kibouchi": "Massala", "category": "nourriture", "emoji": "🧄"},
        {"french": "Ciboulette", "shimaore": "Chouroungou", "kibouchi": "Doungoulou ravigni", "category": "nourriture", "emoji": "🧅"},
        {"french": "Gingembre", "shimaore": "Tsingiziou", "kibouchi": "Sakéyi", "category": "nourriture", "emoji": "🧄"},
        {"french": "Vanille", "shimaore": "Lavani", "kibouchi": "Lavani", "category": "nourriture", "emoji": "🌿"},
        {"french": "Tamarin", "shimaore": "Ouhajou", "kibouchi": "Madirou kakazou", "category": "nourriture", "emoji": "🌰"},
        {"french": "Thé", "shimaore": "Maji ya moro", "kibouchi": "Rayi", "category": "nourriture", "emoji": "🍵"},
        {"french": "Papaye", "shimaore": "Papaye", "kibouchi": "Papaye", "category": "nourriture", "emoji": "🥭"},
        {"french": "Riz non décortiqué", "shimaore": "Chaoula", "kibouchi": "Hanigni", "category": "nourriture", "emoji": "🌾"},
        
        # MAISON (3 mots) - Données du PDF
        {"french": "Maison", "shimaore": "Nyoumba", "kibouchi": "Tragnou", "category": "maison", "emoji": "🏠"},
        {"french": "Porte", "shimaore": "Mlango", "kibouchi": "Varavarangna", "category": "maison", "emoji": "🚪"},
        {"french": "Case", "shimaore": "Banga", "kibouchi": "Bangna", "category": "maison", "emoji": "🏘️"},
        
        # TRANSPORT (7 mots) - Données complètes du PDF
        {"french": "Taxi", "shimaore": "Taxi", "kibouchi": "Taxi", "category": "transport", "emoji": "🚕"},
        {"french": "Moto", "shimaore": "Moto", "kibouchi": "Moto", "category": "transport", "emoji": "🏍️"},
        {"french": "Vélo", "shimaore": "Bicyclette", "kibouchi": "Bicyclette", "category": "transport", "emoji": "🚲"},
        {"french": "Barge", "shimaore": "Markabou", "kibouchi": "Markabou", "category": "transport", "emoji": "🚢"},
        {"french": "Vedette", "shimaore": "Kwassa kwassa", "kibouchi": "Vidéti", "category": "transport", "emoji": "🚤"},
        {"french": "Pirogue", "shimaore": "Laka", "kibouchi": "Lakana", "category": "transport", "emoji": "🛶"},
        {"french": "Avion", "shimaore": "Ndrégué", "kibouchi": "Roplani", "category": "transport", "emoji": "✈️"},
        
        # VETEMENTS (16 mots) - Données complètes du PDF
        {"french": "Vêtement", "shimaore": "Ngouwo", "kibouchi": "Ngouwo", "category": "vetements", "emoji": "👕"},
        {"french": "Salouva", "shimaore": "Salouva", "kibouchi": "Slouvagna", "category": "vetements", "emoji": "👗"},
        {"french": "Chemise", "shimaore": "Chimizi", "kibouchi": "Kamiza", "category": "vetements", "emoji": "👔"},
        {"french": "Pantalon", "shimaore": "Sourouali", "kibouchi": "Pantalon", "category": "vetements", "emoji": "👖"},
        {"french": "Short", "shimaore": "Kaliso", "kibouchi": "Kaliso", "category": "vetements", "emoji": "🩳"},
        {"french": "Sous-vêtement", "shimaore": "Silipou", "kibouchi": "Silipou", "category": "vetements", "emoji": "🩲"},
        {"french": "Chapeau", "shimaore": "Kofia", "kibouchi": "Kofia", "category": "vetements", "emoji": "👒"},
        {"french": "Kamis/Boubou", "shimaore": "Kandzou bolé", "kibouchi": "Ancandzou bé", "category": "vetements", "emoji": "👘"},
        {"french": "Haut de salouva", "shimaore": "Body", "kibouchi": "Body", "category": "vetements", "emoji": "👙"},
        {"french": "T-shirt", "shimaore": "Kandzou", "kibouchi": "Kandzou", "category": "vetements", "emoji": "👕"},
        {"french": "Chaussures", "shimaore": "Kabwa", "kibouchi": "Kabwa", "category": "vetements", "emoji": "👠"},
        {"french": "Baskets/Sneakers", "shimaore": "Magochi", "kibouchi": "Magochi", "category": "vetements", "emoji": "👟"},
        {"french": "Tongs", "shimaore": "Sapatri", "kibouchi": "Sapatri", "category": "vetements", "emoji": "🩴"},
        {"french": "Jupe", "shimaore": "Jipo", "kibouchi": "Jipo", "category": "vetements", "emoji": "👗"},
        {"french": "Robe", "shimaore": "Robo", "kibouchi": "Robo", "category": "vetements", "emoji": "👗"},
        {"french": "Voile", "shimaore": "Kichali", "kibouchi": "Kichali", "category": "vetements", "emoji": "🧕"},
        
        # TRADITION (16 mots) - Données complètes du PDF
        {"french": "Mariage", "shimaore": "Haroussi", "kibouchi": "Haroussi", "category": "tradition", "emoji": "💒"},
        {"french": "Chant mariage traditionnel", "shimaore": "Mlélézi", "kibouchi": "Mlélézi", "category": "tradition", "emoji": "🎵"},
        {"french": "Fiançailles", "shimaore": "Mafounguidzo", "kibouchi": "Mafounguidzo", "category": "tradition", "emoji": "💍"},
        {"french": "Grand mariage", "shimaore": "Manzaraka", "kibouchi": "Manzaraka", "category": "tradition", "emoji": "👑"},
        {"french": "Chant religieux homme", "shimaore": "Moulidi/Dahira/Dinahou", "kibouchi": "Moulidi/Dahira/Dinahou", "category": "tradition", "emoji": "🕌"},
        {"french": "Chant religieux mixte", "shimaore": "Shengué/Madjlis", "kibouchi": "Shengué/Madjlis", "category": "tradition", "emoji": "🕌"},
        {"french": "Chant religieux femme", "shimaore": "Déba", "kibouchi": "Déba", "category": "tradition", "emoji": "🕌"},
        {"french": "Danse traditionnelle mixte", "shimaore": "Shigoma", "kibouchi": "Shigoma", "category": "tradition", "emoji": "💃"},
        {"french": "Danse traditionnelle femme", "shimaore": "Mbiwi/Wadhaha", "kibouchi": "Mbiwi/Wadhaha", "category": "tradition", "emoji": "💃"},
        {"french": "Chant traditionnel", "shimaore": "Mgodro", "kibouchi": "Mgodro", "category": "tradition", "emoji": "🎵"},
        {"french": "Barbecue traditionnelle", "shimaore": "Voulé", "kibouchi": "Voulé", "category": "tradition", "emoji": "🔥"},
        {"french": "Tamtam bœuf", "shimaore": "Ngoma ya nyombé", "kibouchi": "Ngoma ya nyombé", "category": "tradition", "emoji": "🥁"},
        {"french": "Cérémonie", "shimaore": "Shouhouli", "kibouchi": "Shouhouli", "category": "tradition", "emoji": "🎉"},
        {"french": "Boxe traditionnelle", "shimaore": "Mrengué", "kibouchi": "Mouringui", "category": "tradition", "emoji": "🥊"},
        {"french": "Campement", "shimaore": "Tobé", "kibouchi": "Tobé", "category": "tradition", "emoji": "⛺"},
        {"french": "Rite de la pluie", "shimaore": "Mgourou", "kibouchi": "Mgourou", "category": "tradition", "emoji": "🌧️"},
    ]
    
    return authentic_words

def insert_authentic_vocabulary(db):
    """Insérer le vocabulaire authentique dans la base de données"""
    
    print("🚀 Insertion du vocabulaire authentique de l'utilisateur...")
    
    # Obtenir les données authentiques
    authentic_words = create_authentic_vocabulary()
    
    # Préparer les documents pour l'insertion
    documents = []
    for word_data in authentic_words:
        document = {
            "id": str(uuid.uuid4()),
            "french": word_data["french"],
            "shimaore": word_data["shimaore"],
            "kibouchi": word_data["kibouchi"],
            "category": word_data["category"],
            "difficulty": 1,  # Difficulté de base
            "emoji": word_data.get("emoji", ""),
            "created_at": datetime.now(),
            "source": "authentic_user_pdf"
        }
        documents.append(document)
    
    # Insérer tous les documents
    try:
        result = db.words.insert_many(documents)
        print(f"✅ {len(result.inserted_ids)} mots authentiques insérés")
        
        # Statistiques par catégorie
        categories = {}
        for doc in documents:
            cat = doc["category"]
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        
        print(f"\n📊 Répartition par catégories:")
        for cat, count in sorted(categories.items()):
            print(f"  ✅ {cat}: {count} mots")
        
        print(f"\n🎯 Total: {len(documents)} mots authentiques")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion : {e}")
        return False

def main():
    """Script principal de restauration"""
    
    print("=" * 80)
    print("🔥 RESTAURATION DÉFINITIVE DE LA BASE DE DONNÉES AUTHENTIQUE")
    print("=" * 80)
    print("Source: vocabulaire shimaoré kibouchi FR.pdf")
    print("Aucune donnée inventée - UNIQUEMENT vos traductions authentiques")
    print("=" * 80)
    
    # Connexion MongoDB
    client = get_mongo_client()
    if not client:
        return False
    
    db = client[DB_NAME]
    
    # Vider complètement la base de données
    print("\n🗑️ VIDAGE COMPLET DE LA BASE DE DONNÉES...")
    if not clear_database(db):
        return False
    
    # Insérer le vocabulaire authentique
    print("\n📚 INSERTION DU VOCABULAIRE AUTHENTIQUE...")
    if not insert_authentic_vocabulary(db):
        return False
    
    # Vérification finale
    print("\n🔍 VÉRIFICATION FINALE...")
    try:
        total_words = db.words.count_documents({})
        categories = db.words.distinct("category")
        
        print(f"✅ Total mots dans la base : {total_words}")
        print(f"✅ Catégories : {len(categories)}")
        print(f"✅ Liste des catégories : {', '.join(sorted(categories))}")
        
        if total_words > 500:
            print(f"\n🎉 SUCCÈS ! Base de données authentique restaurée avec {total_words} mots")
            print("📝 Toutes les traductions proviennent de votre PDF authentique")
            print("✅ Aucune donnée inventée ou erronée")
            return True
        else:
            print(f"\n❌ Erreur : Seulement {total_words} mots (attendu > 500)")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification : {e}")
        return False
    
    finally:
        client.close()

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 BASE DE DONNÉES AUTHENTIQUE RESTAURÉE AVEC SUCCÈS!")
        print("🔥 Prête pour les intégrations audio!")
    else:
        print("\n❌ ÉCHEC DE LA RESTAURATION")
    
    exit(0 if success else 1)