from __future__ import annotations

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from pays.models import Niveau, Pays
from subscriptions.permissions import (
    has_global_complimentary_access,
    user_has_active_subscription_or_pass,
    user_has_any_manual_access,
)
from subscriptions.subscription_status import build_subscription_status


class ManualComplimentaryLevelAccessTests(TestCase):
    def _create_niveau(self, *, tag: str):
        code_iso = f"X{Pays.objects.count() + 1:02d}"
        pays = Pays.objects.create(
            nom=f"France {tag}",
            code_iso=code_iso,
            ordre=1,
            est_actif=True,
        )
        return Niveau.objects.create(
            nom=f"Terminale {tag}",
            pays=pays,
            ordre=1,
            est_actif=True,
        )

    def _create_user(self, *, tag: str, niveau=None):
        User = get_user_model()
        return User.objects.create_user(
            email=f"{tag}@example.com",
            first_name="Manual",
            last_name="Access",
            password="test-password",
            is_active=True,
            niveau_pays=niveau,
            pays=getattr(niveau, "pays", None),
        )

    def test_manual_access_scoped_to_selected_levels(self):
        level_a = self._create_niveau(tag="scope-a")
        level_b = self._create_niveau(tag="scope-b")
        user = self._create_user(tag="scope-user", niveau=level_a)
        user.complimentary_access_levels.add(level_a)

        self.assertTrue(user_has_any_manual_access(user))
        self.assertFalse(has_global_complimentary_access(user))
        self.assertTrue(user_has_active_subscription_or_pass(user))
        self.assertTrue(user_has_active_subscription_or_pass(user, niveau=level_a))
        self.assertFalse(user_has_active_subscription_or_pass(user, niveau=level_b))

        user.niveau_pays = level_b
        user.pays = level_b.pays
        user.save(update_fields=["niveau_pays", "pays"])
        user.refresh_from_db()
        self.assertFalse(user_has_active_subscription_or_pass(user))

    def test_manual_global_access_keeps_legacy_behavior(self):
        level_a = self._create_niveau(tag="global-a")
        level_b = self._create_niveau(tag="global-b")
        user = self._create_user(tag="global-user", niveau=level_a)
        user.has_complimentary_access = True
        user.save(update_fields=["has_complimentary_access"])

        self.assertTrue(user_has_any_manual_access(user))
        self.assertTrue(has_global_complimentary_access(user))
        self.assertTrue(user_has_active_subscription_or_pass(user))
        self.assertTrue(user_has_active_subscription_or_pass(user, niveau=level_b))

    def test_subscription_status_exposes_scoped_manual_levels(self):
        level_a = self._create_niveau(tag="status-scope-a")
        user = self._create_user(tag="status-scope-user", niveau=level_a)
        user.complimentary_access_levels.add(level_a)

        with patch(
            "subscriptions.subscription_status._list_stripe_subscriptions",
            return_value=[],
        ), patch(
            "subscriptions.subscription_status.get_valid_active_passes_for_user",
            return_value=[],
        ):
            status = build_subscription_status(user)

        self.assertTrue(status["has_manual_access"])
        self.assertFalse(status["has_manual_access_global"])
        self.assertEqual(status["manual_access_scope"], "levels")
        manual_level_ids = {
            level["id"]
            for level in status.get("manual_access_levels", [])
            if isinstance(level, dict) and level.get("id") is not None
        }
        unlocked_level_ids = {
            level["id"]
            for level in status.get("unlocked_levels", [])
            if isinstance(level, dict) and level.get("id") is not None
        }
        self.assertIn(level_a.id, manual_level_ids)
        self.assertIn(level_a.id, unlocked_level_ids)
        self.assertTrue(status["has_access"])

    def test_subscription_status_exposes_global_manual_scope(self):
        level_a = self._create_niveau(tag="status-global-a")
        user = self._create_user(tag="status-global-user", niveau=level_a)
        user.has_complimentary_access = True
        user.save(update_fields=["has_complimentary_access"])

        with patch(
            "subscriptions.subscription_status._list_stripe_subscriptions",
            return_value=[],
        ), patch(
            "subscriptions.subscription_status.get_valid_active_passes_for_user",
            return_value=[],
        ):
            status = build_subscription_status(user)

        self.assertTrue(status["has_manual_access"])
        self.assertTrue(status["has_manual_access_global"])
        self.assertEqual(status["manual_access_scope"], "global")
        self.assertEqual(status.get("manual_access_levels"), [])
        self.assertTrue(status["has_access"])
