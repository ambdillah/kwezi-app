#!/usr/bin/env python3
"""
Script de vérification approfondie des correspondances audio
Analyse les orthographes complètes des mots et de leurs prononciations originales
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# Charger les variables d'environnement
load_dotenv()

def verify_audio_correspondences():
    """Vérifier toutes les correspondances audio avec analyse orthographique."""
    
    try:
        # Connexion à MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        db = client[db_name]
        collection = db.words
        
        print("🔍 VÉRIFICATION APPROFONDIE DES CORRESPONDANCES AUDIO")
        print("=" * 80)
        print("Analyse des orthographes complètes des mots et prononciations")
        print()
        
        # Traiter chaque catégorie
        categories = ['famille', 'nature', 'nombres', 'animaux']
        total_errors = 0
        total_words = 0
        
        for category in categories:
            print(f"📂 ANALYSE CATÉGORIE: {category.upper()}")
            print("-" * 60)
            
            # Récupérer tous les mots de cette catégorie avec système dual
            category_words = list(collection.find({
                "category": category, 
                "dual_audio_system": True
            }))
            
            if not category_words:
                print(f"⚠️ Aucun mot avec système dual trouvé pour {category}")
                continue
            
            # Lister les fichiers audio disponibles
            audio_dir = f"/app/frontend/assets/audio/{category}"
            available_files = []
            if os.path.exists(audio_dir):
                available_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
            
            print(f"📝 {len(category_words)} mots avec système dual")
            print(f"🎵 {len(available_files)} fichiers audio disponibles")
            print()
            
            # Analyser chaque mot
            category_errors = 0
            for word in category_words:
                total_words += 1
                french = word.get('french', 'N/A')
                shimaore = word.get('shimaore', 'N/A')
                kibouchi = word.get('kibouchi', 'N/A')
                
                shimoare_file = word.get('shimoare_audio_filename')
                kibouchi_file = word.get('kibouchi_audio_filename')
                
                word_errors = []
                
                print(f"🔸 **{french}**")
                print(f"   Shimaoré: '{shimaore}'")
                print(f"   Kibouchi: '{kibouchi}'")
                
                # Vérifier correspondance Shimaoré
                if shimoare_file:
                    print(f"   📁 Audio Shimaoré: {shimoare_file}")
                    
                    # Vérifier si le fichier existe
                    if shimoare_file not in available_files:
                        word_errors.append(f"Fichier shimaoré {shimoare_file} INTROUVABLE")
                    else:
                        # Analyser la correspondance orthographique
                        base_filename = shimoare_file.replace('.m4a', '').lower()
                        shimaore_clean = shimaore.lower().replace(' ', '').replace('/', '').replace('-', '').replace("'", "")
                        
                        # Vérifications de correspondance stricte
                        if (base_filename != shimaore_clean and 
                            shimaore_clean not in base_filename and 
                            base_filename not in shimaore_clean):
                            
                            # Vérifications additionnelles pour les cas spéciaux
                            special_cases = check_special_cases(french, shimaore, shimoare_file, category)
                            if not special_cases:
                                word_errors.append(f"SHIMAORÉ: '{shimaore}' ≠ fichier '{shimoare_file}' (base: {base_filename})")
                else:
                    print(f"   ❌ Pas d'audio shimaoré")
                
                # Vérifier correspondance Kibouchi
                if kibouchi_file:
                    print(f"   📁 Audio Kibouchi: {kibouchi_file}")
                    
                    # Vérifier si le fichier existe
                    if kibouchi_file not in available_files:
                        word_errors.append(f"Fichier kibouchi {kibouchi_file} INTROUVABLE")
                    else:
                        # Analyser la correspondance orthographique
                        base_filename = kibouchi_file.replace('.m4a', '').lower()
                        kibouchi_clean = kibouchi.lower().replace(' ', '').replace('/', '').replace('-', '').replace("'", "")
                        
                        # Vérifications de correspondance stricte
                        if (base_filename != kibouchi_clean and 
                            kibouchi_clean not in base_filename and 
                            base_filename not in kibouchi_clean):
                            
                            # Vérifications additionnelles pour les cas spéciaux
                            special_cases = check_special_cases(french, kibouchi, kibouchi_file, category)
                            if not special_cases:
                                word_errors.append(f"KIBOUCHI: '{kibouchi}' ≠ fichier '{kibouchi_file}' (base: {base_filename})")
                else:
                    print(f"   ❌ Pas d'audio kibouchi")
                
                # Afficher les erreurs trouvées
                if word_errors:
                    print(f"   🚨 **ERREURS DÉTECTÉES** ({len(word_errors)}):")
                    for error in word_errors:
                        print(f"     ➤ {error}")
                    category_errors += len(word_errors)
                    total_errors += len(word_errors)
                else:
                    print(f"   ✅ Correspondances correctes")
                
                print()
            
            print(f"📊 Catégorie {category}: {category_errors} erreurs détectées")
            print()
        
        # Résumé final
        print("=" * 80)
        print(f"📈 RÉSUMÉ DE LA VÉRIFICATION")
        print(f"🔍 Total mots analysés: {total_words}")
        print(f"🚨 Total erreurs détectées: {total_errors}")
        
        if total_errors == 0:
            print("✅ Toutes les correspondances sont correctes!")
        else:
            print("⚠️ Des corrections sont nécessaires")
        
        # Proposer des fichiers audio non utilisés
        print("\n📋 ANALYSE DES FICHIERS AUDIO NON UTILISÉS")
        print("-" * 60)
        
        for category in categories:
            audio_dir = f"/app/frontend/assets/audio/{category}"
            if not os.path.exists(audio_dir):
                continue
                
            available_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
            
            # Récupérer les fichiers utilisés
            used_files = set()
            category_words = list(collection.find({
                "category": category, 
                "dual_audio_system": True
            }))
            
            for word in category_words:
                shimoare_file = word.get('shimoare_audio_filename')
                kibouchi_file = word.get('kibouchi_audio_filename')
                if shimoare_file:
                    used_files.add(shimoare_file)
                if kibouchi_file:
                    used_files.add(kibouchi_file)
            
            unused_files = set(available_files) - used_files
            
            print(f"\n🎵 {category.upper()}:")
            print(f"   Total fichiers: {len(available_files)}")
            print(f"   Fichiers utilisés: {len(used_files)}")
            print(f"   Fichiers non utilisés: {len(unused_files)}")
            
            if unused_files:
                print(f"   📁 Fichiers disponibles non utilisés:")
                for unused in sorted(unused_files):
                    print(f"     • {unused}")
        
        client.close()
        return total_errors == 0
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_special_cases(french, local_word, audio_file, category):
    """Vérifier les cas spéciaux de correspondance"""
    
    # Cas spéciaux connus
    special_mappings = {
        'famille': {
            # Cas où le même fichier est utilisé pour les deux langues
            ('baba', 'Baba k.m4a'): True,  # papa en shimaoré mais fichier k
            ('baba', 'Baba s.m4a'): True,  # papa en kibouchi mais fichier s
        },
        'nature': {
            # Cas où les traductions sont identiques
            ('bahari', 'Bahari.m4a'): True,  # mer identique dans les deux langues
            ('caléni', 'Caléni.m4a'): True,  # barrière de corail identique
        },
        'nombres': {
            # Cas spéciaux de nombres
            ('moja', 'Moja.m4a'): True,
            ('areki', 'Areki.m4a'): True,
        },
        'animaux': {
            # Cas d'animaux avec variations
            ('simba', 'Simba.m4a'): True,  # lion identique dans les deux langues
        }
    }
    
    # Vérifier les mappings spéciaux pour la catégorie
    category_mappings = special_mappings.get(category, {})
    local_word_lower = local_word.lower()
    
    for (word, file), is_valid in category_mappings.items():
        if word.lower() == local_word_lower and audio_file == file:
            return is_valid
    
    # Vérifications additionnelles génériques
    
    # 1. Fichiers avec suffixes 's' ou 'k' (shimaoré/kibouchi)
    if audio_file.endswith(' s.m4a') or audio_file.endswith(' k.m4a'):
        base_file = audio_file.replace(' s.m4a', '').replace(' k.m4a', '').lower()
        if base_file in local_word_lower or local_word_lower in base_file:
            return True
    
    # 2. Correspondances partielles acceptables
    audio_base = audio_file.replace('.m4a', '').lower()
    word_parts = local_word_lower.replace(' ', '').replace('/', '').replace('-', '').replace("'", "")
    
    # Si une partie significative correspond (>= 4 caractères)
    if len(word_parts) >= 4:
        if word_parts in audio_base or audio_base in word_parts:
            return True
    
    # 3. Cas de mots composés
    if ' ' in local_word or '/' in local_word:
        parts = local_word.lower().replace('/', ' ').split()
        for part in parts:
            part_clean = part.replace("'", "").replace("-", "")
            if len(part_clean) >= 3 and (part_clean in audio_base or audio_base in part_clean):
                return True
    
    return False

if __name__ == "__main__":
    print("🚀 VÉRIFICATION APPROFONDIE DES CORRESPONDANCES AUDIO")
    print("🎯 Analyse orthographique complète des mots et prononciations")
    print()
    
    success = verify_audio_correspondences()
    
    if success:
        print("🎉 Vérification terminée - Aucune erreur détectée!")
    else:
        print("⚠️ Vérification terminée - Des corrections sont nécessaires")