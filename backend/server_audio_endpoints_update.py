#!/usr/bin/env python3
"""
SCRIPT POUR AJOUTER LES ENDPOINTS AUDIO POUR 4 NOUVELLES SECTIONS
================================================================
Ce script ajoute les endpoints audio pour les sections:
- salutations
- couleurs  
- grammaire
- nourriture

Et met à jour la fonction get_audio_info pour inclure ces sections.
"""

def generate_audio_endpoints():
    """Génère les nouveaux endpoints audio à ajouter"""
    
    sections = ["salutations", "couleurs", "grammaire", "nourriture"]
    
    endpoints_code = ""
    
    for section in sections:
        endpoint_code = f'''
@app.get("/api/audio/{section}/{{filename}}")
async def get_{section}_audio(filename: str):
    """Sert un fichier audio {section}"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/{section}", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio {section} non trouvé: {{filename}}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={{"Content-Disposition": f"inline; filename={{filename}}"}}
    )
'''
        endpoints_code += endpoint_code
    
    return endpoints_code

def generate_audio_info_update():
    """Génère le code mis à jour pour get_audio_info"""
    
    return '''
@app.get("/api/audio/info")
async def get_audio_info():
    """Information sur les fichiers audio disponibles"""
    import os
    
    famille_dir = "/app/frontend/assets/audio/famille"
    nature_dir = "/app/frontend/assets/audio/nature"
    nombres_dir = "/app/frontend/assets/audio/nombres"
    animaux_dir = "/app/frontend/assets/audio/animaux"
    corps_dir = "/app/frontend/assets/audio/corps"
    salutations_dir = "/app/frontend/assets/audio/salutations"
    couleurs_dir = "/app/frontend/assets/audio/couleurs"
    grammaire_dir = "/app/frontend/assets/audio/grammaire"
    nourriture_dir = "/app/frontend/assets/audio/nourriture"
    
    famille_files = []
    nature_files = []
    nombres_files = []
    animaux_files = []
    corps_files = []
    salutations_files = []
    couleurs_files = []
    grammaire_files = []
    nourriture_files = []
    
    if os.path.exists(famille_dir):
        famille_files = [f for f in os.listdir(famille_dir) if f.endswith('.m4a')]
    
    if os.path.exists(nature_dir):
        nature_files = [f for f in os.listdir(nature_dir) if f.endswith('.m4a')]
        
    if os.path.exists(nombres_dir):
        nombres_files = [f for f in os.listdir(nombres_dir) if f.endswith('.m4a')]
        
    if os.path.exists(animaux_dir):
        animaux_files = [f for f in os.listdir(animaux_dir) if f.endswith('.m4a')]
        
    if os.path.exists(corps_dir):
        corps_files = [f for f in os.listdir(corps_dir) if f.endswith('.m4a')]
        
    if os.path.exists(salutations_dir):
        salutations_files = [f for f in os.listdir(salutations_dir) if f.endswith('.m4a')]
        
    if os.path.exists(couleurs_dir):
        couleurs_files = [f for f in os.listdir(couleurs_dir) if f.endswith('.m4a')]
        
    if os.path.exists(grammaire_dir):
        grammaire_files = [f for f in os.listdir(grammaire_dir) if f.endswith('.m4a')]
        
    if os.path.exists(nourriture_dir):
        nourriture_files = [f for f in os.listdir(nourriture_dir) if f.endswith('.m4a')]
    
    return {
        "service": "Audio API intégré - Système Dual Étendu",
        "famille": {
            "count": len(famille_files),
            "files": sorted(famille_files)
        },
        "nature": {
            "count": len(nature_files),
            "files": sorted(nature_files)
        },
        "nombres": {
            "count": len(nombres_files),
            "files": sorted(nombres_files)
        },
        "animaux": {
            "count": len(animaux_files),
            "files": sorted(animaux_files)
        },
        "corps": {
            "count": len(corps_files),
            "files": sorted(corps_files)
        },
        "salutations": {
            "count": len(salutations_files),
            "files": sorted(salutations_files)
        },
        "couleurs": {
            "count": len(couleurs_files),
            "files": sorted(couleurs_files)
        },
        "grammaire": {
            "count": len(grammaire_files),
            "files": sorted(grammaire_files)
        },
        "nourriture": {
            "count": len(nourriture_files),
            "files": sorted(nourriture_files)
        },
        "endpoints": {
            "famille": "/api/audio/famille/{filename}",
            "nature": "/api/audio/nature/{filename}",
            "nombres": "/api/audio/nombres/{filename}",
            "animaux": "/api/audio/animaux/{filename}",
            "corps": "/api/audio/corps/{filename}",
            "salutations": "/api/audio/salutations/{filename}",
            "couleurs": "/api/audio/couleurs/{filename}",
            "grammaire": "/api/audio/grammaire/{filename}",
            "nourriture": "/api/audio/nourriture/{filename}",
            "dual_system": "/api/words/{word_id}/audio/{lang}"
        },
        "total_categories": 9,
        "total_files": len(famille_files) + len(nature_files) + len(nombres_files) + len(animaux_files) + len(corps_files) + len(salutations_files) + len(couleurs_files) + len(grammaire_files) + len(nourriture_files)
    }
'''

def generate_audio_dirs_update():
    """Génère le code mis à jour pour audio_dirs"""
    
    return '''
        audio_dirs = {
            "famille": "/app/frontend/assets/audio/famille",
            "nature": "/app/frontend/assets/audio/nature", 
            "nombres": "/app/frontend/assets/audio/nombres",
            "animaux": "/app/frontend/assets/audio/animaux",
            "corps": "/app/frontend/assets/audio/corps",
            "salutations": "/app/frontend/assets/audio/salutations",
            "couleurs": "/app/frontend/assets/audio/couleurs",
            "grammaire": "/app/frontend/assets/audio/grammaire",
            "nourriture": "/app/frontend/assets/audio/nourriture"
        }
'''

if __name__ == "__main__":
    print("🔧 Génération des nouveaux endpoints audio...")
    print("=" * 50)
    
    print("\n📁 NOUVEAUX ENDPOINTS:")
    print(generate_audio_endpoints())
    
    print("\n🔄 FONCTION get_audio_info MISE À JOUR:")
    print(generate_audio_info_update())
    
    print("\n📂 AUDIO_DIRS MIS À JOUR:")  
    print(generate_audio_dirs_update())