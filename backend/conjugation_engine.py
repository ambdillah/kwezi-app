#!/usr/bin/env python3
"""
MOTEUR DE CONJUGAISON CORRIGÉ pour SHIMAORÉ et KIBOUCHI
Version complète avec conjugaison française correcte
"""

import uuid
from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
import os

def get_database():
    """Connexion à la base de données"""
    MONGO_URL = os.getenv('MONGO_URL')
    DB_NAME = os.getenv('DB_NAME', 'mayotte_app')
    client = MongoClient(MONGO_URL)
    return client[DB_NAME]

class ConjugationEngine:
    def __init__(self):
        # Conjugaisons shimaoré (préfixes selon pronoms et temps)
        # Règles: supprimer "ou" ou "w" de l'infinitif et ajouter le préfixe
        self.shimaore_conjugation = {
            'present': {
                'je': 'nis',      # nisrenga = je parle
                'tu': 'ous',      # ousrenga = tu parles
                'il': 'as',       # asrenga = il parle
                'elle': 'as',     # asrenga = elle parle
                'nous': 'ris',    # risrenga = nous parlons
                'vous': 'mous',   # mousrenga = vous parlez
                'ils': 'was',     # wasrenga = ils parlent
                'elles': 'was'    # wasrenga = elles parlent
            },
            'past': {
                'je': 'naco',     # nacorenga = j'ai parlé
                'tu': 'waco',     # wacorenga = tu as parlé
                'il': 'aco',      # acorenga = il a parlé
                'elle': 'aco',    # acorenga = elle a parlé
                'nous': 'raco',   # racorenga = nous avons parlé
                'vous': 'moico',  # moicorenga = vous avez parlé (CORRIGÉ)
                'ils': 'waco',    # wacorenga = ils ont parlé
                'elles': 'waco'   # wacorenga = elles ont parlé
            },
            'future': {
                'je': 'nitso',    # nitsorenga = je parlerai
                'tu': 'outso',    # outsorenga = tu parleras
                'il': 'atso',     # atsorenga = il parlera
                'elle': 'atso',   # atsorenga = elle parlera
                'nous': 'ritso',  # ritsorenga = nous parlerons
                'vous': 'moutso', # moutsorenga = vous parlerez
                'ils': 'watso',   # watsorenga = ils parleront
                'elles': 'watso'  # watsorenga = elles parleront
            }
        }
        
        # Conjugaisons kibouchi
        # Règles: Présent = supprimer "m", Passé = remplacer "m" par "n", Futur = remplacer "m" par "Mbou"
        self.kibouchi_pronouns = {
            'je': 'zahou',
            'tu': 'anaou', 
            'il': 'izi',
            'elle': 'izi',
            'nous': 'zéhèyi',   # CORRIGÉ: zéhèyi au lieu de atsika
            'vous': 'anaréou',
            'ils': 'réou',
            'elles': 'réou'
        }
        
        # Pronoms personnels en shimaoré et kibouchi
        self.pronouns = {
            'shimaore': {
                'je': 'wami',
                'tu': 'wawé',      # CORRIGÉ: avec accent
                'il': 'wayé',      # CORRIGÉ: avec accent
                'elle': 'wayé',
                'nous': 'wasi',    # CORRIGÉ: wasi (pas wassi)
                'vous': 'wagnou',
                'ils': 'wawo',
                'elles': 'wawo'
            },
            'kibouchi': {
                'je': 'zahou',
                'tu': 'anaou',
                'il': 'izi', 
                'elle': 'izi',
                'nous': 'zéhèyi',  # CORRIGÉ: zéhèyi (pas atsika)
                'vous': 'anaréou',
                'ils': 'réou',
                'elles': 'réou'
            }
        }
        
        # DICTIONNAIRE COMPLET DE CONJUGAISONS FRANÇAISES
        self.french_conjugation = {
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
                    'aimer': "j'aime"
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
                    'aimer': 'tu aimes'
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
                    'aimer': 'il aime'
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
                    'aimer': 'nous aimons'
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
                    'aimer': 'vous aimez'
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
                    'aimer': 'ils aiment'
                }
            }
        }
    
    def get_shimaore_radical(self, infinitive):
        """
        Extrait le radical d'un verbe shimaoré
        Règle: Supprimer 'ou' ou 'w' au début de l'infinitif
        """
        infinitive_lower = infinitive.lower()
        
        # Enlever 'ou' au début
        if infinitive_lower.startswith('ou'):
            return infinitive[2:]
        
        # Enlever 'w' au début si pas de 'ou'
        if infinitive_lower.startswith('w'):
            return infinitive[1:]
        
        return infinitive
    
    def get_kibouchi_radical(self, infinitive):
        """
        Extrait le radical d'un verbe kibouchi
        Règle: Supprimer uniquement le 'm' au début de l'infinitif
        """
        if infinitive.lower().startswith('m'):
            return infinitive[1:]
        
        return infinitive
    
    def conjugate_shimaore(self, infinitive, pronoun, tense='present'):
        """Conjugue un verbe shimaoré"""
        radical = self.get_shimaore_radical(infinitive)
        
        if tense in self.shimaore_conjugation and pronoun in self.shimaore_conjugation[tense]:
            prefix = self.shimaore_conjugation[tense][pronoun]
            return prefix + radical
        
        return infinitive  # Retour par défaut
    
    def conjugate_kibouchi_past(self, verb):
        """
        Règle kibouchi PASSÉ: remplacer le 'm' initial par 'n'
        Si pas de 'm' initial, ajouter 'n' devant
        """
        if verb.startswith('m') or verb.startswith('M'):
            return 'n' + verb[1:]
        else:
            return 'n' + verb
    
    def conjugate_kibouchi_future(self, verb):
        """
        Règle kibouchi FUTUR: remplacer le 'm' initial par 'Mbou'
        """
        if verb.startswith('m') or verb.startswith('M'):
            return 'Mbou' + verb[1:]
        else:
            return 'Mbou' + verb
    
    def conjugate_kibouchi(self, infinitive, pronoun, tense='present'):
        """
        Conjugue un verbe kibouchi selon les règles:
        - PRÉSENT: supprimer le 'm' du verbe
        - PASSÉ: remplacer 'm' par 'n'
        - FUTUR: remplacer 'm' par 'Mbou'
        """
        pronoun_kibouchi = self.kibouchi_pronouns.get(pronoun, pronoun)
        
        if tense == 'present':
            # Supprimer le 'm' initial
            verb_conjugated = self.get_kibouchi_radical(infinitive)
            return f"{pronoun_kibouchi} {verb_conjugated}"
        
        elif tense == 'past':
            # Remplacer 'm' par 'n'
            past_verb = self.conjugate_kibouchi_past(infinitive)
            return f"{pronoun_kibouchi} {past_verb}"
        
        elif tense == 'future':
            # Remplacer 'm' par 'Mbou'
            future_verb = self.conjugate_kibouchi_future(infinitive)
            return f"{pronoun_kibouchi} {future_verb}"
        
        return f"{pronoun_kibouchi} {infinitive}"  # Retour par défaut
    
    def conjugate_french(self, verb_fr, pronoun, tense='present'):
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
        return f"{pronoun} {verb_normalized}"
    
    def create_sentence(self, subject_fr, verb_fr, verb_shimaore, verb_kibouchi, object_fr=None, object_shimaore=None, object_kibouchi=None, tense='present'):
        """Crée une phrase complète en français, shimaoré et kibouchi"""
        
        # Conjugaison française correcte
        french_conjugated = self.conjugate_french(verb_fr, subject_fr.lower(), tense)
        
        # Conjugaison shimaoré et kibouchi
        shimaore_verb = self.conjugate_shimaore(verb_shimaore, subject_fr.lower(), tense)
        kibouchi_verb = self.conjugate_kibouchi(verb_kibouchi, subject_fr.lower(), tense)
        
        # Pronoms pour shimaoré et kibouchi
        shimaore_pronoun = self.pronouns['shimaore'].get(subject_fr.lower(), subject_fr)
        kibouchi_pronoun = self.pronouns['kibouchi'].get(subject_fr.lower(), subject_fr)
        
        # Construction des phrases
        french_sentence = french_conjugated
        shimaore_sentence = f"{shimaore_pronoun} {shimaore_verb}"
        kibouchi_sentence = f"{kibouchi_pronoun} {kibouchi_verb}"
        
        # Ajouter l'objet si présent
        if object_fr and object_shimaore and object_kibouchi:
            french_sentence += f" {object_fr}"
            shimaore_sentence += f" {object_shimaore}"
            kibouchi_sentence += f" {object_kibouchi}"
        
        return {
            'french': french_sentence,
            'shimaore': shimaore_sentence,
            'kibouchi': kibouchi_sentence,
            'tense': tense,
            'words': {
                'shimaore': shimaore_sentence.split(),
                'kibouchi': kibouchi_sentence.split()
            }
        }

def get_available_verbs():
    """Récupère les verbes disponibles dans la base de données"""
    db = get_database()
    verbs = list(db.words.find({"category": "verbes"}))
    
    return verbs

def create_sentence_database():
    """Crée une base de données de phrases conjuguées correctement"""
    print("🏗️ Création de la base de données de phrases avec conjugaison correcte...")
    
    db = get_database()
    sentences_collection = db.sentences
    
    # Supprimer toutes les phrases existantes
    sentences_collection.delete_many({})
    
    # Obtenir les verbes
    verbs = get_available_verbs()
    if not verbs:
        print("❌ Aucun verbe trouvé dans la base de données")
        return 0
    
    print(f"📝 {len(verbs)} verbes trouvés")
    
    # Moteur de conjugaison
    engine = ConjugationEngine()
    
    sentences_to_insert = []
    pronouns = ['je', 'tu', 'il', 'nous', 'vous', 'ils']
    tenses = ['present']  # Commencer par le présent
    
    # Créer des phrases simples (sujet + verbe)
    for verb in verbs[:10]:  # Limiter à 10 verbes pour commencer
        for pronoun in pronouns:
            for tense in tenses:
                try:
                    # Phrase sans objet
                    sentence = engine.create_sentence(
                        subject_fr=pronoun,
                        verb_fr=verb['french'],
                        verb_shimaore=verb['shimaore'],
                        verb_kibouchi=verb.get('kibouchi', ''),
                        tense=tense
                    )
                    
                    sentence_doc = {
                        'id': str(uuid.uuid4()),
                        'type': 'simple_corrected',
                        'difficulty': 1,
                        'french': sentence['french'],
                        'shimaore': sentence['shimaore'],
                        'kibouchi': sentence['kibouchi'],
                        'tense': tense,
                        'shimaore_words': sentence['words']['shimaore'],
                        'kibouchi_words': sentence['words']['kibouchi']
                    }
                    sentences_to_insert.append(sentence_doc)
                except Exception as e:
                    print(f"⚠️ Erreur pour {verb['french']} + {pronoun}: {str(e)}")
    
    # Insérer dans la base de données
    if sentences_to_insert:
        sentences_collection.insert_many(sentences_to_insert)
        print(f"✅ {len(sentences_to_insert)} phrases créées avec conjugaison correcte")
    
    return len(sentences_to_insert)

def test_conjugation():
    """Test du moteur de conjugaison"""
    print("🧪 Test du moteur de conjugaison corrigé...")
    
    engine = ConjugationEngine()
    
    # Test français
    print("\n--- FRANÇAIS ---")
    test_cases = [
        ('parler', 'je', 'present'),
        ('manger', 'tu', 'present'), 
        ('jouer', 'il', 'present'),
        ('marcher', 'nous', 'present'),
        ('courir', 'vous', 'present'),
        ('dormir', 'ils', 'present')
    ]
    
    for verb, pronoun, tense in test_cases:
        conjugated = engine.conjugate_french(verb, pronoun, tense)
        print(f"{verb} + {pronoun} ({tense}): {conjugated}")
    
    # Test shimaoré
    print("\n--- SHIMAORÉ ---")
    print("Verbe: ourenga (parler)")
    for pronoun in ['je', 'tu', 'il', 'nous']:
        for tense in ['present', 'past', 'future']:
            conjugated = engine.conjugate_shimaore('ourenga', pronoun, tense)
            shimaoré_pronoun = engine.pronouns['shimaore'][pronoun]
            print(f"{pronoun} ({tense}): {shimaoré_pronoun} {conjugated}")

def main():
    """Fonction principale pour tester"""
    print("🔧 TEST DU MOTEUR DE CONJUGAISON CORRIGÉ")
    print("=" * 50)
    
    # Test de conjugaison
    test_conjugation()
    
    # Création de la base de phrases (si demandé)
    # sentences_count = create_sentence_database()
    # print(f"\n✅ {sentences_count} phrases créées")

if __name__ == "__main__":
    main()