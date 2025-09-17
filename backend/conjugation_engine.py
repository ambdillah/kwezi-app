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
    """Moteur de conjugaison pour shimaoré et kibouchi"""
    
    def __init__(self):
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
    
    def create_sentence(self, subject_fr, verb_fr, verb_shimaore, verb_kibouchi, object_fr=None, object_shimaore=None, object_kibouchi=None, tense='present'):
        """Crée une phrase complète en français, shimaoré et kibouchi"""
        
        # Conjugaison
        shimaore_verb = self.conjugate_shimaore(verb_shimaore, subject_fr.lower(), tense)
        kibouchi_verb = self.conjugate_kibouchi(verb_kibouchi, subject_fr.lower(), tense)
        
        # Pronoms
        shimaore_pronoun = self.pronouns['shimaore'].get(subject_fr.lower(), subject_fr)
        kibouchi_pronoun = self.pronouns['kibouchi'].get(subject_fr.lower(), subject_fr)
        
        # Construction des phrases
        french_sentence = f"{subject_fr} {verb_fr}"
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
        
        print(f"\n✅ Moteur de conjugaison opérationnel!")
        print(f"📚 {sentences_created} phrases générées pour le jeu")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)