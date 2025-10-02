#!/usr/bin/env python3
"""
Script pour générer un document HTML complet de vérification
avec TOUTES les traductions et audios
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connexion MongoDB
MONGO_URL = os.getenv('MONGO_URL')
DB_NAME = os.getenv('DB_NAME', 'mayotte_app')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
words_collection = db.words

# Récupérer toutes les catégories
categories = words_collection.distinct('category')
categories = sorted(categories)

print(f"📚 Génération du document de vérification...")
print(f"   Catégories trouvées: {len(categories)}")

# Début du HTML
html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kwezi - Vérification Vocabulaire Complet</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            padding: 20px;
            background: #f5f5f5;
        }
        
        .header {
            background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .stat-card .number {
            font-size: 2em;
            font-weight: bold;
            color: #4ECDC4;
        }
        
        .stat-card .label {
            color: #666;
            margin-top: 5px;
        }
        
        .category-section {
            background: white;
            margin-bottom: 30px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            page-break-inside: avoid;
        }
        
        .category-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            font-size: 1.5em;
            font-weight: bold;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th {
            background: #f8f9fa;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #2c3e50;
            border-bottom: 2px solid #dee2e6;
            position: sticky;
            top: 0;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #e9ecef;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .french {
            font-weight: 600;
            color: #2c3e50;
        }
        
        .shimaore {
            color: #667eea;
        }
        
        .kibouchi {
            color: #f093fb;
        }
        
        .audio-status {
            font-size: 0.9em;
        }
        
        .audio-yes {
            color: #28a745;
            font-weight: 600;
        }
        
        .audio-no {
            color: #dc3545;
            font-weight: 600;
        }
        
        .audio-file {
            font-size: 0.85em;
            color: #6c757d;
            font-family: monospace;
            display: block;
            margin-top: 3px;
        }
        
        .checkbox-col {
            width: 40px;
            text-align: center;
        }
        
        .checkbox-col input {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        
        .notes-col {
            min-width: 150px;
        }
        
        .notes-input {
            width: 100%;
            padding: 5px;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            font-size: 0.9em;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .header {
                background: #4ECDC4 !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
            
            .category-header {
                background: #667eea !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
            
            .category-section {
                page-break-inside: avoid;
                break-inside: avoid;
            }
            
            .stats {
                display: none;
            }
        }
        
        .toc {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .toc h2 {
            margin-bottom: 15px;
            color: #2c3e50;
        }
        
        .toc ul {
            list-style: none;
            padding-left: 0;
        }
        
        .toc li {
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
        }
        
        .toc a {
            color: #4ECDC4;
            text-decoration: none;
            font-weight: 500;
        }
        
        .toc a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 Kwezi - Vérification Vocabulaire</h1>
        <p>Document de contrôle complet des traductions et audios</p>
        <p style="font-size: 0.9em; margin-top: 10px;">Généré le: """ + os.popen('date "+%d/%m/%Y à %H:%M"').read().strip() + """</p>
    </div>
"""

# Calculer les statistiques globales
total_words = words_collection.count_documents({})
total_with_sh_audio = words_collection.count_documents({'shimoare_has_audio': True})
total_with_kb_audio = words_collection.count_documents({'kibouchi_has_audio': True})

html_content += f"""
    <div class="stats">
        <div class="stat-card">
            <div class="number">{total_words}</div>
            <div class="label">Mots Total</div>
        </div>
        <div class="stat-card">
            <div class="number">{len(categories)}</div>
            <div class="label">Catégories</div>
        </div>
        <div class="stat-card">
            <div class="number">{total_with_sh_audio}</div>
            <div class="label">Audio Shimaoré</div>
        </div>
        <div class="stat-card">
            <div class="number">{total_with_kb_audio}</div>
            <div class="label">Audio Kibouchi</div>
        </div>
    </div>
"""

# Table des matières
html_content += """
    <div class="toc">
        <h2>📑 Table des Matières</h2>
        <ul>
"""

for category in categories:
    count = words_collection.count_documents({'category': category})
    html_content += f'            <li><a href="#{category}">{category.upper()} ({count} mots)</a></li>\n'

html_content += """
        </ul>
    </div>
"""

# Générer une section pour chaque catégorie
for category in categories:
    words = list(words_collection.find({'category': category}).sort('french', 1))
    
    if not words:
        continue
    
    print(f"   ✓ {category}: {len(words)} mots")
    
    html_content += f"""
    <div class="category-section" id="{category}">
        <div class="category-header">
            📚 {category.upper()} ({len(words)} mots)
        </div>
        <table>
            <thead>
                <tr>
                    <th class="checkbox-col">✓</th>
                    <th>Français</th>
                    <th>Shimaoré</th>
                    <th>Audio Shimaoré</th>
                    <th>Kibouchi</th>
                    <th>Audio Kibouchi</th>
                    <th class="notes-col">Notes / Corrections</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for word in words:
        french = word.get('french', 'N/A')
        shimaore = word.get('shimaore', 'N/A')
        kibouchi = word.get('kibouchi', 'N/A')
        
        audio_sh = word.get('audio_shimaore', '')
        audio_kb = word.get('audio_kibouchi', '')
        
        has_sh_audio = word.get('shimoare_has_audio', False)
        has_kb_audio = word.get('kibouchi_has_audio', False)
        
        # Format audio status
        if has_sh_audio and audio_sh:
            audio_sh_display = f'<span class="audio-yes">✓ OUI</span><span class="audio-file">{audio_sh}</span>'
        else:
            audio_sh_display = '<span class="audio-no">✗ NON</span>'
        
        if has_kb_audio and audio_kb:
            audio_kb_display = f'<span class="audio-yes">✓ OUI</span><span class="audio-file">{audio_kb}</span>'
        else:
            audio_kb_display = '<span class="audio-no">✗ NON</span>'
        
        html_content += f"""
                <tr>
                    <td class="checkbox-col"><input type="checkbox"></td>
                    <td class="french">{french}</td>
                    <td class="shimaore">{shimaore}</td>
                    <td class="audio-status">{audio_sh_display}</td>
                    <td class="kibouchi">{kibouchi}</td>
                    <td class="audio-status">{audio_kb_display}</td>
                    <td class="notes-col"><input type="text" class="notes-input" placeholder="Corriger..."></td>
                </tr>
"""
    
    html_content += """
            </tbody>
        </table>
    </div>
"""

# Fin du HTML
html_content += """
</body>
</html>
"""

# Sauvegarder le fichier
output_file = '/app/VERIFICATION_VOCABULAIRE_COMPLET.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n✅ Document généré: {output_file}")
print(f"\n📊 RÉSUMÉ:")
print(f"   Total mots: {total_words}")
print(f"   Catégories: {len(categories)}")
print(f"   Audio Shimaoré: {total_with_sh_audio}/{total_words} ({int(total_with_sh_audio/total_words*100)}%)")
print(f"   Audio Kibouchi: {total_with_kb_audio}/{total_words} ({int(total_with_kb_audio/total_words*100)}%)")

print(f"\n📥 Pour télécharger le fichier:")
print(f"   Le fichier est disponible à: /app/VERIFICATION_VOCABULAIRE_COMPLET.html")
print(f"   Tu peux l'ouvrir dans un navigateur et l'exporter en PDF")

client.close()
