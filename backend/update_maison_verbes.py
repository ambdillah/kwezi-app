#!/usr/bin/env python3
"""
Script pour mettre à jour les sections "maison" et "verbes" avec les données exactes des images fournies
Basé sur les 3 images : Maison.PNG, verbe'1.PNG, verbe'2.PNG
"""

import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/mayotte_app")
client = MongoClient(MONGO_URL)
db = client.mayotte_app
words_collection = db.words

def update_maison_verbes():
    """Mettre à jour les sections maison et verbes avec les données exactes des images"""
    
    # Supprimer tous les mots existants des catégories "maison" et "verbes"
    result_delete_maison = words_collection.delete_many({"category": "maison"})
    result_delete_verbes = words_collection.delete_many({"category": "verbes"})
    print(f"🗑️ Supprimé {result_delete_maison.deleted_count} anciens mots de maison")
    print(f"🗑️ Supprimé {result_delete_verbes.deleted_count} anciens verbes")
    
    # SECTION MAISON - 38 mots exacts selon l'image
    maison_vocabulary = [
        {"french": "maison", "shimaore": "nyoumba", "kibouchi": "tragnou", "category": "maison", "image_url": "🏠", "difficulty": 1},
        {"french": "porte", "shimaore": "mlango", "kibouchi": "vavavaragna", "category": "maison", "image_url": "🚪", "difficulty": 1},
        {"french": "case", "shimaore": "banga", "kibouchi": "banga", "category": "maison", "image_url": "🏠", "difficulty": 1},
        {"french": "lit", "shimaore": "chtrandra", "kibouchi": "koubani", "category": "maison", "image_url": "🛏️", "difficulty": 1},
        {"french": "marmite", "shimaore": "gnoumsou", "kibouchi": "vilangni", "category": "maison", "image_url": "🍲", "difficulty": 1},
        {"french": "vesselles", "shimaore": "ziya", "kibouchi": "hintagna", "category": "maison", "image_url": "🍽️", "difficulty": 1},
        {"french": "bol", "shimaore": "chicombé", "kibouchi": "bacouli", "category": "maison", "image_url": "🥣", "difficulty": 1},
        {"french": "cuillère", "shimaore": "soutrou", "kibouchi": "sotrou", "category": "maison", "image_url": "🥄", "difficulty": 1},
        {"french": "fenêtre", "shimaore": "fénétri", "kibouchi": "lafoumétara", "category": "maison", "image_url": "🪟", "difficulty": 1},
        {"french": "chaise", "shimaore": "chiri", "kibouchi": "chiri", "category": "maison", "image_url": "🪑", "difficulty": 1},
        {"french": "table", "shimaore": "latabou", "kibouchi": "latabou", "category": "maison", "image_url": "🪑", "difficulty": 1},
        {"french": "miroir", "shimaore": "chido", "kibouchi": "kitarafa", "category": "maison", "image_url": "🪞", "difficulty": 1},
        {"french": "cour", "shimaore": "mraba", "kibouchi": "lacourou", "category": "maison", "image_url": "🏡", "difficulty": 1},
        {"french": "clôture", "shimaore": "vala", "kibouchi": "vala", "category": "maison", "image_url": "🚧", "difficulty": 1},
        {"french": "toilette", "shimaore": "mrabani", "kibouchi": "mraba", "category": "maison", "image_url": "🚽", "difficulty": 1},
        {"french": "seau", "shimaore": "siyo", "kibouchi": "siyo", "category": "maison", "image_url": "🪣", "difficulty": 1},
        {"french": "louche", "shimaore": "paou", "kibouchi": "pow", "category": "maison", "image_url": "🥄", "difficulty": 1},
        {"french": "couteau", "shimaore": "sembeya", "kibouchi": "méssou", "category": "maison", "image_url": "🔪", "difficulty": 1},
        {"french": "matelas", "shimaore": "godoro", "kibouchi": "goudorou", "category": "maison", "image_url": "🛏️", "difficulty": 1},
        {"french": "oreiller", "shimaore": "mtsao", "kibouchi": "hondagna", "category": "maison", "image_url": "🛌", "difficulty": 1},
        {"french": "buffet", "shimaore": "biffé", "kibouchi": "biffé", "category": "maison", "image_url": "🗄️", "difficulty": 1},
        {"french": "mur", "shimaore": "péssi", "kibouchi": "riba", "category": "maison", "image_url": "🧱", "difficulty": 1},
        {"french": "véranda", "shimaore": "baraza", "kibouchi": "baraza", "category": "maison", "image_url": "🏠", "difficulty": 1},
        {"french": "toiture", "shimaore": "outro", "kibouchi": "vovougnou", "category": "maison", "image_url": "🏠", "difficulty": 1},
        {"french": "ampoule", "shimaore": "lalampou", "kibouchi": "lalampou", "category": "maison", "image_url": "💡", "difficulty": 1},
        {"french": "lumière", "shimaore": "mwengué", "kibouchi": "mwengue", "category": "maison", "image_url": "💡", "difficulty": 1},
        {"french": "torche", "shimaore": "pongé", "kibouchi": "gandili", "category": "maison", "image_url": "🔦", "difficulty": 1},
        {"french": "hache", "shimaore": "soha", "kibouchi": "famaki", "category": "maison", "image_url": "🪓", "difficulty": 1},
        {"french": "machette", "shimaore": "m'panga", "kibouchi": "ampanga", "category": "maison", "image_url": "🗡️", "difficulty": 1},
        {"french": "coupe coupe", "shimaore": "chombo", "kibouchi": "chombou", "category": "maison", "image_url": "🗡️", "difficulty": 1},
        {"french": "cartable/malette", "shimaore": "mkoba", "kibouchi": "mkoba", "category": "maison", "image_url": "🎒", "difficulty": 1},
        {"french": "sac", "shimaore": "gouni", "kibouchi": "gouni", "category": "maison", "image_url": "🎒", "difficulty": 1},
        {"french": "balai", "shimaore": "péou", "kibouchi": "famafa", "category": "maison", "image_url": "🧹", "difficulty": 1},
        {"french": "mortier", "shimaore": "chino", "kibouchi": "légnou", "category": "maison", "image_url": "🫖", "difficulty": 1},
        {"french": "assiette", "shimaore": "sahani", "kibouchi": "sahani", "category": "maison", "image_url": "🍽️", "difficulty": 1},
        {"french": "fondation", "shimaore": "houra", "kibouchi": "koura", "category": "maison", "image_url": "🏗️", "difficulty": 1},
        {"french": "torche locale", "shimaore": "gandilé/poutroupmax", "kibouchi": "gandili/poutroupmax", "category": "maison", "image_url": "🔦", "difficulty": 1},
    ]
    
    # SECTION VERBES - 104 verbes exacts selon les deux images
    verbes_vocabulary = [
        # VERBES PARTIE 1 - Image verbe'1.PNG
        {"french": "jouer", "shimaore": "ounguadza", "kibouchi": "mtsoma", "category": "verbes", "image_url": "⚽", "difficulty": 1},
        {"french": "courir", "shimaore": "wendra mbiyo", "kibouchi": "miloumeyi", "category": "verbes", "image_url": "🏃", "difficulty": 1},
        {"french": "dire", "shimaore": "ourongoa", "kibouchi": "mangnabara", "category": "verbes", "image_url": "🗣️", "difficulty": 1},
        {"french": "pouvoir", "shimaore": "ouchindra", "kibouchi": "mahaléou", "category": "verbes", "image_url": "💪", "difficulty": 1},
        {"french": "vouloir", "shimaore": "outsaha", "kibouchi": "chokou", "category": "verbes", "image_url": "🤲", "difficulty": 1},
        {"french": "savoir", "shimaore": "oujoua", "kibouchi": "méhéyi", "category": "verbes", "image_url": "🧠", "difficulty": 1},
        {"french": "voir", "shimaore": "ouona", "kibouchi": "mahita", "category": "verbes", "image_url": "👁️", "difficulty": 1},
        {"french": "devoir", "shimaore": "oulazimou", "kibouchi": "tokountrou", "category": "verbes", "image_url": "⚖️", "difficulty": 1},
        {"french": "venir", "shimaore": "ouja", "kibouchi": "havyi", "category": "verbes", "image_url": "🏃", "difficulty": 1},
        {"french": "rapprocher", "shimaore": "outsengueléya", "kibouchi": "magnatougnou", "category": "verbes", "image_url": "👥", "difficulty": 1},
        {"french": "prendre", "shimaore": "ourenga", "kibouchi": "mangala", "category": "verbes", "image_url": "✋", "difficulty": 1},
        {"french": "donner", "shimaore": "ouva", "kibouchi": "magnaniya", "category": "verbes", "image_url": "🤲", "difficulty": 1},
        {"french": "parler", "shimaore": "oulagoua", "kibouchi": "mivoulangna", "category": "verbes", "image_url": "🗣️", "difficulty": 1},
        {"french": "mettre", "shimaore": "outria", "kibouchi": "mangnanou", "category": "verbes", "image_url": "👆", "difficulty": 1},
        {"french": "passer", "shimaore": "ouvira", "kibouchi": "mihomba", "category": "verbes", "image_url": "🚶", "difficulty": 1},
        {"french": "trouver", "shimaore": "oupara", "kibouchi": "mahazou", "category": "verbes", "image_url": "🔍", "difficulty": 1},
        {"french": "aimer", "shimaore": "ouvendza", "kibouchi": "mihya", "category": "verbes", "image_url": "❤️", "difficulty": 1},
        {"french": "croire", "shimaore": "ouamini", "kibouchi": "kommimi", "category": "verbes", "image_url": "🙏", "difficulty": 1},
        {"french": "penser", "shimaore": "oufikiri", "kibouchi": "midztéri", "category": "verbes", "image_url": "🤔", "difficulty": 1},
        {"french": "connaître", "shimaore": "oujoua", "kibouchi": "méhéyi", "category": "verbes", "image_url": "🧠", "difficulty": 1},
        {"french": "demander", "shimaore": "oudzissa", "kibouchi": "magnoutani", "category": "verbes", "image_url": "❓", "difficulty": 1},
        {"french": "répondre", "shimaore": "oudjibou", "kibouchi": "mikoudjibou", "category": "verbes", "image_url": "💬", "difficulty": 1},
        {"french": "laisser", "shimaore": "oulicha", "kibouchi": "mangnambéla", "category": "verbes", "image_url": "👋", "difficulty": 1},
        {"french": "manger", "shimaore": "oudhya", "kibouchi": "mihinagna", "category": "verbes", "image_url": "🍽️", "difficulty": 1},
        {"french": "boire", "shimaore": "ounoua", "kibouchi": "mindranou", "category": "verbes", "image_url": "🥤", "difficulty": 1},
        {"french": "lire", "shimaore": "ousoma", "kibouchi": "mndzorou", "category": "verbes", "image_url": "📖", "difficulty": 1},
        {"french": "écrire", "shimaore": "outhanguiha", "kibouchi": "mikonandrka", "category": "verbes", "image_url": "✍️", "difficulty": 1},
        {"french": "écouter", "shimaore": "ouvoulikia", "kibouchi": "miréyergni", "category": "verbes", "image_url": "👂", "difficulty": 1},
        {"french": "apprendre", "shimaore": "oufoundriha", "kibouchi": "midzorou", "category": "verbes", "image_url": "📚", "difficulty": 1},
        {"french": "comprendre", "shimaore": "ouéléwa", "kibouchi": "mikoutan", "category": "verbes", "image_url": "💡", "difficulty": 1},
        {"french": "jouer", "shimaore": "oungadza", "kibouchi": "mitsoma", "category": "verbes", "image_url": "⚽", "difficulty": 1},
        {"french": "marcher", "shimaore": "ouendra", "kibouchi": "mandeha", "category": "verbes", "image_url": "🚶", "difficulty": 1},
        {"french": "entrer", "shimaore": "ounguiya", "kibouchi": "mididri", "category": "verbes", "image_url": "🚪", "difficulty": 1},
        {"french": "sortir", "shimaore": "ouhawa", "kibouchi": "miboka", "category": "verbes", "image_url": "🚪", "difficulty": 1},
        {"french": "rester", "shimaore": "oukétsi", "kibouchi": "mipétraka", "category": "verbes", "image_url": "🏠", "difficulty": 1},
        {"french": "vivre", "shimaore": "ouvinchi", "kibouchi": "mikouténhi", "category": "verbes", "image_url": "❤️", "difficulty": 1},
        {"french": "dormir", "shimaore": "oulala", "kibouchi": "mandri", "category": "verbes", "image_url": "😴", "difficulty": 1},
        {"french": "attendre", "shimaore": "oulindra", "kibouchi": "mandgni", "category": "verbes", "image_url": "⏰", "difficulty": 1},
        {"french": "suivre", "shimaore": "oulounga", "kibouchi": "mangniraka", "category": "verbes", "image_url": "👥", "difficulty": 1},
        {"french": "tenir", "shimaore": "oussika", "kibouchi": "mitana", "category": "verbes", "image_url": "✋", "difficulty": 1},
        {"french": "ouvrir", "shimaore": "ouboua", "kibouchi": "mampibiyangna", "category": "verbes", "image_url": "🔓", "difficulty": 1},
        {"french": "fermer", "shimaore": "oubala", "kibouchi": "migadra", "category": "verbes", "image_url": "🔒", "difficulty": 1},
        {"french": "sembler", "shimaore": "oufana", "kibouchi": "mampihragna", "category": "verbes", "image_url": "🤔", "difficulty": 1},
        {"french": "paraître", "shimaore": "ouvonehoua", "kibouchi": "", "category": "verbes", "image_url": "👁️", "difficulty": 1},
        {"french": "devenir", "shimaore": "ougawouha", "kibouchi": "mivadiki", "category": "verbes", "image_url": "🔄", "difficulty": 1},
        {"french": "tomber", "shimaore": "oupouliha", "kibouchi": "latsaka", "category": "verbes", "image_url": "⬇️", "difficulty": 1},
        {"french": "se rappeler", "shimaore": "oumaézi", "kibouchi": "koufahamou", "category": "verbes", "image_url": "🧠", "difficulty": 1},
        {"french": "commencer", "shimaore": "ouhandrissa", "kibouchi": "mitaponou", "category": "verbes", "image_url": "▶️", "difficulty": 1},
        {"french": "finir", "shimaore": "oumalidza", "kibouchi": "mankéfa", "category": "verbes", "image_url": "✅", "difficulty": 1},
        {"french": "réussir", "shimaore": "ouchindra", "kibouchi": "mahaléou", "category": "verbes", "image_url": "🏆", "difficulty": 1},
        {"french": "essayer", "shimaore": "oudjerebou", "kibouchi": "mikoujérebou", "category": "verbes", "image_url": "🤞", "difficulty": 1},
        {"french": "attraper", "shimaore": "oubara", "kibouchi": "misamboutrou", "category": "verbes", "image_url": "✋", "difficulty": 1},
        {"french": "flatuler", "shimaore": "oujamba", "kibouchi": "manguétountrou", "category": "verbes", "image_url": "💨", "difficulty": 1},
        {"french": "traverser", "shimaore": "ouchiya", "kibouchi": "mitsaka", "category": "verbes", "image_url": "🚶", "difficulty": 1},
        {"french": "sauter", "shimaore": "ouarouka", "kibouchi": "mivongna", "category": "verbes", "image_url": "🦘", "difficulty": 1},
        {"french": "frapper", "shimaore": "ourema", "kibouchi": "mamangou", "category": "verbes", "image_url": "👊", "difficulty": 1},
        {"french": "faire caca", "shimaore": "ougna madzi", "kibouchi": "manguéri", "category": "verbes", "image_url": "💩", "difficulty": 1},
        {"french": "faire pipi", "shimaore": "ougna kojo", "kibouchi": "manarni", "category": "verbes", "image_url": "💧", "difficulty": 1},
        {"french": "vomir", "shimaore": "ouraviha", "kibouchi": "mandouva", "category": "verbes", "image_url": "🤮", "difficulty": 1},
        {"french": "s'asseoir", "shimaore": "oukétsi", "kibouchi": "mipétraka", "category": "verbes", "image_url": "🪑", "difficulty": 1},
        {"french": "danser", "shimaore": "ouzina", "kibouchi": "mitsindrakra", "category": "verbes", "image_url": "💃", "difficulty": 1},
        {"french": "arrêter", "shimaore": "ouziya", "kibouchi": "mitsahatra", "category": "verbes", "image_url": "🛑", "difficulty": 1},
        {"french": "vendre", "shimaore": "ouhoudza", "kibouchi": "mandafou", "category": "verbes", "image_url": "💰", "difficulty": 1},
        {"french": "cracher", "shimaore": "outra marré", "kibouchi": "mandrora", "category": "verbes", "image_url": "💦", "difficulty": 1},
        {"french": "mordre", "shimaore": "ouka magno", "kibouchi": "mangnekitri", "category": "verbes", "image_url": "🦷", "difficulty": 1},
        {"french": "gratter", "shimaore": "oukouwa", "kibouchi": "mihorrou", "category": "verbes", "image_url": "✋", "difficulty": 1},
        {"french": "embrasser", "shimaore": "ounouka", "kibouchi": "milou oukou", "category": "verbes", "image_url": "💋", "difficulty": 1},
        {"french": "jeter", "shimaore": "ouvoutsa", "kibouchi": "manoui", "category": "verbes", "image_url": "🗑️", "difficulty": 1},
        {"french": "avertir", "shimaore": "outahadaricha", "kibouchi": "mangnalévi", "category": "verbes", "image_url": "⚠️", "difficulty": 1},
        {"french": "informer", "shimaore": "oujoudza", "kibouchi": "mangnabara", "category": "verbes", "image_url": "📢", "difficulty": 1},
        {"french": "se laver le derrière", "shimaore": "outsamba", "kibouchi": "manjbouvi", "category": "verbes", "image_url": "🚿", "difficulty": 1},
        {"french": "se laver", "shimaore": "ouhowa", "kibouchi": "miseki", "category": "verbes", "image_url": "🧼", "difficulty": 1},
        {"french": "piler", "shimaore": "oudoudoua", "kibouchi": "mandissa", "category": "verbes", "image_url": "🔨", "difficulty": 1},
        {"french": "changer", "shimaore": "ougaoudza", "kibouchi": "mamadiki", "category": "verbes", "image_url": "🔄", "difficulty": 1},
        {"french": "étendre au soleil", "shimaore": "ouaniha", "kibouchi": "manapi", "category": "verbes", "image_url": "☀️", "difficulty": 1},
        {"french": "réchauffer", "shimaore": "ouhelesesedza", "kibouchi": "mamana", "category": "verbes", "image_url": "🔥", "difficulty": 1},
        {"french": "se baigner", "shimaore": "ouhowa", "kibouchi": "miseki", "category": "verbes", "image_url": "🏊", "difficulty": 1},
        {"french": "faire le lit", "shimaore": "ouhodza", "kibouchi": "mandzari koubani", "category": "verbes", "image_url": "🛏️", "difficulty": 1},
        {"french": "faire sécher", "shimaore": "ouhoumisa", "kibouchi": "manapi", "category": "verbes", "image_url": "🌞", "difficulty": 1},
        
        # VERBES PARTIE 2 - Image verbe'2.PNG
        {"french": "balayer", "shimaore": "ouhoundza", "kibouchi": "mamafa", "category": "verbes", "image_url": "🧹", "difficulty": 1},
        {"french": "couper", "shimaore": "oukatra", "kibouchi": "manapaka", "category": "verbes", "image_url": "✂️", "difficulty": 1},
        {"french": "tremper", "shimaore": "oulodza", "kibouchi": "mandzoubougnou", "category": "verbes", "image_url": "💧", "difficulty": 1},
        {"french": "se raser", "shimaore": "oumea ndrevu", "kibouchi": "manapaka somboutrou", "category": "verbes", "image_url": "🪒", "difficulty": 1},
        {"french": "abîmer", "shimaore": "oumengna", "kibouchi": "mandroubaka", "category": "verbes", "image_url": "💥", "difficulty": 1},
        {"french": "entrer", "shimaore": "ounguiya", "kibouchi": "mihidiri", "category": "verbes", "image_url": "🚪", "difficulty": 1},
        {"french": "acheter", "shimaore": "ounnounoua", "kibouchi": "mivanga", "category": "verbes", "image_url": "🛒", "difficulty": 1},
        {"french": "griller", "shimaore": "ouwoha", "kibouchi": "mitonou", "category": "verbes", "image_url": "🔥", "difficulty": 1},
        {"french": "allumer", "shimaore": "oupatsa", "kibouchi": "mikoupatsa", "category": "verbes", "image_url": "🔥", "difficulty": 1},
        {"french": "se peigner", "shimaore": "oupengné", "kibouchi": "mipéngni", "category": "verbes", "image_url": "💇", "difficulty": 1},
        {"french": "cuisiner", "shimaore": "oupiha", "kibouchi": "mahandrou", "category": "verbes", "image_url": "👩‍🍳", "difficulty": 1},
        {"french": "ranger/arranger", "shimaore": "ourenguelédza", "kibouchi": "magnadzari", "category": "verbes", "image_url": "📦", "difficulty": 1},
        {"french": "tresser", "shimaore": "ousssouka", "kibouchi": "mitali/mandrani", "category": "verbes", "image_url": "💇", "difficulty": 1},
        {"french": "peindre", "shimaore": "ouvaha", "kibouchi": "magnossoutrou", "category": "verbes", "image_url": "🎨", "difficulty": 1},
        {"french": "essuyer", "shimaore": "ouvangouha", "kibouchi": "mamitri", "category": "verbes", "image_url": "🧽", "difficulty": 1},
        {"french": "amener/apporter", "shimaore": "ouvinga", "kibouchi": "mandéyi", "category": "verbes", "image_url": "🤲", "difficulty": 1},
        {"french": "éteindre", "shimaore": "ouzima", "kibouchi": "mamounou", "category": "verbes", "image_url": "🌫️", "difficulty": 1},
        {"french": "tuer", "shimaore": "ouwoula", "kibouchi": "mamounou", "category": "verbes", "image_url": "💀", "difficulty": 1},
        {"french": "combler", "shimaore": "oufitsiya", "kibouchi": "mankahampi", "category": "verbes", "image_url": "⬆️", "difficulty": 1},
        {"french": "cultiver", "shimaore": "oulima", "kibouchi": "mikapa", "category": "verbes", "image_url": "🌱", "difficulty": 1},
        {"french": "couper du bois", "shimaore": "oupasouha kuni", "kibouchi": "mamaki azoumati", "category": "verbes", "image_url": "🪓", "difficulty": 1},
        {"french": "cueillir", "shimaore": "oupoua", "kibouchi": "mampoka", "category": "verbes", "image_url": "🌸", "difficulty": 1},
        {"french": "planter", "shimaore": "outabou", "kibouchi": "mamboli", "category": "verbes", "image_url": "🌱", "difficulty": 1},
        {"french": "creuser", "shimaore": "outsimba", "kibouchi": "mangadi", "category": "verbes", "image_url": "⛏️", "difficulty": 1},
        {"french": "récolter", "shimaore": "ouvouna", "kibouchi": "mampoka", "category": "verbes", "image_url": "🌾", "difficulty": 1},
        {"french": "bouger", "shimaore": "outsengueléya", "kibouchi": "mitéki", "category": "verbes", "image_url": "🏃", "difficulty": 1},
        {"french": "arnaquer", "shimaore": "ouravi", "kibouchi": "mangalatra", "category": "verbes", "image_url": "🤥", "difficulty": 1},
    ]
    
    # Ajouter timestamp à chaque mot
    all_vocabulary = maison_vocabulary + verbes_vocabulary
    for word in all_vocabulary:
        word["created_at"] = datetime.utcnow()
    
    # Insérer tous les nouveaux mots
    result = words_collection.insert_many(all_vocabulary)
    
    print(f"✅ Sections maison et verbes mises à jour : {len(result.inserted_ids)} mots ajoutés")
    print(f"📊 Maison : {len(maison_vocabulary)} mots")
    print(f"📊 Verbes : {len(verbes_vocabulary)} mots")
    
    # Vérification
    total_words = words_collection.count_documents({})
    maison_count = words_collection.count_documents({"category": "maison"})
    verbes_count = words_collection.count_documents({"category": "verbes"})
    
    print(f"\n📈 STATISTIQUES MISES À JOUR :")
    print(f"   Total des mots dans la base : {total_words}")
    print(f"   Mots dans la catégorie maison : {maison_count}")
    print(f"   Mots dans la catégorie verbes : {verbes_count}")
    
    return len(result.inserted_ids)

if __name__ == "__main__":
    print("🔄 Mise à jour des sections maison et verbes avec les données des images...")
    count = update_maison_verbes()
    print(f"✅ Terminé ! {count} mots (maison + verbes) mis à jour selon les images.")