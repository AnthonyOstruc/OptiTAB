import stripe
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.models import User
from django.utils import timezone
import logging
from datetime import timedelta

from .models import SubscriptionPlan, UserSubscription, PaymentHistory
from stripe_config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, SUCCESS_URL, CANCEL_URL, FREE_TRIAL_DAYS

stripe.api_key = STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

class CreateCheckoutSessionView(View):
    """Créer une session de paiement Stripe"""
    
    @method_decorator(login_required)
    def post(self, request):
        try:
            data = json.loads(request.body)
            price_id = data.get('price_id')
            
            # Récupérer le plan
            try:
                plan = SubscriptionPlan.objects.get(stripe_price_id=price_id)
            except SubscriptionPlan.DoesNotExist:
                return JsonResponse({'error': 'Plan non trouvé'}, status=404)
            
            # Créer ou récupérer le client Stripe
            customer = None
            if hasattr(request.user, 'subscription') and request.user.subscription.stripe_customer_id:
                customer_id = request.user.subscription.stripe_customer_id
            else:
                customer = stripe.Customer.create(
                    email=request.user.email,
                    name=f"{request.user.first_name} {request.user.last_name}",
                    metadata={'user_id': request.user.id}
                )
                customer_id = customer.id
            
            # Créer la session de checkout
            checkout_session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=SUCCESS_URL + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=CANCEL_URL,
                subscription_data={
                    'trial_period_days': FREE_TRIAL_DAYS,
                    'metadata': {
                        'user_id': request.user.id,
                        'plan_id': plan.id
                    }
                },
                metadata={
                    'user_id': request.user.id,
                    'plan_id': plan.id
                }
            )
            
            return JsonResponse({'checkout_url': checkout_session.url})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class SubscriptionStatusView(View):
    """Récupérer le statut d'abonnement de l'utilisateur"""
    
    @method_decorator(login_required)
    def get(self, request):
        try:
            subscription = request.user.subscription
            return JsonResponse({
                'has_subscription': True,
                'plan_name': subscription.plan.name,
                'status': subscription.status,
                'is_active': subscription.is_active,
                'is_trial': subscription.is_trial,
                'days_remaining_trial': subscription.days_remaining_trial,
                'current_period_end': subscription.current_period_end.isoformat() if subscription.current_period_end else None,
                'features': subscription.plan.features
            })
        except UserSubscription.DoesNotExist:
            return JsonResponse({
                'has_subscription': False,
                'status': 'none'
            })

class CancelSubscriptionView(View):
    """Annuler l'abonnement"""
    
    @method_decorator(login_required)
    def post(self, request):
        try:
            subscription = request.user.subscription
            if subscription.cancel_subscription():
                return JsonResponse({'success': True, 'message': 'Abonnement annulé avec succès'})
            else:
                return JsonResponse({'error': 'Erreur lors de l\'annulation'}, status=400)
        except UserSubscription.DoesNotExist:
            return JsonResponse({'error': 'Aucun abonnement trouvé'}, status=404)

class PlansListView(View):
    """Liste des plans disponibles"""
    
    def get(self, request):
        plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
        plans_data = []
        
        for plan in plans:
            plans_data.append({
                'id': plan.id,
                'name': plan.name,
                'plan_type': plan.plan_type,
                'billing_period': plan.billing_period,
                'price': float(plan.price),
                'stripe_price_id': plan.stripe_price_id,
                'features': plan.features
            })
        
        return JsonResponse({'plans': plans_data})

@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    """Webhook pour gérer les événements Stripe"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Gérer les différents types d'événements
    if event['type'] == 'checkout.session.completed':
        handle_checkout_session_completed(event['data']['object'])
    
    elif event['type'] == 'invoice.payment_succeeded':
        handle_payment_succeeded(event['data']['object'])
    
    elif event['type'] == 'invoice.payment_failed':
        handle_payment_failed(event['data']['object'])
    
    elif event['type'] == 'customer.subscription.updated':
        handle_subscription_updated(event['data']['object'])
    
    elif event['type'] == 'customer.subscription.deleted':
        handle_subscription_deleted(event['data']['object'])
    
    return HttpResponse(status=200)

def handle_checkout_session_completed(session):
    """Gérer la completion d'une session de checkout"""
    try:
        user_id = session['metadata']['user_id']
        plan_id = session['metadata']['plan_id']
        
        user = User.objects.get(id=user_id)
        plan = SubscriptionPlan.objects.get(id=plan_id)
        
        # Récupérer l'abonnement Stripe
        subscription = stripe.Subscription.retrieve(session['subscription'])
        
        # Créer ou mettre à jour l'abonnement utilisateur
        user_subscription, created = UserSubscription.objects.get_or_create(
            user=user,
            defaults={
                'plan': plan,
                'stripe_subscription_id': subscription.id,
                'stripe_customer_id': session['customer'],
                'status': subscription.status,
                'current_period_start': timezone.datetime.fromtimestamp(subscription.current_period_start),
                'current_period_end': timezone.datetime.fromtimestamp(subscription.current_period_end),
                'trial_end': timezone.datetime.fromtimestamp(subscription.trial_end) if subscription.trial_end else None
            }
        )
        
        if not created:
            user_subscription.plan = plan
            user_subscription.stripe_subscription_id = subscription.id
            user_subscription.stripe_customer_id = session['customer']
            user_subscription.status = subscription.status
            user_subscription.current_period_start = timezone.datetime.fromtimestamp(subscription.current_period_start)
            user_subscription.current_period_end = timezone.datetime.fromtimestamp(subscription.current_period_end)
            user_subscription.trial_end = timezone.datetime.fromtimestamp(subscription.trial_end) if subscription.trial_end else None
            user_subscription.save()
        
    except Exception as e:
        logger.error(f"Erreur dans handle_checkout_session_completed: {e}")

def handle_payment_succeeded(invoice):
    """Gérer un paiement réussi"""
    try:
        subscription_id = invoice['subscription']
        subscription = stripe.Subscription.retrieve(subscription_id)
        
        user_subscription = UserSubscription.objects.get(stripe_subscription_id=subscription_id)
        user_subscription.status = 'active'
        user_subscription.current_period_start = timezone.datetime.fromtimestamp(subscription.current_period_start)
        user_subscription.current_period_end = timezone.datetime.fromtimestamp(subscription.current_period_end)
        user_subscription.save()
        
        # Enregistrer le paiement
        PaymentHistory.objects.create(
            user=user_subscription.user,
            stripe_payment_intent_id=invoice['payment_intent'],
            amount=invoice['amount_paid'] / 100,  # Stripe utilise les centimes
            currency=invoice['currency'].upper(),
            status='succeeded',
            description=f"Paiement pour {user_subscription.plan.name}"
        )
        
    except Exception as e:
        logger.error(f"Erreur dans handle_payment_succeeded: {e}")

def handle_payment_failed(invoice):
    """Gérer un paiement échoué"""
    try:
        subscription_id = invoice['subscription']
        user_subscription = UserSubscription.objects.get(stripe_subscription_id=subscription_id)
        user_subscription.status = 'past_due'
        user_subscription.save()
        
    except Exception as e:
        logger.error(f"Erreur dans handle_payment_failed: {e}")

def handle_subscription_updated(subscription):
    """Gérer la mise à jour d'un abonnement"""
    try:
        user_subscription = UserSubscription.objects.get(stripe_subscription_id=subscription['id'])
        user_subscription.status = subscription['status']
        user_subscription.current_period_start = timezone.datetime.fromtimestamp(subscription['current_period_start'])
        user_subscription.current_period_end = timezone.datetime.fromtimestamp(subscription['current_period_end'])
        user_subscription.save()
        
    except Exception as e:
        logger.error(f"Erreur dans handle_subscription_updated: {e}")

def handle_subscription_deleted(subscription):
    """Gérer la suppression d'un abonnement"""
    try:
        user_subscription = UserSubscription.objects.get(stripe_subscription_id=subscription['id'])
        user_subscription.status = 'canceled'
        user_subscription.save()
        
    except Exception as e:
        logger.error(f"Erreur dans handle_subscription_deleted: {e}")
