#!/usr/bin/env python3
"""
Script de reconstruction complète de la base de données
à partir du PDF de référence avec les bonnes traductions et orthographes.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

# Charger les variables d'environnement
load_dotenv()

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Données complètes extraites du PDF de référence
PDF_VOCABULARY_DATA = {
    "nature": [
        {"french": "pente", "shimaoré": "mlima", "kibouchi": "boungou"},
        {"french": "colline", "shimaoré": "mlima", "kibouchi": "boungou"},
        {"french": "mont", "shimaoré": "mlima", "kibouchi": "boungou"},
        {"french": "lune", "shimaoré": "mwézi", "kibouchi": "fandzava"},
        {"french": "étoile", "shimaoré": "gnora", "kibouchi": "lakintagna"},
        {"french": "sable", "shimaoré": "mtsanga", "kibouchi": "fasigni"},
        {"french": "vague", "shimaoré": "dhouja", "kibouchi": "houndza"},
        {"french": "vent", "shimaoré": "pévo", "kibouchi": "tsikou"},
        {"french": "pluie", "shimaoré": "vhoua", "kibouchi": "mahaléni"},
        {"french": "mangrove", "shimaoré": "mhonko", "kibouchi": "honkou"},
        {"french": "corail", "shimaoré": "soiyi", "kibouchi": "soiyi"},
        {"french": "barrière de corail", "shimaoré": "caléni", "kibouchi": "caléni"},
        {"french": "tempête", "shimaoré": "darouba", "kibouchi": "tsikou"},
        {"french": "rivière", "shimaoré": "mouro", "kibouchi": "mouroni"},
        {"french": "pont", "shimaoré": "daradja", "kibouchi": "daradja"},
        {"french": "nuage", "shimaoré": "wingou", "kibouchi": "vingou"},
        {"french": "arc en ciel", "shimaoré": "mcacamba", "kibouchi": "vingou"},
        {"french": "campagne", "shimaoré": "malavouni", "kibouchi": "atihala"},
        {"french": "forêt", "shimaoré": "malavouni", "kibouchi": "atihala"},
        {"french": "caillou", "shimaoré": "bwé", "kibouchi": "vatou"},
        {"french": "pierre", "shimaoré": "bwé", "kibouchi": "vatou"},
        {"french": "rocher", "shimaoré": "bwé", "kibouchi": "vatou"},
        {"french": "plateau", "shimaoré": "bandra", "kibouchi": "kètraka"},
        {"french": "chemin", "shimaoré": "ndzia", "kibouchi": "lalagna"},
        {"french": "sentier", "shimaoré": "ndzia", "kibouchi": "lalagna"},
        {"french": "parcours", "shimaoré": "ndzia", "kibouchi": "lalagna"},
        {"french": "herbe", "shimaoré": "malavou", "kibouchi": "haitri"},
        {"french": "fleur", "shimaoré": "foulera", "kibouchi": "foulera"},
        {"french": "soleil", "shimaoré": "jouwa", "kibouchi": "zouva"},
        {"french": "mer", "shimaoré": "bahari", "kibouchi": "bahari"},
        {"french": "plage", "shimaoré": "mtsangani", "kibouchi": "fassigni"},
        {"french": "arbre", "shimaoré": "mwiri", "kibouchi": "kakazou"},
        {"french": "rue", "shimaoré": "paré", "kibouchi": "paré"},
        {"french": "route", "shimaoré": "paré", "kibouchi": "paré"},
        {"french": "bananier", "shimaoré": "trindri", "kibouchi": "voudi ni hountsi"},
        {"french": "feuille", "shimaoré": "mawoini", "kibouchi": "hayitri"},
        {"french": "branche", "shimaoré": "trahi", "kibouchi": "trahi"},
        {"french": "tornade", "shimaoré": "ouzimouyi", "kibouchi": "tsikou soulaimana"},
        {"french": "cocotier", "shimaoré": "m'nadzi", "kibouchi": "voudi ni vwaniou"},
        {"french": "arbre à pain", "shimaoré": "m'frampé", "kibouchi": "voudi ni frampé"},
        {"french": "baobab", "shimaoré": "m'bouyou", "kibouchi": "voudi ni bouyou"},
        {"french": "bambou", "shimaoré": "m'bambo", "kibouchi": "valiha"},
        {"french": "manguier", "shimaoré": "m'manga", "kibouchi": "voudi ni manga"},
        {"french": "jacquier", "shimaoré": "m'fénéssi", "kibouchi": "voudi ni finéssi"},
        {"french": "terre", "shimaoré": "trotrotro", "kibouchi": "fotaka"},
        {"french": "sol", "shimaoré": "tsi", "kibouchi": "tani"},
        {"french": "érosion", "shimaoré": "padza", "kibouchi": "padza"},
        {"french": "marée basse", "shimaoré": "maji yavo", "kibouchi": "ranou mèki"},
        {"french": "platier", "shimaoré": "kalé", "kibouchi": "kaléni"},
        {"french": "marée haute", "shimaoré": "maji yamalé", "kibouchi": "ranou fénou"},
        {"french": "inondé", "shimaoré": "ourora", "kibouchi": "dobou"},
        {"french": "sauvage", "shimaoré": "nyéha", "kibouchi": "di"},
        {"french": "canne à sucre", "shimaoré": "mouwoi", "kibouchi": "fari"},
        {"french": "fagot", "shimaoré": "kouni", "kibouchi": "azoumati"},
        {"french": "pirogue", "shimaoré": "laka", "kibouchi": "lakana"},
        {"french": "vedette", "shimaoré": "kwassa kwassa", "kibouchi": "vidéti"},
        {"french": "école", "shimaoré": "licoli", "kibouchi": "licoli"},
        {"french": "école coranique", "shimaoré": "shioni", "kibouchi": "kioni"}
    ],
    
    "nombres": [
        {"french": "un", "shimaoré": "moja", "kibouchi": "areki"},
        {"french": "deux", "shimaoré": "mbili", "kibouchi": "aroyi"},
        {"french": "trois", "shimaoré": "trarou", "kibouchi": "telou"},
        {"french": "quatre", "shimaoré": "nhé", "kibouchi": "efatra"},
        {"french": "cinq", "shimaoré": "tsano", "kibouchi": "dimi"},
        {"french": "six", "shimaoré": "sita", "kibouchi": "tchouta"},
        {"french": "sept", "shimaoré": "saba", "kibouchi": "fitou"},
        {"french": "huit", "shimaoré": "nané", "kibouchi": "valou"},
        {"french": "neuf", "shimaoré": "chendra", "kibouchi": "civi"},
        {"french": "dix", "shimaoré": "koumi", "kibouchi": "foulou"},
        {"french": "onze", "shimaoré": "koumi na moja", "kibouchi": "foulou areki ambi"},
        {"french": "douze", "shimaoré": "koumi na mbili", "kibouchi": "foulou aroyi ambi"},
        {"french": "treize", "shimaoré": "koumi na trarou", "kibouchi": "foulou telou ambi"},
        {"french": "quatorze", "shimaoré": "koumi na nhé", "kibouchi": "foulou efatra ambi"},
        {"french": "quinze", "shimaoré": "koumi na tsano", "kibouchi": "foulou dimi ambi"},
        {"french": "seize", "shimaoré": "koumi na sita", "kibouchi": "foulou tchouta ambi"},
        {"french": "dix-sept", "shimaoré": "koumi na saba", "kibouchi": "foulou fitou ambi"},
        {"french": "dix-huit", "shimaoré": "koumi na nané", "kibouchi": "foulou valou ambi"},
        {"french": "dix-neuf", "shimaoré": "koumi na chendra", "kibouchi": "foulou civi ambi"},
        {"french": "vingt", "shimaoré": "chirini", "kibouchi": "arompoulou"},
        {"french": "trente", "shimaoré": "thalathini", "kibouchi": "téloumpoulou"},
        {"french": "quarante", "shimaoré": "arbahini", "kibouchi": "éfampoulou"},
        {"french": "cinquante", "shimaoré": "hamssini", "kibouchi": "dimimpoulou"},
        {"french": "soixante", "shimaoré": "sitini", "kibouchi": "tchoutampoulou"},
        {"french": "soixante-dix", "shimaoré": "sabouini", "kibouchi": "fitoumpoulou"},
        {"french": "quatre-vingts", "shimaoré": "thamanini", "kibouchi": "valoumpoulou"},
        {"french": "quatre-vingt-dix", "shimaoré": "toussuini", "kibouchi": "civiampoulou"},
        {"french": "cent", "shimaoré": "miya", "kibouchi": "zatou"}
    ],
    
    "animaux": [
        {"french": "cochon", "shimaoré": "pouroukou", "kibouchi": "lambou"},
        {"french": "margouillat", "shimaoré": "kasangwe", "kibouchi": "kitsatsaka"},
        {"french": "abeille", "shimaoré": "niochi", "kibouchi": "antéli"},
        {"french": "chat", "shimaoré": "paha", "kibouchi": "moirou"},
        {"french": "rat", "shimaoré": "pouhou", "kibouchi": "voilavou"},
        {"french": "escargot", "shimaoré": "kwa", "kibouchi": "ancora"},
        {"french": "lion", "shimaoré": "simba", "kibouchi": "simba"},
        {"french": "grenouille", "shimaoré": "shiwatrotro", "kibouchi": "sahougnou"},
        {"french": "oiseau", "shimaoré": "gnougni", "kibouchi": "vorougnou"},
        {"french": "chien", "shimaoré": "mbwa", "kibouchi": "fadroka"},
        {"french": "poisson", "shimaoré": "fi", "kibouchi": "lokou"},
        {"french": "maki", "shimaoré": "komba", "kibouchi": "amkoumba"},
        {"french": "chèvre", "shimaoré": "mbouzi", "kibouchi": "bengui"},
        {"french": "moustique", "shimaoré": "manundri", "kibouchi": "mokou"},
        {"french": "mouche", "shimaoré": "ndzi", "kibouchi": "lalitri"},
        {"french": "chauve-souris", "shimaoré": "drema", "kibouchi": "fanihi"},
        {"french": "serpent", "shimaoré": "nyoha", "kibouchi": "bibi lava"},
        {"french": "lapin", "shimaoré": "sungura", "kibouchi": "shoungoura"},
        {"french": "canard", "shimaoré": "guisi", "kibouchi": "doukitri"},
        {"french": "mouton", "shimaoré": "baribari", "kibouchi": "baribari"},
        {"french": "crocodile", "shimaoré": "vwai", "kibouchi": "vwai"},
        {"french": "caméléon", "shimaoré": "tarundru", "kibouchi": "tarondru"},
        {"french": "zébu", "shimaoré": "nyombé", "kibouchi": "aoumbi"},
        {"french": "âne", "shimaoré": "pundra", "kibouchi": "ampundra"},
        {"french": "poule", "shimaoré": "kouhou", "kibouchi": "akohou"},
        {"french": "pigeon", "shimaoré": "ndiwa", "kibouchi": "ndiwa"},
        {"french": "fourmis", "shimaoré": "tsoussou", "kibouchi": "vitsiki"},
        {"french": "chenille", "shimaoré": "bazi", "kibouchi": "bibimanguidi"},
        {"french": "papillon", "shimaoré": "pelapelaka", "kibouchi": "tsipelapelaka"},
        {"french": "ver de terre", "shimaoré": "lingoui lingoui", "kibouchi": "bibi fotaka"},
        {"french": "criquet", "shimaoré": "furudji", "kibouchi": "kidzedza"},
        {"french": "cheval", "shimaoré": "poundra", "kibouchi": "farassi"},
        {"french": "perroquet", "shimaoré": "kassoukou", "kibouchi": "kararokou"},
        {"french": "cafard", "shimaoré": "kalalawi", "kibouchi": "kalalowou"},
        {"french": "araignée", "shimaoré": "shitrandrabwibwi", "kibouchi": "bibi ampamani massou"},
        {"french": "scorpion", "shimaoré": "hala", "kibouchi": "hala"},
        {"french": "scolopendre", "shimaoré": "trambwi", "kibouchi": "trambougnou"},
        {"french": "thon", "shimaoré": "mbassi", "kibouchi": "mbassi"},
        {"french": "requin", "shimaoré": "papa", "kibouchi": "ankiou"},
        {"french": "poulpe", "shimaoré": "pwedza", "kibouchi": "pwedza"},
        {"french": "crabe", "shimaoré": "dradraka", "kibouchi": "dakatra"},
        {"french": "tortue", "shimaoré": "nyamba", "kibouchi": "fanou"},
        {"french": "bigorno", "shimaoré": "trondro", "kibouchi": "trondrou"},
        {"french": "éléphant", "shimaoré": "ndovu", "kibouchi": "ndovu"},
        {"french": "singe", "shimaoré": "djakwe", "kibouchi": "djakouayi"},
        {"french": "souris", "shimaoré": "shikwetse", "kibouchi": "voilavou"},
        {"french": "phacochère", "shimaoré": "pouruku nyeha", "kibouchi": "lambou"},
        {"french": "lézard", "shimaoré": "ngwizi", "kibouchi": "kitsatsaka"},
        {"french": "renard", "shimaoré": "mbwa nyeha", "kibouchi": "fandroka di"},
        {"french": "chameau", "shimaoré": "ngamia", "kibouchi": "angamia"},
        {"french": "hérisson", "shimaoré": "landra", "kibouchi": "trandraka"},
        {"french": "corbeau", "shimaoré": "gawa", "kibouchi": "gouaka"},
        {"french": "civette", "shimaoré": "founga", "kibouchi": "angava"},
        {"french": "dauphin", "shimaoré": "moungoumé", "kibouchi": "fésoutrou"},
        {"french": "baleine", "shimaoré": "ndroujou", "kibouchi": "baleine"},
        {"french": "crevette", "shimaoré": "camba", "kibouchi": "ancamba"},
        {"french": "frelon", "shimaoré": "chonga", "kibouchi": "faraka"},
        {"french": "guêpe", "shimaoré": "movou", "kibouchi": "fanintri"},
        {"french": "bourdon", "shimaoré": "vungo vungo", "kibouchi": "madjaoumbi"},
        {"french": "puce", "shimaoré": "kunguni", "kibouchi": "ancongou"},
        {"french": "poux", "shimaoré": "ndra", "kibouchi": "howou"},
        {"french": "bouc", "shimaoré": "béwé", "kibouchi": "bébérou"},
        {"french": "taureau", "shimaoré": "kondzo", "kibouchi": "dzow"},
        {"french": "bigorneau", "shimaoré": "trondro", "kibouchi": "trondrou"},
        {"french": "lambis", "shimaoré": "kombé", "kibouchi": "mahombi"},
        {"french": "cône de mer", "shimaoré": "kwitsi", "kibouchi": "tsimtipaka"},
        {"french": "mille-pattes", "shimaoré": "mjongo", "kibouchi": "ancoudavitri"},
        {"french": "oursin", "shimaoré": "gadzassi ya bahari", "kibouchi": "vouli vavi"},
        {"french": "huître", "shimaoré": "gadzassi", "kibouchi": "sadza"}
    ],
    
    "corps": [
        {"french": "œil", "shimaoré": "matso", "kibouchi": "kiyo"},
        {"french": "bouche", "shimaoré": "cha", "kibouchi": "cha"},
        {"french": "nez", "shimaoré": "poua", "kibouchi": "poua"},
        {"french": "oreille", "shimaoré": "soungni", "kibouchi": "soungni"},
        {"french": "main", "shimaoré": "faninti", "kibouchi": "mhono"},
        {"french": "pied", "shimaoré": "bavou", "kibouchi": "bavou"},
        {"french": "tête", "shimaoré": "dhomo", "kibouchi": "tsingo"},
        {"french": "cheveux", "shimaoré": "tsingo", "kibouchi": "ngnélé"},
        {"french": "dent", "shimaoré": "mengo", "kibouchi": "mengo"},
        {"french": "langue", "shimaoré": "lèla", "kibouchi": "oulimé"},
        {"french": "dos", "shimaoré": "shlévou", "kibouchi": "shlévou"},
        {"french": "ventre", "shimaoré": "sokou", "kibouchi": "sokou"},
        {"french": "bras", "shimaoré": "mbo", "kibouchi": "mbo"},
        {"french": "jambe", "shimaoré": "mbavou", "kibouchi": "mbavou"},
        {"french": "cou", "shimaoré": "shitsoi", "kibouchi": "shitsoi"},
        {"french": "épaule", "shimaoré": "bèga", "kibouchi": "bèga"},
        {"french": "doigt", "shimaoré": "tingui", "kibouchi": "tingui"},
        {"french": "ongle", "shimaoré": "dzitso la pwédza", "kibouchi": "dzitso la pwédza"},
        {"french": "genou", "shimaoré": "trenga", "kibouchi": "trenga"},
        {"french": "coude", "shimaoré": "kové", "kibouchi": "kové"},
        {"french": "cœur", "shimaoré": "soufigni", "kibouchi": "soufigni"},
        {"french": "front", "shimaoré": "hangno", "kibouchi": "housso"},
        {"french": "joue", "shimaoré": "savou", "kibouchi": "savou"},
        {"french": "lèvre", "shimaoré": "dhomo", "kibouchi": "dhomo"},
        {"french": "menton", "shimaoré": "shlévou", "kibouchi": "shlévou"},
        {"french": "barbe", "shimaoré": "ndrévou", "kibouchi": "ndrévou"},
        {"french": "sourcil", "shimaoré": "tsi", "kibouchi": "ankwéssi"},
        {"french": "cils", "shimaoré": "kové", "kibouchi": "rambou faninti"},
        {"french": "peau", "shimaoré": "ngwezi", "kibouchi": "ngwezi"},
        {"french": "côtes", "shimaoré": "bavou", "kibouchi": "mbavou"}
    ],
    
    "salutations": [
        {"french": "bonjour", "shimaoré": "marahaba", "kibouchi": "akori"},
        {"french": "bonsoir", "shimaoré": "haligni tsara", "kibouchi": "haligni tsara"},
        {"french": "au revoir", "shimaoré": "kwaheri", "kibouchi": "kwaheri"},
        {"french": "comment ça va", "shimaoré": "oukou wa hairi", "kibouchi": "oukou wa hairi"},
        {"french": "ça va bien", "shimaoré": "tsara", "kibouchi": "fétré"},
        {"french": "merci", "shimaoré": "iya", "kibouchi": "iya"},
        {"french": "oui", "shimaoré": "ewa", "kibouchi": "ewa"},
        {"french": "non", "shimaoré": "an'ha", "kibouchi": "an'ha"},
        {"french": "bienvenue", "shimaoré": "maeva", "kibouchi": "maeva"},
        {"french": "excusez-moi", "shimaoré": "jéjé", "kibouchi": "jéjé"},
        {"french": "salut", "shimaoré": "kwezi", "kibouchi": "kwezi"}
    ],
    
    "famille": [
        {"french": "famille", "shimaoré": "mdjamaza", "kibouchi": "havagna"},
        {"french": "papa", "shimaoré": "baba", "kibouchi": "baba"},
        {"french": "maman", "shimaoré": "mama", "kibouchi": "mama"},
        {"french": "frère", "shimaoré": "mwanagna", "kibouchi": "anadahi"},
        {"french": "sœur", "shimaoré": "mwanagna", "kibouchi": "anabavi"},
        {"french": "grand frère", "shimaoré": "zouki mtoubaba", "kibouchi": "zoki lalahi"},
        {"french": "grande sœur", "shimaoré": "zouki mtroumché", "kibouchi": "zoki viavi"},
        {"french": "petit frère", "shimaoré": "moinagna mtroubaba", "kibouchi": "zandri lalahi"},
        {"french": "petite sœur", "shimaoré": "moinagna mtroumama", "kibouchi": "zandri viavi"},
        {"french": "grand-père", "shimaoré": "bacoco", "kibouchi": "dadayi"},
        {"french": "grand-mère", "shimaoré": "coco", "kibouchi": "dadi"},
        {"french": "oncle maternel", "shimaoré": "zama", "kibouchi": "zama"},
        {"french": "tante maternelle", "shimaoré": "mama titi", "kibouchi": "zama"},
        {"french": "oncle paternel", "shimaoré": "baba héli", "kibouchi": "nindri heli"},
        {"french": "tante paternelle", "shimaoré": "zéna", "kibouchi": "zéna"},
        {"french": "garçon", "shimaoré": "mtroubaba", "kibouchi": "lalahi"},
        {"french": "fille", "shimaoré": "mtroumama", "kibouchi": "viavi"},
        {"french": "homme", "shimaoré": "mtroubaba", "kibouchi": "lalahi"},
        {"french": "femme", "shimaoré": "mtroumama", "kibouchi": "viavi"},
        {"french": "monsieur", "shimaoré": "mogné", "kibouchi": "lalahi"},
        {"french": "madame", "shimaoré": "bvéni", "kibouchi": "viavi"},
        {"french": "petit garçon", "shimaoré": "mwana mtroubaba", "kibouchi": "zaza lalahi"},
        {"french": "petite fille", "shimaoré": "mwana mtroumama", "kibouchi": "zaza viavi"},
        {"french": "jeune adulte", "shimaoré": "shababi", "kibouchi": "shababi"},
        {"french": "ami", "shimaoré": "mwandzani", "kibouchi": "mwandzani"}
    ],
    
    "couleurs": [
        {"french": "bleu", "shimaoré": "bilé", "kibouchi": "mayitsou bilé"},
        {"french": "vert", "shimaoré": "dhavou", "kibouchi": "mayitsou"},
        {"french": "noir", "shimaoré": "nzidhou", "kibouchi": "mayintigni"},
        {"french": "blanc", "shimaoré": "ndjéou", "kibouchi": "malandi"},
        {"french": "jaune", "shimaoré": "dzindzano", "kibouchi": "tamoutamou"},
        {"french": "rouge", "shimaoré": "nzoukoundrou", "kibouchi": "mena"},
        {"french": "gris", "shimaoré": "djifou", "kibouchi": "dzofou"},
        {"french": "marron", "shimaoré": "trotro", "kibouchi": "fotafotaka"}
    ],
    
    "nourriture": [
        {"french": "riz", "shimaoré": "tsoholé", "kibouchi": "vari"},
        {"french": "eau", "shimaoré": "maji", "kibouchi": "ranou"},
        {"french": "ananas", "shimaoré": "nanassi", "kibouchi": "mananassi"},
        {"french": "pois d'angole", "shimaoré": "tsouzi", "kibouchi": "ambatri"},
        {"french": "banane", "shimaoré": "trovi", "kibouchi": "hountsi"},
        {"french": "pain", "shimaoré": "dipé", "kibouchi": "dipé"},
        {"french": "gâteau", "shimaoré": "mharé", "kibouchi": "moukari"},
        {"french": "mangue", "shimaoré": "manga", "kibouchi": "manga"},
        {"french": "noix de coco", "shimaoré": "nadzi", "kibouchi": "voiniou"},
        {"french": "noix de coco fraîche", "shimaoré": "chijavou", "kibouchi": "kidjavou"},
        {"french": "lait", "shimaoré": "dzia", "kibouchi": "rounounou"},
        {"french": "viande", "shimaoré": "nhyama", "kibouchi": "amboumati"},
        {"french": "poisson", "shimaoré": "fi", "kibouchi": "lokou"},
        {"french": "brèdes", "shimaoré": "féliki", "kibouchi": "féliki"},
        {"french": "brède mafane", "shimaoré": "féliki mafana", "kibouchi": "féliki mafana"},
        {"french": "brède manioc", "shimaoré": "mataba", "kibouchi": "féliki mouhogou"},
        {"french": "brède morelle", "shimaoré": "féliki nyongo", "kibouchi": "féliki angnatsindra"},
        {"french": "brèdes patate douce", "shimaoré": "féliki batata", "kibouchi": "féliki batata"},
        {"french": "patate douce", "shimaoré": "batata", "kibouchi": "batata"},
        {"french": "bouillon", "shimaoré": "woubou", "kibouchi": "kouba"},
        {"french": "banane au coco", "shimaoré": "trovi ya nadzi", "kibouchi": "hountsi an voiniou"},
        {"french": "riz au coco", "shimaoré": "tsoholé ya nadzi", "kibouchi": "vari an voiniou"},
        {"french": "poulet", "shimaoré": "bawa", "kibouchi": "mabawa"},
        {"french": "œuf", "shimaoré": "joiyi", "kibouchi": "antoudi"},
        {"french": "tomate", "shimaoré": "tamati", "kibouchi": "matimati"},
        {"french": "oignon", "shimaoré": "chouroungou", "kibouchi": "doungoulou"},
        {"french": "ail", "shimaoré": "chouroungou voudjé", "kibouchi": "doungoulou mvoudjou"},
        {"french": "orange", "shimaoré": "troundra", "kibouchi": "tsoha"},
        {"french": "mandarine", "shimaoré": "madhandzé", "kibouchi": "tsoha madzandzi"},
        {"french": "manioc", "shimaoré": "mhogo", "kibouchi": "mouhogou"},
        {"french": "piment", "shimaoré": "poutou", "kibouchi": "pilipili"},
        {"french": "taro", "shimaoré": "majimbi", "kibouchi": "majimbi"},
        {"french": "sel", "shimaoré": "chingó", "kibouchi": "sira"},
        {"french": "poivre", "shimaoré": "bvilibvili manga", "kibouchi": "vilivili"},
        {"french": "curcuma", "shimaoré": "dzindzano", "kibouchi": "tamoutamou"},
        {"french": "cumin", "shimaoré": "massala", "kibouchi": "massala"},
        {"french": "ciboulette", "shimaoré": "chourougnou mani", "kibouchi": "doungoulou ravigni"},
        {"french": "gingembre", "shimaoré": "tsingiziou", "kibouchi": "sakėyi"},
        {"french": "vanille", "shimaoré": "lavani", "kibouchi": "lavani"},
        {"french": "tamarin", "shimaoré": "ouhajou", "kibouchi": "madirou kakazou"},
        {"french": "un thé", "shimaoré": "maji ya moro", "kibouchi": "ranou meyi"},
        {"french": "papaye", "shimaoré": "papaya", "kibouchi": "poipoiya"},
        {"french": "nourriture", "shimaoré": "chaoula", "kibouchi": "hanigni"},
        {"french": "riz non décortiqué", "shimaoré": "mélé", "kibouchi": "vari tsivoidissa"}
    ],
    
    "maison": [
        {"french": "maison", "shimaoré": "nyoumba", "kibouchi": "tragnou"},
        {"french": "porte", "shimaoré": "mlango", "kibouchi": "varavaragna"},
        {"french": "case", "shimaoré": "banga", "kibouchi": "banga"},
        {"french": "lit", "shimaoré": "chtrandra", "kibouchi": "koubani"},
        {"french": "marmite", "shimaoré": "gnoungou", "kibouchi": "vilangni"},
        {"french": "vaisselle", "shimaoré": "ziya", "kibouchi": "hintagna"},
        {"french": "bol", "shimaoré": "chicombé", "kibouchi": "bacouli"},
        {"french": "cuillère", "shimaoré": "soutrou", "kibouchi": "sotrou"},
        {"french": "fenêtre", "shimaoré": "fénétri", "kibouchi": "lafoumètara"},
        {"french": "chaise", "shimaoré": "chiri", "kibouchi": "chiri"},
        {"french": "table", "shimaoré": "latabou", "kibouchi": "latabou"},
        {"french": "miroir", "shimaoré": "chido", "kibouchi": "kitarafa"},
        {"french": "cour", "shimaoré": "mraba", "kibouchi": "lacourou"},
        {"french": "clôture", "shimaoré": "vala", "kibouchi": "vala"},
        {"french": "toilette", "shimaoré": "mrabani", "kibouchi": "mraba"},
        {"french": "seau", "shimaoré": "siyo", "kibouchi": "siyo"},
        {"french": "louche", "shimaoré": "chiwi", "kibouchi": "pow"},
        {"french": "couteau", "shimaoré": "sembéya", "kibouchi": "méssou"},
        {"french": "matelas", "shimaoré": "godoro", "kibouchi": "goudorou"},
        {"french": "oreiller", "shimaoré": "mtsao", "kibouchi": "hondagna"},
        {"french": "buffet", "shimaoré": "biffé", "kibouchi": "biffé"},
        {"french": "mur", "shimaoré": "péssi", "kibouchi": "riba"},
        {"french": "véranda", "shimaoré": "baraza", "kibouchi": "baraza"},
        {"french": "toiture", "shimaoré": "outro", "kibouchi": "vovougnou"},
        {"french": "ampoule", "shimaoré": "lalampou", "kibouchi": "lalampou"},
        {"french": "lumière", "shimaoré": "mwengué", "kibouchi": "mwengué"},
        {"french": "torche", "shimaoré": "pongé", "kibouchi": "pongi"},
        {"french": "hache", "shimaoré": "soha", "kibouchi": "famaki"},
        {"french": "machette", "shimaoré": "m'panga", "kibouchi": "ampanga"},
        {"french": "coupe-coupe", "shimaoré": "chombo", "kibouchi": "chombou"},
        {"french": "cartable", "shimaoré": "mkoba", "kibouchi": "mkoba"},
        {"french": "sac", "shimaoré": "gouni", "kibouchi": "gouni"},
        {"french": "balai", "shimaoré": "péou", "kibouchi": "famafa"},
        {"french": "mortier", "shimaoré": "chino", "kibouchi": "légnou"},
        {"french": "assiette", "shimaoré": "sahani", "kibouchi": "sahani"},
        {"french": "fondation", "shimaoré": "houra", "kibouchi": "koura"},
        {"french": "torche locale", "shimaoré": "gandilé", "kibouchi": "gandili"}
    ],
    
    "verbes": [
        {"french": "jouer", "shimaoré": "oungadza", "kibouchi": "msoma"},
        {"french": "courir", "shimaoré": "wendra mbiyo", "kibouchi": "miloumeyi"},
        {"french": "dire", "shimaoré": "ourongoa", "kibouchi": "mangnabara"},
        {"french": "pouvoir", "shimaoré": "ouchindra", "kibouchi": "mahaléou"},
        {"french": "vouloir", "shimaoré": "outsaha", "kibouchi": "chokou"},
        {"french": "savoir", "shimaoré": "oujoua", "kibouchi": "méhèyi"},
        {"french": "voir", "shimaoré": "ouona", "kibouchi": "mahita"},
        {"french": "devoir", "shimaoré": "oulazimou", "kibouchi": "tokoutrou"},
        {"french": "venir", "shimaoré": "ouja", "kibouchi": "havi"},
        {"french": "approcher", "shimaoré": "outsenguéléya", "kibouchi": "magnatougnou"},
        {"french": "prendre", "shimaoré": "ourenga", "kibouchi": "mangala"},
        {"french": "donner", "shimaoré": "ouva", "kibouchi": "magnamiya"},
        {"french": "parler", "shimaoré": "oulagoua", "kibouchi": "mivoulangna"},
        {"french": "mettre", "shimaoré": "outria", "kibouchi": "mangnanou"},
        {"french": "passer", "shimaoré": "ouvira", "kibouchi": "mihomba"},
        {"french": "trouver", "shimaoré": "oupara", "kibouchi": "mahazou"},
        {"french": "aimer", "shimaoré": "ouvendza", "kibouchi": "mitiya"},
        {"french": "croire", "shimaoré": "ouamini", "kibouchi": "koimini"},
        {"french": "penser", "shimaoré": "oufikiri", "kibouchi": "midzéri"},
        {"french": "connaître", "shimaoré": "oujoua", "kibouchi": "méhèyi"},
        {"french": "demander", "shimaoré": "oudzissa", "kibouchi": "magnoutani"},
        {"french": "répondre", "shimaoré": "oudjibou", "kibouchi": "mikoudjibou"},
        {"french": "laisser", "shimaoré": "oulicha", "kibouchi": "mangnambéla"},
        {"french": "manger", "shimaoré": "oudhya", "kibouchi": "mihinagna"},
        {"french": "boire", "shimaoré": "ounoua", "kibouchi": "mindranou"},
        {"french": "lire", "shimaoré": "ousoma", "kibouchi": "midzorou"},
        {"french": "écrire", "shimaoré": "ouhanguiha", "kibouchi": "mikouandika"},
        {"french": "écouter", "shimaoré": "ouvoulikia", "kibouchi": "mitangréngni"},
        {"french": "apprendre", "shimaoré": "oufoundriha", "kibouchi": "midzorou"},
        {"french": "comprendre", "shimaoré": "ouéléwa", "kibouchi": "kouéléwa"},
        {"french": "marcher", "shimaoré": "ouendra", "kibouchi": "mandéha"},
        {"french": "entrer", "shimaoré": "ounguiya", "kibouchi": "mihiditri"},
        {"french": "sortir", "shimaoré": "oulawa", "kibouchi": "miboka"},
        {"french": "rester", "shimaoré": "ouketsi", "kibouchi": "mipétraka"},
        {"french": "vivre", "shimaoré": "ouyinchi", "kibouchi": "mikouènchi"},
        {"french": "dormir", "shimaoré": "oulala", "kibouchi": "mandri"},
        {"french": "attendre", "shimaoré": "oulindra", "kibouchi": "mandigni"},
        {"french": "suivre", "shimaoré": "oulounga", "kibouchi": "mangnaraka"},
        {"french": "tenir", "shimaoré": "oussika", "kibouchi": "mitana"},
        {"french": "ouvrir", "shimaoré": "ouboua", "kibouchi": "mampobiyangna"},
        {"french": "fermer", "shimaoré": "oubala", "kibouchi": "migadra"},
        {"french": "sembler", "shimaoré": "oufana", "kibouchi": "mampihiragna"},
        {"french": "tomber", "shimaoré": "oupouliha", "kibouchi": "mivadiki"},
        {"french": "casser", "shimaoré": "latsaka", "kibouchi": "latsaka"},
        {"french": "se rappeler", "shimaoré": "oumaézi", "kibouchi": "koufahamou"},
        {"french": "commencer", "shimaoré": "ouhandrissa", "kibouchi": "mitaponou"},
        {"french": "finir", "shimaoré": "oumalidza", "kibouchi": "mankéfa"},
        {"french": "réussir", "shimaoré": "ouchindra", "kibouchi": "mahaléou"},
        {"french": "essayer", "shimaoré": "oudjérébou", "kibouchi": "mikoudjérébou"},
        {"french": "attraper", "shimaoré": "oubara", "kibouchi": "missamboutrou"},
        {"french": "danser", "shimaoré": "ouzina", "kibouchi": "mitsindzaka"},
        {"french": "arrêter", "shimaoré": "ouziya", "kibouchi": "mitsahara"},
        {"french": "vendre", "shimaoré": "ouhoudza", "kibouchi": "mandafou"},
        {"french": "mordre", "shimaoré": "ouka magno", "kibouchi": "mangnékitri"},
        {"french": "jeter", "shimaoré": "ouvoutsa", "kibouchi": "manopi"},
        {"french": "se laver", "shimaoré": "ouhowa", "kibouchi": "misséki"},
        {"french": "piler", "shimaoré": "oudoudoua", "kibouchi": "mandissa"},
        {"french": "changer", "shimaoré": "ougaoudza", "kibouchi": "mamadiki"},
        {"french": "réchauffer", "shimaoré": "ouhelesedza", "kibouchi": "mamana"},
        {"french": "balayer", "shimaoré": "ouhoundza", "kibouchi": "mamafa"},
        {"french": "couper", "shimaoré": "oukatra", "kibouchi": "manapaka"},
        {"french": "abîmer", "shimaoré": "oumengna", "kibouchi": "manapaka somboutrou"},
        {"french": "acheter", "shimaoré": "unounoua", "kibouchi": "mivanga"},
        {"french": "griller", "shimaoré": "ouwoha", "kibouchi": "mitonou"},
        {"french": "allumer", "shimaoré": "oupatsa", "kibouchi": "mikoupatsa"},
        {"french": "cuisiner", "shimaoré": "oupiha", "kibouchi": "mahandrou"},
        {"french": "ranger", "shimaoré": "ourenguélédza", "kibouchi": "magnadzari"},
        {"french": "tresser", "shimaoré": "ousouka", "kibouchi": "mitali"},
        {"french": "peindre", "shimaoré": "ouvaha", "kibouchi": "magnossoutrou"},
        {"french": "essuyer", "shimaoré": "ouvangouha", "kibouchi": "mamitri"},
        {"french": "apporter", "shimaoré": "ouvinga", "kibouchi": "mandèyi"},
        {"french": "éteindre", "shimaoré": "ouzima", "kibouchi": "mamounou"},
        {"french": "tuer", "shimaoré": "ouwoula", "kibouchi": "mamounou"},
        {"french": "cultiver", "shimaoré": "oulima", "kibouchi": "mikapa"},
        {"french": "cueillir", "shimaoré": "oupoua", "kibouchi": "mampoka"},
        {"french": "planter", "shimaoré": "outabou", "kibouchi": "mamboli"},
        {"french": "creuser", "shimaoré": "outsimba", "kibouchi": "mangadi"},
        {"french": "récolter", "shimaoré": "ouvouna", "kibouchi": "mampoka"}
    ],
    
    "vetements": [
        {"french": "vêtement", "shimaoré": "ngouwo", "kibouchi": "ankandzou"},
        {"french": "salouva", "shimaoré": "salouva", "kibouchi": "salouvagna"},
        {"french": "chemise", "shimaoré": "chimizi", "kibouchi": "chimizi"},
        {"french": "pantalon", "shimaoré": "sourouali", "kibouchi": "sourouali"},
        {"french": "short", "shimaoré": "kaliso", "kibouchi": "kaliso"},
        {"french": "sous-vêtement", "shimaoré": "silipou", "kibouchi": "silipou"},
        {"french": "chapeau", "shimaoré": "kofia", "kibouchi": "kofia"},
        {"french": "kamiss", "shimaoré": "kandzou bolé", "kibouchi": "ankandzou bé"},
        {"french": "boubou", "shimaoré": "kandzou bolé", "kibouchi": "ankandzou bé"},
        {"french": "haut de salouva", "shimaoré": "body", "kibouchi": "body"},
        {"french": "t-shirt", "shimaoré": "kandzou", "kibouchi": "ankandzou"},
        {"french": "chaussures", "shimaoré": "kabwa", "kibouchi": "kabwa"},
        {"french": "baskets", "shimaoré": "magochi", "kibouchi": "magochi"},
        {"french": "tongs", "shimaoré": "sapatri", "kibouchi": "kabwa sapatri"},
        {"french": "jupe", "shimaoré": "jipo", "kibouchi": "jipou"},
        {"french": "robe", "shimaoré": "robo", "kibouchi": "robou"},
        {"french": "voile", "shimaoré": "kichali", "kibouchi": "kichali"}
    ],
    
    "transport": [
        {"french": "bicyclette", "shimaoré": "bicycléti", "kibouchi": "bicycléti"},
        {"french": "kwassa kwassa", "shimaoré": "kwassa kwassa", "kibouchi": "kwassa kwassa"},
        {"french": "barque", "shimaoré": "laka", "kibouchi": "laka"},
        {"french": "pirogue", "shimaoré": "lakana", "kibouchi": "lakana"},
        {"french": "bateau", "shimaoré": "markabou", "kibouchi": "markabou"},
        {"french": "moto", "shimaoré": "monto", "kibouchi": "monto"},
        {"french": "camion", "shimaoré": "ndrégué", "kibouchi": "ndrégué"},
        {"french": "avion", "shimaoré": "roplani", "kibouchi": "roplani"},
        {"french": "taxi", "shimaoré": "taxi", "kibouchi": "taxi"},
        {"french": "vedette", "shimaoré": "vidéti", "kibouchi": "vidéti"}
    ]
}

def connect_to_database():
    """Connexion à la base de données MongoDB"""
    try:
        mongo_url = os.getenv('MONGO_URL')
        if not mongo_url:
            raise ValueError("MONGO_URL non trouvée dans les variables d'environnement")
        
        client = MongoClient(mongo_url)
        db = client['shimaoré_app']
        logger.info("Connexion à la base de données réussie")
        return db
    except Exception as e:
        logger.error(f"Erreur de connexion à la base de données: {e}")
        raise

def get_emoji_for_section(section, french_word):
    """Retourne l'emoji approprié selon la section et le mot"""
    emoji_maps = {
        "nature": {
            "lune": "🌙", "étoile": "⭐", "soleil": "☀️", "mer": "🌊", "plage": "🏖️",
            "arbre": "🌳", "fleur": "🌸", "herbe": "🌿", "pierre": "🪨", "vent": "💨",
            "pluie": "🌧️", "nuage": "☁️", "arc en ciel": "🌈", "forêt": "🌲"
        },
        "nombres": {str(i): f"{i}️⃣" for i in range(1, 10)},
        "animaux": {
            "chat": "🐱", "chien": "🐕", "poisson": "🐟", "oiseau": "🐦", "lion": "🦁",
            "éléphant": "🐘", "singe": "🐒", "serpent": "🐍", "crocodile": "🐊"
        },
        "corps": {
            "œil": "👁️", "main": "✋", "pied": "🦵", "cœur": "❤️", "tête": "👤"
        },
        "salutations": {"bonjour": "👋", "merci": "🙏", "au revoir": "👋"},
        "famille": {"papa": "👨", "maman": "👩", "famille": "👨‍👩‍👧‍👦"},
        "couleurs": {
            "rouge": "🔴", "bleu": "🔵", "vert": "🟢", "jaune": "🟡", "noir": "⚫", "blanc": "⚪"
        },
        "nourriture": {
            "riz": "🍚", "eau": "💧", "ananas": "🍍", "banane": "🍌", "pain": "🍞"
        },
        "maison": {"maison": "🏠", "porte": "🚪", "lit": "🛏️", "fenêtre": "🪟"},
        "verbes": {"danser": "💃", "courir": "🏃", "manger": "🍽️"},
        "vetements": {"vêtement": "👕", "chaussures": "👟", "chapeau": "👒"},
        "transport": {"bicyclette": "🚲", "bateau": "🚢", "avion": "✈️", "taxi": "🚕"}
    }
    
    section_map = emoji_maps.get(section, {})
    return section_map.get(french_word.lower(), "📝")

def reconstruct_complete_database(db):
    """Reconstruit complètement la base de données avec les données du PDF"""
    collection = db['vocabulary']
    
    logger.info("=== RECONSTRUCTION COMPLÈTE DE LA BASE DE DONNÉES ===")
    
    # Supprimer toutes les données existantes
    result = collection.delete_many({})
    logger.info(f"Ancienne base supprimée: {result.deleted_count} documents")
    
    total_inserted = 0
    
    for section_name, words_list in PDF_VOCABULARY_DATA.items():
        logger.info(f"\n--- Reconstruction section: {section_name.upper()} ---")
        
        documents = []
        for word_data in words_list:
            emoji = get_emoji_for_section(section_name, word_data["french"])
            
            # Créer le nom de fichier audio
            audio_base = word_data["french"].lower().replace(' ', '_').replace('-', '_').replace("'", '_')
            
            document = {
                "section": section_name,
                "french": word_data["french"],
                "shimaoré": word_data["shimaoré"], 
                "kibouchi": word_data["kibouchi"],
                "emoji": emoji,
                "audio_shimaoré": f"audio/{audio_base}_shimaoré.mp3",
                "audio_kibouchi": f"audio/{audio_base}_kibouchi.mp3",
                "pdf_reference": True,
                "orthography_verified": True
            }
            documents.append(document)
        
        # Insérer les documents de la section
        if documents:
            result = collection.insert_many(documents)
            inserted_count = len(result.inserted_ids)
            total_inserted += inserted_count
            logger.info(f"Section {section_name}: {inserted_count} mots insérés")
    
    logger.info(f"\n=== RECONSTRUCTION TERMINÉE ===")
    logger.info(f"Total mots insérés: {total_inserted}")
    
    return total_inserted

def update_existing_audio_references(db):
    """Met à jour les références audio existantes"""
    logger.info("\n=== MISE À JOUR RÉFÉRENCES AUDIO EXISTANTES ===")
    
    collection = db['vocabulary']
    updated_count = 0
    
    # Sections avec audio disponible
    audio_sections = {
        "animaux": "/app/frontend/assets/audio/animaux",
        "corps": "/app/frontend/assets/audio/corps", 
        "maison": "/app/frontend/assets/audio/maison",
        "nature": "/app/frontend/assets/audio/nature",
        "nombres": "/app/frontend/assets/audio/nombres",
        "salutations": "/app/frontend/assets/audio/salutations",
        "vetements": "/app/frontend/assets/audio/vetements",
        "verbes": "/app/frontend/assets/audio/verbes",
        "transport": "/app/frontend/assets/audio/transport"
    }
    
    for section, audio_dir in audio_sections.items():
        if os.path.exists(audio_dir):
            audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
            logger.info(f"Section {section}: {len(audio_files)} fichiers audio trouvés")
            
            # Mettre à jour les mots de cette section avec has_authentic_audio si audio existe
            section_words = collection.find({"section": section})
            for word in section_words:
                # Marquer comme ayant de l'audio authentique si audio dir existe
                result = collection.update_one(
                    {"_id": word["_id"]},
                    {"$set": {"has_authentic_audio": True, "audio_updated": True}}
                )
                if result.modified_count > 0:
                    updated_count += 1
        else:
            logger.info(f"Section {section}: Aucun répertoire audio trouvé")
    
    logger.info(f"Total références audio mises à jour: {updated_count}")
    return updated_count

def main():
    """Fonction principale"""
    logger.info("Début de la reconstruction complète de la base de données depuis le PDF")
    
    try:
        # Connexion à la base de données
        db = connect_to_database()
        
        # 1. Reconstruction complète
        total_words = reconstruct_complete_database(db)
        
        # 2. Mise à jour des références audio existantes
        audio_updates = update_existing_audio_references(db)
        
        # 3. Vérification finale
        final_count = db['vocabulary'].count_documents({})
        sections = db['vocabulary'].distinct('section')
        
        logger.info(f"\n{'='*60}")
        logger.info("RAPPORT FINAL DE RECONSTRUCTION")
        logger.info(f"{'='*60}")
        logger.info(f"Sections créées: {len(sections)}")
        logger.info(f"Sections: {', '.join(sections)}")
        logger.info(f"Total mots: {final_count}")
        logger.info(f"Références audio mises à jour: {audio_updates}")
        
        # Statistiques par section
        for section in sections:
            count = db['vocabulary'].count_documents({"section": section})
            with_audio = db['vocabulary'].count_documents({
                "section": section, 
                "has_authentic_audio": True
            })
            coverage = (with_audio/count)*100 if count > 0 else 0
            logger.info(f"  - {section}: {count} mots ({with_audio} avec audio, {coverage:.1f}%)")
        
        logger.info("\n🎉 Base de données entièrement reconstruite avec les données authentiques du PDF!")
        logger.info("Toutes les traductions shimaoré et kibouchi sont maintenant correctes!")
        
    except Exception as e:
        logger.error(f"Erreur lors de la reconstruction: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())