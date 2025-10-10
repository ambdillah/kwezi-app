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
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    # TODO: Configurer le webhook secret
    # webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    try:
        # Pour l'instant, on parse l'événement sans vérifier la signature
        # En production, il faut ajouter la vérification
        event = stripe.Event.construct_from(
            await request.json(), stripe.api_key
        )
        
        # Gérer les différents types d'événements
        if event.type == 'checkout.session.completed':
            session = event.data.object
            user_id = session.get('client_reference_id')
            customer_id = session.get('customer')
            subscription_id = session.get('subscription')
            
            # TODO: Mettre à jour l'utilisateur dans MongoDB
            # Marquer comme premium, sauvegarder customer_id et subscription_id
            
            return {"status": "success", "user_id": user_id}
        
        elif event.type == 'customer.subscription.updated':
            subscription = event.data.object
            # Gérer mise à jour abonnement
            return {"status": "updated"}
        
        elif event.type == 'customer.subscription.deleted':
            subscription = event.data.object
            # Gérer annulation abonnement
            return {"status": "cancelled"}
        
        return {"status": "unhandled"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
