from __future__ import annotations

import os
import sys
from datetime import timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from core.services import EmailService
from pays.models import Niveau, Pays
from subscriptions.models import AccessPass, SubscriptionPlan, UserSubscription


class _FakeStripePage:
    def __init__(self, data=None, auto_items=None):
        self.data = data or []
        self._auto_items = auto_items

    def auto_paging_iter(self):
        if self._auto_items is not None:
            return iter(self._auto_items)
        return iter(self.data)


class _FakeSubscriptionAPI:
    def __init__(self, pages=None, error=None):
        self.pages = pages or {}
        self.error = error

    def list(self, status, limit=100):
        if self.error:
            raise self.error
        return self.pages.get(status, _FakeStripePage([]))


class AdminEmailStripeCountTests(TestCase):
    def _create_user(self, *, tag: str):
        User = get_user_model()
        return User.objects.create_user(
            email=f"{tag}@example.com",
            first_name="Test",
            last_name="User",
            password="test-password",
            is_active=True,
        )

    def _create_subscription_plan(self, *, tag: str):
        return SubscriptionPlan.objects.create(
            name="Mensuel",
            plan_type="basic",
            plan_mode="subscription",
            billing_period="monthly",
            price=Decimal("4.99"),
            stripe_price_id=f"price_sub_{tag}",
            features=[],
            is_active=True,
        )

    def _create_pass_plan(self, *, tag: str):
        return SubscriptionPlan.objects.create(
            name="Pass test",
            plan_type="basic",
            plan_mode="one_time",
            billing_period="daily",
            price=Decimal("1.00"),
            stripe_price_id=f"price_pass_{tag}",
            features=[],
            access_days=1,
            is_active=True,
        )

    def _create_level(self, *, tag: str):
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

    def _fake_stripe_module(self, *, active=None, trialing=None, error=None):
        subscription_api = _FakeSubscriptionAPI(
            pages={
                "active": active or _FakeStripePage([]),
                "trialing": trialing or _FakeStripePage([]),
            },
            error=error,
        )
        return SimpleNamespace(Subscription=subscription_api, api_key=None)

    def test_count_active_subscriptions_on_stripe_returns_zero(self):
        stripe_module = self._fake_stripe_module()
        with patch.dict(os.environ, {"STRIPE_SECRET_KEY": "sk_test_dummy"}, clear=False), patch.dict(
            sys.modules, {"stripe": stripe_module}
        ):
            stats = EmailService._count_active_subscriptions_on_stripe()

        self.assertEqual(stats["count"], 0)
        self.assertEqual(stats["mode_label"], "TEST")
        self.assertIsNone(stats["error_message"])

    def test_count_active_subscriptions_on_stripe_filters_cancel_at_period_end(self):
        stripe_module = self._fake_stripe_module(
            active=_FakeStripePage(
                data=[
                    {"id": "sub_1", "cancel_at_period_end": False},
                    {"id": "sub_2", "cancel_at_period_end": True},
                ]
            ),
            trialing=_FakeStripePage(
                data=[{"id": "sub_3", "cancel_at_period_end": False}]
            ),
        )
        with patch.dict(os.environ, {"STRIPE_SECRET_KEY": "sk_test_dummy"}, clear=False), patch.dict(
            sys.modules, {"stripe": stripe_module}
        ):
            stats = EmailService._count_active_subscriptions_on_stripe()

        self.assertEqual(stats["count"], 2)
        self.assertEqual(stats["mode_label"], "TEST")
        self.assertIsNone(stats["error_message"])

    def test_count_active_subscriptions_on_stripe_uses_auto_paging_iter(self):
        active_items = [
            {"id": f"sub_{index}", "cancel_at_period_end": False}
            for index in range(120)
        ]
        stripe_module = self._fake_stripe_module(
            active=_FakeStripePage(data=active_items[:100], auto_items=active_items),
            trialing=_FakeStripePage(data=[]),
        )
        with patch.dict(os.environ, {"STRIPE_SECRET_KEY": "sk_test_dummy"}, clear=False), patch.dict(
            sys.modules, {"stripe": stripe_module}
        ):
            stats = EmailService._count_active_subscriptions_on_stripe()

        self.assertEqual(stats["count"], 120)
        self.assertEqual(stats["mode_label"], "TEST")
        self.assertIsNone(stats["error_message"])

    def test_count_active_subscriptions_on_stripe_returns_error_metadata(self):
        stripe_module = self._fake_stripe_module(error=RuntimeError("stripe down"))
        with patch.dict(os.environ, {"STRIPE_SECRET_KEY": "sk_live_dummy"}, clear=False), patch.dict(
            sys.modules, {"stripe": stripe_module}
        ):
            stats = EmailService._count_active_subscriptions_on_stripe()

        self.assertIsNone(stats["count"])
        self.assertEqual(stats["mode_label"], "LIVE")
        self.assertIn("stripe down", stats["error_message"])
