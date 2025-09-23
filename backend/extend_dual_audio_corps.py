#!/usr/bin/env python3
"""
EXTENSION DU SYSTÈME AUDIO DUAL - SECTION CORPS HUMAIN
====================================================
Extension du système audio dual pour inclure la catégorie "corps"
avec les fichiers audio authentiques fournis par l'utilisateur.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def get_database():
    """Connexion à la base de données MongoDB"""
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    client = MongoClient(mongo_url)
    db_name = os.getenv('DB_NAME', 'mayotte_app')
    db = client[db_name]
    return db

def extend_dual_audio_system_corps():
    """Étendre le système audio dual pour la catégorie corps"""
    
    print("🔧 EXTENSION DU SYSTÈME AUDIO DUAL - SECTION CORPS")
    print("=" * 60)
    
    db = get_database()
    words_collection = db.words
    
    # Répertoire des fichiers audio corps
    audio_dir = "/app/frontend/assets/audio/corps"
    
    if not os.path.exists(audio_dir):
        print(f"❌ Répertoire audio manquant: {audio_dir}")
        return False
    
    # Lister les fichiers audio disponibles
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
    print(f"📁 Fichiers audio trouvés: {len(audio_files)}")
    
    # Correspondances audio pour la section corps
    audio_mappings = {
        # Format: (french_word, shimaore_audio, kibouchi_audio)
        "arrière du crâne": ("Komoi.m4a", "Kitoika.m4a"),
        "barbe": ("Ndrévou.m4a", "Somboutrou.m4a"),
        "bouche": ("Hangno.m4a", "Vava.m4a"),
        "cheveux": ("Ngnélé.m4a", "Fagnéva.m4a"),
        "cheville": ("Dzitso la pwédza.m4a", "Dzitso la pwédza.m4a"),
        "cils": ("Kové.m4a", "Rambou faninti.m4a"),
        "cou": ("Tsingo.m4a", "Vouzougnou.m4a"),
        "côtes": ("Bavou.m4a", "Mbavou.m4a"),
        "dent": ("Magno.m4a", "Hifi.m4a"),
        "doigts": ("Cha.m4a", "Tondrou.m4a"),
        "dos": ("Mengo.m4a", "Vohou.m4a"),
        "fesses": ("Shidzé-mvoumo.m4a", "Fouri.m4a"),
        "front": ("Housso.m4a", "Lahara.m4a"),
        "hanche": ("Trenga.m4a", "Tahezagna.m4a"),
        "joue": ("Savou.m4a", "Fifi.m4a"),
        "langue": ("Oulimé.m4a", "Lèla.m4a"),
        "lèvre": ("Dhomo.m4a", "Soungni.m4a"),
        "main": ("Mhono.m4a", "Tagnana.m4a"),
        "menton": ("Shlévou.m4a", "Sokou.m4a"),
        "nez": ("Poua.m4a", "Horougnou.m4a"),
        "ongle": ("Kofou.m4a", "Angofou.m4a"),
        "oreille": ("Kiyo.m4a", "Soufigni.m4a"),
        "peau": ("Ngwezi.m4a", "Ngwezi.m4a"),
        "pied": ("Mindrou.m4a", "Viti.m4a"),
        "pénis": ("Mbo.m4a", "Kaboudzi.m4a"),
        "sourcil": ("Matso.m4a", "Ankwéssi.m4a"),  # Note: tsi->matso correction
        "testicules": ("Kwendzé.m4a", "Vouancarou.m4a"),  # Note: vouangarou->vouancarou
        "tête": ("Shitsoi.m4a", "Louha.m4a"),
        "vagin": ("Ndzigni.m4a", "Tingui.m4a"),
        "ventre": ("Mimba.m4a", "Kibou.m4a"),
        "épaule": ("Bèga.m4a", "Haveyi.m4a"),
        "œil": ("Matso.m4a", "Faninti.m4a"),
    }
    
    # Vérifier que tous les fichiers audio existent
    missing_files = []
    for french_word, (shimaore_file, kibouchi_file) in audio_mappings.items():
        shimaore_path = os.path.join(audio_dir, shimaore_file)
        kibouchi_path = os.path.join(audio_dir, kibouchi_file)
        
        if not os.path.exists(shimaore_path):
            missing_files.append(f"Shimaoré: {shimaore_file} pour '{french_word}'")
        if not os.path.exists(kibouchi_path):
            missing_files.append(f"Kibouchi: {kibouchi_file} pour '{french_word}'")
    
    if missing_files:
        print("❌ Fichiers audio manquants:")
        for file in missing_files:
            print(f"   - {file}")
        print("📁 Fichiers disponibles:")
        for file in sorted(audio_files):
            print(f"   - {file}")
        return False
    
    # Obtenir tous les mots de la catégorie "corps"
    corps_words = list(words_collection.find({"category": "corps"}))
    print(f"📚 Mots trouvés dans la catégorie corps: {len(corps_words)}")
    
    # Mettre à jour les mots avec les informations audio
    updated_count = 0
    
    for word in corps_words:
        french_word = word['french']
        
        if french_word in audio_mappings:
            shimaore_file, kibouchi_file = audio_mappings[french_word]
            
            # Mise à jour des champs audio
            update_data = {
                "shimoare_audio_filename": shimaore_file,
                "shimoare_has_audio": True,
                "kibouchi_audio_filename": kibouchi_file,
                "kibouchi_has_audio": True,
                "dual_audio_system": True,
                "audio_category": "corps"
            }
            
            # Exécuter la mise à jour
            result = words_collection.update_one(
                {"_id": word["_id"]},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"✅ {french_word}: {shimaore_file} (Shimaoré) + {kibouchi_file} (Kibouchi)")
        else:
            print(f"⚠️  Aucun audio trouvé pour: {french_word}")
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSUMÉ DE L'EXTENSION CORPS:")
    print(f"   - Mots mis à jour: {updated_count}/{len(corps_words)}")
    print(f"   - Fichiers audio utilisés: {len(audio_mappings)} paires")
    print(f"   - Couverture: {(updated_count/len(corps_words)*100):.1f}%")
    
    return updated_count > 0

def main():
    """Fonction principale"""
    try:
        success = extend_dual_audio_system_corps()
        
        if success:
            print("\n✅ Extension du système audio dual pour 'corps' terminée avec succès!")
        else:
            print("\n❌ Échec de l'extension du système audio dual pour 'corps'")
        
        return success
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)