#!/usr/bin/env python3
"""
Diagnostic complet du système audio
Vérifie la cohérence entre base de données et fichiers physiques
"""

from pymongo import MongoClient
import os
from pathlib import Path

def main():
    print("=" * 80)
    print("DIAGNOSTIC COMPLET DU SYSTÈME AUDIO")
    print("=" * 80)
    print()
    
    client = MongoClient("mongodb://localhost:27017")
    db = client["mayotte_app"]
    
    audio_base = "/app/frontend/assets/audio"
    
    problemes = {
        'fichier_manquant': [],
        'reference_invalide': [],
        'dual_system_manquant': []
    }
    
    # Statistiques
    stats = {
        'total_mots': 0,
        'dual_audio_actif': 0,
        'shimaoré_ok': 0,
        'kibouchi_ok': 0,
        'shimaoré_ko': 0,
        'kibouchi_ko': 0
    }
    
    print("Analyse en cours...")
    print()
    
    words = list(db.words.find({}))
    stats['total_mots'] = len(words)
    
    for word in words:
        french = word.get('french', 'N/A')
        category = word.get('category', 'inconnu')
        word_id = str(word.get('_id'))
        
        # Vérifier dual_audio_system
        if not word.get('dual_audio_system'):
            problemes['dual_system_manquant'].append({
                'french': french,
                'category': category,
                'id': word_id
            })
        else:
            stats['dual_audio_actif'] += 1
        
        # Vérifier shimaoré
        shim_audio = word.get('audio_filename_shimaore') or word.get('shimoare_audio_filename')
        if shim_audio:
            # Vérifier si le fichier existe
            audio_path = os.path.join(audio_base, category, shim_audio)
            if os.path.exists(audio_path):
                stats['shimaoré_ok'] += 1
            else:
                stats['shimaoré_ko'] += 1
                problemes['fichier_manquant'].append({
                    'french': french,
                    'langue': 'shimaoré',
                    'fichier': shim_audio,
                    'category': category,
                    'chemin': audio_path
                })
        
        # Vérifier kibouchi
        kib_audio = word.get('audio_filename_kibouchi') or word.get('kibouchi_audio_filename')
        if kib_audio:
            # Vérifier si le fichier existe
            audio_path = os.path.join(audio_base, category, kib_audio)
            if os.path.exists(audio_path):
                stats['kibouchi_ok'] += 1
            else:
                stats['kibouchi_ko'] += 1
                problemes['fichier_manquant'].append({
                    'french': french,
                    'langue': 'kibouchi',
                    'fichier': kib_audio,
                    'category': category,
                    'chemin': audio_path
                })
        
        # Vérifier références invalides (None, "None", vides)
        if shim_audio and (shim_audio == 'None' or shim_audio.strip() == ''):
            problemes['reference_invalide'].append({
                'french': french,
                'langue': 'shimaoré',
                'valeur': repr(shim_audio),
                'category': category
            })
        
        if kib_audio and (kib_audio == 'None' or kib_audio.strip() == ''):
            problemes['reference_invalide'].append({
                'french': french,
                'langue': 'kibouchi',
                'valeur': repr(kib_audio),
                'category': category
            })
    
    # AFFICHAGE DES RÉSULTATS
    print("=" * 80)
    print("STATISTIQUES GLOBALES")
    print("=" * 80)
    print()
    print(f"Total de mots               : {stats['total_mots']}")
    print(f"Dual audio system activé    : {stats['dual_audio_actif']}")
    print()
    print(f"Audio shimaoré OK           : {stats['shimaoré_ok']}")
    print(f"Audio shimaoré KO           : {stats['shimaoré_ko']}")
    print()
    print(f"Audio kibouchi OK           : {stats['kibouchi_ok']}")
    print(f"Audio kibouchi KO           : {stats['kibouchi_ko']}")
    print()
    print("=" * 80)
    print("PROBLÈMES DÉTECTÉS")
    print("=" * 80)
    print()
    
    # Problème 1 : Fichiers manquants
    if problemes['fichier_manquant']:
        print(f"❌ FICHIERS AUDIO MANQUANTS ({len(problemes['fichier_manquant'])})")
        print("-" * 80)
        for i, p in enumerate(problemes['fichier_manquant'][:20], 1):  # Limiter à 20
            print(f"{i}. {p['french']} ({p['langue']})")
            print(f"   Fichier: {p['fichier']}")
            print(f"   Catégorie: {p['category']}")
            print(f"   Chemin: {p['chemin']}")
            print()
        
        if len(problemes['fichier_manquant']) > 20:
            print(f"... et {len(problemes['fichier_manquant']) - 20} autres\n")
    
    # Problème 2 : Références invalides
    if problemes['reference_invalide']:
        print(f"⚠️  RÉFÉRENCES AUDIO INVALIDES ({len(problemes['reference_invalide'])})")
        print("-" * 80)
        for p in problemes['reference_invalide']:
            print(f"• {p['french']} ({p['langue']}) - Valeur: {p['valeur']}")
        print()
    
    # Problème 3 : dual_audio_system manquant
    if problemes['dual_system_manquant']:
        print(f"⚠️  DUAL AUDIO SYSTEM NON ACTIVÉ ({len(problemes['dual_system_manquant'])})")
        print("-" * 80)
        for p in problemes['dual_system_manquant'][:10]:  # Limiter à 10
            print(f"• {p['french']} ({p['category']})")
        
        if len(problemes['dual_system_manquant']) > 10:
            print(f"... et {len(problemes['dual_system_manquant']) - 10} autres\n")
    
    print()
    print("=" * 80)
    print("DIAGNOSTIC TERMINÉ")
    print("=" * 80)
    
    # Sauvegarder le rapport
    with open('/app/DIAGNOSTIC_AUDIO_COMPLET.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("DIAGNOSTIC COMPLET DU SYSTÈME AUDIO\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("STATISTIQUES:\n")
        f.write(f"Total mots: {stats['total_mots']}\n")
        f.write(f"Dual audio actif: {stats['dual_audio_actif']}\n")
        f.write(f"Shimaoré OK: {stats['shimaoré_ok']}\n")
        f.write(f"Shimaoré KO: {stats['shimaoré_ko']}\n")
        f.write(f"Kibouchi OK: {stats['kibouchi_ok']}\n")
        f.write(f"Kibouchi KO: {stats['kibouchi_ko']}\n\n")
        
        f.write(f"FICHIERS MANQUANTS: {len(problemes['fichier_manquant'])}\n")
        for p in problemes['fichier_manquant']:
            f.write(f"  - {p['french']} ({p['langue']}): {p['fichier']}\n")
        
        f.write(f"\nRÉFÉRENCES INVALIDES: {len(problemes['reference_invalide'])}\n")
        for p in problemes['reference_invalide']:
            f.write(f"  - {p['french']} ({p['langue']}): {p['valeur']}\n")
    
    print("📄 Rapport sauvegardé : /app/DIAGNOSTIC_AUDIO_COMPLET.txt")

if __name__ == "__main__":
    main()
