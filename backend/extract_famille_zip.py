#!/usr/bin/env python3
"""
Script pour extraire et organiser les fichiers audio famille depuis le ZIP uploadé.
"""

import os
import requests
import zipfile
import tempfile
import shutil

def extract_famille_audio_zip():
    """Télécharge et extrait le ZIP des fichiers audio famille."""
    
    zip_url = "https://customer-assets.emergentagent.com/job_shimaware/artifacts/ti6ucm9y_Famille-20250922T102326Z-1-001.zip"
    destination_dir = "/app/frontend/assets/audio/famille"
    
    # Créer le répertoire de destination
    os.makedirs(destination_dir, exist_ok=True)
    print(f"📁 Répertoire de destination créé: {destination_dir}")
    print()
    
    try:
        print("📥 Téléchargement du fichier ZIP...")
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
            print("📂 Extraction des fichiers audio...")
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
            print(f"📊 RÉSUMÉ DE L'EXTRACTION")
            print(f"📥 ZIP téléchargé: {file_size} bytes")
            print(f"📂 Fichiers audio extraits: {extracted_count}")
            print(f"📁 Destination: {destination_dir}")
            print()
            
            if audio_files:
                print(f"🎵 FICHIERS AUDIO DISPONIBLES ({len(audio_files)}):")
                for filename in sorted(audio_files):
                    file_path = os.path.join(destination_dir, filename)
                    size = os.path.getsize(file_path)
                    print(f"   - {filename} ({size} bytes)")
                
                print()
                print("✅ Extraction réussie!")
                print("🎯 Les fichiers audio sont maintenant disponibles pour l'application")
                
                # Vérifier la correspondance avec les métadonnées
                print()
                print("🔍 VÉRIFICATION CORRESPONDANCE MÉTADONNÉES...")
                check_metadata_correspondence(audio_files)
                
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

def check_metadata_correspondence(extracted_files):
    """Vérifie la correspondance entre fichiers extraits et métadonnées."""
    
    # Fichiers attendus d'après les métadonnées
    expected_files = [
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
    
    found_files = []
    missing_files = []
    extra_files = []
    
    # Normaliser les noms pour comparaison (insensible à la casse et caractères spéciaux)
    def normalize_filename(filename):
        return filename.lower().replace('é', 'e').replace('è', 'e').replace('à', 'a')
    
    extracted_normalized = {normalize_filename(f): f for f in extracted_files}
    expected_normalized = {normalize_filename(f): f for f in expected_files}
    
    # Vérifier les correspondances
    for norm_expected, original_expected in expected_normalized.items():
        if norm_expected in extracted_normalized:
            found_files.append(extracted_normalized[norm_expected])
        else:
            missing_files.append(original_expected)
    
    # Fichiers en plus
    for norm_extracted, original_extracted in extracted_normalized.items():
        if norm_extracted not in expected_normalized:
            extra_files.append(original_extracted)
    
    # Afficher les résultats
    print(f"✅ Fichiers trouvés et attendus: {len(found_files)}/35")
    print(f"❌ Fichiers manquants: {len(missing_files)}")
    print(f"➕ Fichiers supplémentaires: {len(extra_files)}")
    
    if missing_files:
        print(f"\n⚠️ FICHIERS MANQUANTS:")
        for filename in missing_files[:10]:  # Limiter l'affichage
            print(f"   - {filename}")
        if len(missing_files) > 10:
            print(f"   ... et {len(missing_files) - 10} autres")
    
    if extra_files:
        print(f"\n➕ FICHIERS SUPPLÉMENTAIRES:")
        for filename in extra_files[:5]:  # Limiter l'affichage
            print(f"   - {filename}")
        if len(extra_files) > 5:
            print(f"   ... et {len(extra_files) - 5} autres")
    
    if len(found_files) >= 20:  # Au moins 20 fichiers sur 35
        print(f"\n🎉 Correspondance suffisante! {len(found_files)} fichiers correspondent.")
        return True
    else:
        print(f"\n⚠️ Correspondance partielle. Seulement {len(found_files)} fichiers correspondent.")
        return False

if __name__ == "__main__":
    print("🚀 EXTRACTION FICHIERS AUDIO FAMILLE")
    print("📦 Source: ZIP uploadé via interface")
    print("=" * 50)
    print()
    
    success = extract_famille_audio_zip()
    
    if success:
        print()
        print("🎉 EXTRACTION TERMINÉE AVEC SUCCÈS!")
        print("📱 Les fichiers audio sont maintenant disponibles dans l'application")
        print("🎯 Prochaine étape: Tester la lecture audio dans l'app")
    else:
        print()
        print("💥 EXTRACTION ÉCHOUÉE")
        print("💡 Vérifiez le format du ZIP et réessayez")