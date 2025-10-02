#!/usr/bin/env python3
"""
Script pour régénérer toutes les phrases avec les règles de conjugaison CORRIGÉES
- Shimaoré : préfixes selon pronoms et temps
- Kibouchi : suppression/remplacement du 'm'
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

# Connexion à la base de données
MONGO_URL = os.getenv('MONGO_URL')
DB_NAME = os.getenv('DB_NAME', 'mayotte_app')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Collections
words_collection = db.words
sentences_collection = db.sentences

# Règles de conjugaison CORRIGÉES
SHIMAORE_PREFIXES = {
    'present': {
        'je': 'nis', 'tu': 'ous', 'il': 'as', 'elle': 'as',
        'nous': 'ris', 'vous': 'mous', 'ils': 'was', 'elles': 'was'
    },
    'past': {
        'je': 'naco', 'tu': 'waco', 'il': 'aco', 'elle': 'aco',
        'nous': 'raco', 'vous': 'moico', 'ils': 'waco', 'elles': 'waco'
    },
    'future': {
        'je': 'nitso', 'tu': 'outso', 'il': 'atso', 'elle': 'atso',
        'nous': 'ritso', 'vous': 'moutso', 'ils': 'watso', 'elles': 'watso'
    }
}

PRONOUNS = {
    'shimaore': {
        'je': 'wami', 'tu': 'wawé', 'il': 'wayé', 'elle': 'wayé',
        'nous': 'wasi', 'vous': 'wagnou', 'ils': 'wawo', 'elles': 'wawo'
    },
    'kibouchi': {
        'je': 'zahou', 'tu': 'anaou', 'il': 'izi', 'elle': 'izi',
        'nous': 'zéhèyi', 'vous': 'anaréou', 'ils': 'réou', 'elles': 'réou'
    }
}

# Conjugaisons françaises complètes
FRENCH_CONJUGATIONS = {
    'present': {
        'je': {
            'parler': 'je parle', 'manger': 'je mange', 'jouer': 'je joue',
            'avoir': "j'ai", 'être': 'je suis', 'aller': 'je vais', 'faire': 'je fais',
            'abîmer': "j'abîme", 'acheter': "j'achète", 'aider': "j'aide", 'aimer': "j'aime"
        },
        'tu': {
            'parler': 'tu parles', 'manger': 'tu manges', 'jouer': 'tu joues',
            'avoir': 'tu as', 'être': 'tu es', 'aller': 'tu vas', 'faire': 'tu fais',
            'abîmer': 'tu abîmes', 'acheter': 'tu achètes', 'aider': 'tu aides', 'aimer': 'tu aimes'
        },
        'il': {
            'parler': 'il parle', 'manger': 'il mange', 'jouer': 'il joue',
            'avoir': 'il a', 'être': 'il est', 'aller': 'il va', 'faire': 'il fait',
            'abîmer': 'il abîme', 'acheter': 'il achète', 'aider': 'il aide', 'aimer': 'il aime'
        },
        'nous': {
            'parler': 'nous parlons', 'manger': 'nous mangeons', 'jouer': 'nous jouons',
            'avoir': 'nous avons', 'être': 'nous sommes', 'aller': 'nous allons', 'faire': 'nous faisons',
            'abîmer': 'nous abîmons', 'acheter': 'nous achetons', 'aider': 'nous aidons', 'aimer': 'nous aimons'
        },
        'vous': {
            'parler': 'vous parlez', 'manger': 'vous mangez', 'jouer': 'vous jouez',
            'avoir': 'vous avez', 'être': 'vous êtes', 'aller': 'vous allez', 'faire': 'vous faites',
            'abîmer': 'vous abîmez', 'acheter': 'vous achetez', 'aider': 'vous aidez', 'aimer': 'vous aimez'
        },
        'ils': {
            'parler': 'ils parlent', 'manger': 'ils mangent', 'jouer': 'ils jouent',
            'avoir': 'ils ont', 'être': 'ils sont', 'aller': 'ils vont', 'faire': 'ils font',
            'abîmer': 'ils abîment', 'acheter': 'ils achètent', 'aider': 'ils aident', 'aimer': 'ils aiment'
        }
    }
}

def get_shimaore_radical(verb):
    """Enlève 'ou' ou 'w' au début du verbe shimaoré"""
    verb_lower = verb.lower()
    if verb_lower.startswith('ou'):
        return verb[2:]
    if verb_lower.startswith('w'):
        return verb[1:]
    return verb

def get_kibouchi_radical(verb):
    """Enlève 'm' au début du verbe kibouchi"""
    if verb.lower().startswith('m'):
        return verb[1:]
    return verb

def conjugate_shimaore(verb, pronoun, tense='present'):
    """Conjugue un verbe shimaoré"""
    radical = get_shimaore_radical(verb)
    prefix = SHIMAORE_PREFIXES.get(tense, {}).get(pronoun, '')
    pronoun_shimaore = PRONOUNS['shimaore'].get(pronoun, pronoun)
    
    conjugated_verb = prefix + radical
    return f"{pronoun_shimaore} {conjugated_verb}"

def conjugate_kibouchi(verb, pronoun, tense='present'):
    """Conjugue un verbe kibouchi selon les règles"""
    pronoun_kibouchi = PRONOUNS['kibouchi'].get(pronoun, pronoun)
    
    if tense == 'present':
        # Supprimer le 'm'
        radical = get_kibouchi_radical(verb)
        return f"{pronoun_kibouchi} {radical}"
    
    elif tense == 'past':
        # Remplacer 'm' par 'n'
        if verb.lower().startswith('m'):
            conjugated = 'n' + verb[1:]
        else:
            conjugated = 'n' + verb
        return f"{pronoun_kibouchi} {conjugated}"
    
    elif tense == 'future':
        # Remplacer 'm' par 'Mbou'
        if verb.lower().startswith('m'):
            conjugated = 'Mbou' + verb[1:]
        else:
            conjugated = 'Mbou' + verb
        return f"{pronoun_kibouchi} {conjugated}"
    
    return f"{pronoun_kibouchi} {verb}"

def conjugate_french(verb, pronoun, tense='present'):
    """Conjugue un verbe français"""
    verb_lower = verb.lower()
    
    # Chercher dans le dictionnaire
    if tense in FRENCH_CONJUGATIONS:
        if pronoun in FRENCH_CONJUGATIONS[tense]:
            if verb_lower in FRENCH_CONJUGATIONS[tense][pronoun]:
                return FRENCH_CONJUGATIONS[tense][pronoun][verb_lower]
    
    # Conjugaison automatique pour verbes réguliers en -er
    if verb_lower.endswith('er') and tense == 'present':
        radical = verb_lower[:-2]
        endings = {'je': 'e', 'tu': 'es', 'il': 'e', 'nous': 'ons', 'vous': 'ez', 'ils': 'ent'}
        if pronoun in endings:
            # Gestion de l'élision avec 'je'
            if pronoun == 'je' and radical[0] in 'aeiouhéè':
                return f"j'{radical}{endings[pronoun]}"
            return f"{pronoun} {radical}{endings[pronoun]}"
    
    return f"{pronoun} {verb_lower}"

def regenerate_all_sentences():
    """Régénère toutes les phrases avec les bonnes règles"""
    print("🔄 Régénération des phrases avec règles corrigées...")
    print("=" * 60)
    
    # Récupérer tous les verbes
    verbs = list(words_collection.find({"category": "verbes"}))
    print(f"📚 {len(verbs)} verbes trouvés")
    
    # Supprimer toutes les anciennes phrases
    old_count = sentences_collection.count_documents({})
    sentences_collection.delete_many({})
    print(f"🗑️  {old_count} anciennes phrases supprimées")
    
    # Créer les nouvelles phrases
    new_sentences = []
    pronouns = ['je', 'tu', 'il', 'nous', 'vous', 'ils']
    tenses = ['present', 'past', 'future']
    
    for verb in verbs[:15]:  # Limiter à 15 verbes pour commencer
        verb_fr = verb.get('french', '')
        verb_shimaore = verb.get('shimaore', '')
        verb_kibouchi = verb.get('kibouchi', '')
        
        if not verb_fr or not verb_shimaore or not verb_kibouchi:
            continue
        
        for pronoun in pronouns:
            for tense in tenses:
                try:
                    # Conjuguer dans les 3 langues
                    french_conjugated = conjugate_french(verb_fr, pronoun, tense)
                    shimaore_conjugated = conjugate_shimaore(verb_shimaore, pronoun, tense)
                    kibouchi_conjugated = conjugate_kibouchi(verb_kibouchi, pronoun, tense)
                    
                    sentence = {
                        'id': str(uuid.uuid4()),
                        'type': 'conjugated_corrected',
                        'french': french_conjugated,
                        'shimaore': shimaore_conjugated,
                        'kibouchi': kibouchi_conjugated,
                        'tense': tense,
                        'subject': pronoun,
                        'verb_infinitive_fr': verb_fr,
                        'difficulty': 1 if tense == 'present' else 2 if tense == 'past' else 3,
                        'french_words': french_conjugated.split(),
                        'shimaore_words': shimaore_conjugated.split(),
                        'kibouchi_words': kibouchi_conjugated.split()
                    }
                    
                    new_sentences.append(sentence)
                    
                except Exception as e:
                    print(f"⚠️  Erreur: {verb_fr} + {pronoun} ({tense}): {e}")
    
    # Insérer dans la base
    if new_sentences:
        sentences_collection.insert_many(new_sentences)
        print(f"\n✅ {len(new_sentences)} phrases générées avec succès!")
        
        # Afficher quelques exemples
        print("\n📝 Exemples de phrases générées:")
        print("-" * 60)
        for sentence in new_sentences[:6]:
            print(f"Français: {sentence['french']}")
            print(f"Shimaoré: {sentence['shimaore']}")
            print(f"Kibouchi: {sentence['kibouchi']}")
            print(f"Temps: {sentence['tense']}")
            print()
    
    client.close()
    print("✅ Régénération terminée!")

if __name__ == "__main__":
    regenerate_all_sentences()
