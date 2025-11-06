#!/usr/bin/env python3
"""
Script pour télécharger automatiquement tous les fichiers audio
depuis le Google Drive partagé de la section famille.
"""

import os
import requests
import re
from urllib.parse import unquote
import time

def extract_file_info_from_drive_page(drive_url):
    """Extrait les informations des fichiers depuis la page Google Drive."""
    print(f"🔍 Analyse de la page Google Drive...")
    
    try:
        # Faire une requête pour obtenir le contenu HTML de la page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(drive_url, headers=headers)
        html_content = response.text
        
        # Pattern pour extraire les informations des fichiers audio
        # Chercher les patterns qui correspondent aux fichiers .m4a
        file_pattern = r'"([^"]+\.m4a)"[^}]*"([a-zA-Z0-9_-]{25,})"'
        matches = re.findall(file_pattern, html_content)
        
        files_info = []
        for filename, file_id in matches:
            # Nettoyer le nom de fichier
            clean_filename = unquote(filename).replace('\\u003d', '=')
            files_info.append({
                'filename': clean_filename,
                'file_id': file_id,
                'download_url': f"https://drive.google.com/uc?export=download&id={file_id}"
            })
        
        # Si la méthode ci-dessus ne fonctionne pas, essayer une approche alternative
        if not files_info:
            print("⚠️ Méthode principale échouée, essai d'une approche alternative...")
            
            # Liste manuelle des fichiers identifiés précédemment
            known_files = [
                "Anabavi.m4a", "Anadahi.m4a", "Baba héli-bé.m4a", "Baba k.m4a", 
                "Baba s.m4a", "Baba titi-bolé.m4a", "Bacoco.m4a", "Bweni.m4a",
                "Coco.m4a", "Dadayi.m4a", "Dadi.m4a", "Havagna.m4a", "Lalahi.m4a",
                "Mama titi-bolé.m4a", "Mama.m4a", "Mdjamaza.m4a", "Moina boueni.m4a",
                "Moina.m4a", "Moinagna mtroubaba.m4a", "Moinagna mtroumama.m4a",
                "Mongné.m4a", "Mtroubaba.m4a", "Mtroumama.m4a", "Mwanagna.m4a",
                "Mwandzani.m4a", "Ninfndri héli-bé.m4a", "Tseki lalahi.m4a",
                "Viavi.m4a", "Zama.m4a", "Zena.m4a", "Zoki lalahi.m4a",
                "Zoki viavi.m4a", "Zouki mtroubaba.m4a", "Zouki mtroumché.m4a", "Zouki.m4a"
            ]
            
            # Essayer d'extraire les IDs depuis l'HTML pour ces fichiers
            for filename in known_files:
                # Chercher l'ID dans l'HTML
                escaped_filename = re.escape(filename)
                id_pattern = rf'{escaped_filename}[^"]*"([a-zA-Z0-9_-]{{25,}})"'
                match = re.search(id_pattern, html_content)
                
                if match:
                    file_id = match.group(1)
                    files_info.append({
                        'filename': filename,
                        'file_id': file_id,
                        'download_url': f"https://drive.google.com/uc?export=download&id={file_id}"
                    })
        
        return files_info
        
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {str(e)}")
        return []

def download_file(file_info, destination_dir):
    """Télécharge un fichier depuis Google Drive."""
    filename = file_info['filename']
    download_url = file_info['download_url']
    
    destination_path = os.path.join(destination_dir, filename)
    
    # Éviter de retélécharger si le fichier existe déjà
    if os.path.exists(destination_path):
        print(f"   ⏭️ {filename} existe déjà, passage au suivant")
        return True
    
    try:
        print(f"   📥 Téléchargement de {filename}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(download_url, headers=headers, stream=True)
        
        # Gérer les redirections Google Drive
        if 'accounts.google.com' in response.url or response.status_code == 302:
            print(f"   ⚠️ Redirection détectée pour {filename}, fichier privé ou nécessite authentification")
            return False
            
        if response.status_code == 200:
            with open(destination_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(destination_path)
            print(f"   ✅ {filename} téléchargé ({file_size} bytes)")
            return True
        else:
            print(f"   ❌ Échec téléchargement {filename}: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur téléchargement {filename}: {str(e)}")
        return False

def download_all_famille_audio():
    """Télécharge tous les fichiers audio de la section famille."""
    
    drive_url = "https://drive.google.com/drive/folders/173Ubl3EyZ4cbXDT9ENEgmzEszKJbAdBM?usp=sharing"
    destination_dir = "/app/frontend/assets/audio/famille"
    
    # Créer le répertoire de destination
    os.makedirs(destination_dir, exist_ok=True)
    print(f"📁 Répertoire de destination: {destination_dir}")
    print()
    
    # Extraire les informations des fichiers
    files_info = extract_file_info_from_drive_page(drive_url)
    
    if not files_info:
        print("❌ Aucun fichier détecté. Essai d'une approche alternative...")
        
        # Approche alternative : utiliser les noms de fichiers connus
        # et essayer de deviner les URLs de téléchargement
        print("🔄 Utilisation de la liste des fichiers connus...")
        
        # Cette approche nécessiterait que les fichiers soient publiquement accessibles
        # ce qui n'est généralement pas le cas avec Google Drive
        print("⚠️ Les fichiers Google Drive nécessitent généralement une authentification.")
        print("📋 Solutions alternatives:")
        print("1. Rendre les fichiers publics dans Google Drive")
        print("2. Télécharger manuellement et les placer dans le répertoire")
        print("3. Utiliser l'API Google Drive avec authentification")
        return False
    
    print(f"🎵 {len(files_info)} fichiers audio détectés")
    print()
    
    # Télécharger chaque fichier
    success_count = 0
    failed_count = 0
    
    for i, file_info in enumerate(files_info, 1):
        print(f"📥 [{i}/{len(files_info)}] {file_info['filename']}")
        
        if download_file(file_info, destination_dir):
            success_count += 1
        else:
            failed_count += 1
        
        # Petite pause entre les téléchargements
        time.sleep(0.5)
        print()
    
    # Résumé
    print("=" * 60)
    print(f"📊 RÉSUMÉ DU TÉLÉCHARGEMENT")
    print(f"✅ Réussis: {success_count}")
    print(f"❌ Échecs: {failed_count}")
    print(f"📁 Destination: {destination_dir}")
    print()
    
    if success_count > 0:
        print("🎉 Téléchargement partiel ou complet réussi!")
        
        # Lister les fichiers téléchargés
        downloaded_files = [f for f in os.listdir(destination_dir) if f.endswith('.m4a')]
        print(f"📋 Fichiers téléchargés ({len(downloaded_files)}):")
        for filename in sorted(downloaded_files):
            file_path = os.path.join(destination_dir, filename)
            file_size = os.path.getsize(file_path)
            print(f"   - {filename} ({file_size} bytes)")
    else:
        print("❌ Aucun fichier téléchargé avec succès")
        print("💡 Voir les instructions alternatives ci-dessus")
    
    return success_count > 0

if __name__ == "__main__":
    print("🚀 Début du téléchargement automatique des fichiers audio famille...")
    print("📂 Source: Google Drive partagé")
    print()
    
    success = download_all_famille_audio()
    
    if success:
        print("🎉 Téléchargement terminé!")
    else:
        print("💥 Téléchargement échoué - voir les alternatives proposées")