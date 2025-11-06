#!/usr/bin/env python3
"""
CORRECTION SPÉCIFIQUE: Expressions pratiques importantes
======================================================
Corrige les traductions des expressions pratiques:
- "j'ai besoin d'un médecin": Shimaoré: "ntsaha douktera"
- "je peux avoir des toilettes": Shimaoré: "nissi miya mraba"
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

# Corrections à appliquer (seulement Shimaoré modifié selon la demande)
PRACTICAL_CORRECTIONS = [
    {
        "french": "j'ai besoin d'un médecin",
        "shimaore": "ntsaha douktera",
        # Pas de changement pour Kibouchi - garder l'existant
    },
    {
        "french": "je peux avoir des toilettes", 
        "shimaore": "nissi miya mraba",
        # Pas de changement pour Kibouchi - garder l'existant
    }
]

@protect_database("fix_practical_expressions")
def fix_practical_expressions():
    """Corrige les expressions pratiques en Shimaoré"""
    print("🔧 CORRECTION DES EXPRESSIONS PRATIQUES")
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
    
    for correction in PRACTICAL_CORRECTIONS:
        french = correction["french"]
        shimaore = correction["shimaore"]
        
        print(f"\n🔍 Recherche de l'expression '{french}'...")
        
        # Chercher l'expression existante (insensible à la casse)
        existing_expression = words_collection.find_one({
            "french": {"$regex": f"^{french}$", "$options": "i"}
        })
        
        if existing_expression:
            # Afficher la traduction actuelle
            print(f"📝 Traduction actuelle:")
            print(f"   Français: {existing_expression.get('french', 'N/A')}")
            print(f"   Shimaoré: {existing_expression.get('shimaore', 'N/A')}")
            print(f"   Kibouchi: {existing_expression.get('kibouchi', 'N/A')}")
            
            # Vérifier si une correction est nécessaire pour le Shimaoré
            current_shimaore = existing_expression.get("shimaore", "").strip()
            if current_shimaore != shimaore:
                print(f"  📝 Shimaoré: '{current_shimaore}' → '{shimaore}'")
                
                # Appliquer la correction (seulement Shimaoré)
                result = words_collection.update_one(
                    {"_id": existing_expression["_id"]},
                    {"$set": {"shimaore": shimaore}}
                )
                
                if result.modified_count > 0:
                    print(f"  ✅ Correction appliquée pour '{french}'")
                    corrections_applied += 1
                    
                    # Vérifier la correction
                    updated_expression = words_collection.find_one({"_id": existing_expression["_id"]})
                    print(f"  📝 Traduction corrigée:")
                    print(f"     Shimaoré: {updated_expression.get('shimaore', 'N/A')}")
                    print(f"     Kibouchi: {updated_expression.get('kibouchi', 'N/A')} (inchangé)")
                else:
                    print(f"  ❌ Échec de la correction pour '{french}'")
                    corrections_failed += 1
            else:
                print(f"  ✓ '{french}' est déjà correct en Shimaoré")
        else:
            print(f"  ❌ Expression '{french}' non trouvée dans la base de données")
            corrections_failed += 1
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES CORRECTIONS:")
    print(f"✅ Corrections appliquées: {corrections_applied}")
    print(f"❌ Échecs: {corrections_failed}")
    print(f"📝 Total traité: {len(PRACTICAL_CORRECTIONS)}")
    
    # Vérification finale de l'intégrité
    print("\n🔍 Vérification de l'intégrité post-corrections...")
    is_healthy, message = db_protector.is_database_healthy()
    if is_healthy:
        print("✅ Base de données saine après corrections")
    else:
        print(f"⚠️ Problème détecté: {message}")
    
    client.close()
    return corrections_applied > 0

if __name__ == "__main__":
    print("🚀 Démarrage de la correction des expressions pratiques...")
    
    # Vérifier l'état initial
    print("\n🔍 Vérification de l'état de la base de données...")
    is_healthy, message = db_protector.is_database_healthy()
    if not is_healthy:
        print(f"⚠️ Problème détecté: {message}")
        print("🔄 Restauration recommandée avant correction")
        exit(1)
    
    # Appliquer les corrections
    success = fix_practical_expressions()
    
    if success:
        print("\n🎉 CORRECTIONS APPLIQUÉES AVEC SUCCÈS!")
        print("✅ Les expressions pratiques ont été corrigées en Shimaoré")
        print("\n📋 Expressions corrigées:")
        for expr in PRACTICAL_CORRECTIONS:
            print(f"• {expr['french']}")
            print(f"  - Shimaoré: {expr['shimaore']}")
            print(f"  - Kibouchi: (inchangé)")
        
        # Vérification finale de l'intégrité
        print("\n🔍 Vérification finale de l'intégrité...")
        is_healthy_after, message_after = db_protector.is_database_healthy()
        if is_healthy_after:
            print("✅ Base de données saine après corrections")
        else:
            print(f"⚠️ Problème détecté après corrections: {message_after}")
    else:
        print("\n❌ CORRECTIONS ÉCHOUÉES OU NON NÉCESSAIRES")
    
    print("\nFin du script de correction des expressions pratiques.")