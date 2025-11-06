#!/usr/bin/env python3
"""
SUPPRESSION DES DOUBLONS SELON LES CHOIX UTILISATEUR
===================================================
Supprime les doublons non souhaités selon les décisions de l'utilisateur
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

# Doublons à supprimer selon les choix utilisateur
DOUBLONS_A_SUPPRIMER = [
    # Escargot - supprimer option 2
    {
        "french": "escargot",
        "shimaore": "kowa",
        "kibouchi": "ankora",
        "raison": "Escargot option 2 (utilisateur préfère option 1)"
    },
    # Pirogue - supprimer option 1 
    {
        "french": "pirogue",
        "shimaore": "laka",
        "kibouchi": "laka",
        "category": "nature",
        "raison": "Pirogue option 1 (utilisateur préfère option 2 en transport)"
    },
    # Entrer - supprimer option 2
    {
        "french": "entrer",
        "shimaore": "ounguiya", 
        "kibouchi": "mihidiri",
        "raison": "Entrer option 2 (utilisateur préfère option 1)"
    }
]

@protect_database("supprimer_doublons_choisis")
def supprimer_doublons_selon_choix():
    """Supprime les doublons non souhaités"""
    print("🔧 SUPPRESSION DES DOUBLONS SELON LES CHOIX UTILISATEUR")
    print("=" * 70)
    
    try:
        client = MongoClient(MONGO_URL)
        client.admin.command('ping')
        print(f"✅ Connexion MongoDB établie : {MONGO_URL}")
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB : {e}")
        return False
    
    db = client[DB_NAME]
    words_collection = db.words
    
    doublons_supprimes = 0
    
    for doublon in DOUBLONS_A_SUPPRIMER:
        print(f"\n🔍 Recherche du doublon à supprimer: '{doublon['french']}'")
        print(f"   Shimaoré: '{doublon['shimaore']}', Kibouchi: '{doublon['kibouchi']}'")
        
        # Construire le filtre de recherche
        filtre = {
            "french": {"$regex": f"^{doublon['french']}$", "$options": "i"},
            "shimaore": doublon['shimaore'],
            "kibouchi": doublon['kibouchi']
        }
        
        # Ajouter la catégorie si spécifiée
        if "category" in doublon:
            filtre["category"] = doublon["category"]
        
        # Chercher le doublon à supprimer
        mot_a_supprimer = words_collection.find_one(filtre)
        
        if mot_a_supprimer:
            # Supprimer le doublon
            result = words_collection.delete_one({"_id": mot_a_supprimer["_id"]})
            
            if result.deleted_count > 0:
                print(f"  ✅ Doublon supprimé: {doublon['raison']}")
                doublons_supprimes += 1
            else:
                print(f"  ❌ Échec de la suppression pour '{doublon['french']}'")
        else:
            print(f"  ⚠️ Doublon non trouvé pour '{doublon['french']}'")
    
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DE LA SUPPRESSION DES DOUBLONS:")
    print(f"🗑️ Doublons supprimés selon vos choix: {doublons_supprimes}")
    
    # Vérifier qu'il ne reste plus de doublons
    print("\n🔍 Vérification finale des doublons restants...")
    mots_a_verifier = ["escargot", "pirogue", "entrer"]
    
    for mot_francais in mots_a_verifier:
        count = words_collection.count_documents({
            "french": {"$regex": f"^{mot_francais}$", "$options": "i"}
        })
        if count == 1:
            print(f"  ✅ '{mot_francais}': 1 seul mot (plus de doublon)")
        else:
            print(f"  ⚠️ '{mot_francais}': {count} mots trouvés")
    
    # Vérification finale de l'intégrité
    print("\n🔍 Vérification de l'intégrité post-suppression...")
    is_healthy, message = db_protector.is_database_healthy()
    if is_healthy:
        print("✅ Base de données saine après suppression des doublons")
    else:
        print(f"⚠️ Problème détecté: {message}")
    
    client.close()
    return doublons_supprimes > 0

if __name__ == "__main__":
    print("🚀 Démarrage de la suppression des doublons selon vos choix...")
    
    # Vérifier l'état initial
    print("\n🔍 Vérification de l'état initial de la base de données...")
    is_healthy, message = db_protector.is_database_healthy()
    if not is_healthy:
        print(f"⚠️ Problème détecté avant suppression: {message}")
        print("🔄 Restauration recommandée avant suppression")
        exit(1)
    
    # Effectuer la suppression
    success = supprimer_doublons_selon_choix()
    
    if success:
        print("\n🎉 SUPPRESSION DES DOUBLONS TERMINÉE AVEC SUCCÈS!")
        print("✅ Escargot: gardé Shimaoré='kwa', Kibouchi='ancora'")
        print("✅ Pirogue: gardé Shimaoré='laka', Kibouchi='lakana' (transport)")
        print("✅ Entrer: gardé Shimaoré='ounguiya', Kibouchi='mihiditri'")
        
        # Vérification finale de l'intégrité
        print("\n🔍 Vérification finale de l'intégrité...")
        is_healthy_after, message_after = db_protector.is_database_healthy()
        if is_healthy_after:
            print("✅ Base de données saine après suppression")
        else:
            print(f"⚠️ Problème détecté après suppression: {message_after}")
    else:
        print("\n⚠️ Aucun doublon n'a été supprimé")
    
    print("\nFin du script de suppression des doublons choisis.")