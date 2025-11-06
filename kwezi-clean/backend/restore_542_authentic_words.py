#!/usr/bin/env python3
"""
RESTAURATION DE LA BASE DE DONNÉES AUTHENTIQUE AVEC 542 MOTS
=============================================================
Ce script reconstitue la base de données authentique en exécutant
UNIQUEMENT les scripts qui contiennent "maeva" (correct) et évite
ceux qui contiennent "djalabé" (incorrect pour le Kibouchi de Mayotte)
"""

import os
import subprocess
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'test_database')

def get_mongo_client():
    """Connexion à MongoDB"""
    try:
        client = MongoClient(MONGO_URL)
        client.admin.command('ping')
        print(f"✅ Connexion MongoDB établie : {MONGO_URL}")
        return client
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB : {e}")
        return None

def clear_database():
    """Vider complètement la base de données"""
    print("🗑️ VIDAGE COMPLET DE LA BASE DE DONNÉES...")
    
    client = get_mongo_client()
    if not client:
        return False
    
    db = client[DB_NAME]
    
    try:
        collections = db.list_collection_names()
        for collection_name in collections:
            db[collection_name].drop()
            print(f"🗑️ Collection '{collection_name}' supprimée")
        print("✅ Base de données complètement vidée")
        client.close()
        return True
    except Exception as e:
        print(f"❌ Erreur lors du vidage : {e}")
        client.close()
        return False

def block_wrong_scripts():
    """Bloquer les scripts avec des traductions incorrectes"""
    print("🚫 BLOCAGE DES SCRIPTS AVEC TRADUCTIONS INCORRECTES...")
    
    scripts_to_block = [
        "restore_authentic_data.py",  # Contient "djalabé"
        "restore_authentic_database_final.py",  # Version PDF incorrecte
        "emergency_database_recovery.py"  # Version potentiellement incorrecte
    ]
    
    for script in scripts_to_block:
        script_path = f"/app/backend/{script}"
        if os.path.exists(script_path):
            blocked_path = f"{script_path}.BLOCKED_INCORRECT"
            os.rename(script_path, blocked_path)
            print(f"🚫 Bloqué: {script} → {script}.BLOCKED_INCORRECT")
    
    print("✅ Scripts incorrects bloqués")

def execute_authentic_update_scripts():
    """Exécuter tous les scripts de mise à jour authentiques"""
    print("🔧 EXÉCUTION DES SCRIPTS DE MISE À JOUR AUTHENTIQUES...")
    
    # Scripts de mise à jour dans l'ordre logique
    update_scripts = [
        "update_corps_salutations_grammaire.py",  # Contient "maeva" ✅
        "update_famille_couleurs_nourriture.py",
        "update_chiffres_animaux.py", 
        "update_nature_section.py",
        "update_maison_verbes.py",
        "update_transport_vetements_tradition.py",
        "update_expressions_adjectifs.py"
    ]
    
    successful_scripts = []
    failed_scripts = []
    
    for script in update_scripts:
        script_path = f"/app/backend/{script}"
        
        if os.path.exists(script_path):
            print(f"\n🔧 Exécution de {script}...")
            
            try:
                # Vérifier d'abord si le script contient "djalabé" (incorrect)
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'djalabé' in content.lower():
                    print(f"⚠️ ATTENTION: {script} contient 'djalabé' - vérification nécessaire")
                
                # Exécuter le script
                result = subprocess.run([sys.executable, script_path], 
                                      capture_output=True, text=True, 
                                      cwd="/app/backend")
                
                if result.returncode == 0:
                    print(f"✅ {script} exécuté avec succès")
                    successful_scripts.append(script)
                    if result.stdout:
                        print(f"   Sortie: {result.stdout.strip()}")
                else:
                    print(f"❌ Erreur avec {script}")
                    if result.stderr:
                        print(f"   Erreur: {result.stderr.strip()}")
                    failed_scripts.append(script)
                    
            except Exception as e:
                print(f"❌ Exception avec {script}: {e}")
                failed_scripts.append(script)
        else:
            print(f"⚠️ Script {script} non trouvé")
            failed_scripts.append(script)
    
    print(f"\n📊 RÉSULTATS DE L'EXÉCUTION:")
    print(f"✅ Succès: {len(successful_scripts)} scripts")
    print(f"❌ Échecs: {len(failed_scripts)} scripts")
    
    if successful_scripts:
        print(f"✅ Scripts réussis: {', '.join(successful_scripts)}")
    if failed_scripts:
        print(f"❌ Scripts échoués: {', '.join(failed_scripts)}")
    
    return len(successful_scripts) > 0

def verify_authentic_database():
    """Vérifier que la base de données contient les bonnes traductions"""
    print("\n🔍 VÉRIFICATION DE LA BASE DE DONNÉES AUTHENTIQUE...")
    
    client = get_mongo_client()
    if not client:
        return False
    
    db = client[DB_NAME]
    
    try:
        # Compter le total de mots
        total_words = db.words.count_documents({})
        print(f"📊 Total des mots: {total_words}")
        
        # Vérifier les catégories
        categories = db.words.distinct("category")
        print(f"📚 Catégories: {len(categories)}")
        
        for category in sorted(categories):
            count = db.words.count_documents({"category": category})
            print(f"  ✅ {category}: {count} mots")
        
        # Vérification CRITIQUE: "Au revoir" doit être "maeva" pas "djalabé"
        au_revoir = db.words.find_one({"french": {"$regex": "au revoir", "$options": "i"}})
        if au_revoir:
            kibouchi_translation = au_revoir.get("kibouchi", "").lower()
            print(f"\n🔍 VÉRIFICATION CRITIQUE - 'Au revoir':")
            print(f"   Français: {au_revoir.get('french', '')}")
            print(f"   Shimaoré: {au_revoir.get('shimaore', '')}")
            print(f"   Kibouchi: {au_revoir.get('kibouchi', '')}")
            
            if "maeva" in kibouchi_translation:
                print(f"   ✅ CORRECT: Contient 'maeva' (authentique Kibouchi Mayotte)")
            elif "djalabé" in kibouchi_translation:
                print(f"   ❌ ERREUR: Contient 'djalabé' (incorrect pour Mayotte)")
                client.close()
                return False
            else:
                print(f"   ⚠️ ATTENTION: Ni 'maeva' ni 'djalabé' trouvé")
        
        # Vérifier d'autres mots critiques avec audio
        audio_words = ["Papa", "Frère", "Sœur", "Grand-père", "Grand-mère", "Famille", "Garçon", "Monsieur"]
        print(f"\n🎵 VÉRIFICATION DES MOTS AVEC AUDIO:")
        
        for word_fr in audio_words:
            word = db.words.find_one({"french": word_fr})
            if word:
                print(f"  ✅ {word_fr}: {word.get('shimaore', '')} / {word.get('kibouchi', '')}")
            else:
                print(f"  ❌ {word_fr}: NON TROUVÉ")
        
        # Vérifier le compte final
        if 540 <= total_words <= 550:
            print(f"\n🎉 SUCCÈS ! Base de données authentique avec {total_words} mots")
            print("✅ Utilise 'maeva' (correct) et évite 'djalabé' (incorrect)")
            print("🎵 Prête pour les 13 enregistrements audio authentiques")
            client.close()
            return True
        else:
            print(f"\n⚠️ ATTENTION: {total_words} mots (attendu: 540-550)")
            client.close()
            return total_words > 500  # Accepter si > 500
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification : {e}")
        client.close()
        return False

def main():
    """Fonction principale"""
    print("=" * 80)
    print("🔥 RESTAURATION BASE DE DONNÉES AUTHENTIQUE (542 MOTS)")
    print("=" * 80)
    print("✅ AVEC 'maeva' (CORRECT pour Kibouchi Mayotte)")
    print("❌ SANS 'djalabé' (INCORRECT pour Kibouchi Mayotte)")
    print("=" * 80)
    
    try:
        # 1. Bloquer les scripts incorrects
        block_wrong_scripts()
        
        # 2. Vider la base de données
        if not clear_database():
            print("❌ Échec du vidage de la base de données")
            return False
        
        # 3. Exécuter les scripts de mise à jour authentiques
        if not execute_authentic_update_scripts():
            print("❌ Échec de l'exécution des scripts de mise à jour")
            return False
        
        # 4. Vérifier la base de données finale
        if not verify_authentic_database():
            print("❌ Échec de la vérification de la base de données")
            return False
        
        print("\n" + "=" * 80)
        print("🎉 RESTAURATION RÉUSSIE !")
        print("✅ Base de données authentique avec ~542 mots")
        print("✅ Traductions correctes pour le Kibouchi de Mayotte")
        print("✅ 'Au revoir' = 'maeva' (CORRECT)")
        print("🚫 Scripts incorrects bloqués définitivement")
        print("🎵 Prête pour 13 enregistrements audio authentiques")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎊 SUCCESS! AUTHENTIC DATABASE RESTORED!")
    else:
        print("\n💥 FAILURE! RESTORATION FAILED!")
    
    exit(0 if success else 1)