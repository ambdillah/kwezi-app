#!/usr/bin/env python3
"""
Script pour mettre à jour les sections "expressions" et "adjectifs" avec les données exactes des images fournies
Suppression systématique des doublons et tri par ordre alphabétique
"""

import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/mayotte_app")
client = MongoClient(MONGO_URL)
db = client.mayotte_app
words_collection = db.words

def update_expressions_adjectifs():
    """Mettre à jour les sections expressions et adjectifs avec les données exactes des images"""
    
    # Supprimer tous les mots existants des catégories "expressions" et "adjectifs"
    result_delete_expressions = words_collection.delete_many({"category": "expressions"})
    result_delete_adjectifs = words_collection.delete_many({"category": "adjectifs"})
    print(f"🗑️ Supprimé {result_delete_expressions.deleted_count} anciennes expressions")
    print(f"🗑️ Supprimé {result_delete_adjectifs.deleted_count} anciens adjectifs")
    
    # SECTION EXPRESSIONS - 44 expressions exactes selon l'image (triées par ordre alphabétique)
    expressions_vocabulary = [
        {"french": "à droite", "shimaore": "houméni", "kibouchi": "finana", "category": "expressions", "image_url": "➡️", "difficulty": 1},
        {"french": "à gauche", "shimaore": "potroni", "kibouchi": "kipotrou", "category": "expressions", "image_url": "⬅️", "difficulty": 1},
        {"french": "appelez la police !", "shimaore": "hira sirikali", "kibouchi": "kahiya sirikali", "category": "expressions", "image_url": "🚔", "difficulty": 2},
        {"french": "appelez une ambulance !", "shimaore": "hira ambulanci", "kibouchi": "kahiya ambulanci", "category": "expressions", "image_url": "🚑", "difficulty": 2},
        {"french": "au milieu", "shimaore": "hari", "kibouchi": "angaivou", "category": "expressions", "image_url": "🎯", "difficulty": 1},
        {"french": "avec climatisation ?", "shimaore": "ina climatisation", "kibouchi": "missi climatisation", "category": "expressions", "image_url": "❄️", "difficulty": 2},
        {"french": "avec petit déjeuner ?", "shimaore": "ina kèya", "kibouchi": "missi ankera", "category": "expressions", "image_url": "🥞", "difficulty": 2},
        {"french": "avoir la haine", "shimaore": "outoukiwa", "kibouchi": "marari rohou", "category": "expressions", "image_url": "😠", "difficulty": 2},
        {"french": "bienvenu", "shimaore": "oukaribissa", "kibouchi": "karibou", "category": "expressions", "image_url": "🤗", "difficulty": 1},
        {"french": "c'est loin ?", "shimaore": "ya mbali", "kibouchi": "lavitri", "category": "expressions", "image_url": "📏", "difficulty": 1},
        {"french": "c'est très bon !", "shimaore": "issi jiva", "kibouchi": "matavi soifi", "category": "expressions", "image_url": "😋", "difficulty": 1},
        {"french": "combien ça coûte ?", "shimaore": "kissajé", "kibouchi": "hotri inou moi", "category": "expressions", "image_url": "💰", "difficulty": 1},
        {"french": "combien la nuit ?", "shimaore": "kissagé oukou moja", "kibouchi": "hotri inou hahigni areki", "category": "expressions", "image_url": "🌙", "difficulty": 2},
        {"french": "convivialité", "shimaore": "ouvoimoja", "kibouchi": "ouvoimoja", "category": "expressions", "image_url": "🤝", "difficulty": 2},
        {"french": "entre aide", "shimaore": "oussayidiyana", "kibouchi": "moussada", "category": "expressions", "image_url": "🤝", "difficulty": 2},
        {"french": "excuse-moi/pardon", "shimaore": "soimahani", "kibouchi": "soimahani", "category": "expressions", "image_url": "🙏", "difficulty": 1},
        {"french": "faire crédit", "shimaore": "oukopa", "kibouchi": "midéni", "category": "expressions", "image_url": "💰", "difficulty": 2},
        {"french": "j'ai besoin d'un médecin", "shimaore": "ntsha douktera", "kibouchi": "zahou mila douktera", "category": "expressions", "image_url": "👩‍⚕️", "difficulty": 2},
        {"french": "j'ai compris", "shimaore": "tsi héléwa", "kibouchi": "zahou kouéléwa", "category": "expressions", "image_url": "💡", "difficulty": 1},
        {"french": "j'ai faim", "shimaore": "nissi ona ndza", "kibouchi": "zahou moussari", "category": "expressions", "image_url": "🍽️", "difficulty": 1},
        {"french": "j'ai mal", "shimaore": "nissi kodza", "kibouchi": "zahou marari", "category": "expressions", "image_url": "😵", "difficulty": 1},
        {"french": "j'ai soif", "shimaore": "nissi ona niyora", "kibouchi": "zahou tindi anou", "category": "expressions", "image_url": "💧", "difficulty": 1},
        {"french": "j'arrive de", "shimaore": "tsi lawa", "kibouchi": "zahou boka", "category": "expressions", "image_url": "🏃", "difficulty": 1},
        {"french": "je ne me sens pas bien", "shimaore": "tsissi fétré", "kibouchi": "za maharengni nafoussokou moidéhi", "category": "expressions", "image_url": "😵", "difficulty": 2},
        {"french": "je ne peux pas", "shimaore": "tsi chindri", "kibouchi": "zahou tsi mahaléou", "category": "expressions", "image_url": "🚫", "difficulty": 1},
        {"french": "je peux avoir des toilettes", "shimaore": "tnissi miya mraba", "kibouchi": "zahou mangataka mraba", "category": "expressions", "image_url": "🚽", "difficulty": 1},
        {"french": "je prends ça", "shimaore": "nissi renga ini", "kibouchi": "zahou bou angala ini", "category": "expressions", "image_url": "✋", "difficulty": 1},
        {"french": "je suis perdu", "shimaore": "tsi latsiha", "kibouchi": "zahou véri", "category": "expressions", "image_url": "🤷", "difficulty": 1},
        {"french": "je t'aime", "shimaore": "nisouhou vendza", "kibouchi": "zahou mitia anaou", "category": "expressions", "image_url": "❤️", "difficulty": 1},
        {"french": "je veux manger", "shimaore": "nissi miya chaoula", "kibouchi": "zahou mila ihinagna", "category": "expressions", "image_url": "🍽️", "difficulty": 1},
        {"french": "je voudrais aller à", "shimaore": "nissi tsaha nendré", "kibouchi": "zahou chokou andeha", "category": "expressions", "image_url": "🚶", "difficulty": 1},
        {"french": "joie", "shimaore": "fouraha", "kibouchi": "aravouangna", "category": "expressions", "image_url": "😊", "difficulty": 1},
        {"french": "moins cher s'il vous plaît", "shimaore": "nissi miya ouchoukidzé", "kibouchi": "za mangataka koupoungousza kima", "category": "expressions", "image_url": "💰", "difficulty": 2},
        {"french": "montre-moi", "shimaore": "néssédzéyé", "kibouchi": "ampizaha zahou", "category": "expressions", "image_url": "👁️", "difficulty": 1},
        {"french": "nounou", "shimaore": "mlezi", "kibouchi": "mlezi", "category": "expressions", "image_url": "👵", "difficulty": 1},
        {"french": "où se trouve", "shimaore": "ouparihanoua havi", "kibouchi": "aya moi", "category": "expressions", "image_url": "📍", "difficulty": 1},
        {"french": "où sommes-nous", "shimaore": "ra havi", "kibouchi": "atsika yétou aya", "category": "expressions", "image_url": "📍", "difficulty": 1},
        {"french": "pouvez-vous m'aider ?", "shimaore": "ni sayidié vanou", "kibouchi": "zahou mangataka moussada", "category": "expressions", "image_url": "🤝", "difficulty": 1},
        {"french": "quelqu'un de fiable", "shimaore": "mwaminifou", "kibouchi": "mwaminifou", "category": "expressions", "image_url": "🤝", "difficulty": 2},
        {"french": "respect", "shimaore": "mastaha", "kibouchi": "mastaha", "category": "expressions", "image_url": "🙏", "difficulty": 1},
        {"french": "s'il vous plaît", "shimaore": "tafadali", "kibouchi": "tafadali", "category": "expressions", "image_url": "🙏", "difficulty": 1},
        {"french": "secret", "shimaore": "siri", "kibouchi": "siri", "category": "expressions", "image_url": "🤫", "difficulty": 1},
        {"french": "tout droit", "shimaore": "hondzoha", "kibouchi": "mahitsi", "category": "expressions", "image_url": "⬆️", "difficulty": 1},
        {"french": "trop cher", "shimaore": "hali", "kibouchi": "saroutrou", "category": "expressions", "image_url": "💸", "difficulty": 1},
    ]
    
    # SECTION ADJECTIFS - 45 adjectifs exacts selon l'image (triés par ordre alphabétique)
    adjectifs_vocabulary = [
        {"french": "amoureux", "shimaore": "ouvendza", "kibouchi": "mitiya", "category": "adjectifs", "image_url": "😍", "difficulty": 1},
        {"french": "ancien", "shimaore": "halé", "kibouchi": "kevi", "category": "adjectifs", "image_url": "🏛️", "difficulty": 1},
        {"french": "beau/jolie", "shimaore": "mzouri", "kibouchi": "zatovou", "category": "adjectifs", "image_url": "😍", "difficulty": 1},
        {"french": "bête", "shimaore": "dhaba", "kibouchi": "dhaba", "category": "adjectifs", "image_url": "🤪", "difficulty": 1},
        {"french": "bon", "shimaore": "mwéma", "kibouchi": "tsara", "category": "adjectifs", "image_url": "👍", "difficulty": 1},
        {"french": "calme", "shimaore": "baridi", "kibouchi": "malémi", "category": "adjectifs", "image_url": "😌", "difficulty": 1},
        {"french": "chaud", "shimaore": "moro", "kibouchi": "méyi", "category": "adjectifs", "image_url": "🔥", "difficulty": 1},
        {"french": "colère", "shimaore": "hadabou", "kibouchi": "mélonkou", "category": "adjectifs", "image_url": "😠", "difficulty": 1},
        {"french": "content", "shimaore": "oujiviwa", "kibouchi": "ravou", "category": "adjectifs", "image_url": "😊", "difficulty": 1},
        {"french": "court", "shimaore": "coutri", "kibouchi": "fohlki", "category": "adjectifs", "image_url": "📏", "difficulty": 1},
        {"french": "difficile", "shimaore": "ndziro", "kibouchi": "mahéri", "category": "adjectifs", "image_url": "😵", "difficulty": 1},
        {"french": "drôle", "shimaore": "outsésa", "kibouchi": "mampimoli", "category": "adjectifs", "image_url": "😂", "difficulty": 1},
        {"french": "dur", "shimaore": "mangavou", "kibouchi": "mahéri", "category": "adjectifs", "image_url": "🪨", "difficulty": 1},
        {"french": "facile", "shimaore": "ndzangou", "kibouchi": "mora", "category": "adjectifs", "image_url": "😊", "difficulty": 1},
        {"french": "fâché", "shimaore": "ouja hassira", "kibouchi": "mélonkou", "category": "adjectifs", "image_url": "😠", "difficulty": 1},
        {"french": "fatigué", "shimaore": "ouléméwa", "kibouchi": "vaha", "category": "adjectifs", "image_url": "😴", "difficulty": 1},
        {"french": "faux", "shimaore": "trombo", "kibouchi": "vandi", "category": "adjectifs", "image_url": "❌", "difficulty": 1},
        {"french": "fermé", "shimaore": "oubala", "kibouchi": "migadra", "category": "adjectifs", "image_url": "🔒", "difficulty": 1},
        {"french": "fier", "shimaore": "oujiviwa", "kibouchi": "ravou", "category": "adjectifs", "image_url": "😤", "difficulty": 1},
        {"french": "fort", "shimaore": "ouna ngouvou", "kibouchi": "missi ngouvou", "category": "adjectifs", "image_url": "💪", "difficulty": 1},
        {"french": "froid", "shimaore": "baridi", "kibouchi": "manintsi", "category": "adjectifs", "image_url": "❄️", "difficulty": 1},
        {"french": "gentil", "shimaore": "mwéma", "kibouchi": "tsara rohou", "category": "adjectifs", "image_url": "😊", "difficulty": 1},
        {"french": "grand", "shimaore": "bolé", "kibouchi": "bé", "category": "adjectifs", "image_url": "📏", "difficulty": 1},
        {"french": "gros", "shimaore": "mtronga/tronga", "kibouchi": "bé", "category": "adjectifs", "image_url": "🔵", "difficulty": 1},
        {"french": "honteux", "shimaore": "ouona haya", "kibouchi": "mampiflingnatia", "category": "adjectifs", "image_url": "😳", "difficulty": 1},
        {"french": "important", "shimaore": "mouhimou", "kibouchi": "mouhimou", "category": "adjectifs", "image_url": "⭐", "difficulty": 1},
        {"french": "inquiet", "shimaore": "ouna hamo", "kibouchi": "miyéfitri/kouchanga", "category": "adjectifs", "image_url": "😰", "difficulty": 1},
        {"french": "intelligent", "shimaore": "mstanrabou", "kibouchi": "trara louha", "category": "adjectifs", "image_url": "🧠", "difficulty": 1},
        {"french": "inutile", "shimaore": "kassina mana", "kibouchi": "tsissi fotouri", "category": "adjectifs", "image_url": "🗑️", "difficulty": 1},
        {"french": "jeune", "shimaore": "nrétsa", "kibouchi": "zaza", "category": "adjectifs", "image_url": "👶", "difficulty": 1},
        {"french": "laid", "shimaore": "tsi ndzouzouri", "kibouchi": "ratsi sora", "category": "adjectifs", "image_url": "😬", "difficulty": 1},
        {"french": "léger", "shimaore": "ndzangou", "kibouchi": "mivivagna", "category": "adjectifs", "image_url": "🪶", "difficulty": 1},
        {"french": "long", "shimaore": "drilé", "kibouchi": "labou", "category": "adjectifs", "image_url": "📏", "difficulty": 1},
        {"french": "lourd", "shimaore": "ndziro", "kibouchi": "mavéchatra", "category": "adjectifs", "image_url": "🏋️", "difficulty": 1},
        {"french": "maigre", "shimaore": "tsala", "kibouchi": "mahia", "category": "adjectifs", "image_url": "📏", "difficulty": 1},
        {"french": "mauvais", "shimaore": "mbovou", "kibouchi": "mwadéli", "category": "adjectifs", "image_url": "👎", "difficulty": 1},
        {"french": "méchant", "shimaore": "mbovou", "kibouchi": "ratsi rohou", "category": "adjectifs", "image_url": "😠", "difficulty": 1},
        {"french": "mou", "shimaore": "trémboivou", "kibouchi": "malémi", "category": "adjectifs", "image_url": "🧽", "difficulty": 1},
        {"french": "nerveux", "shimaore": "oussikitiha", "kibouchi": "téhi téhitri", "category": "adjectifs", "image_url": "😰", "difficulty": 1},
        {"french": "nouveau", "shimaore": "piya", "kibouchi": "vowou", "category": "adjectifs", "image_url": "✨", "difficulty": 1},
        {"french": "ouvert", "shimaore": "ouboua", "kibouchi": "mibiyangna", "category": "adjectifs", "image_url": "🔓", "difficulty": 1},
        {"french": "pauvre", "shimaore": "maskini", "kibouchi": "maskini", "category": "adjectifs", "image_url": "💸", "difficulty": 1},
        {"french": "petit", "shimaore": "titi", "kibouchi": "héli", "category": "adjectifs", "image_url": "📏", "difficulty": 1},
        {"french": "propre", "shimaore": "trahara", "kibouchi": "madiou", "category": "adjectifs", "image_url": "✨", "difficulty": 1},
        {"french": "riche", "shimaore": "tadjiri", "kibouchi": "tadjiri", "category": "adjectifs", "image_url": "💰", "difficulty": 1},
        {"french": "sale", "shimaore": "trotro", "kibouchi": "malourou", "category": "adjectifs", "image_url": "🦠", "difficulty": 1},
        {"french": "satisfait", "shimaore": "oufourahi", "kibouchi": "ravou", "category": "adjectifs", "image_url": "😌", "difficulty": 1},
        {"french": "sérieux", "shimaore": "kassidi", "kibouchi": "koussoudi", "category": "adjectifs", "image_url": "😐", "difficulty": 1},
        {"french": "surpris", "shimaore": "oumarouha", "kibouchi": "téhitri", "category": "adjectifs", "image_url": "😲", "difficulty": 1},
        {"french": "triste", "shimaore": "ouna hamo", "kibouchi": "malahélou", "category": "adjectifs", "image_url": "😢", "difficulty": 1},
        {"french": "vieux", "shimaore": "dhouha", "kibouchi": "héla", "category": "adjectifs", "image_url": "👴", "difficulty": 1},
        {"french": "vrai", "shimaore": "kwéli", "kibouchi": "ankitigni", "category": "adjectifs", "image_url": "✅", "difficulty": 1},
    ]
    
    # Fonction pour supprimer les doublons tout en gardant l'ordre alphabétique
    def remove_duplicates(words_list):
        seen = set()
        unique_words = []
        for word in words_list:
            # Utiliser le mot français comme clé unique
            key = word["french"].lower()
            if key not in seen:
                seen.add(key)
                unique_words.append(word)
        return unique_words
    
    # Supprimer les doublons et trier par ordre alphabétique
    expressions_vocabulary = remove_duplicates(sorted(expressions_vocabulary, key=lambda x: x["french"].lower()))
    adjectifs_vocabulary = remove_duplicates(sorted(adjectifs_vocabulary, key=lambda x: x["french"].lower()))
    
    # Ajouter timestamp à chaque mot
    all_vocabulary = expressions_vocabulary + adjectifs_vocabulary
    for word in all_vocabulary:
        word["created_at"] = datetime.utcnow()
    
    # Insérer tous les nouveaux mots
    result = words_collection.insert_many(all_vocabulary)
    
    print(f"✅ Sections expressions et adjectifs mises à jour : {len(result.inserted_ids)} mots ajoutés")
    print(f"📊 Expressions : {len(expressions_vocabulary)} mots (triées alphabétiquement)")
    print(f"📊 Adjectifs : {len(adjectifs_vocabulary)} mots (triés alphabétiquement)")
    
    # Vérification
    total_words = words_collection.count_documents({})
    expressions_count = words_collection.count_documents({"category": "expressions"})
    adjectifs_count = words_collection.count_documents({"category": "adjectifs"})
    
    print(f"\n📈 STATISTIQUES MISES À JOUR :")
    print(f"   Total des mots dans la base : {total_words}")
    print(f"   Mots dans la catégorie expressions : {expressions_count}")
    print(f"   Mots dans la catégorie adjectifs : {adjectifs_count}")
    print(f"\n✨ DOUBLONS SUPPRIMÉS et TRI ALPHABÉTIQUE APPLIQUÉ")
    
    return len(result.inserted_ids)

if __name__ == "__main__":
    print("🔄 Mise à jour des sections expressions et adjectifs avec les données des images...")
    print("🧹 Suppression automatique des doublons et tri alphabétique...")
    count = update_expressions_adjectifs()
    print(f"✅ Terminé ! {count} mots (expressions + adjectifs) mis à jour selon les images.")