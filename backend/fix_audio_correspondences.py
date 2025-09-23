#!/usr/bin/env python3
"""
Script de correction des correspondances audio incorrectes
Basé sur l'analyse de vérification approfondie
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# Charger les variables d'environnement
load_dotenv()

def fix_audio_correspondences():
    """Corriger les correspondances audio incorrectes identifiées."""
    
    try:
        # Connexion à MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.words
        
        print("🔧 CORRECTION DES CORRESPONDANCES AUDIO INCORRECTES")
        print("=" * 70)
        print("Correction des 6 erreurs détectées dans la catégorie famille")
        print()
        
        # Corrections spécifiques basées sur l'analyse
        corrections = [
            {
                "category": "famille",
                "french": "madame",
                "current_shimaore_file": "Bweni.m4a",
                "correct_shimaore_file": "Bwéni.m4a",
                "explanation": "Correction accent: Bweni → Bwéni"
            },
            {
                "category": "famille", 
                "french": "monsieur",
                "current_shimaore_file": "Mongné.m4a",
                "correct_shimaore_file": "Mogné.m4a",
                "explanation": "Correction orthographe: Mongné → Mogné"
            },
            {
                "category": "famille",
                "french": "petit frère",
                "current_kibouchi_file": "Anadahi.m4a",
                "correct_kibouchi_file": "Zandri.m4a",
                "explanation": "Correction correspondance: petit frère kibouchi = zandri"
            },
            {
                "category": "famille",
                "french": "petite sœur", 
                "current_kibouchi_file": "Anabavi.m4a",
                "correct_kibouchi_file": "Zandri.m4a",
                "explanation": "Correction correspondance: petite sœur kibouchi = zandri"
            },
            {
                "category": "famille",
                "french": "tante",
                "current_kibouchi_file": "Ninfndri héli-bé.m4a",
                "correct_kibouchi_file": "Nindri héli-bé.m4a",
                "explanation": "Correction orthographe: Ninfndri → Nindri"
            },
            {
                "category": "famille",
                "french": "tente",
                "current_kibouchi_file": "Ninfndri héli-bé.m4a", 
                "correct_kibouchi_file": "Nindri héli-bé.m4a",
                "explanation": "Correction orthographe: Ninfndri → Nindri"
            }
        ]
        
        # Vérifier les fichiers audio disponibles
        famille_dir = "/app/frontend/assets/audio/famille"
        available_files = []
        if os.path.exists(famille_dir):
            available_files = [f for f in os.listdir(famille_dir) if f.endswith('.m4a')]
        
        print(f"📂 Fichiers audio famille disponibles: {len(available_files)}")
        
        corrections_applied = 0
        corrections_skipped = 0
        
        for i, correction in enumerate(corrections, 1):
            print(f"\n--- Correction {i}/6 ---")
            print(f"🔸 Mot français: {correction['french']}")
            print(f"📝 Explication: {correction['explanation']}")
            
            # Trouver le mot dans la base de données
            word_doc = collection.find_one({
                "category": correction["category"],
                "french": correction["french"]
            })
            
            if not word_doc:
                print(f"❌ Mot '{correction['french']}' non trouvé dans la base")
                corrections_skipped += 1
                continue
            
            # Préparer les mises à jour
            update_fields = {}
            changes_made = []
            
            # Correction Shimaoré si nécessaire
            if "current_shimaore_file" in correction:
                current_file = correction["current_shimaore_file"]
                correct_file = correction["correct_shimaore_file"]
                
                print(f"   Shimaoré: {current_file} → {correct_file}")
                
                # Vérifier si le fichier correct existe
                if correct_file in available_files:
                    update_fields["shimoare_audio_filename"] = correct_file
                    changes_made.append(f"shimaoré: {correct_file}")
                elif current_file in available_files:
                    # Garder l'ancien fichier si le nouveau n'existe pas
                    print(f"   ⚠️ Fichier {correct_file} non trouvé, conservation de {current_file}")
                else:
                    print(f"   ⚠️ Aucun fichier trouvé, suppression de l'audio shimaoré")
                    update_fields["shimoare_audio_filename"] = None
                    update_fields["shimoare_has_audio"] = False
                    changes_made.append("shimaoré: supprimé (fichier introuvable)")
            
            # Correction Kibouchi si nécessaire
            if "current_kibouchi_file" in correction:
                current_file = correction["current_kibouchi_file"]
                correct_file = correction["correct_kibouchi_file"]
                
                print(f"   Kibouchi: {current_file} → {correct_file}")
                
                # Vérifier si le fichier correct existe
                if correct_file in available_files:
                    update_fields["kibouchi_audio_filename"] = correct_file
                    changes_made.append(f"kibouchi: {correct_file}")
                elif current_file in available_files:
                    # Garder l'ancien fichier si le nouveau n'existe pas
                    print(f"   ⚠️ Fichier {correct_file} non trouvé, conservation de {current_file}")
                else:
                    print(f"   ⚠️ Aucun fichier trouvé, suppression de l'audio kibouchi")
                    update_fields["kibouchi_audio_filename"] = None
                    update_fields["kibouchi_has_audio"] = False
                    changes_made.append("kibouchi: supprimé (fichier introuvable)")
            
            # Appliquer les corrections si nécessaires
            if update_fields:
                # Ajouter la timestamp de correction
                update_fields["audio_corrected_at"] = datetime.now()
                
                result = collection.update_one(
                    {"_id": word_doc["_id"]},
                    {"$set": update_fields}
                )
                
                if result.modified_count > 0:
                    print(f"   ✅ Correction appliquée: {', '.join(changes_made)}")
                    corrections_applied += 1
                else:
                    print(f"   ❌ Échec de la correction")
                    corrections_skipped += 1
            else:
                print(f"   ⚠️ Aucune modification nécessaire")
                corrections_skipped += 1
        
        print("\n" + "=" * 70)
        print(f"📊 RÉSUMÉ DES CORRECTIONS")
        print(f"✅ Corrections appliquées: {corrections_applied}")
        print(f"⚠️ Corrections ignorées: {corrections_skipped}")
        print(f"📈 Total traité: {corrections_applied + corrections_skipped}/6")
        
        # Vérification post-correction
        print("\n🔍 VÉRIFICATION POST-CORRECTION")
        print("-" * 50)
        
        post_correction_errors = 0
        for correction in corrections:
            word_doc = collection.find_one({
                "category": correction["category"],
                "french": correction["french"]
            })
            
            if word_doc:
                shimoare_file = word_doc.get('shimoare_audio_filename')
                kibouchi_file = word_doc.get('kibouchi_audio_filename')
                
                print(f"🔸 {correction['french']}:")
                print(f"   Shimaoré: {shimoare_file}")
                print(f"   Kibouchi: {kibouchi_file}")
                
                # Vérifier si les fichiers existent
                errors = []
                if shimoare_file and shimoare_file not in available_files:
                    errors.append(f"Fichier shimaoré {shimoare_file} introuvable")
                    post_correction_errors += 1
                
                if kibouchi_file and kibouchi_file not in available_files:
                    errors.append(f"Fichier kibouchi {kibouchi_file} introuvable")
                    post_correction_errors += 1
                
                if errors:
                    print(f"   🚨 Erreurs: {'; '.join(errors)}")
                else:
                    print(f"   ✅ Correspondances correctes")
        
        print(f"\n📈 Erreurs restantes: {post_correction_errors}")
        
        if post_correction_errors == 0:
            print("🎉 Toutes les correspondances sont maintenant correctes!")
        else:
            print("⚠️ Des erreurs subsistent, vérification manuelle nécessaire")
        
        client.close()
        return post_correction_errors == 0
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 CORRECTION DES CORRESPONDANCES AUDIO")
    print("🎯 Correction des 6 erreurs détectées")
    print()
    
    success = fix_audio_correspondences()
    
    if success:
        print("🎉 Corrections terminées avec succès!")
    else:
        print("⚠️ Corrections terminées avec des erreurs restantes")