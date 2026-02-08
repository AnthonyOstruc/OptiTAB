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

    def test_new_subscription_admin_email_contains_stripe_count_and_mode(self):
        user = self._create_user(tag="admin-mail-new")
        plan = self._create_subscription_plan(tag="admin-mail-new")

        with patch.object(
            EmailService,
            "_count_active_subscriptions_on_stripe",
            return_value={"count": 0, "mode_label": "LIVE", "error_message": None},
        ), patch("core.services.EmailMultiAlternatives") as email_cls:
            email_instance = email_cls.return_value
            email_instance.send.return_value = 1

            success = EmailService.send_new_subscription_notification_to_admin(
                user=user,
                plan=plan,
            )

        self.assertTrue(success)
        body = email_cls.call_args.kwargs["body"]
        self.assertIn("Abonnements actifs Stripe : 0", body)
        self.assertIn("Mode Stripe : LIVE", body)

    def test_new_subscription_admin_email_contains_stats_in_html_when_gift(self):
        beneficiary = self._create_user(tag="admin-mail-gift-beneficiary")
        payer = self._create_user(tag="admin-mail-gift-payer")
        plan = self._create_subscription_plan(tag="admin-mail-gift")

        with patch.object(
            EmailService,
            "_count_active_subscriptions_on_stripe",
            return_value={"count": 0, "mode_label": "TEST", "error_message": None},
        ), patch("core.services.EmailMultiAlternatives") as email_cls:
            email_instance = email_cls.return_value
            email_instance.send.return_value = 1

            success = EmailService.send_new_subscription_notification_to_admin(
                user=beneficiary,
                plan=plan,
                is_gift=True,
                payer=payer,
            )

        self.assertTrue(success)
        email_instance = email_cls.return_value
        html_body = email_instance.attach_alternative.call_args.args[0]
        self.assertIn("Abonnements actifs Stripe", html_body)
        self.assertIn("Passes actifs", html_body)
        self.assertIn("Mode Stripe", html_body)
        self.assertIn("Cadeau", html_body)

    def test_new_subscription_admin_email_uses_achat_pass_title_for_one_time(self):
        user = self._create_user(tag="admin-mail-pass-title")
        pass_plan = self._create_pass_plan(tag="admin-mail-pass-title")
        old_sub_plan = self._create_subscription_plan(tag="admin-mail-pass-title-old-sub")
        niveau = self._create_level(tag="admin-mail-pass-title")
        UserSubscription.objects.create(
            user=user,
            plan=old_sub_plan,
            niveau_pays=niveau,
            status="canceled",
            current_period_end=timezone.now() - timedelta(days=1),
        )

        with patch.object(
            EmailService,
            "_count_active_subscriptions_on_stripe",
            return_value={"count": 0, "mode_label": "TEST", "error_message": None},
        ), patch("core.services.EmailMultiAlternatives") as email_cls:
            email_instance = email_cls.return_value
            email_instance.send.return_value = 1

            success = EmailService.send_new_subscription_notification_to_admin(
                user=user,
                plan=pass_plan,
                niveau=niveau,
            )

        self.assertTrue(success)
        self.assertIn("🎫 Achat pass", email_cls.call_args.kwargs["subject"])
        self.assertNotIn("Réabonnement", email_cls.call_args.kwargs["subject"])
        html_body = email_instance.attach_alternative.call_args.args[0]
        self.assertIn("Achat pass", html_body)

    def test_pass_expiration_admin_email_contains_stripe_count_and_mode(self):
        user = self._create_user(tag="admin-mail-pass")
        pass_plan = self._create_pass_plan(tag="admin-mail-pass")
        access_pass = AccessPass.objects.create(
            user=user,
            plan=pass_plan,
            starts_at=timezone.now() - timedelta(days=1),
            ends_at=timezone.now() - timedelta(minutes=5),
            stripe_payment_intent_id="pi_admin_mail_pass",
            expiration_email_sent=False,
            is_revoked=False,
        )

        with patch.object(
            EmailService,
            "_count_active_subscriptions_on_stripe",
            return_value={"count": 0, "mode_label": "TEST", "error_message": None},
        ), patch("core.services.EmailMultiAlternatives") as email_cls:
            email_instance = email_cls.return_value
            email_instance.send.return_value = 1

            success = EmailService.send_pass_expiration_notification_to_admin(
                user=user,
                access_pass=access_pass,
            )

        self.assertTrue(success)
        body = email_cls.call_args.kwargs["body"]
        self.assertIn("Abonnements actifs Stripe : 0", body)
        self.assertIn("Mode Stripe : TEST", body)

    def test_pass_expiration_admin_email_uses_indisponible_when_stripe_fails(self):
        user = self._create_user(tag="admin-mail-stripe-down")
        pass_plan = self._create_pass_plan(tag="admin-mail-stripe-down")
        subscription_plan = self._create_subscription_plan(tag="admin-mail-stripe-down")
        UserSubscription.objects.create(
            user=user,
            plan=subscription_plan,
            status="active",
            cancel_at_period_end=False,
        )
        access_pass = AccessPass.objects.create(
            user=user,
            plan=pass_plan,
            starts_at=timezone.now() - timedelta(days=1),
            ends_at=timezone.now() - timedelta(minutes=5),
            stripe_payment_intent_id="pi_admin_mail_stripe_down",
            expiration_email_sent=False,
            is_revoked=False,
        )

        with patch.object(
            EmailService,
            "_count_active_subscriptions_on_stripe",
            return_value={
                "count": None,
                "mode_label": "TEST",
                "error_message": "stripe down",
            },
        ), patch("core.services.EmailMultiAlternatives") as email_cls:
            email_instance = email_cls.return_value
            email_instance.send.return_value = 1

            success = EmailService.send_pass_expiration_notification_to_admin(
                user=user,
                access_pass=access_pass,
            )

        self.assertTrue(success)
        body = email_cls.call_args.kwargs["body"]
        self.assertIn("Abonnements actifs Stripe : Indisponible", body)
        self.assertIn("Mode Stripe : TEST", body)
        self.assertIn("Erreur Stripe : stripe down", body)
        self.assertNotIn("Abonnements actifs Stripe : 1", body)

    def test_subscription_confirmation_email_contains_counts(self):
        user = self._create_user(tag="sub-confirm-counts")
        subscription_plan = self._create_subscription_plan(tag="sub-confirm-counts")
        pass_plan = self._create_pass_plan(tag="sub-confirm-counts")
        AccessPass.objects.create(
            user=user,
            plan=pass_plan,
            starts_at=timezone.now() - timedelta(hours=1),
            ends_at=timezone.now() + timedelta(hours=6),
            stripe_payment_intent_id="pi_sub_confirm_counts",
            is_revoked=False,
        )

        with patch.object(
            EmailService,
            "_count_active_subscriptions_on_stripe",
            return_value={"count": 5, "mode_label": "TEST", "error_message": None},
        ), patch("core.services.EmailMultiAlternatives") as email_cls:
            email_instance = email_cls.return_value
            email_instance.send.return_value = 1

            success = EmailService.send_subscription_confirmation(
                user=user,
                plan=subscription_plan,
            )

        self.assertTrue(success)
        body = email_cls.call_args.kwargs["body"]
        self.assertIn("Abonnements actifs Stripe : 5", body)
        self.assertIn("Passes actifs : 1", body)
        html_body = email_instance.attach_alternative.call_args.args[0]
        self.assertIn("Abonnements actifs Stripe", html_body)
        self.assertIn("Passes actifs", html_body)

    def test_subscription_renewal_email_contains_counts(self):
        user = self._create_user(tag="sub-renew-counts")
        subscription_plan = self._create_subscription_plan(tag="sub-renew-counts")
        pass_plan = self._create_pass_plan(tag="sub-renew-counts")
        AccessPass.objects.create(
            user=user,
            plan=pass_plan,
            starts_at=timezone.now() - timedelta(hours=1),
            ends_at=timezone.now() + timedelta(hours=6),
            stripe_payment_intent_id="pi_sub_renew_counts",
            is_revoked=False,
        )

        with patch.object(
            EmailService,
            "_count_active_subscriptions_on_stripe",
            return_value={"count": 3, "mode_label": "LIVE", "error_message": None},
        ), patch("core.services.EmailMultiAlternatives") as email_cls:
            email_instance = email_cls.return_value
            email_instance.send.return_value = 1

            success = EmailService.send_subscription_renewal_notification(
                user=user,
                plan=subscription_plan,
            )

        self.assertTrue(success)
        body = email_cls.call_args.kwargs["body"]
        self.assertIn("Abonnements actifs Stripe : 3", body)
        self.assertIn("Passes actifs : 1", body)
        html_body = email_instance.attach_alternative.call_args.args[0]
        self.assertIn("Abonnements actifs Stripe", html_body)
        self.assertIn("Passes actifs", html_body)
