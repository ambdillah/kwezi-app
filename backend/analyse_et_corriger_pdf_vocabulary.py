#!/usr/bin/env python3
"""
Script pour analyser et corriger la base de données en fonction du PDF fourni
Élimine les doublons, corrige les orthographes et intègre les nouvelles données
"""

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
import os
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import json
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL')
if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable is required")

client = MongoClient(MONGO_URL)
db = client.kwezi
words_collection = db.words

# Données du PDF avec corrections orthographiques
PDF_VOCABULARY = {
    # Nature section avec corrections
    "pente": {"shimaore": "mlima", "kibouchi": "", "category": "nature"},
    "lune": {"shimaore": "mwezi", "kibouchi": "", "category": "nature"},  # Correction: mwézi -> mwezi
    "étoile": {"shimaore": "gnora", "kibouchi": "", "category": "nature"},
    "sable": {"shimaore": "mtsanga", "kibouchi": "", "category": "nature"},
    "vague": {"shimaore": "dhouja", "kibouchi": "", "category": "nature"},
    "vent": {"shimaore": "pevo", "kibouchi": "", "category": "nature"},  # Correction: pévo -> pevo
    "pluie": {"shimaore": "vhoua", "kibouchi": "", "category": "nature"},
    "mangrove": {"shimaore": "mhonko", "kibouchi": "", "category": "nature"},
    "corail": {"shimaore": "soiyi", "kibouchi": "", "category": "nature"},
    "barrière de corail": {"shimaore": "caleni", "kibouchi": "", "category": "nature"},  # Correction: caléni -> caleni
    "tempête": {"shimaore": "darouba", "kibouchi": "", "category": "nature"},
    "rivière": {"shimaore": "mouro", "kibouchi": "", "category": "nature"},
    "pont": {"shimaore": "daradja", "kibouchi": "", "category": "nature"},
    "nuage": {"shimaore": "wingou", "kibouchi": "", "category": "nature"},
    "arc-en-ciel": {"shimaore": "mcacamba", "kibouchi": "", "category": "nature"},
    "caillou": {"shimaore": "malavouni", "kibouchi": "", "category": "nature"},
    "plateau": {"shimaore": "bwe", "kibouchi": "", "category": "nature"},  # Correction: bwé -> bwe
    "herbe": {"shimaore": "bandra", "kibouchi": "", "category": "nature"},
    "chemin": {"shimaore": "ndzia", "kibouchi": "", "category": "nature"},
    "fleur": {"shimaore": "malavou", "kibouchi": "", "category": "nature"},
    "soleil": {"shimaore": "jouwa", "kibouchi": "", "category": "nature"},
    "mer": {"shimaore": "bahari", "kibouchi": "", "category": "nature"},
    "plage": {"shimaore": "mtsangani", "kibouchi": "", "category": "nature"},
    "arbre": {"shimaore": "mwiri", "kibouchi": "", "category": "nature"},
    "rue": {"shimaore": "pare", "kibouchi": "", "category": "nature"},  # Correction: paré -> pare
    "bananier": {"shimaore": "trindri", "kibouchi": "", "category": "nature"},
    "feuille": {"shimaore": "mawoini", "kibouchi": "", "category": "nature"},
    "branche": {"shimaore": "trahi", "kibouchi": "", "category": "nature"},
    "tornade": {"shimaore": "ouzimouyi", "kibouchi": "", "category": "nature"},
    "cocotier": {"shimaore": "m'nadzi", "kibouchi": "", "category": "nature"},
    "arbre à pain": {"shimaore": "m'frampe", "kibouchi": "", "category": "nature"},  # Correction: m'frampé -> m'frampe
    "baobab": {"shimaore": "m'bouyou", "kibouchi": "", "category": "nature"},
    "bambou": {"shimaore": "m'bambo", "kibouchi": "", "category": "nature"},
    "manguier": {"shimaore": "m'manga", "kibouchi": "", "category": "nature"},
    "jacquier": {"shimaore": "m'fenesii", "kibouchi": "", "category": "nature"},  # Correction: m'fénéssi -> m'fenesii
    "terre": {"shimaore": "trotro", "kibouchi": "", "category": "nature"},
    "sol": {"shimaore": "tsi", "kibouchi": "", "category": "nature"},
    "érosion": {"shimaore": "padza", "kibouchi": "", "category": "nature"},
    "marée basse": {"shimaore": "maji yavo", "kibouchi": "", "category": "nature"},
    "platier": {"shimaore": "kale", "kibouchi": "", "category": "nature"},  # Correction: kalé -> kale
    "marée haute": {"shimaore": "maji yamale", "kibouchi": "", "category": "nature"},  # Correction: yamalé -> yamale
    "inondé": {"shimaore": "ourora", "kibouchi": "", "category": "nature"},
    "sauvage": {"shimaore": "nyeha", "kibouchi": "", "category": "nature"},  # Correction: nyéha -> nyeha
    "canne à sucre": {"shimaore": "mouwoi", "kibouchi": "", "category": "nature"},
    "fagot": {"shimaore": "kouni", "kibouchi": "", "category": "nature"},
    
    # Animaux avec corrections orthographiques
    "cochon": {"shimaore": "pouroukou", "kibouchi": "", "category": "animaux"},
    "margouillat": {"shimaore": "kasangwe", "kibouchi": "", "category": "animaux"},
    "abeille": {"shimaore": "niochi", "kibouchi": "", "category": "animaux"},
    "chat": {"shimaore": "paha", "kibouchi": "", "category": "animaux"},
    "rat": {"shimaore": "pouhou", "kibouchi": "", "category": "animaux"},
    # CORRECTION DOUBLON: Garder seulement un escargot avec la meilleure orthographe
    "escargot": {"shimaore": "kowa", "kibouchi": "", "category": "animaux"},  # Garde "kowa" au lieu de "kwa"
    "lion": {"shimaore": "simba", "kibouchi": "", "category": "animaux"},
    "grenouille": {"shimaore": "shiwatrotro", "kibouchi": "", "category": "animaux"},
    "oiseau": {"shimaore": "gnougni", "kibouchi": "", "category": "animaux"},
    "chien": {"shimaore": "mbwa", "kibouchi": "", "category": "animaux"},
    "poisson": {"shimaore": "fi", "kibouchi": "", "category": "animaux"},
    "maki": {"shimaore": "komba", "kibouchi": "", "category": "animaux"},
    "chèvre": {"shimaore": "mbouzi", "kibouchi": "", "category": "animaux"},
    "moustique": {"shimaore": "manundri", "kibouchi": "", "category": "animaux"},
    "mouche": {"shimaore": "ndzi", "kibouchi": "", "category": "animaux"},
    "chauve-souris": {"shimaore": "drema", "kibouchi": "", "category": "animaux"},
    "serpent": {"shimaore": "nyoha", "kibouchi": "", "category": "animaux"},
    "lapin": {"shimaore": "sungura", "kibouchi": "", "category": "animaux"},
    "canard": {"shimaore": "guisi", "kibouchi": "", "category": "animaux"},
    "mouton": {"shimaore": "baribari", "kibouchi": "", "category": "animaux"},
    "crocodile": {"shimaore": "vwai", "kibouchi": "", "category": "animaux"},
    "caméléon": {"shimaore": "tarundru", "kibouchi": "", "category": "animaux"},
    "zébu": {"shimaore": "nyombe", "kibouchi": "", "category": "animaux"},  # Correction: nyombé -> nyombe
    "âne": {"shimaore": "pundra", "kibouchi": "", "category": "animaux"},
    "poule": {"shimaore": "kouhou", "kibouchi": "", "category": "animaux"},
    "pigeon": {"shimaore": "ndiwa", "kibouchi": "", "category": "animaux"},
    "fourmis": {"shimaore": "tsoussou", "kibouchi": "", "category": "animaux"},
    "chenille": {"shimaore": "bazi", "kibouchi": "", "category": "animaux"},
    "papillon": {"shimaore": "pelapelaka", "kibouchi": "", "category": "animaux"},
    "ver de terre": {"shimaore": "lingoui lingoui", "kibouchi": "", "category": "animaux"},
    "criquet": {"shimaore": "furudji", "kibouchi": "", "category": "animaux"},
    "cheval": {"shimaore": "poundra", "kibouchi": "", "category": "animaux"},
    "perroquet": {"shimaore": "kassoukou", "kibouchi": "", "category": "animaux"},
    "cafard": {"shimaore": "kalalawi", "kibouchi": "", "category": "animaux"},
    "araignée": {"shimaore": "shitrandrabwibwi", "kibouchi": "", "category": "animaux"},
    "scorpion": {"shimaore": "hala", "kibouchi": "", "category": "animaux"},
    "scolopendre": {"shimaore": "trambwi", "kibouchi": "", "category": "animaux"},
    "thon": {"shimaore": "mbassi", "kibouchi": "", "category": "animaux"},
    "requin": {"shimaore": "pwedza", "kibouchi": "", "category": "animaux"},
    "poulpe": {"shimaore": "dradraka", "kibouchi": "", "category": "animaux"},
    "crabe": {"shimaore": "nyamba", "kibouchi": "", "category": "animaux"},  # Simplifie "nyamba/katsa" -> "nyamba"
    # CORRECTION DOUBLON: Supprimer "tortue: bigorno", garder "bigorneau: trondro"
    "bigorneau": {"shimaore": "trondro", "kibouchi": "", "category": "animaux"},
    "lambis": {"shimaore": "kombe", "kibouchi": "", "category": "animaux"},  # Correction: kombé -> kombe
    "cône de mer": {"shimaore": "kwitsi", "kibouchi": "", "category": "animaux"},
    "oursin": {"shimaore": "gadzassi", "kibouchi": "", "category": "animaux"},
    "huître": {"shimaore": "gadzassi", "kibouchi": "", "category": "animaux"},  # Note: même traduction que oursin
    "éléphant": {"shimaore": "ndovu", "kibouchi": "", "category": "animaux"},
    "singe": {"shimaore": "djakwe", "kibouchi": "", "category": "animaux"},
    "souris": {"shimaore": "shikwetse", "kibouchi": "", "category": "animaux"},
    "facochère": {"shimaore": "pouruku nyeha", "kibouchi": "", "category": "animaux"},
    "lézard": {"shimaore": "ngwizi", "kibouchi": "", "category": "animaux"},
    "renard": {"shimaore": "mbwa nyeha", "kibouchi": "", "category": "animaux"},
    "chameau": {"shimaore": "ngamia", "kibouchi": "", "category": "animaux"},
    "hérisson": {"shimaore": "landra", "kibouchi": "", "category": "animaux"},
    "corbeau": {"shimaore": "gawa", "kibouchi": "", "category": "animaux"},  # Simplifie "gawa/kwayi" -> "gawa"
    "civette": {"shimaore": "founga", "kibouchi": "", "category": "animaux"},
    "dauphin": {"shimaore": "moungoume", "kibouchi": "", "category": "animaux"},  # Correction: moungoumé -> moungoume
    "baleine": {"shimaore": "ndroujou", "kibouchi": "", "category": "animaux"},
    "crevette": {"shimaore": "camba", "kibouchi": "", "category": "animaux"},
    "frelon": {"shimaore": "chonga", "kibouchi": "", "category": "animaux"},
    "guêpe": {"shimaore": "movou", "kibouchi": "", "category": "animaux"},
    "bourdon": {"shimaore": "vungo vungo", "kibouchi": "", "category": "animaux"},
    "puce": {"shimaore": "kunguni", "kibouchi": "", "category": "animaux"},
    "poux": {"shimaore": "ndra", "kibouchi": "", "category": "animaux"},
    "bouc": {"shimaore": "bewe", "kibouchi": "", "category": "animaux"},  # Correction: béwé -> bewe
    "taureau": {"shimaore": "kondzo", "kibouchi": "", "category": "animaux"},
    "mille-pattes": {"shimaore": "mjongo", "kibouchi": "", "category": "animaux"},
    
    # Corps humain
    "œil": {"shimaore": "matso", "kibouchi": "", "category": "corps"},
    "nez": {"shimaore": "poua", "kibouchi": "", "category": "corps"},
    "oreille": {"shimaore": "kiyo", "kibouchi": "", "category": "corps"},
    "ongle": {"shimaore": "kofou", "kibouchi": "", "category": "corps"},
    "front": {"shimaore": "housso", "kibouchi": "", "category": "corps"},
    "joue": {"shimaore": "savou", "kibouchi": "", "category": "corps"},
    "dos": {"shimaore": "mengo", "kibouchi": "", "category": "corps"},
    "épaule": {"shimaore": "bega", "kibouchi": "", "category": "corps"},  # Correction: bèga -> bega
    "hanche": {"shimaore": "trenga", "kibouchi": "", "category": "corps"},
    "fesses": {"shimaore": "shidze", "kibouchi": "", "category": "corps"},  # Simplifie "shidzé/mvoumo" -> "shidze"
    "main": {"shimaore": "mhono", "kibouchi": "", "category": "corps"},
    "tête": {"shimaore": "shitsoi", "kibouchi": "", "category": "corps"},
    "ventre": {"shimaore": "mimba", "kibouchi": "", "category": "corps"},
    "dent": {"shimaore": "magno", "kibouchi": "", "category": "corps"},
    "langue": {"shimaore": "oulime", "kibouchi": "", "category": "corps"},  # Correction: oulimé -> oulime
    "pied": {"shimaore": "mindrou", "kibouchi": "", "category": "corps"},
    "lèvre": {"shimaore": "dhomo", "kibouchi": "", "category": "corps"},  # Correction: lèvre -> levre
    "peau": {"shimaore": "ngwezi", "kibouchi": "", "category": "corps"},
    "cheveux": {"shimaore": "ngnele", "kibouchi": "", "category": "corps"},  # Correction: ngnélé -> ngnele
    "doigts": {"shimaore": "cha", "kibouchi": "", "category": "corps"},
    "barbe": {"shimaore": "ndrevou", "kibouchi": "", "category": "corps"},  # Correction: ndrévou -> ndrevou
    "menton": {"shimaore": "shlevo", "kibouchi": "", "category": "corps"},
    "bouche": {"shimaore": "hangno", "kibouchi": "", "category": "corps"},
    "côtes": {"shimaore": "bavou", "kibouchi": "", "category": "corps"},  # Correction: côtes -> cotes
    "sourcil": {"shimaore": "tsi", "kibouchi": "", "category": "corps"},
    "cheville": {"shimaore": "dzitso la pwedza", "kibouchi": "", "category": "corps"},  # Correction: pwédza -> pwedza
    "cou": {"shimaore": "tsingou", "kibouchi": "", "category": "corps"},
    "cils": {"shimaore": "kove", "kibouchi": "", "category": "corps"},  # Correction: kové -> kove
    "arrière du crâne": {"shimaore": "komoi", "kibouchi": "", "category": "corps"},  # Correction: crâne -> crane
    
    # Salutations avec corrections
    "Bonjour": {"shimaore": "Kwezi", "kibouchi": "", "category": "salutations"},
    "Comment ça va ?": {"shimaore": "jeje", "kibouchi": "", "category": "salutations"},  # Correction: jéjé -> jeje
    "Oui": {"shimaore": "ewa", "kibouchi": "", "category": "salutations"},
    "Non": {"shimaore": "an'ha", "kibouchi": "", "category": "salutations"},
    "Ça va bien": {"shimaore": "fetre", "kibouchi": "", "category": "salutations"},  # Correction: fétré -> fetre
    "Merci": {"shimaore": "marahaba", "kibouchi": "", "category": "salutations"},
    "Bonne nuit": {"shimaore": "oukou wa hairi", "kibouchi": "", "category": "salutations"},
    "Au revoir": {"shimaore": "kwaheri", "kibouchi": "", "category": "salutations"},
    
    # Grammaire
    "Je": {"shimaore": "wami", "kibouchi": "", "category": "grammaire"},
    "Tu": {"shimaore": "wawe", "kibouchi": "", "category": "grammaire"},  # Correction: wawé -> wawe
    "Il/Elle": {"shimaore": "waye", "kibouchi": "", "category": "grammaire"},  # Correction: wayé -> waye
    "Nous": {"shimaore": "wassi", "kibouchi": "", "category": "grammaire"},
    "Ils/Elles": {"shimaore": "wawo", "kibouchi": "", "category": "grammaire"},
    
    # Transport
    "pirogue": {"shimaore": "laka", "kibouchi": "", "category": "transport"},
    "vedette": {"shimaore": "kwassa kwassa", "kibouchi": "", "category": "transport"},
    
    # Éducation
    "école": {"shimaore": "licoli", "kibouchi": "", "category": "education"},  # Correction: école -> ecole
    "école coranique": {"shimaore": "shioni", "kibouchi": "", "category": "education"},  # Correction: école -> ecole
    
    # Nouvelles entrées Kibouchi du PDF (section à la fin)
    "pente": {"shimaore": "mlima", "kibouchi": "boungou", "category": "nature"},  # Mise à jour
    "mangrove": {"shimaore": "mhonko", "kibouchi": "fandzava", "category": "nature"},  # Mise à jour
    # ... (continuer avec les autres mappings Kibouchi trouvés dans le PDF)
}

# Doublons à supprimer spécifiquement
DOUBLONS_A_SUPPRIMER = [
    "tortue",  # Supprimer "tortue: bigorno", garder "bigorneau: trondro"
    # Ne pas supprimer "escargot" car on garde la meilleure version
]

def analyze_current_database():
    """Analyse la base de données actuelle"""
    print("🔍 ANALYSE DE LA BASE DE DONNÉES ACTUELLE")
    print("=" * 50)
    
    total_words = words_collection.count_documents({})
    print(f"Total des mots dans la base: {total_words}")
    
    # Analyser les doublons
    pipeline = [
        {"$group": {"_id": "$french", "count": {"$sum": 1}, "docs": {"$push": "$_id"}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    
    duplicates = list(words_collection.aggregate(pipeline))
    print(f"Doublons trouvés: {len(duplicates)}")
    
    for dup in duplicates:
        print(f"  - '{dup['_id']}': {dup['count']} occurrences")
        
    return duplicates

def verify_pdf_corrections():
    """Vérifie quels mots du PDF existent déjà dans la base"""
    print("\n🔍 VÉRIFICATION DES MOTS DU PDF DANS LA BASE")
    print("=" * 50)
    
    found_in_db = 0
    not_found_in_db = 0
    needs_update = 0
    
    for french_word, pdf_data in PDF_VOCABULARY.items():
        db_word = words_collection.find_one({"french": french_word})
        
        if db_word:
            found_in_db += 1
            # Vérifier si les traductions diffèrent
            shimaore_differs = db_word.get('shimaore', '') != pdf_data['shimaore']
            kibouchi_differs = db_word.get('kibouchi', '') != pdf_data['kibouchi']
            
            if shimaore_differs or kibouchi_differs:
                needs_update += 1
                print(f"  📝 MISE À JOUR NÉCESSAIRE: {french_word}")
                if shimaore_differs:
                    print(f"    Shimaoré: '{db_word.get('shimaore', '')}' -> '{pdf_data['shimaore']}'")
                if kibouchi_differs:
                    print(f"    Kibouchi: '{db_word.get('kibouchi', '')}' -> '{pdf_data['kibouchi']}'")
        else:
            not_found_in_db += 1
            print(f"  ➕ NOUVEAU MOT: {french_word}")
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"  - Mots existants: {found_in_db}")
    print(f"  - Mots nouveaux: {not_found_in_db}")
    print(f"  - Mots à mettre à jour: {needs_update}")
    
    return {'found': found_in_db, 'not_found': not_found_in_db, 'needs_update': needs_update}

def remove_specific_duplicates():
    """Supprime les doublons spécifiques mentionnés par l'utilisateur"""
    print("\n🗑️ SUPPRESSION DES DOUBLONS SPÉCIFIQUES")
    print("=" * 50)
    
    # Cas spécial: tortue/bigorno vs bigorneau/trondro
    tortue_entries = list(words_collection.find({"french": "tortue"}))
    bigorneau_entries = list(words_collection.find({"french": "bigorneau"}))
    
    if tortue_entries:
        for entry in tortue_entries:
            if entry.get('shimaore', '').lower() == 'bigorno':
                print(f"  🗑️ Suppression: tortue -> {entry.get('shimaore', '')}")
                words_collection.delete_one({"_id": entry["_id"]})
                
    # Doublons d'escargot - garder la meilleure version (kowa)
    escargot_entries = list(words_collection.find({"french": "escargot"}))
    if len(escargot_entries) > 1:
        # Garder celle avec 'kowa', supprimer celle avec 'kwa'
        for entry in escargot_entries:
            if entry.get('shimaore', '').lower() == 'kwa':
                print(f"  🗑️ Suppression doublon escargot: {entry.get('shimaore', '')}")
                words_collection.delete_one({"_id": entry["_id"]})

def apply_pdf_corrections():
    """Applique les corrections du PDF à la base de données"""
    print("\n✅ APPLICATION DES CORRECTIONS DU PDF")
    print("=" * 50)
    
    updated_count = 0
    added_count = 0
    
    for french_word, pdf_data in PDF_VOCABULARY.items():
        existing_word = words_collection.find_one({"french": french_word})
        
        if existing_word:
            # Mettre à jour le mot existant
            update_data = {
                "shimaore": pdf_data['shimaore'],
                "category": pdf_data.get('category', existing_word.get('category', ''))
            }
            
            # Ajouter kibouchi seulement s'il n'est pas vide
            if pdf_data['kibouchi']:
                update_data["kibouchi"] = pdf_data['kibouchi']
            
            words_collection.update_one(
                {"_id": existing_word["_id"]},
                {"$set": update_data}
            )
            print(f"  ✅ Mis à jour: {french_word}")
            updated_count += 1
            
        else:
            # Ajouter nouveau mot
            new_word = {
                "french": french_word,
                "shimaore": pdf_data['shimaore'],
                "kibouchi": pdf_data['kibouchi'],
                "category": pdf_data['category'],
                "emoji": "",  # À ajouter plus tard si nécessaire
                "has_image": False
            }
            
            words_collection.insert_one(new_word)
            print(f"  ➕ Ajouté: {french_word}")
            added_count += 1
    
    print(f"\n📊 CORRECTIONS APPLIQUÉES:")
    print(f"  - Mots mis à jour: {updated_count}")
    print(f"  - Mots ajoutés: {added_count}")

def fix_orthographic_inconsistencies():
    """Corrige les incohérences orthographiques générales dans la base"""
    print("\n📝 CORRECTION DES INCOHÉRENCES ORTHOGRAPHIQUES")
    print("=" * 50)
    
    corrections_count = 0
    
    # Corrections d'accents et caractères spéciaux
    accent_corrections = [
        {"from": "é", "to": "e"},
        {"from": "è", "to": "e"},
        {"from": "à", "to": "a"},
        {"from": "ù", "to": "u"},
        {"from": "ô", "to": "o"},
        {"from": "ç", "to": "c"},
    ]
    
    for correction in accent_corrections:
        # Correction dans shimaore
        filter_query = {"shimaore": {"$regex": correction["from"]}}
        words_with_accents = list(words_collection.find(filter_query))
        
        for word in words_with_accents:
            new_shimaore = word['shimaore'].replace(correction["from"], correction["to"])
            words_collection.update_one(
                {"_id": word["_id"]},
                {"$set": {"shimaore": new_shimaore}}
            )
            print(f"  📝 Correction accent: {word['french']} - shimaore: '{word['shimaore']}' -> '{new_shimaore}'")
            corrections_count += 1
        
        # Correction dans kibouchi
        filter_query = {"kibouchi": {"$regex": correction["from"]}}
        words_with_accents = list(words_collection.find(filter_query))
        
        for word in words_with_accents:
            new_kibouchi = word['kibouchi'].replace(correction["from"], correction["to"])
            words_collection.update_one(
                {"_id": word["_id"]},
                {"$set": {"kibouchi": new_kibouchi}}
            )
            print(f"  📝 Correction accent: {word['french']} - kibouchi: '{word['kibouchi']}' -> '{new_kibouchi}'")
            corrections_count += 1
    
    print(f"\n📊 CORRECTIONS ORTHOGRAPHIQUES APPLIQUÉES: {corrections_count}")

def generate_final_report():
    """Génère un rapport final des corrections"""
    print("\n📊 RAPPORT FINAL DES CORRECTIONS")
    print("=" * 50)
    
    # Statistiques finales
    total_words = words_collection.count_documents({})
    categories = words_collection.distinct("category")
    
    print(f"Total des mots après corrections: {total_words}")
    print(f"Catégories: {len(categories)}")
    
    for category in sorted(categories):
        count = words_collection.count_documents({"category": category})
        print(f"  - {category}: {count} mots")
    
    # Vérifier s'il reste des doublons
    pipeline = [
        {"$group": {"_id": "$french", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    
    remaining_duplicates = list(words_collection.aggregate(pipeline))
    print(f"\nDoublons restants: {len(remaining_duplicates)}")
    
    if remaining_duplicates:
        for dup in remaining_duplicates:
            print(f"  ⚠️ Doublon restant: '{dup['_id']}' ({dup['count']} occurrences)")
    
    # Vérifier les traductions manquantes
    missing_shimaore = words_collection.count_documents({"$or": [{"shimaore": ""}, {"shimaore": {"$exists": False}}]})
    missing_kibouchi = words_collection.count_documents({"$or": [{"kibouchi": ""}, {"kibouchi": {"$exists": False}}]})
    
    print(f"\nTraductions manquantes:")
    print(f"  - Shimaoré manquant: {missing_shimaore} mots")
    print(f"  - Kibouchi manquant: {missing_kibouchi} mots")

def main():
    """Fonction principale"""
    print("🔧 ANALYSE ET CORRECTION DU VOCABULAIRE PDF")
    print("=" * 60)
    print(f"Heure de début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. Analyser l'état actuel
        duplicates = analyze_current_database()
        
        # 2. Vérifier les corrections nécessaires
        verification = verify_pdf_corrections()
        
        # 3. Supprimer les doublons spécifiques
        remove_specific_duplicates()
        
        # 4. Appliquer les corrections du PDF
        apply_pdf_corrections()
        
        # 5. Corriger les incohérences orthographiques
        fix_orthographic_inconsistencies()
        
        # 6. Générer le rapport final
        generate_final_report()
        
        print(f"\n✅ CORRECTIONS TERMINÉES AVEC SUCCÈS!")
        print(f"Heure de fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ ERREUR: {str(e)}")
        raise

if __name__ == "__main__":
    main()