#!/usr/bin/env python3
"""
Intégration automatique des audios d'expressions
Match les fichiers audio avec les mots de la base de données
"""

from pymongo import MongoClient
import os
from difflib import SequenceMatcher
from datetime import datetime

def similarity(a, b):
    """Calcule la similarité entre deux chaînes"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def normalize_text(text):
    """Normalise le texte pour la comparaison"""
    return text.lower().strip().replace("'", "'").replace("'", "'")

def main():
    print("=" * 80)
    print("INTÉGRATION AUTOMATIQUE DES AUDIOS EXPRESSIONS")
    print("=" * 80)
    print()
    
    client = MongoClient("mongodb://localhost:27017")
    db = client["mayotte_app"]
    
    # Récupérer tous les mots de la catégorie expressions
    expressions = list(db.words.find({"category": "expressions"}))
    print(f"📊 Mots expressions dans la base : {len(expressions)}")
    
    # Lister tous les fichiers audio
    audio_dir = "/app/frontend/assets/audio/expressions"
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
    print(f"🎵 Fichiers audio disponibles : {len(audio_files)}")
    print()
    
    matched = 0
    updated_shimaoré = 0
    updated_kibouchi = 0
    no_match = []
    
    # Pour chaque mot, chercher les fichiers audio correspondants
    for word in expressions:
        french = word.get('french', '')
        shimaore = word.get('shimaore', '')
        kibouchi = word.get('kibouchi', '')
        word_id = word['_id']
        
        # Préparer les mises à jour
        updates = {}
        
        # Chercher audio shimaoré
        if shimaore:
            shimaore_norm = normalize_text(shimaore)
            best_match_shim = None
            best_score_shim = 0.0
            
            for audio_file in audio_files:
                audio_name = audio_file.replace('.m4a', '')
                audio_norm = normalize_text(audio_name)
                
                # Calcul de similarité
                score = similarity(shimaore_norm, audio_norm)
                
                # Match exact ou très proche
                if score > best_score_shim:
                    best_score_shim = score
                    best_match_shim = audio_file
            
            # Si match suffisant (>= 0.8), on l'utilise
            if best_match_shim and best_score_shim >= 0.80:
                updates['audio_filename_shimaore'] = best_match_shim
                updates['shimoare_audio_filename'] = best_match_shim
                updates['shimoare_has_audio'] = True
                updated_shimaoré += 1
        
        # Chercher audio kibouchi
        if kibouchi:
            kibouchi_norm = normalize_text(kibouchi)
            best_match_kib = None
            best_score_kib = 0.0
            
            for audio_file in audio_files:
                audio_name = audio_file.replace('.m4a', '')
                audio_norm = normalize_text(audio_name)
                
                # Calcul de similarité
                score = similarity(kibouchi_norm, audio_norm)
                
                # Match exact ou très proche
                if score > best_score_kib:
                    best_score_kib = score
                    best_match_kib = audio_file
            
            # Si match suffisant (>= 0.8), on l'utilise
            if best_match_kib and best_score_kib >= 0.80:
                updates['audio_filename_kibouchi'] = best_match_kib
                updates['kibouchi_audio_filename'] = best_match_kib
                updates['kibouchi_has_audio'] = True
                updated_kibouchi += 1
        
        # Mettre à jour si on a trouvé au moins un audio
        if updates:
            updates['dual_audio_system'] = True
            updates['updated_at'] = datetime.utcnow()
            
            db.words.update_one(
                {"_id": word_id},
                {"$set": updates}
            )
            matched += 1
            print(f"✅ {french}")
            if 'audio_filename_shimaore' in updates:
                print(f"   Shimaoré : {shimaore} → {updates['audio_filename_shimaore']}")
            if 'audio_filename_kibouchi' in updates:
                print(f"   Kibouchi : {kibouchi} → {updates['audio_filename_kibouchi']}")
        else:
            no_match.append({
                'french': french,
                'shimaore': shimaore,
                'kibouchi': kibouchi
            })
    
    print()
    print("=" * 80)
    print("RÉSULTATS")
    print("=" * 80)
    print()
    print(f"✅ Mots mis à jour : {matched}/{len(expressions)}")
    print(f"   • Audios shimaoré ajoutés : {updated_shimaoré}")
    print(f"   • Audios kibouchi ajoutés : {updated_kibouchi}")
    print()
    
    if no_match:
        print(f"⚠️  Mots sans correspondance audio ({len(no_match)}) :")
        for item in no_match[:10]:  # Limiter à 10
            print(f"   • {item['french']} (shimaoré: {item['shimaore']}, kibouchi: {item['kibouchi']})")
        if len(no_match) > 10:
            print(f"   ... et {len(no_match) - 10} autres")
    
    print()
    print("=" * 80)
    
    # Rapport détaillé
    with open('/app/RAPPORT_INTEGRATION_EXPRESSIONS.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RAPPORT INTÉGRATION AUDIOS EXPRESSIONS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write(f"Fichiers audio disponibles : {len(audio_files)}\n")
        f.write(f"Mots expressions : {len(expressions)}\n")
        f.write(f"Mots mis à jour : {matched}\n")
        f.write(f"Audios shimaoré : {updated_shimaoré}\n")
        f.write(f"Audios kibouchi : {updated_kibouchi}\n\n")
        
        if no_match:
            f.write(f"Mots sans correspondance ({len(no_match)}) :\n")
            for item in no_match:
                f.write(f"  - {item['french']} : {item['shimaore']} / {item['kibouchi']}\n")
    
    print("📄 Rapport sauvegardé : /app/RAPPORT_INTEGRATION_EXPRESSIONS.txt")
    print()

if __name__ == "__main__":
    main()
