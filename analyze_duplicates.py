#!/usr/bin/env python3
"""
Script to analyze and remove all duplicates across all sections
"""
import re
from collections import defaultdict

def extract_all_words():
    """Extract all words from server.py and identify duplicates"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all word entries
    word_pattern = r'\{"french": "([^"]+)", "shimaore": "([^"]*)", "kibouchi": "([^"]*)", "category": "([^"]+)", "difficulty": (\d+)\}'
    matches = re.findall(word_pattern, content)
    
    # Group by French word to find duplicates
    words_by_french = defaultdict(list)
    all_words = []
    
    for match in matches:
        french, shimaore, kibouchi, category, difficulty = match
        
        word_entry = {
            'french': french,
            'shimaore': shimaore,
            'kibouchi': kibouchi,
            'category': category,
            'difficulty': int(difficulty)
        }
        
        words_by_french[french].append(word_entry)
        all_words.append(word_entry)
    
    # Find duplicates
    duplicates = {}
    for french, entries in words_by_french.items():
        if len(entries) > 1:
            duplicates[french] = entries
    
    print(f"📊 Analysis Results:")
    print(f"Total words found: {len(all_words)}")
    print(f"Unique French words: {len(words_by_french)}")
    print(f"Duplicated words: {len(duplicates)}")
    
    if duplicates:
        print(f"\n🔍 Duplicates found:")
        for french, entries in duplicates.items():
            print(f"\n'{french}' appears in {len(entries)} places:")
            for i, entry in enumerate(entries, 1):
                print(f"  {i}. Category: {entry['category']}, Shimaoré: '{entry['shimaore']}', Kibouchi: '{entry['kibouchi']}'")
    
    return words_by_french, duplicates, all_words

def decide_best_entry(french, entries):
    """Decide which entry to keep when there are duplicates"""
    
    # Category priority rules - some words belong better in certain categories
    category_priorities = {
        # Body parts should stay in corps
        'corps': ['Bouche', 'Œil', 'Nez', 'Oreille', 'Main', 'Pied', 'Tête', 'Ventre', 'Dent', 'Langue'],
        
        # Animals should stay in animaux
        'animaux': ['Poisson', 'Crevette', 'Chat', 'Chien', 'Oiseau'],
        
        # Food items should generally be in nourriture unless they're more about the animal
        'nourriture': ['Crevettes', 'Langouste', 'Viande', 'Lait', 'Œuf'],
        
        # Numbers should stay in nombres
        'nombres': ['Un', 'Deux', 'Trois', 'Quatre', 'Cinq', 'Six', 'Sept', 'Huit', 'Neuf', 'Dix'],
        
        # Verbs should stay in verbes
        'verbes': []  # Will be filled with verbs if needed
    }
    
    # Check if this word has a preferred category
    for category, preferred_words in category_priorities.items():
        if french in preferred_words:
            # Find entry in preferred category
            for entry in entries:
                if entry['category'] == category:
                    print(f"  → Keeping '{french}' in '{category}' (preferred category)")
                    return entry
    
    # If no specific preference, choose based on logic:
    # 1. If one entry has more complete translations (non-empty shimaoré and kibouchi)
    complete_entries = [e for e in entries if e['shimaore'].strip() and e['kibouchi'].strip()]
    if len(complete_entries) == 1:
        chosen = complete_entries[0]
        print(f"  → Keeping '{french}' in '{chosen['category']}' (most complete translations)")
        return chosen
    
    # 2. If multiple complete entries, prefer certain categories over others
    category_preference_order = ['corps', 'famille', 'salutations', 'grammaire', 'couleurs', 'nombres', 
                               'nourriture', 'animaux', 'maison', 'vetements', 'nature', 'verbes', 
                               'adjectifs', 'expressions', 'transport', 'tradition']
    
    for preferred_cat in category_preference_order:
        for entry in entries:
            if entry['category'] == preferred_cat and entry in (complete_entries if complete_entries else entries):
                print(f"  → Keeping '{french}' in '{preferred_cat}' (category preference)")
                return entry
    
    # 3. As last resort, keep the first entry
    chosen = entries[0]
    print(f"  → Keeping '{french}' in '{chosen['category']}' (first occurrence)")
    return chosen

def remove_duplicates(words_by_french, duplicates):
    """Remove duplicates and keep the best entry for each word"""
    
    print(f"\n🛠️ Removing duplicates...")
    
    unique_words = {}
    removed_count = 0
    
    for french, entries in words_by_french.items():
        if french in duplicates:
            # Choose the best entry
            best_entry = decide_best_entry(french, entries)
            unique_words[french] = best_entry
            removed_count += len(entries) - 1
        else:
            # No duplicates, keep the single entry
            unique_words[french] = entries[0]
    
    print(f"\n📊 Deduplication Results:")
    print(f"Words removed: {removed_count}")
    print(f"Unique words remaining: {len(unique_words)}")
    
    return unique_words

def organize_words_by_category(unique_words):
    """Organize unique words by category"""
    words_by_category = defaultdict(list)
    
    for french, word in unique_words.items():
        words_by_category[word['category']].append(word)
    
    # Sort each category appropriately
    for category in words_by_category:
        if category == "nombres":
            # Sort numbers numerically
            number_order = [
                "Un", "Deux", "Trois", "Quatre", "Cinq", "Six", "Sept", "Huit", "Neuf", "Dix",
                "Onze", "Douze", "Treize", "Quatorze", "Quinze", "Seize", "Dix-sept", "Dix-huit", "Dix-neuf", "Vingt"
            ]
            order_map = {word: i for i, word in enumerate(number_order)}
            words_by_category[category].sort(key=lambda x: order_map.get(x['french'], 999))
        else:
            # Sort alphabetically
            words_by_category[category].sort(key=lambda x: x['french'].lower())
    
    return words_by_category

def main():
    print("🔄 Analyzing all sections for duplicates...")
    words_by_french, duplicates, all_words = extract_all_words()
    
    if not duplicates:
        print("✅ No duplicates found! All words are unique.")
        return
    
    print(f"\n🔧 Processing {len(duplicates)} duplicated words...")
    unique_words = remove_duplicates(words_by_french, duplicates)
    
    words_by_category = organize_words_by_category(unique_words)
    
    print(f"\n📋 Final word count by category:")
    total = 0
    for category, words in words_by_category.items():
        print(f"  {category}: {len(words)} words")
        total += len(words)
    print(f"  TOTAL: {total} words")
    
    return words_by_category

if __name__ == "__main__":
    main()