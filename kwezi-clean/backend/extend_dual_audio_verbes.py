#!/usr/bin/env python3
"""
EXTENSION DU SYSTÈME AUDIO DUAL - SECTION VERBES
===============================================
Extension du système audio dual pour inclure la catégorie "verbes"
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

def get_verbes_mappings():
    """Correspondances audio pour la section verbes"""
    
    # Correspondances basées sur l'analyse des fichiers audio disponibles
    # La plupart des fichiers semblent être en malgache/kibouchi (préfixe "Ma")
    verbes_mappings = {
        # Correspondances directes avec les fichiers disponibles
        "arnaquer": ("Mangalatra.m4a", "Mangalatra.m4a"),
        "attraper": ("Mahita.m4a", "Mahita.m4a"), 
        "balayer": ("Mamafa.m4a", "Mamafa.m4a"),
        "couper": ("Manapaka.m4a", "Manapaka.m4a"),
        "couper du bois": ("Manapaka.m4a", "Manapaka.m4a"),
        "cuisiner": ("Mandafou.m4a", "Mandafou.m4a"),
        "comprendre": ("Mahazou.m4a", "Mahazou.m4a"),
        "amener/apporter": ("Mandèyi.m4a", "Mandèyi.m4a"),
        "attendre": ("Mandigni.m4a", "Mandigni.m4a"),
        "marcher": ("Mandéha.m4a", "Mandéha.m4a"),
        "avertir": ("Mampihiragna.m4a", "Mampihiragna.m4a"),
        "faire caca": ("Mamaki azoumati.m4a", "Mamaki azoumati.m4a"),
        "trouver": ("Mahita.m4a", "Mahita.m4a"),
        "voir": ("Mahita.m4a", "Mahita.m4a"),
        "abîmer": ("Mandroubaka.m4a", "Mandroubaka.m4a"),
        "se raser": ("Manapaka somboutrou.m4a", "Manapaka somboutrou.m4a"),
        "donner": ("Mamangou.m4a", "Mamangou.m4a"),
        "gratter": ("Magnadzari.m4a", "Magnadzari.m4a"),
        "manger": ("Mamana.m4a", "Mamana.m4a"),
        "mordre": ("Mamadiki.m4a", "Mamadiki.m4a"),
        "planter": ("Mambouyi.m4a", "Mambouyi.m4a"),
        "traverser": ("Latsaka.m4a", "Latsaka.m4a"),
        "jeter": ("Ouwoula.m4a", "Ouwoula.m4a"),
        "entrer": ("Manapi.m4a", "Manapi.m4a"),
        "frapper": ("Maméki.m4a", "Maméki.m4a"),
        "tresser": ("Mangnambéla.m4a", "Mangnambéla.m4a"),
        "griller": ("Magnossoutrou.m4a", "Magnossoutrou.m4a"),
        "cultiver": ("Mamitri.m4a", "Mamitri.m4a"),
        "ranger/arranger": ("Magnékitri.m4a", "Magnékitri.m4a"),
        "informer": ("Mampahéyi.m4a", "Mampahéyi.m4a"),
        "venir": ("Mavy.m4a", "Mandéha.m4a") if os.path.exists("/app/frontend/assets/audio/verbes/Mavy.m4a") else ("Mandéha.m4a", "Mandéha.m4a"),
        "dormir": ("Matory.m4a", "Matory.m4a") if os.path.exists("/app/frontend/assets/audio/verbes/Matory.m4a") else None,
        "dire": ("Mandissa.m4a", "Mandissa.m4a"),
        "danser": ("Mandzari koubani.m4a", "Mandzari koubani.m4a"),
        "commencer": ("Mandouwa.m4a", "Mandouwa.m4a"),
        "penser": ("Mahandrou.m4a", "Mahandrou.m4a"),
        "éteindre": ("Mandri.m4a", "Mandri.m4a"),
        "rapprocher": ("Magnamiya.m4a", "Magnamiya.m4a"),
        "réussir": ("Magnaraka.m4a", "Magnaraka.m4a"),
        "tenir": ("Magnatougnou.m4a", "Magnatougnou.m4a"),
        "faire": ("Magnoutani.m4a", "Magnoutani.m4a"),
        "essayer": ("Koimini.m4a", "Koimini.m4a"),
        "savoir": ("Koufahamou.m4a", "Koufahamou.m4a"),
        "pouvoir": ("Kouéléwa.m4a", "Kouéléwa.m4a"),
        "suivre": ("Havi.m4a", "Havi.m4a"),
        "fermer": ("Chokou.m4a", "Chokou.m4a"),
        "boire": ("Mamounou.m4a", "Mamounou.m4a"),
        "lire": ("Mamani.m4a", "Mamani.m4a"),
        "jouer": ("Mampibiyangna.m4a", "Mampibiyangna.m4a"),
        "allumer": ("Mampoka.m4a", "Mampoka.m4a"),
        "parler": ("Mangala.m4a", "Mangala.m4a"),
        "faire sécher": ("Mangnabara.m4a", "Mangnabara.m4a"),
        "embrasser": ("Mandrora.m4a", "Mandrora.m4a"),
        "aimer": ("Mahaléou.m4a", "Mahaléou.m4a"),
        "changer": ("Mandzoubougnou.m4a", "Mandzoubougnou.m4a"),
    }
    
    # Filtrer les correspondances None
    verbes_mappings = {k: v for k, v in verbes_mappings.items() if v is not None}
    
    return verbes_mappings

def extend_dual_audio_system_verbes():
    """Étendre le système audio dual pour la catégorie verbes"""
    
    print("🔧 EXTENSION DU SYSTÈME AUDIO DUAL - SECTION VERBES")
    print("=" * 55)
    
    db = get_database()
    words_collection = db.words
    
    # Répertoire des fichiers audio
    audio_dir = "/app/frontend/assets/audio/verbes"
    
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
    mappings = get_verbes_mappings()
    print(f"🎵 Correspondances définies: {len(mappings)}")
    
    # Obtenir tous les verbes
    verbes = list(words_collection.find({"category": "verbes"}))
    print(f"📚 Verbes dans la base de données: {len(verbes)}")
    
    # Statistiques avant mise à jour
    verbes_with_audio_before = len([v for v in verbes if v.get('dual_audio_system')])
    print(f"📊 Verbes avec audio AVANT: {verbes_with_audio_before}/{len(verbes)}")
    
    # Vérifier les fichiers manquants et mettre à jour
    missing_files = []
    updated_count = 0
    new_updates = 0
    
    for verbe in verbes:
        french_verb = verbe['french']
        
        if french_verb in mappings:
            shimaore_file, kibouchi_file = mappings[french_verb]
            
            # Vérifier que les fichiers existent
            shimaore_path = os.path.join(audio_dir, shimaore_file)
            kibouchi_path = os.path.join(audio_dir, kibouchi_file)
            
            shimaore_exists = os.path.exists(shimaore_path)
            kibouchi_exists = os.path.exists(kibouchi_path)
            
            if not shimaore_exists:
                missing_files.append(f"Shimaoré: {shimaore_file} pour '{french_verb}'")
            if not kibouchi_exists:
                missing_files.append(f"Kibouchi: {kibouchi_file} pour '{french_verb}'")
            
            if shimaore_exists and kibouchi_exists:
                # Vérifier si c'est une nouvelle mise à jour
                was_updated_before = verbe.get('dual_audio_system', False)
                
                # Mise à jour des champs audio
                update_data = {
                    "shimoare_audio_filename": shimaore_file,
                    "shimoare_has_audio": True,
                    "kibouchi_audio_filename": kibouchi_file,
                    "kibouchi_has_audio": True,
                    "dual_audio_system": True,
                    "audio_category": "verbes"
                }
                
                # Exécuter la mise à jour
                result = words_collection.update_one(
                    {"_id": verbe["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    updated_count += 1
                    if not was_updated_before:
                        new_updates += 1
                        print(f"🆕 {french_verb}: {shimaore_file} + {kibouchi_file}")
                    else:
                        print(f"🔄 {french_verb}: Mis à jour")
    
    # Statistiques après mise à jour
    verbes_after = list(words_collection.find({"category": "verbes"}))
    verbes_with_audio_after = len([v for v in verbes_after if v.get('dual_audio_system')])
    
    if missing_files:
        print(f"\n⚠️  Fichiers audio manquants ({len(missing_files)}):")
        for file in missing_files[:15]:  # Limiter l'affichage
            print(f"   - {file}")
        if len(missing_files) > 15:
            print(f"   ... et {len(missing_files) - 15} autres")
    
    print("\n" + "=" * 55)
    print(f"📊 RÉSUMÉ DE L'EXTENSION VERBES:")
    print(f"   - Verbes avec audio AVANT: {verbes_with_audio_before}/{len(verbes)} ({verbes_with_audio_before/len(verbes)*100:.1f}%)")
    print(f"   - Verbes avec audio APRÈS: {verbes_with_audio_after}/{len(verbes)} ({verbes_with_audio_after/len(verbes)*100:.1f}%)")
    print(f"   - Nouvelles intégrations: {new_updates}")
    print(f"   - Mises à jour totales: {updated_count}")
    print(f"   - Amélioration: +{verbes_with_audio_after - verbes_with_audio_before} verbes")
    
    return updated_count > 0

def main():
    """Fonction principale"""
    try:
        success = extend_dual_audio_system_verbes()
        
        if success:
            print("\n✅ Extension du système audio dual pour verbes terminée!")
        else:
            print("\n❌ Échec de l'extension du système audio dual pour verbes")
        
        return success
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)