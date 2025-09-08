# 🚀 Guide d'installation Stripe pour OptiTAB

## 📋 **Étapes d'installation**

### **1. Configuration Stripe Dashboard**

1. **Créer un compte Stripe** : https://dashboard.stripe.com/register
2. **Activer le mode test** dans le dashboard
3. **Récupérer les clés API** :
   - Clé publique : `pk_test_...`
   - Clé secrète : `sk_test_...`

### **2. Configuration des produits**

Dans le dashboard Stripe :

1. **Produits > Créer un produit**
2. Créer ces produits :
   - **OptiTAB Basic Mensuel** - 9.99€/mois
   - **OptiTAB Basic Annuel** - 99.99€/an
   - **OptiTAB Premium Mensuel** - 19.99€/mois  
   - **OptiTAB Premium Annuel** - 199.99€/an

3. **Récupérer les Price IDs** de chaque produit

### **3. Configuration Backend Django**

1. **Installer les dépendances** :
```bash
cd BackendOptiTAB
pip install stripe django-cors-headers
```

2. **Ajouter dans settings.py** :
```python
INSTALLED_APPS = [
    # ... autres apps
    'subscriptions',
    'corsheaders',
]

MIDDLEWARE = [
    # ... autres middleware
    'corsheaders.middleware.CorsMiddleware',
]

# Configuration CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# URL frontend
FRONTEND_URL = "http://localhost:3000"
```

3. **Créer le fichier .env** :
```env
STRIPE_PUBLISHABLE_KEY=pk_test_votre_cle_publique
STRIPE_SECRET_KEY=sk_test_votre_cle_secrete
STRIPE_WEBHOOK_SECRET=whsec_votre_webhook_secret
FRONTEND_URL=http://localhost:3000
```

4. **Mettre à jour stripe_config.py** avec vos Price IDs

5. **Ajouter les URLs dans urls.py principal** :
```python
urlpatterns = [
    # ... autres URLs
    path('api/subscriptions/', include('subscriptions.urls')),
]
```

6. **Migrations** :
```bash
python manage.py makemigrations subscriptions
python manage.py migrate
```

7. **Créer les plans dans la base** :
```bash
python manage.py shell
```
```python
from subscriptions.models import SubscriptionPlan

# Créer les plans
SubscriptionPlan.objects.create(
    name="OptiTAB Basic Mensuel",
    plan_type="basic",
    billing_period="monthly",
    price=9.99,
    stripe_price_id="price_votre_price_id_basic_monthly",
    features=["Accès aux exercices", "Calculatrice scientifique", "Support email"]
)

SubscriptionPlan.objects.create(
    name="OptiTAB Premium Mensuel",
    plan_type="premium", 
    billing_period="monthly",
    price=19.99,
    stripe_price_id="price_votre_price_id_premium_monthly",
    features=["Tout Basic", "Fiches de synthèse", "Quiz illimités", "Support prioritaire"]
)

# Répéter pour les plans annuels...
```

### **4. Configuration Webhook**

1. **Dans Stripe Dashboard > Webhooks**
2. **Créer un endpoint** : `http://localhost:8000/api/subscriptions/webhook/`
3. **Sélectionner les événements** :
   - `checkout.session.completed`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`

4. **Récupérer le secret webhook** et l'ajouter au .env

### **5. Configuration Frontend**

1. **Ajouter les routes dans router/index.js** :
```javascript
const routes = [
  // ... autres routes
  {
    path: '/pricing',
    name: 'Pricing',
    component: () => import('@/views/Pricing.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/subscription',
    name: 'Subscription', 
    component: () => import('@/views/Subscription.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/payment/success',
    name: 'PaymentSuccess',
    component: () => import('@/views/PaymentSuccess.vue')
  },
  {
    path: '/payment/cancel',
    name: 'PaymentCancel',
    component: () => import('@/views/PaymentCancel.vue')
  }
]
```

2. **Ajouter dans la navigation** :
```javascript
// Dans votre composant de navigation
{
  name: 'Abonnement',
  path: '/subscription',
  icon: CreditCardIcon,
  requiresAuth: true
}
```

## 🧪 **Tests**

### **Cartes de test Stripe :**
- **Succès** : `4242 4242 4242 4242`
- **Échec** : `4000 0000 0000 0002`
- **3D Secure** : `4000 0025 0000 3155`

### **Scénarios à tester :**
1. ✅ Création d'abonnement avec essai gratuit
2. ✅ Paiement réussi après essai
3. ✅ Paiement échoué
4. ✅ Annulation d'abonnement
5. ✅ Webhooks (vérifier les logs)

## 🚀 **Démarrage**

1. **Backend** :
```bash
cd BackendOptiTAB
python manage.py runserver
```

2. **Frontend** :
```bash
cd websitecursor
npm run dev
```

3. **Tester** : http://localhost:3000/pricing

## 📊 **Monitoring**

- **Dashboard Stripe** : Suivre les paiements en temps réel
- **Logs Django** : Vérifier les webhooks
- **Base de données** : Vérifier les abonnements utilisateurs

## 🔧 **Personnalisation**

### **Ajouter des fonctionnalités premium :**
```python
# Dans vos vues
from subscriptions.models import UserSubscription

def premium_feature_view(request):
    try:
        subscription = request.user.subscription
        if not subscription.is_active:
            return JsonResponse({'error': 'Abonnement requis'}, status=403)
        
        if subscription.plan.plan_type == 'basic':
            return JsonResponse({'error': 'Plan Premium requis'}, status=403)
            
        # Logique de la fonctionnalité premium
        
    except UserSubscription.DoesNotExist:
        return JsonResponse({'error': 'Abonnement requis'}, status=403)
```

### **Middleware de vérification d'abonnement :**
```python
class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Vérifier l'abonnement pour certaines routes
        if request.path.startswith('/api/premium/'):
            if not hasattr(request.user, 'subscription') or not request.user.subscription.is_active:
                return JsonResponse({'error': 'Abonnement requis'}, status=403)
                
        return self.get_response(request)
```

## 🎯 **Prochaines étapes**

1. **Mise en production** :
   - Passer en mode live sur Stripe
   - Configurer le webhook en production
   - Mettre à jour les clés API

2. **Fonctionnalités avancées** :
   - Factures PDF
   - Gestion des coupons
   - Analytics d'abonnements
   - Notifications par email

## 📞 **Support**

En cas de problème :
1. Vérifier les logs Django
2. Vérifier le dashboard Stripe
3. Tester avec les cartes de test
4. Vérifier la configuration webhook
