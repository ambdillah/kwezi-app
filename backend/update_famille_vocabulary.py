#!/usr/bin/env python3
"""
Mise à jour du vocabulaire de la section "famille"
- Ajouter de nouveaux mots de famille
- Corriger "tante" en "tante maternelle"
"""

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
import os
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL')
client = MongoClient(MONGO_URL)
db = client.kwezi
words_collection = db.words

def update_tante_to_tante_maternelle():
    """Corriger 'tante' en 'tante maternelle'"""
    print("🔧 CORRECTION: tante → tante maternelle")
    print("=" * 40)
    
    # Chercher le mot "tante"
    tante_word = words_collection.find_one({"french": "tante"})
    
    if tante_word:
        # Mettre à jour avec "tante maternelle"
        result = words_collection.update_one(
            {"_id": tante_word["_id"]},
            {"$set": {"french": "tante maternelle"}}
        )
        
        if result.modified_count > 0:
            print(f"  ✅ Corrigé: 'tante' → 'tante maternelle'")
            print(f"     Shimaoré: {tante_word.get('shimaore', 'N/A')}")
            print(f"     Kibouchi: {tante_word.get('kibouchi', 'N/A')}")
        else:
            print(f"  ⚠️ Aucune modification nécessaire")
    else:
        print(f"  ❌ Mot 'tante' non trouvé dans la base")
    
    return True

def add_new_famille_words():
    """Ajouter les nouveaux mots de famille"""
    print("\n➕ AJOUT DE NOUVEAUX MOTS DE FAMILLE")
    print("=" * 40)
    
    # Nouveaux mots à ajouter
    nouveaux_mots = [
        {
            "french": "tante paternelle",
            "shimaore": "nguivavi",
            "kibouchi": "angouvavi",
            "category": "famille",
            "emoji": "👩‍👧‍👦",
            "has_image": False
        },
        {
            "french": "petit garcon", 
            "shimaore": "mwana mtroubaba",
            "kibouchi": "zaza lalahi",
            "category": "famille", 
            "emoji": "👦",
            "has_image": False
        },
        {
            "french": "jeune adulte",
            "shimaore": "chababi",
            "kibouchi": "chababai",
            "category": "famille",
            "emoji": "🧑",
            "has_image": False
        },
        {
            "french": "frere/soeur",
            "shimaore": "moinagna",
            "kibouchi": "",  # Pas de kibouchi mentionné
            "category": "famille",
            "emoji": "👫",
            "has_image": False
        }
    ]
    
    added_count = 0
    updated_count = 0
    
    for mot in nouveaux_mots:
        # Vérifier si le mot existe déjà
        existing = words_collection.find_one({"french": mot["french"]})
        
        if existing:
            # Mettre à jour le mot existant
            words_collection.update_one(
                {"_id": existing["_id"]},
                {"$set": {
                    "shimaore": mot["shimaore"],
                    "kibouchi": mot["kibouchi"],
                    "category": mot["category"],
                    "emoji": mot.get("emoji", existing.get("emoji", "")),
                    "has_image": mot.get("has_image", existing.get("has_image", False))
                }}
            )
            print(f"  🔄 Mis à jour: {mot['french']}")
            print(f"     Shimaoré: {mot['shimaore']}")
            print(f"     Kibouchi: {mot['kibouchi']}")
            updated_count += 1
        else:
            # Ajouter le nouveau mot
            words_collection.insert_one(mot)
            print(f"  ➕ Ajouté: {mot['french']}")
            print(f"     Shimaoré: {mot['shimaore']}")
            print(f"     Kibouchi: {mot['kibouchi']}")
            added_count += 1
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"  - Mots ajoutés: {added_count}")
    print(f"  - Mots mis à jour: {updated_count}")
    
    return added_count + updated_count

def verify_famille_updates():
    """Vérifier que les mises à jour ont été appliquées"""
    print("\n🔍 VÉRIFICATION DES MISES À JOUR")
    print("=" * 40)
    
    # Vérifier "tante maternelle"
    tante_maternelle = words_collection.find_one({"french": "tante maternelle"})
    if tante_maternelle:
        print(f"  ✅ 'tante maternelle' confirmée:")
        print(f"     Shimaoré: {tante_maternelle.get('shimaore', 'N/A')}")
        print(f"     Kibouchi: {tante_maternelle.get('kibouchi', 'N/A')}")
    else:
        print(f"  ❌ 'tante maternelle' non trouvée")
    
    # Vérifier les nouveaux mots
    nouveaux_mots_french = [
        "tante paternelle",
        "petit garcon", 
        "jeune adulte",
        "frere/soeur"
    ]
    
    print(f"\n  📝 Nouveaux mots de famille:")
    for mot_french in nouveaux_mots_french:
        mot = words_collection.find_one({"french": mot_french})
        if mot:
            print(f"    ✅ {mot_french}:")
            print(f"       Shimaoré: {mot.get('shimaore', 'N/A')}")
            print(f"       Kibouchi: {mot.get('kibouchi', 'N/A')}")
        else:
            print(f"    ❌ {mot_french}: non trouvé")
    
    # Statistiques famille
    total_famille = words_collection.count_documents({"category": "famille"})
    print(f"\n📊 Total mots famille: {total_famille}")

def generate_famille_summary():
    """Génère un résumé de tous les mots de famille"""
    print("\n📋 RÉSUMÉ COMPLET - SECTION FAMILLE")
    print("=" * 50)
    
    # Récupérer tous les mots de famille
    famille_words = list(words_collection.find({"category": "famille"}).sort("french", 1))
    
    print(f"Total: {len(famille_words)} mots dans la catégorie 'famille'\n")
    
    for i, mot in enumerate(famille_words, 1):
        french = mot.get('french', 'N/A')
        shimaore = mot.get('shimaore', 'N/A')
        kibouchi = mot.get('kibouchi', 'N/A') if mot.get('kibouchi') else 'Non défini'
        emoji = mot.get('emoji', '')
        
        print(f"{i:2d}. {emoji} {french}")
        print(f"     Shimaoré: {shimaore}")
        print(f"     Kibouchi: {kibouchi}")
        print()

def main():
    """Fonction principale de mise à jour"""
    print("🔧 MISE À JOUR DU VOCABULAIRE FAMILLE")
    print("=" * 60)
    print(f"Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. Corriger "tante" en "tante maternelle"
        update_tante_to_tante_maternelle()
        
        # 2. Ajouter les nouveaux mots de famille
        modifications = add_new_famille_words()
        
        # 3. Vérifier les mises à jour
        verify_famille_updates()
        
        # 4. Générer le résumé complet
        generate_famille_summary()
        
        print(f"✅ MISE À JOUR FAMILLE TERMINÉE!")
        print(f"  - Modifications appliquées: {modifications}")
        
    except Exception as e:
        print(f"❌ ERREUR: {str(e)}")
        raise

if __name__ == "__main__":
    main()