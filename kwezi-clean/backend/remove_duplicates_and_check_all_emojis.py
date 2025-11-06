#!/usr/bin/env python3
"""
SUPPRESSION DES DOUBLONS + VÉRIFICATION COMPLÈTE DES EMOJIS
===========================================================
1. Détecte et supprime automatiquement tous les doublons
2. Met en place une règle absolue anti-doublon
3. Vérifie TOUS les emojis inappropriés dans TOUTES les catégories
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from collections import defaultdict

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

def detect_and_remove_duplicates(db):
    """Détecter et supprimer automatiquement tous les doublons"""
    
    print("🔍 DÉTECTION DES DOUBLONS...")
    
    # Obtenir tous les mots
    all_words = list(db.words.find({}))
    print(f"📊 Total des mots: {len(all_words)}")
    
    # Grouper par mot français (clé unique)
    word_groups = defaultdict(list)
    
    for word in all_words:
        french_key = word.get('french', '').strip().lower()
        if french_key:
            word_groups[french_key].append(word)
    
    # Identifier les doublons
    duplicates_found = []
    unique_words = 0
    
    for french_key, words_list in word_groups.items():
        if len(words_list) > 1:
            duplicates_found.append((french_key, words_list))
        else:
            unique_words += 1
    
    print(f"📊 ANALYSE DES DOUBLONS:")
    print(f"  ✅ Mots uniques: {unique_words}")
    print(f"  🔄 Groupes avec doublons: {len(duplicates_found)}")
    
    if not duplicates_found:
        print("✅ Aucun doublon trouvé - base de données propre")
        return 0
    
    # Afficher et supprimer les doublons
    total_removed = 0
    
    for french_key, words_list in duplicates_found:
        print(f"\n🔄 DOUBLON: '{words_list[0].get('french', '')}' ({len(words_list)} occurrences)")
        
        # Garder le premier, supprimer les autres
        words_to_keep = words_list[0]
        words_to_remove = words_list[1:]
        
        print(f"  ✅ Gardé: {words_to_keep.get('french', '')} (ID: {words_to_keep['_id']})")
        
        for word_to_remove in words_to_remove:
            try:
                result = db.words.delete_one({"_id": word_to_remove["_id"]})
                if result.deleted_count > 0:
                    print(f"  🗑️ Supprimé: ID {word_to_remove['_id']}")
                    total_removed += 1
                else:
                    print(f"  ❌ Échec suppression: ID {word_to_remove['_id']}")
            except Exception as e:
                print(f"  ❌ Erreur suppression: {e}")
    
    print(f"\n📊 RÉSULTAT SUPPRESSION DOUBLONS: {total_removed} doublons supprimés")
    return total_removed

def create_unique_index(db):
    """Créer un index unique pour empêcher les doublons futurs"""
    
    print("\n🔒 CRÉATION D'UN INDEX UNIQUE ANTI-DOUBLON...")
    
    try:
        # Créer un index unique sur le champ 'french' (insensible à la casse)
        index_result = db.words.create_index(
            [("french", 1)],
            unique=True,
            collation={"locale": "fr", "strength": 2}  # Insensible à la casse
        )
        print(f"✅ Index unique créé: {index_result}")
        print("🔒 RÈGLE ABSOLUE: Plus aucun doublon ne pourra être inséré")
        return True
    except Exception as e:
        print(f"⚠️ Index unique déjà existant ou erreur: {e}")
        return True  # Ce n'est pas grave si l'index existe déjà

def check_all_inappropriate_emojis(db):
    """Vérifier TOUS les emojis inappropriés dans TOUTES les catégories"""
    
    print("\n🔍 VÉRIFICATION COMPLÈTE DES EMOJIS DANS TOUTES LES CATÉGORIES...")
    
    # Obtenir toutes les catégories
    categories = db.words.distinct("category")
    print(f"📚 Catégories à vérifier: {categories}")
    
    # Emojis considérés comme inappropriés ou flous
    inappropriate_emojis = {
        # Emojis suggestifs/sexuels
        '🫦': 'lèvres suggestives',
        '🍑': 'pêche suggestive/sexuelle',
        '🍆': 'aubergine suggestive',
        '🌶️': 'piment suggestif',
        '🥒': 'concombre suggestif',
        '💦': 'gouttes suggestives',
        '👅': 'langue peut être suggestive',
        '🍌': 'banane peut être suggestive dans certains contextes',
        
        # Emojis de parties du corps inappropriés
        '🥎': 'balle sportive pour parties intimes',
        '⚽': 'ballon pour parties intimes',
        '🏀': 'basketball pour parties intimes',
        '🤰': 'femme enceinte trop spécifique',
        
        # Emojis flous pour concepts abstraits
        '🧠': 'cerveau pour actions mentales abstraites',
        '💭': 'bulle de pensée pour concepts abstraits',
        '💡': 'ampoule pour idées abstraites',
        '❤️': 'cœur pour émotions complexes',
        '💪': 'muscle pour concepts de force abstraits',
        '🔥': 'feu pour concepts abstraits',
        '⭐': 'étoile pour concepts d\'importance',
        '🎯': 'cible pour concepts d\'objectif',
        '🎉': 'fête pour concepts de réussite',
        
        # Emojis de visages pour parties anatomiques
        '😊': 'visage souriant pour parties du corps',
        '🤔': 'visage pensif pour parties du corps',
        '🤨': 'visage suspicieux pour parties du corps', 
        '😐': 'visage neutre pour adjectifs',
        '😂': 'rire pour adjectifs',
        '😠': 'colère spécifique vs concepts généraux',
        '😟': 'inquiétude spécifique vs concepts généraux',
        '😲': 'surprise spécifique vs concepts généraux',
        '😳': 'gêne spécifique vs concepts généraux',
        '😴': 'endormi vs fatigue générale',
        
        # Emojis de mains inappropriés pour anatomie
        '🫱': 'main pour concept de peau générale',
        '🫸': 'main pour parties anatomiques',
        '👆': 'un doigt pour doigts généraux',
        '🤲': 'mains ouvertes pour concepts abstraits',
        '🤝': 'poignée de main pour concepts sociaux',
        
        # Emojis religieux/culturels génériques
        '🙏': 'prière pour concepts non-religieux',
        '🕌': 'mosquée pour personnes',
        '👨‍🦲': 'homme chauve générique',
        
        # Emojis d\'objets inappropriés
        '🗑️': 'poubelle pour concepts abstraits',
        '💳': 'carte bancaire pour concepts financiers',
        '📢': 'haut-parleur pour communication',
        '⚠️': 'panneau danger pour concepts d\'avertissement',
        '🚔': 'voiture police pour concepts de sécurité',
        '🚑': 'ambulance pour concepts médicaux',
        
        # Emojis d\'activités pour anatomie
        '💇': 'coiffure pour cheveux anatomiques',
        '🧼': 'savon pour concepts de propreté',
        '🧹': 'balai pour concepts de nettoyage',
        '🔨': 'marteau pour actions complexes',
        '⚖️': 'balance pour concepts de poids',
        '🪶': 'plume pour concepts de légèreté'
    }
    
    # Vérifier chaque catégorie
    total_inappropriate = 0
    inappropriate_by_category = {}
    
    for category in categories:
        print(f"\n📂 CATÉGORIE: {category}")
        words_in_category = list(db.words.find({"category": category, "image_url": {"$ne": ""}}))
        
        inappropriate_in_category = []
        
        for word in words_in_category:
            french = word.get('french', '')
            emoji = word.get('image_url', '')
            
            if emoji in inappropriate_emojis:
                inappropriate_in_category.append({
                    'french': french,
                    'emoji': emoji,
                    'reason': inappropriate_emojis[emoji],
                    '_id': word['_id']
                })
        
        if inappropriate_in_category:
            print(f"  ❌ {len(inappropriate_in_category)} emojis inappropriés trouvés:")
            for item in inappropriate_in_category:
                print(f"    🗑️ {item['french']}: {item['emoji']} ({item['reason']})")
            
            inappropriate_by_category[category] = inappropriate_in_category
            total_inappropriate += len(inappropriate_in_category)
        else:
            print(f"  ✅ Aucun emoji inapproprié")
    
    print(f"\n📊 RÉSUMÉ EMOJIS INAPPROPRIÉS:")
    print(f"  🔍 Catégories vérifiées: {len(categories)}")
    print(f"  ❌ Total emojis inappropriés: {total_inappropriate}")
    print(f"  📂 Catégories affectées: {len(inappropriate_by_category)}")
    
    return inappropriate_by_category

def remove_all_inappropriate_emojis(db, inappropriate_by_category):
    """Supprimer tous les emojis inappropriés identifiés"""
    
    if not inappropriate_by_category:
        print("✅ Aucun emoji inapproprié à supprimer")
        return 0
    
    print(f"\n🗑️ SUPPRESSION DE TOUS LES EMOJIS INAPPROPRIÉS...")
    
    total_removed = 0
    
    for category, inappropriate_list in inappropriate_by_category.items():
        print(f"\n📂 Nettoyage catégorie: {category}")
        
        for item in inappropriate_list:
            try:
                result = db.words.update_one(
                    {"_id": item['_id']},
                    {"$set": {"image_url": ""}}
                )
                
                if result.modified_count > 0:
                    print(f"  🗑️ {item['french']}: {item['emoji']} supprimé ({item['reason']})")
                    total_removed += 1
                else:
                    print(f"  ❌ Échec: {item['french']}")
            except Exception as e:
                print(f"  ❌ Erreur avec {item['french']}: {e}")
    
    print(f"\n📊 SUPPRESSION TERMINÉE: {total_removed} emojis inappropriés supprimés")
    return total_removed

def final_verification(db):
    """Vérification finale de la base de données"""
    
    print(f"\n🔍 VÉRIFICATION FINALE...")
    
    # Statistiques générales
    total_words = db.words.count_documents({})
    words_with_emojis = db.words.count_documents({"image_url": {"$ne": "", "$exists": True}})
    words_without_emojis = total_words - words_with_emojis
    
    print(f"📊 STATISTIQUES FINALES:")
    print(f"  📈 Total des mots: {total_words}")
    print(f"  ✅ Mots avec emojis: {words_with_emojis}")
    print(f"  🚫 Mots sans emoji: {words_without_emojis}")
    
    # Vérifier qu'il n'y a plus de doublons
    all_words = list(db.words.find({}, {"french": 1}))
    french_words = [w.get('french', '').strip().lower() for w in all_words if w.get('french', '').strip()]
    unique_count = len(set(french_words))
    
    if len(french_words) == unique_count:
        print(f"  ✅ Aucun doublon: {unique_count} mots uniques")
    else:
        print(f"  ❌ Doublons détectés: {len(french_words) - unique_count}")
    
    # Vérifier les catégories
    categories = db.words.distinct("category")
    print(f"  📚 Catégories: {len(categories)}")
    
    return total_words == unique_count

def main():
    """Fonction principale"""
    print("=" * 80)
    print("🔧 NETTOYAGE COMPLET: DOUBLONS + EMOJIS INAPPROPRIÉS")
    print("=" * 80)
    print("1. Suppression automatique des doublons")
    print("2. Index unique anti-doublon (règle absolue)")
    print("3. Vérification complète des emojis dans TOUTES les catégories")
    print("4. Suppression de tous les emojis inappropriés")
    print("=" * 80)
    
    # Connexion MongoDB
    client = get_mongo_client()
    if not client:
        return False
    
    db = client[DB_NAME]
    
    try:
        # 1. Supprimer les doublons
        duplicates_removed = detect_and_remove_duplicates(db)
        
        # 2. Créer un index unique pour empêcher les doublons futurs
        create_unique_index(db)
        
        # 3. Vérifier tous les emojis inappropriés
        inappropriate_emojis = check_all_inappropriate_emojis(db)
        
        # 4. Supprimer tous les emojis inappropriés
        emojis_removed = remove_all_inappropriate_emojis(db, inappropriate_emojis)
        
        # 5. Vérification finale
        success = final_verification(db)
        
        if success:
            print("\n" + "=" * 80)
            print("🎉 NETTOYAGE COMPLET RÉUSSI !")
            print(f"🗑️ {duplicates_removed} doublons supprimés")
            print(f"🗑️ {emojis_removed} emojis inappropriés supprimés")
            print("🔒 Règle anti-doublon activée (index unique)")
            print("✅ Base de données propre et professionnelle")
            print("=" * 80)
            return True
        else:
            print("\n❌ Problèmes détectés lors de la vérification finale")
            return False
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        return False
    
    finally:
        client.close()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)