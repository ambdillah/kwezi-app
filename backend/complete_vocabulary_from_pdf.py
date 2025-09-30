#!/usr/bin/env python3
"""
AJOUT DU RESTE DU VOCABULAIRE DU PDF
====================================
Ce script ajoute toutes les données restantes du PDF
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URL)
db = client['shimaoré_app']

print("🔄 AJOUT DU RESTE DU VOCABULAIRE PDF")
print("=" * 50)

# DONNÉES RESTANTES DU PDF
remaining_vocabulary = [
    # ========== ANIMAUX (Suite) ==========
    {"section": "animaux", "french": "crocodile", "shimaoré": "vwài", "kibouchi": "vwài"},
    {"section": "animaux", "french": "caméléon", "shimaoré": "tarundru", "kibouchi": "tarondru"},
    {"section": "animaux", "french": "zébu", "shimaoré": "nyombé", "kibouchi": "aoumbi"},
    {"section": "animaux", "french": "âne", "shimaoré": "pundra", "kibouchi": "ampundra"},
    {"section": "animaux", "french": "poule", "shimaoré": "kouhou", "kibouchi": "akohou"},
    {"section": "animaux", "french": "pigeon", "shimaoré": "ndiwa", "kibouchi": "ndiwa"},
    {"section": "animaux", "french": "fourmis", "shimaoré": "tsoussou", "kibouchi": "vitsiki"},
    {"section": "animaux", "french": "chenille", "shimaoré": "bazi", "kibouchi": "bibimanguidi"},
    {"section": "animaux", "french": "papillon", "shimaoré": "pelapelaka", "kibouchi": "tsipelapelaka"},
    {"section": "animaux", "french": "ver de terre", "shimaoré": "lingoui lingoui", "kibouchi": "bibi fotaka"},
    {"section": "animaux", "french": "criquet", "shimaoré": "furudji", "kibouchi": "kidzedza"},
    {"section": "animaux", "french": "cheval", "shimaoré": "poundra", "kibouchi": "karasou"},
    {"section": "animaux", "french": "perroquet", "shimaoré": "kassoukou", "kibouchi": "kalalawi"},
    {"section": "animaux", "french": "cafard", "shimaoré": "kalalawi", "kibouchi": "kalalowou"},
    {"section": "animaux", "french": "araignée", "shimaoré": "shitrandrabwibwi", "kibouchi": "bibi ampamani massou"},
    {"section": "animaux", "french": "scorpion", "shimaoré": "hala", "kibouchi": "hala"},
    {"section": "animaux", "french": "scolopandre", "shimaoré": "trambwi", "kibouchi": "trambougnou"},
    {"section": "animaux", "french": "thon", "shimaoré": "mbassi", "kibouchi": "mbassi"},
    {"section": "animaux", "french": "requin", "shimaoré": "papa", "kibouchi": "ankiou"},
    {"section": "animaux", "french": "poulpe", "shimaoré": "pwedza", "kibouchi": "pwedza"},
    {"section": "animaux", "french": "crabe", "shimaoré": "dradraka", "kibouchi": "dakatra"},
    {"section": "animaux", "french": "tortue", "shimaoré": "nyamba", "kibouchi": "fanou"},
    {"section": "animaux", "french": "bigorneau", "shimaoré": "trondro", "kibouchi": "trondrou"},
    {"section": "animaux", "french": "éléphant", "shimaoré": "ndovu", "kibouchi": "ndovu"},
    {"section": "animaux", "french": "singe", "shimaoré": "djakouayi", "kibouchi": "djakwe"},
    {"section": "animaux", "french": "souris", "shimaoré": "shikwetse", "kibouchi": "voilavou"},
    {"section": "animaux", "french": "facochère", "shimaoré": "pouruku nyeha", "kibouchi": "lambou"},
    {"section": "animaux", "french": "renard", "shimaoré": "mbwa nyeha", "kibouchi": "fandroka di"},
    {"section": "animaux", "french": "chameau", "shimaoré": "ngamia", "kibouchi": "ngwizi"},
    {"section": "animaux", "french": "hérisson", "shimaoré": "landra", "kibouchi": "trandraka"},
    {"section": "animaux", "french": "corbeau", "shimaoré": "gawa", "kibouchi": "gouaka"},
    {"section": "animaux", "french": "civette", "shimaoré": "founga", "kibouchi": "angava"},
    {"section": "animaux", "french": "dauphin", "shimaoré": "moungoumé", "kibouchi": "fésoutrou"},
    {"section": "animaux", "french": "baleine", "shimaoré": "ndroujou", "kibouchi": ""},
    {"section": "animaux", "french": "crevette", "shimaoré": "camba", "kibouchi": "ancamba"},
    {"section": "animaux", "french": "frelon", "shimaoré": "chonga", "kibouchi": "faraka"},
    {"section": "animaux", "french": "guêpe", "shimaoré": "movou", "kibouchi": "fanintri"},
    {"section": "animaux", "french": "bourdon", "shimaoré": "vungo vungo", "kibouchi": "madjaoumbi"},
    {"section": "animaux", "french": "puce", "shimaoré": "kunguni", "kibouchi": "ancongou"},
    {"section": "animaux", "french": "poux", "shimaoré": "indra", "kibouchi": "howou"},
    {"section": "animaux", "french": "bouc", "shimaoré": "béwé", "kibouchi": "bébérou"},
    {"section": "animaux", "french": "taureau", "shimaoré": "kondzo", "kibouchi": "dzow"},
    {"section": "animaux", "french": "lambis", "shimaoré": "kombé", "kibouchi": "mahombi"},
    {"section": "animaux", "french": "cône de mer", "shimaoré": "kwitsi", "kibouchi": "tsimtipaka"},
    {"section": "animaux", "french": "mille-pattes", "shimaoré": "mjongo", "kibouchi": "ancoudavitri"},
    {"section": "animaux", "french": "oursin", "shimaoré": "gadzassi ya bahari", "kibouchi": "voulì vavi"},
    {"section": "animaux", "french": "huître", "shimaoré": "gadzassi", "kibouchi": "sadza"},

    # ========== CORPS HUMAIN ==========
    {"section": "corps_humain", "french": "œil", "shimaoré": "matso", "kibouchi": "faninti"},
    {"section": "corps_humain", "french": "nez", "shimaoré": "poua", "kibouchi": "horougnou"},
    {"section": "corps_humain", "french": "oreille", "shimaoré": "kiyo", "kibouchi": "soufigni"},
    {"section": "corps_humain", "french": "ongle", "shimaoré": "kofou", "kibouchi": "angofou"},
    {"section": "corps_humain", "french": "front", "shimaoré": "housso", "kibouchi": "lahara"},
    {"section": "corps_humain", "french": "joue", "shimaoré": "savou", "kibouchi": "fifi"},
    {"section": "corps_humain", "french": "dos", "shimaoré": "mengo", "kibouchi": "vohou"},
    {"section": "corps_humain", "french": "épaule", "shimaoré": "bèga", "kibouchi": "haveyi"},
    {"section": "corps_humain", "french": "hanche", "shimaoré": "trenga", "kibouchi": "tahezagna"},
    {"section": "corps_humain", "french": "fesses", "shimaoré": "shidzè", "kibouchi": "fouri"},
    {"section": "corps_humain", "french": "main", "shimaoré": "mhono", "kibouchi": "tagnana"},
    {"section": "corps_humain", "french": "tête", "shimaoré": "shitsoi", "kibouchi": "louha"},
    {"section": "corps_humain", "french": "ventre", "shimaoré": "mimba", "kibouchi": "kibou"},
    {"section": "corps_humain", "french": "dent", "shimaoré": "magno", "kibouchi": "hifi"},
    {"section": "corps_humain", "french": "langue", "shimaoré": "oulimé", "kibouchi": "lèla"},
    {"section": "corps_humain", "french": "pied", "shimaoré": "mindrou", "kibouchi": "viti"},
    {"section": "corps_humain", "french": "lèvre", "shimaoré": "dhomo", "kibouchi": "soungni"},
    {"section": "corps_humain", "french": "peau", "shimaoré": "ngwezi", "kibouchi": "ngwezi"},
    {"section": "corps_humain", "french": "cheveux", "shimaoré": "ngnélé", "kibouchi": "fagnéva"},
    {"section": "corps_humain", "french": "doigts", "shimaoré": "cha", "kibouchi": "tondrou"},
    {"section": "corps_humain", "french": "barbe", "shimaoré": "ndrévou", "kibouchi": "somboutrou"},
    {"section": "corps_humain", "french": "vagin", "shimaoré": "ndzigni", "kibouchi": "tingui"},
    {"section": "corps_humain", "french": "testicules", "shimaoré": "kwendzé", "kibouchi": "vouancarou"},
    {"section": "corps_humain", "french": "pénis", "shimaoré": "mbo", "kibouchi": "kaboudzi"},
    {"section": "corps_humain", "french": "menton", "shimaoré": "shlévou", "kibouchi": "sokou"},
    {"section": "corps_humain", "french": "bouche", "shimaoré": "hangno", "kibouchi": "vava"},
    {"section": "corps_humain", "french": "côtes", "shimaoré": "bavou", "kibouchi": "mbavou"},
    {"section": "corps_humain", "french": "sourcil", "shimaoré": "tsi", "kibouchi": "ankwéssi"},
    {"section": "corps_humain", "french": "cheville", "shimaoré": "dzitso la pwédza", "kibouchi": "dzitso la pwédza"},
    {"section": "corps_humain", "french": "cou", "shimaoré": "tsingo", "kibouchi": "vouzougnou"},
    {"section": "corps_humain", "french": "cils", "shimaoré": "kové", "kibouchi": "rambou faninti"},
    {"section": "corps_humain", "french": "arrière du crâne", "shimaoré": "komoi", "kibouchi": "kitoika"},

    # ========== SALUTATIONS ==========
    {"section": "salutations", "french": "bonjour", "shimaoré": "kwezi", "kibouchi": "kwezi"},
    {"section": "salutations", "french": "comment ça va", "shimaoré": "jéjé", "kibouchi": "akori"},
    {"section": "salutations", "french": "oui", "shimaoré": "ewa", "kibouchi": "iya"},
    {"section": "salutations", "french": "non", "shimaoré": "an'ha", "kibouchi": "an'ha"},
    {"section": "salutations", "french": "ça va bien", "shimaoré": "fétré", "kibouchi": "tsara"},
    {"section": "salutations", "french": "merci", "shimaoré": "marahaba", "kibouchi": "marahaba"},
    {"section": "salutations", "french": "bonne nuit", "shimaoré": "oukou wa hairi", "kibouchi": "haligni tsara"},
    {"section": "salutations", "french": "au revoir", "shimaoré": "kwaheri", "kibouchi": "maeva"},

    # ========== GRAMMAIRE ==========
    {"section": "grammaire", "french": "je", "shimaoré": "wami", "kibouchi": "zahou"},
    {"section": "grammaire", "french": "tu", "shimaoré": "wawé", "kibouchi": "anaou"},
    {"section": "grammaire", "french": "il", "shimaoré": "wayé", "kibouchi": "izi"},
    {"section": "grammaire", "french": "elle", "shimaoré": "wayé", "kibouchi": "izi"},
    {"section": "grammaire", "french": "nous", "shimaoré": "wassi", "kibouchi": "atsika"},
    {"section": "grammaire", "french": "vous", "shimaoré": "wagnou", "kibouchi": "anaréou"},
    {"section": "grammaire", "french": "ils", "shimaoré": "wawo", "kibouchi": "réou"},
    {"section": "grammaire", "french": "elles", "shimaoré": "wawo", "kibouchi": "réou"},
    {"section": "grammaire", "french": "le mien", "shimaoré": "yangou", "kibouchi": "ninakahi"},
    {"section": "grammaire", "french": "le tien", "shimaoré": "yaho", "kibouchi": "ninaou"},
    {"section": "grammaire", "french": "le sien", "shimaoré": "yahé", "kibouchi": "ninazi"},
    {"section": "grammaire", "french": "le leur", "shimaoré": "yawo", "kibouchi": "nindréou"},
    {"section": "grammaire", "french": "le nôtre", "shimaoré": "yatrou", "kibouchi": "nintsika"},
    {"section": "grammaire", "french": "le vôtre", "shimaoré": "yangnou", "kibouchi": "ninaréou"},
    {"section": "grammaire", "french": "professeur", "shimaoré": "foundi", "kibouchi": "foundi"},
    {"section": "grammaire", "french": "guide spirituel", "shimaoré": "cadhi", "kibouchi": "cadhi"},
    {"section": "grammaire", "french": "imam", "shimaoré": "imamou", "kibouchi": "imamou"},
    {"section": "grammaire", "french": "voisin", "shimaoré": "djirani", "kibouchi": "djirani"},
    {"section": "grammaire", "french": "maire", "shimaoré": "méra", "kibouchi": "méra"},
    {"section": "grammaire", "french": "élu", "shimaoré": "dhoimana", "kibouchi": "dhoimana"},
    {"section": "grammaire", "french": "pêcheur", "shimaoré": "mlozi", "kibouchi": "ampamintagna"},
    {"section": "grammaire", "french": "agriculteur", "shimaoré": "mlimizi", "kibouchi": "ampikapa"},
    {"section": "grammaire", "french": "éleveur", "shimaoré": "mtsounga", "kibouchi": "ampitsounga"},

    # ========== FAMILLE ==========
    {"section": "famille", "french": "tante maternelle", "shimaoré": "mama titi", "kibouchi": "nindri heli"},
    {"section": "famille", "french": "oncle maternel", "shimaoré": "zama", "kibouchi": "zama"},
    {"section": "famille", "french": "oncle paternel", "shimaoré": "baba titi", "kibouchi": "baba héli"},
    {"section": "famille", "french": "épouse oncle maternel", "shimaoré": "zena", "kibouchi": "zena"},
    {"section": "famille", "french": "petite sœur", "shimaoré": "moinagna mtroumama", "kibouchi": "zandri viavi"},
    {"section": "famille", "french": "petit frère", "shimaoré": "moinagna mtroubaba", "kibouchi": "zandri lalahi"},
    {"section": "famille", "french": "grande sœur", "shimaoré": "zouki mtroumché", "kibouchi": "zoki viavi"},
    {"section": "famille", "french": "grand frère", "shimaoré": "zouki mtroubaba", "kibouchi": "zoki lalahi"},
    {"section": "famille", "french": "frère", "shimaoré": "mwanagna", "kibouchi": "anadahi"},
    {"section": "famille", "french": "sœur", "shimaoré": "mwanagna", "kibouchi": "anabavi"},
    {"section": "famille", "french": "ami", "shimaoré": "mwandzani", "kibouchi": "mwandzani"},
    {"section": "famille", "french": "fille", "shimaoré": "mtroumama", "kibouchi": "viavi"},
    {"section": "famille", "french": "garçon", "shimaoré": "mtroubaba", "kibouchi": "lalahi"},
    {"section": "famille", "french": "monsieur", "shimaoré": "mogné", "kibouchi": "lalahi"},
    {"section": "famille", "french": "grand-père", "shimaoré": "bacoco", "kibouchi": "dadayi"},
    {"section": "famille", "french": "grand-mère", "shimaoré": "coco", "kibouchi": "dadi"},
    {"section": "famille", "french": "madame", "shimaoré": "bwéni", "kibouchi": "viavi"},
    {"section": "famille", "french": "famille", "shimaoré": "mdjamaza", "kibouchi": "havagna"},
    {"section": "famille", "french": "papa", "shimaoré": "baba", "kibouchi": "baba"},
    {"section": "famille", "french": "maman", "shimaoré": "mama", "kibouchi": "mama"},
    {"section": "famille", "french": "tante paternelle", "shimaoré": "zéna", "kibouchi": "zéna"},
    {"section": "famille", "french": "jeune adulte", "shimaoré": "shababi", "kibouchi": "shababi"},
    {"section": "famille", "french": "petit garçon", "shimaoré": "mwana mtroubaba", "kibouchi": "zaza lalahi"},
    {"section": "famille", "french": "petite fille", "shimaoré": "mwana mtroumama", "kibouchi": "zaza viavi"},

    # ========== COULEURS ==========
    {"section": "couleurs", "french": "bleu", "shimaoré": "bilé", "kibouchi": "mayitsou bilé"},
    {"section": "couleurs", "french": "vert", "shimaoré": "dhavou", "kibouchi": "mayitsou"},
    {"section": "couleurs", "french": "noir", "shimaoré": "nzidhou", "kibouchi": "mayintigni"},
    {"section": "couleurs", "french": "blanc", "shimaoré": "ndjéou", "kibouchi": "malandi"},
    {"section": "couleurs", "french": "jaune", "shimaoré": "dzindzano", "kibouchi": "tamoutamou"},
    {"section": "couleurs", "french": "rouge", "shimaoré": "nzoukoundrou", "kibouchi": "mena"},
    {"section": "couleurs", "french": "gris", "shimaoré": "djifou", "kibouchi": "dzofou"},
    {"section": "couleurs", "french": "marron", "shimaoré": "trotro", "kibouchi": "fotafotaka"},
]

print("Insertion des données restantes...")
current_time = datetime.utcnow()

for word_data in remaining_vocabulary:
    word_data.update({
        "created_at": current_time,
        "source": "pdf_reconstruction_complete",
        "pdf_verified": True,
        "orthography_verified": True,
        "complete_reconstruction": True
    })

try:
    result = db.vocabulary.insert_many(remaining_vocabulary)
    print(f"   ✅ {len(result.inserted_ids)} mots supplémentaires ajoutés")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Vérification finale
sections = db.vocabulary.distinct("section")
total = db.vocabulary.count_documents({})
print(f"\n📊 ÉTAT ACTUEL:")
for section in sorted(sections):
    count = db.vocabulary.count_documents({"section": section})
    print(f"   {section}: {count} mots")

print(f"\n🎯 TOTAL: {total} mots dans la base de données")
print("\n✨ Sections ajoutées jusqu'ici: nature, nombres, animaux, corps_humain, salutations, grammaire, famille, couleurs")
print("⏳ Il reste encore à ajouter: nourriture, maison, verbes, expressions, adjectifs, transport, vêtements, tradition")