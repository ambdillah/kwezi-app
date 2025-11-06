#!/usr/bin/env python3
"""
Script pour générer un rapport détaillé des correspondances
mot français → fichier audio assigné
"""

import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

# Ajouter le chemin du backend au PYTHONPATH
sys.path.append('/app/backend')

# Charger les variables d'environnement
load_dotenv()

def generate_audio_mapping_report():
    """Génère un rapport détaillé des correspondances audio."""
    
    try:
        # Connexion à MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.words
        
        print("📋 RAPPORT DES CORRESPONDANCES AUDIO")
        print("=" * 80)
        print("Ce rapport liste tous les mots avec leurs fichiers audio assignés")
        print("Vérifiez que les correspondances sont correctes")
        print("=" * 80)
        print()
        
        # Section FAMILLE
        print("👨‍👩‍👧‍👦 SECTION FAMILLE")
        print("-" * 50)
        
        famille_words = list(collection.find({
            "category": "famille", 
            "has_authentic_audio": True
        }).sort("french", 1))
        
        if famille_words:
            print(f"📊 {len(famille_words)} mots avec audio assigné:")
            print()
            
            for word in famille_words:
                french = word.get('french', 'N/A')
                shimaore = word.get('shimaore', 'N/A')
                kibouchi = word.get('kibouchi', 'N/A')
                audio_filename = word.get('audio_filename', 'N/A')
                audio_lang = word.get('audio_pronunciation_lang', 'N/A')
                
                print(f"🔸 {french}")
                print(f"   Shimaoré: {shimaore}")
                print(f"   Kibouchi: {kibouchi}")
                print(f"   ► Fichier audio: {audio_filename}")
                print(f"   ► Langue du fichier: {audio_lang}")
                print()
        else:
            print("❌ Aucun mot famille avec audio trouvé")
        
        print()
        
        # Section NATURE
        print("🌿 SECTION NATURE")
        print("-" * 50)
        
        nature_words = list(collection.find({
            "category": "nature", 
            "has_authentic_audio": True
        }).sort("french", 1))
        
        if nature_words:
            print(f"📊 {len(nature_words)} mots avec audio assigné:")
            print()
            
            for word in nature_words:
                french = word.get('french', 'N/A')
                shimaore = word.get('shimaore', 'N/A') 
                kibouchi = word.get('kibouchi', 'N/A')
                audio_filename = word.get('audio_filename', 'N/A')
                audio_lang = word.get('audio_pronunciation_lang', 'N/A')
                
                print(f"🔸 {french}")
                print(f"   Shimaoré: {shimaore}")
                print(f"   Kibouchi: {kibouchi}")
                print(f"   ► Fichier audio: {audio_filename}")
                print(f"   ► Langue du fichier: {audio_lang}")
                print()
        else:
            print("❌ Aucun mot nature avec audio trouvé")
        
        print()
        
        # Résumé des fichiers disponibles mais non assignés
        print("📂 FICHIERS AUDIO DISPONIBLES MAIS NON ASSIGNÉS")
        print("-" * 50)
        
        # Fichiers famille
        famille_dir = "/app/frontend/assets/audio/famille"
        assigned_famille_files = [word.get('audio_filename') for word in famille_words if word.get('audio_filename')]
        
        if os.path.exists(famille_dir):
            all_famille_files = [f for f in os.listdir(famille_dir) if f.endswith('.m4a')]
            unassigned_famille = [f for f in all_famille_files if f not in assigned_famille_files]
            
            if unassigned_famille:
                print(f"👨‍👩‍👧‍👦 Fichiers famille non assignés ({len(unassigned_famille)}):")
                for filename in sorted(unassigned_famille):
                    print(f"   - {filename}")
                print()
        
        # Fichiers nature
        nature_dir = "/app/frontend/assets/audio/nature"  
        assigned_nature_files = [word.get('audio_filename') for word in nature_words if word.get('audio_filename')]
        
        if os.path.exists(nature_dir):
            all_nature_files = [f for f in os.listdir(nature_dir) if f.endswith('.m4a')]
            unassigned_nature = [f for f in all_nature_files if f not in assigned_nature_files]
            
            if unassigned_nature:
                print(f"🌿 Fichiers nature non assignés ({len(unassigned_nature)}):")
                for filename in sorted(unassigned_nature):
                    print(f"   - {filename}")
                print()
        
        # Statistiques finales
        print("📈 STATISTIQUES FINALES")
        print("-" * 30)
        total_words_with_audio = len(famille_words) + len(nature_words)
        total_famille_files = len([f for f in os.listdir(famille_dir) if f.endswith('.m4a')]) if os.path.exists(famille_dir) else 0
        total_nature_files = len([f for f in os.listdir(nature_dir) if f.endswith('.m4a')]) if os.path.exists(nature_dir) else 0
        
        print(f"📊 Mots avec audio assigné: {total_words_with_audio}")
        print(f"📂 Fichiers audio disponibles: {total_famille_files + total_nature_files}")
        print(f"   - Famille: {total_famille_files} fichiers")
        print(f"   - Nature: {total_nature_files} fichiers")
        print()
        
        print("🎯 INSTRUCTIONS POUR VÉRIFICATION:")
        print("1. Vérifiez chaque correspondance mot français → fichier audio")
        print("2. Signalez les erreurs de mapping que vous trouvez")
        print("3. Indiquez quels fichiers non assignés correspondent à quels mots")
        print()
        
        # Fermer la connexion
        client.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    generate_audio_mapping_report()