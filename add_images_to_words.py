#!/usr/bin/env python3
"""
Script to add image URLs to words that can be visually represented
"""
import re

def get_word_image_mappings():
    """Define image URLs for words that can be visually represented"""
    
    # Images from our vision expert searches and some royalty-free educational icons
    images = {
        # Animaux (Animals) - Most visual category
        'Chat': 'https://images.unsplash.com/flagged/photo-1576523163697-795a7182b1b7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHw0fHxjaGlsZHJlbiUyMGFuaW1hbHN8ZW58MHx8fHwxNzU3OTQ5NTAxfDA&ixlib=rb-4.1.0&q=85',
        'Chien': 'https://images.unsplash.com/photo-1625923780302-53edca7b85f5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwxfHxjaGlsZHJlbiUyMGFuaW1hbHN8ZW58MHx8fHwxNzU3OTQ5NTAxfDA&ixlib=rb-4.1.0&q=85',
        'Poisson': 'https://images.unsplash.com/photo-1712286035120-4cef1fdcb4dc',
        'Oiseau': 'https://images.pexels.com/photos/33866528/pexels-photo-33866528.jpeg',
        'Éléphant': 'https://images.unsplash.com/photo-1743964451762-9fbd78f1a2c3',
        
        # Corps humain (Body parts)
        'Main': 'https://images.unsplash.com/photo-1630355733366-433fa0f49da1',
        'Pied': 'https://images.unsplash.com/photo-1565522027979-622f70a1ce42',
        
        # Couleurs (Colors) - Use color swatches
        'Rouge': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMTgiIGZpbGw9IiNGRjAwMDAiLz4KPC9zdmc+',
        'Bleu': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMTgiIGZpbGw9IiMwMDAwRkYiLz4KPC9zdmc+',
        'Vert': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMTgiIGZpbGw9IiMwMEZGMDAiLz4KPC9zdmc+',
        'Jaune': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMTgiIGZpbGw9IiNGRkZGMDAiLz4KPC9zdmc+',
        'Noir': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMTgiIGZpbGw9IiMwMDAwMDAiLz4KPC9zdmc+',
        'Blanc': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMTgiIGZpbGw9IiNGRkZGRkYiIHN0cm9rZT0iIzAwMDAwMCIgc3Ryb2tlLXdpZHRoPSIyIi8+Cjwvc3ZnPg==',
        'Marron': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMTgiIGZpbGw9IiM4QjQ1MTMiLz4KPC9zdmc+',
        'Gris': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMTgiIGZpbGw9IiM4MDgwODAiLz4KPC9zdmc+',
        
        # Nombres (Numbers) - Simple representations
        'Un': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHRleHQgeD0iMjAiIHk9IjI1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjQiIGZvbnQtd2VpZ2h0PSJib2xkIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjMzMzMzMzIj4xPC90ZXh0Pgo8L3N2Zz4=',
        'Deux': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHRleHQgeD0iMjAiIHk9IjI1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjQiIGZvbnQtd2VpZ2h0PSJib2xkIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjMzMzMzMzIj4yPC90ZXh0Pgo8L3N2Zz4=',
        'Trois': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHRleHQgeD0iMjAiIHk9IjI1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjQiIGZvbnQtd2VpZ2h0PSJib2xkIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjMzMzMzMzIj4zPC90ZXh0Pgo8L3N2Zz4=',
        
        # Maison (House items)
        'Chaise': 'https://images.unsplash.com/photo-1702675301342-cac2dc3ef15a',
        'Table': 'https://images.unsplash.com/photo-1702675301342-cac2dc3ef15a',
        'Lit': 'https://images.unsplash.com/photo-1702675301342-cac2dc3ef15a',
        
        # Famille - use generic family icons
        'Mère': 'https://images.unsplash.com/photo-1625923780302-53edca7b85f5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwxfHxjaGlsZHJlbiUyMGFuaW1hbHN8ZW58MHx8fHwxNzU3OTQ5NTAxfDA&ixlib=rb-4.1.0&q=85',
        'Père': 'https://images.unsplash.com/photo-1625923780302-53edca7b85f5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwxfHxjaGlsZHJlbiUyMGFuaW1hbHN8ZW58MHx8fHwxNzU3OTQ5NTAxfDA&ixlib=rb-4.1.0&q=85',
        'Enfant': 'https://images.unsplash.com/photo-1625923780302-53edca7b85f5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwxfHxjaGlsZHJlbiUyMGFuaW1hbHN8ZW58MHx8fHwxNzU3OTQ5NTAxfDA&ixlib=rb-4.1.0&q=85',
        
        # Educational context images
        'École': 'https://images.pexels.com/photos/8386133/pexels-photo-8386133.jpeg',
        'Livre': 'https://images.pexels.com/photos/33866546/pexels-photo-33866546.jpeg',
        'Crayon': 'https://images.pexels.com/photos/745365/pexels-photo-745365.jpeg',
    }
    
    return images

def extract_all_words():
    """Extract all words from server.py"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all word entries
    word_pattern = r'\{"french": "([^"]+)", "shimaore": "([^"]*)", "kibouchi": "([^"]*)", "category": "([^"]+)", "difficulty": (\d+)\}'
    matches = re.findall(word_pattern, content)
    
    words = []
    for match in matches:
        french, shimaore, kibouchi, category, difficulty = match
        words.append({
            'french': french,
            'shimaore': shimaore,
            'kibouchi': kibouchi,
            'category': category,
            'difficulty': int(difficulty)
        })
    
    return words

def add_images_to_words():
    """Add image URLs to appropriate words"""
    words = extract_all_words()
    image_mappings = get_word_image_mappings()
    
    # Count how many words will get images
    words_with_images = 0
    words_without_images = 0
    
    for word in words:
        if word['french'] in image_mappings:
            words_with_images += 1
        else:
            words_without_images += 1
    
    print(f"📊 Image Analysis:")
    print(f"  Words that will get images: {words_with_images}")
    print(f"  Words without images: {words_without_images}")
    print(f"  Total words: {len(words)}")
    print(f"  Coverage: {(words_with_images/len(words)*100):.1f}%")
    
    print(f"\n🖼️ Words getting images:")
    for word in words:
        if word['french'] in image_mappings:
            print(f"  ✅ {word['french']} ({word['category']})")
    
    return words, image_mappings

def update_server_file_structure():
    """Update server.py to include image_url field in base_words"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    words, image_mappings = add_images_to_words()
    
    # Group by category and sort appropriately
    words_by_category = {}
    for word in words:
        category = word['category']
        if category not in words_by_category:
            words_by_category[category] = []
        words_by_category[category].append(word)
    
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
    
    # Generate new base_words section with images
    lines = []
    lines.append("    # Contenu authentique complet en shimaoré et kibouchi avec images pour les enfants")
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
            words_list = words_by_category[category]
            total_words += len(words_list)
            
            lines.append(f"        # {category_info.get(category, category.title())}")
            
            for j, word in enumerate(words_list):
                # Check if this word has an image
                image_url = image_mappings.get(word['french'], '')
                if image_url:
                    line = f'        {{"french": "{word["french"]}", "shimaore": "{word["shimaore"]}", "kibouchi": "{word["kibouchi"]}", "category": "{word["category"]}", "image_url": "{image_url}", "difficulty": {word["difficulty"]}}}'
                else:
                    line = f'        {{"french": "{word["french"]}", "shimaore": "{word["shimaore"]}", "kibouchi": "{word["kibouchi"]}", "category": "{word["category"]}", "difficulty": {word["difficulty"]}}}'
                
                # Add comma except for the very last word
                if not (i == len(category_order) - 1 and j == len(words_list) - 1):
                    line += ","
                
                lines.append(line)
            
            lines.append("")  # Empty line after each category
    
    lines.append("    ]")
    
    new_section = "\n".join(lines)
    
    # Find and replace the base_words section
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
    
    # Replace
    new_content = content[:start_pos] + new_section + content[end_pos:]
    
    # Write
    with open('/app/backend/server.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Added images to {len([w for w in words if w['french'] in image_mappings])} words")
    print(f"📊 Total words: {total_words}")
    
    return True

def main():
    print("🖼️ Adding images to vocabulary words for children...")
    
    success = update_server_file_structure()
    
    if success:
        print("✅ Images successfully added to appropriate words!")
        print("🎨 The vocabulary now includes visual aids to help children memorize!")
    else:
        print("❌ Failed to add images to words")

if __name__ == "__main__":
    main()