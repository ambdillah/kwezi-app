#!/usr/bin/env python3
"""
Script de correction ciblée pour appliquer précisément les corrections du PDF
Corrige les problèmes identifiés par le testing agent
"""

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
import os
import re
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL')
client = MongoClient(MONGO_URL)
db = client.kwezi
words_collection = db.words

def fix_escargot_translation():
    """Corrige la traduction d'escargot: 'kwa' -> 'kowa'"""
    print("🐌 CORRECTION ESCARGOT: kwa -> kowa")
    
    # Trouver l'escargot avec 'kwa'
    escargot_kwa = words_collection.find_one({"french": "escargot", "shimaore": "kwa"})
    if escargot_kwa:
        words_collection.update_one(
            {"_id": escargot_kwa["_id"]},
            {"$set": {"shimaore": "kowa"}}
        )
        print("  ✅ Escargot corrigé: 'kwa' -> 'kowa'")
        return True
    else:
        print("  ℹ️ Escargot avec 'kwa' non trouvé")
        return False

def fix_oursin_huitre_translations():
    """Différencie les traductions d'oursin et d'huître"""
    print("🦪 CORRECTION OURSIN/HUITRE: différenciation")
    
    # Corriger oursin
    oursin = words_collection.find_one({"french": "oursin"})
    if oursin and oursin.get("shimaore") == "gadzassi":
        words_collection.update_one(
            {"_id": oursin["_id"]},
            {"$set": {"shimaore": "gadzassi ya bahari"}}
        )
        print("  ✅ Oursin différencié: 'gadzassi ya bahari'")
    
    # Corriger huître
    huitre = words_collection.find_one({"french": "huître"})
    if huitre and huitre.get("shimaore") == "gadzassi":
        words_collection.update_one(
            {"_id": huitre["_id"]},
            {"$set": {"shimaore": "gadzassi ya mshindi"}}
        )
        print("  ✅ Huître différenciée: 'gadzassi ya mshindi'")
    
    return True

def remove_french_accents():
    """Supprime les accents des mots français"""
    print("📝 SUPPRESSION ACCENTS FRANÇAIS")
    
    accent_map = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a', 'á': 'a',
        'ù': 'u', 'û': 'u', 'ü': 'u', 'ú': 'u',
        'ô': 'o', 'ö': 'o', 'ó': 'o', 'ò': 'o',
        'î': 'i', 'ï': 'i', 'í': 'i', 'ì': 'i',
        'ç': 'c', 'ñ': 'n',
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'À': 'A', 'Â': 'A', 'Ä': 'A', 'Á': 'A',
        'Ù': 'U', 'Û': 'U', 'Ü': 'U', 'Ú': 'U',
        'Ô': 'O', 'Ö': 'O', 'Ó': 'O', 'Ò': 'O',
        'Î': 'I', 'Ï': 'I', 'Í': 'I', 'Ì': 'I',
        'Ç': 'C', 'Ñ': 'N'
    }
    
    def remove_accents(text):
        """Supprime les accents d'une chaîne"""
        if not text:
            return text
        result = text
        for accented, plain in accent_map.items():
            result = result.replace(accented, plain)
        return result
    
    # Trouver tous les mots avec accents français
    words_with_accents = list(words_collection.find({}))
    corrections_count = 0
    
    for word in words_with_accents:
        original_french = word.get('french', '')
        corrected_french = remove_accents(original_french)
        
        if original_french != corrected_french:
            words_collection.update_one(
                {"_id": word["_id"]},
                {"$set": {"french": corrected_french}}
            )
            print(f"  📝 {original_french} -> {corrected_french}")
            corrections_count += 1
    
    print(f"  📊 {corrections_count} mots français corrigés")
    return corrections_count

def remove_shimaore_accents():
    """Supprime les accents des traductions shimaoré"""
    print("📝 SUPPRESSION ACCENTS SHIMAORÉ")
    
    accent_map = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a', 'á': 'a',
        'ù': 'u', 'û': 'u', 'ü': 'u', 'ú': 'u',
        'ô': 'o', 'ö': 'o', 'ó': 'o', 'ò': 'o',
        'î': 'i', 'ï': 'i', 'í': 'i', 'ì': 'i',
        'ç': 'c', 'ñ': 'n'
    }
    
    def remove_accents(text):
        """Supprime les accents d'une chaîne"""
        if not text:
            return text
        result = text
        for accented, plain in accent_map.items():
            result = result.replace(accented, plain)
        return result
    
    # Trouver tous les mots avec accents shimaoré
    words_with_accents = list(words_collection.find({"shimaore": {"$regex": "[éèêëàâäáùûüúôöóòîïíìçñ]"}}))
    corrections_count = 0
    
    for word in words_with_accents:
        original_shimaore = word.get('shimaore', '')
        corrected_shimaore = remove_accents(original_shimaore)
        
        if original_shimaore != corrected_shimaore:
            words_collection.update_one(
                {"_id": word["_id"]},
                {"$set": {"shimaore": corrected_shimaore}}
            )
            print(f"  📝 {word.get('french', '')}: {original_shimaore} -> {corrected_shimaore}")
            corrections_count += 1
    
    print(f"  📊 {corrections_count} traductions shimaoré corrigées")
    return corrections_count

def add_missing_pdf_words():
    """Ajoute les mots manquants identifiés dans le PDF"""
    print("➕ AJOUT MOTS MANQUANTS DU PDF")
    
    missing_words = [
        {"french": "pente", "shimaore": "mlima", "kibouchi": "boungou", "category": "nature"},
    ]
    
    added_count = 0
    for word_data in missing_words:
        # Vérifier si le mot existe
        existing = words_collection.find_one({"french": word_data["french"]})
        if not existing:
            word_data["emoji"] = ""
            word_data["has_image"] = False
            words_collection.insert_one(word_data)
            print(f"  ➕ Ajouté: {word_data['french']}")
            added_count += 1
        else:
            # Mettre à jour avec kibouchi si manquant
            if not existing.get("kibouchi") and word_data.get("kibouchi"):
                words_collection.update_one(
                    {"_id": existing["_id"]},
                    {"$set": {"kibouchi": word_data["kibouchi"]}}
                )
                print(f"  🔄 Mis à jour kibouchi: {word_data['french']} -> {word_data['kibouchi']}")
    
    print(f"  📊 {added_count} mots ajoutés")
    return added_count

def verify_bigorno_bigorneau():
    """Vérifie la correction bigorno/bigorneau"""
    print("🐢 VÉRIFICATION BIGORNO/BIGORNEAU")
    
    bigorno = words_collection.find_one({"shimaore": "bigorno"})
    bigorneau = words_collection.find_one({"french": "bigorneau"})
    
    if bigorno:
        print(f"  ⚠️ 'bigorno' trouvé: {bigorno.get('french')} -> {bigorno.get('shimaore')}")
        # Supprimer bigorno si c'est pour tortue
        if bigorno.get('french') == 'tortue':
            words_collection.delete_one({"_id": bigorno["_id"]})
            print("  🗑️ Supprimé: tortue -> bigorno")
    else:
        print("  ✅ Aucun 'bigorno' trouvé")
    
    if bigorneau:
        print(f"  ✅ 'bigorneau' confirmé: {bigorneau.get('shimaore')}")
    else:
        print("  ❌ 'bigorneau' manquant")
    
    return True

def generate_verification_report():
    """Génère un rapport de vérification après corrections"""
    print("\n📊 RAPPORT DE VÉRIFICATION")
    print("=" * 50)
    
    # Statistiques générales
    total_words = words_collection.count_documents({})
    print(f"Total des mots: {total_words}")
    
    # Vérifier les doublons
    pipeline = [
        {"$group": {"_id": "$french", "count": {"$sum": 1}, "docs": {"$push": "$_id"}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    
    duplicates = list(words_collection.aggregate(pipeline))
    print(f"Doublons: {len(duplicates)}")
    if duplicates:
        for dup in duplicates[:5]:
            print(f"  - '{dup['_id']}': {dup['count']} occurrences")
    
    # Vérifier les mots avec accents français
    french_with_accents = words_collection.count_documents({"french": {"$regex": "[éèêëàâäáùûüúôöóòîïíìçñÉÈÊËÀÂÄÁÙÛÜÚÔÖÓÒÎÏÍÌÇÑ]"}})
    print(f"Mots français avec accents: {french_with_accents}")
    
    # Vérifier les traductions shimaoré avec accents
    shimaore_with_accents = words_collection.count_documents({"shimaore": {"$regex": "[éèêëàâäáùûüúôöóòîïíìçñ]"}})
    print(f"Traductions shimaoré avec accents: {shimaore_with_accents}")
    
    # Vérifier couverture kibouchi
    with_kibouchi = words_collection.count_documents({"kibouchi": {"$ne": ""}})
    kibouchi_coverage = (with_kibouchi / total_words * 100) if total_words > 0 else 0
    print(f"Couverture kibouchi: {with_kibouchi}/{total_words} ({kibouchi_coverage:.1f}%)")
    
    # Vérifier cas spécifiques
    escargot = words_collection.find_one({"french": "escargot"})
    if escargot:
        print(f"Escargot: {escargot.get('shimaore', 'N/A')}")
    
    oursin = words_collection.find_one({"french": "oursin"})
    if oursin:
        print(f"Oursin: {oursin.get('shimaore', 'N/A')}")
    
    huitre = words_collection.find_one({"french": "huître"})
    if huitre:
        print(f"Huître: {huitre.get('shimaore', 'N/A')}")
    
    pente = words_collection.find_one({"french": "pente"})
    if pente:
        print(f"Pente: shimaore={pente.get('shimaore', 'N/A')}, kibouchi={pente.get('kibouchi', 'N/A')}")
    
    ecole_no_accent = words_collection.find_one({"french": "ecole"})
    if ecole_no_accent:
        print(f"École (sans accent): trouvée")
    else:
        ecole_with_accent = words_collection.find_one({"french": "école"})
        if ecole_with_accent:
            print(f"École (avec accent): encore présente")

def main():
    """Fonction principale de correction"""
    print("🔧 CORRECTION CIBLÉE DES ERREURS PDF")
    print("=" * 50)
    print(f"Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. Corriger escargot kwa -> kowa
        fix_escargot_translation()
        
        # 2. Différencier oursin/huître
        fix_oursin_huitre_translations()
        
        # 3. Supprimer accents français
        french_corrections = remove_french_accents()
        
        # 4. Supprimer accents shimaoré
        shimaore_corrections = remove_shimaore_accents()
        
        # 5. Ajouter mots manquants
        added_words = add_missing_pdf_words()
        
        # 6. Vérifier bigorno/bigorneau
        verify_bigorno_bigorneau()
        
        # 7. Rapport de vérification
        generate_verification_report()
        
        print(f"\n✅ CORRECTIONS APPLIQUÉES!")
        print(f"  - Corrections français: {french_corrections}")
        print(f"  - Corrections shimaoré: {shimaore_corrections}")
        print(f"  - Mots ajoutés: {added_words}")
        
    except Exception as e:
        print(f"❌ ERREUR: {str(e)}")
        raise

if __name__ == "__main__":
    main()