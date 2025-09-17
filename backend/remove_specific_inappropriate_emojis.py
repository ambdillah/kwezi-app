#!/usr/bin/env python3
"""
SUPPRESSION SPÉCIFIQUE DES EMOJIS TRÈS INAPPROPRIÉS
==================================================
Supprime les emojis identifiés comme très inappropriés :
- 🫦 (lèvres suggestives pour vagin)
- 🍑 (pêche suggestive pour fesses) 
- 🌶️ (piment suggestif pour pénis)
- 🥎 (balle inappropriée pour testicules)
- 👅 (langue peut être suggestive)
- 🤰 (femme enceinte trop spécifique pour ventre)
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'mayotte_app')

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

def remove_specific_inappropriate_emojis():
    """Supprimer les emojis très inappropriés spécifiés"""
    
    print("🗑️ SUPPRESSION DES EMOJIS TRÈS INAPPROPRIÉS...")
    
    client = get_mongo_client()
    if not client:
        return False
    
    db = client[DB_NAME]
    
    # Liste des emojis très inappropriés à supprimer
    very_inappropriate_emojis = [
        '🫦',  # lèvres suggestives pour vagin
        '🍑',  # pêche suggestive pour fesses
        '🌶️',  # piment suggestif (pénis, piment nourriture)
        '🥎',  # balle inappropriée pour testicules
        '👅',  # langue peut être suggestive
        '🤰'   # femme enceinte trop spécifique pour ventre
    ]
    
    cleaned_count = 0
    
    for emoji in very_inappropriate_emojis:
        print(f"\n🔍 Recherche de l'emoji: {emoji}")
        
        # Trouver tous les mots avec cet emoji
        words_with_emoji = list(db.words.find({"image_url": emoji}))
        
        for word in words_with_emoji:
            french = word.get("french", "")
            category = word.get("category", "")
            word_id = word.get("_id")
            
            print(f"  🗑️ Suppression: {french} ({category}): {emoji}")
            
            # Supprimer l'emoji en le remplaçant par une chaîne vide
            try:
                result = db.words.update_one(
                    {"_id": word_id},
                    {"$set": {"image_url": ""}}
                )
                
                if result.modified_count > 0:
                    print(f"    ✅ Supprimé avec succès")
                    cleaned_count += 1
                else:
                    print(f"    ❌ Échec de la suppression")
                    
            except Exception as e:
                print(f"    ❌ Erreur: {e}")
    
    client.close()
    
    print(f"\n📊 RÉSULTAT: {cleaned_count} emojis très inappropriés supprimés")
    return cleaned_count > 0

def verify_removal():
    """Vérifier que les emojis inappropriés ont été supprimés"""
    
    print("\n🔍 VÉRIFICATION DE LA SUPPRESSION...")
    
    client = get_mongo_client()
    if not client:
        return False
    
    db = client[DB_NAME]
    
    # Vérifier que les emojis inappropriés ont disparu
    very_inappropriate_emojis = ['🫦', '🍑', '🌶️', '🥎', '👅', '🤰']
    
    remaining_inappropriate = []
    
    for emoji in very_inappropriate_emojis:
        count = db.words.count_documents({"image_url": emoji})
        if count > 0:
            remaining_inappropriate.append((emoji, count))
    
    if remaining_inappropriate:
        print("❌ EMOJIS INAPPROPRIÉS ENCORE PRÉSENTS:")
        for emoji, count in remaining_inappropriate:
            print(f"  {emoji}: {count} mots")
        client.close()
        return False
    else:
        print("✅ Aucun emoji inapproprié trouvé - Nettoyage réussi!")
    
    # Statistiques finales
    total_words = db.words.count_documents({})
    words_with_emojis = db.words.count_documents({"image_url": {"$ne": "", "$exists": True}})
    words_without_emojis = total_words - words_with_emojis
    
    print(f"\n📊 STATISTIQUES FINALES:")
    print(f"  ✅ Mots avec emojis appropriés: {words_with_emojis}")
    print(f"  🚫 Mots sans emoji: {words_without_emojis}")
    print(f"  📈 Total des mots: {total_words}")
    
    client.close()
    return True

def main():
    """Fonction principale"""
    print("=" * 80)
    print("🗑️ SUPPRESSION DES EMOJIS TRÈS INAPPROPRIÉS")
    print("=" * 80)
    print("Cible: 🫦 🍑 🌶️ 🥎 👅 🤰 (pas de représentation exacte)")
    print("=" * 80)
    
    # Supprimer les emojis inappropriés
    success = remove_specific_inappropriate_emojis()
    
    if success:
        # Vérifier que la suppression a fonctionné
        if verify_removal():
            print("\n" + "=" * 80)
            print("🎉 SUPPRESSION RÉUSSIE !")
            print("✅ Tous les emojis très inappropriés ont été supprimés")
            print("✅ Principe \"signification exacte\" parfaitement respecté")
            print("🚫 Pas d'emoji si pas de représentation exacte")
            print("=" * 80)
            return True
    
    print("\n❌ ÉCHEC DE LA SUPPRESSION")
    return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)