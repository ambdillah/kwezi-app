#!/usr/bin/env python3
"""
ORGANISATION ET NETTOYAGE COMPLET DE LA BASE DE DONNÉES
======================================================
1. Tri alphabétique par catégorie (sauf nombres et grammaire)
2. Suppression d'emojis spécifiques
3. Correction des fautes d'orthographe françaises
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
    "papaye", "vagin", "pénis", "fesses", "fruit du jacquier", 
    "terre", "sol", "platier", "fondation",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"
]

# Corrections d'orthographe françaises communes
CORRECTIONS_ORTHOGRAPHE = {
    # Corrections d'accents
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
    "cote": "côte",
    "gouter": "goûter",
    "ou": "où",
    "ca": "ça",
    "deja": "déjà",
    "priere": "prière",
    "riviere": "rivière",
    "premiere": "première",
    "derniere": "dernière",
    "lumiere": "lumière",
    "matiere": "matière",
    "epoux": "époux",
    "epouse": "épouse",
    
    # Corrections de cédilles
    "garcon": "garçon",
    "francais": "français",
    "lecon": "leçon",
    "recue": "reçue",
    "apercu": "aperçu",
    
    # Corrections de doubles consonnes
    "adresse": "adresse",
    "appareil": "appareil", 
    "apposer": "apposer",
    "arreter": "arrêter",
    "attendre": "attendre",
    "difficile": "difficile",
    "intelligent": "intelligent",
    "interessant": "intéressant",
    "necessite": "nécessité",
    "occassion": "occasion",
    "professionel": "professionnel",
    "recomander": "recommander",
    "developper": "développer",
    
    # Corrections diverses
    "language": "langage",
    "orthographe": "orthographe",
    "rythme": "rythme",
    "sympatique": "sympathique",
    "exercise": "exercice",
    "exemple": "exemple",
    "explication": "explication",
    "definition": "définition",
    
    # Corrections spécifiques courantes
    "apartement": "appartement",
    "apartenir": "appartenir",
    "asseoir": "s'asseoir",
    "comencer": "commencer",
    "coment": "comment",
    "diferent": "différent",
    "enfin": "enfin",
    "environ": "environ",
    "examen": "examen",
    "famile": "famille",
    "interesant": "intéressant",
    "language": "langage",
    "longtemp": "longtemps",
    "mariage": "mariage",
    "marriage": "mariage",
    "mieu": "mieux",
    "milieu": "milieu",
    "nouvele": "nouvelle",
    "oportunite": "opportunité",
    "parler": "parler",
    "particulier": "particulier",
    "peut-etre": "peut-être",
    "plusieures": "plusieurs",
    "prendre": "prendre",
    "probablement": "probablement",
    "quelque chose": "quelque chose",
    "receuil": "recueil",
    "reconaitre": "reconnaître",
    "rendez-vous": "rendez-vous",
    "reussir": "réussir",
    "souvent": "souvent",
    "temp": "temps",
    "toujour": "toujours",
    "travail": "travail",
    "vraiment": "vraiment"
}

# Ordre logique pour la grammaire
ORDRE_GRAMMAIRE = [
    "je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
    "moi", "toi", "lui", "elle", "nous", "vous", "eux", "elles",
    "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses",
    "notre", "nos", "votre", "vos", "leur", "leurs",
    "le", "la", "les", "un", "une", "des",
    "ce", "cette", "ces", "cet",
    "qui", "que", "quoi", "dont", "où",
    "et", "ou", "mais", "donc", "car", "ni", "or",
    "dans", "sur", "sous", "avec", "sans", "pour", "par", "de", "du", "des"
]

def corriger_orthographe_francaise(texte):
    """Corrige l'orthographe française d'un texte"""
    if not texte:
        return texte
    
    texte_corrige = texte.lower().strip()
    
    # Appliquer les corrections d'orthographe
    for erreur, correction in CORRECTIONS_ORTHOGRAPHE.items():
        if texte_corrige == erreur.lower():
            return correction
    
    # Si pas de correction trouvée, retourner le texte original
    return texte

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

@protect_database("organize_and_clean_database")
def organiser_et_nettoyer_database():
    """Organise et nettoie la base de données complètement"""
    print("🔧 ORGANISATION ET NETTOYAGE COMPLET DE LA BASE DE DONNÉES")
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
    
    # Statistiques
    mots_corriges_orthographe = 0
    mots_emojis_supprimes = 0
    categories_triees = 0
    
    # Organiser par catégorie
    mots_par_categorie = {}
    for mot in tous_les_mots:
        categorie = mot.get('category', 'autres')
        if categorie not in mots_par_categorie:
            mots_par_categorie[categorie] = []
        mots_par_categorie[categorie].append(mot)
    
    print(f"📂 Catégories trouvées: {list(mots_par_categorie.keys())}")
    
    # Traiter chaque catégorie
    for categorie, mots in mots_par_categorie.items():
        print(f"\n🔄 Traitement de la catégorie '{categorie}' ({len(mots)} mots)...")
        
        mots_modifies = []
        
        for mot in mots:
            mot_modifie = mot.copy()
            
            # 1. Correction orthographe française
            french_original = mot.get('french', '')
            french_corrige = corriger_orthographe_francaise(french_original)
            
            if french_corrige != french_original:
                mot_modifie['french'] = french_corrige
                mots_corriges_orthographe += 1
                print(f"  📝 Orthographe: '{french_original}' → '{french_corrige}'")
            
            # 2. Suppression d'emojis spécifiques
            if french_corrige.lower() in [m.lower() for m in MOTS_SUPPRIMER_EMOJIS]:
                if mot_modifie.get('image_url') and mot_modifie['image_url'] not in ['', None]:
                    mot_modifie['image_url'] = ""
                    mots_emojis_supprimes += 1
                    print(f"  🚫 Emoji supprimé pour '{french_corrige}'")
            
            mots_modifies.append(mot_modifie)
        
        # 3. Tri selon la catégorie
        if categorie.lower() == 'nombres':
            # Tri par ordre croissant pour les nombres
            mots_modifies.sort(key=lambda x: get_sort_key_nombres(x.get('french', '')))
            print(f"  📊 Catégorie '{categorie}' triée par ordre croissant")
        elif categorie.lower() == 'grammaire':
            # Tri logique pour la grammaire
            mots_modifies.sort(key=lambda x: get_sort_key_grammaire(x.get('french', '')))
            print(f"  📚 Catégorie '{categorie}' triée par ordre logique")
        else:
            # Tri alphabétique pour toutes les autres catégories
            mots_modifies.sort(key=lambda x: x.get('french', '').lower().strip())
            print(f"  🔤 Catégorie '{categorie}' triée par ordre alphabétique")
        
        categories_triees += 1
        
        # Mettre à jour la base de données
        for mot_modifie in mots_modifies:
            words_collection.replace_one(
                {"_id": mot_modifie["_id"]},
                mot_modifie
            )
    
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DE L'ORGANISATION ET NETTOYAGE:")
    print(f"🔤 Catégories triées: {categories_triees}")
    print(f"📝 Mots avec orthographe corrigée: {mots_corriges_orthographe}")
    print(f"🚫 Emojis supprimés: {mots_emojis_supprimes}")
    print(f"📚 Total mots traités: {len(tous_les_mots)}")
    
    # Vérification finale de l'intégrité
    print("\n🔍 Vérification de l'intégrité post-organisation...")
    is_healthy, message = db_protector.is_database_healthy()
    if is_healthy:
        print("✅ Base de données saine après organisation")
    else:
        print(f"⚠️ Problème détecté: {message}")
    
    client.close()
    return True

if __name__ == "__main__":
    print("🚀 Démarrage de l'organisation et nettoyage de la base de données...")
    
    # Vérifier l'état initial
    print("\n🔍 Vérification de l'état initial de la base de données...")
    is_healthy, message = db_protector.is_database_healthy()
    if not is_healthy:
        print(f"⚠️ Problème détecté avant organisation: {message}")
        print("🔄 Restauration recommandée avant organisation")
        exit(1)
    
    # Effectuer l'organisation et le nettoyage
    success = organiser_et_nettoyer_database()
    
    if success:
        print("\n🎉 ORGANISATION ET NETTOYAGE TERMINÉS AVEC SUCCÈS!")
        print("✅ Toutes les catégories sont maintenant organisées")
        print("✅ Les emojis spécifiés ont été supprimés")
        print("✅ L'orthographe française a été corrigée")
        
        # Vérification finale de l'intégrité
        print("\n🔍 Vérification finale de l'intégrité...")
        is_healthy_after, message_after = db_protector.is_database_healthy()
        if is_healthy_after:
            print("✅ Base de données saine après organisation")
        else:
            print(f"⚠️ Problème détecté après organisation: {message_after}")
    else:
        print("\n❌ ÉCHEC DE L'ORGANISATION ET NETTOYAGE")
    
    print("\nFin du script d'organisation et nettoyage.")