#!/usr/bin/env python3
"""
Script pour générer un rapport détaillé des correspondances
traduction → prononciation assignée pour détecter les erreurs
"""

import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

# Ajouter le chemin du backend au PYTHONPATH
sys.path.append('/app/backend')

# Charger les variables d'environnement
load_dotenv()

def analyze_mapping_errors():
    """Analyse les erreurs de correspondance traduction/prononciation."""
    
    try:
        # Connexion à MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.words
        
        print("🔍 RAPPORT DÉTAILLÉ DES CORRESPONDANCES TRADUCTION → PRONONCIATION")
        print("=" * 90)
        print("🚨 OBJECTIF: Détecter les non-correspondances entre traductions et prononciations")
        print("=" * 90)
        print()
        
        # Analyser section famille
        print("👨‍👩‍👧‍👦 SECTION FAMILLE - ANALYSE DÉTAILLÉE")
        print("-" * 70)
        
        famille_words = list(collection.find({
            "category": "famille", 
            "has_authentic_audio": True
        }).sort("french", 1))
        
        famille_errors = []
        
        for word in famille_words:
            french = word.get('french', 'N/A')
            shimaore_translation = word.get('shimaore', 'N/A')
            kibouchi_translation = word.get('kibouchi', 'N/A')
            audio_filename = word.get('audio_filename', 'N/A')
            audio_lang = word.get('audio_pronunciation_lang', 'N/A')
            
            print(f"🔸 {french.upper()}")
            print(f"   📝 Traduction shimaoré: '{shimaore_translation}'")
            print(f"   📝 Traduction kibouchi: '{kibouchi_translation}'")
            print(f"   🎵 Fichier audio assigné: {audio_filename}")
            print(f"   🎯 Langue du fichier: {audio_lang}")
            
            # Analyser les correspondances potentielles
            filename_lower = audio_filename.lower()
            shimaore_lower = shimaore_translation.lower().replace(' ', '').replace('/', '').replace("'", "")
            kibouchi_lower = kibouchi_translation.lower().replace(' ', '').replace('/', '').replace("'", "")
            
            # Détecter les problèmes de correspondance
            issues = []
            
            # Cas 1: Fichier marqué shimaoré mais nom ressemble plus au kibouchi
            if audio_lang == "shimaore" and kibouchi_lower in filename_lower and shimaore_lower not in filename_lower:
                issues.append(f"⚠️ Fichier marqué shimaoré mais le nom '{audio_filename}' ressemble à la traduction kibouchi '{kibouchi_translation}'")
            
            # Cas 2: Fichier marqué kibouchi mais nom ressemble plus au shimaoré  
            if audio_lang == "kibouchi" and shimaore_lower in filename_lower and kibouchi_lower not in filename_lower:
                issues.append(f"⚠️ Fichier marqué kibouchi mais le nom '{audio_filename}' ressemble à la traduction shimaoré '{shimaore_translation}'")
            
            # Cas 3: Fichier "both" mais ne correspond clairement qu'à une langue
            if audio_lang == "both":
                if (kibouchi_lower in filename_lower and shimaore_lower not in filename_lower):
                    issues.append(f"🔄 Fichier marqué 'both' mais nom '{audio_filename}' correspond seulement au kibouchi '{kibouchi_translation}'")
                elif (shimaore_lower in filename_lower and kibouchi_lower not in filename_lower):
                    issues.append(f"🔄 Fichier marqué 'both' mais nom '{audio_filename}' correspond seulement au shimaoré '{shimaore_translation}'")
            
            # Cas spéciaux connus
            if french == "grande sœur":
                if "viavi" in filename_lower and audio_lang != "kibouchi":
                    issues.append(f"🚨 ERREUR CRITIQUE: 'viavi' est kibouchi mais le fichier est marqué '{audio_lang}'")
                if "mtroumché" not in filename_lower and audio_lang == "shimaore":
                    issues.append(f"🚨 ERREUR CRITIQUE: Le fichier ne contient pas 'mtroumché' (shimaoré pour grande sœur)")
            
            if issues:
                famille_errors.append(french)
                print(f"   🚨 PROBLÈMES DÉTECTÉS:")
                for issue in issues:
                    print(f"      {issue}")
            else:
                print(f"   ✅ Correspondance semble correcte")
            
            print()
        
        # Analyser section nature (échantillon)
        print("\n🌿 SECTION NATURE - ANALYSE ÉCHANTILLON (10 premiers mots)")
        print("-" * 70)
        
        nature_words = list(collection.find({
            "category": "nature", 
            "has_authentic_audio": True
        }).sort("french", 1).limit(10))
        
        nature_errors = []
        
        for word in nature_words:
            french = word.get('french', 'N/A')
            shimaore_translation = word.get('shimaore', 'N/A')
            kibouchi_translation = word.get('kibouchi', 'N/A')
            audio_filename = word.get('audio_filename', 'N/A')
            audio_lang = word.get('audio_pronunciation_lang', 'N/A')
            
            print(f"🔸 {french.upper()}")
            print(f"   📝 Shimaoré: '{shimaore_translation}' | Kibouchi: '{kibouchi_translation}'")
            print(f"   🎵 Audio: {audio_filename} ({audio_lang})")
            
            # Analyse rapide
            filename_lower = audio_filename.lower()
            issues = []
            
            # Vérifier si le nom du fichier correspond à une des traductions
            shimaore_match = any(word in filename_lower for word in shimaore_translation.lower().split() if len(word) > 2)
            kibouchi_match = any(word in filename_lower for word in kibouchi_translation.lower().split() if len(word) > 2)
            
            if audio_lang == "shimaore" and not shimaore_match and kibouchi_match:
                issues.append("⚠️ Fichier shimaoré mais nom correspond au kibouchi")
            elif audio_lang == "kibouchi" and not kibouchi_match and shimaore_match:
                issues.append("⚠️ Fichier kibouchi mais nom correspond au shimaoré")
            
            if issues:
                nature_errors.append(french)
                for issue in issues:
                    print(f"      🚨 {issue}")
            else:
                print(f"      ✅ OK")
            print()
        
        # Résumé des erreurs
        print("📊 RÉSUMÉ DES ERREURS DÉTECTÉES")
        print("=" * 50)
        print(f"🚨 Erreurs famille: {len(famille_errors)}/{len(famille_words)}")
        if famille_errors:
            print(f"   Mots avec problèmes: {', '.join(famille_errors)}")
        
        print(f"🚨 Erreurs nature (échantillon): {len(nature_errors)}/{len(nature_words)}")
        if nature_errors:
            print(f"   Mots avec problèmes: {', '.join(nature_errors)}")
        
        print()
        print("🎯 RECOMMANDATIONS:")
        print("1. Vérifiez chaque correspondance signalée ci-dessus")
        print("2. Indiquez-moi les corrections à apporter")
        print("3. Je corrigerai les mappings erronés dans la base de données")
        print()
        
        # Fermer la connexion
        client.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    analyze_mapping_errors()