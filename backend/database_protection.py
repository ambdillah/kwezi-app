#!/usr/bin/env python3
"""
SYSTÈME DE PROTECTION DE LA BASE DE DONNÉES AUTHENTIQUE MAYOTTE
================================================================
Ce module assure la protection systématique de la base de données
authentique contre les pertes de données lors des forks ou 
opérations destructrices.

Fonctionnalités :
- Sauvegarde automatique avant toute opération destructrice
- Vérification de l'intégrité des données
- Restauration d'urgence
- Blocage des opérations dangereuses
- Alertes en cas de tentative de suppression massive
"""

import os
import json
import datetime
from functools import wraps
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'mayotte_app')
BACKUP_DIR = '/app/backup_authentic_db'
MIN_WORDS_THRESHOLD = 500  # Seuil minimum de mots pour considérer la DB comme valide
MIN_CATEGORIES_THRESHOLD = 15  # Seuil minimum de catégories

# Créer le répertoire de sauvegarde
os.makedirs(BACKUP_DIR, exist_ok=True)

class DatabaseProtector:
    """Classe de protection de la base de données"""
    
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[DB_NAME]
        self.words_collection = self.db.words
        self.last_backup_file = None
    
    def get_database_stats(self):
        """Obtient les statistiques de la base de données"""
        total_words = self.words_collection.count_documents({})
        categories = self.words_collection.distinct("category")
        
        category_counts = {}
        for category in categories:
            count = self.words_collection.count_documents({"category": category})
            category_counts[category] = count
        
        return {
            "total_words": total_words,
            "total_categories": len(categories),
            "categories": category_counts,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    
    def is_database_healthy(self):
        """Vérifie si la base de données contient des données authentiques"""
        stats = self.get_database_stats()
        
        # Vérifications de base
        if stats["total_words"] < MIN_WORDS_THRESHOLD:
            return False, f"Nombre de mots insuffisant: {stats['total_words']} < {MIN_WORDS_THRESHOLD}"
        
        if stats["total_categories"] < MIN_CATEGORIES_THRESHOLD:
            return False, f"Nombre de catégories insuffisant: {stats['total_categories']} < {MIN_CATEGORIES_THRESHOLD}"
        
        # Vérifier la présence de catégories essentielles
        essential_categories = ['famille', 'couleurs', 'animaux', 'salutations', 'nombres', 'verbes']
        missing_categories = []
        for cat in essential_categories:
            if cat not in stats["categories"]:
                missing_categories.append(cat)
        
        if missing_categories:
            return False, f"Catégories essentielles manquantes: {missing_categories}"
        
        # Vérifier que "Au revoir" = "maeva" (signature authentique)
        au_revoir = self.words_collection.find_one({"french": {"$regex": "^au revoir$", "$options": "i"}})
        if au_revoir and au_revoir.get("kibouchi", "").lower() != "maeva":
            return False, "Traduction incorrecte pour 'Au revoir' - devrait être 'maeva'"
        
        return True, "Base de données authentique confirmée"
    
    def create_backup(self, reason="manual"):
        """Crée une sauvegarde complète de la base de données"""
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_authentic_db_{timestamp}_{reason}.json"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        
        try:
            # Exporter toutes les données
            words = list(self.words_collection.find({}))
            
            # Convertir ObjectId en string
            for word in words:
                if "_id" in word:
                    word["_id"] = str(word["_id"])
            
            # Sauvegarder avec métadonnées
            backup_data = {
                "metadata": {
                    "timestamp": timestamp,
                    "reason": reason,
                    "total_words": len(words),
                    "db_name": DB_NAME
                },
                "words": words
            }
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            self.last_backup_file = backup_path
            print(f"✅ Sauvegarde créée: {backup_path}")
            print(f"📊 {len(words)} mots sauvegardés")
            return backup_path
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return None
    
    def restore_from_backup(self, backup_path=None):
        """Restaure la base de données depuis une sauvegarde"""
        if not backup_path:
            backup_path = self.last_backup_file
        
        if not backup_path or not os.path.exists(backup_path):
            print("❌ Aucune sauvegarde disponible")
            return False
        
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            words = backup_data.get("words", [])
            if not words:
                print("❌ Sauvegarde vide")
                return False
            
            # Restaurer les données
            self.words_collection.delete_many({})
            
            # Retirer les _id pour éviter les conflits
            for word in words:
                if "_id" in word:
                    del word["_id"]
            
            self.words_collection.insert_many(words)
            
            print(f"✅ Base de données restaurée depuis: {backup_path}")
            print(f"📊 {len(words)} mots restaurés")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la restauration: {e}")
            return False
    
    def emergency_restore(self):
        """Restauration d'urgence depuis le script de restauration"""
        print("🚨 RESTAURATION D'URGENCE EN COURS...")
        try:
            import subprocess
            result = subprocess.run(
                ["python", "/app/backend/restore_542_authentic_words.py"],
                cwd="/app/backend",
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ Restauration d'urgence réussie")
                return True
            else:
                print(f"❌ Erreur lors de la restauration d'urgence: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur critique lors de la restauration d'urgence: {e}")
            return False

# Instance globale du protecteur
db_protector = DatabaseProtector()

def protect_database(operation_name="unknown"):
    """Décorateur pour protéger les opérations de base de données"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"🛡️ PROTECTION DB - Opération: {operation_name}")
            
            # Vérifier l'état de la DB avant l'opération
            is_healthy, status = db_protector.is_database_healthy()
            if not is_healthy:
                print(f"⚠️ Base de données non-authentique détectée: {status}")
                print("🔄 Tentative de restauration d'urgence...")
                if db_protector.emergency_restore():
                    print("✅ Restauration d'urgence réussie")
                else:
                    raise Exception(f"❌ CRITIQUE: Base de données corrompue et restauration échouée: {status}")
            
            # Créer une sauvegarde préventive
            backup_path = db_protector.create_backup(f"before_{operation_name}")
            if not backup_path:
                print("⚠️ Impossible de créer une sauvegarde - opération risquée")
            
            try:
                # Exécuter l'opération protégée
                result = func(*args, **kwargs)
                
                # Vérifier l'état après l'opération
                is_healthy_after, status_after = db_protector.is_database_healthy()
                if not is_healthy_after:
                    print(f"🚨 ALERTE: Opération {operation_name} a corrompu la DB: {status_after}")
                    print("🔄 Restauration automatique...")
                    if backup_path and db_protector.restore_from_backup(backup_path):
                        print("✅ Restauration automatique réussie")
                        raise Exception(f"Opération {operation_name} annulée - DB restaurée")
                    else:
                        db_protector.emergency_restore()
                        raise Exception(f"Opération {operation_name} critique - restauration d'urgence effectuée")
                
                print(f"✅ Opération {operation_name} terminée avec succès")
                return result
                
            except Exception as e:
                print(f"❌ Erreur dans l'opération {operation_name}: {e}")
                # En cas d'erreur, restaurer si possible
                if backup_path:
                    print("🔄 Restauration suite à l'erreur...")
                    db_protector.restore_from_backup(backup_path)
                raise
        
        return wrapper
    return decorator

def check_database_integrity():
    """Fonction utilitaire pour vérifier l'intégrité"""
    is_healthy, status = db_protector.is_database_healthy()
    stats = db_protector.get_database_stats()
    
    print("=" * 50)
    print("🔍 VÉRIFICATION DE L'INTÉGRITÉ DE LA BASE DE DONNÉES")
    print("=" * 50)
    print(f"Statut: {'✅ SAINE' if is_healthy else '❌ CORROMPUE'}")
    print(f"Message: {status}")
    print(f"Total mots: {stats['total_words']}")
    print(f"Total catégories: {stats['total_categories']}")
    print("Catégories:")
    for cat, count in stats['categories'].items():
        print(f"  - {cat}: {count} mots")
    print("=" * 50)
    
    return is_healthy, stats

if __name__ == "__main__":
    # Test du système de protection
    check_database_integrity()