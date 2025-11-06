#!/usr/bin/env python3
"""
CORRECTION FINALE DÉFINITIVE API AUDIO
"""

import os
import shutil

def create_working_audio_route():
    """Créer une route audio qui fonctionne garantie"""
    
    new_route = '''
@app.get("/api/audio/{word_id}/{lang}")
async def get_audio_file(word_id: str, lang: str):
    """Route audio simplifiée et fonctionnelle"""
    try:
        from pymongo import MongoClient
        from bson import ObjectId
        from fastapi.responses import FileResponse
        from fastapi import HTTPException
        import os
        
        # Validation langue
        if lang not in ["shimaore", "kibouchi"]:
            raise HTTPException(status_code=400, detail="Langue non supportée")
        
        # Connexion DB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db = client['shimaoré_app']
        collection = db['vocabulary']
        
        # Récupérer le mot
        try:
            obj_id = ObjectId(word_id)
        except:
            raise HTTPException(status_code=400, detail="ID invalide")
            
        word_doc = collection.find_one({"_id": obj_id})
        if not word_doc:
            raise HTTPException(status_code=404, detail="Mot non trouvé")
        
        # Récupérer le fichier audio
        if lang == "shimaore":
            filename = word_doc.get("audio_shimaoré_filename")
            has_audio = word_doc.get("has_shimaoré_audio", False)
        else:
            filename = word_doc.get("audio_kibouchi_filename")
            has_audio = word_doc.get("has_kibouchi_audio", False)
        
        if not filename or not has_audio:
            raise HTTPException(status_code=404, detail=f"Pas d\\'audio {lang}")
        
        # Chemin du fichier
        section = word_doc.get("section", "verbes")
        file_path = f"/app/frontend/assets/audio/{section}/{filename}"
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Fichier non trouvé")
        
        return FileResponse(
            file_path,
            media_type="audio/mp4",
            headers={"Content-Disposition": f"inline; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")
'''

    # Ajouter la route au server.py
    server_path = "/app/backend/server.py"
    
    with open(server_path, 'r') as f:
        content = f.read()
    
    if "get_audio_file" not in content:
        # Ajouter avant la dernière ligne
        lines = content.split('\n')
        lines.insert(-1, new_route)
        
        with open(server_path, 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ Route audio simplifiée ajoutée")
        return True
    else:
        print("✅ Route audio simplifiée déjà présente")
        return True

def main():
    """Correction finale"""
    print("🚨 CORRECTION FINALE API AUDIO")
    
    # 1. Créer route audio fonctionnelle
    create_working_audio_route()
    
    print("\n🔧 REDÉMARRER LE BACKEND MAINTENANT")
    print("Puis tester: /api/audio/{word_id}/shimaore")
    
    return True

if __name__ == "__main__":
    main()