#!/usr/bin/env python3
"""
Active le système dual audio pour TOUS les mots qui ont des fichiers audio
"""

from pymongo import MongoClient

def main():
    print("=" * 80)
    print("ACTIVATION DU SYSTÈME DUAL AUDIO POUR TOUS LES MOTS")
    print("=" * 80)
    print()
    
    client = MongoClient("mongodb://localhost:27017")
    db = client["mayotte_app"]
    
    # Récupérer tous les mots
    all_words = list(db.words.find({}))
    
    print(f"Total de mots à vérifier : {len(all_words)}")
    print()
    
    updated_count = 0
    
    for word in all_words:
        needs_update = False
        update_fields = {}
        
        # Vérifier shimaoré
        shim_audio = word.get('audio_filename_shimaore') or word.get('shimoare_audio_filename')
        if shim_audio:
            update_fields['shimoare_has_audio'] = True
            if not word.get('dual_audio_system'):
                update_fields['dual_audio_system'] = True
                needs_update = True
        
        # Vérifier kibouchi
        kib_audio = word.get('audio_filename_kibouchi') or word.get('kibouchi_audio_filename')
        if kib_audio:
            update_fields['kibouchi_has_audio'] = True
            if not word.get('dual_audio_system'):
                update_fields['dual_audio_system'] = True
                needs_update = True
        
        # Mettre à jour si nécessaire
        if needs_update or update_fields:
            db.words.update_one(
                {"_id": word["_id"]},
                {"$set": update_fields}
            )
            updated_count += 1
    
    print(f"✅ {updated_count} mots mis à jour avec le système dual audio")
    print()
    
    # Vérification rapide
    dual_audio_count = db.words.count_documents({"dual_audio_system": True})
    print(f"📊 Total de mots avec système dual audio : {dual_audio_count}")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
