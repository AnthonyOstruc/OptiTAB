from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from pays.models import Niveau, Pays
from subscriptions.models import AccessPass, PaymentHistory, SubscriptionPlan
from subscriptions.subscription_status import build_subscription_status


class GiftPassLevelUnlockTests(TestCase):
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
            stripe_price_id=f"price_pass_level_{tag}",
            features=[],
            access_days=1,
            is_active=True,
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

    def _create_pass_payment_history(
        self,
        *,
        owner,
        payment_intent_id: str,
        plan_name: str,
        niveau=None,
    ):
        now = timezone.now()
        return PaymentHistory.objects.create(
            user=owner,
            stripe_payment_intent_id=payment_intent_id,
            amount=Decimal("3.99"),
            currency="EUR",
            status="succeeded",
            description=f"Pass {plan_name}",
            plan_name=plan_name,
            plan_mode="one_time",
            period_start=now - timedelta(minutes=5),
            period_end=now + timedelta(days=1),
            niveau_pays=niveau,
        )

    def _active_pass(self, *, user, plan, payment_intent_id: str, revoked: bool = False):
        now = timezone.now()
        return AccessPass.objects.create(
            user=user,
            plan=plan,
            starts_at=now - timedelta(minutes=5),
            ends_at=now + timedelta(hours=20),
            stripe_payment_intent_id=payment_intent_id,
            is_revoked=revoked,
        )

    def _unlocked_level_ids(self, status):
        return {
            int(level["id"])
            for level in (status.get("unlocked_levels") or [])
            if isinstance(level, dict) and level.get("id") is not None
        }

    def test_gift_pass_unlocks_level_for_child(self):
        parent = self._create_user(tag="gift-level-parent", role="parent")
        child = self._create_user(tag="gift-level-child")
        plan = self._create_pass_plan(tag="gift-child")
        niveau = self._create_niveau(tag="gift-child")
        payment_intent_id = "pi_gift_pass_level_unlock_child"

        self._create_pass_payment_history(
            owner=parent,
            payment_intent_id=payment_intent_id,
            plan_name=plan.name,
            niveau=niveau,
        )
        access_pass = self._active_pass(
            user=child,
            plan=plan,
            payment_intent_id=payment_intent_id,
        )

        with patch(
            "subscriptions.subscription_status._list_stripe_subscriptions",
            return_value=[],
        ), patch(
            "subscriptions.subscription_status.get_valid_active_passes_for_user",
            return_value=[access_pass],
        ):
            status = build_subscription_status(child)

        self.assertTrue(status["has_active_pass"])
        self.assertIsNotNone(status.get("pass_niveau"))
        self.assertEqual(status["pass_niveau"]["id"], niveau.id)
        self.assertIn(niveau.id, self._unlocked_level_ids(status))

    def test_direct_pass_unlock_behavior_is_unchanged(self):
        student = self._create_user(tag="direct-pass-student")
        plan = self._create_pass_plan(tag="direct-pass")
        niveau = self._create_niveau(tag="direct-pass")
        payment_intent_id = "pi_direct_pass_level_unlock"

        self._create_pass_payment_history(
            owner=student,
            payment_intent_id=payment_intent_id,
            plan_name=plan.name,
            niveau=niveau,
        )
        access_pass = self._active_pass(
            user=student,
            plan=plan,
            payment_intent_id=payment_intent_id,
        )

        with patch(
            "subscriptions.subscription_status._list_stripe_subscriptions",
            return_value=[],
        ), patch(
            "subscriptions.subscription_status.get_valid_active_passes_for_user",
            return_value=[access_pass],
        ):
            status = build_subscription_status(student)

        self.assertTrue(status["has_active_pass"])
        self.assertEqual(status["pass_niveau"]["id"], niveau.id)
        self.assertIn(niveau.id, self._unlocked_level_ids(status))

    def test_gift_pass_without_level_history_stays_locked_and_logs_warning(self):
        parent = self._create_user(tag="gift-level-parent-no-niveau", role="parent")
        child = self._create_user(tag="gift-level-child-no-niveau")
        plan = self._create_pass_plan(tag="gift-no-niveau")
        payment_intent_id = "pi_gift_pass_level_missing_niveau"

        self._create_pass_payment_history(
            owner=parent,
            payment_intent_id=payment_intent_id,
            plan_name=plan.name,
            niveau=None,
        )
        access_pass = self._active_pass(
            user=child,
            plan=plan,
            payment_intent_id=payment_intent_id,
        )

        with patch(
            "subscriptions.subscription_status._list_stripe_subscriptions",
            return_value=[],
        ), patch(
            "subscriptions.subscription_status.get_valid_active_passes_for_user",
            return_value=[access_pass],
        ), self.assertLogs("subscriptions.subscription_status", level="WARNING") as log_ctx:
            status = build_subscription_status(child)

        self.assertTrue(status["has_active_pass"])
        self.assertIsNone(status.get("pass_niveau"))
        self.assertEqual(self._unlocked_level_ids(status), set())
        joined_logs = "\n".join(log_ctx.output)
        self.assertIn(f"pass_id={access_pass.id}", joined_logs)
        self.assertIn(f"payment_intent={payment_intent_id}", joined_logs)

    def test_revoked_gift_pass_does_not_unlock_level(self):
        parent = self._create_user(tag="gift-level-parent-revoked", role="parent")
        child = self._create_user(tag="gift-level-child-revoked")
        plan = self._create_pass_plan(tag="gift-revoked")
        niveau = self._create_niveau(tag="gift-revoked")
        payment_intent_id = "pi_gift_pass_revoked_no_unlock"

        self._create_pass_payment_history(
            owner=parent,
            payment_intent_id=payment_intent_id,
            plan_name=plan.name,
            niveau=niveau,
        )
        self._active_pass(
            user=child,
            plan=plan,
            payment_intent_id=payment_intent_id,
            revoked=True,
        )

        with patch(
            "subscriptions.subscription_status._list_stripe_subscriptions",
            return_value=[],
        ):
            status = build_subscription_status(child)

        self.assertFalse(status["has_active_pass"])
        self.assertIsNone(status.get("pass_niveau"))
        self.assertNotIn(niveau.id, self._unlocked_level_ids(status))
