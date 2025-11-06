#!/usr/bin/env python3
"""
CORRECTIONS COMPLÈTES DES VERBES SELON LES TABLEAUX UTILISATEUR
=============================================================
Applique toutes les corrections de verbes fournies dans les tableaux
plus la correction spécifique de "mille-pattes"
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

# Corrections extraites des tableaux utilisateur
VERBES_CORRECTIONS = [
    # Premier tableau
    {"french": "jouer", "shimaore": "ounguadza", "kibouchi": "msoma"},
    {"french": "courir", "shimaore": "wendra mbiyo", "kibouchi": "miloumeyi"},
    {"french": "dire", "shimaore": "ourongoa", "kibouchi": "mangnabara"},
    {"french": "pouvoir", "shimaore": "ouchindra", "kibouchi": "mahaléou"},
    {"french": "vouloir", "shimaore": "outsaha", "kibouchi": "chokou"},
    {"french": "savoir", "shimaore": "oujoua", "kibouchi": "méhèyi"},
    {"french": "voir", "shimaore": "ouona", "kibouchi": "mahita"},
    {"french": "devoir", "shimaore": "oulazimou", "kibouchi": "tokoutrou"},
    {"french": "venir", "shimaore": "ouja", "kibouchi": "havi"},
    {"french": "rapprocher", "shimaore": "outsenguéléya", "kibouchi": "magnatougnou"},
    {"french": "prendre", "shimaore": "ourenga", "kibouchi": "mangala"},
    {"french": "donner", "shimaore": "ouva", "kibouchi": "magnamiya"},
    {"french": "parler", "shimaore": "oulagoua", "kibouchi": "mivoulangna"},
    {"french": "mettre", "shimaore": "outria", "kibouchi": "mangnanou"},
    {"french": "passer", "shimaore": "ouvira", "kibouchi": "mihomba"},
    {"french": "trouver", "shimaore": "oupara", "kibouchi": "mahazou"},
    {"french": "aimer", "shimaore": "ouvendza", "kibouchi": "mitiya"},
    {"french": "croire", "shimaore": "ouamini", "kibouchi": "koimini"},
    {"french": "penser", "shimaore": "oufikiri", "kibouchi": "midzéri"},
    {"french": "connaître", "shimaore": "oujoua", "kibouchi": "méhèyi"},
    {"french": "demander", "shimaore": "oudzissa", "kibouchi": "magnoutani"},
    {"french": "répondre", "shimaore": "oudjibou", "kibouchi": "mikoudjibou"},
    {"french": "laisser", "shimaore": "oulicha", "kibouchi": "mangnambéla"},
    {"french": "manger", "shimaore": "oudhya", "kibouchi": "mihinagna"},
    {"french": "boire", "shimaore": "ounoua", "kibouchi": "mindranou"},
    {"french": "lire", "shimaore": "ousoma", "kibouchi": "midzorou"},
    {"french": "écrire", "shimaore": "ouhanguiha", "kibouchi": "mikouandika"},
    {"french": "écouter", "shimaore": "ouvoulikia", "kibouchi": "mitangréngni"},
    {"french": "apprendre", "shimaore": "oufoundriha", "kibouchi": "midzorou"},
    {"french": "comprendre", "shimaore": "ouéléwa", "kibouchi": "kouéléwa"},
    {"french": "marcher", "shimaore": "ouendra", "kibouchi": "mandéha"},
    {"french": "entrer", "shimaore": "ounguiya", "kibouchi": "mihiditri"},
    {"french": "sortir", "shimaore": "oulawa", "kibouchi": "miboka"},
    {"french": "rester", "shimaore": "ouketi", "kibouchi": "mipétraka"},
    {"french": "vivre", "shimaore": "ouyinchi", "kibouchi": "mikouènchi"},
    {"french": "dormir", "shimaore": "ulala", "kibouchi": "mandri"},
    {"french": "attendre", "shimaore": "oulindra", "kibouchi": "mandigni"},
    {"french": "suivre", "shimaore": "oulounga", "kibouchi": "mangnaraka"},
    {"french": "tenir", "shimaore": "oussika", "kibouchi": "mitana"},
    {"french": "ouvrir", "shimaore": "ouboua", "kibouchi": "mampibiyangna"},
    {"french": "fermer", "shimaore": "oubala", "kibouchi": "migadra"},
    {"french": "sembler", "shimaore": "oufana", "kibouchi": "mamhiragna"},
    {"french": "paraître", "shimaore": "ouwonehoua", "kibouchi": "ouhitagna"},
    {"french": "devenir", "shimaore": "ougawouha", "kibouchi": "mivadiki"},
    {"french": "tomber", "shimaore": "oupouliha", "kibouchi": "latsaka"},
    {"french": "se rappeler", "shimaore": "oumaézi", "kibouchi": "koufahamou"},
    {"french": "commencer", "shimaore": "ouhandrissa", "kibouchi": "mitaponou"},
    {"french": "finir", "shimaore": "oumalidza", "kibouchi": "mankéfa"},
    {"french": "réussir", "shimaore": "ouchindra", "kibouchi": "mahaléou"},
    {"french": "essayer", "shimaore": "oudjérébou", "kibouchi": "mikoudjérébou"},
    {"french": "attraper", "shimaore": "oubara", "kibouchi": "missamboutrou"},
    {"french": "flatuler", "shimaore": "oujamba", "kibouchi": "manguétoutrou"},
    {"french": "traverser", "shimaore": "ouchiya", "kibouchi": "mitsaka"},
    {"french": "sauter", "shimaore": "ouarouka", "kibouchi": "mivongna"},
    {"french": "frapper", "shimaore": "ourema", "kibouchi": "mamangou"},
    {"french": "faire caca", "shimaore": "ougna madzi", "kibouchi": "manguéri"},
    {"french": "faire pipi", "shimaore": "ougna kojo", "kibouchi": "mamani"},
    {"french": "vomir", "shimaore": "ou raviha", "kibouchi": "mandouwa"},
    {"french": "s'asseoir", "shimaore": "ouketi", "kibouchi": "mipétraka"},
    {"french": "danser", "shimaore": "ouzina", "kibouchi": "mitsindzaka"},
    {"french": "arrêter", "shimaore": "ouziya", "kibouchi": "mitsahatra"},
    {"french": "vendre", "shimaore": "ouhoudza", "kibouchi": "mandafou"},
    {"french": "cracher", "shimaore": "outra marré", "kibouchi": "mandrora"},
    {"french": "mordre", "shimaore": "ouka magno", "kibouchi": "mangnékitri"},
    {"french": "gratter", "shimaore": "oukouwa", "kibouchi": "mihotrou"},
    {"french": "embrasser", "shimaore": "ounouka", "kibouchi": "mihoroukou"},
    {"french": "jeter", "shimaore": "ouvoutsa", "kibouchi": "manopi"},
    {"french": "avertir", "shimaore": "outahadaricha", "kibouchi": "mampahéyi"},
    {"french": "informer", "shimaore": "oujoudza", "kibouchi": "mangnabara"},
    {"french": "se laver le derrière", "shimaore": "outsamba", "kibouchi": "mambouyi"},
    {"french": "se laver", "shimaore": "ouhowa", "kibouchi": "misséki"},
    {"french": "piler", "shimaore": "oudoudoua", "kibouchi": "mandissa"},
    {"french": "changer", "shimaore": "ougaoudza", "kibouchi": "mamadiki"},
    {"french": "étendre au soleil", "shimaore": "ouaniha", "kibouchi": "manapi"},
    {"french": "réchauffer", "shimaore": "ouhelesedza", "kibouchi": "mamana"},
    {"french": "se baigner", "shimaore": "ouhowa", "kibouchi": "misséki"},
    {"french": "faire le lit", "shimaore": "ouhodza", "kibouchi": "mandzari koubani"},
    
    # Deuxième tableau
    {"french": "faire sécher", "shimaore": "ouhoumisa", "kibouchi": "manapi"},
    {"french": "balayer", "shimaore": "ouhoundza", "kibouchi": "mamafa"},
    {"french": "couper", "shimaore": "oukatra", "kibouchi": "manapaka"},
    {"french": "tremper", "shimaore": "oulodza", "kibouchi": "mandzoubougnou"},
    {"french": "se raser", "shimaore": "oumea ndrevu", "kibouchi": "manapaka somboutrou"},
    {"french": "abîmer", "shimaore": "oumengna", "kibouchi": "mandroubaka"},
    {"french": "acheter", "shimaore": "ounounoua", "kibouchi": "mivanga"},
    {"french": "griller", "shimaore": "ouwoha", "kibouchi": "mitonou"},
    {"french": "allumer", "shimaore": "oupatsa", "kibouchi": "mikoupatsa"},
    {"french": "se peigner", "shimaore": "oupengné", "kibouchi": "mipèngni"},
    {"french": "cuisiner", "shimaore": "oupiha", "kibouchi": "mahandrou"},
    {"french": "ranger/arranger", "shimaore": "ourenguélédza", "kibouchi": "magnadzari"},
    {"french": "tresser", "shimaore": "oussouka", "kibouchi": "mitali/mandrari"},
    {"french": "peindre", "shimaore": "ouvaha", "kibouchi": "magnossoutrou"},
    {"french": "essuyer", "shimaore": "ouvangouha", "kibouchi": "mamitri"},
    {"french": "amener/apporter", "shimaore": "ouvinga", "kibouchi": "mandèyi"},
    {"french": "éteindre", "shimaore": "ouzima", "kibouchi": "mamounou"},
    {"french": "tuer", "shimaore": "ouwoula", "kibouchi": "mamounou"},
    {"french": "combler", "shimaore": "oufitsiya", "kibouchi": "mankahampi"},
    {"french": "cultiver", "shimaore": "oulima", "kibouchi": "mikapa"},
    {"french": "couper du bois", "shimaore": "oupasouha kuni", "kibouchi": "mamaki azoumati"},
    {"french": "cueillir", "shimaore": "oupoua", "kibouchi": "mampoka"},
    {"french": "planter", "shimaore": "outabou", "kibouchi": "mamboli"},
    {"french": "creuser", "shimaore": "outsimba", "kibouchi": "mangadi"},
    {"french": "récolter", "shimaore": "ouvouna", "kibouchi": "mampoka"},
    {"french": "bouger", "shimaore": "outsenguéléya", "kibouchi": "mitéki"},
    {"french": "arnaquer", "shimaore": "ou ravi", "kibouchi": "mangalatra"},
]

# Correction spécifique pour mille-pattes
MILLE_PATTES_CORRECTION = {
    "french": "mille-pattes",
    "shimaore": "mjongo", 
    "kibouchi": "ancoudavitri"
}

@protect_database("fix_verbes_corrections_tableau")
def apply_verbes_corrections():
    """Applique toutes les corrections de verbes des tableaux"""
    print("🔧 APPLICATION DES CORRECTIONS DE VERBES DES TABLEAUX UTILISATEUR")
    print("=" * 80)
    
    try:
        client = MongoClient(MONGO_URL)
        client.admin.command('ping')
        print(f"✅ Connexion MongoDB établie : {MONGO_URL}")
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB : {e}")
        return False
    
    db = client[DB_NAME]
    words_collection = db.words
    
    corrections_applied = 0
    corrections_failed = 0
    new_words_added = 0
    
    # Ajouter d'abord la correction de mille-pattes
    all_corrections = VERBES_CORRECTIONS + [MILLE_PATTES_CORRECTION]
    
    for correction in all_corrections:
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
            
            current_shimaore = existing_word.get("shimaore", "").strip()
            current_kibouchi = existing_word.get("kibouchi", "").strip()
            
            if current_shimaore != shimaore:
                update_fields["shimaore"] = shimaore
                needs_update = True
                print(f"  📝 Shimaoré: '{current_shimaore}' → '{shimaore}'")
            
            if current_kibouchi != kibouchi:
                update_fields["kibouchi"] = kibouchi
                needs_update = True
                print(f"  📝 Kibouchi: '{current_kibouchi}' → '{kibouchi}'")
            
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
            if french == "mille-pattes":
                category = "animaux"
            elif french in ["ranger/arranger", "amener/apporter", "couper du bois"]:
                category = "verbes"
            else:
                category = "verbes"  # Par défaut pour les verbes
            
            new_word = {
                "french": french,
                "shimaore": shimaore,
                "kibouchi": kibouchi,
                "category": category,
                "difficulty": 1,
            }
            
            # Ajouter le nouveau mot
            result = words_collection.insert_one(new_word)
            if result.inserted_id:
                print(f"  ➕ Nouveau mot ajouté: '{french}' (catégorie: {category})")
                new_words_added += 1
            else:
                print(f"  ❌ Échec de l'ajout du nouveau mot '{french}'")
                corrections_failed += 1
    
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DES CORRECTIONS DE VERBES:")
    print(f"✅ Corrections appliquées: {corrections_applied}")
    print(f"➕ Nouveaux mots ajoutés: {new_words_added}")
    print(f"❌ Échecs: {corrections_failed}")
    print(f"📝 Total traité: {len(all_corrections)}")
    
    # Vérification finale de l'intégrité
    print("\n🔍 Vérification de l'intégrité post-corrections...")
    is_healthy, message = db_protector.is_database_healthy()
    if is_healthy:
        print("✅ Base de données saine après corrections")
    else:
        print(f"⚠️ Problème détecté: {message}")
    
    client.close()
    return corrections_applied > 0 or new_words_added > 0

if __name__ == "__main__":
    print("🚀 Démarrage de l'application des corrections de verbes des tableaux...")
    
    # Vérifier l'état initial
    print("\n🔍 Vérification de l'état initial de la base de données...")
    is_healthy, message = db_protector.is_database_healthy()
    if not is_healthy:
        print(f"⚠️ Problème détecté avant corrections: {message}")
        print("🔄 Restauration recommandée avant d'appliquer les corrections")
        exit(1)
    
    # Appliquer les corrections
    success = apply_verbes_corrections()
    
    if success:
        print("\n🎉 CORRECTIONS DE VERBES APPLIQUÉES AVEC SUCCÈS!")
        print("✅ La base de données a été mise à jour avec toutes les corrections des tableaux")
        print("✅ 'mille-pattes' corrigé avec 'mjongo' (shimaoré) et 'ancoudavitri' (kibouchi)")
        
        # Vérification finale de l'intégrité
        print("\n🔍 Vérification finale de l'intégrité...")
        is_healthy_after, message_after = db_protector.is_database_healthy()
        if is_healthy_after:
            print("✅ Base de données saine après corrections")
        else:
            print(f"⚠️ Problème détecté après corrections: {message_after}")
    else:
        print("\n⚠️ Aucune correction n'a été appliquée")
    
    print("\nFin du script de corrections de verbes.")