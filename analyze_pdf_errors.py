#!/usr/bin/env python3
"""
Analyse du PDF pour identifier les erreurs orthographiques, doublons et incohérences
dans le vocabulaire Shimaoré-Kibouchi
"""

import re
from collections import defaultdict
from typing import Dict, List, Tuple, Set
import json

# Données extraites du PDF (structure simplifiée pour l'analyse)
pdf_data = """
pente/coline/mont | mlima |  |  |
lune | mwézi |  |  |
étoile | gnora |  |  |
sable | mtsanga |  |  |
vague | dhouja |  |  |
vent | pévo |  |  |
pluie | vhoua |  |  |
mangrove | mhonko |  |  |
corail | soiyi |  |  |
barrière de corail | caléni |  |  |
tempête | darouba |  |  |
rivière | mouro |  |  |
pont | daradja |  |  |
nuage | wingou |  |  |
arc-en-ciel | mcacamba |  |  |
campagne/forêt |  |  |  |
caillou/pierre/rocher | malavouni |  |  |
plateau | bwé |  |  |
herbe | bandra |  |  |
chemin/sentier/parcours | ndzia |  |  |
fleur | malavou |  |  |
soleil | jouwa |  |  |
mer | bahari |  |  |
plage | mtsangani |  |  |
arbre | mwiri |  |  |
rue/route | paré |  |  |
bananier | trindri |  |  |
feuille | mawoini |  |  |
branche | trahi |  |  |
tornade | ouzimouyi |  |  |
cocotier | m'nadzi |  |  |
arbre à pain | m'frampé |  |  |
baobab | m'bouyou |  |  |
bambou | m'bambo |  |  |
manguier | m'manga |  |  |
jacquier | m'fénéssi |  |  |
terre | trotro |  |  |
sol | tsi |  |  |
érosion | padza |  |  |
marée basse | maji yavo |  |  |
platier | kalé |  |  |
marée haute | maji yamalé |  |  |
inondé | ourora |  |  |
sauvage | nyéha |  |  |
canne à sucre | mouwoi |  |  |
fagot | kouni |  |  |
pirogue | laka |  |  |
vedette | kwassa kwassa |  |  |
école | licoli |  |  |
école coranique | shioni |  |  |
un | moja |  |  |
deux | mbili |  |  |
trois | trarou |  |  |
quatre | nhé |  |  |
cinq | tsano |  |  |
six | sita |  |  |
sept | saba |  |  |
huit | nané |  |  |
neuf | chendra |  |  |
dix | koumi |  |  |
cochon | pouroukou |  |  |
margouillat | kasangwe |  |  |
abeille | niochi |  |  |
chat | paha |  |  |
rat | pouhou |  |  |
escargot | kwa |  |  |
lion | simba |  |  |
grenouille | shiwatrotro |  |  |
oiseau | gnougni |  |  |
chien | mbwa |  |  |
poisson | fi |  |  |
maki | komba |  |  |
chèvre | mbouzi |  |  |
moustique | manundri |  |  |
mouche | ndzi |  |  |
chauve-souris | drema |  |  |
serpent | nyoha |  |  |
lapin | sungura |  |  |
canard | guisi |  |  |
mouton | baribari |  |  |
crocodile | vwai |  |  |
caméléon | tarundru |  |  |
zébu | nyombé |  |  |
âne | pundra |  |  |
poule | kouhou |  |  |
pigeon | ndiwa |  |  |
fourmis | tsoussou |  |  |
chenille | bazi |  |  |
papillon | pelapelaka |  |  |
ver de terre | lingoui lingoui |  |  |
criquet | furudji |  |  |
cheval | poundra |  |  |
perroquet | kassoukou |  |  |
cafard | kalalawi |  |  |
araignée | shitrandrabwibwi |  |  |
scorpion | hala |  |  |
scolopendre | trambwi |  |  |
thon | mbassi |  |  |
requin | pwedza |  |  |
poulpe | dradraka |  |  |
crabe | nyamba/katsa |  |  |
tortue | bigorno |  |  |
éléphant | ndovu |  |  |
singe | djakwe |  |  |
souris | shikwetse |  |  |
facochère | pouruku nyeha |  |  |
lézard | ngwizi |  |  |
renard | mbwa nyeha |  |  |
chameau | ngamia |  |  |
escargot | kowa |  |  |
hérisson/tanrec | landra |  |  |
corbeau | gawa/kwayi |  |  |
civette | founga |  |  |
dauphin | moungoumé |  |  |
baleine | ndroujou |  |  |
crevette | camba |  |  |
frelon | chonga |  |  |
guêpe | movou |  |  |
bourdon | vungo vungo |  |  |
puce | kunguni |  |  |
poux | ndra |  |  |
bouc | béwé |  |  |
taureau | kondzo |  |  |
bigorneau | trondro |  |  |
lambis | kombé |  |  |
cône de mer | kwitsi |  |  |
gnomarée | gadzassi |  |  |
mille-pattes | mjongo |  |  |
oursin | gadzassi |  |  |
huître | gadzassi |  |  |
œil | matso |  |  |
nez | poua |  |  |
oreille | kiyo |  |  |
ongle | kofou |  |  |
front | housso |  |  |
joue | savou |  |  |
dos | mengo |  |  |
épaule | bèga |  |  |
hanche | trenga |  |  |
fesses | shidzé/mvoumo |  |  |
main | mhono |  |  |
tête | shitsoi |  |  |
ventre | mimba |  |  |
dent | magno |  |  |
langue | oulimé |  |  |
pied | mindrou |  |  |
lèvre | dhomo |  |  |
peau | ngwezi |  |  |
cheveux | ngnélé |  |  |
doigts | cha |  |  |
barbe | ndrévou |  |  |
vagin | ndzigni |  |  |
testicules | kwendzé |  |  |
pénis | mbo |  |  |
menton | shlevo |  |  |
bouche | hangno |  |  |
côtes | bavou |  |  |
sourcil | tsi |  |  |
cheville | dzitso la pwédza |  |  |
coup | tsingou |  |  |
cils | kové |  |  |
arrière du crâne | komoi |  |  |
Bonjour | Kwezi |  |  |
Comment ça va ? | jéjé |  |  |
Oui | ewa |  |  |
Non | an'ha |  |  |
Ça va bien | fétré |  |  |
Merci | marahaba |  |  |
Bonne nuit | oukou wa hairi |  |  |
Au revoir | kwaheri |  |  |
Je | wami |  |  |
Tu | wawé |  |  |
Il/Elle | wayé |  |  |
Nous | wassi |  |  |
Ils/Elles | wawo |  |  |
Boungou |  | boungou |  |
Fandzava |  | fandzava |  |
Lakintagna |  | lakintagna |  |
Fasigni |  | fasigni |  |
Houndza/riaka |  | houndza/riaka |  |
Tsikou |  | tsikou |  |
Mahaléni |  | mahaléini |  |
Honkou |  | honkou |  |
Soiyi |  | soiyi |  |
Caléni |  | caléni |  |
Tsikou |  | tsikou |  |
Mouroni |  | mouroni |  |
"""

def parse_pdf_data() -> List[Dict[str, str]]:
    """Parse les données du PDF et retourne une liste de dictionnaires"""
    entries = []
    lines = [line.strip() for line in pdf_data.strip().split('\n') if line.strip()]
    
    for line in lines:
        if '|' in line:
            parts = [part.strip() for part in line.split('|')]
            if len(parts) >= 4:  # français | shimaoré | kibouchi | remarques
                entry = {
                    'francais': parts[0],
                    'shimaore': parts[1],
                    'kibouchi': parts[2],
                    'remarques': parts[3] if len(parts) > 3 else ''
                }
                if entry['francais']:  # Ne pas inclure les entrées vides
                    entries.append(entry)
    
    return entries

def analyze_duplicates(entries: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """Identifie les doublons basés sur les mots français"""
    duplicates = defaultdict(list)
    
    for entry in entries:
        french_word = entry['francais'].lower().strip()
        if french_word:
            duplicates[french_word].append(entry)
    
    # Ne retourner que les mots qui apparaissent plus d'une fois
    return {k: v for k, v in duplicates.items() if len(v) > 1}

def analyze_similar_translations(entries: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """Identifie les traductions similaires qui pourraient être des doublons"""
    similar_translations = defaultdict(list)
    
    for entry in entries:
        shimaore = entry['shimaore'].lower().strip()
        kibouchi = entry['kibouchi'].lower().strip()
        
        if shimaore:
            similar_translations[shimaore].append(entry)
        if kibouchi:
            similar_translations[kibouchi].append(entry)
    
    # Ne retourner que les traductions qui apparaissent plus d'une fois
    return {k: v for k, v in similar_translations.items() if len(v) > 1}

def analyze_orthographic_inconsistencies(entries: List[Dict[str, str]]) -> Dict[str, List[str]]:
    """Identifie les incohérences orthographiques potentielles"""
    issues = defaultdict(list)
    
    for entry in entries:
        # Vérifier les apostrophes inconsistantes
        shimaore = entry['shimaore']
        kibouchi = entry['kibouchi']
        
        if shimaore:
            # Vérifier les apostrophes
            if "'" in shimaore and shimaore.count("'") != shimaore.count("'"):
                issues['apostrophes_inconsistantes'].append(f"Shimaoré: {shimaore}")
            
            # Vérifier les accents
            if any(char in shimaore for char in ['é', 'è', 'à', 'ù', 'ô']):
                issues['accents_shimaore'].append(shimaore)
        
        if kibouchi:
            if "'" in kibouchi and kibouchi.count("'") != kibouchi.count("'"):
                issues['apostrophes_inconsistantes'].append(f"Kibouchi: {kibouchi}")
            
            if any(char in kibouchi for char in ['é', 'è', 'à', 'ù', 'ô']):
                issues['accents_kibouchi'].append(kibouchi)
    
    return dict(issues)

def analyze_missing_translations(entries: List[Dict[str, str]]) -> Dict[str, List[str]]:
    """Identifie les traductions manquantes"""
    missing = {
        'shimaore_manquant': [],
        'kibouchi_manquant': []
    }
    
    for entry in entries:
        if not entry['shimaore'].strip():
            missing['shimaore_manquant'].append(entry['francais'])
        if not entry['kibouchi'].strip():
            missing['kibouchi_manquant'].append(entry['francais'])
    
    return missing

def identify_specific_corrections_needed(entries: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Identifie les corrections spécifiques nécessaires"""
    corrections = []
    
    # Cas spécifique mentionné par l'utilisateur : bigorno vs bigorneau
    tortue_entries = [e for e in entries if 'tortue' in e['francais'].lower()]
    bigorno_entries = [e for e in entries if 'bigorno' in e['francais'].lower()]
    
    if tortue_entries and bigorno_entries:
        corrections.append({
            'type': 'doublon_tortue',
            'action': 'supprimer_bigorno_garder_bigorneau',
            'entries': tortue_entries + bigorno_entries
        })
    
    # Doublons d'escargot
    escargot_entries = [e for e in entries if 'escargot' in e['francais'].lower()]
    if len(escargot_entries) > 1:
        corrections.append({
            'type': 'doublon_escargot',
            'action': 'fusionner_ou_choisir',
            'entries': escargot_entries
        })
    
    # Traductions multiples (comme crabe: nyamba/katsa)
    for entry in entries:
        if '/' in entry['shimaore'] or '/' in entry['kibouchi']:
            corrections.append({
                'type': 'traduction_multiple',
                'action': 'verifier_si_doublon_ou_variante',
                'entry': entry
            })
    
    return corrections

def main():
    """Fonction principale d'analyse"""
    print("🔍 ANALYSE DU PDF VOCABULAIRE SHIMAORÉ-KIBOUCHI")
    print("=" * 60)
    
    # Parser les données
    entries = parse_pdf_data()
    print(f"📊 Total des entrées trouvées: {len(entries)}")
    
    # Analyser les doublons
    duplicates = analyze_duplicates(entries)
    print(f"\n🔄 DOUBLONS IDENTIFIÉS ({len(duplicates)} cas):")
    for french_word, duplicate_entries in duplicates.items():
        print(f"  • {french_word}: {len(duplicate_entries)} occurrences")
        for i, entry in enumerate(duplicate_entries, 1):
            print(f"    {i}. Shimaoré: '{entry['shimaore']}', Kibouchi: '{entry['kibouchi']}'")
    
    # Analyser les traductions similaires
    similar_translations = analyze_similar_translations(entries)
    print(f"\n🔄 TRADUCTIONS SIMILAIRES ({len(similar_translations)} cas):")
    for translation, similar_entries in similar_translations.items():
        if len(similar_entries) > 1:
            french_words = [e['francais'] for e in similar_entries]
            print(f"  • '{translation}' utilisé pour: {', '.join(french_words)}")
    
    # Analyser les incohérences orthographiques
    orthographic_issues = analyze_orthographic_inconsistencies(entries)
    print(f"\n✏️ INCOHÉRENCES ORTHOGRAPHIQUES:")
    for issue_type, examples in orthographic_issues.items():
        print(f"  • {issue_type}: {len(examples)} cas")
        for example in examples[:5]:  # Limiter à 5 exemples
            print(f"    - {example}")
    
    # Analyser les traductions manquantes
    missing_translations = analyze_missing_translations(entries)
    print(f"\n❌ TRADUCTIONS MANQUANTES:")
    print(f"  • Shimaoré manquant: {len(missing_translations['shimaore_manquant'])} mots")
    print(f"  • Kibouchi manquant: {len(missing_translations['kibouchi_manquant'])} mots")
    
    # Corrections spécifiques
    specific_corrections = identify_specific_corrections_needed(entries)
    print(f"\n🔧 CORRECTIONS SPÉCIFIQUES NÉCESSAIRES ({len(specific_corrections)} cas):")
    for correction in specific_corrections:
        print(f"  • {correction['type']}: {correction['action']}")
    
    # Résumé des actions recommandées
    print(f"\n📋 RÉSUMÉ DES ACTIONS RECOMMANDÉES:")
    print(f"  1. Éliminer les doublons: {len(duplicates)} cas à traiter")
    print(f"  2. Corriger les incohérences orthographiques: {sum(len(v) for v in orthographic_issues.values())} problèmes")
    print(f"  3. Compléter les traductions manquantes: {len(missing_translations['shimaore_manquant']) + len(missing_translations['kibouchi_manquant'])} traductions")
    print(f"  4. Traiter les corrections spécifiques: {len(specific_corrections)} cas")
    
    # Cas spécifique bigorno/bigorneau
    print(f"\n🐢 CAS SPÉCIFIQUE TORTUE (bigorno vs bigorneau):")
    tortue_found = False
    bigorneau_found = False
    for entry in entries:
        if 'tortue' in entry['francais'].lower():
            print(f"  • Tortue trouvée: Shimaoré='{entry['shimaore']}', Kibouchi='{entry['kibouchi']}'")
            tortue_found = True
        elif 'bigorneau' in entry['francais'].lower():
            print(f"  • Bigorneau trouvé: Shimaoré='{entry['shimaore']}', Kibouchi='{entry['kibouchi']}'")
            bigorneau_found = True
    
    if tortue_found and bigorneau_found:
        print("  → ACTION: Supprimer l'entrée 'bigorno' et garder 'bigorneau' comme demandé")
    
    return {
        'total_entries': len(entries),
        'duplicates': duplicates,
        'similar_translations': similar_translations,
        'orthographic_issues': orthographic_issues,
        'missing_translations': missing_translations,
        'specific_corrections': specific_corrections
    }

if __name__ == "__main__":
    analysis_result = main()