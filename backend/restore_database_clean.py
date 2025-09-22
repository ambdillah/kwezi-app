#!/usr/bin/env python3
"""
Script pour restaurer la base de données depuis une sauvegarde propre
et corriger le problème de duplication (2872 → 548 mots)
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# Ajouter le chemin du backend au PYTHONPATH
sys.path.append('/app/backend')

# Charger les variables d'environnement
load_dotenv()

def restore_clean_database():
    """Restaure la base de données depuis la sauvegarde propre de 548 mots."""
    
    # Chemin vers la sauvegarde propre
    backup_path = "/app/backup_authentic_db/backup_authentic_db_20250922_083649_before_update_nombres_section.json"
    
    try:
        # Connexion à MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.words
        
        print(f"🔗 Connexion à MongoDB: {mongo_url}")
        print(f"📊 Base de données: {db_name}")
        print(f"📝 Collection: words")
        print()
        
        # Vérifier l'état actuel
        current_count = collection.count_documents({})
        print(f"📊 État actuel: {current_count} mots dans la base")
        
        # Charger la sauvegarde
        print(f"📂 Chargement de la sauvegarde: {backup_path}")
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        # Vérifier les métadonnées
        metadata = backup_data.get('metadata', {})
        backup_word_count = metadata.get('total_words', 0)
        words = backup_data.get('words', [])
        
        print(f"📋 Métadonnées de la sauvegarde:")
        print(f"   - Timestamp: {metadata.get('timestamp', 'N/A')}")
        print(f"   - Raison: {metadata.get('reason', 'N/A')}")
        print(f"   - Nombre de mots: {backup_word_count}")
        print(f"   - Base de données: {metadata.get('db_name', 'N/A')}")
        print()
        
        if backup_word_count != 548:
            print(f"⚠️ Attention: La sauvegarde contient {backup_word_count} mots au lieu de 548")
            input("Appuyez sur Entrée pour continuer ou Ctrl+C pour annuler...")
        
        # Créer une sauvegarde de l'état actuel corrompu
        print("💾 Création d'une sauvegarde de l'état corrompu actuel...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        corrupted_backup_path = f"/app/backup_authentic_db/backup_corrupted_state_{timestamp}.json"
        
        corrupted_words = list(collection.find({}))
        for word in corrupted_words:
            if "_id" in word:
                word["_id"] = str(word["_id"])
        
        corrupted_backup = {
            "metadata": {
                "timestamp": timestamp,
                "reason": "corrupted_state_before_cleanup",
                "total_words": len(corrupted_words),
                "db_name": db_name
            },
            "words": corrupted_words
        }
        
        with open(corrupted_backup_path, 'w', encoding='utf-8') as f:
            json.dump(corrupted_backup, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Sauvegarde corrompue créée: {corrupted_backup_path}")
        print()
        
        # Vider la collection actuelle
        print("🗑️ Suppression de tous les mots corrompus...")
        result = collection.delete_many({})
        print(f"✅ {result.deleted_count} mots supprimés")
        print()
        
        # Restaurer les mots authentiques
        print("📥 Restauration des mots authentiques...")
        
        # Convertir les données pour insertion
        words_to_insert = []
        for word in words:
            # Supprimer l'_id string pour laisser MongoDB générer un nouvel ObjectId
            if "_id" in word:
                del word["_id"]
            
            # Convertir les timestamps
            if "created_at" in word and isinstance(word["created_at"], str):
                try:
                    word["created_at"] = datetime.fromisoformat(word["created_at"].replace('Z', '+00:00'))
                except:
                    word["created_at"] = datetime.now()
            
            words_to_insert.append(word)
        
        # Insérer par lots
        if words_to_insert:
            result = collection.insert_many(words_to_insert)
            print(f"✅ {len(result.inserted_ids)} mots authentiques restaurés")
        
        # Vérifier l'état final
        final_count = collection.count_documents({})
        print()
        print(f"📊 État final: {final_count} mots dans la base")
        
        # Vérifier quelques échantillons
        print("🔍 Vérification d'échantillons:")
        sample_words = list(collection.find({}).limit(3))
        for word in sample_words:
            french = word.get('french', 'N/A')
            shimaore = word.get('shimaore', 'N/A')
            kibouchi = word.get('kibouchi', 'N/A')
            category = word.get('category', 'N/A')
            print(f"   - {french}: shimaoré='{shimaore}', kibouchi='{kibouchi}', catégorie='{category}'")
        
        print()
        print("✅ Restauration de la base de données terminée avec succès!")
        print(f"📈 Résultat: {current_count} → {final_count} mots")
        
        # Fermer la connexion
        client.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la restauration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Début de la restauration de la base de données...")
    print("🎯 Objectif: Corriger le problème de duplication (2872 → 548 mots)")
    print()
    
    success = restore_clean_database()
    
    if success:
        print("🎉 Restauration terminée avec succès!")
        print("➡️ Prochaine étape: Relancer l'ajout des 8 nombres")
    else:
        print("💥 Échec de la restauration")
        sys.exit(1)