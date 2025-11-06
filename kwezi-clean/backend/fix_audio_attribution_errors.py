#!/usr/bin/env python3
"""
Script pour corriger les erreurs d'attribution d'audios dans la catégorie nourriture
"""

from pymongo import MongoClient
import os

mongo_url = "mongodb://localhost:27017/"
client = MongoClient(mongo_url)
db = client['mayotte_app']
words_collection = db['words']

print("=" * 80)
print("CORRECTION DES ERREURS D'ATTRIBUTION AUDIO - NOURRITURE")
print("=" * 80)

errors = []

# Correction 1: Ail
print("\n1️⃣ Correction 'Ail':")
ail = words_collection.find_one({'french': 'Ail', 'category': 'nourriture'})
if ail:
    print(f"   Trouvé: {ail.get('french')}")
    print(f"   Shimaoré actuel: {ail.get('shimaore')}")
    print(f"   Audio actuel: {ail.get('shimoare_audio_filename')}")
    print(f"   → Doit être: Chouroungou voudjé.m4a")
    
    # Vérifier que le fichier existe
    audio_path = "/app/frontend/assets/audio/nourriture/Chouroungou voudjé.m4a"
    if os.path.exists(audio_path):
        result = words_collection.update_one(
            {'_id': ail['_id']},
            {'$set': {'shimoare_audio_filename': 'Chouroungou voudjé.m4a'}}
        )
        if result.modified_count > 0:
            print(f"   ✅ Audio corrigé")
        else:
            errors.append("Ail: Aucune modification effectuée")
            print(f"   ⚠️ Aucune modification")
    else:
        errors.append(f"Ail: Fichier audio non trouvé: {audio_path}")
        print(f"   ❌ Fichier audio non trouvé")
else:
    errors.append("Ail: Mot non trouvé")
    print(f"   ❌ Mot non trouvé")

# Correction 2: Ciboulette
print("\n2️⃣ Correction 'Ciboulette':")
ciboulette = words_collection.find_one({'french': 'Ciboulette', 'category': 'nourriture'})
if ciboulette:
    print(f"   Trouvé: {ciboulette.get('french')}")
    print(f"   Shimaoré actuel: {ciboulette.get('shimaore')}")
    print(f"   Audio actuel: {ciboulette.get('shimoare_audio_filename')}")
    print(f"   → Doit être shimaoré: chouroungou mani")
    print(f"   → Doit être audio: Chouroungou mani.m4a")
    
    # Vérifier que le fichier existe
    audio_path = "/app/frontend/assets/audio/nourriture/Chouroungou mani.m4a"
    if os.path.exists(audio_path):
        result = words_collection.update_one(
            {'_id': ciboulette['_id']},
            {'$set': {
                'shimaore': 'chouroungou mani',
                'shimoare_audio_filename': 'Chouroungou mani.m4a'
            }}
        )
        if result.modified_count > 0:
            print(f"   ✅ Shimaoré et audio corrigés")
        else:
            errors.append("Ciboulette: Aucune modification effectuée")
            print(f"   ⚠️ Aucune modification")
    else:
        errors.append(f"Ciboulette: Fichier audio non trouvé: {audio_path}")
        print(f"   ❌ Fichier audio non trouvé")
else:
    errors.append("Ciboulette: Mot non trouvé")
    print(f"   ❌ Mot non trouvé")

# Correction 3: Mangue
print("\n3️⃣ Correction 'Mangue':")
mangue = words_collection.find_one({'french': 'Mangue', 'category': 'nourriture'})
if mangue:
    print(f"   Trouvé: {mangue.get('french')}")
    print(f"   Shimaoré actuel: {mangue.get('shimaore')}")
    print(f"   Audio actuel: {mangue.get('shimoare_audio_filename')}")
    print(f"   → Doit être audio: Manga.m4a")
    
    # Vérifier que le fichier existe
    audio_path = "/app/frontend/assets/audio/nourriture/Manga.m4a"
    if os.path.exists(audio_path):
        result = words_collection.update_one(
            {'_id': mangue['_id']},
            {'$set': {'shimoare_audio_filename': 'Manga.m4a'}}
        )
        if result.modified_count > 0:
            print(f"   ✅ Audio corrigé")
        else:
            errors.append("Mangue: Aucune modification effectuée")
            print(f"   ⚠️ Aucune modification")
    else:
        errors.append(f"Mangue: Fichier audio non trouvé: {audio_path}")
        print(f"   ❌ Fichier audio non trouvé")
else:
    errors.append("Mangue: Mot non trouvé")
    print(f"   ❌ Mot non trouvé")

# Vérification finale
print("\n" + "=" * 80)
print("VÉRIFICATION FINALE:")
print("=" * 80)

# Re-vérifier les 3 mots
mots_a_verifier = ['Ail', 'Ciboulette', 'Mangue']
for mot in mots_a_verifier:
    word = words_collection.find_one({'french': mot, 'category': 'nourriture'})
    if word:
        print(f"\n✅ {word.get('french')}")
        print(f"   Shimaoré: {word.get('shimaore')}")
        print(f"   Audio: {word.get('shimoare_audio_filename')}")
        
        # Vérifier le fichier
        audio_file = word.get('shimoare_audio_filename')
        if audio_file:
            audio_path = f"/app/frontend/assets/audio/nourriture/{audio_file}"
            if os.path.exists(audio_path):
                size = os.path.getsize(audio_path) / 1024
                print(f"   Fichier: ✅ Présent ({size:.1f} KB)")
            else:
                print(f"   Fichier: ❌ MANQUANT")
                errors.append(f"{mot}: Fichier audio manquant après correction")

# Résultat final
print("\n" + "=" * 80)
if errors:
    print("❌ SCRIPT TERMINÉ AVEC ERREURS")
    print("=" * 80)
    for error in errors:
        print(f"   • {error}")
else:
    print("✅ AUCUNE ERREUR - Toutes les corrections appliquées!")
    print("=" * 80)
