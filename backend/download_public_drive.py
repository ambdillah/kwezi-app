#!/usr/bin/env python3
"""
Script pour télécharger depuis un dossier Google Drive rendu public.
"""

import os
import requests
import zipfile
import tempfile

def download_from_public_drive(folder_id):
    """Télécharge un dossier Google Drive public en ZIP."""
    
    destination_dir = "/app/frontend/assets/audio/famille"
    os.makedirs(destination_dir, exist_ok=True)
    
    # URL pour télécharger tout le dossier en ZIP
    zip_url = f"https://drive.google.com/uc?export=download&id={folder_id}"
    
    print(f"📥 Téléchargement du dossier Google Drive...")
    print(f"🔗 URL: {zip_url}")
    
    try:
        # Télécharger le ZIP
        response = requests.get(zip_url, stream=True)
        
        if response.status_code == 200:
            # Sauvegarder le ZIP temporairement
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        temp_zip.write(chunk)
                temp_zip_path = temp_zip.name
            
            # Extraire les fichiers .m4a
            print("📂 Extraction des fichiers audio...")
            with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename.endswith('.m4a'):
                        # Extraire le fichier
                        source = zip_ref.open(file_info)
                        target_path = os.path.join(destination_dir, os.path.basename(file_info.filename))
                        
                        with open(target_path, 'wb') as target_file:
                            target_file.write(source.read())
                        
                        print(f"✅ {os.path.basename(file_info.filename)} extrait")
            
            # Nettoyer le fichier temporaire
            os.unlink(temp_zip_path)
            
            # Lister les fichiers téléchargés
            audio_files = [f for f in os.listdir(destination_dir) if f.endswith('.m4a')]
            print(f"\n🎉 {len(audio_files)} fichiers audio téléchargés:")
            for filename in sorted(audio_files):
                print(f"   - {filename}")
            
            return len(audio_files) > 0
            
        else:
            print(f"❌ Échec téléchargement: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 TÉLÉCHARGEMENT DOSSIER GOOGLE DRIVE PUBLIC")
    print("=" * 50)
    
    # ID du dossier depuis l'URL partagée
    folder_id = "173Ubl3EyZ4cbXDT9ENEgmzEszKJbAdBM"
    
    print("⚠️ PRÉREQUIS:")
    print("Le dossier Google Drive doit être rendu public")
    print("(Partage → Tous les utilisateurs ayant le lien peuvent consulter)")
    print()
    
    success = download_from_public_drive(folder_id)
    
    if success:
        print("\n🎉 Téléchargement réussi!")
    else:
        print("\n💥 Téléchargement échoué")
        print("💡 Essayez la méthode alternative (téléchargement manuel + upload)")