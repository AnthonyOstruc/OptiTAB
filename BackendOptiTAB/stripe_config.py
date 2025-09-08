# Configuration Stripe
import os
from django.conf import settings

# Clés Stripe (à mettre dans votre .env)
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_...')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_...')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_...')

# Configuration des produits
STRIPE_PRICE_IDS = {
    'basic_monthly': 'price_...',  # Prix mensuel de base
    'premium_monthly': 'price_...',  # Prix mensuel premium
    'basic_yearly': 'price_...',   # Prix annuel de base
    'premium_yearly': 'price_...'  # Prix annuel premium
}

# Configuration des essais gratuits (en jours)
FREE_TRIAL_DAYS = 7

# URLs de redirection
SUCCESS_URL = settings.FRONTEND_URL + '/payment/success'
CANCEL_URL = settings.FRONTEND_URL + '/payment/cancel'
