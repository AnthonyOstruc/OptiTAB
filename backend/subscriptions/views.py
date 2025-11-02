import stripe
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal
import logging
from datetime import datetime, timedelta, timezone as dt_timezone

from .models import SubscriptionPlan, UserSubscription, PaymentHistory, AccessPass
from django.db import DatabaseError
from stripe_config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, SUCCESS_URL, CANCEL_URL, FREE_TRIAL_DAYS

stripe.api_key = STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

User = get_user_model()

class CreateCheckoutSessionView(APIView):
    """Créer une session de paiement Stripe"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Utiliser DRF pour parser le payload JSON
            price_id = request.data.get('price_id')
            
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
            
            # Créer la session de checkout (abonnement récurrent ou pass unique)
            plan_mode = getattr(plan, 'mode', getattr(plan, 'plan_mode', 'subscription'))
            is_subscription = (plan_mode == 'subscription')

            create_kwargs = dict(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription' if is_subscription else 'payment',
                success_url=SUCCESS_URL + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=CANCEL_URL,
                metadata={
                    'user_id': request.user.id,
                    'plan_id': plan.id,
                    'plan_mode': plan_mode,
                }
            )

            if is_subscription:
                create_kwargs['subscription_data'] = {
                    'trial_period_days': FREE_TRIAL_DAYS,
                    'metadata': {
                        'user_id': request.user.id,
                        'plan_id': plan.id
                    }
                }

            checkout_session = stripe.checkout.Session.create(**create_kwargs)
            
            return JsonResponse({'checkout_url': checkout_session.url})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class SubscriptionStatusView(APIView):
    """Récupérer le statut d'abonnement de l'utilisateur"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = {
            'has_subscription': False,
            'status': 'none',
            'is_active': False,
            'has_active_pass': False,
            'has_manual_access': bool(getattr(request.user, 'has_complimentary_access', False)),
        }

        # Abonnement récurrent
        try:
            subscription = request.user.subscription
            response.update({
                'has_subscription': True,
                'plan_name': subscription.plan.name,
                'status': subscription.status,
                'is_active': subscription.is_active,
                'is_trial': subscription.is_trial,
                'days_remaining_trial': subscription.days_remaining_trial,
                'current_period_end': subscription.current_period_end.isoformat() if subscription.current_period_end else None,
                'features': subscription.plan.features,
            })
        except UserSubscription.DoesNotExist:
            pass

        # Pass one-time actif
        active_pass = (
            AccessPass.objects.filter(user=request.user, ends_at__gt=timezone.now())
            .order_by('-ends_at')
            .first()
        )
        if active_pass:
            response.update({
                'has_active_pass': True,
                'active_pass_plan': active_pass.plan.name,
                'active_pass_ends_at': active_pass.ends_at.isoformat(),
            })

        # Accès manuel (accordé par un admin)
        if response['has_manual_access'] and not response.get('has_subscription'):
            response.setdefault('plan_name', 'Accès manuel')
            response['status'] = 'manual'

        # Accès global (abonnement actif OU pass actif OU accès manuel)
        response['has_access'] = bool(
            response.get('is_active')
            or response.get('has_active_pass')
            or response.get('has_manual_access')
        )
        return JsonResponse(response)

class CancelSubscriptionView(APIView):
    """Annuler l'abonnement"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            subscription = request.user.subscription
            if subscription.cancel_subscription():
                return JsonResponse({'success': True, 'message': 'Abonnement annulé avec succès'})
            else:
                return JsonResponse({'error': 'Erreur lors de l\'annulation'}, status=400)
        except UserSubscription.DoesNotExist:
            return JsonResponse({'error': 'Aucun abonnement trouvé'}, status=404)

class PlansListView(APIView):
    """Liste des plans disponibles"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
            plans_data = []
            for plan in plans:
                plans_data.append({
                    'id': plan.id,
                    'name': plan.name,
                    'plan_type': plan.plan_type,
                    'mode': getattr(plan, 'mode', getattr(plan, 'plan_mode', 'subscription')),
                    'billing_period': plan.billing_period,
                    'price': float(plan.price),
                    'stripe_price_id': plan.stripe_price_id,
                    'features': plan.features,
                    'access_days': getattr(plan, 'access_days', None),
                })
            return JsonResponse({'plans': plans_data})
        except DatabaseError as e:
            logger.error(f"PlansListView DB error: {e}")
            return JsonResponse({
                'error': 'Database not ready. Run migrations and create plans in admin.',
                'hint': 'python manage.py migrate, then add SubscriptionPlan entries',
            }, status=500)

def _is_admin(user):
    try:
        return bool(getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False))
    except Exception:
        return False

def _plan_to_dict(plan):
    return {
        'id': plan.id,
        'name': plan.name,
        'plan_type': plan.plan_type,
        'mode': getattr(plan, 'mode', getattr(plan, 'plan_mode', 'subscription')),
        'billing_period': plan.billing_period,
        'price': float(plan.price),
        'stripe_price_id': plan.stripe_price_id,
        'features': plan.features,
        'access_days': getattr(plan, 'access_days', None),
        'is_active': plan.is_active,
        'created_at': plan.created_at.isoformat() if plan.created_at else None,
    }

class AdminPlansView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)
        qs = SubscriptionPlan.objects.all().order_by('-is_active', 'price')
        return JsonResponse({'plans': [_plan_to_dict(p) for p in qs]})

    def post(self, request):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)
        data = request.data if hasattr(request, 'data') else json.loads(request.body or '{}')
        try:
            name = data.get('name') or ''
            plan_type = data.get('plan_type') or 'basic'
            mode = (data.get('mode') or data.get('plan_mode') or 'subscription').lower()
            billing_period = data.get('billing_period') or 'monthly'
            price = data.get('price')
            stripe_price_id = data.get('stripe_price_id')
            access_days = data.get('access_days')
            features = data.get('features') or []
            is_active = bool(data.get('is_active', True))

            if not name or not stripe_price_id or price is None:
                return JsonResponse({'detail': 'name, price and stripe_price_id are required'}, status=400)

            plan = SubscriptionPlan.objects.create(
                name=name,
                plan_type=plan_type,
                billing_period=billing_period,
                price=price,
                stripe_price_id=stripe_price_id,
                features=features if isinstance(features, list) else [],
                is_active=is_active,
            )
            # set mode/access_days if fields exist
            if hasattr(plan, 'plan_mode'):
                plan.plan_mode = mode
            if hasattr(plan, 'mode'):
                setattr(plan, 'mode', mode)
            if hasattr(plan, 'access_days') and access_days is not None:
                plan.access_days = access_days
            plan.save()
            return JsonResponse({'plan': _plan_to_dict(plan)}, status=201)
        except Exception as e:
            logger.error(f"AdminPlansView.post error: {e}")
            return JsonResponse({'detail': str(e)}, status=400)

class AdminPlanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)
        try:
            plan = SubscriptionPlan.objects.get(pk=pk)
        except SubscriptionPlan.DoesNotExist:
            return JsonResponse({'detail': 'Not found'}, status=404)
        data = request.data if hasattr(request, 'data') else json.loads(request.body or '{}')
        try:
            for field in ['name', 'plan_type', 'billing_period', 'price', 'stripe_price_id', 'is_active']:
                if field in data:
                    setattr(plan, field, data[field])
            # Handle mode / plan_mode
            if 'mode' in data or 'plan_mode' in data:
                mode = (data.get('mode') or data.get('plan_mode')).lower()
                if hasattr(plan, 'plan_mode'):
                    plan.plan_mode = mode
                if hasattr(plan, 'mode'):
                    setattr(plan, 'mode', mode)
            if 'access_days' in data and hasattr(plan, 'access_days'):
                plan.access_days = data.get('access_days')
            if 'features' in data and isinstance(data['features'], list):
                plan.features = data['features']
            plan.save()
            return JsonResponse({'plan': _plan_to_dict(plan)})
        except Exception as e:
            logger.error(f"AdminPlanDetailView.patch error: {e}")
            return JsonResponse({'detail': str(e)}, status=400)

    def delete(self, request, pk):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)
        try:
            plan = SubscriptionPlan.objects.get(pk=pk)
        except SubscriptionPlan.DoesNotExist:
            return JsonResponse({'detail': 'Not found'}, status=404)
        plan.delete()
        return JsonResponse({'deleted': True})


class AdminSubscribersView(APIView):
    """Liste consolidée des abonnés (abonnements + passes) pour l'admin"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)

        try:
            q = (request.GET.get('q') or '').strip().lower()
            active_only = (request.GET.get('active', 'false').lower() == 'true')

            def iso_or_none(dt):
                try:
                    return dt.isoformat() if dt else None
                except Exception:
                    return None

            items = []
            covered_user_ids = set()

            # Abonnements récurrents
            subs_qs = UserSubscription.objects.select_related('user', 'plan')
            # Précharger le montant du dernier paiement pour chaque abonnement (si disponible)
            latest_payment_map = {}
            try:
                latest_payments = (
                    PaymentHistory.objects
                    .filter(stripe_payment_intent_id__isnull=False)
                    .order_by('user_id', '-created_at')
                )
                for payment in latest_payments:
                    if payment.user_id in latest_payment_map:
                        continue
                    latest_payment_map[payment.user_id] = {
                        'amount': float(payment.amount),
                        'currency': (payment.currency or 'EUR').upper(),
                    }
            except Exception as payment_err:
                logger.warning(f"AdminSubscribersView payment lookup failed: {payment_err}")
                latest_payment_map = {}
            for s in subs_qs:
                try:
                    if q:
                        if q not in (s.user.email or '').lower() and q not in (s.user.first_name or '').lower() and q not in (s.user.last_name or '').lower():
                            continue
                    plan = getattr(s, 'plan', None)
                    plan_name = getattr(plan, 'name', '—') if plan else '—'
                    plan_mode = getattr(plan, 'plan_mode', getattr(plan, 'mode', 'subscription')) if plan else 'subscription'
                    billing_period = getattr(plan, 'billing_period', None) if plan else None
                    rec = {
                        'type': 'subscription',
                        'user_id': s.user_id,
                        'email': getattr(s.user, 'email', ''),
                        'first_name': getattr(s.user, 'first_name', ''),
                        'last_name': getattr(s.user, 'last_name', ''),
                        'plan_id': getattr(s, 'plan_id', None),
                        'plan_name': plan_name,
                        'plan_mode': plan_mode,
                        'billing_period': billing_period,
                        'status': s.status,
                        'is_active': bool(getattr(s, 'is_active', False)),
                        'is_trial': bool(getattr(s, 'is_trial', False)),
                        'days_remaining_trial': int(getattr(s, 'days_remaining_trial', 0)),
                        'current_period_start': iso_or_none(getattr(s, 'current_period_start', None)),
                        'current_period_end': iso_or_none(getattr(s, 'current_period_end', None)),
                    }
                    payment_info = latest_payment_map.get(s.user_id)
                    if payment_info:
                        rec.update({
                            'amount_paid': payment_info['amount'],
                            'currency': payment_info['currency'],
                        })
                    elif plan and getattr(plan, 'price', None) is not None:
                        rec.update({
                            'amount_paid': float(plan.price),
                            'currency': 'EUR',
                        })
                    if active_only and not rec['is_active']:
                        continue
                    items.append(rec)
                    covered_user_ids.add(s.user_id)
                except Exception as row_err:
                    logger.error(f"AdminSubscribersView row(sub) error: {row_err}")
                    continue

            # Pass (achats one-time)
            now = timezone.now()
            try:
                pass_qs = AccessPass.objects.select_related('user', 'plan')
                for p in pass_qs:
                    try:
                        if q:
                            if q not in (p.user.email or '').lower() and q not in (p.user.first_name or '').lower() and q not in (p.user.last_name or '').lower():
                                continue
                        plan = getattr(p, 'plan', None)
                        plan_name = getattr(plan, 'name', '—') if plan else '—'
                        plan_mode = getattr(plan, 'plan_mode', getattr(plan, 'mode', 'one_time')) if plan else 'one_time'
                        access_days = getattr(plan, 'access_days', None) if plan else None
                        is_active = bool(p.ends_at and (p.ends_at > now))
                        if active_only and not is_active:
                            continue
                        pass_entry = {
                            'type': 'pass',
                            'user_id': p.user_id,
                            'email': getattr(p.user, 'email', ''),
                            'first_name': getattr(p.user, 'first_name', ''),
                            'last_name': getattr(p.user, 'last_name', ''),
                            'plan_id': getattr(p, 'plan_id', None),
                            'plan_name': plan_name,
                            'plan_mode': plan_mode,
                            'access_days': access_days,
                            'starts_at': iso_or_none(getattr(p, 'starts_at', None)),
                            'ends_at': iso_or_none(getattr(p, 'ends_at', None)),
                            'is_active': is_active,
                        }
                        if plan and getattr(plan, 'price', None) is not None:
                            pass_entry['amount_paid'] = float(plan.price)
                            pass_entry['currency'] = 'EUR'
                        items.append(pass_entry)
                        covered_user_ids.add(p.user_id)
                    except Exception as row_err:
                        logger.error(f"AdminSubscribersView row(pass) error: {row_err}")
                        continue
            except DatabaseError as access_pass_err:
                logger.warning(f"AdminSubscribersView pass query skipped (likely unmigrated): {access_pass_err}")
                # Pas de table (migrations non appliquées) -> ignorer silencieusement côté UI

            # Accès manuels accordés par un administrateur
            try:
                manual_qs = User.objects.filter(has_complimentary_access=True)
                for user in manual_qs:
                    try:
                        if user.id in covered_user_ids:
                            continue
                        if q:
                            if q not in (user.email or '').lower() and q not in (user.first_name or '').lower() and q not in (user.last_name or '').lower():
                                continue
                        manual_entry = {
                            'type': 'manual',
                            'user_id': user.id,
                            'email': getattr(user, 'email', ''),
                            'first_name': getattr(user, 'first_name', ''),
                            'last_name': getattr(user, 'last_name', ''),
                            'plan_id': None,
                            'plan_name': 'Accès manuel',
                            'plan_mode': 'manual',
                            'billing_period': None,
                            'status': 'manual',
                            'is_active': True,
                            'is_trial': False,
                            'days_remaining_trial': 0,
                            'current_period_start': iso_or_none(getattr(user, 'date_joined', None)),
                            'current_period_end': None,
                            'amount_paid': None,
                            'currency': None,
                        }
                        if active_only and not manual_entry['is_active']:
                            continue
                        items.append(manual_entry)
                        covered_user_ids.add(user.id)
                    except Exception as manual_err:
                        logger.error(f"AdminSubscribersView row(manual) error: {manual_err}")
                        continue
            except Exception as manual_qs_err:
                logger.warning(f"AdminSubscribersView manual list failed: {manual_qs_err}")

            # Tri: éléments actifs en premier, puis par date de fin croissante
            def key_fn(x):
                end = x.get('current_period_end') or x.get('ends_at') or ''
                return (0 if x.get('is_active') else 1, end)
            items.sort(key=key_fn)

            return JsonResponse({'items': items, 'total': len(items)})
        except Exception as e:
            logger.error(f"AdminSubscribersView.get error: {e}")
            # Ne pas bloquer l'UI admin: retourner une liste vide avec le message d'erreur
            return JsonResponse({'items': [], 'total': 0, 'error': str(e)}, status=200)


class AdminStripeSyncView(APIView):
    """Synchronise les abonnements Stripe → base locale (abonnements récurrents)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)

        try:
            synced, created, updated, skipped, created_plans = 0, 0, 0, 0, 0

            # Helper: ensure local plan exists from a Stripe price id
            def ensure_plan_from_price(price_id):
                nonlocal created_plans
                plan = SubscriptionPlan.objects.filter(stripe_price_id=price_id).first()
                if plan:
                    return plan
                try:
                    price = stripe.Price.retrieve(price_id, expand=['product'])
                except Exception as e:
                    logger.error(f"Cannot retrieve Stripe price {price_id}: {e}")
                    return None

                amount = price.get('unit_amount') or price.get('unit_amount_decimal') or 0
                try:
                    amount = Decimal(str(amount)) / Decimal('100')
                except Exception:
                    amount = Decimal('0')

                interval = (price.get('recurring') or {}).get('interval') or 'month'
                billing_period = 'monthly'
                if interval == 'year':
                    billing_period = 'yearly'
                elif interval == 'day':
                    billing_period = 'daily'
                elif interval == 'week':
                    billing_period = 'weekly'

                product_name = None
                try:
                    product = price.get('product')
                    if isinstance(product, dict):
                        product_name = product.get('name')
                except Exception:
                    product_name = None
                name = price.get('nickname') or product_name or f"Plan {price_id}"

                plan = SubscriptionPlan.objects.create(
                    name=name,
                    plan_type='basic',
                    billing_period=billing_period,
                    price=amount,
                    stripe_price_id=price_id,
                    features=[],
                    is_active=True,
                )
                # for compatibility with plan_mode/mode
                if hasattr(plan, 'plan_mode'):
                    plan.plan_mode = 'subscription'
                    plan.save()
                elif hasattr(plan, 'mode'):
                    setattr(plan, 'mode', 'subscription')
                    plan.save()
                created_plans += 1
                return plan

            def _from_timestamp(value):
                """Convert Stripe timestamp (seconds) to aware UTC datetime."""
                if not value:
                    return None
                try:
                    return datetime.fromtimestamp(value, tz=dt_timezone.utc)
                except Exception:
                    return None

            # Fetch subscriptions from Stripe with expansions for easier mapping
            # Some Stripe accounts reject unknown 'status' filters; omit for full list
            try:
                subs = stripe.Subscription.list(limit=100, expand=['data.customer', 'data.items.data.price.product'])
            except Exception as list_err:
                logger.warning(f"Stripe list with expand failed, falling back: {list_err}")
                subs = stripe.Subscription.list(limit=100)
            for s in subs.auto_paging_iter():
                try:
                    meta = getattr(s, 'metadata', None) or {}
                    user_id = meta.get('user_id')
                    plan_id_meta = meta.get('plan_id')

                    # Fallback: customer metadata or email → local user
                    customer_email = None
                    if getattr(s, 'customer', None):
                        try:
                            cust = s.customer if isinstance(s.customer, dict) else stripe.Customer.retrieve(s.customer)
                            customer_email = (cust.get('email') if isinstance(cust, dict) else getattr(cust, 'email', None)) or None
                            user_id = user_id or ((cust.get('metadata') or {}).get('user_id') if isinstance(cust, dict) else (getattr(cust, 'metadata', {}) or {}).get('user_id'))
                        except Exception:
                            pass

                    user = None
                    if user_id:
                        try:
                            user = User.objects.get(pk=int(user_id))
                        except Exception:
                            user = None
                    if user is None and customer_email:
                        try:
                            user = User.objects.filter(email__iexact=customer_email).first()
                        except Exception:
                            user = None
                    if user is None:
                        skipped += 1
                        continue

                    # Determine local plan
                    plan = None
                    if plan_id_meta:
                        try:
                            plan = SubscriptionPlan.objects.filter(pk=int(plan_id_meta)).first()
                        except Exception:
                            plan = None
                    if plan is None:
                        try:
                            price_id = s['items']['data'][0]['price']['id']
                        except Exception:
                            price_id = None
                        if price_id:
                            plan = ensure_plan_from_price(price_id)
                    if plan is None:
                        skipped += 1
                        continue

                    defaults = {
                        'plan': plan,
                        'stripe_subscription_id': s.id,
                        'stripe_customer_id': s.customer['id'] if isinstance(s.customer, dict) else s.customer,
                        'status': s.status,
                        'current_period_start': _from_timestamp(getattr(s, 'current_period_start', None)),
                        'current_period_end': _from_timestamp(getattr(s, 'current_period_end', None)),
                        'trial_end': _from_timestamp(getattr(s, 'trial_end', None)),
                    }

                    obj, was_created = UserSubscription.objects.update_or_create(
                        user=user,
                        defaults=defaults,
                    )
                    synced += 1
                    if was_created:
                        created += 1
                    else:
                        updated += 1
                except Exception as inner:
                    logger.error(f"Sync item error: {inner}")
                    skipped += 1

            return JsonResponse({'synced': synced, 'created': created, 'updated': updated, 'skipped': skipped, 'created_plans': created_plans})
        except Exception as e:
            logger.error(f"AdminStripeSyncView.post error: {e}")
            return JsonResponse({'detail': 'Server error', 'error': str(e)}, status=500)

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
        session = event['data']['object']
        # Si la session est un abonnement
        if session.get('subscription'):
            handle_checkout_session_completed(session)
        else:
            handle_checkout_session_payment_completed(session)
    
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


def handle_checkout_session_payment_completed(session):
    """Gérer la completion d'une session de checkout en mode paiement unique"""
    try:
        user_id = session['metadata']['user_id']
        plan_id = session['metadata']['plan_id']
        plan_mode = session['metadata'].get('plan_mode')

        if plan_mode != 'one_time':
            return

        user = User.objects.get(id=user_id)
        plan = SubscriptionPlan.objects.get(id=plan_id)

        # Déterminer la durée d'accès
        days = plan.access_days or 0
        start = timezone.now()
        ends = start + timedelta(days=days)

        # Créer le pass d'accès
        AccessPass.objects.create(
            user=user,
            plan=plan,
            starts_at=start,
            ends_at=ends,
            stripe_payment_intent_id=session.get('payment_intent')
        )

        # Journaliser le paiement
        amount_total = session.get('amount_total')  # en cents
        currency = (session.get('currency') or 'eur').upper()
        if amount_total:
            PaymentHistory.objects.create(
                user=user,
                stripe_payment_intent_id=session.get('payment_intent', ''),
                amount=(amount_total / 100.0),
                currency=currency,
                status='succeeded',
                description=f"Pass {plan.name} ({days} jours)"
            )
    except Exception as e:
        logger.error(f"Erreur dans handle_checkout_session_payment_completed: {e}")

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
