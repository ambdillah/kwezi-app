#!/usr/bin/env python3
"""
CORRECTION SPÉCIFIQUE: Expressions traditionnelles et religieuses
===============================================================
Corrige les traductions des expressions culturelles avec les slashes:
- "chant religieux homme": Shimaoré: "moulidi/dahira/dinahou", Kibouchi: "moulidi/dahira/dinahou"
- "chant religieux mixte": Shimaoré: "shengué/madjilis", Kibouchi: "maoulida/shengué/madjlis"
- "danse traditionnelle femme": Shimaoré: "mbiwi/wadhaha", Kibouchi: "mbiwi/wadhaha"
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

# Corrections à appliquer
EXPRESSIONS_CORRECTIONS = [
    {
        "french": "chant religieux homme",
        "shimaore": "moulidi/dahira/dinahou",
        "kibouchi": "moulidi/dahira/dinahou"
    },
    {
        "french": "chant religieux mixte", 
        "shimaore": "shengué/madjilis",
        "kibouchi": "maoulida/shengué/madjlis"
    },
    {
        "french": "danse traditionnelle femme",
        "shimaore": "mbiwi/wadhaha",
        "kibouchi": "mbiwi/wadhaha"
    }
]

@protect_database("fix_traditional_expressions")
def fix_traditional_expressions():
    """Corrige les expressions traditionnelles avec les slashes"""
    print("🔧 CORRECTION DES EXPRESSIONS TRADITIONNELLES ET RELIGIEUSES")
    print("=" * 80)
    
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
    
    for correction in EXPRESSIONS_CORRECTIONS:
        french = correction["french"]
        shimaore = correction["shimaore"]
        kibouchi = correction["kibouchi"]
        
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
            
            # Vérifier si une correction est nécessaire
            needs_update = False
            update_fields = {}
            
            if existing_expression.get("shimaore", "").strip() != shimaore:
                update_fields["shimaore"] = shimaore
                needs_update = True
                print(f"  📝 Shimaoré: '{existing_expression.get('shimaore', 'N/A')}' → '{shimaore}'")
            
            if existing_expression.get("kibouchi", "").strip() != kibouchi:
                update_fields["kibouchi"] = kibouchi
                needs_update = True
                print(f"  📝 Kibouchi: '{existing_expression.get('kibouchi', 'N/A')}' → '{kibouchi}'")
            
            if needs_update:
                # Appliquer la correction
                result = words_collection.update_one(
                    {"_id": existing_expression["_id"]},
                    {"$set": update_fields}
                )
                
                if result.modified_count > 0:
                    print(f"  ✅ Correction appliquée pour '{french}'")
                    corrections_applied += 1
                    
                    # Vérifier la correction
                    updated_expression = words_collection.find_one({"_id": existing_expression["_id"]})
                    print(f"  📝 Traduction corrigée:")
                    print(f"     Shimaoré: {updated_expression.get('shimaore', 'N/A')}")
                    print(f"     Kibouchi: {updated_expression.get('kibouchi', 'N/A')}")
                else:
                    print(f"  ❌ Échec de la correction pour '{french}'")
                    corrections_failed += 1
            else:
                print(f"  ✓ '{french}' est déjà correct")
        else:
            print(f"  ❌ Expression '{french}' non trouvée dans la base de données")
            corrections_failed += 1
    
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DES CORRECTIONS:")
    print(f"✅ Corrections appliquées: {corrections_applied}")
    print(f"❌ Échecs: {corrections_failed}")
    print(f"📝 Total traité: {len(EXPRESSIONS_CORRECTIONS)}")
    
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
    print("🚀 Démarrage de la correction des expressions traditionnelles...")
    
    # Vérifier l'état initial
    print("\n🔍 Vérification de l'état de la base de données...")
    is_healthy, message = db_protector.is_database_healthy()
    if not is_healthy:
        print(f"⚠️ Problème détecté: {message}")
        print("🔄 Restauration recommandée avant correction")
        exit(1)
    
    # Appliquer les corrections
    success = fix_traditional_expressions()
    
    if success:
        print("\n🎉 CORRECTIONS APPLIQUÉES AVEC SUCCÈS!")
        print("✅ Les expressions traditionnelles ont été corrigées avec les slashes")
        print("\n📋 Expressions corrigées:")
        for expr in EXPRESSIONS_CORRECTIONS:
            print(f"• {expr['french']}")
            print(f"  - Shimaoré: {expr['shimaore']}")
            print(f"  - Kibouchi: {expr['kibouchi']}")
        
        # Vérification finale de l'intégrité
        print("\n🔍 Vérification finale de l'intégrité...")
        is_healthy_after, message_after = db_protector.is_database_healthy()
        if is_healthy_after:
            print("✅ Base de données saine après corrections")
        else:
            print(f"⚠️ Problème détecté après corrections: {message_after}")
    else:
        print("\n❌ CORRECTIONS ÉCHOUÉES OU NON NÉCESSAIRES")
    
    print("\nFin du script de correction des expressions traditionnelles.")