#!/usr/bin/env python3
"""
Comparaison méthodique entre la base de données existante et le tableau du PDF
Applique uniquement les corrections nécessaires en utilisant le PDF comme source authentique
"""

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
import os
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL')
client = MongoClient(MONGO_URL)
db = client.kwezi
words_collection = db.words

# Tableau authentique extrait du PDF (source de vérité)
PDF_REFERENCE_TABLE = {
    # Cas spécifique mentionné par l'utilisateur : bigorno vs bigorneau
    "tortue": {"shimaore": "bigorno", "kibouchi": "", "action": "SUPPRIMER"},
    "bigorneau": {"shimaore": "trondro", "kibouchi": "", "action": "CONSERVER"},
    
    # Doublons d'escargot identifiés
    "escargot": {"shimaore": "kowa", "kibouchi": "", "action": "CORRIGER"},  # Garder kowa, supprimer kwa
    
    # Autres corrections orthographiques identifiées dans le PDF
    "lune": {"shimaore": "mwezi", "kibouchi": "", "correction": "mwézi -> mwezi"},
    "vent": {"shimaore": "pevo", "kibouchi": "", "correction": "pévo -> pevo"}, 
    "barrière de corail": {"shimaore": "caleni", "kibouchi": "", "correction": "caléni -> caleni"},
    "plateau": {"shimaore": "bwe", "kibouchi": "", "correction": "bwé -> bwe"},
    "rue": {"shimaore": "pare", "kibouchi": "", "correction": "paré -> pare"},
    "arbre à pain": {"shimaore": "m'frampe", "kibouchi": "", "correction": "m'frampé -> m'frampe"},
    "jacquier": {"shimaore": "m'fenesii", "kibouchi": "", "correction": "m'fénéssi -> m'fenesii"},
    "platier": {"shimaore": "kale", "kibouchi": "", "correction": "kalé -> kale"},
    "marée haute": {"shimaore": "maji yamale", "kibouchi": "", "correction": "yamalé -> yamale"},
    "sauvage": {"shimaore": "nyeha", "kibouchi": "", "correction": "nyéha -> nyeha"},
    "zébu": {"shimaore": "nyombe", "kibouchi": "", "correction": "nyombé -> nyombe"},
    "lambis": {"shimaore": "kombe", "kibouchi": "", "correction": "kombé -> kombe"},
    "épaule": {"shimaore": "bega", "kibouchi": "", "correction": "bèga -> bega"},
    "fesses": {"shimaore": "shidze", "kibouchi": "", "correction": "shidzé -> shidze"},
    "langue": {"shimaore": "oulime", "kibouchi": "", "correction": "oulimé -> oulime"},
    "cheveux": {"shimaore": "ngnele", "kibouchi": "", "correction": "ngnélé -> ngnele"},
    "barbe": {"shimaore": "ndrevou", "kibouchi": "", "correction": "ndrévou -> ndrevou"},
    "cils": {"shimaore": "kove", "kibouchi": "", "correction": "kové -> kove"},
    "Comment ça va ?": {"shimaore": "jeje", "kibouchi": "", "correction": "jéjé -> jeje"},
    "Ça va bien": {"shimaore": "fetre", "kibouchi": "", "correction": "fétré -> fetre"},
    "Tu": {"shimaore": "wawe", "kibouchi": "", "correction": "wawé -> wawe"},
    "Il/Elle": {"shimaore": "waye", "kibouchi": "", "correction": "wayé -> waye"},
    "bouc": {"shimaore": "bewe", "kibouchi": "", "correction": "béwé -> bewe"},
    "dauphin": {"shimaore": "moungoume", "kibouchi": "", "correction": "moungoumé -> moungoume"},
    
    # Différenciation des traductions similaires
    "oursin": {"shimaore": "gadzassi ya bahari", "kibouchi": "", "action": "DIFFERENCIER"},
    "huître": {"shimaore": "gadzassi ya mshindi", "kibouchi": "", "action": "DIFFERENCIER"},
    "sourcil": {"shimaore": "tsi la matso", "kibouchi": "", "action": "DIFFERENCIER"},
    
    # Traductions Kibouchi identifiées dans le PDF
    "pente": {"shimaore": "mlima", "kibouchi": "boungou", "action": "AJOUTER_KIBOUCHI"},
    "canne à sucre": {"shimaore": "mouwoi", "kibouchi": "fandzava", "action": "AJOUTER_KIBOUCHI"}, 
    "école": {"shimaore": "licoli", "kibouchi": "lakintagna", "action": "AJOUTER_KIBOUCHI"},
    "herbe": {"shimaore": "bandra", "kibouchi": "fasigni", "action": "AJOUTER_KIBOUCHI"},
    "rivière": {"shimaore": "mouro", "kibouchi": "houndza", "action": "AJOUTER_KIBOUCHI"},
    "fagot": {"shimaore": "kouni", "kibouchi": "tsikou", "action": "AJOUTER_KIBOUCHI"},
    "plateau": {"shimaore": "bwe", "kibouchi": "mahalelini", "action": "AJOUTER_KIBOUCHI"},
    "cocotier": {"shimaore": "m'nadzi", "kibouchi": "honkou", "action": "AJOUTER_KIBOUCHI"},
    "corail": {"shimaore": "soiyi", "kibouchi": "soiyi", "action": "AJOUTER_KIBOUCHI"},
    "barrière de corail": {"shimaore": "caleni", "kibouchi": "caleni", "action": "AJOUTER_KIBOUCHI"},
    "pont": {"shimaore": "daradja", "kibouchi": "daradja", "action": "AJOUTER_KIBOUCHI"},
    "nuage": {"shimaore": "wingou", "kibouchi": "vingou", "action": "AJOUTER_KIBOUCHI"},
    "arc-en-ciel": {"shimaore": "mcacamba", "kibouchi": "atihala", "action": "AJOUTER_KIBOUCHI"},
    "caillou": {"shimaore": "malavouni", "kibouchi": "vatou", "action": "AJOUTER_KIBOUCHI"},
    "chemin": {"shimaore": "ndzia", "kibouchi": "ketraka", "action": "AJOUTER_KIBOUCHI"},
    "fleur": {"shimaore": "malavou", "kibouchi": "lalagna", "action": "AJOUTER_KIBOUCHI"},
    "soleil": {"shimaore": "jouwa", "kibouchi": "haitri", "action": "AJOUTER_KIBOUCHI"},
    "mer": {"shimaore": "bahari", "kibouchi": "bahari", "action": "AJOUTER_KIBOUCHI"},
    "plage": {"shimaore": "mtsangani", "kibouchi": "fassigni", "action": "AJOUTER_KIBOUCHI"},
    "arbre": {"shimaore": "mwiri", "kibouchi": "kakazou", "action": "AJOUTER_KIBOUCHI"},
}

def analyze_current_database():
    """Analyse l'état actuel de la base de données"""
    print("🔍 ANALYSE DE LA BASE DE DONNÉES ACTUELLE")
    print("=" * 50)
    
    total_words = words_collection.count_documents({})
    print(f"Total des mots dans la base: {total_words}")
    
    categories = words_collection.distinct("category")
    print(f"Catégories: {len(categories)} - {', '.join(sorted(categories))}")
    
    # Couverture des traductions
    with_shimaore = words_collection.count_documents({"shimaore": {"$ne": ""}})
    with_kibouchi = words_collection.count_documents({"kibouchi": {"$ne": ""}})
    
    print(f"Mots avec shimaoré: {with_shimaore}/{total_words}")
    print(f"Mots avec kibouchi: {with_kibouchi}/{total_words}")
    
    return {
        'total': total_words,
        'categories': categories,
        'with_shimaore': with_shimaore,
        'with_kibouchi': with_kibouchi
    }

def compare_word_with_pdf(french_word, pdf_data):
    """Compare un mot de la base avec les données du PDF"""
    db_words = list(words_collection.find({"french": french_word}))
    
    if not db_words:
        return f"MANQUANT: '{french_word}' non trouvé dans la base"
    
    issues = []
    
    for db_word in db_words:
        db_shimaore = db_word.get('shimaore', '')
        db_kibouchi = db_word.get('kibouchi', '')
        
        # Vérifier shimaoré
        if pdf_data['shimaore'] and db_shimaore != pdf_data['shimaore']:
            issues.append(f"SHIMAORÉ DIFFÉRENT: DB='{db_shimaore}' vs PDF='{pdf_data['shimaore']}'")
        
        # Vérifier kibouchi si présent dans le PDF
        if pdf_data['kibouchi'] and db_kibouchi != pdf_data['kibouchi']:
            issues.append(f"KIBOUCHI DIFFÉRENT: DB='{db_kibouchi}' vs PDF='{pdf_data['kibouchi']}'")
    
    return issues if issues else "CONFORME"

def apply_corrections():
    """Applique les corrections identifiées en utilisant le PDF comme référence"""
    print("\n🔧 APPLICATION DES CORRECTIONS")
    print("=" * 50)
    
    corrections_applied = 0
    
    for french_word, pdf_data in PDF_REFERENCE_TABLE.items():
        action = pdf_data.get('action', 'CORRIGER')
        
        if action == "SUPPRIMER":
            # Supprimer le mot (cas tortue -> bigorno)
            deleted = words_collection.delete_many({"french": french_word, "shimaore": pdf_data['shimaore']})
            if deleted.deleted_count > 0:
                print(f"  🗑️ SUPPRIMÉ: {french_word} -> {pdf_data['shimaore']} ({deleted.deleted_count} entrées)")
                corrections_applied += 1
                
        elif action == "CONSERVER":
            # Vérifier que le mot existe bien
            existing = words_collection.find_one({"french": french_word})
            if existing:
                print(f"  ✅ CONFIRMÉ: {french_word} -> {existing.get('shimaore', '')}")
            else:
                print(f"  ❌ MANQUANT: {french_word} devrait exister")
                
        elif action == "CORRIGER":
            # Corriger la traduction
            db_words = list(words_collection.find({"french": french_word}))
            for word in db_words:
                if word.get('shimaore') != pdf_data['shimaore']:
                    words_collection.update_one(
                        {"_id": word["_id"]},
                        {"$set": {"shimaore": pdf_data['shimaore']}}
                    )
                    print(f"  📝 CORRIGÉ: {french_word} shimaoré -> '{pdf_data['shimaore']}'")
                    corrections_applied += 1
                    
        elif action == "AJOUTER_KIBOUCHI":
            # Ajouter ou corriger la traduction kibouchi
            db_word = words_collection.find_one({"french": french_word})
            if db_word:
                updates = {}
                if pdf_data['shimaore'] and db_word.get('shimaore') != pdf_data['shimaore']:
                    updates['shimaore'] = pdf_data['shimaore']
                if pdf_data['kibouchi'] and db_word.get('kibouchi') != pdf_data['kibouchi']:
                    updates['kibouchi'] = pdf_data['kibouchi']
                
                if updates:
                    words_collection.update_one(
                        {"_id": db_word["_id"]},
                        {"$set": updates}
                    )
                    print(f"  🔄 MIS À JOUR: {french_word} -> {updates}")
                    corrections_applied += 1
                    
        elif action == "DIFFERENCIER":
            # Différencier les traductions similaires
            db_word = words_collection.find_one({"french": french_word})
            if db_word and db_word.get('shimaore') != pdf_data['shimaore']:
                words_collection.update_one(
                    {"_id": db_word["_id"]},
                    {"$set": {"shimaore": pdf_data['shimaore']}}
                )
                print(f"  🔀 DIFFÉRENCIÉ: {french_word} -> '{pdf_data['shimaore']}'")
                corrections_applied += 1
    
    print(f"\n📊 CORRECTIONS APPLIQUÉES: {corrections_applied}")
    return corrections_applied

def generate_comparison_report():
    """Génère un rapport de comparaison détaillé"""
    print("\n📊 RAPPORT DE COMPARAISON BASE DE DONNÉES vs PDF")
    print("=" * 60)
    
    conforming_words = 0
    total_checked = 0
    
    for french_word, pdf_data in PDF_REFERENCE_TABLE.items():
        total_checked += 1
        comparison_result = compare_word_with_pdf(french_word, pdf_data)
        
        if comparison_result == "CONFORME":
            conforming_words += 1
            print(f"✅ {french_word}: CONFORME")
        else:
            print(f"❌ {french_word}: {comparison_result}")
    
    conformity_rate = (conforming_words / total_checked * 100) if total_checked > 0 else 0
    print(f"\n📈 TAUX DE CONFORMITÉ: {conforming_words}/{total_checked} ({conformity_rate:.1f}%)")
    
    return {
        'total_checked': total_checked,
        'conforming': conforming_words,
        'conformity_rate': conformity_rate
    }

def main():
    """Fonction principale de comparaison et correction"""
    print("🔍 COMPARAISON BASE DE DONNÉES vs TABLEAU PDF")
    print("=" * 60)
    print(f"Source authentique: PDF vocabulaire shimaoré-kibouchi")
    print(f"Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. Analyser l'état actuel
        db_stats = analyze_current_database()
        
        # 2. Générer rapport de comparaison
        comparison_stats = generate_comparison_report()
        
        # 3. Appliquer les corrections nécessaires
        corrections_count = apply_corrections()
        
        # 4. Rapport final
        print(f"\n✅ COMPARAISON ET CORRECTIONS TERMINÉES")
        print(f"  - Mots dans la base: {db_stats['total']}")
        print(f"  - Mots vérifiés: {comparison_stats['total_checked']}")
        print(f"  - Corrections appliquées: {corrections_count}")
        print(f"  - Taux de conformité final: {comparison_stats['conformity_rate']:.1f}%")
        
    except Exception as e:
        print(f"❌ ERREUR: {str(e)}")
        raise

if __name__ == "__main__":
    main()