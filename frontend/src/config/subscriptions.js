// Frontend fallback plans if backend list is empty or errors.
// Paste your Stripe Price IDs in a .env.local file as shown below
// VITE_PRICE_MONTHLY=price_xxx
// VITE_PRICE_WEEKLY=price_xxx
// VITE_PRICE_YEARLY=price_xxx
// VITE_PRICE_PASS_MONTH=price_xxx
// VITE_PRICE_PASS_DAY=price_xxx

const env = import.meta.env || {}

const pick = (k) => (env[k] || '').trim()

export const DEFAULT_PLANS = [
  {
    key: 'monthly_sub',
    name: 'Mensuel',
    mode: 'subscription',
    billing_period: 'monthly',
    price: 4.99,
    stripe_price_id: pick('VITE_PRICE_MONTHLY'),
    access_days: null,
    features: [
      'Accès complet à la plateforme de maths',
      'Sans engagement, annulable à tout moment',
    ],
    _badge: 'Recommandé'
  },
  {
    key: 'weekly_sub',
    name: 'Hebdomadaire',
    mode: 'subscription',
    billing_period: 'weekly',
    price: 2.49,
    stripe_price_id: pick('VITE_PRICE_WEEKLY'),
    access_days: null,
    features: [
      'Accès plateforme de maths pendant 7 jours',
      'Renouvellement flexible chaque semaine',
    ],
  },
  {
    key: 'yearly_sub',
    name: 'Annuel',
    mode: 'subscription',
    billing_period: 'yearly',
    price: 50.0,
    stripe_price_id: pick('VITE_PRICE_YEARLY'),
    access_days: null,
    features: [
      'Accès plateforme de maths pendant 12 mois',
      'Économisez ~16% vs mensuel',
    ],
  },
  {
    key: 'pass_month',
    name: 'Pass 1 mois',
    mode: 'one_time',
    billing_period: 'monthly',
    price: 6.99,
    stripe_price_id: pick('VITE_PRICE_PASS_MONTH'),
    access_days: 30,
    features: [
      'Accès plateforme de maths 30 jours',
      'Paiement unique, non reconduit',
    ],
  },
  {
    key: 'pass_day',
    name: 'Pass 24h',
    mode: 'one_time',
    billing_period: 'monthly',
    price: 0.99,
    stripe_price_id: pick('VITE_PRICE_PASS_DAY'),
    access_days: 1,
    features: [
      'Accès plateforme de maths 24 heures',
      'Idéal pour un contrôle/devoir',
    ],
  },
]
