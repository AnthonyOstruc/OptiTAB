Stripe subscription setup (OptiTAB)

1) Configure environment variables (backend/.env)
- STRIPE_SECRET_KEY=sk_live_...
- STRIPE_PUBLISHABLE_KEY=pk_live_...
- STRIPE_WEBHOOK_SECRET=whsec_...
- FRONTEND_BASE_URL=https://optitab.net
# Optional overrides
- STRIPE_SUCCESS_URL=https://optitab.net/billing/success
- STRIPE_CANCEL_URL=https://optitab.net/billing/cancel
- STRIPE_FREE_TRIAL_DAYS=7

2) Install backend dependency
- pip install -r backend/requirements.txt

3) Enable the app and run migrations
- python backend/manage.py makemigrations subscriptions
- python backend/manage.py migrate

4) Create Stripe products/prices and mirror them locally
- In Stripe Dashboard, create Products with recurring Prices (monthly/yearly).
- Copy the Price IDs (price_...)
- In Django admin → Subscription plans, create entries with the matching `stripe_price_id`.

5) Expose a webhook endpoint in Stripe
- Endpoint: https://<your-backend-domain>/api/subscriptions/webhook/
- Events: checkout.session.completed, invoice.payment_succeeded, invoice.payment_failed, customer.subscription.updated, customer.subscription.deleted
- Use the displayed Signing secret as STRIPE_WEBHOOK_SECRET.

6) Frontend flow
- Use the new Billing page at /billing to list plans and redirect to Stripe Checkout.
- On success/cancel, Stripe redirects to /billing/success or /billing/cancel.

