from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from subscriptions.models import SubscriptionPlan, UserSubscription
from subscriptions.views import _runtime_stripe_price_id


class AdminSubscriptionPlanChangeTests(TestCase):
    def _create_user(self, *, tag: str, is_staff: bool = False):
        User = get_user_model()
        return User.objects.create_user(
            email=f"{tag}@example.com",
            first_name="Test",
            last_name="User",
            password="test-password",
            is_active=True,
            is_staff=is_staff,
        )

    def _create_subscription_plan(
        self,
        *,
        tag: str,
        plan_type: str,
        billing_period: str,
        plan_mode: str = "subscription",
        is_active: bool = True,
        access_days: int | None = None,
    ):
        return SubscriptionPlan.objects.create(
            name=f"Plan {tag}",
            plan_type=plan_type,
            plan_mode=plan_mode,
            billing_period=billing_period,
            price=Decimal("9.99"),
            stripe_price_id=f"price_live_{tag}",
            stripe_price_id_test=f"price_test_{tag}",
            features=[],
            is_active=is_active,
            access_days=access_days,
        )

    def setUp(self):
        self.admin = self._create_user(tag="admin-plan-change", is_staff=True)
        self.student = self._create_user(tag="student-plan-change")
        self.other_user = self._create_user(tag="non-admin-plan-change")
        self.basic_plan = self._create_subscription_plan(
            tag="basic-monthly",
            plan_type="basic",
            billing_period="monthly",
        )
        self.premium_plan = self._create_subscription_plan(
            tag="premium-monthly",
            plan_type="premium",
            billing_period="monthly",
        )
        self.one_time_plan = self._create_subscription_plan(
            tag="pass-daily",
            plan_type="basic",
            billing_period="daily",
            plan_mode="one_time",
            access_days=1,
        )
        self.client = APIClient()

    def test_admin_can_change_local_subscription_plan_without_stripe(self):
        subscription = UserSubscription.objects.create(
            user=self.student,
            plan=self.premium_plan,
            status="active",
            current_period_start=timezone.now() - timedelta(days=1),
            current_period_end=timezone.now() + timedelta(days=29),
        )
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            "/api/subscriptions/admin/subscribers/change-plan/",
            data={
                "subscription_id": subscription.id,
                "plan_id": self.basic_plan.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        subscription.refresh_from_db()
        self.assertEqual(subscription.plan_id, self.basic_plan.id)
        self.assertEqual(response.json()["subscription"]["plan_id"], self.basic_plan.id)

    def test_non_admin_cannot_change_subscription_plan(self):
        subscription = UserSubscription.objects.create(
            user=self.student,
            plan=self.premium_plan,
            status="active",
        )
        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(
            "/api/subscriptions/admin/subscribers/change-plan/",
            data={
                "subscription_id": subscription.id,
                "plan_id": self.basic_plan.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_cannot_switch_subscription_to_one_time_plan(self):
        subscription = UserSubscription.objects.create(
            user=self.student,
            plan=self.premium_plan,
            status="active",
        )
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            "/api/subscriptions/admin/subscribers/change-plan/",
            data={
                "subscription_id": subscription.id,
                "plan_id": self.one_time_plan.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("abonnement r\u00e9current", response.json().get("detail", "").lower())

    def test_admin_changes_stripe_subscription_price_when_subscription_is_linked(self):
        now = timezone.now()
        subscription = UserSubscription.objects.create(
            user=self.student,
            plan=self.premium_plan,
            stripe_subscription_id="sub_admin_change_plan",
            status="active",
            current_period_start=now - timedelta(days=5),
            current_period_end=now + timedelta(days=25),
            cancel_at_period_end=False,
        )
        self.client.force_authenticate(user=self.admin)

        stripe_snapshot = {
            "id": subscription.stripe_subscription_id,
            "items": {"data": [{"id": "si_admin_change_plan"}]},
            "metadata": {"user_id": str(self.student.id)},
            "status": "active",
            "cancel_at_period_end": False,
            "current_period_start": int((now - timedelta(days=5)).timestamp()),
            "current_period_end": int((now + timedelta(days=25)).timestamp()),
            "trial_end": None,
        }
        stripe_updated = {
            "id": subscription.stripe_subscription_id,
            "status": "active",
            "cancel_at_period_end": False,
            "current_period_start": int((now - timedelta(days=1)).timestamp()),
            "current_period_end": int((now + timedelta(days=29)).timestamp()),
            "trial_end": None,
        }

        with patch(
            "subscriptions.views.stripe.Subscription.retrieve",
            return_value=stripe_snapshot,
        ), patch(
            "subscriptions.views.stripe.Subscription.modify",
            return_value=stripe_updated,
        ) as stripe_modify_mock:
            response = self.client.post(
                "/api/subscriptions/admin/subscribers/change-plan/",
                data={
                    "subscription_id": subscription.id,
                    "plan_id": self.basic_plan.id,
                },
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        expected_price = _runtime_stripe_price_id(self.basic_plan)
        self.assertIsNotNone(expected_price)
        stripe_modify_mock.assert_called_once_with(
            subscription.stripe_subscription_id,
            items=[{"id": "si_admin_change_plan", "price": expected_price}],
            proration_behavior="none",
            metadata={
                "user_id": str(self.student.id),
                "plan_id": str(self.basic_plan.id),
                "plan_mode": "subscription",
            },
        )
        subscription.refresh_from_db()
        self.assertEqual(subscription.plan_id, self.basic_plan.id)
