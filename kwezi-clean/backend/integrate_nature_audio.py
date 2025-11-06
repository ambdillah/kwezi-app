#!/usr/bin/env python3
"""
Script pour intégrer les prononciations audio de la section nature
en mappant automatiquement les fichiers aux mots existants.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# Ajouter le chemin du backend au PYTHONPATH
sys.path.append('/app/backend')

# Charger les variables d'environnement
load_dotenv()

from database_protection import DatabaseProtector

def integrate_nature_audio():
    """Intègre les fichiers audio nature avec les mots existants."""
    
    # Mapping automatique basé sur les correspondances évidentes
    # Format: filename -> (french_word, pronunciation_lang)
    audio_mappings = {
        # Correspondances directes évidentes
        "Bahari.m4a": ("mer", "both"),
        "Mlima.m4a": ("pente/colline/mont", "shimaore"),
        "Boungou.m4a": ("pente/colline/mont", "kibouchi"),
        "Bwé.m4a": ("caillou/pierre/rocher", "shimaore"),
        "Vatou.m4a": ("caillou/pierre/rocher", "kibouchi"),
        "Mtsanga.m4a": ("sable", "shimaore"),
        "Fasigni.m4a": ("sable", "kibouchi"),
        "Fassigni.m4a": ("plage", "kibouchi"),  # Version alternative
        "Mtsangani.m4a": ("plage", "shimaore"),
        "Kalé.m4a": ("platier", "shimaore"),
        "Kaléni.m4a": ("barrière de corail", "both"),  # ou platier
        "Caléni.m4a": ("barrière de corail", "both"),
        "M_manga.m4a": ("manguier", "shimaore"),
        "Voudi ni manga.m4a": ("manguier", "kibouchi"),
        "M_frampé.m4a": ("arbre à pain", "shimaore"),
        "Voudi ni frampé.m4a": ("arbre à pain", "kibouchi"),
        "M_bouyou.m4a": ("baobab", "shimaore"),
        "Voudi ni bouyou.m4a": ("baobab", "kibouchi"),
        "M_fénéssi.m4a": ("jacquier", "shimaore"),
        "Voudi ni finéssi.m4a": ("jacquier", "kibouchi"),
        "M_nadzi.m4a": ("cocotier", "shimaore"),
        "Voudi ni vwaniou.m4a": ("cocotier", "kibouchi"),
        "M_bambo.m4a": ("bambou", "shimaore"),
        "Valiha.m4a": ("bambou", "kibouchi"),
        "Trindri.m4a": ("bananier", "shimaore"),
        "Voudi ni hountsi.m4a": ("bananier", "kibouchi"),
        "Mwiri.m4a": ("arbre", "shimaore"),
        "Kakazou.m4a": ("arbre", "kibouchi"),
        "Trahi s.m4a": ("branche", "shimaore"),
        "Trahi k.m4a": ("branche", "kibouchi"),
        "Mouro.m4a": ("rivière", "shimaore"),
        "Mouroni.m4a": ("rivière", "kibouchi"),
        "Paré s.m4a": ("rue/route", "shimaore"),
        "Paré k.m4a": ("rue/route", "kibouchi"),
        "Mwézi.m4a": ("lune", "shimaore"),
        "Fandzava.m4a": ("lune", "kibouchi"),
        "Jouwa.m4a": ("soleil", "shimaore"),
        "Zouva.m4a": ("soleil", "kibouchi"),
        "Pévo.m4a": ("vent", "shimaore"),
        "Tsikou.m4a": ("vent", "kibouchi"),
        "Wingou.m4a": ("nuage", "shimaore"),
        "Vingou.m4a": ("nuage", "kibouchi"),
        "Voua.m4a": ("pluie", "shimaore"),
        "Mahaléni.m4a": ("pluie", "kibouchi"),
        "Darouba.m4a": ("tempête", "shimaore"),
        "Tsikou soulaimana.m4a": ("tornade", "kibouchi"),
        "Ouzimouyi.m4a": ("tornade", "shimaore"),
        "Dhouja.m4a": ("vague", "shimaore"),
        "Houndza_riaka.m4a": ("vague", "kibouchi"),
        "Kwassa kwassa.m4a": ("vedette", "shimaore"),
        "Vidéti.m4a": ("vedette", "kibouchi"),
        "Daradja.m4a": ("pont", "both"),
        "Bandra.m4a": ("plateau", "shimaore"),
        "Kètraka.m4a": ("plateau", "kibouchi"),
        "Malavouni.m4a": ("campagne/forêt", "shimaore"),
        "Atihala.m4a": ("campagne/forêt", "kibouchi"),
        "Mhonko.m4a": ("mangrove", "shimaore"),
        "Honkou.m4a": ("mangrove", "kibouchi"),
        "Soiyi s.m4a": ("corail", "shimaore"),
        "Soiyi k.m4a": ("corail", "kibouchi"),
        "Malavou.m4a": ("herbe", "shimaore"),
        "Haitri.m4a": ("herbe", "kibouchi"),
        "Foulera.m4a": ("fleur", "both"),
        "Mawoini.m4a": ("feuille", "shimaore"),
        "Hayitri.m4a": ("feuille", "kibouchi"),
        "Mouwoi.m4a": ("canne à sucre", "shimaore"),
        "Fari.m4a": ("canne à sucre", "kibouchi"),
        "Kouni.m4a": ("fagot", "shimaore"),
        "Azoumati.m4a": ("fagot", "kibouchi"),
        "Ndzia.m4a": ("chemin/sentier/parcours", "shimaore"),
        "Lalagna.m4a": ("chemin/sentier/parcours", "kibouchi"),
        "Trotro.m4a": ("terre", "shimaore"),
        "Fotaka.m4a": ("terre", "kibouchi"),
        "Tani.m4a": ("sol", "kibouchi"),
        "Nyéha.m4a": ("sauvage", "shimaore"),
        "Di.m4a": ("sauvage", "kibouchi"),
        "Ourora.m4a": ("inondé", "shimaore"),
        "Dobou.m4a": ("inondé", "kibouchi"),
        "Maji yamalé.m4a": ("marée haute", "shimaore"),
        "Ranou fénou.m4a": ("marée haute", "kibouchi"),
        "Maji yavo.m4a": ("marée basse", "shimaore"),
        "Ranou mèki.m4a": ("marée basse", "kibouchi"),
        "Mcacamba.m4a": ("arc en ciel", "shimaore"),
        "Licoli.m4a": ("école", "both"),
        "Shioni.m4a": ("école coranique", "shimaore"),
        "Kioni.m4a": ("école coranique", "kibouchi"),
        "Padza s.m4a": ("érosion", "shimaore"),
        "Padza k.m4a": ("érosion", "kibouchi"),
        "Gnora.m4a": ("étoile", "shimaore"),
        "Lakintagna.m4a": ("étoile", "kibouchi"),
    }
    
    try:
        # Connexion à MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.words
        
        # Initialiser la protection de base de données
        db_protection = DatabaseProtector()
        
        print(f"🔗 Connexion à MongoDB: {mongo_url}")
        print(f"📊 Base de données: {db_name}")
        print(f"🌿 Fichiers audio nature à intégrer: {len(audio_mappings)}")
        print()
        
        # Créer une sauvegarde avant modification
        print("💾 Création d'une sauvegarde avant modification...")
        try:
            backup_path = db_protection.create_backup("before_integrate_nature_audio")
            if backup_path:
                print("✅ Sauvegarde créée avec succès")
            else:
                print("⚠️ Échec de la sauvegarde")
        except Exception as e:
            print(f"⚠️ Problème sauvegarde (continuons quand même): {str(e)}")
        print()
        
        # Traiter chaque fichier audio
        mises_a_jour = 0
        correspondances_trouvees = 0
        
        for filename, (french_word, pronunciation_lang) in audio_mappings.items():
            print(f"🎵 Traitement de {filename} pour '{french_word}'...")
            
            # Rechercher le mot dans la base de données
            existing_word = collection.find_one({
                "french": {"$regex": f"^{french_word}$", "$options": "i"},
                "category": "nature"
            })
            
            if existing_word:
                correspondances_trouvees += 1
                print(f"   ✅ Mot trouvé: {french_word}")
                
                # Mettre à jour avec les informations audio
                update_data = {
                    "has_authentic_audio": True,
                    "audio_filename": filename,
                    "audio_pronunciation_lang": pronunciation_lang,
                    "audio_source": "google_drive_nature",
                    "audio_updated_at": datetime.now(),
                    "audio_added_by": "integrate_nature_audio_script"
                }
                
                result = collection.update_one(
                    {"_id": existing_word["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    mises_a_jour += 1
                    print(f"   ✅ Métadonnées audio ajoutées")
                    print(f"      Langue: {pronunciation_lang}")
                    print(f"      Fichier: {filename}")
                else:
                    print(f"   ⚠️ Aucune modification effectuée")
                    
            else:
                print(f"   ❌ Mot '{french_word}' non trouvé dans la catégorie nature")
            
            print()
        
        # Statistiques finales
        print("=" * 60)
        print(f"📈 RÉSUMÉ DE L'INTÉGRATION AUDIO NATURE")
        print(f"🎵 Fichiers audio traités: {len(audio_mappings)}")
        print(f"🔍 Correspondances trouvées: {correspondances_trouvees}")
        print(f"📝 Mots mis à jour: {mises_a_jour}")
        print()
        
        # Vérifier l'état final
        final_nature_with_audio = collection.count_documents({
            "category": "nature", 
            "has_authentic_audio": True
        })
        print(f"📊 Total mots nature avec audio: {final_nature_with_audio}")
        
        print()
        print("✅ Intégration des métadonnées audio nature terminée avec succès!")
        
        # Fermer la connexion
        client.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'intégration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INTÉGRATION DES PRONONCIATIONS AUDIO NATURE")
    print("🌿 Source: 96 fichiers audio nature + mots existants")
    print("=" * 60)
    print()
    
    success = integrate_nature_audio()
    
    if success:
        print("🎉 Intégration terminée avec succès!")
        print("📱 Les mots nature ont maintenant leurs prononciations authentiques!")
    else:
        print("💥 Échec de l'intégration")
        sys.exit(1)