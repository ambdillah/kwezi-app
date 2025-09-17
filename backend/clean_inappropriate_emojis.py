#!/usr/bin/env python3
"""
NETTOYAGE DES EMOJIS INAPPROPRIÉS OU FLOUS
==========================================
Ce script supprime tous les emojis dont la signification est floue ou incorrecte
et ne garde que ceux qui représentent EXACTEMENT le mot.

Principe : Si l'emoji n'est pas une représentation claire et exacte du mot, on le supprime.
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

def identify_inappropriate_emojis():
    """
    Identifier les mots avec des emojis inappropriés ou flous
    Retourne une liste de mots à nettoyer
    """
    
    # Mots avec emojis INAPPROPRIÉS ou FLOUS à supprimer
    inappropriate_emojis = {
        # Parties du corps avec représentations floues
        "pénis": "🌶️",  # Piment = flou/incorrect
        "testicules": "🥚",  # Œuf = flou/incorrect  
        "vagin": "🌸",  # Fleur = flou/incorrect
        "fesses": "🍑",  # Pêche = flou/suggestif
        
        # Concepts abstraits sans représentation exacte
        "respect": "🙏",  # Prière ≠ respect exact
        "convivialité": "🤗",  # Câlin ≠ convivialité exacte
        "entraide": "🤝",  # Poignée de main = proche mais pas exact
        "avoir la haine": "😠",  # Colère = proche mais "haine" plus fort
        "joie": "😄",  # Sourire = proche mais pas identique
        "secret": "🤐",  # Bouche fermée = approximatif
        "faire crédit": "💳",  # Carte bancaire ≠ crédit exact
        
        # Mots trop génériques
        "quelqu'un de fiable": "🤝",  # Trop générique
        "nounou": "👶",  # Bébé ≠ nounou
        
        # Parties du corps difficiles à représenter exactement
        "arrière du crâne": "🤯",  # Explosion ≠ arrière crâne
        "côtes": "🫁",  # Poumons ≠ côtes exactement
        "hanche": "🫴",  # Main ouverte ≠ hanche
        "sourcil": "🤨",  # Visage suspicieux ≠ sourcil exact
        "cils": "👁️",  # Œil général ≠ cils spécifiques
        
        # Actions complexes
        "flatuler": "💨",  # Vent = OK mais peut-être trop suggestif
        "faire caca": "🚽",  # Toilettes = contexte mais pas action exacte
        "faire pipi": "🚽",  # Toilettes = contexte mais pas action exacte
        "vomir": "🤢",  # Nausée ≠ vomir exact
        
        # Concepts abstraits de grammaire
        "professeur": "👨‍🏫",  # OK - représentation exacte (GARDER)
        "guide spirituel": "👨‍🦲",  # Homme chauve ≠ guide spirituel exact
        "imam": "👨‍🦲",  # Homme chauve ≠ imam exact
        
        # Objets sans représentation emoji exacte
        "fagot": "🪵",  # Bois général ≠ fagot exact
        "platier": "🏝️",  # Île ≠ platier exact
        "érosion": "🏞️",  # Paysage ≠ érosion exacte
        
        # Concepts temporels/abstraits
        "marée basse": "🌊",  # Vague générale ≠ marée basse exacte
        "marée haute": "🌊",  # Vague générale ≠ marée haute exacte
        "inondé": "🌊",  # Vague ≠ inondation exacte
        
        # États/conditions
        "sauvage": "🦁",  # Lion ≠ concept "sauvage" général
        "fâché": "😠",  # Colère générale = OK mais "fâché" plus spécifique
        "inquiet": "😟",  # Visage inquiet = OK mais gardons seulement les très exacts
        "surpris": "😲",  # Visage surpris = OK mais gardons seulement les très exacts
        "honteux": "😳",  # Visage gêné = approximatif
        
        # Aliments transformés
        "bouillon": "🍲",  # Ragoût ≠ bouillon exact
        "riz au coco": "🍚",  # Riz simple ≠ riz au coco
        "banane au coco": "🍌",  # Banane simple ≠ banane au coco
    }
    
    # Mots avec emojis APPROPRIÉS à GARDER (représentation exacte)
    appropriate_emojis = {
        # Animaux - représentation exacte
        "chat": "🐱", "chien": "🐕", "poisson": "🐟", "oiseau": "🐦",
        "éléphant": "🐘", "lion": "🦁", "serpent": "🐍", "tortue": "🐢",
        
        # Couleurs - représentation exacte
        "rouge": "🔴", "bleu": "🔵", "vert": "🟢", "jaune": "🟡", 
        "blanc": "⚪", "noir": "⚫",
        
        # Nombres - représentation exacte
        "un": "1️⃣", "deux": "2️⃣", "trois": "3️⃣", "quatre": "4️⃣", "cinq": "5️⃣",
        
        # Famille - représentation exacte
        "papa": "👨", "maman": "👩", "enfant": "👶", "garçon": "👦", "fille": "👧",
        
        # Corps - parties claires
        "œil": "👁️", "main": "✋", "pied": "🦶", "nez": "👃", "oreille": "👂",
        
        # Nature - éléments clairs
        "soleil": "☀️", "lune": "🌙", "arbre": "🌳", "fleur": "🌺", "mer": "🌊",
        
        # Nourriture - items exacts
        "banane": "🍌", "pomme": "🍎", "pain": "🍞", "eau": "💧",
        
        # Actions simples et claires
        "dormir": "💤", "manger": "🍽️", "boire": "🥤",
        
        # Objets usuels
        "maison": "🏠", "porte": "🚪", "voiture": "🚗",
        
        # Salutations avec gestes clairs
        "bonjour": "☀️", "au revoir": "👋", "merci": "🙏",
    }
    
    return inappropriate_emojis, appropriate_emojis

def clean_inappropriate_emojis(db):
    """Nettoyer les emojis inappropriés de la base de données"""
    
    print("🧹 NETTOYAGE DES EMOJIS INAPPROPRIÉS...")
    
    # Obtenir tous les mots avec des emojis (utilise 'image_url' pas 'emoji')
    words_with_emojis = list(db.words.find({"image_url": {"$exists": True, "$ne": ""}}))
    
    print(f"📊 Trouvé {len(words_with_emojis)} mots avec emojis")
    
    cleaned_count = 0
    kept_count = 0
    
    # Mots avec emojis INAPPROPRIÉS ou FLOUS à supprimer
    words_to_clean = {
        # Concepts abstraits difficiles à représenter exactement
        "front": "🤔",  # Visage pensif ≠ front anatomique
        "sourcil": "🤨",  # Visage suspicieux ≠ sourcil spécifique
        "cils": "👁️",  # Œil général ≠ cils spécifiques
        "arrière du crâne": "🤯",  # Explosion mentale ≠ partie anatomique
        "hanche": "🫴",  # Main ouverte ≠ hanche anatomique
        "côtes": "🫁",  # Poumons ≠ côtes osseuses
        "épaule": "💪",  # Muscle/force ≠ épaule anatomique exacte
        
        # Concepts spirituels/professionnels
        "guide spirituel": "👨‍🦲",  # Homme chauve ≠ guide spirituel exact
        "imam": "👨‍🦲",  # Homme chauve ≠ imam exact (trop générique)
        
        # Concepts naturels complexes
        "érosion": "🌊",  # Vague ≠ processus d'érosion
        "marée basse": "🌊",  # Vague générale ≠ marée basse spécifique
        "marée haute": "🌊",  # Vague générale ≠ marée haute spécifique
        "platier": "🪨",  # Pierre ≠ platier récifal spécifique
        "inondé": "🌊",  # Vague ≠ état d'inondation
        "sauvage": "🌿",  # Plante ≠ concept "sauvage"
        "barrière de corail": "🪸",  # Corail simple ≠ barrière complète
        
        # Objets spécifiques mal représentés
        "fagot": "🪵",  # Bois général ≠ fagot assemblé
        "bouillon": "🍲",  # Ragoût ≠ bouillon liquide
        
        # Verbes d'action/état mental
        "savoir": "🧠",  # Cerveau ≠ action de savoir
        "pouvoir": "💪",  # Force ≠ capacité/permission
        "croire": "🙏",  # Prière ≠ action de croire
        "penser": "💭",  # OK mais gardons seulement les représentations très exactes
        "comprendre": "💡",  # Ampoule = idée, pas compréhension exacte
        "apprendre": "📚",  # Livres = contexte mais pas action exacte
        "connaître": "🧠",  # Cerveau ≠ action de connaître
        "se rappeler": "🧠",  # Cerveau ≠ action de rappel
        "sembler": "🤔",  # Visage pensif ≠ action de sembler
        "paraître": "👀",  # Yeux ≠ action de paraître
        "devenir": "🔄",  # Flèche circulaire = approximatif
        "réussir": "🎉",  # Fête = célébration du succès, pas l'action exacte
        "essayer": "🎯",  # Cible = objectif, pas action d'essayer
        
        # États émotionnels complexes
        "inquiet": "😟",  # Visage inquiet = proche mais gardons que l'exact
        "surpris": "😲",  # Visage surpris = proche mais gardons que l'exact
        "honteux": "😳",  # Visage gêné = approximatif
        "fier": "😤",  # Visage fier = approximatif
        "amoureux": "❤️",  # Cœur = amour général, pas état amoureux exact
        "fâché": "😠",  # Colère générale = OK mais "fâché" plus spécifique
        
        # Adjectifs abstraits
        "intelligent": "🧠",  # Cerveau ≠ qualité d'intelligence
        "bête": "🤪",  # Visage fou ≠ bêtise exacte
        "sérieux": "😐",  # Visage neutre ≠ sérieux exact
        "drôle": "😂",  # Rire = réaction au drôle, pas l'adjectif exact
        "important": "⭐",  # Étoile = excellence, pas importance exacte
        "inutile": "🗑️",  # Poubelle = contexte mais pas inutilité exacte
        "faux": "❌",  # Croix rouge = négation, pas fausseté exacte
        "vrai": "✅",  # Coche verte = validation, pas vérité exacte
        "content": "😊",  # Sourire = proche mais gardons que l'exact
        "triste": "😢",  # Visage triste = OK, assez exact
        "fatigué": "😴",  # Visage endormi = proche mais pas identique
        
        # Actions complexes
        "arnaquer": "🕵️",  # Détective ≠ action d'arnaquer
        "informer": "📢",  # Haut-parleur = diffusion, pas information exacte
        "avertir": "⚠️",  # Panneau danger = contexte mais pas action exacte
    }
    
    # Mots avec emojis APPROPRIÉS à ABSOLUMENT GARDER
    keep_these_emojis = {
        # Animaux - représentation exacte parfaite
        "chat", "chien", "poisson", "oiseau", "éléphant", "lion", "serpent", 
        "tortue", "crabe", "requin", "cochon", "cheval", "chèvre", "mouton",
        
        # Couleurs - représentation exacte parfaite  
        "rouge", "bleu", "vert", "jaune", "blanc", "noir",
        
        # Nombres - représentation exacte parfaite
        "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix",
        
        # Famille - représentation claire
        "papa", "maman", "enfant", "garçon", "fille", "bébé",
        
        # Corps - parties anatomiques claires et evidentes
        "œil", "main", "pied", "nez", "oreille", "tête", "bouche", "dent",
        
        # Nature - éléments évidents
        "soleil", "lune", "arbre", "fleur", "mer", "étoile",
        
        # Nourriture - items précis
        "banane", "pomme", "pain", "eau", "riz", "poisson", "œuf",
        
        # Objets usuels évidents
        "maison", "porte", "voiture", "vélo", "avion",
        
        # Actions physiques simples et claires
        "dormir", "manger", "boire", "courir", "marcher",
        
        # Salutations avec gestes universels
        "au revoir", "merci",
        
        # Émotions de base très claires
        "rire", "pleurer"
    }
    
    for word in words_with_emojis:
        french_word = word.get("french", "").lower()
        current_emoji = word.get("image_url", "")
        word_id = word.get("_id")
        
        should_remove = False
        reason = ""
        
        # Vérifier si c'est dans la liste à nettoyer
        if french_word in words_to_clean:
            should_remove = True
            reason = "emoji inapproprié/flou pour ce concept"
            
        # Vérifier si c'est dans la liste à garder absolument
        elif french_word in keep_these_emojis:
            should_remove = False
            reason = "emoji parfaitement approprié - gardé"
            
        # Pour les autres mots, logique conservative : supprimer si concept abstrait
        else:
            # Mots clés indiquant des concepts abstraits ou difficiles à représenter
            abstract_indicators = [
                "faire", "avoir", "être", "aller", "venir", "devoir", "vouloir",
                "très", "plus", "moins", "beaucoup", "peu", "jamais", "toujours", 
                "peut-être", "comment", "pourquoi", "quand", "où", "combien",
                "quelqu'un", "personne", "tout", "rien", "chaque", "plusieurs",
                "spirituel", "religieux", "traditionnel", "culturel", "social",
                "politique", "économique", "psychologique", "émotionnel",
                "difficulté", "facilité", "rapidité", "lenteur", "beauté", "laideur"
            ]
            
            # Si le mot contient des indicateurs abstraits, le nettoyer
            contains_abstract = any(indicator in french_word for indicator in abstract_indicators)
            
            # Ou si c'est un verbe d'action complexe/mentale
            complex_verbs = ["réfléchir", "méditer", "analyser", "critiquer", "juger", "estimer", "évaluer"]
            is_complex_verb = any(verb in french_word for verb in complex_verbs)
            
            if contains_abstract or is_complex_verb:
                should_remove = True
                reason = "concept abstrait détecté"
            else:
                should_remove = False
                reason = "gardé par défaut (semble approprié)"
        
        if should_remove:
            # Supprimer l'emoji en mettant image_url à vide
            db.words.update_one(
                {"_id": word_id},
                {"$set": {"image_url": ""}}
            )
            print(f"🗑️ {word['french']}: {current_emoji} supprimé ({reason})")
            cleaned_count += 1
        else:
            print(f"✅ {word['french']}: {current_emoji} gardé ({reason})")
            kept_count += 1
    
    print(f"\n📊 RÉSULTAT DU NETTOYAGE:")
    print(f"  🗑️ Emojis supprimés: {cleaned_count}")
    print(f"  ✅ Emojis gardés: {kept_count}")
    print(f"  📈 Total traité: {len(words_with_emojis)}")
    
    return cleaned_count

def verify_cleaning(db):
    """Vérifier le résultat du nettoyage"""
    
    print("\n🔍 VÉRIFICATION DU NETTOYAGE...")
    
    # Compter les mots avec et sans emojis
    words_with_emojis = db.words.count_documents({"emoji": {"$ne": ""}})
    words_without_emojis = db.words.count_documents({"emoji": ""})
    total_words = db.words.count_documents({})
    
    print(f"📊 STATISTIQUES FINALES:")
    print(f"  ✅ Mots avec emojis appropriés: {words_with_emojis}")
    print(f"  🚫 Mots sans emoji: {words_without_emojis}")
    print(f"  📈 Total des mots: {total_words}")
    
    # Afficher quelques exemples de mots gardés avec emojis
    print(f"\n✅ EXEMPLES DE MOTS AVEC EMOJIS GARDÉS:")
    examples_with_emojis = list(db.words.find({"emoji": {"$ne": ""}}).limit(10))
    
    for example in examples_with_emojis:
        print(f"  {example.get('french', '')}: {example.get('emoji', '')} (approprié)")
    
    # Afficher quelques exemples de mots nettoyés
    print(f"\n🧹 EXEMPLES DE MOTS NETTOYÉS (sans emoji):")
    examples_without_emojis = list(db.words.find({
        "emoji": "",
        "french": {"$in": ["pénis", "testicules", "vagin", "respect", "secret"]}
    }).limit(5))
    
    for example in examples_without_emojis:
        print(f"  {example.get('french', '')}: (emoji supprimé - approprié)")
    
    print(f"\n✅ Nettoyage terminé - Seuls les emojis avec signification exacte sont conservés")

def main():
    """Fonction principale"""
    print("=" * 80)
    print("🧹 NETTOYAGE DES EMOJIS INAPPROPRIÉS OU FLOUS")
    print("=" * 80)
    print("Principe: Supprimer tous les emojis dont la signification n'est pas EXACTE")
    print("=" * 80)
    
    # Connexion MongoDB
    client = get_mongo_client()
    if not client:
        return False
    
    db = client[DB_NAME]
    
    try:
        # Nettoyer les emojis inappropriés
        cleaned_count = clean_inappropriate_emojis(db)
        
        # Vérifier le résultat
        verify_cleaning(db)
        
        if cleaned_count > 0:
            print("\n" + "=" * 80)
            print("✅ NETTOYAGE RÉUSSI !")
            print(f"🧹 {cleaned_count} emojis inappropriés supprimés")
            print("✅ Seuls les emojis avec signification EXACTE sont conservés")
            print("🎯 Principe respecté: pas d'emoji si pas de représentation exacte")
            print("=" * 80)
        else:
            print("\n✅ Aucun emoji inapproprié trouvé - base déjà propre")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False
    
    finally:
        client.close()

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SUCCESS! EMOJIS CLEANED!")
    else:
        print("\n💥 FAILURE! CLEANING FAILED!")
    
    exit(0 if success else 1)