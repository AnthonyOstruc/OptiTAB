from __future__ import annotations

import logging

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from .models import AccessPass, PaymentHistory
from .stripe_client import stripe, stripe_error

logger = logging.getLogger(__name__)


REFUNDED_STATUSES = ("refunded", "partially_refunded")

# When Stripe says the payment intent is not refunded, we keep that result for a short time
# to avoid hitting Stripe on every request.
PASS_REFUND_CACHE_TTL_NOT_REFUNDED_SECONDS = 10 * 60

# When Stripe says a payment intent is refunded, keep it longer (it should not flip back).
PASS_REFUND_CACHE_TTL_REFUNDED_SECONDS = 24 * 60 * 60


def _refund_cache_key(payment_intent_id: str) -> str:
    return f"pass_refund_status:{payment_intent_id}"

def _should_skip_not_refunded_cache() -> bool:
    # In local dev, Stripe webhooks are often not forwarded; skipping checks for 10 minutes can
    # make refunds look "not applied". We therefore re-check Stripe even if we recently cached
    # "not_refunded" while DEBUG is on.
    return not bool(getattr(settings, "DEBUG", False))


def _refund_status_label(amount_refunded=None, amount_total=None) -> str:
    """Return a refund status label ('refunded' or 'partially_refunded')."""
    if amount_refunded is None:
        return "refunded"
    try:
        refunded_int = int(amount_refunded)
    except (TypeError, ValueError):
        return "refunded"
    try:
        total_int = int(amount_total) if amount_total is not None else None
    except (TypeError, ValueError):
        total_int = None
    if total_int and refunded_int < total_int:
        return "partially_refunded"
    return "refunded"


def stripe_refund_status_for_payment_intent(payment_intent_id: str):
    """Return (status|None, amount_refunded, amount_total).

    status:
      - 'refunded' / 'partially_refunded'
      - 'not_refunded'
      - None if Stripe is unavailable (do not block access in that case)
    """
    if not payment_intent_id:
        return None, None, None
    try:
        pi = stripe.PaymentIntent.retrieve(payment_intent_id)
        latest_charge_id = pi.get("latest_charge")
        if isinstance(latest_charge_id, dict):
            latest_charge_id = latest_charge_id.get("id")
        if not latest_charge_id:
            return "not_refunded", None, None

        charge = stripe.Charge.retrieve(latest_charge_id, expand=["refunds"])
        amount_total = charge.get("amount")
        amount_refunded = charge.get("amount_refunded") or 0
        refunds = (charge.get("refunds") or {}).get("data") or []
        if refunds and not amount_refunded:
            amount_refunded = sum((r.get("amount") or 0) for r in refunds) or amount_refunded
        refunded = bool(charge.get("refunded")) or bool(refunds) or (amount_refunded > 0)
        if not refunded:
            return "not_refunded", amount_refunded, amount_total
        return _refund_status_label(amount_refunded, amount_total), amount_refunded, amount_total
    except stripe_error.StripeError as exc:
        logger.warning(
            "Stripe refund check failed (payment_intent=%s): %s",
            payment_intent_id,
            exc,
        )
        return None, None, None


def _mark_payment_history_status(payment_intent_id: str, status: str) -> int:
    if not payment_intent_id or not status:
        return 0
    return (
        PaymentHistory.objects.filter(stripe_payment_intent_id=payment_intent_id)
        .exclude(status=status)
        .update(status=status)
    )


def revoke_pass_for_payment_intent(
    payment_intent_id: str,
    *,
    amount_refunded=None,
    amount_total=None,
) -> bool:
    """Revoke the AccessPass attached to a PaymentIntent and mark PaymentHistory refunded.

    Intended for webhook handlers / maintenance commands.
    Returns True if a pass exists for this payment intent (even if already revoked).
    """
    if not payment_intent_id:
        return False

    status = _refund_status_label(amount_refunded, amount_total)

    # Mark local history (if any) + cache the refunded status to avoid extra Stripe calls.
    _mark_payment_history_status(payment_intent_id, status)
    cache.set(
        _refund_cache_key(payment_intent_id),
        status,
        PASS_REFUND_CACHE_TTL_REFUNDED_SECONDS,
    )

    access_pass = (
        AccessPass.objects.select_related("user", "plan")
        .filter(stripe_payment_intent_id=payment_intent_id)
        .first()
    )
    if not access_pass:
        logger.info(
            "No AccessPass found for refunded payment_intent=%s (refund_status=%s)",
            payment_intent_id,
            status,
        )
        return False

    if access_pass.is_revoked:
        return True

    access_pass.revoke()
    logger.info(
        "Pass revoked (id=%s, user=%s, plan=%s, refund_status=%s, amount_refunded=%s)",
        access_pass.id,
        getattr(access_pass.user, "email", None) or access_pass.user_id,
        getattr(access_pass.plan, "name", None) or access_pass.plan_id,
        status,
        amount_refunded,
    )
    return True


def sync_refunded_passes(active_passes, *, max_stripe_checks: int = 3):
    """Revoke any refunded passes from a list of active passes.

    Uses, in order:
      1) Local PaymentHistory status (fast)
      2) Cached Stripe refund status (fast)
      3) Stripe API (limited) when needed

    Returns a list of passes that remain valid (not revoked).
    """
    passes = list(active_passes or [])
    if not passes:
        return []

    payment_intents = [
        p.stripe_payment_intent_id
        for p in passes
        if getattr(p, "stripe_payment_intent_id", None)
    ]

    statuses_by_intent = {}
    if payment_intents:
        statuses_by_intent = dict(
            PaymentHistory.objects.filter(stripe_payment_intent_id__in=payment_intents)
            .values_list("stripe_payment_intent_id", "status")
        )

    refunded_intents = {
        pi for pi, status in statuses_by_intent.items() if status in REFUNDED_STATUSES
    }

    for access_pass in passes:
        if access_pass.stripe_payment_intent_id in refunded_intents and not access_pass.is_revoked:
            access_pass.revoke()

    stripe_checks = 0
    for access_pass in passes:
        if access_pass.is_revoked:
            continue
        payment_intent_id = access_pass.stripe_payment_intent_id
        if not payment_intent_id:
            continue

        cache_key = _refund_cache_key(payment_intent_id)
        cached = cache.get(cache_key)

        if cached in REFUNDED_STATUSES:
            _mark_payment_history_status(payment_intent_id, cached)
            access_pass.revoke()
            continue

        if cached == "not_refunded" and _should_skip_not_refunded_cache():
            continue

        if stripe_checks >= max_stripe_checks:
            continue

        stripe_checks += 1
        stripe_status, _amount_refunded, _amount_total = stripe_refund_status_for_payment_intent(payment_intent_id)

        if stripe_status in REFUNDED_STATUSES:
            _mark_payment_history_status(payment_intent_id, stripe_status)
            cache.set(cache_key, stripe_status, PASS_REFUND_CACHE_TTL_REFUNDED_SECONDS)
            access_pass.revoke()
            continue

        if stripe_status == "not_refunded":
            cache.set(cache_key, stripe_status, PASS_REFUND_CACHE_TTL_NOT_REFUNDED_SECONDS)

    return [p for p in passes if not p.is_revoked]


def get_valid_active_passes_for_user(user, *, now=None, max_stripe_checks: int = 3):
    """Return the user's active (non-expired) passes, excluding refunded ones.

    This function also revokes refunded passes as a safety fallback.
    """
    if not user:
        return []
    now = now or timezone.now()
    active_passes = list(
        AccessPass.objects.filter(user=user, ends_at__gt=now, is_revoked=False)
        .select_related("plan")
        .order_by("-ends_at")
    )
    return sync_refunded_passes(active_passes, max_stripe_checks=max_stripe_checks)


def has_valid_active_pass(user, *, now=None) -> bool:
    """Return True if the user has a valid (non-refunded) active pass.

    We try to avoid Stripe calls. Stripe is only called when needed, and results are cached.
    """
    if not user:
        return False
    now = now or timezone.now()

    # IMPORTANT:
    # Do not trust the DB alone for refunds. Stripe refunds can happen asynchronously, and
    # webhooks might be delayed/missed. We therefore run a lightweight sync (with cache)
    # on a small set of candidate passes.
    candidates = list(
        AccessPass.objects.filter(user=user, ends_at__gt=now, is_revoked=False)
        .order_by("-ends_at")[:3]
    )
    if not candidates:
        return False

    remaining = sync_refunded_passes(candidates, max_stripe_checks=1)
    return bool(remaining)
