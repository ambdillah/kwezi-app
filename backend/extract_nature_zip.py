#!/usr/bin/env python3
"""
Script pour extraire et organiser les fichiers audio nature depuis le ZIP uploadé.
"""

import os
import requests
import zipfile
import tempfile
import shutil

def extract_nature_audio_zip():
    """Télécharge et extrait le ZIP des fichiers audio nature."""
    
    zip_url = "https://customer-assets.emergentagent.com/job_shimaware/artifacts/moj64sy3_Nature-20250922T103842Z-1-001.zip"
    destination_dir = "/app/frontend/assets/audio/nature"
    
    # Créer le répertoire de destination
    os.makedirs(destination_dir, exist_ok=True)
    print(f"📁 Répertoire de destination créé: {destination_dir}")
    print()
    
    try:
        print("📥 Téléchargement du fichier ZIP Nature...")
        print(f"🔗 URL: {zip_url}")
        
        # Télécharger le ZIP
        response = requests.get(zip_url, stream=True)
        
        if response.status_code == 200:
            # Sauvegarder temporairement
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        temp_zip.write(chunk)
                temp_zip_path = temp_zip.name
            
            file_size = os.path.getsize(temp_zip_path)
            print(f"✅ ZIP téléchargé ({file_size} bytes)")
            print()
            
            # Extraire le contenu
            print("📂 Extraction des fichiers audio nature...")
            extracted_count = 0
            
            with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                # Lister tous les fichiers dans le ZIP
                file_list = zip_ref.namelist()
                print(f"📋 {len(file_list)} fichiers trouvés dans le ZIP")
                
                for file_path in file_list:
                    # Nettoyer le nom de fichier (supprimer les dossiers)
                    filename = os.path.basename(file_path)
                    
                    # Ne traiter que les fichiers audio
                    if filename.endswith(('.m4a', '.mp3', '.wav', '.aac')) and filename != '':
                        print(f"   📄 Extraction: {filename}")
                        
                        # Extraire le fichier
                        with zip_ref.open(file_path) as source:
                            target_path = os.path.join(destination_dir, filename)
                            with open(target_path, 'wb') as target:
                                shutil.copyfileobj(source, target)
                        
                        # Vérifier la taille du fichier extrait
                        extracted_size = os.path.getsize(target_path)
                        print(f"      ✅ {filename} ({extracted_size} bytes)")
                        extracted_count += 1
                    else:
                        if filename != '':
                            print(f"   ⏭️ Ignoré: {filename} (pas un fichier audio)")
            
            # Nettoyer le fichier temporaire
            os.unlink(temp_zip_path)
            print()
            
            # Résumé des fichiers extraits
            audio_files = [f for f in os.listdir(destination_dir) if f.endswith(('.m4a', '.mp3', '.wav', '.aac'))]
            
            print("=" * 60)
            print(f"📊 RÉSUMÉ DE L'EXTRACTION NATURE")
            print(f"📥 ZIP téléchargé: {file_size} bytes")
            print(f"📂 Fichiers audio extraits: {extracted_count}")
            print(f"📁 Destination: {destination_dir}")
            print()
            
            if audio_files:
                print(f"🌿 FICHIERS AUDIO NATURE DISPONIBLES ({len(audio_files)}):")
                for filename in sorted(audio_files):
                    file_path = os.path.join(destination_dir, filename)
                    size = os.path.getsize(file_path)
                    print(f"   - {filename} ({size} bytes)")
                
                print()
                print("✅ Extraction réussie!")
                print("🎯 Les fichiers audio nature sont maintenant disponibles")
                
                return True
            else:
                print("❌ Aucun fichier audio trouvé dans le ZIP")
                return False
                
        else:
            print(f"❌ Échec téléchargement ZIP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 EXTRACTION FICHIERS AUDIO NATURE")
    print("📦 Source: ZIP uploadé via interface")
    print("=" * 50)
    print()
    
    success = extract_nature_audio_zip()
    
    if success:
        print()
        print("🎉 EXTRACTION NATURE TERMINÉE AVEC SUCCÈS!")
        print("📱 Prochaine étape: Intégrer les métadonnées dans la base de données")
    else:
        print()
        print("💥 EXTRACTION ÉCHOUÉE")
        print("💡 Vérifiez le format du ZIP et réessayez")