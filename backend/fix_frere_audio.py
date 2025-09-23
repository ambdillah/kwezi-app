#!/usr/bin/env python3
"""
Script pour corriger le cas spécial du mot "frère" qui a besoin
de deux fichiers audio différents (un pour chaque langue)
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

def fix_frere_audio():
    """Corrige l'assignation audio pour le mot 'frère'."""
    
    try:
        # Connexion à MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.words
        
        print(f"🔗 Connexion à MongoDB: {mongo_url}")
        print(f"📊 Base de données: {db_name}")
        print()
        
        print("🔧 CORRECTION SPÉCIALE POUR 'FRÈRE'")
        print("=" * 50)
        print("Problème: 'frère' a deux prononciations différentes")
        print("  - Shimaoré: 'mwanagna mtroubaba' → Moinagna mtroubaba.m4a")
        print("  - Kibouchi: 'anadahi' → Anadahi.m4a") 
        print()
        
        # Rechercher le mot "frère"
        frere_word = collection.find_one({"french": "frère"})
        
        if frere_word:
            print(f"✅ Mot 'frère' trouvé:")
            print(f"   Shimaoré: {frere_word.get('shimaore', 'N/A')}")
            print(f"   Kibouchi: {frere_word.get('kibouchi', 'N/A')}")
            print(f"   Fichier actuel: {frere_word.get('audio_filename', 'N/A')}")
            print(f"   Langue actuelle: {frere_word.get('audio_pronunciation_lang', 'N/A')}")
            print()
            
            # Stratégie : créer des champs étendus pour gérer les deux fichiers
            # ou utiliser une approche avec condition dans le système audio
            
            print("🎯 SOLUTION PROPOSÉE:")
            print("Option 1: Ajouter des champs audio étendus")
            print("Option 2: Garder le système actuel mais noter la disponibilité")
            print()
            
            # Pour l'instant, implémenter l'Option 2
            # Ajouter des métadonnées indiquant qu'il y a des fichiers alternatifs
            
            update_data = {
                "audio_shimoare_available": True,
                "audio_shimoare_filename": "Moinagna mtroubaba.m4a",
                "audio_kibouchi_available": True, 
                "audio_kibouchi_filename": "Anadahi.m4a",
                "audio_dual_language_note": "Ce mot a des prononciations différentes dans chaque langue",
                "audio_correction_applied_at": datetime.now(),
                # Garder l'assignation actuelle pour la compatibilité
                "audio_filename": "Anadahi.m4a",  # Kibouchi par défaut
                "audio_pronunciation_lang": "kibouchi"
            }
            
            result = collection.update_one(
                {"_id": frere_word["_id"]},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                print("✅ Métadonnées étendues ajoutées avec succès")
                print("📝 Le système peut maintenant identifier les deux fichiers disponibles")
            else:
                print("⚠️ Aucune modification effectuée")
            
        else:
            print("❌ Mot 'frère' non trouvé dans la base")
        
        print()
        print("📋 PROCHAINES ÉTAPES:")
        print("1. Modifier le système audio frontend pour utiliser les nouveaux champs")
        print("2. Détecter audio_shimoare_filename et audio_kibouchi_filename") 
        print("3. Jouer le bon fichier selon la langue demandée")
        print()
        
        # Fermer la connexion
        client.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 CORRECTION AUDIO SPÉCIFIQUE POUR 'FRÈRE'")
    print()
    
    success = fix_frere_audio()
    
    if success:
        print("🎉 Correction terminée!")
    else:
        print("💥 Échec de la correction")
        sys.exit(1)