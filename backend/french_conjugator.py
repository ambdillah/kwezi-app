#!/usr/bin/env python3
"""
CONJUGATEUR FRANÇAIS AUTOMATIQUE
================================
Système de conjugaison française automatique pour tous les verbes
"""

class FrenchConjugator:
    """Conjugateur français automatique"""
    
    def __init__(self):
        # Verbes irréguliers les plus courants
        self.irregular_verbs = {
            'être': {
                'present': {
                    'je': 'je suis', 'tu': 'tu es', 'il': 'il est', 'elle': 'elle est',
                    'nous': 'nous sommes', 'vous': 'vous êtes', 'ils': 'ils sont', 'elles': 'elles sont'
                }
            },
            'avoir': {
                'present': {
                    'je': "j'ai", 'tu': 'tu as', 'il': 'il a', 'elle': 'elle a',
                    'nous': 'nous avons', 'vous': 'vous avez', 'ils': 'ils ont', 'elles': 'elles ont'
                }
            },
            'aller': {
                'present': {
                    'je': 'je vais', 'tu': 'tu vas', 'il': 'il va', 'elle': 'elle va',
                    'nous': 'nous allons', 'vous': 'vous allez', 'ils': 'ils vont', 'elles': 'elles vont'
                }
            },
            'faire': {
                'present': {
                    'je': 'je fais', 'tu': 'tu fais', 'il': 'il fait', 'elle': 'elle fait',
                    'nous': 'nous faisons', 'vous': 'vous faites', 'ils': 'ils font', 'elles': 'elles font'
                }
            },
            'dire': {
                'present': {
                    'je': 'je dis', 'tu': 'tu dis', 'il': 'il dit', 'elle': 'elle dit',
                    'nous': 'nous disons', 'vous': 'vous dites', 'ils': 'ils disent', 'elles': 'elles disent'
                }
            },
            'pouvoir': {
                'present': {
                    'je': 'je peux', 'tu': 'tu peux', 'il': 'il peut', 'elle': 'elle peut',
                    'nous': 'nous pouvons', 'vous': 'vous pouvez', 'ils': 'ils peuvent', 'elles': 'elles peuvent'
                }
            },
            'vouloir': {
                'present': {
                    'je': 'je veux', 'tu': 'tu veux', 'il': 'il veut', 'elle': 'elle veut',
                    'nous': 'nous voulons', 'vous': 'vous voulez', 'ils': 'ils veulent', 'elles': 'elles veulent'
                }
            },
            'voir': {
                'present': {
                    'je': 'je vois', 'tu': 'tu vois', 'il': 'il voit', 'elle': 'elle voit',
                    'nous': 'nous voyons', 'vous': 'vous voyez', 'ils': 'ils voient', 'elles': 'elles voient'
                }
            },
            'savoir': {
                'present': {
                    'je': 'je sais', 'tu': 'tu sais', 'il': 'il sait', 'elle': 'elle sait',
                    'nous': 'nous savons', 'vous': 'vous savez', 'ils': 'ils savent', 'elles': 'elles savent'
                }
            },
            'venir': {
                'present': {
                    'je': 'je viens', 'tu': 'tu viens', 'il': 'il vient', 'elle': 'elle vient',
                    'nous': 'nous venons', 'vous': 'vous venez', 'ils': 'ils viennent', 'elles': 'elles viennent'
                }
            },
            'partir': {
                'present': {
                    'je': 'je pars', 'tu': 'tu pars', 'il': 'il part', 'elle': 'elle part',
                    'nous': 'nous partons', 'vous': 'vous partez', 'ils': 'ils partent', 'elles': 'elles partent'
                }
            },
            'sortir': {
                'present': {
                    'je': 'je sors', 'tu': 'tu sors', 'il': 'il sort', 'elle': 'elle sort',
                    'nous': 'nous sortons', 'vous': 'vous sortez', 'ils': 'ils sortent', 'elles': 'elles sortent'
                }
            },
            'dormir': {
                'present': {
                    'je': 'je dors', 'tu': 'tu dors', 'il': 'il dort', 'elle': 'elle dort',
                    'nous': 'nous dormons', 'vous': 'vous dormez', 'ils': 'ils dorment', 'elles': 'elles dorment'
                }
            },
            'boire': {
                'present': {
                    'je': 'je bois', 'tu': 'tu bois', 'il': 'il boit', 'elle': 'elle boit',
                    'nous': 'nous buvons', 'vous': 'vous buvez', 'ils': 'ils boivent', 'elles': 'elles boivent'
                }
            },
            'prendre': {
                'present': {
                    'je': 'je prends', 'tu': 'tu prends', 'il': 'il prend', 'elle': 'elle prend',
                    'nous': 'nous prenons', 'vous': 'vous prenez', 'ils': 'ils prennent', 'elles': 'elles prennent'
                }
            },
            'écrire': {
                'present': {
                    'je': "j'écris", 'tu': 'tu écris', 'il': 'il écrit', 'elle': 'elle écrit',
                    'nous': 'nous écrivons', 'vous': 'vous écrivez', 'ils': 'ils écrivent', 'elles': 'elles écrivent'
                }
            },
            'lire': {
                'present': {
                    'je': 'je lis', 'tu': 'tu lis', 'il': 'il lit', 'elle': 'elle lit',
                    'nous': 'nous lisons', 'vous': 'vous lisez', 'ils': 'ils lisent', 'elles': 'elles lisent'
                }
            },
            'comprendre': {
                'present': {
                    'je': 'je comprends', 'tu': 'tu comprends', 'il': 'il comprend', 'elle': 'elle comprend',
                    'nous': 'nous comprenons', 'vous': 'vous comprenez', 'ils': 'ils comprennent', 'elles': 'elles comprennent'
                }
            },
            'apprendre': {
                'present': {
                    'je': "j'apprends", 'tu': 'tu apprends', 'il': 'il apprend', 'elle': 'elle apprend',
                    'nous': 'nous apprenons', 'vous': 'vous apprenez', 'ils': 'ils apprennent', 'elles': 'elles apprennent'
                }
            }
        }
    
    def needs_apostrophe(self, verb):
        """Détermine si le verbe nécessite une apostrophe avec 'je'"""
        return verb.lower().startswith(('a', 'e', 'i', 'o', 'u', 'h', 'à', 'á', 'â', 'ä', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ò', 'ó', 'ô', 'ö', 'ù', 'ú', 'û', 'ü'))
    
    def get_verb_group(self, verb):
        """Détermine le groupe du verbe"""
        verb_lower = verb.lower()
        
        # Verbes du 1er groupe (-er)
        if verb_lower.endswith('er') and verb_lower not in ['aller']:
            return 1
        
        # Verbes du 2ème groupe (-ir avec -issons)
        if verb_lower.endswith('ir') and verb_lower in ['finir', 'choisir', 'agir', 'réfléchir']:
            return 2
        
        # Verbes du 3ème groupe (tout le reste)
        return 3
    
    def conjugate_first_group(self, verb, pronoun):
        """Conjugue un verbe du 1er groupe (-er)"""
        root = verb[:-2]  # Enlever 'er'
        
        endings = {
            'je': 'e', 'tu': 'es', 'il': 'e', 'elle': 'e',
            'nous': 'ons', 'vous': 'ez', 'ils': 'ent', 'elles': 'ent'
        }
        
        conjugated_verb = root + endings[pronoun]
        
        # Gestion des contractions
        if pronoun == 'je' and self.needs_apostrophe(conjugated_verb):
            return f"j'{conjugated_verb}"
        else:
            return f"{pronoun} {conjugated_verb}"
    
    def conjugate_second_group(self, verb, pronoun):
        """Conjugue un verbe du 2ème groupe (-ir)"""
        root = verb[:-2]  # Enlever 'ir'
        
        endings = {
            'je': 'is', 'tu': 'is', 'il': 'it', 'elle': 'it',
            'nous': 'issons', 'vous': 'issez', 'ils': 'issent', 'elles': 'issent'
        }
        
        conjugated_verb = root + endings[pronoun]
        
        if pronoun == 'je' and self.needs_apostrophe(conjugated_verb):
            return f"j'{conjugated_verb}"
        else:
            return f"{pronoun} {conjugated_verb}"
    
    def conjugate_verb(self, verb, pronoun, tense='present'):
        """Conjugue un verbe français"""
        verb_normalized = verb.lower()
        pronoun_normalized = pronoun.lower()
        
        # Vérifier les verbes irréguliers
        if verb_normalized in self.irregular_verbs:
            if tense in self.irregular_verbs[verb_normalized]:
                if pronoun_normalized in self.irregular_verbs[verb_normalized][tense]:
                    return self.irregular_verbs[verb_normalized][tense][pronoun_normalized]
        
        # Conjugaison par groupe
        group = self.get_verb_group(verb_normalized)
        
        if group == 1:
            return self.conjugate_first_group(verb_normalized, pronoun_normalized)
        elif group == 2:
            return self.conjugate_second_group(verb_normalized, pronoun_normalized)
        else:
            # Pour le 3ème groupe, retour par défaut (à améliorer si nécessaire)
            if pronoun_normalized == 'je' and self.needs_apostrophe(verb_normalized):
                return f"j'{verb_normalized}"
            else:
                return f"{pronoun_normalized} {verb_normalized}"

def test_conjugator():
    """Teste le conjugateur français"""
    conjugator = FrenchConjugator()
    
    test_verbs = ['abîmer', 'être', 'avoir', 'parler', 'finir', 'écouter', 'manger']
    pronouns = ['je', 'tu', 'il', 'nous', 'vous', 'ils']
    
    print("=== TEST DU CONJUGATEUR FRANÇAIS ===")
    
    for verb in test_verbs:
        print(f"\nVerbe: {verb}")
        for pronoun in pronouns:
            conjugated = conjugator.conjugate_verb(verb, pronoun)
            print(f"  {conjugated}")

if __name__ == "__main__":
    test_conjugator()