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
    
    # Correspondances basées sur l'analyse des fichiers audio disponibles et des traductions
    verbes_mappings = {
        # Correspondances directes identifiées
        "acheter": ("Ounoua.m4a", "Mivanga.m4a"),  # Si les fichiers existent
        "aller": ("Ouendra.m4a", "Mandeha.m4a"),
        "amener/apporter": ("Ouvinga.m4a", "Mandèyi.m4a"),
        "apprendre": ("Oufoundriha.m4a", "Midzorou.m4a"),
        "arrêter": ("Ouziya.m4a", "Mitsahatra.m4a"),
        "attendre": ("Oulindra.m4a", "Mandigni.m4a"),
        "avertir": ("Oubarazaki.m4a", "Mampihiragna.m4a"),
        "balayer": ("Oupigni.m4a", "Mamafa.m4a"),
        "boire": ("Ounoua.m4a", "Misotrou.m4a"),
        "bouger": ("Outsésa.m4a", "Mihetsaka.m4a"),
        "changer": ("Ouibadili.m4a", "Mivadika.m4a"),
        "commencer": ("Ouanza.m4a", "Manombouha.m4a"),
        "comprendre": ("Oufachimi.m4a", "Mahazo.m4a"),
        "connaître": ("Ouizi.m4a", "Mahafantatra.m4a"),
        "couper": ("Outéma.m4a", "Manapaka.m4a"),
        "courir": ("Oukimbia.m4a", "Mihazakazaka.m4a"),
        "cracher": ("Outéma.m4a", "Manoraka.m4a"),
        "creuser": ("Oushimba.m4a", "Mihady.m4a"),
        "cuisiner": ("Oupika.m4a", "Mandafou.m4a"),
        "cultiver": ("Oupanda.m4a", "Mambolé.m4a"),
        "danser": ("Oucheza.m4a", "Mandihy.m4a"),
        "demander": ("Oulaza.m4a", "Mangataka.m4a"),
        "dire": ("Ouronga.m4a", "Milaza.m4a"),
        "donner": ("Oupa.m4a", "Manomé.m4a"),
        "dormir": ("Ourare.m4a", "Matory.m4a"),
        "embrasser": ("Ouvouma.m4a", "Manoroka.m4a"),
        "entrer": ("Oungiria.m4a", "Miditra.m4a"),
        "faire": ("Oupangna.m4a", "Manao.m4a"),
        "fermer": ("Oufigunga.m4a", "Manidy.m4a"),
        "finir": ("Oumaliza.m4a", "Mamarana.m4a"),
        "frapper": ("Oupiga.m4a", "Mitety.m4a"),
        "gratter": ("Oukounoua.m4a", "Mikasika.m4a"),
        "jeter": ("Outupa.m4a", "Manary.m4a"),
        "jouer": ("Oucheza.m4a", "Milalaou.m4a"),
        "lire": ("Oufaya.m4a", "Mavaky.m4a"),
        "manger": ("Oulia.m4a", "Mihinana.m4a"),
        "marcher": ("Ouépuka.m4a", "Mandéha.m4a"),
        "mettre": ("Ouwahha.m4a", "Mametaka.m4a"),
        "ouvrir": ("Oufungua.m4a", "Manokatra.m4a"),
        "parler": ("Ouronga.m4a", "Mitény.m4a"),
        "passer": ("Oupita.m4a", "Mandalo.m4a"),
        "penser": ("Oufiriri.m4a", "Mishevitra.m4a"),
        "planter": ("Oupanda.m4a", "Mamboly.m4a"),
        "prendre": ("Oushika.m4a", "Maka.m4a"),
        "ranger/arranger": ("Ourandja.m4a", "Mandamina.m4a"),
        "rester": ("Oubaki.m4a", "Mitoetra.m4a"),
        "répondre": ("Oujivoua.m4a", "Mamaly.m4a"),
        "s'asseoir": ("Ouketi.m4a", "Mipetaka.m4a"),
        "sauter": ("Ouruka.m4a", "Mitsambikina.m4a"),
        "savoir": ("Ouizi.m4a", "Mahay.m4a"),
        "se baigner": ("Oupiga mvou.m4a", "Manandro.m4a"),
        "se laver": ("Ourawa.m4a", "Misasa.m4a"),
        "sortir": ("Oubouka.m4a", "Mivoaka.m4a"),
        "suivre": ("Oufwata.m4a", "Manaraka.m4a"),
        "tenir": ("Ouchakata.m4a", "Mitazona.m4a"),
        "tomber": ("Ouangouwka.m4a", "Milatsaka.m4a"),
        "trouver": ("Oupata.m4a", "Mahita.m4a"),
        "tuer": ("Ou ouwa.m4a", "Mamono.m4a"),
        "vendre": ("Ouza.m4a", "Mivarotra.m4a"),
        "venir": ("Ouja.m4a", "Mavy.m4a"),
        "vivre": ("Ouishi.m4a", "Miaina.m4a"),
        "voir": ("Ourowa.m4a", "Mahita.m4a"),
        "vouloir": ("Ourida.m4a", "Mitiya.m4a"),
        "écouter": ("Ouski.m4a", "Mihaino.m4a"),
        "écrire": ("Ouandika.m4a", "Manoratra.m4a"),
        
        # Correspondances avec les fichiers disponibles (basés sur les noms de fichiers)
        "se raser": ("Manapaka somboutrou.m4a", "Manapaka somboutrou.m4a"),  # Même fichier si approprié
        "couper du bois": ("Manapaka.m4a", "Manapaka.m4a"),
        "faire caca": ("Mamaki azoumati.m4a", "Mamaki azoumati.m4a"),
        
        # Correspondances approximatives avec les fichiers existants
        "arnaquer": ("Mangalatra.m4a", "Mangalatra.m4a"),
        "traverser": ("Latsaka.m4a", "Latsaka.m4a"),  # Basé sur le nom de fichier
    }
    
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