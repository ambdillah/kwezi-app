"""
Script pour créer le produit et le prix d'abonnement Premium sur Stripe
"""

import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

print("="*80)
print("CRÉATION DU PRODUIT STRIPE - ABONNEMENT PREMIUM KWEZI")
print("="*80)

try:
    # Créer le produit
    product = stripe.Product.create(
        name="Abonnement Premium Kwezi",
        description="Accès illimité à tous les mots et fonctionnalités de l'application Kwezi",
    )
    
    print(f"\n✅ Produit créé:")
    print(f"   ID: {product.id}")
    print(f"   Nom: {product.name}")
    
    # Créer le prix récurrent (2.90€/mois)
    price = stripe.Price.create(
        product=product.id,
        unit_amount=290,  # 2.90€ en centimes
        currency="eur",
        recurring={"interval": "month"},
    )
    
    print(f"\n✅ Prix créé:")
    print(f"   ID: {price.id}")
    print(f"   Montant: {price.unit_amount/100}€/{price.recurring.interval}")
    
    print(f"\n" + "="*80)
    print(f"CONFIGURATION À AJOUTER DANS .env:")
    print(f"="*80)
    print(f"STRIPE_PRICE_ID_PREMIUM={price.id}")
    print(f"="*80)
    
    # Mettre à jour le .env automatiquement
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    with open('.env', 'w') as f:
        for line in lines:
            if line.startswith('STRIPE_PRICE_ID_PREMIUM='):
                f.write(f'STRIPE_PRICE_ID_PREMIUM={price.id}\n')
            else:
                f.write(line)
    
    print(f"\n✅ Fichier .env mis à jour automatiquement!")
    
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
