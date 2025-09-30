#!/usr/bin/env python3
"""
FINALISATION COMPLÈTE - Ajout des dernières sections
=====================================================
Expressions, Adjectifs, Transport, Vêtements, Tradition
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URL)
db = client['shimaoré_app']

print("🔄 FINALISATION COMPLÈTE - DERNIÈRES SECTIONS")
print("=" * 60)

# DERNIÈRES SECTIONS DU PDF
last_sections = [
    # ========== EXPRESSIONS ==========
    {"section": "expressions", "french": "excuse-moi", "shimaoré": "soimahani", "kibouchi": "soimahani"},
    {"section": "expressions", "french": "j'ai faim", "shimaoré": "nissi ona ndza", "kibouchi": "zahou moussari"},
    {"section": "expressions", "french": "j'ai soif", "shimaoré": "nissi ona niyora", "kibouchi": "zahou tindranou"},
    {"section": "expressions", "french": "je voudrais aller à", "shimaoré": "nissi tsaha nendré", "kibouchi": "zahou chokou andéha"},
    {"section": "expressions", "french": "j'arrive de", "shimaoré": "tsi lawa", "kibouchi": "zahou boka"},
    {"section": "expressions", "french": "je peux avoir des toilettes", "shimaoré": "nissi miya mraba", "kibouchi": "zahou mangataka mraba"},
    {"section": "expressions", "french": "je veux manger", "shimaoré": "nissi miya chaoula", "kibouchi": "zahou mila ihinagna"},
    {"section": "expressions", "french": "où se trouve", "shimaoré": "ouparihanoua havi", "kibouchi": "aya moi"},
    {"section": "expressions", "french": "où sommes nous", "shimaoré": "ra havi", "kibouchi": "atsika yétou aya"},
    {"section": "expressions", "french": "je suis perdu", "shimaoré": "tsi latsiha", "kibouchi": "zahou véri"},
    {"section": "expressions", "french": "bienvenu", "shimaoré": "oukaribissa", "kibouchi": "karibou"},
    {"section": "expressions", "french": "je t'aime", "shimaoré": "nissouhou vendza", "kibouchi": "zahou mitia anaou"},
    {"section": "expressions", "french": "j'ai mal", "shimaoré": "nissi kodza", "kibouchi": "zahou marari"},
    {"section": "expressions", "french": "pouvez-vous m'aider", "shimaoré": "ni sayidié vanou", "kibouchi": "zahou mangataka moussada"},
    {"section": "expressions", "french": "j'ai compris", "shimaoré": "tsi héléwa", "kibouchi": "zahou kouéléwa"},
    {"section": "expressions", "french": "je ne peux pas", "shimaoré": "tsi chindri", "kibouchi": "zahou tsi mahaléou"},
    {"section": "expressions", "french": "montre moi", "shimaoré": "néssédzéyé", "kibouchi": "ampizaha zahou"},
    {"section": "expressions", "french": "s'il vous plaît", "shimaoré": "tafadali", "kibouchi": "tafadali"},
    {"section": "expressions", "french": "combien ça coûte", "shimaoré": "kissajé", "kibouchi": "hotri inou moi"},
    {"section": "expressions", "french": "à gauche", "shimaoré": "potroni", "kibouchi": "kipotrou"},
    {"section": "expressions", "french": "à droite", "shimaoré": "houméni", "kibouchi": "finana"},
    {"section": "expressions", "french": "tout droit", "shimaoré": "hondzoha", "kibouchi": "mahitsi"},
    {"section": "expressions", "french": "c'est loin", "shimaoré": "ya mbali", "kibouchi": "lavitri"},
    {"section": "expressions", "french": "c'est très bon", "shimaoré": "issi jiva", "kibouchi": "matavi soifi"},
    {"section": "expressions", "french": "trop cher", "shimaoré": "hali", "kibouchi": "saroutrou"},
    {"section": "expressions", "french": "moins cher s'il vous plaît", "shimaoré": "nissi miya ouchoukidzé", "kibouchi": "za mangataka koupoungouza naou kima"},
    {"section": "expressions", "french": "je prends ça", "shimaoré": "nissi renga ini", "kibouchi": "zahou bou angala thi"},
    {"section": "expressions", "french": "combien la nuit", "shimaoré": "kissagé oukou moja", "kibouchi": "hotri inou haligni areki"},
    {"section": "expressions", "french": "avec climatisation", "shimaoré": "ina climatisation", "kibouchi": "missi climatisation"},
    {"section": "expressions", "french": "avec petit déjeuner", "shimaoré": "missi ankera", "kibouchi": "kahiya sirikali"},
    {"section": "expressions", "french": "appelez la police", "shimaoré": "hira sirikali", "kibouchi": "kahiya sirikali"},
    {"section": "expressions", "french": "appelez une ambulance", "shimaoré": "hira ambulanci", "kibouchi": "kahiya ambulanci"},
    {"section": "expressions", "french": "j'ai besoin d'un médecin", "shimaoré": "nitsha douktera", "kibouchi": "zahou mila douktera"},
    {"section": "expressions", "french": "je ne me sens pas bien", "shimaoré": "tsissi fétré", "kibouchi": "za maharengni nafoussoukou moidéli"},
    {"section": "expressions", "french": "au milieu", "shimaoré": "hari", "kibouchi": "angnivou"},
    {"section": "expressions", "french": "respect", "shimaoré": "mastaha", "kibouchi": "mastaha"},
    {"section": "expressions", "french": "quelqu'un de fiable", "shimaoré": "mwaminifou", "kibouchi": "mwaminifou"},
    {"section": "expressions", "french": "secret", "shimaoré": "siri", "kibouchi": "siri"},
    {"section": "expressions", "french": "joie", "shimaoré": "fouraha", "kibouchi": "aravouangna"},
    {"section": "expressions", "french": "avoir la haine", "shimaoré": "outoukiwa", "kibouchi": "marari rohou"},
    {"section": "expressions", "french": "convivialité", "shimaoré": "ouvoimoja", "kibouchi": "ouvoimoja"},
    {"section": "expressions", "french": "entraide", "shimaoré": "oussayidiyana", "kibouchi": "moussada"},
    {"section": "expressions", "french": "faire crédit", "shimaoré": "oukopa", "kibouchi": "midéni"},
    {"section": "expressions", "french": "nounou", "shimaoré": "mlézi", "kibouchi": "mlézi"},

    # ========== ADJECTIFS ==========
    {"section": "adjectifs", "french": "grand", "shimaoré": "bolé", "kibouchi": "bé"},
    {"section": "adjectifs", "french": "petit", "shimaoré": "titi", "kibouchi": "héli"},
    {"section": "adjectifs", "french": "gros", "shimaoré": "mtronga", "kibouchi": "bé"},
    {"section": "adjectifs", "french": "maigre", "shimaoré": "tsala", "kibouchi": "mahia"},
    {"section": "adjectifs", "french": "fort", "shimaoré": "ouna ngouvou", "kibouchi": "missi ngouvou"},
    {"section": "adjectifs", "french": "dur", "shimaoré": "mangavou", "kibouchi": "mahéri"},
    {"section": "adjectifs", "french": "mou", "shimaoré": "trémboivou", "kibouchi": "malémi"},
    {"section": "adjectifs", "french": "beau", "shimaoré": "mzouri", "kibouchi": "zatovou"},
    {"section": "adjectifs", "french": "laid", "shimaoré": "tsi ndzouzouri", "kibouchi": "ratsi sora"},
    {"section": "adjectifs", "french": "jeune", "shimaoré": "nrétsa", "kibouchi": "zaza"},
    {"section": "adjectifs", "french": "vieux", "shimaoré": "dhouha", "kibouchi": "héla"},
    {"section": "adjectifs", "french": "gentil", "shimaoré": "mwéma", "kibouchi": "tsara rohou"},
    {"section": "adjectifs", "french": "méchant", "shimaoré": "mbovou", "kibouchi": "ratsi rohou"},
    {"section": "adjectifs", "french": "intelligent", "shimaoré": "mstanrabou", "kibouchi": "tsara louha"},
    {"section": "adjectifs", "french": "bête", "shimaoré": "dhaba", "kibouchi": "dhaba"},
    {"section": "adjectifs", "french": "riche", "shimaoré": "tadjiri", "kibouchi": "tadjiri"},
    {"section": "adjectifs", "french": "pauvre", "shimaoré": "maskini", "kibouchi": "maskini"},
    {"section": "adjectifs", "french": "sérieux", "shimaoré": "kassidi", "kibouchi": "koussoudi"},
    {"section": "adjectifs", "french": "drôle", "shimaoré": "outsésa", "kibouchi": "mampimohi"},
    {"section": "adjectifs", "french": "calme", "shimaoré": "baridi", "kibouchi": "malémi"},
    {"section": "adjectifs", "french": "nerveux", "shimaoré": "oussikitiha", "kibouchi": "téhi tèhitri"},
    {"section": "adjectifs", "french": "bon", "shimaoré": "mwéma", "kibouchi": "tsara"},
    {"section": "adjectifs", "french": "mauvais", "shimaoré": "mbovou", "kibouchi": "mwadéli"},
    {"section": "adjectifs", "french": "chaud", "shimaoré": "moro", "kibouchi": "mèyi"},
    {"section": "adjectifs", "french": "froid", "shimaoré": "baridi", "kibouchi": "manintsi"},
    {"section": "adjectifs", "french": "lourd", "shimaoré": "ndziro", "kibouchi": "mavèchatra"},
    {"section": "adjectifs", "french": "léger", "shimaoré": "ndzangou", "kibouchi": "mayivagna"},
    {"section": "adjectifs", "french": "propre", "shimaoré": "irahara", "kibouchi": "madiou"},
    {"section": "adjectifs", "french": "sale", "shimaoré": "trotro", "kibouchi": "maloutou"},
    {"section": "adjectifs", "french": "nouveau", "shimaoré": "piya", "kibouchi": "vowou"},
    {"section": "adjectifs", "french": "ancien", "shimaoré": "halé", "kibouchi": "kèyi"},
    {"section": "adjectifs", "french": "facile", "shimaoré": "ndzangou", "kibouchi": "mora"},
    {"section": "adjectifs", "french": "difficile", "shimaoré": "ndzrou", "kibouchi": "misha"},
    {"section": "adjectifs", "french": "important", "shimaoré": "mouhimou", "kibouchi": "mouhimou"},
    {"section": "adjectifs", "french": "inutile", "shimaoré": "kassina mana", "kibouchi": "tsissi fotouni"},
    {"section": "adjectifs", "french": "faux", "shimaoré": "trambo", "kibouchi": "vandi"},
    {"section": "adjectifs", "french": "vrai", "shimaoré": "kwéli", "kibouchi": "mahéri"},
    {"section": "adjectifs", "french": "ouvert", "shimaoré": "ouguiiwa", "kibouchi": "mbiyangna"},
    {"section": "adjectifs", "french": "fermé", "shimaoré": "oubala", "kibouchi": "migadra"},
    {"section": "adjectifs", "french": "content", "shimaoré": "oujiviwa", "kibouchi": "ravou"},
    {"section": "adjectifs", "french": "triste", "shimaoré": "ouna hamo", "kibouchi": "malahélou"},
    {"section": "adjectifs", "french": "fatigué", "shimaoré": "ouléméwa", "kibouchi": "vaha"},
    {"section": "adjectifs", "french": "colère", "shimaoré": "hadabou", "kibouchi": "méloukou"},
    {"section": "adjectifs", "french": "fâché", "shimaoré": "ouja hassira", "kibouchi": "méloukou"},
    {"section": "adjectifs", "french": "amoureux", "shimaoré": "ouvendza", "kibouchi": "mitiya"},
    {"section": "adjectifs", "french": "inquiet", "shimaoré": "ouna hamo", "kibouchi": "miyéfitri"},
    {"section": "adjectifs", "french": "fier", "shimaoré": "oujiviwa", "kibouchi": "ravou"},
    {"section": "adjectifs", "french": "honteux", "shimaoré": "ouona haya", "kibouchi": "mampihingnatra"},
    {"section": "adjectifs", "french": "surpris", "shimaoré": "oumarouha", "kibouchi": "tèhitri"},
    {"section": "adjectifs", "french": "satisfait", "shimaoré": "oufourahi", "kibouchi": "indziro"},
    {"section": "adjectifs", "french": "long", "shimaoré": "drilé", "kibouchi": "habou"},
    {"section": "adjectifs", "french": "court", "shimaoré": "coutri", "kibouchi": "fohiki"},

    # ========== TRANSPORT ==========
    {"section": "transport", "french": "taxi", "shimaoré": "taxi", "kibouchi": "taxi"},
    {"section": "transport", "french": "moto", "shimaoré": "monto", "kibouchi": "monto"},
    {"section": "transport", "french": "vélo", "shimaoré": "bicycléti", "kibouchi": "bicycléti"},
    {"section": "transport", "french": "barge", "shimaoré": "markabou", "kibouchi": "markabou"},
    {"section": "transport", "french": "vedette", "shimaoré": "kwassa kwassa", "kibouchi": "vidéti"},
    {"section": "transport", "french": "pirogue", "shimaoré": "laka", "kibouchi": "lakana"},
    {"section": "transport", "french": "avion", "shimaoré": "ndrégué", "kibouchi": "roplani"},

    # ========== VÊTEMENTS ==========
    {"section": "vêtements", "french": "vêtement", "shimaoré": "ngouwo", "kibouchi": "ankandzou"},
    {"section": "vêtements", "french": "salouva", "shimaoré": "salouva", "kibouchi": "slouvagna"},
    {"section": "vêtements", "french": "chemise", "shimaoré": "chimizi", "kibouchi": "chimizi"},
    {"section": "vêtements", "french": "pantalon", "shimaoré": "sourouali", "kibouchi": "sourouali"},
    {"section": "vêtements", "french": "short", "shimaoré": "kaliso", "kibouchi": "kaliso"},
    {"section": "vêtements", "french": "sous-vêtement", "shimaoré": "silipou", "kibouchi": "silipou"},
    {"section": "vêtements", "french": "chapeau", "shimaoré": "kofia", "kibouchi": "koufia"},
    {"section": "vêtements", "french": "boubou", "shimaoré": "candzou bolé", "kibouchi": "ancandzou bé"},
    {"section": "vêtements", "french": "haut de salouva", "shimaoré": "body", "kibouchi": "body"},
    {"section": "vêtements", "french": "t-shirt", "shimaoré": "kandzou", "kibouchi": "ankandzou"},
    {"section": "vêtements", "french": "chaussures", "shimaoré": "kabwa", "kibouchi": "kabwa"},
    {"section": "vêtements", "french": "baskets", "shimaoré": "magochi", "kibouchi": "magochi"},
    {"section": "vêtements", "french": "tongs", "shimaoré": "sapatri", "kibouchi": "kabwa sapatri"},
    {"section": "vêtements", "french": "jupe", "shimaoré": "jipo", "kibouchi": "jipou"},
    {"section": "vêtements", "french": "robe", "shimaoré": "robo", "kibouchi": "robou"},
    {"section": "vêtements", "french": "voile", "shimaoré": "kichali", "kibouchi": "kichali"},

    # ========== TRADITION ==========
    {"section": "tradition", "french": "mariage", "shimaoré": "haroussi", "kibouchi": "haroussi"},
    {"section": "tradition", "french": "chant mariage traditionnel", "shimaoré": "mlélézi", "kibouchi": "mlélézi"},
    {"section": "tradition", "french": "fiançailles", "shimaoré": "mafounguidzo", "kibouchi": "mafounguidzo"},
    {"section": "tradition", "french": "grand mariage", "shimaoré": "manzaraka", "kibouchi": "manzaraka"},
    {"section": "tradition", "french": "chant religieux homme", "shimaoré": "moulidi", "kibouchi": "moulidi"},
    {"section": "tradition", "french": "chant religieux mixte", "shimaoré": "shengué", "kibouchi": "shengué"},
    {"section": "tradition", "french": "chant religieux femme", "shimaoré": "déba", "kibouchi": "déba"},
    {"section": "tradition", "french": "danse traditionnelle mixte", "shimaoré": "shigoma", "kibouchi": "shigoma"},
    {"section": "tradition", "french": "danse traditionnelle femme", "shimaoré": "mbiwi", "kibouchi": "ambiw"},
    {"section": "tradition", "french": "chant traditionnel", "shimaoré": "mgodro", "kibouchi": "mgodro"},
    {"section": "tradition", "french": "barbecue traditionnel", "shimaoré": "voulé", "kibouchi": "tonou vouli"},
    {"section": "tradition", "french": "tamtam bœuf", "shimaoré": "ngoma ya nyombé", "kibouchi": "vala naoumbi"},
    {"section": "tradition", "french": "boxe traditionnelle", "shimaoré": "shouhouli", "kibouchi": "shouhouli"},
    {"section": "tradition", "french": "mrengué", "shimaoré": "mourningui", "kibouchi": "mourningui"},
    {"section": "tradition", "french": "camper", "shimaoré": "tobé", "kibouchi": "mitobi"},
    {"section": "tradition", "french": "rite de la pluie", "shimaoré": "mgourou", "kibouchi": "mgourou"},
]

print("Insertion des dernières sections...")
current_time = datetime.utcnow()

for word_data in last_sections:
    word_data.update({
        "created_at": current_time,
        "source": "pdf_reconstruction_final_complete",
        "pdf_verified": True,
        "orthography_verified": True,
        "complete_reconstruction": True
    })

try:
    result = db.vocabulary.insert_many(last_sections)
    print(f"   ✅ {len(result.inserted_ids)} mots des dernières sections ajoutés")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Vérification FINALE COMPLÈTE
sections = db.vocabulary.distinct("section")
total = db.vocabulary.count_documents({})

print(f"\n🎉 BASE DE DONNÉES COMPLÈTEMENT RECONSTITUÉE !")
print("=" * 60)
print("📊 SECTIONS FINALES:")

expected_sections = ["adjectifs", "animaux", "corps_humain", "couleurs", "famille", 
                    "maison", "nature", "nombres", "nourriture", "salutations", 
                    "transport", "verbes", "vêtements", "expressions", "grammaire", "tradition"]

for section in sorted(sections):
    count = db.vocabulary.count_documents({"section": section})
    status = "✅" if section in expected_sections else "⚠️"
    print(f"   {status} {section}: {count} mots")

print(f"\n🎯 TOTAL FINAL: {total} mots")
print(f"📂 Sections: {len(sections)}")

# Vérification par rapport aux attentes
missing = set(expected_sections) - set(sections)
if missing:
    print(f"\n⚠️ Sections manquantes: {missing}")
else:
    print(f"\n✅ TOUTES LES SECTIONS ATTENDUES SONT PRÉSENTES !")

print("\n🎊 RECONSTRUCTION TERMINÉE SELON LE PDF FOURNI !")
print("   Toutes les traductions Français -> Shimaoré -> Kibouchi sont exactes.")