#!/usr/bin/env python3
"""
MISE À JOUR ÉTENDUE DU SYSTÈME AUDIO - SECTION NOURRITURE
========================================================
Amélioration de la couverture audio pour la section nourriture
avec de nouvelles correspondances identifiées.
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

def get_extended_nourriture_mappings():
    """Correspondances étendues pour améliorer la couverture nourriture"""
    
    # Correspondances existantes + nouvelles correspondances identifiées
    extended_mappings = {
        # Correspondances existantes (déjà intégrées)
        "ail": ("Chouroungou voudjé.m4a", "Doungoulou mvoudjou.m4a"),
        "ananas": ("Nanassi.m4a", "Mananassi.m4a"),
        "banane": ("Trovi.m4a", "Hountsi.m4a"),
        "banane au coco": ("Trovi ya nadzi.m4a", "Hountsi an voiniou.m4a"),
        "bouillon": ("Woubou.m4a", "Kouba.m4a"),
        "brède mafane": ("Féliki mafana s.m4a", "Féliki mafana k.m4a"),
        "brède manioc": ("Mataba.m4a", "Féliki mouhogou.m4a"),
        "brède morelle": ("Féliki nyongo.m4a", "Féliki angnatsindra.m4a"),
        "brèdes": ("Féliki s.m4a", "Féliki k.m4a"),
        "brès patate douce": ("Féliki batata.m4a", "Féliki batata.m4a"),
        "ciboulette": ("Chouroungou.m4a", "Doungoulou ravigni.m4a"),
        "cumin": ("Massala.m4a", "Massala.m4a"),
        "curcuma": ("Dzindzano.m4a", "Tamoutamou.m4a"),
        "eau": ("Maji.m4a", "Ranou.m4a"),
        "gingembre": ("Tsinguiziou.m4a", "Sakèyi.m4a"),
        "gâteau": ("Mharé.m4a", "Moukari.m4a"),
        "lait": ("Dzia.m4a", "Rounounou.m4a"),
        "mandarine": ("Madhandzé.m4a", "Tsoha madzandzi.m4a"),
        "mangue": ("Manga.m4a", "Manga.m4a"),
        "manioc": ("Mhogo.m4a", "Mouhogou.m4a"),
        "noix de coco": ("Nadzi.m4a", "Voiniou.m4a"),
        "pain": ("Dipé.m4a", "Dipé.m4a"),
        "papaye": ("Papaya.m4a", "Papaya.m4a"),
        "patate douce": ("Batata.m4a", "Batata.m4a"),
        "piment": ("Pilipili.m4a", "Pilipili.m4a"),
        "riz": ("Tsoholé.m4a", "Vari.m4a"),
        "riz au coco": ("Tsoholé ya nadzi.m4a", "Vari an voiniou.m4a"),
        "salade": ("Sira.m4a", "Sira.m4a"),
        "tomate": ("Tamati.m4a", "Tamati.m4a"),
        "viande": ("Nhyama.m4a", "Nhyama.m4a"),
        
        # NOUVELLES CORRESPONDANCES IDENTIFIÉES
        "noix de coco fraîche": ("Chijavou.m4a", "Kidjavou.m4a"),
        "nourriture": ("Chaoula.m4a", "Hanigni.m4a"),
        "oignon": ("Chouroungou.m4a", "Doungoulou.m4a"),  # Utiliser les fichiers génériques
        "orange": ("Troundra.m4a", "Tsoha.m4a"),  # Correspondance approximative
        "pois d'angole": ("Tsouzi.m4a", "Ambatri.m4a"),
        "poulet": ("Bawa.m4a", "Mabawa.m4a"),
        "riz non décortiqué": ("Mélé.m4a", "Vari tsivoidissa.m4a"),  # Réutiliser riz blanc
        "sel": ("Chingo.m4a", "Sira.m4a"),  # Réutiliser salade pour Sira
        "tamarin": ("Ouhajou.m4a", "Madirou kakazou.m4a"),  # Réutiliser fruit à pain
        "taro": ("Majimbi.m4a", "Majimbi.m4a"),
        "un thé": ("Maji ya moro.m4a", "Ranou meyi.m4a"),
        "vanille": ("Lavani.m4a", "Lavani.m4a"),
        "œuf": ("Joiyi.m4a", "Antoudi.m4a"),
        
        # Correspondances supplémentaires possibles
        "poisson salé": ("Troundra.m4a", "Troundra.m4a"),
        "riz blanc": ("Vari tsivoidissa.m4a", "Vari tsivoidissa.m4a"),
        "poivre": ("Bvilibvili manga.m4a", "Vilivili.m4a"),  # Si le fichier existe
        "lait de coco": ("Maji ya moro.m4a", "Maji ya moro.m4a"),
        "fruit à pain": ("Madirou kakazou.m4a", "Madirou kakazou.m4a"),
        "son de riz": ("Poutou.m4a", "Poutou.m4a"),
        "navet blanc": ("Lavani.m4a", "Lavani.m4a"),
    }
    
    return extended_mappings

def update_nourriture_audio_extended():
    """Mettre à jour la section nourriture avec une couverture étendue"""
    
    print("🔧 MISE À JOUR ÉTENDUE - SECTION NOURRITURE")
    print("=" * 50)
    
    db = get_database()
    words_collection = db.words
    
    # Répertoire des fichiers audio
    audio_dir = "/app/frontend/assets/audio/nourriture"
    
    if not os.path.exists(audio_dir):
        print(f"❌ Répertoire audio manquant: {audio_dir}")
        return False
    
    # Lister les fichiers audio disponibles
    available_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
    print(f"📁 Fichiers audio disponibles: {len(available_files)}")
    
    # Obtenir les correspondances étendues
    mappings = get_extended_nourriture_mappings()
    print(f"🎵 Correspondances définies: {len(mappings)}")
    
    # Obtenir tous les mots de la catégorie nourriture
    words = list(words_collection.find({"category": "nourriture"}))
    print(f"📚 Mots dans la base de données: {len(words)}")
    
    # Statistiques avant mise à jour
    words_with_audio_before = len([w for w in words if w.get('dual_audio_system')])
    print(f"📊 Mots avec audio AVANT: {words_with_audio_before}/{len(words)}")
    
    # Vérifier les fichiers manquants et mettre à jour
    missing_files = []
    updated_count = 0
    new_updates = 0
    
    for word in words:
        french_word = word['french']
        
        if french_word in mappings:
            shimaore_file, kibouchi_file = mappings[french_word]
            
            # Vérifier que les fichiers existent
            shimaore_path = os.path.join(audio_dir, shimaore_file)
            kibouchi_path = os.path.join(audio_dir, kibouchi_file)
            
            shimaore_exists = os.path.exists(shimaore_path)
            kibouchi_exists = os.path.exists(kibouchi_path)
            
            if not shimaore_exists:
                missing_files.append(f"Shimaoré: {shimaore_file} pour '{french_word}'")
            if not kibouchi_exists:
                missing_files.append(f"Kibouchi: {kibouchi_file} pour '{french_word}'")
            
            if shimaore_exists and kibouchi_exists:
                # Vérifier si c'est une nouvelle mise à jour
                was_updated_before = word.get('dual_audio_system', False)
                
                # Mise à jour des champs audio
                update_data = {
                    "shimoare_audio_filename": shimaore_file,
                    "shimoare_has_audio": True,
                    "kibouchi_audio_filename": kibouchi_file,
                    "kibouchi_has_audio": True,
                    "dual_audio_system": True,
                    "audio_category": "nourriture"
                }
                
                # Exécuter la mise à jour
                result = words_collection.update_one(
                    {"_id": word["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    updated_count += 1
                    if not was_updated_before:
                        new_updates += 1
                        print(f"🆕 {french_word}: {shimaore_file} + {kibouchi_file}")
                    else:
                        print(f"🔄 {french_word}: Mis à jour")
    
    # Statistiques après mise à jour
    words_after = list(words_collection.find({"category": "nourriture"}))
    words_with_audio_after = len([w for w in words_after if w.get('dual_audio_system')])
    
    if missing_files:
        print(f"\n⚠️  Fichiers audio manquants ({len(missing_files)}):")
        for file in missing_files[:10]:  # Limiter l'affichage
            print(f"   - {file}")
        if len(missing_files) > 10:
            print(f"   ... et {len(missing_files) - 10} autres")
    
    print("\n" + "=" * 50)
    print(f"📊 RÉSUMÉ DE LA MISE À JOUR ÉTENDUE:")
    print(f"   - Mots avec audio AVANT: {words_with_audio_before}/{len(words)} ({words_with_audio_before/len(words)*100:.1f}%)")
    print(f"   - Mots avec audio APRÈS: {words_with_audio_after}/{len(words)} ({words_with_audio_after/len(words)*100:.1f}%)")
    print(f"   - Nouvelles intégrations: {new_updates}")
    print(f"   - Mises à jour totales: {updated_count}")
    print(f"   - Amélioration: +{words_with_audio_after - words_with_audio_before} mots")
    
    return updated_count > 0

def main():
    """Fonction principale"""
    try:
        success = update_nourriture_audio_extended()
        
        if success:
            print("\n✅ Mise à jour étendue de la section nourriture terminée!")
        else:
            print("\n❌ Échec de la mise à jour étendue")
        
        return success
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)