#!/usr/bin/env python3
"""
EXTENSION DU SYSTÈME AUDIO DUAL - SECTION ADJECTIFS
==================================================
Extension du système audio dual pour inclure la catégorie "adjectifs"
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

def get_adjectifs_mappings():
    """Correspondances audio pour la section adjectifs"""
    
    # Correspondances basées sur l'analyse des fichiers audio disponibles et des traductions
    adjectifs_mappings = {
        # Correspondances directes avec les fichiers audio disponibles
        "ancien": ("Halé.m4a", "Kèyi.m4a"),
        "bête": ("Dhaba.m4a", "Dhaba.m4a"),  # Même fichier
        "calme": ("Baridi.m4a", "Malémi.m4a"),
        "chaud": ("Moro.m4a", "Mèyi.m4a"),
        "content": ("Oujiviwa.m4a", "Ravou.m4a"),
        "court": ("Koutri.m4a", "Fohiki.m4a"),
        "difficile": ("Ndziro.m4a", "Mahéri.m4a"),
        "drôle": ("Outsésa.m4a", "Mampimohi.m4a"),
        "dur": ("Mangavou.m4a", "Mahéri.m4a"),
        "facile": ("Ndzangou.m4a", "Mora.m4a"),
        "fatigué": ("Ouléméwa.m4a", "Vaha.m4a"),
        "faux": ("Trambo.m4a", "Vandi.m4a"),
        "fermé": ("Oubala.m4a", "Migadra.m4a"),
        "fier": ("Oujiviwa.m4a", "Ravou.m4a"),  # Même que content
        "froid": ("Baridi.m4a", "Manintsi.m4a"),
        "grand": ("Bolé.m4a", "Bé.m4a"),
        "gros": ("Tronga.m4a", "Bé.m4a"),  # Réutiliser Bé pour grand
        "honteux": ("Ouona haya.m4a", "Mampihingnatra.m4a"),
        "important": ("Mouhimou.m4a", "Mouhimou.m4a"),  # Même fichier
        "inquiet": ("Ouna hamo.m4a", "Miyéfitri-kouchanga.m4a"),
        "inutile": ("Kassina mana.m4a", "Tsissi fotouni.m4a"),
        "jeune": ("Nrétsa.m4a", "Zaza.m4a"),
        "long": ("Drilé.m4a", "Habou.m4a"),
        "lourd": ("Ndziro.m4a", "Mavèchatra.m4a"),
        "léger": ("Ndzangou.m4a", "Mayivagna.m4a"),
        "maigre": ("Tsala.m4a", "Mahia.m4a"),
        "mou": ("Trémboivou.m4a", "Malémi.m4a"),
        "nerveux": ("Oussikitiha.m4a", "Tèhitri.m4a"),
        "nouveau": ("Piya.m4a", "Vowou.m4a"),
        "ouvert": ("Ouboua.m4a", "Mibiyangna.m4a"),
        "pauvre": ("Maskini.m4a", "Maskini.m4a"),  # Même fichier
        "petit": ("Titi.m4a", "Héli.m4a"),
        "propre": ("Trahara.m4a", "Madiou.m4a"),
        "riche": ("Tadjiri.m4a", "Tadjiri.m4a"),  # Même fichier
        "sale": ("Trotro.m4a", "Maloutou.m4a"),
        "satisfait": ("Oufourahi.m4a", "Ravou.m4a"),
        "surpris": ("Oumarouha.m4a", "Tèhitri.m4a"),
        "sérieux": ("Kassidi.m4a", "Koussoudi.m4a"),
        "triste": ("Ouna hamo.m4a", "Malahélou.m4a"),
        "vieux": ("Dhouha.m4a", "Héla.m4a"),
        "vrai": ("Kwéli.m4a", "Ankitigni.m4a"),
    }
    
    return adjectifs_mappings

def extend_dual_audio_system_adjectifs():
    """Étendre le système audio dual pour la catégorie adjectifs"""
    
    print("🔧 EXTENSION DU SYSTÈME AUDIO DUAL - SECTION ADJECTIFS")
    print("=" * 60)
    
    db = get_database()
    words_collection = db.words
    
    # Répertoire des fichiers audio
    audio_dir = "/app/frontend/assets/audio/adjectifs"
    
    if not os.path.exists(audio_dir):
        print(f"❌ Répertoire audio manquant: {audio_dir}")
        return False
    
    # Lister les fichiers audio disponibles
    available_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
    print(f"📁 Fichiers audio disponibles: {len(available_files)}")
    
    # Afficher quelques fichiers pour diagnostic
    print("📋 Échantillon de fichiers disponibles:")
    for file in sorted(available_files)[:10]:
        print(f"   - {file}")
    
    # Obtenir les correspondances
    mappings = get_adjectifs_mappings()
    print(f"🎵 Correspondances définies: {len(mappings)}")
    
    # Obtenir tous les adjectifs
    adjectifs = list(words_collection.find({"category": "adjectifs"}))
    print(f"📚 Adjectifs dans la base de données: {len(adjectifs)}")
    
    # Statistiques avant mise à jour
    adjectifs_with_audio_before = len([a for a in adjectifs if a.get('dual_audio_system')])
    print(f"📊 Adjectifs avec audio AVANT: {adjectifs_with_audio_before}/{len(adjectifs)}")
    
    # Vérifier les fichiers manquants et mettre à jour
    missing_files = []
    updated_count = 0
    new_updates = 0
    
    for adjectif in adjectifs:
        french_adj = adjectif['french']
        
        if french_adj in mappings:
            shimaore_file, kibouchi_file = mappings[french_adj]
            
            # Vérifier que les fichiers existent
            shimaore_path = os.path.join(audio_dir, shimaore_file)
            kibouchi_path = os.path.join(audio_dir, kibouchi_file)
            
            shimaore_exists = os.path.exists(shimaore_path)
            kibouchi_exists = os.path.exists(kibouchi_path)
            
            if not shimaore_exists:
                missing_files.append(f"Shimaoré: {shimaore_file} pour '{french_adj}'")
            if not kibouchi_exists:
                missing_files.append(f"Kibouchi: {kibouchi_file} pour '{french_adj}'")
            
            if shimaore_exists and kibouchi_exists:
                # Vérifier si c'est une nouvelle mise à jour
                was_updated_before = adjectif.get('dual_audio_system', False)
                
                # Mise à jour des champs audio
                update_data = {
                    "shimoare_audio_filename": shimaore_file,
                    "shimoare_has_audio": True,
                    "kibouchi_audio_filename": kibouchi_file,
                    "kibouchi_has_audio": True,
                    "dual_audio_system": True,
                    "audio_category": "adjectifs"
                }
                
                # Exécuter la mise à jour
                result = words_collection.update_one(
                    {"_id": adjectif["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    updated_count += 1
                    if not was_updated_before:
                        new_updates += 1
                        print(f"🆕 {french_adj}: {shimaore_file} + {kibouchi_file}")
                    else:
                        print(f"🔄 {french_adj}: Mis à jour")
    
    # Statistiques après mise à jour
    adjectifs_after = list(words_collection.find({"category": "adjectifs"}))
    adjectifs_with_audio_after = len([a for a in adjectifs_after if a.get('dual_audio_system')])
    
    if missing_files:
        print(f"\n⚠️  Fichiers audio manquants ({len(missing_files)}):")
        for file in missing_files[:15]:  # Limiter l'affichage
            print(f"   - {file}")
        if len(missing_files) > 15:
            print(f"   ... et {len(missing_files) - 15} autres")
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSUMÉ DE L'EXTENSION ADJECTIFS:")
    print(f"   - Adjectifs avec audio AVANT: {adjectifs_with_audio_before}/{len(adjectifs)} ({adjectifs_with_audio_before/len(adjectifs)*100:.1f}%)")
    print(f"   - Adjectifs avec audio APRÈS: {adjectifs_with_audio_after}/{len(adjectifs)} ({adjectifs_with_audio_after/len(adjectifs)*100:.1f}%)")
    print(f"   - Nouvelles intégrations: {new_updates}")
    print(f"   - Mises à jour totales: {updated_count}")
    print(f"   - Amélioration: +{adjectifs_with_audio_after - adjectifs_with_audio_before} adjectifs")
    
    return updated_count > 0

def main():
    """Fonction principale"""
    try:
        success = extend_dual_audio_system_adjectifs()
        
        if success:
            print("\n✅ Extension du système audio dual pour adjectifs terminée!")
        else:
            print("\n❌ Échec de l'extension du système audio dual pour adjectifs")
        
        return success
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)