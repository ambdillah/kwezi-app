#!/usr/bin/env python3
"""
Script pour télécharger les fichiers audio avec des URLs directes.
L'utilisateur peut fournir les URLs directes depuis Google Drive.
"""

import os
import requests
import time

def download_files_from_urls():
    """Télécharge les fichiers depuis des URLs directes."""
    
    destination_dir = "/app/frontend/assets/audio/famille"
    os.makedirs(destination_dir, exist_ok=True)
    
    print("📁 Répertoire de destination créé:", destination_dir)
    print()
    print("🔗 INSTRUCTIONS POUR OBTENIR LES URLs DIRECTES:")
    print("1. Allez sur votre Google Drive")
    print("2. Clic droit sur chaque fichier .m4a → 'Obtenir le lien'")
    print("3. Changez les permissions à 'Tous les utilisateurs ayant le lien peuvent consulter'")
    print("4. Copiez le lien qui ressemble à:")
    print("   https://drive.google.com/file/d/XXXXX/view?usp=sharing")
    print("5. Modifiez-le en:")
    print("   https://drive.google.com/uc?export=download&id=XXXXX")
    print()
    
    # URLs d'exemple - à remplacer par les vraies URLs
    file_urls = {
        # Format: "nom_fichier.m4a": "https://drive.google.com/uc?export=download&id=FILE_ID"
        "Anabavi.m4a": "",  # À remplir
        "Anadahi.m4a": "",  # À remplir
        "Mama.m4a": "",     # À remplir (exemple)
        # ... Ajouter tous les autres fichiers
    }
    
    print("⚠️ Ce script nécessite que vous ajoutiez les URLs directes dans le code.")
    print("📝 Modifiez le dictionnaire 'file_urls' dans le script avec vos URLs.")
    print()
    
    return False

# Version interactive
def interactive_download():
    """Version interactive pour télécharger fichier par fichier."""
    
    destination_dir = "/app/frontend/assets/audio/famille"
    os.makedirs(destination_dir, exist_ok=True)
    
    print("🎵 TÉLÉCHARGEMENT INTERACTIF")
    print("=" * 50)
    print("Entrez les URLs de téléchargement direct un par un.")
    print("Format attendu: https://drive.google.com/uc?export=download&id=XXXXX")
    print("Tapez 'fin' pour terminer.")
    print()
    
    downloaded_count = 0
    
    while True:
        filename = input("📝 Nom du fichier (ex: Mama.m4a): ").strip()
        if filename.lower() == 'fin':
            break
            
        if not filename.endswith('.m4a'):
            filename += '.m4a'
            
        url = input(f"🔗 URL directe pour {filename}: ").strip()
        if not url:
            continue
            
        # Télécharger le fichier
        try:
            print(f"📥 Téléchargement de {filename}...")
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                file_path = os.path.join(destination_dir, filename)
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                file_size = os.path.getsize(file_path)
                print(f"✅ {filename} téléchargé ({file_size} bytes)")
                downloaded_count += 1
            else:
                print(f"❌ Échec: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
        
        print()
    
    print(f"🎉 Téléchargement terminé! {downloaded_count} fichiers téléchargés.")
    return downloaded_count > 0

if __name__ == "__main__":
    print("🚀 TÉLÉCHARGEUR AUDIO FAMILLE")
    print("=" * 40)
    print()
    
    choice = input("Choisissez une option:\n1. Instructions URLs directes\n2. Téléchargement interactif\nVotre choix (1 ou 2): ").strip()
    
    if choice == "1":
        download_files_from_urls()
    elif choice == "2":
        interactive_download()
    else:
        print("❌ Choix invalide")