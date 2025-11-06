#!/usr/bin/env python3
"""
Script d'analyse des préfixes de verbes dans toutes les phrases
Identifie tous les préfixes uniques utilisés pour améliorer la coloration
"""

from pymongo import MongoClient
from collections import defaultdict
import re

def main():
    print("=" * 80)
    print("ANALYSE COMPLÈTE DES PRÉFIXES DE VERBES")
    print("=" * 80)
    print()
    
    # Connexion à MongoDB
    client = MongoClient("mongodb://localhost:27017")
    db = client["mayotte_app"]
    
    # Préfixes actuellement reconnus
    KNOWN_SHIMAORE_PREFIXES = {
        'present': {'nis', 'ous', 'as', 'ris', 'mous', 'was'},
        'past': {'naco', 'waco', 'aco', 'raco', 'mwaco'},
        'future': {'nitso', 'outso', 'atso', 'ritso', 'moutso', 'watso'}
    }
    
    KNOWN_KIBOUCHI_PREFIXES = {
        'present': {'za', 'ana', 'izi', 'zéheyi', 'anaréou', 'réou'},
        'past': {'ni'},
        'future': {'bou'}
    }
    
    # Mots à ignorer (pronoms, articles, conjonctions)
    IGNORE_WORDS_SHIM = {
        'wami', 'wawe', 'waye', 'wasi', 'wagnou', 'wawo',
        'na', 'ya', 'la', 'de', 'le', 'un', 'une', 'et'
    }
    
    IGNORE_WORDS_KIB = {
        'zahou', 'anaou', 'izi', 'atsika', 'anarou', 'rou',
        'za', 'ana', 'na', 'ya'
    }
    
    # Récupérer toutes les phrases
    sentences = list(db.sentences.find({}, {
        'french': 1,
        'shimaore': 1,
        'kibouchi': 1,
        'shimaore_words': 1,
        'kibouchi_words': 1,
        'tense': 1
    }))
    
    print(f"Total de phrases à analyser: {len(sentences)}")
    print()
    
    # Collecter les verbes par temps
    shimaore_verbs_by_tense = defaultdict(set)
    kibouchi_verbs_by_tense = defaultdict(set)
    
    for sent in sentences:
        tense = sent.get('tense', 'unknown')
        
        # Analyser shimaoré
        shim_words = sent.get('shimaore_words', [])
        for word in shim_words:
            word_lower = word.lower().strip()
            
            # Ignorer les mots connus
            if word_lower in IGNORE_WORDS_SHIM:
                continue
            
            # Ignorer les mots très courts
            if len(word_lower) < 3:
                continue
            
            # Vérifier si ce n'est pas déjà reconnu
            is_known = False
            for known_prefixes in KNOWN_SHIMAORE_PREFIXES.values():
                for prefix in known_prefixes:
                    if word_lower.startswith(prefix):
                        is_known = True
                        break
                if is_known:
                    break
            
            if not is_known:
                shimaore_verbs_by_tense[tense].add(word)
        
        # Analyser kibouchi
        kib_words = sent.get('kibouchi_words', [])
        for word in kib_words:
            word_lower = word.lower().strip()
            
            # Ignorer les mots connus
            if word_lower in IGNORE_WORDS_KIB:
                continue
            
            # Ignorer les mots très courts
            if len(word_lower) < 3:
                continue
            
            # Vérifier si ce n'est pas déjà reconnu
            is_known = False
            for known_prefixes in KNOWN_KIBOUCHI_PREFIXES.values():
                for prefix in known_prefixes:
                    if word_lower.startswith(prefix):
                        is_known = True
                        break
                if is_known:
                    break
            
            if not is_known:
                kibouchi_verbs_by_tense[tense].add(word)
    
    # Afficher les résultats
    print("🔍 MOTS SHIMAORÉ NON RECONNUS PAR TEMPS")
    print("-" * 80)
    for tense in ['present', 'past', 'future']:
        words = shimaore_verbs_by_tense.get(tense, set())
        print(f"\n{tense.upper()} ({len(words)} mots):")
        for word in sorted(words)[:20]:  # Afficher les 20 premiers
            print(f"  • {word}")
    
    print()
    print("=" * 80)
    print("🔍 MOTS KIBOUCHI NON RECONNUS PAR TEMPS")
    print("-" * 80)
    for tense in ['present', 'past', 'future']:
        words = kibouchi_verbs_by_tense.get(tense, set())
        print(f"\n{tense.upper()} ({len(words)} mots):")
        for word in sorted(words)[:20]:  # Afficher les 20 premiers
            print(f"  • {word}")
    
    print()
    print("=" * 80)
    print("📊 ANALYSE DES PRÉFIXES POTENTIELS")
    print("=" * 80)
    print()
    
    # Essayer de détecter les préfixes communs
    def extract_common_prefixes(words_set, max_prefix_length=5):
        """Extrait les préfixes communs d'un ensemble de mots"""
        prefix_counts = defaultdict(int)
        
        for word in words_set:
            word_lower = word.lower()
            for length in range(2, min(max_prefix_length + 1, len(word_lower))):
                prefix = word_lower[:length]
                prefix_counts[prefix] += 1
        
        # Garder seulement les préfixes qui apparaissent plusieurs fois
        common_prefixes = {prefix: count for prefix, count in prefix_counts.items() if count >= 3}
        return dict(sorted(common_prefixes.items(), key=lambda x: x[1], reverse=True))
    
    print("SHIMAORÉ - Préfixes potentiels par temps:")
    for tense in ['present', 'past', 'future']:
        words = shimaore_verbs_by_tense.get(tense, set())
        if words:
            prefixes = extract_common_prefixes(words)
            print(f"\n  {tense}:")
            for prefix, count in list(prefixes.items())[:10]:
                print(f"    '{prefix}' apparaît {count} fois")
    
    print()
    print("KIBOUCHI - Préfixes potentiels par temps:")
    for tense in ['present', 'past', 'future']:
        words = kibouchi_verbs_by_tense.get(tense, set())
        if words:
            prefixes = extract_common_prefixes(words)
            print(f"\n  {tense}:")
            for prefix, count in list(prefixes.items())[:10]:
                print(f"    '{prefix}' apparaît {count} fois")
    
    print()
    print("=" * 80)
    print("✅ ANALYSE TERMINÉE")
    print("=" * 80)

if __name__ == "__main__":
    main()
