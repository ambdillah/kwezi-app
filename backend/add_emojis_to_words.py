#!/usr/bin/env python3
"""
AJOUT D'ÉMOJIS AUX MOTS ET EXPRESSIONS
=====================================
Associe des émojis aux mots de la base de données UNIQUEMENT quand c'est 
clair et approprié pour les enfants. Sinon, ne met rien.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def get_database():
    """Connexion à la base de données MongoDB"""
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    client = MongoClient(mongo_url)
    db_name = os.getenv('DB_NAME', 'mayotte_app')
    db = client[db_name]
    return db

def create_emoji_mapping():
    """
    Crée un mapping des mots français vers des émojis appropriés pour les enfants.
    Uniquement les émojis clairs et évidents.
    """
    emoji_mapping = {
        # FAMILLE - émojis clairs pour la famille
        "Papa": "👨",
        "Maman": "👩", 
        "Enfant": "👶",
        "Bébé": "👶",
        "Frère": "👦",
        "Sœur": "👧",
        "Grand-père": "👴",
        "Grand-mère": "👵",
        "Garçon": "👦",
        "Fille": "👧",
        "Ami": "👫",
        "Famille": "👨‍👩‍👧‍👦",
        
        # COULEURS - cercles colorés
        "Rouge": "🔴",
        "Bleu": "🔵",
        "Vert": "🟢",
        "Jaune": "🟡",
        "Noir": "⚫",
        "Blanc": "⚪",
        "Marron": "🟤",
        "Orange": "🟠",
        "Violet": "🟣",
        "Rose": "🩷",
        "Gris": "⚫",
        
        # NOMBRES - chiffres émojis
        "Un": "1️⃣",
        "Deux": "2️⃣", 
        "Trois": "3️⃣",
        "Quatre": "4️⃣",
        "Cinq": "5️⃣",
        "Six": "6️⃣",
        "Sept": "7️⃣",
        "Huit": "8️⃣",
        "Neuf": "9️⃣",
        "Dix": "🔟",
        
        # ANIMAUX - émojis d'animaux évidents
        "Chat": "🐱",
        "Chien": "🐕",
        "Poisson": "🐟",
        "Oiseau": "🐦",
        "Éléphant": "🐘",
        "Lion": "🦁",
        "Souris": "🐭",
        "Poule": "🐔",
        "Cochon": "🐷",
        "Vache": "🐄",
        "Cheval": "🐴",
        "Mouton": "🐑",
        "Chèvre": "🐐",
        "Âne": "🫏",
        "Canard": "🦆",
        "Papillon": "🦋",
        "Abeille": "🐝",
        "Araignée": "🕷️",
        "Serpent": "🐍",
        "Grenouille": "🐸",
        "Tortue": "🐢",
        "Crabe": "🦀",
        "Crevette": "🦐",
        "Escargot": "🐌",
        "Fourmis": "🐜",
        "Mouche": "🪰",
        "Moustique": "🦟",
        "Singe": "🐒",
        "Corbeau": "🐦‍⬛",
        "Pigeon": "🕊️",
        "Perroquet": "🦜",
        
        # CORPS HUMAIN - parties visibles et appropriées
        "Tête": "🧠",
        "Main": "✋",
        "Pied": "🦶",
        "Œil": "👁️",
        "Nez": "👃",
        "Oreille": "👂",
        "Bouche": "👄",
        "Dent": "🦷",
        "Cheveux": "💇",
        "Doigts": "👆",
        "Ongle": "💅",
        "Barbe": "🧔",
        
        # NOURRITURE - aliments évidents
        "Pain": "🍞",
        "Eau": "💧",
        "Lait": "🥛",
        "Œuf": "🥚",
        "Poisson": "🐟",
        "Viande": "🥩",
        "Riz": "🍚",
        "Banane": "🍌",
        "Pomme": "🍎",
        "Orange": "🍊",
        "Ananas": "🍍",
        "Mangue": "🥭",
        "Noix de coco": "🥥",
        "Café": "☕",
        "Thé": "🍵",
        "Sucre": "🍯",
        "Sel": "🧂",
        "Piment": "🌶️",
        "Salade": "🥗",
        "Miel": "🍯",
        
        # MAISON - objets de maison clairs
        "Maison": "🏠",
        "Porte": "🚪",
        "Lit": "🛏️",
        "Chaise": "🪑",
        "Table": "🪑",
        
        # TRANSPORT - moyens de transport
        "Voiture": "🚗",
        "Avion": "✈️",
        "Bateau": "⛵",
        "Vélo": "🚲",
        "Moto": "🏍️",
        "Pirogue": "🛶",
        "Taxi": "🚕",
        
        # VÊTEMENTS - vêtements évidents
        "Chapeau": "👒",
        "Chaussures": "👠",
        "Chemise": "👔",
        "Pantalon": "👖",
        "Robe": "👗",
        "Jupe": "👗",
        "T-shirt": "👕",
        "Lunettes": "👓",
        "Veste": "🧥",
        "Short": "🩳",
        
        # NATURE - éléments naturels
        "Soleil": "☀️",
        "Lune": "🌙",
        "Étoile": "⭐",
        "Arbre": "🌳",
        "Fleur": "🌸",
        "Mer": "🌊",
        "Plage": "🏖️",
        "Montagne": "⛰️",
        "Rivière": "🏞️",
        "Pluie": "🌧️",
        "Vent": "💨",
        "Feu": "🔥",
        "Sable": "🏖️",
        
        # SALUTATIONS - gestes et émotions
        "Bonjour": "👋",
        "Au revoir": "👋",
        "Merci": "🙏",
        "S'il vous plaît": "🙏",
        "Bonsoir": "🌆",
        "Bonne nuit": "🌙",
        
        # EXPRESSIONS - émotions et concepts clairs
        "Oui": "✅",
        "Non": "❌",
        "J'ai faim": "😋",
        "J'ai soif": "🥤",
        "Aujourd'hui": "📅",
        "Demain": "📅",
        "Hier": "📅",
        "Maintenant": "⏰",
        "Très": "💯",
        "Beaucoup": "🔢",
        "Vite": "⚡",
        
        # ADJECTIFS - concepts visuels clairs
        "Grand": "📏",
        "Petit": "📏",
        "Chaud": "🔥",
        "Froid": "❄️",
        "Beau": "😍",
        "Bon": "👍",
        "Mauvais": "👎",
        "Nouveau": "🆕",
        "Vieux": "👴",
        "Rapide": "⚡",
        "Lent": "🐌",
        "Fort": "💪",
        "Propre": "✨",
        "Sale": "🫤",
        "Ouvert": "🔓",
        "Fermé": "🔒",
        "Haut": "⬆️",
        "Bas": "⬇️",
        "Facile": "😊",
        "Difficile": "😓",
        
        # VERBES - actions claires
        "Manger": "🍽️",
        "Boire": "🥤",
        "Dormir": "😴",
        "Marcher": "🚶",
        "Courir": "🏃",
        "Jouer": "🎮",
        "Lire": "📖",
        "Écrire": "✍️",
        "Voir": "👁️",
        "Écouter": "👂",
        "Parler": "💬",
        "Chanter": "🎵",
        "Danser": "💃",
        "Cuisiner": "👨‍🍳",
        "Se laver": "🧼",
        "S'asseoir": "🪑",
        
        # GRAMMAIRE - personnages pour les pronoms
        "Je": "👤",
        "Tu": "👥",
        "Il": "👤",
        "Elle": "👤",
        "Nous": "👥",
        "Vous": "👥",
        "Ils": "👥",
        "Elles": "👥",
        
        # OBJETS SCOLAIRES
        "École": "🏫",
        "Livre": "📚",
        "Crayon": "✏️",
        "Stylo": "🖊️",
        
        # MÉTÉO ET TEMPS
        "Il pleut": "🌧️",
        "Il fait beau": "☀️",
        "Il fait chaud": "🔥",
        "Tempête": "⛈️",
        
        # MUSIQUE ET TRADITION (uniquement les évidents)
        "Musique": "🎵",
        "Danse": "💃",
        "Fête": "🎉",
    }
    
    return emoji_mapping

def add_emojis_to_database():
    """Ajoute les émojis aux mots dans la base de données"""
    print("🎨 Ajout d'émojis aux mots et expressions...")
    
    db = get_database()
    words_collection = db.words
    
    # Obtenir le mapping des émojis
    emoji_mapping = create_emoji_mapping()
    
    # Récupérer tous les mots
    all_words = list(words_collection.find())
    print(f"📊 Total des mots dans la base: {len(all_words)}")
    
    updated_count = 0
    skipped_count = 0
    
    for word in all_words:
        french_word = word['french']
        
        # Vérifier si on a un emoji approprié pour ce mot
        if french_word in emoji_mapping:
            emoji = emoji_mapping[french_word]
            
            # Mettre à jour le mot avec l'emoji
            words_collection.update_one(
                {"_id": word["_id"]},
                {"$set": {"image_url": emoji}}
            )
            print(f"✅ {french_word} → {emoji}")
            updated_count += 1
        else:
            # Pas d'emoji approprié, laisser vide
            words_collection.update_one(
                {"_id": word["_id"]},
                {"$unset": {"image_url": ""}}
            )
            skipped_count += 1
    
    print(f"\n📊 Résultats:")
    print(f"✅ Mots avec émojis ajoutés: {updated_count}")
    print(f"⏭️  Mots sans emoji (approprié): {skipped_count}")
    print(f"📝 Total traité: {updated_count + skipped_count}")
    
    return updated_count

def verify_emoji_additions():
    """Vérifie les émojis ajoutés"""
    print("🔍 Vérification des émojis ajoutés...")
    
    db = get_database()
    words_collection = db.words
    
    # Compter les mots avec et sans émojis
    words_with_emojis = words_collection.count_documents({"image_url": {"$exists": True, "$ne": ""}})
    words_without_emojis = words_collection.count_documents({"$or": [{"image_url": {"$exists": False}}, {"image_url": ""}]})
    total_words = words_collection.count_documents({})
    
    print(f"📊 Statistiques finales:")
    print(f"   Mots avec émojis: {words_with_emojis}")
    print(f"   Mots sans emoji: {words_without_emojis}")
    print(f"   Total des mots: {total_words}")
    print(f"   Pourcentage avec émojis: {(words_with_emojis/total_words*100):.1f}%")
    
    # Afficher quelques exemples par catégorie
    categories = words_collection.distinct("category")
    print(f"\n🎨 Exemples d'émojis par catégorie:")
    
    for category in sorted(categories)[:5]:  # Afficher les 5 premières catégories
        examples = list(words_collection.find(
            {"category": category, "image_url": {"$exists": True, "$ne": ""}},
            {"french": 1, "image_url": 1}
        ).limit(3))
        
        if examples:
            examples_str = ", ".join([f"{ex['french']} {ex['image_url']}" for ex in examples])
            print(f"   {category}: {examples_str}")
    
    return words_with_emojis > 0

def main():
    """Fonction principale"""
    print("=" * 70)
    print("🎨 AJOUT D'ÉMOJIS AUX MOTS ET EXPRESSIONS")
    print("=" * 70)
    print("Ajoute des émojis UNIQUEMENT aux mots avec une signification")
    print("claire et appropriée pour les enfants.")
    print("=" * 70)
    
    try:
        # Ajouter les émojis
        updated_count = add_emojis_to_database()
        
        # Vérifier les résultats
        success = verify_emoji_additions()
        
        if success and updated_count > 0:
            print("\n" + "=" * 70)
            print("✅ AJOUT D'ÉMOJIS TERMINÉ AVEC SUCCÈS!")
            print(f"🎨 {updated_count} mots ont reçu des émojis appropriés")
            print("👶 Seuls les émojis clairs et adaptés aux enfants ont été ajoutés")
            print("🚫 Les mots sans emoji évident ont été laissés vides")
            print("=" * 70)
        else:
            print("\n❌ ERREUR lors de l'ajout des émojis")
            return False
            
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        print("L'ajout d'émojis a échoué.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)