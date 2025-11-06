#!/usr/bin/env python3
"""
CORRECTION DES ASSOCIATIONS EMOJI INCORRECTES
=============================================
Corriger les emojis qui ne correspondent PAS exactement au mot :
- Papaye avec mangue 🥭 → SUPPRIMER (papaye ≠ mangue)
- Vanille avec feuilles 🌿 → SUPPRIMER (vanille ≠ feuilles génériques)
- Et autres associations incorrectes similaires

Principe : Si l'emoji ne représente pas EXACTEMENT le mot, le supprimer.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'mayotte_app')

def get_mongo_client():
    """Connexion à MongoDB"""
    try:
        client = MongoClient(MONGO_URL)
        client.admin.command('ping')
        print(f"✅ Connexion MongoDB établie : {MONGO_URL}")
        return client
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB : {e}")
        return None

def find_incorrect_emoji_associations(db):
    """Trouver les associations emoji incorrectes"""
    
    print("🔍 RECHERCHE DES ASSOCIATIONS EMOJI INCORRECTES...")
    
    # Associations spécifiquement INCORRECTES identifiées
    incorrect_associations = {
        # FRUITS - Associations fausses
        'papaye': {
            'incorrect_emoji': '🥭',  # Mangue ≠ Papaye
            'reason': 'Mangue 🥭 ≠ Papaye (fruits différents)'
        },
        'mangue': {
            'correct_emoji': '🥭',  # Mangue = OK
            'reason': 'Mangue 🥭 = Mangue (correct)'
        },
        
        # ÉPICES/AROMATES - Associations fausses
        'vanille': {
            'incorrect_emoji': '🌿',  # Feuilles génériques ≠ Vanille spécifique
            'reason': 'Feuilles 🌿 ≠ Vanille (trop générique)'
        },
        'curcuma': {
            'incorrect_emoji': '🧄',  # Ail ≠ Curcuma
            'reason': 'Ail 🧄 ≠ Curcuma (épices différentes)'
        },
        'gingembre': {
            'incorrect_emoji': '🧄',  # Ail ≠ Gingembre
            'reason': 'Ail 🧄 ≠ Gingembre (épices différentes)'
        },
        'cumin': {
            'incorrect_emoji': '🧄',  # Ail ≠ Cumin
            'reason': 'Ail 🧄 ≠ Cumin (épices différentes)'
        },
        
        # LÉGUMES - Associations fausses
        'taro': {
            'incorrect_emoji': '🥔',  # Pomme de terre ≠ Taro
            'reason': 'Pomme de terre 🥔 ≠ Taro (tubercules différents)'
        },
        'manioc': {
            'incorrect_emoji': '🥔',  # Pomme de terre ≠ Manioc
            'reason': 'Pomme de terre 🥔 ≠ Manioc (tubercules différents)'
        },
        
        # ALIMENTS TRANSFORMÉS - Pas de représentation exacte
        'riz au coco': {
            'incorrect_emoji': '🍚',  # Riz simple ≠ Riz au coco
            'reason': 'Riz simple 🍚 ≠ Riz au coco (préparations différentes)'
        },
        'banane au coco': {
            'incorrect_emoji': '🍌',  # Banane simple ≠ Banane au coco
            'reason': 'Banane simple 🍌 ≠ Banane au coco (préparations différentes)'
        },
        
        # PLATS CUISINÉS - Pas de représentation exacte
        'bouillon': {
            'incorrect_emoji': '🍲',  # Ragoût ≠ Bouillon liquide
            'reason': 'Ragoût 🍲 ≠ Bouillon liquide (consistances différentes)'
        },
        
        # OBJETS SPÉCIFIQUES - Représentations fausses
        'pirogue': {
            'incorrect_emoji': '🛶',  # Canoe générique ≠ Pirogue traditionnelle
            'reason': 'Canoe 🛶 ≠ Pirogue traditionnelle (embarcations différentes)'
        },
        'kwassa kwassa': {
            'incorrect_emoji': '🚤',  # Vedette générique ≠ Kwassa kwassa spécifique
            'reason': 'Vedette 🚤 ≠ Kwassa kwassa (embarcations différentes)'
        },
        
        # CONCEPTS CULTURELS - Pas de représentation exacte
        'salouva': {
            'incorrect_emoji': '👗',  # Robe générique ≠ Salouva traditionnel
            'reason': 'Robe 👗 ≠ Salouva traditionnel (vêtements différents)'
        },
        
        # PARTIES ANATOMIQUES - Représentations approximatives
        'cou': {
            'incorrect_emoji': '🦒',  # Girafe ≠ Cou humain
            'reason': 'Girafe 🦒 ≠ Cou humain (anatomies différentes)'
        },
        'cheville': {
            'incorrect_emoji': '🦶',  # Pied complet ≠ Cheville spécifique
            'reason': 'Pied 🦶 ≠ Cheville (parties anatomiques différentes)'
        },
        
        # MATÉRIAUX/OBJETS - Représentations fausses
        'bambou': {
            'incorrect_emoji': '🎋',  # Décoration bambou ≠ Bambou plante
            'reason': 'Décoration 🎋 ≠ Bambou plante (contextes différents)'
        },
        
        # ÉMOTIONS/ÉTATS - Représentations approximatives
        'triste': {
            'incorrect_emoji': '😢',  # Visage qui pleure ≠ tristesse générale
            'reason': 'Pleurer 😢 ≠ Tristesse générale (émotions spécifiques)'
        },
        'content': {
            'incorrect_emoji': '😊',  # Sourire ≠ Contentement
            'reason': 'Sourire 😊 ≠ Contentement (émotions différentes)'
        },
        
        # ACTIONS - Représentations approximatives
        'rire': {
            'incorrect_emoji': '😂',  # Pleurs de rire ≠ Rire simple
            'reason': 'Pleurs de rire 😂 ≠ Rire simple (intensités différentes)'
        }
    }
    
    # Rechercher ces mots dans la base
    incorrect_found = []
    
    for word_french, emoji_info in incorrect_associations.items():
        # Chercher le mot dans la base
        word_doc = db.words.find_one({'french': {'$regex': f'^{word_french}$', '$options': 'i'}})
        
        if word_doc:
            current_emoji = word_doc.get('image_url', '')
            word_id = word_doc.get('_id')
            
            # Vérifier si c'est une association incorrecte
            if 'incorrect_emoji' in emoji_info and current_emoji == emoji_info['incorrect_emoji']:
                incorrect_found.append({
                    'french': word_doc.get('french', ''),
                    'current_emoji': current_emoji,
                    'reason': emoji_info['reason'],
                    '_id': word_id,
                    'category': word_doc.get('category', '')
                })
                print(f"❌ INCORRECT: {word_doc.get('french', '')}: {current_emoji} - {emoji_info['reason']}")
            elif 'correct_emoji' in emoji_info and current_emoji == emoji_info['correct_emoji']:
                print(f"✅ CORRECT: {word_doc.get('french', '')}: {current_emoji} - {emoji_info['reason']}")
        else:
            print(f"? {word_french}: non trouvé dans la base")
    
    return incorrect_found

def find_additional_incorrect_associations(db):
    """Chercher d'autres associations potentiellement incorrectes"""
    
    print(f"\n🔍 RECHERCHE D'AUTRES ASSOCIATIONS POTENTIELLEMENT INCORRECTES...")
    
    # Rechercher des patterns d'associations douteuses
    all_words = list(db.words.find({'image_url': {'$ne': ''}}))
    
    additional_incorrect = []
    
    for word in all_words:
        french = word.get('french', '').lower()
        emoji = word.get('image_url', '')
        category = word.get('category', '')
        
        # Associations suspectes à vérifier manuellement
        suspicious_patterns = [
            # Fruits différents avec même emoji
            (french == 'orange' and emoji == '🍊', 'Orange avec orange - OK'),
            (french == 'mandarine' and emoji == '🍊', 'Mandarine avec orange - agrumes similaires mais différents'),
            (french == 'citron' and emoji == '🍊', 'Citron avec orange - agrumes mais couleurs différentes'),
            
            # Légumes/tubercules avec représentations génériques
            ('patate' in french and emoji == '🍠', 'Patate douce - représentation approximative'),
            
            # Animaux avec représentations génériques
            (french == 'margouillat' and emoji == '🦎', 'Margouillat avec lézard générique'),
            (french == 'caméléon' and emoji == '🦎', 'Caméléon avec lézard générique'),
            
            # Vêtements culturels avec représentations génériques
            ('kamis' in french and emoji == '👘', 'Kamis avec kimono - vêtements différents'),
            ('boubou' in french and emoji == '👘', 'Boubou avec kimono - vêtements différents'),
        ]
        
        for condition, reason in suspicious_patterns:
            if condition:
                if 'différents' in reason or 'générique' in reason:
                    additional_incorrect.append({
                        'french': word.get('french', ''),
                        'current_emoji': emoji,
                        'reason': reason,
                        '_id': word.get('_id'),
                        'category': category
                    })
    
    return additional_incorrect

def remove_incorrect_associations(db, incorrect_associations):
    """Supprimer toutes les associations incorrectes"""
    
    if not incorrect_associations:
        print("✅ Aucune association incorrecte trouvée")
        return 0
    
    print(f"\n🗑️ SUPPRESSION DES ASSOCIATIONS INCORRECTES...")
    
    removed_count = 0
    
    for item in incorrect_associations:
        try:
            result = db.words.update_one(
                {'_id': item['_id']},
                {'$set': {'image_url': ''}}
            )
            
            if result.modified_count > 0:
                print(f"🗑️ {item['french']} ({item['category']}): {item['current_emoji']} supprimé")
                print(f"   Raison: {item['reason']}")
                removed_count += 1
            else:
                print(f"❌ Échec: {item['french']}")
                
        except Exception as e:
            print(f"❌ Erreur avec {item['french']}: {e}")
    
    return removed_count

def verify_corrections(db):
    """Vérifier que les corrections ont été appliquées"""
    
    print(f"\n🔍 VÉRIFICATION DES CORRECTIONS...")
    
    # Vérifier les mots spécifiquement corrigés
    target_words = ['papaye', 'vanille', 'curcuma', 'gingembre', 'taro', 'manioc']
    
    for word_name in target_words:
        word = db.words.find_one({'french': {'$regex': f'^{word_name}$', '$options': 'i'}})
        if word:
            emoji = word.get('image_url', '')
            if emoji == '':
                print(f"✅ {word.get('french', '')}: Emoji incorrect supprimé")
            else:
                print(f"⚠️ {word.get('french', '')}: Encore emoji {emoji}")
        else:
            print(f"? {word_name}: non trouvé")
    
    # Statistiques finales
    total_words = db.words.count_documents({})
    words_with_emojis = db.words.count_documents({'image_url': {'$ne': '', '$exists': True}})
    words_without_emojis = total_words - words_with_emojis
    
    print(f"\n📊 STATISTIQUES APRÈS CORRECTION:")
    print(f"  📈 Total des mots: {total_words}")
    print(f"  ✅ Mots avec emojis: {words_with_emojis}")
    print(f"  🚫 Mots sans emoji: {words_without_emojis}")
    
    return True

def main():
    """Fonction principale"""
    print("=" * 80)
    print("🔧 CORRECTION DES ASSOCIATIONS EMOJI INCORRECTES")
    print("=" * 80)
    print("Exemples : Papaye🥭→❌ (mangue≠papaye), Vanille🌿→❌ (feuilles≠vanille)")
    print("Principe: Si emoji ≠ mot exact → SUPPRIMER")
    print("=" * 80)
    
    # Connexion MongoDB
    client = get_mongo_client()
    if not client:
        return False
    
    db = client[DB_NAME]
    
    try:
        # 1. Chercher les associations spécifiquement incorrectes
        incorrect_associations = find_incorrect_emoji_associations(db)
        
        # 2. Chercher d'autres associations potentiellement incorrectes
        additional_incorrect = find_additional_incorrect_associations(db)
        
        # 3. Combiner toutes les associations incorrectes
        all_incorrect = incorrect_associations + additional_incorrect
        
        print(f"\n📊 RÉSUMÉ:")
        print(f"  ❌ Associations incorrectes spécifiques: {len(incorrect_associations)}")
        print(f"  ⚠️ Associations douteuses additionnelles: {len(additional_incorrect)}")
        print(f"  🗑️ Total à corriger: {len(all_incorrect)}")
        
        # 4. Supprimer toutes les associations incorrectes
        removed_count = remove_incorrect_associations(db, all_incorrect)
        
        # 5. Vérifier les corrections
        verify_corrections(db)
        
        if removed_count > 0:
            print("\n" + "=" * 80)
            print("🎉 CORRECTIONS RÉUSSIES !")
            print(f"🗑️ {removed_count} associations emoji incorrectes supprimées")
            print("✅ Fini les confusions type 'papaye🥭' ou 'vanille🌿'")
            print("✅ Seuls les emojis parfaitement exacts sont conservés")
            print("=" * 80)
            return True
        else:
            print("\n✅ Aucune association incorrecte trouvée - base déjà correcte")
            return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False
    
    finally:
        client.close()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)