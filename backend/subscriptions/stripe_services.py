import logging
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import SubscriptionPlan, UserSubscription, PaymentHistory
from pays.models import Niveau
from .stripe_client import stripe, stripe_error
from .helpers import (
    _append_level_to_description,
    _build_plan_payload,
    _extract_invoice_period,
    _extract_level_from_invoice,
    _extract_price_from_stripe_subscription,
    _fetch_niveau_by_id,
    _format_level_label_from_obj,
    _from_timestamp,
    _is_stripe_subscription_active,
    _level_label_from_metadata,
    _map_stripe_status,
    _stripe_obj_to_dict,
)

logger = logging.getLogger(__name__)
User = get_user_model()

STRIPE_INVOICE_CUSTOM_FIELDS_MAX = 4
STRIPE_TEMP_CUSTOM_FIELD_NAMES = ('Niveau', 'Bénéficiaire')


def _sanitize_stripe_custom_field_value(value: str, limit: int) -> str:
    return (value or '').strip().replace('\n', ' ')[:limit]


def _merge_stripe_custom_fields(existing_fields, requested_fields, max_fields=STRIPE_INVOICE_CUSTOM_FIELDS_MAX):
    """Merge/upsert Stripe custom_fields while preserving order and constraints."""
    if not isinstance(existing_fields, list):
        existing_fields = []

    normalized_existing = []
    existing_by_name = {}
    for field in existing_fields:
        if not isinstance(field, dict):
            continue
        name = str(field.get('name') or '').strip()
        value = str(field.get('value') or '').strip()
        if not name:
            continue
        if name not in existing_by_name:
            normalized_existing.append(name)
        existing_by_name[name] = value

    merged = []
    used = set()

    # Keep existing order first, upserting requested values when matching.
    for name in normalized_existing:
        if name in used:
            continue
        value = existing_by_name.get(name, '')
        for req_name, req_value in requested_fields:
            if req_name == name and req_value:
                value = req_value
        merged.append({
            'name': _sanitize_stripe_custom_field_value(name, 40),
            'value': _sanitize_stripe_custom_field_value(value, 140),
        })
        used.add(name)

    # Append requested fields that are not present yet.
    for name, value in requested_fields:
        if not value or name in used:
            continue
        if len(merged) >= max_fields:
            break
        merged.append({
            'name': _sanitize_stripe_custom_field_value(name, 40),
            'value': _sanitize_stripe_custom_field_value(value, 140),
        })
        used.add(name)

    return merged[:max_fields]


def _prime_customer_invoice_custom_fields(customer_id, metadata):
    """Set temporary customer-level invoice custom fields so the very first invoice includes them."""
    if not customer_id:
        return
    try:
        niveau_label = (_level_label_from_metadata(metadata) or '').strip()
        is_gift = str((metadata or {}).get('is_gift') or '').lower() == 'true'
        beneficiary_email = ((metadata or {}).get('beneficiary_email') or '').strip()
        beneficiary_name = ((metadata or {}).get('beneficiary_name') or '').strip()

        requested = []
        if niveau_label:
            requested.append(('Niveau', niveau_label))
        if is_gift and (beneficiary_name or beneficiary_email):
            # Format: "Nom Prénom" sur une ligne, email sur la ligne suivante
            beneficiary_display = beneficiary_name or beneficiary_email
            if beneficiary_name and beneficiary_email:
                beneficiary_display = f"{beneficiary_name}\n{beneficiary_email}"[:140]
            requested.append(('Bénéficiaire', beneficiary_display))
        if not requested:
            return

        customer = stripe.Customer.retrieve(customer_id)
        customer_data = _stripe_obj_to_dict(customer)
        existing = ((customer_data.get('invoice_settings') or {}).get('custom_fields') or [])
        merged = _merge_stripe_custom_fields(existing, requested)
        if merged == existing:
            return
        stripe.Customer.modify(customer_id, invoice_settings={'custom_fields': merged})
    except stripe_error.StripeError as exc:
        logger.warning("Impossible de préparer les custom_fields client Stripe (%s): %s", customer_id, exc)


def _clear_customer_temp_invoice_custom_fields(customer_id, names=STRIPE_TEMP_CUSTOM_FIELD_NAMES):
    """Remove only OptiTAB temporary fields from customer.invoice_settings.custom_fields."""
    if not customer_id:
        return
    try:
        customer = stripe.Customer.retrieve(customer_id)
        customer_data = _stripe_obj_to_dict(customer)
        existing = ((customer_data.get('invoice_settings') or {}).get('custom_fields') or [])
        if not isinstance(existing, list) or not existing:
            return
        names_set = set(names or [])
        filtered = [
            field for field in existing
            if isinstance(field, dict) and str(field.get('name') or '').strip() not in names_set
        ]
        if filtered == existing:
            return
        stripe.Customer.modify(customer_id, invoice_settings={'custom_fields': filtered})
    except stripe_error.StripeError as exc:
        logger.warning("Impossible de nettoyer les custom_fields client Stripe (%s): %s", customer_id, exc)


def _hydrate_payment_history_invoice(payment_history):
    """Assure la présence des URLs de facture en rafraîchissant depuis Stripe si nécessaire."""
    if payment_history.invoice_pdf_url and payment_history.hosted_invoice_url:
        return payment_history.invoice_pdf_url, payment_history.hosted_invoice_url

    invoice_id = _resolve_invoice_id_from_payment_history(payment_history)

    if not invoice_id:
        return payment_history.invoice_pdf_url, payment_history.hosted_invoice_url

    try:
        invoice = stripe.Invoice.retrieve(invoice_id)
        _update_payment_history_urls(payment_history, invoice)
    except stripe_error.StripeError as exc:
        logger.warning(f"Impossible de récupérer la facture Stripe {invoice_id}: {exc}")

    return payment_history.invoice_pdf_url, payment_history.hosted_invoice_url


def _resolve_invoice_id_from_payment_history(payment_history):
    """Résout l'ID de facture depuis un PaymentHistory."""
    invoice_id = payment_history.stripe_invoice_id
    if invoice_id:
        return invoice_id

    payment_intent_id = payment_history.stripe_payment_intent_id
    if not payment_intent_id:
        return None

    try:
        pi = stripe.PaymentIntent.retrieve(payment_intent_id, expand=['invoice'])
        latest_charge_id = pi.get('latest_charge') or ''
        invoice_ref = pi.get('invoice')
        
        if invoice_ref:
            if isinstance(invoice_ref, str):
                invoice_data = stripe.Invoice.retrieve(invoice_ref)
            else:
                invoice_data = invoice_ref
            invoice_id = invoice_data.get('id')
            payment_history.stripe_invoice_id = invoice_id
            payment_history.save(update_fields=['stripe_invoice_id'])
            return invoice_id

        # Fallback: utiliser le reçu de charge
        if latest_charge_id:
            _try_update_hosted_url_from_charge(payment_history, latest_charge_id)
            
    except stripe_error.StripeError as exc:
        logger.warning(f"Impossible de récupérer PaymentIntent {payment_intent_id}: {exc}")

    return None


def _try_update_hosted_url_from_charge(payment_history, charge_id):
    """Tente de récupérer l'URL du reçu depuis une charge Stripe."""
    try:
        charge = stripe.Charge.retrieve(charge_id)
        receipt_url = charge.get('receipt_url') or ''
        if receipt_url and not payment_history.hosted_invoice_url:
            payment_history.hosted_invoice_url = receipt_url
            payment_history.save(update_fields=['hosted_invoice_url'])
    except stripe_error.StripeError as exc:
        logger.warning(f"Impossible de récupérer le reçu Stripe {charge_id}: {exc}")


def _update_payment_history_urls(payment_history, invoice):
    """Met à jour les URLs de facture depuis un objet Invoice Stripe."""
    updated_fields = []
    invoice_pdf = invoice.get('invoice_pdf') or ''
    hosted_url = invoice.get('hosted_invoice_url') or ''
    
    if invoice_pdf and invoice_pdf != payment_history.invoice_pdf_url:
        payment_history.invoice_pdf_url = invoice_pdf
        updated_fields.append('invoice_pdf_url')
    if hosted_url and hosted_url != payment_history.hosted_invoice_url:
        payment_history.hosted_invoice_url = hosted_url
        updated_fields.append('hosted_invoice_url')
    
    if updated_fields:
        payment_history.save(update_fields=updated_fields)


def _apply_stripe_subscription_updates(subscription, stripe_data):
    """Applique les mises à jour depuis les données Stripe à un abonnement local.
    
    Retourne la liste des champs mis à jour.
    """
    updated_fields = []
    
    updates = [
        ('current_period_start', _from_timestamp(stripe_data.get('current_period_start'))),
        ('current_period_end', _from_timestamp(stripe_data.get('current_period_end'))),
        ('trial_end', _from_timestamp(stripe_data.get('trial_end'))),
        ('status', _map_stripe_status(stripe_data.get('status'))),
        ('cancel_at_period_end', bool(stripe_data.get('cancel_at_period_end'))),
    ]
    
    for field, value in updates:
        if value is None:
            continue
        current = getattr(subscription, field)
        if value != current:
            setattr(subscription, field, value)
            updated_fields.append(field)
    
    if updated_fields:
        if 'updated_at' not in updated_fields:
            updated_fields.append('updated_at')
        subscription.save(update_fields=updated_fields)
    
    return updated_fields


def _refresh_subscription_from_stripe(subscription):
    """
    Garantit que les dates clés (début/fin de période, fin d'essai, statut)
    sont renseignées pour un abonnement persisté localement.
    """
    if not subscription or not subscription.stripe_subscription_id:
        return subscription

    needs_period = not subscription.current_period_start or not subscription.current_period_end
    needs_trial = subscription.status == 'trialing' and not subscription.trial_end
    if not needs_period and not needs_trial:
        return subscription

    try:
        stripe_sub = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
        _apply_stripe_subscription_updates(subscription, stripe_sub)
    except stripe_error.InvalidRequestError as exc:
        logger.warning(
            "Stripe subscription %s introuvable pour hydratation: %s",
            subscription.stripe_subscription_id,
            exc,
        )
    except stripe_error.StripeError as exc:
        logger.warning(
            "Impossible de rafraîchir l'abonnement Stripe %s: %s",
            subscription.stripe_subscription_id,
            exc,
        )

    return subscription


def _refresh_subscription_from_snapshot(subscription, stripe_snapshot):
    """
    Met à jour un abonnement local à partir d'un snapshot Stripe déjà chargé.
    Utilisé pour refléter rapidement les annulations faites côté Stripe.
    """
    if not subscription or not stripe_snapshot:
        return subscription

    _apply_stripe_subscription_updates(subscription, stripe_snapshot)
    return subscription


def _sync_level_subscriptions_from_stripe(user, niveau_obj):
    """
    Met à jour les abonnements d'un utilisateur pour un niveau donné
    en se synchronisant avec Stripe (utilisé pour éviter les blocages
    quand un abonnement a été annulé côté Stripe).
    """
    if not user or not niveau_obj:
        return []

    subs = list(
        UserSubscription.objects.filter(user=user, niveau_pays=niveau_obj)
    )
    for sub in subs:
        stripe_id = sub.stripe_subscription_id
        if not stripe_id:
            continue
        try:
            stripe_sub = stripe.Subscription.retrieve(stripe_id)
            stripe_snapshot = _stripe_obj_to_dict(stripe_sub)
            _refresh_subscription_from_snapshot(sub, stripe_snapshot)
        except stripe_error.InvalidRequestError:
            # Abonnement Stripe introuvable -> marquer comme annulé localement
            updated_fields = []
            if sub.status != 'canceled':
                sub.status = 'canceled'
                updated_fields.append('status')
            if sub.cancel_at_period_end:
                sub.cancel_at_period_end = False
                updated_fields.append('cancel_at_period_end')
            if not sub.current_period_end or sub.current_period_end > timezone.now():
                sub.current_period_end = timezone.now()
                updated_fields.append('current_period_end')
            if updated_fields:
                if 'updated_at' not in updated_fields:
                    updated_fields.append('updated_at')
                sub.save(update_fields=updated_fields)
        except stripe_error.StripeError as exc:
            logger.warning(
                "Stripe sync failed for subscription %s (user=%s): %s",
                stripe_id,
                getattr(user, 'id', None),
                exc
            )
            continue

    return subs


def _build_gifted_subscriptions_from_stripe(stripe_subscriptions, current_user):
    """Construit la liste des abonnements offerts par l'utilisateur courant."""
    if not stripe_subscriptions or not current_user:
        return []

    current_user_id = str(current_user.id)
    gift_entries = []
    beneficiary_ids = set()

    for stripe_sub in stripe_subscriptions:
        metadata = stripe_sub.get('metadata') or {}
        payer_id = metadata.get('payer_user_id')
        beneficiary_id = metadata.get('user_id')
        if not payer_id or str(payer_id) != current_user_id:
            continue
        if beneficiary_id and str(beneficiary_id) == current_user_id:
            continue
        gift_entries.append((stripe_sub, metadata))
        if beneficiary_id:
            try:
                beneficiary_ids.add(int(beneficiary_id))
            except (TypeError, ValueError):
                pass

    beneficiary_lookup = {}
    if beneficiary_ids:
        try:
            beneficiary_lookup = {
                u.id: u for u in User.objects.filter(id__in=beneficiary_ids)
            }
        except Exception:
            beneficiary_lookup = {}

    gifted_payloads = []
    for stripe_sub, metadata in gift_entries:
        beneficiary_id = metadata.get('user_id')
        beneficiary_obj = None
        if beneficiary_id:
            try:
                beneficiary_obj = beneficiary_lookup.get(int(beneficiary_id))
            except (TypeError, ValueError):
                beneficiary_obj = None

        beneficiary_email = (
            metadata.get('beneficiary_email') or
            getattr(beneficiary_obj, 'email', None)
        )
        beneficiary_first = getattr(beneficiary_obj, 'first_name', '') if beneficiary_obj else ''
        beneficiary_last = getattr(beneficiary_obj, 'last_name', '') if beneficiary_obj else ''
        beneficiary_display = ' '.join([p for p in [beneficiary_first, beneficiary_last] if p]).strip()

        niveau_id = metadata.get('niveau_pays_id')
        niveau_obj = _fetch_niveau_by_id(niveau_id) if niveau_id else None
        niveau_payload = None
        if niveau_obj:
            niveau_payload = {
                'id': niveau_obj.id,
                'nom': niveau_obj.nom,
                'pays': {
                    'id': niveau_obj.pays.id,
                    'nom': niveau_obj.pays.nom,
                    'drapeau_emoji': getattr(niveau_obj.pays, 'drapeau_emoji', None)
                } if getattr(niveau_obj, 'pays', None) else None
            }

        plan_obj = None
        plan_id = metadata.get('plan_id')
        if plan_id:
            try:
                plan_obj = SubscriptionPlan.objects.filter(id=int(plan_id)).first()
            except (TypeError, ValueError):
                plan_obj = None
        if not plan_obj:
            price_id = None
            try:
                items = stripe_sub.get('items', {}).get('data', [])
                if items:
                    price_id = items[0].get('price', {}).get('id')
            except Exception:
                price_id = None
            if price_id:
                plan_obj = SubscriptionPlan.objects.filter(stripe_price_id=price_id).first()

        stripe_price = _extract_price_from_stripe_subscription(stripe_sub)
        plan_payload = _build_plan_payload(plan_obj, stripe_price, stripe_sub)

        status = _map_stripe_status(stripe_sub.get('status'))
        start_dt = _from_timestamp(stripe_sub.get('current_period_start'))
        end_dt = _from_timestamp(stripe_sub.get('current_period_end'))
        trial_dt = _from_timestamp(stripe_sub.get('trial_end'))
        started_dt = _from_timestamp(stripe_sub.get('start_date')) or start_dt

        gifted_payloads.append({
            'stripe_subscription_id': stripe_sub.get('id'),
            'status': status,
            'is_active': _is_stripe_subscription_active(stripe_sub),
            'is_trial': status == 'trialing',
            'cancel_at_period_end': bool(stripe_sub.get('cancel_at_period_end')),
            'current_period_start': start_dt.isoformat() if start_dt else None,
            'current_period_end': end_dt.isoformat() if end_dt else None,
            'trial_end': trial_dt.isoformat() if trial_dt else None,
            'started_at': started_dt.isoformat() if started_dt else None,
            'beneficiary': {
                'id': getattr(beneficiary_obj, 'id', None),
                'first_name': beneficiary_first or '',
                'last_name': beneficiary_last or '',
                'email': beneficiary_email,
                'display_name': beneficiary_display or beneficiary_email or ''
            },
            'plan': plan_payload,
            'niveau': niveau_payload
        })

    return gifted_payloads


def _get_stripe_customer_id(user):
    if not user:
        return None
    try:
        customer_id = getattr(user, 'stripe_customer_id', None)
        if customer_id:
            return customer_id
    except Exception:
        pass

    try:
        subscription = user.subscription
        if subscription and subscription.stripe_customer_id:
            return subscription.stripe_customer_id
    except Exception:
        pass

    subs_manager = getattr(user, 'subscriptions', None)
    if subs_manager is not None:
        sub = subs_manager.filter(stripe_customer_id__isnull=False).order_by('-created_at').first()
        if sub:
            return sub.stripe_customer_id
    return None


def _create_stripe_customer(user):
    customer = stripe.Customer.create(
        email=user.email,
        name=f"{user.first_name} {user.last_name}",
        metadata={'user_id': user.id}
    )
    customer_id = customer.id
    try:
        if hasattr(user, 'stripe_customer_id') and user.stripe_customer_id != customer_id:
            user.stripe_customer_id = customer_id
            user.save(update_fields=['stripe_customer_id'])
    except Exception:
        pass
    return customer_id


def _list_stripe_subscriptions(user, limit=50):
    customer_id = _get_stripe_customer_id(user)
    if not customer_id:
        return []
    try:
        data = stripe.Subscription.list(
            customer=customer_id,
            status='all',
            limit=limit,
            expand=['data.items.data.price', 'data.latest_invoice', 'data.plan.product']
        )
        return list(getattr(data, 'data', []) or [])
    except stripe_error.StripeError as exc:
        logger.warning(f"Unable to list Stripe subscriptions for user {user.id}: {exc}")
        return []


def _sync_payment_history_from_stripe(user, limit=12):
    """
    S'assure que les factures Stripe récentes existent dans PaymentHistory.
    Permet de combler les écarts (par ex. si un webhook n'a pas été reçu).
    """
    try:
        subscription = user.subscription
    except (UserSubscription.DoesNotExist, AttributeError):
        subscription = None
    except Exception:
        subscription = None

    customer_id = getattr(subscription, 'stripe_customer_id', None)
    if not customer_id:
        customer_id = getattr(user, 'stripe_customer_id', None)
    if not customer_id:
        return 0

    # Préparer une table de correspondance stripe_subscription_id -> UserSubscription
    subscriptions_map = {}
    try:
        subs_qs = (
            UserSubscription.objects
            .filter(user=user, stripe_subscription_id__isnull=False)
            .select_related('plan', 'niveau_pays', 'niveau_pays__pays')
        )
        for sub in subs_qs:
            subscriptions_map[sub.stripe_subscription_id] = sub
    except Exception:
        subs_qs = []

    try:
        total_target = int(limit or 12)
    except (TypeError, ValueError):
        total_target = 12
    total_target = max(1, min(total_target, 500))

    synced = 0
    default_plan_name = getattr(getattr(subscription, 'plan', None), 'name', 'OptiTAB')
    fetched = 0
    starting_after = None

    while fetched < total_target:
        page_limit = min(100, total_target - fetched)
        params = {
            'customer': customer_id,
            'limit': page_limit,
            'expand': ['data.lines']
        }
        if starting_after:
            params['starting_after'] = starting_after

        try:
            stripe_invoices = stripe.Invoice.list(**params)
        except stripe_error.StripeError as exc:
            logger.warning(f"Stripe invoice sync failed for user {user.id}: {exc}")
            break

        data = getattr(stripe_invoices, 'data', None) or []
        if not data:
            break

        for invoice in data:
            invoice_id = invoice.get('id')
            if not invoice_id:
                continue

            payment_intent_id = invoice.get('payment_intent') or f'invoice_{invoice_id}'
            invoice_metadata = invoice.get('metadata') or {}
            stripe_sub_id = invoice.get('subscription')
            linked_subscription = subscriptions_map.get(stripe_sub_id)
            niveau_obj = None
            niveau_id = invoice_metadata.get('niveau_pays_id')
            if niveau_id:
                niveau_obj = _fetch_niveau_by_id(niveau_id)
            level_label = _level_label_from_metadata(invoice_metadata)

            extracted_label, extracted_niveau = _extract_level_from_invoice(invoice)
            if extracted_niveau and not niveau_obj:
                niveau_obj = extracted_niveau
            if extracted_label:
                level_label = extracted_label

            if not level_label:
                niveau_fallback = getattr(linked_subscription, 'niveau_pays', None) or getattr(subscription, 'niveau_pays', None)
                level_label = _format_level_label_from_obj(niveau_fallback)
            plan_source = linked_subscription or subscription
            plan_obj = getattr(plan_source, 'plan', None)
            plan_name = (
                invoice_metadata.get('plan_name') or
                getattr(plan_obj, 'name', None) or
                default_plan_name
            )
            if (not invoice_metadata.get('plan_name')):
                line_description = None
                lines = (invoice.get('lines') or {}).get('data') or []
                if lines:
                    line_description = lines[0].get('description')
                if line_description:
                    cleaned = line_description.split('(')[0]
                    cleaned = cleaned.replace('1 ×', '').strip()
                    if cleaned:
                        plan_name = cleaned
            plan_mode = invoice_metadata.get('plan_mode') or (invoice_metadata.get('mode'))
            if not plan_mode:
                plan_mode = 'subscription' if stripe_sub_id else 'one_time'
            niveau_obj = (
                niveau_obj or
                getattr(linked_subscription, 'niveau_pays', None) or
                getattr(subscription, 'niveau_pays', None)
            )
            if plan_mode == 'one_time':
                base_description = invoice.get('description') or f"Pass {plan_name}"
            else:
                base_description = invoice.get('description') or f"Paiement pour {plan_name}"
            period_start, period_end = _extract_invoice_period(invoice)

            defaults = {
                'stripe_payment_intent_id': payment_intent_id,
                'hosted_invoice_url': (invoice.get('hosted_invoice_url') or ''),
                'invoice_pdf_url': (invoice.get('invoice_pdf') or ''),
                'amount': ((invoice.get('amount_paid') or invoice.get('total') or 0) / 100.0),
                'currency': (invoice.get('currency') or 'EUR').upper(),
                'status': invoice.get('status') or 'paid',
                'description': _append_level_to_description(base_description, level_label),
                'niveau_label': level_label or '',
                'niveau_pays': niveau_obj,
                'plan_name': plan_name or '',
                'plan_mode': plan_mode,
                'period_start': period_start,
                'period_end': period_end,
            }

            payment_history, created = PaymentHistory.objects.get_or_create(
                user=user,
                stripe_invoice_id=invoice_id,
                defaults=defaults
            )

            if created:
                synced += 1
                continue

            niveau_info_available = bool(niveau_id) or bool(level_label)
            updated_fields = []
            for field, value in defaults.items():
                if field == 'niveau_pays' and not niveau_info_available:
                    continue
                if field == 'niveau_label' and not niveau_info_available:
                    continue
                current_value = getattr(payment_history, field)
                if field == 'niveau_pays':
                    current_id = current_value.id if current_value else None
                    value_id = value.id if value else None
                    if current_id != value_id:
                        setattr(payment_history, field, value)
                        updated_fields.append(field)
                    continue
                if current_value != value:
                    setattr(payment_history, field, value)
                    updated_fields.append(field)

            if updated_fields:
                payment_history.save(update_fields=updated_fields)

        fetched += len(data)
        if not getattr(stripe_invoices, 'has_more', False):
            break
        starting_after = data[-1].id

    return synced


__all__ = [
    'STRIPE_INVOICE_CUSTOM_FIELDS_MAX',
    'STRIPE_TEMP_CUSTOM_FIELD_NAMES',
    '_clear_customer_temp_invoice_custom_fields',
    '_prime_customer_invoice_custom_fields',
    '_sanitize_stripe_custom_field_value',
    '_merge_stripe_custom_fields',
    '_hydrate_payment_history_invoice',
    '_refresh_subscription_from_stripe',
    '_refresh_subscription_from_snapshot',
    '_sync_level_subscriptions_from_stripe',
    '_build_gifted_subscriptions_from_stripe',
    '_get_stripe_customer_id',
    '_create_stripe_customer',
    '_list_stripe_subscriptions',
    '_sync_payment_history_from_stripe',
]
