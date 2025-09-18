#!/usr/bin/env python3
"""
CORRECTION DES EMOJIS DES NOMBRES 11-20
=======================================
Remplace les emojis composés qui s'affichent verticalement par des solutions plus adaptées
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from database_protection import protect_database, db_protector

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'mayotte_app')

# Corrections d'emojis pour les nombres 11-20
CORRECTIONS_NOMBRES_EMOJIS = {
    "onze": "11",        # Texte simple au lieu de 1️⃣1️⃣
    "douze": "12",       # Texte simple au lieu de 1️⃣2️⃣
    "treize": "13",      # Texte simple au lieu de 1️⃣3️⃣
    "quatorze": "14",    # Texte simple au lieu de 1️⃣4️⃣
    "quinze": "15",      # Texte simple au lieu de 1️⃣5️⃣
    "seize": "16",       # Texte simple au lieu de 1️⃣6️⃣
    "dix-sept": "17",    # Texte simple au lieu de 1️⃣7️⃣
    "dix-huit": "18",    # Texte simple au lieu de 1️⃣8️⃣
    "dix-neuf": "19",    # Texte simple au lieu de 1️⃣9️⃣
    "vingt": "20"        # Texte simple au lieu de 2️⃣0️⃣
}

@protect_database("fix_nombres_emojis")
def corriger_emojis_nombres():
    """Corrige les emojis des nombres 11-20 pour un meilleur affichage"""
    print("🔧 CORRECTION DES EMOJIS DES NOMBRES 11-20")
    print("=" * 60)
    
    try:
        client = MongoClient(MONGO_URL)
        client.admin.command('ping')
        print(f"✅ Connexion MongoDB établie : {MONGO_URL}")
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB : {e}")
        return False
    
    db = client[DB_NAME]
    words_collection = db.words
    
    corrections_applied = 0
    corrections_failed = 0
    
    for french, nouvel_emoji in CORRECTIONS_NOMBRES_EMOJIS.items():
        print(f"\n🔍 Recherche de '{french}'...")
        
        # Chercher le nombre
        nombre = words_collection.find_one({
            "french": {"$regex": f"^{french}$", "$options": "i"},
            "category": "nombres"
        })
        
        if nombre:
            ancien_emoji = nombre.get('image_url', '')
            print(f"  📝 Emoji actuel: '{ancien_emoji}'")
            print(f"  🔄 Nouveau: '{nouvel_emoji}'")
            
            # Appliquer la correction
            result = words_collection.update_one(
                {"_id": nombre["_id"]},
                {"$set": {"image_url": nouvel_emoji}}
            )
            
            if result.modified_count > 0:
                print(f"  ✅ Correction appliquée pour '{french}'")
                corrections_applied += 1
            else:
                print(f"  ❌ Échec de la correction pour '{french}'")
                corrections_failed += 1
        else:
            print(f"  ❌ Nombre '{french}' non trouvé")
            corrections_failed += 1
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES CORRECTIONS D'EMOJIS NOMBRES:")
    print(f"✅ Corrections appliquées: {corrections_applied}")
    print(f"❌ Échecs: {corrections_failed}")
    print(f"📝 Total traité: {len(CORRECTIONS_NOMBRES_EMOJIS)}")
    
    # Vérification finale de l'intégrité
    print("\n🔍 Vérification de l'intégrité post-corrections...")
    is_healthy, message = db_protector.is_database_healthy()
    if is_healthy:
        print("✅ Base de données saine après corrections")
    else:
        print(f"⚠️ Problème détecté: {message}")
    
    # Afficher le résultat final
    print("\n📊 RÉSULTAT FINAL DES NOMBRES:")
    nombres = list(words_collection.find({"category": "nombres"}).sort([("french", 1)]))
    for nombre in nombres:
        print(f"  {nombre.get('french', 'N/A')}: {nombre.get('image_url', 'N/A')}")
    
    client.close()
    return corrections_applied > 0

if __name__ == "__main__":
    print("🚀 Démarrage de la correction des emojis des nombres 11-20...")
    
    # Vérifier l'état initial
    print("\n🔍 Vérification de l'état initial de la base de données...")
    is_healthy, message = db_protector.is_database_healthy()
    if not is_healthy:
        print(f"⚠️ Problème détecté avant corrections: {message}")
        print("🔄 Restauration recommandée avant corrections")
        exit(1)
    
    # Appliquer les corrections
    success = corriger_emojis_nombres()
    
    if success:
        print("\n🎉 CORRECTIONS D'EMOJIS APPLIQUÉES AVEC SUCCÈS!")
        print("✅ Les nombres 11-20 utilisent maintenant du texte simple")
        print("✅ L'affichage devrait être aligné horizontalement")
        print("✅ Plus de problème d'affichage vertical des chiffres")
        
        # Vérification finale de l'intégrité
        print("\n🔍 Vérification finale de l'intégrité...")
        is_healthy_after, message_after = db_protector.is_database_healthy()
        if is_healthy_after:
            print("✅ Base de données saine après corrections")
        else:
            print(f"⚠️ Problème détecté après corrections: {message_after}")
    else:
        print("\n⚠️ Aucune correction n'a été appliquée")
    
    print("\nFin du script de correction des emojis nombres.")