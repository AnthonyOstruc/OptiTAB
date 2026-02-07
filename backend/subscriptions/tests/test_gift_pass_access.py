from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from subscriptions.handlers import handle_checkout_session_payment_completed
from subscriptions.models import AccessPass, PaymentHistory, SubscriptionPlan


class GiftPassAccessTests(TestCase):
    def _create_user(self, *, tag: str, role: str = "student"):
        User = get_user_model()
        return User.objects.create_user(
            email=f"{tag}@example.com",
            first_name="Test",
            last_name="User",
            password="test-password",
            is_active=True,
            role=role,
        )

    def _create_pass_plan(self, *, tag: str):
        return SubscriptionPlan.objects.create(
            name="Pass 1 jour",
            plan_type="basic",
            plan_mode="one_time",
            billing_period="daily",
            price=Decimal("3.99"),
            stripe_price_id=f"price_pass_{tag}",
            features=[],
            access_days=1,
            is_active=True,
        )

    def test_gift_pass_uses_beneficiary_email_when_user_id_points_to_parent(self):
        parent = self._create_user(tag="gift-pass-parent", role="parent")
        child = self._create_user(tag="gift-pass-child", role="student")
        plan = self._create_pass_plan(tag="gift-pass-access")
        payment_intent_id = "pi_gift_pass_child_access"

        session = {
            "id": "cs_gift_pass_child_access",
            "status": "complete",
            "payment_status": "paid",
            "amount_total": 399,
            "currency": "eur",
            "payment_intent": payment_intent_id,
            "metadata": {
                "user_id": str(parent.id),
                "payer_user_id": str(parent.id),
                "plan_id": str(plan.id),
                "plan_mode": "one_time",
                "is_gift": "true",
                "beneficiary_email": child.email,
                "beneficiary_name": child.full_name,
            },
        }

        with patch(
            "subscriptions.handlers.EmailService.send_gift_subscription_notification",
            return_value=True,
        ) as gift_notif_mock, patch(
            "subscriptions.handlers.EmailService.send_gift_purchase_confirmation",
            return_value=True,
        ) as purchase_notif_mock, patch(
            "subscriptions.handlers.EmailService.send_new_subscription_notification_to_admin",
            return_value=True,
        ):
            handle_checkout_session_payment_completed(session)

        created_pass = AccessPass.objects.get(stripe_payment_intent_id=payment_intent_id)
        self.assertEqual(created_pass.user_id, child.id)
        self.assertFalse(created_pass.is_revoked)
        self.assertGreater(created_pass.ends_at, timezone.now())

        payment = PaymentHistory.objects.get(stripe_payment_intent_id=payment_intent_id)
        self.assertEqual(payment.user_id, parent.id)
        self.assertEqual(payment.status, "succeeded")

        self.assertEqual(gift_notif_mock.call_args.kwargs["recipient"].id, child.id)
        self.assertEqual(gift_notif_mock.call_args.kwargs["gifter"].id, parent.id)
        self.assertEqual(purchase_notif_mock.call_args.kwargs["payer"].id, parent.id)
        self.assertEqual(purchase_notif_mock.call_args.kwargs["recipient"].id, child.id)

    def test_gift_pass_is_recreated_if_payment_history_exists_without_pass(self):
        parent = self._create_user(tag="gift-pass-parent-history", role="parent")
        child = self._create_user(tag="gift-pass-child-history", role="student")
        plan = self._create_pass_plan(tag="gift-pass-history")
        payment_intent_id = "pi_gift_pass_existing_history"

        PaymentHistory.objects.create(
            user=parent,
            stripe_payment_intent_id=payment_intent_id,
            amount=Decimal("3.99"),
            currency="EUR",
            status="succeeded",
            description="Pass cadeau",
            plan_name=plan.name,
            plan_mode="one_time",
            period_start=timezone.now() - timedelta(minutes=1),
            period_end=timezone.now() + timedelta(days=1),
        )

        session = {
            "id": "cs_gift_pass_existing_history",
            "status": "complete",
            "payment_status": "paid",
            "amount_total": 399,
            "currency": "eur",
            "payment_intent": payment_intent_id,
            "metadata": {
                "user_id": str(child.id),
                "payer_user_id": str(parent.id),
                "plan_id": str(plan.id),
                "plan_mode": "one_time",
                "is_gift": "true",
                "beneficiary_email": child.email,
            },
        }

        with patch(
            "subscriptions.handlers.EmailService.send_gift_subscription_notification",
            return_value=True,
        ) as gift_notif_mock, patch(
            "subscriptions.handlers.EmailService.send_gift_purchase_confirmation",
            return_value=True,
        ) as purchase_notif_mock, patch(
            "subscriptions.handlers.EmailService.send_new_subscription_notification_to_admin",
            return_value=True,
        ):
            handle_checkout_session_payment_completed(session)

        created_pass = AccessPass.objects.get(stripe_payment_intent_id=payment_intent_id)
        self.assertEqual(created_pass.user_id, child.id)
        self.assertFalse(created_pass.is_revoked)
        self.assertGreater(created_pass.ends_at, timezone.now())

        self.assertEqual(PaymentHistory.objects.filter(stripe_payment_intent_id=payment_intent_id).count(), 1)
        gift_notif_mock.assert_not_called()
        purchase_notif_mock.assert_not_called()
