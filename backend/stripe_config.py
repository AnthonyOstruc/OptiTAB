import os

# Stripe credentials
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')

# Frontend URLs for redirect after checkout
FRONTEND_BASE_URL = os.getenv('FRONTEND_BASE_URL', 'http://localhost:3000')
SUCCESS_URL = os.getenv('STRIPE_SUCCESS_URL', f"{FRONTEND_BASE_URL}/billing/success")
CANCEL_URL = os.getenv('STRIPE_CANCEL_URL', f"{FRONTEND_BASE_URL}/billing/cancel")

# Trial configuration
FREE_TRIAL_DAYS = int(os.getenv('STRIPE_FREE_TRIAL_DAYS', '7'))

