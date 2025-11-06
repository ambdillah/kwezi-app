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

# Conjugaisons françaises complètes - TOUS LES TEMPS
FRENCH_CONJUGATIONS = {
    'present': {
        'je': {
            'parler': 'je parle', 'manger': 'je mange', 'jouer': 'je joue',
            'avoir': "j'ai", 'être': 'je suis', 'aller': 'je vais', 'faire': 'je fais',
            'abîmer': "j'abîme", 'acheter': "j'achète", 'aider': "j'aide", 'aimer': "j'aime",
            'apporter': "j'apporte", 'amener': "j'amène"
        },
        'tu': {
            'parler': 'tu parles', 'manger': 'tu manges', 'jouer': 'tu joues',
            'avoir': 'tu as', 'être': 'tu es', 'aller': 'tu vas', 'faire': 'tu fais',
            'abîmer': 'tu abîmes', 'acheter': 'tu achètes', 'aider': 'tu aides', 'aimer': 'tu aimes',
            'apporter': 'tu apportes', 'amener': 'tu amènes'
        },
        'il': {
            'parler': 'il parle', 'manger': 'il mange', 'jouer': 'il joue',
            'avoir': 'il a', 'être': 'il est', 'aller': 'il va', 'faire': 'il fait',
            'abîmer': 'il abîme', 'acheter': 'il achète', 'aider': 'il aide', 'aimer': 'il aime',
            'apporter': 'il apporte', 'amener': 'il amène'
        },
        'nous': {
            'parler': 'nous parlons', 'manger': 'nous mangeons', 'jouer': 'nous jouons',
            'avoir': 'nous avons', 'être': 'nous sommes', 'aller': 'nous allons', 'faire': 'nous faisons',
            'abîmer': 'nous abîmons', 'acheter': 'nous achetons', 'aider': 'nous aidons', 'aimer': 'nous aimons',
            'apporter': 'nous apportons', 'amener': 'nous amenons'
        },
        'vous': {
            'parler': 'vous parlez', 'manger': 'vous mangez', 'jouer': 'vous jouez',
            'avoir': 'vous avez', 'être': 'vous êtes', 'aller': 'vous allez', 'faire': 'vous faites',
            'abîmer': 'vous abîmez', 'acheter': 'vous achetez', 'aider': 'vous aidez', 'aimer': 'vous aimez',
            'apporter': 'vous apportez', 'amener': 'vous amenez'
        },
        'ils': {
            'parler': 'ils parlent', 'manger': 'ils mangent', 'jouer': 'ils jouent',
            'avoir': 'ils ont', 'être': 'ils sont', 'aller': 'ils vont', 'faire': 'ils font',
            'abîmer': 'ils abîment', 'acheter': 'ils achètent', 'aider': 'ils aident', 'aimer': 'ils aiment',
            'apporter': 'ils apportent', 'amener': 'ils amènent'
        }
    },
    'past': {
        'je': {
            'parler': "j'ai parlé", 'manger': "j'ai mangé", 'jouer': "j'ai joué",
            'avoir': "j'ai eu", 'être': "j'ai été", 'aller': 'je suis allé', 'faire': "j'ai fait",
            'abîmer': "j'ai abîmé", 'acheter': "j'ai acheté", 'aider': "j'ai aidé", 'aimer': "j'ai aimé",
            'apporter': "j'ai apporté", 'amener': "j'ai amené"
        },
        'tu': {
            'parler': 'tu as parlé', 'manger': 'tu as mangé', 'jouer': 'tu as joué',
            'avoir': 'tu as eu', 'être': 'tu as été', 'aller': 'tu es allé', 'faire': 'tu as fait',
            'abîmer': 'tu as abîmé', 'acheter': 'tu as acheté', 'aider': 'tu as aidé', 'aimer': 'tu as aimé',
            'apporter': 'tu as apporté', 'amener': 'tu as amené'
        },
        'il': {
            'parler': 'il a parlé', 'manger': 'il a mangé', 'jouer': 'il a joué',
            'avoir': 'il a eu', 'être': 'il a été', 'aller': 'il est allé', 'faire': 'il a fait',
            'abîmer': 'il a abîmé', 'acheter': 'il a acheté', 'aider': 'il a aidé', 'aimer': 'il a aimé',
            'apporter': 'il a apporté', 'amener': 'il a amené'
        },
        'nous': {
            'parler': 'nous avons parlé', 'manger': 'nous avons mangé', 'jouer': 'nous avons joué',
            'avoir': 'nous avons eu', 'être': 'nous avons été', 'aller': 'nous sommes allés', 'faire': 'nous avons fait',
            'abîmer': 'nous avons abîmé', 'acheter': 'nous avons acheté', 'aider': 'nous avons aidé', 'aimer': 'nous avons aimé',
            'apporter': 'nous avons apporté', 'amener': 'nous avons amené'
        },
        'vous': {
            'parler': 'vous avez parlé', 'manger': 'vous avez mangé', 'jouer': 'vous avez joué',
            'avoir': 'vous avez eu', 'être': 'vous avez été', 'aller': 'vous êtes allés', 'faire': 'vous avez fait',
            'abîmer': 'vous avez abîmé', 'acheter': 'vous avez acheté', 'aider': 'vous avez aidé', 'aimer': 'vous avez aimé',
            'apporter': 'vous avez apporté', 'amener': 'vous avez amené'
        },
        'ils': {
            'parler': 'ils ont parlé', 'manger': 'ils ont mangé', 'jouer': 'ils ont joué',
            'avoir': 'ils ont eu', 'être': 'ils ont été', 'aller': 'ils sont allés', 'faire': 'ils ont fait',
            'abîmer': 'ils ont abîmé', 'acheter': 'ils ont acheté', 'aider': 'ils ont aidé', 'aimer': 'ils ont aimé',
            'apporter': 'ils ont apporté', 'amener': 'ils ont amené'
        }
    },
    'future': {
        'je': {
            'parler': 'je parlerai', 'manger': 'je mangerai', 'jouer': 'je jouerai',
            'avoir': "j'aurai", 'être': 'je serai', 'aller': "j'irai", 'faire': 'je ferai',
            'abîmer': "j'abîmerai", 'acheter': "j'achèterai", 'aider': "j'aiderai", 'aimer': "j'aimerai",
            'apporter': "j'apporterai", 'amener': "j'amènerai"
        },
        'tu': {
            'parler': 'tu parleras', 'manger': 'tu mangeras', 'jouer': 'tu joueras',
            'avoir': 'tu auras', 'être': 'tu seras', 'aller': 'tu iras', 'faire': 'tu feras',
            'abîmer': 'tu abîmeras', 'acheter': 'tu achèteras', 'aider': 'tu aideras', 'aimer': 'tu aimeras',
            'apporter': 'tu apporteras', 'amener': 'tu amèneras'
        },
        'il': {
            'parler': 'il parlera', 'manger': 'il mangera', 'jouer': 'il jouera',
            'avoir': 'il aura', 'être': 'il sera', 'aller': 'il ira', 'faire': 'il fera',
            'abîmer': 'il abîmera', 'acheter': 'il achètera', 'aider': 'il aidera', 'aimer': 'il aimera',
            'apporter': 'il apportera', 'amener': 'il amènera'
        },
        'nous': {
            'parler': 'nous parlerons', 'manger': 'nous mangerons', 'jouer': 'nous jouerons',
            'avoir': 'nous aurons', 'être': 'nous serons', 'aller': 'nous irons', 'faire': 'nous ferons',
            'abîmer': 'nous abîmerons', 'acheter': 'nous achèterons', 'aider': 'nous aiderons', 'aimer': 'nous aimerons',
            'apporter': 'nous apporterons', 'amener': 'nous amènerons'
        },
        'vous': {
            'parler': 'vous parlerez', 'manger': 'vous mangerez', 'jouer': 'vous jouerez',
            'avoir': 'vous aurez', 'être': 'vous serez', 'aller': 'vous irez', 'faire': 'vous ferez',
            'abîmer': 'vous abîmerez', 'acheter': 'vous achèterez', 'aider': 'vous aiderez', 'aimer': 'vous aimerez',
            'apporter': 'vous apporterez', 'amener': 'vous amènerez'
        },
        'ils': {
            'parler': 'ils parleront', 'manger': 'ils mangeront', 'jouer': 'ils joueront',
            'avoir': 'ils auront', 'être': 'ils seront', 'aller': 'ils iront', 'faire': 'ils feront',
            'abîmer': 'ils abîmeront', 'acheter': 'ils achèteront', 'aider': 'ils aideront', 'aimer': 'ils aimeront',
            'apporter': 'ils apporteront', 'amener': 'ils amèneront'
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

def get_complete_french_conjugations():
    """Dictionnaire COMPLET de conjugaisons pour tous les verbes courants"""
    return {
        'present': {
            'je': {
                'abîmer': "j'abîme", 'acheter': "j'achète", 'aider': "j'aide", 'aimer': "j'aime",
                'aller': 'je vais', 'allumer': "j'allume", 'amener': "j'amène", 'apporter': "j'apporte",
                'apprendre': "j'apprends", 'arnaquer': "j'arnaque", 'arrêter': "j'arrête", 'attendre': "j'attends",
                'attraper': "j'attrape", 'avertir': "j'avertis", 'avoir': "j'ai", 'balayer': 'je balaye',
                'boire': 'je bois', 'bouger': 'je bouge', 'changer': 'je change', 'combler': 'je comble',
                'commencer': 'je commence', 'comprendre': 'je comprends', 'connaître': 'je connais',
                'courir': 'je cours', 'danser': 'je danse', 'demander': 'je demande', 'descendre': 'je descends',
                'devenir': 'je deviens', 'dire': 'je dis', 'donner': 'je donne', 'dormir': 'je dors',
                'écouter': "j'écoute", 'écrire': "j'écris", 'emmener': "j'emmène", 'entendre': "j'entends",
                'entrer': "j'entre", 'essayer': "j'essaie", 'être': 'je suis', 'faire': 'je fais',
                'fermer': 'je ferme', 'finir': 'je finis', 'jeter': 'je jette', 'jouer': 'je joue',
                'laver': 'je lave', 'lever': 'je lève', 'lire': 'je lis', 'manger': 'je mange',
                'marcher': 'je marche', 'monter': 'je monte', 'parler': 'je parle', 'partir': 'je pars',
                'passer': 'je passe', 'penser': 'je pense', 'perdre': 'je perds', 'porter': 'je porte',
                'pouvoir': 'je peux', 'prendre': 'je prends', 'quitter': 'je quitte', 'regarder': 'je regarde',
                'rentrer': 'je rentre', 'répondre': 'je réponds', 'rester': 'je reste', 'retourner': 'je retourne',
                'revenir': 'je reviens', 'rire': 'je ris', 'savoir': 'je sais', 'sentir': 'je sens',
                'sortir': 'je sors', 'tenir': 'je tiens', 'tomber': 'je tombe', 'tourner': 'je tourne',
                'travailler': 'je travaille', 'trouver': 'je trouve', 'vendre': 'je vends', 'venir': 'je viens',
                'vivre': 'je vis', 'voir': 'je vois', 'vouloir': 'je veux'
            },
            'tu': {
                'abîmer': 'tu abîmes', 'acheter': 'tu achètes', 'aider': 'tu aides', 'aimer': 'tu aimes',
                'aller': 'tu vas', 'allumer': 'tu allumes', 'amener': 'tu amènes', 'apporter': 'tu apportes',
                'apprendre': 'tu apprends', 'arnaquer': 'tu arnaques', 'arrêter': 'tu arrêtes', 'attendre': 'tu attends',
                'attraper': 'tu attrapes', 'avertir': 'tu avertis', 'avoir': 'tu as', 'balayer': 'tu balayes',
                'boire': 'tu bois', 'bouger': 'tu bouges', 'changer': 'tu changes', 'combler': 'tu combles',
                'commencer': 'tu commences', 'comprendre': 'tu comprends', 'connaître': 'tu connais',
                'courir': 'tu cours', 'danser': 'tu danses', 'demander': 'tu demandes', 'descendre': 'tu descends',
                'devenir': 'tu deviens', 'dire': 'tu dis', 'donner': 'tu donnes', 'dormir': 'tu dors',
                'écouter': 'tu écoutes', 'écrire': 'tu écris', 'emmener': 'tu emmènes', 'entendre': 'tu entends',
                'entrer': 'tu entres', 'essayer': 'tu essaies', 'être': 'tu es', 'faire': 'tu fais',
                'fermer': 'tu fermes', 'finir': 'tu finis', 'jeter': 'tu jettes', 'jouer': 'tu joues',
                'laver': 'tu laves', 'lever': 'tu lèves', 'lire': 'tu lis', 'manger': 'tu manges',
                'marcher': 'tu marches', 'monter': 'tu montes', 'parler': 'tu parles', 'partir': 'tu pars',
                'passer': 'tu passes', 'penser': 'tu penses', 'perdre': 'tu perds', 'porter': 'tu portes',
                'pouvoir': 'tu peux', 'prendre': 'tu prends', 'quitter': 'tu quittes', 'regarder': 'tu regardes',
                'rentrer': 'tu rentres', 'répondre': 'tu réponds', 'rester': 'tu restes', 'retourner': 'tu retournes',
                'revenir': 'tu reviens', 'rire': 'tu ris', 'savoir': 'tu sais', 'sentir': 'tu sens',
                'sortir': 'tu sors', 'tenir': 'tu tiens', 'tomber': 'tu tombes', 'tourner': 'tu tournes',
                'travailler': 'tu travailles', 'trouver': 'tu trouves', 'vendre': 'tu vends', 'venir': 'tu viens',
                'vivre': 'tu vis', 'voir': 'tu vois', 'vouloir': 'tu veux'
            },
            'il': {
                'abîmer': 'il abîme', 'acheter': 'il achète', 'aider': 'il aide', 'aimer': 'il aime',
                'aller': 'il va', 'allumer': 'il allume', 'amener': 'il amène', 'apporter': 'il apporte',
                'apprendre': 'il apprend', 'arnaquer': 'il arnaque', 'arrêter': 'il arrête', 'attendre': 'il attend',
                'attraper': 'il attrape', 'avertir': 'il avertit', 'avoir': 'il a', 'balayer': 'il balaye',
                'boire': 'il boit', 'bouger': 'il bouge', 'changer': 'il change', 'combler': 'il comble',
                'commencer': 'il commence', 'comprendre': 'il comprend', 'connaître': 'il connaît',
                'courir': 'il court', 'danser': 'il danse', 'demander': 'il demande', 'descendre': 'il descend',
                'devenir': 'il devient', 'dire': 'il dit', 'donner': 'il donne', 'dormir': 'il dort',
                'écouter': 'il écoute', 'écrire': 'il écrit', 'emmener': 'il emmène', 'entendre': 'il entend',
                'entrer': 'il entre', 'essayer': 'il essaie', 'être': 'il est', 'faire': 'il fait',
                'fermer': 'il ferme', 'finir': 'il finit', 'jeter': 'il jette', 'jouer': 'il joue',
                'laver': 'il lave', 'lever': 'il lève', 'lire': 'il lit', 'manger': 'il mange',
                'marcher': 'il marche', 'monter': 'il monte', 'parler': 'il parle', 'partir': 'il part',
                'passer': 'il passe', 'penser': 'il pense', 'perdre': 'il perd', 'porter': 'il porte',
                'pouvoir': 'il peut', 'prendre': 'il prend', 'quitter': 'il quitte', 'regarder': 'il regarde',
                'rentrer': 'il rentre', 'répondre': 'il répond', 'rester': 'il reste', 'retourner': 'il retourne',
                'revenir': 'il revient', 'rire': 'il rit', 'savoir': 'il sait', 'sentir': 'il sent',
                'sortir': 'il sort', 'tenir': 'il tient', 'tomber': 'il tombe', 'tourner': 'il tourne',
                'travailler': 'il travaille', 'trouver': 'il trouve', 'vendre': 'il vend', 'venir': 'il vient',
                'vivre': 'il vit', 'voir': 'il voit', 'vouloir': 'il veut'
            },
            'nous': {
                'abîmer': 'nous abîmons', 'acheter': 'nous achetons', 'aider': 'nous aidons', 'aimer': 'nous aimons',
                'aller': 'nous allons', 'allumer': 'nous allumons', 'amener': 'nous amenons', 'apporter': 'nous apportons',
                'apprendre': 'nous apprenons', 'arnaquer': 'nous arnaquons', 'arrêter': 'nous arrêtons', 'attendre': 'nous attendons',
                'attraper': 'nous attrapons', 'avertir': 'nous avertissons', 'avoir': 'nous avons', 'balayer': 'nous balayons',
                'boire': 'nous buvons', 'bouger': 'nous bougeons', 'changer': 'nous changeons', 'combler': 'nous comblons',
                'commencer': 'nous commençons', 'comprendre': 'nous comprenons', 'connaître': 'nous connaissons',
                'courir': 'nous courons', 'danser': 'nous dansons', 'demander': 'nous demandons', 'descendre': 'nous descendons',
                'devenir': 'nous devenons', 'dire': 'nous disons', 'donner': 'nous donnons', 'dormir': 'nous dormons',
                'écouter': 'nous écoutons', 'écrire': 'nous écrivons', 'emmener': 'nous emmenons', 'entendre': 'nous entendons',
                'entrer': 'nous entrons', 'essayer': 'nous essayons', 'être': 'nous sommes', 'faire': 'nous faisons',
                'fermer': 'nous fermons', 'finir': 'nous finissons', 'jeter': 'nous jetons', 'jouer': 'nous jouons',
                'laver': 'nous lavons', 'lever': 'nous levons', 'lire': 'nous lisons', 'manger': 'nous mangeons',
                'marcher': 'nous marchons', 'monter': 'nous montons', 'parler': 'nous parlons', 'partir': 'nous partons',
                'passer': 'nous passons', 'penser': 'nous pensons', 'perdre': 'nous perdons', 'porter': 'nous portons',
                'pouvoir': 'nous pouvons', 'prendre': 'nous prenons', 'quitter': 'nous quittons', 'regarder': 'nous regardons',
                'rentrer': 'nous rentrons', 'répondre': 'nous répondons', 'rester': 'nous restons', 'retourner': 'nous retournons',
                'revenir': 'nous revenons', 'rire': 'nous rions', 'savoir': 'nous savons', 'sentir': 'nous sentons',
                'sortir': 'nous sortons', 'tenir': 'nous tenons', 'tomber': 'nous tombons', 'tourner': 'nous tournons',
                'travailler': 'nous travaillons', 'trouver': 'nous trouvons', 'vendre': 'nous vendons', 'venir': 'nous venons',
                'vivre': 'nous vivons', 'voir': 'nous voyons', 'vouloir': 'nous voulons'
            },
            'vous': {
                'abîmer': 'vous abîmez', 'acheter': 'vous achetez', 'aider': 'vous aidez', 'aimer': 'vous aimez',
                'aller': 'vous allez', 'allumer': 'vous allumez', 'amener': 'vous amenez', 'apporter': 'vous apportez',
                'apprendre': 'vous apprenez', 'arnaquer': 'vous arnaquez', 'arrêter': 'vous arrêtez', 'attendre': 'vous attendez',
                'attraper': 'vous attrapez', 'avertir': 'vous avertissez', 'avoir': 'vous avez', 'balayer': 'vous balayez',
                'boire': 'vous buvez', 'bouger': 'vous bougez', 'changer': 'vous changez', 'combler': 'vous comblez',
                'commencer': 'vous commencez', 'comprendre': 'vous comprenez', 'connaître': 'vous connaissez',
                'courir': 'vous courez', 'danser': 'vous dansez', 'demander': 'vous demandez', 'descendre': 'vous descendez',
                'devenir': 'vous devenez', 'dire': 'vous dites', 'donner': 'vous donnez', 'dormir': 'vous dormez',
                'écouter': 'vous écoutez', 'écrire': 'vous écrivez', 'emmener': 'vous emmenez', 'entendre': 'vous entendez',
                'entrer': 'vous entrez', 'essayer': 'vous essayez', 'être': 'vous êtes', 'faire': 'vous faites',
                'fermer': 'vous fermez', 'finir': 'vous finissez', 'jeter': 'vous jetez', 'jouer': 'vous jouez',
                'laver': 'vous lavez', 'lever': 'vous levez', 'lire': 'vous lisez', 'manger': 'vous mangez',
                'marcher': 'vous marchez', 'monter': 'vous montez', 'parler': 'vous parlez', 'partir': 'vous partez',
                'passer': 'vous passez', 'penser': 'vous pensez', 'perdre': 'vous perdez', 'porter': 'vous portez',
                'pouvoir': 'vous pouvez', 'prendre': 'vous prenez', 'quitter': 'vous quittez', 'regarder': 'vous regardez',
                'rentrer': 'vous rentrez', 'répondre': 'vous répondez', 'rester': 'vous restez', 'retourner': 'vous retournez',
                'revenir': 'vous revenez', 'rire': 'vous riez', 'savoir': 'vous savez', 'sentir': 'vous sentez',
                'sortir': 'vous sortez', 'tenir': 'vous tenez', 'tomber': 'vous tombez', 'tourner': 'vous tournez',
                'travailler': 'vous travaillez', 'trouver': 'vous trouvez', 'vendre': 'vous vendez', 'venir': 'vous venez',
                'vivre': 'vous vivez', 'voir': 'vous voyez', 'vouloir': 'vous voulez'
            },
            'ils': {
                'abîmer': 'ils abîment', 'acheter': 'ils achètent', 'aider': 'ils aident', 'aimer': 'ils aiment',
                'aller': 'ils vont', 'allumer': 'ils allument', 'amener': 'ils amènent', 'apporter': 'ils apportent',
                'apprendre': 'ils apprennent', 'arnaquer': 'ils arnaquent', 'arrêter': 'ils arrêtent', 'attendre': 'ils attendent',
                'attraper': 'ils attrapent', 'avertir': 'ils avertissent', 'avoir': 'ils ont', 'balayer': 'ils balayent',
                'boire': 'ils boivent', 'bouger': 'ils bougent', 'changer': 'ils changent', 'combler': 'ils comblent',
                'commencer': 'ils commencent', 'comprendre': 'ils comprennent', 'connaître': 'ils connaissent',
                'courir': 'ils courent', 'danser': 'ils dansent', 'demander': 'ils demandent', 'descendre': 'ils descendent',
                'devenir': 'ils deviennent', 'dire': 'ils disent', 'donner': 'ils donnent', 'dormir': 'ils dorment',
                'écouter': 'ils écoutent', 'écrire': 'ils écrivent', 'emmener': 'ils emmènent', 'entendre': 'ils entendent',
                'entrer': 'ils entrent', 'essayer': 'ils essaient', 'être': 'ils sont', 'faire': 'ils font',
                'fermer': 'ils ferment', 'finir': 'ils finissent', 'jeter': 'ils jettent', 'jouer': 'ils jouent',
                'laver': 'ils lavent', 'lever': 'ils lèvent', 'lire': 'ils lisent', 'manger': 'ils mangent',
                'marcher': 'ils marchent', 'monter': 'ils montent', 'parler': 'ils parlent', 'partir': 'ils partent',
                'passer': 'ils passent', 'penser': 'ils pensent', 'perdre': 'ils perdent', 'porter': 'ils portent',
                'pouvoir': 'ils peuvent', 'prendre': 'ils prennent', 'quitter': 'ils quittent', 'regarder': 'ils regardent',
                'rentrer': 'ils rentrent', 'répondre': 'ils répondent', 'rester': 'ils restent', 'retourner': 'ils retournent',
                'revenir': 'ils reviennent', 'rire': 'ils rient', 'savoir': 'ils savent', 'sentir': 'ils sentent',
                'sortir': 'ils sortent', 'tenir': 'ils tiennent', 'tomber': 'ils tombent', 'tourner': 'ils tournent',
                'travailler': 'ils travaillent', 'trouver': 'ils trouvent', 'vendre': 'ils vendent', 'venir': 'ils viennent',
                'vivre': 'ils vivent', 'voir': 'ils voient', 'vouloir': 'ils veulent'
            }
        },
        'past': {
            'je': {
                'abîmer': "j'ai abîmé", 'acheter': "j'ai acheté", 'aider': "j'ai aidé", 'aimer': "j'ai aimé",
                'aller': 'je suis allé', 'allumer': "j'ai allumé", 'amener': "j'ai amené", 'apporter': "j'ai apporté",
                'apprendre': "j'ai appris", 'arnaquer': "j'ai arnaqué", 'arrêter': "j'ai arrêté", 'attendre': "j'ai attendu",
                'attraper': "j'ai attrapé", 'avertir': "j'ai averti", 'avoir': "j'ai eu", 'balayer': "j'ai balayé",
                'boire': "j'ai bu", 'bouger': "j'ai bougé", 'changer': "j'ai changé", 'combler': "j'ai comblé",
                'commencer': "j'ai commencé", 'comprendre': "j'ai compris", 'connaître': "j'ai connu",
                'courir': "j'ai couru", 'danser': "j'ai dansé", 'demander': "j'ai demandé", 'descendre': 'je suis descendu',
                'devenir': 'je suis devenu', 'dire': "j'ai dit", 'donner': "j'ai donné", 'dormir': "j'ai dormi",
                'écouter': "j'ai écouté", 'écrire': "j'ai écrit", 'emmener': "j'ai emmené", 'entendre': "j'ai entendu",
                'entrer': 'je suis entré', 'essayer': "j'ai essayé", 'être': "j'ai été", 'faire': "j'ai fait",
                'fermer': "j'ai fermé", 'finir': "j'ai fini", 'jeter': "j'ai jeté", 'jouer': "j'ai joué",
                'laver': "j'ai lavé", 'lever': "j'ai levé", 'lire': "j'ai lu", 'manger': "j'ai mangé",
                'marcher': "j'ai marché", 'monter': 'je suis monté', 'parler': "j'ai parlé", 'partir': 'je suis parti',
                'passer': "j'ai passé", 'penser': "j'ai pensé", 'perdre': "j'ai perdu", 'porter': "j'ai porté",
                'pouvoir': "j'ai pu", 'prendre': "j'ai pris", 'quitter': "j'ai quitté", 'regarder': "j'ai regardé",
                'rentrer': 'je suis rentré', 'répondre': "j'ai répondu", 'rester': 'je suis resté', 'retourner': 'je suis retourné',
                'revenir': 'je suis revenu', 'rire': "j'ai ri", 'savoir': "j'ai su", 'sentir': "j'ai senti",
                'sortir': 'je suis sorti', 'tenir': "j'ai tenu", 'tomber': 'je suis tombé', 'tourner': "j'ai tourné",
                'travailler': "j'ai travaillé", 'trouver': "j'ai trouvé", 'vendre': "j'ai vendu", 'venir': 'je suis venu',
                'vivre': "j'ai vécu", 'voir': "j'ai vu", 'vouloir': "j'ai voulu"
            },
            'tu': {
                'abîmer': 'tu as abîmé', 'acheter': 'tu as acheté', 'aider': 'tu as aidé', 'aimer': 'tu as aimé',
                'aller': 'tu es allé', 'allumer': 'tu as allumé', 'amener': 'tu as amené', 'apporter': 'tu as apporté',
                'apprendre': 'tu as appris', 'arnaquer': 'tu as arnaqué', 'arrêter': 'tu as arrêté', 'attendre': 'tu as attendu',
                'attraper': 'tu as attrapé', 'avertir': 'tu as averti', 'avoir': 'tu as eu', 'balayer': 'tu as balayé',
                'boire': 'tu as bu', 'bouger': 'tu as bougé', 'changer': 'tu as changé', 'combler': 'tu as comblé',
                'commencer': 'tu as commencé', 'comprendre': 'tu as compris', 'connaître': 'tu as connu',
                'courir': 'tu as couru', 'danser': 'tu as dansé', 'demander': 'tu as demandé', 'descendre': 'tu es descendu',
                'devenir': 'tu es devenu', 'dire': 'tu as dit', 'donner': 'tu as donné', 'dormir': 'tu as dormi',
                'écouter': 'tu as écouté', 'écrire': 'tu as écrit', 'emmener': 'tu as emmené', 'entendre': 'tu as entendu',
                'entrer': 'tu es entré', 'essayer': 'tu as essayé', 'être': 'tu as été', 'faire': 'tu as fait',
                'fermer': 'tu as fermé', 'finir': 'tu as fini', 'jeter': 'tu as jeté', 'jouer': 'tu as joué',
                'laver': 'tu as lavé', 'lever': 'tu as levé', 'lire': 'tu as lu', 'manger': 'tu as mangé',
                'marcher': 'tu as marché', 'monter': 'tu es monté', 'parler': 'tu as parlé', 'partir': 'tu es parti',
                'passer': 'tu as passé', 'penser': 'tu as pensé', 'perdre': 'tu as perdu', 'porter': 'tu as porté',
                'pouvoir': 'tu as pu', 'prendre': 'tu as pris', 'quitter': 'tu as quitté', 'regarder': 'tu as regardé',
                'rentrer': 'tu es rentré', 'répondre': 'tu as répondu', 'rester': 'tu es resté', 'retourner': 'tu es retourné',
                'revenir': 'tu es revenu', 'rire': 'tu as ri', 'savoir': 'tu as su', 'sentir': 'tu as senti',
                'sortir': 'tu es sorti', 'tenir': 'tu as tenu', 'tomber': 'tu es tombé', 'tourner': 'tu as tourné',
                'travailler': 'tu as travaillé', 'trouver': 'tu as trouvé', 'vendre': 'tu as vendu', 'venir': 'tu es venu',
                'vivre': 'tu as vécu', 'voir': 'tu as vu', 'vouloir': 'tu as voulu'
            },
            'il': {
                'abîmer': 'il a abîmé', 'acheter': 'il a acheté', 'aider': 'il a aidé', 'aimer': 'il a aimé',
                'aller': 'il est allé', 'allumer': 'il a allumé', 'amener': 'il a amené', 'apporter': 'il a apporté',
                'apprendre': 'il a appris', 'arnaquer': 'il a arnaqué', 'arrêter': 'il a arrêté', 'attendre': 'il a attendu',
                'attraper': 'il a attrapé', 'avertir': 'il a averti', 'avoir': 'il a eu', 'balayer': 'il a balayé',
                'boire': 'il a bu', 'bouger': 'il a bougé', 'changer': 'il a changé', 'combler': 'il a comblé',
                'commencer': 'il a commencé', 'comprendre': 'il a compris', 'connaître': 'il a connu',
                'courir': 'il a couru', 'danser': 'il a dansé', 'demander': 'il a demandé', 'descendre': 'il est descendu',
                'devenir': 'il est devenu', 'dire': 'il a dit', 'donner': 'il a donné', 'dormir': 'il a dormi',
                'écouter': 'il a écouté', 'écrire': 'il a écrit', 'emmener': 'il a emmené', 'entendre': 'il a entendu',
                'entrer': 'il est entré', 'essayer': 'il a essayé', 'être': 'il a été', 'faire': 'il a fait',
                'fermer': 'il a fermé', 'finir': 'il a fini', 'jeter': 'il a jeté', 'jouer': 'il a joué',
                'laver': 'il a lavé', 'lever': 'il a levé', 'lire': 'il a lu', 'manger': 'il a mangé',
                'marcher': 'il a marché', 'monter': 'il est monté', 'parler': 'il a parlé', 'partir': 'il est parti',
                'passer': 'il a passé', 'penser': 'il a pensé', 'perdre': 'il a perdu', 'porter': 'il a porté',
                'pouvoir': 'il a pu', 'prendre': 'il a pris', 'quitter': 'il a quitté', 'regarder': 'il a regardé',
                'rentrer': 'il est rentré', 'répondre': 'il a répondu', 'rester': 'il est resté', 'retourner': 'il est retourné',
                'revenir': 'il est revenu', 'rire': 'il a ri', 'savoir': 'il a su', 'sentir': 'il a senti',
                'sortir': 'il est sorti', 'tenir': 'il a tenu', 'tomber': 'il est tombé', 'tourner': 'il a tourné',
                'travailler': 'il a travaillé', 'trouver': 'il a trouvé', 'vendre': 'il a vendu', 'venir': 'il est venu',
                'vivre': 'il a vécu', 'voir': 'il a vu', 'vouloir': 'il a voulu'
            },
            'nous': {
                'abîmer': 'nous avons abîmé', 'acheter': 'nous avons acheté', 'aider': 'nous avons aidé', 'aimer': 'nous avons aimé',
                'aller': 'nous sommes allés', 'allumer': 'nous avons allumé', 'amener': 'nous avons amené', 'apporter': 'nous avons apporté',
                'apprendre': 'nous avons appris', 'arnaquer': 'nous avons arnaqué', 'arrêter': 'nous avons arrêté', 'attendre': 'nous avons attendu',
                'attraper': 'nous avons attrapé', 'avertir': 'nous avons averti', 'avoir': 'nous avons eu', 'balayer': 'nous avons balayé',
                'boire': 'nous avons bu', 'bouger': 'nous avons bougé', 'changer': 'nous avons changé', 'combler': 'nous avons comblé',
                'commencer': 'nous avons commencé', 'comprendre': 'nous avons compris', 'connaître': 'nous avons connu',
                'courir': 'nous avons couru', 'danser': 'nous avons dansé', 'demander': 'nous avons demandé', 'descendre': 'nous sommes descendus',
                'devenir': 'nous sommes devenus', 'dire': 'nous avons dit', 'donner': 'nous avons donné', 'dormir': 'nous avons dormi',
                'écouter': 'nous avons écouté', 'écrire': 'nous avons écrit', 'emmener': 'nous avons emmené', 'entendre': 'nous avons entendu',
                'entrer': 'nous sommes entrés', 'essayer': 'nous avons essayé', 'être': 'nous avons été', 'faire': 'nous avons fait',
                'fermer': 'nous avons fermé', 'finir': 'nous avons fini', 'jeter': 'nous avons jeté', 'jouer': 'nous avons joué',
                'laver': 'nous avons lavé', 'lever': 'nous avons levé', 'lire': 'nous avons lu', 'manger': 'nous avons mangé',
                'marcher': 'nous avons marché', 'monter': 'nous sommes montés', 'parler': 'nous avons parlé', 'partir': 'nous sommes partis',
                'passer': 'nous avons passé', 'penser': 'nous avons pensé', 'perdre': 'nous avons perdu', 'porter': 'nous avons porté',
                'pouvoir': 'nous avons pu', 'prendre': 'nous avons pris', 'quitter': 'nous avons quitté', 'regarder': 'nous avons regardé',
                'rentrer': 'nous sommes rentrés', 'répondre': 'nous avons répondu', 'rester': 'nous sommes restés', 'retourner': 'nous sommes retournés',
                'revenir': 'nous sommes revenus', 'rire': 'nous avons ri', 'savoir': 'nous avons su', 'sentir': 'nous avons senti',
                'sortir': 'nous sommes sortis', 'tenir': 'nous avons tenu', 'tomber': 'nous sommes tombés', 'tourner': 'nous avons tourné',
                'travailler': 'nous avons travaillé', 'trouver': 'nous avons trouvé', 'vendre': 'nous avons vendu', 'venir': 'nous sommes venus',
                'vivre': 'nous avons vécu', 'voir': 'nous avons vu', 'vouloir': 'nous avons voulu'
            },
            'vous': {
                'abîmer': 'vous avez abîmé', 'acheter': 'vous avez acheté', 'aider': 'vous avez aidé', 'aimer': 'vous avez aimé',
                'aller': 'vous êtes allés', 'allumer': 'vous avez allumé', 'amener': 'vous avez amené', 'apporter': 'vous avez apporté',
                'apprendre': 'vous avez appris', 'arnaquer': 'vous avez arnaqué', 'arrêter': 'vous avez arrêté', 'attendre': 'vous avez attendu',
                'attraper': 'vous avez attrapé', 'avertir': 'vous avez averti', 'avoir': 'vous avez eu', 'balayer': 'vous avez balayé',
                'boire': 'vous avez bu', 'bouger': 'vous avez bougé', 'changer': 'vous avez changé', 'combler': 'vous avez comblé',
                'commencer': 'vous avez commencé', 'comprendre': 'vous avez compris', 'connaître': 'vous avez connu',
                'courir': 'vous avez couru', 'danser': 'vous avez dansé', 'demander': 'vous avez demandé', 'descendre': 'vous êtes descendus',
                'devenir': 'vous êtes devenus', 'dire': 'vous avez dit', 'donner': 'vous avez donné', 'dormir': 'vous avez dormi',
                'écouter': 'vous avez écouté', 'écrire': 'vous avez écrit', 'emmener': 'vous avez emmené', 'entendre': 'vous avez entendu',
                'entrer': 'vous êtes entrés', 'essayer': 'vous avez essayé', 'être': 'vous avez été', 'faire': 'vous avez fait',
                'fermer': 'vous avez fermé', 'finir': 'vous avez fini', 'jeter': 'vous avez jeté', 'jouer': 'vous avez joué',
                'laver': 'vous avez lavé', 'lever': 'vous avez levé', 'lire': 'vous avez lu', 'manger': 'vous avez mangé',
                'marcher': 'vous avez marché', 'monter': 'vous êtes montés', 'parler': 'vous avez parlé', 'partir': 'vous êtes partis',
                'passer': 'vous avez passé', 'penser': 'vous avez pensé', 'perdre': 'vous avez perdu', 'porter': 'vous avez porté',
                'pouvoir': 'vous avez pu', 'prendre': 'vous avez pris', 'quitter': 'vous avez quitté', 'regarder': 'vous avez regardé',
                'rentrer': 'vous êtes rentrés', 'répondre': 'vous avez répondu', 'rester': 'vous êtes restés', 'retourner': 'vous êtes retournés',
                'revenir': 'vous êtes revenus', 'rire': 'vous avez ri', 'savoir': 'vous avez su', 'sentir': 'vous avez senti',
                'sortir': 'vous êtes sortis', 'tenir': 'vous avez tenu', 'tomber': 'vous êtes tombés', 'tourner': 'vous avez tourné',
                'travailler': 'vous avez travaillé', 'trouver': 'vous avez trouvé', 'vendre': 'vous avez vendu', 'venir': 'vous êtes venus',
                'vivre': 'vous avez vécu', 'voir': 'vous avez vu', 'vouloir': 'vous avez voulu'
            },
            'ils': {
                'abîmer': 'ils ont abîmé', 'acheter': 'ils ont acheté', 'aider': 'ils ont aidé', 'aimer': 'ils ont aimé',
                'aller': 'ils sont allés', 'allumer': 'ils ont allumé', 'amener': 'ils ont amené', 'apporter': 'ils ont apporté',
                'apprendre': 'ils ont appris', 'arnaquer': 'ils ont arnaqué', 'arrêter': 'ils ont arrêté', 'attendre': 'ils ont attendu',
                'attraper': 'ils ont attrapé', 'avertir': 'ils ont averti', 'avoir': 'ils ont eu', 'balayer': 'ils ont balayé',
                'boire': 'ils ont bu', 'bouger': 'ils ont bougé', 'changer': 'ils ont changé', 'combler': 'ils ont comblé',
                'commencer': 'ils ont commencé', 'comprendre': 'ils ont compris', 'connaître': 'ils ont connu',
                'courir': 'ils ont couru', 'danser': 'ils ont dansé', 'demander': 'ils ont demandé', 'descendre': 'ils sont descendus',
                'devenir': 'ils sont devenus', 'dire': 'ils ont dit', 'donner': 'ils ont donné', 'dormir': 'ils ont dormi',
                'écouter': 'ils ont écouté', 'écrire': 'ils ont écrit', 'emmener': 'ils ont emmené', 'entendre': 'ils ont entendu',
                'entrer': 'ils sont entrés', 'essayer': 'ils ont essayé', 'être': 'ils ont été', 'faire': 'ils ont fait',
                'fermer': 'ils ont fermé', 'finir': 'ils ont fini', 'jeter': 'ils ont jeté', 'jouer': 'ils ont joué',
                'laver': 'ils ont lavé', 'lever': 'ils ont levé', 'lire': 'ils ont lu', 'manger': 'ils ont mangé',
                'marcher': 'ils ont marché', 'monter': 'ils sont montés', 'parler': 'ils ont parlé', 'partir': 'ils sont partis',
                'passer': 'ils ont passé', 'penser': 'ils ont pensé', 'perdre': 'ils ont perdu', 'porter': 'ils ont porté',
                'pouvoir': 'ils ont pu', 'prendre': 'ils ont pris', 'quitter': 'ils ont quitté', 'regarder': 'ils ont regardé',
                'rentrer': 'ils sont rentrés', 'répondre': 'ils ont répondu', 'rester': 'ils sont restés', 'retourner': 'ils sont retournés',
                'revenir': 'ils sont revenus', 'rire': 'ils ont ri', 'savoir': 'ils ont su', 'sentir': 'ils ont senti',
                'sortir': 'ils sont sortis', 'tenir': 'ils ont tenu', 'tomber': 'ils sont tombés', 'tourner': 'ils ont tourné',
                'travailler': 'ils ont travaillé', 'trouver': 'ils ont trouvé', 'vendre': 'ils ont vendu', 'venir': 'ils sont venus',
                'vivre': 'ils ont vécu', 'voir': 'ils ont vu', 'vouloir': 'ils ont voulu'
            }
        },
        'future': {
            'je': {
                'abîmer': "j'abîmerai", 'acheter': "j'achèterai", 'aider': "j'aiderai", 'aimer': "j'aimerai",
                'aller': "j'irai", 'allumer': "j'allumerai", 'amener': "j'amènerai", 'apporter': "j'apporterai",
                'apprendre': "j'apprendrai", 'arnaquer': "j'arnaquerai", 'arrêter': "j'arrêterai", 'attendre': "j'attendrai",
                'attraper': "j'attraperai", 'avertir': "j'avertirai", 'avoir': "j'aurai", 'balayer': 'je balayerai',
                'boire': 'je boirai', 'bouger': 'je bougerai', 'changer': 'je changerai', 'combler': 'je comblerai',
                'commencer': 'je commencerai', 'comprendre': 'je comprendrai', 'connaître': 'je connaîtrai',
                'courir': 'je courrai', 'danser': 'je danserai', 'demander': 'je demanderai', 'descendre': 'je descendrai',
                'devenir': 'je deviendrai', 'dire': 'je dirai', 'donner': 'je donnerai', 'dormir': 'je dormirai',
                'écouter': "j'écouterai", 'écrire': "j'écrirai", 'emmener': "j'emmènerai", 'entendre': "j'entendrai",
                'entrer': "j'entrerai", 'essayer': "j'essaierai", 'être': 'je serai', 'faire': 'je ferai',
                'fermer': 'je fermerai', 'finir': 'je finirai', 'jeter': 'je jetterai', 'jouer': 'je jouerai',
                'laver': 'je laverai', 'lever': 'je lèverai', 'lire': 'je lirai', 'manger': 'je mangerai',
                'marcher': 'je marcherai', 'monter': 'je monterai', 'parler': 'je parlerai', 'partir': 'je partirai',
                'passer': 'je passerai', 'penser': 'je penserai', 'perdre': 'je perdrai', 'porter': 'je porterai',
                'pouvoir': 'je pourrai', 'prendre': 'je prendrai', 'quitter': 'je quitterai', 'regarder': 'je regarderai',
                'rentrer': 'je rentrerai', 'répondre': 'je répondrai', 'rester': 'je resterai', 'retourner': 'je retournerai',
                'revenir': 'je reviendrai', 'rire': 'je rirai', 'savoir': 'je saurai', 'sentir': 'je sentirai',
                'sortir': 'je sortirai', 'tenir': 'je tiendrai', 'tomber': 'je tomberai', 'tourner': 'je tournerai',
                'travailler': 'je travaillerai', 'trouver': 'je trouverai', 'vendre': 'je vendrai', 'venir': 'je viendrai',
                'vivre': 'je vivrai', 'voir': 'je verrai', 'vouloir': 'je voudrai'
            },
            'tu': {
                'abîmer': 'tu abîmeras', 'acheter': 'tu achèteras', 'aider': 'tu aideras', 'aimer': 'tu aimeras',
                'aller': 'tu iras', 'allumer': 'tu allumeras', 'amener': 'tu amèneras', 'apporter': 'tu apporteras',
                'apprendre': 'tu apprendras', 'arnaquer': 'tu arnaqueras', 'arrêter': 'tu arrêteras', 'attendre': 'tu attendras',
                'attraper': 'tu attraperas', 'avertir': 'tu avertiras', 'avoir': 'tu auras', 'balayer': 'tu balayeras',
                'boire': 'tu boiras', 'bouger': 'tu bougeras', 'changer': 'tu changeras', 'combler': 'tu combleras',
                'commencer': 'tu commenceras', 'comprendre': 'tu comprendras', 'connaître': 'tu connaîtras',
                'courir': 'tu courras', 'danser': 'tu danseras', 'demander': 'tu demanderas', 'descendre': 'tu descendras',
                'devenir': 'tu deviendras', 'dire': 'tu diras', 'donner': 'tu donneras', 'dormir': 'tu dormiras',
                'écouter': 'tu écouteras', 'écrire': 'tu écriras', 'emmener': 'tu emmèneras', 'entendre': 'tu entendras',
                'entrer': 'tu entreras', 'essayer': 'tu essaieras', 'être': 'tu seras', 'faire': 'tu feras',
                'fermer': 'tu fermeras', 'finir': 'tu finiras', 'jeter': 'tu jetteras', 'jouer': 'tu joueras',
                'laver': 'tu laveras', 'lever': 'tu lèveras', 'lire': 'tu liras', 'manger': 'tu mangeras',
                'marcher': 'tu marcheras', 'monter': 'tu monteras', 'parler': 'tu parleras', 'partir': 'tu partiras',
                'passer': 'tu passeras', 'penser': 'tu penseras', 'perdre': 'tu perdras', 'porter': 'tu porteras',
                'pouvoir': 'tu pourras', 'prendre': 'tu prendras', 'quitter': 'tu quitteras', 'regarder': 'tu regarderas',
                'rentrer': 'tu rentreras', 'répondre': 'tu répondras', 'rester': 'tu resteras', 'retourner': 'tu retourneras',
                'revenir': 'tu reviendras', 'rire': 'tu riras', 'savoir': 'tu sauras', 'sentir': 'tu sentiras',
                'sortir': 'tu sortiras', 'tenir': 'tu tiendras', 'tomber': 'tu tomberas', 'tourner': 'tu tourneras',
                'travailler': 'tu travailleras', 'trouver': 'tu trouveras', 'vendre': 'tu vendras', 'venir': 'tu viendras',
                'vivre': 'tu vivras', 'voir': 'tu verras', 'vouloir': 'tu voudras'
            },
            'il': {
                'abîmer': 'il abîmera', 'acheter': 'il achètera', 'aider': 'il aidera', 'aimer': 'il aimera',
                'aller': 'il ira', 'allumer': 'il allumera', 'amener': 'il amènera', 'apporter': 'il apportera',
                'apprendre': 'il apprendra', 'arnaquer': 'il arnaquera', 'arrêter': 'il arrêtera', 'attendre': 'il attendra',
                'attraper': 'il attrapera', 'avertir': 'il avertira', 'avoir': 'il aura', 'balayer': 'il balayera',
                'boire': 'il boira', 'bouger': 'il bougera', 'changer': 'il changera', 'combler': 'il comblera',
                'commencer': 'il commencera', 'comprendre': 'il comprendra', 'connaître': 'il connaîtra',
                'courir': 'il courra', 'danser': 'il dansera', 'demander': 'il demandera', 'descendre': 'il descendra',
                'devenir': 'il deviendra', 'dire': 'il dira', 'donner': 'il donnera', 'dormir': 'il dormira',
                'écouter': 'il écoutera', 'écrire': 'il écrira', 'emmener': 'il emmènera', 'entendre': 'il entendra',
                'entrer': 'il entrera', 'essayer': 'il essaiera', 'être': 'il sera', 'faire': 'il fera',
                'fermer': 'il fermera', 'finir': 'il finira', 'jeter': 'il jettera', 'jouer': 'il jouera',
                'laver': 'il lavera', 'lever': 'il lèvera', 'lire': 'il lira', 'manger': 'il mangera',
                'marcher': 'il marchera', 'monter': 'il montera', 'parler': 'il parlera', 'partir': 'il partira',
                'passer': 'il passera', 'penser': 'il pensera', 'perdre': 'il perdra', 'porter': 'il portera',
                'pouvoir': 'il pourra', 'prendre': 'il prendra', 'quitter': 'il quittera', 'regarder': 'il regardera',
                'rentrer': 'il rentrera', 'répondre': 'il répondra', 'rester': 'il restera', 'retourner': 'il retournera',
                'revenir': 'il reviendra', 'rire': 'il rira', 'savoir': 'il saura', 'sentir': 'il sentira',
                'sortir': 'il sortira', 'tenir': 'il tiendra', 'tomber': 'il tombera', 'tourner': 'il tournera',
                'travailler': 'il travaillera', 'trouver': 'il trouvera', 'vendre': 'il vendra', 'venir': 'il viendra',
                'vivre': 'il vivra', 'voir': 'il verra', 'vouloir': 'il voudra'
            },
            'nous': {
                'abîmer': 'nous abîmerons', 'acheter': 'nous achèterons', 'aider': 'nous aiderons', 'aimer': 'nous aimerons',
                'aller': 'nous irons', 'allumer': 'nous allumerons', 'amener': 'nous amènerons', 'apporter': 'nous apporterons',
                'apprendre': 'nous apprendrons', 'arnaquer': 'nous arnaquerons', 'arrêter': 'nous arrêterons', 'attendre': 'nous attendrons',
                'attraper': 'nous attraperons', 'avertir': 'nous avertirons', 'avoir': 'nous aurons', 'balayer': 'nous balayerons',
                'boire': 'nous boirons', 'bouger': 'nous bougerons', 'changer': 'nous changerons', 'combler': 'nous comblerons',
                'commencer': 'nous commencerons', 'comprendre': 'nous comprendrons', 'connaître': 'nous connaîtrons',
                'courir': 'nous courrons', 'danser': 'nous danserons', 'demander': 'nous demanderons', 'descendre': 'nous descendrons',
                'devenir': 'nous deviendrons', 'dire': 'nous dirons', 'donner': 'nous donnerons', 'dormir': 'nous dormirons',
                'écouter': 'nous écouterons', 'écrire': 'nous écrirons', 'emmener': 'nous emmènerons', 'entendre': 'nous entendrons',
                'entrer': 'nous entrerons', 'essayer': 'nous essaierons', 'être': 'nous serons', 'faire': 'nous ferons',
                'fermer': 'nous fermerons', 'finir': 'nous finirons', 'jeter': 'nous jetterons', 'jouer': 'nous jouerons',
                'laver': 'nous laverons', 'lever': 'nous lèverons', 'lire': 'nous lirons', 'manger': 'nous mangerons',
                'marcher': 'nous marcherons', 'monter': 'nous monterons', 'parler': 'nous parlerons', 'partir': 'nous partirons',
                'passer': 'nous passerons', 'penser': 'nous penserons', 'perdre': 'nous perdrons', 'porter': 'nous porterons',
                'pouvoir': 'nous pourrons', 'prendre': 'nous prendrons', 'quitter': 'nous quitterons', 'regarder': 'nous regarderons',
                'rentrer': 'nous rentrerons', 'répondre': 'nous répondrons', 'rester': 'nous resterons', 'retourner': 'nous retournerons',
                'revenir': 'nous reviendrons', 'rire': 'nous rirons', 'savoir': 'nous saurons', 'sentir': 'nous sentirons',
                'sortir': 'nous sortirons', 'tenir': 'nous tiendrons', 'tomber': 'nous tomberons', 'tourner': 'nous tournerons',
                'travailler': 'nous travaillerons', 'trouver': 'nous trouverons', 'vendre': 'nous vendrons', 'venir': 'nous viendrons',
                'vivre': 'nous vivrons', 'voir': 'nous verrons', 'vouloir': 'nous voudrons'
            },
            'vous': {
                'abîmer': 'vous abîmerez', 'acheter': 'vous achèterez', 'aider': 'vous aiderez', 'aimer': 'vous aimerez',
                'aller': 'vous irez', 'allumer': 'vous allumerez', 'amener': 'vous amènerez', 'apporter': 'vous apporterez',
                'apprendre': 'vous apprendrez', 'arnaquer': 'vous arnaquerez', 'arrêter': 'vous arrêterez', 'attendre': 'vous attendrez',
                'attraper': 'vous attraperez', 'avertir': 'vous avertirez', 'avoir': 'vous aurez', 'balayer': 'vous balayerez',
                'boire': 'vous boirez', 'bouger': 'vous bougerez', 'changer': 'vous changerez', 'combler': 'vous comblerez',
                'commencer': 'vous commencerez', 'comprendre': 'vous comprendrez', 'connaître': 'vous connaîtrez',
                'courir': 'vous courrez', 'danser': 'vous danserez', 'demander': 'vous demanderez', 'descendre': 'vous descendrez',
                'devenir': 'vous deviendrez', 'dire': 'vous direz', 'donner': 'vous donnerez', 'dormir': 'vous dormirez',
                'écouter': 'vous écouterez', 'écrire': 'vous écrirez', 'emmener': 'vous emmènerez', 'entendre': 'vous entendrez',
                'entrer': 'vous entrerez', 'essayer': 'vous essaierez', 'être': 'vous serez', 'faire': 'vous ferez',
                'fermer': 'vous fermerez', 'finir': 'vous finirez', 'jeter': 'vous jetterez', 'jouer': 'vous jouerez',
                'laver': 'vous laverez', 'lever': 'vous lèverez', 'lire': 'vous lirez', 'manger': 'vous mangerez',
                'marcher': 'vous marcherez', 'monter': 'vous monterez', 'parler': 'vous parlerez', 'partir': 'vous partirez',
                'passer': 'vous passerez', 'penser': 'vous penserez', 'perdre': 'vous perdrez', 'porter': 'vous porterez',
                'pouvoir': 'vous pourrez', 'prendre': 'vous prendrez', 'quitter': 'vous quitterez', 'regarder': 'vous regarderez',
                'rentrer': 'vous rentrerez', 'répondre': 'vous répondrez', 'rester': 'vous resterez', 'retourner': 'vous retournerez',
                'revenir': 'vous reviendrez', 'rire': 'vous rirez', 'savoir': 'vous saurez', 'sentir': 'vous sentirez',
                'sortir': 'vous sortirez', 'tenir': 'vous tiendrez', 'tomber': 'vous tomberez', 'tourner': 'vous tournerez',
                'travailler': 'vous travaillerez', 'trouver': 'vous trouverez', 'vendre': 'vous vendrez', 'venir': 'vous viendrez',
                'vivre': 'vous vivrez', 'voir': 'vous verrez', 'vouloir': 'vous voudrez'
            },
            'ils': {
                'abîmer': 'ils abîmeront', 'acheter': 'ils achèteront', 'aider': 'ils aideront', 'aimer': 'ils aimeront',
                'aller': 'ils iront', 'allumer': 'ils allumeront', 'amener': 'ils amèneront', 'apporter': 'ils apporteront',
                'apprendre': 'ils apprendront', 'arnaquer': 'ils arnaqueront', 'arrêter': 'ils arrêteront', 'attendre': 'ils attendront',
                'attraper': 'ils attraperont', 'avertir': 'ils avertiront', 'avoir': 'ils auront', 'balayer': 'ils balayeront',
                'boire': 'ils boiront', 'bouger': 'ils bougeront', 'changer': 'ils changeront', 'combler': 'ils combleront',
                'commencer': 'ils commenceront', 'comprendre': 'ils comprendront', 'connaître': 'ils connaîtront',
                'courir': 'ils courront', 'danser': 'ils danseront', 'demander': 'ils demanderont', 'descendre': 'ils descendront',
                'devenir': 'ils deviendront', 'dire': 'ils diront', 'donner': 'ils donneront', 'dormir': 'ils dormiront',
                'écouter': 'ils écouteront', 'écrire': 'ils écriront', 'emmener': 'ils emmèneront', 'entendre': 'ils entendront',
                'entrer': 'ils entreront', 'essayer': 'ils essaieront', 'être': 'ils seront', 'faire': 'ils feront',
                'fermer': 'ils fermeront', 'finir': 'ils finiront', 'jeter': 'ils jetteront', 'jouer': 'ils joueront',
                'laver': 'ils laveront', 'lever': 'ils lèveront', 'lire': 'ils liront', 'manger': 'ils mangeront',
                'marcher': 'ils marcheront', 'monter': 'ils monteront', 'parler': 'ils parleront', 'partir': 'ils partiront',
                'passer': 'ils passeront', 'penser': 'ils penseront', 'perdre': 'ils perdront', 'porter': 'ils porteront',
                'pouvoir': 'ils pourront', 'prendre': 'ils prendront', 'quitter': 'ils quitteront', 'regarder': 'ils regarderont',
                'rentrer': 'ils rentreront', 'répondre': 'ils répondront', 'rester': 'ils resteront', 'retourner': 'ils retourneront',
                'revenir': 'ils reviendront', 'rire': 'ils riront', 'savoir': 'ils sauront', 'sentir': 'ils sentiront',
                'sortir': 'ils sortiront', 'tenir': 'ils tiendront', 'tomber': 'ils tomberont', 'tourner': 'ils tourneront',
                'travailler': 'ils travailleront', 'trouver': 'ils trouveront', 'vendre': 'ils vendront', 'venir': 'ils viendront',
                'vivre': 'ils vivront', 'voir': 'ils verront', 'vouloir': 'ils voudront'
            }
        }
    }

# Charger le dictionnaire complet
FRENCH_CONJUGATIONS = get_complete_french_conjugations()

def conjugate_french(verb, pronoun, tense='present'):
    """Conjugue un verbe français correctement"""
    verb_lower = verb.lower()
    
    # Utiliser le dictionnaire de conjugaisons complet
    if tense in FRENCH_CONJUGATIONS and pronoun in FRENCH_CONJUGATIONS[tense]:
        if verb_lower in FRENCH_CONJUGATIONS[tense][pronoun]:
            return FRENCH_CONJUGATIONS[tense][pronoun][verb_lower]
    
    # Fallback pour verbes du 1er groupe non répertoriés
    if verb_lower.endswith('er') and tense == 'present':
        radical = verb_lower[:-2]
        endings = {'je': 'e', 'tu': 'es', 'il': 'e', 'nous': 'ons', 'vous': 'ez', 'ils': 'ent'}
        if pronoun in endings:
            # Gestion de l'élision
            if pronoun == 'je' and radical and radical[0] in 'aeiouhéè':
                return f"j'{radical}{endings[pronoun]}"
            return f"{pronoun} {radical}{endings[pronoun]}"
    
    # Dernier fallback
    print(f"⚠️  Conjugaison manquante: {verb} ({pronoun}, {tense})")
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
