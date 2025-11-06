"""
Routes Stripe pour gérer les abonnements Premium
"""

import stripe
import os
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PRICE_ID = os.getenv('STRIPE_PRICE_ID_PREMIUM')

router = APIRouter(prefix="/api/stripe", tags=["stripe"])

class CheckoutRequest(BaseModel):
    user_id: str
    success_url: str
    cancel_url: str

class PortalRequest(BaseModel):
    customer_id: str
    return_url: str

@router.post("/create-checkout-session")
async def create_checkout_session(request: CheckoutRequest):
    """
    Créer une session de paiement Stripe pour l'abonnement Premium
    """
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': STRIPE_PRICE_ID,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.success_url,
            cancel_url=request.cancel_url,
            client_reference_id=request.user_id,
            metadata={
                'user_id': request.user_id
            }
        )
        
        return {
            "sessionId": checkout_session.id,
            "url": checkout_session.url
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-portal-session")
async def create_portal_session(request: PortalRequest):
    """
    Créer une session du portail client Stripe pour gérer l'abonnement
    """
    try:
        portal_session = stripe.billing_portal.Session.create(
            customer=request.customer_id,
            return_url=request.return_url,
        )
        
        return {
            "url": portal_session.url
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Webhook pour recevoir les événements Stripe
    """
    from pymongo import MongoClient
    from datetime import datetime
    from bson import ObjectId
    
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    # Configuration webhook secret (optionnel en développement, OBLIGATOIRE en production)
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    try:
        # Connexion MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
        db_name = os.getenv('DB_NAME', 'mayotte_app')
        client = MongoClient(mongo_url)
        db = client[db_name]
        users_collection = db['users']
        
        # Vérifier la signature si le secret est configuré
        if webhook_secret and sig_header:
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, webhook_secret
                )
            except stripe.error.SignatureVerificationError:
                raise HTTPException(status_code=400, detail="Invalid signature")
        else:
            # En développement : parser sans vérification
            event = stripe.Event.construct_from(
                await request.json(), stripe.api_key
            )
        
        # Gérer les différents types d'événements
        if event.type == 'checkout.session.completed':
            session = event.data.object
            user_id = session.get('client_reference_id')
            customer_id = session.get('customer')
            subscription_id = session.get('subscription')
            
            # Mettre à jour ou créer l'utilisateur dans MongoDB
            if user_id:
                result = users_collection.update_one(
                    {'user_id': user_id},
                    {
                        '$set': {
                            'is_premium': True,
                            'stripe_customer_id': customer_id,
                            'stripe_subscription_id': subscription_id,
                            'premium_since': datetime.utcnow(),
                            'updated_at': datetime.utcnow()
                        },
                        '$setOnInsert': {
                            'user_id': user_id,
                            'created_at': datetime.utcnow(),
                            'words_learned': 0,
                            'total_score': 0
                        }
                    },
                    upsert=True  # CRITIQUE: Créer l'utilisateur s'il n'existe pas
                )
                
                action = "créé et" if result.upserted_id else "mis à jour:"
                print(f"✅ Utilisateur {user_id} {action} Premium activé")
                print(f"   Customer ID: {customer_id}")
                print(f"   Subscription ID: {subscription_id}")
                print(f"   Documents modifiés/créés: {result.modified_count or 1}")
            
            return {"status": "success", "user_id": user_id}
        
        elif event.type == 'customer.subscription.updated':
            subscription = event.data.object
            customer_id = subscription.get('customer')
            subscription_status = subscription.get('status')
            
            # Trouver l'utilisateur par customer_id
            user = users_collection.find_one({'stripe_customer_id': customer_id})
            
            if user:
                # Mettre à jour le statut selon l'état de l'abonnement
                is_premium = subscription_status in ['active', 'trialing']
                
                users_collection.update_one(
                    {'_id': user['_id']},
                    {
                        '$set': {
                            'is_premium': is_premium,
                            'subscription_status': subscription_status,
                            'updated_at': datetime.utcnow()
                        }
                    }
                )
                
                print(f"✅ Abonnement mis à jour pour {user.get('user_id')}")
                print(f"   Status: {subscription_status}")
                print(f"   Premium: {is_premium}")
            
            return {"status": "updated", "subscription_status": subscription_status}
        
        elif event.type == 'customer.subscription.deleted':
            subscription = event.data.object
            customer_id = subscription.get('customer')
            
            # Trouver l'utilisateur par customer_id
            user = users_collection.find_one({'stripe_customer_id': customer_id})
            
            if user:
                # Retirer le statut premium
                users_collection.update_one(
                    {'_id': user['_id']},
                    {
                        '$set': {
                            'is_premium': False,
                            'subscription_status': 'cancelled',
                            'premium_cancelled_at': datetime.utcnow(),
                            'updated_at': datetime.utcnow()
                        }
                    }
                )
                
                print(f"❌ Abonnement annulé pour {user.get('user_id')}")
            
            return {"status": "cancelled"}
        
        # Autres événements non gérés
        print(f"⚠️ Événement non géré: {event.type}")
        return {"status": "unhandled", "type": event.type}
    
    except Exception as e:
        print(f"❌ Erreur webhook Stripe: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
