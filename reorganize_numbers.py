#!/usr/bin/env python3
"""
Script to reorganize numbers in numerical order (1 to 20) instead of alphabetical
"""
import re

def extract_all_words():
    """Extract all words from server.py"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all word entries
    word_pattern = r'\{"french": "([^"]+)", "shimaore": "([^"]*)", "kibouchi": "([^"]*)", "category": "([^"]+)", "difficulty": (\d+)\}'
    matches = re.findall(word_pattern, content)
    
    # Group by category
    words_by_category = {}
    
    for match in matches:
        french, shimaore, kibouchi, category, difficulty = match
        
        if category not in words_by_category:
            words_by_category[category] = []
        
        words_by_category[category].append({
            'french': french,
            'shimaore': shimaore,
            'kibouchi': kibouchi,
            'category': category,
            'difficulty': int(difficulty)
        })
    
    # Sort each category - SPECIAL handling for numbers
    for category in words_by_category:
        if category == "nombres":
            # Sort numbers in numerical order (1 to 20)
            number_order = [
                "Un", "Deux", "Trois", "Quatre", "Cinq", "Six", "Sept", "Huit", "Neuf", "Dix",
                "Onze", "Douze", "Treize", "Quatorze", "Quinze", "Seize", "Dix-sept", "Dix-huit", "Dix-neuf", "Vingt"
            ]
            
            # Create a mapping for proper order
            order_map = {word: i for i, word in enumerate(number_order)}
            
            # Sort by numerical order
            words_by_category[category].sort(key=lambda x: order_map.get(x['french'], 999))
            
            print(f"📊 Numbers organized in numerical order (1-20):")
            for word in words_by_category[category]:
                print(f"   {word['french']}")
        else:
            # Sort alphabetically for all other categories
            words_by_category[category].sort(key=lambda x: x['french'].lower())
    
    return words_by_category

def generate_new_base_words(words_by_category):
    """Generate new base_words section with numbers in numerical order"""
    lines = []
    lines.append("    # Contenu authentique complet en shimaoré et kibouchi basé sur les tableaux fournis (version finale organisée alphabétiquement sauf nombres)")
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
    
    print(f"📊 Total words: {total_words}")
    print(f"📊 Numbers in category: {len(words_by_category.get('nombres', []))}")
    
    return "\n".join(lines)

def rebuild_server_file(words_by_category):
    """Rebuild the entire server.py file with numbers in numerical order"""
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
    print("🔄 Extracting all words and reorganizing numbers numerically...")
    words_by_category = extract_all_words()
    
    print("\n🔄 Rebuilding server.py with numbers in numerical order (1-20)...")
    success = rebuild_server_file(words_by_category)
    
    if success:
        print("✅ server.py successfully updated!")
        print("✅ Numbers are now organized numerically (1-20) instead of alphabetically!")
        print("✅ All other categories remain alphabetically sorted!")
    else:
        print("❌ Failed to update server.py")

if __name__ == "__main__":
    main()