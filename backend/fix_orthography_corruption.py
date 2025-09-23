#!/usr/bin/env python3
"""
Script pour corriger les corruptions orthographiques détectées
comme "bwéni" → "bvéni" pour "madame"
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# Ajouter le chemin du backend au PYTHONPATH
sys.path.append('/app/backend')

# Charger les variables d'environnement
load_dotenv()

from database_protection import DatabaseProtector

def fix_orthography_corruption():
    """Corrige les corruptions orthographiques détectées."""
    
    # Corrections orthographiques identifiées
    orthography_fixes = [
        {
            "french": "madame",
            "correct_shimaore": "bwéni",  # Était corrompu en "bvéni"
            "correct_kibouchi": "viavi",  # Garder si correct
            "issue": "shimaoré corrompu: bvéni → bwéni"
        },
        # Ajouter d'autres corrections si nécessaire
    ]
    
    try:
        # Connexion à MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.words
        
        # Initialiser la protection de base de données
        db_protection = DatabaseProtector()
        
        print(f"🔗 Connexion à MongoDB: {mongo_url}")
        print(f"📊 Base de données: {db_name}")
        print(f"🔧 Corrections orthographiques à appliquer: {len(orthography_fixes)}")
        print()
        
        # Créer une sauvegarde avant correction
        print("💾 Création d'une sauvegarde avant correction...")
        try:
            backup_path = db_protection.create_backup("before_fix_orthography_corruption")
            if backup_path:
                print("✅ Sauvegarde créée avec succès")
            else:
                print("⚠️ Échec de la sauvegarde")
        except Exception as e:
            print(f"⚠️ Problème sauvegarde (continuons quand même): {str(e)}")
        print()
        
        # Appliquer chaque correction
        corrections_applied = 0
        
        for fix in orthography_fixes:
            french_word = fix["french"]
            correct_shimaore = fix["correct_shimaore"]
            correct_kibouchi = fix["correct_kibouchi"]
            issue = fix["issue"]
            
            print(f"🔧 Correction de '{french_word}'...")
            print(f"   Issue: {issue}")
            
            # Rechercher le mot dans la base
            existing_word = collection.find_one({
                "french": {"$regex": f"^{french_word}$", "$options": "i"}
            })
            
            if existing_word:
                current_shimaore = existing_word.get("shimaore", "N/A")
                current_kibouchi = existing_word.get("kibouchi", "N/A")
                
                print(f"   ✅ Mot trouvé: {french_word}")
                print(f"      Shimaoré actuel: '{current_shimaore}' → '{correct_shimaore}'")
                print(f"      Kibouchi actuel: '{current_kibouchi}' → '{correct_kibouchi}'")
                
                # Préparer les corrections
                update_data = {
                    "shimaore": correct_shimaore,
                    "kibouchi": correct_kibouchi,
                    "orthography_corrected_at": datetime.now(),
                    "orthography_corrected_by": "fix_orthography_corruption_script",
                    "orthography_issue_fixed": issue
                }
                
                # Appliquer la correction
                result = collection.update_one(
                    {"_id": existing_word["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    corrections_applied += 1
                    print(f"   ✅ Correction appliquée avec succès")
                else:
                    print(f"   ⚠️ Aucune modification effectuée")
                    
            else:
                print(f"   ❌ Mot '{french_word}' non trouvé")
            
            print()
        
        # Statistiques finales
        print("=" * 60)
        print(f"📈 RÉSUMÉ DES CORRECTIONS ORTHOGRAPHIQUES")
        print(f"🔧 Corrections appliquées: {corrections_applied}")
        print(f"📝 Corrections tentées: {len(orthography_fixes)}")
        print()
        
        print("✅ Correction des corruptions orthographiques terminée!")
        
        # Fermer la connexion
        client.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 CORRECTION DES CORRUPTIONS ORTHOGRAPHIQUES")
    print("🎯 Objectif: Restaurer les orthographes correctes (ex: bvéni → bwéni)")
    print("=" * 60)
    print()
    
    success = fix_orthography_corruption()
    
    if success:
        print("🎉 Corrections terminées avec succès!")
        print("📱 Les orthographes devraient maintenant être correctes")
    else:
        print("💥 Échec des corrections")
        sys.exit(1)