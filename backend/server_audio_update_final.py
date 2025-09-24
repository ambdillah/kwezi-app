#!/usr/bin/env python3
"""
MISE À JOUR FINALE DU SERVEUR AUDIO - 16 CATÉGORIES
==================================================
Code mis à jour pour inclure les 4 nouvelles sections dans get_audio_info
et audio_dirs: vetements, maison, tradition, transport
"""

# Code pour remplacer dans server.py à partir de la ligne avec les vérifications des répertoires

def get_updated_audio_info_section():
    return '''
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
        
    if os.path.exists(verbes_dir):
        verbes_files = [f for f in os.listdir(verbes_dir) if f.endswith('.m4a')]
        
    if os.path.exists(expressions_dir):
        expressions_files = [f for f in os.listdir(expressions_dir) if f.endswith('.m4a')]
        
    if os.path.exists(adjectifs_dir):
        adjectifs_files = [f for f in os.listdir(adjectifs_dir) if f.endswith('.m4a')]
        
    if os.path.exists(vetements_dir):
        vetements_files = [f for f in os.listdir(vetements_dir) if f.endswith('.m4a')]
        
    if os.path.exists(maison_dir):
        maison_files = [f for f in os.listdir(maison_dir) if f.endswith('.m4a')]
        
    if os.path.exists(tradition_dir):
        tradition_files = [f for f in os.listdir(tradition_dir) if f.endswith('.m4a')]
        
    if os.path.exists(transport_dir):
        transport_files = [f for f in os.listdir(transport_dir) if f.endswith('.m4a')]
    
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
        "verbes": {
            "count": len(verbes_files),
            "files": sorted(verbes_files)
        },
        "expressions": {
            "count": len(expressions_files),
            "files": sorted(expressions_files)
        },
        "adjectifs": {
            "count": len(adjectifs_files),
            "files": sorted(adjectifs_files)
        },
        "vetements": {
            "count": len(vetements_files),
            "files": sorted(vetements_files)
        },
        "maison": {
            "count": len(maison_files),
            "files": sorted(maison_files)
        },
        "tradition": {
            "count": len(tradition_files),
            "files": sorted(tradition_files)
        },
        "transport": {
            "count": len(transport_files),
            "files": sorted(transport_files)
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
            "verbes": "/api/audio/verbes/{filename}",
            "expressions": "/api/audio/expressions/{filename}",
            "adjectifs": "/api/audio/adjectifs/{filename}",
            "vetements": "/api/audio/vetements/{filename}",
            "maison": "/api/audio/maison/{filename}",
            "tradition": "/api/audio/tradition/{filename}",
            "transport": "/api/audio/transport/{filename}",
            "dual_system": "/api/words/{word_id}/audio/{lang}"
        },
        "total_categories": 16,
        "total_files": len(famille_files) + len(nature_files) + len(nombres_files) + len(animaux_files) + len(corps_files) + len(salutations_files) + len(couleurs_files) + len(grammaire_files) + len(nourriture_files) + len(verbes_files) + len(expressions_files) + len(adjectifs_files) + len(vetements_files) + len(maison_files) + len(tradition_files) + len(transport_files)
    }
'''

def get_updated_audio_dirs():
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
            "nourriture": "/app/frontend/assets/audio/nourriture",
            "verbes": "/app/frontend/assets/audio/verbes",
            "expressions": "/app/frontend/assets/audio/expressions",
            "adjectifs": "/app/frontend/assets/audio/adjectifs",
            "vetements": "/app/frontend/assets/audio/vetements",
            "maison": "/app/frontend/assets/audio/maison",
            "tradition": "/app/frontend/assets/audio/tradition",
            "transport": "/app/frontend/assets/audio/transport"
        }
'''

if __name__ == "__main__":
    print("🔧 Code mis à jour pour 16 catégories audio")
    print("Instructions: Appliquer ces modifications dans server.py")