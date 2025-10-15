#!/usr/bin/env python3
"""
CORRECTION CRITIQUE : Verbes kibouchi au présent
Règle correcte : Au PRÉSENT, les verbes kibouchi restent à l'INFINITIF (avec le "m")
"""

from pymongo import MongoClient
from datetime import datetime
import json

def main():
    print("=" * 80)
    print("CORRECTION DES VERBES KIBOUCHI AU PRÉSENT")
    print("⚠️  RÈGLE : Au présent, garder le verbe à l'infinitif (avec 'm')")
    print("=" * 80)
    print()
    
    # Connexion
    client = MongoClient("mongodb://localhost:27017")
    db = client["mayotte_app"]
    
    # 1. BACKUP des phrases au présent
    print("1. CRÉATION DU BACKUP...")
    backup_sentences = list(db.sentences.find({"tense": "present"}))
    
    with open('/app/backend/backup_present_kibouchi.json', 'w', encoding='utf-8') as f:
        json.dump(backup_sentences, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"   ✅ Backup créé : {len(backup_sentences)} phrases sauvegardées")
    print()
    
    # 2. Récupérer tous les verbes avec leurs infinitifs kibouchi
    print("2. CHARGEMENT DES VERBES À L'INFINITIF...")
    verbes = list(db.words.find(
        {"category": "verbes", "kibouchi": {"$exists": True}},
        {"french": 1, "kibouchi": 1}
    ))
    
    # Créer un mapping français → kibouchi infinitif
    verbe_mapping = {}
    for v in verbes:
        french = v.get('french', '').lower()
        kibouchi_inf = v.get('kibouchi', '')
        if french and kibouchi_inf:
            verbe_mapping[french] = kibouchi_inf
    
    print(f"   ✅ {len(verbe_mapping)} verbes chargés")
    print()
    
    # 3. Analyser les phrases au présent
    print("3. ANALYSE DES PHRASES AU PRÉSENT...")
    sentences_present = list(db.sentences.find(
        {"tense": "present"},
        {"french": 1, "kibouchi": 1, "kibouchi_words": 1, "verb": 1}
    ))
    
    corrections_needed = []
    
    for sent in sentences_present:
        french_sentence = sent.get('french', '').lower()
        current_kib_words = sent.get('kibouchi_words', [])
        
        if len(current_kib_words) >= 2:
            current_verb_kib = current_kib_words[1]
            
            # Chercher le verbe français correspondant
            # On cherche dans le mapping si le verbe actuel correspond à un infinitif sans "m"
            found_infinitif = None
            for verb_fr, infinitif in verbe_mapping.items():
                # Si l'infinitif commence par "m" et qu'en enlevant le "m" ça correspond au verbe actuel
                if infinitif.lower().startswith('m'):
                    infinitif_sans_m = infinitif[1:].lower()
                    if current_verb_kib.lower() == infinitif_sans_m:
                        found_infinitif = infinitif
                        break
            
            # Vérifier aussi si le verbe actuel est déjà l'infinitif correct
            if found_infinitif and current_verb_kib != found_infinitif:
                corrections_needed.append({
                    'sentence_id': sent['_id'],
                    'french': sent.get('french'),
                    'current_verb': current_verb_kib,
                    'correct_verb': found_infinitif,
                    'current_words': current_kib_words,
                    'current_sentence': sent.get('kibouchi')
                })
    
    print(f"   📊 {len(corrections_needed)} phrases à corriger")
    print()
    
    if not corrections_needed:
        print("✅ Aucune correction nécessaire ! Les phrases sont déjà correctes.")
        return
    
    # 4. Afficher quelques exemples
    print("4. EXEMPLES DE CORRECTIONS À EFFECTUER (5 premiers):")
    print("-" * 80)
    for i, corr in enumerate(corrections_needed[:5], 1):
        print(f"{i}. {corr['french']}")
        print(f"   Verbe actuel : {corr['current_verb']}")
        print(f"   Verbe correct : {corr['correct_verb']}")
        print(f"   Mots actuels : {corr['current_words']}")
        print()
    
    # 5. Demander confirmation
    print("=" * 80)
    print(f"⚠️  ATTENTION : {len(corrections_needed)} phrases vont être modifiées")
    print("=" * 80)
    response = input("\nVoulez-vous procéder aux corrections ? (oui/non) : ")
    
    if response.lower() != 'oui':
        print("\n❌ Correction annulée par l'utilisateur")
        return
    
    # 6. Appliquer les corrections
    print("\n5. APPLICATION DES CORRECTIONS...")
    corrections_applied = 0
    
    for corr in corrections_needed:
        # Reconstruire la phrase et les mots avec le bon infinitif
        new_words = corr['current_words'].copy()
        if len(new_words) > 1:
            new_words[1] = corr['correct_verb']  # Remplacer le verbe
        
        # Reconstruire la phrase complète
        new_sentence = " ".join(new_words)
        
        # Mettre à jour dans la base
        result = db.sentences.update_one(
            {"_id": corr['sentence_id']},
            {"$set": {
                "kibouchi": new_sentence,
                "kibouchi_words": new_words,
                "updated_at": datetime.utcnow(),
                "correction_note": "Verbe kibouchi au présent corrigé en infinitif"
            }}
        )
        
        if result.modified_count > 0:
            corrections_applied += 1
    
    print(f"   ✅ {corrections_applied} phrases corrigées avec succès")
    print()
    
    # 7. Vérification finale
    print("6. VÉRIFICATION FINALE...")
    test_sentences = list(db.sentences.find({"tense": "present"}).limit(5))
    print("   Exemples de phrases corrigées :")
    for sent in test_sentences:
        print(f"   • {sent.get('french')} → {sent.get('kibouchi')}")
    
    print()
    print("=" * 80)
    print("✅ CORRECTION TERMINÉE AVEC SUCCÈS")
    print("=" * 80)
    print()
    print(f"📊 Résumé :")
    print(f"  • Phrases analysées : {len(sentences_present)}")
    print(f"  • Phrases corrigées : {corrections_applied}")
    print(f"  • Backup sauvegardé : backup_present_kibouchi.json")
    print()

if __name__ == "__main__":
    main()
