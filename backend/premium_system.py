"""
Système de gestion Premium pour Kwezi
Gère les utilisateurs, abonnements et limitations
"""
from fastapi import HTTPException
from pymongo import MongoClient
from datetime import datetime, timedelta
from typing import Optional
import os

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
DB_NAME = os.getenv("DB_NAME", "mayotte_app")
db = client[DB_NAME]

users_collection = db.users
words_collection = db.words

# Configuration
FREE_WORDS_LIMIT = 250
PREMIUM_MONTHLY_PRICE = 2.90  # EUR
PREMIUM_YEARLY_PRICE = 29.00  # EUR

def create_user(user_id: str, email: Optional[str] = None):
    """Créer un nouvel utilisateur gratuit"""
    existing = users_collection.find_one({"user_id": user_id})
    if existing:
        return existing
    
    user_data = {
        "user_id": user_id,
        "email": email,
        "is_premium": False,
        "premium_expires_at": None,
        "subscription_type": None,
        "created_at": datetime.utcnow(),
        "last_login": datetime.utcnow(),
        "words_learned": 0,
        "total_score": 0,
        "streak_days": 0,
        "last_activity_date": None
    }
    
    result = users_collection.insert_one(user_data)
    user_data["_id"] = result.inserted_id
    return user_data

def get_user(user_id: str):
    """Récupérer les informations d'un utilisateur"""
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        # Créer automatiquement l'utilisateur s'il n'existe pas
        return create_user(user_id)
    
    # Vérifier si l'abonnement premium est expiré
    if user.get("is_premium") and user.get("premium_expires_at"):
        if user["premium_expires_at"] < datetime.utcnow():
            # Abonnement expiré, révoquer le premium
            users_collection.update_one(
                {"user_id": user_id},
                {"$set": {"is_premium": False}}
            )
            user["is_premium"] = False
    
    return user

def upgrade_to_premium(user_id: str, subscription_type: str = "monthly"):
    """Simuler l'achat Premium (pour tests)"""
    user = get_user(user_id)
    
    # Calculer la date d'expiration
    if subscription_type == "monthly":
        expires_at = datetime.utcnow() + timedelta(days=30)
    elif subscription_type == "yearly":
        expires_at = datetime.utcnow() + timedelta(days=365)
    else:
        raise HTTPException(status_code=400, detail="Type d'abonnement invalide")
    
    # Mettre à jour l'utilisateur
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "is_premium": True,
            "premium_expires_at": expires_at,
            "subscription_type": subscription_type,
            "last_login": datetime.utcnow()
        }}
    )
    
    updated_user = get_user(user_id)
    return updated_user

def get_words_for_user(user_id: Optional[str] = None, category: Optional[str] = None):
    """Récupérer les mots accessibles pour un utilisateur"""
    # Si pas d'user_id fourni, retourner version limitée pour invité
    is_premium = False
    if user_id:
        user = get_user(user_id)
        is_premium = user.get("is_premium", False)
    
    # Construire la requête MongoDB
    query = {}
    if category:
        query["category"] = category
    
    # Récupérer les mots
    words = list(words_collection.find(query).sort([("difficulty", 1), ("_id", 1)]))
    
    # Limiter si utilisateur gratuit
    if not is_premium:
        words = words[:FREE_WORDS_LIMIT]
    
    # Formater les résultats
    for word in words:
        word["id"] = str(word["_id"])
        del word["_id"]
    
    return {
        "words": words,
        "total": len(words),
        "is_premium": is_premium,
        "limit_reached": not is_premium and len(words) >= FREE_WORDS_LIMIT
    }

def update_user_activity(user_id: str, words_learned: int = 0, score: int = 0):
    """Mettre à jour l'activité utilisateur"""
    user = get_user(user_id)
    
    today = datetime.utcnow().date()
    last_activity = user.get("last_activity_date")
    
    # Calculer la série (streak)
    streak_days = user.get("streak_days", 0)
    if last_activity:
        last_activity_date = last_activity.date() if isinstance(last_activity, datetime) else last_activity
        days_diff = (today - last_activity_date).days
        
        if days_diff == 1:
            # Série continue
            streak_days += 1
        elif days_diff > 1:
            # Série cassée
            streak_days = 1
    else:
        # Premier jour
        streak_days = 1
    
    # Mettre à jour
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "last_activity_date": datetime.utcnow(),
            "streak_days": streak_days,
            "last_login": datetime.utcnow()
        },
        "$inc": {
            "words_learned": words_learned,
            "total_score": score
        }}
    )
    
    return get_user(user_id)

def get_user_stats(user_id: str):
    """Récupérer les statistiques d'un utilisateur"""
    user = get_user(user_id)
    
    return {
        "user_id": user["user_id"],
        "is_premium": user.get("is_premium", False),
        "premium_expires_at": user.get("premium_expires_at"),
        "words_learned": user.get("words_learned", 0),
        "total_score": user.get("total_score", 0),
        "streak_days": user.get("streak_days", 0),
        "created_at": user.get("created_at"),
        "subscription_type": user.get("subscription_type")
    }
