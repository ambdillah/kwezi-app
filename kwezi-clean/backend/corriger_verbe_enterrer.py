#!/usr/bin/env python3
"""
Script de correction du verbe "Entérer" → "Enterrer"
Ajoute le verbe avec l'orthographe correcte et les traductions authentiques
"""

from pymongo import MongoClient
from datetime import datetime

def main():
    print("=" * 80)
    print("CORRECTION DU VERBE : Entérer → Enterrer")
    print("=" * 80)
    print()
    
    # Connexion à MongoDB
    client = MongoClient("mongodb://localhost:27017")
    db = client["mayotte_app"]
    words_collection = db["words"]
    
    # 1. Vérifier si "Entérer" existe (ne devrait pas)
    print("1. Vérification de l'existence du verbe 'Entérer'...")
    enterer_old = words_collection.find_one({"french": "Entérer", "category": "verbes"})
    if enterer_old:
        print("   ⚠️  Verbe 'Entérer' trouvé (ID: {})".format(enterer_old['_id']))
        print("   → Suppression avant ajout de la version corrigée...")
        result = words_collection.delete_one({"_id": enterer_old['_id']})
        print(f"   ✅ Supprimé: {result.deleted_count} document")
    else:
        print("   ✅ Verbe 'Entérer' non trouvé (normal)")
    print()
    
    # 2. Vérifier si "Enterrer" existe déjà
    print("2. Vérification de l'existence du verbe 'Enterrer'...")
    enterrer_exists = words_collection.find_one({"french": "Enterrer", "category": "verbes"})
    if enterrer_exists:
        print("   ⚠️  Verbe 'Enterrer' existe déjà (ID: {})".format(enterrer_exists['_id']))
        print("   → Mise à jour des traductions si nécessaire...")
        
        # Vérifier les traductions
        needs_update = False
        update_fields = {}
        
        if enterrer_exists.get('shimaore') != 'oudziha':
            update_fields['shimaore'] = 'oudziha'
            needs_update = True
        
        if enterrer_exists.get('kibouchi') != 'mandévigni':
            update_fields['kibouchi'] = 'mandévigni'
            needs_update = True
        
        if needs_update:
            # Ajouter aussi les champs audio (nouveau format)
            update_fields.update({
                'audio_filename_shimaore': 'Oudziha.m4a',
                'audio_filename_kibouchi': 'Mandévigni.m4a',
                'shimoare_has_audio': True,
                'kibouchi_has_audio': True,
                'dual_audio_system': True,
                'updated_at': datetime.utcnow()
            })
            
            result = words_collection.update_one(
                {"_id": enterrer_exists['_id']},
                {"$set": update_fields}
            )
            print(f"   ✅ Verbe mis à jour: {result.modified_count} document")
            print(f"   Champs mis à jour: {', '.join(update_fields.keys())}")
        else:
            print("   ✅ Traductions déjà correctes, aucune mise à jour nécessaire")
        
        print()
        print("=" * 80)
        print("✅ CORRECTION TERMINÉE - Verbe 'Enterrer' présent avec les bonnes traductions")
        print("=" * 80)
        return
    
    # 3. Ajouter le verbe "Enterrer"
    print("3. Ajout du verbe 'Enterrer' avec traductions authentiques...")
    print()
    
    nouveau_verbe = {
        "french": "Enterrer",
        "shimaore": "oudziha",
        "kibouchi": "mandévigni",
        "category": "verbes",
        "emoji": "⚰️",
        
        # Nouveau système audio dual
        "audio_filename_shimaore": "Oudziha.m4a",
        "audio_filename_kibouchi": "Mandévigni.m4a",
        "shimoare_has_audio": True,
        "kibouchi_has_audio": True,
        "dual_audio_system": True,
        
        # Métadonnées
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "source": "correction_orthographique",
        "verified": True
    }
    
    print("   Verbe à ajouter:")
    print(f"   - French: {nouveau_verbe['french']}")
    print(f"   - Shimaoré: {nouveau_verbe['shimaore']}")
    print(f"   - Kibouchi: {nouveau_verbe['kibouchi']}")
    print(f"   - Audio shimaoré: {nouveau_verbe['audio_filename_shimaore']}")
    print(f"   - Audio kibouchi: {nouveau_verbe['audio_filename_kibouchi']}")
    print()
    
    result = words_collection.insert_one(nouveau_verbe)
    print(f"   ✅ Verbe ajouté avec succès (ID: {result.inserted_id})")
    print()
    
    # 4. Vérification finale
    print("4. Vérification finale...")
    total_verbes = words_collection.count_documents({"category": "verbes"})
    enterrer_final = words_collection.find_one({"french": "Enterrer", "category": "verbes"})
    
    print(f"   Total de verbes: {total_verbes}")
    print(f"   Verbe 'Enterrer' présent: {'✅ OUI' if enterrer_final else '❌ NON'}")
    
    if enterrer_final:
        print()
        print("   Détails du verbe:")
        print(f"   - ID: {enterrer_final['_id']}")
        print(f"   - French: {enterrer_final['french']}")
        print(f"   - Shimaoré: {enterrer_final['shimaore']}")
        print(f"   - Kibouchi: {enterrer_final['kibouchi']}")
        print(f"   - Audio shimaoré: {enterrer_final.get('audio_filename_shimaore', 'N/A')}")
        print(f"   - Audio kibouchi: {enterrer_final.get('audio_filename_kibouchi', 'N/A')}")
        print(f"   - Dual audio system: {enterrer_final.get('dual_audio_system', False)}")
    
    print()
    print("=" * 80)
    print("✅ CORRECTION TERMINÉE AVEC SUCCÈS")
    print("=" * 80)
    print()
    print("Résumé:")
    print("  • Verbe 'Enterrer' ajouté avec orthographe correcte ✅")
    print("  • Traductions authentiques: oudziha (shimaoré), mandévigni (kibouchi) ✅")
    print("  • Fichiers audio: Oudziha.m4a, Mandévigni.m4a ✅")
    print(f"  • Total de verbes: {total_verbes}")
    print()

if __name__ == "__main__":
    main()
