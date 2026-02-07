from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone

from subscriptions.models import AccessPass, PaymentHistory, SubscriptionPlan
from subscriptions.stripe_client import stripe_error
from subscriptions.subscription_status import build_subscription_status


class GiftedPassRefundVisibilityTests(TestCase):
    def setUp(self):
        super().setUp()
        cache.clear()

    def _create_user(self, *, tag: str, role: str = "student"):
        User = get_user_model()
        return User.objects.create_user(
            email=f"{tag}@example.com",
            first_name="Test",
            last_name="User",
            password="test-password",
            role=role,
            is_active=True,
        )

    def _create_pass_plan(self, *, tag: str):
        return SubscriptionPlan.objects.create(
            name="Pass 1 jour",
            plan_type="basic",
            plan_mode="one_time",
            billing_period="daily",
            price=Decimal("3.99"),
            stripe_price_id=f"price_pass_refund_{tag}",
            features=[],
            access_days=1,
            is_active=True,
        )

    def _create_parent_payment_and_child_pass(
        self,
        *,
        parent,
        child,
        plan,
        payment_intent_id: str,
    ):
        now = timezone.now()
        payment = PaymentHistory.objects.create(
            user=parent,
            stripe_payment_intent_id=payment_intent_id,
            amount=Decimal("3.99"),
            currency="EUR",
            status="succeeded",
            description="Pass cadeau",
            plan_name=plan.name,
            plan_mode="one_time",
            period_start=now - timedelta(hours=1),
            period_end=now + timedelta(hours=23),
        )
        access_pass = AccessPass.objects.create(
            user=child,
            plan=plan,
            starts_at=now - timedelta(hours=1),
            ends_at=now + timedelta(hours=23),
            stripe_payment_intent_id=payment_intent_id,
            is_revoked=False,
        )
        return payment, access_pass

    def test_non_refunded_gifted_pass_remains_visible(self):
        parent = self._create_user(tag="gifted-pass-parent-visible", role="parent")
        child = self._create_user(tag="gifted-pass-child-visible")
        plan = self._create_pass_plan(tag="visible")
        payment_intent_id = "pi_gifted_pass_visible"
        payment, access_pass = self._create_parent_payment_and_child_pass(
            parent=parent,
            child=child,
            plan=plan,
            payment_intent_id=payment_intent_id,
        )

        with patch(
            "subscriptions.subscription_status._list_stripe_subscriptions",
            return_value=[],
        ), patch(
            "subscriptions.pass_access.stripe.PaymentIntent.retrieve",
            return_value={"latest_charge": f"ch_{payment_intent_id}"},
        ), patch(
            "subscriptions.pass_access.stripe.Charge.retrieve",
            return_value={
                "amount": 399,
                "amount_refunded": 0,
                "refunded": False,
                "refunds": {"data": []},
            },
        ):
            status = build_subscription_status(parent)

        self.assertEqual(len(status["gifted_passes"]), 1)
        self.assertEqual(status["gifted_passes"][0]["id"], access_pass.id)
        access_pass.refresh_from_db()
        payment.refresh_from_db()
        self.assertFalse(access_pass.is_revoked)
        self.assertEqual(payment.status, "succeeded")

    def test_refunded_gifted_pass_disappears_without_webhook(self):
        parent = self._create_user(tag="gifted-pass-parent-refunded", role="parent")
        child = self._create_user(tag="gifted-pass-child-refunded")
        plan = self._create_pass_plan(tag="refunded")
        payment_intent_id = "pi_gifted_pass_refunded"
        payment, access_pass = self._create_parent_payment_and_child_pass(
            parent=parent,
            child=child,
            plan=plan,
            payment_intent_id=payment_intent_id,
        )

        with patch(
            "subscriptions.subscription_status._list_stripe_subscriptions",
            return_value=[],
        ), patch(
            "subscriptions.pass_access.stripe.PaymentIntent.retrieve",
            return_value={"latest_charge": f"ch_{payment_intent_id}"},
        ), patch(
            "subscriptions.pass_access.stripe.Charge.retrieve",
            return_value={
                "amount": 399,
                "amount_refunded": 399,
                "refunded": True,
                "refunds": {"data": [{"amount": 399}]},
            },
        ):
            status = build_subscription_status(parent)

        self.assertEqual(status["gifted_passes"], [])
        access_pass.refresh_from_db()
        payment.refresh_from_db()
        self.assertTrue(access_pass.is_revoked)
        self.assertIn(payment.status, {"refunded", "partially_refunded"})

    def test_mixed_refunded_and_non_refunded_gifted_passes(self):
        parent = self._create_user(tag="gifted-pass-parent-mixed", role="parent")
        child_refunded = self._create_user(tag="gifted-pass-child-mixed-refunded")
        child_active = self._create_user(tag="gifted-pass-child-mixed-active")
        plan = self._create_pass_plan(tag="mixed")
        refunded_pi = "pi_gifted_pass_mixed_refunded"
        active_pi = "pi_gifted_pass_mixed_active"

        payment_refunded, pass_refunded = self._create_parent_payment_and_child_pass(
            parent=parent,
            child=child_refunded,
            plan=plan,
            payment_intent_id=refunded_pi,
        )
        payment_active, pass_active = self._create_parent_payment_and_child_pass(
            parent=parent,
            child=child_active,
            plan=plan,
            payment_intent_id=active_pi,
        )

        def fake_pi_retrieve(payment_intent_id):
            return {"latest_charge": f"ch_{payment_intent_id}"}

        def fake_charge_retrieve(charge_id, expand=None):
            if charge_id == f"ch_{refunded_pi}":
                return {
                    "amount": 399,
                    "amount_refunded": 399,
                    "refunded": True,
                    "refunds": {"data": [{"amount": 399}]},
                }
            return {
                "amount": 399,
                "amount_refunded": 0,
                "refunded": False,
                "refunds": {"data": []},
            }

        with patch(
            "subscriptions.subscription_status._list_stripe_subscriptions",
            return_value=[],
        ), patch(
            "subscriptions.pass_access.stripe.PaymentIntent.retrieve",
            side_effect=fake_pi_retrieve,
        ), patch(
            "subscriptions.pass_access.stripe.Charge.retrieve",
            side_effect=fake_charge_retrieve,
        ):
            status = build_subscription_status(parent)

        self.assertEqual(len(status["gifted_passes"]), 1)
        self.assertEqual(status["gifted_passes"][0]["id"], pass_active.id)
        pass_refunded.refresh_from_db()
        pass_active.refresh_from_db()
        payment_refunded.refresh_from_db()
        payment_active.refresh_from_db()
        self.assertTrue(pass_refunded.is_revoked)
        self.assertFalse(pass_active.is_revoked)
        self.assertIn(payment_refunded.status, {"refunded", "partially_refunded"})
        self.assertEqual(payment_active.status, "succeeded")

    def test_gifted_pass_stays_visible_when_stripe_is_unavailable(self):
        parent = self._create_user(tag="gifted-pass-parent-stripe-down", role="parent")
        child = self._create_user(tag="gifted-pass-child-stripe-down")
        plan = self._create_pass_plan(tag="stripe-down")
        payment_intent_id = "pi_gifted_pass_stripe_down"
        payment, access_pass = self._create_parent_payment_and_child_pass(
            parent=parent,
            child=child,
            plan=plan,
            payment_intent_id=payment_intent_id,
        )

        with patch(
            "subscriptions.subscription_status._list_stripe_subscriptions",
            return_value=[],
        ), patch(
            "subscriptions.pass_access.stripe.PaymentIntent.retrieve",
            side_effect=stripe_error.StripeError("stripe down"),
        ):
            status = build_subscription_status(parent)

        self.assertEqual(len(status["gifted_passes"]), 1)
        self.assertEqual(status["gifted_passes"][0]["id"], access_pass.id)
        access_pass.refresh_from_db()
        payment.refresh_from_db()
        self.assertFalse(access_pass.is_revoked)
        self.assertEqual(payment.status, "succeeded")
