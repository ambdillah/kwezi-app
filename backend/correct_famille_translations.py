#!/usr/bin/env python3
"""
Script de correction des traductions famille pour correspondre aux fichiers audio
Basé sur l'analyse de vérification approfondie
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# Charger les variables d'environnement
load_dotenv()

def correct_famille_translations():
    """Corriger les traductions famille pour correspondre aux fichiers audio disponibles."""
    
    try:
        # Connexion à MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.words
        
        print("🔧 CORRECTION DES TRADUCTIONS FAMILLE")
        print("=" * 60)
        print("Correction pour correspondre aux fichiers audio disponibles")
        print()
        
        # Corrections spécifiques basées sur l'analyse des fichiers disponibles
        corrections = [
            {
                "french": "petit frère",
                "current_kibouchi": "zandri",
                "correct_kibouchi": "anadahi",
                "explanation": "Correction: 'zandri' → 'anadahi' pour correspondre au fichier Anadahi.m4a"
            },
            {
                "french": "petite sœur",
                "current_kibouchi": "zandri", 
                "correct_kibouchi": "anabavi",
                "explanation": "Correction: 'zandri' → 'anabavi' pour correspondre au fichier Anabavi.m4a"
            }
        ]
        
        corrections_applied = 0
        
        for i, correction in enumerate(corrections, 1):
            print(f"--- Correction {i}/{len(corrections)} ---")
            print(f"🔸 Mot français: {correction['french']}")
            print(f"📝 {correction['explanation']}")
            
            # Trouver le mot dans la base de données
            word_doc = collection.find_one({
                "category": "famille",
                "french": correction["french"]
            })
            
            if not word_doc:
                print(f"❌ Mot '{correction['french']}' non trouvé dans la base")
                continue
            
            # Afficher l'état actuel
            current_kibouchi = word_doc.get('kibouchi', 'N/A')
            print(f"   Actuel Kibouchi: '{current_kibouchi}'")
            print(f"   Nouveau Kibouchi: '{correction['correct_kibouchi']}'")
            
            # Appliquer la correction
            update_fields = {
                "kibouchi": correction["correct_kibouchi"],
                "translation_corrected_at": datetime.now()
            }
            
            result = collection.update_one(
                {"_id": word_doc["_id"]},
                {"$set": update_fields}
            )
            
            if result.modified_count > 0:
                print(f"   ✅ Correction appliquée avec succès")
                corrections_applied += 1
            else:
                print(f"   ❌ Échec de la correction")
            
            print()
        
        print("=" * 60)
        print(f"📊 RÉSUMÉ DES CORRECTIONS")
        print(f"✅ Corrections appliquées: {corrections_applied}")
        print(f"📈 Total traité: {corrections_applied}/{len(corrections)}")
        
        # Vérification post-correction
        print("\n🔍 VÉRIFICATION POST-CORRECTION")
        print("-" * 40)
        
        for correction in corrections:
            word_doc = collection.find_one({
                "category": "famille",
                "french": correction["french"]
            })
            
            if word_doc:
                kibouchi = word_doc.get('kibouchi', 'N/A')
                kibouchi_file = word_doc.get('kibouchi_audio_filename', 'N/A')
                
                print(f"🔸 {correction['french']}:")
                print(f"   Kibouchi: '{kibouchi}'")
                print(f"   Fichier: {kibouchi_file}")
                
                # Vérifier la correspondance
                expected_file = correction['correct_kibouchi'].capitalize() + '.m4a'
                if kibouchi_file == expected_file:
                    print(f"   ✅ Correspondance correcte")
                else:
                    print(f"   ⚠️ Fichier attendu: {expected_file}")
                print()
        
        # Vérifier et corriger le problème du doublon "tente"/"tante"
        print("🔍 VÉRIFICATION DU DOUBLON TENTE/TANTE")
        print("-" * 40)
        
        tante_words = list(collection.find({
            "category": "famille",
            "french": {"$in": ["tante", "tente"]}
        }))
        
        if len(tante_words) > 1:
            print(f"⚠️ {len(tante_words)} mots trouvés pour tante/tente:")
            
            for word in tante_words:
                print(f"   - {word['french']}: '{word.get('shimaore')}' / '{word.get('kibouchi')}'")
            
            # Supprimer le doublon "tente" s'il existe
            tente_word = collection.find_one({
                "category": "famille", 
                "french": "tente"
            })
            
            if tente_word:
                print(f"   🗑️ Suppression du doublon 'tente'...")
                result = collection.delete_one({"_id": tente_word["_id"]})
                if result.deleted_count > 0:
                    print(f"   ✅ Doublon 'tente' supprimé")
                else:
                    print(f"   ❌ Échec suppression doublon")
        else:
            print("✅ Pas de doublon détecté")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 CORRECTION DES TRADUCTIONS FAMILLE")
    print("🎯 Correspondance avec les fichiers audio disponibles")
    print()
    
    success = correct_famille_translations()
    
    if success:
        print("🎉 Corrections terminées avec succès!")
    else:
        print("⚠️ Corrections terminées avec des erreurs")