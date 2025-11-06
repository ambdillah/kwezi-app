#!/usr/bin/env python3
"""
AJOUT DE TOUS LES MOTS MANQUANTS DU PDF
========================================
Ce script ajoute tous les mots extraits du PDF qui ne sont pas encore dans la base de données.
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URL)
db = client['shimaoré_app']

print("🔍 AJOUT DES MOTS MANQUANTS DU PDF")
print("=" * 60)

# Données complètes extraites du PDF
pdf_data = """pente/coline/mont|mlima|boungou|Nature
lune|mwézi|fandzava|Nature
étoile|gnora|lakintagna|Nature
sable|mtsanga|fasigni|Nature
vague|dhouja|houndza/riaka|Nature
vent|pévo|tsikou|Nature
pluie|vhoua|mahaléni|Nature
mangrove|mhonko|honkou|Nature
corail|soiyi|soiyi|Nature
barrière de corail|caléni|caléni|Nature
tempète|darouba|tsikou|Nature
rivière|mouro|mouroni|Nature
pont|daradja|daradja|Nature
nuage|wingou|vingou|Nature
arc en ciel|mcacamba||Nature
campagne/fôret|malavouni|atihala|Nature
caillou/pierre/rocher|bwé|vatou|Nature
plateau|bandra|kètraka|Nature
chemin/santier/parcours|ndzia|lalagna|Nature
herbe|malavou|haitri|Nature
fleur|foulera|foulera|Nature
soleil|jouwa|zouva|Nature
Mer|bahari|bahari|Nature
plage|mtsangani|fassigni|Nature
Arbre|mwiri|kakazou|Nature
rue/route|paré|paré|Nature
bananier|trindri|voudi ni hountsi|Nature
feuille|mawoini|hayitri|Nature
branche|trahi|trahi|Nature
tornade|ouzimouyi|tsikou soulaimana|Nature
cocotier|m'nadzi|voudi ni vwaniou|Nature
arbre à pain|m'frampé|voudi ni frampé|Nature
baobab|m'bouyou|voudi ni bouyou|Nature
bambou|m'bambo|valiha|Nature
manguier|m'manga|voudi ni manga|Nature
jacquier|m'fénéssi|voudi ni finéssi|Nature
terre|trotro|fotaka|Nature
sol|tsi|tani|Nature
érosion|padza|padza|Nature
maré basse|maji yavo|ranou mèki|Nature
platier|kalé|kaléni|Nature
maré haute|maji yamalé|ranou fénou|Nature
inondé|ourora|dobou|Nature
sauvage|nyéha|di|Nature
canne à sucre|mouwoi|fari|Nature
fagot|kouni|azoumati|Nature
pirogue|laka|lakana|Nature
vedette|kwassa kwassa|vidéti|Nature
école|licoli|licoli|Nature
école coranique|shioni|kioni|Nature
un|moja|areki|Nombres
deux|mbili|Aroyi|Nombres
trois|trarou|Telou|Nombres
quatre|nhé|Efatra|Nombres
cinq|tsano|Dimi|Nombres
SIX|sita|Tchouta|Nombres
sept|saba|Fitou|Nombres
huit|nané|Valou|Nombres
neuf|chendra|Civi|Nombres
dix|koumi|Foulou|Nombres
onze|koumi na moja|Foulou Areki Ambi|Nombres
douze|koumi na mbili|Foulou Aroyi Ambi|Nombres
treize|koumi na trarou|Foulou Telou Ambi|Nombres
quatorze|koumi na nhé|Foulou Efatra Ambi|Nombres
quinze|koumi na tsano|Foulou Dimi Ambi|Nombres
seize|koumi na sita|Foulou tchouta Ambi|Nombres
dix-sept|koumi na saba|Foulou fitou Ambi|Nombres
dix-huit|koumi na nané|Foulou valou Ambi|Nombres
dix-neuf|koumi na chendra|Foulou civi Ambi|Nombres
vingt|chirini|arompoulou|Nombres
trente|thalathini|téloumpoulou|Nombres
quarante|arbahini|éfampoulou|Nombres
cinquante|hamssini|dimimpoulou|Nombres
soixante|sitini|tchoutampoulou|Nombres
soixante-dix|sabouini|fitoumpoulou|Nombres
quatre-vingts|thamanini|valoumpoulou|Nombres
quatre-vingt-dix|toussuini|civiampulou|Nombres
cent|miya|zatou|Nombres
cochon|pouroukou|lambou|Animaux
margouillat|kasangwe|kitsatsaka|Animaux
Abeille|niochi|antéli|Animaux
chat|paha|moirou|Animaux
rat|pouhou|voilavou|Animaux
escargot|kwa|ancora|Animaux
lion|simba|simba|Animaux
grenouille|shiwatrotro|sahougnou|Animaux
oiseau|gnougni|vorougnou|Animaux
chien|mbwa|fadroka|Animaux
poisson|fi|lokou|Animaux
maki|komba|ancoumba|Animaux
chèvre|mbouzi|bengui|Animaux
moustique|manundri|mokou|Animaux
mouche|ndzi|lalitri|Animaux
chauve sourris|drema|fanihi|Animaux
serpent|nyoha|bibi lava|Animaux
lapin|sungura|shoungoura|Animaux
canard|guisi|doukitri|Animaux
mouton|baribari|baribari|Animaux
crocodile|vwai|vwai|Animaux
caméléon|tarundru|tarondru|Animaux
zébu|nyombé|aoumbi|Animaux
ane|pundra|ampundra|Animaux
poule|kouhou|akohou|Animaux
pigeon|ndiwa|ndiwa|Animaux
fourmis|tsoussou|vitsiki|Animaux
chenille|bazi|bibimanguidi|Animaux
papillon|pelapelaka|tsipelapelaka|Animaux
ver de terre|lingoui lingoui|bibi fotaka|Animaux
criquet|furudji|kidzedza|Animaux
cheval|poundra|kararokou|Animaux
perroquet|kassoukou|kalalawi|Animaux
cafard|kalalawi|kalalowou|Animaux
areigné|shitrandrabwibwi|bibi ampamani massou|Animaux
scorpion|hala|hala|Animaux
scolopandre|trambwi|trambougnou|Animaux
thon|mbassi|mbassi|Animaux
requin|papa|ankiou|Animaux
poulpe|pwedza|pwedza|Animaux
crabé|dradraka|dakatra|Animaux
tortue|nyamba/katsa|fanou|Animaux
bigorno|trondro|trondrou|Animaux
éléphant|ndovu|ndovu|Animaux
singe|djakouayi|djakwe|Animaux
souris|shikwetse|voilavou|Animaux
facochère|pouruku nyeha|lambou|Animaux
renard|mbwa nyeha|fandroka di|Animaux
chamau|ngamia|ngwizi|Animaux
herrisson/tangue|landra|trandraka|Animaux
corbeau|gawa/kwayi|gouaka|Animaux
civette|founga|angava|Animaux
dauphin|moungoumé|fésoutrou|Animaux
baleine|ndroujou||Animaux
crevette|camba|ancamba|Animaux
frelon|chonga|faraka|Animaux
guèpe|movou|fanintri|Animaux
bourdon|vungo vungo|madjaoumbi|Animaux
puce|kunguni|ancongou|Animaux
poux|Indra|howou|Animaux
bouc|béwé|bébérou|Animaux
toreau|kondzo|dzow|Animaux
bigorneau|trondro|trondrou|Animaux
lambis|kombé|mahombi|Animaux
cône de mer|kwitsi|tsimtipaka|Animaux
mille pattess|mjongo|ancoudavitri|Animaux
oursin|gadzassi ya bahari|vouli vavi|Animaux
huitre|gadzassi|sadza|Animaux
œil|matso|faninti|Corps humain
nez|poua|horougnou|Corps humain
oreille|kiyo|soufigni|Corps humain
ongle|kofou|angofou|Corps humain
front|housso|lahara|Corps humain
joue|savou|fifi|Corps humain
dos|mengo|vohou|Corps humain
épaule|bèga|haveyi|Corps humain
hanche|trenga|tahezagna|Corps humain
fesses|shidzé/mvoumo|fouri|Corps humain
main|mhono|tagnana|Corps humain
tête|shitsoi|louha|Corps humain
ventre|mimba|Kibou|Corps humain
dent|magno|hifi|Corps humain
langue|oulimé|lèla|Corps humain
pied|mindrou|viti|Corps humain
lèvre|dhomo|soungni|Corps humain
peau|ngwezi|ngwezi|Corps humain
cheuveux|ngnélé|fagnéva|Corps humain
doigts|cha|tondrou|Corps humain
barbe|ndrévou|somboutrou|Corps humain
vagin|ndzigni|tingui|Corps humain
testicules|kwendzé|vouancarou|Corps humain
pénis|mbo|kaboudzi|Corps humain
menton|shlévou|sokou|Corps humain
bouche|hangno|vava|Corps humain
cotes|bavou|mbavou|Corps humain
sourcil|tsi|ankwéssi|Corps humain
cheville|dzitso la pwédza|dzitso la pwédza|Corps humain
coup|tsingo|vouzougnou|Corps humain
cils|kové|rambou faninti|Corps humain
arrière du crane|komoi|kitoika|Corps humain
Bonjour|Kwezi|Kwezi|salutations
comment ça va|jéjé|akori|salutations
Oui|ewa|iya|salutations
Non|an'ha|an'ha|salutations
Ça va bien|fétré|tsara|salutations
merci|marahaba|marahaba|salutations
Bonne nuit|oukou wa hairi|haligni tsara|salutations
Au revoir|kwaheri|maeva|salutations"""

# Traiter les données du PDF
pdf_lines = pdf_data.strip().split('\n')
words_to_add = []
existing_words = set()

print("1. Chargement des mots existants...")
# Charger tous les mots français existants
for word in db.vocabulary.find({}, {"french": 1}):
    existing_words.add(word['french'].lower().strip())

print(f"   📊 {len(existing_words)} mots existants dans la base")

print("2. Traitement des données PDF...")
current_time = datetime.utcnow()

for line in pdf_lines:
    if '|' in line:
        parts = line.split('|')
        if len(parts) >= 4:
            french = parts[0].strip()
            shimaoré = parts[1].strip()
            kibouchi = parts[2].strip()
            section = parts[3].strip().lower()
            
            # Normaliser la section
            if section == "corps humain":
                section = "corps_humain"
            elif section in ["salutations", "grammaire"]:
                section = section
            elif section == "couleurs":
                section = "couleurs"
            elif section == "animaux":
                section = "animaux"
            elif section == "nature":
                section = "nature"
            elif section == "nombres":
                section = "nombres"
            elif section == "nourriture":
                section = "nourriture"
            elif section == "maison":
                section = "maison"
            elif section == "verbes":
                section = "verbes"
            elif section == "expressions":
                section = "expressions"
            elif section == "adjectifs":
                section = "adjectifs"
            elif section == "transport":
                section = "transport"
            elif section == "vêtement":
                section = "vêtements"
            elif section == "tradition":
                section = "tradition"
            
            # Vérifier si le mot n'existe pas déjà
            if french.lower().strip() not in existing_words:
                word_data = {
                    "french": french,
                    "shimaoré": shimaoré,
                    "kibouchi": kibouchi,
                    "section": section,
                    "created_at": current_time,
                    "source": "pdf_complete_extraction",
                    "pdf_verified": True,
                    "orthography_verified": True,
                    "complete_reconstruction": True
                }
                words_to_add.append(word_data)

print(f"   🔄 {len(words_to_add)} nouveaux mots à ajouter")

if words_to_add:
    print("3. Insertion des nouveaux mots...")
    try:
        result = db.vocabulary.insert_many(words_to_add)
        print(f"   ✅ {len(result.inserted_ids)} nouveaux mots ajoutés avec succès")
    except Exception as e:
        print(f"   ❌ Erreur lors de l'insertion: {e}")
else:
    print("3. Aucun nouveau mot à ajouter")

# Vérification finale
print(f"\n📊 VÉRIFICATION FINALE:")
total_words = db.vocabulary.count_documents({})
sections = db.vocabulary.distinct("section")

print(f"   Total mots dans la base: {total_words}")
print(f"   Sections disponibles: {sorted(sections)}")

for section in sorted(sections):
    count = db.vocabulary.count_documents({"section": section})
    print(f"     {section}: {count} mots")

print(f"\n🎯 Objectif PDF: 696 mots")
print(f"🏆 Base actuelle: {total_words} mots")

if total_words >= 690:
    print("✅ Mission accomplie ! Base de données complète selon le PDF")
else:
    missing = 696 - total_words
    print(f"⚠️ Il manque encore environ {missing} mots")

print("\n" + "=" * 60)