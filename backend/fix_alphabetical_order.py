#!/usr/bin/env python3
"""
CORRECTION DU TRI ALPHABÉTIQUE DANS LA BASE DE DONNÉES
=====================================================
Réorganise physiquement les documents dans MongoDB dans l'ordre alphabétique
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

# Ordre logique pour la grammaire
ORDRE_GRAMMAIRE = [
    "je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
    "il/elle", "ils/elles",
    "moi", "toi", "lui", "nous", "vous", "eux", "elles",
    "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses",
    "notre", "nos", "votre", "vos", "leur", "leurs",
    "le", "la", "les", "un", "une", "des",
    "ce", "cette", "ces", "cet",
    "qui", "que", "quoi", "dont", "où",
    "et", "ou", "mais", "donc", "car", "ni", "or",
    "dans", "sur", "sous", "avec", "sans", "pour", "par", "de", "du", "des"
]

def get_sort_key_grammaire(mot_francais):
    """Retourne une clé de tri pour la grammaire selon l'ordre logique"""
    mot_lower = mot_francais.lower().strip()
    
    if mot_lower in ORDRE_GRAMMAIRE:
        return ORDRE_GRAMMAIRE.index(mot_lower)
    else:
        # Mots non dans la liste logique vont à la fin, par ordre alphabétique
        return 1000 + ord(mot_lower[0]) if mot_lower else 1000

def get_sort_key_nombres(mot_francais):
    """Retourne une clé de tri pour les nombres (ordre croissant)"""
    # Mapping des nombres en français vers leurs valeurs numériques
    nombres_francais = {
        "zéro": 0, "un": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
        "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10,
        "onze": 11, "douze": 12, "treize": 13, "quatorze": 14, "quinze": 15,
        "seize": 16, "dix-sept": 17, "dix-huit": 18, "dix-neuf": 19, "vingt": 20,
        "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
        "11": 11, "12": 12, "13": 13, "14": 14, "15": 15, "16": 16, "17": 17, "18": 18, "19": 19, "20": 20
    }
    
    mot_lower = mot_francais.lower().strip()
    return nombres_francais.get(mot_lower, 1000)  # 1000 pour les non-nombres

@protect_database("fix_alphabetical_order")
def corriger_ordre_alphabetique():
    """Corrige l'ordre alphabétique en supprimant et réinsérant tous les documents"""
    print("🔧 CORRECTION DE L'ORDRE ALPHABÉTIQUE DANS LA BASE DE DONNÉES")
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
    
    # Récupérer tous les mots
    print("\n📚 Récupération de tous les mots...")
    tous_les_mots = list(words_collection.find({}))
    print(f"✅ {len(tous_les_mots)} mots récupérés")
    
    # Organiser par catégorie
    mots_par_categorie = {}
    for mot in tous_les_mots:
        categorie = mot.get('category', 'autres')
        if categorie not in mots_par_categorie:
            mots_par_categorie[categorie] = []
        mots_par_categorie[categorie].append(mot)
    
    print(f"📂 Catégories trouvées: {list(mots_par_categorie.keys())}")
    
    # Vider complètement la collection
    print("\n🗑️ Suppression de tous les documents...")
    result = words_collection.delete_many({})
    print(f"✅ {result.deleted_count} documents supprimés")
    
    # Réinsérer les mots dans l'ordre correct
    total_inseres = 0
    
    for categorie, mots in mots_par_categorie.items():
        print(f"\n🔄 Traitement de la catégorie '{categorie}' ({len(mots)} mots)...")
        
        # Trier selon la catégorie
        if categorie.lower() == 'nombres':
            # Tri par ordre croissant pour les nombres
            mots_tries = sorted(mots, key=lambda x: get_sort_key_nombres(x.get('french', '')))
            print(f"  📊 Catégorie '{categorie}' triée par ordre croissant")
        elif categorie.lower() == 'grammaire':
            # Tri logique pour la grammaire
            mots_tries = sorted(mots, key=lambda x: get_sort_key_grammaire(x.get('french', '')))
            print(f"  📚 Catégorie '{categorie}' triée par ordre logique")
        else:
            # Tri alphabétique pour toutes les autres catégories
            mots_tries = sorted(mots, key=lambda x: x.get('french', '').lower().strip())
            print(f"  🔤 Catégorie '{categorie}' triée par ordre alphabétique")
            
            # Afficher les 5 premiers pour vérification
            premiers_mots = [mot.get('french', '') for mot in mots_tries[:5]]
            print(f"    Premiers mots: {', '.join(premiers_mots)}")
        
        # Préparer les documents pour insertion (sans _id)
        documents_a_inserer = []
        for mot in mots_tries:
            # Créer une copie du document sans l'ancien _id
            nouveau_document = {k: v for k, v in mot.items() if k != '_id'}
            documents_a_inserer.append(nouveau_document)
        
        # Insérer les documents dans l'ordre
        if documents_a_inserer:
            result = words_collection.insert_many(documents_a_inserer)
            print(f"  ✅ {len(result.inserted_ids)} mots insérés dans l'ordre pour '{categorie}'")
            total_inseres += len(result.inserted_ids)
    
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DE LA CORRECTION D'ORDRE:")
    print(f"🔤 Total mots réorganisés: {total_inseres}")
    print(f"📂 Catégories traitées: {len(mots_par_categorie)}")
    
    # Vérification finale de l'intégrité
    print("\n🔍 Vérification de l'intégrité post-réorganisation...")
    is_healthy, message = db_protector.is_database_healthy()
    if is_healthy:
        print("✅ Base de données saine après réorganisation")
    else:
        print(f"⚠️ Problème détecté: {message}")
    
    client.close()
    return True

if __name__ == "__main__":
    print("🚀 Démarrage de la correction de l'ordre alphabétique...")
    
    # Vérifier l'état initial
    print("\n🔍 Vérification de l'état initial de la base de données...")
    is_healthy, message = db_protector.is_database_healthy()
    if not is_healthy:
        print(f"⚠️ Problème détecté avant réorganisation: {message}")
        print("🔄 Restauration recommandée avant réorganisation")
        exit(1)
    
    # Effectuer la correction
    success = corriger_ordre_alphabetique()
    
    if success:
        print("\n🎉 CORRECTION DE L'ORDRE ALPHABÉTIQUE TERMINÉE AVEC SUCCÈS!")
        print("✅ Tous les mots sont maintenant dans l'ordre alphabétique correct")
        print("✅ Les catégories nombres et grammaire suivent leur logique spécifique")
        
        # Vérification finale de l'intégrité
        print("\n🔍 Vérification finale de l'intégrité...")
        is_healthy_after, message_after = db_protector.is_database_healthy()
        if is_healthy_after:
            print("✅ Base de données saine après correction")
        else:
            print(f"⚠️ Problème détecté après correction: {message_after}")
    else:
        print("\n❌ ÉCHEC DE LA CORRECTION DE L'ORDRE ALPHABÉTIQUE")
    
    print("\nFin du script de correction de l'ordre alphabétique.")