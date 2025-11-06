#!/usr/bin/env python3
"""
EXTENSION DU SYSTÈME AUDIO DUAL - 4 NOUVELLES SECTIONS
=====================================================
Extension du système audio dual pour inclure les catégories:
- vetements (16 mots)
- maison (37 mots) 
- tradition (16 mots)
- transport (7 mots)

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

def get_4_sections_mappings():
    """Correspondances audio pour les 4 nouvelles sections"""
    
    mappings = {}
    
    # VÊTEMENTS (16 mots)
    mappings["vetements"] = {
        "baskets/sneakers": ("Magochi.m4a", "Magochi.m4a"),
        "chapeau": ("Kofia.m4a", "Koufia.m4a"),
        "chaussures": ("Kabwa.m4a", "Kabwa.m4a"),
        "chemise": ("Chimizi.m4a", "Chimizi.m4a"),
        "haut de salouva": ("Body.m4a", "Body.m4a"),
        "jupe": ("Jipo.m4a", "Ripou.m4a"),
        "kamiss/boubou": ("Ancandzou bé.m4a", "Ancandzou bé.m4a"),
        "pantalon": ("Sourouali.m4a", "Sourouali.m4a"),
        "robe": ("Robo.m4a", "Robo.m4a"),
        "salouva": ("Salouvagna.m4a", "Salouvagna.m4a"),
        "short": ("Kaliso.m4a", "Kaliso.m4a"),
        "sous vêtement": ("Silipou.m4a", "Silipou.m4a"),
        "t shirt": ("Kandzou.m4a", "Kandzou.m4a"),
        "tongs": ("Sapatri.m4a", "Kabwa sapatri.m4a"),
        "voile": ("Kichali s.m4a", "Kichali k.m4a"),
        "vêtement": ("Ngouvwo.m4a", "Ankandzou.m4a"),
    }
    
    # MAISON (37 mots)
    mappings["maison"] = {
        "ampoule": ("Lalampou.m4a", "Lalampou.m4a"),
        "assiette": ("Sahani.m4a", "Sahani.m4a"),
        "balai": ("Péou.m4a", "Famafa.m4a"),
        "bol": ("Chicombé.m4a", "Bacouli.m4a"),
        "buffet": ("Biffé.m4a", "Biffé.m4a"),
        "cartable/malette": ("Mkoba.m4a", "Mkoba.m4a"),
        "case": ("Banga.m4a", "Banga.m4a"),
        "chaise": ("Chiri.m4a", "Chiri.m4a"),
        "clôture": ("Vala s.m4a", "Vala k.m4a"),
        "coupe coupe": ("Chombo.m4a", "Chombou.m4a"),
        "cour": ("Mraba.m4a", "Lacourou.m4a"),
        "couteau": ("Sembeya.m4a", "Méssou.m4a"),
        "cuillère": ("Soutrou.m4a", "Sotrou.m4a"),
        "fenêtre": ("Fénétri.m4a", "Lafoumétara.m4a"),
        "fondation": ("Houra.m4a", "Koura.m4a"),
        "hache": ("Soha.m4a", "Famaki.m4a"),
        "lit": ("Chtrandra.m4a", "Koubani.m4a"),
        "louche": ("Paou.m4a", "Pow.m4a"),
        "lumière": ("Mwengué.m4a", "Mwengue.m4a"),
        "machette": ("M_panga.m4a", "Ampanga.m4a"),
        "maison": ("Nyoumba.m4a", "Tragnou.m4a"),
        "marmite": ("Gnoungou.m4a", "Vilangni.m4a"),
        "matelas": ("Godoro.m4a", "Goudorou.m4a"),
        "miroir": ("Chido.m4a", "Kitarafa.m4a"),
        "mortier": ("Chino.m4a", "Légnou.m4a"),
        "mur": ("Péssi.m4a", "Riba.m4a"),
        "oreiller": ("Mtsao.m4a", "Hondagna.m4a"),
        "porte": ("Mlango.m4a", "Varavaragna.m4a"),
        "sac": ("Gouni s.m4a", "Gouni k.m4a"),
        "seau": ("Siyo.m4a", "Siyo.m4a"),
        "table": ("Latabou.m4a", "Latabou.m4a"),
        "toilette": ("Mrabani.m4a", "Mraba.m4a"),
        "toiture": ("Outro.m4a", "Vovougnou.m4a"),
        "torche": ("Pongé.m4a", "Pongi.m4a"),
        "torche locale": ("Gandilé-poutroupmax.m4a", "Gandili-poutroupmax.m4a"),
        "vesselles": ("Ziya.m4a", "Hintagna.m4a"),
        "véranda": ("Baraza.m4a", "Baraza.m4a"),
    }
    
    # TRADITION (16 mots)
    mappings["tradition"] = {
        "barbecue traditionnelle": ("Voulé.m4a", "Voulé.m4a"),
        "boxe traditionnelle": ("Mrengué.m4a", "Mouringui.m4a"),
        "camper": ("Tobé.m4a", "Mitobi.m4a"),
        "chant mariage traditionnel": ("Manzaraka.m4a", "Manzaraka.m4a"),
        "chant religieux femme": ("Deba.m4a", "Deba.m4a"),
        "chant religieux homme": ("Moulidi-dahira-dinahou.m4a", "Moulidi-dahira-dinahou.m4a"),
        "chant religieux mixte": ("Shengué-madjlis.m4a", "Maoulida shengué-madjlis.m4a"),
        "chant traditionnelle": ("Mgodro.m4a", "Mgodro.m4a"),
        "cérémonie": ("Shouhouli.m4a", "Shouhouli.m4a"),
        "danse traditionnelle femme": ("Mbiwi-wadhaha.m4a", "Mbiwi-wadhaha.m4a"),
    }
    
    # TRANSPORT (7 mots)
    mappings["transport"] = {
        "avion": ("Ndrégué.m4a", "Roplani.m4a"),
        "barge": ("Markabou.m4a", "Markabou.m4a"),
        "motos": ("Monto.m4a", "Monto.m4a"),
        "pirogue": ("Laka.m4a", "Lakana.m4a"),
        "taxis": ("Taxi.m4a", "Taxi.m4a"),
        "vedettes": ("Kwassa kwassa.m4a", "Videti.m4a"),
        "vélos": ("Bicycléti.m4a", "Bicycléti.m4a"),
    }
    
    return mappings

def extend_dual_audio_system_4_sections():
    """Étendre le système audio dual pour les 4 nouvelles sections"""
    
    print("🔧 EXTENSION DU SYSTÈME AUDIO DUAL - 4 NOUVELLES SECTIONS")
    print("=" * 65)
    
    db = get_database()
    words_collection = db.words
    
    # Répertoires des fichiers audio
    base_audio_dir = "/app/frontend/assets/audio"
    
    all_mappings = get_4_sections_mappings()
    
    total_updated = 0
    total_errors = 0
    
    for category, mappings in all_mappings.items():
        print(f"\n📂 Section: {category.upper()}")
        print("-" * 50)
        
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
        
        if not words:
            print(f"⚠️ Aucun mot trouvé pour la catégorie: {category}")
            continue
        
        # Statistiques avant mise à jour
        words_with_audio_before = len([w for w in words if w.get('dual_audio_system')])
        print(f"📊 Mots avec audio AVANT: {words_with_audio_before}/{len(words)}")
        
        # Vérifier quels fichiers audio existent
        missing_files = []
        for french_word, (shimaore_file, kibouchi_file) in mappings.items():
            shimaore_path = os.path.join(audio_dir, shimaore_file)
            kibouchi_path = os.path.join(audio_dir, kibouchi_file)
            
            if not os.path.exists(shimaore_path):
                missing_files.append(f"Shimaoré: {shimaore_file} pour '{french_word}'")
            if not os.path.exists(kibouchi_path):
                missing_files.append(f"Kibouchi: {kibouchi_file} pour '{french_word}'")
        
        # Mettre à jour les mots avec les informations audio
        updated_count = 0
        new_updates = 0
        
        for word in words:
            french_word = word['french']
            
            if french_word in mappings:
                shimaore_file, kibouchi_file = mappings[french_word]
                
                # Vérifier que les fichiers existent avant de mettre à jour
                shimaore_exists = os.path.exists(os.path.join(audio_dir, shimaore_file))
                kibouchi_exists = os.path.exists(os.path.join(audio_dir, kibouchi_file))
                
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
                        "audio_category": category
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
                else:
                    if not shimaore_exists or not kibouchi_exists:
                        total_errors += 1
        
        # Statistiques après mise à jour
        words_after = list(words_collection.find({"category": category}))
        words_with_audio_after = len([w for w in words_after if w.get('dual_audio_system')])
        
        if missing_files:
            print(f"\n⚠️  Fichiers audio manquants ({len(missing_files)}):")
            for file in missing_files[:5]:  # Limiter l'affichage
                print(f"   - {file}")
            if len(missing_files) > 5:
                print(f"   ... et {len(missing_files) - 5} autres")
        
        print(f"📊 Section {category}: {words_with_audio_after}/{len(words)} mots mis à jour")
        total_updated += words_with_audio_after
    
    print("\n" + "=" * 65)
    print(f"📊 RÉSUMÉ GLOBAL - 4 NOUVELLES SECTIONS:")
    print(f"   - Mots mis à jour: {total_updated}")
    print(f"   - Erreurs: {total_errors}")
    print(f"   - Nouvelles catégories avec audio dual: 4")
    
    return total_updated > 0

def main():
    """Fonction principale"""
    try:
        success = extend_dual_audio_system_4_sections()
        
        if success:
            print("\n✅ Extension du système audio dual pour 4 nouvelles sections terminée!")
        else:
            print("\n❌ Échec de l'extension du système audio dual")
        
        return success
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)