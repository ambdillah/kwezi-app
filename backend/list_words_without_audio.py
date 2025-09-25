#!/usr/bin/env python3
"""
Script pour lister tous les mots sans correspondance audio dans la base de données
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

# Charger les variables d'environnement
load_dotenv()

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_database():
    """Connexion à la base de données MongoDB"""
    try:
        mongo_url = os.getenv('MONGO_URL')
        if not mongo_url:
            raise ValueError("MONGO_URL non trouvée dans les variables d'environnement")
        
        client = MongoClient(mongo_url)
        db = client['shimaoré_app']
        logger.info("Connexion à la base de données réussie")
        return db
    except Exception as e:
        logger.error(f"Erreur de connexion à la base de données: {e}")
        raise

def get_words_without_audio(db):
    """Récupère tous les mots sans audio authentique"""
    collection = db['vocabulary']
    
    # Chercher les mots sans audio authentique
    query = {
        "$or": [
            {"has_authentic_audio": {"$ne": True}},
            {"has_authentic_audio": {"$exists": False}},
            {"audio_authentic": {"$exists": False}},
            {"audio_authentic": {"$eq": ""}}
        ]
    }
    
    words_without_audio = list(collection.find(query))
    
    return words_without_audio

def organize_by_section(words):
    """Organise les mots par section"""
    sections = {}
    
    for word in words:
        section = word.get('section', 'unknown')
        if section not in sections:
            sections[section] = []
        
        sections[section].append({
            'french': word.get('french', 'N/A'),
            'shimaoré': word.get('shimaoré', 'N/A'),
            'kibouchi': word.get('kibouchi', 'N/A'),
            'audio_ref': word.get('audio_authentic', 'Aucun')
        })
    
    return sections

def display_words_without_audio():
    """Affiche tous les mots sans correspondance audio"""
    
    try:
        # Connexion à la base
        db = connect_to_database()
        
        # Récupérer les statistiques globales
        collection = db['vocabulary']
        total_words = collection.count_documents({})
        words_with_audio = collection.count_documents({"has_authentic_audio": True})
        words_without_audio_list = get_words_without_audio(db)
        words_without_audio_count = len(words_without_audio_list)
        
        print(f"\n{'='*80}")
        print("LISTE COMPLÈTE DES MOTS SANS CORRESPONDANCE AUDIO")
        print(f"{'='*80}")
        print(f"Total mots dans la base: {total_words}")
        print(f"Mots avec audio: {words_with_audio}")
        print(f"Mots SANS audio: {words_without_audio_count}")
        print(f"Couverture audio: {(words_with_audio/total_words)*100:.1f}%")
        
        # Organiser par section
        sections = organize_by_section(words_without_audio_list)
        
        print(f"\n{'='*80}")
        print("DÉTAIL PAR SECTION")
        print(f"{'='*80}")
        
        for section_name, words in sorted(sections.items()):
            print(f"\n--- SECTION: {section_name.upper()} ({len(words)} mots sans audio) ---")
            
            for i, word in enumerate(words, 1):
                print(f"{i:2d}. {word['french']:<25} | shimaoré: {word['shimaoré']:<25} | kibouchi: {word['kibouchi']}")
        
        print(f"\n{'='*80}")
        print("RÉSUMÉ PAR SECTION")
        print(f"{'='*80}")
        
        total_missing = 0
        for section_name, words in sorted(sections.items()):
            section_total = collection.count_documents({"section": section_name})
            section_with_audio = collection.count_documents({
                "section": section_name,
                "has_authentic_audio": True
            })
            section_without_audio = len(words)
            coverage = (section_with_audio / section_total) * 100 if section_total > 0 else 0
            
            print(f"{section_name:<15} | Total: {section_total:>3} | Avec audio: {section_with_audio:>3} | Sans audio: {section_without_audio:>3} | Couverture: {coverage:>5.1f}%")
            total_missing += section_without_audio
        
        print(f"\n{'='*80}")
        print("SECTIONS PRIORITAIRES À COMPLÉTER")
        print(f"{'='*80}")
        
        # Identifier les sections avec le plus de mots manquants
        priority_sections = []
        for section_name, words in sections.items():
            if len(words) > 5:  # Plus de 5 mots sans audio
                section_total = collection.count_documents({"section": section_name})
                coverage = ((section_total - len(words)) / section_total) * 100 if section_total > 0 else 0
                priority_sections.append((section_name, len(words), coverage))
        
        # Trier par nombre de mots manquants
        priority_sections.sort(key=lambda x: x[1], reverse=True)
        
        for section_name, missing_count, coverage in priority_sections:
            print(f"🔴 {section_name:<15} | {missing_count:>3} fichiers audio manquants | Couverture: {coverage:>5.1f}%")
        
        print(f"\n{'='*80}")
        print("RECOMMANDATIONS")
        print(f"{'='*80}")
        
        if total_missing == 0:
            print("🎉 PARFAIT! Tous les mots ont des correspondances audio!")
        elif total_missing < 50:
            print(f"✅ TRÈS BIEN! Seulement {total_missing} mots sans audio sur {total_words}")
            print("Vous pouvez procéder au développement des jeux.")
        elif total_missing < 100:
            print(f"⚠️ BIEN. {total_missing} mots sans audio sur {total_words}")
            print("Considérez compléter les sections prioritaires ci-dessus.")
        else:
            print(f"🔴 ATTENTION. {total_missing} mots sans audio sur {total_words}")
            print("Recommandé de compléter les fichiers audio avant les jeux.")
        
        return words_without_audio_list
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        return []

def main():
    """Fonction principale"""
    words_without_audio = display_words_without_audio()
    return len(words_without_audio)

if __name__ == "__main__":
    missing_count = main()
    exit(missing_count)