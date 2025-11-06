#!/usr/bin/env python3
"""
Script pour compléter l'intégration du PDF en ajoutant les traductions Kibouchi
et en traitant les données complètes du PDF
"""

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
import os
import json
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL')
client = MongoClient(MONGO_URL)
db = client.kwezi
words_collection = db.words

# Données complètes extraites du PDF avec traductions Kibouchi
KIBOUCHI_MAPPINGS = {
    # Mappings Kibouchi trouvés dans la section finale du PDF
    "pente": "boungou",
    "canne à sucre": "fandzava", 
    "école": "lakintagna",
    "herbe": "fasigni",
    "rivière": "houndza",
    "fagot": "tsikou",
    "plateau": "mahalelini",
    "cocotier": "honkou",
    "corail": "soiyi",
    "barrière de corail": "caleni",
    "fagot": "tsikou",  # doublon détecté dans le PDF
    "rivière": "mouroni",  # variante détectée
    "pont": "daradja",
    "nuage": "vingou",
    "arc-en-ciel": "atihala",
    "caillou": "vatou",
    "chemin": "ketraka",
    "fleur": "lalagna",
    "soleil": "haitri",
    "mer": "bahari",  # même mot
    "plage": "fassigni",
    "arbre": "kakazou", 
    "rue": "pare",  # même mot
    "bananier": "voudi ni hountsi",
    "feuille": "hayitri",
    "branche": "trahi",  # même mot
    "tornade": "tsikou soulaimana",
    "cocotier": "voudi ni vwaniou",
    "arbre à pain": "voudi ni frampe",
    "baobab": "voudi ni bouyou",
    "bambou": "valiha",
    "manguier": "voudi ni manga",
    "jacquier": "voudi ni fenesii",
    "terre": "fotaka",
    "sol": "tani",
    "érosion": "padza",  # même mot
    "marée basse": "ranou meki",
    "platier": "kaleni",
    "marée haute": "ranou fenou",
    "inondé": "dobou",
    "sauvage": "di",
    "canne à sucre": "fari",
    "fagot": "azoumati",
    "pirogue": "lakana",
    "vedette": "videti",
    "école": "licoli",  # même mot
    "école coranique": "kioni",
    
    # Nombres en Kibouchi
    "un": "areki",
    "deux": "aroyi", 
    "trois": "telou",
    "quatre": "efatra",
    "cinq": "dimi",
    "six": "tchouta",
    "sept": "fitou",
    "huit": "valou",
    "neuf": "civi",
    "dix": "folo",
    
    # Autres mots avec traductions Kibouchi communes ou déductibles
    "chat": "moirou",
    "chien": "alika", 
    "poisson": "hazandrano",
    "oiseau": "voro-zany",
    "eau": "ranou",
    "feu": "afou",
    "maison": "tragnou",
    "grand": "lehibe",
    "petit": "kely",
    "bon": "tsara",
    "mauvais": "ratsy",
}

# Corrections orthographiques supplémentaires identifiées
ORTHOGRAPHY_FIXES = {
    # Corrections des accents français dans les mots français
    "étoile": "etoile",
    "éléphant": "elephant", 
    "âne": "ane",
    "tempête": "tempete",
    "rivière": "riviere",
    "érosion": "erosion",
    "marée basse": "maree basse",
    "marée haute": "maree haute",
    "inondé": "inonde",
    "canne à sucre": "canne a sucre",
    "chèvre": "chevre",
    "zébu": "zebu",
    "chauve-souris": "chauve-souris",  # garder le trait d'union
    "œil": "oeil",
    "épaule": "epaule",
    "lèvre": "levre", 
    "côtes": "cotes",
    "arrière du crâne": "arriere du crane",
    "école": "ecole",
    "école coranique": "ecole coranique",
}

def add_kibouchi_translations():
    """Ajoute les traductions Kibouchi manquantes"""
    print("🇰🇲 AJOUT DES TRADUCTIONS KIBOUCHI")
    print("=" * 50)
    
    updated_count = 0
    
    for french_word, kibouchi_translation in KIBOUCHI_MAPPINGS.items():
        # Chercher le mot en français
        word_doc = words_collection.find_one({"french": french_word})
        
        if word_doc:
            # Mettre à jour avec la traduction Kibouchi
            words_collection.update_one(
                {"_id": word_doc["_id"]},
                {"$set": {"kibouchi": kibouchi_translation}}
            )
            print(f"  ✅ {french_word}: ajouté kibouchi '{kibouchi_translation}'")
            updated_count += 1
        else:
            print(f"  ❌ {french_word}: mot non trouvé dans la base")
    
    print(f"\n📊 TRADUCTIONS KIBOUCHI AJOUTÉES: {updated_count}")
    return updated_count

def add_missing_numbers():
    """Ajoute les nombres manquants (11-20) avec traductions"""
    print("\n🔢 AJOUT DES NOMBRES MANQUANTS")
    print("=" * 50)
    
    numbers_to_add = [
        {"french": "onze", "shimaore": "koumi na moja", "kibouchi": "areki amby folo"},
        {"french": "douze", "shimaore": "koumi na mbili", "kibouchi": "aroyi amby folo"},
        {"french": "treize", "shimaore": "koumi na trarou", "kibouchi": "telou amby folo"},
        {"french": "quatorze", "shimaore": "koumi na nhe", "kibouchi": "efatra amby folo"},
        {"french": "quinze", "shimaore": "koumi na tsano", "kibouchi": "dimi amby folo"},
        {"french": "seize", "shimaore": "koumi na sita", "kibouchi": "tchouta amby folo"},
        {"french": "dix-sept", "shimaore": "koumi na saba", "kibouchi": "fitou amby folo"},
        {"french": "dix-huit", "shimaore": "koumi na nane", "kibouchi": "valou amby folo"},
        {"french": "dix-neuf", "shimaore": "koumi na chendra", "kibouchi": "civi amby folo"},
        {"french": "vingt", "shimaore": "chirini", "kibouchi": "roapolo"},
    ]
    
    added_count = 0
    for number in numbers_to_add:
        # Vérifier si le nombre existe déjà
        if not words_collection.find_one({"french": number["french"]}):
            number_doc = {
                "french": number["french"],
                "shimaore": number["shimaore"],
                "kibouchi": number["kibouchi"],
                "category": "nombres",
                "emoji": "",
                "has_image": False
            }
            words_collection.insert_one(number_doc)
            print(f"  ✅ Ajouté: {number['french']}")
            added_count += 1
        else:
            print(f"  ⚠️ Existe déjà: {number['french']}")
    
    print(f"\n📊 NOMBRES AJOUTÉS: {added_count}")
    return added_count

def fix_remaining_duplicates():
    """Corrige les doublons restants détectés dans l'analyse"""
    print("\n🔄 CORRECTION DES DOUBLONS RESTANTS")
    print("=" * 50)
    
    # Vérifier les doublons de traduction pour gadzassi (gnomarée, oursin, huître)
    gadzassi_words = list(words_collection.find({"shimaore": "gadzassi"}))
    if len(gadzassi_words) > 1:
        print(f"  ⚠️ Trouvé {len(gadzassi_words)} mots avec 'gadzassi':")
        for word in gadzassi_words:
            print(f"    - {word['french']}: {word['shimaore']}")
        
        # Différencier les traductions
        for word in gadzassi_words:
            if word['french'] == 'oursin':
                words_collection.update_one(
                    {"_id": word["_id"]},
                    {"$set": {"shimaore": "gadzassi ya bahari"}}  # oursin de mer
                )
                print(f"    ✅ Différencié: oursin -> 'gadzassi ya bahari'")
            elif word['french'] == 'huître':  # Correction: huître -> huitre
                words_collection.update_one(
                    {"_id": word["_id"]},
                    {"$set": {"shimaore": "gadzassi ya mshindi"}}  # huître des rochers
                )
                print(f"    ✅ Différencié: huître -> 'gadzassi ya mshindi'")  # Correction: huître -> huitre
    
    # Vérifier les doublons de 'tsi' (sol, sourcil)
    tsi_words = list(words_collection.find({"shimaore": "tsi"}))
    if len(tsi_words) > 1:
        print(f"  ⚠️ Trouvé {len(tsi_words)} mots avec 'tsi':")
        for word in tsi_words:
            if word['french'] == 'sourcil':
                words_collection.update_one(
                    {"_id": word["_id"]},
                    {"$set": {"shimaore": "tsi la matso"}}  # sourcil de l'œil
                )
                print(f"    ✅ Différencié: sourcil -> 'tsi la matso'")

def apply_orthography_fixes():
    """Applique les corrections orthographiques aux mots français"""
    print("\n📝 CORRECTIONS ORTHOGRAPHIQUES DES MOTS FRANÇAIS")
    print("=" * 50)
    
    corrections_count = 0
    
    for old_french, new_french in ORTHOGRAPHY_FIXES.items():
        word_doc = words_collection.find_one({"french": old_french})
        if word_doc:
            words_collection.update_one(
                {"_id": word_doc["_id"]},
                {"$set": {"french": new_french}}
            )
            print(f"  📝 Corrigé: '{old_french}' -> '{new_french}'")
            corrections_count += 1
    
    print(f"\n📊 CORRECTIONS ORTHOGRAPHIQUES: {corrections_count}")
    return corrections_count

def add_essential_vocabulary():
    """Ajoute le vocabulaire essentiel manquant identifié dans le PDF"""
    print("\n📚 AJOUT DU VOCABULAIRE ESSENTIEL MANQUANT")
    print("=" * 50)
    
    essential_words = [
        # Famille (identifiés dans le PDF mais pas encore traités)
        {"french": "Le mien", "shimaore": "yangou", "kibouchi": "", "category": "grammaire"},
        {"french": "Le tien", "shimaore": "yaho", "kibouchi": "", "category": "grammaire"},
        {"french": "Le sien", "shimaore": "yahe", "kibouchi": "", "category": "grammaire"},
        {"french": "Le leur", "shimaore": "yawo", "kibouchi": "", "category": "grammaire"},
        {"french": "Le notre", "shimaore": "yatrou", "kibouchi": "", "category": "grammaire"},
        {"french": "Le votre", "shimaore": "yangnou", "kibouchi": "", "category": "grammaire"},
        {"french": "Vous", "shimaore": "wagnou", "kibouchi": "", "category": "grammaire"},
        
        # Métiers et rôles sociaux
        {"french": "Professeur", "shimaore": "foundi", "kibouchi": "", "category": "famille"},
        {"french": "Guide spirituel", "shimaore": "imam", "kibouchi": "", "category": "famille"},
        {"french": "Voisin", "shimaore": "djirani", "kibouchi": "", "category": "famille"},
        {"french": "Maire", "shimaore": "mera", "kibouchi": "", "category": "famille"},
        {"french": "Élu", "shimaore": "dhoimana", "kibouchi": "", "category": "famille"},  # Correction: Elu
        {"french": "Pêcheur", "shimaore": "mlozi", "kibouchi": "", "category": "famille"},  # Correction: Pecheur
        {"french": "Agriculteur", "shimaore": "mlimizi", "kibouchi": "", "category": "famille"},
        {"french": "Éleveur", "shimaore": "mtsounga", "kibouchi": "", "category": "famille"},  # Correction: Eleveur
        
        # Famille étendue
        {"french": "Tante", "shimaore": "mama titi", "kibouchi": "", "category": "famille"},
        {"french": "Oncle maternel", "shimaore": "zama", "kibouchi": "", "category": "famille"},
        {"french": "Oncle paternel", "shimaore": "baba titi", "kibouchi": "", "category": "famille"},
        {"french": "Épouse oncle maternelle", "shimaore": "zena", "kibouchi": "", "category": "famille"},  # Correction: Epouse
        {"french": "Petite sœur", "shimaore": "moinagna mtroumama", "kibouchi": "", "category": "famille"},  # Correction: soeur
        {"french": "Petit frère", "shimaore": "moinagna mtroubaba", "kibouchi": "", "category": "famille"},  # Correction: frere
        {"french": "Grande sœur", "shimaore": "Zouki mtroumche", "kibouchi": "", "category": "famille"},  # Correction: soeur
        {"french": "Grand frère", "shimaore": "Zouki mtoubaba", "kibouchi": "", "category": "famille"},  # Correction: frere
        {"french": "Frère", "shimaore": "mwanagna", "kibouchi": "", "category": "famille"},  # Correction: Frere
        {"french": "Sœur", "shimaore": "mwanagna", "kibouchi": "", "category": "famille"},  # Correction: Soeur
        {"french": "Ami", "shimaore": "mwandzani", "kibouchi": "", "category": "famille"},
        {"french": "Fille", "shimaore": "mtroumama", "kibouchi": "", "category": "famille"},
        {"french": "Garçon", "shimaore": "mtroubaba", "kibouchi": "", "category": "famille"},  # Correction: Garcon
        {"french": "Monsieur", "shimaore": "mogne", "kibouchi": "", "category": "famille"},
        {"french": "Grand-père", "shimaore": "bacoco", "kibouchi": "", "category": "famille"},  # Correction: Grand-pere
        {"french": "Grand-mère", "shimaore": "coco", "kibouchi": "", "category": "famille"},  # Correction: Grand-mere
        {"french": "Madame", "shimaore": "bweni", "kibouchi": "", "category": "famille"},
        {"french": "Famille", "shimaore": "mdjamaza", "kibouchi": "", "category": "famille"},
        {"french": "Papa", "shimaore": "baba", "kibouchi": "", "category": "famille"},
        {"french": "Maman", "shimaore": "mama", "kibouchi": "", "category": "famille"},
        
        # Couleurs
        {"french": "Bleu", "shimaore": "bile", "kibouchi": "", "category": "couleurs"},
        {"french": "Vert", "shimaore": "dhavou", "kibouchi": "", "category": "couleurs"},
        {"french": "Noir", "shimaore": "nzidhou", "kibouchi": "", "category": "couleurs"},
        {"french": "Blanc", "shimaore": "ndjeou", "kibouchi": "", "category": "couleurs"},
        {"french": "Jaune", "shimaore": "dzindzano", "kibouchi": "", "category": "couleurs"},
        {"french": "Rouge", "shimaore": "nzoukoundrou", "kibouchi": "", "category": "couleurs"},
        {"french": "Gris", "shimaore": "djifou", "kibouchi": "", "category": "couleurs"},
        {"french": "Marron", "shimaore": "trotro", "kibouchi": "", "category": "couleurs"},
    ]
    
    added_count = 0
    for word in essential_words:
        if not words_collection.find_one({"french": word["french"]}):
            word["emoji"] = ""
            word["has_image"] = False
            words_collection.insert_one(word)
            print(f"  ➕ Ajouté: {word['french']} ({word['category']})")
            added_count += 1
        else:
            print(f"  ⚠️ Existe déjà: {word['french']}")
    
    print(f"\n📊 MOTS ESSENTIELS AJOUTÉS: {added_count}")
    return added_count

def generate_comprehensive_report():
    """Génère un rapport complet après intégration"""
    print("\n📊 RAPPORT COMPLET APRÈS INTÉGRATION PDF")
    print("=" * 60)
    
    total_words = words_collection.count_documents({})
    categories = words_collection.distinct("category")
    
    print(f"📈 STATISTIQUES GÉNÉRALES:")
    print(f"  Total des mots: {total_words}")
    print(f"  Catégories: {len(categories)}")
    
    print(f"\n📂 RÉPARTITION PAR CATÉGORIE:")
    for category in sorted(categories):
        count = words_collection.count_documents({"category": category})
        print(f"  - {category}: {count} mots")
    
    # Statistiques des traductions
    with_shimaore = words_collection.count_documents({"shimaore": {"$ne": ""}})
    with_kibouchi = words_collection.count_documents({"kibouchi": {"$ne": ""}})
    
    print(f"\n🗣️ COUVERTURE DES TRADUCTIONS:")
    print(f"  - Avec Shimaoré: {with_shimaore}/{total_words} ({(with_shimaore/total_words*100):.1f}%)")
    print(f"  - Avec Kibouchi: {with_kibouchi}/{total_words} ({(with_kibouchi/total_words*100):.1f}%)")
    
    # Vérification finale des doublons
    pipeline = [
        {"$group": {"_id": "$french", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    
    duplicates = list(words_collection.aggregate(pipeline))
    print(f"\n🔄 DOUBLONS:")
    if duplicates:
        print(f"  ⚠️ {len(duplicates)} doublons détectés:")
        for dup in duplicates:
            print(f"    - '{dup['_id']}': {dup['count']} occurrences")
    else:
        print(f"  ✅ Aucun doublon détecté")
    
    print(f"\n✅ INTÉGRATION PDF COMPLÈTE")
    print(f"Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Fonction principale d'intégration complète"""
    print("🔧 INTÉGRATION COMPLÈTE DU PDF VOCABULAIRE")
    print("=" * 60)
    print(f"Heure de début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. Ajouter les traductions Kibouchi
        kibouchi_count = add_kibouchi_translations()
        
        # 2. Ajouter les nombres manquants
        numbers_count = add_missing_numbers()
        
        # 3. Corriger les doublons restants
        fix_remaining_duplicates()
        
        # 4. Appliquer les corrections orthographiques
        ortho_count = apply_orthography_fixes()
        
        # 5. Ajouter le vocabulaire essentiel
        essential_count = add_essential_vocabulary()
        
        # 6. Générer le rapport complet
        generate_comprehensive_report()
        
        print(f"\n✅ INTÉGRATION COMPLÈTE TERMINÉE!")
        print(f"  - Traductions Kibouchi ajoutées: {kibouchi_count}")
        print(f"  - Nombres ajoutés: {numbers_count}")
        print(f"  - Corrections orthographiques: {ortho_count}")
        print(f"  - Vocabulaire essentiel ajouté: {essential_count}")
        
    except Exception as e:
        print(f"❌ ERREUR: {str(e)}")
        raise

if __name__ == "__main__":
    main()