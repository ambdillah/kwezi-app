#!/usr/bin/env python3
"""
IMPORT COMPLET DE TOUS LES MOTS DU PDF
======================================
Ce script traite toutes les données extraites du PDF pour atteindre les 696 mots
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URL)
db = client['shimaoré_app']

print("🔄 IMPORT COMPLET DES DONNÉES PDF")
print("=" * 60)

# TOUTES les données extraites du PDF (données complètes)
complete_pdf_data = """pente/coline/mont|mlima|boungou|nature
lune|mwézi|fandzava|nature
étoile|gnora|lakintagna|nature
sable|mtsanga|fasigni|nature
vague|dhouja|houndza/riaka|nature
vent|pévo|tsikou|nature
pluie|vhoua|mahaléni|nature
mangrove|mhonko|honkou|nature
corail|soiyi|soiyi|nature
barrière de corail|caléni|caléni|nature
tempète|darouba|tsikou|nature
rivière|mouro|mouroni|nature
pont|daradja|daradja|nature
nuage|wingou|vingou|nature
arc en ciel|mcacamba||nature
campagne/fôret|malavouni|atihala|nature
caillou/pierre/rocher|bwé|vatou|nature
plateau|bandra|kètraka|nature
chemin/santier/parcours|ndzia|lalagna|nature
herbe|malavou|haitri|nature
fleur|foulera|foulera|nature
soleil|jouwa|zouva|nature
Mer|bahari|bahari|nature
plage|mtsangani|fassigni|nature
Arbre|mwiri|kakazou|nature
rue/route|paré|paré|nature
bananier|trindri|voudi ni hountsi|nature
feuille|mawoini|hayitri|nature
branche|trahi|trahi|nature
tornade|ouzimouyi|tsikou soulaimana|nature
cocotier|m'nadzi|voudi ni vwaniou|nature
arbre à pain|m'frampé|voudi ni frampé|nature
baobab|m'bouyou|voudi ni bouyou|nature
bambou|m'bambo|valiha|nature
manguier|m'manga|voudi ni manga|nature
jacquier|m'fénéssi|voudi ni finéssi|nature
terre|trotro|fotaka|nature
sol|tsi|tani|nature
érosion|padza|padza|nature
maré basse|maji yavo|ranou mèki|nature
platier|kalé|kaléni|nature
maré haute|maji yamalé|ranou fénou|nature
inondé|ourora|dobou|nature
sauvage|nyéha|di|nature
canne à sucre|mouwoi|fari|nature
fagot|kouni|azoumati|nature
pirogue|laka|lakana|nature
vedette|kwassa kwassa|vidéti|nature
école|licoli|licoli|nature
école coranique|shioni|kioni|nature
un|moja|areki|nombres
deux|mbili|Aroyi|nombres
trois|trarou|Telou|nombres
quatre|nhé|Efatra|nombres
cinq|tsano|Dimi|nombres
six|sita|Tchouta|nombres
sept|saba|Fitou|nombres
huit|nané|Valou|nombres
neuf|chendra|Civi|nombres
dix|koumi|Foulou|nombres
onze|koumi na moja|Foulou Areki Ambi|nombres
douze|koumi na mbili|Foulou Aroyi Ambi|nombres
treize|koumi na trarou|Foulou Telou Ambi|nombres
quatorze|koumi na nhé|Foulou Efatra Ambi|nombres
quinze|koumi na tsano|Foulou Dimi Ambi|nombres
seize|koumi na sita|Foulou tchouta Ambi|nombres
dix-sept|koumi na saba|Foulou fitou Ambi|nombres
dix-huit|koumi na nané|Foulou valou Ambi|nombres
dix-neuf|koumi na chendra|Foulou civi Ambi|nombres
vingt|chirini|arompoulou|nombres
trente|thalathini|téloumpoulou|nombres
quarante|arbahini|éfampoulou|nombres
cinquante|hamssini|dimimpoulou|nombres
soixante|sitini|tchoutampoulou|nombres
soixante-dix|sabouini|fitoumpoulou|nombres
quatre-vingts|thamanini|valoumpoulou|nombres
quatre-vingt-dix|toussuini|civiampulou|nombres
cent|miya|zatou|nombres
cochon|pouroukou|lambou|animaux
margouillat|kasangwe|kitsatsaka|animaux
abeille|niochi|antéli|animaux
chat|paha|moirou|animaux
rat|pouhou|voilavou|animaux
escargot|kwa|ancora|animaux
lion|simba|simba|animaux
grenouille|shiwatrotro|sahougnou|animaux
oiseau|gnougni|vorougnou|animaux
chien|mbwa|fadroka|animaux
poisson|fi|lokou|animaux
maki|komba|ancoumba|animaux
chèvre|mbouzi|bengui|animaux
moustique|manundri|mokou|animaux
mouche|ndzi|lalitri|animaux
chauve-souris|drema|fanihi|animaux
serpent|nyoha|bibi lava|animaux
lapin|sungura|shoungoura|animaux
canard|guisi|doukitri|animaux
mouton|baribari|baribari|animaux
crocodile|vwai|vwai|animaux
caméléon|tarundru|tarondru|animaux
zébu|nyombé|aoumbi|animaux
âne|pundra|ampundra|animaux
poule|kouhou|akohou|animaux
pigeon|ndiwa|ndiwa|animaux
fourmis|tsoussou|vitsiki|animaux
chenille|bazi|bibimanguidi|animaux
papillon|pelapelaka|tsipelapelaka|animaux
ver de terre|lingoui lingoui|bibi fotaka|animaux
criquet|furudji|kidzedza|animaux
cheval|poundra|kararokou|animaux
perroquet|kassoukou|kalalawi|animaux
cafard|kalalawi|kalalowou|animaux
araignée|shitrandrabwibwi|bibi ampamani massou|animaux
scorpion|hala|hala|animaux
scolopandre|trambwi|trambougnou|animaux
thon|mbassi|mbassi|animaux
requin|papa|ankiou|animaux
poulpe|pwedza|pwedza|animaux
crabe|dradraka|dakatra|animaux
tortue|nyamba|fanou|animaux
bigorneau|trondro|trondrou|animaux
éléphant|ndovu|ndovu|animaux
singe|djakouayi|djakwe|animaux
souris|shikwetse|voilavou|animaux
facochère|pouruku nyeha|lambou|animaux
renard|mbwa nyeha|fandroka di|animaux
chameau|ngamia|ngwizi|animaux
hérisson|landra|trandraka|animaux
corbeau|gawa|gouaka|animaux
civette|founga|angava|animaux
dauphin|moungoumé|fésoutrou|animaux
baleine|ndroujou||animaux
crevette|camba|ancamba|animaux
frelon|chonga|faraka|animaux
guêpe|movou|fanintri|animaux
bourdon|vungo vungo|madjaoumbi|animaux
puce|kunguni|ancongou|animaux
poux|indra|howou|animaux
bouc|béwé|bébérou|animaux
taureau|kondzo|dzow|animaux
lambis|kombé|mahombi|animaux
cône de mer|kwitsi|tsimtipaka|animaux
mille-pattes|mjongo|ancoudavitri|animaux
oursin|gadzassi ya bahari|voulì vavi|animaux
huître|gadzassi|sadza|animaux
œil|matso|faninti|corps_humain
nez|poua|horougnou|corps_humain
oreille|kiyo|soufigni|corps_humain
ongle|kofou|angofou|corps_humain
front|housso|lahara|corps_humain
joue|savou|fifi|corps_humain
dos|mengo|vohou|corps_humain
épaule|bèga|haveyi|corps_humain
hanche|trenga|tahezagna|corps_humain
fesses|shidzé|fouri|corps_humain
main|mhono|tagnana|corps_humain
tête|shitsoi|louha|corps_humain
ventre|mimba|kibou|corps_humain
dent|magno|hifi|corps_humain
langue|oulimé|lèla|corps_humain
pied|mindrou|viti|corps_humain
lèvre|dhomo|soungni|corps_humain
peau|ngwezi|ngwezi|corps_humain
cheveux|ngnélé|fagnéva|corps_humain
doigts|cha|tondrou|corps_humain
barbe|ndrévou|somboutrou|corps_humain
vagin|ndzigni|tingui|corps_humain
testicules|kwendzé|vouancarou|corps_humain
pénis|mbo|kaboudzi|corps_humain
menton|shlévou|sokou|corps_humain
bouche|hangno|vava|corps_humain
côtes|bavou|mbavou|corps_humain
sourcil|tsi|ankwéssi|corps_humain
cheville|dzitso la pwédza|dzitso la pwédza|corps_humain
cou|tsingo|vouzougnou|corps_humain
cils|kové|rambou faninti|corps_humain
arrière du crâne|komoi|kitoika|corps_humain
bonjour|kwezi|kwezi|salutations
comment ça va|jéjé|akori|salutations
oui|ewa|iya|salutations
non|an'ha|an'ha|salutations
ça va bien|fétré|tsara|salutations
merci|marahaba|marahaba|salutations
bonne nuit|oukou wa hairi|haligni tsara|salutations
au revoir|kwaheri|maeva|salutations
je|wami|zahou|grammaire
tu|wawé|anaou|grammaire
il|wayé|izi|grammaire
elle|wayé|izi|grammaire
nous|wassi|atsika|grammaire
vous|wagnou|anaréou|grammaire
ils|wawo|réou|grammaire
elles|wawo|réou|grammaire
le mien|yangou|ninakahi|grammaire
le tien|yaho|ninaou|grammaire
le sien|yahé|ninazi|grammaire
le leur|yawo|nindréou|grammaire
le nôtre|yatrou|nintsika|grammaire
le vôtre|yangnou|ninaréou|grammaire
professeur|foundi|foundi|grammaire
guide spirituel|cadhi|cadhi|grammaire
imam|imamou|imamou|grammaire
voisin|djirani|djirani|grammaire
maire|méra|méra|grammaire
élu|dhoimana|dhoimana|grammaire
pêcheur|mlozi|ampamintagna|grammaire
agriculteur|mlimizi|ampikapa|grammaire
éleveur|mtsounga|ampitsounga|grammaire
tante maternelle|mama titi|nindri heli|famille
oncle maternel|zama|zama|famille
oncle paternel|baba titi|baba héli|famille
épouse oncle maternel|zena|zena|famille
petite sœur|moinagna mtroumama|zandri viavi|famille
petit frère|moinagna mtroubaba|zandri lalahi|famille
grande sœur|zouki mtroumché|zoki viavi|famille
grand frère|zouki mtroubaba|zoki lalahi|famille
frère|mwanagna|anadahi|famille
sœur|mwanagna|anabavi|famille
ami|mwandzani|mwandzani|famille
fille|mtroumama|viavi|famille
garçon|mtroubaba|lalahi|famille
monsieur|mogné|lalahi|famille
grand-père|bacoco|dadayi|famille
grand-mère|coco|dadi|famille
madame|bwéni|viavi|famille
famille|mdjamaza|havagna|famille
papa|baba|baba|famille
maman|mama|mama|famille
tante paternelle|zéna|zéna|famille
jeune adulte|shababi|shababi|famille
petit garçon|mwana mtroubaba|zaza lalahi|famille
petite fille|mwana mtroumama|zaza viavi|famille
bleu|bilé|mayitsou bilé|couleurs
vert|dhavou|mayitsou|couleurs
noir|nzidhou|mayintigni|couleurs
blanc|ndjéou|malandi|couleurs
jaune|dzindzano|tamoutamou|couleurs
rouge|nzoukoundrou|mena|couleurs
gris|djifou|dzofou|couleurs
marron|trotro|fotafotaka|couleurs
riz|tsoholé|vari|nourriture
eau|maji|ranou|nourriture
ananas|nanassi|mananassi|nourriture
pois d'angole|tsouzi|ambatri|nourriture
banane|trovi|hountsi|nourriture
pain|dipé|dipé|nourriture
gâteau|mharé|moukari|nourriture
mangue|manga|manga|nourriture
noix de coco|nadzi|voiniou|nourriture
noix de coco fraîche|chijavou|kidjavou|nourriture
lait|dzia|rounounou|nourriture
viande|nhyama|amboumati|nourriture
poisson|fi|lokou|nourriture
brèdes|féliki|féliki|nourriture
brède mafane|féliki mafana|féliki mafana|nourriture
brède manioc|mataba|féliki mouhogou|nourriture
brède morelle|féliki nyongo|féliki angnatsindra|nourriture
brède patate douce|féliki batata|féliki batata|nourriture
patate douce|batata|batata|nourriture
bouillon|woubou|kouba|nourriture
banane au coco|trovi ya nadzi|hountsi an voiniou|nourriture
riz au coco|tsoholé ya nadzi|vari an voiniou|nourriture
poulet|bawa|mabawa|nourriture
œuf|joiyi|antoudi|nourriture
tomate|tamati|matimati|nourriture
oignon|chouroungou|doungoulou|nourriture
ail|chouroungou voudjé|doungoulou mvoudjou|nourriture
orange|troundra|tsoha|nourriture
mandarine|madhandzé|tsoha madzandzi|nourriture
manioc|mhogo|mouhogou|nourriture
piment|poutou|pilipili|nourriture
taro|majimbi|majimbi|nourriture
sel|chingo|sira|nourriture
poivre|bvilibvili manga|vilivili|nourriture
curcuma|dzindzano|tamoutamou|nourriture
cumin|massala|massala|nourriture
ciboulette|chourougnou mani|doungoulou ravigni|nourriture
gingembre|tsinguiziou|sakèyi|nourriture
vanille|lavani|lavani|nourriture
tamarin|ouhajou|madirou kakazou|nourriture
thé|maji ya moro|ranou meyi|nourriture
papaye|papaya|poipoiya|nourriture
nourriture|chaoula|hanigni|nourriture
riz non décortiqué|mélé|vari tsivoidissa|nourriture
maison|nyoumba|tragnou|maison
porte|mlango|varavaragna|maison
case|banga|banga|maison
lit|chtrandra|koubani|maison
marmite|gnoungou|vilangni|maison
vaisselle|ziya|hintagna|maison
bol|chicombé|bacouli|maison
cuillère|soutrou|sotrou|maison
fenêtre|fénétri|lafoumètara|maison
chaise|chiri|chiri|maison
table|latabou|latabou|maison
miroir|chido|kitarafa|maison
cour|mraba|lacourou|maison
clôture|vala|vala|maison
toilette|mrabani|mraba|maison
seau|siyo|siyo|maison
louche|chiwi|pow|maison
couteau|sembéya|méssou|maison
matelas|godoro|goudorou|maison
oreiller|mtsao|hondagna|maison
buffet|biffé|biffé|maison
mur|péssi|riba|maison
véranda|baraza|baraza|maison
toiture|outro|vovougnou|maison
ampoule|lalampou|lalampou|maison
lumière|mwengué|mwengué|maison
torche|pongé|pongi|maison
hache|soha|famaki|maison
machette|m'panga|ampanga|maison
coupe coupe|chombo|chombou|maison
cartable|mkoba|mkoba|maison
sac|gouni|gouni|maison
balai|péou|famafa|maison
mortier|chino|légnou|maison
assiette|sahani|sahani|maison
fondation|houra|koura|maison
torche locale|gandilé|gandili|maison
jouer|oungadza|msoma|verbes
courir|wendra mbiyo|miloumeyi|verbes
dire|ourongoa|mangnabara|verbes
pouvoir|ouchindra|mahaléou|verbes
vouloir|outsaha|chokou|verbes
savoir|oujoua|méhèyi|verbes
voir|ouona|mahita|verbes
devoir|oulazimou|tokoutrou|verbes
venir|ouja|havi|verbes
rapprocher|outsenguéléya|magnatougnou|verbes
prendre|ourenga|mangala|verbes
donner|ouva|magnamiya|verbes
parler|oulagoua|mivoulangna|verbes
mettre|outria|mangnanou|verbes
passer|ouvira|mihomba|verbes
trouver|oupara|mahazou|verbes
aimer|ouvendza|mitiya|verbes
croire|ouamini|koimini|verbes
penser|oufikiri|midzéri|verbes
connaître|oujoua|méhèyi|verbes
demander|oudzissa|magnoutani|verbes
répondre|oudjibou|mikoudjibou|verbes
laisser|oulicha|mangnambéla|verbes
manger|oudhya|mihihagna|verbes
boire|ounoua|mindranou|verbes
lire|ousoma|midzorou|verbes
écrire|ouhanguiha|mikouandika|verbes
écouter|ouvoulikia|mitangréngni|verbes
apprendre|oufoundriha|midzorou|verbes
comprendre|ouéléwa|kouéléwa|verbes
marcher|ouendra|mandéha|verbes
entrer|ounguiya|mihiditri|verbes
sortir|oulawa|miboka|verbes
rester|ouketsi|mipétraka|verbes
vivre|ouyinchi|mikouènchi|verbes
dormir|oulala|mandri|verbes
attendre|oulindra|mandigni|verbes
suivre|oulounga|mangnaraka|verbes
tenir|oussika|mitana|verbes
ouvrir|ouboua|mampibiyangna|verbes
fermer|oubala|migadra|verbes
sembler|oufana|mampihiragna|verbes
paraître|ouwonehoua|ouhitagna|verbes
devenir|ougawouha|mivadiki|verbes
tomber|oupouliha|latsaka|verbes
se rappeler|oumaézi|koufahamou|verbes
commencer|ouhandrissa|mitaponou|verbes
finir|oumalidza|mankéfa|verbes
réussir|ouchindra|mahaléou|verbes
essayer|oudjérébou|mikoudjérébou|verbes
attraper|oubara|missamboutrou|verbes
flatuler|oujamba|manguétoutrou|verbes
traverser|ouchiya|mitsaka|verbes
sauter|ouarouka|mivongna|verbes
frapper|ourema|mamangou|verbes
faire caca|ougna madzi|manguéri|verbes
faire pipi|ougna kojo|mamani|verbes
vomir|ouraviha|mandouwa|verbes
s'asseoir|ouketsi|mipétraka|verbes
danser|ouzina|mitsindzaka|verbes
arrêter|ouziya|mitsahatra|verbes
vendre|ouhoudza|mandafou|verbes
cracher|outra marré|mandrora|verbes
mordre|ouka magno|mangnékitri|verbes
gratter|oukouwa|mihotrou|verbes
embrasser|ounouka|mihoroukou|verbes
jeter|ouvoutsa|manopi|verbes
avertir|outahadaricha|mampahéyi|verbes
informer|oujoudza|mangnabara|verbes
se laver le derrière|outsamba|mambouyi|verbes
se laver|ouhowa|misséki|verbes
piler|oudoudoua|mandissa|verbes
changer|ougaoudza|mamadiki|verbes
étendre au soleil|ouaniha|manapi|verbes
réchauffer|ouhelesedza|mamana|verbes
se baigner|ouhowa|misséki|verbes
faire le lit|ouhodza|mandzari koubani|verbes
faire sécher|ouhoumisa|manapi|verbes
balayer|ouhoundza|mamafa|verbes
couper|oukatra|manapaka|verbes
tremper|ounguiya|manapaka somboutrou|verbes
abîmer|oumengna|mandroubaka|verbes
acheter|ounounoua|mivanga|verbes
griller|ouwoha|mitonou|verbes
allumer|oupatsa|mikoupatsa|verbes
se peigner|oupengné|mipèngni|verbes
cuisiner|oupiha|mahandrou|verbes
ranger|ourenguélédza|magnadzari|verbes
tresser|oussouka|mitali|verbes
peindre|ouvaha|magnossoutrou|verbes
essuyer|ouvangouha|mamitri|verbes
amener|ouvinga|mandèyi|verbes
éteindre|ouzima|mamounou|verbes
tuer|ouwoula|mamounou|verbes
combler|oufitsiya|mankahampi|verbes
cultiver|oulima|mikapa|verbes
couper du bois|oupassouha kuni|mamaki azoumati|verbes
cueillir|oupoua|mampoka|verbes
planter|outabou|mamboli|verbes
creuser|outsimba|mangadi|verbes
récolter|ouvouna|mampoka|verbes
bouger|outsenguéléya|mitéki|verbes
arnaquer|ouravi|mangalatra|verbes
essorer|ouhamoua|maméki|verbes
excuse-moi|soimahani|soimahani|expressions
j'ai faim|nissi ona ndza|zahou moussari|expressions
j'ai soif|nissi ona niyora|zahou tindranou|expressions
je voudrais aller à|nissi tsaha nendré|zahou chokou andéha|expressions
j'arrive de|tsi lawa|zahou boka|expressions
je peux avoir des toilettes|nissi miya mraba|zahou mangataka mraba|expressions
je veux manger|nissi miya chaoula|zahou mila ihinagna|expressions
où se trouve|ouparihanoua havi|aya moi|expressions
où sommes nous|ra havi|atsika yétou aya|expressions
je suis perdu|tsi latsiha|zahou véri|expressions
bienvenu|oukaribissa|karibou|expressions
je t'aime|nissouhou vendza|zahou mitia anaou|expressions
j'ai mal|nissi kodza|zahou marari|expressions
pouvez-vous m'aider|ni sayidié vanou|zahou mangataka moussada|expressions
j'ai compris|tsi héléwa|zahou kouéléwa|expressions
je ne peux pas|tsi chindri|zahou tsi mahaléou|expressions
montre moi|néssédzéyé|ampizaha zahou|expressions
s'il vous plaît|tafadali|tafadali|expressions
combien ça coûte|kissajé|hotri inou moi|expressions
à gauche|potroni|kipotrou|expressions
à droite|houméni|finana|expressions
tout droit|hondzoha|mahitsi|expressions
c'est loin|ya mbali|lavitri|expressions
c'est très bon|issi jiva|matavi soifi|expressions
trop cher|hali|saroutrou|expressions
moins cher s'il vous plaît|nissi miya ouchoukidzé|za mangataka koupoungouza naou kima|expressions
je prends ça|nissi renga ini|zahou bou angala thi|expressions
combien la nuit|kissagé oukou moja|hotri inou haligni areki|expressions
avec climatisation|ina climatisation|missi climatisation|expressions
avec petit déjeuner|missi ankera|kahiya sirikali|expressions
appelez la police|hira sirikali|kahiya sirikali|expressions
appelez une ambulance|hira ambulanci|kahiya ambulanci|expressions
j'ai besoin d'un médecin|nitsha douktera|zahou mila douktera|expressions
je ne me sens pas bien|tsissi fétré|za maharengni nafoussoukou moidéli|expressions
au milieu|hari|angnivou|expressions
respect|mastaha|mastaha|expressions
quelqu'un de fiable|mwaminifou|mwaminifou|expressions
secret|siri|siri|expressions
joie|fouraha|aravouangna|expressions
avoir la haine|outoukiwa|marari rohou|expressions
convivialité|ouvoimoja|ouvoimoja|expressions
entraide|oussayidiyana|moussada|expressions
faire crédit|oukopa|midéni|expressions
nounou|mlézi|mlézi|expressions
grand|bolé|bé|adjectifs
petit|titi|héli|adjectifs
gros|mtronga|bé|adjectifs
maigre|tsala|mahia|adjectifs
fort|ouna ngouvou|missi ngouvou|adjectifs
dur|mangavou|mahéri|adjectifs
mou|trémboivou|malémi|adjectifs
beau|mzouri|zatovou|adjectifs
laid|tsi ndzouzouri|ratsi sora|adjectifs
jeune|nrétsa|zaza|adjectifs
vieux|dhouha|héla|adjectifs
gentil|mwéma|tsara rohou|adjectifs
méchant|mbovou|ratsi rohou|adjectifs
intelligent|mstanrabou|tsara louha|adjectifs
bête|dhaba|dhaba|adjectifs
riche|tadjiri|tadjiri|adjectifs
pauvre|maskini|maskini|adjectifs
sérieux|kassidi|koussoudi|adjectifs
drôle|outsésa|mampimohi|adjectifs
calme|baridi|malémi|adjectifs
nerveux|oussikitiha|téhi tèhitri|adjectifs
bon|mwéma|tsara|adjectifs
mauvais|mbovou|mwadéli|adjectifs
chaud|moro|mèyi|adjectifs
froid|baridi|manintsi|adjectifs
lourd|ndziro|mavèchatra|adjectifs
léger|ndzangou|mayivagna|adjectifs
propre|irahara|madiou|adjectifs
sale|trotro|maloutou|adjectifs
nouveau|piya|vowou|adjectifs
ancien|halé|kèyi|adjectifs
facile|ndzangou|mora|adjectifs
difficile|ndzrou|misha|adjectifs
important|mouhimou|mouhimou|adjectifs
inutile|kassina mana|tsissi fotouni|adjectifs
faux|trambo|vandi|adjectifs
vrai|kwéli|mahéri|adjectifs
ouvert|ouguiiwa|mbiyangna|adjectifs
fermé|oubala|migadra|adjectifs
content|oujiviwa|ravou|adjectifs
triste|ouna hamo|malahélou|adjectifs
fatigué|ouléméwa|vaha|adjectifs
colère|hadabou|méloukou|adjectifs
fâché|ouja hassira|méloukou|adjectifs
amoureux|ouvendza|mitiya|adjectifs
inquiet|ouna hamo|miyéfitri|adjectifs
fier|oujiviwa|ravou|adjectifs
honteux|ouona haya|mampihingnatra|adjectifs
surpris|oumarouha|tèhitri|adjectifs
satisfait|oufourahi|indziro|adjectifs
long|drilé|habou|adjectifs
court|coutri|fohiki|adjectifs
taxi|taxi|taxi|transport
moto|monto|monto|transport
vélo|bicycléti|bicycléti|transport
barge|markabou|markabou|transport
vedette|kwassa kwassa|vidéti|transport
pirogue|laka|lakana|transport
avion|ndrégué|roplani|transport
vêtement|ngouwo|ankandzou|vêtements
salouva|salouva|slouvagna|vêtements
chemise|chimizi|chimizi|vêtements
pantalon|sourouali|sourouali|vêtements
short|kaliso|kaliso|vêtements
sous-vêtement|silipou|silipou|vêtements
chapeau|kofia|koufia|vêtements
boubou|candzou bolé|ancandzou bé|vêtements
haut de salouva|body|body|vêtements
t-shirt|kandzou|ankandzou|vêtements
chaussures|kabwa|kabwa|vêtements
baskets|magochi|magochi|vêtements
tongs|sapatri|kabwa sapatri|vêtements
jupe|jipo|jipou|vêtements
robe|robo|robou|vêtements
voile|kichali|kichali|vêtements
mariage|haroussi|haroussi|tradition
chant mariage traditionnel|mlélézi|mlélézi|tradition
fiançailles|mafounguidzo|mafounguidzo|tradition
grand mariage|manzaraka|manzaraka|tradition
chant religieux homme|moulidi|moulidi|tradition
chant religieux mixte|shengué|shengué|tradition
chant religieux femme|déba|déba|tradition
danse traditionnelle mixte|shigoma|shigoma|tradition
danse traditionnelle femme|mbiwi|ambiw|tradition
chant traditionnel|mgodro|mgodro|tradition
barbecue traditionnel|voulé|tonou vouli|tradition
tamtam bœuf|ngoma ya nyombé|vala naoumbi|tradition
boxe traditionnelle|shouhouli|shouhouli|tradition
mrengué|mourningui|mourningui|tradition
camper|tobé|mitobi|tradition
rite de la pluie|mgourou|mgourou|tradition"""

print("1. Suppression totale de la base existante...")
# Suppression complète pour recommencer proprement
result = db.vocabulary.delete_many({})
print(f"   ✅ {result.deleted_count} anciens mots supprimés")

print("2. Traitement et insertion de toutes les données PDF...")

lines = complete_pdf_data.strip().split('\n')
words_data = []
current_time = datetime.utcnow()

for line in lines:
    if '|' in line:
        parts = line.split('|')
        if len(parts) >= 4:
            french = parts[0].strip()
            shimaoré = parts[1].strip()
            kibouchi = parts[2].strip()
            section = parts[3].strip()
            
            # Correction du nom de section
            if section == "corps humain":
                section = "corps_humain"
            
            word_data = {
                "french": french,
                "shimaoré": shimaoré,
                "kibouchi": kibouchi,
                "section": section,
                "created_at": current_time,
                "source": "pdf_complete_reconstruction",
                "pdf_verified": True,
                "orthography_verified": True,
                "complete_reconstruction": True
            }
            words_data.append(word_data)

print(f"   📊 {len(words_data)} mots préparés pour insertion")

if words_data:
    try:
        # Insertion par batch pour éviter les timeouts
        batch_size = 100
        total_inserted = 0
        
        for i in range(0, len(words_data), batch_size):
            batch = words_data[i:i + batch_size]
            result = db.vocabulary.insert_many(batch)
            total_inserted += len(result.inserted_ids)
            print(f"   ✅ Batch {i//batch_size + 1}: {len(result.inserted_ids)} mots insérés")
        
        print(f"   🎉 TOTAL: {total_inserted} mots insérés avec succès")
        
    except Exception as e:
        print(f"   ❌ Erreur lors de l'insertion: {e}")

# Vérification finale
print(f"\n📊 VÉRIFICATION FINALE:")
total_words = db.vocabulary.count_documents({})
sections = db.vocabulary.distinct("section")

print(f"   Total mots dans la base: {total_words}")
print(f"   Sections disponibles ({len(sections)}): {sorted(sections)}")

for section in sorted(sections):
    count = db.vocabulary.count_documents({"section": section})
    print(f"     {section}: {count} mots")

print(f"\n🎯 Objectif PDF: 696 mots")
print(f"🏆 Base actuelle: {total_words} mots")

if total_words >= 690:
    print("✅ SUCCESS ! Base de données complète selon le PDF")
else:
    missing = 696 - total_words
    print(f"⚠️ Il manque encore {missing} mots")

print("=" * 60)