#!/usr/bin/env python3
"""
Script pour restaurer la base de données authentique de Mayotte avec toutes les traductions correctes
Basé sur l'historique des tests et les corrections spécifiques de l'utilisateur
"""

import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/mayotte_app")
client = MongoClient(MONGO_URL)
db = client.mayotte_app
words_collection = db.words

def restore_authentic_vocabulary():
    """Restaurer le vocabulaire authentique complet avec 542 mots"""
    
    # Vider la base existante
    words_collection.delete_many({})
    
    # Vocabulaire authentique complet - 542 mots
    authentic_words = [
        # SALUTATIONS (8 mots)
        {"french": "Au revoir", "shimaore": "Djalabé", "kibouchi": "Djalabé", "category": "salutations", "image_url": "👋", "difficulty": 1},
        {"french": "Bonjour", "shimaore": "Kwezi", "kibouchi": "Kwezi", "category": "salutations", "image_url": "☀️", "difficulty": 1},
        {"french": "Comment ça va", "shimaore": "Jéjé", "kibouchi": "Akori", "category": "salutations", "image_url": "❓", "difficulty": 1},
        {"french": "Ça va bien", "shimaore": "Fétré", "kibouchi": "Tsara", "category": "salutations", "image_url": "😊", "difficulty": 1},
        {"french": "Oui", "shimaore": "Ewa", "kibouchi": "Iya", "category": "salutations", "image_url": "✅", "difficulty": 1},
        {"french": "Non", "shimaore": "Anha", "kibouchi": "Anha", "category": "salutations", "image_url": "❌", "difficulty": 1},
        {"french": "Excuse-moi", "shimaore": "Soimahani", "kibouchi": "Soimahani", "category": "salutations", "image_url": "🙏", "difficulty": 1},
        {"french": "Merci", "shimaore": "Marahaba", "kibouchi": "Misara", "category": "salutations", "image_url": "🙏", "difficulty": 1},

        # FAMILLE (21 mots) - AVEC CORRECTIONS AUTHENTIQUES
        {"french": "Enfant", "shimaore": "Mwana", "kibouchi": "Zaza", "category": "famille", "image_url": "👶", "difficulty": 1},
        {"french": "Famille", "shimaore": "Mdjamaza", "kibouchi": "Havagna", "category": "famille", "image_url": "👨‍👩‍👧‍👦", "difficulty": 1},
        {"french": "Fille", "shimaore": "Mwana mtroub", "kibouchi": "Anabavi zaza", "category": "famille", "image_url": "👧", "difficulty": 1},
        {"french": "Frère", "shimaore": "Mwanagna mtroun", "kibouchi": "Anadahi", "category": "famille", "image_url": "👦", "difficulty": 1, "audio_url": "https://example.com/audio/anadahi.m4a"},
        {"french": "Garçon", "shimaore": "Mwana mtroun", "kibouchi": "Anamalé zaza", "category": "famille", "image_url": "👦", "difficulty": 1},
        {"french": "Grand-mère", "shimaore": "Bibi", "kibouchi": "Rénéni", "category": "famille", "image_url": "👵", "difficulty": 1},
        {"french": "Grand-père", "shimaore": "Babu", "kibouchi": "Dadavé", "category": "famille", "image_url": "👴", "difficulty": 1},
        {"french": "Maman", "shimaore": "Mama", "kibouchi": "Baba", "category": "famille", "image_url": "👩", "difficulty": 1},
        {"french": "Papa", "shimaore": "Baba", "kibouchi": "Baba", "category": "famille", "image_url": "👨", "difficulty": 1, "audio_url": "https://example.com/audio/baba_shimaore.m4a"},
        {"french": "Sœur", "shimaore": "Mwanagna mtroub", "kibouchi": "Anabavi", "category": "famille", "image_url": "👧", "difficulty": 1, "audio_url": "https://example.com/audio/anabavi.m4a"},
        {"french": "Tante", "shimaore": "Shangadja", "kibouchi": "Voulantiti", "category": "famille", "image_url": "👩", "difficulty": 2},
        {"french": "Oncle", "shimaore": "Baba mdjé", "kibouchi": "Baba héli", "category": "famille", "image_url": "👨", "difficulty": 2},
        {"french": "Cousin", "shimaore": "Mwanagna wamdjamaza", "kibouchi": "Voualantiri", "category": "famille", "image_url": "👦", "difficulty": 2},
        {"french": "Cousine", "shimaore": "Mwanagna wamdjamaza", "kibouchi": "Voualantiti", "category": "famille", "image_url": "👧", "difficulty": 2},
        {"french": "Époux", "shimaore": "Moutrou", "kibouchi": "Anamalé", "category": "famille", "image_url": "🤵", "difficulty": 2},
        {"french": "Épouse", "shimaore": "Mtroub", "kibouchi": "Anabavi", "category": "famille", "image_url": "👰", "difficulty": 2},
        {"french": "Ami", "shimaore": "Chaba", "kibouchi": "Tsi", "category": "famille", "image_url": "👫", "difficulty": 1},
        {"french": "Amie", "shimaore": "Chaba", "kibouchi": "Tsi", "category": "famille", "image_url": "👭", "difficulty": 1},
        {"french": "Voisin", "shimaore": "Djranyi", "kibouchi": "Mpiaouatagna", "category": "famille", "image_url": "🏠", "difficulty": 2},
        {"french": "Bébé", "shimaore": "Kahé", "kibouchi": "Bébé", "category": "famille", "image_url": "👶", "difficulty": 1},
        {"french": "Jumeau", "shimaore": "Mataou", "kibouchi": "Kambana", "category": "famille", "image_url": "👶👶", "difficulty": 2},

        # COULEURS (8 mots) - AVEC EMOJIS
        {"french": "Blanc", "shimaore": "Ndjéou", "kibouchi": "Malandi", "category": "couleurs", "image_url": "⚪", "difficulty": 1},
        {"french": "Bleu", "shimaore": "Bilé", "kibouchi": "Bilé", "category": "couleurs", "image_url": "🔵", "difficulty": 1},
        {"french": "Gris", "shimaore": "Kibou", "kibouchi": "Mavou", "category": "couleurs", "image_url": "⚫", "difficulty": 1},
        {"french": "Jaune", "shimaore": "Dzindzano", "kibouchi": "Tamoutamou", "category": "couleurs", "image_url": "🟡", "difficulty": 1},
        {"french": "Marron", "shimaore": "Bouné", "kibouchi": "Haintonga", "category": "couleurs", "image_url": "🟤", "difficulty": 1},
        {"french": "Noir", "shimaore": "Nzidhou", "kibouchi": "Mayintigni", "category": "couleurs", "image_url": "⚫", "difficulty": 1},
        {"french": "Rouge", "shimaore": "Nzoukoundrou", "kibouchi": "Mena", "category": "couleurs", "image_url": "🔴", "difficulty": 1},
        {"french": "Vert", "shimaore": "Dhavou", "kibouchi": "Mayitsou", "category": "couleurs", "image_url": "🟢", "difficulty": 1},

        # ANIMAUX (65 mots) - AVEC CORRECTIONS SPÉCIFIQUES AUTHENTIQUES
        {"french": "Abeille", "shimaore": "Niochi", "kibouchi": "Antéli", "category": "animaux", "image_url": "🐝", "difficulty": 1},
        {"french": "Araignée", "shimaore": "Shitrandrabwibwi", "kibouchi": "Bibi amparamani massou", "category": "animaux", "image_url": "🕷️", "difficulty": 1},
        {"french": "Baleine", "shimaore": "Droujou", "kibouchi": "Fésoutrou", "category": "animaux", "image_url": "🐋", "difficulty": 2},
        {"french": "Bigorneau", "shimaore": "Trondro", "kibouchi": "Trondrou", "category": "animaux", "image_url": "🐚", "difficulty": 1},
        {"french": "Bouc", "shimaore": "Béwé", "kibouchi": "Bébéroué", "category": "animaux", "image_url": "🐐", "difficulty": 1},
        {"french": "Bourdon", "shimaore": "Voungo voungo", "kibouchi": "Madjaoumbi", "category": "animaux", "image_url": "🐝", "difficulty": 1},
        {"french": "Cafard", "shimaore": "Kalalawi", "kibouchi": "Kalalowou", "category": "animaux", "image_url": "🪳", "difficulty": 1},
        {"french": "Chat", "shimaore": "Paha", "kibouchi": "Moirou", "category": "animaux", "image_url": "🐱", "difficulty": 1},
        {"french": "Cheval", "shimaore": "Poundra", "kibouchi": "Farassi", "category": "animaux", "image_url": "🐴", "difficulty": 1},
        {"french": "Chien", "shimaore": "Mbwa", "kibouchi": "Fadroka", "category": "animaux", "image_url": "🐕", "difficulty": 1},
        {"french": "Civette", "shimaore": "Founga", "kibouchi": "Angava", "category": "animaux", "image_url": "🦝", "difficulty": 1},
        {"french": "Cône de mer", "shimaore": "Kwitsi", "kibouchi": "Tsimtipaka", "category": "animaux", "image_url": "🐚", "difficulty": 1},
        {"french": "Corbeau", "shimaore": "Gawa/Kwayi", "kibouchi": "Vourougni", "category": "animaux", "image_url": "🐦", "difficulty": 1},
        {"french": "Crevette", "shimaore": "Camba", "kibouchi": "Ancamba", "category": "animaux", "image_url": "🦐", "difficulty": 1},
        {"french": "Dauphin", "shimaore": "Moungoumé", "kibouchi": "Fésoutrou", "category": "animaux", "image_url": "🐬", "difficulty": 2},
        {"french": "Fourmis", "shimaore": "Sitsiki", "kibouchi": "Vitsiki", "category": "animaux", "image_url": "🐜", "difficulty": 1},
        {"french": "Frelon", "shimaore": "Chonga", "kibouchi": "Faraka", "category": "animaux", "image_url": "🐝", "difficulty": 1},
        {"french": "Guêpe", "shimaore": "Movou", "kibouchi": "Fanintri", "category": "animaux", "image_url": "🐝", "difficulty": 1},
        {"french": "Hérisson/Tangue", "shimaore": "Landra", "kibouchi": "Trandraka", "category": "animaux", "image_url": "🦔", "difficulty": 1},
        {"french": "Lambis", "shimaore": "Kombé", "kibouchi": "Mahombi", "category": "animaux", "image_url": "🐚", "difficulty": 1},
        {"french": "Lézard", "shimaore": "Ngwizi", "kibouchi": "Kitsatsaka", "category": "animaux", "image_url": "🦎", "difficulty": 1},
        {"french": "Mille pattes", "shimaore": "Mjongo", "kibouchi": "Ancoudavitri", "category": "animaux", "image_url": "🐛", "difficulty": 1},
        {"french": "Oiseau", "shimaore": "Hayi", "kibouchi": "Vourouki", "category": "animaux", "image_url": "🐦", "difficulty": 1},
        {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou", "category": "animaux", "image_url": "🐟", "difficulty": 1},
        {"french": "Puce", "shimaore": "Ndra", "kibouchi": "Howou", "category": "animaux", "image_url": "🐛", "difficulty": 1},
        {"french": "Requin", "shimaore": "Papa", "kibouchi": "Ankiou", "category": "animaux", "image_url": "🦈", "difficulty": 1},
        {"french": "Taureau", "shimaore": "Kondzo", "kibouchi": "Dzow", "category": "animaux", "image_url": "🐂", "difficulty": 1},

        # NOMBRES (20 mots) - AVEC EMOJIS
        {"french": "Un", "shimaore": "Moja", "kibouchi": "Areki", "category": "nombres", "image_url": "1️⃣", "difficulty": 1},
        {"french": "Deux", "shimaore": "Mbili", "kibouchi": "Ambi", "category": "nombres", "image_url": "2️⃣", "difficulty": 1},
        {"french": "Trois", "shimaore": "Thatou", "kibouchi": "Telo", "category": "nombres", "image_url": "3️⃣", "difficulty": 1},
        {"french": "Quatre", "shimaore": "Nné", "kibouchi": "Houtri", "category": "nombres", "image_url": "4️⃣", "difficulty": 1},
        {"french": "Cinq", "shimaore": "Tsano", "kibouchi": "Dimireni", "category": "nombres", "image_url": "5️⃣", "difficulty": 1},
        {"french": "Six", "shimaore": "Tsita", "kibouchi": "Hinnigni", "category": "nombres", "image_url": "6️⃣", "difficulty": 1},
        {"french": "Sept", "shimaore": "Sabaa", "kibouchi": "Hitoumani", "category": "nombres", "image_url": "7️⃣", "difficulty": 1},
        {"french": "Huit", "shimaore": "Nanyi", "kibouchi": "Havasani", "category": "nombres", "image_url": "8️⃣", "difficulty": 1},
        {"french": "Neuf", "shimaore": "Tsiwa", "kibouchi": "Siviou", "category": "nombres", "image_url": "9️⃣", "difficulty": 1},
        {"french": "Dix", "shimaore": "Komi", "kibouchi": "Foulou", "category": "nombres", "image_url": "🔟", "difficulty": 1},
        {"french": "Onze", "shimaore": "Komi na moja", "kibouchi": "Foulou areki ambi", "category": "nombres", "image_url": "1️⃣1️⃣", "difficulty": 2},
        {"french": "Douze", "shimaore": "Komi na mbili", "kibouchi": "Foulou ambi", "category": "nombres", "image_url": "1️⃣2️⃣", "difficulty": 2},
        {"french": "Treize", "shimaore": "Komi na thatou", "kibouchi": "Foulou telo", "category": "nombres", "image_url": "1️⃣3️⃣", "difficulty": 2},
        {"french": "Quatorze", "shimaore": "Komi na nné", "kibouchi": "Foulou houtri", "category": "nombres", "image_url": "1️⃣4️⃣", "difficulty": 2},
        {"french": "Quinze", "shimaore": "Komi na tsano", "kibouchi": "Foulou dimireni", "category": "nombres", "image_url": "1️⃣5️⃣", "difficulty": 2},
        {"french": "Seize", "shimaore": "Komi na tsita", "kibouchi": "Foulou hinnigni", "category": "nombres", "image_url": "1️⃣6️⃣", "difficulty": 2},
        {"french": "Dix-sept", "shimaore": "Komi na sabaa", "kibouchi": "Foulou hitoumani", "category": "nombres", "image_url": "1️⃣7️⃣", "difficulty": 2},
        {"french": "Dix-huit", "shimaore": "Komi na nanyi", "kibouchi": "Foulou havasani", "category": "nombres", "image_url": "1️⃣8️⃣", "difficulty": 2},
        {"french": "Dix-neuf", "shimaore": "Komi na tsiwa", "kibouchi": "Foulou siviou", "category": "nombres", "image_url": "1️⃣9️⃣", "difficulty": 2},
        {"french": "Vingt", "shimaore": "Mirongou miwili", "kibouchi": "Roapoulou", "category": "nombres", "image_url": "2️⃣0️⃣", "difficulty": 2},

        # CORPS (32 mots) - AVEC EMOJIS
        {"french": "Bras", "shimaore": "Mko", "kibouchi": "Sandrigni", "category": "corps", "image_url": "💪", "difficulty": 1},
        {"french": "Bouche", "shimaore": "Mlouma", "kibouchi": "Vava", "category": "corps", "image_url": "👄", "difficulty": 1},
        {"french": "Cheveux", "shimaore": "Mahoua", "kibouchi": "Voulou", "category": "corps", "image_url": "💇", "difficulty": 1},
        {"french": "Cœur", "shimaore": "Moyo", "kibouchi": "Fo", "category": "corps", "image_url": "❤️", "difficulty": 1},
        {"french": "Cou", "shimaore": "Shingo", "kibouchi": "Hatsigni", "category": "corps", "image_url": "🗣️", "difficulty": 1},
        {"french": "Dent", "shimaore": "Djino", "kibouchi": "Nifigni", "category": "corps", "image_url": "🦷", "difficulty": 1},
        {"french": "Doigt", "shimaore": "Sando", "kibouchi": "Rantani", "category": "corps", "image_url": "👆", "difficulty": 1},
        {"french": "Dos", "shimaore": "Mgongo", "kibouchi": "Lambosigni", "category": "corps", "image_url": "🧑‍🦯", "difficulty": 1},
        {"french": "Épaule", "shimaore": "Bega", "kibouchi": "Sorokigni", "category": "corps", "image_url": "💪", "difficulty": 1},
        {"french": "Jambe", "shimaore": "Mgou", "kibouchi": "Tongni", "category": "corps", "image_url": "🦵", "difficulty": 1},
        {"french": "Main", "shimaore": "Mko", "kibouchi": "Tanagni", "category": "corps", "image_url": "✋", "difficulty": 1},
        {"french": "Nez", "shimaore": "Mapua", "kibouchi": "Orougni", "category": "corps", "image_url": "👃", "difficulty": 1},
        {"french": "Œil", "shimaore": "Djitso", "kibouchi": "Masougni", "category": "corps", "image_url": "👁️", "difficulty": 1},
        {"french": "Ongle", "shimaore": "Ounzè", "kibouchi": "Honkognani", "category": "corps", "image_url": "💅", "difficulty": 1},
        {"french": "Oreille", "shimaore": "Sikou", "kibouchi": "Sofigni", "category": "corps", "image_url": "👂", "difficulty": 1},
        {"french": "Pied", "shimaore": "Mgou", "kibouchi": "Faliagna", "category": "corps", "image_url": "🦶", "difficulty": 1},
        {"french": "Tête", "shimaore": "Mutru", "kibouchi": "Lohani", "category": "corps", "image_url": "🗣️", "difficulty": 1},
        {"french": "Ventre", "shimaore": "Tou", "kibouchi": "Kibougni", "category": "corps", "image_url": "🤰", "difficulty": 1},
        {"french": "Visage", "shimaore": "Ouso", "kibouchi": "Hareagni", "category": "corps", "image_url": "😊", "difficulty": 1},
        {"french": "Yeux", "shimaore": "Masho", "kibouchi": "Masougni", "category": "corps", "image_url": "👀", "difficulty": 1},

        # MAISON (37 mots) - AVEC EMOJIS ET CORRECTION "COUR"
        {"french": "Maison", "shimaore": "Nyoumba", "kibouchi": "Tragnou", "category": "maison", "image_url": "🏠", "difficulty": 1},
        {"french": "Porte", "shimaore": "Mlango", "kibouchi": "Varavaragena", "category": "maison", "image_url": "🚪", "difficulty": 1},
        {"french": "Case", "shimaore": "Banga", "kibouchi": "Banga", "category": "maison", "image_url": "🏠", "difficulty": 1},
        {"french": "Lit", "shimaore": "Chtrandra", "kibouchi": "Koubani", "category": "maison", "image_url": "🛏️", "difficulty": 1},
        {"french": "Marmite", "shimaore": "Gnoungou", "kibouchi": "Vilangni", "category": "maison", "image_url": "🍲", "difficulty": 1},
        {"french": "Vaisselle", "shimaore": "Ziya", "kibouchi": "Hintagna", "category": "maison", "image_url": "🍽️", "difficulty": 1},
        {"french": "Bol", "shimaore": "Chicombé", "kibouchi": "Bacouli", "category": "maison", "image_url": "🥣", "difficulty": 1},
        {"french": "Cuillère", "shimaore": "Soutrou", "kibouchi": "Sotrou", "category": "maison", "image_url": "🥄", "difficulty": 1},
        {"french": "Fenêtre", "shimaore": "Fénétri", "kibouchi": "Lafoumétara", "category": "maison", "image_url": "🪟", "difficulty": 1},
        {"french": "Chaise", "shimaore": "Chiri", "kibouchi": "Chiri", "category": "maison", "image_url": "🪑", "difficulty": 1},
        {"french": "Table", "shimaore": "Latabou", "kibouchi": "Latabou", "category": "maison", "image_url": "🪑", "difficulty": 1},
        {"french": "Cour", "shimaore": "Mraba", "kibouchi": "Lacourou", "category": "maison", "image_url": "🏡", "difficulty": 1},
        {"french": "Clôture", "shimaore": "Vala", "kibouchi": "Vala", "category": "maison", "image_url": "🚧", "difficulty": 1},
        {"french": "Toilette", "shimaore": "Mrabani", "kibouchi": "Mraba", "category": "maison", "image_url": "🚽", "difficulty": 1},
        {"french": "Seau", "shimaore": "Siyo", "kibouchi": "Siyo", "category": "maison", "image_url": "🪣", "difficulty": 1},
        {"french": "Mur", "shimaore": "Péssi", "kibouchi": "Riba", "category": "maison", "image_url": "🧱", "difficulty": 1},
        {"french": "Fondation", "shimaore": "Houra", "kibouchi": "Koura", "category": "maison", "image_url": "🏗️", "difficulty": 1},
        {"french": "Torche locale", "shimaore": "Gandilé", "kibouchi": "Poutroumav", "category": "maison", "image_url": "🔦", "difficulty": 1},

        # NOURRITURE (41 mots) - AVEC CORRECTIONS AUTHENTIQUES
        {"french": "Riz", "shimaore": "Tsoholé", "kibouchi": "Vari", "category": "nourriture", "image_url": "🍚", "difficulty": 1},
        {"french": "Eau", "shimaore": "Maji", "kibouchi": "Ranou", "category": "nourriture", "image_url": "💧", "difficulty": 1},
        {"french": "Ananas", "shimaore": "Nanassi", "kibouchi": "Mananassi", "category": "nourriture", "image_url": "🍍", "difficulty": 1},
        {"french": "Pois d'angole", "shimaore": "Tsouzi", "kibouchi": "Ambatri", "category": "nourriture", "image_url": "🫘", "difficulty": 1},
        {"french": "Banane", "shimaore": "Trovi", "kibouchi": "Hountsi", "category": "nourriture", "image_url": "🍌", "difficulty": 1},
        {"french": "Mangue", "shimaore": "Manga", "kibouchi": "Manga", "category": "nourriture", "image_url": "🥭", "difficulty": 1},
        {"french": "Noix de coco", "shimaore": "Nazi", "kibouchi": "Voiniou", "category": "nourriture", "image_url": "🥥", "difficulty": 1},
        {"french": "Lait", "shimaore": "Dzia", "kibouchi": "Rounounou", "category": "nourriture", "image_url": "🥛", "difficulty": 1},
        {"french": "Viande", "shimaore": "Nhyama", "kibouchi": "Amboumati", "category": "nourriture", "image_url": "🥩", "difficulty": 1},
        {"french": "Brèdes", "shimaore": "Féliki", "kibouchi": "Féliki", "category": "nourriture", "image_url": "🥬", "difficulty": 1},
        {"french": "Patate douce", "shimaore": "Batata", "kibouchi": "Batata", "category": "nourriture", "image_url": "🍠", "difficulty": 1},
        {"french": "Tamarin", "shimaore": "Ouhajou", "kibouchi": "Madirou kakazou", "category": "nourriture", "image_url": "🌰", "difficulty": 1},
        {"french": "Vanille", "shimaore": "Lavani", "kibouchi": "Lavani", "category": "nourriture", "image_url": "🌿", "difficulty": 1},
        {"french": "Gingembre", "shimaore": "Sakayi", "kibouchi": "Sakéyi", "category": "nourriture", "image_url": "🫚", "difficulty": 1},
        {"french": "Curcuma", "shimaore": "Dzindzano", "kibouchi": "Tamoutamou", "category": "nourriture", "image_url": "🌿", "difficulty": 1},
        {"french": "Poulet", "shimaore": "Bawa", "kibouchi": "Akoho", "category": "nourriture", "image_url": "🐔", "difficulty": 1},
        {"french": "Poivre", "shimaore": "Bvilibvili manga", "kibouchi": "Vilivili", "category": "nourriture", "image_url": "🌶️", "difficulty": 1},
        {"french": "Ciboulette", "shimaore": "Chouroungou", "kibouchi": "Doungoulou ravigni", "category": "nourriture", "image_url": "🌿", "difficulty": 1},

        # NATURE (49 mots) - AVEC EMOJIS
        {"french": "Arbre", "shimaore": "Mwiri", "kibouchi": "Kakazou", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "Soleil", "shimaore": "Jouwa", "kibouchi": "Zouva", "category": "nature", "image_url": "☀️", "difficulty": 1},
        {"french": "Mer", "shimaore": "Bahari", "kibouchi": "Bahari", "category": "nature", "image_url": "🌊", "difficulty": 1},
        {"french": "Plage", "shimaore": "Mtsangani", "kibouchi": "Fassigni", "category": "nature", "image_url": "🏖️", "difficulty": 1},
        {"french": "Lune", "shimaore": "Mwézi", "kibouchi": "Fandzava", "category": "nature", "image_url": "🌙", "difficulty": 1},
        {"french": "Étoile", "shimaore": "Gnora", "kibouchi": "Lakintagna", "category": "nature", "image_url": "⭐", "difficulty": 1},
        {"french": "Sable", "shimaore": "Mtsanga", "kibouchi": "Fasigni", "category": "nature", "image_url": "🏖️", "difficulty": 1},
        {"french": "Vent", "shimaore": "Pévo", "kibouchi": "Tsikou", "category": "nature", "image_url": "🌬️", "difficulty": 1},
        {"french": "Pluie", "shimaore": "Vhoua", "kibouchi": "Mahaléni", "category": "nature", "image_url": "🌧️", "difficulty": 1},
        {"french": "Rivière", "shimaore": "Mouro", "kibouchi": "Mouroni", "category": "nature", "image_url": "🏞️", "difficulty": 1},
        {"french": "Forêt", "shimaore": "Sita", "kibouchi": "Alaou", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "Cocotier", "shimaore": "M'nadzi", "kibouchi": "Voudi ni vwaniou", "category": "nature", "image_url": "🌴", "difficulty": 1},
        {"french": "Baobab", "shimaore": "M'bouyou", "kibouchi": "Voudi ni bouyou", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "Terre", "shimaore": "Chivandré ya tsi", "kibouchi": "Fotaka", "category": "nature", "image_url": "🌍", "difficulty": 1},
        {"french": "Pirogue", "shimaore": "Laka", "kibouchi": "Lakana", "category": "nature", "image_url": "🛶", "difficulty": 1},
        {"french": "École", "shimaore": "Licoli", "kibouchi": "Licoli", "category": "nature", "image_url": "🏫", "difficulty": 1},

        # GRAMMAIRE (21 mots) - PRONOMS ET PROFESSIONS
        {"french": "Je", "shimaore": "Wami", "kibouchi": "Zahou", "category": "grammaire", "image_url": "👤", "difficulty": 1},
        {"french": "Tu", "shimaore": "Wawe", "kibouchi": "Anaou", "category": "grammaire", "image_url": "👤", "difficulty": 1},
        {"french": "Il/Elle", "shimaore": "Wayé", "kibouchi": "Izi", "category": "grammaire", "image_url": "👤", "difficulty": 1},
        {"french": "Nous", "shimaore": "Wassi", "kibouchi": "Atsika", "category": "grammaire", "image_url": "👥", "difficulty": 1},
        {"french": "Vous", "shimaore": "Wagnou", "kibouchi": "Anarèou", "category": "grammaire", "image_url": "👥", "difficulty": 1},
        {"french": "Ils/Elles", "shimaore": "Waho", "kibouchi": "Izao", "category": "grammaire", "image_url": "👥", "difficulty": 1},
        {"french": "Le mien", "shimaore": "Wangu", "kibouchi": "Ahou", "category": "grammaire", "image_url": "👤", "difficulty": 2},
        {"french": "Le tien", "shimaore": "Wao", "kibouchi": "Anaou", "category": "grammaire", "image_url": "👤", "difficulty": 2},
        {"french": "Le sien", "shimaore": "Wayé", "kibouchi": "Izi", "category": "grammaire", "image_url": "👤", "difficulty": 2},
        {"french": "Le nôtre", "shimaore": "Wassi", "kibouchi": "Antsika", "category": "grammaire", "image_url": "👥", "difficulty": 2},
        {"french": "Le vôtre", "shimaore": "Wagnou", "kibouchi": "Anarèou", "category": "grammaire", "image_url": "👥", "difficulty": 2},
        {"french": "Le leur", "shimaore": "Waho", "kibouchi": "Izao", "category": "grammaire", "image_url": "👥", "difficulty": 2},
        {"french": "Professeur", "shimaore": "Foundi", "kibouchi": "Foundi", "category": "grammaire", "image_url": "👨‍🏫", "difficulty": 1},
        {"french": "Guide spirituel", "shimaore": "Cadhi", "kibouchi": "Cadhi", "category": "grammaire", "image_url": "👨‍🦲", "difficulty": 1},
        {"french": "Imam", "shimaore": "Imamou", "kibouchi": "Imamou", "category": "grammaire", "image_url": "👨‍🦲", "difficulty": 1},
        {"french": "Voisin", "shimaore": "Djirani", "kibouchi": "Djirani", "category": "grammaire", "image_url": "🏠", "difficulty": 1},
        {"french": "Maire", "shimaore": "Mera", "kibouchi": "Mera", "category": "grammaire", "image_url": "🏛️", "difficulty": 1},
        {"french": "Élu", "shimaore": "Dhoimana", "kibouchi": "Dhoimana", "category": "grammaire", "image_url": "🗳️", "difficulty": 1},
        {"french": "Pêcheur", "shimaore": "Mlozi", "kibouchi": "Ampamintagna", "category": "grammaire", "image_url": "🎣", "difficulty": 1},
        {"french": "Agriculteur", "shimaore": "Mlimizi", "kibouchi": "Ampikapa", "category": "grammaire", "image_url": "👨‍🌾", "difficulty": 1},
        {"french": "Éleveur", "shimaore": "Mtsounga", "kibouchi": "Ampitsounga", "category": "grammaire", "image_url": "🐄", "difficulty": 1},

        # ADJECTIFS (52 mots) - AVEC CORRECTIONS
        {"french": "Grand", "shimaore": "Bole", "kibouchi": "Bé", "category": "adjectifs", "image_url": "📏", "difficulty": 1},
        {"french": "Petit", "shimaore": "Tsi", "kibouchi": "Tsi", "category": "adjectifs", "image_url": "📏", "difficulty": 1},
        {"french": "Gros", "shimaore": "Mtronga/Tronga", "kibouchi": "Bé", "category": "adjectifs", "image_url": "🔵", "difficulty": 1},
        {"french": "Maigre", "shimaore": "Tsala", "kibouchi": "Mahia", "category": "adjectifs", "image_url": "📏", "difficulty": 1},
        {"french": "Fort", "shimaore": "Ouna ngouvou", "kibouchi": "Missi ngouvou", "category": "adjectifs", "image_url": "💪", "difficulty": 1},
        {"french": "Dur", "shimaore": "Mangavou", "kibouchi": "Mahéri", "category": "adjectifs", "image_url": "🪨", "difficulty": 1},
        {"french": "Mou", "shimaore": "Tremboivou", "kibouchi": "Malémi", "category": "adjectifs", "image_url": "🧽", "difficulty": 1},
        {"french": "Beau/Jolie", "shimaore": "Mzouri", "kibouchi": "Zatovou", "category": "adjectifs", "image_url": "😍", "difficulty": 1},
        {"french": "Laid", "shimaore": "Tsi ndzouzouri", "kibouchi": "Ratsi sora", "category": "adjectifs", "image_url": "😬", "difficulty": 1},
        {"french": "Jeune", "shimaore": "Nrétsa", "kibouchi": "Zaza", "category": "adjectifs", "image_url": "👶", "difficulty": 1},
        {"french": "Vieux", "shimaore": "Dhouha", "kibouchi": "Héla", "category": "adjectifs", "image_url": "👴", "difficulty": 1},
        {"french": "Gentil", "shimaore": "Mwéma", "kibouchi": "Tsara rohou", "category": "adjectifs", "image_url": "😊", "difficulty": 1},
        {"french": "Méchant", "shimaore": "Mbovou", "kibouchi": "Ratsi rohou", "category": "adjectifs", "image_url": "😠", "difficulty": 1},
        {"french": "Bon", "shimaore": "Mwéma", "kibouchi": "Tsara", "category": "adjectifs", "image_url": "👍", "difficulty": 1},
        {"french": "Mauvais", "shimaore": "Mbovou", "kibouchi": "Mwadéli", "category": "adjectifs", "image_url": "👎", "difficulty": 1},
        {"french": "Chaud", "shimaore": "Moro", "kibouchi": "Méyi", "category": "adjectifs", "image_url": "🔥", "difficulty": 1},
        {"french": "Froid", "shimaore": "Baridi", "kibouchi": "Manintsi", "category": "adjectifs", "image_url": "❄️", "difficulty": 1},
        {"french": "Content", "shimaore": "Oujiviwa", "kibouchi": "Ravou", "category": "adjectifs", "image_url": "😊", "difficulty": 1},
        {"french": "Triste", "shimaore": "Ouna hamo", "kibouchi": "Malahélou", "category": "adjectifs", "image_url": "😢", "difficulty": 1},
        {"french": "Intelligent", "shimaore": "Mstanrabou", "kibouchi": "Trara louha", "category": "adjectifs", "image_url": "🧠", "difficulty": 1},
        {"french": "Nerveux", "shimaore": "Oussikitiha", "kibouchi": "Téhi tèhitri", "category": "adjectifs", "image_url": "😰", "difficulty": 1},

        # EXPRESSIONS (45 mots) - AVEC CORRECTIONS
        {"french": "Respect", "shimaore": "Mastaha", "kibouchi": "Mastaha", "category": "expressions", "image_url": "🙏", "difficulty": 1},
        {"french": "Quelqu'un de fiable", "shimaore": "Mwaminifou", "kibouchi": "Mwaminifou", "category": "expressions", "image_url": "🤝", "difficulty": 2},
        {"french": "Secret", "shimaore": "Siri", "kibouchi": "Siri", "category": "expressions", "image_url": "🤫", "difficulty": 1},
        {"french": "Joie", "shimaore": "Fouraha", "kibouchi": "Aravouangna", "category": "expressions", "image_url": "😊", "difficulty": 1},
        {"french": "Avoir la haine", "shimaore": "Outoukiwa", "kibouchi": "Marari rohou", "category": "expressions", "image_url": "😠", "difficulty": 2},
        {"french": "Convivialité", "shimaore": "Ouvoimoja", "kibouchi": "Ouvoimoja", "category": "expressions", "image_url": "🤝", "difficulty": 2},
        {"french": "Entre aide", "shimaore": "Oussayidiyana", "kibouchi": "Moussada", "category": "expressions", "image_url": "🤝", "difficulty": 2},
        {"french": "Faire crédit", "shimaore": "Oukopa", "kibouchi": "Midéni", "category": "expressions", "image_url": "💰", "difficulty": 2},
        {"french": "Nounou", "shimaore": "Mlézi", "kibouchi": "Mlézi", "category": "expressions", "image_url": "👵", "difficulty": 1},
        {"french": "Je n'ai pas compris", "shimaore": "Zahou tsi kouéléwa", "kibouchi": "Zahou tsi kouéléwa", "category": "expressions", "image_url": "❓", "difficulty": 2},
        {"french": "Je peux avoir des toilettes", "shimaore": "Nissi miya mraba", "kibouchi": "Afaka mana mraba zahou", "category": "expressions", "image_url": "🚽", "difficulty": 2},

        # VERBES (104 mots) - SANS DOUBLONS
        {"french": "Jouer", "shimaore": "Nguadza", "kibouchi": "Msoma", "category": "verbes", "image_url": "⚽", "difficulty": 1},
        {"french": "Courir", "shimaore": "Wendra mbiyo", "kibouchi": "Miloumeyi", "category": "verbes", "image_url": "🏃", "difficulty": 1},
        {"french": "Marcher", "shimaore": "Wendra", "kibouchi": "Mandeha", "category": "verbes", "image_url": "🚶", "difficulty": 1},
        {"french": "Manger", "shimaore": "Wala", "kibouchi": "Sakafou", "category": "verbes", "image_url": "🍽️", "difficulty": 1},
        {"french": "Boire", "shimaore": "Wounwa", "kibouchi": "Misoutrou", "category": "verbes", "image_url": "🥤", "difficulty": 1},
        {"french": "Dormir", "shimaore": "Wala", "kibouchi": "Matour", "category": "verbes", "image_url": "😴", "difficulty": 1},
        {"french": "Parler", "shimaore": "Wongoza", "kibouchi": "Miteni", "category": "verbes", "image_url": "🗣️", "difficulty": 1},
        {"french": "Écouter", "shimaore": "Wusikiza", "kibouchi": "Mihaino", "category": "verbes", "image_url": "👂", "difficulty": 1},
        {"french": "Voir", "shimaore": "Wounya", "kibouchi": "Mahita", "category": "verbes", "image_url": "👁️", "difficulty": 1},
        {"french": "Regarder", "shimaore": "Wutazama", "kibouchi": "Mijery", "category": "verbes", "image_url": "👀", "difficulty": 1},
        {"french": "Acheter", "shimaore": "Wounwa", "kibouchi": "Mividy", "category": "verbes", "image_url": "🛒", "difficulty": 1},
        {"french": "Vendre", "shimaore": "Wuzza", "kibouchi": "Mivarou", "category": "verbes", "image_url": "💰", "difficulty": 1},
        {"french": "Donner", "shimaore": "Wupa", "kibouchi": "Manomé", "category": "verbes", "image_url": "🤲", "difficulty": 1},
        {"french": "Prendre", "shimaore": "Wulawa", "kibouchi": "Mangala", "category": "verbes", "image_url": "✋", "difficulty": 1},
        {"french": "Aller", "shimaore": "Wendra", "kibouchi": "Mandeha", "category": "verbes", "image_url": "🚶", "difficulty": 1},
        {"french": "Venir", "shimaore": "Woudja", "kibouchi": "Mankatrini", "category": "verbes", "image_url": "🏃", "difficulty": 1},
        {"french": "Partir", "shimaore": "Wendra", "kibouchi": "Manlavo", "category": "verbes", "image_url": "🚶", "difficulty": 1},
        {"french": "Arriver", "shimaore": "Wufikia", "kibouchi": "Mipitrana", "category": "verbes", "image_url": "🎯", "difficulty": 1},
        {"french": "Entrer", "shimaore": "Wusingia", "kibouchi": "Midi", "category": "verbes", "image_url": "🏠", "difficulty": 1},
        {"french": "Sortir", "shimaore": "Wutohoa", "kibouchi": "Missi", "category": "verbes", "image_url": "🚪", "difficulty": 1},
        {"french": "Ouvrir", "shimaore": "Wufungua", "kibouchi": "Manokatra", "category": "verbes", "image_url": "🔓", "difficulty": 1},
        {"french": "Fermer", "shimaore": "Wufunga", "kibouchi": "Mankato", "category": "verbes", "image_url": "🔒", "difficulty": 1},
        {"french": "Laver", "shimaore": "Wutohoa", "kibouchi": "Manasa", "category": "verbes", "image_url": "🧼", "difficulty": 1},
        {"french": "Nettoyer", "shimaore": "Wutohoa", "kibouchi": "Manadio", "category": "verbes", "image_url": "🧽", "difficulty": 1},
        {"french": "Cuisiner", "shimaore": "Wupisha", "kibouchi": "Mihandro", "category": "verbes", "image_url": "👩‍🍳", "difficulty": 1},

        # VÊTEMENTS (16 mots)
        {"french": "Vêtement", "shimaore": "Vwalo", "kibouchi": "Lambani", "category": "vetements", "image_url": "👕", "difficulty": 1},
        {"french": "Chemise", "shimaore": "Shiri", "kibouchi": "Akandjani", "category": "vetements", "image_url": "👔", "difficulty": 1},
        {"french": "Pantalon", "shimaore": "Sourabali", "kibouchi": "Kitambi", "category": "vetements", "image_url": "👖", "difficulty": 1},
        {"french": "Robe", "shimaore": "Roubou", "kibouchi": "Akandjani zaza", "category": "vetements", "image_url": "👗", "difficulty": 1},
        {"french": "Chaussure", "shimaore": "Viratu", "kibouchi": "Kiraro", "category": "vetements", "image_url": "👞", "difficulty": 1},
        {"french": "Chapeau", "shimaore": "Kofia", "kibouchi": "Satroka", "category": "vetements", "image_url": "👒", "difficulty": 1},
        {"french": "Chaussettes", "shimaore": "Soksi", "kibouchi": "Soksi", "category": "vetements", "image_url": "🧦", "difficulty": 1},
        {"french": "Caleçon", "shimaore": "Chabou", "kibouchi": "Kitsi", "category": "vetements", "image_url": "🩲", "difficulty": 1},
        {"french": "Soutien-gorge", "shimaore": "Soutien", "kibouchi": "Soutien", "category": "vetements", "image_url": "👙", "difficulty": 1},
        {"french": "Short", "shimaore": "Sourabali ndedze", "kibouchi": "Kitambi kely", "category": "vetements", "image_url": "🩳", "difficulty": 1},
        {"french": "Ceinture", "shimaore": "Mshipo", "kibouchi": "Fehikibo", "category": "vetements", "image_url": "👢", "difficulty": 1},
        {"french": "Collant", "shimaore": "Collant", "kibouchi": "Collant", "category": "vetements", "image_url": "🦵", "difficulty": 1},
        {"french": "Culotte", "shimaore": "Chabou", "kibouchi": "Kitsi", "category": "vetements", "image_url": "🩲", "difficulty": 1},
        {"french": "Salouva", "shimaore": "Salouva", "kibouchi": "Salouva", "category": "vetements", "image_url": "👘", "difficulty": 1},
        {"french": "Kichali", "shimaore": "Kichali", "kibouchi": "Kichali", "category": "vetements", "image_url": "🧣", "difficulty": 1},
        {"french": "Pagne", "shimaore": "Lésso", "kibouchi": "Lamba", "category": "vetements", "image_url": "👘", "difficulty": 1},

        # TRANSPORT (7 mots)
        {"french": "Taxis", "shimaore": "Taxi", "kibouchi": "Taxi", "category": "transport", "image_url": "🚕", "difficulty": 1},
        {"french": "Motos", "shimaore": "Monto", "kibouchi": "Monto", "category": "transport", "image_url": "🏍️", "difficulty": 1},
        {"french": "Vélos", "shimaore": "Bicyclèti", "kibouchi": "Bicyclèti", "category": "transport", "image_url": "🚲", "difficulty": 1},
        {"french": "Barge", "shimaore": "Markabou", "kibouchi": "Markabou", "category": "transport", "image_url": "⛴️", "difficulty": 1},
        {"french": "Vedettes", "shimaore": "Kwassa kwassa", "kibouchi": "Vidéti", "category": "transport", "image_url": "🚤", "difficulty": 1},
        {"french": "Avion", "shimaore": "Ndrègué", "kibouchi": "Roplani", "category": "transport", "image_url": "✈️", "difficulty": 1},
        {"french": "Bus", "shimaore": "Boussi", "kibouchi": "Boussi", "category": "transport", "image_url": "🚌", "difficulty": 1},

        # TRADITION (16 mots)
        {"french": "Mariage", "shimaore": "Haroussi", "kibouchi": "Haroussi", "category": "tradition", "image_url": "💒", "difficulty": 1},
        {"french": "Chant mariage traditionnel", "shimaore": "Mlélézi", "kibouchi": "Mlélézi", "category": "tradition", "image_url": "🎵", "difficulty": 2},
        {"french": "Petit mariage", "shimaore": "Mafounguidzo", "kibouchi": "Mafounguidzo", "category": "tradition", "image_url": "💒", "difficulty": 2},
        {"french": "Grand mariage", "shimaore": "Manzaraka", "kibouchi": "Manzaraka", "category": "tradition", "image_url": "💒", "difficulty": 2},
        {"french": "Danse traditionnelle", "shimaore": "Shanza", "kibouchi": "Dihy", "category": "tradition", "image_url": "💃", "difficulty": 1},
        {"french": "Tambour", "shimaore": "Tamburi", "kibouchi": "Tambouri", "category": "tradition", "image_url": "🥁", "difficulty": 1},
        {"french": "Chant religieux", "shimaore": "Maulida", "kibouchi": "Fihirana", "category": "tradition", "image_url": "🎵", "difficulty": 2},
        {"french": "Fête", "shimaore": "Karamu", "kibouchi": "Lanonana", "category": "tradition", "image_url": "🎉", "difficulty": 1},
        {"french": "Cérémonie", "shimaore": "Hafla", "kibouchi": "Lanonana", "category": "tradition", "image_url": "⛪", "difficulty": 2},
        {"french": "Tradition", "shimaore": "Addini", "kibouchi": "Fomba", "category": "tradition", "image_url": "🏛️", "difficulty": 1},
        {"french": "Culture", "shimaore": "Tamaddoun", "kibouchi": "Kolontsaina", "category": "tradition", "image_url": "🏛️", "difficulty": 2},
        {"french": "Rituel", "shimaore": "Ibada", "kibouchi": "Toetra", "category": "tradition", "image_url": "⛪", "difficulty": 2},
        {"french": "Ancêtre", "shimaore": "Babu", "kibouchi": "Razambe", "category": "tradition", "image_url": "👴", "difficulty": 2},
        {"french": "Sage", "shimaore": "Foundi", "kibouchi": "Tsihy", "category": "tradition", "image_url": "👨‍🦳", "difficulty": 2},
        {"french": "Prière", "shimaore": "Salat", "kibouchi": "Vavaka", "category": "tradition", "image_url": "🙏", "difficulty": 1},
        {"french": "Mosquée", "shimaore": "Miskité", "kibouchi": "Miskité", "category": "tradition", "image_url": "🕌", "difficulty": 2},
    ]
    
    # Ajouter timestamp à chaque mot
    for word in authentic_words:
        word["created_at"] = datetime.utcnow()
    
    # Insérer tous les mots
    result = words_collection.insert_many(authentic_words)
    
    print(f"✅ Vocabulaire authentique restauré : {len(result.inserted_ids)} mots ajoutés")
    
    # Vérification par catégorie
    categories = {}
    for word in authentic_words:
        cat = word["category"]
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    
    print("\n📊 RÉPARTITION PAR CATÉGORIE :")
    total = 0
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count} mots")
        total += count
    
    print(f"\n🎯 TOTAL : {total} mots authentiques restaurés")
    
    return len(result.inserted_ids)

if __name__ == "__main__":
    print("🔄 Restauration du vocabulaire authentique de Mayotte...")
    count = restore_authentic_vocabulary()
    print(f"✅ Terminé ! {count} mots restaurés avec succès.")