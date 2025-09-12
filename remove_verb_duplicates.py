#!/usr/bin/env python3
"""
Script to remove duplicate verbs from server.py
"""
import re
import json

def find_and_remove_verb_duplicates():
    """Find and remove duplicate verbs from server.py"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all word entries using regex
    word_pattern = r'\{"french": "([^"]+)", "shimaore": "([^"]*)", "kibouchi": "([^"]*)", "category": "([^"]+)", "difficulty": (\d+)\}'
    matches = re.findall(word_pattern, content)
    
    # Extract verbs and identify duplicates
    verbs = []
    verb_seen = {}
    duplicates_found = []
    
    for match in matches:
        french, shimaore, kibouchi, category, difficulty = match
        
        if category == "verbes":
            word_entry = {
                'french': french,
                'shimaore': shimaore,
                'kibouchi': kibouchi,
                'category': category,
                'difficulty': int(difficulty)
            }
            
            # Check if this exact verb (french) has been seen before
            if french in verb_seen:
                # This is a duplicate
                duplicates_found.append(french)
                print(f"🔍 Duplicate found: {french}")
            else:
                # First occurrence, keep it
                verb_seen[french] = word_entry
                verbs.append(word_entry)
    
    print(f"\n📊 Summary:")
    print(f"Total verbs found: {len(matches) if 'verbes' in [m[3] for m in matches] else 'N/A'}")
    print(f"Unique verbs: {len(verbs)}")
    print(f"Duplicates found: {len(duplicates_found)}")
    print(f"Duplicates: {sorted(set(duplicates_found))}")
    
    return verbs, duplicates_found

def rebuild_server_file(unique_verbs):
    """Rebuild server.py with unique verbs only"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the verbs section
    verb_start_pattern = r'(        # Vêtements \(section complète\)\n.*?\n        \n)'
    verb_end_pattern = r'(        \n        # Nature \(mise à jour complète\))'
    
    start_match = re.search(verb_start_pattern, content, re.DOTALL)
    end_match = re.search(verb_end_pattern, content, re.DOTALL)
    
    if not start_match or not end_match:
        print("❌ Could not find verbs section boundaries")
        return False
    
    # Build new verbs section
    verbs_lines = []
    verbs_lines.append("        # Verbes d'action complets (basés sur les 5 tableaux fournis)")
    
    # Sort verbs alphabetically
    unique_verbs.sort(key=lambda x: x['french'].lower())
    
    for i, verb in enumerate(unique_verbs):
        line = f'        {{"french": "{verb["french"]}", "shimaore": "{verb["shimaore"]}", "kibouchi": "{verb["kibouchi"]}", "category": "{verb["category"]}", "difficulty": {verb["difficulty"]}}}'
        if i < len(unique_verbs) - 1:  # Add comma except for last item
            line += ","
        verbs_lines.append(line)
    
    verbs_lines.append("")  # Empty line after verbs section
    
    new_verbs_section = "\n".join(verbs_lines)
    
    # Replace the verbs section
    before_verbs = content[:start_match.end()]
    after_verbs = content[end_match.start():]
    
    new_content = before_verbs + new_verbs_section + after_verbs
    
    # Write the new file
    with open('/app/backend/server.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    print("🔄 Finding duplicate verbs in server.py...")
    unique_verbs, duplicates = find_and_remove_verb_duplicates()
    
    if len(duplicates) > 0:
        print(f"\n🛠️ Rebuilding server.py with {len(unique_verbs)} unique verbs...")
        success = rebuild_server_file(unique_verbs)
        
        if success:
            print("✅ server.py has been successfully updated!")
            print(f"📝 Removed {len(duplicates)} duplicate verb entries.")
            print(f"📝 {len(unique_verbs)} unique verbs remain, sorted alphabetically.")
        else:
            print("❌ Failed to rebuild server.py")
    else:
        print("✅ No duplicates found in verbs section!")

if __name__ == "__main__":
    main()