#!/usr/bin/env python3
"""
Script de correction du formatage des mots français
- Remet les accents appropriés sur les mots français
- Ajoute les majuscules sur les premières lettres
- Corrige les erreurs de la correction précédente
"""

import os
import sys
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def connect_to_database():
    """Se connecte à la base de données MongoDB"""
    MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/mayotte_app')
    DB_NAME = os.getenv('DB_NAME', 'mayotte_app')
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
    return db.words

def backup_database():
    """Crée une sauvegarde avant corrections"""
    collection = connect_to_database()
    words = list(collection.find({}))
    
    backup_filename = f"/app/backend/backup_formatting_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Convertir ObjectId et datetime en string pour JSON
    for word in words:
        if '_id' in word:
            word['_id'] = str(word['_id'])
        for key, value in word.items():
            if isinstance(value, datetime):
                word[key] = value.isoformat()
    
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    
    print(f"Sauvegarde créée: {backup_filename}")
    return backup_filename

def fix_french_formatting():
    """Corrige le formatage des mots français"""
    collection = connect_to_database()
    
    # Corrections spécifiques pour remettre les accents et majuscules
    french_corrections = {
        # Remettre les accents appropriés et majuscules
        "frere": "Frère",
        "etoile": "Étoile", 
        "ecole": "École",
        "tete": "Tête",
        "tempete": "Tempête",
        "riviere": "Rivière",
        "erosion": "Érosion",
        "inonde": "Inondé",
        "huitre": "Huître",
        
        # Ajouter majuscules aux autres mots
        "grand-pere": "Grand-père",
        "grand-mere": "Grand-mère", 
        "comment ca va": "Comment ça va",
        "ca va bien": "Ça va bien",
        "au revoir": "Au revoir",
        "barriere de corail": "Barrière de corail",
        "maree basse": "Marée basse",
        "maree haute": "Marée haute",
        "canne a sucre": "Canne à sucre",
        "arbre a pain": "Arbre à pain",
        "ecole coranique": "École coranique",
        
        # Famille - majuscules
        "famille": "Famille",
        "papa": "Papa",
        "maman": "Maman",
        "tante maternelle": "Tante maternelle",
        "tante paternelle": "Tante paternelle",
        "oncle paternel": "Oncle paternel",
        "petit garcon": "Petit garçon",
        "jeune adulte": "Jeune adulte",
        
        # Corps - majuscules
        "oeil": "Œil",
        "nez": "Nez",
        "main": "Main",
        "pied": "Pied",
        
        # Salutations - majuscules
        "bonjour": "Bonjour",
        "oui": "Oui", 
        "non": "Non",
        "merci": "Merci",
        
        # Grammaire - majuscules
        "je": "Je",
        "tu": "Tu",
        "il": "Il",
        "nous": "Nous",
        "vous": "Vous",
        "ils": "Ils",
        
        # Couleurs - majuscules
        "bleu": "Bleu",
        "vert": "Vert", 
        "noir": "Noir",
        "blanc": "Blanc",
        "jaune": "Jaune",
        "rouge": "Rouge",
        "gris": "Gris",
        "marron": "Marron",
        
        # Nature - majuscules et accents
        "pente": "Pente",
        "mer": "Mer",
        "soleil": "Soleil",
        "arbre": "Arbre",
        "terre": "Terre",
        "pierre": "Pierre",
        "chemin": "Chemin",
        "route": "Route"
    }
    
    corrections_applied = 0
    
    print("=== CORRECTION DU FORMATAGE FRANÇAIS ===")
    
    for current_french, correct_french in french_corrections.items():
        result = collection.update_one(
            {"french": current_french},
            {"$set": {
                "french": correct_french,
                "updated_at": datetime.utcnow(),
                "french_formatting_corrected": True
            }}
        )
        
        if result.modified_count > 0:
            print(f"✓ Corrigé: '{current_french}' → '{correct_french}'")
            corrections_applied += 1
        elif result.matched_count > 0:
            print(f"- Déjà correct: '{current_french}'")
    
    return corrections_applied

def apply_general_capitalization():
    """Applique la capitalisation générale aux mots qui n'ont pas été traités spécifiquement"""
    collection = connect_to_database()
    
    print("\n=== CAPITALISATION GÉNÉRALE ===")
    
    # Obtenir tous les mots
    words = collection.find({})
    general_corrections = 0
    
    for word in words:
        french = word.get('french', '')
        if french and french[0].islower():
            # Capitaliser seulement si pas déjà traité spécifiquement
            if not word.get('french_formatting_corrected'):
                capitalized = french.capitalize()
                
                result = collection.update_one(
                    {"_id": word["_id"]},
                    {"$set": {
                        "french": capitalized,
                        "updated_at": datetime.utcnow(),
                        "general_capitalization_applied": True
                    }}
                )
                
                if result.modified_count > 0:
                    print(f"✓ Capitalisé: '{french}' → '{capitalized}'")
                    general_corrections += 1
    
    return general_corrections

def verify_corrections():
    """Vérifie les corrections appliquées"""
    collection = connect_to_database()
    
    print(f"\n=== VÉRIFICATION DES CORRECTIONS ===")
    
    # Vérifier quelques corrections clés
    test_words = ["Frère", "École", "Tête", "Grand-père", "Œil", "Étoile"]
    
    for french_word in test_words:
        word = collection.find_one({"french": french_word})
        if word:
            print(f"✓ Trouvé: '{french_word}'")
        else:
            print(f"✗ Manquant: '{french_word}'")
    
    # Statistiques
    total_words = collection.count_documents({})
    corrected_words = collection.count_documents({"french_formatting_corrected": True})
    capitalized_words = collection.count_documents({"general_capitalization_applied": True})
    
    print(f"\nSTATISTIQUES:")
    print(f"Total mots: {total_words}")
    print(f"Corrections spécifiques: {corrected_words}")
    print(f"Capitalisations générales: {capitalized_words}")

def main():
    """Fonction principale"""
    print("=== CORRECTION DU FORMATAGE DES MOTS FRANÇAIS ===")
    print("Remise des accents appropriés et ajout des majuscules\n")
    
    # Créer sauvegarde
    backup_file = backup_database()
    
    try:
        # Appliquer corrections spécifiques
        specific_corrections = fix_french_formatting()
        
        # Appliquer capitalisation générale
        general_corrections = apply_general_capitalization()
        
        total_corrections = specific_corrections + general_corrections
        print(f"\n✅ {total_corrections} corrections appliquées:")
        print(f"  - Corrections spécifiques: {specific_corrections}")
        print(f"  - Capitalisations générales: {general_corrections}")
        
        # Vérifier
        verify_corrections()
        
        print(f"\n🎉 FORMATAGE FRANÇAIS CORRIGÉ AVEC SUCCÈS!")
        print(f"Sauvegarde disponible: {backup_file}")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        print(f"Restaurez la sauvegarde si nécessaire: {backup_file}")
        raise

if __name__ == "__main__":
    main()