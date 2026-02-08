from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from pays.models import Niveau, Pays
from subscriptions.models import AccessPass, PaymentHistory, SubscriptionPlan, UserSubscription


class GiftCheckoutDuplicateLevelGuardTests(TestCase):
    def setUp(self):
        self.api_client = APIClient()

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

    def _create_niveau(self, *, tag: str):
        pays = Pays.objects.create(
            nom=f"France {tag}",
            code_iso=f"FR{tag[:1].upper()}",
            ordre=1,
            est_actif=True,
        )
        return Niveau.objects.create(
            nom=f"Terminale {tag}",
            pays=pays,
            ordre=1,
            est_actif=True,
        )

    def _create_pass_plan(self, *, tag: str):
        return SubscriptionPlan.objects.create(
            name="Pass 1 jour",
            plan_type="basic",
            plan_mode="one_time",
            billing_period="daily",
            price=Decimal("3.99"),
            stripe_price_id=f"price_pass_gift_guard_{tag}",
            features=[],
            access_days=1,
            is_active=True,
        )

    def _create_subscription_plan(self, *, tag: str):
        return SubscriptionPlan.objects.create(
            name="Mensuel",
            plan_type="basic",
            plan_mode="subscription",
            billing_period="monthly",
            price=Decimal("7.99"),
            stripe_price_id=f"price_sub_gift_guard_{tag}",
            features=[],
            is_active=True,
        )

    def test_parent_gift_pass_blocked_if_child_already_has_same_level_unlocked_from_another_parent(self):
        parent_buying = self._create_user(tag="gift-parent-a", role="parent")
        parent_existing = self._create_user(tag="gift-parent-b", role="parent")
        child = self._create_user(tag="gift-child-a", role="student")
        level = self._create_niveau(tag="a")
        pass_plan = self._create_pass_plan(tag="a")
        now = timezone.now()

        payment_intent = "pi_gift_level_guard_existing"
        PaymentHistory.objects.create(
            user=parent_existing,
            stripe_payment_intent_id=payment_intent,
            amount=Decimal("3.99"),
            currency="EUR",
            status="succeeded",
            description="Pass 1 jour",
            plan_name=pass_plan.name,
            plan_mode="one_time",
            period_start=now - timedelta(hours=1),
            period_end=now + timedelta(hours=20),
            niveau_pays=level,
        )
        AccessPass.objects.create(
            user=child,
            plan=pass_plan,
            starts_at=now - timedelta(hours=1),
            ends_at=now + timedelta(hours=20),
            stripe_payment_intent_id=payment_intent,
            is_revoked=False,
        )

        self.api_client.force_authenticate(user=parent_buying)

        with patch("subscriptions.views._get_stripe_customer_id") as get_customer_mock:
            response = self.api_client.post(
                "/api/subscriptions/create-checkout-session/",
                data={
                    "price_id": pass_plan.stripe_price_id,
                    "niveau_pays_id": level.id,
                    "beneficiary_email": child.email,
                },
                format="json",
            )

        self.assertEqual(response.status_code, 400)
        self.assertIn("déjà ce niveau débloqué", response.json().get("error", ""))
        get_customer_mock.assert_not_called()

    def test_parent_gift_subscription_blocked_if_child_already_has_same_level_subscription(self):
        parent = self._create_user(tag="gift-sub-parent", role="parent")
        child = self._create_user(tag="gift-sub-child", role="student")
        level = self._create_niveau(tag="b")
        subscription_plan = self._create_subscription_plan(tag="b")
        now = timezone.now()

        UserSubscription.objects.create(
            user=child,
            plan=subscription_plan,
            niveau_pays=level,
            status="active",
            current_period_start=now - timedelta(days=1),
            current_period_end=now + timedelta(days=29),
        )

        self.api_client.force_authenticate(user=parent)

        with patch("subscriptions.views._get_stripe_customer_id") as get_customer_mock:
            response = self.api_client.post(
                "/api/subscriptions/create-checkout-session/",
                data={
                    "price_id": subscription_plan.stripe_price_id,
                    "niveau_pays_id": level.id,
                    "beneficiary_email": child.email,
                },
                format="json",
            )

        self.assertEqual(response.status_code, 400)
        self.assertIn("déjà ce niveau débloqué", response.json().get("error", ""))
        get_customer_mock.assert_not_called()

    def test_parent_gift_allowed_when_child_unlock_is_on_another_level(self):
        parent = self._create_user(tag="gift-parent-allowed", role="parent")
        child = self._create_user(tag="gift-child-allowed", role="student")
        current_level = self._create_niveau(tag="c")
        target_level = self._create_niveau(tag="d")
        pass_plan = self._create_pass_plan(tag="c")
        now = timezone.now()

        existing_intent = "pi_gift_level_guard_other_level"
        PaymentHistory.objects.create(
            user=parent,
            stripe_payment_intent_id=existing_intent,
            amount=Decimal("3.99"),
            currency="EUR",
            status="succeeded",
            description="Pass 1 jour",
            plan_name=pass_plan.name,
            plan_mode="one_time",
            period_start=now - timedelta(hours=1),
            period_end=now + timedelta(hours=20),
            niveau_pays=current_level,
        )
        AccessPass.objects.create(
            user=child,
            plan=pass_plan,
            starts_at=now - timedelta(hours=1),
            ends_at=now + timedelta(hours=20),
            stripe_payment_intent_id=existing_intent,
            is_revoked=False,
        )

        self.api_client.force_authenticate(user=parent)

        with patch(
            "subscriptions.views._get_stripe_customer_id",
            return_value="cus_gift_guard_parent",
        ), patch(
            "subscriptions.views.stripe.Customer.modify",
            return_value=None,
        ), patch(
            "subscriptions.views.stripe.checkout.Session.create",
            return_value=SimpleNamespace(url="https://checkout.example.com/session"),
        ):
            response = self.api_client.post(
                "/api/subscriptions/create-checkout-session/",
                data={
                    "price_id": pass_plan.stripe_price_id,
                    "niveau_pays_id": target_level.id,
                    "beneficiary_email": child.email,
                },
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json().get("checkout_url"),
            "https://checkout.example.com/session",
        )
