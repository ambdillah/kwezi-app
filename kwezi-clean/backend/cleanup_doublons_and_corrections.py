#!/usr/bin/env python3
"""
NETTOYAGE COMPLET : DOUBLONS, EMOJIS ET CORRECTIONS
==================================================
1. Détecte et analyse tous les doublons
2. Supprime les emojis spécifiés
3. Applique les corrections demandées
4. Corrige l'orthographe française
"""

import os
import re
from pymongo import MongoClient
from dotenv import load_dotenv
from database_protection import protect_database, db_protector

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'mayotte_app')

# Mots dont il faut supprimer les emojis
MOTS_SUPPRIMER_EMOJIS = [
    "testicules", "côtes", "fruit du jacquier", "scolopendre", 
    "puce", "poux", "oursin"
]

# Corrections spécifiques demandées
CORRECTIONS_SPECIFIQUES = {
    "mille-pattes": {"shimaore": "mjongo", "kibouchi": "ancoudavitri"},
    "mille pattes": {"shimaore": "mjongo", "kibouchi": "ancoudavitri"},
    "phacochère": {"kibouchi": "lambou di"}
}

# Corrections d'orthographe françaises
CORRECTIONS_ORTHOGRAPHE = {
    # Accents manquants
    "cotes": "côtes",
    "scolopedre": "scolopendre", 
    "testicule": "testicules",
    "mille pattes": "mille-pattes",
    "phacochere": "phacochère",
    "phacochare": "phacochère",
    
    # Autres corrections courantes
    "eleve": "élève",
    "eleveur": "éleveur", 
    "ecole": "école",
    "ecrire": "écrire",
    "ecouter": "écouter",
    "etudier": "étudier",
    "etoile": "étoile",
    "etre": "être",
    "hopital": "hôpital",
    "hotel": "hôtel",
    "ile": "île",
    "theatre": "théâtre",
    "fete": "fête",
    "foret": "forêt",
    "garcon": "garçon",
    "francais": "français",
    "lecon": "leçon",
    "apartement": "appartement",
    "diferent": "différent",
    "language": "langage",
    "reussir": "réussir",
    "vraiment": "vraiment"
}

def detecter_doublons(words_collection):
    """Détecte tous les doublons dans la base de données"""
    print("🔍 DÉTECTION DES DOUBLONS...")
    
    # Récupérer tous les mots
    tous_les_mots = list(words_collection.find({}))
    
    # Grouper par mot français (insensible à la casse)
    mots_groupes = {}
    for mot in tous_les_mots:
        french_key = mot.get('french', '').lower().strip()
        if french_key:
            if french_key not in mots_groupes:
                mots_groupes[french_key] = []
            mots_groupes[french_key].append(mot)
    
    # Identifier les doublons
    doublons = {}
    for french_key, mots in mots_groupes.items():
        if len(mots) > 1:
            doublons[french_key] = mots
    
    print(f"📊 {len(doublons)} groupes de doublons détectés")
    return doublons

def analyser_doublon(mots):
    """Analyse un groupe de doublons pour déterminer s'ils sont identiques ou différents"""
    if len(mots) <= 1:
        return "unique", None
    
    # Comparer les traductions
    premier_mot = mots[0]
    traductions_identiques = True
    
    for mot in mots[1:]:
        if (mot.get('shimaore', '').strip() != premier_mot.get('shimaore', '').strip() or
            mot.get('kibouchi', '').strip() != premier_mot.get('kibouchi', '').strip()):
            traductions_identiques = False
            break
    
    if traductions_identiques:
        return "identiques", None
    else:
        return "differents", mots

@protect_database("cleanup_doublons_and_corrections")
def nettoyer_base_complete():
    """Effectue le nettoyage complet de la base de données"""
    print("🔧 NETTOYAGE COMPLET DE LA BASE DE DONNÉES")
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
    
    # Statistiques
    doublons_supprimes = 0
    emojis_supprimes = 0
    corrections_orthographe = 0
    corrections_traductions = 0
    doublons_differents = []
    
    # 1. DÉTECTION ET ANALYSE DES DOUBLONS
    doublons = detecter_doublons(words_collection)
    
    for french_key, mots in doublons.items():
        type_doublon, mots_differents = analyser_doublon(mots)
        
        if type_doublon == "identiques":
            # Supprimer tous sauf le premier
            print(f"🗑️ Suppression de {len(mots)-1} doublons identiques pour '{french_key}'")
            for mot in mots[1:]:
                words_collection.delete_one({"_id": mot["_id"]})
                doublons_supprimes += 1
                
        elif type_doublon == "differents":
            print(f"❓ Doublons avec traductions différentes pour '{french_key}':")
            for i, mot in enumerate(mots, 1):
                print(f"   {i}. Shimaoré: '{mot.get('shimaore', 'N/A')}', Kibouchi: '{mot.get('kibouchi', 'N/A')}' (Catégorie: {mot.get('category', 'N/A')})")
            doublons_differents.append((french_key, mots))
    
    # 2. CORRECTIONS D'ORTHOGRAPHE ET SUPPRESSIONS D'EMOJIS
    print(f"\n📝 APPLICATION DES CORRECTIONS...")
    tous_les_mots = list(words_collection.find({}))
    
    for mot in tous_les_mots:
        mot_modifie = False
        
        # Correction orthographe française
        french_original = mot.get('french', '')
        french_corrige = CORRECTIONS_ORTHOGRAPHE.get(french_original.lower(), french_original)
        
        if french_corrige != french_original:
            words_collection.update_one(
                {"_id": mot["_id"]},
                {"$set": {"french": french_corrige}}
            )
            print(f"  📝 Orthographe: '{french_original}' → '{french_corrige}'")
            corrections_orthographe += 1
            mot_modifie = True
        
        # Suppression d'emojis spécifiques
        french_check = french_corrige.lower()
        if any(mot_cible.lower() in french_check for mot_cible in MOTS_SUPPRIMER_EMOJIS):
            if mot.get('image_url') and mot['image_url'] not in ['', None]:
                words_collection.update_one(
                    {"_id": mot["_id"]},
                    {"$set": {"image_url": ""}}
                )
                print(f"  🚫 Emoji supprimé pour '{french_corrige}'")
                emojis_supprimes += 1
                mot_modifie = True
        
        # Corrections de traductions spécifiques
        for mot_francais, corrections in CORRECTIONS_SPECIFIQUES.items():
            if french_check == mot_francais.lower():
                updates = {}
                if "shimaore" in corrections:
                    current_shimaore = mot.get('shimaore', '')
                    if current_shimaore != corrections["shimaore"]:
                        updates["shimaore"] = corrections["shimaore"]
                        print(f"  🔄 Shimaoré pour '{french_corrige}': '{current_shimaore}' → '{corrections['shimaore']}'")
                
                if "kibouchi" in corrections:
                    current_kibouchi = mot.get('kibouchi', '')
                    if current_kibouchi != corrections["kibouchi"]:
                        updates["kibouchi"] = corrections["kibouchi"]
                        print(f"  🔄 Kibouchi pour '{french_corrige}': '{current_kibouchi}' → '{corrections['kibouchi']}'")
                
                if updates:
                    words_collection.update_one(
                        {"_id": mot["_id"]},
                        {"$set": updates}
                    )
                    corrections_traductions += 1
                    mot_modifie = True
    
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DU NETTOYAGE COMPLET:")
    print(f"🗑️ Doublons identiques supprimés: {doublons_supprimes}")
    print(f"🚫 Emojis supprimés: {emojis_supprimes}")
    print(f"📝 Corrections d'orthographe: {corrections_orthographe}")
    print(f"🔄 Corrections de traductions: {corrections_traductions}")
    print(f"❓ Doublons avec traductions différentes: {len(doublons_differents)}")
    
    # Afficher les doublons nécessitant une décision manuelle
    if doublons_differents:
        print("\n" + "=" * 80)
        print("❓ DOUBLONS NÉCESSITANT UNE DÉCISION MANUELLE:")
        print("=" * 80)
        for french_key, mots in doublons_differents:
            print(f"\n🔍 Mot: '{french_key.upper()}'")
            for i, mot in enumerate(mots, 1):
                print(f"   Option {i}: Shimaoré='{mot.get('shimaore', 'N/A')}', Kibouchi='{mot.get('kibouchi', 'N/A')}', Catégorie={mot.get('category', 'N/A')}")
        print("\n⚠️ IMPORTANT: Veuillez indiquer quels doublons supprimer pour ces mots.")
    
    # Vérification finale de l'intégrité
    print("\n🔍 Vérification de l'intégrité post-nettoyage...")
    is_healthy, message = db_protector.is_database_healthy()
    if is_healthy:
        print("✅ Base de données saine après nettoyage")
    else:
        print(f"⚠️ Problème détecté: {message}")
    
    client.close()
    return doublons_differents

if __name__ == "__main__":
    print("🚀 Démarrage du nettoyage complet de la base de données...")
    
    # Vérifier l'état initial
    print("\n🔍 Vérification de l'état initial de la base de données...")
    is_healthy, message = db_protector.is_database_healthy()
    if not is_healthy:
        print(f"⚠️ Problème détecté avant nettoyage: {message}")
        print("🔄 Restauration recommandée avant nettoyage")
        exit(1)
    
    # Effectuer le nettoyage
    doublons_differents = nettoyer_base_complete()
    
    print("\n🎉 NETTOYAGE COMPLET TERMINÉ!")
    print("✅ Doublons identiques supprimés")
    print("✅ Emojis indésirables supprimés") 
    print("✅ Orthographe française corrigée")
    print("✅ Traductions spécifiques corrigées")
    
    if doublons_differents:
        print(f"\n⚠️ {len(doublons_differents)} groupes de doublons nécessitent votre décision")
        print("Merci de préciser lesquels supprimer pour chaque groupe affiché ci-dessus.")
    
    print("\nFin du script de nettoyage complet.")