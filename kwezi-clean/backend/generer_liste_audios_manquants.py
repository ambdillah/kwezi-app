#!/usr/bin/env python3
"""
Génère la liste complète et exacte de tous les audios manquants
Format : Mot français | Shimaoré/Kibouchi | Nom fichier attendu
"""

from pymongo import MongoClient
import os

def main():
    print("=" * 80)
    print("GÉNÉRATION LISTE COMPLÈTE DES AUDIOS MANQUANTS")
    print("=" * 80)
    print()
    
    client = MongoClient("mongodb://localhost:27017")
    db = client["mayotte_app"]
    
    audio_base_path = "/app/frontend/assets/audio"
    
    # Récupérer tous les mots
    words = list(db.words.find({}).sort([("category", 1), ("french", 1)]))
    
    manquants_shimaore = []
    manquants_kibouchi = []
    
    for word in words:
        french = word.get('french', '')
        category = word.get('category', '')
        shimaore = word.get('shimaore', '')
        kibouchi = word.get('kibouchi', '')
        
        category_path = os.path.join(audio_base_path, category)
        
        # Vérifier shimaoré
        if shimaore:
            audio_ref_shim = word.get('audio_filename_shimaore') or word.get('shimoare_audio_filename')
            
            if audio_ref_shim:
                # Il y a une référence, vérifier si le fichier existe
                audio_path = os.path.join(category_path, audio_ref_shim)
                if not os.path.exists(audio_path):
                    manquants_shimaore.append({
                        'french': french,
                        'mot': shimaore,
                        'category': category,
                        'fichier': audio_ref_shim
                    })
            else:
                # Pas de référence audio du tout
                manquants_shimaore.append({
                    'french': french,
                    'mot': shimaore,
                    'category': category,
                    'fichier': f'{shimaore}.m4a'
                })
        
        # Vérifier kibouchi
        if kibouchi:
            audio_ref_kib = word.get('audio_filename_kibouchi') or word.get('kibouchi_audio_filename')
            
            if audio_ref_kib:
                # Il y a une référence, vérifier si le fichier existe
                audio_path = os.path.join(category_path, audio_ref_kib)
                if not os.path.exists(audio_path):
                    manquants_kibouchi.append({
                        'french': french,
                        'mot': kibouchi,
                        'category': category,
                        'fichier': audio_ref_kib
                    })
            else:
                # Pas de référence audio du tout
                manquants_kibouchi.append({
                    'french': french,
                    'mot': kibouchi,
                    'category': category,
                    'fichier': f'{kibouchi}.m4a'
                })
    
    # Affichage console
    print(f"📊 Total audios manquants : {len(manquants_shimaore) + len(manquants_kibouchi)}")
    print(f"   • Shimaoré : {len(manquants_shimaore)} fichiers")
    print(f"   • Kibouchi : {len(manquants_kibouchi)} fichiers")
    print()
    
    # Sauvegarder en format texte lisible
    with open('/app/LISTE_COMPLETE_AUDIOS_MANQUANTS.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("LISTE COMPLÈTE DES AUDIOS MANQUANTS - APPLICATION KWEZI\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"Total : {len(manquants_shimaore) + len(manquants_kibouchi)} fichiers audio à créer\n\n")
        
        # Section Shimaoré
        f.write("=" * 100 + "\n")
        f.write(f"AUDIOS MANQUANTS SHIMAORÉ ({len(manquants_shimaore)} fichiers)\n")
        f.write("=" * 100 + "\n\n")
        
        # Grouper par catégorie
        categories_shim = {}
        for item in manquants_shimaore:
            cat = item['category']
            if cat not in categories_shim:
                categories_shim[cat] = []
            categories_shim[cat].append(item)
        
        for cat in sorted(categories_shim.keys()):
            items = categories_shim[cat]
            f.write(f"\n📁 CATÉGORIE : {cat.upper()} ({len(items)} fichiers)\n")
            f.write("-" * 100 + "\n")
            for item in items:
                f.write(f"\nMot français : {item['french']}\n")
                f.write(f"Mot shimaoré : {item['mot']}\n")
                f.write(f"Fichier audio : {item['fichier']}\n")
                f.write(f"Dossier      : /frontend/assets/audio/{item['category']}/\n")
        
        # Section Kibouchi
        f.write("\n\n")
        f.write("=" * 100 + "\n")
        f.write(f"AUDIOS MANQUANTS KIBOUCHI ({len(manquants_kibouchi)} fichiers)\n")
        f.write("=" * 100 + "\n\n")
        
        # Grouper par catégorie
        categories_kib = {}
        for item in manquants_kibouchi:
            cat = item['category']
            if cat not in categories_kib:
                categories_kib[cat] = []
            categories_kib[cat].append(item)
        
        for cat in sorted(categories_kib.keys()):
            items = categories_kib[cat]
            f.write(f"\n📁 CATÉGORIE : {cat.upper()} ({len(items)} fichiers)\n")
            f.write("-" * 100 + "\n")
            for item in items:
                f.write(f"\nMot français : {item['french']}\n")
                f.write(f"Mot kibouchi : {item['mot']}\n")
                f.write(f"Fichier audio : {item['fichier']}\n")
                f.write(f"Dossier      : /frontend/assets/audio/{item['category']}/\n")
    
    print("✅ Fichier texte créé : /app/LISTE_COMPLETE_AUDIOS_MANQUANTS.txt")
    
    # Sauvegarder en format CSV pour Excel
    with open('/app/LISTE_COMPLETE_AUDIOS_MANQUANTS.csv', 'w', encoding='utf-8') as f:
        f.write("Langue,Catégorie,Mot_Français,Mot_Local,Nom_Fichier_Audio,Dossier\n")
        
        for item in manquants_shimaore:
            f.write(f"Shimaoré,{item['category']},{item['french']},{item['mot']},{item['fichier']},/frontend/assets/audio/{item['category']}/\n")
        
        for item in manquants_kibouchi:
            f.write(f"Kibouchi,{item['category']},{item['french']},{item['mot']},{item['fichier']},/frontend/assets/audio/{item['category']}/\n")
    
    print("✅ Fichier CSV créé : /app/LISTE_COMPLETE_AUDIOS_MANQUANTS.csv")
    
    # Créer une version JSON pour traitement automatique
    import json
    
    data = {
        'total': len(manquants_shimaore) + len(manquants_kibouchi),
        'shimaore': {
            'count': len(manquants_shimaore),
            'fichiers': manquants_shimaore
        },
        'kibouchi': {
            'count': len(manquants_kibouchi),
            'fichiers': manquants_kibouchi
        }
    }
    
    with open('/app/LISTE_COMPLETE_AUDIOS_MANQUANTS.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ Fichier JSON créé : /app/LISTE_COMPLETE_AUDIOS_MANQUANTS.json")
    
    print()
    print("=" * 80)
    print("STATISTIQUES PAR CATÉGORIE")
    print("=" * 80)
    print()
    
    # Stats shimaoré
    print("📊 SHIMAORÉ :")
    for cat in sorted(categories_shim.keys()):
        print(f"   • {cat:<20} : {len(categories_shim[cat]):>3} fichiers")
    
    print()
    
    # Stats kibouchi
    print("📊 KIBOUCHI :")
    for cat in sorted(categories_kib.keys()):
        print(f"   • {cat:<20} : {len(categories_kib[cat]):>3} fichiers")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
