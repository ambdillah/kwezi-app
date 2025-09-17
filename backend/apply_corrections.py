#!/usr/bin/env python3
"""
Script pour appliquer les corrections spécifiques selon le tableau fourni par l'utilisateur
Corrections des traductions en shimaoré et kibouchi
"""

import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/mayotte_app")
client = MongoClient(MONGO_URL)
db = client.mayotte_app
words_collection = db.words

def apply_corrections():
    """Appliquer toutes les corrections selon le tableau fourni"""
    
    print("🔄 Application des corrections selon le tableau fourni...")
    
    # Dictionnaire des corrections à appliquer
    corrections = {
        # Verbes - corrections
        "vivre": {"shimaore": "ouyinchi", "kibouchi": "mikouénchi"},
        "attendre": {"shimaore": "oulindra", "kibouchi": "mandgni"},
        "faire pipi": {"shimaore": "ougna kojo", "kibouchi": "mamani"},
        "embrasser": {"shimaore": "ounouka", "kibouchi": "mihoroukou"},
        "avertir": {"shimaore": "outahadaricha", "kibouchi": "mampaheyi"},
        "se laver le derrière": {"shimaore": "outsamba", "kibouchi": "mambouyi"},
        "se laver": {"shimaore": "ouhowa", "kibouchi": "misseki"},
        "réchauffer": {"shimaore": "ouhelesedza", "kibouchi": "mamana"},
        "jouer": {"shimaore": "ounguadza", "kibouchi": "msoma"},
        "donner": {"shimaore": "ouva", "kibouchi": "magnamiya"},
        "entrer": {"shimaore": "ounguiya", "kibouchi": "mihidiri"},
        
        # Expressions - corrections
        "au milieu": {"shimaore": "hari", "kibouchi": "angnivou"},
        "j'ai soif": {"shimaore": "nissi ona niyora", "kibouchi": "zahou tindranou"},
        "je prends ça": {"shimaore": "nissi renga ini", "kibouchi": "zahou bou angala tihi"},
        "moins cher s'il vous plaît": {"shimaore": "nissi miya ouchoukidze", "kibouchi": "za mangataka koupoundouza kima"},
        "bonne nuit": {"shimaore": "oukou wa hairi", "kibouchi": "haligni tsara"},
        "au revoir": {"shimaore": "kwaheri", "kibouchi": "maeva"},
        
        # Adjectifs - corrections
        "colère": {"shimaore": "hadabou", "kibouchi": "meloukou"},
        "court": {"shimaore": "coutri", "kibouchi": "fohiki"},
        "drôle": {"shimaore": "outsésa", "kibouchi": "mampimohi"},
        "faux": {"shimaore": "trambo", "kibouchi": "vandi"},
        "long": {"shimaore": "drile", "kibouchi": "habou"},
        "sale": {"shimaore": "trotro", "kibouchi": "maloutou"},
        
        # Famille - corrections
        "tante": {"shimaore": "mama titi/bolé", "kibouchi": "nindri heli/bé"},
        "petite sœur": {"shimaore": "moinagna mtroumama", "kibouchi": "zandri viavi"},
        "petit frère": {"shimaore": "moinagna mtroubaba", "kibouchi": "zandri lalahi"},
        "nounou": {"shimaore": "mlezi", "kibouchi": "mlezi"},
        
        # Couleurs - corrections
        "bleu": {"shimaore": "bilé", "kibouchi": "mayitsou bilé"},
        "gris": {"shimaore": "djifou", "kibouchi": "dzofou"},
        
        # Animaux - corrections
        "pigeon": {"shimaore": "ndiwa", "kibouchi": "ndiwa"},
        "fourmis": {"shimaore": "tsoussou", "kibouchi": "vitsiki"},
        "mille pattes": {"shimaore": "mjongo", "kibouchi": "ancoudafiri"},
        "oursin": {"shimaore": "gadzassi", "kibouchi": "vouli vayi"},
        "huître": {"shimaore": "gadzassi", "kibouchi": "sadza"},
        
        # Corps - corrections
        "arrière du crâne": {"shimaore": "komoi", "kibouchi": "kiroika"},
        
        # Maison - corrections
        "marmite": {"shimaore": "gnoumsou", "kibouchi": "vilangni"},
        "torche": {"shimaore": "pongé", "kibouchi": "pongi"},  # Correction en rouge
    }
    
    corrections_appliquees = 0
    mots_non_trouves = []
    
    # Appliquer chaque correction
    for mot_francais, nouvelles_traductions in corrections.items():
        # Chercher le mot dans la base de données (insensible à la casse)
        query = {"french": {"$regex": f"^{mot_francais}$", "$options": "i"}}
        mots_trouves = list(words_collection.find(query))
        
        if mots_trouves:
            for mot in mots_trouves:
                # Mettre à jour les traductions
                update_data = {
                    "shimaore": nouvelles_traductions["shimaore"],
                    "kibouchi": nouvelles_traductions["kibouchi"],
                    "updated_at": datetime.utcnow()
                }
                
                result = words_collection.update_one(
                    {"_id": mot["_id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    corrections_appliquees += 1
                    print(f"✅ Corrigé '{mot_francais}': {nouvelles_traductions['shimaore']} / {nouvelles_traductions['kibouchi']}")
                else:
                    print(f"⚠️ Aucune modification pour '{mot_francais}' (déjà à jour)")
        else:
            mots_non_trouves.append(mot_francais)
            print(f"❌ Mot non trouvé : '{mot_francais}'")
    
    # Résumé des corrections
    print(f"\n📊 RÉSUMÉ DES CORRECTIONS :")
    print(f"   ✅ Corrections appliquées : {corrections_appliquees}")
    print(f"   ❌ Mots non trouvés : {len(mots_non_trouves)}")
    
    if mots_non_trouves:
        print(f"   📋 Mots non trouvés : {', '.join(mots_non_trouves)}")
    
    # Vérification finale
    total_words = words_collection.count_documents({})
    print(f"   📈 Total des mots dans la base : {total_words}")
    
    return corrections_appliquees

def verify_corrections():
    """Vérifier quelques-unes des corrections appliquées"""
    print("\n🔍 Vérification de quelques corrections...")
    
    test_words = ["torche", "bleu", "j'ai soif", "marmite", "fourmis"]
    
    for word in test_words:
        result = words_collection.find_one({"french": {"$regex": f"^{word}$", "$options": "i"}})
        if result:
            print(f"✅ {word}: {result['shimaore']} / {result['kibouchi']}")
        else:
            print(f"❌ {word}: Non trouvé")

if __name__ == "__main__":
    print("🔧 Application des corrections selon le tableau fourni...")
    count = apply_corrections()
    verify_corrections()
    print(f"\n✅ Terminé ! {count} corrections appliquées avec succès.")