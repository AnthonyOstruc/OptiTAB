Stripe subscription setup (OptiTAB)

1) Configure environment variables safely by environment

Local development (`backend/.env`):
- STRIPE_SECRET_KEY=sk_test_...
- STRIPE_PUBLISHABLE_KEY=pk_test_...
- STRIPE_WEBHOOK_SECRET=whsec_... (from Stripe Test mode)
- Optional explicit alias: STRIPE_WEBHOOK_SECRET_TEST=whsec_...
- FRONTEND_BASE_URL=http://localhost:3000
- STRIPE_ENV=dev

Production (Render environment variables):
- STRIPE_SECRET_KEY=sk_live_...
- STRIPE_PUBLISHABLE_KEY=pk_live_...
- Recommended: STRIPE_WEBHOOK_SECRET_LIVE=whsec_... (from Stripe Live mode)
- If Stripe Test mode also points to the same production URL: STRIPE_WEBHOOK_SECRET_TEST=whsec_...
- Backward-compatible fallback: STRIPE_WEBHOOK_SECRET=whsec_... (single secret only)
- FRONTEND_BASE_URL=https://optitab.net

Optional overrides:
- STRIPE_SUCCESS_URL=https://optitab.net/billing/success
- STRIPE_CANCEL_URL=https://optitab.net/billing/cancel
- STRIPE_FREE_TRIAL_DAYS=0  # Set to a positive number only if you offer a free trial

Safety guard (enabled by default):
- Local/dev refuses `*_live_*` Stripe keys.
- Production refuses `*_test_*` Stripe keys.
- Override only in emergency with `STRIPE_DISABLE_MODE_GUARD=true`.

2) Install backend dependency
- pip install -r backend/requirements.txt

3) Enable the app and run migrations
- python backend/manage.py makemigrations subscriptions
- python backend/manage.py migrate

4) Create the four offers in Stripe (Test mode first)
- Subscriptions (recurring):
  - Monthly: 4.99 EUR, interval monthly → get `price_...`
  - Yearly: 50.00 EUR, interval yearly → get `price_...`
- One‑time passes (non‑recurring):
  - 1 month pass: 6.99 EUR, one‑time
  - 1 day pass: 0.99 EUR, one‑time

Mirror in Django admin → Subscription plans:
- For subscriptions: set `mode = subscription`, `billing_period = monthly/yearly`, `stripe_price_id`, `price`.
- For passes: set `mode = one_time`, `billing_period` can be monthly (cosmetic), `access_days` = 30 for 1‑month pass, 1 for 1‑day pass, `stripe_price_id`, `price`.

5) Expose a webhook endpoint in Stripe
- Endpoint: https://<your-backend-domain>/api/subscriptions/webhook/
- Events:
  - checkout.session.completed
  - invoice.created
  - invoice.payment_succeeded
  - invoice.payment_failed
  - customer.subscription.updated
  - customer.subscription.deleted
  - charge.refunded
- refund.created
- refund.updated
- charge.refund.created
- charge.refund.updated
- Recommended: use separate webhook endpoints/URLs for Stripe Test and Stripe Live.
- If both Stripe modes target the same backend URL, set both `STRIPE_WEBHOOK_SECRET_LIVE` and `STRIPE_WEBHOOK_SECRET_TEST` on the backend.
- `STRIPE_WEBHOOK_SECRET` remains supported as a legacy single-secret fallback.

6) Frontend flow

7) Optional: Seed the 4 plans from CLI
- Run after migrations:
  - python backend/manage.py seed_subscription_plans \
      --monthly price_XXXX \
      --yearly price_YYYY \
      --pass-month price_ZZZZ \
      --pass-day price_WWWW
- This creates/updates the four plans with your Stripe Price IDs.
- Use the new Billing page at /billing to list plans and redirect to Stripe Checkout.
- On success/cancel, Stripe redirects to /billing/success or /billing/cancel.

8) Local dev fallback (si le webhook n'est pas joignable)
- L'URL `/api/subscriptions/checkout-session/status/?session_id=...` permet au frontend de forcer la finalisation d'une session Stripe après la redirection `success_url`.
- Cela garantit que les abonnements/passes sont créés même sans tunnel Stripe CLI.

9) Important local frontend setting
- In local frontend dev, keep API on local backend (`http://localhost:8000`).
- Do not set `VITE_USE_REMOTE_IN_DEV=true`, otherwise your local UI can hit production backend.
