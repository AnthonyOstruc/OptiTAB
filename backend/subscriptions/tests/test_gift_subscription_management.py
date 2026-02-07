from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from subscriptions.models import SubscriptionPlan, UserSubscription
from subscriptions.stripe_services import _build_gifted_subscriptions_from_stripe


class GiftSubscriptionManagementTests(TestCase):
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

    def _create_subscription_plan(self, *, tag: str):
        return SubscriptionPlan.objects.create(
            name="Mensuel",
            plan_type="basic",
            plan_mode="subscription",
            billing_period="monthly",
            price=Decimal("7.99"),
            stripe_price_id=f"price_gift_{tag}",
            features=[],
            is_active=True,
        )

    def _create_child_subscription(self, *, child, plan, stripe_subscription_id: str, cancel_at_period_end=False):
        now = timezone.now()
        return UserSubscription.objects.create(
            user=child,
            plan=plan,
            stripe_subscription_id=stripe_subscription_id,
            status="active",
            current_period_start=now - timedelta(days=1),
            current_period_end=now + timedelta(days=29),
            cancel_at_period_end=cancel_at_period_end,
        )

    def setUp(self):
        self.parent = self._create_user(tag="gift-parent-manage", role="parent")
        self.child = self._create_user(tag="gift-child-manage", role="student")
        self.plan = self._create_subscription_plan(tag="gift-manage")
        self.api_client = APIClient()

    def test_parent_can_cancel_gift_subscription_with_payer_metadata(self):
        subscription = self._create_child_subscription(
            child=self.child,
            plan=self.plan,
            stripe_subscription_id="sub_gift_parent_cancel",
        )
        self.api_client.force_authenticate(user=self.parent)

        stripe_snapshot = {
            "id": subscription.stripe_subscription_id,
            "metadata": {
                "is_gift": "true",
                "user_id": str(self.child.id),
                "payer_user_id": str(self.parent.id),
                "beneficiary_email": self.child.email,
            },
            "customer": {"email": self.parent.email},
        }

        def fake_cancel_subscription(instance):
            instance.cancel_at_period_end = True
            instance.save(update_fields=["cancel_at_period_end", "updated_at"])
            return True

        with patch(
            "subscriptions.views.stripe.Subscription.retrieve",
            return_value=stripe_snapshot,
        ), patch.object(
            UserSubscription,
            "cancel_subscription",
            autospec=True,
            side_effect=fake_cancel_subscription,
        ), patch(
            "subscriptions.views._schedule_cancellation_emails"
        ) as schedule_mock:
            response = self.api_client.post(
                "/api/subscriptions/cancel/",
                data={"stripe_subscription_id": subscription.stripe_subscription_id},
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        subscription.refresh_from_db()
        self.assertTrue(subscription.cancel_at_period_end)
        self.assertTrue(schedule_mock.called)
        self.assertEqual(schedule_mock.call_args.kwargs.get("user_subscription_id"), subscription.id)

    def test_parent_can_cancel_legacy_gift_subscription_without_payer_metadata(self):
        subscription = self._create_child_subscription(
            child=self.child,
            plan=self.plan,
            stripe_subscription_id="sub_gift_parent_legacy_cancel",
        )
        self.api_client.force_authenticate(user=self.parent)

        legacy_snapshot = {
            "id": subscription.stripe_subscription_id,
            "metadata": {
                "is_gift": "true",
                "user_id": str(self.child.id),
                "beneficiary_email": self.child.email,
            },
            "customer": {"email": self.parent.email},
        }

        def fake_cancel_subscription(instance):
            instance.cancel_at_period_end = True
            instance.save(update_fields=["cancel_at_period_end", "updated_at"])
            return True

        with patch(
            "subscriptions.views.stripe.Subscription.retrieve",
            return_value=legacy_snapshot,
        ), patch.object(
            UserSubscription,
            "cancel_subscription",
            autospec=True,
            side_effect=fake_cancel_subscription,
        ), patch(
            "subscriptions.views._schedule_cancellation_emails"
        ):
            response = self.api_client.post(
                "/api/subscriptions/cancel/",
                data={"stripe_subscription_id": subscription.stripe_subscription_id},
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        subscription.refresh_from_db()
        self.assertTrue(subscription.cancel_at_period_end)

    def test_parent_can_reactivate_child_gift_subscription(self):
        subscription = self._create_child_subscription(
            child=self.child,
            plan=self.plan,
            stripe_subscription_id="sub_gift_parent_reactivate",
            cancel_at_period_end=True,
        )
        self.api_client.force_authenticate(user=self.parent)

        auth_snapshot = {
            "id": subscription.stripe_subscription_id,
            "metadata": {
                "is_gift": "true",
                "user_id": str(self.child.id),
                "payer_user_id": str(self.parent.id),
                "beneficiary_email": self.child.email,
            },
            "customer": {"email": self.parent.email},
        }
        updated_snapshot = {
            "id": subscription.stripe_subscription_id,
            "status": "active",
            "cancel_at_period_end": False,
        }

        def retrieve_side_effect(*args, **kwargs):
            if kwargs.get("expand"):
                return auth_snapshot
            return updated_snapshot

        with patch(
            "subscriptions.views.stripe.Subscription.retrieve",
            side_effect=retrieve_side_effect,
        ), patch(
            "subscriptions.views.stripe.Subscription.modify",
            return_value=None,
        ), patch(
            "subscriptions.views.EmailService.send_reactivation_notification_to_admin",
            return_value=True,
        ):
            response = self.api_client.post(
                "/api/subscriptions/reactivate/",
                data={"stripe_subscription_id": subscription.stripe_subscription_id},
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        subscription.refresh_from_db()
        self.assertFalse(subscription.cancel_at_period_end)
        self.assertEqual(subscription.status, "active")

    def test_parent_cannot_manage_non_gift_subscription_of_child(self):
        subscription = self._create_child_subscription(
            child=self.child,
            plan=self.plan,
            stripe_subscription_id="sub_non_gift_child",
        )
        self.api_client.force_authenticate(user=self.parent)

        non_gift_snapshot = {
            "id": subscription.stripe_subscription_id,
            "metadata": {
                "user_id": str(self.child.id),
                "is_gift": "false",
            },
            "customer": {"email": self.child.email},
        }

        with patch(
            "subscriptions.views.stripe.Subscription.retrieve",
            return_value=non_gift_snapshot,
        ):
            response = self.api_client.post(
                "/api/subscriptions/cancel/",
                data={"stripe_subscription_id": subscription.stripe_subscription_id},
                format="json",
            )

        self.assertEqual(response.status_code, 403)

    def test_build_gifted_subscriptions_includes_legacy_gifts_without_payer_metadata(self):
        now = timezone.now()
        stripe_subscriptions = [
            {
                "id": "sub_legacy_gift_parent_list",
                "status": "active",
                "cancel_at_period_end": False,
                "current_period_start": int((now - timedelta(days=2)).timestamp()),
                "current_period_end": int((now + timedelta(days=28)).timestamp()),
                "start_date": int((now - timedelta(days=30)).timestamp()),
                "metadata": {
                    "is_gift": "true",
                    "user_id": str(self.child.id),
                    "beneficiary_email": self.child.email,
                    "beneficiary_name": "Test User",
                    "plan_id": str(self.plan.id),
                },
                "items": {"data": []},
            }
        ]

        gifted = _build_gifted_subscriptions_from_stripe(stripe_subscriptions, self.parent)

        self.assertEqual(len(gifted), 1)
        self.assertEqual(gifted[0]["stripe_subscription_id"], "sub_legacy_gift_parent_list")
        self.assertEqual(gifted[0]["beneficiary"]["email"], self.child.email)
