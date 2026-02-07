from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from subscriptions.handlers import handle_charge_refunded, handle_refund_event
from subscriptions.models import AccessPass, PaymentHistory, SubscriptionPlan
from subscriptions.pass_access import has_valid_active_pass, revoke_pass_for_payment_intent
from subscriptions.stripe_client import stripe_error


class RefundPassTests(TestCase):
    def _setup_pass(self, *, payment_intent_id: str):
        User = get_user_model()
        user = User.objects.create_user(
            email=f"{payment_intent_id}@example.com",
            first_name="Test",
            last_name="User",
            password="test-password",
            is_active=True,
        )

        plan = SubscriptionPlan.objects.create(
            name="Pass test",
            plan_type="basic",
            plan_mode="one_time",
            billing_period="daily",
            price=Decimal("1.00"),
            stripe_price_id=f"price_{payment_intent_id}",
            features=[],
            access_days=1,
            is_active=True,
        )

        starts_at = timezone.now()
        ends_at = starts_at + timedelta(days=1)

        access_pass = AccessPass.objects.create(
            user=user,
            plan=plan,
            starts_at=starts_at,
            ends_at=ends_at,
            stripe_payment_intent_id=payment_intent_id,
        )

        payment = PaymentHistory.objects.create(
            user=user,
            stripe_payment_intent_id=payment_intent_id,
            amount=Decimal("1.00"),
            currency="EUR",
            status="succeeded",
            description="Pass test",
            plan_name=plan.name,
            plan_mode="one_time",
            period_start=starts_at,
            period_end=ends_at,
        )

        return user, plan, access_pass, payment

    def test_revoke_pass_for_payment_intent_revokes_and_marks_payment_refunded(self):
        payment_intent_id = "pi_test_refund_full"
        _user, _plan, access_pass, payment = self._setup_pass(payment_intent_id=payment_intent_id)

        found = revoke_pass_for_payment_intent(
            payment_intent_id,
            amount_refunded=1000,
            amount_total=1000,
        )
        self.assertTrue(found)

        access_pass.refresh_from_db()
        payment.refresh_from_db()

        self.assertTrue(access_pass.is_revoked)
        self.assertIsNotNone(access_pass.revoked_at)
        self.assertEqual(payment.status, "refunded")

    def test_handle_charge_refunded_revokes_pass(self):
        payment_intent_id = "pi_test_charge_refunded"
        _user, _plan, access_pass, payment = self._setup_pass(payment_intent_id=payment_intent_id)

        handle_charge_refunded(
            {
                "id": "ch_test_1",
                "payment_intent": payment_intent_id,
                "amount": 1000,
                "amount_refunded": 1000,
                "refunded": True,
            }
        )

        access_pass.refresh_from_db()
        payment.refresh_from_db()

        self.assertTrue(access_pass.is_revoked)
        self.assertEqual(payment.status, "refunded")

    def test_handle_refund_event_revokes_pass_and_marks_partially_refunded(self):
        payment_intent_id = "pi_test_refund_partial"
        _user, _plan, access_pass, payment = self._setup_pass(payment_intent_id=payment_intent_id)

        handle_refund_event(
            {
                "id": "re_test_1",
                "status": "succeeded",
                "payment_intent": payment_intent_id,
                "amount": 500,
                "charge": {
                    "id": "ch_test_2",
                    "payment_intent": payment_intent_id,
                    "amount": 1000,
                    "amount_refunded": 500,
                },
            }
        )

        access_pass.refresh_from_db()
        payment.refresh_from_db()

        self.assertTrue(access_pass.is_revoked)
        self.assertEqual(payment.status, "partially_refunded")

    def test_revoke_pass_is_idempotent(self):
        payment_intent_id = "pi_test_idempotent"
        _user, _plan, access_pass, payment = self._setup_pass(payment_intent_id=payment_intent_id)

        revoke_pass_for_payment_intent(payment_intent_id, amount_refunded=1000, amount_total=1000)
        access_pass.refresh_from_db()
        payment.refresh_from_db()
        revoked_at_first = access_pass.revoked_at
        self.assertTrue(access_pass.is_revoked)
        self.assertEqual(payment.status, "refunded")

        revoke_pass_for_payment_intent(payment_intent_id, amount_refunded=1000, amount_total=1000)
        access_pass.refresh_from_db()

        self.assertTrue(access_pass.is_revoked)
        self.assertEqual(access_pass.revoked_at, revoked_at_first)

    def test_has_valid_active_pass_revokes_when_stripe_reports_refunded(self):
        from unittest.mock import patch

        payment_intent_id = "pi_test_stripe_fallback_refund"
        user, _plan, access_pass, payment = self._setup_pass(payment_intent_id=payment_intent_id)

        with patch(
            "subscriptions.pass_access.stripe.PaymentIntent.retrieve",
            return_value={"latest_charge": "ch_test_123"},
        ), patch(
            "subscriptions.pass_access.stripe.Charge.retrieve",
            return_value={
                "amount": 1000,
                "amount_refunded": 1000,
                "refunded": True,
                "refunds": {"data": [{"amount": 1000}]},
            },
        ):
            self.assertFalse(has_valid_active_pass(user))

        access_pass.refresh_from_db()
        payment.refresh_from_db()
        self.assertTrue(access_pass.is_revoked)
        self.assertEqual(payment.status, "refunded")

    def test_has_valid_active_pass_does_not_block_when_stripe_unavailable(self):
        from unittest.mock import patch

        payment_intent_id = "pi_test_stripe_unavailable"
        user, _plan, access_pass, payment = self._setup_pass(payment_intent_id=payment_intent_id)

        with patch(
            "subscriptions.pass_access.stripe.PaymentIntent.retrieve",
            side_effect=stripe_error.StripeError("stripe down"),
        ):
            self.assertTrue(has_valid_active_pass(user))

        access_pass.refresh_from_db()
        payment.refresh_from_db()
        self.assertFalse(access_pass.is_revoked)
        self.assertEqual(payment.status, "succeeded")
