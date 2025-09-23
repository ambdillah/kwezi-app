#!/usr/bin/env python3
"""
Script pour étendre le système audio dual aux sections nature, nombres et animaux
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

def extend_dual_audio_system():
    """Étendre le système dual aux catégories nature, nombres et animaux."""
    
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
        
        print("🔧 EXTENSION DU SYSTÈME AUDIO DUAL")
        print("=" * 60)
        print("Objectif: Étendre aux sections nature, nombres et animaux")
        print()
        
        # Créer une sauvegarde avant restructuration
        print("💾 Création d'une sauvegarde avant extension...")
        try:
            backup_path = db_protection.create_backup("before_audio_extension")
            if backup_path:
                print("✅ Sauvegarde créée avec succès")
            else:
                print("⚠️ Échec de la sauvegarde")
        except Exception as e:
            print(f"⚠️ Problème sauvegarde (continuons quand même): {str(e)}")
        print()
        
        # Traiter chaque catégorie
        categories = ['nature', 'nombres', 'animaux']
        total_restructured = 0
        
        for category in categories:
            print(f"📂 TRAITEMENT CATÉGORIE: {category.upper()}")
            print("-" * 50)
            
            # Récupérer tous les mots de cette catégorie
            category_words = list(collection.find({"category": category}))
            print(f"📝 {len(category_words)} mots trouvés dans {category}")
            
            if not category_words:
                print(f"⚠️ Aucun mot trouvé pour {category}, passage à la suivante")
                continue
            
            # Lister les fichiers audio disponibles pour cette catégorie
            audio_dir = f"/app/frontend/assets/audio/{category}"
            available_files = []
            if os.path.exists(audio_dir):
                available_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
            
            print(f"🎵 {len(available_files)} fichiers audio disponibles pour {category}")
            
            category_restructured = 0
            
            for word in category_words:
                french = word.get('french', 'N/A')
                shimaore = word.get('shimaore', 'N/A').lower()
                kibouchi = word.get('kibouchi', 'N/A').lower()
                
                print(f"  🔸 {french}")
                print(f"     Shimaoré: '{word.get('shimaore', 'N/A')}'")
                print(f"     Kibouchi: '{word.get('kibouchi', 'N/A')}'")
                
                # Chercher les correspondances audio
                shimoare_file = None
                kibouchi_file = None
                
                # Logique de correspondance basique pour commencer
                # On cherche des correspondances directes avec les traductions
                for filename in available_files:
                    base_name = filename.replace('.m4a', '').lower()
                    
                    # Correspondance avec shimaoré (sans espaces ni slashes)
                    shimaore_clean = shimaore.replace(' ', '').replace('/', '').replace('-', '').replace("'", "")
                    if (base_name == shimaore_clean or 
                        base_name.replace(' ', '').replace('-', '').replace("'", "") == shimaore_clean or
                        base_name in shimaore or
                        shimaore_clean in base_name.replace(' ', '').replace('-', '').replace("'", "")):
                        shimoare_file = filename
                    
                    # Correspondance avec kibouchi (sans espaces ni slashes)
                    kibouchi_clean = kibouchi.replace(' ', '').replace('/', '').replace('-', '').replace("'", "")
                    if (base_name == kibouchi_clean or
                        base_name.replace(' ', '').replace('-', '').replace("'", "") == kibouchi_clean or
                        base_name in kibouchi or
                        kibouchi_clean in base_name.replace(' ', '').replace('-', '').replace("'", "")):
                        kibouchi_file = filename
                
                # Mappings spéciaux pour nombres (logique numérique)
                if category == 'nombres':
                    number_mappings = {
                        'un': {'shimaore': 'Moja.m4a', 'kibouchi': 'Areki.m4a'},
                        'deux': {'shimaore': 'Mbili.m4a', 'kibouchi': 'Aroyi.m4a'},
                        'trois': {'shimaore': 'Trarou.m4a', 'kibouchi': 'Telou.m4a'},
                        'quatre': {'shimaore': 'Nhé.m4a', 'kibouchi': 'Efatra.m4a'},
                        'cinq': {'shimaore': 'Tsano.m4a', 'kibouchi': 'Dimi.m4a'},
                        'six': {'shimaore': 'Sita.m4a', 'kibouchi': 'Tchouta.m4a'},
                        'sept': {'shimaore': 'Saba.m4a', 'kibouchi': 'Fitou.m4a'},
                        'huit': {'shimaore': 'Nané.m4a', 'kibouchi': 'Valou.m4a'},
                        'neuf': {'shimaore': 'Chendra.m4a', 'kibouchi': 'Civi.m4a'},
                        'dix': {'shimaore': 'Koumi.m4a', 'kibouchi': 'Foulou.m4a'},
                        'vingt': {'shimaore': 'Chirini.m4a', 'kibouchi': 'Arompoulou.m4a'},
                        'trente': {'shimaore': 'Thalathini.m4a', 'kibouchi': 'Téloumpoulou.m4a'},
                        'quarante': {'shimaore': 'Arbahini.m4a', 'kibouchi': 'Efampoulou.m4a'},
                        'cinquante': {'shimaore': 'Hamssini.m4a', 'kibouchi': 'Dimimpoulou.m4a'},
                        'soixante': {'shimaore': 'Sitini.m4a', 'kibouchi': 'Tchoutampoulou.m4a'},
                        'soixante-dix': {'shimaore': 'Sabini.m4a', 'kibouchi': 'Fitoumpoulou.m4a'},
                        'quatre-vingts': {'shimaore': 'Thamanini.m4a', 'kibouchi': 'Valoumpoulou.m4a'},
                        'cent': {'shimaore': 'Miya.m4a', 'kibouchi': 'Zatou.m4a'}
                    }
                    
                    if french.lower() in number_mappings:
                        mapping = number_mappings[french.lower()]
                        # Vérifier si les fichiers existent
                        if mapping['shimaore'] in available_files:
                            shimoare_file = mapping['shimaore']
                        if mapping['kibouchi'] in available_files:
                            kibouchi_file = mapping['kibouchi']
                
                # Afficher les résultats
                if shimoare_file:
                    print(f"     🎵 Shimaoré: {shimoare_file}")
                else:
                    print(f"     ❌ Shimaoré: Aucun fichier trouvé")
                
                if kibouchi_file:
                    print(f"     🎵 Kibouchi: {kibouchi_file}")
                else:
                    print(f"     ❌ Kibouchi: Aucun fichier trouvé")
                
                # Appliquer la restructuration
                update_data = {
                    # Nouvelle structure avec colonnes séparées
                    "shimoare_audio_filename": shimoare_file if shimoare_file else None,
                    "kibouchi_audio_filename": kibouchi_file if kibouchi_file else None,
                    "shimoare_has_audio": bool(shimoare_file),
                    "kibouchi_has_audio": bool(kibouchi_file),
                    "dual_audio_system": True,
                    "audio_restructured_at": datetime.now(),
                    # Mettre à jour les anciens champs pour compatibilité
                    "has_authentic_audio": bool(shimoare_file or kibouchi_file),
                    "audio_filename": shimoare_file if shimoare_file else kibouchi_file,
                    "audio_pronunciation_lang": "dual_system",
                    "audio_source": f"restructured_dual_system_{category}"
                }
                
                result = collection.update_one(
                    {"_id": word["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    category_restructured += 1
                    print(f"     ✅ Restructuration appliquée")
                else:
                    print(f"     ⚠️ Aucune modification effectuée")
                
                print()
            
            print(f"📈 Catégorie {category}: {category_restructured} mots restructurés")
            total_restructured += category_restructured
            print()
        
        # Statistiques finales
        print("=" * 60)
        print(f"📊 RÉSUMÉ DE L'EXTENSION")
        print(f"🔧 Total mots restructurés: {total_restructured}")
        print()
        
        # Vérification finale par catégorie
        for category in categories:
            dual_system_words = list(collection.find({"category": category, "dual_audio_system": True}))
            shimoare_audio_count = len([w for w in dual_system_words if w.get('shimoare_has_audio')])
            kibouchi_audio_count = len([w for w in dual_system_words if w.get('kibouchi_has_audio')])
            
            print(f"📂 {category.upper()}:")
            print(f"   🎵 Mots avec audio shimaoré: {shimoare_audio_count}")
            print(f"   🎵 Mots avec audio kibouchi: {kibouchi_audio_count}")
            print(f"   📊 Total mots avec système dual: {len(dual_system_words)}")
            print()
        
        print("✅ Extension du système dual terminée!")
        print("🎯 Les catégories nature, nombres et animaux ont maintenant des colonnes séparées")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 EXTENSION SYSTÈME AUDIO DUAL")
    print("🎯 Objectif: Étendre aux catégories nature, nombres et animaux")
    print()
    
    success = extend_dual_audio_system()
    
    if success:
        print("🎉 Extension terminée avec succès!")
    else:
        print("💥 Échec de l'extension")
        sys.exit(1)