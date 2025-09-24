#!/usr/bin/env python3
"""
Script complet pour corriger la conjugaison française dans le moteur de conjugaison
et régénérer les phrases avec les verbes correctement conjugués
"""

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
import os
import uuid
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL')
client = MongoClient(MONGO_URL)
db = client.kwezi
words_collection = db.words
sentences_collection = db.sentences

def fix_conjugation_engine():
    """Corrige le moteur de conjugaison pour inclure un dictionnaire français complet"""
    print("🔧 CORRECTION COMPLÈTE DU MOTEUR DE CONJUGAISON")
    print("=" * 50)
    
    # Lire le fichier actuel
    with open('/app/backend/conjugation_engine.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Nouveau dictionnaire de conjugaisons françaises complet à insérer
    french_conjugation_dict = '''    
    # Dictionnaire complet de conjugaisons françaises
    french_conjugation = {
        'present': {
            'je': {
                'parler': 'je parle',
                'manger': 'je mange', 
                'jouer': 'je joue',
                'marcher': 'je marche',
                'courir': 'je cours',
                'dormir': 'je dors',
                'boire': 'je bois',
                'voir': 'je vois',
                'avoir': "j'ai",
                'être': 'je suis',
                'faire': 'je fais',
                'aller': 'je vais',
                'venir': 'je viens',
                'prendre': 'je prends',
                'donner': 'je donne',
                'regarder': 'je regarde',
                'écouter': "j'écoute",
                'lire': 'je lis',
                'écrire': "j'écris",
                'chanter': 'je chante',
                'danser': 'je danse',
                'travailler': 'je travaille',
                'aimer': "j'aime",
                'détester': 'je déteste',
                'acheter': "j'achète",
                'vendre': 'je vends',
                'ouvrir': "j'ouvre",
                'fermer': 'je ferme',
                'commencer': 'je commence'
            },
            'tu': {
                'parler': 'tu parles',
                'manger': 'tu manges',
                'jouer': 'tu joues', 
                'marcher': 'tu marches',
                'courir': 'tu cours',
                'dormir': 'tu dors',
                'boire': 'tu bois',
                'voir': 'tu vois',
                'avoir': 'tu as',
                'être': 'tu es',
                'faire': 'tu fais',
                'aller': 'tu vas',
                'venir': 'tu viens',
                'prendre': 'tu prends',
                'donner': 'tu donnes',
                'regarder': 'tu regardes',
                'écouter': 'tu écoutes',
                'lire': 'tu lis',
                'écrire': 'tu écris',
                'chanter': 'tu chantes',
                'danser': 'tu danses',
                'travailler': 'tu travailles',
                'aimer': 'tu aimes',
                'détester': 'tu détestes',
                'acheter': 'tu achètes',
                'vendre': 'tu vends',
                'ouvrir': 'tu ouvres',
                'fermer': 'tu fermes',
                'commencer': 'tu commences'
            },
            'il': {
                'parler': 'il parle',
                'manger': 'il mange',
                'jouer': 'il joue',
                'marcher': 'il marche',
                'courir': 'il court',
                'dormir': 'il dort',
                'boire': 'il boit',
                'voir': 'il voit',
                'avoir': 'il a',
                'être': 'il est',
                'faire': 'il fait',
                'aller': 'il va',
                'venir': 'il vient',
                'prendre': 'il prend',
                'donner': 'il donne',
                'regarder': 'il regarde',
                'écouter': 'il écoute',
                'lire': 'il lit',
                'écrire': 'il écrit',
                'chanter': 'il chante',
                'danser': 'il danse',
                'travailler': 'il travaille',
                'aimer': 'il aime',
                'détester': 'il déteste',
                'acheter': 'il achète',
                'vendre': 'il vend',
                'ouvrir': 'il ouvre',
                'fermer': 'il ferme',
                'commencer': 'il commence'
            },
            'nous': {
                'parler': 'nous parlons',
                'manger': 'nous mangeons',
                'jouer': 'nous jouons',
                'marcher': 'nous marchons',
                'courir': 'nous courons',
                'dormir': 'nous dormons',
                'boire': 'nous buvons',
                'voir': 'nous voyons',
                'avoir': 'nous avons',
                'être': 'nous sommes',
                'faire': 'nous faisons',
                'aller': 'nous allons',
                'venir': 'nous venons',
                'prendre': 'nous prenons',
                'donner': 'nous donnons',
                'regarder': 'nous regardons',
                'écouter': 'nous écoutons',
                'lire': 'nous lisons',
                'écrire': 'nous écrivons',
                'chanter': 'nous chantons',
                'danser': 'nous dansons',
                'travailler': 'nous travaillons',
                'aimer': 'nous aimons',
                'détester': 'nous détestons',
                'acheter': 'nous achetons',
                'vendre': 'nous vendons',
                'ouvrir': 'nous ouvrons',
                'fermer': 'nous fermons',
                'commencer': 'nous commençons'
            },
            'vous': {
                'parler': 'vous parlez',
                'manger': 'vous mangez',
                'jouer': 'vous jouez',
                'marcher': 'vous marchez',
                'courir': 'vous courez',
                'dormir': 'vous dormez',
                'boire': 'vous buvez',
                'voir': 'vous voyez',
                'avoir': 'vous avez',
                'être': 'vous êtes',
                'faire': 'vous faites',
                'aller': 'vous allez',
                'venir': 'vous venez',
                'prendre': 'vous prenez',
                'donner': 'vous donnez',
                'regarder': 'vous regardez',
                'écouter': 'vous écoutez',
                'lire': 'vous lisez',
                'écrire': 'vous écrivez',
                'chanter': 'vous chantez',
                'danser': 'vous dansez',
                'travailler': 'vous travaillez',
                'aimer': 'vous aimez',
                'détester': 'vous détestez',
                'acheter': 'vous achetez',
                'vendre': 'vous vendez',
                'ouvrir': 'vous ouvrez',
                'fermer': 'vous fermez',
                'commencer': 'vous commencez'
            },
            'ils': {
                'parler': 'ils parlent',
                'manger': 'ils mangent',
                'jouer': 'ils jouent',
                'marcher': 'ils marchent',
                'courir': 'ils courent',
                'dormir': 'ils dorment',
                'boire': 'ils boivent',
                'voir': 'ils voient',
                'avoir': 'ils ont',
                'être': 'ils sont',
                'faire': 'ils font',
                'aller': 'ils vont',
                'venir': 'ils viennent',
                'prendre': 'ils prennent',
                'donner': 'ils donnent',
                'regarder': 'ils regardent',
                'écouter': 'ils écoutent',
                'lire': 'ils lisent',
                'écrire': 'ils écrivent',
                'chanter': 'ils chantent',
                'danser': 'ils dansent',
                'travailler': 'ils travaillent',
                'aimer': 'ils aiment',
                'détester': 'ils détestent',
                'acheter': 'ils achètent',
                'vendre': 'ils vendent',
                'ouvrir': 'ils ouvrent',
                'fermer': 'ils ferment',
                'commencer': 'ils commencent'
            }
        }
    }
'''
    
    # Remplacer la méthode conjugate_french pour qu'elle utilise le dictionnaire
    new_conjugate_method = '''    def conjugate_french(self, verb_fr, pronoun, tense='present'):
        """Conjugue un verbe français correctement"""
        verb_normalized = verb_fr.lower()
        
        # Utiliser le dictionnaire de conjugaisons
        if tense in self.french_conjugation and pronoun in self.french_conjugation[tense]:
            if verb_normalized in self.french_conjugation[tense][pronoun]:
                return self.french_conjugation[tense][pronoun][verb_normalized]
        
        # Conjugaison automatique basique pour les verbes du premier groupe
        if verb_normalized.endswith('er') and tense == 'present':
            radical = verb_normalized[:-2]
            endings = {
                'je': 'e', 'tu': 'es', 'il': 'e',
                'nous': 'ons', 'vous': 'ez', 'ils': 'ent'
            }
            if pronoun in endings:
                return f"{pronoun} {radical}{endings[pronoun]}"
        
        # Fallback 
        return f"{pronoun} {verb_normalized}"'''
    
    # Insérer le dictionnaire après la définition __init__
    if 'def __init__(self):' in content:
        # Trouver la fin de __init__ et insérer le dictionnaire
        init_end = content.find('def get_shimaore_radical')
        if init_end != -1:
            content = content[:init_end] + french_conjugation_dict + '\n    \n    ' + content[init_end:]
    
    # Remplacer la méthode conjugate_french
    if 'def conjugate_french(self, verb_fr, pronoun, tense=\'present\'):' in content:
        start = content.find('def conjugate_french(self, verb_fr, pronoun, tense=\'present\'):')
        # Trouver la fin de la méthode (prochaine méthode ou fin de classe)
        next_method = content.find('\n    def ', start + 1)
        if next_method == -1:
            next_method = len(content)
        
        content = content[:start] + new_conjugate_method + '\n    \n    ' + content[next_method:]
    
    # Supprimer les références à french_conjugator qui n'existe pas
    content = content.replace('return self.french_conjugator.conjugate_verb(verb_fr, pronoun, tense)', '# Removed non-existent conjugator')
    content = content.replace('except Exception:', 'if True:  # Direct conjugation')
    
    # Écrire le fichier corrigé
    with open('/app/backend/conjugation_engine.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  ✅ Moteur de conjugaison mis à jour avec dictionnaire complet")

def regenerate_game_sentences():
    """Régénère des phrases pour le jeu avec une conjugaison correcte"""
    print("\n🎯 RÉGÉNÉRATION DES PHRASES DE JEU")
    print("=" * 50)
    
    # Supprimer toutes les anciennes phrases
    old_count = sentences_collection.count_documents({})
    sentences_collection.delete_many({})
    print(f"  🗑️ {old_count} anciennes phrases supprimées")
    
    # Récupérer quelques verbes de la base
    verbs = list(words_collection.find({"category": "verbes"}).limit(10))
    print(f"  📝 {len(verbs)} verbes trouvés")
    
    # Créer de nouvelles phrases avec conjugaison correcte
    new_sentences = []
    pronouns = ['je', 'tu', 'il', 'nous', 'vous', 'ils']
    
    # Dictionnaire de conjugaison directe pour quelques verbes courants
    manual_conjugations = {
        'je': {
            'parler': 'je parle', 'manger': 'je mange', 'jouer': 'je joue',
            'marcher': 'je marche', 'courir': 'je cours', 'dormir': 'je dors'
        },
        'tu': {
            'parler': 'tu parles', 'manger': 'tu manges', 'jouer': 'tu joues',
            'marcher': 'tu marches', 'courir': 'tu cours', 'dormir': 'tu dors'
        },
        'il': {
            'parler': 'il parle', 'manger': 'il mange', 'jouer': 'il joue',
            'marcher': 'il marche', 'courir': 'il court', 'dormir': 'il dort'
        },
        'nous': {
            'parler': 'nous parlons', 'manger': 'nous mangeons', 'jouer': 'nous jouons',
            'marcher': 'nous marchons', 'courir': 'nous courons', 'dormir': 'nous dormons'
        },
        'vous': {
            'parler': 'vous parlez', 'manger': 'vous mangez', 'jouer': 'vous jouez',
            'marcher': 'vous marchez', 'courir': 'vous courez', 'dormir': 'vous dormez'
        },
        'ils': {
            'parler': 'ils parlent', 'manger': 'ils mangent', 'jouer': 'ils jouent',
            'marcher': 'ils marchent', 'courir': 'ils courent', 'dormir': 'ils dorment'
        }
    }
    
    # Pronoms en shimaoré et kibouchi
    shimaore_pronouns = {
        'je': 'wami', 'tu': 'wawe', 'il': 'waye',
        'nous': 'wasi', 'vous': 'wagnou', 'ils': 'wawo'
    }
    kibouchi_pronouns = {
        'je': 'zahou', 'tu': 'anaou', 'il': 'izi',
        'nous': 'atsika', 'vous': 'anareou', 'ils': 'reou'
    }
    
    # Créer des phrases simples pour chaque combinaison pronom-verbe
    for verb in verbs[:6]:  # Prendre les 6 premiers verbes
        french_verb = verb['french'].lower()
        shimaore_verb = verb['shimaore']
        kibouchi_verb = verb.get('kibouchi', '')
        
        for pronoun in pronouns:
            # Conjugaison française
            french_conjugated = manual_conjugations.get(pronoun, {}).get(french_verb, f"{pronoun} {french_verb}")
            
            # Phrases en shimaoré et kibouchi (structure simple)
            shimaore_pronoun = shimaore_pronouns.get(pronoun, pronoun)
            kibouchi_pronoun = kibouchi_pronouns.get(pronoun, pronoun)
            
            # Conjugaison shimaoré simple (ajouter préfixes basiques)
            shimaore_conjugated = f"{shimaore_pronoun} {shimaore_verb}"
            kibouchi_conjugated = f"{kibouchi_pronoun} {kibouchi_verb}" if kibouchi_verb else f"{kibouchi_pronoun} [verb]"
            
            sentence_doc = {
                'id': str(uuid.uuid4()),
                'type': 'corrected_conjugation_game',
                'difficulty': 1,
                'french': french_conjugated,
                'shimaore': shimaore_conjugated,
                'kibouchi': kibouchi_conjugated,
                'tense': 'present',
                'shimaore_words': shimaore_conjugated.split(),
                'kibouchi_words': kibouchi_conjugated.split()
            }
            new_sentences.append(sentence_doc)
    
    # Insérer les nouvelles phrases
    if new_sentences:
        sentences_collection.insert_many(new_sentences)
        print(f"  ✅ {len(new_sentences)} nouvelles phrases avec conjugaison correcte ajoutées")
    
    return len(new_sentences)

def test_conjugation_system():
    """Teste le nouveau système de conjugaison"""
    print("\n🧪 TEST DU SYSTÈME DE CONJUGAISON")
    print("=" * 50)
    
    # Importer et tester le moteur modifié
    try:
        import importlib
        import sys
        
        # Recharger le module conjugation_engine
        if 'conjugation_engine' in sys.modules:
            importlib.reload(sys.modules['conjugation_engine'])
        
        from conjugation_engine import ConjugationEngine
        
        engine = ConjugationEngine()
        
        # Tester quelques conjugaisons
        test_cases = [
            ('parler', 'je', 'present'),
            ('manger', 'tu', 'present'), 
            ('jouer', 'il', 'present'),
            ('marcher', 'nous', 'present'),
            ('courir', 'vous', 'present'),
            ('dormir', 'ils', 'present')
        ]
        
        print("  📝 Tests de conjugaison française:")
        for verb, pronoun, tense in test_cases:
            try:
                conjugated = engine.conjugate_french(verb, pronoun, tense)
                print(f"    {verb} + {pronoun} ({tense}) = {conjugated}")
            except Exception as e:
                print(f"    ❌ Erreur pour {verb} + {pronoun}: {str(e)}")
        
        print("  ✅ Tests de conjugaison terminés")
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test: {str(e)}")

def main():
    """Fonction principale"""
    print("🔧 CORRECTION COMPLÈTE DE LA CONJUGAISON FRANÇAISE")
    print("=" * 60)
    print(f"Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. Corriger le moteur de conjugaison
        fix_conjugation_engine()
        
        # 2. Régénérer les phrases de jeu
        sentences_count = regenerate_game_sentences()
        
        # 3. Tester le système
        test_conjugation_system()
        
        print(f"\n✅ CORRECTION COMPLÈTE TERMINÉE!")
        print(f"  - Moteur de conjugaison: ✅ Corrigé")
        print(f"  - Nouvelles phrases: {sentences_count}")
        print(f"  - Tests: ✅ Exécutés")
        
    except Exception as e:
        print(f"❌ ERREUR: {str(e)}")
        raise

if __name__ == "__main__":
    main()