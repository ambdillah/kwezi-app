"""
Script pour mettre à jour la section expressions avec les nouvelles données
ATTENTION: Orthographe exacte pour correspondance audio
"""

import sys
import os
from pymongo import MongoClient
import shutil
from pathlib import Path

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client['mayotte_app']
words_collection = db['words']

# Données des expressions avec orthographe EXACTE pour correspondance audio
nouvelles_expressions = [
    {
        "french": "En haut",
        "shimaore": "oujou",
        "kibouchi": "agnabou",
        "audio_shimaore": "Oujou.m4a",
        "audio_kibouchi": "Agnabou.m4a",
        "emoji": "⬆️"
    },
    {
        "french": "En bas",
        "shimaore": "outsini",
        "kibouchi": "ambani",
        "audio_shimaore": "Outsini.m4a",
        "audio_kibouchi": "Ambani.m4a",
        "emoji": "⬇️"
    },
    {
        "french": "Devant",
        "shimaore": "mbéli",
        "kibouchi": "alouha",
        "audio_shimaore": "Mbéli.m4a",
        "audio_kibouchi": "Alouha.m4a",
        "emoji": "👉"
    },
    {
        "french": "Derrière",
        "shimaore": "nyouma",
        "kibouchi": "anfara",
        "audio_shimaore": "Nyouma.m4a",
        "audio_kibouchi": "Anfara.m4a",
        "emoji": "👈"
    },
    {
        "french": "Loin",
        "shimaore": "mbali",
        "kibouchi": "lavitri",
        "audio_shimaore": "Mbali.m4a",
        "audio_kibouchi": None,  # Pas dans le ZIP
        "emoji": "↔️"
    },
    {
        "french": "Tout prêt",
        "shimaore": "karibou",
        "kibouchi": "marini",
        "audio_shimaore": None,  # Pas dans le ZIP
        "audio_kibouchi": "Marini.m4a",
        "emoji": "📍"
    },
    {
        "french": "Lundi",
        "shimaore": "mfoumo rarou",
        "kibouchi": "tinayini",
        "audio_shimaore": "Mfoumo rarou.m4a",
        "audio_kibouchi": "Tinayini.m4a",
        "emoji": "📅"
    },
    {
        "french": "Mardi",
        "shimaore": "mfoumo nhé",
        "kibouchi": "talata",
        "audio_shimaore": "Mfoumo nhé.m4a",
        "audio_kibouchi": "Talata.m4a",
        "emoji": "📅"
    },
    {
        "french": "Mercredi",
        "shimaore": "mfoumo tsano",
        "kibouchi": "roubiya",
        "audio_shimaore": "Mfoumo tsano.m4a",
        "audio_kibouchi": "Roubiya.m4a",
        "emoji": "📅"
    },
    {
        "french": "Jeudi",
        "shimaore": "yahowa",
        "kibouchi": "lahamissi",
        "audio_shimaore": "Yahowa.m4a",
        "audio_kibouchi": "Lahamissi.m4a",
        "emoji": "📅"
    },
    {
        "french": "Vendredi",
        "shimaore": "idjïmoi",
        "kibouchi": "djouma",
        "audio_shimaore": "Idjimoi.m4a",  # Sans tréma dans le fichier
        "audio_kibouchi": "Djouma.m4a",
        "emoji": "📅"
    },
    {
        "french": "Samedi",
        "shimaore": "mfoumo tsi",
        "kibouchi": "boutsi",
        "audio_shimaore": "Mfoumo tsi.m4a",
        "audio_kibouchi": "Boutsi.m4a",
        "emoji": "📅"
    },
    {
        "french": "Dimanche",
        "shimaore": "mfoumo vili",
        "kibouchi": "dimassi",
        "audio_shimaore": "Mfoumo vili.m4a",
        "audio_kibouchi": "Dimassi.m4a",
        "emoji": "📅"
    },
    {
        "french": "Semaine",
        "shimaore": "mfoumo",
        "kibouchi": "hérignandra",
        "audio_shimaore": "Mfoumo.m4a",
        "audio_kibouchi": "Hérignandra.m4a",
        "emoji": "📆"
    },
    {
        "french": "Mois",
        "shimaore": "mwézi",
        "kibouchi": "fandzava",
        "audio_shimaore": None,  # Pas de fichier Mwézi.m4a séparé
        "audio_kibouchi": None,  # Pas de fichier séparé
        "emoji": "🗓️"
    },
    {
        "french": "Année",
        "shimaore": "mwaha",
        "kibouchi": "moika",
        "audio_shimaore": "Mwaha.m4a",
        "audio_kibouchi": "Moika.m4a",
        "emoji": "📅"
    },
    {
        "french": "Enceinte",
        "shimaore": "oumïra",
        "kibouchi": "ankïbou",
        "audio_shimaore": "Oumira.m4a",  # Sans tréma
        "audio_kibouchi": "Ankibou.m4a",  # Sans tréma
        "emoji": "🤰"
    },
    {
        "french": "Demander un service",
        "shimaore": "oumiya hadja",
        "kibouchi": "mangataka hadja",
        "audio_shimaore": "Oumiya hadja.m4a",
        "audio_kibouchi": "Mangataka hadja.m4a",
        "emoji": "🙏"
    },
    {
        "french": "Épreuve",
        "shimaore": "mti'hano",
        "kibouchi": "machidranou",
        "audio_shimaore": "Mtihano.m4a",  # Sans apostrophe
        "audio_kibouchi": "Machindranou.m4a",  # 'n' au lieu de 'd' 
        "emoji": "📝"
    },
    {
        "french": "C'est amer",
        "shimaore": "ina nyongo",
        "kibouchi": "maféki",
        "audio_shimaore": "Ina nyongo.m4a",
        "audio_kibouchi": "Mafèki.m4a",  # Accent grave
        "emoji": "😖"
    },
    {
        "french": "C'est sucré",
        "shimaore": "ina nguizi",
        "kibouchi": "mami",
        "audio_shimaore": "Ina nguizi.m4a",
        "audio_kibouchi": "Mami.m4a",
        "emoji": "🍬"
    },
    {
        "french": "C'est acide",
        "shimaore": "ina kali",
        "kibouchi": "matsïkou",
        "audio_shimaore": "Ina kali.m4a",
        "audio_kibouchi": "Matsikou.m4a",  # Sans tréma
        "emoji": "🍋"
    }
]

def copier_fichiers_audio():
    """Copier les fichiers audio du dossier temporaire vers le dossier assets/audio"""
    source_dir = Path("/tmp/expressions_audio")
    dest_dir = Path("/app/frontend/assets/audio")
    
    if not dest_dir.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
    
    fichiers_copies = []
    fichiers_manquants = []
    
    for file in source_dir.rglob("*.m4a"):
        dest_file = dest_dir / file.name
        shutil.copy2(file, dest_file)
        fichiers_copies.append(file.name)
        print(f"✅ Copié: {file.name}")
    
    return fichiers_copies, fichiers_manquants

def mettre_a_jour_expressions():
    """Mettre à jour ou ajouter les expressions dans la base de données"""
    
    print("\n🔄 Mise à jour de la section expressions...\n")
    
    # Copier les fichiers audio
    print("📁 Copie des fichiers audio...")
    fichiers_copies, fichiers_manquants = copier_fichiers_audio()
    print(f"✅ {len(fichiers_copies)} fichiers audio copiés\n")
    
    expressions_ajoutees = 0
    expressions_mises_a_jour = 0
    
    for expr in nouvelles_expressions:
        french = expr['french']
        
        # Vérifier si l'expression existe déjà
        existing = words_collection.find_one({
            "french": {"$regex": f"^{french}$", "$options": "i"},
            "category": "expressions"
        })
        
        # Préparer le document
        document = {
            "french": french,
            "shimaore": expr['shimaore'],
            "kibouchi": expr['kibouchi'],
            "category": "expressions",
            "emoji": expr['emoji']
        }
        
        # Ajouter les champs audio si disponibles
        if expr['audio_shimaore']:
            document['audio_filename_shimaore'] = expr['audio_shimaore']
        
        if expr['audio_kibouchi']:
            document['audio_filename_kibouchi'] = expr['audio_kibouchi']
        
        # Ajouter les flags si au moins un audio existe
        if expr['audio_shimaore'] or expr['audio_kibouchi']:
            document['has_authentic_audio'] = True
            document['dual_audio_system'] = True
        
        if existing:
            # Mettre à jour l'expression existante
            words_collection.update_one(
                {"_id": existing['_id']},
                {"$set": document}
            )
            expressions_mises_a_jour += 1
            print(f"🔄 Mis à jour: {french}")
        else:
            # Ajouter la nouvelle expression
            words_collection.insert_one(document)
            expressions_ajoutees += 1
            print(f"➕ Ajouté: {french}")
        
        # Afficher l'état des audios
        audio_shim = f"✅ {expr['audio_shimaore']}" if expr['audio_shimaore'] else "❌ pas d'audio"
        audio_kib = f"✅ {expr['audio_kibouchi']}" if expr['audio_kibouchi'] else "❌ pas d'audio"
        print(f"   Shimaoré: {expr['shimaore']} {audio_shim}")
        print(f"   Kibouchi: {expr['kibouchi']} {audio_kib}")
        print()
    
    # Statistiques finales
    total_expressions = words_collection.count_documents({"category": "expressions"})
    expressions_avec_audio = words_collection.count_documents({
        "category": "expressions",
        "has_authentic_audio": True
    })
    
    print("\n" + "="*60)
    print("📊 STATISTIQUES FINALES")
    print("="*60)
    print(f"✅ Expressions ajoutées: {expressions_ajoutees}")
    print(f"🔄 Expressions mises à jour: {expressions_mises_a_jour}")
    print(f"📚 Total expressions dans la base: {total_expressions}")
    print(f"🔊 Expressions avec audio authentique: {expressions_avec_audio} ({expressions_avec_audio/total_expressions*100:.1f}%)")
    print(f"📁 Fichiers audio copiés: {len(fichiers_copies)}")
    print("="*60)

if __name__ == "__main__":
    try:
        mettre_a_jour_expressions()
        print("\n✅ Mise à jour de la section expressions terminée avec succès!")
    except Exception as e:
        print(f"\n❌ Erreur lors de la mise à jour: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
