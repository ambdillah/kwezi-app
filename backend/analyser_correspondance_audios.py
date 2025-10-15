#!/usr/bin/env python3
"""
Analyse complète de la correspondance entre les mots et leurs fichiers audio
Principe : Le nom de l'audio doit correspondre au nom du mot (shimaoré ou kibouchi)
"""

from pymongo import MongoClient
import os
import re
from difflib import SequenceMatcher

def normalize_for_comparison(text):
    """Normalise un texte pour comparaison (enlève accents, ponctuation, espaces)"""
    if not text:
        return ""
    # Minuscules
    text = text.lower()
    # Enlever certains caractères spéciaux mais garder les espaces et tirets
    text = text.replace("'", "").replace('"', "").replace(".", "")
    return text.strip()

def similarity(a, b):
    """Calcule la similarité entre deux chaînes (0 à 1)"""
    return SequenceMatcher(None, normalize_for_comparison(a), normalize_for_comparison(b)).ratio()

def find_audio_file_in_directory(category_path, word_text):
    """Cherche un fichier audio correspondant au mot dans le dossier de catégorie"""
    if not os.path.exists(category_path):
        return None, 0
    
    word_normalized = normalize_for_comparison(word_text)
    best_match = None
    best_similarity = 0
    
    for filename in os.listdir(category_path):
        if filename.endswith('.m4a'):
            # Enlever l'extension
            file_base = filename[:-4]
            file_normalized = normalize_for_comparison(file_base)
            
            # Calculer la similarité
            sim = similarity(word_text, file_base)
            
            # Si très similaire (>= 0.8), c'est probablement le bon fichier
            if sim >= 0.8 and sim > best_similarity:
                best_match = filename
                best_similarity = sim
    
    return best_match, best_similarity

def main():
    print("=" * 80)
    print("ANALYSE COMPLÈTE DE LA CORRESPONDANCE MOTS <-> AUDIOS")
    print("=" * 80)
    print()
    print("Principe : Le nom de l'audio doit correspondre au nom du mot")
    print("Cela peut prendre quelques minutes...")
    print()
    
    # Connexion
    client = MongoClient("mongodb://localhost:27017")
    db = client["mayotte_app"]
    
    # Chemin de base des audios
    audio_base_path = "/app/frontend/assets/audio"
    
    # Récupérer tous les mots
    words = list(db.words.find({}).sort("category", 1))
    
    print(f"Total de mots à analyser : {len(words)}")
    print()
    
    # Listes des problèmes
    problemes = {
        "audio_manquant_shimaore": [],
        "audio_manquant_kibouchi": [],
        "audio_incorrect_shimaore": [],
        "audio_incorrect_kibouchi": [],
        "audio_non_reference": [],
        "audio_ok": 0
    }
    
    print("Analyse en cours...")
    print()
    
    for i, word in enumerate(words, 1):
        if i % 100 == 0:
            print(f"  Progression : {i}/{len(words)} mots analysés...")
        
        french = word.get('french', '')
        category = word.get('category', '')
        shimaore = word.get('shimaore', '')
        kibouchi = word.get('kibouchi', '')
        
        category_path = os.path.join(audio_base_path, category)
        
        # Vérifier shimaoré
        if shimaore:
            audio_ref_shim = word.get('audio_filename_shimaore') or word.get('shimoare_audio_filename')
            
            if not audio_ref_shim:
                # Pas de référence audio, chercher un fichier correspondant
                found_file, sim = find_audio_file_in_directory(category_path, shimaore)
                if found_file:
                    problemes["audio_non_reference"].append({
                        "french": french,
                        "mot": shimaore,
                        "langue": "shimaoré",
                        "category": category,
                        "fichier_trouve": found_file,
                        "similarite": f"{sim:.2f}"
                    })
                else:
                    problemes["audio_manquant_shimaore"].append({
                        "french": french,
                        "mot": shimaore,
                        "category": category
                    })
            else:
                # Il y a une référence, vérifier si le fichier existe et correspond
                audio_path = os.path.join(category_path, audio_ref_shim)
                if os.path.exists(audio_path):
                    # Le fichier existe, vérifier la correspondance du nom
                    audio_base = audio_ref_shim[:-4]  # Sans .m4a
                    sim = similarity(shimaore, audio_base)
                    
                    if sim < 0.8:  # Correspondance faible
                        problemes["audio_incorrect_shimaore"].append({
                            "french": french,
                            "mot": shimaore,
                            "category": category,
                            "audio_reference": audio_ref_shim,
                            "similarite": f"{sim:.2f}"
                        })
                    else:
                        problemes["audio_ok"] += 1
                else:
                    problemes["audio_manquant_shimaore"].append({
                        "french": french,
                        "mot": shimaore,
                        "category": category,
                        "audio_reference": audio_ref_shim
                    })
        
        # Vérifier kibouchi
        if kibouchi:
            audio_ref_kib = word.get('audio_filename_kibouchi') or word.get('kibouchi_audio_filename')
            
            if not audio_ref_kib:
                # Pas de référence audio, chercher un fichier correspondant
                found_file, sim = find_audio_file_in_directory(category_path, kibouchi)
                if found_file:
                    problemes["audio_non_reference"].append({
                        "french": french,
                        "mot": kibouchi,
                        "langue": "kibouchi",
                        "category": category,
                        "fichier_trouve": found_file,
                        "similarite": f"{sim:.2f}"
                    })
                else:
                    problemes["audio_manquant_kibouchi"].append({
                        "french": french,
                        "mot": kibouchi,
                        "category": category
                    })
            else:
                # Il y a une référence, vérifier si le fichier existe et correspond
                audio_path = os.path.join(category_path, audio_ref_kib)
                if os.path.exists(audio_path):
                    # Le fichier existe, vérifier la correspondance du nom
                    audio_base = audio_ref_kib[:-4]  # Sans .m4a
                    sim = similarity(kibouchi, audio_base)
                    
                    if sim < 0.8:  # Correspondance faible
                        problemes["audio_incorrect_kibouchi"].append({
                            "french": french,
                            "mot": kibouchi,
                            "category": category,
                            "audio_reference": audio_ref_kib,
                            "similarite": f"{sim:.2f}"
                        })
                    else:
                        problemes["audio_ok"] += 1
                else:
                    problemes["audio_manquant_kibouchi"].append({
                        "french": french,
                        "mot": kibouchi,
                        "category": category,
                        "audio_reference": audio_ref_kib
                    })
    
    # Affichage des résultats
    print()
    print("=" * 80)
    print("RÉSULTATS DE L'ANALYSE")
    print("=" * 80)
    print()
    
    print(f"✅ Audios corrects : {problemes['audio_ok']}")
    print()
    
    # Problème 1 : Audios manquants shimaoré
    if problemes["audio_manquant_shimaore"]:
        print(f"❌ AUDIOS MANQUANTS SHIMAORÉ : {len(problemes['audio_manquant_shimaore'])}")
        for p in problemes["audio_manquant_shimaore"][:20]:
            print(f"   • {p['french']} ({p['category']})")
            print(f"     Mot shimaoré : {p['mot']}")
            if 'audio_reference' in p:
                print(f"     Audio référencé mais manquant : {p['audio_reference']}")
        if len(problemes["audio_manquant_shimaore"]) > 20:
            print(f"   ... et {len(problemes['audio_manquant_shimaore']) - 20} autres")
        print()
    
    # Problème 2 : Audios manquants kibouchi
    if problemes["audio_manquant_kibouchi"]:
        print(f"❌ AUDIOS MANQUANTS KIBOUCHI : {len(problemes['audio_manquant_kibouchi'])}")
        for p in problemes["audio_manquant_kibouchi"][:20]:
            print(f"   • {p['french']} ({p['category']})")
            print(f"     Mot kibouchi : {p['mot']}")
            if 'audio_reference' in p:
                print(f"     Audio référencé mais manquant : {p['audio_reference']}")
        if len(problemes["audio_manquant_kibouchi"]) > 20:
            print(f"   ... et {len(problemes['audio_manquant_kibouchi']) - 20} autres")
        print()
    
    # Problème 3 : Audios incorrects shimaoré
    if problemes["audio_incorrect_shimaore"]:
        print(f"⚠️  AUDIOS MAL NOMMÉS SHIMAORÉ : {len(problemes['audio_incorrect_shimaore'])}")
        for p in problemes["audio_incorrect_shimaore"][:20]:
            print(f"   • {p['french']} ({p['category']})")
            print(f"     Mot shimaoré : {p['mot']}")
            print(f"     Audio référencé : {p['audio_reference']}")
            print(f"     Similarité : {p['similarite']}")
        if len(problemes["audio_incorrect_shimaore"]) > 20:
            print(f"   ... et {len(problemes['audio_incorrect_shimaore']) - 20} autres")
        print()
    
    # Problème 4 : Audios incorrects kibouchi
    if problemes["audio_incorrect_kibouchi"]:
        print(f"⚠️  AUDIOS MAL NOMMÉS KIBOUCHI : {len(problemes['audio_incorrect_kibouchi'])}")
        for p in problemes["audio_incorrect_kibouchi"][:20]:
            print(f"   • {p['french']} ({p['category']})")
            print(f"     Mot kibouchi : {p['mot']}")
            print(f"     Audio référencé : {p['audio_reference']}")
            print(f"     Similarité : {p['similarite']}")
        if len(problemes["audio_incorrect_kibouchi"]) > 20:
            print(f"   ... et {len(problemes['audio_incorrect_kibouchi']) - 20} autres")
        print()
    
    # Problème 5 : Audios non référencés mais existants
    if problemes["audio_non_reference"]:
        print(f"💡 AUDIOS EXISTANTS MAIS NON RÉFÉRENCÉS : {len(problemes['audio_non_reference'])}")
        for p in problemes["audio_non_reference"][:20]:
            print(f"   • {p['french']} ({p['category']}) - {p['langue']}")
            print(f"     Mot : {p['mot']}")
            print(f"     Fichier trouvé : {p['fichier_trouve']}")
            print(f"     Similarité : {p['similarite']}")
        if len(problemes["audio_non_reference"]) > 20:
            print(f"   ... et {len(problemes['audio_non_reference']) - 20} autres")
        print()
    
    # Sauvegarder le rapport complet
    print("=" * 80)
    print("Sauvegarde du rapport complet...")
    
    with open('/app/RAPPORT_CORRESPONDANCE_AUDIOS.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RAPPORT COMPLET - CORRESPONDANCE MOTS <-> AUDIOS\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Audios corrects : {problemes['audio_ok']}\n\n")
        
        if problemes["audio_manquant_shimaore"]:
            f.write(f"\n❌ AUDIOS MANQUANTS SHIMAORÉ ({len(problemes['audio_manquant_shimaore'])}):\n")
            for p in problemes["audio_manquant_shimaore"]:
                f.write(f"  • {p['french']} ({p['category']}) - {p['mot']}\n")
                if 'audio_reference' in p:
                    f.write(f"    Référencé : {p['audio_reference']}\n")
        
        if problemes["audio_manquant_kibouchi"]:
            f.write(f"\n❌ AUDIOS MANQUANTS KIBOUCHI ({len(problemes['audio_manquant_kibouchi'])}):\n")
            for p in problemes["audio_manquant_kibouchi"]:
                f.write(f"  • {p['french']} ({p['category']}) - {p['mot']}\n")
                if 'audio_reference' in p:
                    f.write(f"    Référencé : {p['audio_reference']}\n")
        
        if problemes["audio_incorrect_shimaore"]:
            f.write(f"\n⚠️  AUDIOS MAL NOMMÉS SHIMAORÉ ({len(problemes['audio_incorrect_shimaore'])}):\n")
            for p in problemes["audio_incorrect_shimaore"]:
                f.write(f"  • {p['french']} ({p['category']})\n")
                f.write(f"    Mot : {p['mot']}\n")
                f.write(f"    Audio : {p['audio_reference']} (similarité: {p['similarite']})\n")
        
        if problemes["audio_incorrect_kibouchi"]:
            f.write(f"\n⚠️  AUDIOS MAL NOMMÉS KIBOUCHI ({len(problemes['audio_incorrect_kibouchi'])}):\n")
            for p in problemes["audio_incorrect_kibouchi"]:
                f.write(f"  • {p['french']} ({p['category']})\n")
                f.write(f"    Mot : {p['mot']}\n")
                f.write(f"    Audio : {p['audio_reference']} (similarité: {p['similarite']})\n")
        
        if problemes["audio_non_reference"]:
            f.write(f"\n💡 AUDIOS NON RÉFÉRENCÉS ({len(problemes['audio_non_reference'])}):\n")
            for p in problemes["audio_non_reference"]:
                f.write(f"  • {p['french']} ({p['category']}) - {p['langue']}\n")
                f.write(f"    Mot : {p['mot']}\n")
                f.write(f"    Fichier : {p['fichier_trouve']} (similarité: {p['similarite']})\n")
    
    print("✅ Rapport complet sauvegardé : /app/RAPPORT_CORRESPONDANCE_AUDIOS.txt")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
