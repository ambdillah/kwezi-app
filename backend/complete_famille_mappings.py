#!/usr/bin/env python3
"""
Script pour compléter les mappings famille manquants
en suivant la logique s/k pour différencier les langues
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

def complete_famille_mappings():
    """Complete les mappings famille manquants."""
    
    # Mappings à compléter basés sur l'analyse
    mappings_to_add = [
        {
            "french": "papa",
            "shimoare_file": "Baba s.m4a",  # s = shimaoré
            "kibouchi_file": "Baba k.m4a",  # k = kibouchi
            "note": "Même orthographe 'baba' dans les deux langues"
        },
        {
            "french": "oncle paternel", 
            "shimoare_file": "Baba titi-bolé.m4a",  # Correspond à "Baba titi/bolé"
            "kibouchi_file": "Baba héli-bé.m4a",    # Correspond à "Baba heli/bé"
            "note": "Différentes orthographes selon la langue"
        },
        {
            "french": "monsieur",
            "shimoare_file": "Mongné.m4a",    # Correspond à "mogné"
            "kibouchi_file": "Lalahi.m4a",    # Correspond à "lalahi" (générique homme)
            "note": "Fichiers différents selon la langue"
        },
        {
            "french": "madame",
            "shimoare_file": "Bweni.m4a",     # Correspond à "bwéni"
            "kibouchi_file": "Viavi.m4a",     # Correspond à "viavi" (générique femme)
            "note": "Fichiers différents selon la langue"
        },
        {
            "french": "tante",
            "shimoare_file": "Mama titi-bolé.m4a",   # Correspond à "mama titi/bolé"
            "kibouchi_file": "Ninfndri héli-bé.m4a", # Correspond à "nindri heli/bé"
            "note": "Différentes orthographes selon la langue"
        },
        {
            "french": "tente",
            "shimoare_file": "Mama titi-bolé.m4a",   # Même que tante (même traduction)
            "kibouchi_file": "Ninfndri héli-bé.m4a", # Même que tante (même traduction)
            "note": "Même traduction que 'tante'"
        }
    ]
    
    # Cas spéciaux où on utilise le fichier existant pour les deux langues
    same_audio_mappings = [
        {
            "french": "femme",
            "use_existing": "fille/femme",  # Utiliser le mapping existant
            "note": "Même traductions que fille"
        },
        {
            "french": "fille", 
            "use_existing": "fille/femme",  # Utiliser le mapping existant
            "note": "Même traductions que femme"
        },
        {
            "french": "garçon",
            "use_existing": "garçon/homme",  # Utiliser le mapping existant
            "note": "Même traductions que homme"
        },
        {
            "french": "homme",
            "use_existing": "garçon/homme",  # Utiliser le mapping existant
            "note": "Même traductions que garçon"
        }
    ]
    
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
        
        print("🔧 COMPLÉTION DES MAPPINGS FAMILLE")
        print("=" * 50)
        
        # Traiter les mappings avec fichiers spécifiques
        mappings_created = 0
        
        for mapping in mappings_to_add:
            french_word = mapping["french"]
            shimoare_file = mapping["shimoare_file"] 
            kibouchi_file = mapping["kibouchi_file"]
            note = mapping["note"]
            
            print(f"🔸 {french_word}")
            print(f"   📝 Note: {note}")
            
            # Rechercher le mot
            word = collection.find_one({"french": french_word})
            if word:
                shimaore = word.get('shimaore', 'N/A')
                kibouchi = word.get('kibouchi', 'N/A')
                
                print(f"   ✅ Mot trouvé:")
                print(f"      Shimaoré: '{shimaore}' → {shimoare_file}")
                print(f"      Kibouchi: '{kibouchi}' → {kibouchi_file}")
                
                # Déterminer quel fichier utiliser par défaut
                # Si même orthographe, utiliser shimaoré par défaut
                if shimaore.lower().replace('/', '').replace(' ', '') == kibouchi.lower().replace('/', '').replace(' ', ''):
                    default_file = shimoare_file
                    default_lang = "both"
                    print(f"      → Orthographe identique, utilisation: {default_file} (both)")
                else:
                    # Utiliser le fichier shimaoré par défaut
                    default_file = shimoare_file
                    default_lang = "shimaore"
                    print(f"      → Orthographes différentes, utilisation: {default_file} (shimaore)")
                
                # Appliquer le mapping
                update_data = {
                    "has_authentic_audio": True,
                    "audio_filename": default_file,
                    "audio_pronunciation_lang": default_lang,
                    "audio_source": "complete_famille_mappings",
                    "audio_updated_at": datetime.now(),
                    # Métadonnées étendues pour les deux fichiers
                    "audio_shimoare_filename": shimoare_file,
                    "audio_kibouchi_filename": kibouchi_file,
                    "audio_mapping_note": note
                }
                
                result = collection.update_one(
                    {"_id": word["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    mappings_created += 1
                    print(f"      ✅ Mapping créé avec succès")
                else:
                    print(f"      ⚠️ Aucune modification effectuée")
            else:
                print(f"   ❌ Mot '{french_word}' non trouvé")
            
            print()
        
        # Traiter les cas spéciaux (utiliser mapping existant)
        print("🔄 RÉUTILISATION DE MAPPINGS EXISTANTS")
        print("-" * 40)
        
        for mapping in same_audio_mappings:
            french_word = mapping["french"]
            use_existing = mapping["use_existing"]
            note = mapping["note"]
            
            print(f"🔸 {french_word}")
            print(f"   📝 Note: {note}")
            
            # Trouver le mot existant avec audio
            existing_word = collection.find_one({"french": use_existing, "has_authentic_audio": True})
            target_word = collection.find_one({"french": french_word})
            
            if existing_word and target_word:
                print(f"   ✅ Copie du mapping de '{use_existing}' vers '{french_word}'")
                
                # Copier les données audio
                update_data = {
                    "has_authentic_audio": True,
                    "audio_filename": existing_word.get('audio_filename'),
                    "audio_pronunciation_lang": existing_word.get('audio_pronunciation_lang'),
                    "audio_source": "copied_from_" + use_existing.replace('/', '_'),
                    "audio_updated_at": datetime.now(),
                    "audio_copy_note": f"Copié depuis {use_existing} - {note}"
                }
                
                result = collection.update_one(
                    {"_id": target_word["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    mappings_created += 1
                    print(f"      ✅ Mapping copié avec succès")
                else:
                    print(f"      ⚠️ Aucune modification effectuée")
            else:
                print(f"   ❌ Impossible de copier: source ou cible non trouvée")
            
            print()
        
        # Statistiques finales
        print("=" * 50)
        print(f"📈 RÉSUMÉ DE LA COMPLÉTION")
        print(f"✅ Nouveaux mappings créés: {mappings_created}")
        
        # Vérification finale
        total_audio = collection.count_documents({"has_authentic_audio": True})
        famille_audio = collection.count_documents({"category": "famille", "has_authentic_audio": True})
        
        print(f"🎵 Total mots avec audio: {total_audio}")
        print(f"👨‍👩‍👧‍👦 Mots famille avec audio: {famille_audio}")
        print()
        
        print("✅ Complétion des mappings famille terminée!")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 COMPLÉTION DES MAPPINGS FAMILLE")
    print("🎯 Objectif: Compléter tous les mappings manquants")
    print()
    
    success = complete_famille_mappings()
    
    if success:
        print("🎉 Complétion terminée avec succès!")
    else:
        print("💥 Échec de la complétion")
        sys.exit(1)