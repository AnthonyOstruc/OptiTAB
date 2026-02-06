from __future__ import annotations

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from subscriptions.models import AccessPass, PaymentHistory
from subscriptions.pass_access import (
    REFUNDED_STATUSES,
    revoke_pass_for_payment_intent,
    stripe_refund_status_for_payment_intent,
)


def _parse_date(value: str | None):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


class Command(BaseCommand):
    help = "Revoke AccessPass that has been refunded in Stripe."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=365)
        parser.add_argument("--since", type=str, default=None)
        parser.add_argument("--until", type=str, default=None)
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--payment-intent", type=str, default=None)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        days = options.get("days")
        since_raw = options.get("since")
        until_raw = options.get("until")
        limit = int(options.get("limit") or 0)
        payment_intent = options.get("payment_intent")
        dry_run = bool(options.get("dry_run"))

        now = timezone.now()
        since = _parse_date(since_raw)
        until = _parse_date(until_raw)

        if since:
            since = timezone.make_aware(since) if timezone.is_naive(since) else since
        elif days and days > 0:
            since = now - timedelta(days=days)

        if until:
            until = timezone.make_aware(until) if timezone.is_naive(until) else until

        qs = AccessPass.objects.filter(is_revoked=False, stripe_payment_intent_id__isnull=False)

        if payment_intent:
            qs = qs.filter(stripe_payment_intent_id=payment_intent)
        if since:
            qs = qs.filter(created_at__gte=since)
        if until:
            qs = qs.filter(created_at__lte=until)

        qs = qs.order_by("-created_at")
        if limit and limit > 0:
            qs = qs[:limit]

        total = qs.count() if hasattr(qs, "count") else len(list(qs))
        self.stdout.write(f"Scanning {total} pass records...")

        revoked = 0
        skipped = 0
        already_refunded = 0
        stripe_errors = 0

        for access_pass in qs:
            payment_intent_id = access_pass.stripe_payment_intent_id
            if not payment_intent_id:
                skipped += 1
                continue

            payment = (
                PaymentHistory.objects
                .filter(stripe_payment_intent_id=payment_intent_id)
                .only("status")
                .first()
            )

            if payment and (payment.status in REFUNDED_STATUSES):
                already_refunded += 1
                if not dry_run:
                    revoke_pass_for_payment_intent(payment_intent_id)
                    revoked += 1
                continue

            stripe_status, amount_refunded, amount_total = stripe_refund_status_for_payment_intent(payment_intent_id)
            if stripe_status is None:
                stripe_errors += 1
                continue

            if stripe_status == "not_refunded":
                skipped += 1
                continue

            if not dry_run:
                revoke_pass_for_payment_intent(
                    payment_intent_id,
                    amount_refunded=amount_refunded,
                    amount_total=amount_total,
                )
            revoked += 1

        self.stdout.write(
            "Done. revoked=%s, already_refunded=%s, skipped=%s, stripe_errors=%s, dry_run=%s"
            % (revoked, already_refunded, skipped, stripe_errors, dry_run)
        )
