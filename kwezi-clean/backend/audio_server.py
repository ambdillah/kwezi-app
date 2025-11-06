#!/usr/bin/env python3
"""
Serveur HTTP simple pour servir les fichiers audio authentiques
depuis les répertoires extraits vers le frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

# Créer l'app FastAPI pour l'audio
audio_app = FastAPI(title="Audio Server", description="Serveur de fichiers audio authentiques")

# Ajouter CORS
audio_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Répertoires audio
FAMILLE_AUDIO_DIR = "/app/frontend/assets/audio/famille"
NATURE_AUDIO_DIR = "/app/frontend/assets/audio/nature"

@audio_app.get("/")
async def root():
    """Point d'entrée du serveur audio"""
    return {
        "service": "Audio Server",
        "status": "running",
        "endpoints": {
            "famille": "/audio/famille/{filename}",
            "nature": "/audio/nature/{filename}",
            "list_famille": "/audio/famille/",
            "list_nature": "/audio/nature/"
        }
    }

@audio_app.get("/audio/famille/")
async def list_famille_audio():
    """Liste tous les fichiers audio famille disponibles"""
    try:
        if not os.path.exists(FAMILLE_AUDIO_DIR):
            return {"error": "Répertoire famille non trouvé", "files": []}
        
        files = [f for f in os.listdir(FAMILLE_AUDIO_DIR) if f.endswith('.m4a')]
        return {
            "category": "famille",
            "count": len(files),
            "files": sorted(files)
        }
    except Exception as e:
        return {"error": str(e), "files": []}

@audio_app.get("/audio/nature/")
async def list_nature_audio():
    """Liste tous les fichiers audio nature disponibles"""
    try:
        if not os.path.exists(NATURE_AUDIO_DIR):
            return {"error": "Répertoire nature non trouvé", "files": []}
        
        files = [f for f in os.listdir(NATURE_AUDIO_DIR) if f.endswith('.m4a')]
        return {
            "category": "nature", 
            "count": len(files),
            "files": sorted(files)
        }
    except Exception as e:
        return {"error": str(e), "files": []}

@audio_app.get("/audio/famille/{filename}")
async def get_famille_audio(filename: str):
    """Sert un fichier audio famille"""
    file_path = os.path.join(FAMILLE_AUDIO_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio famille non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@audio_app.get("/audio/nature/{filename}")
async def get_nature_audio(filename: str):
    """Sert un fichier audio nature"""
    file_path = os.path.join(NATURE_AUDIO_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio nature non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4", 
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

def start_audio_server():
    """Démarre le serveur audio sur le port 8002"""
    print("🎵 DÉMARRAGE DU SERVEUR AUDIO")
    print("Port: 8002")
    print("Endpoints:")
    print("  - http://localhost:8002/audio/famille/{filename}")
    print("  - http://localhost:8002/audio/nature/{filename}")
    print()
    
    uvicorn.run(
        "audio_server:audio_app",
        host="0.0.0.0",
        port=8002,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    start_audio_server()