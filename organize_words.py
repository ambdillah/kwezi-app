#!/usr/bin/env python3
"""
Script to organize words alphabetically by category in server.py
"""
import re
import json

def extract_words_from_server():
    """Extract all words from server.py"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all word entries using regex
    word_pattern = r'\{"french": "([^"]+)", "shimaore": "([^"]*)", "kibouchi": "([^"]*)", "category": "([^"]+)", "difficulty": (\d+)\}'
    matches = re.findall(word_pattern, content)
    
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
    
    # Sort each category alphabetically by French word
    for category in words_by_category:
        words_by_category[category].sort(key=lambda x: x['french'].lower())
    
    return words_by_category

def generate_organized_words_section(words_by_category):
    """Generate the organized words section"""
    lines = []
    lines.append("    # Contenu authentique complet en shimaoré et kibouchi basé sur les tableaux fournis (version finale organisée alphabétiquement)")
    lines.append("    base_words = [")
    
    # Define category order and French names
    category_info = {
        'salutations': 'Salutations et expressions courantes',
        'grammaire': 'Grammaire complète : Pronoms personnels, possessifs et métiers',
        'famille': 'Famille (vocabulaire familial étendu)',
        'couleurs': 'Couleurs (palette complète)',
        'animaux': 'Animaux (liste complète mise à jour)',
        'nombres': 'Nombres (corrigés)',
        'corps': 'Corps humain (mise à jour complète)',
        'nourriture': 'Nourriture (mise à jour complète)',
        'maison': 'Maison (section complète)',
        'vetements': 'Vêtements (section complète)',
        'verbes': 'Verbes d\'action complets (basés sur les 5 tableaux fournis)',
        'nature': 'Nature (mise à jour complète)',
        'adjectifs': 'Adjectifs (section complète)',
        'expressions': 'Expressions (section complète)',
        'transport': 'Transport (section complète)',
        'tradition': 'Tradition (éléments culturels de Mayotte)'
    }
    
    # Process categories in logical order
    category_order = ['salutations', 'grammaire', 'famille', 'couleurs', 'animaux', 'nombres', 
                     'corps', 'nourriture', 'maison', 'vetements', 'verbes', 'nature', 
                     'adjectifs', 'expressions', 'transport', 'tradition']
    
    for category in category_order:
        if category in words_by_category:
            words = words_by_category[category]
            if words:
                lines.append(f"        # {category_info.get(category, category.title())}")
                for word in words:
                    line = f'        {{"french": "{word["french"]}", "shimaore": "{word["shimaore"]}", "kibouchi": "{word["kibouchi"]}", "category": "{word["category"]}", "difficulty": {word["difficulty"]}}}'
                    if word != words[-1] or category != category_order[-1]:
                        line += ","
                    lines.append(line)
                lines.append("")
    
    lines.append("    ]")
    return "\n".join(lines)

def create_new_server_file(words_by_category):
    """Create new server.py with organized words"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the start and end of the base_words section
    start_pattern = r'    # Contenu authentique complet.*?\n    base_words = \['
    end_pattern = r'    \]'
    
    # Find the positions
    start_match = re.search(start_pattern, content, re.DOTALL)
    if not start_match:
        print("Could not find start of base_words section")
        return False
    
    start_pos = start_match.start()
    
    # Find the end position after the start
    remaining_content = content[start_match.end():]
    end_match = re.search(end_pattern, remaining_content)
    if not end_match:
        print("Could not find end of base_words section")
        return False
    
    end_pos = start_match.end() + end_match.end()
    
    # Generate new organized section
    new_words_section = generate_organized_words_section(words_by_category)
    
    # Replace the section
    new_content = content[:start_pos] + new_words_section + content[end_pos:]
    
    # Write the new file
    with open('/app/backend/server.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    print("🔄 Extracting words from server.py...")
    words_by_category = extract_words_from_server()
    
    print("📊 Words found by category:")
    total_words = 0
    for category, words in words_by_category.items():
        print(f"  {category}: {len(words)} mots")
        total_words += len(words)
    print(f"  Total: {total_words} mots")
    
    print("\n🔤 Organizing words alphabetically by category...")
    success = create_new_server_file(words_by_category)
    
    if success:
        print("✅ server.py has been successfully reorganized with alphabetical sorting!")
        print("📝 All words are now sorted alphabetically within their respective categories.")
    else:
        print("❌ Failed to reorganize server.py")

if __name__ == "__main__":
    main()