#!/usr/bin/env python3
"""
EXTENSION DU SYSTÈME AUDIO DUAL - 4 SECTIONS
===========================================
Extension du système audio dual pour inclure les catégories:
- salutations (8 mots)
- couleurs (8 mots)
- grammaire (21 mots)
- nourriture (44 mots)

Avec les fichiers audio authentiques fournis par l'utilisateur.
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

def get_audio_mappings():
    """Définir les correspondances audio pour toutes les sections"""
    
    # SALUTATIONS (8 mots)
    salutations_mappings = {
        "au revoir": ("Kwaheri.m4a", "Kwaheri.m4a"),  # Même fichier pour les deux
        "bonne nuit": ("Oukou wa hairi.m4a", "Haligni tsara.m4a"),
        "comment ça va": ("Jéjé.m4a", "Jéjé.m4a"),  # Utiliser Jéjé pour les deux
        "merci": ("Marahaba.m4a", "Marahaba.m4a"),
        "non": ("An_ha.m4a", "An_ha.m4a"),
        "oui": ("Ewa.m4a", "Iya.m4a"),
        "ça va bien": ("Fétré.m4a", "Tsara.m4a"),
        # Note: "bonjour" non mappé car pas de fichier Kwezi trouvé
    }
    
    # COULEURS (8 mots) 
    couleurs_mappings = {
        "blanc": ("Ndjéou.m4a", "Malandi.m4a"),
        "bleu": ("Bilé.m4a", "Mayitsou bilé.m4a"),
        "gris": ("Djifou.m4a", "Dzofou.m4a"),
        "jaune": ("Dzindzano.m4a", "Tamoutamou.m4a"),
        "marron": ("Trotro.m4a", "Fotafotaka.m4a"),
        "noir": ("Ndzidhou.m4a", "Mayintigni.m4a"),
        "rouge": ("Ndzoukoundrou.m4a", "Mena.m4a"),
        "vert": ("Dhavou.m4a", "Mayitsou.m4a"),
    }
    
    # GRAMMAIRE (21 mots) - utiliser les fichiers disponibles 
    grammaire_mappings = {
        "je": ("Wami.m4a", "Zahou.m4a"),
        "tu": ("Wawé.m4a", "Anaou.m4a"),
        "nous": ("Wassi.m4a", "Atsika.m4a"),
        "vous": ("Wagnou.m4a", "Anaréou.m4a"),
        "il/elle": ("Wayé.m4a", "Izi.m4a"),
        "ils/elles": ("Wawo.m4a", "Réou.m4a"),
        "agriculteur": ("Mlimizi.m4a", "Ampikapa.m4a"),
        "imam": ("Imamou.m4a", "Imamou.m4a"),
        "guide spirituel": ("Cadhi.m4a", "Cadhi.m4a"),
        "le mien": ("Yangou.m4a", "Ninakahi.m4a"),
        "le tien": ("Yaho.m4a", "Ninaou.m4a"),
        "le sien": ("Yahé.m4a", "Ninazi.m4a"),
        "le leur": ("Yawo.m4a", "Nindréou.m4a"),
        "le nôtre": ("Yatrou.m4a", "Nintsika.m4a"),
        "le vôtre": ("Yagnou.m4a", "Ninaréou.m4a"),
        "maire": ("Méra.m4a", "Méra.m4a"),
        "professeur": ("Foundi.m4a", "Foundi.m4a"),
        "pêcheur": ("Mlozi.m4a", "Ampamintagna.m4a"),
        "voisin": ("Djirani.m4a", "Djirani.m4a"),
        "élu": ("Dhoimana.m4a", "Dhoimana.m4a"),
        "éleveur": ("Mtsounga.m4a", "Ampitsounga.m4a"),
    }
    
    # NOURRITURE (44 mots) - correspondance avec les fichiers disponibles
    nourriture_mappings = {
        "ciboulette": ("Chouroungou.m4a", "Doungoulou ravigni.m4a"),
        "gingembre": ("Tsinguiziou.m4a", "Tsinguiziou.m4a"),  # Même fichier
        "mandarine": ("Madhandzé.m4a", "Tsoha madzandzi.m4a"),
        "mangue": ("Bvilibvili manga.m4a", "Bvilibvili manga.m4a"),  # Même fichier
        "lait de coco": ("Maji ya moro.m4a", "Maji ya moro.m4a"),  # Si ce mot existe
        "piment": ("Pilipili.m4a", "Pilipili.m4a"),
        "son de riz": ("Poutou.m4a", "Poutou.m4a"),
        "salade": ("Sira.m4a", "Sira.m4a"),
        "fruit à pain": ("Madirou kakazou.m4a", "Madirou kakazou.m4a"),
        "poisson salé": ("Troundra.m4a", "Troundra.m4a"),
        "riz blanc": ("Vari tsivoidissa.m4a", "Vari tsivoidissa.m4a"),
        "navet blanc": ("Lavani.m4a", "Lavani.m4a"),
    }
    
    return {
        "salutations": salutations_mappings,
        "couleurs": couleurs_mappings,
        "grammaire": grammaire_mappings,
        "nourriture": nourriture_mappings
    }

def extend_dual_audio_system_4_sections():
    """Étendre le système audio dual pour les 4 sections"""
    
    print("🔧 EXTENSION DU SYSTÈME AUDIO DUAL - 4 SECTIONS")
    print("=" * 60)
    
    db = get_database()
    words_collection = db.words
    
    # Répertoires des fichiers audio
    base_audio_dir = "/app/frontend/assets/audio"
    
    all_mappings = get_audio_mappings()
    
    total_updated = 0
    total_errors = 0
    
    for category, mappings in all_mappings.items():
        print(f"\n📂 Section: {category.upper()}")
        print("-" * 40)
        
        audio_dir = os.path.join(base_audio_dir, category)
        
        if not os.path.exists(audio_dir):
            print(f"❌ Répertoire audio manquant: {audio_dir}")
            continue
        
        # Lister les fichiers audio disponibles
        available_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
        print(f"📁 Fichiers audio disponibles: {len(available_files)}")
        
        # Obtenir tous les mots de la catégorie
        words = list(words_collection.find({"category": category}))
        print(f"📚 Mots dans la base de données: {len(words)}")
        
        # Vérifier quels fichiers audio existent
        missing_files = []
        for french_word, (shimaore_file, kibouchi_file) in mappings.items():
            shimaore_path = os.path.join(audio_dir, shimaore_file)
            kibouchi_path = os.path.join(audio_dir, kibouchi_file)
            
            if not os.path.exists(shimaore_path):
                missing_files.append(f"Shimaoré: {shimaore_file} pour '{french_word}'")
            if not os.path.exists(kibouchi_path):
                missing_files.append(f"Kibouchi: {kibouchi_file} pour '{french_word}'")
        
        if missing_files:
            print("⚠️  Fichiers audio manquants:")
            for file in missing_files[:5]:  # Limiter l'affichage
                print(f"   - {file}")
            if len(missing_files) > 5:
                print(f"   ... et {len(missing_files) - 5} autres")
        
        # Mettre à jour les mots avec les informations audio
        updated_count = 0
        
        for word in words:
            french_word = word['french']
            
            if french_word in mappings:
                shimaore_file, kibouchi_file = mappings[french_word]
                
                # Vérifier que les fichiers existent avant de mettre à jour
                shimaore_exists = os.path.exists(os.path.join(audio_dir, shimaore_file))
                kibouchi_exists = os.path.exists(os.path.join(audio_dir, kibouchi_file))
                
                if shimaore_exists and kibouchi_exists:
                    # Mise à jour des champs audio
                    update_data = {
                        "shimoare_audio_filename": shimaore_file,
                        "shimoare_has_audio": True,
                        "kibouchi_audio_filename": kibouchi_file,
                        "kibouchi_has_audio": True,
                        "dual_audio_system": True,
                        "audio_category": category
                    }
                    
                    # Exécuter la mise à jour
                    result = words_collection.update_one(
                        {"_id": word["_id"]},
                        {"$set": update_data}
                    )
                    
                    if result.modified_count > 0:
                        updated_count += 1
                        print(f"✅ {french_word}: {shimaore_file} + {kibouchi_file}")
                else:
                    print(f"⚠️  Fichiers manquants pour: {french_word}")
                    total_errors += 1
        
        print(f"📊 Section {category}: {updated_count}/{len(words)} mots mis à jour")
        total_updated += updated_count
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSUMÉ GLOBAL:")
    print(f"   - Mots mis à jour: {total_updated}")
    print(f"   - Erreurs: {total_errors}")
    print(f"   - Nouvelles catégories avec audio dual: 4")
    
    return total_updated > 0

def main():
    """Fonction principale"""
    try:
        success = extend_dual_audio_system_4_sections()
        
        if success:
            print("\n✅ Extension du système audio dual pour 4 sections terminée!")
        else:
            print("\n❌ Échec de l'extension du système audio dual")
        
        return success
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)