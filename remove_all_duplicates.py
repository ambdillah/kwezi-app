#!/usr/bin/env python3
"""
Script to remove all duplicates and rebuild server.py
"""
import re
from collections import defaultdict

def extract_and_deduplicate():
    """Extract all words and remove duplicates"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all word entries
    word_pattern = r'\{"french": "([^"]+)", "shimaore": "([^"]*)", "kibouchi": "([^"]*)", "category": "([^"]+)", "difficulty": (\d+)\}'
    matches = re.findall(word_pattern, content)
    
    # Group by French word to find duplicates
    words_by_french = defaultdict(list)
    
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
    
    # Decisions for specific duplicates based on analysis
    duplicate_decisions = {
        'Poisson': 'animaux',  # Animals (zoological context)
        'Bouche': 'corps',     # Body parts
        'Ongle': 'corps',      # Body parts
        'Bol': 'maison',       # House items
        'Clôture': 'maison',   # House items - keep first translation (Mraba/Mraba) 
        'Mur': 'maison',       # House items - keep first translation (Houra/Riba)
        'Toilette': 'maison',  # House items
        'Pirogue': 'nature'    # Nature context (traditional boat in natural setting)
    }
    
    # For Clôture and Mur, we need to specify which translation to keep
    specific_translations = {
        'Clôture': {'shimaore': 'Mraba', 'kibouchi': 'Mraba'},
        'Mur': {'shimaore': 'Houra', 'kibouchi': 'Riba'}
    }
    
    unique_words = {}
    duplicates_found = 0
    
    for french, entries in words_by_french.items():
        if len(entries) > 1:
            duplicates_found += len(entries) - 1
            
            # Use our decision logic
            if french in duplicate_decisions:
                preferred_category = duplicate_decisions[french]
                
                # Find the entry in preferred category
                chosen_entry = None
                for entry in entries:
                    if entry['category'] == preferred_category:
                        chosen_entry = entry
                        break
                
                # If we have specific translation preferences
                if french in specific_translations and chosen_entry:
                    chosen_entry['shimaore'] = specific_translations[french]['shimaore']
                    chosen_entry['kibouchi'] = specific_translations[french]['kibouchi']
                
                if chosen_entry:
                    unique_words[french] = chosen_entry
                    print(f"✅ Kept '{french}' in '{preferred_category}' category")
                else:
                    # Fallback to first entry
                    unique_words[french] = entries[0]
                    print(f"⚠️ Fallback: Kept first '{french}' entry")
            else:
                # No specific rule, keep first
                unique_words[french] = entries[0]
                print(f"⚠️ No rule for '{french}', kept first entry")
        else:
            # No duplicates
            unique_words[french] = entries[0]
    
    print(f"\n📊 Removed {duplicates_found} duplicate entries")
    print(f"📊 {len(unique_words)} unique words remaining")
    
    return unique_words

def organize_by_category(unique_words):
    """Organize words by category with proper sorting"""
    words_by_category = defaultdict(list)
    
    for french, word in unique_words.items():
        words_by_category[word['category']].append(word)
    
    # Sort each category appropriately
    for category in words_by_category:
        if category == "nombres":
            # Sort numbers numerically (1-20)
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

def generate_new_base_words(words_by_category):
    """Generate new base_words section without duplicates"""
    lines = []
    lines.append("    # Contenu authentique complet en shimaoré et kibouchi basé sur les tableaux fournis (version finale sans doublons)")
    lines.append("    base_words = [")
    
    # Category order
    category_order = ['salutations', 'grammaire', 'famille', 'couleurs', 'animaux', 'nombres', 
                     'corps', 'nourriture', 'maison', 'vetements', 'verbes', 'nature', 
                     'adjectifs', 'expressions', 'transport', 'tradition']
    
    category_info = {
        'salutations': 'Salutations et expressions courantes',
        'grammaire': 'Grammaire complète : Pronoms personnels, possessifs et métiers',
        'famille': 'Famille (vocabulaire familial étendu)',
        'couleurs': 'Couleurs (palette complète)',
        'animaux': 'Animaux (liste complète mise à jour)',
        'nombres': 'Nombres (organisés de 1 à 20)',
        'corps': 'Corps humain (mise à jour complète)',
        'nourriture': 'Nourriture (mise à jour complète)',
        'maison': 'Maison (section complète)',
        'vetements': 'Vêtements (section complète)',
        'verbes': 'Verbes d\'action complets (basés sur les 5 tableaux fournis) - doublons supprimés',
        'nature': 'Nature (mise à jour complète)',
        'adjectifs': 'Adjectifs (section complète)',
        'expressions': 'Expressions (section complète)',
        'transport': 'Transport (section complète)',
        'tradition': 'Tradition (éléments culturels de Mayotte)'
    }
    
    total_words = 0
    
    for i, category in enumerate(category_order):
        if category in words_by_category and words_by_category[category]:
            words = words_by_category[category]
            total_words += len(words)
            
            lines.append(f"        # {category_info.get(category, category.title())}")
            
            for j, word in enumerate(words):
                line = f'        {{"french": "{word["french"]}", "shimaore": "{word["shimaore"]}", "kibouchi": "{word["kibouchi"]}", "category": "{word["category"]}", "difficulty": {word["difficulty"]}}}'
                
                # Add comma except for the very last word
                if not (i == len(category_order) - 1 and j == len(words) - 1):
                    line += ","
                
                lines.append(line)
            
            lines.append("")  # Empty line after each category
    
    lines.append("    ]")
    
    print(f"📊 Final total: {total_words} unique words")
    
    return "\n".join(lines)

def rebuild_server_file(words_by_category):
    """Rebuild server.py without duplicates"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find base_words section
    start_pattern = r'    # Contenu authentique complet.*?\n    base_words = \['
    end_pattern = r'    \]'
    
    start_match = re.search(start_pattern, content, re.DOTALL)
    if not start_match:
        print("❌ Could not find start of base_words section")
        return False
    
    start_pos = start_match.start()
    
    # Find the end position
    remaining_content = content[start_match.end():]
    end_match = re.search(end_pattern, remaining_content)
    if not end_match:
        print("❌ Could not find end of base_words section")
        return False
    
    end_pos = start_match.end() + end_match.end()
    
    # Generate new section
    new_section = generate_new_base_words(words_by_category)
    
    # Replace
    new_content = content[:start_pos] + new_section + content[end_pos:]
    
    # Write
    with open('/app/backend/server.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    print("🔄 Removing all duplicates from all sections...")
    unique_words = extract_and_deduplicate()
    
    words_by_category = organize_by_category(unique_words)
    
    print(f"\n📋 Words by category after deduplication:")
    for category, words in words_by_category.items():
        print(f"  {category}: {len(words)} words")
    
    print("\n🔄 Rebuilding server.py...")
    success = rebuild_server_file(words_by_category)
    
    if success:
        print("✅ server.py successfully updated!")
        print("✅ All duplicates removed across all sections!")
        print("✅ Organization maintained (alphabetical + numerical for numbers)!")
    else:
        print("❌ Failed to update server.py")

if __name__ == "__main__":
    main()