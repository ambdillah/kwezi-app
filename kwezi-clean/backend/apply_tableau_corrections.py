#!/usr/bin/env python3
"""
APPLICATION DES CORRECTIONS DU TABLEAU UTILISATEUR
==================================================
Ce script applique les corrections spécifiques du tableau fourni
par l'utilisateur pour corriger certains mots et expressions.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from database_protection import protect_database, db_protector

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'mayotte_app')

def get_mongo_client():
    """Connexion à MongoDB"""
    try:
        client = MongoClient(MONGO_URL)
        client.admin.command('ping')
        print(f"✅ Connexion MongoDB établie : {MONGO_URL}")
        return client
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB : {e}")
        return None

# Corrections extraites du tableau utilisateur
CORRECTIONS = [
    # Corrections critiques identifiées
    {"french": "vivre", "shimaore": "ouyinchi", "kibouchi": "mikouènchi"},
    {"french": "attendre", "shimaore": "oulindra", "kibouchi": "mandigni"},
    {"french": "faire pipi", "shimaore": "ougna kojo", "kibouchi": "mamani"},
    {"french": "embrasser", "shimaore": "ounouka", "kibouchi": "mihoroukou"},
    {"french": "avertir", "shimaore": "outahadaricha", "kibouchi": "mampahéyi"},
    {"french": "se laver le derrière", "shimaore": "outsamba", "kibouchi": "mambouyi"},
    {"french": "se laver", "shimaore": "ouhowa", "kibouchi": "misséki"},
    {"french": "réchauffer", "shimaore": "ouhelesedza", "kibouchi": "mamana"},
    {"french": "au milieu", "shimaore": "hari", "kibouchi": "angnivou"},
    {"french": "colère", "shimaore": "hadabou", "kibouchi": "méloukou"},
    {"french": "court", "shimaore": "coutri", "kibouchi": "fohiki"},
    {"french": "drôle", "shimaore": "outsésa", "kibouchi": "mampimohi"},
    {"french": "faux", "shimaore": "trambo", "kibouchi": "vandi"},
    {"french": "long", "shimaore": "drilé", "kibouchi": "habou"},
    {"french": "sale", "shimaore": "trotro", "kibouchi": "maloutou"},
    {"french": "j'ai soif", "shimaore": "nissi ona niyora", "kibouchi": "zahou tindranou"},
    {"french": "je prends ça", "shimaore": "nissi renga ini", "kibouchi": "zahou bou angala tihi"},
    {"french": "moins cher s'il vous plaît", "shimaore": "nissi miya ouchoukidzé", "kibouchi": "za mangataka koupoungouza kima"},
    {"french": "nounou", "shimaore": "mlézi", "kibouchi": "mlézi"},
    {"french": "jouer", "shimaore": "ounguadza", "kibouchi": "msoma"},
    {"french": "donner", "shimaore": "ouva", "kibouchi": "magnamiya"},
    {"french": "entrer", "shimaore": "ounguïya", "kibouchi": "mihiditri"},
    {"french": "pigeon", "shimaore": "ndiwa", "kibouchi": "ndiwa"},
    {"french": "fourmis", "shimaore": "tjoussou", "kibouchi": "vitsiki"},
    {"french": "mille-pattes", "shimaore": "mjongo", "kibouchi": "ancoudafitri"},
    {"french": "oursin", "shimaore": "gadzassi", "kibouchi": "vouli vavi"},
    {"french": "huître", "shimaore": "gadzassi", "kibouchi": "sadza"},
    {"french": "arrière du crâne", "shimaore": "komoi", "kibouchi": "kitoika"},
    {"french": "bonne nuit", "shimaore": "oukou wa hairi", "kibouchi": "haligni tsara"},
    {"french": "au revoir", "shimaore": "kwaheri", "kibouchi": "maeva"},
    {"french": "tante", "shimaore": "mama titi/bolé", "kibouchi": "nindri heli/bé"},
    {"french": "petite sœur", "shimaore": "moinagna mtroumama", "kibouchi": "zandri viavi"},
    {"french": "petit frère", "shimaore": "moinagna mtroubaba", "kibouchi": "zandri lalahi"},
    {"french": "bleu", "shimaore": "bilé", "kibouchi": "mayitsou bilé"},
    {"french": "gris", "shimaore": "djifou", "kibouchi": "dzofou"},
    {"french": "marmite", "shimaore": "gnoungou", "kibouchi": "vilangni"},
    {"french": "torche", "shimaore": "pongé", "kibouchi": "pongi"},
]

@protect_database("apply_corrections")
def apply_corrections():
    """Applique les corrections du tableau utilisateur"""
    print("🔧 APPLICATION DES CORRECTIONS DU TABLEAU UTILISATEUR")
    print("=" * 60)
    
    client = get_mongo_client()
    if not client:
        return False
    
    db = client[DB_NAME]
    words_collection = db.words
    
    corrections_applied = 0
    corrections_failed = 0
    new_words_added = 0
    
    for correction in CORRECTIONS:
        french = correction["french"]
        shimaore = correction["shimaore"]
        kibouchi = correction["kibouchi"]
        
        print(f"\n🔍 Recherche de '{french}'...")
        
        # Chercher le mot existant (insensible à la casse)
        existing_word = words_collection.find_one({
            "french": {"$regex": f"^{french}$", "$options": "i"}
        })
        
        if existing_word:
            # Vérifier si une correction est nécessaire
            needs_update = False
            update_fields = {}
            
            if existing_word.get("shimaore", "").lower() != shimaore.lower():
                update_fields["shimaore"] = shimaore
                needs_update = True
                print(f"  📝 Shimaoré: '{existing_word.get('shimaore', 'N/A')}' → '{shimaore}'")
            
            if existing_word.get("kibouchi", "").lower() != kibouchi.lower():
                update_fields["kibouchi"] = kibouchi
                needs_update = True
                print(f"  📝 Kibouchi: '{existing_word.get('kibouchi', 'N/A')}' → '{kibouchi}'")
            
            if needs_update:
                # Appliquer la correction
                result = words_collection.update_one(
                    {"_id": existing_word["_id"]},
                    {"$set": update_fields}
                )
                
                if result.modified_count > 0:
                    print(f"  ✅ Correction appliquée pour '{french}'")
                    corrections_applied += 1
                else:
                    print(f"  ❌ Échec de la correction pour '{french}'")
                    corrections_failed += 1
            else:
                print(f"  ✓ '{french}' est déjà correct")
        else:
            # Mot non trouvé - déterminer la catégorie appropriée
            category = determine_category(french)
            
            new_word = {
                "french": french,
                "shimaore": shimaore,
                "kibouchi": kibouchi,
                "category": category,
                "difficulty": 1,
                # Pas d'image_url pour les nouveaux mots pour l'instant
            }
            
            # Ajouter le nouveau mot
            result = words_collection.insert_one(new_word)
            if result.inserted_id:
                print(f"  ➕ Nouveau mot ajouté: '{french}' (catégorie: {category})")
                new_words_added += 1
            else:
                print(f"  ❌ Échec de l'ajout du nouveau mot '{french}'")
                corrections_failed += 1
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES CORRECTIONS:")
    print(f"✅ Corrections appliquées: {corrections_applied}")
    print(f"➕ Nouveaux mots ajoutés: {new_words_added}")
    print(f"❌ Échecs: {corrections_failed}")
    print(f"📝 Total traité: {len(CORRECTIONS)}")
    
    # Vérification finale de l'intégrité
    print("\n🔍 Vérification de l'intégrité post-corrections...")
    is_healthy, message = db_protector.is_database_healthy()
    if is_healthy:
        print("✅ Base de données saine après corrections")
    else:
        print(f"⚠️ Problème détecté: {message}")
    
    client.close()
    return corrections_applied > 0 or new_words_added > 0

def determine_category(french_word):
    """Détermine la catégorie appropriée pour un mot"""
    word_lower = french_word.lower()
    
    # Catégories basées sur le contenu
    if any(keyword in word_lower for keyword in ["je", "j'ai", "moins", "prends"]):
        return "expressions"
    elif any(keyword in word_lower for keyword in ["sœur", "frère", "tante", "nounou"]):
        return "famille"
    elif any(keyword in word_lower for keyword in ["vivre", "attendre", "faire", "embrasser", "donner", "jouer", "entrer"]):
        return "verbes"
    elif any(keyword in word_lower for keyword in ["pigeon", "fourmis", "mille-pattes", "oursin", "huître"]):
        return "animaux"
    elif any(keyword in word_lower for keyword in ["bleu", "gris"]):
        return "couleurs"
    elif any(keyword in word_lower for keyword in ["marmite", "torche"]):
        return "maison"
    elif any(keyword in word_lower for keyword in ["crâne", "derrière"]):
        return "corps"
    elif any(keyword in word_lower for keyword in ["colère", "court", "drôle", "faux", "long", "sale"]):
        return "adjectifs"
    elif any(keyword in word_lower for keyword in ["milieu", "bonne nuit", "au revoir"]):
        return "expressions"
    else:
        return "expressions"  # Catégorie par défaut

if __name__ == "__main__":
    print("🚀 Démarrage de l'application des corrections du tableau...")
    
    # Vérifier l'état initial
    print("\n🔍 Vérification de l'état initial de la base de données...")
    is_healthy, message = db_protector.is_database_healthy()
    if not is_healthy:
        print(f"⚠️ Problème détecté avant corrections: {message}")
        print("🔄 Restauration recommandée avant d'appliquer les corrections")
        exit(1)
    
    # Appliquer les corrections
    success = apply_corrections()
    
    if success:
        print("\n🎉 CORRECTIONS APPLIQUÉES AVEC SUCCÈS!")
        print("✅ La base de données a été mise à jour avec les corrections du tableau")
    else:
        print("\n⚠️ Aucune correction n'a été appliquée")
    
    print("\nFin du script de corrections.")