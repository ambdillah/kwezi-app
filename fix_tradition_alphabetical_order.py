#!/usr/bin/env python3
"""
Script to fix alphabetical order in tradition section
"""
import re

def extract_and_sort_tradition_words():
    """Extract tradition words and sort them alphabetically"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all word entries
    word_pattern = r'\{"french": "([^"]+)", "shimaore": "([^"]*)", "kibouchi": "([^"]*)", "category": "([^"]+)", "difficulty": (\d+)\}'
    matches = re.findall(word_pattern, content)
    
    # Extract tradition words
    tradition_words = []
    for match in matches:
        french, shimaore, kibouchi, category, difficulty = match
        if category == "tradition":
            tradition_words.append({
                'french': french,
                'shimaore': shimaore,
                'kibouchi': kibouchi,
                'category': category,
                'difficulty': int(difficulty)
            })
    
    # Sort alphabetically by French word
    tradition_words.sort(key=lambda x: x['french'].lower())
    
    print(f"📚 Tradition words in correct alphabetical order:")
    for i, word in enumerate(tradition_words, 1):
        print(f"{i:2d}. {word['french']}")
    
    return tradition_words

def rebuild_tradition_section(tradition_words):
    """Rebuild the tradition section with correct alphabetical order"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate new tradition section
    lines = []
    lines.append("        # Tradition (éléments culturels de Mayotte)")
    
    for i, word in enumerate(tradition_words):
        line = f'        {{"french": "{word["french"]}", "shimaore": "{word["shimaore"]}", "kibouchi": "{word["kibouchi"]}", "category": "{word["category"]}", "difficulty": {word["difficulty"]}}}'
        if i < len(tradition_words) - 1:  # Add comma except for last item
            line += ","
        lines.append(line)
    
    new_tradition_section = "\n".join(lines)
    
    # Find the tradition section boundaries
    start_pattern = r'        # Tradition \(éléments culturels de Mayotte\)\n'
    end_pattern = r'        \n    \]'
    
    # Find start
    start_match = re.search(start_pattern, content)
    if not start_match:
        print("❌ Could not find tradition section start")
        return False
    
    start_pos = start_match.start()
    
    # Find end (next section or end of array)
    remaining_content = content[start_match.end():]
    
    # Look for the next section comment or end of array
    next_section_pattern = r'\n        # [A-Z]'
    end_array_pattern = r'\n    \]'
    
    next_section_match = re.search(next_section_pattern, remaining_content)
    end_array_match = re.search(end_array_pattern, remaining_content)
    
    if next_section_match:
        end_pos = start_match.end() + next_section_match.start()
    elif end_array_match:
        end_pos = start_match.end() + end_array_match.start()
    else:
        print("❌ Could not find tradition section end")
        return False
    
    # Replace the tradition section
    new_content = content[:start_pos] + new_tradition_section + content[end_pos:]
    
    # Write the updated file
    with open('/app/backend/server.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    print("🔤 Fixing alphabetical order in tradition section...")
    
    # Extract and sort tradition words
    tradition_words = extract_and_sort_tradition_words()
    
    if len(tradition_words) != 16:
        print(f"⚠️ Expected 16 tradition words, found {len(tradition_words)}")
    
    # Rebuild the section
    success = rebuild_tradition_section(tradition_words)
    
    if success:
        print("✅ Tradition section successfully reordered alphabetically!")
        print("📚 'Fiançailles' is now in its correct alphabetical position!")
    else:
        print("❌ Failed to reorder tradition section")

if __name__ == "__main__":
    main()