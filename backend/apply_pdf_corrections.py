#!/usr/bin/env python3
"""
Script pour appliquer les corrections identifiées du PDF de vocabulaire shimaoré-kibouchi
Applique les corrections de manière sécurisée avec sauvegarde
"""

import os
import sys
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId

load_dotenv()

def connect_to_database():
    """Se connecte à la base de données MongoDB"""
    MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/mayotte_app')
    DB_NAME = os.getenv('DB_NAME', 'mayotte_app')
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
    return db.words

def backup_database():
    """Crée une sauvegarde de la base avant modifications"""
    collection = connect_to_database()
    words = list(collection.find({}))
    
    backup_filename = f"/app/backend/backup_words_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Convertir ObjectId en string pour JSON
    for word in words:
        if '_id' in word:
            word['_id'] = str(word['_id'])
    
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    
    print(f"Sauvegarde créée: {backup_filename}")
    return backup_filename

def apply_critical_corrections():
    """Applique les corrections critiques identifiées"""
    collection = connect_to_database()
    
    corrections_applied = 0
    
    print("=== APPLICATION DES CORRECTIONS CRITIQUES ===")
    
    # 1. Corrections orthographiques françaises (suppression d'accents)
    french_corrections = [
        {"from": "étoile", "to": "etoile"},
        {"from": "école", "to": "ecole"},
        {"from": "barrière de corail", "to": "barriere de corail"},
        {"from": "tempête", "to": "tempete"},
        {"from": "rivière", "to": "riviere"},
        {"from": "érosion", "to": "erosion"},
        {"from": "marée basse", "to": "maree basse"},
        {"from": "marée haute", "to": "maree haute"},
        {"from": "inondé", "to": "inonde"},
        {"from": "canne à sucre", "to": "canne a sucre"},
        {"from": "arbre à pain", "to": "arbre a pain"},
        {"from": "école coranique", "to": "ecole coranique"},
        {"from": "tête", "to": "tete"},
        {"from": "comment ça va", "to": "comment ca va"},
        {"from": "ça va bien", "to": "ca va bien"},
        {"from": "frère", "to": "frere"},
        {"from": "grand-père", "to": "grand-pere"},
        {"from": "grand-mère", "to": "grand-mere"},
        {"from": "huître", "to": "huitre"}
    ]
    
    for correction in french_corrections:
        result = collection.update_one(
            {"french": correction["from"]},
            {"$set": {
                "french": correction["to"],
                "updated_at": datetime.utcnow(),
                "corrected_from_pdf": True
            }}
        )
        if result.modified_count > 0:
            print(f"✓ Français: '{correction['from']}' → '{correction['to']}'")
            corrections_applied += 1
    
    # 2. Corrections spécifiques de traductions
    translation_corrections = [
        # Escargot: correction kwa → kowa
        {
            "french": "escargot",
            "updates": {"shimaore": "kowa"}
        },
        # Oursin: différenciation avec huître
        {
            "french": "oursin", 
            "updates": {"shimaore": "gadzassi ya bahari"}
        },
        # Nous: correction wassi → wasi
        {
            "french": "nous",
            "updates": {"shimaore": "wasi"}
        },
        # Corrections kibouchi pour les nombres
        {
            "french": "neuf",
            "updates": {"kibouchi": "foulu"}
        },
        {
            "french": "dix", 
            "updates": {"kibouchi": "foulu"}
        }
    ]
    
    for correction in translation_corrections:
        updates = correction["updates"].copy()
        updates["updated_at"] = datetime.utcnow()
        updates["corrected_from_pdf"] = True
        
        result = collection.update_one(
            {"french": correction["french"]},
            {"$set": updates}
        )
        if result.modified_count > 0:
            changes = ", ".join([f"{k}: '{v}'" for k, v in correction["updates"].items()])
            print(f"✓ Traduction '{correction['french']}': {changes}")
            corrections_applied += 1
    
    # 3. Ajout des mots manquants critiques
    new_words = [
        {
            "french": "pente",
            "shimaore": "mlima", 
            "kibouchi": "boungou",
            "category": "nature",
            "difficulty": 1
        },
        {
            "french": "tante maternelle",
            "shimaore": "mama titi",
            "kibouchi": "zama", 
            "category": "famille",
            "difficulty": 2
        },
        {
            "french": "tante paternelle", 
            "shimaore": "zena",
            "kibouchi": "zena",
            "category": "famille", 
            "difficulty": 2
        },
        {
            "french": "petit garcon",
            "shimaore": "mwana mtroubaba",
            "kibouchi": "zaza lalahi",
            "category": "famille",
            "difficulty": 1
        },
        {
            "french": "jeune adulte",
            "shimaore": "shababi",
            "kibouchi": "shababi", 
            "category": "famille",
            "difficulty": 2
        }
    ]
    
    for word in new_words:
        # Vérifier si le mot existe déjà
        existing = collection.find_one({"french": word["french"]})
        if not existing:
            word_data = word.copy()
            word_data.update({
                "created_at": datetime.utcnow(),
                "added_from_pdf": True,
                "image_url": None,
                "audio_url": None
            })
            
            collection.insert_one(word_data)
            print(f"✓ Ajouté: '{word['french']}' ({word['category']})")
            corrections_applied += 1
        else:
            print(f"- Existe déjà: '{word['french']}'")
    
    return corrections_applied

def verify_corrections():
    """Vérifie que les corrections ont été appliquées"""
    collection = connect_to_database()
    
    print("\n=== VÉRIFICATION DES CORRECTIONS ===")
    
    # Vérifier quelques corrections clés
    test_cases = [
        {"french": "etoile", "expected": True},
        {"french": "ecole", "expected": True}, 
        {"french": "escargot", "check_shimaore": "kowa"},
        {"french": "nous", "check_shimaore": "wasi"},
        {"french": "tante maternelle", "expected": True}
    ]
    
    all_good = True
    for test in test_cases:
        word = collection.find_one({"french": test["french"]})
        if test.get("expected") and word:
            print(f"✓ Trouvé: '{test['french']}'")
        elif test.get("check_shimaore"):
            if word and word.get("shimaore") == test["check_shimaore"]:
                print(f"✓ Correction vérifiée: '{test['french']}' → shimaore: '{test['check_shimaore']}'")
            else:
                print(f"✗ Erreur: '{test['french']}' - shimaoré attendu: '{test['check_shimaore']}'")
                all_good = False
        elif test.get("expected") and not word:
            print(f"✗ Manquant: '{test['french']}'")
            all_good = False
    
    # Compter le total après corrections
    total_words = collection.count_documents({})
    total_corrected = collection.count_documents({"corrected_from_pdf": True})
    total_added = collection.count_documents({"added_from_pdf": True})
    
    print(f"\nSTATISTIQUES FINALES:")
    print(f"Total mots: {total_words}")
    print(f"Mots corrigés: {total_corrected}")
    print(f"Mots ajoutés: {total_added}")
    
    return all_good

def main():
    """Fonction principale"""
    print("=== APPLICATION DES CORRECTIONS PDF VOCABULAIRE ===")
    
    # Créer une sauvegarde
    backup_file = backup_database()
    
    try:
        # Appliquer les corrections
        corrections_count = apply_critical_corrections()
        
        print(f"\n✅ {corrections_count} corrections appliquées avec succès")
        
        # Vérifier les corrections
        if verify_corrections():
            print(f"\n🎉 TOUTES LES CORRECTIONS SONT VÉRIFIÉES !")
            print(f"Sauvegarde disponible: {backup_file}")
        else:
            print(f"\n⚠️  Certaines corrections nécessitent une vérification manuelle")
            
    except Exception as e:
        print(f"\n❌ ERREUR lors de l'application des corrections: {e}")
        print(f"Restaurez la sauvegarde si nécessaire: {backup_file}")
        raise

if __name__ == "__main__":
    main()