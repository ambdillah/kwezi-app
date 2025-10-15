#!/usr/bin/env python3
"""
Correction des 10 erreurs audio critiques identifiées
Phase 1 - Corrections Urgentes
"""

from pymongo import MongoClient
from datetime import datetime

def main():
    print("=" * 80)
    print("CORRECTION DES ERREURS AUDIO CRITIQUES - PHASE 1")
    print("=" * 80)
    print()
    
    client = MongoClient("mongodb://localhost:27017")
    db = client["mayotte_app"]
    
    corrections = []
    
    # ============================================================================
    # CORRECTION 1 & 2 : INVERSION TOITURE/TORCHE (Maison - Shimaoré)
    # ============================================================================
    print("🔧 Correction 1-2 : Inversion Toiture/Torche...")
    
    toiture = db.words.find_one({"french": "Toiture"})
    torche = db.words.find_one({"french": "Torche locale"})
    
    if toiture and torche:
        # Inverser les audios
        toiture_audio = toiture.get('audio_filename_shimaore') or toiture.get('shimoare_audio_filename')
        torche_audio = torche.get('audio_filename_shimaore') or torche.get('shimoare_audio_filename')
        
        # Mettre à jour Toiture avec l'audio correct
        db.words.update_one(
            {"_id": toiture["_id"]},
            {"$set": {
                "audio_filename_shimaore": "Outro.m4a",
                "shimoare_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Toiture : Gandilé_poutroumax.m4a → Outro.m4a")
        
        # Mettre à jour Torche locale avec l'audio correct
        db.words.update_one(
            {"_id": torche["_id"]},
            {"$set": {
                "audio_filename_shimaore": "Gandilé_poutroumax.m4a",
                "shimoare_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Torche locale : Outro.m4a → Gandilé_poutroumax.m4a")
    
    # ============================================================================
    # CORRECTION 3 : INVERSION NEUF/DIX-NEUF (Nombres - Kibouchi)
    # ============================================================================
    print("🔧 Correction 3 : Inversion Neuf/Dix-neuf...")
    
    neuf = db.words.find_one({"french": "Neuf"})
    dix_neuf = db.words.find_one({"french": "Dix-neuf"})
    
    if neuf and dix_neuf:
        # Inverser les audios
        db.words.update_one(
            {"_id": neuf["_id"]},
            {"$set": {
                "audio_filename_kibouchi": "Civi.m4a",
                "kibouchi_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Neuf : Foulou civi ambi.m4a → Civi.m4a")
        
        db.words.update_one(
            {"_id": dix_neuf["_id"]},
            {"$set": {
                "audio_filename_kibouchi": "Foulou civi ambi.m4a",
                "kibouchi_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Dix-neuf : Civi.m4a → Foulou civi ambi.m4a")
    
    # ============================================================================
    # CORRECTION 4 : PAPA - Audio shimaoré (devrait être simple)
    # ============================================================================
    print("🔧 Correction 4 : Papa audio shimaoré...")
    
    papa = db.words.find_one({"french": "Papa"})
    if papa:
        # Pour l'instant, on garde Baba héli-bé.m4a car c'est l'audio qui existe
        # L'utilisateur devra fournir Baba.m4a simple s'il veut le changer
        # On documente juste que c'est un audio composé
        corrections.append("⚠️  Papa : Baba héli-bé.m4a (audio composé, à remplacer par Baba.m4a si disponible)")
    
    # ============================================================================
    # CORRECTION 5-14 : LIER LES AUDIOS NON RÉFÉRENCÉS (10 fichiers)
    # ============================================================================
    print("🔧 Corrections 5-14 : Lier les audios existants non référencés...")
    
    # 5. Fâché (kibouchi) - méloukou → Méloukou.m4a
    fache = db.words.find_one({"french": "Fâché"})
    if fache:
        db.words.update_one(
            {"_id": fache["_id"]},
            {"$set": {
                "audio_filename_kibouchi": "Méloukou.m4a",
                "kibouchi_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Fâché (kibouchi) : Ajout Méloukou.m4a")
    
    # 6. Fourmis (shimaoré) - tsoussou → Tsoussou.m4a
    fourmis = db.words.find_one({"french": "Fourmis"})
    if fourmis:
        db.words.update_one(
            {"_id": fourmis["_id"]},
            {"$set": {
                "audio_filename_shimaore": "Tsoussou.m4a",
                "shimoare_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Fourmis (shimaoré) : Ajout Tsoussou.m4a")
    
    # 7. Tante maternelle (kibouchi) - nindri heli bé → Ninfndri héli_bé.m4a
    tante_mat = db.words.find_one({"french": "Tante maternelle"})
    if tante_mat:
        db.words.update_one(
            {"_id": tante_mat["_id"]},
            {"$set": {
                "audio_filename_kibouchi": "Ninfndri héli_bé.m4a",
                "kibouchi_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Tante maternelle (kibouchi) : Ajout Ninfndri héli_bé.m4a")
    
    # 8. Torche locale (kibouchi) - déjà traité dans correction 2, mais ajouter kibouchi
    if torche:
        db.words.update_one(
            {"_id": torche["_id"]},
            {"$set": {
                "audio_filename_kibouchi": "Gandili-poutroumax.m4a",
                "kibouchi_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Torche locale (kibouchi) : Ajout Gandili-poutroumax.m4a")
    
    # 9. Quatre-vingt-dix (kibouchi) - civiampulou → Civiampoulou.m4a
    quatre_vingt_dix = db.words.find_one({"french": "Quatre-vingt-dix"})
    if quatre_vingt_dix:
        db.words.update_one(
            {"_id": quatre_vingt_dix["_id"]},
            {"$set": {
                "audio_filename_kibouchi": "Civiampoulou.m4a",
                "kibouchi_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Quatre-vingt-dix (kibouchi) : Ajout Civiampoulou.m4a")
    
    # 10. S'asseoir (shimaoré) - ouketsi → Ouketsi.m4a
    asseoir = db.words.find_one({"french": "S'asseoir"})
    if asseoir:
        db.words.update_one(
            {"_id": asseoir["_id"]},
            {"$set": {
                "audio_filename_shimaore": "Ouketsi.m4a",
                "shimoare_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ S'asseoir (shimaoré) : Ajout Ouketsi.m4a")
    
    # 11. Sembler (kibouchi) - mamhiragna → Mampihiragna.m4a
    sembler = db.words.find_one({"french": "Sembler"})
    if sembler:
        db.words.update_one(
            {"_id": sembler["_id"]},
            {"$set": {
                "audio_filename_kibouchi": "Mampihiragna.m4a",
                "kibouchi_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Sembler (kibouchi) : Ajout Mampihiragna.m4a")
    
    # 12. Vomir (shimaoré) - ou raviha → Ouraviha.m4a
    vomir = db.words.find_one({"french": "Vomir"})
    if vomir:
        db.words.update_one(
            {"_id": vomir["_id"]},
            {"$set": {
                "audio_filename_shimaore": "Ouraviha.m4a",
                "shimoare_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Vomir (shimaoré) : Ajout Ouraviha.m4a")
    
    # 13. Écouter (kibouchi) - mitangréngni → Mitandréngni.m4a
    ecouter = db.words.find_one({"french": "Écouter"})
    if ecouter:
        db.words.update_one(
            {"_id": ecouter["_id"]},
            {"$set": {
                "audio_filename_kibouchi": "Mitandréngni.m4a",
                "kibouchi_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Écouter (kibouchi) : Ajout Mitandréngni.m4a")
    
    # 14. Éplucher (shimaoré) - oukouwa → Oukouwa.m4a
    eplucher = db.words.find_one({"french": "Éplucher"})
    if eplucher:
        db.words.update_one(
            {"_id": eplucher["_id"]},
            {"$set": {
                "audio_filename_shimaore": "Oukouwa.m4a",
                "shimoare_has_audio": True,
                "audio_updated_at": datetime.utcnow()
            }}
        )
        corrections.append("✅ Éplucher (shimaoré) : Ajout Oukouwa.m4a")
    
    # ============================================================================
    # AFFICHAGE DES RÉSULTATS
    # ============================================================================
    print()
    print("=" * 80)
    print("RÉSULTATS DES CORRECTIONS")
    print("=" * 80)
    print()
    
    for i, correction in enumerate(corrections, 1):
        print(f"{i}. {correction}")
    
    print()
    print(f"✅ Total de corrections appliquées : {len(corrections)}")
    print()
    print("=" * 80)
    
    # Sauvegarder le rapport
    with open('/app/RAPPORT_CORRECTIONS_PHASE1.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RAPPORT DES CORRECTIONS - PHASE 1\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        
        for i, correction in enumerate(corrections, 1):
            f.write(f"{i}. {correction}\n")
        
        f.write(f"\n✅ Total : {len(corrections)} corrections appliquées\n")
    
    print("📄 Rapport sauvegardé : /app/RAPPORT_CORRECTIONS_PHASE1.txt")
    print()

if __name__ == "__main__":
    main()
