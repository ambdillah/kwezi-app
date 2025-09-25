#!/usr/bin/env python3
"""
Script d'analyse et de mise à jour de la base de données à partir du PDF vocabulaire
Compare le contenu du PDF avec la base de données existante
Identifie les corrections orthographiques, doublons et mises à jour nécessaires
"""

import os
import sys
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import re

load_dotenv()

# Données extraites du PDF
PDF_VOCABULARY = {
    # Nature
    "pente": {"french": "pente", "shimaore": "mlima", "kibouchi": "boungou", "category": "nature"},
    "lune": {"french": "lune", "shimaore": "mwezi", "kibouchi": "fandzava", "category": "nature"},
    "etoile": {"french": "etoile", "shimaore": "gnora", "kibouchi": "lakintagna", "category": "nature"},
    "sable": {"french": "sable", "shimaore": "mtsanga", "kibouchi": "fasigni", "category": "nature"},
    "vague": {"french": "vague", "shimaore": "dhouja", "kibouchi": "houndza", "category": "nature"},
    "vent": {"french": "vent", "shimaore": "pevo", "kibouchi": "tsikou", "category": "nature"},
    "pluie": {"french": "pluie", "shimaore": "vhoua", "kibouchi": "mahaleni", "category": "nature"},
    "mangrove": {"french": "mangrove", "shimaore": "mhonko", "kibouchi": "honkou", "category": "nature"},
    "corail": {"french": "corail", "shimaore": "soiyi", "kibouchi": "soiyi", "category": "nature"},
    "barriere de corail": {"french": "barriere de corail", "shimaore": "caleni", "kibouchi": "caleni", "category": "nature"},
    "tempete": {"french": "tempete", "shimaore": "darouba", "kibouchi": "tsikou", "category": "nature"},
    "riviere": {"french": "riviere", "shimaore": "mouro", "kibouchi": "mouroni", "category": "nature"},
    "pont": {"french": "pont", "shimaore": "daradja", "kibouchi": "daradja", "category": "nature"},
    "nuage": {"french": "nuage", "shimaore": "wingou", "kibouchi": "vingou", "category": "nature"},
    "arc en ciel": {"french": "arc en ciel", "shimaore": "mcacamba", "kibouchi": "", "category": "nature"},
    "foret": {"french": "foret", "shimaore": "malavouni", "kibouchi": "atihala", "category": "nature"},
    "pierre": {"french": "pierre", "shimaore": "bwe", "kibouchi": "vatou", "category": "nature"},
    "plateau": {"french": "plateau", "shimaore": "bandra", "kibouchi": "ketraka", "category": "nature"},
    "chemin": {"french": "chemin", "shimaore": "ndzia", "kibouchi": "lalagna", "category": "nature"},
    "herbe": {"french": "herbe", "shimaore": "malavou", "kibouchi": "haitri", "category": "nature"},
    "fleur": {"french": "fleur", "shimaore": "foulera", "kibouchi": "foulera", "category": "nature"},
    "soleil": {"french": "soleil", "shimaore": "jouwa", "kibouchi": "zouva", "category": "nature"},
    "mer": {"french": "mer", "shimaore": "bahari", "kibouchi": "bahari", "category": "nature"},
    "plage": {"french": "plage", "shimaore": "mtsangani", "kibouchi": "fassigni", "category": "nature"},
    "arbre": {"french": "arbre", "shimaore": "mwiri", "kibouchi": "kakazou", "category": "nature"},
    "route": {"french": "route", "shimaore": "pare", "kibouchi": "pare", "category": "nature"},
    "bananier": {"french": "bananier", "shimaore": "trindri", "kibouchi": "voudi ni hountsi", "category": "nature"},
    "feuille": {"french": "feuille", "shimaore": "mawoini", "kibouchi": "hayitri", "category": "nature"},
    "branche": {"french": "branche", "shimaore": "trahi", "kibouchi": "trahi", "category": "nature"},
    "tornade": {"french": "tornade", "shimaore": "ouzimouyi", "kibouchi": "tsikou soulaimana", "category": "nature"},
    "cocotier": {"french": "cocotier", "shimaore": "m'nadzi", "kibouchi": "voudi ni vwaniou", "category": "nature"},
    "arbre a pain": {"french": "arbre a pain", "shimaore": "m'frampe", "kibouchi": "voudi ni frampe", "category": "nature"},
    "baobab": {"french": "baobab", "shimaore": "m'bouyou", "kibouchi": "voudi ni bouyou", "category": "nature"},
    "bambou": {"french": "bambou", "shimaore": "m'bambo", "kibouchi": "voudi ni manga", "category": "nature"},
    "manguier": {"french": "manguier", "shimaore": "m'manga", "kibouchi": "voudi ni finessi", "category": "nature"},
    "jacquier": {"french": "jacquier", "shimaore": "m'fenessi", "kibouchi": "fotaka", "category": "nature"},
    "terre": {"french": "terre", "shimaore": "trotro", "kibouchi": "tani", "category": "nature"},
    "sol": {"french": "sol", "shimaore": "tsi", "kibouchi": "padza", "category": "nature"},
    "erosion": {"french": "erosion", "shimaore": "padza", "kibouchi": "ranou meki", "category": "nature"},
    "maree basse": {"french": "maree basse", "shimaore": "maji yavo", "kibouchi": "kaleni", "category": "nature"},
    "platier": {"french": "platier", "shimaore": "kale", "kibouchi": "ranou fenou", "category": "nature"},
    "maree haute": {"french": "maree haute", "shimaore": "maji yamale", "kibouchi": "dobou", "category": "nature"},
    "inonde": {"french": "inonde", "shimaore": "ourora", "kibouchi": "nyeha", "category": "nature"},
    "sauvage": {"french": "sauvage", "shimaore": "di", "kibouchi": "di", "category": "nature"},
    "canne a sucre": {"french": "canne a sucre", "shimaore": "mouwoi", "kibouchi": "fari", "category": "nature"},
    "fagot": {"french": "fagot", "shimaore": "kouni", "kibouchi": "azoumati", "category": "nature"},
    "pirogue": {"french": "pirogue", "shimaore": "laka", "kibouchi": "lakana", "category": "transport"},
    "vedette": {"french": "vedette", "shimaore": "kwassa kwassa", "kibouchi": "videti", "category": "transport"},
    "ecole": {"french": "ecole", "shimaore": "licoli", "kibouchi": "licoli", "category": "education"},
    "ecole coranique": {"french": "ecole coranique", "shimaore": "shioni", "kibouchi": "kioni", "category": "education"},
    
    # Nombres
    "un": {"french": "un", "shimaore": "moja", "kibouchi": "areki", "category": "nombres"},
    "deux": {"french": "deux", "shimaore": "mbili", "kibouchi": "aroyi", "category": "nombres"},
    "trois": {"french": "trois", "shimaore": "trarou", "kibouchi": "telou", "category": "nombres"},
    "quatre": {"french": "quatre", "shimaore": "nhe", "kibouchi": "efatra", "category": "nombres"},
    "cinq": {"french": "cinq", "shimaore": "tsano", "kibouchi": "dimi", "category": "nombres"},
    "six": {"french": "six", "shimaore": "sita", "kibouchi": "tchouta", "category": "nombres"},
    "sept": {"french": "sept", "shimaore": "saba", "kibouchi": "fitou", "category": "nombres"},
    "huit": {"french": "huit", "shimaore": "nane", "kibouchi": "valou", "category": "nombres"},
    "neuf": {"french": "neuf", "shimaore": "chendra", "kibouchi": "foulu", "category": "nombres"},
    "dix": {"french": "dix", "shimaore": "koumi", "kibouchi": "foulu", "category": "nombres"},
    "onze": {"french": "onze", "shimaore": "koumi na moja", "kibouchi": "foulu areki ambi", "category": "nombres"},
    "douze": {"french": "douze", "shimaore": "koumi na mbili", "kibouchi": "foulu aroyi ambi", "category": "nombres"},
    "treize": {"french": "treize", "shimaore": "koumi na trarou", "kibouchi": "foulu telou ambi", "category": "nombres"},
    "quatorze": {"french": "quatorze", "shimaore": "koumi na nhe", "kibouchi": "foulu efatra ambi", "category": "nombres"},
    "quinze": {"french": "quinze", "shimaore": "koumi na tsano", "kibouchi": "foulu dimi ambi", "category": "nombres"},
    "seize": {"french": "seize", "shimaore": "koumi na sita", "kibouchi": "foulu tchouta ambi", "category": "nombres"},
    "dix-sept": {"french": "dix-sept", "shimaore": "koumi na saba", "kibouchi": "foulu fitou ambi", "category": "nombres"},
    "dix-huit": {"french": "dix-huit", "shimaore": "koumi na nane", "kibouchi": "foulu valou ambi", "category": "nombres"},
    "dix-neuf": {"french": "dix-neuf", "shimaore": "koumi na chendra", "kibouchi": "foulu civi ambi", "category": "nombres"},
    "vingt": {"french": "vingt", "shimaore": "chirini", "kibouchi": "arompoulou", "category": "nombres"},
    "cent": {"french": "cent", "shimaore": "miya", "kibouchi": "zatou", "category": "nombres"},
    
    # Animaux (sélection pour éviter de surcharger le script)
    "cochon": {"french": "cochon", "shimaore": "pouroukou", "kibouchi": "lambou", "category": "animaux"},
    "chat": {"french": "chat", "shimaore": "paha", "kibouchi": "moirou", "category": "animaux"},
    "chien": {"french": "chien", "shimaore": "mbwa", "kibouchi": "fadroka", "category": "animaux"},
    "escargot": {"french": "escargot", "shimaore": "kowa", "kibouchi": "ancora", "category": "animaux"},  # Correction potentielle
    "poisson": {"french": "poisson", "shimaore": "fi", "kibouchi": "lokou", "category": "animaux"},
    "tortue": {"french": "tortue", "shimaore": "nyamba", "kibouchi": "fanou", "category": "animaux"},
    "bigorneau": {"french": "bigorneau", "shimaore": "bigorno", "kibouchi": "trondrou", "category": "animaux"},
    "oursin": {"french": "oursin", "shimaore": "gadzassi ya bahari", "kibouchi": "sadza", "category": "animaux"},  # Correction différenciation
    "huitre": {"french": "huitre", "shimaore": "gadzassi", "kibouchi": "faninti", "category": "animaux"},  # Correction différenciation
    
    # Corps Humain (sélection)
    "oeil": {"french": "oeil", "shimaore": "matso", "kibouchi": "faninti", "category": "corps"},
    "nez": {"french": "nez", "shimaore": "poua", "kibouchi": "horougnou", "category": "corps"},
    "main": {"french": "main", "shimaore": "mhono", "kibouchi": "tagnana", "category": "corps"},
    "tete": {"french": "tete", "shimaore": "shitsoi", "kibouchi": "louha", "category": "corps"},
    "pied": {"french": "pied", "shimaore": "mindrou", "kibouchi": "viti", "category": "corps"},
    
    # Salutations
    "bonjour": {"french": "bonjour", "shimaore": "kwezi", "kibouchi": "kwezi", "category": "salutations"},
    "comment ca va": {"french": "comment ca va", "shimaore": "jeje", "kibouchi": "akori", "category": "salutations"},
    "oui": {"french": "oui", "shimaore": "ewa", "kibouchi": "iya", "category": "salutations"},
    "non": {"french": "non", "shimaore": "an'ha", "kibouchi": "an'ha", "category": "salutations"},
    "ca va bien": {"french": "ca va bien", "shimaore": "fetre", "kibouchi": "tsara", "category": "salutations"},
    "merci": {"french": "merci", "shimaore": "marahaba", "kibouchi": "marahaba", "category": "salutations"},
    "au revoir": {"french": "au revoir", "shimaore": "kwaheri", "kibouchi": "maeva", "category": "salutations"},
    
    # Grammaire
    "je": {"french": "je", "shimaore": "wami", "kibouchi": "zahou", "category": "grammaire"},
    "tu": {"french": "tu", "shimaore": "wawe", "kibouchi": "anaou", "category": "grammaire"},
    "il": {"french": "il", "shimaore": "waye", "kibouchi": "izi", "category": "grammaire"},
    "nous": {"french": "nous", "shimaore": "wasi", "kibouchi": "atsika", "category": "grammaire"},  # Correction "wasi" au lieu de "wassi"
    "vous": {"french": "vous", "shimaore": "wagnou", "kibouchi": "anareou", "category": "grammaire"},
    "ils": {"french": "ils", "shimaore": "wawo", "kibouchi": "reou", "category": "grammaire"},
    
    # Famille (sélection avec corrections)
    "famille": {"french": "famille", "shimaore": "mdjamaza", "kibouchi": "havagna", "category": "famille"},
    "papa": {"french": "papa", "shimaore": "baba", "kibouchi": "baba", "category": "famille"},
    "maman": {"french": "maman", "shimaore": "mama", "kibouchi": "mama", "category": "famille"},
    "frere": {"french": "frere", "shimaore": "mwanagna", "kibouchi": "anadahi", "category": "famille"},
    "soeur": {"french": "soeur", "shimaore": "mwanagna", "kibouchi": "anabavi", "category": "famille"},
    "grand-pere": {"french": "grand-pere", "shimaore": "bacoco", "kibouchi": "dadayi", "category": "famille"},
    "grand-mere": {"french": "grand-mere", "shimaore": "coco", "kibouchi": "dadi", "category": "famille"},
    "tante maternelle": {"french": "tante maternelle", "shimaore": "mama titi", "kibouchi": "zama", "category": "famille"},
    "oncle paternel": {"french": "oncle paternel", "shimaore": "baba heli", "kibouchi": "nindri heli", "category": "famille"},
    "tante paternelle": {"french": "tante paternelle", "shimaore": "zena", "kibouchi": "zena", "category": "famille"},
    "petit garcon": {"french": "petit garcon", "shimaore": "mwana mtroubaba", "kibouchi": "zaza lalahi", "category": "famille"},
    "jeune adulte": {"french": "jeune adulte", "shimaore": "shababi", "kibouchi": "shababi", "category": "famille"},
    "frere soeur": {"french": "frere soeur", "shimaore": "moinagna", "kibouchi": "", "category": "famille"},
    
    # Couleurs
    "bleu": {"french": "bleu", "shimaore": "bile", "kibouchi": "mayitsou bile", "category": "couleurs"},
    "vert": {"french": "vert", "shimaore": "dhavou", "kibouchi": "mayitsou", "category": "couleurs"},
    "noir": {"french": "noir", "shimaore": "nzidhou", "kibouchi": "mayintigni", "category": "couleurs"},
    "blanc": {"french": "blanc", "shimaore": "ndjeou", "kibouchi": "malandi", "category": "couleurs"},
    "jaune": {"french": "jaune", "shimaore": "dzindzano", "kibouchi": "tamoutamou", "category": "couleurs"},
    "rouge": {"french": "rouge", "shimaore": "dzifou", "kibouchi": "fotafotaka", "category": "couleurs"},
    "gris": {"french": "gris", "shimaore": "ranou", "kibouchi": "tsoholi", "category": "couleurs"},
    "marron": {"french": "marron", "shimaore": "trotro", "kibouchi": "vari", "category": "couleurs"},
}

def normalize_french_word(word):
    """Normalise les mots français en supprimant les accents"""
    # Mappings pour les accents français courants
    accent_map = {
        'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
        'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
        'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
        'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
        'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
        'ý': 'y', 'ÿ': 'y',
        'ç': 'c', 'ñ': 'n'
    }
    
    normalized = word.lower()
    for accented, unaccented in accent_map.items():
        normalized = normalized.replace(accented, unaccented)
    return normalized

def normalize_shimaore_word(word):
    """Normalise les mots shimaoré en supprimant les accents"""
    # Shimaoré utilise certains accents qu'il faut normaliser
    accent_map = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a',
        'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
        'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
        'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o'
    }
    
    normalized = word.lower()
    for accented, unaccented in accent_map.items():
        normalized = normalized.replace(accented, unaccented)
    return normalized

def connect_to_database():
    """Se connecte à la base de données MongoDB"""
    MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/mayotte_app')
    DB_NAME = os.getenv('DB_NAME', 'mayotte_app')
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
    return db.words

def analyze_database_vs_pdf():
    """Analyse les différences entre la base de données et le PDF"""
    collection = connect_to_database()
    
    # Obtenir tous les mots de la base
    db_words = list(collection.find({}))
    
    print(f"=== ANALYSE DE LA BASE DE DONNÉES VS PDF ===")
    print(f"Mots dans la base de données: {len(db_words)}")
    print(f"Mots dans le PDF: {len(PDF_VOCABULARY)}")
    
    # Analyser les corrections orthographiques nécessaires
    orthographic_corrections = []
    word_updates = []
    duplicates = []
    missing_words = []
    
    # Créer un index des mots de la base par français normalisé
    db_index = {}
    for word in db_words:
        french = word.get('french', '')
        normalized = normalize_french_word(french)
        if normalized not in db_index:
            db_index[normalized] = []
        db_index[normalized].append(word)
    
    # Vérifier les doublons dans la base
    print(f"\n=== DOUBLONS DÉTECTÉS ===")
    for french_norm, words in db_index.items():
        if len(words) > 1:
            print(f"DOUBLON: '{words[0]['french']}' - {len(words)} entrées")
            duplicates.extend(words[1:])  # Garder le premier, marquer les autres comme doublons
    
    print(f"Total doublons à supprimer: {len(duplicates)}")
    
    # Comparer avec le PDF
    print(f"\n=== COMPARAISON AVEC LE PDF ===")
    
    for pdf_key, pdf_word in PDF_VOCABULARY.items():
        french_norm = normalize_french_word(pdf_word['french'])
        
        if french_norm in db_index:
            # Le mot existe, vérifier les traductions
            db_word = db_index[french_norm][0]  # Prendre le premier si doublons
            
            # Vérifier les corrections orthographiques nécessaires
            changes = []
            
            # Français
            if db_word['french'] != pdf_word['french']:
                changes.append(f"français: '{db_word['french']}' -> '{pdf_word['french']}'")
            
            # Shimaoré 
            db_shimaore = normalize_shimaore_word(db_word.get('shimaore', ''))
            pdf_shimaore = normalize_shimaore_word(pdf_word['shimaore'])
            if db_shimaore != pdf_shimaore:
                changes.append(f"shimaoré: '{db_word.get('shimaore', '')}' -> '{pdf_word['shimaore']}'")
            
            # Kibouchi
            if db_word.get('kibouchi', '') != pdf_word['kibouchi']:
                changes.append(f"kibouchi: '{db_word.get('kibouchi', '')}' -> '{pdf_word['kibouchi']}'")
            
            if changes:
                correction = {
                    'word_id': db_word['_id'],
                    'french_current': db_word['french'],
                    'french_new': pdf_word['french'],
                    'changes': changes,
                    'pdf_data': pdf_word
                }
                orthographic_corrections.append(correction)
        else:
            # Mot manquant dans la base
            missing_words.append(pdf_word)
    
    # Afficher les résultats
    print(f"\nCORRECTIONS ORTHOGRAPHIQUES NÉCESSAIRES: {len(orthographic_corrections)}")
    for correction in orthographic_corrections[:10]:  # Afficher les 10 premières
        print(f"  - {correction['french_current']}: {', '.join(correction['changes'])}")
    
    print(f"\nMOTS MANQUANTS À AJOUTER: {len(missing_words)}")
    for word in missing_words[:10]:  # Afficher les 10 premiers
        print(f"  - {word['french']} ({word['category']})")
    
    return {
        'orthographic_corrections': orthographic_corrections,
        'duplicates': duplicates,
        'missing_words': missing_words,
        'total_db_words': len(db_words)
    }

def apply_corrections(analysis_results, dry_run=True):
    """Applique les corrections identifiées"""
    collection = connect_to_database()
    
    corrections = analysis_results['orthographic_corrections']
    duplicates = analysis_results['duplicates']
    missing_words = analysis_results['missing_words']
    
    print(f"\n=== {'SIMULATION' if dry_run else 'APPLICATION'} DES CORRECTIONS ===")
    
    # 1. Supprimer les doublons
    if duplicates:
        print(f"\n1. Suppression des doublons ({len(duplicates)} mots):")
        for duplicate in duplicates:
            print(f"   - Supprimer: {duplicate['french']} (ID: {duplicate['_id']})")
            if not dry_run:
                collection.delete_one({'_id': duplicate['_id']})
    
    # 2. Appliquer les corrections orthographiques
    if corrections:
        print(f"\n2. Corrections orthographiques ({len(corrections)} mots):")
        for correction in corrections:
            print(f"   - {correction['french_current']}: {', '.join(correction['changes'])}")
            if not dry_run:
                update_data = {}
                pdf_data = correction['pdf_data']
                update_data['french'] = pdf_data['french']
                update_data['shimaore'] = pdf_data['shimaore'] 
                update_data['kibouchi'] = pdf_data['kibouchi']
                update_data['category'] = pdf_data['category']
                update_data['updated_at'] = datetime.utcnow()
                
                collection.update_one(
                    {'_id': correction['word_id']},
                    {'$set': update_data}
                )
    
    # 3. Ajouter les mots manquants
    if missing_words:
        print(f"\n3. Ajout des mots manquants ({len(missing_words)} mots):")
        for word in missing_words:
            print(f"   - Ajouter: {word['french']} ({word['category']})")
            if not dry_run:
                new_word = {
                    'french': word['french'],
                    'shimaore': word['shimaore'],
                    'kibouchi': word['kibouchi'],
                    'category': word['category'],
                    'difficulty': 1,
                    'created_at': datetime.utcnow(),
                    'updated_from_pdf': True
                }
                collection.insert_one(new_word)
    
    # Statistiques finales
    total_changes = len(duplicates) + len(corrections) + len(missing_words)
    print(f"\nTOTAL DES MODIFICATIONS: {total_changes}")
    print(f"  - Doublons supprimés: {len(duplicates)}")
    print(f"  - Corrections appliquées: {len(corrections)}")
    print(f"  - Mots ajoutés: {len(missing_words)}")
    
    if dry_run:
        print(f"\n⚠️  SIMULATION TERMINÉE - Aucune modification appliquée")
        print(f"   Pour appliquer les changements, relancer avec dry_run=False")
    else:
        print(f"\n✅ MODIFICATIONS APPLIQUÉES AVEC SUCCÈS")

def main():
    """Fonction principale"""
    print("=== ANALYSE ET CORRECTION DU VOCABULAIRE SHIMAORÉ-KIBOUCHI ===")
    print("Comparaison entre la base de données et le PDF fourni\n")
    
    # Analyser les différences
    results = analyze_database_vs_pdf()
    
    # Demander confirmation pour appliquer
    print(f"\nVoulez-vous appliquer ces corrections ? (simulation d'abord)")
    
    # Faire une simulation d'abord
    apply_corrections(results, dry_run=True)
    
    # Demander confirmation pour les vraies modifications
    response = input("\nAppliquer réellement ces modifications ? (oui/non): ")
    if response.lower() in ['oui', 'o', 'yes', 'y']:
        apply_corrections(results, dry_run=False)
        
        # Vérification finale
        collection = connect_to_database()
        final_count = collection.count_documents({})
        print(f"\nVÉRIFICATION FINALE:")
        print(f"Nombre total de mots après correction: {final_count}")
    else:
        print("Modifications annulées.")

if __name__ == "__main__":
    main()