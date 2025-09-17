#!/usr/bin/env python3
"""
MOTEUR DE CONJUGAISON SHIMAORÉ ET KIBOUCHI
==========================================
Système de conjugaison automatique basé sur les règles grammaticales
fournies par l'utilisateur.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import uuid
from french_conjugator import FrenchConjugator
from french_conjugator import FrenchConjugator

# Charger les variables d'environnement
load_dotenv()

def get_database():
    """Connexion à la base de données MongoDB"""
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    client = MongoClient(mongo_url)
    db_name = os.getenv('DB_NAME', 'mayotte_app')
    db = client[db_name]
    return db

class ConjugationEngine:
    """Moteur de conjugaison pour shimaoré, kibouchi et français"""
    
    def __init__(self):
        # Initialiser le conjugateur français automatique
        self.french_conjugator = FrenchConjugator()
        
        # Règles de conjugaison française
        self.french_conjugation = {
            'present': {
                'je': {'abîmer': "j'abîme", 'acheter': "j'achète", 'aimer': "j'aime", 'allumer': "j'allume", 
                       'apprendre': "j'apprends", 'arriver': "j'arrive", 'attendre': "j'attends", 'avoir': "j'ai",
                       'balayer': 'je balaie', 'boire': 'je bois', 'chercher': 'je cherche', 'comprendre': 'je comprends',
                       'couper': 'je coupe', 'courir': 'je cours', 'creuser': 'je creuse', 'cuisiner': 'je cuisine',
                       'cultiver': 'je cultive', 'demander': 'je demande', 'dire': 'je dis', 'donner': 'je donne',
                       'dormir': 'je dors', 'écouter': "j'écoute", 'écrire': "j'écris", 'entrer': "j'entre",
                       'être': 'je suis', 'faire': 'je fais', 'finir': 'je finis', 'jouer': 'je joue',
                       'lire': 'je lis', 'manger': 'je mange', 'marcher': 'je marche', 'parler': 'je parle',
                       'partir': 'je pars', 'planter': 'je plante', 'pouvoir': 'je peux', 'prendre': 'je prends',
                       'ranger': 'je range', 'répondre': 'je réponds', 'rester': 'je reste', 'revenir': 'je reviens',
                       'savoir': 'je sais', 'sortir': 'je sors', 'trouver': 'je trouve', 'venir': 'je viens',
                       'voir': 'je vois', 'vouloir': 'je veux'},
                'tu': {'abîmer': 'tu abîmes', 'acheter': 'tu achètes', 'aimer': 'tu aimes', 'allumer': 'tu allumes',
                       'apprendre': 'tu apprends', 'arriver': 'tu arrives', 'attendre': 'tu attends', 'avoir': 'tu as',
                       'balayer': 'tu balaies', 'boire': 'tu bois', 'chercher': 'tu cherches', 'comprendre': 'tu comprends',
                       'couper': 'tu coupes', 'courir': 'tu cours', 'creuser': 'tu creuses', 'cuisiner': 'tu cuisines',
                       'cultiver': 'tu cultives', 'demander': 'tu demandes', 'dire': 'tu dis', 'donner': 'tu donnes',
                       'dormir': 'tu dors', 'écouter': 'tu écoutes', 'écrire': 'tu écris', 'entrer': 'tu entres',
                       'être': 'tu es', 'faire': 'tu fais', 'finir': 'tu finis', 'jouer': 'tu joues',
                       'lire': 'tu lis', 'manger': 'tu manges', 'marcher': 'tu marches', 'parler': 'tu parles',
                       'partir': 'tu pars', 'planter': 'tu plantes', 'pouvoir': 'tu peux', 'prendre': 'tu prends',
                       'ranger': 'tu ranges', 'répondre': 'tu réponds', 'rester': 'tu restes', 'revenir': 'tu reviens',
                       'savoir': 'tu sais', 'sortir': 'tu sors', 'trouver': 'tu trouves', 'venir': 'tu viens',
                       'voir': 'tu vois', 'vouloir': 'tu veux'},
                'il': {'abîmer': 'il abîme', 'acheter': 'il achète', 'aimer': 'il aime', 'allumer': 'il allume',
                       'apprendre': 'il apprend', 'arriver': 'il arrive', 'attendre': 'il attend', 'avoir': 'il a',
                       'balayer': 'il balaie', 'boire': 'il boit', 'chercher': 'il cherche', 'comprendre': 'il comprend',
                       'couper': 'il coupe', 'courir': 'il court', 'creuser': 'il creuse', 'cuisiner': 'il cuisine',
                       'cultiver': 'il cultive', 'demander': 'il demande', 'dire': 'il dit', 'donner': 'il donne',
                       'dormir': 'il dort', 'écouter': 'il écoute', 'écrire': 'il écrit', 'entrer': 'il entre',
                       'être': 'il est', 'faire': 'il fait', 'finir': 'il finit', 'jouer': 'il joue',
                       'lire': 'il lit', 'manger': 'il mange', 'marcher': 'il marche', 'parler': 'il parle',
                       'partir': 'il part', 'planter': 'il plante', 'pouvoir': 'il peut', 'prendre': 'il prend',
                       'ranger': 'il range', 'répondre': 'il répond', 'rester': 'il reste', 'revenir': 'il revient',
                       'savoir': 'il sait', 'sortir': 'il sort', 'trouver': 'il trouve', 'venir': 'il vient',
                       'voir': 'il voit', 'vouloir': 'il veut'},
                'elle': {'abîmer': 'elle abîme', 'acheter': 'elle achète', 'aimer': 'elle aime', 'allumer': 'elle allume',
                         'apprendre': 'elle apprend', 'arriver': 'elle arrive', 'attendre': 'elle attend', 'avoir': 'elle a',
                         'balayer': 'elle balaie', 'boire': 'elle boit', 'chercher': 'elle cherche', 'comprendre': 'elle comprend',
                         'couper': 'elle coupe', 'courir': 'elle court', 'creuser': 'elle creuse', 'cuisiner': 'elle cuisine',
                         'cultiver': 'elle cultive', 'demander': 'elle demande', 'dire': 'elle dit', 'donner': 'elle donne',
                         'dormir': 'elle dort', 'écouter': 'elle écoute', 'écrire': 'elle écrit', 'entrer': 'elle entre',
                         'être': 'elle est', 'faire': 'elle fait', 'finir': 'elle finit', 'jouer': 'elle joue',
                         'lire': 'elle lit', 'manger': 'elle mange', 'marcher': 'elle marche', 'parler': 'elle parle',
                         'partir': 'elle part', 'planter': 'elle plante', 'pouvoir': 'elle peut', 'prendre': 'elle prend',
                         'ranger': 'elle range', 'répondre': 'elle répond', 'rester': 'elle reste', 'revenir': 'elle revient',
                         'savoir': 'elle sait', 'sortir': 'elle sort', 'trouver': 'elle trouve', 'venir': 'elle vient',
                         'voir': 'elle voit', 'vouloir': 'elle veut'},
                'nous': {'abîmer': 'nous abîmons', 'acheter': 'nous achetons', 'aimer': 'nous aimons', 'allumer': 'nous allumons',
                         'apprendre': 'nous apprenons', 'arriver': 'nous arrivons', 'attendre': 'nous attendons', 'avoir': 'nous avons',
                         'balayer': 'nous balayons', 'boire': 'nous buvons', 'chercher': 'nous cherchons', 'comprendre': 'nous comprenons',
                         'couper': 'nous coupons', 'courir': 'nous courons', 'creuser': 'nous creusons', 'cuisiner': 'nous cuisinons',
                         'cultiver': 'nous cultivons', 'demander': 'nous demandons', 'dire': 'nous disons', 'donner': 'nous donnons',
                         'dormir': 'nous dormons', 'écouter': 'nous écoutons', 'écrire': 'nous écrivons', 'entrer': 'nous entrons',
                         'être': 'nous sommes', 'faire': 'nous faisons', 'finir': 'nous finissons', 'jouer': 'nous jouons',
                         'lire': 'nous lisons', 'manger': 'nous mangeons', 'marcher': 'nous marchons', 'parler': 'nous parlons',
                         'partir': 'nous partons', 'planter': 'nous plantons', 'pouvoir': 'nous pouvons', 'prendre': 'nous prenons',
                         'ranger': 'nous rangeons', 'répondre': 'nous répondons', 'rester': 'nous restons', 'revenir': 'nous revenons',
                         'savoir': 'nous savons', 'sortir': 'nous sortons', 'trouver': 'nous trouvons', 'venir': 'nous venons',
                         'voir': 'nous voyons', 'vouloir': 'nous voulons'},
                'vous': {'abîmer': 'vous abîmez', 'acheter': 'vous achetez', 'aimer': 'vous aimez', 'allumer': 'vous allumez',
                         'apprendre': 'vous apprenez', 'arriver': 'vous arrivez', 'attendre': 'vous attendez', 'avoir': 'vous avez',
                         'balayer': 'vous balayez', 'boire': 'vous buvez', 'chercher': 'vous cherchez', 'comprendre': 'vous comprenez',
                         'couper': 'vous coupez', 'courir': 'vous courez', 'creuser': 'vous creusez', 'cuisiner': 'vous cuisinez',
                         'cultiver': 'vous cultivez', 'demander': 'vous demandez', 'dire': 'vous dites', 'donner': 'vous donnez',
                         'dormir': 'vous dormez', 'écouter': 'vous écoutez', 'écrire': 'vous écrivez', 'entrer': 'vous entrez',
                         'être': 'vous êtes', 'faire': 'vous faites', 'finir': 'vous finissez', 'jouer': 'vous jouez',
                         'lire': 'vous lisez', 'manger': 'vous mangez', 'marcher': 'vous marchez', 'parler': 'vous parlez',
                         'partir': 'vous partez', 'planter': 'vous plantez', 'pouvoir': 'vous pouvez', 'prendre': 'vous prenez',
                         'ranger': 'vous rangez', 'répondre': 'vous répondez', 'rester': 'vous restez', 'revenir': 'vous revenez',
                         'savoir': 'vous savez', 'sortir': 'vous sortez', 'trouver': 'vous trouvez', 'venir': 'vous venez',
                         'voir': 'vous voyez', 'vouloir': 'vous voulez'},
                'ils': {'abîmer': 'ils abîment', 'acheter': 'ils achètent', 'aimer': 'ils aiment', 'allumer': 'ils allument',
                        'apprendre': 'ils apprennent', 'arriver': 'ils arrivent', 'attendre': 'ils attendent', 'avoir': 'ils ont',
                        'balayer': 'ils balaient', 'boire': 'ils boivent', 'chercher': 'ils cherchent', 'comprendre': 'ils comprennent',
                        'couper': 'ils coupent', 'courir': 'ils courent', 'creuser': 'ils creusent', 'cuisiner': 'ils cuisinent',
                        'cultiver': 'ils cultivent', 'demander': 'ils demandent', 'dire': 'ils disent', 'donner': 'ils donnent',
                        'dormir': 'ils dorment', 'écouter': 'ils écoutent', 'écrire': 'ils écrivent', 'entrer': 'ils entrent',
                        'être': 'ils sont', 'faire': 'ils font', 'finir': 'ils finissent', 'jouer': 'ils jouent',
                        'lire': 'ils lisent', 'manger': 'ils mangent', 'marcher': 'ils marchent', 'parler': 'ils parlent',
                        'partir': 'ils partent', 'planter': 'ils plantent', 'pouvoir': 'ils peuvent', 'prendre': 'ils prennent',
                        'ranger': 'ils rangent', 'répondre': 'ils répondent', 'rester': 'ils restent', 'revenir': 'ils reviennent',
                        'savoir': 'ils savent', 'sortir': 'ils sortent', 'trouver': 'ils trouvent', 'venir': 'ils viennent',
                        'voir': 'ils voient', 'vouloir': 'ils veulent'},
                'elles': {'abîmer': 'elles abîment', 'acheter': 'elles achètent', 'aimer': 'elles aiment', 'allumer': 'elles allument',
                          'apprendre': 'elles apprennent', 'arriver': 'elles arrivent', 'attendre': 'elles attendent', 'avoir': 'elles ont',
                          'balayer': 'elles balaient', 'boire': 'elles boivent', 'chercher': 'elles cherchent', 'comprendre': 'elles comprennent',
                          'couper': 'elles coupent', 'courir': 'elles courent', 'creuser': 'elles creusent', 'cuisiner': 'elles cuisinent',
                          'cultiver': 'elles cultivent', 'demander': 'elles demandent', 'dire': 'elles disent', 'donner': 'elles donnent',
                          'dormir': 'elles dorment', 'écouter': 'elles écoutent', 'écrire': 'elles écrivent', 'entrer': 'elles entrent',
                          'être': 'elles sont', 'faire': 'elles font', 'finir': 'elles finissent', 'jouer': 'elles jouent',
                          'lire': 'elles lisent', 'manger': 'elles mangent', 'marcher': 'elles marchent', 'parler': 'elles parlent',
                          'partir': 'elles partent', 'planter': 'elles plantent', 'pouvoir': 'elles peuvent', 'prendre': 'elles prennent',
                          'ranger': 'elles rangent', 'répondre': 'elles répondent', 'rester': 'elles restent', 'revenir': 'elles reviennent',
                          'savoir': 'elles savent', 'sortir': 'elles sortent', 'trouver': 'elles trouvent', 'venir': 'elles viennent',
                          'voir': 'elles voient', 'vouloir': 'elles veulent'}
            }
        }
        
        # Règles de conjugaison shimaoré
        self.shimaore_conjugation = {
            'present': {
                'je': 'nis',
                'tu': 'ous', 
                'il': 'as',
                'elle': 'as',
                'nous': 'ris',
                'vous': 'mous',
                'ils': 'was',
                'elles': 'was'
            },
            'past': {
                'je': 'naco',
                'tu': 'waco',
                'il': 'aco', 
                'elle': 'aco',
                'nous': 'raco',
                'vous': 'mwaco',
                'ils': 'waco',
                'elles': 'waco'
            },
            'future': {
                'je': 'nitso',
                'tu': 'outso',
                'il': 'atso',
                'elle': 'atso', 
                'nous': 'ritso',
                'vous': 'moutso',
                'ils': 'watso',
                'elles': 'watso'
            }
        }
        
        # Règles de conjugaison kibouchi
        self.kibouchi_conjugation = {
            'present': {
                'je': 'za',
                'tu': 'ana',
                'il': 'izi',
                'elle': 'izi',
                'nous': 'zéheyi',
                'vous': 'anaréou',
                'ils': 'réou',
                'elles': 'réou'
            },
            # Pour le passé et futur, on appliquera des transformations spéciales
        }
        
        # Pronoms français vers shimaoré/kibouchi
        self.pronouns = {
            'shimaore': {
                'je': 'Wami',
                'tu': 'Wawé', 
                'il': 'Wayé',
                'elle': 'Wayé',
                'nous': 'Wassi',
                'vous': 'Wagnou',
                'ils': 'Wawo',
                'elles': 'Wawo'
            },
            'kibouchi': {
                'je': 'Zahou',
                'tu': 'Anaou',
                'il': 'Izi',
                'elle': 'Izi', 
                'nous': 'Atsika',
                'vous': 'Anaréou',
                'ils': 'Réou',
                'elles': 'Réou'
            }
        }
    
    def get_shimaore_radical(self, infinitive):
        """Extrait le radical d'un verbe shimaoré (enlève 'ou' ou 'Ou')"""
        if infinitive.lower().startswith('ou'):
            return infinitive[2:]  # Enlever 'ou' ou 'Ou'
        return infinitive
    
    def conjugate_shimaore(self, infinitive, pronoun, tense='present'):
        """Conjugue un verbe shimaoré"""
        radical = self.get_shimaore_radical(infinitive)
        
        if tense in self.shimaore_conjugation and pronoun in self.shimaore_conjugation[tense]:
            prefix = self.shimaore_conjugation[tense][pronoun]
            return prefix + radical
        
        return infinitive  # Retour par défaut
    
    def conjugate_kibouchi_past(self, verb):
        """Règle spéciale pour le passé kibouchi: m→n et préfixe 'ni' si pas de 'm' initial"""
        if verb.startswith('m'):
            # Remplacer le 'm' initial par 'n'
            return 'n' + verb[1:]
        else:
            # Ajouter préfixe 'ni' si pas de 'm' initial
            return 'ni' + verb
    
    def conjugate_kibouchi_future(self, verb):
        """Règle spéciale pour le futur kibouchi: m→i"""
        return verb.replace('m', 'i')
    
    def conjugate_kibouchi(self, infinitive, pronoun, tense='present'):
        """Conjugue un verbe kibouchi"""
        if tense == 'present':
            if pronoun in self.kibouchi_conjugation['present']:
                prefix = self.kibouchi_conjugation['present'][pronoun]
                return f"{prefix} {infinitive}"
        
        elif tense == 'past':
            if pronoun in self.kibouchi_conjugation['present']:
                prefix = self.kibouchi_conjugation['present'][pronoun]
                past_verb = self.conjugate_kibouchi_past(infinitive)
                return f"{prefix} {past_verb}"
        
        elif tense == 'future':
            if pronoun in self.kibouchi_conjugation['present']:
                prefix = self.kibouchi_conjugation['present'][pronoun]
                future_verb = self.conjugate_kibouchi_future(infinitive)
                return f"{prefix} bou {future_verb}"
        
        return infinitive  # Retour par défaut
    
    def conjugate_french(self, verb_fr, pronoun, tense='present'):
        """Conjugue un verbe français correctement"""
        # Utiliser le conjugateur automatique français
        try:
            return self.french_conjugator.conjugate_verb(verb_fr, pronoun, tense)
        except Exception:
            # Fallback vers l'ancienne méthode si erreur
            verb_normalized = verb_fr.lower()
            
            if tense in self.french_conjugation and pronoun in self.french_conjugation[tense]:
                if verb_normalized in self.french_conjugation[tense][pronoun]:
                    return self.french_conjugation[tense][pronoun][verb_normalized]
            
            # Conjugaison par défaut si pas trouvée
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
    
    # Filtrer les verbes shimaoré qui commencent par 'ou' ou 'Ou'
    shimaore_infinitives = []
    for verb in verbs:
        if verb['shimaore'].lower().startswith('ou'):
            shimaore_infinitives.append({
                'french': verb['french'],
                'shimaore': verb['shimaore'],
                'kibouchi': verb['kibouchi']
            })
    
    print(f"Verbes infinitifs trouvés: {len(shimaore_infinitives)}")
    return shimaore_infinitives

def create_sentence_database():
    """Crée une base de données de phrases pour le jeu"""
    print("🏗️ Création de la base de données de phrases...")
    
    db = get_database()
    sentences_collection = db.sentences
    
    # Supprimer les phrases existantes
    sentences_collection.delete_many({})
    
    engine = ConjugationEngine()
    verbs = get_available_verbs()
    
    # Obtenir quelques objets courants
    common_objects = [
        {'french': 'du poisson', 'shimaore': 'fi', 'kibouchi': 'lokou'},
        {'french': 'de l\'eau', 'shimaore': 'maji', 'kibouchi': 'ranou'},
        {'french': 'du riz', 'shimaore': 'tsoholé', 'kibouchi': 'vari'},
        {'french': 'le chat', 'shimaore': 'paha', 'kibouchi': 'moirou'},
        {'french': 'la maison', 'shimaore': 'nyoumba', 'kibouchi': 'tragnou'}
    ]
    
    sentences_to_insert = []
    pronouns = ['je', 'tu', 'il', 'nous', 'vous', 'ils']
    tenses = ['present', 'past', 'future']
    
    # Créer des phrases simples (sujet + verbe)
    for verb in verbs[:10]:  # Utiliser les 10 premiers verbes
        for pronoun in pronouns:
            for tense in tenses:
                # Phrase sans objet
                sentence = engine.create_sentence(
                    subject_fr=pronoun,
                    verb_fr=verb['french'],
                    verb_shimaore=verb['shimaore'],
                    verb_kibouchi=verb['kibouchi'],
                    tense=tense
                )
                
                sentence_doc = {
                    'id': str(uuid.uuid4()),
                    'type': 'simple',
                    'difficulty': 1,
                    'french': sentence['french'],
                    'shimaore': sentence['shimaore'],
                    'kibouchi': sentence['kibouchi'],
                    'tense': tense,
                    'shimaore_words': sentence['words']['shimaore'],
                    'kibouchi_words': sentence['words']['kibouchi']
                }
                sentences_to_insert.append(sentence_doc)
    
    # Créer des phrases avec objet (sujet + verbe + objet)
    for verb in verbs[:5]:  # Utiliser les 5 premiers verbes
        for obj in common_objects[:3]:  # 3 objets courants
            for pronoun in ['je', 'tu', 'il']:  # Simplifier pour commencer
                sentence = engine.create_sentence(
                    subject_fr=pronoun,
                    verb_fr=verb['french'],
                    verb_shimaore=verb['shimaore'],
                    verb_kibouchi=verb['kibouchi'],
                    object_fr=obj['french'],
                    object_shimaore=obj['shimaore'],
                    object_kibouchi=obj['kibouchi'],
                    tense='present'
                )
                
                sentence_doc = {
                    'id': str(uuid.uuid4()),
                    'type': 'with_object',
                    'difficulty': 2,
                    'french': sentence['french'],
                    'shimaore': sentence['shimaore'],
                    'kibouchi': sentence['kibouchi'],
                    'tense': 'present',
                    'shimaore_words': sentence['words']['shimaore'],
                    'kibouchi_words': sentence['words']['kibouchi']
                }
                sentences_to_insert.append(sentence_doc)
    
    # Insérer dans la base de données
    if sentences_to_insert:
        sentences_collection.insert_many(sentences_to_insert)
        print(f"✅ {len(sentences_to_insert)} phrases créées")
    
    return len(sentences_to_insert)

def test_conjugation():
    """Test du moteur de conjugaison"""
    print("🧪 Test du moteur de conjugaison...")
    
    engine = ConjugationEngine()
    
    # Test shimaoré
    print("\n--- SHIMAORÉ ---")
    print("Verbe: ourenga (parler)")
    for pronoun in ['je', 'tu', 'il']:
        for tense in ['present', 'past', 'future']:
            conjugated = engine.conjugate_shimaore('ourenga', pronoun, tense)
            print(f"{pronoun} ({tense}): {conjugated}")
    
    # Test kibouchi  
    print("\n--- KIBOUCHI ---")
    print("Verbe: misoma (jouer)")
    for pronoun in ['je', 'tu', 'il']:
        for tense in ['present', 'past', 'future']:
            conjugated = engine.conjugate_kibouchi('misoma', pronoun, tense)
            print(f"{pronoun} ({tense}): {conjugated}")
    
    # Test de phrases complètes
    print("\n--- PHRASES COMPLÈTES ---")
    sentence = engine.create_sentence(
        subject_fr='je',
        verb_fr='mange',
        verb_shimaore='oudhya',
        verb_kibouchi='mihinagna',
        object_fr='du poisson',
        object_shimaore='fi', 
        object_kibouchi='lokou'
    )
    
    print(f"Français: {sentence['french']}")
    print(f"Shimaoré: {sentence['shimaore']}")  
    print(f"Kibouchi: {sentence['kibouchi']}")

def main():
    """Fonction principale"""
    print("=" * 70)
    print("🔧 MOTEUR DE CONJUGAISON SHIMAORÉ ET KIBOUCHI")
    print("=" * 70)
    
    try:
        # Test du moteur
        test_conjugation()
        
        # Créer la base de données de phrases
        sentences_created = create_sentence_database()
        
        print("\n✅ Moteur de conjugaison opérationnel!")
        print(f"📚 {sentences_created} phrases générées pour le jeu")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)