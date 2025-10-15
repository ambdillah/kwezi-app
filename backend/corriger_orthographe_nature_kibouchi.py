#!/usr/bin/env python3
"""
Correction des orthographes erronées dans la section Nature (Kibouchi)
D'après le tableau fourni par l'utilisateur
"""

from pymongo import MongoClient
from datetime import datetime

def main():
    print("=" * 80)
    print("CORRECTION ORTHOGRAPHE NATURE - KIBOUCHI")
    print("=" * 80)
    print()
    
    client = MongoClient("mongodb://localhost:27017")
    db = client["mayotte_app"]
    
    corrections = []
    
    # ============================================================================
    # CORRECTION 1 : Remplacer "youdi" par "voudi" (y -> v)
    # ============================================================================
    print("🔧 Correction 1-5 : Remplacement y -> v dans les arbres...")
    
    # arbre à pain : youdi ni frapé -> voudi ni frapé
    arbre_pain = db.words.find_one({"french": "arbre à pain"})
    if arbre_pain and arbre_pain.get('kibouchi'):
        old_kib = arbre_pain.get('kibouchi')
        new_kib = old_kib.replace('youdi', 'voudi')
        if old_kib != new_kib:
            db.words.update_one(
                {"_id": arbre_pain["_id"]},
                {"$set": {"kibouchi": new_kib}}
            )
            corrections.append(f"✅ arbre à pain : '{old_kib}' → '{new_kib}'")
            
            # Corriger aussi le nom du fichier audio
            old_audio = arbre_pain.get('audio_filename_kibouchi') or arbre_pain.get('kibouchi_audio_filename')
            if old_audio and 'youdi' in old_audio.lower():
                new_audio = old_audio.replace('Youdi', 'Voudi').replace('youdi', 'voudi')
                db.words.update_one(
                    {"_id": arbre_pain["_id"]},
                    {"$set": {"audio_filename_kibouchi": new_audio}}
                )
                corrections.append(f"   Audio : '{old_audio}' → '{new_audio}'")
    
    # baobab : youdi ni bouyou -> voudi ni bouyou
    baobab = db.words.find_one({"french": "baobab"})
    if baobab and baobab.get('kibouchi'):
        old_kib = baobab.get('kibouchi')
        new_kib = old_kib.replace('youdi', 'voudi')
        if old_kib != new_kib:
            db.words.update_one(
                {"_id": baobab["_id"]},
                {"$set": {"kibouchi": new_kib}}
            )
            corrections.append(f"✅ baobab : '{old_kib}' → '{new_kib}'")
            
            # Corriger aussi le nom du fichier audio
            old_audio = baobab.get('audio_filename_kibouchi') or baobab.get('kibouchi_audio_filename')
            if old_audio and 'youdi' in old_audio.lower():
                new_audio = old_audio.replace('Youdi', 'Voudi').replace('youdi', 'voudi')
                db.words.update_one(
                    {"_id": baobab["_id"]},
                    {"$set": {"audio_filename_kibouchi": new_audio}}
                )
                corrections.append(f"   Audio : '{old_audio}' → '{new_audio}'")
    
    # cocotier : youdi ni vwoniou -> voudi ni vwaniou (y->v et aussi o->a)
    cocotier = db.words.find_one({"french": "cocotier"})
    if cocotier and cocotier.get('kibouchi'):
        old_kib = cocotier.get('kibouchi')
        # Correction selon le tableau : vudi ni vwaniou
        new_kib = "vudi ni vwaniou"
        if old_kib != new_kib:
            db.words.update_one(
                {"_id": cocotier["_id"]},
                {"$set": {"kibouchi": new_kib}}
            )
            corrections.append(f"✅ cocotier : '{old_kib}' → '{new_kib}'")
            
            # Corriger le nom du fichier audio : Voudi ni vwaniou.m4a
            db.words.update_one(
                {"_id": cocotier["_id"]},
                {"$set": {"audio_filename_kibouchi": "Voudi ni vwaniou.m4a"}}
            )
            corrections.append(f"   Audio : 'Youdi ni vwoniou.m4a' → 'Voudi ni vwaniou.m4a'")
    
    # jacquier : youdi ni finéssi -> voudi ni finéssi
    jacquier = db.words.find_one({"french": "jacquier"})
    if jacquier and jacquier.get('kibouchi'):
        old_kib = jacquier.get('kibouchi')
        new_kib = old_kib.replace('youdi', 'voudi').replace('vudi', 'voudi')
        if old_kib != new_kib:
            db.words.update_one(
                {"_id": jacquier["_id"]},
                {"$set": {"kibouchi": new_kib}}
            )
            corrections.append(f"✅ jacquier : '{old_kib}' → '{new_kib}'")
            
            # Corriger aussi le nom du fichier audio
            old_audio = jacquier.get('audio_filename_kibouchi') or jacquier.get('kibouchi_audio_filename')
            if old_audio and 'youdi' in old_audio.lower():
                new_audio = old_audio.replace('Youdi', 'Voudi').replace('youdi', 'voudi')
                db.words.update_one(
                    {"_id": jacquier["_id"]},
                    {"$set": {"audio_filename_kibouchi": new_audio}}
                )
                corrections.append(f"   Audio : '{old_audio}' → '{new_audio}'")
    
    # manguier : youdi ni manga -> voudi ni manga
    manguier = db.words.find_one({"french": "manguier"})
    if manguier and manguier.get('kibouchi'):
        old_kib = manguier.get('kibouchi')
        new_kib = old_kib.replace('youdi', 'voudi').replace('vudi', 'voudi')
        if old_kib != new_kib:
            db.words.update_one(
                {"_id": manguier["_id"]},
                {"$set": {"kibouchi": new_kib}}
            )
            corrections.append(f"✅ manguier : '{old_kib}' → '{new_kib}'")
            
            # Corriger aussi le nom du fichier audio
            old_audio = manguier.get('audio_filename_kibouchi') or manguier.get('kibouchi_audio_filename')
            if old_audio and 'youdi' in old_audio.lower():
                new_audio = old_audio.replace('Youdi', 'Voudi').replace('youdi', 'voudi')
                db.words.update_one(
                    {"_id": manguier["_id"]},
                    {"$set": {"audio_filename_kibouchi": new_audio}}
                )
                corrections.append(f"   Audio : '{old_audio}' → '{new_audio}'")
    
    # ============================================================================
    # CORRECTION 2 : sable : fasi -> fasigni
    # ============================================================================
    print("🔧 Correction 6 : sable...")
    
    sable = db.words.find_one({"french": "sable"})
    if sable and sable.get('kibouchi'):
        old_kib = sable.get('kibouchi')
        new_kib = "fasigni"
        if old_kib != new_kib:
            db.words.update_one(
                {"_id": sable["_id"]},
                {"$set": {"kibouchi": new_kib}}
            )
            corrections.append(f"✅ sable : '{old_kib}' → '{new_kib}'")
            
            # Corriger le nom du fichier audio
            db.words.update_one(
                {"_id": sable["_id"]},
                {"$set": {"audio_filename_kibouchi": "Fasigni.m4a"}}
            )
            corrections.append(f"   Audio : 'Fasi.m4a' → 'Fasigni.m4a'")
    
    # ============================================================================
    # CORRECTION 3 : vague : hou -> houndza/riaka
    # ============================================================================
    print("🔧 Correction 7 : vague...")
    
    vague = db.words.find_one({"french": "vague"})
    if vague and vague.get('kibouchi'):
        old_kib = vague.get('kibouchi')
        # D'après le tableau : houndza/riaka
        new_kib = "houndza/riaka"
        if old_kib != new_kib:
            db.words.update_one(
                {"_id": vague["_id"]},
                {"$set": {"kibouchi": new_kib}}
            )
            corrections.append(f"✅ vague : '{old_kib}' → '{new_kib}'")
            
            # Corriger le nom du fichier audio
            db.words.update_one(
                {"_id": vague["_id"]},
                {"$set": {"audio_filename_kibouchi": "Houndza.m4a"}}
            )
            corrections.append(f"   Audio : 'Hou.m4a' → 'Houndza.m4a'")
    
    # ============================================================================
    # CORRECTION 4 : Vérifier feuille - devrait être hayïtri (avec ï)
    # ============================================================================
    print("🔧 Correction 8 : feuille...")
    
    feuille = db.words.find_one({"french": "feuille"})
    if feuille and feuille.get('kibouchi'):
        old_kib = feuille.get('kibouchi')
        new_kib = "hayïtri"
        if old_kib != new_kib:
            db.words.update_one(
                {"_id": feuille["_id"]},
                {"$set": {"kibouchi": new_kib}}
            )
            corrections.append(f"✅ feuille : '{old_kib}' → '{new_kib}'")
            
            # Audio devrait être Hayïtri.m4a
            db.words.update_one(
                {"_id": feuille["_id"]},
                {"$set": {"audio_filename_kibouchi": "Hayïtri.m4a"}}
            )
            corrections.append(f"   Audio confirmé : 'Hayïtri.m4a'")
    
    # ============================================================================
    # CORRECTION 5 : Vérifier herbe - devrait être haïtri
    # ============================================================================
    print("🔧 Correction 9 : herbe...")
    
    herbe = db.words.find_one({"french": "herbe"})
    if herbe and herbe.get('kibouchi'):
        old_kib = herbe.get('kibouchi')
        new_kib = "haïtri"
        if old_kib != new_kib:
            db.words.update_one(
                {"_id": herbe["_id"]},
                {"$set": {"kibouchi": new_kib}}
            )
            corrections.append(f"✅ herbe : '{old_kib}' → '{new_kib}'")
            
            # Audio devrait être Haïtri.m4a
            db.words.update_one(
                {"_id": herbe["_id"]},
                {"$set": {"audio_filename_kibouchi": "Haïtri.m4a"}}
            )
            corrections.append(f"   Audio confirmé : 'Haïtri.m4a'")
    
    # ============================================================================
    # AFFICHAGE DES RÉSULTATS
    # ============================================================================
    print()
    print("=" * 80)
    print("RÉSULTATS DES CORRECTIONS")
    print("=" * 80)
    print()
    
    if corrections:
        for i, correction in enumerate(corrections, 1):
            print(f"{i}. {correction}")
        print()
        print(f"✅ Total de corrections appliquées : {len(corrections)}")
    else:
        print("ℹ️  Aucune correction nécessaire - Tout est déjà correct")
    
    print()
    print("=" * 80)
    
    # Sauvegarder le rapport
    with open('/app/RAPPORT_CORRECTIONS_ORTHOGRAPHE_NATURE.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RAPPORT DES CORRECTIONS ORTHOGRAPHE NATURE - KIBOUCHI\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        
        if corrections:
            for i, correction in enumerate(corrections, 1):
                f.write(f"{i}. {correction}\n")
            f.write(f"\n✅ Total : {len(corrections)} corrections appliquées\n")
        else:
            f.write("ℹ️  Aucune correction nécessaire\n")
    
    print("📄 Rapport sauvegardé : /app/RAPPORT_CORRECTIONS_ORTHOGRAPHE_NATURE.txt")
    print()

if __name__ == "__main__":
    main()
