#!/usr/bin/env python3
"""
Correction mwanagna → moinagna et intégration audio baba kibouchi
"""

from pymongo import MongoClient
from datetime import datetime

def main():
    print("=" * 80)
    print("CORRECTIONS : mwanagna → moinagna + baba kibouchi")
    print("=" * 80)
    print()
    
    client = MongoClient("mongodb://localhost:27017")
    db = client["mayotte_app"]
    
    corrections = []
    
    # ============================================================================
    # CORRECTION 1 : Frère - mwanagna → moinagna
    # ============================================================================
    print("🔧 Correction 1 : Frère...")
    
    frere = db.words.find_one({"french": "Frère"})
    if frere:
        old_shim = frere.get('shimaore', '')
        print(f"  Ancien shimaoré : {old_shim}")
        
        # Mettre à jour le mot ET créer un nouvel audio simple
        db.words.update_one(
            {"_id": frere["_id"]},
            {"$set": {
                "shimaore": "moinagna",
                "audio_filename_shimaore": "Moinagna.m4a",
                "shimoare_audio_filename": "Moinagna.m4a",
                "shimoare_has_audio": True,
                "updated_at": datetime.utcnow()
            }}
        )
        corrections.append(f"✅ Frère : '{old_shim}' → 'moinagna' (Audio: Moinagna.m4a)")
        print(f"  Nouveau shimaoré : moinagna")
        print(f"  Audio : Moinagna.m4a")
        print()
    
    # ============================================================================
    # CORRECTION 2 : Sœur - mwanagna → moinagna
    # ============================================================================
    print("🔧 Correction 2 : Sœur...")
    
    soeur = db.words.find_one({"french": "Sœur"})
    if soeur:
        old_shim = soeur.get('shimaore', '')
        print(f"  Ancien shimaoré : {old_shim}")
        
        # Mettre à jour le mot ET utiliser le même audio simple
        db.words.update_one(
            {"_id": soeur["_id"]},
            {"$set": {
                "shimaore": "moinagna",
                "audio_filename_shimaore": "Moinagna.m4a",
                "shimoare_audio_filename": "Moinagna.m4a",
                "shimoare_has_audio": True,
                "updated_at": datetime.utcnow()
            }}
        )
        corrections.append(f"✅ Sœur : '{old_shim}' → 'moinagna' (Audio: Moinagna.m4a)")
        print(f"  Nouveau shimaoré : moinagna")
        print(f"  Audio : Moinagna.m4a")
        print()
    
    # ============================================================================
    # CORRECTION 3 : Papa - vérifier que baba kibouchi a le bon audio
    # ============================================================================
    print("🔧 Correction 3 : Papa (baba kibouchi)...")
    
    papa = db.words.find_one({"french": "Papa"})
    if papa:
        current_kib_audio = papa.get('audio_filename_kibouchi') or papa.get('kibouchi_audio_filename')
        print(f"  Audio kibouchi actuel : {current_kib_audio}")
        
        # S'assurer que les DEUX formats de champs sont corrects
        db.words.update_one(
            {"_id": papa["_id"]},
            {"$set": {
                "audio_filename_kibouchi": "Baba k.m4a",
                "kibouchi_audio_filename": "Baba k.m4a",
                "kibouchi_has_audio": True,
                "updated_at": datetime.utcnow()
            }}
        )
        corrections.append(f"✅ Papa (baba kibouchi) : Audio confirmé/mis à jour → 'Baba k.m4a'")
        print(f"  Audio kibouchi : Baba k.m4a ✅")
        print()
    
    # ============================================================================
    # AFFICHAGE DES RÉSULTATS
    # ============================================================================
    print("=" * 80)
    print("RÉSUMÉ DES CORRECTIONS")
    print("=" * 80)
    print()
    
    for i, correction in enumerate(corrections, 1):
        print(f"{i}. {correction}")
    
    print()
    print(f"✅ Total : {len(corrections)} corrections appliquées")
    print()
    
    # ============================================================================
    # VÉRIFICATION
    # ============================================================================
    print("=" * 80)
    print("VÉRIFICATION")
    print("=" * 80)
    print()
    
    frere_check = db.words.find_one({"french": "Frère"})
    if frere_check:
        print("Frère :")
        print(f"  shimaoré : {frere_check.get('shimaore')}")
        print(f"  audio_filename_shimaore : {frere_check.get('audio_filename_shimaore')}")
        print(f"  shimoare_audio_filename : {frere_check.get('shimoare_audio_filename')}")
        print()
    
    soeur_check = db.words.find_one({"french": "Sœur"})
    if soeur_check:
        print("Sœur :")
        print(f"  shimaoré : {soeur_check.get('shimaore')}")
        print(f"  audio_filename_shimaore : {soeur_check.get('audio_filename_shimaore')}")
        print(f"  shimoare_audio_filename : {soeur_check.get('shimoare_audio_filename')}")
        print()
    
    papa_check = db.words.find_one({"french": "Papa"})
    if papa_check:
        print("Papa :")
        print(f"  kibouchi : {papa_check.get('kibouchi')}")
        print(f"  audio_filename_kibouchi : {papa_check.get('audio_filename_kibouchi')}")
        print(f"  kibouchi_audio_filename : {papa_check.get('kibouchi_audio_filename')}")
        print()
    
    print("=" * 80)
    
    # Sauvegarder le rapport
    with open('/app/RAPPORT_CORRECTIONS_MOINAGNA_BABA.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RAPPORT DES CORRECTIONS - mwanagna → moinagna + baba\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        
        for i, correction in enumerate(corrections, 1):
            f.write(f"{i}. {correction}\n")
        
        f.write(f"\n✅ Total : {len(corrections)} corrections appliquées\n")
    
    print("📄 Rapport sauvegardé : /app/RAPPORT_CORRECTIONS_MOINAGNA_BABA.txt")
    print()

if __name__ == "__main__":
    main()
