#!/usr/bin/env python3
"""
EXTENSION DU SYSTÈME AUDIO DUAL - SECTION EXPRESSIONS
===================================================
Extension du système audio dual pour inclure la catégorie "expressions"
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

def get_expressions_mappings():
    """Correspondances audio pour la section expressions"""
    
    # Correspondances basées sur l'analyse des fichiers audio disponibles et des traductions
    expressions_mappings = {
        # Correspondances directes identifiées avec les fichiers audio
        "appelez la police !": ("Hira sirikali.m4a", "Kahiya sirikali.m4a"),
        "appelez une ambulance !": ("Hira ambulanci.m4a", "Kahiya ambulanci.m4a"),
        "au milieu": ("Hari.m4a", "Angnivou.m4a"),
        "avec climatisation ?": ("Ina climatisation.m4a", "Ina climatisation.m4a"),  # Même fichier si pas d'équivalent
        "avec petit déjeuner ?": ("Ina kèya.m4a", "Ina kèya.m4a"),  # Même fichier si pas d'équivalent
        "c'est très bon !": ("Issi jiva.m4a", "Issi jiva.m4a"),  # Même fichier
        "combien la nuit ?": ("Hotri inou haligni areki.m4a", "Hotri inou haligni areki.m4a"),  # Même fichier
        "combien ça coûte ?": ("Hotri inou moi.m4a", "Hotri inou moi.m4a"),  # Même fichier
        "joie": ("Fouraha.m4a", "Aravouagna.m4a"),
        "montre-moi": ("Ampizaha zahou.m4a", "Ampizaha zahou.m4a"),  # Même fichier
        "où se trouve": ("Aya moi.m4a", "Aya moi.m4a"),  # Même fichier
        "où sommes-nous": ("Atsika yétou aya.m4a", "Atsika yétou aya.m4a"),  # Même fichier
        "tout droit": ("Hondzoha.m4a", "Hondzoha.m4a"),  # Même fichier
        "trop cher": ("Hali.m4a", "Hali.m4a"),  # Même fichier
        "à droite": ("Houméni.m4a", "Houméni.m4a"),  # Même fichier
        "à gauche": ("Finana.m4a", "Finana.m4a"),  # Même fichier
    }
    
    return expressions_mappings

def extend_dual_audio_system_expressions():
    """Étendre le système audio dual pour la catégorie expressions"""
    
    print("🔧 EXTENSION DU SYSTÈME AUDIO DUAL - SECTION EXPRESSIONS")
    print("=" * 60)
    
    db = get_database()
    words_collection = db.words
    
    # Répertoire des fichiers audio
    audio_dir = "/app/frontend/assets/audio/expressions"
    
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
    mappings = get_expressions_mappings()
    print(f"🎵 Correspondances définies: {len(mappings)}")
    
    # Obtenir toutes les expressions
    expressions = list(words_collection.find({"category": "expressions"}))
    print(f"📚 Expressions dans la base de données: {len(expressions)}")
    
    # Statistiques avant mise à jour
    expressions_with_audio_before = len([e for e in expressions if e.get('dual_audio_system')])
    print(f"📊 Expressions avec audio AVANT: {expressions_with_audio_before}/{len(expressions)}")
    
    # Vérifier les fichiers manquants et mettre à jour
    missing_files = []
    updated_count = 0
    new_updates = 0
    
    for expression in expressions:
        french_expr = expression['french']
        
        if french_expr in mappings:
            shimaore_file, kibouchi_file = mappings[french_expr]
            
            # Vérifier que les fichiers existent
            shimaore_path = os.path.join(audio_dir, shimaore_file)
            kibouchi_path = os.path.join(audio_dir, kibouchi_file)
            
            shimaore_exists = os.path.exists(shimaore_path)
            kibouchi_exists = os.path.exists(kibouchi_path)
            
            if not shimaore_exists:
                missing_files.append(f"Shimaoré: {shimaore_file} pour '{french_expr}'")
            if not kibouchi_exists:
                missing_files.append(f"Kibouchi: {kibouchi_file} pour '{french_expr}'")
            
            if shimaore_exists and kibouchi_exists:
                # Vérifier si c'est une nouvelle mise à jour
                was_updated_before = expression.get('dual_audio_system', False)
                
                # Mise à jour des champs audio
                update_data = {
                    "shimoare_audio_filename": shimaore_file,
                    "shimoare_has_audio": True,
                    "kibouchi_audio_filename": kibouchi_file,
                    "kibouchi_has_audio": True,
                    "dual_audio_system": True,
                    "audio_category": "expressions"
                }
                
                # Exécuter la mise à jour
                result = words_collection.update_one(
                    {"_id": expression["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    updated_count += 1
                    if not was_updated_before:
                        new_updates += 1
                        print(f"🆕 {french_expr}: {shimaore_file} + {kibouchi_file}")
                    else:
                        print(f"🔄 {french_expr}: Mis à jour")
    
    # Statistiques après mise à jour
    expressions_after = list(words_collection.find({"category": "expressions"}))
    expressions_with_audio_after = len([e for e in expressions_after if e.get('dual_audio_system')])
    
    if missing_files:
        print(f"\n⚠️  Fichiers audio manquants ({len(missing_files)}):")
        for file in missing_files[:10]:  # Limiter l'affichage
            print(f"   - {file}")
        if len(missing_files) > 10:
            print(f"   ... et {len(missing_files) - 10} autres")
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSUMÉ DE L'EXTENSION EXPRESSIONS:")
    print(f"   - Expressions avec audio AVANT: {expressions_with_audio_before}/{len(expressions)} ({expressions_with_audio_before/len(expressions)*100:.1f}%)")
    print(f"   - Expressions avec audio APRÈS: {expressions_with_audio_after}/{len(expressions)} ({expressions_with_audio_after/len(expressions)*100:.1f}%)")
    print(f"   - Nouvelles intégrations: {new_updates}")
    print(f"   - Mises à jour totales: {updated_count}")
    print(f"   - Amélioration: +{expressions_with_audio_after - expressions_with_audio_before} expressions")
    
    return updated_count > 0

def main():
    """Fonction principale"""
    try:
        success = extend_dual_audio_system_expressions()
        
        if success:
            print("\n✅ Extension du système audio dual pour expressions terminée!")
        else:
            print("\n❌ Échec de l'extension du système audio dual pour expressions")
        
        return success
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)