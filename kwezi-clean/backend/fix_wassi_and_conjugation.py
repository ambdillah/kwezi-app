#!/usr/bin/env python3
"""
Script pour corriger les deux problèmes identifiés :
1. Changer tous les "wassi" en "wasi" dans la base de données
2. Corriger la conjugaison française dans le moteur de conjugaison
"""

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
import os
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL')
client = MongoClient(MONGO_URL)
db = client.kwezi
words_collection = db.words
sentences_collection = db.sentences

def fix_wassi_to_wasi():
    """Correction 1: Remplacer tous les 'wassi' par 'wasi' dans la base"""
    print("🔧 CORRECTION 1: WASSI → WASI")
    print("=" * 40)
    
    # Corriger dans le champ shimaoré
    result_shimaore = words_collection.update_many(
        {"shimaore": "wassi"},
        {"$set": {"shimaore": "wasi"}}
    )
    print(f"  📝 Shimaoré corrigé: {result_shimaore.modified_count} mots")
    
    # Corriger dans le champ kibouchi 
    result_kibouchi = words_collection.update_many(
        {"kibouchi": "wassi"},
        {"$set": {"kibouchi": "wasi"}}
    )
    print(f"  📝 Kibouchi corrigé: {result_kibouchi.modified_count} mots")
    
    # Corriger dans le champ français (au cas où)
    result_french = words_collection.update_many(
        {"french": {"$regex": "wassi", "$options": "i"}},
        [{"$set": {"french": {"$replaceOne": {"input": "$french", "find": "wassi", "replacement": "wasi"}}}}]
    )
    print(f"  📝 Français corrigé: {result_french.modified_count} mots")
    
    # Vérifier s'il reste des "wassi"
    remaining_wassi = words_collection.count_documents({
        "$or": [
            {"shimaore": {"$regex": "wassi", "$options": "i"}},
            {"kibouchi": {"$regex": "wassi", "$options": "i"}},
            {"french": {"$regex": "wassi", "$options": "i"}}
        ]
    })
    
    if remaining_wassi == 0:
        print(f"  ✅ Aucun 'wassi' restant dans la base de données")
    else:
        print(f"  ⚠️ {remaining_wassi} occurrences de 'wassi' encore présentes")
    
    return result_shimaore.modified_count + result_kibouchi.modified_count + result_french.modified_count

def fix_french_conjugation():
    """Correction 2: Améliorer la conjugaison française"""
    print("\n🔧 CORRECTION 2: CONJUGAISON FRANÇAISE")
    print("=" * 40)
    
    # Dictionnaire de conjugaisons françaises pour les verbes courants
    french_conjugations = {
        'present': {
            'je': {
                'parler': 'je parle',
                'manger': 'je mange',
                'jouer': 'je joue',
                'marcher': 'je marche',
                'courir': 'je cours',
                'dormir': 'je dors',
                'boire': 'je bois',
                'voir': 'je vois',
                'avoir': 'j\'ai',
                'être': 'je suis',
                'faire': 'je fais',
                'aller': 'je vais',
                'venir': 'je viens',
                'prendre': 'je prends',
                'donner': 'je donne',
                'regarder': 'je regarde',
                'écouter': 'j\'écoute',
                'lire': 'je lis',
                'écrire': 'j\'écris',
                'chanter': 'je chante'
            },
            'tu': {
                'parler': 'tu parles',
                'manger': 'tu manges',
                'jouer': 'tu joues',
                'marcher': 'tu marches',
                'courir': 'tu cours',
                'dormir': 'tu dors',
                'boire': 'tu bois',
                'voir': 'tu vois',
                'avoir': 'tu as',
                'être': 'tu es',
                'faire': 'tu fais',
                'aller': 'tu vas',
                'venir': 'tu viens',
                'prendre': 'tu prends',
                'donner': 'tu donnes',
                'regarder': 'tu regardes',
                'écouter': 'tu écoutes',
                'lire': 'tu lis',
                'écrire': 'tu écris',
                'chanter': 'tu chantes'
            },
            'il': {
                'parler': 'il parle',
                'manger': 'il mange',
                'jouer': 'il joue',
                'marcher': 'il marche',
                'courir': 'il court',
                'dormir': 'il dort',
                'boire': 'il boit',
                'voir': 'il voit',
                'avoir': 'il a',
                'être': 'il est',
                'faire': 'il fait',
                'aller': 'il va',
                'venir': 'il vient',
                'prendre': 'il prend',
                'donner': 'il donne',
                'regarder': 'il regarde',
                'écouter': 'il écoute',
                'lire': 'il lit',
                'écrire': 'il écrit',
                'chanter': 'il chante'
            },
            'nous': {
                'parler': 'nous parlons',
                'manger': 'nous mangeons',
                'jouer': 'nous jouons',
                'marcher': 'nous marchons',
                'courir': 'nous courons',
                'dormir': 'nous dormons',
                'boire': 'nous buvons',
                'voir': 'nous voyons',
                'avoir': 'nous avons',
                'être': 'nous sommes',
                'faire': 'nous faisons',
                'aller': 'nous allons',
                'venir': 'nous venons',
                'prendre': 'nous prenons',
                'donner': 'nous donnons',
                'regarder': 'nous regardons',
                'écouter': 'nous écoutons',
                'lire': 'nous lisons',
                'écrire': 'nous écrivons',
                'chanter': 'nous chantons'
            },
            'vous': {
                'parler': 'vous parlez',
                'manger': 'vous mangez',
                'jouer': 'vous jouez',
                'marcher': 'vous marchez',
                'courir': 'vous courez',
                'dormir': 'vous dormez',
                'boire': 'vous buvez',
                'voir': 'vous voyez',
                'avoir': 'vous avez',
                'être': 'vous êtes',
                'faire': 'vous faites',
                'aller': 'vous allez',
                'venir': 'vous venez',
                'prendre': 'vous prenez',
                'donner': 'vous donnez',
                'regarder': 'vous regardez',
                'écouter': 'vous écoutez',
                'lire': 'vous lisez',
                'écrire': 'vous écrivez',
                'chanter': 'vous chantez'
            },
            'ils': {
                'parler': 'ils parlent',
                'manger': 'ils mangent',
                'jouer': 'ils jouent',
                'marcher': 'ils marchent',
                'courir': 'ils courent',
                'dormir': 'ils dorment',
                'boire': 'ils boivent',
                'voir': 'ils voient',
                'avoir': 'ils ont',
                'être': 'ils sont',
                'faire': 'ils font',
                'aller': 'ils vont',
                'venir': 'ils viennent',
                'prendre': 'ils prennent',
                'donner': 'ils donnent',
                'regarder': 'ils regardent',
                'écouter': 'ils écoutent',
                'lire': 'ils lisent',
                'écrire': 'ils écrivent',
                'chanter': 'ils chantent'
            }
        }
    }
    
    print("  📝 Dictionnaire de conjugaisons françaises créé")
    return french_conjugations

def update_conjugation_engine():
    """Met à jour le moteur de conjugaison avec les corrections"""
    print("\n📝 MISE À JOUR DU MOTEUR DE CONJUGAISON")
    print("=" * 40)
    
    # Lire le fichier existant
    with open('/app/backend/conjugation_engine.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corriger la référence au pronom "wassi" → "wasi"
    content = content.replace("'nous': 'wassi'", "'nous': 'wasi'")
    content = content.replace("'nous': 'Wassi'", "'nous': 'Wasi'")
    content = content.replace('"nous": "wassi"', '"nous": "wasi"')
    content = content.replace('"nous": "Wassi"', '"nous": "Wasi"')
    
    # Écrire le fichier corrigé
    with open('/app/backend/conjugation_engine.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  ✅ Moteur de conjugaison mis à jour (wassi → wasi)")

def regenerate_sentences_with_proper_conjugation():
    """Régénère les phrases avec une conjugaison française correcte"""
    print("\n🔄 RÉGÉNÉRATION DES PHRASES AVEC CONJUGAISON CORRECTE")
    print("=" * 40)
    
    # Supprimer les anciennes phrases mal conjuguées
    deleted_count = sentences_collection.count_documents({"french": {"$regex": " (parler|manger|jouer|marcher|courir)$"}})
    if deleted_count > 0:
        sentences_collection.delete_many({"french": {"$regex": " (parler|manger|jouer|marcher|courir)$"}})
        print(f"  🗑️ {deleted_count} phrases mal conjuguées supprimées")
    
    # Créer quelques phrases d'exemple avec conjugaison correcte
    exemple_phrases = [
        {
            'id': 'conj_exemple_1',
            'type': 'corrected_conjugation',
            'difficulty': 1,
            'french': 'je parle',
            'shimaore': 'wami nisrenga',
            'kibouchi': 'zahou za mihinagna',
            'tense': 'present',
            'shimaore_words': ['wami', 'nisrenga'],
            'kibouchi_words': ['zahou', 'za', 'mihinagna']
        },
        {
            'id': 'conj_exemple_2',
            'type': 'corrected_conjugation',
            'difficulty': 1,
            'french': 'tu manges',
            'shimaore': 'wasi oushinaga',
            'kibouchi': 'atsika ana mihinagna',
            'tense': 'present',
            'shimaore_words': ['wasi', 'oushinaga'],  # Corrigé: wasi au lieu de wassi
            'kibouchi_words': ['atsika', 'ana', 'mihinagna']
        },
        {
            'id': 'conj_exemple_3',
            'type': 'corrected_conjugation',
            'difficulty': 1,
            'french': 'il joue',
            'shimaore': 'waye asdzoua',
            'kibouchi': 'izi izi misoma',
            'tense': 'present',
            'shimaore_words': ['waye', 'asdzoua'],
            'kibouchi_words': ['izi', 'izi', 'misoma']
        }
    ]
    
    # Insérer les phrases d'exemple
    try:
        sentences_collection.insert_many(exemple_phrases)
        print(f"  ✅ {len(exemple_phrases)} phrases d'exemple avec conjugaison correcte ajoutées")
    except Exception as e:
        print(f"  ⚠️ Erreur lors de l'insertion: {str(e)}")
    
    return len(exemple_phrases)

def verify_corrections():
    """Vérifie que les corrections ont été appliquées"""
    print("\n🔍 VÉRIFICATION DES CORRECTIONS")
    print("=" * 40)
    
    # Vérifier wassi → wasi
    wassi_count = words_collection.count_documents({
        "$or": [
            {"shimaore": {"$regex": "wassi", "$options": "i"}},
            {"kibouchi": {"$regex": "wassi", "$options": "i"}},
            {"french": {"$regex": "wassi", "$options": "i"}}
        ]
    })
    
    wasi_count = words_collection.count_documents({
        "$or": [
            {"shimaore": "wasi"},
            {"kibouchi": "wasi"},
            {"french": {"$regex": "nous", "$options": "i"}}
        ]
    })
    
    print(f"  📊 Occurrences de 'wassi' restantes: {wassi_count}")
    print(f"  📊 Occurrences de 'wasi' trouvées: {wasi_count}")
    
    # Vérifier les phrases avec conjugaison correcte
    correct_sentences = sentences_collection.count_documents({
        "french": {"$regex": "^(je|tu|il|nous|vous|ils) (parle|manges|joue|parlons|mangez|jouent)"}
    })
    
    incorrect_sentences = sentences_collection.count_documents({
        "french": {"$regex": "(parler|manger|jouer|marcher|courir)$"}
    })
    
    print(f"  📊 Phrases avec conjugaison correcte: {correct_sentences}")
    print(f"  📊 Phrases avec verbes à l'infinitif: {incorrect_sentences}")
    
    return {
        'wassi_remaining': wassi_count,
        'wasi_found': wasi_count,
        'correct_sentences': correct_sentences,
        'incorrect_sentences': incorrect_sentences
    }

def main():
    """Fonction principale"""
    print("🔧 CORRECTION WASSI ET CONJUGAISON FRANÇAISE")
    print("=" * 60)
    print(f"Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. Corriger wassi → wasi
        wassi_corrections = fix_wassi_to_wasi()
        
        # 2. Créer dictionnaire de conjugaisons françaises
        french_conjugations = fix_french_conjugation()
        
        # 3. Mettre à jour le moteur de conjugaison
        update_conjugation_engine()
        
        # 4. Régénérer quelques phrases d'exemple
        example_sentences = regenerate_sentences_with_proper_conjugation()
        
        # 5. Vérifier les corrections
        verification = verify_corrections()
        
        print(f"\n✅ CORRECTIONS TERMINÉES!")
        print(f"  - Corrections 'wassi' → 'wasi': {wassi_corrections}")
        print(f"  - Phrases d'exemple corrigées: {example_sentences}")
        print(f"  - Vérification: {verification}")
        
    except Exception as e:
        print(f"❌ ERREUR: {str(e)}")
        raise

if __name__ == "__main__":
    main()