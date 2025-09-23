#!/usr/bin/env python3
"""
Script pour restructurer la base de données avec des colonnes séparées
pour les prononciations shimaoré et kibouchi
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

def restructure_audio_database():
    """Restructure la base avec colonnes audio séparées pour chaque langue."""
    
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
        print()
        
        print("🔧 RESTRUCTURATION DE LA BASE DE DONNÉES AUDIO")
        print("=" * 60)
        print("Objectif: Créer des colonnes séparées pour prononciations")
        print("- shimoare_audio_filename")
        print("- kibouchi_audio_filename")
        print("- shimoare_has_audio")
        print("- kibouchi_has_audio")
        print()
        
        # Créer une sauvegarde avant restructuration
        print("💾 Création d'une sauvegarde avant restructuration...")
        try:
            backup_path = db_protection.create_backup("before_audio_restructure")
            if backup_path:
                print("✅ Sauvegarde créée avec succès")
            else:
                print("⚠️ Échec de la sauvegarde")
        except Exception as e:
            print(f"⚠️ Problème sauvegarde (continuons quand même): {str(e)}")
        print()
        
        # Mapper tous les fichiers audio disponibles aux traductions
        print("📂 ANALYSE DES FICHIERS AUDIO DISPONIBLES")
        print("-" * 50)
        
        audio_dir = "/app/frontend/assets/audio/famille"
        all_files = []
        if os.path.exists(audio_dir):
            all_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
        
        print(f"🎵 {len(all_files)} fichiers audio disponibles")
        
        # Récupérer tous les mots de famille
        famille_words = list(collection.find({"category": "famille"}))
        print(f"👨‍👩‍👧‍👦 {len(famille_words)} mots famille dans la base")
        print()
        
        print("🎯 CRÉATION DES CORRESPONDANCES AUDIO DUALES")
        print("-" * 50)
        
        restructured_count = 0
        
        for word in famille_words:
            french = word.get('french', 'N/A')
            shimaore = word.get('shimaore', 'N/A').lower()
            kibouchi = word.get('kibouchi', 'N/A').lower()
            
            print(f"🔸 {french}")
            print(f"   Shimaoré: '{word.get('shimaore', 'N/A')}'")
            print(f"   Kibouchi: '{word.get('kibouchi', 'N/A')}'")
            
            # Chercher les fichiers correspondants
            shimoare_file = None
            kibouchi_file = None
            
            for filename in all_files:
                base_name = filename.replace('.m4a', '').lower()
                
                # Correspondance directe avec shimaoré
                if (base_name == shimaore or 
                    base_name.replace(' ', '').replace('/', '') == shimaore.replace(' ', '').replace('/', '') or
                    base_name in shimaore or
                    shimaore in base_name):
                    shimoare_file = filename
                
                # Correspondance directe avec kibouchi
                if (base_name == kibouchi or
                    base_name.replace(' ', '').replace('/', '') == kibouchi.replace(' ', '').replace('/', '') or
                    base_name in kibouchi or
                    kibouchi in base_name):
                    kibouchi_file = filename
                
                # Correspondances spécifiques avec suffixes s/k
                if ' s' in filename.lower() and (shimaore in base_name.replace(' s', '') or base_name.replace(' s', '') in shimaore):
                    shimoare_file = filename
                
                if ' k' in filename.lower() and (kibouchi in base_name.replace(' k', '') or base_name.replace(' k', '') in kibouchi):
                    kibouchi_file = filename
            
            # Cas spéciaux connus
            special_mappings = {
                'papa': {'shimoare': 'Baba s.m4a', 'kibouchi': 'Baba k.m4a'},
                'oncle paternel': {'shimoare': 'Baba titi-bolé.m4a', 'kibouchi': 'Baba héli-bé.m4a'},
                'madame': {'shimoare': 'Bweni.m4a', 'kibouchi': 'Viavi.m4a'},
                'monsieur': {'shimoare': 'Mongné.m4a', 'kibouchi': 'Lalahi.m4a'},
                'tante': {'shimoare': 'Mama titi-bolé.m4a', 'kibouchi': 'Ninfndri héli-bé.m4a'},
                'tente': {'shimoare': 'Mama titi-bolé.m4a', 'kibouchi': 'Ninfndri héli-bé.m4a'},
                'famille': {'shimoare': 'Mdjamaza.m4a', 'kibouchi': 'Havagna.m4a'},
                'grand-mère': {'shimoare': 'Coco.m4a', 'kibouchi': 'Dadi.m4a'},
                'grand-père': {'shimoare': 'Bacoco.m4a', 'kibouchi': 'Dadayi.m4a'},
                'grande sœur': {'shimoare': 'Zouki mtroumché.m4a', 'kibouchi': 'Zoki viavi.m4a'},
                'grand frère': {'shimoare': 'Zouki mtroubaba.m4a', 'kibouchi': 'Zoki lalahi.m4a'},
                'frère': {'shimoare': 'Moinagna mtroubaba.m4a', 'kibouchi': 'Anadahi.m4a'},
                'sœur': {'shimoare': 'Moinagna mtroumama.m4a', 'kibouchi': 'Anabavi.m4a'},
                'petit frère': {'shimoare': 'Moinagna mtroubaba.m4a', 'kibouchi': 'Anadahi.m4a'},
                'petite sœur': {'shimoare': 'Moinagna mtroumama.m4a', 'kibouchi': 'Anabavi.m4a'},
                'garçon': {'shimoare': 'Mtroubaba.m4a', 'kibouchi': 'Lalahi.m4a'},
                'homme': {'shimoare': 'Mtroubaba.m4a', 'kibouchi': 'Lalahi.m4a'},
                'fille': {'shimoare': 'Mtroumama.m4a', 'kibouchi': 'Viavi.m4a'},
                'femme': {'shimoare': 'Mtroumama.m4a', 'kibouchi': 'Viavi.m4a'},
                'maman': {'shimoare': 'Mama.m4a', 'kibouchi': 'Mama.m4a'},
                'ami': {'shimoare': 'Mwandzani.m4a', 'kibouchi': 'Mwandzani.m4a'},
                'oncle maternel': {'shimoare': 'Zama.m4a', 'kibouchi': 'Zama.m4a'},
                'épouse oncle maternel': {'shimoare': 'Zena.m4a', 'kibouchi': 'Zena.m4a'}
            }
            
            if french in special_mappings:
                shimoare_file = special_mappings[french]['shimoare']
                kibouchi_file = special_mappings[french]['kibouchi']
            
            # Afficher les résultats
            if shimoare_file:
                print(f"   🎵 Shimaoré: {shimoare_file}")
            else:
                print(f"   ❌ Shimaoré: Aucun fichier trouvé")
            
            if kibouchi_file:
                print(f"   🎵 Kibouchi: {kibouchi_file}")
            else:
                print(f"   ❌ Kibouchi: Aucun fichier trouvé")
            
            # Appliquer la restructuration
            update_data = {
                # Nouvelle structure avec colonnes séparées
                "shimoare_audio_filename": shimoare_file if shimoare_file else None,
                "kibouchi_audio_filename": kibouchi_file if kibouchi_file else None,
                "shimoare_has_audio": bool(shimoare_file),
                "kibouchi_has_audio": bool(kibouchi_file),
                "dual_audio_system": True,
                "audio_restructured_at": datetime.now(),
                # Supprimer les anciens champs
                "has_authentic_audio": bool(shimoare_file or kibouchi_file),
                "audio_filename": shimoare_file if shimoare_file else kibouchi_file,
                "audio_pronunciation_lang": "dual_system",
                "audio_source": "restructured_dual_system"
            }
            
            result = collection.update_one(
                {"_id": word["_id"]},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                restructured_count += 1
                print(f"   ✅ Restructuration appliquée")
            else:
                print(f"   ⚠️ Aucune modification effectuée")
            
            print()
        
        # Statistiques finales
        print("=" * 60)
        print(f"📈 RÉSUMÉ DE LA RESTRUCTURATION")
        print(f"🔧 Mots restructurés: {restructured_count}")
        print()
        
        # Vérification finale
        dual_system_words = list(collection.find({"dual_audio_system": True}))
        shimoare_audio_count = len([w for w in dual_system_words if w.get('shimoare_has_audio')])
        kibouchi_audio_count = len([w for w in dual_system_words if w.get('kibouchi_has_audio')])
        
        print(f"🎵 Mots avec audio shimaoré: {shimoare_audio_count}")
        print(f"🎵 Mots avec audio kibouchi: {kibouchi_audio_count}")
        print(f"📊 Total mots restructurés: {len(dual_system_words)}")
        print()
        
        print("✅ Restructuration de la base de données terminée!")
        print("🎯 Chaque mot a maintenant des colonnes séparées pour chaque langue")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 RESTRUCTURATION BASE DE DONNÉES AUDIO")
    print("🎯 Objectif: Colonnes séparées pour prononciations shimaoré/kibouchi")
    print()
    
    success = restructure_audio_database()
    
    if success:
        print("🎉 Restructuration terminée avec succès!")
    else:
        print("💥 Échec de la restructuration")
        sys.exit(1)